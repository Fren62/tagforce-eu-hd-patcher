# Yu-Gi-Oh! GX Tag Force 1 — Patcheur européen (HD + textes corrigés)

[English](README.md) · [Italiano](README.it.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md)

Patcheur gratuit et open source pour **Yu-Gi-Oh! GX Tag Force** (PSP), version européenne **ULES00600 v1.01**.
À partir de *votre propre* ISO, il produit une copie dans la langue choisie (**anglais, français, allemand, espagnol, italien**), avec les parties que vous sélectionnez :

- **textures HD** pour PPSSPP : cartes grandes et petites dont le texte est redessiné dans votre langue, textes de l'interface, bannière du titre ;
- **correction des dialogues et des textes** : fautes de frappe, accents, espaces et restes d'autres langues dans les dialogues, les phrases des duels et les textes de l'interface ;
- **correction des cartes** : noms et descriptions des cartes ;
- **suppression des autres langues** : ISO plus légère, le jeu reste dans la langue choisie quelle que soit la langue système de la PSP, et le sélecteur de langue (écran du premier démarrage et entrée du menu principal) disparaît car il serait inutile.

> **État : première version.** Les patchs sont vérifiés fichier par fichier pour chaque combinaison de modules, et les cinq langues ont été testées dans PPSSPP (démarrage, écran titre, duels de démonstration). Le mode histoire, l'éditeur de deck et la boutique n'ont pas encore été joués à fond. L'installateur graphique est nouveau : testé sous Windows ; la version Linux est produite par GitHub Actions et n'a pas encore été lancée sur un vrai bureau Linux.

## Ce qu'il vous faut

- Votre propre ISO **ULES00600 v1.01** (européenne). MD5 du dump complet : `719c99478032a4210ae877832061e9fd` ([redump.org](http://redump.org/)). Les copies sans les 2 derniers Ko de zéros sont aussi acceptées.
- [PPSSPP](https://www.ppsspp.org/) avec **Remplacer les textures** activé ; résolution de rendu 4x recommandée.

Ce dépôt **ne contient pas** le jeu ni de données extraites du jeu : les patchs (`.tfp`) ne contiennent que des différences binaires par rapport aux fichiers d'origine.

## Installateur graphique (recommandé)

1. Téléchargez depuis la page [Releases](../../releases) `tfpatch-gui.exe` (Windows) ou `tfpatch-gui-linux-x86_64` (Linux ; lancez d'abord `chmod +x tfpatch-gui-linux-x86_64`).
2. Lancez-le. Le programme s'ouvre dans la langue de votre PC (anglais si ce n'en est pas une des cinq) et affiche la bannière *Tomate Mystique* de la **langue du patch**, identique par défaut à celle du programme mais modifiable séparément.
3. Choisissez votre ISO d'origine, laissez ou décochez les modules (tous sont activés par défaut), choisissez où enregistrer l'ISO et, pour les textures HD, le dossier de données de PPSSPP. La **taille finale de l'ISO et celle du pack de textures s'affichent en direct** et changent quand vous cochez ou décochez des modules.
4. Cliquez sur **Installer**. Le patch et les modules de textures sont téléchargés depuis les Releases et vérifiés (SHA-256) ; votre ISO d'origine n'est jamais modifiée.

Remarques sur les options :
- Sans *Retirer les autres langues du jeu*, le jeu garde ses cinq langues et son sélecteur ; seule la langue du patch reçoit les corrections et les textures HD.
- *Textures HD* crée un `textures.zip` séparé dans `<dossier de données PPSSPP>/PSP/TEXTURES/ULES00600/` (le même fichier fonctionne sur Android : copiez-le au même chemin sur le téléphone). Si ce dossier contient déjà un autre pack de textures, déplacez-le d'abord.

## Ligne de commande

Téléchargez `tfpatch.exe` (Windows) ou `tfpatch-linux-x86_64` (Linux ; `chmod +x` d'abord). Patchs : `patch_fr.tfp`, `patch_en.tfp`, `patch_de.tfp`, `patch_es.tfp`, `patch_it.tfp`.

```
tfpatch iso --iso ULES00600.iso --patch patch_fr.tfp --out ULES00600_fr.iso
tfpatch textures --lang fr --out textures.zip
```

`tfpatch iso` accepte `--no-cards`, `--no-text` et `--keep-languages` (les trois modules ci-dessus, désactivés) et `--dry-run` (affiche la taille finale de l'ISO en octets). `tfpatch textures` télécharge `base.zip` et le module de la langue, vérifie leur SHA-256 et les fusionne en un seul `textures.zip` (donnez un dossier à `--out` pour extraire ; avec `--source DOSSIER`, on utilise des fichiers déjà téléchargés). Sous Linux, tapez `./tfpatch-linux-x86_64`.

## Limites connues

- Une sauvegarde créée dans une autre langue que celle du patch n'est pas réalignée.
- Seul l'émulateur PPSSPP est pris en charge (le patch remplace un module du jeu dans l'ISO et les textures sont des textures de remplacement PPSSPP).
- Les modules de textures pèsent environ 1 Go par langue, plus une base de 1,4 Go commune à toutes les langues (le module anglais est petit).

## Fonctionnement

1. `patcher/strumenti/crea_patch_modulare.py` construit, pour chaque langue, l'ISO avec seulement les corrections des cartes, seulement celles des textes, et les deux, puis écrit un `.tfp` modulaire (format 2) : un zip avec `patch.json` et des deltas bsdiff, chacun étiqueté avec les modules dont il a besoin (`cards`, `text`, `strip`).
2. `patcher/tfpatch` (Rust) vérifie le MD5, sélectionne les deltas des modules actifs et écrit l'ISO sous forme compacte : mêmes en-tête et répertoires, puis seulement les données encore utilisées. La taille finale est calculée sans rien écrire, ce qui permet à l'installateur de l'afficher en direct.
3. Avec `strip`, `libtitle.prx` est modifié (`patcher/strumenti/salta_lingua.py`) pour supprimer l'écran et l'entrée de menu de langue et fixer la langue, et les fichiers des autres langues pointent vers les données de la langue choisie.
4. `patcher/strumenti/crea_moduli.py` crée `base.zip` et un `<langue>.zip` par langue ; `patcher/strumenti/manifest.py` complète `manifest.json` (SHA-256, patchs, tailles des ISO).
5. `verifica_modulare.py`, `verifica_iso.py` et `verifica_texture.py` contrôlent les résultats ; `costruisci_modulari.sh LANGUE...` refait et vérifie chaque combinaison.

Les textes, les règles éditoriales et les corrections se trouvent dans `strumenti/` (`correzioni/`, `dati/`). `GUIDA_NUOVA_LINGUA.md`, `REGISTRO_SCELTE.md` et `MODIFICHE_<LANGUE>.md` documentent la méthode et les choix (en italien).

## Compiler depuis les sources

```
cd patcher/tfpatch && cargo build --release
```

Cela compile `tfpatch` (ligne de commande) et `tfpatch-gui`. Sous Linux, l'interface graphique demande les paquets de développement habituels X11/Wayland/OpenGL.

## Crédits

- **MikeyMK** — *Yu-Gi-Oh! GX Tag Force 1 HD Remastered* (base des textures HD, version US).
- **chrisfand** — cartes HD.
- Polices libres (OFL) : XCharter, Libre Baskerville, Newsreader, Alegreya et d'autres, téléchargées par `strumenti/font_alternativi/scarica_font.sh`.

Projet de fans non officiel et sans but lucratif, non affilié à Konami. *Yu-Gi-Oh!* est une marque de Konami.

## Licence

Le code est publié sous [licence MIT](LICENSE). La licence ne couvre que le code : les textes du jeu appartiennent à Konami, et les textures HD s'appuient sur le travail de MikeyMK et chrisfand cité ci-dessus.
