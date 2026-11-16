---
type: work
id: WORK-012
title: "case3 질문별 반복 탐색·근거 선별·전달 검증"
status: todo
product: procedure-hub
feature: phub-recommend
work_type: change
owner: "clinic_chat backend 워커(코디 발주)"
progress: 0
created_at: 2026-11-02
updated_at: 2026-11-03
depends_on:
  - "SPEC-006 0.3.15 §3-4-1-5~9 / SPEC-005 0.3.10 §5-16-1"
  - "WORK-011 WP12-H 공개 projection 구현·검증 인계(WP12-A 선행)"
  - "WORK-011 §5-5 선택 관계·전역 메모 공개 계약 및 §6-9 검증 완료(관계 어댑터 WP-4 선행)"
links:
  spec: "orchestration/work/phub-recommend/SPEC-006.md 0.3.15 §3-4-1-5~9 · §3-4-7 · §4 · §7-10"
  hub: "orchestration/work/phub-recommend/WORK-011.md"
  review: "orchestration/work/phub-recommend/review-info-absence-work011012.md (이전 0.3.9판 검수; 재검수 필요)"
---

# 앱 case3 수집·전달 분리

SPEC-006 **0.3.15 §3-4-1-9가 active scope 적용·완료의 현행 정본**이고, 노드 갈래 선택은 §3-4-1-7(0.3.13 primitive 정정 포함), 자연어 검증·전달은 §3-4-1-8을 따른다. §3-4-1-5의 수집 원장·전달/범위 검증 계약은 유지한다. §3-4-1-6의 page마다 Jev 단일 선택은 실패한 0.3.11 실행 기록이다. SPEC 0.3.8/0.3.9와 이 WORK의 이전 판에 적힌 초기 4걸음 전체 상한, 안전 8KB·일반 20KB·원문 15KB 장부, 예산 80%·Jev `enough`, 응답 초과 전체 배제는 당시 실행/설계 기록일 뿐 새 코드의 종료·누락 조건이 아니다. Jev는 의도·시작점에 이어 새 그래프 노드 후보 묶음의 관련성과 종료를 판단한다. 동일 노드 내부의 필요한 facet/page 진행은 앱이 담당한다. 앱은 유효한 후보·근거/적용 범위·필수 안전·부재 증명만 결정론적으로 검증한다. WP-1~10의 구현 여부 문장은 당시 계획/실행 기록이며 WP12의 수락 증거가 아니다. 현재 잔여 범위와 직렬 관문은 아래 WP12가 소유한다. T4만으로 WORK-011 관계 충족을 증명하지 않는다.

## 범위와 의존

- 코드 레포는 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`. 착수 때 HEAD·작업 상태·Hub build hash를 기록한다. 앱과 실제 서버/Gold build를 HEAD로 추정하지 않는다. 이 문서 작업에서는 앱 코드·서버·DB·평가 기록을 수정하지 않는다.
- 원천/Gold에 없는 사실을 생성하거나 질문별 Gold 정답 ID로 페이지에 점프하지 않는다. 동일 질문의 모든 명시 대상과 필수 facet, 관련 안전 항목을 추적한다. 이웃 선택은 Jev가 하되 다음 선택지가 있으면 초기 4걸음 뒤에도 순회한다.
- Hub의 `expand(page)`는 기존 페이지 계약을 사용한다. WORK-011의 선택 관계 API·전역 메모 경로와 §6-9 코드·격리 fixture PASS를 코디가 확인·인계한 뒤 WP-4 코드를 착수한다. [공개 계약 인계](WORK-011-public-contract-handoff.md)의 build·응답을 기준으로 구현하고, 실제 서버·앱 동일 build hash는 기능 활성화 전 관문으로 둔다. `pair_scope`, claim/대안별 source·`applies_to`, 방향, Q139 `global_claims/scope_complete`가 없으면 관계 facet 지원 완료 금지. 현재 T4 `sections=all`, 묶인 pairs, `pairs_more_n`은 증거가 아니다.
- 사용자 포트 18005/3700/3800/8700/8800/54329, `procedure-*` 컨테이너 비조작. Hub build가 섞인 동안 성능 측정 금지. 239×3은 고정 50 결과와 사용자 승격 판단 뒤 별도 발주.

## 종료·선별 계약

아래 0.3.10 당시 frontier 기술 중 Jev의 개별 section/page 선택은 §3-4-1-7의 0.3.13 Noul 정정으로 대체됐다. 현행 선택 단위는 노드 후보 묶음이며, active context 완료는 §3-4-1-9/WP12를 우선한다.

1. `question_targets[]{target_key,span,role,candidate_ids,selected_id?,status,basis,required_sections,required_facets}`를 만들고 명시 양쪽(I-06)·비교 방향·안전 checks/site_caution/safety.management 및 관련 위험·금기·고지를 추적한다. 경쟁 동의어 후보를 전부 필수 대상으로 삼지 않고 모호성은 `ambiguous`로 둔다. Q067.2/Q099.1 대상 동일성도 미확정이다.
2. `frontier`는 node/neighbor 종류·목록의 다음 묶음/`(node,section,page)`/확정 pair·전역 메모 범위로 관리한다. build+정규화 요청 tuple과 방문 집합으로 중복 호출을 막는다. 앱은 안전·명시 target seed와 미지원 facet의 관련 후보를 보존해 Jev에 우선 제시하고, Jev가 각 순회의 node/section/page 후보 또는 종료를 고른다. `more`는 다음 page의 후보 자격일 뿐 자동 호출 명령이 아니다. 지원된 facet의 뒤 page는 취소하고 미지원 facet의 뒤 page는 후보로 남긴다. page만 전진해도 진전으로 센다. 4걸음은 초기 탐색 기본값이고 전체 hard stop이 아니다. 고정 category 바이트 장부나 Noul/80%가 탐색을 막지 않는다.
3. 각 필수 target/facet/안전 항목은 필요한 인용 가능 fact·출처·적용 범위·고지가 확인되면 `received_supported`로 닫는다. 지원 뒤 무관한 이웃·마지막 page는 더 읽지 않고 `not_required`와 이유를 남긴다. **부재 판정**에는 해당 node/section 마지막 page `more=0` 또는 완료 `empty`, 필요한 이웃·pair·global 범위의 완료 증거가 필수다. `frontier_exhausted`와 부재 범위의 `lookup_complete`를 따로 판정한다. 모든 필수 대상·facet·안전 항목이 지원 또는 완료 조회에 근거한 정당한 부재로 닫히고 미지원 필수 frontier가 남지 않아야 `complete/enough`다. 후보가 소진돼도 필수 미조회 범위가 있으면 `incomplete`, 실제 deadline/timeout/도구 오류/컨텍스트 제한이면 `blocked/incomplete`다. 동일 frontier 반복·`more` 모순은 `no_progress`로 닫는다. 미완료를 원장 전체의 사실 부재로 말하지 않는다. 자동 동일 tuple 재시도는 0회.
4. 수집 원장에는 모든 응답의 fact ID·원문·source·flags·scope·page·`more`·실제 compact bytes·ms·선별 사유를 남긴다. cut fact는 `expand(fact_ids)` 원문 조회 뒤에만 인용한다. Claude에는 질문 target/facet 관련 인용 가능 원문과 출처, 필수 안전 fact·고지, 적용 범위가 맞는 관계 주장/대안만 ID·scope 중복 제거 후 준다. 탈락 fact도 원장에 남긴다. 분할이 필요하면 facet별 묶음의 ID/출처를 보존해 대조·병합하고 처리 실패 범위를 `incomplete`로 남긴다. 입력 cap 절단으로 사실을 조용히 버리지 않는다. `retrieval_limits`는 의료 출처가 아니다.
5. 코드 워커는 기존 클라이언트 기본값과 격리 측정치를 근거로 전체 deadline·호출 timeout을 설정하고 값·근거·`blocked` 분포를 보고한다. 모델 컨텍스트는 사용 provider의 실제 한도로 검증한다. 10초/2초는 이전 미승인 추천값으로 현행 요구가 아니다. 제한 도달은 `blocked/incomplete`이고 사실 부재가 아니다. 7초 TTFT 목표를 근거 수집 중단 조건으로 쓰지 않는다. 큰 입력의 선별·분할과 추가 순회의 시간·품질을 고정 50에서 함께 보고한다.

## WP·코드 표면·시험

| WP | 계획 코드 표면 | 구현 및 검증 증거 |
|---|---|---|
| 0 기준·fixture | `clinic_chat/cases/case3.py`, `clinic_chat/clients/hub_rest.py`, `clinic_chat/config.py`, `tests/fake_hub/*`, `tests/phase8/test_case3_walk.py` 읽기 | HEAD/status/build 기록, 기존 `sample50-questions.txt` QID·baseline 고정. `rg -n 'taken|fill|enough|expand\(|pair_check|walk_byte_budget' clinic_chat tests`로 현 구현 차이를 남긴다. |
| 1 질문 대상·안전 범위 | `clinic_chat/cases/case3.py`, 실제 `clinic_chat/jev/*` 후보 파서, `tests/fake_jev.py`, `tests/phase8/test_case3_walk.py` | span/role/후보/선택 근거와 target별 facet·안전 필수 목록. 명시 seed 우선, 동일 node의 target provenance 유지. Q015/Q072 queue, Q069/Q173 resolve 재생. |
| 2 반복 frontier·page | `clinic_chat/cases/case3.py`, `clinic_chat/clients/hub_rest.py`, `clinic_chat/config.py`, `tests/fake_hub/*`, `tests/phase8/test_case3_walk.py` | node/neighbor/section/page/pair tuple 방문·pending·완료 상태. 초기 4걸음 뒤 필수 근거가 비면 추가 순회, `more` 2~7쪽, 무진전/반복/오류 종료. 186 첫 쪽 ID 순서 보존, Q085/Q098/Q136/Q160 뒤쪽 ID 재생. 앞 page에서 필요한 지원 사실을 찾으면 무관한 뒤 page를 `not_required`로 닫고, 뒤 page에서만 지원되면 계속 걷는 두 시험을 추가한다. |
| 3 상태·운영 한계 | `clinic_chat/cases/case3.py`, `clinic_chat/config.py`, `clinic_chat/runner.py`, `tests/phase8/test_case3_walk.py`, `tests/phase4/test_timing_runs.py` | `received_supported|unresolved_absence|ambiguous|blocked`와 `frontier_exhausted|lookup_complete|complete|incomplete`; 부재 판정은 `more=0` 및 필요한 이웃/pair/global 범위 완료를 증명한다. 미지원 필수 frontier가 남으면 `incomplete` 시험. 예산·Noul·4걸음 단독 종료 금지. 가짜 시계/timeout/context-limit/도구 오류와 동일 tuple 자동 재시도 0회 시험. 운영 시간값은 기존 기본값·격리 측정으로 정하고 보고한다. |
| 4 관계 어댑터(Hub 관문 뒤) | `clinic_chat/clients/hub_rest.py`, `clinic_chat/cases/case3.py`, `tests/fake_hub/*`, `tests/phase8/test_case3_walk.py` | WORK-011 공개 schema로 확정 단위 쌍만 중복 제거 조회. `a/b` 방향, `pair_scope.complete`, claim/대안별 fact/source/적용 범위, Q139 별도 전역 메모. Q018/Q064/Q139/Q173 5문장/4질문 개별 재생; Hub 미완료/잘림은 미지원. |
| 5 수집 원장·Claude 선별/분할 | `clinic_chat/cases/case3.py`, `clinic_chat/runner.py`, `prompts/case3.md`, `clinic_chat/verify_runs.py`, `clinic_chat/report.py`, `clinic_chat/rerun_report.py`, `tests/phase8/*`, `tests/cli/*` | 수집 전체와 전달 선택을 별도 trace. 관련 원문·출처·안전·관계 scope만 전달, 탈락 ID/사유 보존. 큰 입력 facet 묶음·분할 병합/미처리 `incomplete`. Q004/Q237 복합 원인, Q004.1 전달 뒤 답, Q021/Q058/Q122 부분 답, Q017/Q050/Q147 인접 근거 전이 금지 재생. |
| 6 검증·50 준비 | `clinic_chat/verify_runs.py`, `clinic_chat/rerun_report.py`, `tests/phase8/*`, `tests/cli/*`; 보고 산출은 레포 밖 | tuple/page 누락·동일 Gold ID 본문 불일치·수집→전달 누락·미지원 enough·안전/고지 누락·scope 전이·분할 유실 FAIL. 동일 build/commit 새 실행 내부 결정론 두 번 대조. 고정 50 QID baseline 짝 비교, 누락/오류/timeout도 50 분모. |
| 7 실물 과탐색 보정 | `clinic_chat/cases/case3.py`, `tests/phase8/test_case3_walk.py`, 필요시 검증기·보고기 | 11-02 격리 Q002에서 4,329 Hub 요청·수신 13.58MB·Claude 전달 2.06MB(4,025 facts/153 owners)·CLI `$1` 한도 실패. Q001 일반 표현 `주름이`가 5개 단위 시술의 명시 target으로 오인되어 모호 판정. I-01의 부위·고민 anchor와 명시 시술 target 분리, 직접 추천 관계의 갈래별 frontier, 해당 갈래·조건·안전 section만 조회, 불필요한 형제 unit 전파 금지. 선택 fact를 질문의 답변 계획·안전 고지에 필요한 출처로 묶고 답변에서 전달 ID 전부 인용 강제 금지. 완료·부재 증거와 제외 사유 유지. Q001/Q002/Q004/Q006 새 smoke에서 구조적 완료·CLI 정상 답변·Q002 네 갈래 출처, 호출/bytes/TTFT를 보고한 뒤에만 새 50배치. |
| 8 Q002 답변용 근거·안전·검증 | `clinic_chat/cases/case3.py`, `prompts/case3.md`, `tests/phase8/test_case3_walk.py`, 필요시 검증기 | 11-02 실물 Q002는 네 관계 역할 전달 PASS지만 75 fact·112 facet·15 target/첫 입력 77.7KB, 답 검증 두 번 실패, 부분 답 안전·관련성 FAIL. 동일 unit의 중복 branch를 답변에서 합치고 역할 edge는 각각 보존한다. 다른 complaint overview를 빼고 질문 범위의 이름/역할/필수 안전만 묶는다. unit을 통해 받은 family/site_caution/check/disclosure의 적용 경로를 Gold 관계·owner/source/조건으로 증명해 선택한다. 임상 주장 제목에는 인용, 순수 문진·안내에는 비임상 판정, 재작성에는 실패 문장·이유·사용 가능 근거를 보낸다. 재작성 실패 시 raw fact 나열 금지. 네 역할+필러 부위 위험/검증된 보톡스 제한 근거, 인접 complaint 배제, 안전/관련성/인용 통과를 단일 Q002 실물 관문으로 확인한 뒤 대표 4문항, 그 뒤 고정 50으로 간다. |
| 9 Jev 동적 frontier·종료 | `clinic_chat/cases/case3.py`, Jev choice 어댑터/질문, `tests/fake_jev.py`, `tests/phase8/test_case3_walk.py` | Q002 답 관문 보수 후에도 290 Hub 호출·133개 side effects page·1.54MB 수신. SPEC-006 0.3.11 §3-4-1-6에 따라 **매 frontier에서 Jev가 질문과 후보의 관련성, 확장할 노드/section/page 또는 종료를 선택**한다. 앱은 허용된 typed edge·ID/build/source/scope/방향과 필수 target×facet/안전 완료를 검증한다. 지원된 facet의 뒤 page는 `not_required`, 미지원 facet만 동적으로 깊게 탐색, 부재 주장 facet만 허용 범위 끝까지 증명한다. Jev 조기 종료·무효 ID·반복 선택은 성공으로 세지 않는다. Q002 역할 edge 4개는 얕게 평가하되 7 unit 전수 페이지는 금지. 명시 두 target·뒤 page 유일 근거·조건부 위험·진짜 부재·deadline/오류와 I-02~I-08 회귀. 같은 Gold Q002 단일 실물에서 호출/bytes/TTFT와 답 인용·안전·관련성을 함께 검증한 뒤 대표 4문항, 고정 50 순서. |
| 10 Jev 노드 묶음 선택·facet 페이지 종료(9 수정) | `clinic_chat/cases/case3.py`, `tests/fake_jev.py`, `tests/phase8/test_case3_walk.py`; 필요시 Hub Gold 원천 투영은 별도 WORK-011/Hub 발주 | WP-9 단일 page 선택은 Q002에서 Jev 245회·Hub 461회·TTFT 73초와 팔자 보톡스 고유 위험 누락으로 실패. SPEC-006 0.3.12 §3-4-1-7로 **다음 노드 후보 묶음에서만 Jev가 여러 갈래/종료를 선택**하도록 바꾼다. 선택된 노드의 필요한 facet page는 앱이 원문·scope를 대조해 지원되면 즉시 종료하고, 미지원/부재 증명 범위만 뒤 page로 간다. 7 unit을 자동 필수로 만들지 않는다. Gold에서 해당 부위 주요 위험이 비면 안전 없이 추천하지 않으며, 원장 `botox_specific.risk` 투영 필요 여부를 공개 사실로 판정한다. Jev·Hub 호출/bytes/TTFT와 답 의료 안전을 한 Q002 실물에서 동시에 비교하고 회귀 후 대표 4문항→고정 50으로 간다. |

WP-1~3과 WP-4는 별도 착수 관문을 둔다. WP-4는 코디의 WORK-011 공개 계약·§6-9 코드/격리 fixture PASS 확인과 인계 뒤 시작한다. 사용자 서버·앱의 동일 build hash 확인은 기능 활성화·실물 평가 전에 수행한다. WP-5는 WP-1~4의 수집/관계 상태와 실제 provider 한계를 반영한다. Hub의 page·요청당 fact ID·관계 응답 상한은 준수하되 전체 탐색 상한으로 해석하지 않는다. 검증 명령 초안: `uv run pytest tests/phase8/test_case3_walk.py tests/phase8/test_verify_runs.py tests/phase4/test_timing_runs.py tests/cli/test_rerun_report.py -q`; 구현 뒤 `uv run pytest -q && uv run ruff check .`. 이 문서 단계에서 새 평가는 실행하지 않는다.

**WP-8 검수 수용 보강:** 답변 묶음은 모든 명시 target·필수 facet/안전/고지를 `included|justified_not_required|unresolved|blocked`로 대조한다. 선택 안전 fact의 공개 관계 chain과 build/unit/family·site/조건/owner/source를 trace에 남기며 `owner == unit`이나 문구 유사성만으로 적용하지 않는다. 반대 부위·타 family·타 complaint·조건 불일치와 owner만 같은 가짜 안전 fact는 배제, 같은 범위 시술명/방식은 유지하는 양·음성 fixture를 둔다. 명시 두 target·나중 page 유일 근거·조건부 금기·고지가 빠지면 답 성공 금지. 효과 제목 인용과 순수 문진 허용, 실패 문장·이유·사용 가능한 ID를 넣은 재작성, 재작성 실패 후 축약 답의 안전·관련성·인용·부재 범위 재검사 및 raw fact 나열 금지를 각각 시험한다. Q002 고정 ID는 시험 기대값에만 쓴다. `q002-answer-contract-review.md`의 WARN 보강을 구현 게이트로 삼는다.

**WP-9 우선순위·Choice 구현 계약:** WP-2/3의 section/page 자동 진행은 0.3.10 구현 단계 기록이다. WP-9부터는 SPEC-006 §3-4-1-6이 해당 순서를 대체한다. 현 Jev `Choice`는 한 질문에 criteria 하나를 반환하므로 `action=expand|stop_answer|stop_incomplete`와 앱이 발행한 `candidate_key` Choice로 한 후보씩 선택·상태 갱신한다. 여러 후보는 다음 순회에서 다시 선택한다. 키는 `(build,target_key,facet,node,edge/kind,section,page)`에만 대응하고 >255 후보는 2단 선택 후 원본 집합에 대조한다. 앱은 Jev 관련성 판단을 키워드 규칙으로 대신하지 않으며, Jev의 stop/후보 소진만으로 `lookup_complete`·`absence_proved`를 만들지 않는다. 명시 target과 실제 말할 갈래의 필수 안전·고지는 면제 불가, 선택하지 않은 비필수 후보만 이유 있는 `justified_not_required`다. stop_answer에는 `supported|absence_proved`와 부재 범위 증명, stop_incomplete에는 미지원 필수 범위·`retrieval_limits`를 요구한다. 같은 tuple/방향 오류/옛 build/무효 Jev 답/반복 선택은 실행하지 않고 재선택 또는 `no_progress/incomplete`로 닫는다. fake Jev의 후보 매핑·>255·빈 후보·오류, 첫 page 지원 종료와 page 2~7 유일 지원, cut 원문, 두 명시 target, 조건부 위험·금기·고지, 진짜 부재, 도구/시간 장애, I-02~I-08 방향을 수용 시험으로 둔다.

**WP-10 우선 계약:** 위 WP-9의 `한 후보/page마다 Jev`는 0.3.11 실패 실행을 설명하는 기록으로만 읽는다. 현행은 0.3.12 §3-4-1-7: 새 **그래프 노드 갈래 묶음**에서 한 Jev 호출의 복수 Choice 슬롯으로 관련 후보 여러 개 또는 종료를 고른다. 동일 노드의 section/page 내부 진행은 앱이 지원 fact·원문/source/scope·필수 안전을 검증해 지원되면 닫고, 미지원이면 필요한 뒤 page만 읽는다. WP-9의 타입/ID/부재/안전 검증은 유지한다. Q002 7 unit 전수·page별 245 Jev 호출은 회귀 실패 조건이다.

**WP-10 검수 차단 해소:** `pick_1..pick_k(k=min(4,후보 수))`는 동일 후보 키+`none` 중 하나를 반환한다. `action=expand`에서 none 제거·중복 첫 값 유지·슬롯 순서 실행 후 남은 후보를 재제시한다. stop과 유효 pick 동시 반환은 거부/1회 재선택 후 계속되면 `no_progress/incomplete`. >254+none은 후보 묶음 2단 선택을 쓰고 미선택 묶음은 보존한다. 선택된 노드의 직접 역할→명시 facet→주요 위험/조건/고지 첫 page, slim 후보 ID만 full 확인, 명확한 scope+의미 지원이면 뒤 page 종료, 불명확하면 짧은 후보 집합만 Jev 평가, 미지원이면 뒤 page 진행이다. page 2~7의 유일 근거는 계속 찾는다. 직접 역할 edge는 모두 얕게 확인하되 Jev가 고르지 않은 선택적 unit을 답 갈래 필수로 승격하지 않는다. 명시 target/실제 답 갈래의 안전은 면제 불가, 답 계획에 갈래가 추가되면 다시 열며, site-specific 주요 위험의 Gold 공개 적용 증거가 없으면 해당 갈래 추천을 보류한다. Q002 fixture에서 `pick_1=2,pick_2=3,pick_3=none`, stop+pick 충돌, 중복/무효/옛 build/역방향, page 1 종료·page 7 유일 근거·cut/범위 불일치, 안전 공백, 진짜 부재/오류와 다른 의도 회귀를 검사한다.

**0.3.13 TypeSafe 공식 primitive 정정:** 위 동일 후보 `pick_1..pick_k`는 여러 독립 Choice가 같은 후보를 고를 수 있으므로 구현 계약에서 폐기한다. 다음 노드 후보마다 관련성 `Noul` 하나와 현재 답 준비 `Noul` 하나를 **같은 `system_one` 요청**으로 보낸다. 후보별 yes 확률을 근거/위험도에 맞춘 임계값과 불확실 구간으로 해석해 여러 후보를 선택·보류할 수 있다. 명시 target/필수 안전은 낮은 점수만으로 면제하지 않으며, 답 준비 점수도 앱의 근거·범위·안전/부재 검증을 대체하지 않는다. 질문 ID가 가리키는 후보 정보와 미지원 facet을 구조화 state로 짧게 보내고 API 한도 시 후보 묶음을 나눠 전부 합친다. 후보별 Noul·선택/보류 이유·누락 묶음·앱 종료 판정을 trace로 남긴다. fake Jev에서 후보 1/2/3에 yes 확률 0.1/0.9/0.8이면 2·3을 선택하고 한 API 호출인지, 동일 Choice 슬롯 반복이 없는지, 불확실/오류·안전 필수/부재 경계를 검사한다. 이 정정은 WP-10의 노드 단위 Jev·facet별 page 종료 계약을 유지한다.

## trace·개별 재생·50문항 관문

- `walk.frontier_rounds[]`: 순회 번호, 후보/선택/신규 tuple, 진전 종류, 잔여와 중지 사유. `walk.received[]`: build/node/section/page/fact 원문·출처/`more`/bytes/ms. `walk.relations[]`: 정규화 pair·완료·claim/대안 scope. `walk.facets[]`: target·필수 항목·지원 ID·상태·미조회 범위. `walk.selection[]`: fact ID별 포함/제외 이유·Claude 묶음 ID. `retrieval_limits[]`: 지원하지 못한 target/facet과 실제 사유. 전체 호출 바이트와 최종 전달 바이트를 분리 기록한다.
- 개별 재생은 Q015/Q072/Q069/Q173 대상·queue, Q085/Q098/Q136/Q160 page, Q018/Q064/Q139/Q173 관계, Q004/Q237 복합 원인, Q004.1 수집→전달→답, Q021/Q058/Q122 부분 답, Q017/Q050/Q147 적용 범위/안전 전이를 본다. 각 질문에 기대 Gold ID·원문·source가 있으면 수집/전달/답 세 지점별로 대조하되 기대 ID로 탐색하지 않는다. Q067.2/Q099.1과 Q226.2/Q229.2는 미확정으로 남긴다.
- 새 실행 내부는 동일 Hub build/앱 commit으로 결정론 재생하고 bytes·선택·상태를 비교한다. 역사적 baseline 50은 QID/질문/채점 계약으로 짝짓고 각 build/commit과 판 차이를 병기한다. 첫 실물 실행은 고정 50 QID의 case3 한 번이다. 직접 근거가 있는데 부재라고 한 **문장 건수와 질문 수를 별도** 집계한다. 정확성·안전·필수 고지·인용/전달 누락·비대상 회귀·TTFT p50/p90·단계 시간·낭비 호출·blocked/incomplete 분포를 보고한다. 안전/지연 악화 시 승격을 보류하고 사용자에게 결과를 보여준 뒤 239×3 여부를 정한다. 50은 W-4 최종 합격이 아니다. fullrun-v2 안전 87.5% 미달과 안전 실패 28 중 25의 8KB 절단 관측은 baseline/원인 일부로 병기하며 전체 회복 수로 쓰지 않는다.

## 끝 조건

- [ ] 명시 target·필수 facet·안전과 중복 없는 frontier가 초기 4걸음 뒤에도 필요한 범위를 순회한다. 지원 fact를 찾으면 무관한 범위를 `not_required`로 닫고, 부재를 주장할 때만 page/pair/이웃의 실제 완료를 증명한다. 미지원 필수 범위와 `blocked/incomplete`를 구분하며 고정 바이트/80%/Noul만으로 `enough` 또는 사실 부재가 나오지 않는다.
- [ ] 186 첫 page 순서·뒤 page 4사례·관계 5문장/4질문을 개별 재생한다. WORK-011의 선택 쌍·전역 메모 검증 전에는 관계 지원 완료가 없다.
- [ ] 수집 fact와 Claude 전달 fact의 ID·본문·출처·scope가 대조되고 탈락 기록·분할 누락·필수 안전/고지·부분 답변·인접 근거 전이를 검증기가 판정한다. 원천/Gold에 없는 사실을 만들지 않는다.
- [ ] 단위 시험/ruff와 동일 판 결정론이 통과하고, 고정 50×1의 문장/질문·안전·정확성·지연 결과를 사용자에게 제시한다. 사용자 판단 전 239×3을 발주하지 않는다.

## 열린 결정

## WP-11 자연어 claim·번호 출처·최종 전달시간

**실제17 all-hold 후 보정:** 정본 §3-4-1-8의 새 실험 계약과 `wp11-calibration-review.md` R1/R2/R3를 적용한다. 후보 prompt/state 하나의 lossless 투영·역할 명확화만 구현하고 기존 정책은 보존한다. 원본48을 보존한 수정 fixture와 scorer adapter, C/H 분리/hash·blind 요청·사전 grid/단일 선택 도구를 offline 검수한 뒤 최대72/retry0 실제 평가를 별도 발주한다. API 실행 전 라벨/입력 동일성·가족/템플릿 한계·모델/문턱/선정 규칙을 동결하며 기본off/빈registry는 유지한다.

**검수 보강 우선:** SPEC-006 §3-4-1-8의 B-01/B-02 보강이 제안 §3의 cited-only source_indices와 장기 분할 문구보다 우선한다. 앱 소유 cited/context 집합으로 누락 반대 근거를 강제 대조하고, 필수 원자 정보가 없으면 전체 원문/조건을 불가분 requirement로 보존한다. manifest 행/source/span/hash/build/scope/필수 이유와 승인 claim→렌더 대응을 모델 태그로 줄이지 않는다. 커버된 claim이 탈락하면 커버 결과를 재사용하지 않는다. 첫 경로는 한 논리 의미 요청 한도 초과 시 보류, 생성 최대2회, 새 retrieval 없음이다. 검수 보고 A01~A20을 수용 시험으로 적용하고 한국어 의미 정책 미검증이면 플래그 활성화 금지다. callback 예외·단일시도·fresh timing과 SDK 물리재시도/논리요청 구분도 구현한다.

SPEC-006 0.3.15 §3-4-1-8이 답변 의역·표시·계측의 정본이며 수집/노드 Noul/안전 scope는 기존 계약을 유지한다. 상세 구현 제안 `wp11-answer-quality-proposal.md` §2~8을 검수·구현 자료로 사용한다. 첫 범위는 coverage I-01 CLI의 claim_v1 플래그다.

1. 신규 answer_contract 모듈에서 strict claim/source/requirement schema, 앱 provenance 검증, 독립 claim별 Jev Choice/requirement coverage 질문 배치, fail-closed 승인·최대1회 수정·원문 축약/보류를 구현한다. 임상 의미를 토큰 겹침으로 승인하지 않는다. 한국어 의역/반대/조건·수치·위험 누락 라벨 평가가 선행하며 fake 판정만으로 모델 의미 효능을 주장하지 않는다.
2. case3/prompt/기존 CLI schema 경로에 연결하고 검증된 claim과 고정 제목만 렌더한다. ID는 trace에 남기고 사용자 답은 번호 출처로 보여준다. 필러 8개 고지/primary risk 및 제안 §5의 21행 requirement 대응을 보존한 채 중복을 줄인다. 미지원 여섯 갈래는 계속 보류한다.
3. timing/runner/finish에 최종 validation/on_text 시작·완료/case 완료를 같은 clock으로 기록하고 CLI timing 덮어쓰기를 막는다. 보고/검증 도구는 기존 TTFT·새 final delivery·judge 시간을 구분한다.
4. 전체 suite/Ruff, schema/위조scope/임상 의미/필수coverage/렌더/가짜시계·모든 실패전달 회귀 뒤 코드 검수, 같은 Gold Q002 단일 실물로 실제 환자 답·의미 판정·번호표·최종시각을 저장한다. 의료 judge와 가독성을 따로 판정한 뒤 대표4→고정50으로 간다. 실물 실패 후 반복 batch는 추가 발주로 통제한다.

### 열린 결정(기존)

고정 50의 승격 문턱은 그 결과를 본 뒤 결정한다. 운영 deadline·호출 timeout은 코드 워커가 기존 기본값·격리 측정으로 정하고 결과에 남긴다. 안전 추가 페이지의 고정 바이트 절단 여부는 더 이상 열린 결정이 아니다. WORK-011 관계 경로·schema·상한은 Hub 구현/§6-9 검증으로 확정한다. `next_page_bytes`는 현 Hub 계약에 없으며 필요하면 실제 낭비 호출·TTFT를 본 뒤 별도 판단한다. 원천 공백 후보 104·미해결 30과 부분 근거 89행의 미전달 84는 별도 근거 조사 대상이지 자동 회복 수가 아니다.


## WP12 — active scope 계약 구현·검증 직렬 계획

**현재 기준(2026-11-03).** [WP11 응답 검수](../../../reference/2026-10-30-hub-evals/build-out/wp11-response-review-scope-contract-report.md) §1~9에서 R01/R02/R03 한정 PASS·기존 offline700/저장 응답28 회귀 PASS가 보고됐다. actual57 included47/held9/excluded1, 추가326 및 전체419는 기존 fixture 관측이지 새 수신/전체 적용 완료가 아니다. WP11 calibration/빈 registry/기본 off와 미지원 여섯 갈래를 유지한다. 새 semantic 정책/model/threshold는 이 계획 범위 밖이다. 아래 모든 단계는 **TODO**이며 문서 작성으로 구현/원천 사실 해소/최종 성공을 소급하지 않는다.

### WP12-A — Hub 인계 뒤 앱 연결

- **Status**: TODO
- **의존**: WORK-011 WP12-H의 구현·공개 schema/fixture·오류/unknown 표 수락. SPEC-005 0.3.10 §5-16-1, SPEC-006 0.3.15 §3-4-1-9가 계약 정본이며 중복 shape는 만들지 않는다.

| 계획 파일(clinic_chat 레포 기준) | 작업·관찰 가능한 완료 증거 |
|---|---|
| `clinic_chat/clients/hub_rest.py` | 선택 fact_projection 전달; 생략 full/명시 full/scope 요청·echo·요청 tuple 기록. scope와 sections/neighbor/full=true/page 혼용 금지 |
| `clinic_chat/cases/case3.py` | `_expand_receipt_error`, full cache/receipts·semantic_candidate·get_page·context_candidate·`_collect_context_relations`의 공통 validator와 staged 수집 연결. source.file/path/owner/section canonical join 후 meta 존재/hash/version 별도 검증; full/scope cache 분리·현재 inventory 재대조 |
| `clinic_chat/cases/answer_contract.py` 및 실제 binder 모듈 | attachment/applicable/required 분리, source별 qualifier/witness 검증, unknown 영향 branch hold, manifest·context_source_indices·coverage 재개방. product 선택 ID/null과 답 scope를 앱 소유로 결합 |
| `clinic_chat/verify_runs.py`, `clinic_chat/report.py`, 필요 시 `clinic_chat/runner.py` | inventory/scope/original/manifest 각각의 상태, 제외/unknown 이유와 witness, mode 요청·bytes/ms/cache hit, held 종료·최종 delivery/timing을 보존. 기존 TTFT와 최종 전달 시간 구분 |
| `tests/phase8/test_public_response_replay.py`, `tests/phase8/test_context_binding.py`, `tests/phase8/test_context_collection.py`, `tests/phase8/test_case3_walk.py`, `tests/phase8/test_wp10_absence_bypass.py`, `tests/fixtures/wp11_live_public/` 및 해당 manifest 시험 | 실제 저장 응답 기반 정상/변조와 generic source별 검증; 새 fixture는 원본 보존·hash/생성 근거 분리. 정확한 기존 파일 위치는 착수 rg로 확인하고 차이를 보고 |

- **작업**:
  - [ ] active scope inventory→unresolved IDs scope metadata→필요 original→manifest를 분리한다. row마다 metadata 존재/hash/version·attachment witness·적용 판정·필수 여부/이유·unknown 영향·justified_not_required 증거를 기록한다.
  - [ ] K8 exact target join, combo row/index/field/anchor/ambiguity, product 관계/family override/selection, note CC와 pair unknown, family/site leaf를 같은 계약으로 연결한다. QID/실제9·326 ID의 런타임 allowlist 금지.
  - [ ] original 미수신과 scope 미확정을 독립 유지한다. claim/product/branch/site/condition 변경 시 관련 proof·장부·의무·coverage 무효화 후 재개방한다. 새 retrieval는 bundle 확정 전에만 한다.
  - [ ] 알려진 타 scope만 이유·witness로 제외하고 실제 주장/필수 경고 영향 unknown은 branch hold한다. 원천 공백이면 graph 확대 없이 held로 종결한다. 일반 시술에서 미선택 제품 위험의 일반 사실 승격과 attachment 전체 강제 필수화를 모두 막는다.
- **검증**: 아래 독립 검수의 동일 수용 행렬을 개발 회귀에도 적용한다.
- **완료 증거**: 미작성. 구현 diff·trace shape·mode/cache/provenance 양성/음성·각 단계 상태 전이와 원천상 남은 unknown 목록을 보고한다.

### WP12-R — 독립 offline 검수

- **Status**: TODO
- **의존**: Hub→앱 구현 인계 완료. 구현자의 자체 PASS와 분리된 검수 발주는 코디가 한다.

| 수용 축 | 양성·변조·누락과 기대 |
|---|---|
| R01/R02/R03·기본 호환 | 변경 전 actual57 exact baseline(47/9/1) 보존 재생과 변경 후 source별 판정 delta를 ID/근거별 보고. 정상 role cache 재사용/실제 생성 회귀를 유지하고 hold 기대값으로 바꾸지 않음. 기존28 변조·build/node/명시echo/unique/exact membership/provenance·현재 inventory 재검증 유지 |
| K8 | 실제 []/false/target_keys=M2 원천으로 준비·상담 문맥 보존. meta 누락/null/false→true·target 변경·wrong owner/source/path/type/build는 hold; T5 metadata가 있으면 selected와 교차 일치 |
| combo7+추가13 | 실제 row/index/field/source/units/anchor 양성 join과 ambiguity 보존. wrong member/path/source ID, ambiguity 삭제·단독 site 역상속·anchor→member 위조는 거부. 승인된 family/비교 범위 보존과 단독 unit proof 금지를 각각 시험; 같은 scope limitations/상충 누락 금지 |
| product276 | 실제 one-hop/product_unit은 attachment 양성만 증명. 다중 family auto-M4/override_of=M4와 active M2를 별도 대조. 미선택 제품의 일반 사실 승격 금지; 증명된 다른 scope 제외와 영향 unknown hold를 각각 검증. 제품 선택 추가 시 장부/manifest/coverage 재개방 |
| note7·family/site | note source=step7/CC witness 양성, pair 없으면 pair_scope_unknown, 다른 pair/context mismatch를 단독 효능으로 승인 금지. patient 언어 중복 자동 제외·SE root/SC row/site label-only 위조 거부; 원천 qualifier 보존 |
| mode/cache/provenance | full 생략 호환·명시 full/scope echo, scope text/line 없음·original 미수신, scope 캐시로 full 충족 금지. mode 누락/불일치·extra/missing/duplicate ID·meta 충돌/타입·wrong row·unsupported version 거부. source dict 전체 equality 대신 canonical join+metadata 별도 검사; missing/null/[]/false 차이와 과거 slim meta 부재 정상 join 확인 |
| 장부·필수 의미 | support 충분+inventory 미완료, inventory 완료+영향 unknown, scope 완료+필요 original 누락, manifest/approved claim/render span 누락 모두 hold. 동일 scope 경고의 낮은 relevance·조건 미언급 면제 금지. 증명된 타 scope·정당 non-required는 witness와 함께 닫힘. claim 제거 후 coverage 재사용 금지 |
| 경계·실패 | deadline/error/no_progress·불완전 edge를 unknown/incomplete로 기록. 빈 registry/기본 off, 기존 의미 hard gate 유지; 전체 graph/section-full·고정 budget·새 임상 facts/정책/threshold 없음 |

- **검증**:
  - [ ] 저장 원본/새 projection fixture의 hash·build/publication/원천 row join 증거를 대조한다. 기존700은 선행 보고 결과로만 인용하고 현재 코드에서 전체 offline suite를 새로 실행한다. 700개 기존 회귀를 제거하지 않고 신규 수와 분리하며 전체 pytest/Ruff/diff 검사를 보고한다. Hub 기존 회귀도 별도 보고한다.
  - [ ] 정상 경로가 여전히 생성되는 시험과 변조만 hold되는 시험을 짝지어 확인한다. 코드 PASS가 unresolved scope를 승인으로 바꾸지 않음을 확인한다.
- **완료 증거**: 미작성. 결함 심각도/재현·source별 해결/잔여 unknown·PASS 한계를 포함한 독립 보고. source 정보 부재와 구현 실패를 분리한다.

### WP12-L — 격리 실제 공개 receipt

- **Status**: TODO
- **의존**: 독립 offline 검수 수락 뒤 코디의 별도 실행 발주. offline PASS가 live/model/배치 실행을 자동 승인하지 않는다.
- **작업**:
  - [ ] 시작에 본인 process/port/격리 DB·publication 참조·source hashes·Hub/app commit을 기록한다. 기존 사용자 서버/DB/env/publication과 포트 18005/3700/3800/8700/8800/54329·procedure-* 컨테이너를 변경하지 않는다.
  - [ ] 같은 publication/build에서 REST/MCP full 기본·scope·선택 full 실제 raw 응답과 요청/hash를 저장한다. 새 mode/source-specific projection·original 미수신/수신·binder 판정·unknown 종료를 확인한다. 새 build가 불가피하면 같은 원천·차이 manifest를 코디에 먼저 인계하고 혼합 build 검증은 금지한다.
  - [ ] source/export/hash/publication 불변과 앱 동일 build를 확인하고 원문·scope 누락/위조가 새 공개 receipt에서도 hold되는지 확인한다. raw 산출에 key/env를 남기지 않으며 소유 process만 cleanup한다.
- **검증**: 실제 수신 provenance와 요청 tuple/mode·ID·metadata/full join·각 장부 상태를 저장 fixture와 대조한다. resolved K8와 원천상 unresolved combo/product/note를 각각 보고하며 9/326/419 전부 승인 의무 없음.
- **완료 증거**: 미작성. 실제 receipt는 모델 의미 정확도/환자 답 성공 증거와 구분한다.

### WP12-Q — 실제 Q002 답 생성·가독성 관문

- **Status**: TODO
- **의존**: 격리 receipt 수락과 기존 semantic 정책/registry 관문 충족 뒤 코디의 별도 모델 실행 발주. source unknown이 답 갈래에 영향을 주면 그 갈래 held를 유지한다. 기존 policy를 이 작업에서 교체하지 않는다.
- **작업·검증**:
  - [ ] 동일 Gold와 명시된 실행 판에서 실제 답 생성·최종 delivery를 저장한다. branch별 supported/held·필수 안전/조건/상충·증명된 제외를 구분하고 held를 정보 없음/전체 성공으로 말하지 않는다.
  - [ ] requirement→approved claim→source→렌더 span, 번호 인용표, 자연스러운 한국어·중복·읽기 순서·정의 없는 숫자/raw dump 방지와 실제 callback 성공을 대조한다. 의료 안전/관련성 검수와 가독성을 별도로 판정한다.
  - [ ] Jev/Hub 호출수·mode별 full 감소·bytes·Claude 입력·모델 TTFT/최종 전달 지연·오류를 같은 build 기준선과 비교한다. 속도 목표로 필수 경고를 자르지 않는다.
  - [ ] 실패하면 반복 batch로 덮지 않고 이유·남은 원천 공백·다음 발주 여부를 보고한다. 수락 후 대표4→고정50은 별도 발주이며 전체419 승인·239×3·최종 성공을 선약하지 않는다.
- **완료 증거**: 미작성. 구현 완료, 공개 receipt 수신 완료, 원천 미확정 해소, 실제 답/가독성 수락을 각각 보고한다.

### WP12 남은 쟁점

combo의 exact site와 canonical pair 없는 note의 subject/pair는 새 projection 구현만으로 확정되지 않는다. product 선택/override의 실제 답 scope, patient 언어 잎의 의미 동일성·필수 qualifier 보존도 receipt/검증별로 판단하며 자동 완료하지 않는다. 보수적 기본은 §3-4-1-9의 범위 보존 또는 영향 branch hold로 이미 정했고, 추가 임상 추론이나 새 semantic 문턱을 정하는 일은 별도 결정 범위다. 기존 고정50 승격 문턱·기타 열린 결정은 그대로 남는다.
