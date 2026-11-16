"""Verify audit artifact references, arithmetic and input preservation (no generators)."""
import hashlib
import json
import re
from pathlib import Path
OUT=Path(__file__).resolve().parent
J=lambda p:json.loads(p.read_text())
inventory=J(OUT/'inventory.json')
checks=[]
def checked(name, ok, **detail):
    checks.append({'check':name,'pass':bool(ok),**detail})
for f in inventory['files']:
    p=Path(f['file'])
    checked('input_preserved',p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'],file=str(p))
issues=J(OUT/'issues.json')['issues']
checked('issue_ids_unique',len(issues)==len({x['id'] for x in issues}),count=len(issues))
required={'id','stage','origin','silver','transformation_rule','classification','impact','certainty','required_metadata','proposed_fix','confirmation_question'}
checked('issue_contract',all(required<=set(x) for x in issues))
def value_at(file,path):
    obj=J(Path(file))
    assert path.startswith('$'),path
    for dot,bracket in re.findall(r'\.([^\.\[\]]+)|\[(\d+|\x27[^\x27]*\x27|"[^"]*")\]',path[1:]):
        key=dot if dot else int(bracket) if bracket.isdigit() else bracket[1:-1]
        obj=obj[key]
    return obj
for i in issues:
    refs=(i['origin'] if isinstance(i['origin'],list) else [i['origin']])+[i['silver']]
    for ref in refs:
        try:
            value=value_at(ref['file'],ref['jsonpath'])
            checked('issue_reference_value',value==ref['value'],issue=i['id'],file=ref['file'],path=ref['jsonpath'])
        except Exception as exc:
            checked('issue_reference_value',False,issue=i['id'],path=ref['jsonpath'],error=str(exc))
schema=J(OUT/'schema-proposal.json')
field_keys={'meaning','type','required','missing','null','empty_array','origin','responsibility','migration'}
checked('schema_field_contracts',all(field_keys<=set(f) for f in schema['fields']),count=len(schema['fields']))
checked('schema_field_names_unique',len(schema['fields'])==len({f['name'] for f in schema['fields']}))
direct=J(OUT/'direct-comparisons.json')
checked('direct_comparison_arithmetic',sum(direct['summary'].values())==len(direct['checks'])==9785)
checked('direct_differences',sum(not c['equal'] for c in direct['checks'])==3)
collisions=J(OUT/'normalization-collisions.json')
checked('loss_evidence_count',len(collisions)==3 and sum(len(c['lost_original_leaves']) for c in collisions)==10)
ids=J(OUT/'id-design.json')
checked('primary_ID_groups',len(ids['primary_id_uniqueness'])==14 and all(not v['duplicates'] for v in ids['primary_id_uniqueness'].values()))
report=(OUT/'report.md').read_text()
for label,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',report):
    if not target.startswith(('https:','http:','#')):
        checked('report_link_exists',(OUT/target).exists(),target=target)
table=report.split('### 3.2')[1].split('### 3.3')[0]
nums=[]
for line in table.splitlines():
    if line.startswith('| step'):
        ns=re.findall(r'\d[\d,]*',line.split('|')[2])
        nums.extend(int(n.replace(',','')) for n in ns)
checked('report_comparison_arithmetic',sum(nums)==9785,total=sum(nums))
result={'scope':'artifact correctness and immutable inputs only; not clinical validation','passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'checks':checks}
(OUT/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':result['passed'],'failed':result['failed'],'failures':[c for c in checks if not c['pass']]},ensure_ascii=False))
raise SystemExit(bool(result['failed']))
