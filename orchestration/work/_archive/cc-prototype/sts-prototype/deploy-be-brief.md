# [backend] 배포 — back 이미지(Dockerfile) · GitHub Actions arm64 → GHCR

너는 **cc-prototype `backend` 워커**. 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype`. 근거 **DEC-003**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/10-decision/decision-003-cc-deploy.md`

## 할 것
1. `cc/back/Dockerfile`(arm64 에서 빌드 · 실행 — python 3.12 slim + uv, 비루트, 포트 8600, `uvicorn app.main:app --host 0.0.0.0 --port 8600`). **`data/` 를 이미지에 넣지 마라**(`.dockerignore`) — 런타임에 마운트: `CC_DB_PATH`(PVC) · `CC_SCENARIO_DIR` · `CC_KOS_STAFF_PATH`(Secret 마운트) · `SONIOX_API_KEY`(Secret env)
2. 시작 때 DB 가 비어 있으면 시나리오로 `seed build` 를 한 번 하는 진입 스크립트(이미 있으면 건너뜀) — 경로는 env
3. **헬스 엔드포인트** `GET /api/health` → 200(없으면 추가)
4. **CORS**: 같은 출처 배포(`https://ccc.medisolveai.xyz`, `/api` 경로) — `CC_FRONT_ORIGIN` 로 그대로 열리는지 확인
5. **GitHub Actions** `.github/workflows/cc-back-image.yml`(레포 루트 — 이 파일만 루트 허용): `cc/back/**` 변경 시 · 수동 실행 — arm64(`ubuntu-24.04-arm` 러너 또는 buildx+qemu) 빌드 → `ghcr.io/kknaksss/cc-prototype-back:<sha>`(+ `main` 태그 X, latest X). 패키지 권한 `packages: write`
6. `cc/back/README.md` 에 배포 env 목록

## 범위 · 검증
- `cc/back/` + `.github/workflows/cc-back-image.yml` 만. 커밋 · push 금지(코디가 push 해서 Actions 를 돌린다)
- 로컬 `docker build` 가 되면 1회(arm64 맥이라 그대로) · 이미지 안에 `data/` 없음 확인 · 컨테이너를 임시 포트로 띄워 `/api/health` 200 확인 후 종료(8600 · 3600 금지)
- `uv run pytest` · `ruff` 1회
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/deploy-be-report.md` — env · 마운트 경로 · 이미지 이름 표(infra 워커가 본다)

## 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_7993d892-b5e4-4ff8-8ee9-ade502f64924 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] backend: <질문>" --enter`
