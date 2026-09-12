# [planner] SPEC-004 0.4.10 — D47 배치 근거 검증 구간은 회의 전체 · D48 빠른 시작 자리표시 안건 제목은 AI 가 채움

너는 **sc-ax planner 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec`(HEAD a149b3ad = 0.4.9). `products/sc-ax/20-spec/spec-004-meeting-note.md` · `10-decision.md` · `30-work/work-001-*.md` · `work-003-*.md` 만. 커밋 금지.

## 사용자 결정 (2026-09-11, 실물 2회차)
- **D47**: 회의 중 배치는 매번 AI 트랙 전체를 새로 쓴다(지금대로). 근거(evidence) 검증 구간은 「이번 배치가 읽은 구간」이 아니라 **회의 시작부터 지금까지 적재된 확정 발화 전체**다. 지금 §7.1 검증 문구(「미처리 구간 밖이면 강등」)를 정정. 근거는 §10-8(실재 구간만) 유지.
- **D48**: 빠른 시작이 만드는 안건은 **자리표시**(title_placeholder)다. §7.3(사람 안건 제목 불변)의 예외 — AI 배치가 자리표시 안건의 제목을 채우고 매 배치 최신화한다. 사람이 제목을 직접 고치면 그 뒤 불변. 출처는 manual 유지. 화면 「안건 N. {제목}」.

## 할 것
§7.1 검증 행 정정 · §7.3 예외 한 줄 · §3(빠른 시작) 자리표시 · 10-decision D47·D48 · work-001(빠른 시작 안건) · work-003(검증 구간·자리표시 제목 갱신·검증 항목). SPEC 0.4.10 변경 이력 한 줄. 다른 절 손대지 마라.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_e155b48b-1a1f-4392-99eb-2889228625e7 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "planner 완료: SPEC 0.4.10 D47·D48" \
  --body "변경 파일 / 요약 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] planner 완료 — 0.4.10. 상세는 인박스." --enter
```
