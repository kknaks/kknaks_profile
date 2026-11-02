# [planner] SPEC-003 정정 r1 — 리뷰 S1~S12 · 처분 반영

너는 같은 cc-prototype `planner` 워커다(코디 워크트리). 리뷰 `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/review-wp1-5-report.md` 맨 끝 「SPEC 쪽을 고쳐야 하는 것」 S1~S12 를 **처분 `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/fix-decisions-r1.md`** 대로 SPEC-003 에 반영한다(버전 0.1.0 → 0.2.0 · 바뀐 절 표시). 사실 정정: 시스템 계정 id = `get-user-account` data.id(S1) · 같은 단계 flow-step 400(S2) · call 400 조건은 OQ(S11). allowed_paths = `para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` 만. public grep 0.

## 5-1. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "planner 완료: SPEC-003 정정 r1" \
  --body "변경 파일 / SPEC 절 요약 / WP 목록 / 열린 것 / DEC 대응표 누락 0 여부 / 검증"

orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] planner SPEC-003 · WORK-003 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] planner: <질문>" --enter`
