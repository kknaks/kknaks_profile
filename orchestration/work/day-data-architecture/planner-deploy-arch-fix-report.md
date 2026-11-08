# planner-deploy-arch-fix 결과 보고 — done (미커밋)

`products/day/40-architecture/deployment.md` · `log.md` 한 줄 · lint `--strict` 0 error.

| W | 고친 곳 |
|---|---|
| W1 | 흐름 표 「시작」 prod = **fast-forward 로만** — dev 에서 배포 · 확인한 commit 그대로(`git push origin <sha>:prod` 또는 승격 워크플로) · merge · squash 금지(새 commit 이면 같은 이미지가 깨짐) · sequence 에 「fast-forward push」 |
| W2 | 흐름 표 「롤백」 = 수동 실행 워크플로(환경 · 이전 성공 SHA) → 그 이미지로 재배포 · 새 줄 「migration 되돌리기 = 안 함(forward-only) · 이전 이미지가 새 스키마에서 돌게 migration 을 쓴다」 |
| W3 | sequence · 표 prod 순서 = **① prod migration**(수동 워크플로 · 승인 · dev 에 같은 revision 확인 · upgrade head) → **② prod 배포**(head 확인만 · 다르면 중지) · 미결 「승인 수단」 = 세부(승인 문자열 등)만 남김 |
| W4 | 사용자 준비 목록에 GitHub 쪽 4줄 — Environments(dev · prod) · 브랜치별 OIDC federated credential · Actions 변수(비밀값은 Key Vault) · 브랜치 규칙(prod fast-forward · 누가 push · 강제 여부는 사용자) |
