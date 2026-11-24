# [spec] SPEC-010 고침 10 (너는 새 스펙 워커 — 앞 맥락 없음 · 스펙 문서 · 검수 리포트 · 결정 표 `_RESUME.md` §2 를 먼저 읽어라) — r7 FAIL(P1 1 · P2 4) → 0.2.7 (11-20)

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 재검수 `$W/review-spec-010-r7.md` 의 P1 1(TP14 본문에 ⑤ 예외 「규칙 continue · LLM return + 유효 to → return」 넣기 · T17 성립) · P2 4 전부를 검수 「고칠 방향」 대로 `$W/SPEC-010-consult-myeongdong.md` 에 반영해 0.2.7. 문서 1 개만 · 코드 수정 0 · 커밋 0 · 서브에이전트 0. 그리고 WP-2 코드 검수 P2(`$W/review-wp2.md`) 가운데 스펙 문구로 닫을 것(⑤ 드롭다운 가격 vs §6-1 PR1 한 줄)도 같이.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_3d139262-8d63-4045-acb8-cbe37d8d96cb --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: SPEC-010 0.2.7" --body "r7 반영"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] spec 고침 10 완료 — <한 줄>. 상세는 인박스." --enter
```
