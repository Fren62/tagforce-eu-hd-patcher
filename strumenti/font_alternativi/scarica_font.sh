#!/bin/sh
# Scarica i font LIBERI usati come alternativa ai font di macOS (licenza OFL, tranne XCharter: licenza Bitstream Charter, libera).
# Destinazione: scaricati/  (poi: python crea_istanze.py -> static/ con Regular/Medium/Bold/Black dei font variabili)
set -e
D=$(cd "$(dirname "$0")" && pwd)/scaricati; mkdir -p "$D"; cd "$D"
G=https://raw.githubusercontent.com/google/fonts/main/ofl
dl(){ curl -sL -o "$2" "$G/$1/$3"; }
dl ptserifcaption PTSerifCaption-Regular.ttf PT_Serif-Caption-Web-Regular.ttf   # = PT Serif Caption di macOS (stesso carattere)
dl ptserifcaption PTSerifCaption-Italic.ttf  PT_Serif-Caption-Web-Italic.ttf
dl charissil CharisSIL-Bold.ttf CharisSIL-Bold.ttf; dl charissil CharisSIL-Regular.ttf CharisSIL-Regular.ttf
for f in CrimsonPro LibreBaskerville SourceSerif4 Literata Newsreader Lora Gelasio LibreCaslonText Faustina Alegreya Vollkorn EBGaramond; do
  d=$(echo $f | tr 'A-Z' 'a-z'); axes='%5Bwght%5D'; case $f in SourceSerif4|Literata|Newsreader) axes='%5Bopsz,wght%5D';; esac
  dl $d $f.ttf "$f$axes.ttf"; [ $f = LibreBaskerville ] || dl $d $f-Italic.ttf "$f-Italic$axes.ttf"
done
# XCharter (derivato da Bitstream Charter): https://mirrors.ctan.org/fonts/xcharter.zip -> xcharter/opentype/*.otf
# --- sostituti dei font Apple usati da interfaccia, scritte del duello, schermata VS, tutorial (tutti OFL/Apache) ---
A=https://raw.githubusercontent.com/google/fonts/main/ofl
dla(){ curl -sL -o "$2" "$A/$1/$3"; }
dla tinos Tinos-Bold.ttf Tinos-Bold.ttf; dla tinos Tinos-Regular.ttf Tinos-Regular.ttf; dla tinos Tinos-Italic.ttf Tinos-Italic.ttf                       # Times / Times Bold
dla arimo Arimo.ttf 'Arimo%5Bwght%5D.ttf'                                                                    # Helvetica / Arial
dl jost Jost.ttf 'Jost%5Bwght%5D.ttf'                                                                        # Futura
dl barlowcondensed BarlowCondensed-Medium.ttf BarlowCondensed-Medium.ttf                                      # Futura Condensed Medium
dl barlowcondensed BarlowCondensed-ExtraBold.ttf BarlowCondensed-ExtraBold.ttf                                # Futura Condensed ExtraBold
dl archivoblack ArchivoBlack-Regular.ttf ArchivoBlack-Regular.ttf                                             # Arial Black
dl comicneue ComicNeue-Bold.ttf ComicNeue-Bold.ttf                                                            # Comic Sans MS Bold
dl kalam Kalam-Regular.ttf Kalam-Regular.ttf; dl kalam Kalam-Bold.ttf Kalam-Bold.ttf                          # Chalkboard SE
dl ptsans PTSans-Bold.ttf PT_Sans-Web-Bold.ttf; dl ptsans PTSans-Regular.ttf PT_Sans-Web-Regular.ttf         # PT Sans (e' lo stesso font)
dl inter Inter.ttf 'Inter%5Bopsz,wght%5D.ttf'                                                                 # SF Pro
dl nunito Nunito.ttf 'Nunito%5Bwght%5D.ttf'                                                                   # SF Pro Rounded / SF Compact Rounded
dl notosansjp NotoSansJP.ttf 'NotoSansJP%5Bwght%5D.ttf'                                                       # Hiragino Sans (kanji)
dl mplusrounded1c MPLUSRounded1c-Medium.ttf MPLUSRounded1c-Medium.ttf                                         # Hiragino Maru Gothic
