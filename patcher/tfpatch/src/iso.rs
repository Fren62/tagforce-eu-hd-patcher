//! Minimal ISO9660: reads the directory tree and edits file entries *in place*
//! (extent and size). New data is appended at the end of the image.
use anyhow::{Result, bail};
use std::collections::HashMap;
use std::fs::File;
use std::io::{Read, Seek, SeekFrom, Write};

pub const SECTOR: u64 = 2048;

#[derive(Clone, Copy, Debug)]
pub struct FileEntry {
    pub rec_off: u64, // position of the directory record in the image file
    pub extent: u32,
    pub size: u32,
}

pub struct Iso {
    pub f: File,
    pub files: HashMap<String, FileEntry>, // path (e.g. "/PSP_GAME/USRDIR/x.ehp", without ";1") -> entry
    pub meta_end: u64,                     // first byte after descriptors, path tables and directories (file data excluded)
}

fn le32(b: &[u8], o: usize) -> u32 {
    u32::from_le_bytes(b[o..o + 4].try_into().unwrap())
}

impl Iso {
    pub fn open(mut f: File) -> Result<Self> {
        let mut pvd = vec![0u8; SECTOR as usize];
        f.seek(SeekFrom::Start(16 * SECTOR))?;
        f.read_exact(&mut pvd)?;
        if &pvd[1..6] != b"CD001" || pvd[0] != 1 {
            bail!("not an ISO9660 image (primary volume descriptor missing)");
        }
        let root = &pvd[156..190];
        let mut iso = Iso { f, files: HashMap::new(), meta_end: 17 * SECTOR };
        // path tables (little and big endian, main and optional): size at 132, positions at 140/144 (LE) and 148/152 (BE)
        let table_size = le32(&pvd, 132) as u64;
        for (o, big_endian) in [(140, false), (144, false), (148, true), (152, true)] {
            let lba = if big_endian { u32::from_be_bytes(pvd[o..o + 4].try_into().unwrap()) } else { le32(&pvd, o) } as u64;
            if lba != 0 {
                iso.meta_end = iso.meta_end.max((lba * SECTOR + table_size).next_multiple_of(SECTOR));
            }
        }
        iso.read_dir("", le32(root, 2), le32(root, 10))?;
        Ok(iso)
    }

    fn read_dir(&mut self, prefix: &str, extent: u32, size: u32) -> Result<()> {
        self.meta_end = self.meta_end.max((extent as u64 * SECTOR + size as u64).next_multiple_of(SECTOR));
        let mut buf = vec![0u8; size as usize];
        self.f.seek(SeekFrom::Start(extent as u64 * SECTOR))?;
        self.f.read_exact(&mut buf)?;
        let mut pos = 0usize;
        while pos < buf.len() {
            let len = buf[pos] as usize;
            if len == 0 {
                pos = (pos / SECTOR as usize + 1) * SECTOR as usize; // records never cross a sector boundary
                continue;
            }
            let r = &buf[pos..pos + len];
            let name_len = r[32] as usize;
            let raw_name = &r[33..33 + name_len];
            let is_dir = r[25] & 2 != 0;
            if raw_name != [0u8] && raw_name != [1u8] {
                let mut name = String::from_utf8_lossy(raw_name).to_string();
                if let Some(i) = name.rfind(';') {
                    name.truncate(i);
                }
                let path = format!("{prefix}/{name}");
                let (ext, sz) = (le32(r, 2), le32(r, 10));
                if is_dir {
                    self.read_dir(&path, ext, sz)?;
                } else {
                    let rec_off = extent as u64 * SECTOR + pos as u64;
                    self.files.insert(path, FileEntry { rec_off, extent: ext, size: sz });
                }
            }
            pos += len;
        }
        Ok(())
    }

    pub fn read_file(&mut self, e: &FileEntry) -> Result<Vec<u8>> {
        let mut b = vec![0u8; e.size as usize];
        self.f.seek(SeekFrom::Start(e.extent as u64 * SECTOR))?;
        self.f.read_exact(&mut b)?;
        Ok(b)
    }
}

/// Writes extent and size (little and big endian) into the directory record at `rec_off` of `f`.
pub fn set_entry<W: Write + Seek>(f: &mut W, rec_off: u64, extent: u32, size: u32) -> Result<()> {
    let mut r = [0u8; 16];
    r[0..4].copy_from_slice(&extent.to_le_bytes());
    r[4..8].copy_from_slice(&extent.to_be_bytes());
    r[8..12].copy_from_slice(&size.to_le_bytes());
    r[12..16].copy_from_slice(&size.to_be_bytes());
    f.seek(SeekFrom::Start(rec_off + 2))?;
    f.write_all(&r)?;
    Ok(())
}

/// Writes the volume size (in sectors, little and big endian) into the primary volume descriptor.
pub fn set_volume_size<W: Write + Seek>(f: &mut W, sectors: u32) -> Result<()> {
    let mut r = [0u8; 8];
    r[0..4].copy_from_slice(&sectors.to_le_bytes());
    r[4..8].copy_from_slice(&sectors.to_be_bytes());
    f.seek(SeekFrom::Start(16 * SECTOR + 80))?;
    f.write_all(&r)?;
    Ok(())
}
