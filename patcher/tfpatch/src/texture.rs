//! Downloads base.zip + <language>.zip (listed in manifest.json with SHA-256) and merges them into a single
//! textures.zip (files of the language module override those of the base) or extracts them into a folder.
use anyhow::{Context, Result, bail};
use serde::Deserialize;
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, HashSet};
use std::fs::File;
use std::io::{Read, Write};
use std::path::{Path, PathBuf};

pub const DEFAULT_SOURCE: &str = "https://github.com/Fren62/tagforce-eu-hd-patcher/releases/latest/download";

#[derive(clap::Args)]
pub struct Args {
    /// language: it fr de es en
    #[arg(long)]
    lang: String,
    /// output: a .zip file (recommended, also works on Android) or a folder (PSP/TEXTURES/ULES00600)
    #[arg(long)]
    out: PathBuf,
    /// URL or local folder containing manifest.json, base.zip and <language>.zip
    #[arg(long, default_value = DEFAULT_SOURCE)]
    source: String,
    /// folder for the downloads (default: next to the output)
    #[arg(long)]
    cache: Option<PathBuf>,
}

#[derive(Deserialize, Clone)]
pub struct Asset {
    pub file: String,
    pub size: u64,
    pub sha256: String,
}

/// Contents of manifest.json.
#[derive(Deserialize)]
pub struct Manifest {
    pub base: Asset,
    pub languages: BTreeMap<String, Asset>,
    /// ISO patches per language (patch_<language>.tfp)
    #[serde(default)]
    pub patch: BTreeMap<String, Asset>,
    /// final ISO size per language and module combination (key "cards,text,strip" as digits, e.g. "111")
    #[serde(default)]
    pub iso_sizes: BTreeMap<String, BTreeMap<String, u64>>,
    /// accepted MD5 values for the original ISO
    #[serde(default)]
    pub iso_md5: Vec<String>,
}

fn open_source(source: &str, name: &str) -> Result<Box<dyn Read + Send + Sync>> {
    if source.starts_with("http://") || source.starts_with("https://") {
        let url = format!("{}/{name}", source.trim_end_matches('/'));
        let r = ureq::get(&url).call().with_context(|| format!("download failed: {url}"))?;
        Ok(Box::new(r.into_body().into_reader()))
    } else {
        Ok(Box::new(File::open(Path::new(source).join(name)).with_context(|| format!("{name} not found in {source}"))?))
    }
}

fn hex(b: impl AsRef<[u8]>) -> String {
    b.as_ref().iter().map(|x| format!("{x:02x}")).collect()
}

fn sha256_file(p: &Path) -> Result<String> {
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

pub fn read_manifest(source: &str) -> Result<Manifest> {
    Ok(serde_json::from_reader(open_source(source, "manifest.json")?)?)
}

/// Brings the archive into the cache (skips the download if it is already there and correct).
/// `progress(downloaded, total)`.
pub fn download(source: &str, a: &Asset, cache: &Path, progress: &mut dyn FnMut(u64, u64)) -> Result<PathBuf> {
    std::fs::create_dir_all(cache)?;
    let dst = cache.join(&a.file);
    if dst.exists() && std::fs::metadata(&dst)?.len() == a.size && sha256_file(&dst)? == a.sha256 {
        progress(a.size, a.size);
        return Ok(dst);
    }
    let tmp = dst.with_extension("part");
    let mut r = open_source(source, &a.file)?;
    let mut f = File::create(&tmp)?;
    let mut h = Sha256::new();
    let mut buf = vec![0u8; 1 << 20];
    let mut total = 0u64;
    loop {
        let n = r.read(&mut buf)?;
        if n == 0 {
            break;
        }
        h.update(&buf[..n]);
        f.write_all(&buf[..n])?;
        total += n as u64;
        progress(total, a.size);
    }
    drop(f);
    if hex(h.finalize()) != a.sha256 {
        let _ = std::fs::remove_file(&tmp);
        bail!("{}: wrong SHA-256 (corrupted download)", a.file);
    }
    std::fs::rename(&tmp, &dst)?;
    Ok(dst)
}

/// Merges base + module into `out` (.zip = one uncompressed archive; anything else = a folder).
pub fn compose(base_zip: &Path, module_zip: &Path, out: &Path, progress: &mut dyn FnMut(f32)) -> Result<()> {
    let mut base = zip::ZipArchive::new(File::open(base_zip)?)?;
    let mut module = zip::ZipArchive::new(File::open(module_zip)?)?;
    if out.extension().is_some_and(|e| e.eq_ignore_ascii_case("zip")) {
        if let Some(p) = out.parent() {
            std::fs::create_dir_all(p)?;
        }
        let overridden: HashSet<String> = module.file_names().map(String::from).collect();
        let mut w = zip::ZipWriter::new(File::create(out)?);
        let total = (base.len() + module.len()).max(1);
        for i in 0..base.len() {
            let e = base.by_index_raw(i)?;
            if !overridden.contains(e.name()) {
                w.raw_copy_file(e)?;
            }
            if i % 200 == 0 {
                progress(i as f32 / total as f32);
            }
        }
        for i in 0..module.len() {
            w.raw_copy_file(module.by_index_raw(i)?)?;
            if i % 200 == 0 {
                progress((base.len() + i) as f32 / total as f32);
            }
        }
        w.finish()?;
    } else {
        base.extract(out)?;
        progress(0.7);
        module.extract(out)?; // overwrites
    }
    progress(1.0);
    Ok(())
}

pub fn run(a: Args) -> Result<()> {
    let m = read_manifest(&a.source)?;
    let lang = m
        .languages
        .get(&a.lang)
        .with_context(|| format!("language '{}' not available (available: {:?})", a.lang, m.languages.keys()))?;
    let cache = a.cache.clone().unwrap_or_else(|| a.out.parent().map(|p| p.to_path_buf()).unwrap_or_default().join("tfpatch_cache"));
    for asset in [&m.base, lang] {
        eprintln!("downloading {} ({} MB)...", asset.file, asset.size >> 20);
        let mut last = 0u64;
        download(&a.source, asset, &cache, &mut |t, total| {
            if t * 10 / total.max(1) != last * 10 / total.max(1) {
                eprintln!("  {}%", t * 100 / total.max(1));
            }
            last = t;
        })?;
    }
    eprintln!("building {}...", a.out.display());
    compose(&cache.join(&m.base.file), &cache.join(&lang.file), &a.out, &mut |_| {})?;
    eprintln!("done");
    Ok(())
}
