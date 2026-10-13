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

#[derive(Deserialize)]
struct Asset {
    file: String,
    size: u64,
    sha256: String,
}

#[derive(Deserialize)]
struct Manifest {
    base: Asset,
    lingue: BTreeMap<String, Asset>,
}

fn http(url: &str) -> Result<Box<dyn Read + Send + Sync>> {
    let r = ureq::get(url).call().with_context(|| format!("download fallito: {url}"))?;
    Ok(Box::new(r.into_body().into_reader()))
}

fn apri(source: &str, nome: &str) -> Result<Box<dyn Read + Send + Sync>> {
    if source.starts_with("http://") || source.starts_with("https://") {
        http(&format!("{}/{nome}", source.trim_end_matches('/')))
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

/// Porta in cache l'archivio (salta il download se c'e' gia' ed e' corretto).
fn scarica(source: &str, a: &Asset, cache: &Path) -> Result<PathBuf> {
    let dst = cache.join(&a.file);
    if dst.exists() && std::fs::metadata(&dst)?.len() == a.size && sha_file(&dst)? == a.sha256 {
        eprintln!("{}: gia' scaricato", a.file);
        return Ok(dst);
    }
    eprintln!("scarico {} ({} MB)...", a.file, a.size >> 20);
    let tmp = dst.with_extension("part");
    let mut r = apri(source, &a.file)?;
    let mut f = File::create(&tmp)?;
    let mut h = Sha256::new();
    let mut buf = vec![0u8; 1 << 20];
    loop {
        let n = r.read(&mut buf)?;
        if n == 0 {
            break;
        }
        h.update(&buf[..n]);
        f.write_all(&buf[..n])?;
    }
    drop(f);
    if hex(h.finalize()) != a.sha256 {
        let _ = std::fs::remove_file(&tmp);
        bail!("{}: SHA-256 errato (download corrotto)", a.file);
    }
    std::fs::rename(&tmp, &dst)?;
    Ok(dst)
}

pub fn esegui(a: Args) -> Result<()> {
    let m: Manifest = serde_json::from_reader(apri(&a.source, "manifest.json")?)?;
    let lang = m.lingue.get(&a.lang).with_context(|| format!("lingua '{}' non disponibile (ci sono: {:?})", a.lang, m.lingue.keys()))?;
    let cache = a.cache.clone().unwrap_or_else(|| a.out.parent().map(|p| p.to_path_buf()).unwrap_or_default().join("tfpatch_cache"));
    std::fs::create_dir_all(&cache)?;
    let pb = scarica(&a.source, &m.base, &cache)?;
    let pl = scarica(&a.source, lang, &cache)?;
    let mut base = zip::ZipArchive::new(File::open(pb)?)?;
    let mut modulo = zip::ZipArchive::new(File::open(pl)?)?;

    if a.out.extension().is_some_and(|e| e.eq_ignore_ascii_case("zip")) {
        eprintln!("compongo {}...", a.out.display());
        let sovrascritti: HashSet<String> = modulo.file_names().map(String::from).collect();
        let mut w = zip::ZipWriter::new(File::create(&a.out)?);
        for i in 0..base.len() {
            let e = base.by_index_raw(i)?;
            if !sovrascritti.contains(e.name()) {
                w.raw_copy_file(e)?;
            }
        }
        for i in 0..modulo.len() {
            w.raw_copy_file(modulo.by_index_raw(i)?)?;
        }
        w.finish()?;
    } else {
        eprintln!("estraggo in {}...", a.out.display());
        base.extract(&a.out)?;
        modulo.extract(&a.out)?; // sovrascrive
    }
    eprintln!("fatto");
    Ok(())
}
