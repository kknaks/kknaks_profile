# [infra] WORK-008 Phase 4 — AX 세션 런타임 홈을 Mac 호스트 공유 경로로 (B-03)

너는 **strong-hajin `infra` 워커**다. 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/infra/role.md` (+ 같은 폴더 문서).
작업 워크트리: `/Users/kknaks/orca/workspaces/k8s_infra_mac/strong-hajin-polish-infra` (base origin/main, 회사 org 레포 `MediSolveAIDev/k8s_infra_mac`).

## 배경
운영 회의 요약이 실패한다(`…/orchestration/work/strong-hajin-polish/research-meeting-summary.md`): AX(codex) 세션 파일이 각 파드 컨테이너 로컬(`/app/.scax/codex-runtime`)에 저장돼, 회의 중 back 에서 연 세션을 worker-meeting 이 이어 가지 못한다. 녹음처럼 **Mac 호스트 공유 경로**에 둔다(사용자 2026-10-01).
코드 쪽(Phase 4, backend 워커)은 env **`SCAX_CODEX_RUNTIME_HOME`** 으로 이 경로를 받는다(없으면 기존 기본값).

## 계약
- hostPath **`/mnt/mac/strong-hajin/codex-runtime`** (녹음·자료 hostPath 와 같은 방식, `DirectoryOrCreate` 등 기존 관례) 를 **back · worker-conversation · worker-material · worker-meeting · worker-report** 다섯에 **같은 컨테이너 경로**로 마운트하고, 다섯 모두에 env `SCAX_CODEX_RUNTIME_HOME=<그 컨테이너 경로>`
- 다섯이 `lima-worker-1` 고정인지 확인(nodeSelector/affinity) — 아니면 [질문]
- 값은 `values-prod.yaml`(필요하면 values.yaml 기본) 에서 끌 수 있게. 기존 `codex-home` PVC(`/root/.codex` 인증)는 **건드리지 않는다**
- 쓰는 곳 전부: 차트 템플릿에서 back·워커 deployment 를 grep 으로 전부 세고, 하나라도 빠지지 않게
- 노드 디렉터리 생성이 필요하면 RUNBOOK-002 §2-4 처럼 명령만 보고에 적는다(실행하지 마라)

## allowed_paths
- `charts/strong-hajin/` 만

## 하지 말 것
- 클러스터 적용·Argo sync·push·커밋·PR 금지. 공유 mediness 리소스 변경 금지. 비밀값 발명·출력 금지

## 검증
```
helm lint charts/strong-hajin -f charts/strong-hajin/values-prod.yaml
helm template strong-hajin charts/strong-hajin -f charts/strong-hajin/values-prod.yaml -n strong-hajin-prod
```
렌더 결과에서 다섯 deployment 의 volumeMount·env 를 발췌해 보고.

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send --to term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --from <네 워커handle> --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "infra 완료: WORK-008 Phase 4 codex-runtime hostPath" --body "변경 파일 / 다섯 deployment 렌더 발췌 / lint·template 결과 / 노드에서 할 명령"
orca terminal send --terminal term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --text "[worker_done] infra 완료 — codex-runtime hostPath. 상세는 인박스." --enter
```
