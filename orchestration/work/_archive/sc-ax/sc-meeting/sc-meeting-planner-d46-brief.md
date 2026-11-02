# [planner] SPEC-004 0.4.9 — D46 회의 중 AI 요약에 「다음 할 일」 후보(읽기 전용)

너는 **sc-ax planner 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec`(HEAD ef0d19a1 = 0.4.8). `products/sc-ax/20-spec/spec-004-meeting-note.md` · `10-decision.md` · `30-work/work-003-*.md` · `work-004-*.md` · `work-006-*.md` 만. 커밋 금지.

## 사용자 결정 (2026-09-11, D46)
회의 중 AI 중간 요약도 안건별 「다음 할 일」 후보를 낸다. **읽기 전용** — 회의 중에는 업무 생성·후보 빼기 없음. 승격은 종료 뒤 최종 합성 결과에서만(지금대로). 계약 상세: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/sc-meeting-live-todos-contract.md`.

## 할 것
- §4.2-6 표 「다음 할 일: 회의 중 없다」 → 「회의 중 후보(읽기 전용, provisional) · 최종에서 새로」. §7.1 출력에 `todos`. §8 최종 합성이 provisional 을 지우고 새로 뽑는다. §9 승격 게이트에 provisional 409.
- 10-decision D46 행. work-003(배치 todos·provisional 적재·push) · work-004(최종이 provisional 정리) · work-006(AI 탭 렌더 검증) 갱신. SPEC 0.4.9 변경 이력 한 줄. 다른 절 손대지 마라.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_e155b48b-1a1f-4392-99eb-2889228625e7 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "planner 완료: SPEC 0.4.9 D46" \
  --body "변경 파일 / 요약 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] planner 완료 — 0.4.9. 상세는 인박스." --enter
```
