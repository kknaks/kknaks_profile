"""Read-only review; writes only into this review directory. stdlib only."""
import sys, os, json, copy, hashlib, runpy, contextlib, io, shutil
from pathlib import Path
from collections import Counter
os.environ['PYTHONDONTWRITEBYTECODE']='1'
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
P=R.parent/'silver-design-pilot'
sys.path.insert(0,str(P))
import common, validate as v, schema, project
def dump(name,x): (R/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
paths={str(x) for x in P.rglob('*') if x.is_file()}
paths.update(x['file'] for x in common.read(P/'inputs-start.json'))
def manifest():return [{'file':x,'sha256':common.sha(x),'bytes':Path(x).stat().st_size} for x in sorted(paths)]
start=common.read(R/'review-start.json') if (R/'review-start.json').exists() else manifest()
if not (R/'review-start.json').exists():dump('review-start.json',start)
p=common.read(P/'pilot.json');g=common.read(P/'graph-projection.json')
checks=v.safe_validate(p,g)
mut=v.mutation_tests(p)
extra=[{'check':'input_start_hash','pass':common.sha(x['file'])==x['sha256'] and Path(x['file']).stat().st_size==x['bytes'],'file':x['file'],'expected_sha256':x['sha256'],'current_sha256':common.sha(x['file'])} for x in common.read(P/'inputs-start.json')]
extra.append({'check':'schema_artifact','pass':common.read(P/'schema.json')==schema.SCHEMA})
dump('existing-rerun.json',{'checks':checks+extra,'mutations':mut,'passed':sum(x['pass'] for x in checks+extra),'failed':sum(not x['pass'] for x in checks+extra)})
out=[]
def test(name,fn):
 q=copy.deepcopy(p);fn(q);c=v.safe_validate(q,project.project(q));fails=[x for x in c if not x['pass']]
 out.append({'probe':name,'accepted':not fails,'failed_checks':fails[:8]})
def case(q,cid):return next(x for x in q['cases'] if x['id']==cid)
def item(q,group,rid):return next(x for x in q[group] if x['id']==rid)
def claim(q,cid):return item(q,'claims',case(q,cid)['claim_refs'][0])
def scope(q,cid):return item(q,'scopes',case(q,cid)['scope_refs'][0])
def replace_id(q,old,new):
 def walk(x):
  if isinstance(x,dict):
   for k,vv in x.items():x[k]=new if vv==old else walk(vv)
  elif isinstance(x,list):
   for i,vv in enumerate(x):x[i]=new if vv==old else walk(vv)
  return x
 walk(q)
test('positive_control',lambda q:None)
test('decision_dangling_target',lambda q:q['decisions'][0].update(target_refs=['clm:'+'0'*64]))
test('decision_authority_changed_to_human',lambda q:q['decisions'][0]['authority'].update(kind='human'))
test('decision_dangling_supersedes',lambda q:q['decisions'][0].update(supersedes=['dec:'+'0'*64]))
test('override_dangling_claim',lambda q:claim(q,'PRODUCT-SCOPE-01')['override'].update(claim_refs=['clm:'+'0'*64]))
test('override_wrong_scope_type',lambda q:claim(q,'PRODUCT-SCOPE-01')['override'].update(scope_ref=q['entities'][0]['id']))
test('attachment_witness_wrong_ref_types',lambda q:q['attachments'][0].update(witness=[{'mapping_ref':q['claims'][0]['id'],'edge_ref':'missing','component_ref':'missing','source_ref':q['claims'][0]['id']}]))
test('axis_dangling_entity',lambda q:scope(q,'LOSS-01')['axes']['product'].update(included=['product:missing']))
test('scope_family_qualifier_erased_language',lambda q:scope(q,'PATIENT-LANG-01').update(axes={}))
test('claim_wrong_raw_field',lambda q:claim(q,'LOSS-01').update(raw_field='safety.common_completely_wrong'))
test('claim_predicate_changed_language',lambda q:claim(q,'PATIENT-LANG-01').update(predicate='safety.common'))
test('claim_variant_links_wrong_existing_claim',lambda q:next(x for x in q['claims'] if x['language']=='ko')['variant'].update(of=q['claims'][0]['id']))
test('claim_id_arbitrarily_changed_with_refs',lambda q:replace_id(q,q['claims'][0]['id'],'clm:'+'0'*64))
test('mapping_rule_wrong_version',lambda q:next(x for x in q['mappings'] if x['rule'])['rule'].update(version='incorrect-version'))
test('mapping_drop_exact_selection',lambda q:next(x for x in q['mappings'] if x['purpose']=='identity' and x['rule'] and x['rule']['id']=='step7-apply.py').update(selected_refs=[]))
test('snapshot_source_kind_wrong',lambda q:q['snapshots'][0].update(source_kind='research'))
test('source_native_id_wrong',lambda q:next(x for x in q['source_records'] if x['native_id']).update(native_id='wrong-native-id'))
test('combo_scope_container_erased',lambda q:q['scopes'][7].update(axes={}))
test('timing_days_false_instead_of_null',lambda q:next(x for x in q['relation_claims'] if x['relation_kind']=='timing')['field_conditions']['days'].update(value=False))
test('timing_interval_changed',lambda q:next(x for x in q['relation_claims'] if x['relation_kind']=='timing')['interval'].update(min=0,max=0,unit='day'))
test('relation_direction_unfounded',lambda q:next(x for x in q['relation_claims'] if x['arity']==3).update(direction='directed'))
test('case_wrong_claim_ref_existing',lambda q:case(q,'PATIENT-LANG-01').update(attachment_refs=[q['attachments'][0]['id']]))
test('scope_unknown_to_explicit_language',lambda q:scope(q,'PATIENT-LANG-01').update(application_state='explicit'))
test('schema_bool_in_integer_arity',lambda q:q['relation_claims'][0].update(arity=True))
test('schema_number_in_raw_value',lambda q:q['source_records'][0].update(raw_value=0))
dump('additional-probes.json',out)

# Use the actual builder functions, with output redirected in memory.
captured={};oldwrite=common.write;common.write=lambda n,x:captured.update({n:x})
with contextlib.redirect_stdout(io.StringIO()): ns=runpy.run_path(str(P/'build.py'))
common.write=oldwrite
dump('builder-repro.json',{'same_pilot_after_JSON_serialization':json.loads(json.dumps(captured['pilot.json']))==p})
f=Path(next(x['file'] for x in p['source_records'] if x['file'].endswith('problem-packages.json')))
target=R/'relocation'/f.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(f,target)
ptr='/problems/8/complaints/10';before=ns['src'](f,ptr);after=ns['src'](target,ptr)
dump('relocation.json',{'original':str(f),'copy':str(target),'pointer':ptr,'same_bytes':f.read_bytes()==target.read_bytes(),'original_sha256':common.sha(f),'copy_sha256':common.sha(target),'original_snapshot':ns['files'][str(f)],'copy_snapshot':ns['files'][str(target)],'original_occurrence':before,'copy_occurrence':after,'snapshot_id_collision_count':len(ns['p']['snapshots'])-len({x['id'] for x in ns['p']['snapshots']})})
target.unlink();target.parent.rmdir()
end=manifest();dump('review-end.json',end);dump('immutability.json',{'files':len(start),'unchanged':start==end})
print(json.dumps({'existing_pass':sum(x['pass'] for x in checks+extra),'existing_fail':sum(not x['pass'] for x in checks+extra),'mutation_rejected':sum(x['rejected'] for x in mut),'additional':out,'immutable':start==end},ensure_ascii=False))

