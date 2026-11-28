# delivery-fix-1 결과 보고 — Delivery 검수 D1 ~ D9 · Issue #300 · #301 · #302 본문

## 상태: done

## 쓴 길

`mediness start-delivery` 의 정해진 길 — 같은 idempotency key · **contract_version 2** · `scope_delta`(사유) · 같은 baseline origin/main `b9ac374e`(fetch 로 그대로 확인) → `--plan` → `--apply`. `gh issue edit` 는 쓰지 않음.

| Issue | apply 결과 | 새 digest(v2) | next_action |
|---|---|---|---|
| #300 BE | `scope-delta-recorded` · core healthy · baseline ready · execution ready | `sha256:ec58d8e8b4fe8db1578c8f1c310bd86286c1872c937dfc7d3bc1cab2d347ff52` | review-delivery-plan(human_gate) |
| #301 웹 | 같음 | `sha256:3f666dc8bc2e0b3af30b6615ac077a6bf732046894eda6cdfbf6d46524655f28` | 같음 |
| #302 앱 | 같음 | `sha256:a818253ff7c69e8b2593d8afc589e66393a3e2769e16b2d5320736e6732dd55c` | 같음 |

v1 digest 는 이제 stale(승인 receipt 는 v1 에도 적용된 적 없음 · 이번에도 적용 안 함). 파일 = `delivery/wp{1-be,2-web,3-app}-{request,plan,apply}-v2.json` · `.err` · 생성기 `delivery/gen-v2.py`(v1 request 를 읽어 고침). 막힌 것 없음.

## 공통 계약 ① ~ ⑤

한 번 쓰고(`gen-v2.py` `CONTRACT`) 세 Issue 의 target_delta · review_surface 둘째 줄에 같게 붙임 — Issue 본문에서 뽑아 비교: 세 Issue **한 글자까지 같음**(2,079자).

## D 별 반영 자리 (고친 뒤 Issue 본문 `gh issue view` 로 다시 대조 — 전부 ✓)

| D | 반영 자리 | 대조 문자열(본문에 있음) |
|---|---|---|
| D1 | 공통 ① `bands[] {group_id, column_id, start_min, end_min, line, lane_from, lane_to}`(멤버 가장 이른 시작 ~ 가장 늦은 끝 · 행 넘으면 ⓖ) · 앱 Band camelCase `endMin` 새 칸 · #301 「Rule 15 그리기」 띠 = bands 값 · A2 · #302 표 줄 띠 = bands · A1 · #300 배치 값 줄 · schemas 입구 | 세 Issue `bands[] {group_id, …}` · #301 「동행 띠 = `bands[]` 값으로」 · #302 「띠 = `bands` 값으로」 |
| D2 | #300 배치 값 줄 「R71 동행 판정(`can_join` · `valid_members` — `reservation_layout.py:75-87` · `:115-116` `_row` · `:29` `ROW_MINUTES` · `reservation_companions.py:31`)은 30분 그대로 — 배치 행(60분)과 함수 · 상수를 나눔」 · A2 「1시간 행 안 30분 경계를 넘는 두 카드(12:10 · 12:40)는 묶이지 않음 · 자동 빠짐도 30분」 · 수정 후보에 companions · P2 · 공통 ① 놓는 순서 「동행 = 이웃 자리 · 이어진 빈 자리 첫 묶음(OQ-R43)」 | ✓ |
| D3 | #301 새 줄(코디 기본값): 누르기 · 놓기 시각 = **30분 단위 그대로** · y ↔ 분 = 행 높이를 따른 매핑(`resY`) · `day.js:2347` `RES_SLOT_MIN` · `:3058-3066` · `:2074` · SPEC 한 줄은 머지 뒤 재결속 때 · A2 · 수정 후보 · P2 | ✓ |
| D4 | 공통 ② 「웹 = 열 `title` · `interval_minutes` · 앱 JSON = 기존 Column `title` · `intervalMinutes`(새 칸 없음)」 | ✓ 세 Issue |
| D5 | 세 Issue [계약 원천] 줄 — 「spec-baseline:pending」 지움 → 「CLI 가 main 판 target SPEC 이 stable 이라 spec-baseline:ready 로 정함 · main 판은 근거 아님 · 머지 뒤 재결속」 | 본문 `spec-baseline:pending` 0건 |
| D6 | #300 수정 후보: `schemas/reservations.py`(Card · Band `endMin` · Row · Column) · `schemas/reservation_detail.py`(:171 · :225-246) · `routers/api/displays.py` `public_origin`(:55 — 두 벌) · `services/questionnaire_kos.py`(:146-158) · F6 줄 「하나로 모으거나 같은 값 테스트」 · A1 「origin 함수 하나(또는 두 `public_origin` 같은 값 테스트)」 · 문진 6개월 줄 · A4 · A5 「다시 보내기 대상 = 제출 행만(read 행 제외)」 | ✓ |
| D7 | #300 open_questions 에서 「DAY-SPEC-006 OQ-R46 ⓗ 앱 값은 WP-3」 줄 지움 | 본문에 없음 |
| D8 | 공통 ④ 기기 줄 모양(기기명 · 점 초록 연결 · 빨강 미연결 · 상태 · 미연결도 보이고 누름) · #301 [여권 스캔] 줄 · A3 「줄 = 기기명 [점] 상태 · 미연결 줄도 누름」 | ✓ |
| D9 | #302 표 줄 「시간 칸 선 · 회색 글자(`:313-321`) · 대체 행(`:173-174`) = 1시간 행 · 띠 = bands(`:351-363`)」 · A1 · 수정 후보 줄(:52 · :173-174 · :249 · :313-321 · :351-363 · :374-378) · P2 | ✓ |
| 참고 | #300 「동작 변화」 줄 끝 「고객 차트 「초진 설문」(`queries/customers.py:449-454`)에도 `source = read` 행이 보이게 됨(SPEC-000 ④ 귀결)」 · 수정 후보에 customers(읽기만 확인) | ✓ |

그 밖 대조: 세 Issue 본문 `/open/` 0건(새 공개 KOS 호출 없음) · 새 화면 문구 0(「6개월 경과」 = 결정 글자 · D43 · D48 열린 채).

## 바꾸지 않은 것

SPEC 본문(D3 의 SPEC-007 「열 × 30분 칸」 한 줄은 머지 뒤 재결속 때 — 코디 기본값) · 코드 · 승인 receipt · PR #971(머지 안 함) · 30-work · log(이번 고침은 Issue 본문만 — 필요하면 재결속 때 같이).
