"""Build an issue-first review, without changing candidate or source data."""
import json, hashlib
from pathlib import Path
H=Path(__file__).resolve().parent
D=json.loads((H/'cards.json').read_text())
C={c['id']:c for c in D['cards']}
G={g['label']:g for g in D['groups']}
def sha(x):return hashlib.sha256(x).hexdigest()
def row(g):
 cs=[C[i] for i in g['card_ids']]; raw=D['sources'][g['row_source_ref']]; cur=[D['sources'][s] for s in g['current_source_refs']]
 targets=[]
 for t in cs[0]['targets']:
  proofs=[]
  for ref in t['source_refs']:
   s=D['sources'][ref];v=s['raw_value']
   proofs.append({'file':s['file'],'pointer':s['pointer'],'matching_ledger_entries':[x for x in v.get('sources',[]) if x.get('id')==g['native_id']],'key':v.get('key'),'notes':v.get('notes',[])})
  targets.append({**t,'proofs':proofs})
 return {'id':g['id'],'name':g['label'],'native_id':g['native_id'],'raw_context':{k:v for k,v in raw['raw_value'].items() if k!='extracted'},'raw_file':raw['file'],'raw_pointer':raw['pointer'],'silver_context':[{'file':s['file'],'pointer':s['pointer'],'value':{k:v for k,v in s['raw_value'].items() if k!='source_text'}} for s in cur],'targets':targets,'fields':[{'id':c['id'],'claim_ref':c['claim_ref'],'scope_ref':c['scope_ref'],'field':c['raw_field'],'value':c['raw_value'],'pointer':c['raw_pointer'],'source_refs':c['source_refs'],'raw_hash':c['raw_hash'],'current_values':c['current_values']} for c in cs]}
rows={g['label']:row(g) for g in D['groups']};issues=[]
def issue(id,title,kind,status,problem,facts,unknown,impact,plan,question,options,names,focus=None):
 rr=[rows[n] for n in names]
 issues.append(dict(id=id,title=title,kind=kind,status=status,problem=problem,facts=facts,unknown=unknown,impact=impact,plan=plan,question=question,options=[{'id':x,'label':y,'effect':z} for x,y,z in options],rows=rr,focus=focus or [],field_ids=sorted({f['id'] for r in rr for f in r['fields']})))
source_options=[('investigate','출처와 적용 범위부터 확인','담당자가 원문 작성 근거와 문장별 범위를 조사합니다. 내용이 맞다고 승인하는 선택이 아닙니다.'),('hold','이번에는 사용 보류 유지','해당 미확정 정보의 자동 적용을 보류합니다. 원문은 보존합니다.'),('comment','다른 처리 의견','아래 메모에 원하는 처리 방향을 적습니다.')]
issue('scope-hyperhidrosis','다한증 설명에 왜 교근 섬유화가 들어 있나?','source','문맥 불일치 의심 · 의학적 오류 확정 아님','겨드랑이·손·발을 설명하는 원문 행에 “교근 섬유화” 문장이 함께 들어 있습니다. 여러 시술에 연결되는 문제와 별개로, 이 문장이 이 행의 설명에 들어가야 하는지 확인할 필요가 있습니다.',['원문 이름: 다한증 / detail: 겨드랑이 · 손 · 발','safety.note 원문: 반복 시술 시 1.5% 정도의 교근 섬유화 가능성','aftercare에는 “수평 자세 유지 (겨드랑이 시술 시 팔 올린 상태 유지)”도 포함되어 있습니다.'],'교근 문장의 출처 및 다한증 항목에 포함한 이유, 겨드랑이 조건 문장이 손·발에도 적용되는지 미확인입니다.','범위를 나누지 않고 공통 설명으로 쓰면 손·발 시술 질문에도 겨드랑이 조건이나 교근 문장을 전달할 수 있습니다. 현재 서비스에서 실제로 이런 답변이 나왔다는 재현 결과는 아닙니다.','원문 작성 근거를 확인하고 공통/부위별 문장을 나누는 안을 조사합니다. 조사 전에는 수치 삭제·의학적 사실 확정·다른 부위로 이동하지 않습니다.','이 문장들의 출처와 부위별 적용 범위를 먼저 조사할까요?',source_options,['다한증'],['safety.note','aftercare'])
issue('scope-wrinkle','이마·미간 등 주름 묶음에 “교근 섬유화 1.5%”가 공통으로 들어 있음','source','문맥 확인 필요','이 원문은 이마·미간·눈가·자갈턱·콧등을 한 행에 담고 있지만, 장기 부작용 필드에는 특정 문장이 하나 들어 있습니다. 행 전체의 공통 정보인지 문장별 범위를 정해야 합니다.',['원문 detail: 이마 · 미간 · 눈가 · 자갈턱 · 콧등','safety.long_term 원문: 반복 시술 시 1.5% 교근 섬유화 위험'],'문장에 적힌 수치의 출처, 어느 시술에 해당하는지 이 자료만으로 확정하지 않았습니다.','다섯 시술에 일괄 적용하면 이마·미간 질문에도 이 문장이 공통 장기 부작용으로 나갈 수 있습니다.','원문 연결 5개는 보존하되 이 문장까지 5개 모두에 적용하는 것으로 승인하지 않습니다. 출처와 문장별 범위를 확인합니다.','이 장기 부작용 문장의 근거와 적용 대상을 확인할까요?',source_options,['주름'],['safety.long_term'])
issue('scope-neck','목주름·턱선 설명에도 같은 교근 문장이 들어 있음','source','문맥 확인 필요','목주름/턱선 행에 “교근 섬유화 위험(1.5%)”가 적혀 있습니다. 다른 행에도 비슷한 문장이 반복된 사실은 확인되지만, 잘못 복사된 것인지는 아직 확인하지 않았습니다.',['원문 이름: 목주름/턱선 / detail: 네페르티티 리프트','safety.note 원문: 반복 시술 시 교근 섬유화 위험(1.5%)'],'이 문장을 목·턱선 시술 설명에 포함한 원문 근거가 미확인입니다.','범위 없이 연결하면 목 시술의 부작용 답변에도 이 문장이 나갈 수 있습니다.','동일 문장 반복의 생성 경로와 원문 근거를 확인합니다. 확인 없이 삭제하거나 다른 시술로 옮기지 않습니다.','반복 문장의 출처를 조사할까요?',source_options,['목주름/턱선'],['safety.note'])
issue('scope-plla','실리프팅의 PLLA 행에 “주입부위·비가교HA” 설명이 섞여 있음','source','소재와 시술 방식 문맥 확인 필요','이 행은 실리프팅 후보 4개와 연결되어 있는데, 본문에는 “주입부위”, “육아종”, “비가교HA와 동시 사용 금기”가 적혀 있습니다. 이 설명이 PLLA 실을 말하는지 다른 PLLA 시술을 말하는지 확인이 필요합니다.',['기존 실버 후보: 얼굴 전체·코·목·턱선 실리프팅','safety.common: 주입부위 부종(3-5일)','safety.serious: 비가교HA와의 동시 사용 금기(24-72시간 분해 상충)','aftercare에는 PLLA 실 흡수 12-18개월 문장도 함께 있습니다.'],'실과 주입형 소재의 설명이 섞인 것인지, 각 문장의 근거가 무엇인지 미확인입니다. 표현만으로 의학적 오류를 확정하지 않습니다.','행 전체를 실리프팅에 붙이면 시술 방식이 다른 설명을 함께 전달할 가능성이 있습니다.','실리프팅 원문 문맥과 각 문장의 출처부터 대조합니다. 실/주입형을 이름만으로 합치거나 내용을 자동 수정하지 않습니다.','PLLA 설명의 출처와 시술 방식부터 확인할까요?',source_options,['PLLA'],['safety.common','safety.serious','aftercare'])
shared=['주름','다한증','입꼬리/잇몸미소/코끝','목주름/턱선','빼당주사']
for n in shared:
 r=rows[n]
 assert len(r['targets'])>1
 assert all(any(p['matching_ledger_entries'] for p in t['proofs']) for t in r['targets']),n
issue('shared-owner','여러 시술에 연결된 원문을 “대상 미확정”으로 묶은 것은 이관 규칙 문제','migration','복수 연결 근거 확인 · 문장별 적용 승인과 별개','5개 원문 행은 기존 실버에 여러 단위 시술의 연결이 명시돼 있고, 각 시술의 sources에도 같은 원문 ID가 기록돼 있습니다. 그런데 새 후보판은 단일 소유 대상을 고르지 못했다는 이유로 17개 필드의 연결을 만들지 않았습니다. 여러 연결이라는 사실만으로 사용자에게 하나를 고르라고 할 수 없습니다.',['5개 행 모두 기존 units 배열과 대상 시술의 ledger source ID를 서로 대조했습니다.','예: 주름 → 이마·미간·눈가·턱끝·콧등 보톡스 5개','현재 후보판: 이 5행의 17필드는 원문을 보존했지만 attachment가 없습니다.'],'기존 복수 연결은 확인됐습니다. 다만 각 부작용 문장이 연결된 모든 시술에 공통 적용된다는 임상적 의미까지 확인된 것은 아닙니다.','이 연결을 계속 누락한 채 사용하면 근거가 남아 있어도 해당 시술에서 정보를 찾지 못할 수 있습니다. 모든 문장을 통째로 배포하면 반대로 적용 범위를 넓힐 수 있습니다.','원문 기록과 복수 시술의 연결을 보존하는 이관 규칙으로 검토합니다. 문장별 적용 범위는 따로 유지하고, 위 문맥 확인 건은 자동 배포하지 않습니다. 하나만 고르는 UI는 없앱니다.','개별 부작용을 판정할 필요는 없습니다. 이 복수 연결 보존 방향에 이견이 있는지만 남겨 주세요.',[('proceed','복수 연결 보존 방향으로 진행','이관 규칙 보완과 검증을 진행합니다. 모든 문장을 모든 시술에 적용하라는 승인이 아닙니다.'),('hold','이관 규칙 변경 보류','원문과 기존 연결을 보존하며 새 연결 생성은 보류합니다.'),('comment','다른 구조 제안','원하는 연결 구조를 메모합니다.')],shared)
skin=rows['스킨보톡스'];assert not any(p['matching_ledger_entries'] for t in skin['targets'] for p in t['proofs'])
issue('skin-lineage','스킨보톡스는 후보 1개인데도 원문 ID로 연결 근거를 추적할 수 없음','lineage','연결 근거 단절 확인','기존 실버는 스킨보톡스를 U5-009에 연결한다고 적고 있습니다. 하지만 U5-009의 sources에는 이 원문 ID M4-P-3가 없습니다. 후보가 여러 개라서 막힌 경우가 아닙니다.',['원문 M4-P-3 note: 보톡스 희석 피내주사법 (별도 제품 아님)','기존 실버: attach=단위 시술, units=[U5-009], product=null','U5-009 source ID 목록에는 M4-P-3가 없습니다.','기존 실버 basis에는 원천 위치 M4와 계열 M1의 충돌 및 DEC-002 D-02를 근거로 기록했습니다.'],'기록된 결정 문서가 이 원문 행의 연결을 실제로 승인했는지 원문까지 대조하지 않았습니다. 이름이 비슷하다는 이유로 확정하지 않습니다.','연결을 포기하면 해당 원문 정보가 빠질 수 있고, 이름만으로 붙이면 결정 근거 없이 다른 항목 정보를 합칠 수 있습니다.','기존 basis에 명시된 결정 문서와 원문 ID를 대조해 누락인지 잘못된 연결인지 확인합니다. 확인되면 관계와 출처를 함께 보완하는 안을 만듭니다.','기존 결정 문서까지 추적해서 연결 근거를 복원할까요?',source_options,['스킨보톡스'])
for g in D['groups']:
 n=g['label'];c=C[g['card_ids'][0]]
 if c['attachment_reason']!='candidate_only':continue
 r=rows[n];ts=' · '.join(t['label'] for t in r['targets']);detail=r['raw_context'].get('detail') or '(원문 detail 없음)'
 if n in ['PDO','PCL','PLCL','PLLA','PCA실','PLLA+PCL복합실']:
  missing=f'원문은 “{n}”라는 소재/항목을 설명합니다. 후보는 부위별 실리프팅입니다. 이 소재를 쓰는 시술인지와 문장별 부위 범위를 구분할 근거를 더 확인해야 합니다.'
 elif n in ['코그(Cog)','모노','볼륨실']:
  missing=f'원문은 “{n}”라는 실의 형태/항목을 설명하고, 후보는 부위별 실리프팅입니다. 형태와 부위가 다른 축이므로 한 부위만 고르거나 전부 적용할 근거가 이 후보 목록만으로는 생기지 않습니다.'
 elif n in ['기타 엑소좀','줄기세포배양액','줄기세포유래 엑소좀']:
  missing='후보에 얼굴·두피 및 주입/도포 방식이 함께 있습니다. 원문 설명 중 어떤 문장이 어느 부위·방식에 적용되는지 후보 목록에는 확정되어 있지 않습니다.'
 elif n=='알렉산드라이트':
  missing='원문 detail은 “755nm 색소+제모”인데 후보에는 알렉스토닝과 프락셀이 있습니다. 파장/원리와 시술 방식이 다른 축이므로 이름만으로 둘 중 하나를 확정할 수 없습니다. 제모에 해당하는 대상이 이 목록에서 빠졌는지도 확인해야 합니다.'
 else:
  missing=f'원문은 “{n}”라는 명칭과 “{detail}”를 기록하고, 후보는 부위별 지방분해주사입니다. 명칭의 실제 구성과 부위별 사용 관계가 후보 목록에서 확정되지 않았습니다.'
 issue('candidate-'+g['native_id'],f'{n}: 아래 시술들은 확정 연결이 아니라 기존 후보 목록','candidate','기존 실버부터 후보 · 오류 확정 아님',missing,[f'원문 이름: {n} / detail: {detail}','기존 실버 attach=단위 시술 후보',f'기존 후보: {ts}',f'이번 후보판에서 보류된 필드: {len(r["fields"])}개. 원문 값은 보존되어 있습니다.'],'어느 후보를 선택할지뿐 아니라 복수 적용인지, 문장별 조건이 필요한지가 미확인입니다. 후보가 많다는 사실 자체는 오류가 아닙니다.',f'전부 연결하면 “{r["targets"][0]["label"]}”와 다른 부위/방식에도 같은 설명을 줄 수 있습니다. 전부 제외하면 관련 근거를 찾지 못할 수 있습니다. 이는 적용 시 예상 영향이며 현재 서비스 오류 재현 결과는 아닙니다.','기존 후보는 그대로 보존하고 원문·결정 근거로 실제 사용 관계와 문장별 범위를 조사합니다. 여기서 하나의 시술을 찍게 하지 않습니다.','이 후보 관계의 근거 조사를 진행할까요, 이번에는 보류할까요?',source_options,[n])
out=[g['label'] for g in D['groups'] if C[g['card_ids'][0]]['attachment_reason']=='out_of_batch_entity']
issue('out-of-batch','37개 행은 데이터 오류가 아니라 이번 이관 범위에서 제외된 자료','coverage','이관 범위 제외 확인 · 품질 오류 판정 아님','패키지·도포제·의약품 등 37개 원문 행, 83개 필드는 기존 실버에도 원문 보관으로 기록되어 있습니다. 이번 대상 엔티티 이관에 포함하지 않았다는 이유로 남은 것입니다. 83개를 각각 사용자가 수정할 문제로 내놓으면 안 됩니다.',['각 행의 기존 attach 값은 아래 목록에서 확인할 수 있습니다.','예: 풀페이스큐레이션 → 원문 보관(6단계 패키지)','예: 하이드로퀴논 → 원문 보관(값)','예: 이소트레티노인 → 원문 보관(시술 아님(다른 단계))'],'후속 범위에서 어떤 엔티티로 다룰지, 개별 내용의 임상적 정확성은 이번 목록에서 확정하지 않았습니다.','이 항목까지 질문에 답해야 한다면 현 범위로는 충분하지 않습니다. 다른 시술에 억지로 붙이면 설명의 주체가 바뀔 수 있습니다.','원문을 보존하고 별도 이관 범위로 묶습니다. 필요하다면 패키지/약물/홈케어 등 대상 종류부터 조사합니다. 83개 필드별 승인이나 내용 수정은 요구하지 않습니다.','이 37개도 다음 이관 범위에 포함할까요?',[('next_batch','후속 이관 범위에 포함','대상 종류와 관계를 조사하는 다음 작업에 포함합니다. 즉시 시술 정보로 배포하지 않습니다.'),('hold','현재 작업에서는 제외 유지','보존 자료로 두고 현재 이관 범위는 확대하지 않습니다.'),('comment','일부만 포함','메모에 필요한 항목 이름을 적습니다.')],out)
assert len(issues)==26,len(issues)
assert len({r['id'] for x in issues for r in x['rows']})==62
assert len({f for x in issues for f in x['field_ids']})==152
review={'version':'silver-issue-review/2','candidate':D['meta'],'issues':issues,'counts':{'issues':26,'source_rows':62,'fields':152,'categories':{'source':4,'migration':1,'lineage':1,'candidate':19,'coverage':1}},'source_cards_sha256':sha((H/'cards.json').read_bytes()),'notice':'원문/연결 구조 대조입니다. 의학적 사실을 검증한 결과가 아닙니다. 선택은 후속 처리 방향이며 원문 수정·임상 승인·정본 적용이 아닙니다.'}
# Fingerprint all issue explanations and input refs; choices are bound to this exact edition.
review['review_fingerprint']=sha(json.dumps(review,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
(H/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
inline=json.dumps(review,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('&','\\u0026')
discussion=json.loads((H/'discussion-notes.json').read_text()) if (H/'discussion-notes.json').exists() else {'review_fingerprint':review['review_fingerprint'],'issues':{}}
assert discussion['review_fingerprint']==review['review_fingerprint'], 'discussion notes refer to a different review edition'
discussion_inline=json.dumps(discussion,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('&','\\u0026')
(H/'index.html').write_text((H/'review-template.html').read_text().replace('/*REVIEW_DATA*/',inline).replace('/*DISCUSSION_NOTES*/',discussion_inline))
print(json.dumps(review['counts'],ensure_ascii=False))
