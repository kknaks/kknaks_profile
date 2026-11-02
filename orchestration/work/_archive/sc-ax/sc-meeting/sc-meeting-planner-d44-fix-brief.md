# [planner] SPEC-004 0.4.8 — D44 정정: 재전사 폴백 없음(실패 = 회의 「실패」) · 종료 뒤 원문 재조회 · 회의 중 칩 점프

너는 **sc-ax planner 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec`(HEAD 64601f7c). `products/sc-ax/20-spec/spec-004-meeting-note.md` · `10-decision.md` · `30-work/work-004-*.md` · `work-006-*.md` 만. 커밋 금지.

## 사용자 결정 (2026-09-11) — 실물 테스트 1회차에서
1. **D44 정정 — 재전사 폴백 없음.** 재전사가 실패하면(업로드·상태 error·결과 수신·빈 결과·상한·녹음 없음) 회의는 **실패** 상태로 가고 실패 사유는 D43 대로 사람 말, [다시 시도]는 재전사부터. 실시간 원문 위에서 합성하지 않는다. done 인 회의의 원문·합성 재료는 **언제나 재전사 결과**(`transcript_source` 는 항상 final). 0.4.7 에 적힌 「실패 시 실시간 원문 유지」 갈래·화면 안내 문구를 지운다.
2. **종료 뒤 화면은 원문을 다시 읽는다**(§5.2/§5.4 화면 규칙): 상태 전이(in_progress→summarizing→done|failed) 때 스크립트 탭 원문 재조회. 재전사로 원문이 통째로 바뀌기 때문.
3. **회의 중에도 시간 칩 → 스크립트 이동**: AI 요약 탭 줄의 근거 칩은 회의 중에도 누르면 스크립트 탭의 그 구간으로 간다(지금 스펙은 끝난 회의만).
4. 기록: 회의 중 AI 요약에는 「다음 할 일」이 없다(최종 합성만) — 변경 아님, 확인만. §7 에 이미 있으면 손대지 마라.

## 할 것
SPEC 0.4.8(변경 이력 한 줄) · 10-decision D44 행 정정(폴백 문구 삭제, 실패 규칙) · work-004(재전사 실패 = failed·재시도) · work-006(재조회·칩 점프 검증 항목). 다른 절 손대지 마라.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_e155b48b-1a1f-4392-99eb-2889228625e7 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "planner 완료: SPEC 0.4.8 D44 정정" \
  --body "변경 파일 / 정정 요약 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] planner 완료 — 0.4.8. 상세는 인박스." --enter
```
