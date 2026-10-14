//! Scarica base.zip + <lingua>.zip (manifest.json con SHA-256) e li compone in un unico textures.zip
//! (i file della lingua sovrascrivono quelli del base) oppure li estrae in una cartella.
use anyhow::{Context, Result, bail};
use serde::Deserialize;
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, HashSet};
use std::fs::File;
use std::io::{Read, Write};
use std::path::{Path, PathBuf};

pub const SORGENTE: &str = "https://github.com/Fren62/tagforce-eu-hd-patcher/releases/latest/download";

#[derive(clap::Args)]
pub struct Args {
    /// lingua: it fr de es en
    #[arg(long)]
    lang: String,
    /// output: un file .zip (consigliato, anche per Android) oppure una cartella (PSP/TEXTURES/ULES00600)
    #[arg(long)]
    out: PathBuf,
    /// URL o cartella locale con manifest.json, base.zip e <lingua>.zip
    #[arg(long, default_value = SORGENTE)]
    source: String,
    /// cartella per i download (default: accanto all'output)
    #[arg(long)]
    cache: Option<PathBuf>,
}

#[derive(Deserialize, Clone)]
pub struct Asset {
    pub file: String,
    pub size: u64,
    pub sha256: String,
}

#[derive(Deserialize)]
pub struct Manifest {
    pub base: Asset,
    pub lingue: BTreeMap<String, Asset>,
    /// patch ISO per lingua (patch_<lingua>.tfp)
    #[serde(default)]
    pub patch: BTreeMap<String, Asset>,
    /// dimensione della ISO finale per lingua e combinazione di moduli (chiave "cards,text,strip" = "111")
    #[serde(default)]
    pub iso_sizes: BTreeMap<String, BTreeMap<String, u64>>,
    /// MD5 accettati per la ISO originale
    #[serde(default)]
    pub iso_md5: Vec<String>,
}

fn apri(source: &str, nome: &str) -> Result<Box<dyn Read + Send + Sync>> {
    if source.starts_with("http://") || source.starts_with("https://") {
        let url = format!("{}/{nome}", source.trim_end_matches('/'));
        let r = ureq::get(&url).call().with_context(|| format!("download fallito: {url}"))?;
        Ok(Box::new(r.into_body().into_reader()))
    } else {
        Ok(Box::new(File::open(Path::new(source).join(nome)).with_context(|| format!("manca {nome} in {source}"))?))
    }
}

fn hex(b: impl AsRef<[u8]>) -> String {
    b.as_ref().iter().map(|x| format!("{x:02x}")).collect()
}

fn sha_file(p: &Path) -> Result<String> {
    let mut h = Sha256::new();
    let mut f = File::open(p)?;
    let mut buf = vec![0u8; 1 << 22];
    loop {
        let n = f.read(&mut buf)?;
        if n == 0 {
            break;
        }
        h.update(&buf[..n]);
    }
    Ok(hex(h.finalize()))
}

pub fn leggi_manifest(source: &str) -> Result<Manifest> {
    Ok(serde_json::from_reader(apri(source, "manifest.json")?)?)
}

/// Porta in cache l'archivio (salta il download se c'e' gia' ed e' corretto). `progress(scaricati, totali)`.
pub fn scarica(source: &str, a: &Asset, cache: &Path, progress: &mut dyn FnMut(u64, u64)) -> Result<PathBuf> {
    std::fs::create_dir_all(cache)?;
    let dst = cache.join(&a.file);
    if dst.exists() && std::fs::metadata(&dst)?.len() == a.size && sha_file(&dst)? == a.sha256 {
        progress(a.size, a.size);
        return Ok(dst);
    }
    let tmp = dst.with_extension("part");
    let mut r = apri(source, &a.file)?;
    let mut f = File::create(&tmp)?;
    let mut h = Sha256::new();
    let mut buf = vec![0u8; 1 << 20];
    let mut tot = 0u64;
    loop {
        let n = r.read(&mut buf)?;
        if n == 0 {
            break;
        }
        h.update(&buf[..n]);
        f.write_all(&buf[..n])?;
        tot += n as u64;
        progress(tot, a.size);
    }
    drop(f);
    if hex(h.finalize()) != a.sha256 {
        let _ = std::fs::remove_file(&tmp);
        bail!("{}: SHA-256 errato (download corrotto)", a.file);
    }
    std::fs::rename(&tmp, &dst)?;
    Ok(dst)
}

/// Compone base + modulo in `out` (.zip = un solo archivio non compresso; altrimenti cartella).
pub fn componi(base_zip: &Path, modulo_zip: &Path, out: &Path, progress: &mut dyn FnMut(f32)) -> Result<()> {
    let mut base = zip::ZipArchive::new(File::open(base_zip)?)?;
    let mut modulo = zip::ZipArchive::new(File::open(modulo_zip)?)?;
    if out.extension().is_some_and(|e| e.eq_ignore_ascii_case("zip")) {
        if let Some(p) = out.parent() {
            std::fs::create_dir_all(p)?;
        }
        let sovrascritti: HashSet<String> = modulo.file_names().map(String::from).collect();
        let mut w = zip::ZipWriter::new(File::create(out)?);
        let tot = (base.len() + modulo.len()).max(1);
        for i in 0..base.len() {
            let e = base.by_index_raw(i)?;
            if !sovrascritti.contains(e.name()) {
                w.raw_copy_file(e)?;
            }
            if i % 200 == 0 {
                progress(i as f32 / tot as f32);
            }
        }
        for i in 0..modulo.len() {
            w.raw_copy_file(modulo.by_index_raw(i)?)?;
            if i % 200 == 0 {
                progress((base.len() + i) as f32 / tot as f32);
            }
        }
        w.finish()?;
    } else {
        base.extract(out)?;
        progress(0.7);
        modulo.extract(out)?; // sovrascrive
    }
    progress(1.0);
    Ok(())
}

pub fn esegui(a: Args) -> Result<()> {
    let m = leggi_manifest(&a.source)?;
    let lang = m.lingue.get(&a.lang).with_context(|| format!("lingua '{}' non disponibile (ci sono: {:?})", a.lang, m.lingue.keys()))?;
    let cache = a.cache.clone().unwrap_or_else(|| a.out.parent().map(|p| p.to_path_buf()).unwrap_or_default().join("tfpatch_cache"));
    for asset in [&m.base, lang] {
        eprintln!("scarico {} ({} MB)...", asset.file, asset.size >> 20);
        let mut ultimo = 0u64;
        scarica(&a.source, asset, &cache, &mut |t, tot| {
            if t * 10 / tot.max(1) != ultimo * 10 / tot.max(1) {
                eprintln!("  {}%", t * 100 / tot.max(1));
            }
            ultimo = t;
        })?;
    }
    eprintln!("compongo {}...", a.out.display());
    componi(&cache.join(&m.base.file), &cache.join(&lang.file), &a.out, &mut |_| {})?;
    eprintln!("fatto");
    Ok(())
}
