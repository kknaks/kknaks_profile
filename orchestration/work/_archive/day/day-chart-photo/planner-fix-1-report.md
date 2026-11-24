# planner-fix-1 결과 보고 — 검수 review-doc-1 반영 + 결정 C17

## 상태: done

워크트리 `mediness-mediness/day-chart-photo-spec` · 미커밋(앞 판 위에 이어서). 바꾼 파일 = `products/day/20-spec/spec-002-procedure-board.md` · `10-decision.md` · `log.md`. 커밋 · push 없음.

## 1. 결정 C17 (OQ-83 ⓐ 닫음)

| 자리 (spec-002 줄) | 바꾼 것 |
|---|---|
| :45 개정 ㉘ 머리글 | 「같은 날 보충」 ⑩ C17 · ⑪ W1 ~ W9 요약 |
| :405 U-14 「다른 사람이 먼저 저장했으면」 | 「걸린 줄만 빼고 저장」 기본값 ~~취소선~~ + 「→ C17 · 사용자 2026-11-24」 |
| :406 U-14 새 줄 「저장 충돌 — 저장 전에 KOS 확인」 | KOS 지금 값 vs 연 때 값 · 하나라도 다르면 탭 전체 안 함 · 걸린 줄 = KOS 글 + 줄바꿈 + 내 글 · 담당자 KOS 값 · 안 걸린 줄 그대로 · 토스트(글자 OQ-90) · 다시 [저장] = 같은 확인 · C17-기본값 |
| :632 API 차트 탭 저장 행 | 요청 `rows[]` 에 `baseBody` · `baseDoctorStaffId`(이름 제안) |
| :648 차트 JSON | `tasks[].{chart}.base = {body, doctorStaffId}`(열 때 DAY 사본) |
| :653 「차트 탭 저장 응답」 | 앞 판 응답 문단 취소선 → 새 모양 `{status, saved, conflicts[{taskId, body(이어 붙인 글), staffId, base, baseLogId}], lastSavedAt}` · 충돌 = 409 · 저장 0 |
| :778 · :784 · :785 · :788 매트릭스 | 충돌 행 고침 · KOS 읽기 실패 행(200 · DAY 사본만) · `chart_too_long`(400 · 한도 OQ) 행 · 검사 순서 한 줄 |
| :858 토스트 표 | `chart_conflict` 기획 글자 취소선(뜻이 안 맞음) → 비움(OQ-90) · `chart_too_long` 비움 |
| :1154 규칙 31 머리 | 앞 판 검사 순서 취소선 → 새 순서 · **KOS 지금 값 읽기** · **KOS 판정 안 하는 줄** · **연 때 값을 무엇으로 비교하나** |
| :1257 · :1264 §4 표 | C17 행 더함 · 「충돌(연 때 값)」 행 바꿈 |
| :1306 OQ-83 | ⓐ 닫음(C17) · ⓒ = 섞이면 충돌 먼저(W7) |

- **연 때 값 = 열 때 응답의 `base`(DAY 사본 = DAY 가 아는 KOS 값)를 요청이 되돌려 보낸다.** `baseLogId` 만으로는 모자란 이유 셋: ① 「원장 변경」(규칙 27)은 차트 이력 없이 집도의를 바꾼다 ② KOS 웹 수정이 10초 조회로 사본에 오기 전이면 `baseLogId` 가 그대로다 ③ 걸린 뒤 다시 저장할 때 기준이 「방금 본 KOS 값」이어야 같은 줄이 계속 걸리지 않는다(걸린 응답이 `base` · `baseLogId` 를 새로 준다). `baseLogId` 검사(DAY 쪽)는 그대로 둔다.
- **KOS 읽기 API(코드 사실)** = 내부 `schedule/v1/queries/get-schedule-detail {scheduleId}` — `KosAdapter.fetch_visit_tasks`(`emr/kos/__init__.py:222` · **시스템 계정 토큰 · 읽기**) · mapper `assigneeMemo` → `assignee_note` · `doctorMemo` → `doctor_note` · `doctors[]` → `doctor_external_ids`(`emr/kos/mapper.py:479-480 · :488`). 요청당 1회 · **transaction 밖에서 먼저** 읽는다.
- **확인 대상 아님**: 시술 전 의사차트(결정 (가) — KOS 에 안 씀 · KOS 웹 수정은 규칙 32 ④ 가 [수락] 때 맡음) · 반영 대기 쓰기가 있는 줄(DAY 사본이 더 새것 — 기본값 · OQ-91 ⓐ).
- C17-기본값: KOS 읽기 실패 = DAY 사본(`baseLogId`)만으로 검사 · 저장 진행 · 표시 없음 / 길이 초과 = 400 `chart_too_long`(제안). **한도 값은 SPEC · 코드 어디에도 없어 OQ-90 ⓒ** 로 둠.

## 2. WARN 반영

| WARN | 자리 | 반영 |
|---|---|---|
| W1 | 규칙 31 :1154 · DB :1276 | 저장 event 요청당 1행 `visit.chart_save` · outbox intent 전부 그 event 에 묶음(`_queue`) · 규칙 27 `task.doctor_change` 줄마다 그대로 |
| W2 | 매트릭스 :796 · 다음 줄 · 연결 없음 행 | 토큰 없음 · KOS 401 = 401 `session_expired`(코드 공지 저장 `_staff_token` · `end_session_on_kos_401` 과 같게 · 기본값) · 그 밖 503 `kos_unavailable` · SPEC-006 어긋남 = 「무관(기존)」 한 줄 |
| W3 | 규칙 39 ① :1172 · API :636 · KOS 사진 표 :1081 · :1082 · :1087 · OQ-87 :1310 | 썸네일 = 목록 조각을 그릴 때 서명 1회 → 서버 GET → `data:` 로 실음(캐시 없음) · `…/thumb` 경로 취소선 · 원본 = 목록 → 서명 → GET · 삭제 = 1 목록 → 2 삭제 → 3 목록 |
| W4 | 규칙 39 ⑤ :1172 · 규칙 21 :1145 | 짧은 읽기 끝냄 → KOS 호출(transaction 없음) → `event_log` 1행 따로 커밋 |
| W5 | :71 개정 ⑯ 머리글 | 자동 저장 괄호 취소선 + 「→ 개정 ㉘ · 2026-11-24 명시적 저장」 |
| W6 | :648 | 옛 「차트 저장 성공 본문」 취소선 + 「→ 개정 ㉘ 『차트 탭 저장 응답』」 |
| W7 | :788 · 규칙 31 · U-14 :394 | 400 → 404(바로 시작과 같게) · 섞이면 충돌 먼저(409 `chart_conflict` 하나 · 담당자 검사는 다시 저장 때) |
| W8 | API :632 | JSON 짝 「없음 — 웹만」 · 옛 `POST /api/tasks/{task_id}/chart`(`routers/api/board.py:267`) = 지우는 대상 |
| W9 | :648 | 열 때 「최근 저장」 = 그 차트 종류 `tasks[].{chart}.savedAt` 최댓값(새 칸 없음) |
| 실물 자리 — 사진 읽기 토큰 | OQ-92 :1315 | 직원 토큰 그대로(기본값 · DAY 세션 만료 = KOS 토큰 만료 · DAY-SPEC-001 S-4) |

## 3. OQ

- 닫음: **OQ-83 ⓐ**(C17).
- 새로: **OQ-90**(충돌 토스트 글자 · 걸린 칸 표시 · 글자 한도 값 · `chart_too_long` 글자 · KOS 확인 실패 표시) · **OQ-91**(반영 대기 줄 건너뜀 · KOS 글이 빌 때 이어 붙이기 · 간호관리 담당자(KOS 칸 없음) · DAY 쪽만 걸린 줄의 「지금 글」 · KOS 집도의가 원장 목록 밖 · 원장 변경을 충돌로 셈) · **OQ-92**(사진 읽기 토큰).
- 고침: OQ-87 ⓒ(썸네일 서명 시점 · 캐시).

## 4. 그 밖

- `10-decision.md` 「현재 결론」 C17 한 줄(escalation 없음). `log.md` spec-change 1행.
- 새 migration 없음 — `base` 는 저장하지 않고 응답 · 요청으로만 오감(:1276).

## 검증

`python3 scripts/lint-pipeline.py --strict` → **0 error · 263 warning** · `products/day/` 0건(263건은 전부 타 제품 — 무관). 바꾼 표 열 수 점검 통과.

## 미결·주의점

- 차트 글 한도가 지금 정해진 곳이 없다 — C17-기본값 「길이 오류」는 한도 값이 정해져야 뜻이 생긴다(OQ-90 ⓒ).
- KOS 확인은 시스템 계정 읽기(코드 그대로)라 C10 류 「직원 토큰」 결정과 상관없다 — 사진 읽기만 직원 토큰(OQ-92).
- C17 로 기획 4-2 예외 1 토스트 글자를 쓰지 않게 됐다(뜻이 다름) — 글자 결정 필요(OQ-90 ⓐ).
