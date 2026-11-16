"""Independent, bounded semantic counterexamples with all revision IDs recomputed."""
import copy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent;V=R.parent/'silver-design-pilot-v2'
sys.dont_write_bytecode=True;sys.path.insert(0,str(V))
from identity import revise
from validate import safe_validate
from project import project
p=json.loads((V/'pilot.json').read_text());out=[]
def scope(q,cid):
 case=next(c for c in q['cases'] if c['id']==cid)
 return next(s for s in q['scopes'] if s['id']==case['scope_refs'][0])
def language(q):return scope(q,'PATIENT-LANG-01')
def run(name,mut):
 q=copy.deepcopy(p);mut(q);revise(q)
 try:
  checks=safe_validate(q,project(q));failed=[c for c in checks if not c['pass']]
  out.append({'probe':name,'accepted':not failed,'failed_checks':failed,'total_checks':len(checks),'normalized_id_failures':sum(c['check']=='normalized_revision_id' for c in failed)})
 except Exception as e:out.append({'probe':name,'implementation_error':repr(e),'cause':repr(e.__cause__)})
run('positive_rehashed',lambda q:None)
run('language_scope_excludes_its_included_M2',lambda q:language(q)['axes']['family'].update(excluded=['family:M2']))
run('language_scope_explicit_to_unknown_axis',lambda q:language(q)['axes']['family'].update(knowledge='unknown'))
run('language_scope_adds_unrelated_container',lambda q:language(q).update(container_scope_ref=q['scopes'][7]['id']))
run('combo_scope_excludes_its_source_container',lambda q:q['scopes'][7]['axes']['container'].update(excluded=list(q['scopes'][7]['axes']['container']['included'])))
run('resolution_policy_version_forged',lambda q:q['resolutions'][0]['policy'].update(version='incorrect-version'))
run('attachment_rule_id_version_forged',lambda q:q['attachments'][0]['rule'].update(id='invented-rule',version='incorrect-version'))
run('language_axis_literal_disguised_as_entity',lambda q:language(q)['axes']['family'].update(value_kind='source_literals'))
run('approved_decision_wrong_existing_target',lambda q:q['decisions'][0].update(target_refs=[q['claims'][0]['id']]))
run('timing_invented_numeric_interval',lambda q:next(r for r in q['relation_claims'] if r['relation_kind']=='timing')['interval'].update(min=0,max=0,unit='day'))
run('override_wrong_existing_scope',lambda q:next(c for c in q['claims'] if c['override'])['override'].update(scope_ref=q['scopes'][0]['id']))
(R/'independent-additional.json').write_text(json.dumps({'probes':out,'mutations':len(out)-1,'accepted_mutations':sum(x.get('accepted',False) for x in out[1:]),'implementation_errors':sum('implementation_error' in x for x in out)},ensure_ascii=False,indent=2)+'\n')
print(json.dumps([{k:x[k] for k in ['probe','accepted','implementation_error'] if k in x} for x in out]))
