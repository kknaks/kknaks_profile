# prod-deploy-re1 frontend-2 결과 보고 — W3 방 옮기기 목록 상태(Delivery #245 v2 · SPEC-002 개정 ⑱ U-15 · E53)

## 상태: done (커밋 · push 안 함)

## 수행 — 바뀐 파일
| 파일 | 줄 | 내용 |
|---|---|---|
| `backend/day/services/board_rules.py` | :27 | `ROOM_TAKEN_STEPS` = 판 카드(procedure_waiting · procedure) · 접수(reception) · 귀가 대기(procedure_done). 상담 단계 · 귀가(completed) · 예약은 넣지 않음(OQ-51 미결) |
| 〃 | :582 ~ | `room_takers()` — 방 → 그 방에 있는 오늘 방문 id: 위 단계 방문의 `visit.room_id` + 그 방문의 점유 방(`hold_room` = 살아 있는 「방 배정」의 방). 같은 고객의 다른 방문도 그대로 셈 |
| 〃 | :599 ~ · :1062 | `rooms_view()` — 스냅샷 `rooms[]` = `{id, title, takenBy: [방문 id]}` · 빈 방 먼저 → 배정됨 · 각 묶음 안 `room.order`(stable sort). **rooms 관련만** 손댐(home_room 등 W5 아님) |
| `backend/day/templates/partials/board_parts.html` | :309 ~ (`room_pop`) | 줄마다 상태 글자 — 원장 목록과 같은 마크업 `<span class="day-opt__status[ is-free]">` · 글자 「비어 있음」 / 「배정됨」 둘만. **옮기는 카드 자기 자신**은 `takenBy` 에서 빼고 판정 → 카드마다 다시 묶음(빈 방 먼저 · 묶음 안 서버 순서). 배정됨 방도 라디오 그대로(고를 수 있음) |
| `backend/day/routers/kit_board.py` | :228 | 견본에 빈 방 「시술실 E」 하나 추가(견본 판의 방은 전부 사람이 있어 「비어 있음」 견본이 없었음) |
| `backend/tests/architecture/test_screen_copy.py` | — | 「배정됨」 근거(SPEC-002 U-15 · E53 개정 ⑱) |
| `backend/tests/day/board/test_board_rules.py` · `backend/tests/day/web/test_board_page.py` | — | 아래 검증 |

## 계약 · 결정
- 스냅샷 `rooms[]` 배정됨 칸 이름 = **`takenBy`**(방문 id 목록 · 스펙 :597 「배정됨 칸 이름은 구현 PR」). bool 이 아니라 목록인 이유: 「옮기는 카드 자기 자신 제외」는 카드마다 달라 서버 한 값으로 못 냄 → 화면이 그 카드 id 를 빼고 판정. 서버 순서는 모든 방문 기준(빈 방 먼저), 화면은 카드 기준으로 다시 묶음.
- 앱(`app/lib`)은 스냅샷 `rooms` 를 읽지 않음(grep) — 앱 영향 없음.
- 원장 목록과 같은 모양: 비어 있음 = `is-free`(파랑) · 배정됨 = 기본(옅은 회색). 묶음 머리 줄 없음(OQ-51 「머리 줄을 둘지」 미결 — 안 둠).

## 검증
- `uv run pytest -q -m "not infra" backend/tests` → **880 passed**(새 rules 시험: 판 카드 · 점유 방 · 접수 · 귀가 대기 · 같은 고객 다른 방문 = 배정됨 / 상담 · 귀가 · 예약 = 안 셈 / 순서 빈 방 먼저 → room.order · 웹: V1 팝오버 = 「시술실 E 비어 있음(is-free)」 → 나머지 7개 「배정됨」 room.order · 라디오 8개)
- `scripts/build-css.sh` → 53.5KB(새 클래스 없음) · 내 파일 `ruff check` · `ruff format --check` 통과 · 인라인 스크립트 · style 속성 0
- 캡처: `fe-captures/fe2-board-room-pop.png` — 견본 판(가짜 값) · 시술실 A 카드 방 옮기기 팝오버(열린 상태는 하네스가 강제 — 수정 1 과 같은 방식)
- pending: infra 시험(`scripts/test.sh` — 사용자 포트 · 프로세스 안 건드림) · 실브라우저 e2e

## 이슈 · 코디가 확인할 것
1. **동시 수정 주의**: 이 작업 중 `uv run ruff format backend/tests backend/day` 를 한 번 돌렸다(내 파일 정리용). 그때 backend 워커가 고치던 `backend/day/emr/*`(base · kos/__init__ · kos/mapper · kos/writes · normalized · sync)가 포맷될 수 있었다 — 그 파일들 `ruff check` 에 줄 길이 오류 2개(`emr/kos/__init__.py:182` · `emr/kos/writes.py:23`)가 있고 이건 그 워커 몫(문자열이라 포맷이 못 고침). 그 뒤로는 내 파일만 포맷함. backend 워커에게 「파일이 바깥에서 바뀌었을 수 있음」 알려 주길.
2. OQ-51(상담 단계 · 귀가 방문 · 묶음 머리 줄) 정해지면 `ROOM_TAKEN_STEPS` 한 줄 · 템플릿 한 곳.
3. 차트 모달 미커밋 변경(fe-1 수정 1 ~ 3) 그대로 남아 있음.
