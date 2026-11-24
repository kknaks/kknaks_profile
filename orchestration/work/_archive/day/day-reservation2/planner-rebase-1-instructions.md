# [planner · 마감] 스펙 PR #961 을 main 최신 위로 rebase — 개정 번호 겹침 정리

같은 터미널 · 같은 맥락. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation2-spec`(브랜치 `kknaksss/day-reservation2-spec` · 커밋 3: `479d8f46` · `54bbeb14` · `6eba367a`). **이번엔 커밋 · force-push 허용(머지 금지)**.

- main 이 앞서 나감: **`69ef0dcb` #960 「차트 명시적 저장 · 시술전후사진 — DAY-SPEC-002 개정 ㉘」**. 우리도 SPEC-002 개정 ㉘ 을 썼다 → **번호가 겹친다**. 충돌 파일: `spec-000-data-model.md` · `spec-002-procedure-board.md` · `log.md`(그 밖 10-decision · 20-spec · 30-work 도 확인)
1. `git fetch origin main` → `git rebase origin/main`
2. 충돌은 **main(#960) 내용을 그대로 두고 우리 것을 그 뒤에**. 우리 SPEC-002 개정 = **㉙** 로 번호 변경(본문 · 개정 이력 · 다른 문서에서 「002 ㉘」 을 가리키는 곳 전부 grep 해서 ㉙ — SPEC-007 · 006 · 30-work · 10-decision · log · 20-spec). SPEC-000 도 main 이 같은 개정 번호를 썼으면 같은 방식으로 다음 번호. migration 번호를 적은 곳은 main(#960) 쪽 `0024_customer_memo` · `0025_visit_photo` · 우리 `0026` ~ `0028`(구현 머지 CENTURION_DAY #280 · dev `55e60aa4`) 과 맞는지
3. 30-work Spec Coverage SPEC-007 행: 「구현 = CENTURION_DAY #280(dev `55e60aa4`)」 채움
4. `python3 scripts/lint-pipeline.py --strict` products/day 0 error → 커밋 정리(rebase 결과 그대로 · 고친 것 있으면 커밋 하나 더) → `git push --force-with-lease`
5. 완료 보고 두 명령(subject 「planner 완료: rebase 1」 · 이번 dispatch 값) — 바꾼 번호 표 · 새 HEAD SHA · PR mergeable 상태(`gh pr view 961 --repo MediSolveAIDev/mediness --json mergeable`)
