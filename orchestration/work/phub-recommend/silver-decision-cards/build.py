"""Read-only source extraction; writes only next to this script."""
import json, hashlib, pathlib, collections
HERE=pathlib.Path(__file__).resolve().parent
BASE=HERE.parent
CAND=BASE/'silver-batch1-candidate'
def sha(b): return hashlib.sha256(b).hexdigest()
def read(n): return json.loads((CAND/(n+'.json')).read_text())
def write(n,d): (HERE/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def inventory(): return {p.name:sha(p.read_bytes()) for p in sorted(CAND.rglob('*')) if p.is_file()}
def pointer(d,p):
 for bit in p.lstrip('/').split('/') if p else []:
  bit=bit.replace('~1','/').replace('~0','~'); d=d[int(bit)] if isinstance(d,list) else d[bit]
 return d
if not (HERE/'results/candidate-start.json').exists(): write('results/candidate-start.json',inventory())
r=read('records'); safety=read('safety-claims'); rows=read('source-row-index'); ledgers=read('mapping-ledger'); identity=read('identity-ledger'); coverage=read('coverage'); im=read('input-manifest'); om=read('output-manifest')
src={x['id']:x for x in r['source_records']}; claims={x['id']:x for x in r['claims']}; mappings={x['id']:x for x in r['mappings']}; scopes={x['id']:x for x in r['scopes']}
registry={x['id']:x for k in ['products','families','registry'] for x in r[k]}
fields=[x for x in safety['fields'] if x['attachment_state']=='not_created']
reasons={'candidate_only':'후보 여럿','out_of_batch_entity':'이번 범위 밖','owner_unresolved':'대상 미확정'}
recommend={'candidate_only':('원장확인','후보로 기록된 관계만으로 이 필드의 단일 대상을 정할 수 없습니다. 원장 관계와 적용 범위를 확인해 주세요.'),'out_of_batch_entity':('후속이관유지','원문은 보존되어 있습니다. 이번에 이관하지 않은 대상이므로 후속 묶음에서 다룹니다.'),'owner_unresolved':('원장확인','단일 소유 대상이 검증되지 않았습니다. 원장의 대상 관계와 필드가 말하는 범위를 먼저 확인해 주세요.')}
selected_rows={s:next(x for x in rows if x['category']=='safety' and s in x['source_refs']) for s in {x['row_source_ref'] for x in fields}}
file_cache={}; used_src={}; groups={}; cards=[]
def evidence(ref):
 s=src[ref]; used_src[ref]=s
 p=s['file']
 if p not in file_cache:
  b=pathlib.Path(p).read_bytes(); assert sha(b)==s['source_sha256'],p
  file_cache[p]=json.loads(b)
 assert pointer(file_cache[p],s['pointer'])==s['raw_value'],ref
 return s
def target(ref):
 e=registry[ref]; ss=[evidence(s) for s in e['source_refs']]
 label=e.get('label') or next((s['raw_value'].get('name') for s in ss if isinstance(s['raw_value'],dict) and s['raw_value'].get('name')),e['native_id'])
 return {'id':ref,'label':label,'type':e['type'] if 'type' in e else ref.split(':')[0],'source_refs':e['source_refs'],'limited_registry':e.get('limited_registry',False)}
for f in fields:
 row=evidence(f['row_source_ref']); idx=selected_rows[row['id']]; cl=claims[f['claim_ref']]; scope=scopes[f['scope_ref']]; ms=[mappings[m] for m in f['mapping_refs']]
 assert cl['raw_value']==f['raw_value'] and cl['subject_ref'] is None
 gid='row:'+sha((row['logical_file_key']+'\0'+row['pointer']+'\0'+row['source_sha256']).encode())
 if gid not in groups:
  cur=[evidence(s) for s in idx['source_refs'] if s!=row['id']]
  groups[gid]={'id':gid,'label':row['raw_value'].get('name',f['legacy_id']),'native_id':f['legacy_id'],'row_source_ref':row['id'],'current_source_refs':[s['id'] for s in cur],'source_index':idx,'card_ids':[]}
 refs=set(f['source_refs'])
 for m in ms:
  refs.update(m['source_refs'])
  for c in m['candidates']: refs.update(c.get('raw_refs',[]))
 for ax in scope['axes'].values():refs.update(ax.get('raw_refs',[]))
 for ref in refs:evidence(ref)
 allowed=sorted({c['target_ref'] for m in ms if m['purpose']=='identity' for c in m['candidates'] if c['target_ref'] in registry})
 targets=[target(ref) for ref in allowed]
 why=f['attachment_reason']; rec,basis=recommend[why]
 card={**f,'id':'field:'+sha((f['claim_ref']+'\0'+f['scope_ref']).encode()),'group_id':gid,'label':groups[gid]['label'],'reason_label':reasons[why],'data_type':'사후관리' if f['predicate']=='aftercare' else '안전 정보','question':'이 원문 필드를 '+('후속 이관 묶음에 그대로 남길지, 원장 확인이 필요한지 정해 주세요.' if why=='out_of_batch_entity' else '어떤 대상과 범위에 연결할 수 있는지 원장 근거로 확인해 주세요.'),'recommendation':rec,'recommendation_basis':basis,'uncertainty':'임상 적용과 제품 선택은 검토하지 않았습니다. 원문 관계 확인 전 자동 대상 확정은 불가합니다.','resolution_kind':'후속 데이터 이관' if why=='out_of_batch_entity' else '원천 관계 확인 필요','transformation_note':'필드명 정규화는 기존 mapping에 기록되어 있으나 대상 확정 문제를 해결하지 않습니다.','claim':cl,'scope':scope,'mappings':ms,'mapping_ledger':[x for x in ledgers if x['mapping_ref'] in f['mapping_refs']] if ledgers and 'mapping_ref' in ledgers[0] else [x for x in ledgers if x.get('id') in f['mapping_refs']],'targets':targets,'raw_hash':sha(json.dumps(f['raw_value'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()),'source_hashes':{s:src[s]['source_sha256'] for s in f['source_refs']},'current_values':[{'source_ref':s,'value':src[s]['raw_value'].get('source_text',{}).get(f['raw_field']), 'present':f['raw_field'] in src[s]['raw_value'].get('source_text',{})} for s in groups[gid]['current_source_refs']]}
 cards.append(card);groups[gid]['card_ids'].append(card['id'])
assert len(cards)==152 and collections.Counter(x['attachment_reason'] for x in cards)=={'candidate_only':49,'out_of_batch_entity':83,'owner_unresolved':20}
assert len({x['id'] for x in cards})==152
meta={'schema_version':'silver-decisions/1','artifact_version':'silver-decision-cards/1','candidate_input_fingerprint':sha((CAND/'input-manifest.json').read_bytes()),'candidate_output_fingerprint':sha((CAND/'output-manifest.json').read_bytes()),'upstream_input_fingerprint':om['input_manifest_sha256'],'candidate_schema_version':r['record_schema_version'],'p5_status':'FAIL_미승인_검증기보완중','p5_note':'P5 최종 FAIL: scope 원문 의미 검사와 line 관계 삭제 탐지 누락. 현재 candidate 값과 미부착152필드 분류는 정상 확인됐으나 데이터판 적용은 미승인입니다.','p5_review_report':'../silver-batch1-review/report.md','p5_review_report_sha256':sha((BASE/'silver-batch1-review/report.md').read_bytes())}
data={'meta':meta,'counts':{'fields':len(cards),'groups':len(groups),'reasons':dict(collections.Counter(x['attachment_reason'] for x in cards))},'groups':list(groups.values()),'cards':cards,'sources':used_src,'identity_ledger':[x for x in identity if set(x['new_refs']) & {t['id'] for c in cards for t in c['targets']}],'candidate_coverage_summary':{'file':'../silver-batch1-candidate/coverage.json','sha256':sha((CAND/'coverage.json').read_bytes()),'keys':list(coverage)}}
write('cards.json',data)
# Export schema validates structure; UI additionally validates all identity/fingerprint/hash/target references.
props={'card_id':{'type':'string','enum':[c['id'] for c in cards]},'claim_ref':{'type':'string'},'scope_ref':{'type':'string'},'source_refs':{'type':'array','items':{'type':'string'},'uniqueItems':True},'source_hashes':{'type':'object','additionalProperties':{'type':'string','pattern':'^[a-f0-9]{64}$'}},'raw_hash':{'type':'string','pattern':'^[a-f0-9]{64}$'},'choice':{'enum':['','hold','source_check','defer','link_proposal']},'reason':{'type':'string'},'note':{'type':'string'},'text_proposal':{'type':'string'},'target_ref':{'type':['string','null']},'status':{'enum':['draft','reviewed']},'decided_at':{'type':['string','null'],'format':'date-time'}}
export_props={k:{'const':v} for k,v in meta.items() if k in ['schema_version','artifact_version','candidate_input_fingerprint','candidate_output_fingerprint']}
export_props.update({'exported_at':{'type':'string','format':'date-time'},'decisions':{'type':'array','maxItems':152,'items':{'type':'object','additionalProperties':False,'required':list(props),'properties':props}}})
item_rules=[]
for c in cards:
 exact={k:{'const':c[k]} for k in ['claim_ref','scope_ref','source_refs','source_hashes','raw_hash']}
 exact['target_ref']={'enum':[None]+[t['id'] for t in c['targets']]}
 item_rules.append({'if':{'properties':{'card_id':{'const':c['id']}}},'then':{'properties':exact}})
item_rules += [
 {'if':{'properties':{'choice':{'const':''}}},'then':{'properties':{'decided_at':{'type':'null'},'status':{'const':'draft'}}},'else':{'properties':{'decided_at':{'type':'string','format':'date-time'}}}},
 {'if':{'properties':{'choice':{'enum':['','hold','source_check','defer']}}},'then':{'properties':{'target_ref':{'type':'null'}}}},
 {'if':{'properties':{'status':{'const':'reviewed'}}},'then':{'properties':{'choice':{'enum':['hold','source_check','defer','link_proposal']},'reason':{'pattern':r'\S'}}}},
 {'if':{'properties':{'status':{'const':'reviewed'},'choice':{'const':'link_proposal'}}},'then':{'properties':{'target_ref':{'type':'string'}}}}
]
export_props['decisions']['items']['allOf']=item_rules
write('decision-schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','title':'결정 제안 JSON (반영 전)','type':'object','additionalProperties':False,'required':list(export_props),'properties':export_props,'$comment':'카드 ID 중복, 실제 ref/hash와 target 후보, 선택별 필수 근거, 기존 편집 충돌은 index.html의 validateBundle에서 추가 검사. reviewed는 이 UI의 검토 표시이며 clinical 승인이 아님.'})
template=(HERE/'template.html').read_text(); inline=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e').replace('\u2028','\\u2028').replace('\u2029','\\u2029');(HERE/'index.html').write_text(template.replace('/*INLINE_DATA*/',inline))
print(json.dumps(data['counts'],ensure_ascii=False))

# The issue-first UI supersedes the old field-picking template.
import runpy
runpy.run_path(str(HERE/"build-review.py"),run_name="__main__")
