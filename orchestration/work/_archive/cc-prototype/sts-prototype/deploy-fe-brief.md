# [frontend] 배포 — front 이미지(Dockerfile) · GitHub Actions arm64 → GHCR

너는 **cc-prototype `frontend` 워커**. 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype`. 근거 **DEC-003**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/10-decision/decision-003-cc-deploy.md`
(WP11 화면 작업은 시안 r5 뒤에 따로 온다 — 이번엔 배포 파일만)

## 할 것
1. `cc/front/Dockerfile` — Next.js standalone(`output: 'standalone'`), arm64, 비루트, 포트 3600. **API 주소 = 같은 출처**: `NEXT_PUBLIC_API_BASE_URL` 를 빌드 인자로(배포값 `https://ccc.medisolveai.xyz`) — 통역 WS 가 `wss://ccc.medisolveai.xyz/api/interpret` 로 가는지 확인(`http→ws` 변환이 https→wss 도 되는지)
2. **GitHub Actions** `.github/workflows/cc-front-image.yml`(레포 루트 — 이 파일만): `cc/front/**` 변경 · 수동 — arm64 빌드(빌드 인자 = 배포 주소) → `ghcr.io/kknaksss/cc-prototype-front:<sha>`(latest X)
3. `cc/front/README.md` 배포 문단

## 범위 · 검증
- `cc/front/` + `.github/workflows/cc-front-image.yml` 만. 커밋 · push 금지
- `npx tsc --noEmit` · `npm run lint` · `npm run build` 1회 · 로컬 `docker build` 1회 · 임시 포트로 띄워 200 확인 후 종료(3600 · 8600 금지)
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/deploy-fe-report.md`

## 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_b8c9cf80-7ebb-4df8-8d9c-db451c88c768 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] frontend: <질문>" --enter`
