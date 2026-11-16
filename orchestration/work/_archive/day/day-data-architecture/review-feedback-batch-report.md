# 리뷰 리포트 — day-data-architecture / code · 화면 피드백 수정 묶음 (커밋 전 · 2026-11-06)

대상: 마지막 커밋 `3cbb2e08` 이후 미커밋 변경 전부(32 파일 · +908/−203 · 새 파일 `services/outbox_kick.py` · migration `0005_outbox_sender` · `tests/day/board/test_outbox_kick.py` · `home.html` 삭제).
읽기 전용으로 봤다. KOS 호출은 하지 않았다. **compose 는 건드리지 않았다.** 테스트는 `-m "not infra"` 만 돌렸다.
기준: `board-feedback.md` F1 · F3 ~ F16(F2 취소) · SPEC-002 ⑥⑦⑧ · 원천 `procedure-board-decisions.md` · 작업 리포트 8개 · Issue #230 v7 · #231 v4.
범위가 커서 백엔드(F3 · F4 · F5 · F7 · F10 · F16 · migration)와 화면(F1 · F6 · F7 · F9 · F11 ~ F15 · day.js)을 두 갈래로 나눠 읽었다. 아래 지적은 파일:줄을 다시 열어 확인한 것이다.

## 판정: WARN (FAIL 0) — 커밋 가능

피드백 항목은 결정대로 들어갔다.
- 규칙 위반(손 CSS · 인라인 스크립트 · `hx-on` · `innerHTML` · 실데이터 · 비밀값)은 0이다.
- 누른 사람 토큰 · migration 0005 · 데모 연결만 여는 trial 쓰기 · 바로 보내기의 중복 방지가 맞다.

머지 전에 고치면 좋은 것은 **W1(바로 보내기 발행에 시간 상한 없음 — 조작 응답이 Redis 에 매달릴 수 있음)** 이다. 한 줄 수정이다. 나머지는 낮음이거나 데모 실물 확인 대상이다.

## 직접 돌린 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **299 passed · 155 deselected / 3.4s** |
| `uv run ruff check backend scripts` | All checks passed |
| grep(`templates/**` · `day.js`) | `style=` 0 · `<style>` 0 · `hx-on` 0 · `on*=` 0 · `<script>` 본문 0 · `innerHTML`/`eval`/`new Function` 0 · tailwind 임의값 0 |
| `day.css` 빌드 | 첫 줄 `source-sha256` = 지금 `app.css` 해시(지문 테스트 통과) |
| 비밀값(`deploy/local.env` 의 KOS 키 · 테넌트 · 시스템 이메일 · 비밀번호 · `DAY_ADMIN_EMAILS` 값) | 추적 · 미추적 파일 0 |
| 실데이터(`명동` · `세라미크`) | 금지 문구 · 부정 단언 3곳뿐 |
| `KOS_TRIAL_WRITES_ON_LIVE` | 기본 `False`(`config.py`). `local.env` · compose 에 없음 = 꺼짐 |

## 피드백 항목별

| # | 판정 | 근거 |
|---|---|---|
| F1 팝오버 위치 | 결정대로 | `day.js:94-113` — 버튼 아래(넘치면 왼쪽으로 당김 · 아래 공간 없으면 위) · 덮개 없는 `div.day-pop`(`ui.html:343-346`) · 바깥 클릭 · Esc · X 로 닫힘. **폭은 480**(`--day-pop-w`×2 · `app.css:502`). 피드백 표는 「약 640」, 작업 리포트 c 는 사용자 「시안 비율로」 정정이 근거라 했다 → `board-feedback.md` F1 줄을 고칠 것(코디) |
| F3 다시 호출 | 결정대로 | 아래 따로 |
| F4 줄 순서 | 결정대로 | `board_rules.py:448-464` 진행중(시작 → 오더) → 대기(오더) → 완료(완료 시각) · 단위 테스트 |
| F5 귀가 대기 → 판에서 빠짐 | 결정대로 | `board_rules.py:23 · 66-73` 판 카드 = 시술 대기 · 시술 중만 · 단위 테스트(`test_board_rules.py:92-`). 조작은 409 `visit_home`(`board.py:110`). 화면 테스트는 W5 |
| F6 필터 · 보기 바꾸기 뺌 | 결정대로 | `board_main.html:12-13` |
| F7 입실 → 국적 | 결정대로 | 값 그대로 · 없으면 안 그림(`board_parts.html:116-117`) · 스냅샷 `queries/board.py:96` · `board_rules.py:484 · 536-540 · 560-564` 변환 없음 |
| F9 손잡이 아이콘 | 결정대로 | `ui.grip` · `icons.html:19` = 시안. 권한(edit) 없으면 그리지 않음 |
| F10 누른 사람 토큰 · 쓰기 열기 | 결정대로 | 아래 따로 |
| F11 창 위치 · 「0개」 · 판 사라짐 | 결정대로(확인 남음) | `pop_trigger`(`board_parts.html:148`) · `fillPickProcs` 가 `form=` 체크를 센다(`day.js:285-301`) · 열린 동안 판 받기 미룸(`busy`). 원인 = 「오래 열린 탭의 옛 day.js + 새 조각」(작업 리포트 c) → 정적 파일 판이 다르면 새로 읽는 장치(`day.js:634-638` · `base.html:11` · `board_main.html:7`). 재현 증명은 없다 — **사용자가 새 탭에서 한 번 확인**(W4) |
| F12 다시 누르면 선택 해제 | 결정대로 | `day.js:504-513` 카드 · 인박스 |
| F13 수락 · 재호출 작은 팝오버 | 결정대로 | 한 칸 · 폭 **240**(피드백 표 값 · 시안 `.pop` 은 320) · 최대 높이 380 · 머리 · 버튼(`ui.html:368-409`) |
| F14 X 닫힘 | 결정대로 | `data-day-pop-close`(`ui.html:368`) → `day.js:502` |
| F15 빈 판 문구 뺌 | 결정대로 | `board_main.html:53` |
| F16 바로 보내기 | 결정대로(W1) | 아래 따로 |
| 로그인 뒤 갈 곳 | 정리됨 | `after_login()` = `/board`(`login.py:64-70`) · `home.html` 참조 0 |

### F3 다시 호출

- 호출 대상(`pickable`) = 준비중 · 호출 · 수락(`board_rules.py:167-173`). 진행중 · 완료는 `task_not_pickable`.
- 유효 호출 = 그 시술이 든 가장 최근 호출(`:49-57`). 앞 수락은 새 호출 기준으로 찾지 않으므로 무효가 되고, `start_block` 이 `call_not_accepted` 로 막는다(`:226-237`).
- 앞 호출의 `closed_at` 은 그 호출을 유효 호출로 갖던 시술이 **전부** 새 호출로 넘어갔을 때만 채운다(`board.py:463-474 · 504 · 557`, `closed_at IS NULL` 조건). `doctor_call_task` 는 새 호출에 더하기만 해 이력이 남는다. 맞다.
- KOS: 다시 호출의 `call-tasks-doctors` 재전송은 cc D-26 · D-27 근거의 **trial** 이다. 데모 연결이거나 `KOS_TRIAL_WRITES_ON_LIVE` 일 때만 계획에 들어간다(`writes.py:114-121`). → W2 · W3.

### F10 누른 사람 토큰 · migration 0005 · 데모만 열림

- 모든 쓰기 `sender_staff_id = current.staff_id`(`board.py:291`). 대리 수락이면 누른 간호사다. event actor 는 수락한 의사로 남는다(`:604-614`). KOS `doctorIds` = 수락한 의사 외부 id(`:621-629` · `writes.py:122-129`). 테스트 `test_KOS_쓰기는_누른_사람_이름으로_적재`(의사 ≠ 누른 간호사)가 있다.
- migration `0005`: `external_outbox.sender_staff_id` NULL 허용 · FK `staff.id`(이름 규칙 `op.f`) · backfill 없음 · downgrade 는 FK → 칸 순. 모델 `models/task.py:183` 과 맞고 HEAD 테스트도 갱신했다. 칸이 빈 옛 행은 `event_log.actor_staff_id` 로 토큰을 찾는다(`outbox.py:360-362`). 옛 수락 행은 의사 토큰을 기다리다 1800초 뒤 failed 가 된다 — 로컬 옛 데이터라 낮음.
- 열린 쓰기:
  - HAR 확인 6가지는 모든 연결에 열린다.
  - **trial 다섯은 데모 연결에만 열린다**: 시작 취소 `PROCEDURE_WAITING` · 귀가 대기 `PROCEDURE_DONE` · 완료 취소 `complete=false` · `cancel-flow-tasks` · 다시 호출 재전송. 판단은 `factory.py:96-98`(`trial_writes = is_demo or 설정`)이다. 보내기 직전에도 `writes.py:63-78` 이 다시 가른다(다시 호출 재전송은 본문이 처음 호출과 같아 계획에서만 막힌다). 어댑터 캐시 지문에 `is_demo` 를 넣어 연결이 바뀌면 다시 만든다(`factory.py:36`).

### F16 바로 보내기

- `board._finish`(`:329-336`): commit → `board_changed` → 쓰기가 있으면 `outbox_kick.send_now`. 트랜잭션 밖이고, 쓰기 0건이면 발행하지 않는다.
- `send_now` 는 태스크 이름으로 `AsyncKicker.kiq` 하고, 예외는 삼키며 이름만 로그로 남긴다(`outbox_kick.py:29-39`). 응답 실패로 번지지 않는다.
- 중복: 병원별 Redis 잠금(겹치면 `skipped_locked`) + pending → sent 조건부 UPDATE 로 두 번 나가지 않는다. 실물(작업 리포트 c)에서 발행 +0.10초 · 10초 회차 `done {}` 로 겹침 없음을 확인했다.

## WARN

### W1. 바로 보내기 발행에 시간 상한이 없다 — `services/board.py:335` · `services/outbox_kick.py:35` · `common/tasks/broker.py:24-36`
- 조작 응답 안에서 `await kicker.kiq(...)` 를 기다린다. broker 는 `redis_url` 만으로 만들어 socket timeout 이 없고, `asyncio.timeout` 으로 감싸지도 않았다. Redis 가 거부가 아니라 **멈춰 있으면** [시작] · [호출] 응답이 같이 멈춘다. 예외를 삼키는 처리는 「실패」만 막고 「멈춤」은 못 막는다. AGENTS 「async 경로에 timeout 명시」 위반이다.
- 고칠 방향: `send_now` 안을 `async with asyncio.timeout(1.0)`(설정값)으로 감싸 넘으면 로그 + False. 또는 commit 뒤 응답을 막지 않게 `asyncio.create_task`(참조 보관). 앞의 것이 단순하다. DB 없는 테스트 1(멈추는 가짜 broker → 상한 안에 False).

### W2. 다시 호출 재전송(trial)의 확인 조건이 KOS 상태와 안 맞을 수 있다 — `emr/kos/writes.py:114-121`
- 이미 수락된(KOS 에서 READY · doctorIds 있음) 시술에 `call-tasks-doctors` 를 다시 보내고 확인 조건을 `status=waiting` 으로 둔다. KOS 가 READY 를 유지하면 조건이 끝내 맞지 않는다. 그러면 stale(180초) 뒤 failed 가 되고, 그 방문의 뒤 쓰기도 함께 막힌다.
- KOS `doctorIds` 를 비우는 쓰기가 없어서, 동기화 뒤 줄에는 앞서 수락한 의사가 `kos_doctor` 로 계속 보일 수 있다(`board_rules.py:131-136`).
- 반대로 이미 WAITING 인 다시 호출은 조건이 바로 맞아, 보냈는지를 증명하지 못한다.
- 데모 연결에만 열리므로 **데모 실물 1회로 KOS 동작을 확인한 뒤** 조건을 정할 것(A8 · W5 b 와 같이).

### W3. 운영 연결에서 「새 호출 + 다시 호출」을 섞어 고르면 처음 호출분도 KOS 에 안 간다 — `services/board.py:525`
- `is_recall_of(tasks)` 가 하나라도 이미 호출된 시술이면 `recall=True` 다. trial 이 꺼진(운영) 연결에서는 `call_doctors` 쓰기 전체가 `not_supported` 가 되어, 같이 고른 **처음 호출 시술까지** KOS 호출이 빠진다. 방 · 담당자만 나간다. 기록에는 드러나지만 반쪽이다.
- 고칠 방향: 처음 호출분과 다시 호출분을 나눠 `call_doctors` 를 둘로 계획한다. 지금은 운영 연결이 없으니(dev = 데모만) 운영 열기 전에 고치면 된다.

### W4. F11 「판 사라짐」은 원인 설명만 있고 재현 증명 · 회귀 테스트가 없다 · 새로고침 장치의 범위
- 「옛 day.js + 새 조각」 설명과 정적 파일 판 비교 → 새로 읽기(`day.js:634-638`)는 그럴듯하다. 사용자에게 **새 탭에서 한 번 확인**을 받을 것.
- 장치의 위험: `asset_v` 가 파일 **mtime**(`web.py:41-46`)이다. api 레플리카 · 이미지마다 mtime 이 다르면 응답마다 판이 달라 새로 읽기를 되풀이할 수 있다. 지금(단일 로컬)은 문제없다. 배포 Delivery 에서 빌드 값(`day.css` 첫 줄 sha 등)으로 바꿀 것. 조작 응답에서 새로 읽기가 나면 그 순간 화면 상태(체크 등)가 사라진다 — 배포 직후 한 번뿐이라 받아들임.

### W5. 테스트 몇 곳이 결정을 잠그지 못한다(「조용히 통과」 — 아래 표)

### W6. 낮음
- 팝오버는 `position: fixed` 인데 `.day-board` 스크롤 때 위치를 다시 잡거나 닫지 않는다. 판을 스크롤하면 버튼에서 떨어져 뜬다(`day.js:135` 는 resize 만).
- Tab 으로 팝오버 밖에 나가도 안 닫힌다.
- `app.css:499-516` 새 규칙에 날 px(6 · 10 · 12 · 14 · 16)가 있다. 토큰 파일 안이고 기존 `.day-call__*` 와 같은 방식이라 규칙 위반은 아니다.
- 주석이 옛 상태 그대로다: `board.py:719` 「KOS 쓰기는 닫혀 있다」 · `:779` 「둘 다 닫혀 있다」 → trial 로. `test_board_page.py:58` 「E09 · E10(자리만)」. 테스트 이름 `test_병원_하나면_쿠키를_심고_견본으로_간다…`(`test_web_login.py:44`) → 지금은 `/board`.
- `cancel-flow-tasks` 본문 `reason=CANCEL` 은 cc 에서 가져온 모양이고 HAR 이 없다(trial · 데모 실물로 확인).

## 조용히 통과하는 자리

| 자리 | 왜 · 고칠 방향 |
|---|---|
| `test_board_page.py:78` F5 판 순서 | `order[4:] in ([], [V5])` 라 귀가 대기 카드가 판에 남아도 통과한다. `:107-108` 도 `if … in html:` 안이다. 서버 판 조건은 확정됐고 규칙 단위 테스트가 지키니 실해는 없다. 화면 테스트도 `== []` 로 고정할 것 |
| `test_outbox_kick.py` 「commit 뒤 발행」 | `commits == 1` 만 보므로 발행을 commit 앞에 해도 통과한다. 발행 시점의 commit 수(=1)를 기록해 순서를 단언할 것 |
| `test_kos_board_contract.py` `test_cc_근거_쓰기는_trial_에서만_열린다` | `[1:]` 로 잘라 데모 연결의 다시 호출 계획 경로 · 본문은 검증하지 않는다 |
| 운영 연결(`is_demo=False`) API 경로 | `board.py:261` `trial_writes(...)` 를 `True` 로 바꿔도 깨지는 API 테스트가 없다(planner 단위만). W3 섞어 고르기도 테스트 없음 |
| day.js 동작(F1 위치 · F12 해제 · F14 X · F11 N개) | JS 회귀 테스트가 없다(마크업 단언만). `test_정적_파일_판…` 은 `reload()` 글자만 본다. 브라우저 실물 · 스크린샷으로 대신했다 — 받아들임 |

## 코디가 할 것

- `board-feedback.md` F1 폭(640 → 480) · F13(240 · 시안 320 아님) 표기를 실제 결정으로 고친다.
- 사용자 새 탭 확인(F11).
- 데모 실물에서 trial 쓰기 다섯(특히 다시 호출 재전송 · `cancel-flow-tasks` 본문)의 KOS 동작 확인 → W2 · W6 의 확인 조건 · 본문 확정.
