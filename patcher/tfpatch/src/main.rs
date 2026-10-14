use anyhow::{Result, bail};
use clap::Parser;
use std::path::PathBuf;
use tfpatch::{apply, texture};

#[derive(Parser)]
#[command(about = "Patcher for the European Yu-Gi-Oh! GX Tag Force 1 (ULES00600 v1.01)")]
enum Cmd {
    /// Apply a language patch (.tfp) to the ISO
    Iso(IsoArgs),
    /// Download the texture modules of a language and build textures.zip (or a folder)
    Textures(texture::Args),
}

#[derive(clap::Args)]
struct IsoArgs {
    /// original ISO (it is never modified)
    #[arg(long)]
    iso: PathBuf,
    /// patch package of the language
    #[arg(long)]
    patch: PathBuf,
    /// output ISO (not needed with --dry-run)
    #[arg(long)]
    out: Option<PathBuf>,
    /// do not apply the card corrections
    #[arg(long)]
    no_cards: bool,
    /// do not apply the corrections to dialogues, in-duel lines and interface texts
    #[arg(long)]
    no_text: bool,
    /// keep the other languages in the ISO (and the language selection screen)
    #[arg(long)]
    keep_languages: bool,
    /// only print the final size of the ISO
    #[arg(long)]
    dry_run: bool,
}

fn main() -> Result<()> {
    match Cmd::parse() {
        Cmd::Iso(a) => {
            let o = apply::Options { cards: !a.no_cards, text: !a.no_text, strip: !a.keep_languages };
            if a.dry_run {
                println!("{}", apply::final_size(&a.iso, &a.patch, &o)?);
                return Ok(());
            }
            let Some(out) = a.out else { bail!("--out is missing") };
            let meta = apply::read_meta(&a.patch)?;
            eprintln!("verifying the ISO...");
            if !apply::verify_iso(&a.iso, &[meta.iso_md5.as_str()])? {
                bail!("ISO not recognised: the European ULES00600 v1.01 is required");
            }
            eprintln!("applying the '{}' patch...", meta.language);
            let mut last = -1i32;
            apply::apply(&a.iso, &a.patch, &out, &o, &mut |f, m| {
                let p = (f * 100.0) as i32;
                if p / 10 != last / 10 {
                    eprintln!("{p:3}% {m}");
                }
                last = p;
            })?;
            eprintln!("done: {}", out.display());
            Ok(())
        }
        Cmd::Textures(a) => texture::run(a),
    }
}
