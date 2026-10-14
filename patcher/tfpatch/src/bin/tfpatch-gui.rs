#![cfg_attr(all(not(debug_assertions), windows), windows_subsystem = "windows")]
//! Graphical installer: patch language, selectable modules, live final size, automatic ISO / PPSSPP search.
use eframe::egui::{self, Color32, Pos2, Rect, RichText, Stroke, Vec2};
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::sync::{Arc, Mutex};
use tfpatch::apply::{self, Options};
use tfpatch::i18n::{self, ALL, Lang, format_size};
use tfpatch::search;
use tfpatch::texture::{self, Manifest};

const BANNER_PNG: [&[u8]; 5] = [
    include_bytes!("../../assets/banner_en.png"),
    include_bytes!("../../assets/banner_it.png"),
    include_bytes!("../../assets/banner_fr.png"),
    include_bytes!("../../assets/banner_de.png"),
    include_bytes!("../../assets/banner_es.png"),
];

#[derive(Clone)]
enum IsoState {
    NotChosen,
    Checking,
    Ok,
    Invalid,
}

#[derive(Clone)]
enum Job {
    Idle,
    Running { fraction: f32, step: String },
    Done(Vec<PathBuf>),
    Failed(String),
}

#[derive(Clone)]
enum SearchState {
    Idle,
    Running,
    Finished { iso: Option<PathBuf>, ppsspp: Option<PathBuf> },
}

/// State shared between the UI thread and the worker threads.
struct Shared {
    manifest: Option<Result<Arc<Manifest>, String>>,
    iso: IsoState,
    job: Job,
    search: SearchState,
    last_search_result: Option<(Option<PathBuf>, Option<PathBuf>)>, // shown in the advanced options
}

struct App {
    ui_lang: Lang,
    patch_lang: Lang,
    textures: bool,
    text: bool,
    cards: bool,
    strip: bool,
    iso_path: String,
    out_path: String, // computed: output folder + automatic file name
    out_dir: String,  // folder chosen by the user (empty = same folder as the original ISO)
    ppsspp: String,
    shared: Arc<Mutex<Shared>>,
    banner: HashMap<Lang, egui::TextureHandle>,
    source: String,
    // Test hooks, set through TFPATCH_TEST (see `apply_test_env`)
    sim_none: bool,       // the search finds nothing
    sim_no_ppsspp: bool,  // the search does not find PPSSPP
    sim_searching: bool,  // the search never ends
    open_advanced: bool,  // open the advanced options at startup
    auto_search: bool,    // start the search at startup even if an ISO was given
    auto_install: bool,   // check the ISO and start the installation by itself
    started: bool,
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

/// Draws a small flag (simple shapes, no image files needed).
fn draw_flag(ui: &mut egui::Ui, lang: Lang, height: f32) {
    let (rect, _) = ui.allocate_exact_size(Vec2::new(height * 1.5, height), egui::Sense::hover());
    let p = ui.painter_at(rect);
    let rgb = |r: u8, g: u8, b: u8| Color32::from_rgb(r, g, b);
    let vertical_stripes = |colors: [Color32; 3]| {
        let w = rect.width() / 3.0;
        for (i, col) in colors.iter().enumerate() {
            p.rect_filled(Rect::from_min_size(Pos2::new(rect.left() + w * i as f32, rect.top()), Vec2::new(w + 0.5, rect.height())), 0.0, *col);
        }
    };
    let horizontal_stripes = |colors: [Color32; 3], parts: [f32; 3]| {
        let mut y = rect.top();
        for (col, k) in colors.iter().zip(parts) {
            let h = rect.height() * k;
            p.rect_filled(Rect::from_min_size(Pos2::new(rect.left(), y), Vec2::new(rect.width(), h + 0.5)), 0.0, *col);
            y += h;
        }
    };
    match lang {
        Lang::It => vertical_stripes([rgb(0, 146, 70), rgb(255, 255, 255), rgb(206, 43, 55)]),
        Lang::Fr => vertical_stripes([rgb(0, 85, 164), rgb(255, 255, 255), rgb(239, 65, 53)]),
        Lang::De => horizontal_stripes([rgb(0, 0, 0), rgb(221, 0, 0), rgb(255, 206, 0)], [1.0 / 3.0; 3]),
        Lang::Es => horizontal_stripes([rgb(170, 21, 27), rgb(241, 191, 0), rgb(170, 21, 27)], [0.25, 0.5, 0.25]),
        Lang::En => {
            p.rect_filled(rect, 0.0, rgb(1, 33, 105));
            let (a, b, c, d) = (rect.left_top(), rect.right_top(), rect.left_bottom(), rect.right_bottom());
            let t = rect.height();
            p.line_segment([a, d], Stroke::new(t * 0.2, Color32::WHITE));
            p.line_segment([b, c], Stroke::new(t * 0.2, Color32::WHITE));
            p.line_segment([a, d], Stroke::new(t * 0.07, rgb(200, 16, 46)));
            p.line_segment([b, c], Stroke::new(t * 0.07, rgb(200, 16, 46)));
            let m = rect.center();
            p.rect_filled(Rect::from_center_size(m, Vec2::new(rect.width(), t * 0.34)), 0.0, Color32::WHITE);
            p.rect_filled(Rect::from_center_size(m, Vec2::new(t * 0.34, t)), 0.0, Color32::WHITE);
            p.rect_filled(Rect::from_center_size(m, Vec2::new(rect.width(), t * 0.2)), 0.0, rgb(200, 16, 46));
            p.rect_filled(Rect::from_center_size(m, Vec2::new(t * 0.2, t)), 0.0, rgb(200, 16, 46));
        }
    }
    p.rect_stroke(rect, 0.0, Stroke::new(1.0, Color32::from_gray(90)), egui::StrokeKind::Inside);
}

fn language_picker(ui: &mut egui::Ui, id: &str, lang: &mut Lang) {
    ui.horizontal(|ui| {
        draw_flag(ui, *lang, 16.0);
        egui::ComboBox::from_id_salt(id).selected_text(lang.name()).show_ui(ui, |ui| {
            for l in ALL {
                ui.horizontal(|ui| {
                    draw_flag(ui, l, 14.0);
                    ui.selectable_value(lang, l, l.name());
                });
            }
        });
    });
}

impl App {
    fn new(cc: &eframe::CreationContext<'_>) -> Self {
        let ui_lang = Lang::from_system(sys_locale::get_locale());
        let source = std::env::var("TFPATCH_SOURCE").unwrap_or_else(|_| texture::DEFAULT_SOURCE.to_string());
        let shared = Arc::new(Mutex::new(Shared {
            manifest: None,
            iso: IsoState::NotChosen,
            job: Job::Idle,
            search: SearchState::Idle,
            last_search_result: None,
        }));
        {
            let (shared, source, ctx) = (shared.clone(), source.clone(), cc.egui_ctx.clone());
            std::thread::spawn(move || {
                let r = texture::read_manifest(&source).map(Arc::new).map_err(|e| format!("{e:#}"));
                shared.lock().unwrap().manifest = Some(r);
                ctx.request_repaint();
            });
        }
        let mut banner = HashMap::new();
        for (i, l) in ALL.iter().enumerate() {
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
            ppsspp: String::new(),
            shared,
            banner,
            source,
            sim_none: false,
            sim_no_ppsspp: false,
            sim_searching: false,
            open_advanced: false,
            auto_search: false,
            auto_install: false,
            started: false,
        };
        app.apply_test_env();
        if app.iso_path.is_empty() {
            app.start_search(&cc.egui_ctx); // the basic user does nothing: the ISO and the PPSSPP folder are searched automatically
        }
        app
    }

    /// Test hook only: TFPATCH_TEST="ui=fr,patch=de,textures=0,text=1,cards=1,strip=0,iso=...,out=...,ppsspp=...,
    /// auto=1,search=1,adv=1,sim=none|no_ppsspp|searching" sets the initial state.
    fn apply_test_env(&mut self) {
        let Ok(v) = std::env::var("TFPATCH_TEST") else { return };
        let language = |x: &str| ALL.iter().copied().find(|l| l.code() == x);
        for kv in v.split(',') {
            let Some((k, val)) = kv.split_once('=') else { continue };
            match k {
                "ui" => self.ui_lang = language(val).unwrap_or(self.ui_lang),
                "patch" => self.patch_lang = language(val).unwrap_or(self.patch_lang),
                "textures" => self.textures = val == "1",
                "text" => self.text = val == "1",
                "cards" => self.cards = val == "1",
                "strip" => self.strip = val == "1",
                "iso" => self.iso_path = val.to_string(),
                "out" => {
                    self.out_dir = Path::new(val).parent().map(|p| p.display().to_string()).unwrap_or_default();
                }
                "ppsspp" => self.ppsspp = val.to_string(),
                "auto" => self.auto_install = val == "1",
                "search" => self.auto_search = val == "1",
                "adv" => self.open_advanced = val == "1",
                "sim" => {
                    self.sim_none = val == "none";
                    self.sim_no_ppsspp = val == "no_ppsspp";
                    self.sim_searching = val == "searching";
                }
                _ => {}
            }
        }
    }

    fn options(&self) -> Options {
        Options { cards: self.cards, text: self.text, strip: self.strip }
    }

    /// Output folder (the chosen one, otherwise the folder of the ISO) + automatic name <original>_<language>.iso
    fn update_output_path(&mut self) {
        if self.iso_path.is_empty() {
            return;
        }
        let p = Path::new(&self.iso_path);
        let stem = p.file_stem().map(|s| s.to_string_lossy().to_string()).unwrap_or_else(|| "ULES00600".into());
        let dir = if self.out_dir.trim().is_empty() { p.parent().map(|d| d.to_path_buf()).unwrap_or_default() } else { PathBuf::from(&self.out_dir) };
        self.out_path = search::normalize_path(&dir.join(format!("{stem}_{}.iso", self.patch_lang.code())).display().to_string());
    }

    fn check_iso(&mut self, ctx: &egui::Context) {
        let shared = self.shared.clone();
        shared.lock().unwrap().iso = IsoState::Checking;
        let (path, ctx) = (PathBuf::from(&self.iso_path), ctx.clone());
        let md5: Vec<String> = match &shared.lock().unwrap().manifest {
            Some(Ok(m)) => m.iso_md5.clone(),
            _ => vec![],
        };
        std::thread::spawn(move || {
            let expected: Vec<&str> = md5.iter().map(|s| s.as_str()).collect();
            let ok = apply::verify_iso(&path, &expected).unwrap_or(false);
            shared.lock().unwrap().iso = if ok { IsoState::Ok } else { IsoState::Invalid };
            ctx.request_repaint();
        });
    }

    fn start_search(&mut self, ctx: &egui::Context) {
        let shared = self.shared.clone();
        shared.lock().unwrap().search = SearchState::Running;
        if self.sim_searching {
            return;
        }
        let ctx = ctx.clone();
        std::thread::spawn(move || {
            let iso = search::find_iso(std::time::Duration::from_secs(30), 1).into_iter().next();
            let ppsspp = search::find_ppsspp(std::time::Duration::from_secs(15)).into_iter().next();
            shared.lock().unwrap().search = SearchState::Finished { iso, ppsspp };
            ctx.request_repaint();
        });
    }

    fn choose_iso(&mut self, ctx: &egui::Context) {
        if let Some(p) = rfd::FileDialog::new().add_filter("ISO", &["iso", "ISO"]).pick_file() {
            self.iso_path = search::normalize_path(&p.display().to_string());
            self.update_output_path();
            self.check_iso(ctx);
        }
    }

    fn choose_ppsspp(&mut self) {
        if let Some(p) = rfd::FileDialog::new().pick_folder() {
            self.ppsspp = search::normalize_path(&p.display().to_string());
        }
    }

    fn start_install(&mut self, ctx: &egui::Context) {
        self.update_output_path();
        let shared = self.shared.clone();
        let (iso, out, ppsspp) = (
            PathBuf::from(search::normalize_path(&self.iso_path)),
            PathBuf::from(search::normalize_path(&self.out_path)),
            PathBuf::from(search::normalize_path(&self.ppsspp)),
        );
        let (opts, lang, textures_on, source) = (self.options(), self.patch_lang, self.textures, self.source.clone());
        let ctx = ctx.clone();
        let t = i18n::tr(self.ui_lang);
        let steps = [t.step_manifest, t.step_patch, t.step_verify, t.step_iso, t.step_dl, t.step_compose];
        shared.lock().unwrap().job = Job::Running { fraction: 0.0, step: steps[0].to_string() };
        std::thread::spawn(move || {
            let set_progress = |f: f32, s: &str| {
                shared.lock().unwrap().job = Job::Running { fraction: f, step: s.to_string() };
                ctx.request_repaint();
            };
            let result: anyhow::Result<Vec<PathBuf>> = (|| {
                let cache = cache_dir();
                let m = texture::read_manifest(&source)?;
                let code = lang.code();
                let patch_asset = m.patch.get(code).ok_or_else(|| anyhow::anyhow!("patch '{code}' not available"))?;
                set_progress(0.01, steps[1]);
                let patch = texture::download(&source, patch_asset, &cache, &mut |_, _| {})?;
                set_progress(0.02, steps[2]);
                let meta = apply::read_meta(&patch)?;
                let mut expected: Vec<&str> = m.iso_md5.iter().map(|s| s.as_str()).collect();
                expected.push(meta.iso_md5.as_str());
                if !apply::verify_iso(&iso, &expected)? {
                    anyhow::bail!("ISO not recognised");
                }
                if iso == out {
                    anyhow::bail!("the output ISO cannot be the original one");
                }
                let iso_weight = if textures_on { 0.40 } else { 1.0 };
                set_progress(0.10, steps[3]);
                apply::apply(&iso, &patch, &out, &opts, &mut |f, _| set_progress(0.10 + (iso_weight - 0.10) * f, steps[3]))?;
                let mut written = vec![out.clone()];
                if textures_on {
                    let module = m.languages.get(code).ok_or_else(|| anyhow::anyhow!("texture modules '{code}' not available"))?;
                    let total = (m.base.size + module.size).max(1) as f32;
                    let mut done = 0u64;
                    let mut zips = vec![];
                    for a in [&m.base, module] {
                        let done_before = done;
                        zips.push(texture::download(&source, a, &cache, &mut |t, _| {
                            set_progress(0.40 + 0.45 * (done_before + t) as f32 / total, &format!("{} ({})", steps[4], a.file));
                        })?);
                        done += a.size;
                    }
                    let dest = ppsspp.join("PSP").join("TEXTURES").join("ULES00600").join("textures.zip");
                    texture::compose(&zips[0], &zips[1], &dest, &mut |f| set_progress(0.85 + 0.15 * f, steps[5]))?;
                    written.push(dest);
                }
                Ok(written)
            })();
            shared.lock().unwrap().job = match result {
                Ok(f) => Job::Done(f),
                Err(e) => Job::Failed(format!("{e:#}")),
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
        let (manifest, iso_state, job) = {
            let s = self.shared.lock().unwrap();
            (s.manifest.clone(), s.iso.clone(), s.job.clone())
        };
        let busy = matches!(job, Job::Running { .. });
        if self.out_path.is_empty() && !self.iso_path.is_empty() {
            self.update_output_path();
        }
        let search_state = self.shared.lock().unwrap().search.clone();
        if let SearchState::Finished { iso, ppsspp } = search_state.clone() {
            let iso = if self.sim_none { None } else { iso };
            let ppsspp = if self.sim_none || self.sim_no_ppsspp { None } else { ppsspp };
            if let Some(i) = &iso {
                self.iso_path = search::normalize_path(&i.display().to_string());
                self.update_output_path();
                self.check_iso(ctx);
            }
            if let Some(p) = &ppsspp {
                self.ppsspp = search::normalize_path(&p.display().to_string());
            }
            let mut s = self.shared.lock().unwrap();
            s.last_search_result = Some((iso, ppsspp));
            s.search = SearchState::Idle;
        }
        if self.auto_search && matches!(search_state, SearchState::Idle) {
            self.auto_search = false;
            self.start_search(ctx);
        }
        if self.auto_install && matches!(&manifest, Some(Ok(_))) {
            if !self.iso_path.is_empty() && matches!(iso_state, IsoState::NotChosen) {
                self.check_iso(ctx);
            } else if !self.started && matches!(iso_state, IsoState::Ok) {
                self.started = true;
                self.start_install(ctx);
            }
        }
        egui::CentralPanel::default().show(ui_root, |ui| {
            egui::ScrollArea::vertical().show(ui, |ui| {
                ui.add_enabled_ui(!busy, |ui| {
                    // banner of the patch language
                    if let Some(tex) = self.banner.get(&self.patch_lang) {
                        let w = ui.available_width().min(640.0);
                        let h = w * tex.size()[1] as f32 / tex.size()[0] as f32;
                        ui.vertical_centered(|ui| ui.add(egui::Image::new(tex).fit_to_exact_size(Vec2::new(w, h))));
                    }
                    ui.add_space(6.0);
                    ui.vertical_centered(|ui| ui.heading(t.app_title));
                    ui.add_space(6.0);
                    // languages
                    let old_patch_lang = self.patch_lang;
                    ui.horizontal(|ui| {
                        ui.label(t.ui_language);
                        let before = self.ui_lang;
                        language_picker(ui, "ui_lang", &mut self.ui_lang);
                        if before != self.ui_lang && self.patch_lang == before {
                            self.patch_lang = self.ui_lang; // by default the patch follows the program language
                        }
                        ui.add_space(24.0);
                        ui.label(t.patch_language);
                        language_picker(ui, "patch_lang", &mut self.patch_lang);
                    });
                    if old_patch_lang != self.patch_lang {
                        self.update_output_path();
                    }
                    ui.add_space(4.0);
                    ui.separator();
                    let searching = matches!(search_state, SearchState::Running);
                    let green = Color32::from_rgb(60, 170, 80);
                    let orange = Color32::from_rgb(220, 150, 60);
                    let red = Color32::from_rgb(220, 70, 70);
                    // ISO: only the result; the button appears only when it was not found
                    ui.label(RichText::new(t.iso_label).strong());
                    ui.horizontal(|ui| match (&iso_state, searching) {
                        (IsoState::Ok, _) => {
                            ui.label(RichText::new(format!("✔ {}", t.iso_ok)).color(green));
                        }
                        (IsoState::Checking, _) => {
                            ui.spinner();
                            ui.label(t.iso_checking);
                        }
                        (_, true) if self.iso_path.is_empty() => {
                            ui.spinner();
                            ui.label(RichText::new(t.auto_searching).weak());
                        }
                        (state, _) => {
                            let (text, col) = if matches!(state, IsoState::Invalid) { (t.iso_bad, red) } else { (t.auto_no_iso, orange) };
                            ui.label(RichText::new(text).color(col));
                            if ui.button(t.browse).clicked() {
                                self.choose_iso(ctx);
                            }
                        }
                    });
                    // PPSSPP folder (only needed for the HD textures)
                    if self.textures {
                        ui.add_space(4.0);
                        ui.label(RichText::new(t.out_ppsspp).strong());
                        ui.horizontal(|ui| {
                            if !self.ppsspp.trim().is_empty() {
                                ui.label(RichText::new(format!("✔ {}", t.ppsspp_ok)).color(green));
                            } else if searching {
                                ui.spinner();
                                ui.label(RichText::new(t.auto_searching).weak());
                            } else {
                                ui.label(RichText::new(t.auto_no_ppsspp).color(orange));
                                if ui.button(t.browse).clicked() {
                                    self.choose_ppsspp();
                                }
                            }
                        });
                    }
                    ui.separator();
                    // modules
                    ui.label(RichText::new(t.modules).strong());
                    let module = |ui: &mut egui::Ui, v: &mut bool, name: &str, description: &str| {
                        ui.checkbox(v, name);
                        ui.label(RichText::new(description).weak().small());
                        ui.add_space(2.0);
                    };
                    module(ui, &mut self.textures, t.m_textures, t.m_textures_d);
                    module(ui, &mut self.text, t.m_text, t.m_text_d);
                    module(ui, &mut self.cards, t.m_cards, t.m_cards_d);
                    module(ui, &mut self.strip, t.m_strip, t.m_strip_d);
                    ui.separator();
                    // result: sizes in real time
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
                            let iso = m.iso_sizes.get(code).and_then(|s| s.get(&apply::size_key(&self.options()))).copied();
                            let tex = if self.textures { m.languages.get(code).map(|a| a.size + m.base.size) } else { Some(0) };
                            egui::Grid::new("sizes").num_columns(2).spacing([16.0, 4.0]).show(ui, |ui| {
                                ui.label(t.size_iso);
                                ui.label(RichText::new(iso.map(|b| format_size(b, l)).unwrap_or("—".into())).strong().size(18.0));
                                ui.end_row();
                                if self.textures {
                                    ui.label(t.size_tex);
                                    ui.label(tex.map(|b| format_size(b, l)).unwrap_or("—".into()));
                                    ui.end_row();
                                    ui.label(t.size_dl);
                                    let patch = m.patch.get(code).map(|a| a.size).unwrap_or(0);
                                    ui.label(tex.map(|b| format_size(b + patch, l)).unwrap_or("—".into()));
                                    ui.end_row();
                                }
                            });
                        }
                    }
                    ui.separator();
                    egui::CollapsingHeader::new(t.advanced).default_open(self.open_advanced).show(ui, |ui| {
                        if ui.add_enabled(!searching, egui::Button::new(t.auto_btn)).clicked() {
                            self.start_search(ctx);
                        }
                        let last = self.shared.lock().unwrap().last_search_result.clone();
                        if let Some((iso, pp)) = last {
                            if let Some(i) = iso {
                                ui.label(RichText::new(format!("{} {}", t.auto_found_iso, search::normalize_path(&i.display().to_string()))).small());
                            }
                            if let Some(p) = pp {
                                ui.label(RichText::new(format!("{} {}", t.auto_found_ppsspp, search::normalize_path(&p.display().to_string()))).small());
                            }
                        }
                        ui.add_space(4.0);
                        ui.label(RichText::new(t.iso_label).strong());
                        ui.horizontal(|ui| {
                            let r = ui.add(egui::TextEdit::singleline(&mut self.iso_path).desired_width(ui.available_width() - 110.0));
                            if r.changed() {
                                self.iso_path = search::normalize_path(&self.iso_path);
                                if Path::new(&self.iso_path).is_file() {
                                    self.update_output_path();
                                    self.check_iso(ctx);
                                }
                            }
                            if ui.button(t.browse).clicked() {
                                self.choose_iso(ctx);
                            }
                        });
                        ui.add_space(4.0);
                        ui.label(RichText::new(t.out_folder).strong());
                        ui.horizontal(|ui| {
                            let mut shown = if self.out_dir.trim().is_empty() {
                                Path::new(&self.out_path).parent().map(|d| d.display().to_string()).unwrap_or_default()
                            } else {
                                self.out_dir.clone()
                            };
                            if ui.add(egui::TextEdit::singleline(&mut shown).desired_width(ui.available_width() - 110.0)).changed() {
                                self.out_dir = search::normalize_path(&shown);
                                self.update_output_path();
                            }
                            if ui.button(t.browse).clicked()
                                && let Some(p) = rfd::FileDialog::new().pick_folder()
                            {
                                self.out_dir = search::normalize_path(&p.display().to_string());
                                self.update_output_path();
                            }
                        });
                        if !self.out_path.is_empty() {
                            let name = Path::new(&self.out_path).file_name().map(|n| n.to_string_lossy().to_string()).unwrap_or_default();
                            ui.label(RichText::new(format!("{} {}", t.out_name, name)).weak().small());
                        }
                        if self.textures {
                            ui.add_space(4.0);
                            ui.label(RichText::new(t.out_ppsspp).strong());
                            ui.horizontal(|ui| {
                                if ui.add(egui::TextEdit::singleline(&mut self.ppsspp).desired_width(ui.available_width() - 110.0)).changed() {
                                    self.ppsspp = search::normalize_path(&self.ppsspp);
                                }
                                if ui.button(t.browse).clicked() {
                                    self.choose_ppsspp();
                                }
                            });
                            ui.label(RichText::new(search::normalize_path(t.ppsspp_hint)).weak().small());
                        }
                    });
                });
                ui.add_space(10.0);
                // install
                let ready = matches!(iso_state, IsoState::Ok)
                    && !self.out_path.trim().is_empty()
                    && (!self.textures || !self.ppsspp.trim().is_empty())
                    && matches!(&manifest, Some(Ok(_)));
                ui.vertical_centered(|ui| match &job {
                    Job::Running { fraction, step } => {
                        ui.label(t.working);
                        ui.add(egui::ProgressBar::new(*fraction).show_percentage().desired_width(520.0));
                        ui.label(RichText::new(step).weak());
                    }
                    _ => {
                        let b = ui.add_enabled(ready, egui::Button::new(RichText::new(t.install).size(18.0)).min_size(Vec2::new(220.0, 36.0)));
                        if !matches!(iso_state, IsoState::Ok) {
                            ui.label(RichText::new(t.need_iso).weak().small());
                        }
                        if b.clicked() {
                            self.start_install(ctx);
                        }
                    }
                });
                match &job {
                    Job::Done(files) => {
                        ui.add_space(6.0);
                        ui.colored_label(Color32::from_rgb(60, 170, 80), RichText::new(t.done).heading());
                        for p in files {
                            ui.label(search::normalize_path(&p.display().to_string()));
                        }
                    }
                    Job::Failed(e) => {
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
