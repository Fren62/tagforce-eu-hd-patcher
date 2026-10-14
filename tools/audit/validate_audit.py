"""Adds technical and contextual findings to the two documents, without modifying the ROM."""
import csv,json,re,html,collections,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2];out=root/'confronti/audit_traduzioni'
source=Path(sys.argv[1]);allrows=json.loads(source.read_text());raw={f"{x['sc']}/{x['b']}#{x['n']}":x for x in allrows}
with (out/'audit_traduzioni.csv').open(encoding='utf-8-sig',newline='') as f:
 reader=csv.DictReader(f);fields=list(reader.fieldnames);rows=list(reader)
report=json.loads(Path(__file__).with_name('archive_validation.json').read_text());assert report['fonti_verificate_dagli_archivi']==len(rows)==1378
contextnotes={
 'st01_t01/MorningE#100':'Il rifiuto precede il saluto “a domani” (#101); il parlante teme di essere sgradito. Proposta coerente con la scena, soggetto errato della vecchia proposta eliminato.',
 'st02_t01/Scr005E#5':'#3–#8: Chazz lamenta la mancanza di carisma dei presenti; Jaden risponde di essere emozionato, non di difendere Chazz. Il JA e l’IT della scena condividono gli stessi indici; è l’EN a riscrivere lo scambio.',
 'st02_t01/Scr005E#6':'#3–#8: risposta sarcastica alla spensieratezza di Jaden, non “parlavo di te”. Confermata la proposta sul JA.',
 'st02_t01/Scr005E#7':'#3–#8: Chazz vuole chiudere la sfida in fretta e aggiungerla alla propria leggenda. Confermato il singolare del segnaposto.',
 'st02_t01/Scr020E#3':'#0–#4: la parlante si presenta e parla della propria speranza di farsi riconoscere da Alexis. La prima persona IT è coerente; il cambio in seconda persona EN non va seguito.',
 'st02_t01/Scr020E#4':'Completa #3: “forse Alexis riconoscerà il mio valore”. Non promette al giocatore che Alexis riconoscerà il suo.',
 'st01_t01/Scr029E#31':'#30 introduce i ripieni; #31 specifica l’uovo unico deposto ogni giorno dalla gallina d’oro; #32 nomina il panino. Le due nuove proposte formano una frase coerente.',
 'st01_t01/Scr029E#32':'Leggere con #31: è il panino a essere una squisitezza, non soltanto l’uovo.',
 'st01_t01/Scr003E#146':'#146–#152: attività familiare di produzione del sake, shochu inviato da casa, interruzione e “scherzavo”. L’EN sostituisce deliberatamente l’alcol con salsa piccante; non è uno slittamento degli indici.',
 'st01_t01/Scr003E#147':'#146–#149: la frase si interrompe prima di esplicitare l’invito. Eliminati paga, sconto e invito aggiunti dalla localizzazione EN.',
 'st01_t01/Scr003E#151':'Ripetizione della sequenza #146–#149: stessa resa della battuta #147.',
 'st01_t01/Scr130E#7':'#6 richiama lo studente Slifer Rosso che usa Fusioni; #7 ricorda il soprannome tramite 《C001_4》. Il segnaposto deve restare dinamico, non “fannullone”.',
 'st01_t01/Scr111E#27':'#25–#29: ricetta/carta offerte dal personaggio, che lamenta di passare inosservato e promette un duello in cui farà sentire la sua presenza. Ripristinata la lettura riferita al parlante.',
 'st01_t01/Scr002E#430':'#429: Syrus si addormenta durante la lezione; #430 deve badare al gatto per punizione. Il nome JA ファラオ è esplicitato, mentre EN/IT usano correttamente il segnaposto localizzato 《C145_1》. Differenza intenzionale.',
}
for n in range(1,6):contextnotes[f'st02_t01/SysMsg#{n}']='I cinque record JA/EN #1–#5 sono distinti (sonno, lezione, due scelte, frequenza della lezione). I cinque IT ripetono lo stesso messaggio sul computer. Verificati direttamente negli archivi: difetto del testo italiano, non errore di estrazione; utilizzo effettivo nel gioco ancora da confermare.'
for k in ['st01_t01/Scr021E#2','st02_t01/Scr021E#2','st02_t01/Scr021E#7']:contextnotes[k]='#0–#8: giudizio sprezzante della parlante, non risultato di una prova. Massimo dei punti non esplicitato. “4” è l’adattamento italiano concordato con l’utente, coerente nelle tre occorrenze.'
contextnotes.update(json.loads(Path(__file__).with_name('context_consistency.json').read_text()))
for name in ['validazione_fonti','validazione_contesto','validazione_gioco','contesto_ja_it']:
 if name not in fields:fields.append(name)
def cleanja(s):return re.sub(r'\$R(.+?)\([^)]*\)',r'\1',s)
for r in rows:
 x=raw[r['id']];assert x['i']==r['italiano_attuale'] and x['e']==r['inglese'] and cleanja(x['j'])==r['giapponese']
 r['validazione_fonti']='Verificata negli archivi EHP JA/EN/IT: indice, stringa e decodifica corrispondono'
 r['validazione_contesto']=contextnotes.get(r['id'],'Non conclusa: il confronto per indice e il riscontro lessicale non certificano parlante, ramo narrativo o segmentazione semantica')
 r['validazione_gioco']='Non provata nella scena originale'
 if r['id'] in ['st01_t01/Scr021E#2','st02_t01/Scr021E#2','st02_t01/Scr021E#7']:r['validazione_gioco']='Impaginazione della stessa proposta verificata mediante sostituzione temporanea RAM in un dialogo di prova; non nella scena originale'
 seq=[]
 for n in range(max(0,x['n']-2),x['n']+3):
  y=raw.get(f"{x['sc']}/{x['b']}#{n}")
  if y:seq.append({'id':f"{x['sc']}/{x['b']}#{n}",'ja':cleanja(y['j']),'it':y['i']})
 r['contesto_ja_it']=json.dumps(seq,ensure_ascii=False)
 if r['id'] in ['st01_t01/Iso005E#8','st01_t01/Iso005E#6','st02_t01/Scr001E#10','st02_t01/Scr005E#13','st01_t01/LessonE#203','st01_t01/LessonE#294']:
  r['controllo_coerenza']=r['controllo_coerenza'].replace('Stessa battuta JA, rese diverse: confronto contestuale','Differenza di resa intenzionale verificata nel contesto')
 if r['id'] in ['st02_t01/Scr126E#2','st02_t01/Scr126E#5','st01_t01/Scr004E#20','st01_t01/Scr004E#26','st01_t01/Scr004E#34']:
  r['controllo_coerenza']=r['controllo_coerenza'].replace('Genere del parlante da confermare nel contesto, non dai soli pronomi JA','Accordo femminile riscontrato nel profilo del personaggio; ramo in gioco non verificato')
 if r['id']=='st01_t01/Scr002E#430':r['controllo_coerenza']='Differenza JA/IT intenzionale: ファラオ → 《C145_1》, nome localizzato del gatto'
report['riscontri_contestuali_espliciti']=len(contextnotes)
report['proposte_impaginate_in_dialogo_prova']=3
report['scena_originale_proposte_testate']=0
report['limiti']='Nessuna nuova proposta applicata alla ROM. RAM ripristinata al termine. I conteggi uguali non garantiscono corrispondenza semantica. Controllo font su due righe e a capo automatico; paginazione lunga non certificata.'
Path(__file__).with_name('archive_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
with (out/'audit_traduzioni.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
e=lambda s:html.escape(str(s)).replace('\n','<br>')
htmlpath=out/'audit_traduzioni.html';head=htmlpath.read_text().split('<table>')[0].split('<h3>Validazione</h3>')[0]
head+='<h3>Validazione</h3><p>1378 fonti ricontrollate direttamente in sei archivi EHP; 2136 coppie indice/stringhe valide. Nessuna scena ha un numero di record diverso fra JA, EN e IT. Questo prova la correttezza dell’estrazione, non l’equivalenza semantica delle battute. '+str(len(contextnotes))+' riscontri contestuali espliciti riportati per riga. Tre occorrenze della proposta del voto condividono il testo provato nel renderer tramite RAM. Nessuna proposta provata nella propria scena originale. Restano da confermare i rami narrativi, i parlanti incerti e la paginazione dei testi lunghi.</p>'
parts=[head,'<table><tr>'+''.join('<th>'+s+'</th>' for s in ['Gravità / ID','Giapponese','Inglese','Italiano attuale','Proposta rivista','Motivo','Validazione e contesto'])+'</tr>']
for r in rows:
 context='<details><summary>Battute vicine JA / IT</summary>'+''.join('<p><b>'+e(x['id'])+'</b><br>JA: '+e(x['ja'])+'<br>IT: '+e(x['it'])+'</p>' for x in json.loads(r['contesto_ja_it']))+'</details>'
 status=''.join('<p>'+e(r[k])+'</p>' for k in ['validazione_fonti','validazione_contesto','validazione_gioco','controllo_coerenza'])+context
 vals=[e(r['gravita']+' — '+r['id']),e(r['giapponese']),e(r['inglese']),e(r['italiano_attuale']),e(r['italiano_proposto'])+'<details><summary>Proposta precedente</summary>'+e(r['proposta_pre_revisione'])+'</details>',e(r['motivo'])+'<details><summary>Motivazione precedente</summary>'+e(r['motivo_pre_revisione'])+'</details>',status]
 parts.append('<tr>'+''.join('<td'+(' class="p"' if i==4 else '')+'>'+v+'</td>' for i,v in enumerate(vals))+'</tr>')
parts.append('</table></html>');htmlpath.write_text('\n'.join(parts),encoding='utf-8')
with (out/'audit_traduzioni.csv').open(encoding='utf-8-sig',newline='') as f:check=list(csv.DictReader(f))
assert len(check)==1378 and all(json.loads(r['contesto_ja_it']) for r in check)
print({'fonti_verificate':len(check),'riscontri_contesto':len(contextnotes),'resa_voto_testata':'dialogo RAM','scene_originali_testate':0})
