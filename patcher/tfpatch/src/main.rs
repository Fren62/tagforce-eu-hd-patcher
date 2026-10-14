use anyhow::{Result, bail};
use clap::Parser;
use std::path::PathBuf;
use tfpatch::{apply, texture};

#[derive(Parser)]
#[command(about = "Patcher per Yu-Gi-Oh! GX Tag Force 1 europeo (ULES00600 v1.01)")]
enum Cmd {
    /// Applica una patch di lingua (.tfp) alla ISO
    Iso(IsoArgs),
    /// Scarica i moduli texture di una lingua e compone textures.zip (o una cartella)
    Textures(texture::Args),
}

#[derive(clap::Args)]
struct IsoArgs {
    /// ISO originale (non viene modificata)
    #[arg(long)]
    iso: PathBuf,
    /// pacchetto di patch della lingua
    #[arg(long)]
    patch: PathBuf,
    /// ISO di uscita (con --dry-run non serve)
    #[arg(long)]
    out: Option<PathBuf>,
    /// non applicare le correzioni alle carte
    #[arg(long)]
    no_cards: bool,
    /// non applicare le correzioni a dialoghi, frasi dei duelli e interfaccia
    #[arg(long)]
    no_text: bool,
    /// tieni le altre lingue nella ISO (e la schermata di scelta lingua)
    #[arg(long)]
    keep_languages: bool,
    /// stampa solo la dimensione finale della ISO
    #[arg(long)]
    dry_run: bool,
}

fn main() -> Result<()> {
    match Cmd::parse() {
        Cmd::Iso(a) => {
            let o = apply::Options { cards: !a.no_cards, text: !a.no_text, strip: !a.keep_languages };
            if a.dry_run {
                println!("{}", apply::dimensione(&a.iso, &a.patch, &o)?);
                return Ok(());
            }
            let Some(out) = a.out else { bail!("manca --out") };
            let meta = apply::leggi_meta(&a.patch)?;
            eprintln!("verifico la ISO...");
            if !apply::verifica_iso(&a.iso, &[meta.iso_md5.as_str()])? {
                bail!("ISO non riconosciuta: serve ULES00600 v1.01 europea");
            }
            eprintln!("applico la patch '{}'...", meta.lingua);
            let mut ultimo = -1i32;
            apply::applica(&a.iso, &a.patch, &out, &o, &mut |f, m| {
                let p = (f * 100.0) as i32;
                if p / 10 != ultimo / 10 {
                    eprintln!("{p:3}% {m}");
                }
                ultimo = p;
            })?;
            eprintln!("fatto: {}", out.display());
            Ok(())
        }
        Cmd::Textures(a) => texture::esegui(a),
    }
}
