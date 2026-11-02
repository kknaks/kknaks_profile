# [planner] SPEC-003 0.6.0 · WORK-008 — review-doc r5 처분 반영(작게)

너는 **cc-prototype `planner` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/planner/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라. 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc`(코디와 공유).

## 원천
- 리뷰 `orchestration/work/overall-board/procedure-review-doc-r5.md`(FAIL 0 · WARN 5)
- 처분표 `orchestration/work/overall-board/procedure-review-doc-r5-dispositions.md` — **planner 몫 전부**(W1 · W2 · W3 · W4 · W5)
- 앞 판 보고 `orchestration/work/overall-board/procedure-spec-r7-report.md`(0.6.0 이 무엇을 바꿨나)

## 할 일
- `para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` 0.6.0 안에서 고친다(버전 그대로 · 줄 끝 `(r8)`) · `30-work/work-008-procedure-board-v2.md` Meta · WP-FE3 · WP-E2E · `log.md` 한 줄
- 보고서 `orchestration/work/overall-board/procedure-spec-r8-report.md`(처분 줄 → 고친 곳 대조표)

## 금지 · 검증
- allowed_paths = 위 세 파일 + 보고서. 코드 수정 금지 · 실명 · KOS id · 키 · 토큰 금지
- 검증: 처분 5줄 → 고친 곳 빠짐 0 · grep 0

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 커밋·push 금지.
```bash
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_c122938e-d139-4263-8c45-1ae7904ecff3 --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "planner 완료: <한 줄>" --body "보고서 경로 / 바뀐 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
