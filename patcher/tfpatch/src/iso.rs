//! ISO9660 minimale: legge l'albero delle directory e modifica *sul posto* le voci dei file
//! (extent e dimensione). I dati nuovi vengono accodati in fondo alla ISO.
use anyhow::{Result, bail};
use std::collections::HashMap;
use std::fs::File;
use std::io::{Read, Seek, SeekFrom, Write};

pub const SECTOR: u64 = 2048;

#[derive(Clone, Copy, Debug)]
pub struct Voce {
    pub rec_off: u64, // posizione del directory record nel file
    pub extent: u32,
    pub size: u32,
}

pub struct Iso {
    pub f: File,
    pub voci: HashMap<String, Voce>, // percorso (es. "/PSP_GAME/USRDIR/x.ehp", senza ";1") -> voce
    pub meta_fine: u64,              // primo byte dopo descrittori, path table e directory (dati dei file esclusi)
}

fn le32(b: &[u8], o: usize) -> u32 {
    u32::from_le_bytes(b[o..o + 4].try_into().unwrap())
}

impl Iso {
    pub fn apri(mut f: File) -> Result<Self> {
        let mut pvd = vec![0u8; SECTOR as usize];
        f.seek(SeekFrom::Start(16 * SECTOR))?;
        f.read_exact(&mut pvd)?;
        if &pvd[1..6] != b"CD001" || pvd[0] != 1 {
            bail!("non e' una ISO9660 (descrittore primario mancante)");
        }
        let root = &pvd[156..190];
        let mut iso = Iso { f, voci: HashMap::new(), meta_fine: 17 * SECTOR };
        // path table (little e big endian, principale e opzionale): dimensione a 132, posizioni a 140/144 (LE) e 148/152 (BE)
        let tsize = le32(&pvd, 132) as u64;
        for (o, be) in [(140, false), (144, false), (148, true), (152, true)] {
            let lba = if be { u32::from_be_bytes(pvd[o..o + 4].try_into().unwrap()) } else { le32(&pvd, o) } as u64;
            if lba != 0 {
                iso.meta_fine = iso.meta_fine.max((lba * SECTOR + tsize).next_multiple_of(SECTOR));
            }
        }
        iso.leggi_dir("", le32(root, 2), le32(root, 10))?;
        Ok(iso)
    }

    fn leggi_dir(&mut self, prefisso: &str, extent: u32, size: u32) -> Result<()> {
        self.meta_fine = self.meta_fine.max((extent as u64 * SECTOR + size as u64).next_multiple_of(SECTOR));
        let mut buf = vec![0u8; size as usize];
        self.f.seek(SeekFrom::Start(extent as u64 * SECTOR))?;
        self.f.read_exact(&mut buf)?;
        let mut pos = 0usize;
        while pos < buf.len() {
            let len = buf[pos] as usize;
            if len == 0 {
                pos = (pos / SECTOR as usize + 1) * SECTOR as usize; // i record non attraversano i settori
                continue;
            }
            let r = &buf[pos..pos + len];
            let nlen = r[32] as usize;
            let nome = &r[33..33 + nlen];
            let is_dir = r[25] & 2 != 0;
            if nome != [0u8] && nome != [1u8] {
                let mut n = String::from_utf8_lossy(nome).to_string();
                if let Some(i) = n.rfind(';') {
                    n.truncate(i);
                }
                let path = format!("{prefisso}/{n}");
                let (ext, sz) = (le32(r, 2), le32(r, 10));
                if is_dir {
                    self.leggi_dir(&path, ext, sz)?;
                } else {
                    let rec_off = extent as u64 * SECTOR + pos as u64;
                    self.voci.insert(path, Voce { rec_off, extent: ext, size: sz });
                }
            }
            pos += len;
        }
        Ok(())
    }

    pub fn leggi_file(&mut self, v: &Voce) -> Result<Vec<u8>> {
        let mut b = vec![0u8; v.size as usize];
        self.f.seek(SeekFrom::Start(v.extent as u64 * SECTOR))?;
        self.f.read_exact(&mut b)?;
        Ok(b)
    }

}

/// Scrive extent e dimensione (little e big endian) nel directory record, alla posizione `rec_off` di `f`.
pub fn imposta<W: Write + Seek>(f: &mut W, rec_off: u64, extent: u32, size: u32) -> Result<()> {
    let mut r = [0u8; 16];
    r[0..4].copy_from_slice(&extent.to_le_bytes());
    r[4..8].copy_from_slice(&extent.to_be_bytes());
    r[8..12].copy_from_slice(&size.to_le_bytes());
    r[12..16].copy_from_slice(&size.to_be_bytes());
    f.seek(SeekFrom::Start(rec_off + 2))?;
    f.write_all(&r)?;
    Ok(())
}

pub fn imposta_volume<W: Write + Seek>(f: &mut W, settori: u32) -> Result<()> {
    let mut r = [0u8; 8];
    r[0..4].copy_from_slice(&settori.to_le_bytes());
    r[4..8].copy_from_slice(&settori.to_be_bytes());
    f.seek(SeekFrom::Start(16 * SECTOR + 80))?;
    f.write_all(&r)?;
    Ok(())
}
