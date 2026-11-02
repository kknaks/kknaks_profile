
# [infra] Strong Hajin 운영 첫 배포 — 이미지 push → 클러스터 준비 → 시드 복원 → sync → https 로그인 실측

너는 **strong-hajin `infra` 워커**다. **너는 앞 맥락이 하나도 없다** — 아래가 전부다. 먼저 역할 문서를 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-배포/orchestration/roles/strong-hajin/infra/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-배포/orchestration/work/strong-hajin-deploy/_RESUME.md` §2 결정 표 (배포 결정의 SoT)

작업 워크트리(infra): `/Users/kknaks/orca/workspaces/k8s_infra_mac/strong-hajin-deploy-infra` · 이미지 빌드 소스(code): `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy`

## 1. SSOT — 먼저 읽을 것

- `_RESUME.md` §2 — host `ax.medisolveai.xyz` · registry `ghcr.io/kknaksss` · 운영 데이터 = 로컬 시드 DB dump · AI = 노드 `/opt/codex`·`/opt/claude` 마운트 · dmg 서명은 이 작업 밖
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-배포/orchestration/config/projects/mediness.json` 의 `environments` — 접속 경로(`ssh medi-me`, kubectl 절대경로 `/opt/homebrew/bin/kubectl`), mediness 가 이미지 태그·배포를 어떻게 하는지. **같은 클러스터를 쓴다**
- `/Users/kknaks/orca/workspaces/k8s_infra_mac/strong-hajin-deploy-infra/charts/strong-hajin/` (templates·values·values-prod·NOTES.txt) · `/Users/kknaks/orca/workspaces/k8s_infra_mac/strong-hajin-deploy-infra/argocd/applications/strong-hajin-*.yaml` · `/Users/kknaks/orca/workspaces/k8s_infra_mac/strong-hajin-deploy-infra/charts/datastores/values-strong-hajin.yaml` · `/Users/kknaks/orca/workspaces/k8s_infra_mac/strong-hajin-deploy-infra/charts/cloudflared/values.yaml`
- `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy/deploy/k8s/` (back·front Dockerfile·nginx.conf)
- 기대는 개념: 해당 없음

## 2. 배경

code `kknaks/Strong_hajin#5`(main `cdb0f3f`)와 infra `MediSolveAIDev/k8s_infra_mac#5`(main `f04d4cb`)가 머지됐다. 차트는 `image.tag` 가 비어 있어
렌더를 거부하고, Argo Application 두 개(`strong-hajin-prod`·`strong-hajin-datastores`)는 **수동 sync** 다. 클러스터에는 아직 아무것도 없다.
docker 는 `ghcr.io` 에 `kknaksss` 로 로그인돼 있다(write:packages).

## 3. 계약

- 이미지: `ghcr.io/kknaksss/strong-hajin-back:<tag>` · `ghcr.io/kknaksss/strong-hajin-front:<tag>` (차트 `_helpers.tpl:29` 규칙), `<tag>` = `cdb0f3f-arm64`, `linux/arm64`
- 네임스페이스 `strong-hajin-prod` · 시크릿 이름은 차트가 정한다(`values.yaml` `secretName`·`postgres.passwordSecret`·`imagePullSecrets`)
- 운영 DB 내용 = 로컬 demo DB(`127.0.0.1:54329/ax_demo`, local-stack 은 `COMPOSE_PROJECT_NAME=strong-hajin-work`)의 dump — catalog + 실제 유저 4명. `auth_sessions` 행은 제외

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/k8s_infra_mac/strong-hajin-deploy-infra/charts/strong-hajin/templates/_helpers.tpl` — host·image 필수값
- `/Users/kknaks/orca/workspaces/k8s_infra_mac/strong-hajin-deploy-infra/charts/strong-hajin/templates/back.yaml`·`worker.yaml` — secretRef·hostPath·AI 마운트가 요구하는 것
- `/Users/kknaks/orca/workspaces/k8s_infra_mac/strong-hajin-deploy-infra/charts/strong-hajin/templates/configmap.yaml` — 시크릿에 넣지 말아야 할 값과 넣어야 할 값의 경계

## 5. allowed_paths

- infra 워크트리: `charts/strong-hajin/values-prod.yaml` 의 `image.tag` **한 줄**만(커밋은 코디). 먼저 `git -C /Users/kknaks/orca/workspaces/k8s_infra_mac/strong-hajin-deploy-infra fetch && git -C /Users/kknaks/orca/workspaces/k8s_infra_mac/strong-hajin-deploy-infra checkout -B kknaksss/strong-hajin-deploy-infra origin/main` 으로 머지된 main 위에 선다
- code 워크트리: 읽기 + 빌드만. 먼저 `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy fetch && git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy checkout --detach origin/main` (미커밋 변경 없음을 확인하고)
- 클러스터: **`strong-hajin-prod` 네임스페이스와 그 안의 리소스만.** 노드에는 차트가 요구하는 hostPath 디렉토리 생성만
- Argo: `strong-hajin-datastores`·`strong-hajin-prod` 두 앱의 수동 sync 만

## 6. 단계

1. 이미지: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy` 에서 `deploy/k8s/*.Dockerfile` 로 arm64 두 장 빌드 → push. `docker manifest inspect` 로 arm64 확인
2. 태그: `values-prod.yaml` `image.tag: cdb0f3f-arm64` → `helm lint` + `helm template -f values-prod.yaml` 렌더 성공 확인. **여기서 멈추고 코디에게 보고(태그 커밋·머지는 코디)** — 코디가 머지했다고 답하면 다음으로
3. 클러스터 준비(`ssh medi-me`): 네임스페이스 · `ghcr-pull`(dockerconfigjson — 토큰은 `gh auth token` 을 **파이프로만** 넘기고 출력·파일 저장 금지) · 앱 시크릿 · DB 비밀번호 시크릿(새로 생성한 무작위 값, 출력 금지) · hostPath 디렉토리 · `/opt/codex`·`/opt/claude` 가 노드에 있는지 확인(없으면 멈추고 질문)
4. Cloudflare: `ax.medisolveai.xyz` 가 터널로 들어오는지. mediness 호스트가 DNS 를 어떻게 잡았는지 먼저 보고 같은 방식. **Cloudflare 대시보드 조작이 필요하면 멈추고 질문**
5. `strong-hajin-datastores` sync → DB 준비 → 로컬 시드 dump 복원(스키마+데이터, `auth_sessions` 제외) → `strong-hajin-prod` sync
6. 실측: `https://ax.medisolveai.xyz/` 200 · `/api/auth/providers` 가 `local:true` 이고 `demo_accounts` 없음 · 4명 중 1명 로그인(비밀번호는 코디를 통해 사용자에게 받는다 — 추측·기록 금지) · WS 핸드셰이크 1회 · 워커 4 파드 Ready

## 7. 하지 말 것

- mediness 네임스페이스·공유 리소스(cloudflared 차트 포함) 수정 금지. 클러스터 전역 리소스 생성 금지(네임스페이스 제외)
- Argo 앱에 automated sync 켜지 마라
- 비밀값을 화면·파일·리포트에 남기지 마라
- git 커밋·push·PR 금지(코디 몫). dmg 빌드는 이 작업 밖
- 막히면 30분 헤매지 말고 질문. **되돌릴 수 없는 명령(delete·drop·PVC 삭제) 전에는 반드시 질문**

## 8. 검증

```
Strong Hajin 차트만 helm lint 및 prod helm template. 명시 이미지 태그, 기존 앱과 이름·namespace 격리, 같은 origin FE/API/WS 라우팅·PVC·secretRef 확인.
```
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-배포/orchestration/work/strong-hajin-deploy/report-infra-deploy.md` — 단계별 실행 명령(비밀값 가림)·결과·실측 수치. 단계 2 에서 한 번, 끝에서 한 번 갱신

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_8d586fcb-a104-4f31-9f5f-fd3b659a1d24 --from term_8246ef20-5da7-4ec6-b39f-e867feb3ee64 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "infra 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_8d586fcb-a104-4f31-9f5f-fd3b659a1d24 \
  --text "[worker_done] infra 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_8d586fcb-a104-4f31-9f5f-fd3b659a1d24 --text "[질문] infra: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
