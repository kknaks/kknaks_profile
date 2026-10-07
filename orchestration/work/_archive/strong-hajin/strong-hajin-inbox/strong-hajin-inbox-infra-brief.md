
# [infra] WORK-011 Phase INFRA — 외부 채널 운영 배치(연동 워커 · hostPath · Secret · AX_WEB_ORIGIN)

너는 **strong-hajin `infra` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/roles/strong-hajin/infra/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/k8s_infra_mac/strong-hajin-inbox-infra`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 워크트리는 너 혼자 쓴다(인프라 레포). 클러스터 적용·push 금지.

## 1. SSOT — 먼저 읽을 것 (너는 맥락이 없다 — 이게 전부다)

- **WORK-011** `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/30-work/work-011-external-channels.md` — 「Phase INFRA」 절과 「반영」 절(★4 순서: hostPath mkdir → manual SQL → Secret → 차트 → 이미지 → dmg)
- **SPEC-008** `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-008-external-channels.md` v0.5.1 — §5 프로세스 배치(연동 워커 **레플리카 1** · Socket Mode 단일 소유) · 파드×마운트 표 · env 이름(외부 `GOOGLE_*`·`GMAIL_*`·`SLACK_*`, 내부 `AX_*`) · 업로드 한도
- 백엔드 실제 env·엔트리포인트: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/be2-report.md`(연동 워커 실행 명령) · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/be3-report.md`(hostPath 경로 env) · 코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-inbox`(읽기만 — `backend/src/ax_workspace/bootstrap/settings.py`)
- **검수 필수 W-1** `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/review-be1.md` — 운영 configmap 에 **`AX_WEB_ORIGIN`(=https://ax.medisolveai.xyz)** 이 없으면 OAuth redirect·콜백이 localhost 가 된다 · `AX_API_ORIGIN` 도 확인
- 운영 런북 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/70-runbook/runbook-002-production-deploy.md`(§2-4 hostPath · §148-156 Secret patch 방식 · 차트는 비밀값 없음)

**기대는 개념** — 해당 없음.

## 2~4. 무엇을

Strong Hajin 차트(`charts/strong-hajin/`)에 외부 채널 운영 배치를 더한다. 차트는 **값만 이름으로 참조**(Secret 은 사람이 out-of-band 로 만든다).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `charts/strong-hajin/`
- `charts/datastores/values-strong-hajin.yaml`
- `argocd/applications/strong-hajin-*.yaml`
- `argocd/projects/strong-hajin.yaml`

## 6. 구현 단계

1. **연동 워커 Deployment**(이미지 = back 이미지 · 명령 = be2-report 의 연동 워커 엔트리포인트 · **replicas 1 고정 · strategy Recreate**(Socket Mode 단일 소유 — 롤링 중 둘이 붙지 않게)) · back 과 같은 `secretRef`·configmap
2. **configmap**: `AX_WEB_ORIGIN`·`AX_API_ORIGIN`(운영 origin) · hostPath 경로 env(카톡 첨부·프로필 이미지 — be3-report 이름 그대로) · 그 밖 비밀 아닌 값
3. **Secret 키**(값 없음 — 런북에 patch 명령으로): `GOOGLE_OAUTH_CLIENT_ID/SECRET` · `GMAIL_PUBSUB_TOPIC/SUBSCRIPTION` · `SLACK_CLIENT_ID/SECRET` · `SLACK_APP_TOKEN` · 토큰 암호화 키(`AX_…` — 이름은 코드 기준) · **Pub/Sub 서비스 계정 키 파일** → 별도 Secret 을 **파일 볼륨으로 마운트**하고 `GOOGLE_PUBSUB_SA_KEY_FILE` 을 그 경로로
4. **hostPath 마운트**: 카톡 첨부·프로필 이미지 저장 폴더 — 쓰는 파드(back · 필요하면 연동 워커)에만 · 타입 Directory(★4: 노드에 폴더가 먼저 있어야 함 — 반영 절에 mkdir 명령)
5. **ingress body size**: 업로드 한도 50MB 를 받도록(`proxy-body-size` 등 — 지금 값 확인 · 앱 한도와 같으면 여유를 두어 앱이 413 을 먼저 내게)
6. **WS 라우팅**: 새 메시지함 WS 경로(be3-report)가 같은 origin 으로 back 에 붙는지 · 타임아웃
7. 운영 반영 문서: WORK-011 반영 절과 맞춘 **명령 목록**(mkdir · manual SQL · Secret patch(값은 `~/.config/google/env`·`~/.config/slack/env` 에서 읽어 stdin) · 차트 · Argo 수동 sync · 롤백 역순)을 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/infra-deploy-steps.md` 로 남겨라 — **실행하지 마라**

## 7. 범위 제약

- 클러스터 적용·Argo sync·push·Release 금지 · 공유 Mediness·클러스터 기반 리소스 금지 · 비밀값 금지

## 8. 검증

```
Strong Hajin 차트만 helm lint 및 dev/prod helm template. 명시 이미지 태그, 기존 앱과 이름·namespace 격리, 같은 origin FE/API/WS 라우팅·PVC·secretRef 확인. 클러스터 적용·GitOps push·Release 발행 없이 로컬 렌더 결과를 보고.
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
  --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_92255e52-73b0-43f3-8eee-d733434da316 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "infra 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b \
  --text "[worker_done] infra 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[질문] infra: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
