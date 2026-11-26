# merge-dev-2 결과 보고 — 코드 ← origin/dev · 스펙 ← origin/main

## 상태: done (두 워크트리 모두 MERGE_HEAD 상태 · 충돌 0 · 전부 `git add` · 커밋 안 함)

| 워크트리 | HEAD | MERGE_HEAD | 결과 |
|---|---|---|---|
| 코드 `CENTURION_DAY/day-app-re1` | `ab8f6553` | `d03baacb`(origin/dev) | 충돌 5 풀림 · staged 87 파일 |
| 스펙 `mediness-mediness/day-app-re1-spec` | `a018f4fa` | `ae8cec61`(origin/main) | 충돌 6 풀림 + 우리 번호 다시 매김 · staged 13 파일 |

커밋 · push · rebase · stash · reset 은 하지 않았다. 로컬 스택(11040) · 시뮬레이터 · KOS 실물은 건드리지 않았다(`check.sh` 는 격리 인프라).

## 1. 코드 — 충돌 5 푼 방법

| 파일 | 충돌 | 푼 방법 |
|---|---|---|
| `app/lib/ui/theme.dart` | 우리 `consultWait` · `consult`(주석 「개정 ㉒」) vs dev `reception` 추가 + 같은 두 색 | dev 블록(`reception = Ms.primary` + 주석) 그대로 + 우리 줄 끝 주석 유지. 색 값은 둘이 같다 |
| `backend/day/routers/api/board.py` | import — 우리 `iso` · `chart_conflicts_json` · `chart_saved_at` · `board_photos` vs dev `board_sort` | 합집합: `from day.policies.board_rule_values import board_sort, iso` + 우리 두 import |
| `backend/day/services/board_events.py` | import — 우리 `VisitId` vs dev `ExternalOutbox` | 합집합: `EventLogId, HospitalId, VisitId` · `EventLog, ExternalOutbox` |
| `backend/tests/architecture/test_api_contracts.py` | schema 모듈 목록 — 우리 `board_charts` · `photos` vs dev `board_room_view` | 셋 다 |
| `backend/day/static/day.css` | 생성 파일 | 손으로 안 풂 — dev 판을 꺼낸 뒤 `scripts/build-css.sh` 로 다시 생성(143.8KB). `check.sh` 의 CSS 재현 검사 통과 |

## 2. 코드 — 자동 합친 겹침 8 확인

| 파일 | dev 쪽 변경 | 우리 쪽과의 관계 · 판정 |
|---|---|---|
| `backend/day/emr/base.py` | `WritePlanner.supports(kind)` 추상 메서드 · `EmrAdapter.system_write_token()`(기본 None) | 우리 추가(`identity` 계열 — 여권 스캔 고객 수정 · 사진 · 문진 제출)와 다른 메서드. `WritePlanner` 구현체는 `KosWritePlanner` 하나이고 dev 가 `supports` 를 구현해 둠(`emr/kos/writes.py:476`) → mypy 통과. 뜻 맞음 |
| `backend/day/emr/kos/__init__.py` | `KosAdapter.system_write_token` 추가(「방 배정」 자동 완료 전용 시스템 토큰) | 우리 identity 쓰기 메서드와 겹치지 않음. 우리 쓰기는 여전히 직원 토큰 경로. 뜻 맞음 |
| `backend/day/schemas/events.py` | `KosFailedEvent.eventId` 설명 글만 바뀜 | 이벤트 종류는 그대로. 우리 `display` 이벤트(`board_events.display_changed`)와 겹치지 않음 |
| `backend/day/static/day.js` | 방별 순 `[data-day-room-view]` 재요청 · `ResizeObserver` 칸 높이 보조 | 우리 예약 상세 · 띄우기 · 문진 코드와 다른 영역. ESLint · 프런트 시험 131/131 |
| `backend/day/styles/app.css` | 방별 순 방 칸 스타일 | 다른 선택자. CSS 재생성 · Stylelint 통과 |
| `backend/tests/architecture/test_screen_copy.py` | 「방이 비었어요」 · 「… 시술 중에서 이동 진행중입니다」 등록 | 우리 등록 항목과 다른 키. 화면 글자 레지스트리 시험 통과 |
| `app/lib/core/copy.dart` | `sortWaitLabel` · `sortRoomLabel` · `emptyRoomLabel` · `holdRoomLine` | 파일 끝에 붙음. 우리 글자와 이름 겹침 없음 · `flutter analyze` 0 |
| `scripts/frontend/tests/fixtures/reservations-page.html` | #286: 레일 「예약」 · 「고객」 · 헤더 「예약 현황」 탭을 `<a>` → `<span>`(링크 막음) | 우리 변경(SSE `sse-swap="reservation,write_confirmed,display"`)은 다른 줄 → 둘 다 남음. 메뉴는 **되살리지 않음**. 예약 화면 · 예약 상세 버튼 시험 함께 통과 |

migration: dev 새 revision 없음. `uv run alembic -c backend/migrations/alembic.ini heads` = `0029_display_questionnaire_kos (head)` 1개(down = `0028_visit_discharge_reason`).

## 3. dev 변경이 우리 기능에 주는 영향

- **동작 영향: 확인된 것 없음.** 충돌은 import · 목록 합치기뿐이고, 시험 전체가 통과했다.
- #292 「KOS 담당자 = 누른 직원」은 판 조작(호출 · 귀가 대기 · 바로 시작)의 assignees 만 바꾼다. 우리 쓰기(여권 스캔 고객 수정 · 사진 · 문진 제출 — `emr/kos/identity.py`)는 그 경로를 지나지 않는다.
- `WritePlanner.supports` 는 부르는 쪽이 먼저 확인하라는 새 계약이다(`base.py:108-111`). 지금 이것을 부르는 곳은 `services/board_room_assign.py:313-314` 뿐이다. 우리 새 쓰기는 planner 를 거치지 않으므로 바꿀 것이 없다.
- `theme.dart` 의 `Day.reception` 이 새로 생겼다(dev). 예약 상세 단계 색을 우리가 따로 정의한 곳은 없다.

## 4. 스펙 — 충돌 6 푼 방법

먼저 **merge base(`b152d463`) 이후 우리가 넣은 줄에서만** 번호를 다시 매겼다(base 에는 다시 매긴 번호가 하나도 없어서 우리 쪽에만 생긴 번호임을 확인함). 그다음 3-way 로 다시 합쳤고, 남은 충돌을 아래처럼 풀었다.

| 파일 | 충돌 | 푼 방법 |
|---|---|---|
| SPEC-002 | ① `last_updated` ② sources ③ 머리 개정 인용 ④ 범위 표 두 행 ⑤ 「개정 — 달라진 곳」 절 | ① main `2026-11-26` ② 두 쪽 다 ③ 최신이 위로: 우리 ㉜ → main ㉛ → main ㉚ ④ 칸 단위로 합침(1행은 main 쪽 변경 「빈 방 칸 보임」, 2행은 우리 쪽 변경 「차트 쓰기 넣음 ㉜」) ⑤ 번호 순: main ㉛ 절 → 우리 ㉜ 절 |
| SPEC-003 | ① `last_updated` ② 머리 개정 인용 ③ U 절 ④ 서버 의존 D 표 | ① main ② 번호 순: main ㉑ → 우리 ㉒ · ㉓ ③ main U-23(정렬 탭) → 우리 U-24 ~ U-31 ④ main D-7 → 우리 D-8 · D-9 |
| SPEC-005 | ① 머리 개정 인용 ② 「정할 것」 OQ 표 | ① main(KOS 호출 알림) → 우리(띄우기 푸시 + 보충) ② main 「KOS 에서 건 호출」 OQ-N21 ~ N24 → 우리 「띄우기」 OQ-N25 · N26 |
| SPEC-007 | `last_updated` | main. 머리 고침 인용은 자동으로 합쳐짐: main 고침 5 → 우리 고침 6 |
| 30-work | 같은 칸에 두 쪽이 Delivery 링크를 덧붙임(SPEC-002 · 003 · 005 · 007) | 칸 안에서 main 링크 → 우리 링크 순으로 이어 붙임 · 상태 `in_dev` 그대로 |
| log | 행 묶음 | 날짜 내림차순: main 11-26 행 9개 → 우리 11-25 행 7개 → main 11-25 행 11개. 두 쪽 행을 모두 남김 |

합친 뒤 생긴 `>` 빈 인용 줄 겹침 3곳(SPEC-002 · 003 · 005)을 정리했다.

### 스펙 번호 대응표(우리 것만 바뀜 · main 번호는 그대로)

| 이름공간 | 바뀌기 전(우리) | 바뀐 뒤 | 바꾼 수 | 사유(main 이 먼저 쓴 번호) |
|---|---|---|---|---|
| DAY-SPEC-002 개정 | ㉚(앱 차트 · 사진 `/api` JSON 짝) | **㉜** | 48 | main ㉚ = KOS 원장 호출 · ㉛ = 방 배정 자동 완료 |
| DAY-SPEC-002 OQ | OQ-99 · OQ-100 | **OQ-119 · OQ-120** | 5 · 3 | main OQ-99 ~ OQ-118 |
| DAY-SPEC-003 개정 | ㉑(차트) · ㉒(WORK-002) | **㉒ · ㉓** | 68 · 83 | main ㉑ = 정렬 탭 · 방별 순 |
| DAY-SPEC-003 U | U-23 ~ U-30 | **U-24 ~ U-31**(+1) | 152 | main U-23 = 정렬 탭 · 방별 순 |
| DAY-SPEC-003 OQ | OQ-A63 ~ OQ-A91 | **OQ-A67 ~ OQ-A95**(+4) | 147 | main OQ-A63 ~ A66 |
| DAY-SPEC-003 서버 의존 | D-7(차트 JSON) · D-8(예약 JSON) | **D-8 · D-9** | 6 · 2 | main D-7 = 방별 순 서버 값 |
| DAY-SPEC-005 OQ | OQ-N21 · OQ-N22 | **OQ-N25 · OQ-N26** | 5 · 6 | main OQ-N21 ~ N24 |
| DAY-SPEC-007 고침 | 고침 5(WORK-002) | **고침 6** | 97 | main 고침 5 = 「방 배정 있음」 판정 |

- 바꾼 범위: SPEC-000 · 002 · 003 · 004 · 005 · 006 · 007 · `20-spec.md` · `10-decision.md` · `30-work.md` · `log.md` 의 우리 줄(본문 · 다른 문서 참조 · 표 · 대응표).
- 일부러 **안 바꾼 것**: `20-spec.md` 의 base 줄 두 곳(「정렬 탭 … — 개정 ㉑」 · 「되돌리기 … — 개정 ㉒」 = SPEC-002 의 ㉑ · ㉒). 「DAY-SPEC-002 개정 ㉑ · ㉒」 같은 SPEC-002 참조. SPEC-002 base 에 목록 번호로 쓰인 「㉚ **C36**」. 리뷰 번호(W7 · W8 · U1 · S1 · L4)와 「결정 4」는 각 리포트 · 개정 안에서만 뜻이 있는 참조라 그대로 뒀다.
- 맨 앞의 넓은 겹침 검사(merge base 뒤 두 쪽이 같은 ID 를 새로 쓴 경우)에서 남은 겹침은 위 리뷰 번호 같은 범위 안 참조뿐이다.

### 끊긴 참조 검사(grep · 합친 결과 전체 문서)

| 검사 | 참조 수 | 정의 없음 |
|---|---|---|
| OQ-A* → SPEC-003 OQ 표 행 | 92 | 0 |
| OQ-N* → SPEC-005 OQ 표 행 | 26 | 0 |
| SPEC-002 OQ-9x ~ 120 → SPEC-002 OQ 표 행 | 31 | 0 |
| SPEC-003 U-* → `#### U-n.` 절 | 20 | 0 |
| 「SPEC-003 개정 ㉑ ~ ㉙」 → SPEC-003 머리 개정 | 3 | 0 |
| 「SPEC-002 개정 ㉑ ~ ㉟」 → SPEC-002 머리 개정 | 12 | 0 |
| 「SPEC-007 고침 n」 → SPEC-007 머리 고침 | 3 | 0 |
| SPEC-003 D-7 ~ D-9 → 서버 의존 표 행 | 3 | 0 |

뜻 검사도 했다. 합친 결과에 남은 `U-23` 은 모두 정렬 탭 · 방별 순 뜻이다. 차트 · 예약 · 문진 · 여권 문맥에 SPEC-003 `개정 ㉑`, 띄우기 · 문진 · 여권 문맥에 `고침 5`, 차트 문맥에 `개정 ㉚` 이 남은 곳은 없다. 손으로 본 의심 줄은 모두 SPEC-002 자기 ㉑ 이거나 main 쪽 문장이었다. 충돌 표시 0 · 중복 정의 0(OQ-A3 이 둘인 것은 main 에도 있던 그대로).

## 5. 시험 수치(코드 워크트리 · 합친 상태)

| 검사 | 결과 |
|---|---|
| `uv run alembic … heads` | 1개 — `0029_display_questionnaire_kos` |
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **544 passed** · ~81 skipped · 0 failed |
| `scripts/check.sh`(전체 1회) | **exit 0** — 구조 · Jinja(704 소스) · ruff · format · mypy · taut-audit · taut-check · frontend(**131/131**) · tests(**3185 passed** · 393s). 증거 `.local/checks/20261126-172634-51501` |

실패가 없어서 합치기 때문인지 원래 깨진 것인지 가를 것도 없다.

## 6. 남은 위험 · 코디가 확인할 것

1. **코드 주석 · 시험 설명이 옛 스펙 번호를 가리킨다.** 우리 코드 변경분(`55e60aa4..ab8f6553`)에서 스펙 번호를 인용하는 것이 대략 SPEC-007 `고침 5` 81 · SPEC-003 `U-23 ~ U-30` 116 · `OQ-A63+` 43 · `개정 ㉒` 30 · SPEC-002 `개정 ㉚` 22 · `OQ-N21/22` 2 · `OQ-99/100` 1 이다(약 119 파일). dev 코드는 main 번호를 쓴다(예: `theme.dart` 「DAY-SPEC-003 U-23 ② · OQ-A65」 = 정렬 탭). 그래서 합친 코드 안에 같은 번호가 두 뜻으로 섞여 있다. 브리프 범위(스펙 문서)와 「합치기와 무관한 수정 금지」에 따라 **코드는 손대지 않았다.** 위 대응표대로 기계적으로 바꿀 수 있다 — 별도 dispatch 로 할지 정해 달라. `test_screen_copy.py` 의 VISIBLE 값(스펙 인용 글)도 여기에 들어간다. 화면 글자는 아니다.
2. 스펙 문서의 개정 머리 · 대응표 안 「다른 문서 참조」 번호도 모두 따라 바꿨다. 다만 mediness PR #964 본문 · GitHub Issue #281 · #282 · #287 · #288 본문에 옛 번호(SPEC-003 개정 ㉑ · ㉒ · U-23 등)가 있다면 그쪽은 이 작업 범위 밖이라 그대로다.
3. SPEC-002 머리 개정 인용 순서를 「최신이 위」(㉜ → ㉛ → ㉚)로 뒀다. 날짜가 모두 11-25 라 번호로 정했다. log 의 11-25 행은 우리 행을 main 11-25 행 위에 두었다(같은 날 안의 시간 순서는 행에 없다).
4. 30-work 의 SPEC-002 칸은 main 의 긴 #289 설명 뒤에 우리 「개정 ㉜ = #281 · #282」가 붙어 읽기가 길다. 뜻은 손대지 않았다.
