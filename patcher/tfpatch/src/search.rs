//! Automatic search for the European ISO and for the PPSSPP data folder.
use std::collections::{HashSet, VecDeque};
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

/// Sizes in bytes of the ULES00600 v1.01 ISO: the copy without the final 2 KB of zeros and the complete dump.
pub const ISO_SIZES: [u64; 2] = [834_893_824, 834_895_872];

/// Folders that are not worth visiting.
fn should_skip(name: &str) -> bool {
    let n = name.to_ascii_lowercase();
    n.starts_with('.')
        || n.starts_with('$')
        || matches!(
            n.as_str(),
            "windows" | "program files" | "program files (x86)" | "programdata" | "appdata" | "system volume information"
                | "node_modules" | "target" | "library" | "proc" | "sys" | "dev" | "usr" | "bin" | "lib" | "lib64" | "sbin"
                | "etc" | "var" | "snap" | "recovery" | "intel" | "nvidia" | "windowsapps" | "steamapps"
        )
}

fn home() -> Option<PathBuf> {
    std::env::var_os("USERPROFILE").or_else(|| std::env::var_os("HOME")).map(PathBuf::from)
}

/// Roots of the drives (letters on Windows, common mount points elsewhere).
fn drives() -> Vec<PathBuf> {
    if cfg!(windows) {
        ('A'..='Z').map(|c| PathBuf::from(format!("{c}:\\"))).filter(|p| p.exists()).collect()
    } else {
        ["/mnt", "/media", "/run/media"].iter().map(PathBuf::from).filter(|p| p.exists()).collect()
    }
}

/// Breadth-first walk (folders closest to the roots first) until `deadline`.
/// `f(path, is_dir, metadata)` returns true to stop the walk.
fn walk(roots: Vec<(PathBuf, usize)>, deadline: Instant, f: &mut dyn FnMut(&Path, bool, &fs::Metadata) -> bool) {
    let mut seen: HashSet<PathBuf> = HashSet::new();
    let mut queue: VecDeque<(PathBuf, usize)> = VecDeque::new();
    for (r, depth) in roots {
        if r.is_dir() && seen.insert(r.clone()) {
            queue.push_back((r, depth));
        }
    }
    while let Some((dir, depth)) = queue.pop_front() {
        if Instant::now() > deadline {
            return;
        }
        let Ok(rd) = fs::read_dir(&dir) else { continue };
        for e in rd.flatten() {
            let p = e.path();
            let Ok(md) = e.metadata() else { continue };
            let is_dir = md.is_dir();
            if f(&p, is_dir, &md) {
                return;
            }
            if is_dir && depth > 0 && !should_skip(&e.file_name().to_string_lossy()) && seen.insert(p.clone()) {
                queue.push_back((p, depth - 1));
            }
        }
    }
}

/// Looks for ISO files with the right size (the caller verifies the MD5). At most `max` results.
pub fn find_iso(time_limit: Duration, max: usize) -> Vec<PathBuf> {
    let deadline = Instant::now() + time_limit;
    let mut roots: Vec<(PathBuf, usize)> = Vec::new();
    if let Some(h) = home() {
        for (sub, depth) in [("Downloads", 4), ("Documents", 4), ("Desktop", 3), ("Games", 4), ("OneDrive", 3), ("PPSSPP", 4)] {
            roots.push((h.join(sub), depth));
        }
        roots.push((h.clone(), 2));
    }
    for d in drives() {
        // usual folder names, including some localized ones
        for sub in ["Games", "Roms", "ROMs", "ISO", "PSP", "Emulators", "Giochi", "Spiele", "Juegos", "Jeux", "Download", "Downloads"] {
            roots.push((d.join(sub), 5));
        }
        roots.push((d, 6));
    }
    let mut found: Vec<PathBuf> = Vec::new();
    walk(roots, deadline, &mut |p, is_dir, md| {
        if !is_dir
            && p.extension().is_some_and(|e| e.eq_ignore_ascii_case("iso"))
            && ISO_SIZES.contains(&md.len())
            && !found.contains(&p.to_path_buf())
        {
            found.push(p.to_path_buf());
        }
        found.len() >= max
    });
    found
}

/// A PPSSPP data folder contains PSP/SAVEDATA, PSP/GAME or PSP/SYSTEM.
fn is_ppsspp_data(p: &Path) -> bool {
    ["SAVEDATA", "GAME", "SYSTEM"].iter().any(|s| p.join("PSP").join(s).is_dir())
}

/// PPSSPP data folders found, most likely first (the first one is the one to use).
pub fn find_ppsspp(time_limit: Duration) -> Vec<PathBuf> {
    let mut v: Vec<PathBuf> = Vec::new();
    let mut add = |p: PathBuf| {
        if is_ppsspp_data(&p) && !v.contains(&p) {
            v.push(p);
        }
    };
    if let Some(h) = home() {
        add(h.join("Documents").join("PPSSPP"));
        add(h.join("OneDrive").join("Documents").join("PPSSPP"));
        add(h.join("AppData").join("Roaming").join("PPSSPP"));
        add(h.join("AppData").join("Local").join("PPSSPP"));
        add(h.join(".config").join("ppsspp"));
        add(h.join(".var").join("app").join("org.ppsspp.PPSSPP").join("config").join("ppsspp"));
        add(h.join("Library").join("Application Support").join("PPSSPP"));
    }
    if !v.is_empty() {
        return v;
    }
    // portable install or another drive: look for a folder containing PSP/SAVEDATA (or GAME/SYSTEM)
    let deadline = Instant::now() + time_limit;
    let mut roots: Vec<(PathBuf, usize)> = Vec::new();
    for d in drives() {
        roots.push((d, 5));
    }
    if let Some(h) = home() {
        roots.insert(0, (h, 4));
    }
    walk(roots, deadline, &mut |p, is_dir, _| {
        if is_dir && p.file_name().is_some_and(|n| n.eq_ignore_ascii_case("PSP")) {
            if let Some(parent) = p.parent() {
                if is_ppsspp_data(parent) && !v.contains(&parent.to_path_buf()) {
                    v.push(parent.to_path_buf());
                }
            }
        }
        !v.is_empty()
    });
    v
}

/// On Windows always use backslashes (paths mixing `/` and `\` look bad).
pub fn normalize_path(s: &str) -> String {
    if cfg!(windows) { s.replace('/', "\\") } else { s.to_string() }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn normalized_paths() {
        if cfg!(windows) {
            assert_eq!(normalize_path("F:/a/b\\c.iso"), "F:\\a\\b\\c.iso");
        } else {
            assert_eq!(normalize_path("/a/b"), "/a/b");
        }
    }

    #[test]
    #[ignore] // manual timing: cargo test --release --lib -- --ignored --nocapture
    fn search_timing() {
        let t = std::time::Instant::now();
        let iso = find_iso(Duration::from_secs(30), 1);
        println!("ISO {:?} in {:?}", iso, t.elapsed());
        let t = std::time::Instant::now();
        println!("PPSSPP {:?} in {:?}", find_ppsspp(Duration::from_secs(15)), t.elapsed());
    }

    #[test]
    fn skipped_folders() {
        assert!(should_skip("Windows") && should_skip(".git") && should_skip("$Recycle.Bin"));
        assert!(!should_skip("Games"));
    }
}
