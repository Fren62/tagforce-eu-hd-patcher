//! Ricerca automatica della ISO europea e della cartella dati di PPSSPP.
use std::collections::{HashSet, VecDeque};
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

/// Dimensioni in byte della ISO ULES00600 v1.01: la copia senza i 2 KB finali di zeri e il dump completo.
pub const DIMENSIONI_ISO: [u64; 2] = [834_893_824, 834_895_872];

/// Cartelle che non vale la pena visitare.
fn da_saltare(nome: &str) -> bool {
    let n = nome.to_ascii_lowercase();
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

/// Radici dei dischi (lettere su Windows, home e punti di mount comuni altrove).
fn dischi() -> Vec<PathBuf> {
    if cfg!(windows) {
        ('A'..='Z').map(|c| PathBuf::from(format!("{c}:\\"))).filter(|p| p.exists()).collect()
    } else {
        ["/mnt", "/media", "/run/media"].iter().map(PathBuf::from).filter(|p| p.exists()).collect()
    }
}

/// Visita in ampiezza (le cartelle piu' vicine alla radice prima) fino a `fine`. `f(percorso, e_cartella, metadati)`.
fn cammina(radici: Vec<(PathBuf, usize)>, fine: Instant, f: &mut dyn FnMut(&Path, bool, &fs::Metadata) -> bool) {
    let mut visti: HashSet<PathBuf> = HashSet::new();
    let mut coda: VecDeque<(PathBuf, usize)> = VecDeque::new();
    for (r, d) in radici {
        if r.is_dir() && visti.insert(r.clone()) {
            coda.push_back((r, d));
        }
    }
    while let Some((dir, prof)) = coda.pop_front() {
        if Instant::now() > fine {
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
            if is_dir && prof > 0 && !da_saltare(&e.file_name().to_string_lossy()) && visti.insert(p.clone()) {
                coda.push_back((p, prof - 1));
            }
        }
    }
}

/// Cerca le ISO con la dimensione giusta (la verifica dell'MD5 la fa chi chiama). Al massimo `max` risultati.
pub fn trova_iso(limite: Duration, max: usize) -> Vec<PathBuf> {
    let fine = Instant::now() + limite;
    let mut radici: Vec<(PathBuf, usize)> = Vec::new();
    if let Some(h) = home() {
        for (sub, d) in [("Downloads", 4), ("Documents", 4), ("Desktop", 3), ("Games", 4), ("OneDrive", 3), ("PPSSPP", 4)] {
            radici.push((h.join(sub), d));
        }
        radici.push((h.clone(), 2));
    }
    for d in dischi() {
        for sub in ["Games", "Roms", "ROMs", "ISO", "PSP", "Emulators", "Giochi", "Download", "Downloads"] {
            radici.push((d.join(sub), 5));
        }
        radici.push((d, 6));
    }
    let mut trovati: Vec<PathBuf> = Vec::new();
    cammina(radici, fine, &mut |p, is_dir, md| {
        if !is_dir
            && p.extension().is_some_and(|e| e.eq_ignore_ascii_case("iso"))
            && DIMENSIONI_ISO.contains(&md.len())
            && !trovati.contains(&p.to_path_buf())
        {
            trovati.push(p.to_path_buf());
        }
        trovati.len() >= max
    });
    trovati
}

/// Una cartella dati di PPSSPP contiene PSP/SAVEDATA, PSP/GAME o PSP/SYSTEM.
fn e_dati_ppsspp(p: &Path) -> bool {
    ["SAVEDATA", "GAME", "SYSTEM"].iter().any(|s| p.join("PSP").join(s).is_dir())
}

/// Cartelle dati di PPSSPP trovate, in ordine di probabilita' (la prima e' quella da usare).
pub fn trova_ppsspp(limite: Duration) -> Vec<PathBuf> {
    let mut v: Vec<PathBuf> = Vec::new();
    let mut aggiungi = |p: PathBuf| {
        if e_dati_ppsspp(&p) && !v.contains(&p) {
            v.push(p);
        }
    };
    if let Some(h) = home() {
        aggiungi(h.join("Documents").join("PPSSPP"));
        aggiungi(h.join("OneDrive").join("Documents").join("PPSSPP"));
        aggiungi(h.join("AppData").join("Roaming").join("PPSSPP"));
        aggiungi(h.join("AppData").join("Local").join("PPSSPP"));
        aggiungi(h.join(".config").join("ppsspp"));
        aggiungi(h.join(".var").join("app").join("org.ppsspp.PPSSPP").join("config").join("ppsspp"));
        aggiungi(h.join("Library").join("Application Support").join("PPSSPP"));
    }
    if !v.is_empty() {
        return v;
    }
    // versione portatile o cartella in un altro disco: cerca una cartella che contenga PSP/SAVEDATA (o GAME/SYSTEM)
    let fine = Instant::now() + limite;
    let mut radici: Vec<(PathBuf, usize)> = Vec::new();
    for d in dischi() {
        radici.push((d, 5));
    }
    if let Some(h) = home() {
        radici.insert(0, (h, 4));
    }
    cammina(radici, fine, &mut |p, is_dir, _| {
        if is_dir && p.file_name().is_some_and(|n| n.eq_ignore_ascii_case("PSP")) {
            if let Some(par) = p.parent() {
                if e_dati_ppsspp(par) && !v.contains(&par.to_path_buf()) {
                    v.push(par.to_path_buf());
                }
            }
        }
        !v.is_empty()
    });
    v
}

/// In Windows usa sempre le barre rovesciate (i percorsi mescolati `/` e `\` sono brutti da vedere).
pub fn normalizza(s: &str) -> String {
    if cfg!(windows) { s.replace('/', "\\") } else { s.to_string() }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn percorsi_normalizzati() {
        if cfg!(windows) {
            assert_eq!(normalizza("F:/a/b\\c.iso"), "F:\\a\\b\\c.iso");
        } else {
            assert_eq!(normalizza("/a/b"), "/a/b");
        }
    }

    #[test]
    #[ignore] // prova manuale: cargo test --release --lib -- --ignored --nocapture
    fn tempo_ricerca() {
        let t = std::time::Instant::now();
        let iso = trova_iso(Duration::from_secs(30), 1);
        println!("ISO {:?} in {:?}", iso, t.elapsed());
        let t = std::time::Instant::now();
        println!("PPSSPP {:?} in {:?}", trova_ppsspp(Duration::from_secs(15)), t.elapsed());
    }

    #[test]
    fn cartelle_da_saltare() {
        assert!(da_saltare("Windows") && da_saltare(".git") && da_saltare("$Recycle.Bin"));
        assert!(!da_saltare("Games"));
    }
}
