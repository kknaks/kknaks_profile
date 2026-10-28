# [reviewer_doc] 시술 현황 문서 검수 r5 — SPEC-003 0.6.0 · WORK-008

너는 **cc-prototype `reviewer_doc` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/reviewer/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라. 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` — **read-only** · 리포트 1개.

## 기준
- 결정 정본 = `orchestration/work/overall-board/_RESUME.md` §2 **10-26 · 10-27 줄 중 시술 현황에 닿는 것**(2계층 · 부상태 색 · W2 · 2계층 기본값 · 한글 발음 · 웹 구현본 정본 · OQ-519 닫힘)
- 색 · 이름 원본 = `para/projects/summer-star/cc-prototype/20-spec/spec-005-reservation-board.md` 0.4.0 §5.1 · 구현 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/front/components/reservations/view.tsx`
- 화면 정본 = 배포된 웹 구현(`/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/` · branch `kknaksss/overall-board-2` · 읽기만) — 시안 대조로 FAIL 하지 마라

## 대상(planner 보고 `orchestration/work/overall-board/procedure-spec-r7-report.md`)
- `para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` 0.6.0(r7 줄) · `30-work/work-008-procedure-board-v2.md`(새) · `reference/2026-10-12-cc-prototype/workflow-v2.md` 시술 차트 초안 · README · log
- 바뀐 줄: `git -C /Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc diff 901267f..HEAD -- para reference` 가 비면 `git -C /Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc diff -- para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md para/projects/summer-star/cc-prototype/30-work/work-008-procedure-board-v2.md reference/2026-10-12-cc-prototype/workflow-v2.md`

## 볼 것(지적마다 `파일:줄` · 근거 · FAIL/WARN/PASS)
1. 결정 줄 → 절 반영 전수
2. **§5.14 2계층 대조표가 코드의 지금 표시를 전부 덮나**(grep 으로 상태 글자 · Badge · 범례 · 칩 · 점 전수) · ● 바꿈 / ○ 그대로 구분이 맞나 · 색이 SPEC-005 구현 값과 같나
3. W2(§5.12 · §6.3): 「판 안」 범위 · Esc · 귀가 대기 카드 위 · 필터 중 · 시작 순서면 저장 없음 — FE 가 SPEC 만 보고 짤 수 있나
4. 발음(§6.3): 자리 · 말줄임 · 빈 값 · 앱 영향(§10.1)
5. WORK-008: WP 대상 파일 · 완료 조건 · 검증 · E2E #27~#32 가 사용자 실물 자리인가 · 예약 현황 회귀
6. 차트 초안은 **계약 아님** — 결정을 지어냈는지만 본다(지어냈으면 FAIL)
7. public(실명 · KOS id · 키 · 토큰 0)

산출물: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/procedure-review-doc-r5.md`. FAIL 은 구현을 막는 것만 · 짧게 — **frontend 가 같은 SPEC 으로 병렬 구현 중**이다.

## 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 과 다르면 preamble 쪽으로만.

- 커밋·push·PR 금지.

```bash
orca orchestration send \
  --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_8a9b50a6-5f7d-4c90-8ce3-866e16b2d06f \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "보고서 경로 / 바뀐 파일 / 검증 수치 / FAIL·WARN 또는 미결"

orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[질문] reviewer_doc: <질문>" --enter`
