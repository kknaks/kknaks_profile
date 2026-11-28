# review-delivery-1 — WP 나누기 · CENTURION_DAY #300 · #301 · #302

**판정: WARN** — FAIL 0 · WARN 9.

- 결정 표 11-27 행과 SPEC 개정분의 큰 항목(F1 ~ F6 · F4 · KOS 내부 legacy · Rule 15 ⓐ ~ ⓙ · 앱 표 · D44 · D45 · D46 ② · D47 · D49)은 세 Issue 어딘가에 다 들어갔다.
- 공개 KOS 새 호출은 0이고 지어낸 화면 문구도 0이다.
- 다만 **동행 띠(`bands[]`) 계약이 세 Issue 공통 계약 ①에서 빠졌다.** 그런데 웹 · 앱 둘 다 띠를 그린다(D1).
- **동행 조건 R71 이 배치와 같은 `_row` 함수를 쓰는 코드 입구가 BE 수정 후보에 없다**(D2).
- 1시간 행에서 **빈 칸 누르기 · 옮기기 놓을 자리를 몇 분 단위로 잡을지**가 비어 있다(D3).
- 이 셋은 병렬 구현 전에 Issue 계약에 적어야 한다. 나머지는 이름 · 문장 정리다.

대상:
- 세 Issue(`gh issue view`)의 사람용 본문
- `delivery-1-report.md`
- SPEC 브랜치 `99085866`(`ad317cf4` + 30-work · log)
- 코드 `65506f35`(읽기만)

Issue · 파일 수정은 하지 않았다.

## 지적

| # | Issue / 파일:줄 | 근거 | 고칠 방향 |
|---|---|---|---|
| D1 | #300 · #301 · #302 「BE ↔ 웹 · 앱 계약 ①」 | ① 에는 `rows[]` · `cards[]` 만 있고 **`bands[]` 가 없다**. SPEC 은 띠 = 「멤버를 다 감싸는 상자(가장 이른 시작 ~ 가장 늦은 끝)」로 정했다(`spec-006:318` · OQ-R43 닫힘 `:856`). 길이가 다른 멤버면 상자가 행을 넘을 수 있다(ⓖ). 지금 값 `Band{start_min, line, lane_from, lane_to}`(`policies/reservation_layout.py:59` · `:147` · `schemas/reservations.py:67-74`)에는 끝 · 높이가 없다. 웹 `reservations_parts.html:122-124` · 앱 `reservation_table.dart:351-363` 이 둘 다 이 값으로 그린다. 「화면은 다시 계산 안 함」이면 웹 · 앱이 각자 상자 높이를 지어내게 된다 | ① 에 `bands[] {group_id, column_id, start_min, end_min, line, lane_from, lane_to}` 를 더한다(앱 camelCase `endMin`). 뜻은 「end_min = 멤버 가장 늦은 끝 · 행을 넘으면 ⓖ 그림 규칙」. #301 · #302 범위에 「띠 = bands 값으로」 한 줄 |
| D2 | #300 「배치 값」 · 수정 후보 | 동행 조건 `can_join`(R71 「같은 30분 행」)이 배치와 **같은 `_row()` · `ROW_MINUTES`** 를 쓴다(`policies/reservation_layout.py:75-87` · `:115-116` · `:29`). 그 사용처는 `services/reservation_companions.py:31` · `valid_members`(R67 자동 빠짐)다. 배치를 1시간 행으로 바꾸며 `ROW_MINUTES = 60` 으로 고치면 묶기 · 자동 빠짐 조건이 **조용히 1시간으로 넓어진다**(R71 은 그대로 — `spec-006:318`). 같은 #300 ①의 놓는 순서에도 SPEC ⓑ 의 「동행 = 이웃 자리 · 이어진 빈 자리 첫 묶음」(OQ-R43)이 빠졌다. 지금 문구 「같은 시작이면 R73 · 겹치지 않는 가장 앞 자리」만으로는 시작이 다른 같은 그룹 멤버가 떨어져 놓일 수 있다 | #300 에 두 줄을 더한다. ⓐ 「R71 동행 판정(`can_join` · `valid_members`)은 30분 그대로 — 배치 행(60분)과 함수 · 상수를 나눔」을 범위와 A2 테스트(1시간 행 안 30분 경계 넘는 두 카드는 묶이지 않음)에 넣는다. ⓑ 「동행 = 이어진 빈 자리 첫 묶음(OQ-R43)」을 ① 놓는 순서에 넣는다. 수정 후보에 `services/reservation_companions.py` 를 더한다 |
| D3 | #301 범위 · 수정 후보 · SPEC `spec-007:109` | 웹 `day.js:2347` `RES_SLOT_MIN = 30`(놓을 자리 · 빈 칸 누르기) · `:3065-3066`(y → 시각) · `:2074`(현재 시각 선 y 기본식 `/ 30 × 70`)는 30분 칸을 전제로 한다. SPEC-007 `:109` 「표 빈 칸 누르기(열 × **30분 칸**)」은 이번 개정에서 그대로다. 1시간 행에서 빈 자리를 누르거나 카드를 놓을 때 시각을 30분 단위로 잡을지 · 행(1시간) 단위로 잡을지 SPEC · Issue 어디에도 없다(F1 [+] 은 그룹 간격으로 정해짐). 구현자가 지을 자리 | 코디 기본값 한 줄을 #301 에 넣는다(추천: 「누르기 · 놓기 시각 = 30분 단위 그대로 · y ↔ 분 은 행 높이를 따른 매핑(`resY`)」 — 지금 동작 유지 · 결정 다시 여는 것 아님). 수정 후보에 `day.js` 의 이 세 자리를 적는다. SPEC 쪽 한 줄은 머지 뒤 v2 재결속 때 |
| D4 | 세 Issue ② | 「칸 이름 = BE 가 정하고 이 Issue 에 적음」 — 앱 JSON `Column` 에 이미 `title` · `intervalMinutes` 가 있다(`schemas/reservations.py:31` · `:33`). 빈칸으로 두면 #302 가 기다린다 | ② 를 「웹 = 열 `title` · `interval_minutes` · 앱 JSON = 기존 `title` · `intervalMinutes`(새 칸 없음)」로 고정 |
| D5 | 세 Issue 「[계약 원천]」 줄 | 「최초 Delivery = **spec-baseline:pending**」이라 적었지만 실제 상태는 `spec-baseline:ready`(기술 추적 · delivery-1-report 「막힌 것 2」)다. 한 Issue 안에서 두 말이다 | 「(CLI 가 main 판 stable 로 ready 를 정함 · main 판은 근거 아님 · 머지 뒤 v2 재결속)」으로 바꾼다 — 상태 말을 하나로 |
| D6 | #300 수정 후보 | 빠진 입구가 셋 있다. ① 앱 JSON 모양 `schemas/reservations.py`(Card `endMin` · Band) · `schemas/reservation_detail.py:171` · `:225-246`(`questionnaire.expired`). ② `public_origin` 이 **두 벌**이다(`routers/reservation_displays.py:46` · `routers/api/displays.py:55`) — 앱 상세 `routers/api/reservations.py:104` 가 어느 쪽을 쓸지. ③ 고객 문진 원천을 고객 단위로 바꾸면 `services/questionnaire_kos.py:146-158`(다시 보내기 = 「그 방문 마지막 행」)이 `source = read` 행을 잡지 않아야 한다 | 수정 후보에 위 파일을 더하고, A1 에 「같은 `public_origin` 하나(또는 두 함수 같은 값 테스트)」를 넣는다. A4 · A5 에 「다시 보내기 대상 = 제출 행만(read 행 제외)」 한 줄 |
| D7 | #300 「아직 결정이 필요한 것」 | 「DAY-SPEC-006 OQ-R46 ⓗ 앱 값은 WP-3」 — OQ-R46 은 닫혔다(ⓗ = 앱 지금 30분 칸 × 2). 열린 것처럼 읽힌다 | 줄을 지우거나 「(닫힘 · ⓗ · WP-3 가 그 값을 씀)」 |
| D8 | #301 범위 · A3 | F5 기기 팝오버 줄 모양 「기기명 · 점(초록 연결 · 빨강 미연결) · 상태 · 미연결도 보이고 누름」(결정 행 F5 · spec-007 규칙 7)이 범위 · 완료 조건에 없다(「기기 줄」만) | A3 에 「줄 = 기기명 [점] 상태 · 미연결 줄도 누름」 |
| D9 | #302 범위 · 수정 후보 | 앱 표는 고정 66 말고도 30분 전제가 더 있다. `reservation_table.dart:174`(rows 없을 때 30분 대체 행) · `:313-321`(30분마다 시간 칸 · 회색 글자) · `:351-363`(띠)이다. Issue 는 「고정 66 · 시작 행 안 lane / line 을 바꿈」만 적었다 | 범위에 「시간 칸 선 · 대체 행 = 1시간 행 · 띠 = bands(D1)」을 더한다 |

참고(판정 밖):
- 고객 차트 「초진 설문」(`queries/customers.py:449-454`)은 이미 고객 단위 마지막 행을 읽는다. 그래서 `source = read`(KOS 에서 낸 문진) 행이 차트에도 보이게 된다. SPEC-000 ④ 가 사본으로 담기로 했으므로 맞는 귀결로 보이지만, Issue 「동작 변화」 줄에 한마디 남기면 QA 가 놀라지 않는다.
- delivery-1-report 의 「pending 아님」 처리(우회 안 함 · 코디 답 a)는 바르다.

## 범위 대조

| 규칙(원천) | #300 BE | #301 웹 | #302 앱 | 판정 |
|---|---|---|---|---|
| F1 오른쪽 70 · 점선 [+] · 툴팁(끝 = 그룹 간격) · 등록 창 (spec-006 U-1 · U-10) | ② 열 값 | 범위 · A1 | 없음(읽기 전용 ✓) | ✓ · 이름 D4 |
| F2 · Rule 15 ⓐ ~ ⓕ(1시간 행 · 5 자리 · 줄 접기 · 길이 비례) | ① · A2 | 그리기 · A2 | 표 · A1 | ✓ |
| Rule 15 ⓖ 행 넘는 카드 | ① · A2 | ✓ | ✓ | ✓ · 띠는 D1 |
| ⓗ 140 / 앱 30분 칸 × 2 | ① | ✓ 140 | ✓ | ✓ |
| ⓘ 오픈 전 · 마감 뒤 · ⓙ 정각 아닌 오픈 | ① · A2 | 왼쪽 글자 · 회색 면 | (값 그대로) | ✓ |
| 동행 띠 상자 · 이어진 빈 자리(OQ-R43) | **없음** | 「멤버 감싸는 상자」 글자만 | 없음 | **D1 · D2** |
| R71 동행 조건 30분 그대로 | **없음** | — | — | **D2** |
| 빈 칸 누르기 · 옮기기 놓을 시각 | — | **없음** | — | **D3** |
| F3 [문진 QR] 한 단계 팝오버 · 이 화면 QR 없앰 · 링크 10분 | ④ | 범위 · A3 | 앱 그대로 ✓ | ✓ |
| F5 기기 팝오버(점 · 미연결 누름) · [여권 스캔] 같은 팝오버 | ④ | 기기 줄 · 모달 카드 없앰 | — | 줄 모양 D8 |
| F6 origin 필수 · 4곳 · 실제 service 시험 | 범위 · A1 · A7 | — | — | ✓ · D6 ② |
| F4 6개월(고객 단위 · env · 재진) · D49 KST 달력 | A4 | A4 | A2 | ✓ |
| D47 앱 「6개월 경과」 · `questionnaire.expired` | ③ | ✓ | A2 | ✓ |
| KOS 문진 읽기 별도 태스크 · 내부 legacy · 공개 0 테스트 | A3 | — | — | ✓ |
| D46 ① inputType · subText 비움 · INPUT_BOX = memo | 범위 | — | — | ✓ |
| D46 ② 제출 id = 읽은 id e2e | A7 | — | — | ✓ |
| D46 ③ 한 건 = 마지막 · ④ 그 고객만 건너뜀 | 범위 · A3 | — | — | ✓ |
| 제출 id 남기기(`identity.py:161-165`) · 백필 안 함 | 범위 · non-goal | — | — | ✓ |
| D44 링크 다시 씀 · 기기 줄 = 취소 → 새 요청 | ④ · A5 | A3 | — | ✓ |
| D45 SSE 다시 그림이 팝오버 안 닫음 | 조각 경계 | A6 e2e | — | ✓ |
| 호출 수 예외(SPEC-002 결정 1) · DAY-ESC-001 참조 | 동작 변화 줄 | — | — | ✓ |
| OQ-D43 · D48 지금 글자 | 열린 것 | non-goal | — | ✓ |
| 모달 디자인 · 외국인 신분 확인 범위 밖 | non-goal | non-goal | — | ✓ |

## 코드 표면 grep

| 입구(grep) | 코드 자리 | Issue 에 있나 |
|---|---|---|
| `detail_view(` 호출 5곳 | `routers/reservation_displays.py:68`(이미 origin) · `routers/reservation_detail.py:179` · `:327` · `:407` · `routers/api/reservations.py:104` | ✓ 4곳 + 이미 있는 1곳 = 전부 |
| `public_origin` 정의 | `routers/reservation_displays.py:46` · `routers/api/displays.py:55` | 하나만 적힘 → D6 |
| `reservation_layout` 사용처 | `policies/reservations.py:28-35` · `services/reservation_companions.py:31` · `tests/day/test_reservation_layout.py` | companions 없음 → D2 |
| 배치 상수 · 함수 | `policies/reservation_layout.py:28-29`(LANES · ROW_MINUTES) · `:115`(`_row`) · `:119`(seat) · `:152`(rows · 축 시작부터 30분) · `policies/reservations.py:53` · `:212-213`(축 08:00) · `:149`(open_min = 0) | ✓(open_min 확인 포함) |
| 앱 JSON 모양 | `schemas/reservations.py:28-35`(Column title · intervalMinutes) · `:43-49`(Card) · `:60`(Row) · `:67-74`(Band) · `schemas/reservation_detail.py:139` · `:171` · `:225-246` | 「presentation」로만 → D4 · D6 |
| 웹 배치 그리기 | `templates/partials/reservations_parts.html:67-73`(카드) · `:93-130`(rows · 띠 · 현재 시각 선) · `static/day.js:2197-2300`(resLayout · R70 66 고정 · `line × slot`) | ✓(파일 단위) · 띠 D1 |
| 웹 30분 전제 | `static/day.js:2074`(현재 시각 선 기본 y) · `:2347` `RES_SLOT_MIN = 30` · `:3058-3066`(놓을 자리 · 빈 칸) | **없음 → D3** |
| 앱 표 | `app/lib/ui/reservation_table.dart:52`(66) · `:173-174`(대체 30분 행) · `:249`(열 폭) · `:313-321`(30분 시간 칸) · `:351-363`(띠) · `:374-378`(카드) | 66 만 → D9 |
| 문진 원천(방문 → 고객) | `services/questionnaire_reads.py:38`(visit_id) · `services/reservation_detail.py:166` · `:187` · `queries/customers.py:449-454`(이미 고객 단위) · `services/questionnaire_kos.py:146-158`(다시 보내기) | reads · detail ✓ · 다시 보내기 → D6 ③ · 차트 참고 |
| 일정 회차 뒤 태스크 발행 | `tasks/emr.py:101-115`(구매 회차 발행 꼴) | ✓ |
| 공개 KOS 경로 | 코드 `/open/` 9 = SPEC-002 목록 9 | 새 호출 0 ✓ |

## 완료 조건 · migration · baseline

- **완료 조건**: 세 Issue 모두 로컬 KOS DEMO 지점 실물 e2e 1회로 확인할 수 있다(#300 A7 · #301 A6 · #302 A4). 자동 테스트도 각자 있다(pytest · 화면 테스트 · flutter test). 웹 · 앱 e2e 가 BE 머지 뒤라는 순서도 적혀 있다.
- **migration**: 없다(새 칸 · 테이블 없음). 인덱스가 필요하면 `0032`(alembic head `20261126_0031` 다음)로 하고, 되돌리기 = downgrade · revert 다. 세 Issue 모두 있다.
- **baseline**: 세 Issue 다 `b9ac374e` + 「[계약 원천] mediness#971 `ad317cf4`」 줄이 있다(D5 의 pending 글자만 고침).
- **공개 KOS · 문구**:
  - 새 공개 호출 0 이고, 문진 읽기 = 내부 `get-questionnaire-submit/legacy` 다.
  - #300 A3 이 「공개 경로 호출 0」을 테스트로 고정한다.
  - 새 화면 문구 0 이다(「6개월 경과」 = 결정 글자 · D43 · D48 = 지금 글자).
