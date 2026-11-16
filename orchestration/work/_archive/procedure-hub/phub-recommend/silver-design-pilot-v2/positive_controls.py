"""Positive controls retain usable identity facts and unknown clinical status."""
import copy
from common import *
from identity import revise
from project import project
from validate import safe_validate
p=read(O/'pilot.json');q=revise(copy.deepcopy(p));checks=safe_validate(q,project(q))
results=[{'check':'rehash_positive_idempotent','pass':q==p},{'check':'rehash_positive_validator','pass':all(c['pass'] for c in checks)},{'check':'identity_selected_exact8','pass':len([m for m in p['mappings'] if m['purpose']=='identity' and m['state']=='exact' and m['selected_refs']])==8},{'check':'candidate_selected0','pass':not any(m['selected_refs'] for m in p['mappings'] if m['state'] in ['ambiguous','unresolved','compatible_candidate'])},{'check':'unapproved_clinical_edge0','pass':all(a['application_state']=='unknown' for a in p['attachments'])},{'check':'identity_lookup8_source_facts167','pass':len(project(p)['identity_lookup'])==8 and len(project(p)['source_fact_lookup'])==167}]
write('positive-controls.json',{'checks':results,'passed':sum(c['pass'] for c in results),'failed':sum(not c['pass'] for c in results)})
print(__import__('json').dumps(read(O/'positive-controls.json')))
assert all(c['pass'] for c in results)
