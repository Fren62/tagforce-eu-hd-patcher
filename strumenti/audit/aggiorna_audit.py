"""Aggiorna i due audit dalle correzioni JA esplicite, senza toccare il gioco."""
import csv, json, re, html, collections
from pathlib import Path
root=Path(__file__).resolve().parents[2]
out=root/'confronti/audit_traduzioni'
with (out/'audit_traduzioni.csv').open(encoding='utf-8-sig',newline='') as f:
 reader=csv.DictReader(f);fields=list(reader.fieldnames);rows=list(reader)
fixes=json.loads(Path(__file__).with_name('revisione_ja.json').read_text())
ids={r['id'] for r in rows}
assert len(rows)==1378 and len(ids)==len(rows) and set(fixes)<=ids
originals={r['id']:(r['giapponese'],r['inglese'],r['italiano_attuale']) for r in rows}
extra=['proposta_pre_revisione','motivo_pre_revisione','nota_revisione_ja']
for f in extra:
 if f not in fields:fields.append(f)
notes={
 'st01_t01/Scr111E#27':'Le righe #25–#29 parlano del personaggio che passa inosservato. Il soggetto omesso di 忘れないでね si riferisce plausibilmente a lui, non alla carta; recuperato il contrasto con #28 sulla sua presenza.',
 'st01_t01/MorningE#22':'Il tasto ○ giapponese è adattato al tasto × di conferma della versione europea; conservati i codici colore.',
 'st01_t01/MorningE#26':'Il tasto ○ giapponese è adattato al tasto × di conferma della versione europea; conservati i codici colore.',
 'st01_t01/MorningE#100':'ボクなんかとじゃ…イヤだよね esprime il timore che l’altro non voglia stare con il parlante; non dice che il giocatore è di intralcio.',
 'st01_t01/Scr003E#147':'仕送り è denaro inviato dalla famiglia, non una paga; la frase termina in sospeso e non esplicita un invito a bere.',
 'st01_t01/Scr003E#151':'仕送り è denaro inviato dalla famiglia, non una paga; la frase termina in sospeso.',
 'st01_t01/Scr007E#563':'Adattamento del gioco fonetico ショウ/show/しょうがない. La proposta conserva una battuta sullo show ma non replica il gioco con il nome giapponese di Syrus; resa umoristica da valutare.',
 'st02_t01/Scr020E#3':'Soggetto omesso in JA: la parlante si augura il riconoscimento di Alexis (riga seguente), quindi prima persona; seconda persona EN non assunta come autorità.',
 'st02_t01/Scr020E#4':'認めてもらえるかも indica una speranza della parlante, non una promessa al giocatore; va letta con #3.',
 'st01_t01/Scr054E#26':'解けなくなりました letteralmente indica che la tensione non riesce più a sciogliersi. Anche JA #115/#116 di Iso010E usa questa forma; possibile refuso giapponese, non si adotta silenziosamente il senso opposto EN.',
 'st01_t01/Iso010E#116':'解けなくなりました non significa “non sono più teso”: può essere un refuso JA. Proposta letterale prudente; verificare intenzione e scena.',
 'st01_t01/Scr001E#627':'見えないからって richiama il fatto che chi ascolta non vede: non prova l’assenza delle pietanze descritte; rimossa l’affermazione inventata “lì non c’è niente”.',
 'st01_t01/Scr001E#500':'ドロマンジュウ gioca su draw e manju, non indica un giorno dedicato alle ciambelle; resa descrittiva del dolce da pescare, da confrontare con la battuta precedente.',
 'st01_t01/Scr029E#31':'Frase unita alla riga #32: la gallina d’oro dell’Accademia depone un uovo al giorno usato per questo panino.',
 'st01_t01/Scr029E#32':'Seconda parte della frase #31: 絶品 indica una squisitezza; le due proposte vanno lette insieme.'
}
for r in rows:
 r.setdefault('proposta_pre_revisione',r['italiano_proposto'])
 r.setdefault('motivo_pre_revisione',r['motivo'])
 if r['id'] in fixes:
  r['italiano_proposto']=fixes[r['id']]
  note=notes.get(r['id'],'Proposta riformulata sul testo giapponese riportato: recupera il significato, i dettagli e/o i segnaposto senza assumere la resa inglese come riferimento. Confrontare anche la proposta precedente.')
  if r['id'] in ['st01_t01/Scr021E#2','st02_t01/Scr021E#2','st02_t01/Scr021E#7']:
   note='Scelta di localizzazione concordata con l’utente: 20 punti → 4, voto italiano nettamente insufficiente. Il massimo non è indicato in questa scena; non è una conversione aritmetica attestata. Stessa resa in tutte le occorrenze.'
  r['nota_revisione_ja']=note
  r['motivo']='Riferimento JA: '+r['giapponese'].replace('\n',' / ')+' — '+note
 else:r['nota_revisione_ja']='Confronto della proposta con il giapponese estratto effettuato; conservata in questo passaggio. Non equivale ad approvazione per la patch.'
 # shortcut: uniforma solo grafia e lessico già scelti, non il tono dei singoli personaggi.
 s=r['italiano_proposto']
 s=re.sub(r'\bSandwich\b','Panino',s);s=re.sub(r'\bsandwich\b','panino',s)
 s=re.sub(r'\bDuelli tag\b','Tag Duel',s)
 s=re.sub(r'\bDuello\b','duello',s);s=re.sub(r'\bDuelli\b','duelli',s)
 s=re.sub(r'\bMedaglie GX\b','medaglie GX',s)
 s=s.replace("d'ananasso","all'ananas").replace("d’ananasso","all’ananas").replace("d'uva","all'uva")
 r['italiano_proposto']=s
 r['revisione_significato']='Confronto con JA estratto effettuato; validazione contestuale e nel gioco ancora necessaria'
norm=lambda s:re.sub(r'\s+',' ',s.replace('’',"'")).strip().casefold()
groups=collections.defaultdict(set)
for r in rows:
 if r['giapponese'].strip():groups[r['giapponese'].strip()].add(norm(r['italiano_proposto']))
tokens=lambda s:collections.Counter(re.findall(r'《[^》]+》|\$[A-Z]\d+',s))
for r in rows:
 flags=[]
 if not r['giapponese'].strip():flags.append('JA assente')
 if tokens(r['giapponese'])!=tokens(r['italiano_proposto']):flags.append('Segnaposto/formattazione diversi da JA: verificare prima della patch')
 if len(groups[r['giapponese'].strip()])>1:flags.append('Stessa battuta JA, rese diverse: confronto contestuale')
 if any(w in r['motivo_pre_revisione'].lower() for w in ['femminil','maschil','parlante donna']) and re.search(r'\b(?:battut[aoe]|assort[ao]|sorpres[ao]|pront[ao]|brav[ao]|scordat[ao]|iscritt[ao]|divertit[ao])\b',r['italiano_proposto'],re.I):flags.append('Genere del parlante da confermare nel contesto, non dai soli pronomi JA')
 if r['scena'].split('/')[-1].startswith(('Iso','Lesson')):flags.append('Scena narrativa: verificare segmentazione JA/IT; confronto per indice non sufficiente')
 if r['id'] in notes:flags.append(notes[r['id']])
 r['controllo_coerenza']='; '.join(flags) or 'Nessuna anomalia nelle verifiche automatiche; contesto non certificato'
assert all(originals[r['id']]==(r['giapponese'],r['inglese'],r['italiano_attuale']) for r in rows)
with (out/'audit_traduzioni.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
e=lambda s:html.escape(str(s)).replace('\n','<br>')
counts=collections.Counter(r['gravita'] for r in rows)
policy='Il giapponese è il riferimento di significato. L’inglese è una localizzazione da confrontare, non l’autorità semantica. Si preservano intenzione, tono del personaggio e livello di formalità, adattando in italiano nomi e riferimenti culturali quando opportuno. Un adattamento esplicito non è un errore: per queste tre battute, 20 punti è reso con un 4 su richiesta dell’utente, per mantenere un giudizio nettamente insufficiente. Terminologia: ricetta per レシピ; formula/incantesimo per 呪文; Tag Duel invariabile; Bestie Sacre; Cavalieri dell’Ombra; Dormitorio Slifer Rosso, Dormitorio Ra Giallo, Dormitorio Obelisk Blu. Panino anziché alternare panino e sandwich. Deck e PDA invariabili; duello, carta, medaglia e ricetta sono nomi comuni. Mantenere i segnaposto tecnici e verificare i nomi delle voci rispetto alla UI effettiva. Non appiattire le voci dei personaggi su un unico registro.'
parts=['<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Audit traduzioni</title><style>body{font:14px system-ui;margin:16px;color:#222}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:6px;vertical-align:top}th{position:sticky;top:0;background:#eee}.p{background:#eaffea}summary{cursor:pointer}</style>', '<h2>Audit delle traduzioni italiane — 17 blocchi degli script estratti</h2>',f'<p>{len(rows)} proposte: {counts["alta"]} alta, {counts["media"]} media, {counts["bassa"]} bassa. Nessuna modifica applicata al gioco.</p>','<h3>Coerenza e riferimento giapponese</h3><p>'+e(policy)+'</p>',f'<p>Secondo passaggio: {len(fixes)} proposte riformulate esplicitamente sul JA e controllo delle restanti proposte contro il JA estratto. La proposta precedente e la motivazione precedente restano consultabili. Questo audit non certifica l’allineamento di tutte le scene né costituisce una patch approvata: i testi possono essere suddivisi diversamente fra lingue, le righe vuote possono essere inutilizzate e il genere va verificato sul parlante. Gli a capo e la lunghezza delle nuove proposte non sono ancora validati nel gioco.</p>', '<table><tr>'+''.join('<th>'+s+'</th>' for s in ['Gravità / ID','Giapponese','Inglese','Italiano attuale','Proposta rivista','Motivo della proposta','Controllo / stato'])+'</tr>']
for r in rows:
 vals=[e(r['gravita']+' — '+r['id']),e(r['giapponese']),e(r['inglese']),e(r['italiano_attuale']),e(r['italiano_proposto'])+'<details><summary>Proposta precedente</summary>'+e(r['proposta_pre_revisione'])+'</details>',e(r['motivo'])+'<details><summary>Motivazione precedente</summary>'+e(r['motivo_pre_revisione'])+'</details>',e(r['controllo_coerenza'])+'<p>'+e(r['revisione_significato'])+'</p>']
 parts.append('<tr>'+''.join('<td'+(' class="p"' if i==4 else '')+'>'+v+'</td>' for i,v in enumerate(vals))+'</tr>')
parts.append('</table></html>');(out/'audit_traduzioni.html').write_text('\n'.join(parts),encoding='utf-8')
with (out/'audit_traduzioni.csv').open(encoding='utf-8-sig',newline='') as f:check=list(csv.DictReader(f))
assert len(check)==len(rows)
assert len({r['italiano_proposto'] for r in check if r['id'] in ['st01_t01/Scr021E#2','st02_t01/Scr021E#2','st02_t01/Scr021E#7']})==1
assert all(originals[r['id']]==(r['giapponese'],r['inglese'],r['italiano_attuale']) for r in check)
print({'righe':len(check),'revisioni_esplicite':len(fixes),'proposte_modificate':sum(r['italiano_proposto']!=r['proposta_pre_revisione'] for r in check),'avvisi':sum(r['controllo_coerenza'].startswith('Nessuna')==False for r in check)})
