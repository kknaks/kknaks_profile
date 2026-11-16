---
type: work
id: WORK-011
title: "case3 정보 없음 — Hub 선택 관계·전역 메모 읽기 계약"
status: todo
product: procedure-hub
feature: phub-recommend
work_type: change
owner: "Hub backend 워커(코디 발주)"
progress: 0
created_at: 2026-11-02
updated_at: 2026-11-03
depends_on:
  - "SPEC-005 0.3.10 §5-16-1 / SPEC-006 0.3.15 §3-4-1-9 (selected scope projection 짝 계약)"
  - "기존 0.3.9 선택 관계·전역 메모 사용자 WORK 리뷰(별도 선행)"
links:
  spec: "orchestration/work/phub-recommend/SPEC-005.md 0.3.10 §5-5 · §5-16 · §5-16-1 · §6-9"
  review: "orchestration/work/phub-recommend/review-info-absence-spec005006-v2.md (FAIL 0 · WARN 3)"
  next: "orchestration/work/phub-recommend/WORK-012.md"
---

# Hub 선택 관계·전역 메모 읽기

SPEC-005 0.3.10이 현행 계약 정본이다. selected scope projection은 아래 WP12-H, 기존 선택 관계·전역 메모는 종전 WP-0~5로 분리한다. 이 WORK는 구현 순서·코드 표면·검증 증거를 정한다. **현 코드/서버가 새 계약을 제공한다는 뜻이 아니다.** 사용자 WORK 리뷰 뒤 코디가 외부 레포 워커에게 발주한다. 앱 관계 어댑터(WORK-012)는 이 WORK의 공개 응답 계약과 §6-9 검증이 닫힌 뒤 착수한다. 앱 페이지 수집은 기존 `expand(page)` 계약으로 독립 진행 가능하지만, **Hub 빌드가 섞인 서버에서 측정하지 않는다.**

## 기준·범위

- 코드 레포: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend`, 읽기 기준 HEAD `2edc190`. 워커는 착수 때 HEAD·`git status --short`·빌드 ID를 기록하고 차이가 있으면 표면을 다시 조사한다.
- 기존 T4는 기본 응답에서 주장 원문 ≤2/쌍, 대안 개수만, `from/rule` 생략이다. `sections=evidence`에도 대안 원문 출처는 없고, `sections=all`에도 claim/대안별 fact ID·source 결속은 보장되지 않는다. 묶인 `pairs:[[a,b],…]`와 `pairs_more_n`(개수)은 특정 확정 쌍의 수신 증거가 아니다. 현 `relations_all.global`·`pair_check.global`은 Q139 전역 메모 수신 증거가 아니다(§5-5; 재검수 W-1/P-3).
- 기존 `expand(id, sections=[s], page=p≥1)`는 section당 12줄, `more[s]`는 **요청 p 뒤** 잔여 줄 수, 0이면 생략이다. 첫 페이지 ID 순서·40자/cut·`fact_ids` 인용 규칙을 지킨다. `peek.sections[].bytes`는 첫 페이지 compact 전체 응답 비용뿐이다. `next_page_bytes`는 만들지 않는다(§5-16).
- 비범위: 원장 사실 생성·Q226.2/Q229.2 구조 edge를 의료 fact로 간주하기·Jev/앱 정책 변경·전체 평가·사용자 18005 포트 또는 `procedure-*` 컨테이너 조작. 원장 인용 본문은 이 문서와 공개 시험 fixture에 복사하지 않는다.

## 공개 계약을 닫는 설계 선택(WP-1 산출)

기존 T4를 바꾸지 않는 **전용 선택 읽기**를 우선안으로 한다. REST `POST /procedure-hub/gold/pairs/selected`와 `POST /procedure-hub/gold/global-claims` 및 같은 코어의 MCP 도구를 제안한다. Hub 워커는 기존 route·service 관례와 충돌 여부를 확인해 경로·입력·응답 JSON 예시·오류 코드를 WP-1에서 확정하고, 코디가 앱 어댑터 착수 전에 계약 문서/시험 출력으로 수락한다. 경로가 바뀌면 이 WORK와 앱 어댑터 입력을 함께 갱신한다.

| 호출 | 필수 의미와 상한 제안 | 완료 판정 |
|---|---|---|
| selected pair | 정본 단위 시술 `a,b` **정확히 둘**. `prior?`, `sub_condition?`, `include_conditional?`, `sections?`를 기존 T4와 같은 뜻으로 전달한다. 조회 키는 `build+정규화 입력+prior+sub_condition+include_conditional+sections`; 양방향 정규화는 중복 제거에만 쓰고 반환의 `a/b`, `value.first`, `by_direction`은 원 방향을 보존한다. 응답 상한 **64 KiB 제안**: 넘으면 `truncated`와 실제 크기·사유를 내고 완료로 표시하지 않는다. `64`는 node `fact_ids` 상한이며 관계 API의 64개 상한으로 전용하지 않는다. | `pair_scope{a,b,build,complete,status:found|empty|truncated|error}`. `empty`는 확정 쌍의 범위 조회가 끝났고 행이 없을 때만. `resolved{value,field_status,by_direction,source_fact_ids[]}`, claim별 `fact_id,text,source{file,path},flags,applies_to,quotable`, 대안별 `value,fact_ids[],source,applies_to`를 결속한다. `pairs_more_n`만으로 누락 판정 금지. |
| global claims | Q139의 `scope:all#evidence#step8_notes[26]`을 R8 edge owner와 별도 조회. 확정 쌍·scope/condition을 입력받는 방식과 **32 KiB 응답 상한 제안**을 WP-1에서 확정한다. | `global_claims[]{fact_id,text,source{file,path},applies_to{pair?,scope,condition?},priority,quotable}`, `scope_complete`, `status:found|empty|truncated|error`. 적용 범위 일치와 scope 완료가 확인되어야 인용 가능. |

상한은 **기술 설계 제안**이다. 실제 데이터 크기·REST/MCP 직렬화 비용을 WP-1에서 재고 상한이나 페이지 방식이 바뀌면 코디에게 계약 차이를 보고한다. 잘린 응답을 조용히 `empty` 또는 `found/complete`로 바꾸지 않는다. 0.3.9 당시 앱은 full 15KB 장부에서 초과 응답 전체를 배제했으나, SPEC-006 0.3.10 앱은 수집 중 고정 full 장부로 배제하지 않고 Claude 전달 한계를 근거 선별·분할로 처리한다. Hub의 호출별 상한은 앱 전체 탐색 상한이 아니다. D-13b의 resolved 한 값과 대안을 분리하고, 한 출처를 다른 claim에 복사하거나 edge에서 의료 문장을 합성하지 않는다.

## 순서·코드 표면·검증

| WP | 코드 레포/허용 경로(계획) | 실행·증거 | SPEC |
|---|---|---|---|
| 0 기준점 | `backend` 읽기만 | `git log -1`, `git status --short`; `rg -n 'pair_check|relations_all|pairs_more_n|global_claims|def expand|more\[' app/modules/gold app/router app/schema tests`로 전체 호출 표면 기록. 현재 build/서버와 HEAD를 동일시하지 않음. | §5-5 · §5-16 |
| 1 계약·fixture | `app/modules/gold/{tools,service,mcp_server,application,memory,repository,config}.py`, `app/router/gold.py`, `app/schema/gold.py`, `app/swagger_docs/gold.py`, `tests/test_gold_*`, `tests/test_public_api_contract.py` 중 필요한 곳 | 확정 단위 쌍·미확정 계열·동일 ID 자기 쌍·prior·조건부·방향·묶인 쌍·truncated/empty/error 및 Q139 별도 메모의 입력/출력 표를 먼저 작성. 기존 T4 응답 차이를 fixture로 고정. `rg`로 드러난 누락 경로는 보고서에 추가. | §5-5 |
| 2 선택 관계 | 위 gold core/route/schema/MCP 및 관계 시험 | 원천 R8 fact의 ID·원문·출처·적용 범위를 resolved/claim/대안 각각에 결속. 요청 원 방향과 dedup key 분리. `pair_scope.complete`가 사실인 경우만 empty/found; 초과·오류는 미완료. REST와 MCP 같은 코어·순서. | §5-5 · §6-9 |
| 3 전역 메모 | 위 gold core/route/schema/MCP 및 전역 시험 | Q139 메모를 별도 scope로 조회·부착. scope 불일치와 source 없는 행은 인용 불가; R8 두 행만 받은 상태를 global complete로 표시하지 않음. | §5-5 · §6-9 |
| 4 기존 페이지 회귀 | `app/modules/gold/tools.py`, `tests/test_gold_v33_expand.py`, `tests/test_gold_v32_walk.py`, 관련 도구 시험 | 186개 기존 section 호출의 1쪽 **ID 순서** 비교(바이트 동일성 요구 아님), page 2~7의 목표 ID와 `more`/12줄/40자/cut/원문 자격, `safety.management`, peek 1쪽 compact bytes 차 0. page 비용 metadata 추가 없음. | §5-16 · §6-9 |
| 5 빌드·서버 인계 | `scripts/gold_build.py`, `scripts/gold_export.py`, `backend/build-out/` 보고 산출(코드 워커 발주 시 허용 범위 재확인) | 같은 build/정규화 요청 두 번의 fact ID·순서·본문·상태·바이트 일치; 새 빌드가 필요하면 입력 해시·새 build ID·이전 대비 manifest. 격리된 inprocess/별도 포트에서 먼저 검증. 발행·사용자 서버 18005 갱신은 코디가 앱 호환 판과 함께 예약하고 갱신 전후 build hash를 확인. 혼합 빌드 측정 금지. | §6-9 |

구현 워커의 검증 명령 초안(실제 repo의 실행 환경을 WP-0에서 확정): `uv run pytest tests/test_gold_tools.py tests/test_gold_v33_expand.py tests/test_gold_mcp.py tests/test_public_api_contract.py -q`, 신규 선택 관계·전역 메모 시험, `uv run pytest -q --ignore=tests/integration`, `uv run ruff check .`. DB/build를 쓰는 명령은 격리된 워커 환경에서만 실행하고 실행 로그·build hash·두 번 비교 산출물을 보고한다. **이 WORK 작성 단계에서는 실행하지 않는다.**

§6-9 대표 재생은 Q018.1 `R8-0163`, Q064.1 `R8-0075`, Q139.1/2 `R8-0218/0219`, Q173.1 `R8-0111`의 fact ID·원문 일치·쌍별 resolved·claim/대안별 source와 Q139 전역 메모를 **별도** 대조한다. 페이지는 Q085.2/Q098.1/Q136.1/Q160.1을 본다. 이는 관계 **5문장/4질문**의 접근 검증이지 답변 회복 또는 전체 개선 수가 아니다. 미확정 Q067.2/Q099.1 대상 동일성 및 Q226.2/Q229.2 매핑은 결과에 미확정으로 남긴다.

## 끝 조건·인계

- [ ] WP-1 공개 경로·schema·상한·오류/부분 응답 의미를 코디가 수락하고 앱 워커에게 동일한 계약 파일/출력을 전달한다.
- [ ] 선택 쌍의 `pair_scope`와 Q139 `scope_complete`가 실제 범위 완료를 뜻하며, provenance 없는 claim/대안은 지원 사실로 세지 않는다. 기존 T4 계약과 회귀가 유지된다.
- [ ] §6-9의 결정론·186 첫 쪽 ID 순서·뒤 페이지 4사례·관계 5문장/4질문·전역 메모가 각각 증거로 통과한다. 실패는 ID/사유별로 남긴다.
- [ ] [공개 계약 인계](WORK-011-public-contract-handoff.md)의 격리 build hash와 응답 fixture로 앱 관계 어댑터 코드를 작성한다. 실제 서버·앱이 같은 build hash를 읽는지 확인한 뒤에만 기능을 활성화하고 평가한다. 사용자 포트/컨테이너는 이 WORK 워커가 조작하지 않는다.

## 열린 결정

V-22의 관계 전용 경로·정확한 상한은 WP-1 기술 계약으로 닫는다. V-23의 뒤 페이지 `next_page_bytes`는 현 범위에서 채택하지 않고, 초과 호출량/지연 측정 뒤 별도 판단한다. V-24 원천 명제와 V-25 실제 수혜 건수는 이 구현만으로 확정하지 않는다. WORK 사용자 리뷰가 코드 발주의 선행 조건이다.

## WP12-H — selected scope projection(추가 계획)

- **Status**: TODO
- **설명**: SPEC-005 §5-16-1의 wire 계약을 먼저 구현·검증해 앱에 인계한다. 원천 graph/DB/build facts를 새 임상 사실로 수정하지 않는다. 기존 관계 인계 파일은 과거 수신 증거로 유지하며 새 projection이 이미 제공된 것으로 소급하지 않는다.
- **의존**: SPEC-005 0.3.10 / SPEC-006 0.3.15 정본 → 이 Hub 단계 → WORK-012 WP12-A → 독립 검수 → 격리 receipt → 실제 Q002. 코드/실험 발주는 코디가 별도로 수행한다.

| 계획 파일(backend 기준) | 작업·완료 증거 |
|---|---|
| `app/schema/gold.py` | ExpandRequest optional fact_projection full/scope, scope exact IDs 전용·혼용/타입/중복/상한 검증. 기본 full 생략 호환과 명시 mode echo 시험 |
| `app/modules/gold/tools.py` | `_walk_row/expand` selected 행에 source.meta/scope_projection; source row exact join helper와 subject별 qualifiers·unknown. 기본 slim/page/section-full 보존; scope text/line 없음. membership/canonical source/순서/flags/gap·more 유지 |
| `app/modules/gold/{memory,service,mcp_server,application}.py` 중 필요한 곳 | FactRows/attached_to/attrs.silver/기존 edge/source_refs를 읽기 전용으로 연결. source-specific attachment와 임상 적용 분리. 같은 core를 REST/MCP에 노출하고 mode 전파·echo 일치 |
| `app/router/gold.py`, `app/swagger_docs/gold.py` | 기존 route 및 공개 문서·MCP schema에 같은 요청/오류/기본값. 새 임상 판정 API·owner frontier 추가 없음 |
| `tests/test_gold_v33_expand.py`, `tests/test_gold_mcp.py`, `tests/test_public_api_contract.py`, 필요한 `tests/test_gold_*` | 저장 공개 응답과 같은 build의 원천 row를 대조한 양성·변조 fixture. 신규 시험 파일이 필요하면 구현 발주에서 이름을 고정하며 본 문서 작업은 생성하지 않음 |

- **작업**:
  - [ ] 시작 HEAD/status·원천/export/publication/hash를 기록하고 같은 build의 실제 저장 응답/원천만 대조한다. 이전 보고서 기준 build `567677edfe7123e9`를 fresh 다른 build와 섞지 않는다.
  - [ ] K8 전체 metadata, combo member/anchor locator·ambiguity, product linkage/override, note CC/pair unknown, family/site leaf를 generic row join으로 투영한다. source.meta의 missing/null/[]/false를 보존하며 없는 applies/pair/site를 생성하지 않는다.
  - [ ] subject/version/unknown reason과 필드 경로, canonical join 키·metadata 존재/hash 검사와 오류 계약을 앱에 넘긴다. `selected_product`는 앱 소유이며 Hub가 추정하지 않는다.
  - [ ] 기존 source.meta 없는 slim/full 소비자도 canonical join 가능한 additive 응답임을 확인하고 section 기본 응답 ID/정렬·peek bytes/기존 관계 API를 유지한다.
- **검증**:
  - [ ] full/scope REST/MCP 동일성, 명시 mode echo, 기본 full, ≤64/exact membership·중복/추가/누락 ID·wrong build/node/source/owner·잘못된 row/member index·타입·mode 혼용 거부.
  - [ ] scope original 미수신·text/line 부재, source 부재와 null/[]/false 보존, 양 mode metadata 일치; ambiguous site/pair 부재를 unknown으로 유지. 알 수 없는 subject/version은 proof 불가.
  - [ ] 기존 186 first-page ID 순서·뒤 page/more·peek bytes 차0·T4/global 관계 회귀와 Hub offline suite/Ruff를 실행한다. 기존700은 앱 전체 suite 기준이며 Hub 테스트 수로 합산하지 않는다.
- **완료 증거**: 미작성. 구현 diff·HEAD/build·요청/응답 shape·오류/unknown 표·raw fixture hash·검증 로그를 코디에게 인계한 뒤 앱 단계를 연다. 이 단계 PASS로 source ambiguity 해소·전체419 승인·실제 답 성공을 주장하지 않는다.
