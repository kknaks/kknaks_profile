# 리뷰 리포트 — fix-feedback / doc 검수 3 (2루프 스펙 spec-3 · spec-4) (2026-11-17)

- 검수 대상: 워크트리 `mediness-mediness/fix-feedback-spec` 의 미커밋 diff 5파일(개정 ㉒ · SPEC-005 2차 · SPEC-003 ⑰ 보충 · 20-spec.md · log.md)
- 기준: `e2e-feedback.md`(F-5 행 · E1 ~ E6), `_RESUME.md` §2 2026-11-17 행(:34-49, 특히 :46 알림 미룸 · :47 KOS 호출 취소 없음), `spec-3/4-instructions.md`, `review-doc-2-report.md` D1 ~ D4, `review-code-1-report.md` W3 · W5 · W6 · W8
- 코드 대조: `CENTURION_DAY/fix-feedback`(`4f8316a7` + 1루프 미커밋 diff). 읽기만 했다.
- 줄 번호는 지금 파일 기준이다. spec-002 = `products/day/20-spec/spec-002-procedure-board.md`, spec-005 = `products/day/20-spec/spec-005-notifications.md`

## 판정: FAIL (한 줄만 고치면 PASS)

결정 정본의 항목은 모두 같은 값으로 스펙에 들어갔다(F-5/E4 · E3 · E5 · E6 · E2 없음 · 알림 미룸 · KOS 호출 취소 없음). 화면 글자도 넘치지 않았다. D1 · D2 · D3 · D4 · W5 · W6 · W8 도 반영됐다. 호출 취소 저장 방법은 코드 사실과 맞고 be · fe 가 지을 수 있다. lint 는 ERROR 0 이다.

그런데 **호출 취소 알림의 migration 문장이 SPEC-005 계약 본문에 취소선 없이 하나 남아 있다**(F1). 지시서 기준(「호출 취소 알림 · 새 알림 종류 · migration 이 계약에 남아 있으면 FAIL」)으로는 FAIL 이다. 그 한 문장만 지우거나 취소선을 치면 PASS 다.

## FAIL

| # | 자리 | 지적 | 근거 | 고칠 방향 |
|---|---|---|---|---|
| F1 | `spec-005-notifications.md:444` §5 「모델 대조」 `chat` 종류 줄 | 「**호출 취소 알림(2026-11-17 2차 개정)은 새 알림 행 종류라 이 enum 에 값 추가 = migration 1개**(앱 푸시까지 보내면 `push_kind` 도 · §5 OQ-N14) — 칸 · 표는 그대로(`doctor_call_id` · `visit_id` 재사용)」가 취소선 없이 살아 있다. spec-4 가 다른 곳(:32 · :75 · :159 · :263 · :433, spec-002 :1008)은 다 「다음 스펙 · migration 없음」으로 고쳤는데 이 줄만 빠졌다. 그래서 같은 SPEC 안에서 :75 「migration — 다음 스펙」과 :444 「migration 1개」가 서로 어긋난다. be 가 「모델 대조」를 보면 migration 을 만들 수 있다 | `_RESUME.md:46`(알림 미룸 · migration 피함) · spec-4-instructions 1 · spec-4-report 「고친 곳」에 :444 가 없음 | 그 문장을 `~~…~~` 로 막고 「→ 이번엔 호출 취소 알림을 쓰지 않으므로 새 알림 종류 · migration 없음(다음 스펙 — 사용자 2026-11-17 · OQ-N14)」로 바꾼다. spec-002 :1008 과 같은 꼴로 쓰면 된다 |

## WARN (착수는 막지 않는다)

| # | 자리 | 지적 | 고칠 방향 |
|---|---|---|---|
| W1 | `spec-005:34` 2026-11-17(1차) 개정 머리 노트 끝 「보충」 | 「기본값 … `document.hidden` 일 때만 …」이 취소선 없이 남아 있다. 바로 위 :32 2차 노트와 U-5 :157 · S-6 :197 · 매트릭스 · OQ-N9 :428 은 「늘 띄운다」로 고쳤다. 머리 노트는 기록 성격이라 FAIL 로 보지 않았다. 다만 이 줄만 읽으면 뒤집힌 기본값을 믿게 된다 | 그 구절을 `~~`document.hidden` 일 때만~~ → 늘(2차 개정 E5)` 으로 고친다 |
| W2 | `spec-003-mobile-app.md:70` 개정 ⑰ ② | 「그 글자를 그대로 둘지는 DAY-SPEC-002 OQ-62」가 남아 있다. 같은 줄 ⑦ 에는 「OQ-62 닫음 — 웹만 · 앱 「담당의 미정」 그대로」가 있어 뜻은 닫혔다 | ② 의 그 구절에 취소선을 치고 「→ ⑦」을 붙인다(사소) |
| W3 | `log.md:18`(spec-3 행) | 「호출 취소 알림 · 새 종류 = `notification_kind` enum migration」 · 「KOS 명령 미확인 HAR 대기」가 적혀 있다. 바로 위 :17(spec-4 행)이 그것을 뒤집는다. log 는 누적 기록이라 고칠 의무는 없다 | 그대로 둬도 된다. PR 본문에 「:17 이 :18 의 알림 · migration · HAR 부분을 뒤집음」이라고 한 줄 적는다 |
| W4 | spec-002 규칙 38 :953 · spec-005 OQ-N14 ⓕ :433 | 호출 취소 뒤에도 원래 「원장 호출」 알림 행 · 앱 푸시가 그대로 남는다(닫을지는 다음 스펙 ⓕ). 원장이 그 앱 푸시나 알림으로 [수락]을 누를 수 있다. 그러면 남은 줄이 없을 때는 기존 `call_closed`, 남은 줄이 있을 때는 남은 줄만 수락된다. 코드상 수락은 `deleted_at IS NULL` 줄만 본다(`queries/board.py:230`). 스펙에 이 결과가 적혀 있지 않다. 지금 동작에서 자연히 나오는 결과라 새로 지을 것은 없다 | 규칙 38 끝에 「원래 원장 호출 알림 행 · 푸시는 그대로 — 그걸로 수락하면 기존 규칙(`call_closed` · 남은 줄만)」 한 줄을 넣는다(선택) |
| W5 | spec-002 :742 · :782 `task_not_called` 토스트 「비워 둠」 | 코드상 모르는 코드는 `message_of` 가 「요청이 올바르지 않습니다」로 떨어진다(`routers/board.py:167-174`). 그래서 실제 화면 글자는 그 글자가 된다. W3(`conflict`)와 같은 꼴이고, 글자를 지어 넣지 않은 것은 맞다 | 지금대로 둔다. be 브리프에 「`MESSAGES` 에 넣지 않음 → 일반 글자로 떨어짐」 한 줄 |

## 1. 결정 정본 대조 (빠짐 없음 · 같은 값)

| 결정 | 정본 | 스펙 자리 | 판정 |
|---|---|---|---|
| F-5 = E4: 준비중 ⋮ 없음 · 호출 → 「호출 취소」(준비중으로) · 진행중 → 시작 취소 · 완료 → 완료 취소 | e2e F-5 행 · E4 · `_RESUME:44` | spec-002 :171(E50) · :224 · :226 · :275 · :437(S-6 4) · :541 · :547 · :578 · :595 · :740-743 · :756 · :927(규칙 20) · :953(규칙 38) · :999 | OK |
| 호출 취소 **알림은 미룸** · 앱 푸시도 미룸 | `_RESUME:46` | spec-002 :42 · :226 · :275 · :437 · :740 · :953 · :1008(모두 취소선 + 다음 스펙) · spec-005 :32 · :75 · :159 · :263 · :433 · spec-003 :70 ⑥ · 20-spec.md :35 | **:444 한 곳 빠짐 → F1** |
| KOS 호출 취소 없음 → DAY 만 · KOS 데스크 「호출」 남는 것 감수 · OQ-68 닫음 | `_RESUME:47` | spec-002 :847(KOS 쓰기 표) · :953 · :437 · :1032(OQ-68 닫음) | OK |
| E5 웹 OS 알림 늘 띄움(OQ-N9 뒤집음) | `_RESUME:43` · E5 | spec-005 :32 · :157(U-5) · :197(S-6) · 매트릭스 「웹 — DAY 탭 열림」 행 · :428(OQ-N9 닫음) | OK (:34 의 옛 문구는 W1) |
| E6 차트 = 시술 이름 글자만 + 호버 「차트 작성」 | `_RESUME:45` · E6 | spec-002 :175 · :229 · :346-347 · :371 · :930(규칙 23) · :990 · :1001 | OK |
| E3 바로 시작 줄 「간호관리 · 진행 mm:ss」 · 완료 「간호관리 · n분」 · 원장 바꾸기 같게 | E3 | spec-002 :225 · :228 · :660(`systemDoctor`) · :943 · :1000 · :1038(OQ-62 닫음) | OK |
| E2 팝오버 잘림 = 스펙 변경 없음(버그) | E2 | 개정 ㉒ 노트 ④(:42) | OK |
| E1 고칠 것 없음 | E1 | spec-005 :32 · spec-002 ㉒ ④ | OK |
| 수락 줄 ⋮ 없음(기본값 꼬리표) | spec-3 지시 「정할 것」 | spec-002 :226 · OQ-67 ⓐ :1031 | OK |

## 2. 넘침 (화면 글자)

diff 에 새로 들어간 「…」를 HEAD 와 비교했다. 새 화면 글자는 허용 추가분 세 개뿐이다: 「호출 취소」 · 「간호관리」(「간호관리 · 진행 mm:ss」 · 「간호관리 · n분」) · 「차트 작성」. 나머지는 1루프 사용자 말(「바로 시작 · N건」 · 「시술순」 · 「방별순」)이거나, 사용자 말을 따온 것이거나, 절 이름이거나, 기존 글자(「다른 원장이 먼저 받았습니다」 · 「요청이 올바르지 않습니다」)다. 확인 창 · 성공 토스트 · `task_not_called` 글자는 비워 뒀다(:782 · OQ-67 ⓓ ⓕ). **넘침 없음.**

## 3. 검수 잔여 반영

| 잔여 | 자리 | 판정 |
|---|---|---|
| D1 귀가 대기 취소 웹 응답 = 판 전체 다시 받기 | spec-002 :594(본문 없음 · `HX-Trigger: day:board-refresh` · `X-Day-Version` 없음) · :887. 코드 `routers/board.py:741-765` 와 같음 | OK |
| D1 · D2 · W8 `sort` 는 GET 쿼리로만 · `hx-get` 에 박음 · 「판 전체를 다시 그리는 응답만」 | spec-002 :592(옛 문장 취소선) | OK |
| D3 log PR 칸 | `log.md:17-19` 모두 5칸 | OK |
| D4 `room.order` → `sort_order` | spec-002 :351 · :670 · 규칙 33 :939 — 살아 있는 `room.order` 없음(:52 개정 ⑱ 노트는 기록) | OK |
| W5 직전 단계가 판 단계가 아니면 `procedure` | OQ-58 ⓐ :1022(ⓐ 닫음) | OK |
| W6 연결 없는 병원 = DAY 만 | 규칙 34 :946 | OK |
| W3 `conflict` 토스트 글자 | OQ-66 ⓓ(열림) | OK(지시대로 열어 둠) |
| **새 모순** | spec-005 :75 ↔ :444(F1) · :34 ↔ :157(W1) · spec-003 :70 ② ↔ ⑦(W2) | F1 만 FAIL |

## 4. 호출 취소 — 코드 사실 대조 · 지을 수 있는가

| 스펙 주장 | 코드 사실 | 맞나 |
|---|---|---|
| 유효 호출 = 그 줄이 든 가장 최근 호출 · 그 호출이 닫혔으면 없음 → 준비중(규칙 38 · :547) | `services/board_rules.py:62-69`(`latest` → `closed_at is None` 만 `_effective`) · `task_state` :118-126(호출 없으면 `ready_wait`) | 맞음 |
| 저장 = 그 줄이 든 **열린 호출 전부**의 `doctor_call_task.deleted_at` + 받을 시술 없는 호출 `closed_at` · migration 없음 | `doctor_call_task` PK = (call_id, task_id)이고 `Timestamps` 에 `deleted_at` 이 있다(`models/task.py:143-147`). 그 테이블을 읽는 곳은 모두 `deleted_at IS NULL` 로 거른다: 판 조회 `queries/board.py:229-230`, 알림 본문 시술 수 `services/notifications.py:363-364`. 쓰는 곳은 새 호출 행뿐이다(`services/board.py:629 · 685` — 재호출도 새 call id 라 PK 충돌 없음). `closed_at` 칸도 있고 재호출에서 이미 쓴다(`services/board.py:595-596`) | 맞음. 열린 호출만 지워도 남는 「가장 최근」 호출은 닫힌 호출이라 유효 호출이 없다 → 「앞 호출로 되살아나지 않음」이 성립한다 |
| 수락됨 → `call_already_accepted`(기존 코드 · 기존 글자) | `routers/board.py:122` · `board_rules.py:264-272` | 맞음 |
| `task_not_called`(새 코드 · 글자 비움) | 없음(새로 만듦) · `message_of` 는 일반 글자로 떨어진다 | 맞음(W5) |
| KOS 쓰기 없음 · 다음 동기화가 되돌리지 않음 | `DoctorCall(` 을 만드는 곳은 `services/board.py` 뿐(동기화 아님) · 줄 상태는 KOS WAITING 을 보지 않음(`task_state`) | 맞음 |
| 지금 호출 취소 라우트 · 서비스 없음 | `routers/board.py` · `services/board.py` 에 cancel 관련 없음(grep 0) · `doctor_call_cancel` 흔적도 없음(be 가 알림을 미리 지은 것 없음) | 맞음 |

**착수 막는 것 표**

| 항목 | 누구 | 막나 | 메모 |
|---|---|---|---|
| F1 SPEC-005 :444 migration 문장 | be | **예(문서 정합)** — 그 줄을 보고 `notification_kind` migration 을 만들면 결정(`_RESUME:46`)과 어긋난다 | 한 줄 고치거나 be 브리프에 「알림 · migration 없음」을 명시 |
| 경로 `POST /board/tasks/{task_id}/cancel-call` · 본문 없음 · `board` edit · 응답 = 카드 조각 + 인박스 OOB + `version` · 검사 순서 401→403→404→409 `visit_home`→`call_already_accepted`→`task_not_called` | be · fe | 아니오 | 「제안」 꼬리표지만 닫혀 있다(:578 · :595 · :756) |
| ⋮ 노출(호출 줄만 「호출 취소」 · 준비중 · 수락 줄 없음 · `board` edit) | fe | 아니오 | :226 |
| 「간호관리」 · `tasks[].systemDoctor` · 원장 바꾸기 열기(`board_parts.html` `t.doctor` 조건) | be · fe | 아니오 | :225 · :228 · :660 |
| 차트 여는 곳 = 이름 글자 + 호버 「차트 작성」 | fe | 아니오 | :229 |
| 웹 OS 알림 늘(조건에서 `document.hidden` 뺌) | fe | 아니오 | spec-005 :157 |
| OQ-67 ⓐ~ⓕ 기본값 | be · fe | 아니오 | 모두 기본값 있음 :1031 |

## 5. lint

`python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error** · 263 warning. `products/day/` 는 ERROR 0 · WARN 0 이다(경고는 모두 selly 등 다른 제품에 원래 있던 것).

## 6. 정리

- 고칠 것: **F1 한 줄**(spec-005:444). 고치면 PASS(WARN W1 · W2 사소).
- 리뷰어는 파일을 고치지 않았다. 이 리포트만 썼다.
