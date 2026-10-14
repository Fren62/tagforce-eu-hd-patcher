"""Check every mapping and decode every PNG; usage: validate_pack.py PACK REPORT.json."""
from pathlib import Path
import sys, re, json, collections
from PIL import Image

def mappings(path):
    rows=[]; section=''
    for number,line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(),1):
        line=line.strip()
        if line.startswith('['): section=line.lower()
        if section=='[hashes]':
            m=re.fullmatch(r'([0-9a-fA-F]{24})\s*=\s*(.*)',line)
            if m: rows.append((number,m[1].lower(),m[2].strip()))
    return rows

def audit(root):
    root=Path(root).resolve(); errors=[]; ini_reports=[]; referenced=set()
    for ini in sorted(root.rglob('textures.ini')):
        seen={}; rows=mappings(ini)
        for line,key,target in rows:
            if not target: continue # Empty replacement deliberately disables a hash.
            p=Path(target)
            if '\\' in target or p.is_absolute() or '..' in p.parts:
                errors.append([str(ini.relative_to(root)),line,'nonportable_path',target]);continue
            if key in seen and seen[key]!=target:
                errors.append([str(ini.relative_to(root)),line,'conflicting_duplicate',key,seen[key],target])
            seen[key]=target;referenced.add(target)
            if not (root/p).is_file(): errors.append([str(ini.relative_to(root)),line,'missing',target])
        ini_reports.append({'ini':str(ini.relative_to(root)),'mappings':len(rows),'unique_keys':len(seen)})
    dimensions=collections.Counter(); modes=collections.Counter(); count=0
    for path in sorted(root.rglob('*.png')):
        count+=1
        try:
            with Image.open(path) as im:
                im.load();dimensions[str(im.size)]+=1;modes[im.mode]+=1
        except Exception as e: errors.append([str(path.relative_to(root)),'decode',str(e)])
    return {'ini':ini_reports,'png_decoded':count,'dimensions':dict(dimensions),'modes':dict(modes),'referenced_files':len(referenced),'errors':errors}

if __name__=='__main__':
    result=audit(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(result,indent=2,ensure_ascii=False))
    print(json.dumps({k:v for k,v in result.items() if k not in ('dimensions','errors')},ensure_ascii=False));print('errors:',len(result['errors']))
    sys.exit(bool(result['errors']))
