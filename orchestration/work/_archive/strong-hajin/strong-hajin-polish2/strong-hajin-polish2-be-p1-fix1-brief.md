# [backend] WORK-009 Phase 1 — 검수 FAIL·WARN 재수정 (fix1)

앞 판 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/strong-hajin-polish2-be-p1-brief.md` (+add1) 의 규칙이 그대로다(subject 「backend 완료: WORK-009 Phase 1 fix1」). 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/review-be-p1-report.md` 를 전부 읽어라. ⚠ frontend 워커가 같은 워크트리 `frontend/` 에서 2a-1 fix1 중 — `backend/`(+inventory) 만.

## 코디 판단 — 전부 고친다
1. **F1** 화면에 닿는 스키마 title 「기한」·「기한 없애기」·「기한 삭제」 → **「마감일」·「마감일 없애기」·「마감일 삭제」**: `task_commands.py:52`·`:131`·`:133` · `request_commands.py:54-55` · `project_commands.py:56` · `task_creation.py:17`. **`Field(title=…)` 에 「기한」이 남은 곳을 전부 grep** 해서, `_command_edit_contract` 등으로 화면 라벨이 되는 모델이면 바꾼다(안 되는 것은 표에 이유). inventory 는 그 항목만 다시 패치
2. **W1 → (a)** 저장도 지금 붙인 자료 ID(`attachment_draft_ids`)를 함께 남긴다 — 저장 회차 스냅샷과 그 뒤 draft 없는 confirm(같은 자료 ID)의 스냅샷이 같아 **등록 때 회차가 오르지 않는다**. FE 2a-1 은 이미 저장·등록 둘 다 붙인 자료 ID 를 싣는다. 계약 테스트: 자료가 붙은 `task.create_self` 초안 저장 → 등록 → 회차 그대로 · 업무에 자료 연결. (SPEC 줄은 코디가 고친다)
3. **W2** 소유자가 아닌 persona 의 `save_draft` → 거부(지금 코드의 응답 그대로)이고 회차 그대로인 계약 테스트
4. **W3** `task_results.py:53` `TaskScheduleReleaseView` docstring 을 **네 자리**(+ 완료의 마감일 채움: 완료·완료 보고 제출)로. inventory 그 항목만
5. **W4** 마감일 채움 테스트에 **살아 있는 배정**을 두고 완료/완료 보고 → 배정 그대로 · `released_count == 0` · 훅이 실제로 돈 증거(`test_task_schedules.py` 시작일 채움 방식)
6. 직렬 패스 흔들림 1건 — 다시 나오면 테스트 이름을 보고에 적는다
