# [backend] D40 승격 요청자 = 시스템(회의) · D38 안건 출처 다섯

너는 **sc-ax backend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = e297e1e). `backend/` 만. 커밋 금지. work 모듈은 최소 변경 + 기존 work 계약 회귀 0.

## D40 (사용자 09-11) — 승격으로 생기는 업무 요청은 **시스템(회의)이 보낸다**
- `promote` 가 만드는 `work_requests` 의 `requester_id` = 시스템 행위자(예: `system:meeting`, 상수 한 곳). 원장에 **`promoted_by_member_id`**(새 nullable 열, reset_demo/sync) = 누른 사람. 누른 사람은 `cc_member_ids` 에도 넣는다(읽기 가시성).
- 게이트: 요청자 전용 조작(수정·거두기·증빙 등 `request.requester_id != principal` 검사 자리)은 **`promoted_by_member_id` 도 요청자와 같게** 본다(헬퍼 하나로 모아 기존 호출자는 그대로). 수락·거절은 담당자 그대로.
- **담당 후보 제한 없음**: 시스템이 보내므로 `is_work_request_assignee` 조직 경계 검사를 회의 승격 경로에서 걷는다(`eligible_member_ids` 참석자 예외는 필요 없어짐 — 걷되 work 기본 경로는 불변). 자기 자신 배정 허용 유지.
- 응답·업무 상세 투영: 요청자 표시용으로 `requester_kind:"system"` + `source_meeting_title`(회의명|title_candidate) 를 요청 상세 응답에 싣는다(FE 는 나중에 「회의 · {회의명}」으로 그림). 진행 기록 첫 줄 「회의 {회의명}에서 {누른 사람}이 업무 요청을 만들었다」(actor = 누른 사람).
- 테스트: 요청자 = 시스템 · promoted_by·cc 저장 · 누른 사람이 수정/거둘 수 있음 · 교차 조직 담당 201 · 담당자 수락 시 task 출처 복사 그대로 · 기존 work 계약 5파일 회귀 0.

## D38 (재정정) — 안건 출처 다섯
- `source` 허용값 `manual|set|carried|derived|ai` (AI 정리는 다섯 번째 **종류**). set·derived 는 값만(만드는 경로 없음). 그 밖 422. 합성 보존 규칙 `source != ai` 그대로.

## 검증
```
cd backend && uv run pytest -q tests/contract/test_meeting_finalize.py tests/contract/test_meeting_core.py <work 계약 5파일> tests/architecture -m 'not integration'. 검증 1회
```

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: D40 시스템 요청자·D38 출처 다섯" \
  --body "변경 파일 / 스키마 / 검증 수치(+work 회귀) / FE 인계 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — D40·D38. 상세는 인박스." --enter
```
