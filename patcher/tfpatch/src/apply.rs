//! Applicazione di una patch modulare (formato 2) alla ISO: selezione dei moduli, calcolo della dimensione finale
//! (senza scrivere nulla) e scrittura della ISO compatta.
use crate::iso;
use anyhow::{Context, Result, bail};
use md5::Md5;
use serde::Deserialize;
use sha2::{Digest, Sha256};
use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{BufWriter, Read, Seek, SeekFrom, Write};
use std::path::Path;

/// MD5 della ISO europea ULES00600 v1.01 completa (redump.org); la copia del progetto manca dei 2 KB finali di zeri.
pub const MD5_REDUMP: &str = "719c99478032a4210ae877832061e9fd";

/// Moduli attivi (tutti veri = installazione completa).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Options {
    pub cards: bool,
    pub text: bool,
    pub strip: bool,
}

impl Default for Options {
    fn default() -> Self {
        Options { cards: true, text: true, strip: true }
    }
}

impl Options {
    fn attivi(&self) -> HashSet<&'static str> {
        let mut s = HashSet::new();
        if self.cards {
            s.insert("cards");
        }
        if self.text {
            s.insert("text");
        }
        if self.strip {
            s.insert("strip");
        }
        s
    }
}

#[derive(Deserialize, Clone)]
pub struct Voce {
    pub op: String,
    pub path: String,
    #[serde(default)]
    pub src: Option<String>,
    #[serde(default)]
    pub blob: Option<String>,
    #[serde(default)]
    pub sha256: Option<String>,
    #[serde(default)]
    pub size: Option<u64>,
    #[serde(default)]
    pub target: Option<String>,
    #[serde(default)]
    pub needs: Vec<String>,
}

#[derive(Deserialize)]
pub struct Meta {
    pub formato: u32,
    pub lingua: String,
    pub iso_md5: String,
    pub voci: Vec<Voce>,
}

pub fn hex(b: impl AsRef<[u8]>) -> String {
    b.as_ref().iter().map(|x| format!("{x:02x}")).collect()
}

pub fn leggi_meta(patch: &Path) -> Result<Meta> {
    let mut zip = zip::ZipArchive::new(File::open(patch).with_context(|| format!("patch non apribile: {}", patch.display()))?)?;
    let meta: Meta = serde_json::from_reader(zip.by_name("patch.json")?)?;
    if meta.formato != 2 {
        bail!("formato di patch non supportato ({}): serve una patch modulare (formato 2)", meta.formato);
    }
    Ok(meta)
}

/// MD5 della ISO: (cosi' com'e', con i 2 KB finali di zeri aggiunti).
pub fn md5_iso(path: &Path) -> Result<(String, String)> {
    let mut h = Md5::new();
    let mut f = File::open(path)?;
    let mut buf = vec![0u8; 1 << 22];
    loop {
        let n = f.read(&mut buf)?;
        if n == 0 {
            break;
        }
        h.update(&buf[..n]);
    }
    let diretto = hex(h.clone().finalize());
    h.update([0u8; 2048]);
    Ok((diretto, hex(h.finalize())))
}

/// Controlla che la ISO sia la ULES00600 v1.01 europea (accetta anche la copia senza i 2 KB finali di zeri).
pub fn verifica_iso(path: &Path, md5_attesi: &[&str]) -> Result<bool> {
    let (diretto, con_zeri) = md5_iso(path)?;
    Ok(md5_attesi.contains(&diretto.as_str()) || md5_attesi.contains(&con_zeri.as_str()) || con_zeri == MD5_REDUMP)
}

/// Chiave della tabella delle dimensioni nel manifest: cards, text, strip come cifre (es. "111").
pub fn chiave(o: &Options) -> String {
    format!("{}{}{}", o.cards as u8, o.text as u8, o.strip as u8)
}

#[derive(Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
enum D {
    Orig(u32, u32), // extent, dimensione
    Mem(usize),     // indice in `scelte`
}

/// Voci da applicare, nell'ordine: prima i dati (per ogni file quella con piu' `needs` tutti attivi), poi i link.
fn scegli<'a>(voci: &'a [Voce], o: &Options) -> Vec<&'a Voce> {
    let attivi = o.attivi();
    let ok = |v: &Voce| v.needs.iter().all(|n| attivi.contains(n.as_str()));
    let mut migliore: HashMap<&str, &Voce> = HashMap::new();
    let mut ordine: Vec<&str> = Vec::new();
    for v in voci.iter().filter(|v| v.op != "link" && ok(v)) {
        match migliore.get(v.path.as_str()) {
            None => {
                ordine.push(&v.path);
                migliore.insert(&v.path, v);
            }
            Some(p) if v.needs.len() > p.needs.len() => {
                migliore.insert(&v.path, v);
            }
            _ => {}
        }
    }
    let mut out: Vec<&Voce> = ordine.iter().map(|p| migliore[p]).collect();
    out.extend(voci.iter().filter(|v| v.op == "link" && ok(v)));
    out
}

struct Piano {
    stato: HashMap<String, D>,
    unici: Vec<D>,
}

fn costruisci(src: &iso::Iso, scelte: &[&Voce]) -> Result<Piano> {
    let mut stato: HashMap<String, D> = src.voci.iter().map(|(p, v)| (p.clone(), D::Orig(v.extent, v.size))).collect();
    for (i, v) in scelte.iter().enumerate() {
        if !stato.contains_key(&v.path) {
            bail!("file non presente nella ISO: {}", v.path);
        }
        match v.op.as_str() {
            "delta" | "new" => {
                stato.insert(v.path.clone(), D::Mem(i));
            }
            "link" => {
                let t = *stato.get(v.target.as_ref().context("target mancante")?).context("target non nella ISO")?;
                stato.insert(v.path.clone(), t);
            }
            o => bail!("operazione sconosciuta: {o}"),
        }
    }
    let min_extent = src.voci.values().filter(|v| v.size > 0).map(|v| v.extent as u64 * iso::SECTOR).min().unwrap_or(u64::MAX);
    if src.meta_fine > min_extent {
        bail!("struttura della ISO non prevista (directory dopo i dati)");
    }
    let mut unici: Vec<D> = stato.values().copied().filter(|d| !matches!(d, D::Orig(_, 0))).collect();
    unici.sort();
    unici.dedup();
    Ok(Piano { stato, unici })
}

/// Dimensione in byte della ISO finale con questi moduli (non scrive nulla, non legge i dati).
pub fn dimensione(iso_path: &Path, patch: &Path, o: &Options) -> Result<u64> {
    let meta = leggi_meta(patch)?;
    let src = iso::Iso::apri(File::open(iso_path)?)?;
    let scelte = scegli(&meta.voci, o);
    let piano = costruisci(&src, &scelte)?;
    let mut tot = src.meta_fine;
    for d in &piano.unici {
        let len = match d {
            D::Orig(_, n) => *n as u64,
            D::Mem(i) => scelte[*i].size.context("size mancante")?,
        };
        tot += len.next_multiple_of(iso::SECTOR);
    }
    Ok(tot)
}

/// Scrive la ISO patchata. `progress(frazione 0..1, messaggio)`.
pub fn applica(iso_path: &Path, patch: &Path, out: &Path, o: &Options, progress: &mut dyn FnMut(f32, &str)) -> Result<()> {
    let meta = leggi_meta(patch)?;
    let mut zip = zip::ZipArchive::new(File::open(patch)?)?;
    let mut src = iso::Iso::apri(File::open(iso_path)?)?;
    let scelte = scegli(&meta.voci, o);
    let piano = costruisci(&src, &scelte)?;

    // 1. dati nuovi: delta applicati e controllati
    let mut mem: HashMap<usize, Vec<u8>> = HashMap::new();
    let n_data = scelte.iter().filter(|v| v.op != "link").count().max(1);
    let mut fatti = 0;
    for (i, v) in scelte.iter().enumerate() {
        if v.op == "link" {
            continue;
        }
        let mut blob = Vec::new();
        zip.by_name(v.blob.as_ref().context("blob mancante")?)?.read_to_end(&mut blob)?;
        let nuovo = if v.op == "delta" {
            let s = src.voci.get(v.src.as_ref().context("src mancante")?).copied().context("src non nella ISO")?;
            let orig = src.leggi_file(&s)?;
            let mut buf = Vec::new();
            qbsdiff::Bspatch::new(&blob)?.apply(&orig, &mut buf)?;
            buf
        } else {
            blob
        };
        if Some(nuovo.len() as u64) != v.size || Some(hex(Sha256::digest(&nuovo))) != v.sha256 {
            bail!("risultato errato per {}", v.path);
        }
        mem.insert(i, nuovo);
        fatti += 1;
        progress(0.3 * fatti as f32 / n_data as f32, &v.path);
    }

    // 2. ISO compatta: intestazione e directory invariate, poi solo i dati ancora usati
    let mut out_f = BufWriter::new(File::create(out).with_context(|| format!("non riesco a creare {}", out.display()))?);
    let mut testa = vec![0u8; src.meta_fine as usize];
    src.f.seek(SeekFrom::Start(0))?;
    src.f.read_exact(&mut testa)?;
    out_f.write_all(&testa)?;
    let mut sett = (src.meta_fine / iso::SECTOR) as u32;
    let mut posto: HashMap<D, u32> = HashMap::new();
    let tot_blocchi = piano.unici.len().max(1);
    for (k, d) in piano.unici.iter().enumerate() {
        posto.insert(*d, sett);
        let len = match d {
            D::Orig(e, n) => {
                src.f.seek(SeekFrom::Start(*e as u64 * iso::SECTOR))?;
                std::io::copy(&mut (&src.f).take(*n as u64), &mut out_f)?;
                *n as u64
            }
            D::Mem(i) => {
                let m = &mem[i];
                out_f.write_all(m)?;
                m.len() as u64
            }
        };
        let pad = len.next_multiple_of(iso::SECTOR) - len;
        out_f.write_all(&vec![0u8; pad as usize])?;
        sett += len.div_ceil(iso::SECTOR) as u32;
        if k % 16 == 0 {
            progress(0.3 + 0.7 * k as f32 / tot_blocchi as f32, "ISO");
        }
    }
    let mut out_f = out_f.into_inner().map_err(|e| e.into_error())?;
    for (p, v) in &src.voci {
        let d = piano.stato[p];
        let (e, n) = match d {
            D::Orig(_, 0) => continue,
            D::Orig(_, n) => (posto[&d], n),
            D::Mem(i) => (posto[&d], mem[&i].len() as u32),
        };
        iso::imposta(&mut out_f, v.rec_off, e, n)?;
    }
    iso::imposta_volume(&mut out_f, sett)?;
    out_f.flush()?;
    progress(1.0, "ISO");
    Ok(())
}
