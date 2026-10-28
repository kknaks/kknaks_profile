# [backend] interpret-pwa WP8 — 이미지 빌드 워크플로(GitHub Actions · arm64 · main 만)

너는 interpret-pwa backend 워커다(역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/backend/role.md`). 워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc`.
⚠ frontend 워커가 `front/` 에서 WP6 작업 중 — `front/` 는 건드리지 마라. `.env` 열지 마라.

## 할 일 (DEC-001 D-26)

- `.github/workflows/` 에 back · front 이미지 빌드 → `ghcr.io/kknaksss/interpret-pwa-back:<sha>` · `ghcr.io/kknaksss/interpret-pwa-front:<sha>` (linux/arm64 · **main push 만** · 수동 실행 workflow_dispatch 도). `latest` 태그 금지
- **원형을 본뜬다**: `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:.github/workflows/procedure-back-image.yml` (+ 같은 폴더 front 용이 있으면 그것도) — runner · QEMU/buildx · GHCR 로그인(GITHUB_TOKEN · packages: write) 방식 그대로
- front 빌드 인자 `NEXT_PUBLIC_API_BASE_URL=https://tongky.medisolveai.xyz` (워크플로에 박는다 — 공개 값)
- back · front Dockerfile 이 arm64 로 빌드되는지 로컬 `docker buildx build --platform linux/arm64` 각 1회(푸시 없음 · front 는 빌드 인자 넣고). 오래 걸리면 back 만 하고 front 는 pending
- allowed_paths: `.github/workflows/**` 만 (Dockerfile 수정이 필요하면 고치지 말고 `[질문]`)
- 커밋 · push 금지 · 실제 Actions 실행은 main 머지 뒤

## 완료 보고

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/wp8-be-report.md`. 두 명령 모두:
```bash
orca orchestration send --to term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: WP8 이미지 워크플로 <한 줄>" --body "변경 파일 / 요약 / 검증 / 미결"
orca terminal send --terminal term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 --text "[worker_done] backend WP8 이미지 워크플로 완료 — <한 줄>. 상세는 인박스." --enter
```
