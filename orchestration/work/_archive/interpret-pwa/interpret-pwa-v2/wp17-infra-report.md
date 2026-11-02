# WP17 infra 리포트 — back PVC · 통역 기록 env (D-41 · SPEC-001 0.6.0 §9.6)

- 워크트리: `k8s_infra_mac/interpret-pwa-v2` (branch `kknaksss/interpret-pwa-v2`, base 17e059b) · **커밋 · push · sync · apply 안 함**
- 이미지 태그: **안 바꿈** (back `2a9d5a5` · front `fe8475e` 그대로) — WP16 머지 sha 가 나오면 WP18 에서 `back.imageTag`(또는 `image.tag` 하나로 정리)

## 바꾼 파일

| 파일 | 내용 |
|---|---|
| `charts/interpret-pwa/templates/back-pvc.yaml` (신규) | PVC `interpret-pwa-records` · RWO · `local-path` · 1Gi · `helm.sh/resource-policy: keep` — cc-prototype `back-pvc.yaml` 선례 그대로 |
| `charts/interpret-pwa/templates/back.yaml` | `nodeSelector` 블록 · `volumeMounts` `/data` ← PVC · `volumes` · 「Stateless」 주석 → RollingUpdate 유지 이유(노드 고정 · 줄 단위 append) |
| `charts/interpret-pwa/templates/configmap.yaml` | `INTERPRET_RECORD_DIR: "/data/records"` + 렌더 가드(`recordsDir` 가 `dataDir` 밖이면 `fail` — 기록이 컨테이너 fs 에 써져 재시작 때 사라지는 실수 방지) |
| `charts/interpret-pwa/values.yaml` | `back.recordsPvcName` · `recordsStorage: 1Gi` · `dataDir: /data` · `recordsDir: /data/records` · `podSecurityContext.fsGroup: 10001` · `nodeSelector: {}` · 「No volumes → no fsGroup」 주석 고침 |
| `charts/interpret-pwa/values-prod.yaml` | `back.nodeSelector: {kubernetes.io/hostname: lima-worker-1}` (태그 줄은 그대로) |
| `charts/interpret-pwa/templates/NOTES.txt` | 5번 — PVC Bound 조건 · nodeSelector · 기동 로그 |
| `docs/interpret-pwa-deploy.md` | 개요(Stateless → PVC) · ConfigMap 문단 · **「통역 기록」 절**(PVC · keep · 노드 고정 이유 · RollingUpdate 이유 · back 이 하는 7일 삭제 규칙 · 기동 로그) · **「꺼내기」**(`get pod` → `exec ls` → `kubectl cp <pod>:/data/records/<YYYY-MM-DD>.jsonl` · `exec cat` 대안 · `exec rm` 초기화 · ⚠ 대화 문장 — git 밖에서 보고 지움 · 보고는 수치만) · Redeploy(기록은 PVC 로 남음) · Verify(§9.6 — PVC Bound · lima-worker-1 · 로그 · 7일 삭제 시험) |

ArgoCD AppProject `interpret-pwa` 는 `namespaceResourceWhitelist: */*` 라 PVC 추가에 변경 불필요. 시크릿 · `.env.example` 무변경(`INTERPRET_RECORD_DIR` 은 ConfigMap · §2.4).

## 검증

| 명령 | 결과 |
|---|---|
| `helm lint charts/interpret-pwa -f values-prod.yaml` | 1 chart linted, 0 failed (INFO icon 권장만) |
| `helm template … -f values-prod.yaml` | OK — PVC `interpret-pwa-records`(local-path · 1Gi · keep) · `nodeSelector kubernetes.io/hostname: lima-worker-1` · `fsGroup: 10001` · mount `/data` · `claimName: interpret-pwa-records` · ConfigMap `INTERPRET_RECORD_DIR: "/data/records"` |
| `helm template … --set host=x.example,image.registry=ghcr.io/fake,image.tag=fake0000` (기본 values · 가짜 태그) | OK — nodeSelector 없음(기본 `{}`) |
| `--set back.recordsDir=/tmp/rec` | 의도대로 렌더 거부: `back.recordsDir must sit under back.dataDir …` |
| `kubeconform -strict -kubernetes-version 1.30.0` (prod + fake) | 14 resources · Valid 14 · Invalid 0 |
| `helm install --dry-run=client` NOTES | 5번 렌더 정상 |
| `kubectl apply --dry-run=client` | 로컬 kubeconfig 없음(localhost:8080 openapi 실패) — kubeconform 으로 대체 |
| 비밀값 | 렌더 결과 `kind: Secret` 0 · 값 0 |

- back 이미지(`python:3.12-slim` · Debian)에 `tar` 있음 → `kubectl cp` 사용 가능. `exec cat` 은 대안으로 문서에 둠.

## 남은 것 (WP18)
- WP16 머지 sha → `values-prod.yaml` back 태그 → infra PR 머지 → ArgoCD 수동 sync → §9.6 ① ~ ⑦.
- 첫 sync 때 PVC 는 WaitForFirstConsumer 라 back pod 가 `lima-worker-1` 에 잡혀야 Bound — `get pvc,pod -o wide` 로 확인.
