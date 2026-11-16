"""Curated findings and proposed contract. Reads source; writes audit artifacts only."""
import collections
import hashlib
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
W=OUT.parent
RAW=Path('/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26')
J=lambda p: json.loads(p.read_text())
S5=J(W/'step5-units.json'); S7=J(W/'step7-concerns.json'); S8=J(W/'step8-relations.json'); S9=J(W/'step9-explanations.json')
PP=J(RAW/'problem-packages.json')
issues=[]
def ref(file,path,text):
    file=Path(file)
    if path.startswith(file.stem+'.'):
        path='$'+path[len(file.stem):]
    return {'file':str(file),'jsonpath':path,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'value':text}
def issue(id,stage,group,classification,certainty,origin,silver,rule,impact,metadata,fix,question,proposed=None):
    issues.append(dict(id=id,stage=stage,systemic_group=group,classification=classification,certainty=certainty,
                       origin=origin,silver=silver,transformation_rule=rule,impact=impact,required_metadata=metadata,
                       proposed_fix=fix,confirmation_question=question,proposed_record=proposed))

for i,c in enumerate(J(OUT/'normalization-collisions.json'),1):
    src={v['source_field']:v['value'] for v in c['sources']}
    issue(f'LOSS-{i:02}',5,'normalize-overwrite','silver_omission','confirmed',
          [ref(c['raw_file'],c['raw_path']+'.'+k,v) for k,v in src.items()],ref(W/'step5-units.json',c['silver_path']+"['safety.common']",c['current']),
          {'file':str(W/'step5-apply.py'),'lines':[613,620,629,648,664,674,699], 'decision':'$.extracted_rule.key_normalize','operation':'out[normalized_key]=value; last original key silently wins'},
          {'lost_original_leaves':c['lost_original_leaves'],'lost_leaf_count':len(c['lost_original_leaves']), 'record_id':c['record_id'], 'downstream':'source_text -> side_effect_override -> Gold facts; row-local loss, not proof each string absent everywhere'},
          ['source original field/path','normalization mapping record','one-to-many collision provenance'],
          '각 원천 필드를 독립 claim으로 보존하고 normalized predicate로 연결한다; common 목록을 자동 대체하지 않는다.',
          '원문값 복구에 임상 추정은 필요 없음; 두 목록의 관계/중복 통합 정책은 별도로 결정한다.',
          {'claims':[{'source_field':k,'raw_value':v,'normalized_predicate':'safety.common','mapping_state':'normalized','clinical_equivalence':'unreviewed'} for k,v in src.items()],'resolution':None})

for ci,rid,wrong in [(10,'R8-0366','P9-3'),(11,'R8-0367','P9-1')]:
    c=PP['problems'][8]['complaints'][ci]
    ix,row=next((i,r) for i,r in enumerate(S8['claims']) if r['id']==rid)
    issue(f'ANCHOR-{ci}',[7,8],'duplicate-cc-first-match','silver_misinterpretation','confirmed',
          ref(RAW/'problem-packages.json',f'$.problems[8].complaints[{ci}]',c),ref(W/'step8-relations.json',f'$.claims[{ix}]',row),
          {'file':str(W/'step7-apply.py'),'lines':[963,966,1186,1190,1249,1392], 'consumer':str(W/'step8-apply.py')+':820-824,1324-1380','operation':'correspondence narrows by detail; CC edge uses cands[0]; PID:CC identity omits row/group/detail'},
          {'expected_concern_from_original_group':'P9-4','actual_concern':wrong,'raw_procedure_rows':2,'relation':rid,'wrong_group':'튼살 -> '+wrong},
          ['source_record_id','snapshot+JSON pointer','cc_group','correspondence mapping id','scope concern id'],
          '원천 complaint 행마다 locator를 키로 사용하고 detail/group으로 이미 확인된 대응을 재사용한다; 중복 이름은 한 행으로 합치지 않는다.',
          '이 두 행의 원장 그룹은 명확하며 확인 없이 다른 그룹으로 옮길 근거가 없다; 원장 수정 의도가 있으면 원천 담당자가 별도로 답한다.',
          {'source_record':f'problem-packages:$.problems[8].complaints[{ci}]','source_scope':{'concern_group':'튼살','concern_ref':'P9-4'},'mapping_state':'source_structure','legacy_name_key':f"P9:{c['cc']}",'raw_claims_preserved':True})

raw_cb=[(pi,ci,bi,cb) for pi,p in enumerate(PP['problems']) for ci,c in enumerate(p['complaints']) for bi,cb in enumerate(c.get('combos') or [])]
notes=[(i,n) for i,n in enumerate(S7['step8_notes']) if n['source']=='problem-packages.complaints[].combos']
for (pi,ci,bi,cb),(ni,n) in zip(raw_cb,notes):
    if len(cb['combo'])!=1: continue
    issue(f'ARITY-{ni:03}',7,'singleton-pair-label','silver_representation','confirmed',
          ref(RAW/'problem-packages.json',f'$.problems[{pi}].complaints[{ci}].combos[{bi}]',cb),ref(W/'step7-concerns.json',f'$.step8_notes[{ni}]',n),
          {'file':str(W/'step7-apply.py'),'lines':[1817,1820],'consumer':str(W/'step8-apply.py')+':1358-1362','operation':'all raw combos labelled 시너지(쌍 주장); step8 correctly routes singleton to attrs'},
          '원장 구성원1개인 원문21행이 step7에서 쌍 주장으로 잘못 표시된다; step8은 이를 singleton 속성으로 분류하므로 쌍 임상 사실의 신규 생성이 입증된 것은 아니다.',
          ['relation arity','claim type','step8 destination reference'],
          'kind를 실제 arity와 맞추고 singleton은 단독속성으로, pair/n-ary는 구성과 생성 규칙을 명시한다.',
          '원장이 단독이라고 쓴 행이다; 시너지 상대를 새로 추가하지 않는다.',
          {'claim_type':'single_procedure_attribute','members_raw':cb['combo'],'relation':None,'mapping_state':'source_structure'})

row=S8['claims'][0]
issue('SCOPE-ORDER-01',8,'same-site-order-qualifier','silver_scope_metadata','confirmed',
      ref(RAW/'contraindications.json','$.rules[0]',J(RAW/'contraindications.json')['rules'][0]),ref(W/'step8-relations.json','$.claims[0]',row),
      {'file':str(W/'step8-apply.py'),'lines':[895,906,908],'operation':'first derived from interval+note; interval parser only receives interval text'},
      '동일 부위에서만의 순서와 다른 부위 순서 무관이라는 원문은 reason에 보존되나 interval.first=a, condition=null/options=null이다; structured first 단독 소비에 필요한 조건이 없다. 현재 staff_check 상태는 남아 있다.',
      ['per-field condition','same_site vs different_site','original clause locator','resolution status'],
      '같은 날 가능과 부위별 순서 주장을 분리한다; 조건 모름일 때 first를 확정하지 않는다.',
      '원문 조건은 명시돼 있어 새 임상 사실 불필요; 원천 상충은 별도 의료진 검토로 남긴다.',
      {'claims':[{'predicate':'same_day','raw_value':True},{'predicate':'first','value':'a','scope':{'site_relation':'same_site'}},{'predicate':'order_constraint','value':'none_stated_required','scope':{'site_relation':'different_site'}}],'resolution':{'state':'staff_check','approved_first':None}})

c=PP['problems'][1]['complaints'][3]
issue('ORIGIN-CC-01',[7,8],'palja-neck-source-conflict','origin_inconsistency','confirmed',
      ref(RAW/'problem-packages.json','$.problems[1].complaints[3]',c),ref(W/'step7-concerns.json','$.step8_notes[111]',S7['step8_notes'][111]),
      {'file':str(W/'step7-apply.py'),'lines':[1817,1820],'operation':'verbatim name/reason/evidence join'},
      '팔자주름 CC 안에 목주름 role/reason이 원장부터 존재한다; Silver 텍스트 오기라고 단정할 수 없다. CC 기반 attachment가 문장 자체의 부위 범위를 증명하지 않는다.',
      ['container_scope','statement_scope','scope_conflict','origin_question_id'],
      '팔자 컨테이너와 목주름 원문을 모두 보존하고 scope_conflict를 열어 원장 담당자에게 재확인한다.',
      '이 스킨부스터+리프팅 조합은 팔자 CC에 속하는가, 목주름 행을 잘못 복사한 것인가?')

for cid in ['RC-CP-volume','RC-CP-wrinkle']:
    ix,co=next((i,c) for i,c in enumerate(S7['combos']) if c['id']==cid)
    ri,raw=next((i,c) for i,c in enumerate(J(RAW/'procedure-comparison.json')['comparisons']) if c['id']==co['source_id'])
    mi=0 if cid.endswith('volume') else 1
    issue('CAND-'+co['source_id'],7,'comparison-candidate-scope','mapping_undetermined','confirmed_undetermined',
          ref(RAW/'procedure-comparison.json',f'$.comparisons[{ri}]',raw),ref(W/'step7-concerns.json',f'$.combos[{ix}].members[{mi}]',co['members'][mi]),
          {'file':str(W/'step7-apply.py'),'lines':[1780,1791],'operation':'member name resolver; text attrs stored separately; no exact member site approval'},
          'U5-082..089는 후보8개이며 확정 부위8개가 아니다; 비교 subtitle와 best_for 부위 원문은 존재하지만 비교 맥락/멤버 주장/개별 부위 적용을 나눠 표현하지 않는다.',
          ['mapping state','candidate set semantics','context scope','member field scope','source locator'],
          'member 후보군과 비교 앵커를 보존하고 candidate membership을 단독 unit 적용 승인으로 소비하지 못하게 한다.',
          'subtitle의 부위가 모든 멤버·모든 잎의 적용 범위인가? 원장에 없는 정확한 단독 부위는 미확정으로 둔다.',
          {'mapping':{'state':'candidate','candidates':co['members'][mi]['units'],'selected':None,'quantifier':'one_or_more_not_all_approved'},'context_raw':co['anchor']['subtitle'],'member_scope':{'knowledge':'unresolved'},'application_decision':None})

for ni,rid in zip([109,110,111,132,133,134,135],['R8-0277','R8-0278','R8-0279','R8-0298','R8-0299','R8-0300','R8-0301']):
    ci,c=next((i,c) for i,c in enumerate(S8['claims']) if c['id']==rid)
    loc=next(x for x in J(OUT/'step8-origin-locators.json') if x['id']==rid)
    issue(f'NOTE-LINK-{ni}',[7,8],'note-claim-lineage','silver_provenance_metadata','confirmed',
          ref(loc['source_file'],loc['source_path'],next(cb for pi,cj,bi,cb in raw_cb if loc['source_path']==f'$.problems[{pi}].complaints[{cj}].combos[{bi}]')),
          ref(W/'step7-concerns.json',f'$.step8_notes[{ni}]',S7['step8_notes'][ni]),
          {'file':str(W/'step7-apply.py'),'lines':[1820],'consumer':str(W/'step8-apply.py')+':1358-1380','operation':'step7 note stores flattened text; step8 independently emits canonical claim'},
          f'이 메모의 원천 pair/구성은 원장에 있고 {rid}도 이미 존재한다; 메모에 claim_refs와 exact 원문 locator가 없어 연결을 재발명하게 된다. 해당 pair 존재는 단독 unit 효과 승인과 별개다.',
          ['source_record_id','claim_refs','relation arity','attachment rule','applicability status'],
          f'동일 원문 locator로 {rid}와 연결하고 claim 양끝/조건을 재사용한다; text 유사도나 where만으로 승인하지 않는다.',
          '새 임상 pair 질문은 불필요; [111] 원천 부위 상충 등 명시 불일치는 별도 질문을 유지한다.',
          {'note_origin':loc,'claim_refs':[rid],'relation_endpoints':{'a':c['a'],'b':c['b']},'source_condition':c.get('condition'),'application_decision':None})

pi,pl=next((i,p) for i,p in enumerate(S5['product_links']) if p['product']=='auto-M4-1775361378128')
raw_tax=J(RAW/'taxonomy.json'); oi,os,op=next((i,j,k) for i,m in enumerate(raw_tax['modality']) for j,s in enumerate(m['subcategories']) for k,it in enumerate(s['items']) if it['id']==pl['product'])
issue('PRODUCT-SCOPE-01',5,'multi-family-override','silver_scope_metadata','confirmed',
      ref(RAW/'taxonomy.json',f'$.modality[{oi}].subcategories[{os}].items[{op}]',raw_tax['modality'][oi]['subcategories'][os]['items'][op]),ref(W/'step5-units.json',f'$.product_links[{pi}]',pl),
      {'file':str(W/'step5-apply.py'),'lines':[674,699],'operation':'product has M4 primary and M2 secondary; inherited candidates include M2 units but safety override_of remains family:M4'},
      'M2 후보 연결과 M4 범위 override는 서로 다르다; 저장44/상속1379쌍은 제품 선택 사건이나 모든 제품원문의 M2 승인 근거가 아니다. 기존276은 재집계한 결함 수가 아니다.',
      ['product+family scope','selected product state','override_of','inheritance evidence','fact attachment vs application'],
      '기존 override_of/priority/level을 유지하고 product mapping과 임상 주장 범위·실제 선택을 분리한다.',
      '이 M4 원문이 이 라인의 M2 허가 제품에도 적용되는가? 원천만으로 닫히지 않으면 미확정이다.',
      {'mapping':{'product':pl['product'],'candidate_units':pl['inherited_candidates'],'state':'compatible_candidate'},'claim_scope':{'family':'M4'},'selected_product':None,'apply_to_M2':'unknown'})

for rid in ['K8-0028','K8-0029']:
    ix,c=next((i,c) for i,c in enumerate(S8['conditions']['not_condition']) if c['id']==rid)
    loc=next(x for x in J(OUT/'step8-origin-locators.json') if x['id']==rid)
    issue('PROJECTION-'+rid,8,'K8-projection','gold_projection_metadata','confirmed_in_code',
          ref(loc['source_file'],loc['source_path']+'.label',c['text']),ref(W/'step8-relations.json',f'$.conditions.not_condition[{ix}]',c),
          {'file':str(RAW.parent/'phub-recommend/backend/app/modules/gold/build.py'),'lines':[774,783],'public_consumer':'app/modules/gold/tools.py:_walk_row'},
          '실버에 target family:M2, conditions:[], kind가 이미 존재한다; metadata를 보이지 않는 것은 실버 임상 원문 누락과 다르다. live API/DB 상태는 이번에 검증하지 않았다.',
          ['target','not_condition','conditions knowledge','source origin and canonical fact locator'],
          '추후 허용된 Gold 변경에서 이미 저장된 target/conditions/kind metadata를 보존해 소비하도록 계약을 정한다.',
          '의료 조건을 새로 만들 필요 없음; []는 이 원천 항목의 사람 조건 부재이며 위험 없음이 아니다.',
          {'claim_type':c['kind'],'target':c['target'],'conditions':{'knowledge':'not_applicable','included':[]},'source_claim_id':rid})

st=S8['evidence']['statements'][19]
lit=J(RAW/'literature-evidence.json')['categories']['M2']['adverse_effects'][2]
issue('PATIENT-LANG-01',8,'language-claim-variant','origin_qualifier_difference','confirmed',
      ref(RAW/'literature-evidence.json','$.categories.M2.adverse_effects[2]',lit),ref(W/'step8-relations.json','$.evidence.statements[19]',st),
      {'file':str(W/'step8-apply.py'),'operation':'statement/patient_{lang} values copied into statements.patient; Gold emits each leaf'},
      'patient.ko에 수개월 뒤 지연성이라는 한정이 있으나 statement와 다른 언어 잎에는 그 구절이 없다; 번역/동일 의미로 자동 접으면 한정이 사라진다. Silver는 원문을 보존했다.',
      ['language','variant_of','equivalence review status','qualifier original text'],
      '언어별 별도 claim variant로 보존하고 검토 없이 의미 동일/중복 제거하지 않는다.',
      'ko의 지연성 설명이 인용 statement의 승인된 보충인가? 이번에는 문헌을 새로 조회하지 않는다.')

ns=S9['node_slots'][280]
rec={r['id']:r for r in S9['records']}
issue('RESOLUTION-01',9,'source-claims-vs-policy-resolution','resolution_policy_visibility','confirmed',
      [ref(RAW/(rec[r]['source']['file']+'.json'),rec[r]['source']['path'],rec[r]['text']) for r in ns['records']],ref(W/'step9-explanations.json','$.node_slots[280]',ns),
      {'file':str(W/'step9-apply.py'),'lines':[375,401],'decision':'D9-3 ② 짧은 쪽'},
      '3-6개월과6-9개월 원문 둘 다 실버에 있으나 짧은 쪽만 emit된다; 이는 승인된 보수 규칙의 결과이지 새 원천 합의나 원장 정정이 아니다. 전체196②슬롯/343 alternatives가 같은 분리 원칙의 대상이다.',
      ['resolution rule/version','source claim IDs','alternatives','policy vs clinical review'],
      '원천 claim 집합과 resolved view를 별도 식별하고 resolved view만 내보낼 때 충돌·대안 존재를 표시한다.',
      '두 기간의 제품/횟수/조건 차이가 원장에 없는 경우 보수 선택과 임상 확인 상태를 분리한다.',
      {'source_claims':[{'id':r,'text':rec[r]['text']} for r in ns['records']],'resolution':{'rule':'D9-3','selection':'shorter_duration','selected':ns['resolved'],'alternatives':ns['alternatives'],'clinical_consensus':False}})

(OUT/'issues.json').write_text(json.dumps({'counting_rule':'Issue evidence rows, not independent clinical defects; systemic_group deduplicates causes; overlaps explicitly allowed; prior 9/326 not added', 'summary':dict(collections.Counter(i['classification'] for i in issues)),'issues':issues},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'issue_evidence_rows':len(issues),'classification_counts':dict(collections.Counter(i['classification'] for i in issues))},ensure_ascii=False))
