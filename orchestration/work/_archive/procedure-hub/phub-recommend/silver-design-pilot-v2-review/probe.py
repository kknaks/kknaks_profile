"""Read-only v2 rerun. Writes/copies only beneath this review directory."""
import contextlib, copy, hashlib, io, json, runpy, sys
from pathlib import Path
R=Path(__file__).resolve().parent
V=R.parent/'silver-design-pilot-v2'
sys.dont_write_bytecode=True
def read(path):return json.loads(Path(path).read_text())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(name,data):(R/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def manifest(paths):return [{'file':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(set(paths))]
protected=read(V/'protected-start.json')
paths=[Path(row['file']) for rows in protected.values() for row in rows]
paths+=list(V.rglob('*'))
paths=[p for p in paths if p.is_file()]
start=manifest(paths);write('review-start.json',start)
sys.path.insert(0,str(V))
import common
original_read=common.read
outputs=set()
def output(name,obj):outputs.add(name);write(name,obj)
def redirected_read(path):
 path=Path(path)
 return read(R/path.name) if path.parent==V and path.name in outputs else original_read(path)
common.write=output;common.read=redirected_read
import validate, project, identity, schema
p=read(V/'pilot.json')
checks=validate.safe_validate(p,read(V/'graph-projection.json'))
write('baseline.json',{'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'checks':checks,'schema_matches':read(V/'schema.json')==schema.SCHEMA})
for filename in ['probes.py','semantic_probes.py','positive_controls.py','identity_tests.py','source_review.py']:
 text=(V/filename).read_text()
 if filename=='identity_tests.py':text=text.replace("scratch=O/'_identity_scratch'","scratch=REVIEW/'_identity_scratch'")
 if filename=='source_review.py':text=text.replace("(R/'independent-source.json').write_text","(REVIEW/'independent-source.json').write_text")
 with contextlib.redirect_stdout(io.StringIO()) as log:
  exec(compile(text,str(V/filename),'exec'),{'__file__':str(V/filename),'__name__':'review_rerun','REVIEW':R})
 write(filename+'.execution.json',{'stdout':log.getvalue(),'source_sha256':sha(V/filename),'redirection':'output only; original code unchanged'})
write('rerun-integrity.json',{'protected_unchanged_after_reruns':start==manifest(paths),'files':len(start),'basis_code':manifest(list(V.glob('*.py')))})
end=manifest(paths);write('review-end.json',end)
write('immutability.json',{'files':len(start),'unchanged':start==end,'changes':[{'start':a,'end':b} for a,b in zip(start,end) if a!=b]})
print(json.dumps({'baseline_passed':sum(c['pass'] for c in checks),'baseline_failed':sum(not c['pass'] for c in checks),'protected_unchanged':start==manifest(paths),'files':len(start)}))
