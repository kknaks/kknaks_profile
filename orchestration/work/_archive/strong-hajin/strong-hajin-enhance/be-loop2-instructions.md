# [backend] WORK-012 2루프 — E-6 AX 가 회의 생성 초안을 못 고친다

기존 구현 브리프 규칙 그대로(커밋 금지 · 포트 금지 · 관련 시험만). 코드 = 같은 브랜치(`cc5d46d` 위). **frontend 워커가 `frontend/` 에서 2루프 작업 중 — 건드리지 마라.** 근거 = `W/e2e-feedback-batch-1.md` E-6.

## 증상(운영 2026-10-07 17:43)
AX 회의 생성 카드(`meeting.reservation.create`, 초안 1회차) 뒤 사용자가 「서형석 전창원 추가해야 하는데」 → AX 가 `action_item_command`(command=`save_draft`, expected_version=1, base_submission_version, draft)를 **4번** 불렀고 전부 `failed`. `tool_invocations.error_summary` 는 「실패: failed」 뿐 — 사유가 가려져 있다.

## 할 일
1. **원인을 재현으로 찾는다** — 회의 생성 초안에 AX 도구 경로(MCP `action_item_command` → `platform/action_center.py` `execute`·`_save_draft` · `modules/actions/confirmation.py` `decide_ax_confirmation`)로 참석자를 더하는 `save_draft` 를 시험으로 재현. 업무(`task.create_self`)의 같은 경로와 어디서 갈라지는지(draft 필드 검증 · 첨부 `"task"` 고정 · base_snapshot 모양 · 회의 draft 병합 등) 파일:줄로
2. **고친다** — 회의 초안도 업무 초안처럼 AX 가 `save_draft` 로 회차+1(참석자·시간·회의실·안건·목적 등 회의 고유 필드 — OQ-901). 화면의 [수정]→BookingModal 편집 창 저장 경로(WP3)와 같은 결과여야 한다
3. **실패 사유가 가려지지 않게** — 도구 실패의 `error_summary` 에 사람이 읽을 사유(코드·한 줄)가 남게. AX 가 같은 실패를 그대로 네 번 되풀이하지 않도록 도구 응답 오류가 모델에 사유를 준다
4. 시험: 회의 초안 save_draft(참석자 추가 · 시간 변경) 성공 · 업무 초안 회귀 없음 · 오류 사유 노출
- 리포트 `W/be-loop2-report.md`(원인 · 고친 곳 · 시험) · 완료 보고 두 명령(subject 「backend 완료: 2루프 E-6」) · **코디handle = term_367ca23a-f846-44c0-afc7-07b6655df214**
