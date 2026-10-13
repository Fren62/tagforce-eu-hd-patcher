# Yu-Gi-Oh! GX Tag Force 1 — Patcheur européen (HD + textes corrigés)

[English](README.md) · [Italiano](README.it.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md)

Patcheur gratuit et open source pour **Yu-Gi-Oh! GX Tag Force** (PSP), version européenne **ULES00600 v1.01**.
À partir de *votre propre* ISO, il produit une copie dans la langue choisie (**anglais, français, allemand, espagnol, italien**) avec :

- **textes corrigés** : noms et descriptions des cartes, dialogues, phrases des duels et chaînes de l'interface (fautes de frappe, accents, espaces, restes d'autres langues) ;
- **textures HD** pour PPSSPP : cartes grandes et petites dont le texte est redessiné dans votre langue, textes de l'interface, bannière du titre ;
- **plus de sélecteur de langue** : l'écran de choix au premier démarrage et l'entrée de choix de la langue du menu principal sont supprimés (la langue est fixe), car ils seraient inutiles ;
- **une seule langue dans l'ISO** : les autres langues sont retirées, l'ISO est donc plus légère (environ 610 Mo au lieu de 835 Mo) et le jeu reste dans la langue choisie quelle que soit la langue système de la PSP.

> **État : première version (v0.1.0).** Les cinq patchs d'ISO sont vérifiés fichier par fichier. Jeu testé dans PPSSPP jusqu'ici : italien et français (démarrage, titre, menu principal). L'anglais, l'allemand et l'espagnol doivent encore être testés à fond. Pas encore d'interface graphique, seulement la ligne de commande.

## Ce qu'il vous faut

- Votre propre ISO **ULES00600 v1.01** (européenne). MD5 du dump complet : `719c99478032a4210ae877832061e9fd` ([redump.org](http://redump.org/)). Les copies sans les 2 derniers Ko de zéros sont aussi acceptées.
- [PPSSPP](https://www.ppsspp.org/) avec **Remplacer les textures** activé ; résolution de rendu 4x recommandée.

Ce dépôt **ne contient pas** le jeu ni de données extraites du jeu : les patchs (`.tfp`) ne contiennent que des différences binaires par rapport aux fichiers d'origine.

## Utilisation (ligne de commande)

Téléchargez depuis la page [Releases](../../releases) : `tfpatch.exe` (Windows) ou `tfpatch-linux-x86_64` (Linux ; lancez d'abord `chmod +x tfpatch-linux-x86_64`), ainsi que le patch de votre langue (`patch_fr.tfp`, `patch_en.tfp`, `patch_de.tfp`, `patch_es.tfp` ou `patch_it.tfp`).

Les commandes ci-dessous utilisent `tfpatch` ; sous Linux, tapez `./tfpatch-linux-x86_64`.

1. Patchez l'ISO (l'original n'est jamais modifié) :

   ```
   tfpatch iso --iso ULES00600.iso --patch patch_fr.tfp --out ULES00600_fr.iso
   ```

2. Créez le pack de textures HD. L'outil télécharge `base.zip` et le module de votre langue depuis les Releases, vérifie leur SHA-256 et les fusionne en un seul `textures.zip` :

   ```
   tfpatch textures --lang fr --out textures.zip
   ```

3. Copiez `textures.zip` dans `<dossier de données PPSSPP>/PSP/TEXTURES/ULES00600/textures.zip` (même chemin sur Android ; ne le décompressez pas). Pour extraire dans un dossier, donnez un dossier à `--out`. Avec `--source DOSSIER`, on utilise des fichiers déjà téléchargés.

4. Dans PPSSPP : Paramètres → Graphismes → activez **Remplacer les textures**, puis lancez `ULES00600_fr.iso`.

Codes de langue pour `--lang` et pour les patchs : `fr`, `en`, `de`, `es`, `it`.

## Limites connues

- Une sauvegarde créée dans une autre langue que celle du patch n'est pas réalignée.
- Seul l'émulateur PPSSPP est pris en charge (le patch remplace un module du jeu dans l'ISO et les textures sont des textures de remplacement PPSSPP).
- Les modules de textures pèsent environ 1 Go par langue (`base.zip` 1,4 Go, commun à toutes les langues ; le module anglais est petit).

## Fonctionnement

1. `patcher/strumenti/crea_patch.py` compare l'ISO d'origine à l'ISO finale d'une langue et écrit un paquet `.tfp` (un zip avec `patch.json` et des deltas bsdiff).
2. `patcher/tfpatch` (Rust) vérifie le MD5, applique les deltas et réécrit l'ISO sous forme compacte : mêmes en-tête et répertoires, puis seulement les données encore utilisées (les autres langues sont laissées de côté).
3. `patcher/strumenti/salta_lingua.py` modifie `libtitle.prx` pour supprimer l'écran et l'entrée de menu de langue et fixer la langue.
4. `patcher/strumenti/crea_moduli.py` crée `base.zip`, un `<langue>.zip` par langue et `manifest.json` (SHA-256).
5. `patcher/strumenti/verifica_iso.py` et `verifica_texture.py` contrôlent les résultats ; `costruisci_patch.sh LANGUE...` refait et vérifie toute la chaîne.

Les textes, les règles éditoriales et les corrections se trouvent dans `strumenti/` (`correzioni/`, `dati/`). `GUIDA_NUOVA_LINGUA.md`, `REGISTRO_SCELTE.md` et `MODIFICHE_<LANGUE>.md` documentent la méthode et les choix (en italien).

## Compiler depuis les sources

```
cd patcher/tfpatch && cargo build --release
```

## Crédits

- **MikeyMK** — *Yu-Gi-Oh! GX Tag Force 1 HD Remastered* (base des textures HD, version US).
- **chrisfand** — cartes HD.
- Polices libres (OFL) : XCharter, Libre Baskerville, Newsreader, Alegreya et d'autres, téléchargées par `strumenti/font_alternativi/scarica_font.sh`.

Projet de fans non officiel et sans but lucratif, non affilié à Konami. *Yu-Gi-Oh!* est une marque de Konami.

## Licence

Le code est publié sous [licence MIT](LICENSE). La licence ne couvre que le code : les textes du jeu appartiennent à Konami, et les textures HD s'appuient sur le travail de MikeyMK et chrisfand cité ci-dessus.
