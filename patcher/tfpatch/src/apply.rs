//! Applies a modular patch (format 2) to the ISO: module selection, final size computation
//! (without writing anything) and writing of the compact ISO.
use crate::iso;
use anyhow::{Context, Result, bail};
use md5::Md5;
use serde::Deserialize;
use sha2::{Digest, Sha256};
use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{BufWriter, Read, Seek, SeekFrom, Write};
use std::path::Path;

/// MD5 of the complete European ULES00600 v1.01 dump (redump.org); the project's copy lacks the final 2 KB of zeros.
pub const MD5_REDUMP: &str = "719c99478032a4210ae877832061e9fd";

/// Active modules (all true = full installation).
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
    fn active(&self) -> HashSet<&'static str> {
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

/// One operation of the patch: `delta` (bsdiff against the same file of the original ISO), `new` (whole content)
/// or `link` (the path points to the data of another path). `needs` lists the modules that must be active.
#[derive(Deserialize, Clone)]
pub struct Entry {
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

/// Contents of `patch.json`. The JSON keys keep their original (Italian) names: they are part of the file format
/// shared with the released tools, so they must not change.
#[derive(Deserialize)]
pub struct PatchMeta {
    #[serde(rename = "formato")]
    pub format: u32,
    #[serde(rename = "lingua")]
    pub language: String,
    pub iso_md5: String,
    #[serde(rename = "voci")]
    pub entries: Vec<Entry>,
}

pub fn hex(b: impl AsRef<[u8]>) -> String {
    b.as_ref().iter().map(|x| format!("{x:02x}")).collect()
}

pub fn read_meta(patch: &Path) -> Result<PatchMeta> {
    let mut zip = zip::ZipArchive::new(File::open(patch).with_context(|| format!("cannot open patch: {}", patch.display()))?)?;
    let meta: PatchMeta = serde_json::from_reader(zip.by_name("patch.json")?)?;
    if meta.format != 2 {
        bail!("unsupported patch format ({}): a modular patch (format 2) is required", meta.format);
    }
    Ok(meta)
}

/// MD5 of the ISO: (as is, with the final 2 KB of zeros appended).
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
    let as_is = hex(h.clone().finalize());
    h.update([0u8; 2048]);
    Ok((as_is, hex(h.finalize())))
}

/// Checks that the ISO is the European ULES00600 v1.01 (the copy without the final 2 KB of zeros is accepted too).
pub fn verify_iso(path: &Path, expected_md5: &[&str]) -> Result<bool> {
    let (as_is, padded) = md5_iso(path)?;
    Ok(expected_md5.contains(&as_is.as_str()) || expected_md5.contains(&padded.as_str()) || padded == MD5_REDUMP)
}

/// Key of the size table in the manifest: cards, text, strip as digits (e.g. "111").
pub fn size_key(o: &Options) -> String {
    format!("{}{}{}", o.cards as u8, o.text as u8, o.strip as u8)
}

#[derive(Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
enum Data {
    Orig(u32, u32), // extent, size: data that stays where it is in the original ISO
    Mem(usize),     // index into the selected entries: data produced by the patch
}

/// Entries to apply, in order: data first (for each file the one with the most `needs`, all active), then the links.
fn select<'a>(entries: &'a [Entry], o: &Options) -> Vec<&'a Entry> {
    let active = o.active();
    let enabled = |e: &Entry| e.needs.iter().all(|n| active.contains(n.as_str()));
    let mut best: HashMap<&str, &Entry> = HashMap::new();
    let mut order: Vec<&str> = Vec::new();
    for e in entries.iter().filter(|e| e.op != "link" && enabled(e)) {
        match best.get(e.path.as_str()) {
            None => {
                order.push(&e.path);
                best.insert(&e.path, e);
            }
            Some(p) if e.needs.len() > p.needs.len() => {
                best.insert(&e.path, e);
            }
            _ => {}
        }
    }
    let mut out: Vec<&Entry> = order.iter().map(|p| best[p]).collect();
    out.extend(entries.iter().filter(|e| e.op == "link" && enabled(e)));
    out
}

struct Plan {
    state: HashMap<String, Data>,
    unique: Vec<Data>,
}

fn build_plan(src: &iso::Iso, selected: &[&Entry]) -> Result<Plan> {
    let mut state: HashMap<String, Data> = src.files.iter().map(|(p, e)| (p.clone(), Data::Orig(e.extent, e.size))).collect();
    for (i, e) in selected.iter().enumerate() {
        if !state.contains_key(&e.path) {
            bail!("file not present in the ISO: {}", e.path);
        }
        match e.op.as_str() {
            "delta" | "new" => {
                state.insert(e.path.clone(), Data::Mem(i));
            }
            "link" => {
                let t = *state.get(e.target.as_ref().context("missing link target")?).context("link target not in the ISO")?;
                state.insert(e.path.clone(), t);
            }
            o => bail!("unknown operation: {o}"),
        }
    }
    let min_extent = src.files.values().filter(|e| e.size > 0).map(|e| e.extent as u64 * iso::SECTOR).min().unwrap_or(u64::MAX);
    if src.meta_end > min_extent {
        bail!("unexpected ISO layout (directories after file data)");
    }
    let mut unique: Vec<Data> = state.values().copied().filter(|d| !matches!(d, Data::Orig(_, 0))).collect();
    unique.sort();
    unique.dedup();
    Ok(Plan { state, unique })
}

/// Size in bytes of the final ISO with these modules (writes nothing, reads no file data).
pub fn final_size(iso_path: &Path, patch: &Path, o: &Options) -> Result<u64> {
    let meta = read_meta(patch)?;
    let src = iso::Iso::open(File::open(iso_path)?)?;
    let selected = select(&meta.entries, o);
    let plan = build_plan(&src, &selected)?;
    let mut total = src.meta_end;
    for d in &plan.unique {
        let len = match d {
            Data::Orig(_, n) => *n as u64,
            Data::Mem(i) => selected[*i].size.context("missing size")?,
        };
        total += len.next_multiple_of(iso::SECTOR);
    }
    Ok(total)
}

/// Writes the patched ISO. `progress(fraction 0..1, message)`.
pub fn apply(iso_path: &Path, patch: &Path, out: &Path, o: &Options, progress: &mut dyn FnMut(f32, &str)) -> Result<()> {
    let meta = read_meta(patch)?;
    let mut zip = zip::ZipArchive::new(File::open(patch)?)?;
    let mut src = iso::Iso::open(File::open(iso_path)?)?;
    let selected = select(&meta.entries, o);
    let plan = build_plan(&src, &selected)?;

    // 1. new data: deltas applied and checked
    let mut mem: HashMap<usize, Vec<u8>> = HashMap::new();
    let n_data = selected.iter().filter(|e| e.op != "link").count().max(1);
    let mut done = 0;
    for (i, e) in selected.iter().enumerate() {
        if e.op == "link" {
            continue;
        }
        let mut blob = Vec::new();
        zip.by_name(e.blob.as_ref().context("missing blob")?)?.read_to_end(&mut blob)?;
        let new_data = if e.op == "delta" {
            let s = src.files.get(e.src.as_ref().context("missing src")?).copied().context("src not in the ISO")?;
            let orig = src.read_file(&s)?;
            let mut buf = Vec::new();
            qbsdiff::Bspatch::new(&blob)?.apply(&orig, &mut buf)?;
            buf
        } else {
            blob
        };
        if Some(new_data.len() as u64) != e.size || Some(hex(Sha256::digest(&new_data))) != e.sha256 {
            bail!("wrong result for {}", e.path);
        }
        mem.insert(i, new_data);
        done += 1;
        progress(0.3 * done as f32 / n_data as f32, &e.path);
    }

    // 2. compact ISO: header and directories unchanged, then only the data still in use
    let mut out_f = BufWriter::new(File::create(out).with_context(|| format!("cannot create {}", out.display()))?);
    let mut head = vec![0u8; src.meta_end as usize];
    src.f.seek(SeekFrom::Start(0))?;
    src.f.read_exact(&mut head)?;
    out_f.write_all(&head)?;
    let mut sector = (src.meta_end / iso::SECTOR) as u32;
    let mut placed: HashMap<Data, u32> = HashMap::new();
    let n_blocks = plan.unique.len().max(1);
    for (k, d) in plan.unique.iter().enumerate() {
        placed.insert(*d, sector);
        let len = match d {
            Data::Orig(e, n) => {
                src.f.seek(SeekFrom::Start(*e as u64 * iso::SECTOR))?;
                std::io::copy(&mut (&src.f).take(*n as u64), &mut out_f)?;
                *n as u64
            }
            Data::Mem(i) => {
                let m = &mem[i];
                out_f.write_all(m)?;
                m.len() as u64
            }
        };
        let pad = len.next_multiple_of(iso::SECTOR) - len;
        out_f.write_all(&vec![0u8; pad as usize])?;
        sector += len.div_ceil(iso::SECTOR) as u32;
        if k % 16 == 0 {
            progress(0.3 + 0.7 * k as f32 / n_blocks as f32, "ISO");
        }
    }
    let mut out_f = out_f.into_inner().map_err(|e| e.into_error())?;
    for (p, entry) in &src.files {
        let d = plan.state[p];
        let (e, n) = match d {
            Data::Orig(_, 0) => continue,
            Data::Orig(_, n) => (placed[&d], n),
            Data::Mem(i) => (placed[&d], mem[&i].len() as u32),
        };
        iso::set_entry(&mut out_f, entry.rec_off, e, n)?;
    }
    iso::set_volume_size(&mut out_f, sector)?;
    out_f.flush()?;
    progress(1.0, "ISO");
    Ok(())
}
