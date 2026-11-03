"""Bounded closeout probes for the changed scope/rule mechanisms only."""
import sys,json,copy,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];V=R.parent/'silver-design-pilot-v2';sys.path.insert(0,str(V))
from identity import revise
from validate import safe_validate
from project import project
from invariants import inspect
from ref_contract import ATTACHMENT_RULE
p=json.loads((V/'pilot.json').read_text());out=[]
def test(name,fn,expected=False):
 q=copy.deepcopy(p);fn(q);revise(q);checks=safe_validate(q,project(q));failed=[x for x in checks if not x['pass']]
 out.append({'name':name,'accepted':not failed,'expected_accepted':expected,'expectation_met':(not failed)==expected,'normalized_id_failures':sum(x['check']=='normalized_revision_id' for x in failed),'failed_checks':failed})
def context(q):return next(s for s in q['scopes'] if s['id']==q['scopes'][157]['container_scope_ref'])
test('comparison_context_excluded_duplicates',lambda q:context(q)['axes']['container'].update(excluded=['other','other']))
test('comparison_member_wrong_source_evidence',lambda q:q['scopes'][157]['axes']['site'].update(raw_refs=q['claims'][0]['source_refs']))
test('comparison_context_wrong_source_evidence',lambda q:context(q)['axes']['container'].update(raw_refs=q['claims'][0]['source_refs']))
test('source_role_duplicate_with_wrong_complaint',lambda q:next(s for s in q['scopes'] if 'container' in s['axes'] and len(s['axes']['container']['included'])==2 and len(set(s['axes']['container']['included']))==1)['axes']['container'].update(raw_refs=q['claims'][0]['source_refs']))
test('attachment_wrong_reachable_scope',lambda q:q['attachments'][0].update(scope_ref=q['scopes'][7]['id']))
test('attachment_claim_subjectless',lambda q:q['attachments'][0].update(claim_refs=[next(c['id'] for c in q['claims'] if c['subject_ref'] is None)]))
test('resolution_empty_policy_version',lambda q:q['resolutions'][0]['policy'].update(version=''))
test('normal_rehashed_preserves_values',lambda q:None,True)
# Generic unknown values are allowed if evidence exists. This isolated inspection
# control adds a synthetic site identity, not a source/clinical approval assertion.
q=copy.deepcopy(p);q['entities'].append({'id':'site:generic-control','type':'site','native_id':'generic-control','source_refs':p['claims'][0]['source_refs']})
q['scopes'].append({'id':'scope:generic-control','axes':{'site':{'knowledge':'unknown','included':['site:generic-control'],'excluded':[],'raw_refs':p['claims'][0]['source_refs'],'value_kind':'entity_refs'}},'container_scope_ref':None,'statement_qualifiers':[],'conflicts':[],'application_state':'unknown','record_schema_version':p['schema_version'],'mapping_rule_revision':p['mapping_rule_revision']})
revise(q);generic=inspect(q);generic_failed=[x for x in generic if not x['pass']]
# Independent provenance comparison: fixed declarations versus actual files, never build output.
actual={k:hashlib.sha256((V/f).read_bytes()).hexdigest() for k,f in [('implementation_sha256','build.py'),('contract_sha256','contract.md')]}
source_decision=json.loads((V.parent/'step9-decisions.json').read_text())
policy=p['resolutions'][0]['policy'];rule_hash=hashlib.sha256((V.parent/'step9-apply.py').read_bytes()).hexdigest()
positive={'comparison_parents':sum(s['container_scope_ref'] is not None for s in p['scopes']),'exact_identity':sum(m['purpose']=='identity' and m['state']=='exact' for m in p['mappings']),'ambiguous_candidate_counts':[len(m['candidates']) for m in p['mappings'] if m['state']=='ambiguous'],'ambiguous_selected':sum(len(m['selected_refs']) for m in p['mappings'] if m['state']=='ambiguous'),'source_role_duplicate_scopes':sum('container' in s['axes'] and len(s['axes']['container']['included'])>len(set(s['axes']['container']['included'])) for s in p['scopes']),'claims':len(p['claims']),'attachments':len(p['attachments'])}
result={'probes':out,'all_expectations_met':all(x['expectation_met'] for x in out),'generic_unknown_candidate_control':{'inspection_only':True,'accepted':not generic_failed,'failures':generic_failed,'clinical_positive':False},'declaration_actual_hashes':actual,'fingerprints_match':all(ATTACHMENT_RULE[k]==v for k,v in actual.items()),'resolution_actual_source_match':policy['version']==str(source_decision['version']) and policy['id']=='D9-3' and policy['code_sha256']==rule_hash,'positive':positive}
(R/'results/independent.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['probes','generic_unknown_candidate_control']},ensure_ascii=False));print('generic_unknown',not generic_failed)
