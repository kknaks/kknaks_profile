# case3 정보 없음 — SPEC-005/006 0.3.9 검수

**종합 판정: FAIL 1 · WARN 4 · PASS 7.** 신규 접근·수집 계약 자체는 제안서 재검수의 F-1~F-3을 대체로 정본에 옮겼다. 다만 **SPEC-006의 이전 메모 우선 문구가 0.3.9의 뒤 페이지 수집을 무효화할 수 있어 WORK 발주 전에 바로잡아야 한다**(F-1). 또한 선택 관계 API/전역 메모의 실제 경로·응답 상한, 안전 추가 페이지 정책, retrieval deadline/timeout 숫자는 아직 WORK의 확정 입력이 아니다. 현 Hub·앱 구현이 신규 계약을 제공한다는 판정은 금지한다. 이번 검수에서는 코드·서버·DB를 바꾸거나 새 평가를 실행하지 않았다.

## 읽은 판과 적용 범위

- 대상은 `SPEC-005.md` v3.5 **0.3.9**(2026-11-02, 48행) 및 `SPEC-006.md` v2.9 **0.3.9**(2026-11-02, 40행)이다. 이전 정본 근거는 `SPEC-005.v3.3.md` 0.3.4, `SPEC-006.v2.7.md` 0.3.7과 두 SPEC 머리의 v3.4/0.3.5·v2.8/0.3.8 변경 기록(005:50-53, 006:42-44)이다. **직전 0.3.5·0.3.8 별도 스냅샷 파일은 이 작업 폴더에서 찾지 못했다.** 제안서의 직전판 명시(`info-absence-spec-proposal.md:5`)와 변경 기록으로 의존을 대조했으므로 직전 파일 대 직전 파일의 완전 diff는 검증하지 못했다.
- `info-absence-spec-proposal.md` 2026-11-02 수정본, `review-info-absence-spec-proposal-v2.md`(재검수 WARN), `_RESUME.md` 2026-11-01~02 결정(특히 136,157행), `info-absence-remediation-plan.md:40-54`, ignored audit `root-cause-next.md`, `direct-fact-worktable.md`, `partial-claims-worktable.md`를 읽었다. 기준 실행은 **`b202611020020-edc407`**, Gold build **`567677edfe7123e9`**(`direct-fact-worktable.md:3-5`)이며 이번에 서버 현 상태를 확인한 값이 아니다.
- 읽기 전용 코드 HEAD: Hub `2edc190e70d4322f69672cc0e9e23417169e63cd`, 앱 `078ac99b2f307de65acdcdecc9beb94bcda1249c`. 아래 `Hub tools.py`는 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/app/modules/gold/tools.py`, `앱 case3.py`는 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals/clinic_chat/cases/case3.py`다. 문서·코드·build의 판이 같다는 뜻은 아니다.

## 지적

| 판정 | 대상 파일:줄 | 대조 근거와 판단 |
|---|---|---|
| **FAIL F-1 · 구현 전 차단: 이전 메모 우선순위** | `SPEC-006.md:42-43,305-317` | 0.3.9은 후속 fill의 `page≥2`와 tuple 상태를 새 규범으로 삼는다. 그러나 0.3.8/0.3.7 기록이 여전히 “메모와 이 스펙이 다르면 메모가 정본”이라고 한다. 그 메모 `phub-recommend-walk-fix3.md:8`은 fill을 “아직 안 받은 섹션 · 1쪽”으로 한정한다. 구현자가 우선 문구를 따르면 Q085/Q098/Q136/Q160을 막는 옛 규칙을 채택한다(`root-cause-next.md:9,15`; `direct-fact-worktable.md:56-57,63,70`). 0.3.9 조항이 과거 메모보다 우선함을 명시해야 한다. |
| **WARN W-1 · 관계 API 기술 설계 미확정** | `SPEC-005.md:617-621,1072`; `SPEC-006.md:315,872` | 새 `pair_scope`, claim별 source, 대안별 fact/source, `global_claims`는 필요한 계약을 구체화했지만 선택 원문 모드인지 전용 API인지, 경로·상한·정확한 필드는 Hub WORK로 넘겼다. 현 T4 `Hub tools.py:1376-1378,1464-1467,1507-1518`에는 claim별 source가 없고 기본/evidence의 alternatives는 개수, `from/rule`은 빠진다. `Hub tools.py:1537-1543`의 `pairs_more_n`도 개수다. `root-cause-next.md:7`의 5문장/4질문과 Q139 scope:all은 현 T4 성공 근거가 아니다. Hub WORK에서 응답 schema·실제 R8/전역 메모 경로를 확정한 후 앱 어댑터를 발주해야 한다. |
| **WARN W-2 · 제품 정책과 시간값 미확정** | `SPEC-006.md:313,317,874-876` | 안전 추가 페이지 rank 갱신/우선순위·안전 8KB 절단 뒤 일반 예산 사용, 전체 retrieval deadline·호출별 timeout 값이 열린 채다. `_RESUME.md:136`의 fullrun-v2 안전 87.5%는 목표 90% 미달이고, `phub-recommend-walk-fix4.md:6-7`은 기존 첫 페이지 안전 우선만 결정했다. 새 안전 정책을 확정하지 않은 채 배포 WORK를 진행할 수 없다. 7초 TTFT는 timeout 숫자의 근거가 아니다. |
| **WARN W-3 · 직전판 보존과 오래된 본문** | `SPEC-005.md:8,48,50-52,838`; `SPEC-006.md:8,40,42-44,330,377` | 0.3.9과 짝 의존은 명시했다. 그러나 직전 005 0.3.5·006 0.3.8의 별도 보관본은 없고, 006:330은 여전히 005 v3.3/0.3.4를 “정본”이라 부르며 006:377은 “걸음은 1쪽만”이라고 일반화한다. 005:838도 006 v2 대응을 현재 계약처럼 읽기 쉽다. 006:325-330 및 305-317의 새 후속 fill 조항이 우선한다고 밝혀야 판독 혼선을 줄인다. |
| **WARN W-4 · 승격 문턱은 사용자 결정 대기** | `SPEC-006.md:809-812,868,876` | 50 QID×case3 1회의 정확성 최소 개선량·TTFT p50/p90 허용 악화 폭이 미승인이다. `info-absence-remediation-plan.md:40-45`와 `_RESUME.md:157`의 W-4(182×2 평균 58/90/7)를 50×1에 그대로 대입하지 않은 점은 맞다. 50 결과 뒤 사용자 검토 전 239×3 발주는 막혔다. |
| **PASS P-1 · 현 T4와 신규 계약 구별** | `SPEC-005.md:609-621`; `SPEC-006.md:315` | `Hub tools.py:1441-1450,1519-1525`의 grouped pairs 및 `pairs_more_n`을 정확히 설명한다. `sections=all`로도 claim/대안별 출처 완성을 주장하지 않고, 미확정 단위 쌍·missing ID·예산 배제를 성공에서 제외한다. Q139 `scope:all#evidence#step8_notes[26]`을 R8과 별도 경로로 둔 것도 `review-info-absence-spec-proposal-v2.md:14-16`에 맞다. |
| **PASS P-2 · page/more와 실제 코드의 차이** | `SPEC-005.md:829-832,860`; `SPEC-006.md:311,325-326` | `Hub tools.py:2241-2257,2283-2291,2302-2312`는 page≥1, 12줄, 요청 페이지 뒤 `more`, 0 생략을 구현하고 `next_page_bytes`는 없다. 새 계약은 peek bytes를 1쪽에만 쓰고 뒤 페이지는 실제 전체 응답으로 판단한다. 현 앱 `clients/hub_rest.py:59-65`, `앱 case3.py:779,1045-1048`은 page를 넘기지 않고 section 단위 taken을 쓰므로 구현 전 표시가 정확하다. |
| **PASS P-3 · 대상/facet과 enough** | `SPEC-006.md:307-311` | 명시 비교 양쪽, 동의어 대안, 모호성, target_key/provenance, 미방문 seed, facet별 적용 범위·인용·출처를 구분한다. `앱 case3.py:1363-1371`은 현재 fact와 Noul/예산만으로 enough 종료 가능하며 `root-cause-next.md:17-19`의 queue/resolve 누락과 대조된다. 새 조항은 현 구현이라는 주장을 하지 않는다. |
| **PASS P-4 · 세 예산과 초과 응답** | `SPEC-005.md:619,860`; `SPEC-006.md:313-317,329-331` | 안전 8,000B·일반 20,000B·cut/관계 원문 15,000B를 요청 전 한 장부에 귀속하고 초과 응답 전체를 배제한다. actual/accepted, 중복 ID 비용, 지연을 나눠 기록한다. 앱 기본값 `config.py:73-82,94`와 일치하지만 서버 실행 env는 이번에 확인하지 않았다. 005의 64는 `expand(fact_ids)`에만 적용된다(`Hub tools.py:2260-2261`). |
| **PASS P-5 · 부분 답변** | `SPEC-006.md:459`; `partial-claims-worktable.md:7-25` | `retrieval_limits`를 인용 근거로 승격하지 않고, 채택·적용 범위가 맞는 사실만 답한 뒤 나머지를 유보한다. Q017/Q050/Q147의 인접 근거 전이 금지 및 Q021/Q058/Q122의 전달 사실 검사가 맞다. 부분 89행 중 미전달 84는 조사 후보이지 84건 오류 확정이 아니다. |
| **PASS P-6 · 005↔006 회귀 관문** | `SPEC-005.md:1042-1044`; `SPEC-006.md:864-868` | 동일 build 결정론·186개 1쪽 ID 순서·2~7쪽 네 사례·관계 R8 5문장/4질문·Q139 별도 메모가 대응한다. 006은 queue/resolve·복합 원인·부분 답변·비대상 회귀와 고정 50→239×3 순서를 보탠다. `info-absence-remediation-plan.md:42-45`와 같고 대표 사례 통과를 전체 회복으로 과장하지 않는다. |
| **PASS P-7 · 미확정 원장 명제 유지** | `SPEC-005.md:1074`; `SPEC-006.md:866` | Q067.2/Q099.1의 대상 동일성과 Q226.2/Q229.2의 구조 edge/fact 대응을 확정하지 않았다. `direct-fact-worktable.md:81-84`와 `root-cause-next.md:11,23`에 맞게 적재 규칙이나 수혜 건수를 만들지 않았다. |

## WORK 전에 닫을 결정

**사용자 제품 판단:** 안전 추가 페이지의 최초 1쪽 보호·rank 갱신 순서와 8KB 소진 후 일반 예산 보충 여부(`SPEC-006.md:313,874`), hard stop에서 채택된 사실만으로 답할 범위(`SPEC-006.md:459,876`), 고정 50의 최소 정확성 개선량·허용 TTFT 악화 폭 및 239×3 승격(`SPEC-006.md:868,876`). 현재 4걸음·20/8/15KB를 바꾸려면 별도 사용자 결정이 필요하다.

**기술 설계·발주 입력:** 006의 과거 메모 우선 문구 수정(F-1), 005 선택 관계/전역 메모의 모드·경로·schema·상한과 실제 R8/메모 검증(W-1), page 응답의 전체 배제와 비용 기록·tuple 상태 전이 구현(`SPEC-005.md:860`; `SPEC-006.md:311,341`), 추가 호출의 전체 deadline·개별 timeout 숫자와 실패 trace(W-2). 관계 Hub WORK가 먼저 계약·관문을 통과하고 앱 WORK가 그 응답을 받아야 한다(`SPEC-005.md:1044`; `SPEC-006.md:872`).
