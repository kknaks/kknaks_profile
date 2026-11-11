# 리뷰 리포트 — day-procedure-board-2 / code — CENTURION_DAY#236 backend 단계 (2026-11-10)

대상: `CENTURION_DAY/day-procedure-board-2` 미커밋 diff 15파일(96fff917 이후 · backend 만 — 템플릿 · 화면 라우터 · static · styles 안 바뀜).
SSOT: Delivery #236 v2(A1~A10 · 바뀌는 것 ①~⑯) · DAY-SPEC-002 개정 ⑬ ⑭(U-10 표 · 규칙 5 ~ 9 · 16 · 19 · 23 · 26 · 27 · 케이스 매트릭스 · 스냅샷 모양 · KOS 쓰기 표) · `_RESUME.md` §2.
파일 경로는 `backend/` 기준.

## 판정: WARN (FAIL 0)

backend 몫 Acceptance(A1 · A3 · A4 · A5 · A7 · A8 백엔드분, A2 차트 API)는 스펙대로 구현됐고 테스트도 실제로 막는다. 아래 WARN 5건은 스펙이 말하지 않은 곳(spec-sync 거리)과 테스트 빈칸, 성능이다. 머지를 막을 것은 없다.

검증(직접 돌림):
- `DAY_ENV_FILE=…/local.env scripts/test.sh -q` → **612 passed · 10 failed · 15 errors**(42s). 실패 · 오류 25건은 **전부 `tests/day/web/test_board_page.py`** 이고 원인은 하나 — `jinja2.UndefinedError: 'dict object' has no attribute 'anesthesia'` (`templates/partials/board_parts.html:52` `anesthesia_chip(card)` ← `board_main.html:22` 가 `inbox.need` 항목을 카드로 그림). `inbox.need` 항목이 카드 → `{**need, visitId, card}` 로 바뀐 탓이고, 템플릿은 아직 `card.need` · `a.lastMinutes`(`board_parts.html:56` · `:128` · `:132`)를 읽는다. **백엔드 회귀 아님 — 템플릿 몫(브리프 5 확인).** Python 쪽에 지운 이름(`need()` · `called_ids` · `is_recall_of` · `CALL_LIMIT_MIN` · `ANES_LIMIT_MIN` · `overSec` · `lastMinutes`)을 부르는 곳은 0(`grep`).
- `uv run ruff check backend scripts` → All checks passed · `ruff format --check` → 160 files already formatted.

## FAIL

없음.

## WARN

### W1. 원장 바꾸기가 수락 기록(`doctor_call_accept.doctor_staff_id`)을 새 원장으로 고쳐 쓴다 — 스펙은 말하지 않는다(워커 미결 ①)
- `day/services/board.py:846-851` — 유효 호출의 수락 행 `doctor_staff_id` 를 새 원장으로 `update`. 처음 수락한 원장은 `event_log task.doctor_change.payload.fromStaffId` 에만 남는다.
- 스펙: 규칙 8 「시술마다 `doctor_call_accept`(`doctor_staff_id` = **고른 원장** · `accepted_at`)」 · 규칙 9 「수락에서 누른 사람은 남기지 않는다 · actor = 수락한 의사」 · 규칙 27 「시술 상태 · `started_at` · 호출 · 수락 기록의 **시각**은 그대로, 그 시술의 **담당 원장**이 새 원장」 · 규칙 19 는 ~~`doctor_call_accept.doctor_staff_id` 가 그 원장인 시술~~ 을 지우고 「담당 원장(수락한 원장 · 바꿨으면 새 원장)」으로 바꿨다. 즉 스펙은 「수락한 원장」과 「담당 원장」을 다른 말로 쓰는데, 구현은 둘을 한 칸으로 합쳤다.
- 판단: 화면 · 스냅샷 결과는 스펙과 같다(「{원장} 수락 완료 HH:MM」 = 새 원장 · `accepted_at` 그대로 · 원장 상태 · 검색 담당의 — `test_원장_바꾸기_수락_시술` 이 단언). 규칙 9 와는 부딪치지 않는다(event_log actor 는 그대로). 다만 「누가 수락했나」가 표에서 사라지고, 앱(OQ-29 이전 원장 취소 알림)은 event_log 를 읽어야 한다. 정해지지 않은 자리라 **FAIL 아님** — spec-sync 때 규칙 27 에 「수락 행의 원장도 새 원장 · 처음 수락한 원장은 event_log 에만」 한 줄로 결정을 남기거나, 코디가 사용자에게 확인. (다른 방법: 수락 행은 두고 `task_doctor` 가 event_log 마지막 바꾸기를 우선 — 조회 비용이 W2 만큼 늘어난다.)
- 같이 볼 것: 한 호출에 시술이 둘 이상이면(수락은 호출 통째) 한 시술만 바꿨을 때 「수락 뒤 미시작」 카드는 그 호출 전체가 다시 세고(`board_rules.py:395-428` since = 그 호출 시술들 중 마지막 바꾼 시각), `doctorName` 은 첫 시술의 담당 원장만 보인다(`:427`). 스펙 U-10 「{원장} 수락 n분째」는 원장이 여럿인 경우를 말하지 않는다 — OQ-32 와 같은 빈칸. 구현 선택으로 두되 spec-sync 때 적을 것.

### W2. `doctor_changed_at` 조회가 인덱스 없는 `event_log` 를 매번 훑는다(워커 미결 ②)
- `day/queries/board.py:234-246` — `load_world` 마다(스냅샷 · SSE 다시 그리기 · 모든 조작 · 검색 · 차트) `event_log` 를 `hospital_id` · `visit_id IN (오늘 방문)` · `type` · `payload->>'taskId'` 로 group by.
- `day/models/task.py:152-163` `EventLog` 에 인덱스가 없다(`fk()` 는 인덱스를 만들지 않음 — `models/_columns.py:38`). `event_log` 는 쌓기만 하는 표라 날이 갈수록 seq scan 이 길어진다. 오늘 테스트 규모에선 안 보인다(`test_방문_1개와_10개의_쿼리_수가_같다` 는 쿼리 수만 본다).
- #236 은 「migration 없음」이라 이번에 인덱스를 넣을 수는 없다. 다음 migration 때 `event_log (hospital_id, type, visit_id)`(또는 `(visit_id)`) 인덱스를 넣을 것을 WP/Issue 후속으로 남기기를 권한다. 당장 할 수 있는 것: 조건에 `occurred_at >= 오늘 시작`을 더해도 인덱스 없이는 효과가 작다.

### W3. `touched()` 가 확인 키를 「외부 칸」으로 묶으면서 #236 밖 op 의 superseded 판정도 바뀌었다 — 맞는 방향이지만 그 경우는 테스트가 없다
- `day/emr/outbox.py:66-75` `TASK_KEY_FIELDS` · `:586-597` `touched()` — `status` · `status_not` · `status_in` 을 모두 `status` 칸으로 본다(원장 바꾸기의 `doctors_equal` ↔ 수락의 `doctors_contain` 을 같은 `doctors` 칸으로 묶으려고 넣은 것).
- 그 결과 [종료](`status="done"` · `kos/writes.py:157`) 뒤 「완료 취소」(`status_not="done"` · `:151`)가 보내지면 앞 [종료] op 이 superseded → confirmed 가 된다. 이전에는 두 키가 겹치지 않아, [종료] op 이 확인되기 전에 「완료 취소」가 나가면 다음 조회에서 [종료]가 「안 맞음」으로 세져 `complete=true` 를 다시 보내 KOS 를 되돌릴 수 있었다. 스펙 §3 「뒤 op 이 같은 값을 다시 바꾸면 앞 op 은 confirmed([종료] 뒤 「완료 취소」 — cc SPEC-003 §4.4)」와 맞으므로 **고친 것**이다. 다만 원장 바꾸기 범위를 넘는 동작 변경인데 이 경우를 단언하는 테스트가 없다(`tests/day/emr/test_kos_board_contract.py` 는 호출 → 수락 `:176` · 수락 → 원장 바꾸기 `:286` 만). [종료] → 「완료 취소」 superseded 테스트 1개와 Issue/PR 본문 한 줄을 권한다.

### W4. 원장 바꾸기의 「KOS 외부 id 없음 → skipped」 경로를 테스트가 밟지 않는다
- `day/services/board.py:885-893` — 새 원장 외부 id 가 없으면 `Skipped("change_doctor")`(조용히 건너뛰지 않고 `event_log.payload.kos` 에 남는 패턴). 수락에는 같은 테스트가 있다(`test_의사_외부_id_가_없으면_수락_쓰기는_skipped`) · 원장 바꾸기에는 없다. 코드는 같은 `_queue` 를 쓰니 동작은 맞을 것 — 테스트 1개로 막아 두기를 권한다.

### W5. 화면 라우터 문서 문자열이 옛 `need.overSec` 를 말한다(frontend 몫 · 기록만)
- `day/routers/board.py:32` · `:36` 「카드 `need` 에 `overSec` … 확인 필요는 `need.overSec` 큰 순」 — 이제 `needs[]` · 걸린 시각 이른 순(`board_rules.py:760-777`). 화면 라우터는 frontend 몫이라 이번 diff 대상은 아니지만, frontend 단계에서 템플릿과 함께 고칠 것(fe 브리프에 `inbox.need` 모양은 이미 적혀 있음).

## PASS — Acceptance 별(백엔드분)

| A | 볼 것 | 코드 | 테스트(실제로 막나) |
|---|---|---|---|
| A1 ① | pickable = 준비중만 · 호출에 준비중 아닌 것 섞이면 409 `task_not_pickable` · 다시 부르는 KOS 쓰기 없음 | `board_rules.py:173-185` · `services/board.py:539` `again=set()` | `test_호출은_준비중만_재호출_수락은_닫힘_받을것없음`(호출 · 수락 · 진행 · 완료 각각 `task_not_pickable`) · `test_전체_선택은_준비중이_없으면_꺼진다` · API `test_준비중이_아닌_시술이_섞인_호출은_task_not_pickable` |
| A2 ③ (API) | 차트 = 오늘 판 카드 · 「시술 완료」 탭 방문만 · 그 밖 404 | `services/board.py` `chart()` · `board_rules.py:735` `is_chartable` · `routers/api/board.py` `GET /visits/{id}/chart` | `test_차트는_판과_시술_완료_탭_방문의_메모를_준다`(다른 병원 · 카드 없던 방문 404) · rules `test_차트는_판_카드와_시술_완료_탭_방문만` |
| A3 ⑥ | 「시술 완료」 탭 고객만 · 발음 · 영문 낱말 순서 무관 · 빈칸 · 대소문자 · 담당 원장 · 관리실(`room.title`) · 차트 번호 X · 순서 그대로 · 빈 검색어 = 원래 목록 · JSON = `doneTab[]` 모양 · KOS 안 부름 | `board_rules.py:703-733` · `routers/api/board.py` `GET /board/search` | infra `test_고객_검색은_시술_완료_탭_고객만_찾는_말대로`(판 고객 「고객」 → [] · 지난 방문 · 다른 병원 없음 · `"yui tanaka"` · `"나카 유"` · `"가원장"` · `"vip"` · `"CH-777"` → [] · `""`/`"   "` → tab · 결과 == doneTab 항목) · rules 2개 |
| A4 ⑧ ⑨ ⑩ | 5상황 since · 풀리는 때 · `limitMin`(home 0) · 상황 1개 = 1장 · 호출 하나 = 1장 · 걸린 시각 이른 순 · 귀가 대기 방문 없음 · 기준 분 env · canRecall 호출 줄만 · 호출 줄 재호출 5분 전에도 · 「귀가 대기 전」 카드의 [귀가 대기] | `board_rules.py:354-445` · `common/config.py` `BOARD_{WAIT,ANES,CALL,ACCEPT}_MIN`(5 · 20 · 5 · 5) · `queries/board.py` `BoardLimits` · 스냅샷 `limits{waitMin, anesMin, callMin, acceptMin}` · `needs[]{why, since, limitMin, callId, doctorName}` — 스펙 스냅샷 모양과 칸 이름 · 뜻 일치 | rules `test_확인_필요_*` 7개 · `test_한_고객_여러_상황은_카드_여럿_걸린_시각_이른_순` · `test_기준_분_설정을_바꾸면_따라_바뀐다` · `test_재호출은_호출_줄에만_5분_전에도` · API `test_호출_줄_재호출은_5분_전에도` · `test_귀가_대기_전_확인_필요_카드의_귀가_대기` |
| A5 ⑪ ⑫ | 마취 새 회차 · `lastSeconds` · 마취 중 [귀가 대기] = 열린 마취 닫음(`ended_by` = 누른 직원 · 같은 transaction) · event_log `visit.home` 1행 payload 닫은 회차 · KOS op 없음 | `services/board.py:774-791` · `board_rules.py` `lastSeconds` | `test_마취_끝난_뒤_다시_시작하면_새_회차_마지막_회차_lastSeconds` · `test_마취_중_귀가_대기는_열린_마취를_닫는다` · rules `test_마취는_회차마다_쌓고_화면은_마지막_회차` |
| A6 ⑬ (값) | {원장} = 담당 원장(수락 · 진행 · 완료) | `board_rules.py` `task_doctor` | rules `test_원장_글자는_수락_진행_완료_줄의_담당_원장` (글자 자체는 템플릿 몫) |
| A7 ⑭ | 수락 · 진행중만(그 밖 409 `task_not_assignable`) · 원장 목록 밖 409 `doctor_not_listed` · 같은 원장 = 변화 없음(event 0) · 상태 · `started_at` · `accepted_at` 그대로 · 담당 원장 · 원장 상태 = 새 원장 · outbox `change-tasks-doctors` 1건 `doctorIds=[새 원장]` · 토큰 = 누른 사람 · 확인 `doctors_equal`(덮어쓰기) · event_log `task.doctor_change` 1행(from · to · actor = 누른 직원) · 수락 뒤 미시작 카드 닫힘 · 그때부터 다시 셈 · 권한 `board` edit(OQ-30) | `services/board.py:818-895` · `board_rules.py:254-258` `doctor_change_block` · `kos/writes.py:127-136` · `outbox.py:564` · `sync.py:1178` guard | API 5개(`test_원장_바꾸기_*` · `test_원장을_바꾸면_수락_뒤_미시작_카드가_닫히고_다시_센다` · 권한 403) · rules `test_원장을_바꾸면_수락_뒤_미시작은_닫히고_다시_센다`(바꾼 뒤 1분 = 없음 · 5분 = since 가 바꾼 시각 · doctorName 새 원장) · 계약 3개(본문 · `doctors_equal` 은 덧붙이기면 안 맞음 · guard `doctors`) |
| A8 ⑮ | 이미 수락된 호출에 뒤 수락 409 `call_already_accepted` · 먼저 저장된 것만 · 방문 advisory lock 아래 검사 | `board_rules.py:238-252` · `services/board.py` `_world` → `_lock_visit` | API `test_동시_수락은_뒤_쪽이_call_already_accepted`(`asyncio.gather` 두 요청 · 200/409 · 수락 행 의사 = 이긴 쪽만) · rules `test_동시_수락은_먼저_저장된_것이_남는다` |
| A9 ⑯ (API 회귀) | 되돌리기 동작 · KOS 쓰기 그대로 | 변경 없음 | 기존 `test_409_마취_호출_수락_시작_종료_되돌리기` 등 통과 |

## outbox (브리프 3)

- 원장 바꾸기 op = `change-tasks-doctors {scheduleId, sequences:[그 시술], doctorIds:[새 원장 1명]}` 1건 · expect `{"tasks": {"<seq>": {"doctors_equal": [새 원장]}}}` — KOS 쓰기 표 · OQ-31(덮어쓰기)와 같다.
- 앞 수락 op 재전송: 수락(`doctors_contain` + `status`)과 원장 바꾸기(`doctors_equal`)가 같은 `("task", seq, "doctors")` 를 만지므로, 원장 바꾸기가 sent/confirmed 가 되면 앞 수락 op 은 superseded → confirmed. 앞 수락을 다시 보내 KOS 를 앞 원장으로 되돌리는 일은 없다(`test_수락_뒤_원장을_바꾸면_앞_수락_쓰기는_확인으로_본다`).
- 순서: 같은 방문 op 은 `seq` 순으로 나가므로 아직 안 나간 수락 op 이 있어도 수락(앞 원장) → 바꾸기(새 원장) 순으로 나가 끝값 = 새 원장. 원장을 A→B→A 로 두 번 바꾸면 앞 바꾸기가 뒤 바꾸기에 superseded.
- 중복 쓰기: 같은 원장이면 `rollback` 후 `{ok: true}` · op · event 0(`services/board.py` · 테스트로 event 0 단언). 조회 덮어쓰기: op 확인 전엔 `guard_of` 가 `doctors` 칸을 막는다(`sync.py:1178` · 계약 테스트).
- `VisitTaskStaff` upsert `on_conflict(task_id, staff_id, role)` = 복합 PK 라 바꿨다 되돌리는(soft-delete 행 되살리기) 경로도 안전.

## 워커 미결

- ① → W1. ② → W2.
- ③ ~ ⑤: 이 리뷰 브리프에 내용이 없어(보고 요약에 번호만) 따로 대조하지 못했다. 이 리포트의 W3 · W4 · 「조용히 통과하는 자리」가 해당하면 그쪽으로 본다 — 코디가 원문을 주면 다시 본다.

## 조용히 통과하는 자리 · 계약 밖 변경 · 지어낸 문구 (브리프 4)

- 조용히 통과: 원장 바꾸기 외부 id 없음 → `Skipped`(event_log 에 남음 · 테스트만 없음 — W4). 동기화 연결 없는 병원 → op 없음(기존 규칙 그대로). 빈 단언 · 폴백 없음.
- 계약 밖: 스냅샷에서 `need` · `overSec` · `lastMinutes` 가 빠지고 `needs` · `limits.waitMin/acceptMin` · `canRecall` · `lastSeconds` 가 들어갔다 — 전부 스펙 스냅샷 모양(개정 ⑬)대로. 서버 렌더용 `inbox()["need"]` 항목 모양(`{**need, visitId, card}`)은 스펙 밖 내부 값(앱 JSON 아님) — fe 브리프에 적혀 있다.
- 라우트 경로 3개 · `task.doctor_change` · `task_not_assignable` · `call_already_accepted` = 스펙 「제안」 그대로. `doctor_not_listed` 는 매트릭스 `:554`.
- 지어낸 화면 문구 0 — 백엔드는 글자를 만들지 않는다(`call_already_accepted` 토스트 「다른 원장이 먼저 받았습니다」 MESSAGES 는 fe 몫 · `task_not_assignable` 글자는 OQ-33 미정이라 비움).

## 직원이 실물에서 만날 자리

- 원장을 바꾼 뒤 호출 탭 「수락함」 카드 · 수락 줄은 새 원장 이름만 보인다 — 처음 받은 원장은 화면 어디에도 없다(W1 · 의도라면 스펙에 적기).
- 한 호출에 시술 여러 개를 같이 수락한 뒤 하나만 원장을 바꾸면 「{원장} 수락 n분째」 카드가 통째 사라졌다가 다시 세고, 이름은 첫 시술 원장으로 보인다(W1).
- 원장 바꾸기는 dev(KOS 데모 지점)에서만 실물 확인(A7) — KOS 집도의가 새 원장 1명으로 바뀌고 다음 조회가 그 값을 주는지.
- 판 화면은 frontend 단계 전까지 열리지 않는다(템플릿이 `card.need` · `lastMinutes` 를 읽어 500) — 지금 브랜치를 dev 에 올리면 판이 깨진다. frontend 단계와 같은 PR 로만 나갈 것.

## 참고(기존 부채)

- `urgency()` 의 「수락됨 = 2.0」 고정값 · 정렬 규칙은 이번 변경 밖(그대로).
- `event_log` 인덱스 없음은 #236 이전부터(W2 가 처음으로 매 조회에 읽게 만들었을 뿐).
