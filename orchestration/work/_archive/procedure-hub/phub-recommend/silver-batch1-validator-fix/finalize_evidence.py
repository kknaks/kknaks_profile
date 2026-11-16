"""Snapshot protected inputs and final validator code; never write the candidate."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;B=R.parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,v):(R/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
start_rows=json.loads((R/'protected-start.json').read_text())
start_by_path={}
for row in start_rows:
    assert row['file'] not in start_by_path or start_by_path[row['file']]==row
    start_by_path[row['file']]=row
start=list(start_by_path.values());end=[];changes=[]
allowed={str((B/'silver-batch1-migration'/n).resolve()) for n in ['validate.py','test_contract.py']}
for before in start:
    p=Path(before['file']);after={'file':str(p),'sha256':sha(p) if p.is_file() else None,'bytes':p.stat().st_size if p.is_file() else None};end.append(after)
    if before!=after:changes.append({'file':str(p),'authorized':str(p) in allowed,'before':before,'after':after})
write('protected-end.json',end)
write('protection-result.json',{'protected_files':len(start),'changed':changes,'unexpected_changes':[r for r in changes if not r['authorized']],
    'candidate_unchanged':all(not r['file'].startswith(str((B/'silver-batch1-candidate').resolve())+'/') for r in changes)})
write('code-hashes.json',[{'file':str((B/'silver-batch1-migration'/n).resolve()),'sha256':sha(B/'silver-batch1-migration'/n)} for n in ['validate.py','independent_source.py','test_contract.py','build.py','rules.py','transport.py','type-contract.json','expected-inputs.json','expected-rules.json']])
