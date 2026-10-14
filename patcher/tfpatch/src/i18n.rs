//! Lingue dell'interfaccia: inglese, italiano, francese, tedesco, spagnolo.

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
pub enum Lang {
    En,
    It,
    Fr,
    De,
    Es,
}

pub const TUTTE: [Lang; 5] = [Lang::En, Lang::It, Lang::Fr, Lang::De, Lang::Es];

impl Lang {
    /// codice usato nei nomi dei file (patch_<codice>.tfp, <codice>.zip)
    pub fn code(self) -> &'static str {
        match self {
            Lang::En => "en",
            Lang::It => "it",
            Lang::Fr => "fr",
            Lang::De => "de",
            Lang::Es => "es",
        }
    }

    pub fn nome(self) -> &'static str {
        match self {
            Lang::En => "English",
            Lang::It => "Italiano",
            Lang::Fr => "Français",
            Lang::De => "Deutsch",
            Lang::Es => "Español",
        }
    }

    /// da una stringa di locale ("it-IT", "fr_CA", "de"...)
    pub fn da_locale(loc: &str) -> Option<Lang> {
        let p = loc.split(['-', '_', '.']).next()?.to_ascii_lowercase();
        TUTTE.iter().copied().find(|l| l.code() == p)
    }

    /// lingua del sistema se e' una delle cinque, altrimenti inglese
    pub fn di_sistema(locale: Option<String>) -> Lang {
        locale.as_deref().and_then(Lang::da_locale).unwrap_or(Lang::En)
    }
}

/// Dimensione leggibile, con il separatore decimale della lingua (1,4 GB / 1.4 GB).
pub fn formatta_dimensione(byte: u64, l: Lang) -> String {
    const MB: f64 = 1_048_576.0;
    let mb = byte as f64 / MB;
    let s = if mb >= 1024.0 { format!("{:.2} GB", mb / 1024.0) } else { format!("{:.0} MB", mb) };
    match l {
        Lang::En => s,
        _ => s.replace('.', ","),
    }
}

pub struct Tr {
    pub app_title: &'static str,
    pub ui_language: &'static str,
    pub patch_language: &'static str,
    pub iso_label: &'static str,
    pub browse: &'static str,
    pub iso_none: &'static str,
    pub iso_checking: &'static str,
    pub iso_ok: &'static str,
    pub iso_bad: &'static str,
    pub modules: &'static str,
    pub m_textures: &'static str,
    pub m_textures_d: &'static str,
    pub m_text: &'static str,
    pub m_text_d: &'static str,
    pub m_cards: &'static str,
    pub m_cards_d: &'static str,
    pub m_strip: &'static str,
    pub m_strip_d: &'static str,
    pub result: &'static str,
    pub size_iso: &'static str,
    pub size_tex: &'static str,
    pub size_dl: &'static str,
    pub out_iso: &'static str,
    pub out_ppsspp: &'static str,
    pub ppsspp_hint: &'static str,
    pub install: &'static str,
    pub working: &'static str,
    pub done: &'static str,
    pub failed: &'static str,
    pub step_manifest: &'static str,
    pub step_patch: &'static str,
    pub step_verify: &'static str,
    pub step_iso: &'static str,
    pub step_dl: &'static str,
    pub step_compose: &'static str,
    pub need_iso: &'static str,
    pub need_out: &'static str,
    pub offline: &'static str,
    pub auto_btn: &'static str,
    pub auto_searching: &'static str,
    pub auto_found_iso: &'static str,
    pub auto_found_ppsspp: &'static str,
    pub auto_no_iso: &'static str,
    pub auto_no_ppsspp: &'static str,
    pub out_folder: &'static str,
    pub out_name: &'static str,
    pub advanced: &'static str,
    pub ppsspp_ok: &'static str,
    pub footer: &'static str,
}

const EN: Tr = Tr {
    app_title: "Yu-Gi-Oh! GX Tag Force 1 — EU patcher",
    ui_language: "Program language",
    patch_language: "Patch language",
    iso_label: "Original ISO (ULES00600 v1.01, European)",
    browse: "Browse…",
    iso_none: "Select your ISO file.",
    iso_checking: "Checking the ISO…",
    iso_ok: "ISO recognised.",
    iso_bad: "This is not the European ULES00600 v1.01 ISO.",
    modules: "Modules",
    m_textures: "HD textures",
    m_textures_d: "Cards, interface and banner redrawn in HD for PPSSPP. Saved as a separate textures.zip.",
    m_text: "Dialogue and text corrections",
    m_text_d: "Fixes typos, accents and spacing in dialogues, in-duel lines and interface texts.",
    m_cards: "Card corrections",
    m_cards_d: "Fixes card names and descriptions.",
    m_strip: "Remove the other languages from the game",
    m_strip_d: "Smaller ISO; the game stays in the chosen language and the language selector is removed.",
    result: "Result",
    size_iso: "ISO size",
    size_tex: "HD texture pack (separate file)",
    size_dl: "To download",
    out_iso: "Save the patched ISO as",
    out_ppsspp: "PPSSPP data folder",
    ppsspp_hint: "textures.zip goes to <folder>/PSP/TEXTURES/ULES00600/",
    install: "Install",
    working: "Working…",
    done: "Done!",
    failed: "Something went wrong",
    step_manifest: "Reading the module list…",
    step_patch: "Downloading the patch…",
    step_verify: "Verifying the ISO…",
    step_iso: "Building the ISO…",
    step_dl: "Downloading textures",
    step_compose: "Building textures.zip…",
    need_iso: "Choose a valid ISO first.",
    need_out: "Choose where to save the ISO.",
    offline: "Can't reach the download server. Check your connection.",
    auto_btn: "Find ISO and PPSSPP folder automatically",
    auto_searching: "Searching… (up to 30 seconds)",
    auto_found_iso: "ISO found:",
    auto_found_ppsspp: "PPSSPP folder found:",
    auto_no_iso: "ISO not found: choose it with Browse.",
    auto_no_ppsspp: "PPSSPP folder not found: choose it with Browse.",
    out_folder: "Save the patched ISO in this folder",
    out_name: "It will be named:",
    advanced: "Advanced options",
    ppsspp_ok: "PPSSPP folder found.",
    footer: "Unofficial fan project, not affiliated with Konami. HD textures based on the work of MikeyMK and chrisfand. MIT license.",
};

const IT: Tr = Tr {
    app_title: "Yu-Gi-Oh! GX Tag Force 1 — Patcher europeo",
    ui_language: "Lingua del programma",
    patch_language: "Lingua della patch",
    iso_label: "ISO originale (ULES00600 v1.01, europea)",
    browse: "Sfoglia…",
    iso_none: "Scegli il file della tua ISO.",
    iso_checking: "Controllo della ISO…",
    iso_ok: "ISO riconosciuta.",
    iso_bad: "Questa non è la ISO europea ULES00600 v1.01.",
    modules: "Moduli",
    m_textures: "Texture in HD",
    m_textures_d: "Carte, interfaccia e banner ridisegnati in HD per PPSSPP. Salvate in un textures.zip a parte.",
    m_text: "Correzione di dialoghi e testi",
    m_text_d: "Corregge refusi, accenti e spazi in dialoghi, frasi dei duelli e testi dell'interfaccia.",
    m_cards: "Correzione delle carte",
    m_cards_d: "Corregge nomi e descrizioni delle carte.",
    m_strip: "Rimuovi le altre lingue dal gioco",
    m_strip_d: "ISO più leggera; il gioco resta nella lingua scelta e il selettore della lingua sparisce.",
    result: "Risultato",
    size_iso: "Peso della ISO",
    size_tex: "Pacchetto texture HD (file separato)",
    size_dl: "Da scaricare",
    out_iso: "Salva la ISO patchata come",
    out_ppsspp: "Cartella dati di PPSSPP",
    ppsspp_hint: "textures.zip va in <cartella>/PSP/TEXTURES/ULES00600/",
    install: "Installa",
    working: "Lavoro in corso…",
    done: "Fatto!",
    failed: "Qualcosa è andato storto",
    step_manifest: "Leggo l'elenco dei moduli…",
    step_patch: "Scarico la patch…",
    step_verify: "Verifico la ISO…",
    step_iso: "Creo la ISO…",
    step_dl: "Scarico le texture",
    step_compose: "Creo textures.zip…",
    need_iso: "Scegli prima una ISO valida.",
    need_out: "Scegli dove salvare la ISO.",
    offline: "Non riesco a raggiungere il server dei download. Controlla la connessione.",
    auto_btn: "Cerca ISO e cartella di PPSSPP in automatico",
    auto_searching: "Ricerca in corso… (fino a 30 secondi)",
    auto_found_iso: "ISO trovata:",
    auto_found_ppsspp: "Cartella di PPSSPP trovata:",
    auto_no_iso: "ISO non trovata: sceglila con Sfoglia.",
    auto_no_ppsspp: "Cartella di PPSSPP non trovata: scegliila con Sfoglia.",
    out_folder: "Salva la ISO patchata in questa cartella",
    out_name: "Si chiamerà:",
    advanced: "Opzioni avanzate",
    ppsspp_ok: "Cartella di PPSSPP trovata.",
    footer: "Progetto di appassionati non ufficiale, non affiliato a Konami. Texture HD basate sul lavoro di MikeyMK e chrisfand. Licenza MIT.",
};

const FR: Tr = Tr {
    app_title: "Yu-Gi-Oh! GX Tag Force 1 — Patcheur européen",
    ui_language: "Langue du programme",
    patch_language: "Langue du patch",
    iso_label: "ISO d'origine (ULES00600 v1.01, européenne)",
    browse: "Parcourir…",
    iso_none: "Choisissez votre fichier ISO.",
    iso_checking: "Vérification de l'ISO…",
    iso_ok: "ISO reconnue.",
    iso_bad: "Ce n'est pas l'ISO européenne ULES00600 v1.01.",
    modules: "Modules",
    m_textures: "Textures HD",
    m_textures_d: "Cartes, interface et bannière redessinées en HD pour PPSSPP. Enregistrées dans un textures.zip séparé.",
    m_text: "Correction des dialogues et des textes",
    m_text_d: "Corrige fautes de frappe, accents et espaces dans les dialogues, les phrases des duels et les textes de l'interface.",
    m_cards: "Correction des cartes",
    m_cards_d: "Corrige les noms et les descriptions des cartes.",
    m_strip: "Retirer les autres langues du jeu",
    m_strip_d: "ISO plus légère ; le jeu reste dans la langue choisie et le sélecteur de langue disparaît.",
    result: "Résultat",
    size_iso: "Taille de l'ISO",
    size_tex: "Pack de textures HD (fichier séparé)",
    size_dl: "À télécharger",
    out_iso: "Enregistrer l'ISO patchée sous",
    out_ppsspp: "Dossier de données de PPSSPP",
    ppsspp_hint: "textures.zip ira dans <dossier>/PSP/TEXTURES/ULES00600/",
    install: "Installer",
    working: "Travail en cours…",
    done: "Terminé !",
    failed: "Un problème est survenu",
    step_manifest: "Lecture de la liste des modules…",
    step_patch: "Téléchargement du patch…",
    step_verify: "Vérification de l'ISO…",
    step_iso: "Création de l'ISO…",
    step_dl: "Téléchargement des textures",
    step_compose: "Création de textures.zip…",
    need_iso: "Choisissez d'abord une ISO valide.",
    need_out: "Choisissez où enregistrer l'ISO.",
    offline: "Impossible de joindre le serveur de téléchargement. Vérifiez votre connexion.",
    auto_btn: "Chercher l'ISO et le dossier PPSSPP automatiquement",
    auto_searching: "Recherche en cours… (jusqu'à 30 secondes)",
    auto_found_iso: "ISO trouvée :",
    auto_found_ppsspp: "Dossier PPSSPP trouvé :",
    auto_no_iso: "ISO introuvable : choisissez-la avec Parcourir.",
    auto_no_ppsspp: "Dossier PPSSPP introuvable : choisissez-le avec Parcourir.",
    out_folder: "Enregistrer l'ISO patchée dans ce dossier",
    out_name: "Elle s'appellera :",
    advanced: "Options avancées",
    ppsspp_ok: "Dossier PPSSPP trouvé.",
    footer: "Projet de fans non officiel, non affilié à Konami. Textures HD basées sur le travail de MikeyMK et chrisfand. Licence MIT.",
};

const DE: Tr = Tr {
    app_title: "Yu-Gi-Oh! GX Tag Force 1 — Europäischer Patcher",
    ui_language: "Programmsprache",
    patch_language: "Sprache des Patches",
    iso_label: "Original-ISO (ULES00600 v1.01, europäisch)",
    browse: "Durchsuchen…",
    iso_none: "Wählen Sie Ihre ISO-Datei.",
    iso_checking: "ISO wird geprüft…",
    iso_ok: "ISO erkannt.",
    iso_bad: "Das ist nicht die europäische ISO ULES00600 v1.01.",
    modules: "Module",
    m_textures: "HD-Texturen",
    m_textures_d: "Neu gezeichnete Karten, Oberfläche und Banner für PPSSPP. Wird als separate textures.zip gespeichert.",
    m_text: "Korrektur von Dialogen und Texten",
    m_text_d: "Behebt Tippfehler, Akzente und Leerzeichen in Dialogen, Duellsprüchen und Oberflächentexten.",
    m_cards: "Kartenkorrekturen",
    m_cards_d: "Korrigiert Kartennamen und -beschreibungen.",
    m_strip: "Andere Sprachen aus dem Spiel entfernen",
    m_strip_d: "Kleinere ISO; das Spiel bleibt in der gewählten Sprache und die Sprachauswahl entfällt.",
    result: "Ergebnis",
    size_iso: "Größe der ISO",
    size_tex: "HD-Texturpaket (separate Datei)",
    size_dl: "Herunterzuladen",
    out_iso: "Gepatchte ISO speichern unter",
    out_ppsspp: "PPSSPP-Datenordner",
    ppsspp_hint: "textures.zip kommt nach <Ordner>/PSP/TEXTURES/ULES00600/",
    install: "Installieren",
    working: "Wird bearbeitet…",
    done: "Fertig!",
    failed: "Etwas ist schiefgelaufen",
    step_manifest: "Modulliste wird gelesen…",
    step_patch: "Patch wird heruntergeladen…",
    step_verify: "ISO wird geprüft…",
    step_iso: "ISO wird erstellt…",
    step_dl: "Texturen werden heruntergeladen",
    step_compose: "textures.zip wird erstellt…",
    need_iso: "Wählen Sie zuerst eine gültige ISO.",
    need_out: "Wählen Sie, wo die ISO gespeichert werden soll.",
    offline: "Der Download-Server ist nicht erreichbar. Prüfen Sie Ihre Verbindung.",
    auto_btn: "ISO und PPSSPP-Ordner automatisch suchen",
    auto_searching: "Suche läuft… (bis zu 30 Sekunden)",
    auto_found_iso: "ISO gefunden:",
    auto_found_ppsspp: "PPSSPP-Ordner gefunden:",
    auto_no_iso: "ISO nicht gefunden: mit „Durchsuchen“ auswählen.",
    auto_no_ppsspp: "PPSSPP-Ordner nicht gefunden: mit „Durchsuchen“ auswählen.",
    out_folder: "Gepatchte ISO in diesem Ordner speichern",
    out_name: "Dateiname:",
    advanced: "Erweiterte Optionen",
    ppsspp_ok: "PPSSPP-Ordner gefunden.",
    footer: "Inoffizielles Fanprojekt, nicht mit Konami verbunden. HD-Texturen basieren auf der Arbeit von MikeyMK und chrisfand. MIT-Lizenz.",
};

const ES: Tr = Tr {
    app_title: "Yu-Gi-Oh! GX Tag Force 1 — Parcheador europeo",
    ui_language: "Idioma del programa",
    patch_language: "Idioma del parche",
    iso_label: "ISO original (ULES00600 v1.01, europea)",
    browse: "Examinar…",
    iso_none: "Elige el archivo de tu ISO.",
    iso_checking: "Comprobando la ISO…",
    iso_ok: "ISO reconocida.",
    iso_bad: "Esta no es la ISO europea ULES00600 v1.01.",
    modules: "Módulos",
    m_textures: "Texturas HD",
    m_textures_d: "Cartas, interfaz y banner redibujados en HD para PPSSPP. Se guardan en un textures.zip aparte.",
    m_text: "Corrección de diálogos y textos",
    m_text_d: "Corrige erratas, acentos y espacios en diálogos, frases de los duelos y textos de la interfaz.",
    m_cards: "Corrección de cartas",
    m_cards_d: "Corrige nombres y descripciones de las cartas.",
    m_strip: "Quitar los demás idiomas del juego",
    m_strip_d: "ISO más ligera; el juego se queda en el idioma elegido y desaparece el selector de idioma.",
    result: "Resultado",
    size_iso: "Tamaño de la ISO",
    size_tex: "Pack de texturas HD (archivo aparte)",
    size_dl: "A descargar",
    out_iso: "Guardar la ISO parcheada como",
    out_ppsspp: "Carpeta de datos de PPSSPP",
    ppsspp_hint: "textures.zip irá en <carpeta>/PSP/TEXTURES/ULES00600/",
    install: "Instalar",
    working: "Trabajando…",
    done: "¡Listo!",
    failed: "Algo ha salido mal",
    step_manifest: "Leyendo la lista de módulos…",
    step_patch: "Descargando el parche…",
    step_verify: "Comprobando la ISO…",
    step_iso: "Creando la ISO…",
    step_dl: "Descargando texturas",
    step_compose: "Creando textures.zip…",
    need_iso: "Elige primero una ISO válida.",
    need_out: "Elige dónde guardar la ISO.",
    offline: "No se puede llegar al servidor de descargas. Revisa tu conexión.",
    auto_btn: "Buscar la ISO y la carpeta de PPSSPP automáticamente",
    auto_searching: "Buscando… (hasta 30 segundos)",
    auto_found_iso: "ISO encontrada:",
    auto_found_ppsspp: "Carpeta de PPSSPP encontrada:",
    auto_no_iso: "ISO no encontrada: elígela con Examinar.",
    auto_no_ppsspp: "Carpeta de PPSSPP no encontrada: elígela con Examinar.",
    out_folder: "Guardar la ISO parcheada en esta carpeta",
    out_name: "Se llamará:",
    advanced: "Opciones avanzadas",
    ppsspp_ok: "Carpeta de PPSSPP encontrada.",
    footer: "Proyecto de aficionados no oficial, no afiliado a Konami. Texturas HD basadas en el trabajo de MikeyMK y chrisfand. Licencia MIT.",
};

pub fn tr(l: Lang) -> &'static Tr {
    match l {
        Lang::En => &EN,
        Lang::It => &IT,
        Lang::Fr => &FR,
        Lang::De => &DE,
        Lang::Es => &ES,
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn lingua_di_sistema() {
        assert_eq!(Lang::di_sistema(Some("it-IT".into())), Lang::It);
        assert_eq!(Lang::di_sistema(Some("fr_CA".into())), Lang::Fr);
        assert_eq!(Lang::di_sistema(Some("de".into())), Lang::De);
        assert_eq!(Lang::di_sistema(Some("es-419".into())), Lang::Es);
        assert_eq!(Lang::di_sistema(Some("pt-BR".into())), Lang::En);
        assert_eq!(Lang::di_sistema(None), Lang::En);
    }

    #[test]
    fn dimensioni() {
        assert_eq!(formatta_dimensione(609_267_712, Lang::En), "581 MB");
        assert_eq!(formatta_dimensione(1_493_017_044, Lang::It), "1,39 GB");
        assert_eq!(formatta_dimensione(1_493_017_044, Lang::En), "1.39 GB");
    }
}
