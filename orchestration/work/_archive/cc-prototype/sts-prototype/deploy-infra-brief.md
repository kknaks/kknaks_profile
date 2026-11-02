# [infra] cc-prototype 배포 — charts/cc-prototype · ArgoCD 앱 · cloudflared 호스트

너는 **cc-prototype `infra` 워커**. 먼저 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/infra/role.md` (+ 같은 폴더 rules · skills · tools · workflow)
작업 워크트리: `/Users/kknaks/orca/workspaces/k8s_infra_mac/sts-prototype`(레포 `MediSolveAIDev/k8s_infra_mac`, base `origin/main`). 커밋 · push · PR 은 코디.

## SSOT
- **DEC-003**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/10-decision/decision-003-cc-deploy.md` — 도메인 `ccc.medisolveai.xyz` · 같은 출처(`/api` → back) · 공개 · 데이터는 Secret 마운트 · arm64 GHCR · 수동 sync
- 본뜰 차트: `charts/strong-hajin`(back · front · ingress · configmap) · `argocd/applications/strong-hajin-prod.yaml` · `charts/cloudflared/values.yaml`(hosts)
- 앱 계약: back 워커가 지금 쓰는 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/deploy-be-report.md`(env · 마운트 · 이미지) — 아직 없으면 아래 값으로 짜고 맞으면 그대로:
  - back `ghcr.io/kknaksss/cc-prototype-back:<sha>` · 포트 8600 · `/api/health` · env `CC_DB_PATH=/data/db/cc.db`(PVC) · `CC_SCENARIO_DIR=/data/scenario` · `CC_KOS_STAFF_PATH=/data/staff/kos-staff.json`(둘 다 Secret 마운트) · `SONIOX_API_KEY`(Secret env) · `CC_FRONT_ORIGIN=https://ccc.medisolveai.xyz`
  - front `ghcr.io/kknaksss/cc-prototype-front:<sha>` · 포트 3600
  - SSE `/api/events` · WebSocket `/api/interpret`

## 할 것
1. `charts/cc-prototype/`: back(Deployment replica **1** · Recreate · PVC 1Gi · Secret 마운트 2개 · secretRef env) · front(Deployment) · Service 2 · **Ingress**(host `ccc.medisolveai.xyz`, `/api` → back, `/` → front, SSE 버퍼링 끔 · 긴 read/send timeout · WS Upgrade) · image registry/tag 는 values(비면 렌더 실패하게 — strong-hajin 방식) · GHCR pull secret 참조(이름만)
2. `values-prod.yaml` · `argocd/applications/cc-prototype-prod.yaml`(namespace `cc-prototype-prod`, CreateNamespace, **수동 sync**) · 필요하면 `argocd/projects/cc-prototype.yaml`
3. **`charts/cloudflared/values.yaml` hosts 에 `ccc.medisolveai.xyz` 한 줄 추가**(이 파일은 이 한 줄만 허락)
4. `provisioning/secrets/cc-prototype-prod.env.example`(키 이름만) + docs 에 **코디/사용자가 할 일**: Secret 3개 만드는 `kubectl create secret` 명령(soniox env · scenario 디렉터리 · staff 파일 · ghcr pull) · DNS `cloudflared tunnel route dns <tunnel> ccc.medisolveai.xyz` · argocd 수동 sync
5. 실배포 · sync · kubectl apply 하지 마라

## 범위 · 검증
- allowed: `charts/cc-prototype/` · `argocd/applications/cc-prototype*.yaml` · `argocd/projects/cc-prototype.yaml` · `charts/cloudflared/values.yaml`(한 줄) · `provisioning/secrets/cc-prototype*.env.example` · `docs/` cc-prototype 문단. 그 밖 금지
```
helm lint charts/cc-prototype · helm template … -f values-prod.yaml --set image.tag=test · kubectl apply --dry-run=client — 각 1회. 다른 앱 무수정. 시크릿 값 0
```
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/deploy-infra-report.md` — 만든 파일 · 검증 · **사용자/코디 할 일 체크리스트**(명령 그대로)

## 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_38643bb0-bece-4c6f-abd4-eb8a801ed023 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "infra 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과 / 사용자 할 일 / 미결"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] infra 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] infra: <질문>" --enter`
