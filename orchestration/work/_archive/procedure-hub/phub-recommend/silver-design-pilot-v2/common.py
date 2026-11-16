"""Local artifact helpers. Never executes a production generator or touches its inputs."""
import json, hashlib, re
from pathlib import Path
O=Path(__file__).resolve().parent
B=O.parent
A=B/'silver-origin-structure-audit'
D=B/'silver-entity-graph-design'
def read(p): return json.loads(Path(p).read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(name,data): (O/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def digest(x): return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def pointer(path):
 assert path.startswith('$'),path
 parts=[]
 for dot,b in re.findall(r'\.([^\.\[\]]+)|\[(\d+|\x27[^\x27]*\x27|"[^"]*")\]',path[1:]):
  parts.append(dot if dot else b if b.isdigit() else b[1:-1])
 return ''.join('/'+x.replace('~','~0').replace('/','~1') for x in parts)
def get(obj,p):
 if not p:return obj
 assert p.startswith('/')
 for k in p[1:].split('/'):
  k=k.replace('~1','/').replace('~0','~');obj=obj[int(k)] if isinstance(obj,list) else obj[k]
 return obj
def walk(obj,p=''):
 yield p,obj
 if isinstance(obj,dict):
  for k,v in obj.items():yield from walk(v,p+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(obj,list):
  for i,v in enumerate(obj):yield from walk(v,p+'/'+str(i))
def leaves(obj,p=''):
 if isinstance(obj,(list,dict)) and obj:
  for k,v in (enumerate(obj) if isinstance(obj,list) else obj.items()):yield from leaves(v,p+'/'+str(k).replace('~','~0').replace('/','~1'))
 else:yield p,obj
