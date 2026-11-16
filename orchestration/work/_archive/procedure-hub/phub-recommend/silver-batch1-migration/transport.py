"""Transport only; no transformation oracle. Python standard library."""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SCHEMA = 'silver-batch1/1'

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(canonical(value) + b'\n')

def escape(key):
    return str(key).replace('~', '~0').replace('/', '~1')

def pointer(value, ptr):
    if ptr == '':
        return value
    if not ptr.startswith('/'):
        raise ValueError('not RFC6901: '+ptr)
    for k in ptr[1:].split('/'):
        k = k.replace('~1', '/').replace('~0', '~')
        value = value[int(k)] if isinstance(value, list) else value[k]
    return value

def leaves(value):
    if isinstance(value, dict):
        return sum(map(leaves, value.values()))
    if isinstance(value, list):
        return sum(map(leaves, value))
    return 1

def inventory(path):
    p = Path(path)
    return {'file': str(p), 'sha256': sha(p), 'bytes': p.stat().st_size}

def verify_fixed_inputs():
    expected = load(HERE/'expected-inputs.json')
    for name, h in expected.items():
        if sha(BASE/name) != h:
            raise ValueError('fixed contract/oracle changed: '+name)

def read_inputs(path, locator_root=None):
    rows = load(path)
    documents = {}
    locators = {}
    for row in rows:
        key = (row['domain'], row['logical_file_key'])
        p = Path(locator_root)/row['domain']/row['logical_file_key'] if locator_root else Path(row['file'])
        if sha(p) != row['sha256'] or p.stat().st_size != row['bytes']:
            raise ValueError('input hash/bytes mismatch: '+str(p))
        raw = p.read_text(encoding='utf-8')
        documents[key] = json.loads(raw) if p.suffix=='.json' else raw
        locators[key] = str(p)
    return rows, documents, locators
