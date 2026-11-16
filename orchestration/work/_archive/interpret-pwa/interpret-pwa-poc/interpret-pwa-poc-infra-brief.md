# [infra] interpret-pwa(통키) 배포 준비 — charts/interpret-pwa · ArgoCD · cloudflared 호스트 · 시크릿 예시 (sync 없음)

너는 **interpret-pwa `infra` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/infra/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/k8s_infra_mac/interpret-pwa-poc`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

혼자 쓰는 워크트리다. **준비만** — ArgoCD sync · kubectl apply · 시크릿 생성은 하지 않는다(로컬 E2E · main 머지 뒤 코디 · 사용자).

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` **D-26**(도메인 `tongky.medisolveai.xyz` · 네임스페이스 `interpret-pwa-prod` · 이미지 `ghcr.io/kknaksss/interpret-pwa-{back,front}:<sha>`) · D-12
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` §2(포트 back 8800 · front 3800 · env 이름) · §5.2(WS `/api/interpret`) · §8(PWA · HTTPS)
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` WP8 행(범위 · 완료 조건 · 검증)
- 앱 계약(read-only): `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc/back/Dockerfile` · `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc/front/Dockerfile` · `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc/docker-compose.yml` · `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc/.env.example` · `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc/back/app/main.py`(헬스 `/api/health`)

## 2. 배경 / 무엇을 바꾸나

통키(실시간 통역 PWA)를 Mac Studio 클러스터에 올릴 준비. **cc-prototype 배포를 그대로 본뜬다** — 같은 레포 · 같은 Cloudflare Tunnel · 같은 GHCR(private · `ghcr-pull`). 다른 점: DB · PVC 없음(무상태) · 통역 WebSocket 이 오래 열린다.

## 3. 계약

- back: 포트 8800 · `/api/*` · WS `/api/interpret` · 헬스 `GET /api/health` · env 는 Secret `interpret-pwa-secret` envFrom(이름 목록 = `.env.example`) · `INTERPRET_FRONT_ORIGIN=https://tongky.medisolveai.xyz` 는 configmap(값이 공개라 git 에 둬도 됨 — 판단 근거를 리포트에)
- front: 포트 3800 · `NEXT_PUBLIC_API_BASE_URL` 은 **빌드 때** 들어간다(이미지 쪽 몫 — 차트는 모름) · 같은 호스트라 `https://tongky.medisolveai.xyz`
- 이미지 태그는 main 빌드 sha — 지금은 없다. cc-prototype 처럼 비어 있으면 렌더를 거부하는 방식으로 두고, 검증은 가짜 태그를 `--set` 으로 넣어 lint · template · dry-run

## 4. 먼저 읽을 핵심 파일 (이 레포 origin/main)

- `charts/cc-prototype/**` · `argocd/applications/cc-prototype-prod.yaml` · `argocd/projects/cc-prototype.yaml` · `provisioning/secrets/cc-prototype-prod.env.example` · `docs/cc-prototype-deploy.md`
- `charts/cloudflared/values.yaml`(호스트 목록 — `ccc.medisolveai.xyz` 줄 옆에 한 줄)

## 5. allowed_paths

- `charts/interpret-pwa/` · `argocd/applications/interpret-pwa-prod.yaml` · `argocd/projects/interpret-pwa.yaml` · `provisioning/secrets/interpret-pwa-prod.env.example` · `docs/interpret-pwa-deploy.md`
- `charts/cloudflared/values.yaml` — **호스트 한 줄 추가만**(D-26 이 허락)

## 6. 구현 단계

1. `charts/interpret-pwa` — cc-prototype 차트에서 back · front · ingress · configmap 만(PVC · APNs · nodeSelector 없음). replica 1 · arm64 · `imagePullSecrets: ghcr-pull`. ingress: `/api` → back · `/` → front · **WS 업그레이드 · proxy-read/send-timeout 3600 · 버퍼링 끔**(cc-prototype 의 interpret 설정 확인) · back readiness/liveness `/api/health`
2. ArgoCD Application(수동 sync · CreateNamespace) + AppProject
3. cloudflared 호스트 `tongky.medisolveai.xyz` 한 줄
4. 시크릿 예시(이름만) · `docs/interpret-pwa-deploy.md`(시크릿 3종 만드는 명령 — `interpret-pwa-secret` · `ghcr-pull` · 순서 · 첫 sync · 확인 · 휴대폰 확인 항목 SPEC §9.5)
5. 검증(아래) → 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/wp8-infra-report.md`

## 7. 범위 제약

- sync · apply · 시크릿 생성 · 다른 앱 차트 수정 금지 · 커밋 · push 금지 · 키 값 0

## 8. 검증

```
helm lint charts/interpret-pwa · helm template … -f values-prod.yaml · kubectl apply --dry-run=client — 각 1회. 다른 앱 차트·앱 무수정. 시크릿 값 0. 클러스터 접근이 없으면 실배포·sync 는 pending 으로 보고
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "infra 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 \
  --text "[worker_done] infra 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 --text "[질문] infra: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
