
# [backend] WP-130 검수 FAIL 정정 — 깨진 테스트 26건·첨부 바인딩 결함

너는 **mediness `backend` 워커**다. 검수 리포트의 BE 몫 FAIL 을 정정한다 — 좁은 라운드.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/backend/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-improve` (미커밋 위. **front/ 금지 — FE 워커 병렬**)

## SSOT
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/review-code130-report.md` — 위반 ①③·WARN 좌표 전부

## 해야 할 일
1. **위반 ① — 깨진 테스트 26건 갱신**: `back/tests/api/test_version_wbs_checkitem.py:318-320·511`·`back/tests/services/test_version_progress.py:218·262·296` — WBS status=done PATCH 가 이제 completionNote 없이 422 다. 두 파일을 새 계약(completionNote 제공 또는 422 단언)으로 갱신. «선행 실패» 재분류가 아니라 **테스트를 계약에 맞춘다**
2. **위반 ③ — 첨부 바인딩 오소비 차단**: `back/app/services/landing_chat/turns.py:170` 의 Redis 바인딩이 모든 발화에 심기고 소비자 검증이 없어 30분 내 다음 «생성» 발화가 남의 첨부를 붙인다. 정정: 바인딩에 **소유자(member_id)·방(room_id) 검증**을 걸고, **생성 발화 흐름에서만 소비 + 소비 즉시 삭제**(1회성). 수정 카드 첨부는 **v1 미지원으로 명확화** — 스키마 잔재(schemas/action_runtime.py:103-105)·on_reject 훅 중 죽은 자리를 제거하거나 «v2» 주석으로 봉인(반쪽 구현 잔재 금지)
3. **WARN 처리 2건**: 25MB 검사를 전량 수신 전 Content-Length 선검사 추가(스트리밍 한도) · 리포트 WARN 중 주석 오타류 정정
4. 재검증: 갱신 2파일 + 신규 테스트(바인딩 소유자·1회성) + wp130 테스트 1회 — 수치 보고

**하지 말 것**: 위 좌표 밖 수정 금지·422 술어 자체 변경 금지·front/ 금지.

## 완료 보고 — 문구 변경 금지
> ⚠ 핸들은 dispatch preamble 값을 믿어라.
```bash
orca orchestration send --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "backend fix 완료: <한 줄>" --body "정정 목록/테스트 수치"
orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[worker_done] backend(130 fix) — <한 줄>. 상세는 인박스." --enter
```
