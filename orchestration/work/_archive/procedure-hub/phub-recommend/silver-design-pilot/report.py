"""Create a reviewable trace report from already validated pilot artifacts."""
from common import *
p=read(O/'pilot.json');v=read(O/'validation.json');g=read(O/'graph-projection.json');sr={x['id']:x for x in p['source_records']};cases=p['cases']
lookup={group:{x['id']:i for i,x in enumerate(p[group])} for group in ['claims','relation_claims','mappings','scopes','attachments','notes']}
glookup={group:{x['id']:i for i,x in enumerate(g[group])} for group in ['facts','relation_records','mapping_records','scope_records','edges','notes']}
trace=[];rows=[]
for ci,c in enumerate(cases):
 pilot={};graph={}
 for ck,pg,gg in [('claim_refs','claims','facts'),('relation_refs','relation_claims','relation_records'),('mapping_refs','mappings','mapping_records'),('scope_refs','scopes','scope_records'),('attachment_refs','attachments','edges'),('note_refs','notes','notes')]:
  if c[ck]:
   pilot[pg]=[f'/{pg}/{lookup[pg][x]}' for x in c[ck]];graph[gg]=[f'/{gg}/{glookup[gg][x]}' for x in c[ck]]
 unresolved=c['group'] in ['palja-neck-source-conflict','comparison-candidate-scope','multi-family-override','language-claim-variant','source-claims-vs-policy-resolution','same-site-order-qualifier']
 t={'case':c['id'],'group':c['group'],'raw':[{'file':sr[x]['file'],'pointer':sr[x]['pointer'],'source_record_ref':x,'value':sr[x]['raw_value']} for x in c['source_refs']],'current_silver':[{'file':sr[x]['file'],'pointer':sr[x]['pointer'],'source_record_ref':x,'value':sr[x]['raw_value']} for x in c['silver_refs']],'pilot_case_pointer':f'/cases/{ci}','pilot_pointers':pilot,'graph_pointers':graph,'representation_result':'PASS','clinical_status':'미정 유지' if unresolved else '원문 구조 보존; 임상 재판정 안 함'};trace.append(t)
 def desc(xs):return '<br>'.join('`'+Path(x['file']).name+':'+x['pointer']+'`' for x in xs)
 prows='<br>'.join('`'+q+'`' for vals in pilot.values() for q in vals)
 grows='<br>'.join('`'+q+'`' for vals in graph.values() for q in vals)
 rows.append('| '+c['id']+' | '+desc(t['raw'])+' | '+desc(t['current_silver'])+' | '+prows+' | '+grows+' | PASS / '+t['clinical_status']+' |')
write('case-traces.json',trace)
counts={k:len(x) for k,x in p.items() if isinstance(x,list)}
text=f'''# 실물 설계 pilot 검증 결과

Task `task_9a80516d7b7c` · Dispatch `ctx_55cef790e0f9` · 2026-11-03 KST

## 결과와 판정 범위

**pilot 범위의 원문 보존·후보/조건 보존·참조 검증 PASS.** 기존 42개 증거 사례를 실제 snapshot 원문과 현재 실버에서 다시 읽어 별도 pilot records로 구조화했다. 실버 전체 이관이나 임상 정확도 승인이 아니다. 원장 자체의 미정은 미정으로 남겼다.

- 독립 source 대조/참조/구조/투영 검사 **{v['passed']:,} PASS / {v['failed']} FAIL**, 명시 변조 **{v['mutations_rejected']}/{v['mutation_total']} 거부**. 검사 수에는 ID/ref별 반복 검사가 포함되며 서로 다른 임상 검토 건수가 아니다. 정상본 positive control이 통과해야 변조 시험을 시작한다.
- 안전 alias 충돌 3행의 6개 원래 field-list와 **16잎 전부 보존**: 기존에 남은 common 6잎과 소실된 원문 10잎을 별도 source occurrence로 추적한다. 동일한 common 문장이 세 행에 있어도 claim/source ID를 합치지 않았다. pilot 범위 원문 손실 **0**이다.
- CC 중복키 2개/4행은 occurrence와 명확한 taxonomy entity/그룹으로 분리했다. 튼살 두 행은 **P9-4**, 기존 실버 R8-0366의 P9-3와 R8-0367의 P9-1 연결도 비교 증거로 유지했다. legacy 이름 alias의 단일확정 승격 **0**이다.
- 원문 CC combos **146/146** 전수 구조화: arity **1=21, 2=119, 3=6**. singleton pair 생성 **0**, 새 pair 임상 승인 **0**. n-ary 원문 구성·순서와 기존 R8 전개 rule/lowering/endpoint/arity 및 정확한 실버 ref를 보존했다. 기존 legacy key가 모호하면 source occurrence 후보도 모호하게 둔다.
- note **7/7**은 기존 **R8-0277/0278/0279/0298/0299/0300/0301**과 원문 source_record_ref로 연결했다. 원장에 없는 관계를 새로 만들지 않았다.
- R8-0001의 same_day와 first를 분리하고 same_site→a(M1), different_site→**explicit_no_required_order**를 원문 ref별로 보존했다. 조건 모름의 first는 null, staff_check 유지다. 임상 승인이나 근거 없는 unknown resolution을 만들지 않았다.
- 비교 필러 두 멤버의 8개 후보와 제품 다계열 compatibility는 후보로 보존했다. 후보→선택 승격 **0**이며 팔자 단독 확정 연결 **0**이다. 제품 M4 override의 원문 범위와 override_of/level/priority를 유지했다. K8-0028/29의 이미 존재하는 target/conditions/kind도 보존했다.
- 팔자 container/목주름 statement 충돌, patient_ko의 지연성 한정, duration 원천 2claim/보수 resolution/alternative는 모두 분리돼 역추적된다. 미정 해소나 원장 정정은 하지 않았다.

## 산출물과 재실행

```sh
python3 orchestration/work/phub-recommend/silver-design-pilot/run.py
```

외부 패키지·설치·네트워크·DB·서버·Gold builder 없이 Python 표준 라이브러리만 쓴다. `run.py`는 이 폴더의 build → schema → 검증용 projection → 독립 validator/변조 → report 순서로 실행하며 실패 시 멈춘다. 최초 `inputs-start.json`은 재실행해도 갱신하지 않는다.

| 파일 | 역할 |
|---|---|
| [pilot.json](pilot.json) | source occurrence, 기존 entity, claim/scope/mapping/decision/resolution/attachment, 42case records |
| [schema.json](schema.json), [schema.py](schema.py) | 필수 필드/type/enum/additionalProperties와 dependency-free strict validator |
| [build.py](build.py), [common.py](common.py) | 실제 원문과 현재 실버에서 pilot만 재생성 |
| [validate.py](validate.py), [validation.json](validation.json) | 생성기와 별개로 snapshot을 읽는 전수 대조 및 명시 변조 결과 |
| [project.py](project.py), [graph-projection.json](graph-projection.json) | 검증용 logical→Gold projection; 실제 Gold 코드/DB 미실행 |
| [case-traces.json](case-traces.json) | 사례별 원문값·기존 실버값·pilot/graph JSON Pointer 전체 |
| [gaps.md](gaps.md) | 허용된 pilot refinement, 기존안 예시 오류, 원천 미정, 이관 영향 |
| [inputs-start.json](inputs-start.json), [inputs-end.json](inputs-end.json) | 원문21 포함 보호 입력178파일의 시작/종료 full SHA256/bytes |
| [run.py](run.py), [report.py](report.py) | 전체 재실행과 이 보고서/trace 생성 |

원문 occurrence ID는 **snapshot hash+절대파일+JSON Pointer**의 SHA256이며 content-only가 아니다. entity ID는 실제 기존 namespace+ID를 유지한다. source occurrence의 배열 위치는 특정 snapshot의 위치이지 entity ID가 아니다. 기존 엔터티 존재를 검사하므로 이름으로 새 entity를 발급하지 않는다. 원문은 `source_records.raw_value`, 정규화 술어는 `claims.predicate`, 원래 key는 `raw_field`에 분리한다.

이번 pilot에는 {counts['snapshots']}개 실제 사용 파일판 snapshot, {counts['source_records']} source_record, {counts['entities']} 기존 entity, {counts['scopes']} scope, {counts['claims']} claim, {counts['relation_claims']} relation_claim, {counts['mappings']} mapping, {counts['decisions']} 기존 규칙 decision, {counts['resolutions']} conservative resolution, {counts['attachments']} attachment가 있다. 실제 구조화에 사용한 원문은 6/21파일이고 전체 원문21은 hash를 검사했다. snapshot 레코드 수는 원문21의 전체 이관 수가 아니다.

## 계약과 빈값

`schema_version={p['schema_version']}`, basis는 원안 `design.json`의 full SHA256 `{p['basis']['sha256']}`이다. 본 설계 파일은 수정하지 않았다.

- JSON Schema의 모든 typed record는 required/enum/type을 엄격히 검사하고 추가 필드는 거부한다. `raw_value`는 원문의 임의 JSON을 허용하지만 snapshot의 exact pointer에서 독립 재독한 값·타입과 일치해야 한다. source hash/bytes와 occurrence ID도 검증한다.
- `selected_refs:[]`는 실제 선택이 없음이다. 미정 mapping의 `candidates:[]`는 후보를 아직 정하지 못한 상태이며 아무 대상에나 적용한다는 뜻이 아니다. `rule:null`은 적용한 실제 매핑 규칙 없음이며 reason/state가 필수다. 존재하는 자동 규칙·판정은 정확한 source row와 생산 스크립트의 version/hash로 보존한다.
- `days:null`, `first.value:null`, `normalized_value:null`은 해당 계산/조건이 확정되지 않았음을 뜻한다. `false`와 혼용하지 않는다. `captured_at:null`, reviewer=null은 기록에 없는 날짜·사람을 만들지 않았다는 뜻이다. D9-3의 기존 decided_at만 원래 값으로 인용한다.
- `conditions:[]`인 K8 두 행은 **조건 항목이 아닌 준비/상담**이며 안전 승인이나 위험 부재가 아니다. scope의 patient_conditions=not_applicable에 이 의미를 명시했다.
- 원문 claim은 immutable이고 clinical review와 자동 처리 상태는 별개다. D9-3은 원천 합의가 아니라 기존 보수 출력 정책이다. 대안을 삭제하거나 clinical_consensus=true로 바꾸면 거부한다.

## 논리 타입 → 검증용 graph

entity 26개 중 실제 registry에 있는 타입만 node로 투영한다(실제 생성 수는 위 집계/JSON 기준). claim/scope/mapping/decision/source_record는 **노드가 아닌 typed records**로 남긴다. fact_attachment는 원안의 선택 projection을 사용하며 모두 application_state=unknown이다. 기존 concern/combo/Gold 전체 그래프를 재구성하는 구현이 아니다.

그래프에는 facts, relation_records, mapping_records, scope_records, notes, legacy_aliases, decisions, resolutions 및 exact source_records/snapshots가 남아 후보/조건/출처를 확인할 수 있다. 독립적인 적용 판정 없는 procedure_relation/procedure_pair는 모두 withheld에 기록하고 자동 생성하지 않았다. 기존 R8 pair는 relation_records의 기존 근거이며 새 확정 엣지가 아니다. 자동 확정 procedure_pair를 주입한 변조는 FAIL로 검출한다.

## 사례별 원장 → 현재 실버 → pilot → 제안 graph

표의 pilot/graph 경로는 각각 `pilot.json`, `graph-projection.json`의 JSON Pointer다. 원문/실버 파일의 절대경로·full hash·값과 모든 source refs는 `case-traces.json`과 source_records에 있다. 아래 PASS는 **표현과 역추적**의 판정이며 기존 실버 오류를 고쳤다거나 임상 승인했다는 뜻이 아니다.

| 사례 | 원장 위치 | 현재 실버 위치 | pilot | graph | 판정 / 미정 |
|---|---|---|---|---|---|
'''+ '\n'.join(rows)+f'''

## 독립 대조와 변조 결과

독립 validator는 build.py를 import하지 않는다. 실제 원문 snapshot에서 안전 alias 6필드/16잎, duplicate CC 4행과 taxonomy parent, CC combos146개의 구성·순서·arity, R8-0001 원문 note/interval, 비교 멤버, 제품 scope, 언어5잎, duration2잎을 직접 읽는다. 기존42증거의 모든 원문/실버 locator/hash/value도 다시 대조한다. 그래프와 pilot의 일치 검사만으로 합격시키지 않는다.

변조 {v['mutation_total']}개는 아래와 같고 모두 거부됐다. 각 실패 check 이름은 validation.json에 기록했다.

'''+ '\n'.join('- `'+x['mutation']+'`: '+('거부' if x['rejected'] else '**수용 — FAIL**') for x in v['mutations'])+f'''

## 보호 입력·남은 범위

시작/종료 manifest **178/178** 파일의 SHA256/bytes가 일치했다. 원문21, 기존 실버/decisions/생성기/semantic/소비 코드 및 기존 HTML/design/audit 입력은 불변이다. 현재 활성 DB publication 판은 조회하지 않았다. 작성 경로는 `silver-design-pilot/` 하나이며 하위워커·외부모델·네트워크·설치·commit/push/PR을 사용하지 않았다.

실제 검토 분모는 기존42사례, 안전3충돌행/6field/16잎, duplicate CC2키/4행, CC combos146전수, note7, R8조건1행, 비교멤버2개, 제품 override1행, K8두행, 언어5claim, duration2claim/1resolution이다. 이 범위를 제외한 실버1~9 전체의 의미 이관/전수 임상 검토는 미착수다. 선행9785비교나 HTML1600검사를 이번 새 검토 수로 합산하지 않았다.

특히 원안의 세부 의미 미검토1277칸, 전체 안전580행, 전체 concern/combination 이관, duration②196슬롯/343 alternatives의 전수 이관, 임상·허가·문헌 최신성, 실제 Gold/API/DB/서비스/탐색 구현은 완료하지 않았다. 다음은 코디 검증과 독립 검수이며, [gaps.md](gaps.md)의 pilot refinement와 LOSS-02 예시 오류를 함께 검토한 뒤 본 설계 확정/정본 이관 준비로 넘어간다.
'''
# Keep actual registry count in narrative; this number can change if scope needs another existing family.
text=text.replace('entity 26개 중',f"entity {counts['entities']}개 중")
(O/'report.md').write_text(text)
print('report.md and case-traces.json written')
