#![cfg_attr(all(not(debug_assertions), windows), windows_subsystem = "windows")]
//! Interfaccia grafica del patcher: scelta della lingua della patch, moduli, dimensione finale in tempo reale.
use eframe::egui::{self, Color32, Pos2, Rect, RichText, Stroke, Vec2};
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::sync::{Arc, Mutex};
use tfpatch::apply::{self, Options};
use tfpatch::cerca;
use tfpatch::i18n::{self, Lang, TUTTE, formatta_dimensione};
use tfpatch::texture::{self, Manifest};

const BANNER_PNG: [&[u8]; 5] = [
    include_bytes!("../../assets/banner_en.png"),
    include_bytes!("../../assets/banner_it.png"),
    include_bytes!("../../assets/banner_fr.png"),
    include_bytes!("../../assets/banner_de.png"),
    include_bytes!("../../assets/banner_es.png"),
];

#[derive(Clone)]
enum IsoStato {
    Nessuna,
    Controllo,
    Ok,
    No,
}

#[derive(Clone)]
enum Lavoro {
    Fermo,
    InCorso { frazione: f32, passo: String },
    Fatto(Vec<PathBuf>),
    Errore(String),
}

#[derive(Clone)]
enum Ricerca {
    Ferma,
    InCorso,
    Fine { iso: Option<PathBuf>, ppsspp: Option<PathBuf> },
}

struct Condiviso {
    manifest: Option<Result<Arc<Manifest>, String>>,
    iso: IsoStato,
    lavoro: Lavoro,
    ricerca: Ricerca,
    esito_ricerca: Option<(Option<PathBuf>, Option<PathBuf>)>, // ultimo risultato, da mostrare sotto il tasto
}

struct App {
    ui_lang: Lang,
    patch_lang: Lang,
    textures: bool,
    text: bool,
    cards: bool,
    strip: bool,
    iso_path: String,
    out_path: String, // calcolato: cartella di uscita + nome automatico
    out_dir: String,  // cartella scelta dall'utente (vuota = la stessa della ISO originale)
    sim_nessuna: bool, // solo collaudo: la ricerca non trova nulla
    sim_nopp: bool,    // solo collaudo: la ricerca non trova PPSSPP
    sim_cercando: bool, // solo collaudo: la ricerca non finisce mai
    ppsspp: String,
    sh: Arc<Mutex<Condiviso>>,
    banner: HashMap<Lang, egui::TextureHandle>,
    source: String,
    adv: bool,        // solo collaudo: apre "Opzioni avanzate" all'avvio
    cerca_auto: bool, // solo collaudo: avvia la ricerca automatica all'apertura
    auto: bool,     // solo collaudo: TFPATCH_PROVA=...,auto=1 controlla la ISO e avvia l'installazione da solo
    avviato: bool,
}

fn cache_dir() -> PathBuf {
    if let Ok(d) = std::env::var("LOCALAPPDATA") {
        return PathBuf::from(d).join("tfpatch").join("cache");
    }
    if let Ok(d) = std::env::var("XDG_CACHE_HOME") {
        return PathBuf::from(d).join("tfpatch");
    }
    PathBuf::from(std::env::var("HOME").unwrap_or_default()).join(".cache").join("tfpatch")
}

fn bandiera(ui: &mut egui::Ui, l: Lang, h: f32) {
    let (rect, _) = ui.allocate_exact_size(Vec2::new(h * 1.5, h), egui::Sense::hover());
    let p = ui.painter_at(rect);
    let c = |r: u8, g: u8, b: u8| Color32::from_rgb(r, g, b);
    let strisce_v = |cols: [Color32; 3]| {
        let w = rect.width() / 3.0;
        for (i, col) in cols.iter().enumerate() {
            p.rect_filled(Rect::from_min_size(Pos2::new(rect.left() + w * i as f32, rect.top()), Vec2::new(w + 0.5, rect.height())), 0.0, *col);
        }
    };
    let strisce_o = |cols: [Color32; 3], parti: [f32; 3]| {
        let mut y = rect.top();
        for (col, k) in cols.iter().zip(parti) {
            let hh = rect.height() * k;
            p.rect_filled(Rect::from_min_size(Pos2::new(rect.left(), y), Vec2::new(rect.width(), hh + 0.5)), 0.0, *col);
            y += hh;
        }
    };
    match l {
        Lang::It => strisce_v([c(0, 146, 70), c(255, 255, 255), c(206, 43, 55)]),
        Lang::Fr => strisce_v([c(0, 85, 164), c(255, 255, 255), c(239, 65, 53)]),
        Lang::De => strisce_o([c(0, 0, 0), c(221, 0, 0), c(255, 206, 0)], [1.0 / 3.0; 3]),
        Lang::Es => strisce_o([c(170, 21, 27), c(241, 191, 0), c(170, 21, 27)], [0.25, 0.5, 0.25]),
        Lang::En => {
            p.rect_filled(rect, 0.0, c(1, 33, 105));
            let (a, b, cc, d) = (rect.left_top(), rect.right_top(), rect.left_bottom(), rect.right_bottom());
            let t = rect.height();
            p.line_segment([a, d], Stroke::new(t * 0.2, Color32::WHITE));
            p.line_segment([b, cc], Stroke::new(t * 0.2, Color32::WHITE));
            p.line_segment([a, d], Stroke::new(t * 0.07, c(200, 16, 46)));
            p.line_segment([b, cc], Stroke::new(t * 0.07, c(200, 16, 46)));
            let m = rect.center();
            p.rect_filled(Rect::from_center_size(m, Vec2::new(rect.width(), t * 0.34)), 0.0, Color32::WHITE);
            p.rect_filled(Rect::from_center_size(m, Vec2::new(t * 0.34, t)), 0.0, Color32::WHITE);
            p.rect_filled(Rect::from_center_size(m, Vec2::new(rect.width(), t * 0.2)), 0.0, c(200, 16, 46));
            p.rect_filled(Rect::from_center_size(m, Vec2::new(t * 0.2, t)), 0.0, c(200, 16, 46));
        }
    }
    p.rect_stroke(rect, 0.0, Stroke::new(1.0, Color32::from_gray(90)), egui::StrokeKind::Inside);
}

fn selettore_lingua(ui: &mut egui::Ui, id: &str, lang: &mut Lang) {
    ui.horizontal(|ui| {
        bandiera(ui, *lang, 16.0);
        egui::ComboBox::from_id_salt(id).selected_text(lang.nome()).show_ui(ui, |ui| {
            for l in TUTTE {
                ui.horizontal(|ui| {
                    bandiera(ui, l, 14.0);
                    ui.selectable_value(lang, l, l.nome());
                });
            }
        });
    });
}

impl App {
    fn new(cc: &eframe::CreationContext<'_>) -> Self {
        let ui_lang = Lang::di_sistema(sys_locale::get_locale());
        let source = std::env::var("TFPATCH_SOURCE").unwrap_or_else(|_| texture::SORGENTE.to_string());
        let sh = Arc::new(Mutex::new(Condiviso { manifest: None, iso: IsoStato::Nessuna, lavoro: Lavoro::Fermo, ricerca: Ricerca::Ferma, esito_ricerca: None }));
        {
            let (sh, source, ctx) = (sh.clone(), source.clone(), cc.egui_ctx.clone());
            std::thread::spawn(move || {
                let r = texture::leggi_manifest(&source).map(Arc::new).map_err(|e| format!("{e:#}"));
                sh.lock().unwrap().manifest = Some(r);
                ctx.request_repaint();
            });
        }
        let mut banner = HashMap::new();
        for (i, l) in TUTTE.iter().enumerate() {
            let img = image::load_from_memory(BANNER_PNG[i]).expect("banner").to_rgba8();
            let ci = egui::ColorImage::from_rgba_unmultiplied([img.width() as usize, img.height() as usize], img.as_raw());
            banner.insert(*l, cc.egui_ctx.load_texture(format!("banner_{}", l.code()), ci, egui::TextureOptions::LINEAR));
        }
        let mut app = App {
            ui_lang,
            patch_lang: ui_lang,
            textures: true,
            text: true,
            cards: true,
            strip: true,
            iso_path: String::new(),
            out_path: String::new(),
            out_dir: String::new(),
            sim_nessuna: false,
            sim_nopp: false,
            sim_cercando: false,
            ppsspp: String::new(),
            sh,
            banner,
            source,
            adv: false,
            cerca_auto: false,
            auto: false,
            avviato: false,
        };
        app.prova_da_ambiente();
        if app.iso_path.is_empty() {
            app.cerca(&cc.egui_ctx); // l'utente base non deve fare nulla: ISO e cartella di PPSSPP si cercano da soli
        }
        app
    }

    /// Solo per collaudo: TFPATCH_PROVA="ui=fr,patch=de,textures=0,text=1,cards=1,strip=0" imposta lo stato iniziale.
    fn prova_da_ambiente(&mut self) {
        let Ok(v) = std::env::var("TFPATCH_PROVA") else { return };
        let lingua = |x: &str| TUTTE.iter().copied().find(|l| l.code() == x);
        for kv in v.split(',') {
            let Some((k, val)) = kv.split_once('=') else { continue };
            match k {
                "ui" => self.ui_lang = lingua(val).unwrap_or(self.ui_lang),
                "patch" => self.patch_lang = lingua(val).unwrap_or(self.patch_lang),
                "textures" => self.textures = val == "1",
                "text" => self.text = val == "1",
                "cards" => self.cards = val == "1",
                "strip" => self.strip = val == "1",
                "iso" => self.iso_path = val.to_string(),
                "out" => {
                    self.out_dir = Path::new(val).parent().map(|p| p.display().to_string()).unwrap_or_default();
                }
                "ppsspp" => self.ppsspp = val.to_string(),
                "auto" => self.auto = val == "1",
                "cerca" => self.cerca_auto = val == "1",
                "adv" => self.adv = val == "1",
                "sim" => {
                    self.sim_nessuna = val == "nessuna";
                    self.sim_nopp = val == "nopp";
                    self.sim_cercando = val == "cercando";
                }
                _ => {}
            }
        }
    }

    fn opzioni(&self) -> Options {
        Options { cards: self.cards, text: self.text, strip: self.strip }
    }

    /// Cartella di uscita (quella scelta, altrimenti quella della ISO) + nome automatico <originale>_<lingua>.iso
    fn aggiorna_uscita(&mut self) {
        if self.iso_path.is_empty() {
            return;
        }
        let p = Path::new(&self.iso_path);
        let stem = p.file_stem().map(|s| s.to_string_lossy().to_string()).unwrap_or_else(|| "ULES00600".into());
        let dir = if self.out_dir.trim().is_empty() { p.parent().map(|d| d.to_path_buf()).unwrap_or_default() } else { PathBuf::from(&self.out_dir) };
        self.out_path = cerca::normalizza(&dir.join(format!("{stem}_{}.iso", self.patch_lang.code())).display().to_string());
    }

    fn controlla_iso(&mut self, ctx: &egui::Context) {
        let sh = self.sh.clone();
        sh.lock().unwrap().iso = IsoStato::Controllo;
        let (path, ctx) = (PathBuf::from(&self.iso_path), ctx.clone());
        let md5: Vec<String> = match &sh.lock().unwrap().manifest {
            Some(Ok(m)) => m.iso_md5.clone(),
            _ => vec![],
        };
        std::thread::spawn(move || {
            let attesi: Vec<&str> = md5.iter().map(|s| s.as_str()).collect();
            let ok = apply::verifica_iso(&path, &attesi).unwrap_or(false);
            sh.lock().unwrap().iso = if ok { IsoStato::Ok } else { IsoStato::No };
            ctx.request_repaint();
        });
    }

    fn cerca(&mut self, ctx: &egui::Context) {
        let sh = self.sh.clone();
        sh.lock().unwrap().ricerca = Ricerca::InCorso;
        if self.sim_cercando {
            return;
        }
        let ctx = ctx.clone();
        std::thread::spawn(move || {
            let iso = cerca::trova_iso(std::time::Duration::from_secs(30), 1).into_iter().next();
            let ppsspp = cerca::trova_ppsspp(std::time::Duration::from_secs(15)).into_iter().next();
            sh.lock().unwrap().ricerca = Ricerca::Fine { iso, ppsspp };
            ctx.request_repaint();
        });
    }

    fn scegli_iso(&mut self, ctx: &egui::Context) {
        if let Some(p) = rfd::FileDialog::new().add_filter("ISO", &["iso", "ISO"]).pick_file() {
            self.iso_path = cerca::normalizza(&p.display().to_string());
            self.aggiorna_uscita();
            self.controlla_iso(ctx);
        }
    }

    fn scegli_ppsspp(&mut self) {
        if let Some(p) = rfd::FileDialog::new().pick_folder() {
            self.ppsspp = cerca::normalizza(&p.display().to_string());
        }
    }

    fn avvia(&mut self, ctx: &egui::Context) {
        self.aggiorna_uscita();
        let sh = self.sh.clone();
        let (iso, out, ppsspp) = (
            PathBuf::from(cerca::normalizza(&self.iso_path)),
            PathBuf::from(cerca::normalizza(&self.out_path)),
            PathBuf::from(cerca::normalizza(&self.ppsspp)),
        );
        let (o, lang, texture_on, source) = (self.opzioni(), self.patch_lang, self.textures, self.source.clone());
        let ctx = ctx.clone();
        let t = i18n::tr(self.ui_lang);
        let passi = [t.step_manifest, t.step_patch, t.step_verify, t.step_iso, t.step_dl, t.step_compose];
        sh.lock().unwrap().lavoro = Lavoro::InCorso { frazione: 0.0, passo: passi[0].to_string() };
        std::thread::spawn(move || {
            let imposta = |f: f32, p: &str| {
                sh.lock().unwrap().lavoro = Lavoro::InCorso { frazione: f, passo: p.to_string() };
                ctx.request_repaint();
            };
            let r: anyhow::Result<Vec<PathBuf>> = (|| {
                let cache = cache_dir();
                let m = texture::leggi_manifest(&source)?;
                let code = lang.code();
                let pa = m.patch.get(code).ok_or_else(|| anyhow::anyhow!("patch '{code}' non disponibile"))?;
                imposta(0.01, passi[1]);
                let patch = texture::scarica(&source, pa, &cache, &mut |_, _| {})?;
                imposta(0.02, passi[2]);
                let meta = apply::leggi_meta(&patch)?;
                let mut attesi: Vec<&str> = m.iso_md5.iter().map(|s| s.as_str()).collect();
                attesi.push(meta.iso_md5.as_str());
                if !apply::verifica_iso(&iso, &attesi)? {
                    anyhow::bail!("ISO non riconosciuta");
                }
                if iso == out {
                    anyhow::bail!("l'ISO di uscita non puo' essere quella originale");
                }
                let peso_iso = if texture_on { 0.40 } else { 1.0 };
                imposta(0.10, passi[3]);
                apply::applica(&iso, &patch, &out, &o, &mut |f, _| imposta(0.10 + (peso_iso - 0.10) * f, passi[3]))?;
                let mut fatti = vec![out.clone()];
                if texture_on {
                    let lm = m.lingue.get(code).ok_or_else(|| anyhow::anyhow!("moduli texture '{code}' non disponibili"))?;
                    let tot = (m.base.size + lm.size).max(1) as f32;
                    let mut fatto = 0u64;
                    let mut zips = vec![];
                    for a in [&m.base, lm] {
                        let base_f = fatto;
                        zips.push(texture::scarica(&source, a, &cache, &mut |t, _| {
                            imposta(0.40 + 0.45 * (base_f + t) as f32 / tot, &format!("{} ({})", passi[4], a.file));
                        })?);
                        fatto += a.size;
                    }
                    let dest = ppsspp.join("PSP").join("TEXTURES").join("ULES00600").join("textures.zip");
                    texture::componi(&zips[0], &zips[1], &dest, &mut |f| imposta(0.85 + 0.15 * f, passi[5]))?;
                    fatti.push(dest);
                }
                Ok(fatti)
            })();
            sh.lock().unwrap().lavoro = match r {
                Ok(f) => Lavoro::Fatto(f),
                Err(e) => Lavoro::Errore(format!("{e:#}")),
            };
            ctx.request_repaint();
        });
    }
}

impl eframe::App for App {
    fn ui(&mut self, ui_root: &mut egui::Ui, _frame: &mut eframe::Frame) {
        let ctx = ui_root.ctx().clone();
        let ctx = &ctx;
        let t = i18n::tr(self.ui_lang);
        let (manifest, iso_stato, lavoro) = {
            let s = self.sh.lock().unwrap();
            (s.manifest.clone(), s.iso.clone(), s.lavoro.clone())
        };
        let occupato = matches!(lavoro, Lavoro::InCorso { .. });
        if self.out_path.is_empty() && !self.iso_path.is_empty() {
            self.aggiorna_uscita();
        }
        let ricerca = self.sh.lock().unwrap().ricerca.clone();
        if let Ricerca::Fine { iso, ppsspp } = ricerca.clone() {
            let iso = if self.sim_nessuna { None } else { iso };
            let ppsspp = if self.sim_nessuna || self.sim_nopp { None } else { ppsspp };
            if let Some(i) = &iso {
                self.iso_path = cerca::normalizza(&i.display().to_string());
                self.aggiorna_uscita();
                self.controlla_iso(ctx);
            }
            if let Some(p) = &ppsspp {
                self.ppsspp = cerca::normalizza(&p.display().to_string());
            }
            let mut s = self.sh.lock().unwrap();
            s.esito_ricerca = Some((iso, ppsspp));
            s.ricerca = Ricerca::Ferma;
        }
        if self.cerca_auto && matches!(ricerca, Ricerca::Ferma) {
            self.cerca_auto = false;
            self.cerca(ctx);
        }
        if self.auto && matches!(&manifest, Some(Ok(_))) {
            if !self.iso_path.is_empty() && matches!(iso_stato, IsoStato::Nessuna) {
                self.controlla_iso(ctx);
            } else if !self.avviato && matches!(iso_stato, IsoStato::Ok) {
                self.avviato = true;
                self.avvia(ctx);
            }
        }
        egui::CentralPanel::default().show(ui_root, |ui| {
            egui::ScrollArea::vertical().show(ui, |ui| {
                ui.add_enabled_ui(!occupato, |ui| {
                    // banner della lingua della patch
                    if let Some(tex) = self.banner.get(&self.patch_lang) {
                        let w = ui.available_width().min(640.0);
                        let h = w * tex.size()[1] as f32 / tex.size()[0] as f32;
                        ui.vertical_centered(|ui| ui.add(egui::Image::new(tex).fit_to_exact_size(Vec2::new(w, h))));
                    }
                    ui.add_space(6.0);
                    ui.vertical_centered(|ui| ui.heading(t.app_title));
                    ui.add_space(6.0);
                    // lingue
                    let vecchia = self.patch_lang;
                    ui.horizontal(|ui| {
                        ui.label(t.ui_language);
                        let prima = self.ui_lang;
                        selettore_lingua(ui, "ui_lang", &mut self.ui_lang);
                        if prima != self.ui_lang && self.patch_lang == prima {
                            self.patch_lang = self.ui_lang; // di default la patch segue la lingua del programma
                        }
                        ui.add_space(24.0);
                        ui.label(t.patch_language);
                        selettore_lingua(ui, "patch_lang", &mut self.patch_lang);
                    });
                    if vecchia != self.patch_lang {
                        self.aggiorna_uscita();
                    }
                    ui.add_space(4.0);
                    ui.separator();
                    let cercando = matches!(ricerca, Ricerca::InCorso);
                    let verde = Color32::from_rgb(60, 170, 80);
                    let arancio = Color32::from_rgb(220, 150, 60);
                    let rosso = Color32::from_rgb(220, 70, 70);
                    // ISO: solo il risultato; il pulsante compare solo se non si e' trovata
                    ui.label(RichText::new(t.iso_label).strong());
                    ui.horizontal(|ui| match (&iso_stato, cercando) {
                        (IsoStato::Ok, _) => {
                            ui.label(RichText::new(format!("✔ {}", t.iso_ok)).color(verde));
                        }
                        (IsoStato::Controllo, _) => {
                            ui.spinner();
                            ui.label(t.iso_checking);
                        }
                        (_, true) if self.iso_path.is_empty() => {
                            ui.spinner();
                            ui.label(RichText::new(t.auto_searching).weak());
                        }
                        (stato, _) => {
                            let (testo, col) = if matches!(stato, IsoStato::No) { (t.iso_bad, rosso) } else { (t.auto_no_iso, arancio) };
                            ui.label(RichText::new(testo).color(col));
                            if ui.button(t.browse).clicked() {
                                self.scegli_iso(ctx);
                            }
                        }
                    });
                    // cartella di PPSSPP (serve solo per le texture HD)
                    if self.textures {
                        ui.add_space(4.0);
                        ui.label(RichText::new(t.out_ppsspp).strong());
                        ui.horizontal(|ui| {
                            if !self.ppsspp.trim().is_empty() {
                                ui.label(RichText::new(format!("✔ {}", t.ppsspp_ok)).color(verde));
                            } else if cercando {
                                ui.spinner();
                                ui.label(RichText::new(t.auto_searching).weak());
                            } else {
                                ui.label(RichText::new(t.auto_no_ppsspp).color(arancio));
                                if ui.button(t.browse).clicked() {
                                    self.scegli_ppsspp();
                                }
                            }
                        });
                    }
                    ui.separator();
                    // moduli
                    ui.label(RichText::new(t.modules).strong());
                    let modulo = |ui: &mut egui::Ui, v: &mut bool, nome: &str, desc: &str| {
                        ui.checkbox(v, nome);
                        ui.label(RichText::new(desc).weak().small());
                        ui.add_space(2.0);
                    };
                    modulo(ui, &mut self.textures, t.m_textures, t.m_textures_d);
                    modulo(ui, &mut self.text, t.m_text, t.m_text_d);
                    modulo(ui, &mut self.cards, t.m_cards, t.m_cards_d);
                    modulo(ui, &mut self.strip, t.m_strip, t.m_strip_d);
                    ui.separator();
                    // risultato: dimensioni in tempo reale
                    ui.label(RichText::new(t.result).strong());
                    match &manifest {
                        None => {
                            ui.spinner();
                        }
                        Some(Err(_)) => {
                            ui.colored_label(Color32::from_rgb(220, 70, 70), t.offline);
                        }
                        Some(Ok(m)) => {
                            let code = self.patch_lang.code();
                            let l = self.ui_lang;
                            let iso = m.iso_sizes.get(code).and_then(|s| s.get(&apply::chiave(&self.opzioni()))).copied();
                            let tex = if self.textures { m.lingue.get(code).map(|a| a.size + m.base.size) } else { Some(0) };
                            egui::Grid::new("dimensioni").num_columns(2).spacing([16.0, 4.0]).show(ui, |ui| {
                                ui.label(t.size_iso);
                                ui.label(RichText::new(iso.map(|b| formatta_dimensione(b, l)).unwrap_or("—".into())).strong().size(18.0));
                                ui.end_row();
                                if self.textures {
                                    ui.label(t.size_tex);
                                    ui.label(tex.map(|b| formatta_dimensione(b, l)).unwrap_or("—".into()));
                                    ui.end_row();
                                    ui.label(t.size_dl);
                                    let patch = m.patch.get(code).map(|a| a.size).unwrap_or(0);
                                    ui.label(tex.map(|b| formatta_dimensione(b + patch, l)).unwrap_or("—".into()));
                                    ui.end_row();
                                }
                            });
                        }
                    }
                    ui.separator();
                    egui::CollapsingHeader::new(t.advanced).default_open(self.adv).show(ui, |ui| {
                        if ui.add_enabled(!cercando, egui::Button::new(t.auto_btn)).clicked() {
                            self.cerca(ctx);
                        }
                        let esito = self.sh.lock().unwrap().esito_ricerca.clone();
                        if let Some((iso, pp)) = esito {
                            if let Some(i) = iso {
                                ui.label(RichText::new(format!("{} {}", t.auto_found_iso, cerca::normalizza(&i.display().to_string()))).small());
                            }
                            if let Some(p) = pp {
                                ui.label(RichText::new(format!("{} {}", t.auto_found_ppsspp, cerca::normalizza(&p.display().to_string()))).small());
                            }
                        }
                        ui.add_space(4.0);
                        ui.label(RichText::new(t.iso_label).strong());
                        ui.horizontal(|ui| {
                            let r = ui.add(egui::TextEdit::singleline(&mut self.iso_path).desired_width(ui.available_width() - 110.0));
                            if r.changed() {
                                self.iso_path = cerca::normalizza(&self.iso_path);
                                if Path::new(&self.iso_path).is_file() {
                                    self.aggiorna_uscita();
                                    self.controlla_iso(ctx);
                                }
                            }
                            if ui.button(t.browse).clicked() {
                                self.scegli_iso(ctx);
                            }
                        });
                        ui.add_space(4.0);
                        ui.label(RichText::new(t.out_folder).strong());
                        ui.horizontal(|ui| {
                            let mut mostra = if self.out_dir.trim().is_empty() {
                                Path::new(&self.out_path).parent().map(|d| d.display().to_string()).unwrap_or_default()
                            } else {
                                self.out_dir.clone()
                            };
                            if ui.add(egui::TextEdit::singleline(&mut mostra).desired_width(ui.available_width() - 110.0)).changed() {
                                self.out_dir = cerca::normalizza(&mostra);
                                self.aggiorna_uscita();
                            }
                            if ui.button(t.browse).clicked()
                                && let Some(p) = rfd::FileDialog::new().pick_folder()
                            {
                                self.out_dir = cerca::normalizza(&p.display().to_string());
                                self.aggiorna_uscita();
                            }
                        });
                        if !self.out_path.is_empty() {
                            let nome = Path::new(&self.out_path).file_name().map(|n| n.to_string_lossy().to_string()).unwrap_or_default();
                            ui.label(RichText::new(format!("{} {}", t.out_name, nome)).weak().small());
                        }
                        if self.textures {
                            ui.add_space(4.0);
                            ui.label(RichText::new(t.out_ppsspp).strong());
                            ui.horizontal(|ui| {
                                if ui.add(egui::TextEdit::singleline(&mut self.ppsspp).desired_width(ui.available_width() - 110.0)).changed() {
                                    self.ppsspp = cerca::normalizza(&self.ppsspp);
                                }
                                if ui.button(t.browse).clicked() {
                                    self.scegli_ppsspp();
                                }
                            });
                            ui.label(RichText::new(cerca::normalizza(t.ppsspp_hint)).weak().small());
                        }
                    });
                });
                ui.add_space(10.0);
                // installa
                let pronto = matches!(iso_stato, IsoStato::Ok)
                    && !self.out_path.trim().is_empty()
                    && (!self.textures || !self.ppsspp.trim().is_empty())
                    && matches!(&manifest, Some(Ok(_)));
                ui.vertical_centered(|ui| match &lavoro {
                    Lavoro::InCorso { frazione, passo } => {
                        ui.label(t.working);
                        ui.add(egui::ProgressBar::new(*frazione).show_percentage().desired_width(520.0));
                        ui.label(RichText::new(passo).weak());
                    }
                    _ => {
                        let b = ui.add_enabled(pronto, egui::Button::new(RichText::new(t.install).size(18.0)).min_size(Vec2::new(220.0, 36.0)));
                        if !matches!(iso_stato, IsoStato::Ok) {
                            ui.label(RichText::new(t.need_iso).weak().small());
                        }
                        if b.clicked() {
                            self.avvia(ctx);
                        }
                    }
                });
                match &lavoro {
                    Lavoro::Fatto(f) => {
                        ui.add_space(6.0);
                        ui.colored_label(Color32::from_rgb(60, 170, 80), RichText::new(t.done).heading());
                        for p in f {
                            ui.label(cerca::normalizza(&p.display().to_string()));
                        }
                    }
                    Lavoro::Errore(e) => {
                        ui.add_space(6.0);
                        ui.colored_label(Color32::from_rgb(220, 70, 70), RichText::new(t.failed).strong());
                        ui.label(e);
                    }
                    _ => {}
                }
                ui.add_space(10.0);
                ui.vertical_centered(|ui| ui.label(RichText::new(t.footer).weak().small()));
            });
        });
    }
}

fn main() -> eframe::Result {
    let opts = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default().with_inner_size([720.0, 880.0]).with_min_inner_size([560.0, 520.0]),
        ..Default::default()
    };
    eframe::run_native("tfpatch", opts, Box::new(|cc| Ok(Box::new(App::new(cc)))))
}
