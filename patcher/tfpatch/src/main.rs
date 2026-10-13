mod iso;
mod texture;

use anyhow::{Context, Result, bail};
use clap::Parser;
use md5::Md5;
use serde::Deserialize;
use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufWriter, Read, Seek, SeekFrom, Write};
use std::path::PathBuf;

/// MD5 della ISO europea ULES00600 v1.01 completa (redump.org); l'originale del progetto manca dei 2 KB finali di zeri.
const MD5_REDUMP: &str = "719c99478032a4210ae877832061e9fd";

#[derive(Parser)]
#[command(about = "Patcher per Yu-Gi-Oh! GX Tag Force 1 europeo (ULES00600 v1.01)")]
enum Cmd {
    /// Applica una patch di lingua (.tfp) alla ISO
    Iso(Args),
    /// Scarica i moduli texture di una lingua e compone textures.zip (o una cartella)
    Textures(texture::Args),
}

#[derive(clap::Args)]
struct Args {
    /// ISO originale (non viene modificata)
    #[arg(long)]
    iso: PathBuf,
    /// pacchetto di patch della lingua
    #[arg(long)]
    patch: PathBuf,
    /// ISO di uscita
    #[arg(long)]
    out: PathBuf,
}

#[derive(Deserialize)]
struct Meta {
    lingua: String,
    iso_md5: String,
    voci: Vec<VoceP>,
}

#[derive(Deserialize)]
struct VoceP {
    op: String,
    path: String,
    #[serde(default)]
    src: Option<String>,
    #[serde(default)]
    blob: Option<String>,
    #[serde(default)]
    sha256: Option<String>,
    #[serde(default)]
    size: Option<u64>,
    #[serde(default)]
    target: Option<String>,
}

fn hex(b: impl AsRef<[u8]>) -> String {
    b.as_ref().iter().map(|x| format!("{x:02x}")).collect()
}

fn md5_iso(p: &PathBuf) -> Result<(String, String)> {
    let mut h = Md5::new();
    let mut f = File::open(p)?;
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

fn main() -> Result<()> {
    match Cmd::parse() {
        Cmd::Iso(a) => iso_cmd(a),
        Cmd::Textures(a) => texture::esegui(a),
    }
}

fn iso_cmd(a: Args) -> Result<()> {
    let mut zip = zip::ZipArchive::new(File::open(&a.patch).context("patch non apribile")?)?;
    let meta: Meta = serde_json::from_reader(zip.by_name("patch.json")?)?;

    eprintln!("verifico la ISO...");
    let (md5, md5_pad) = md5_iso(&a.iso)?;
    if md5 != meta.iso_md5 && md5_pad != MD5_REDUMP {
        bail!("ISO non riconosciuta (MD5 {md5}): serve ULES00600 v1.01 europea");
    }

    let mut src = iso::Iso::apri(File::open(&a.iso)?)?;

    // 1. piano: per ogni file, da dove vengono i dati (ISO originale oppure memoria)
    #[derive(Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
    enum D {
        Orig(u32, u32), // extent, dimensione
        Mem(usize),
    }
    let mut stato: HashMap<String, D> = src.voci.iter().map(|(p, v)| (p.clone(), D::Orig(v.extent, v.size))).collect();
    let mut mem: Vec<Vec<u8>> = Vec::new();
    eprintln!("applico la patch '{}' ({} voci)...", meta.lingua, meta.voci.len());
    for v in &meta.voci {
        match v.op.as_str() {
            "delta" | "new" => {
                let mut blob = Vec::new();
                zip.by_name(v.blob.as_ref().context("blob mancante")?)?.read_to_end(&mut blob)?;
                let nuovo = if v.op == "delta" {
                    let s = src.voci.get(v.src.as_ref().context("src mancante")?).copied().context("src non nella ISO")?;
                    let orig = src.leggi_file(&s)?;
                    let mut out = Vec::new();
                    qbsdiff::Bspatch::new(&blob)?.apply(&orig, &mut out)?;
                    out
                } else {
                    blob
                };
                if Some(nuovo.len() as u64) != v.size || Some(hex(Sha256::digest(&nuovo))) != v.sha256 {
                    bail!("risultato errato per {}", v.path);
                }
                if !stato.contains_key(&v.path) {
                    bail!("file non presente nella ISO: {}", v.path);
                }
                mem.push(nuovo);
                stato.insert(v.path.clone(), D::Mem(mem.len() - 1));
            }
            "link" => {
                let t = *stato.get(v.target.as_ref().context("target mancante")?).context("target non nella ISO")?;
                if !stato.contains_key(&v.path) {
                    bail!("file non presente nella ISO: {}", v.path);
                }
                stato.insert(v.path.clone(), t);
            }
            o => bail!("operazione sconosciuta: {o}"),
        }
    }

    // 2. nuova ISO compatta: intestazione/directory invariate, poi solo i dati ancora referenziati (i file senza
    //    piu' voci, cioe' le altre lingue, vengono lasciati fuori)
    let min_extent = src.voci.values().filter(|v| v.size > 0).map(|v| v.extent as u64 * iso::SECTOR).min().unwrap_or(u64::MAX);
    if src.meta_fine > min_extent {
        bail!("struttura della ISO non prevista (directory dopo i dati)");
    }
    let mut unici: Vec<D> = stato.values().copied().filter(|d| !matches!(d, D::Orig(_, 0))).collect();
    unici.sort();
    unici.dedup();
    eprintln!("scrivo la ISO ({} blocchi di dati)...", unici.len());
    let mut out = BufWriter::new(File::create(&a.out)?);
    let mut testa = vec![0u8; src.meta_fine as usize];
    src.f.seek(SeekFrom::Start(0))?;
    src.f.read_exact(&mut testa)?;
    out.write_all(&testa)?;
    let mut sett = (src.meta_fine / iso::SECTOR) as u32;
    let mut posto: HashMap<D, u32> = HashMap::new();
    for d in &unici {
        posto.insert(*d, sett);
        let len = match d {
            D::Orig(e, n) => {
                src.f.seek(SeekFrom::Start(*e as u64 * iso::SECTOR))?;
                std::io::copy(&mut (&src.f).take(*n as u64), &mut out)?;
                *n as u64
            }
            D::Mem(i) => {
                out.write_all(&mem[*i])?;
                mem[*i].len() as u64
            }
        };
        let pad = len.next_multiple_of(iso::SECTOR) - len;
        out.write_all(&vec![0u8; pad as usize])?;
        sett += (len.div_ceil(iso::SECTOR)) as u32;
    }
    let mut out = out.into_inner().map_err(|e| e.into_error())?;
    for (p, v) in &src.voci {
        let d = stato[p];
        let (e, n) = match d {
            D::Orig(_, 0) => continue,
            D::Orig(_, n) => (posto[&d], n),
            D::Mem(i) => (posto[&d], mem[i].len() as u32),
        };
        iso::imposta(&mut out, v.rec_off, e, n)?;
    }
    iso::imposta_volume(&mut out, sett)?;
    out.flush()?;
    eprintln!("fatto: {}", a.out.display());
    Ok(())
}
