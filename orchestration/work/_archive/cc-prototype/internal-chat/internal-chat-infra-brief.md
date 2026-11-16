# [infra] 직원 앱 내부 채팅 — 사진 볼륨 20Gi · 업로드 한도 100m (charts/cc-prototype)

너는 **cc-prototype `infra` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/roles/cc-prototype/infra/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/k8s_infra_mac/internal-chat`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md` **D-58 · D-59** (그리고 D-49 ~ D-53 동영상)
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` §9 사진 · 동영상 (0.3.0 — 한도 100MB 문구는 D-58 로 90MB 가 이긴다)
- `/Users/kknaks/orca/workspaces/k8s_infra_mac/internal-chat/charts/cc-prototype/` 전체 · `/Users/kknaks/orca/workspaces/k8s_infra_mac/internal-chat/docs/` 의 cc-prototype 문단

**기대는 개념**: 해당 없음

## 2. 배경

직원 앱 채팅에 동영상(3분 · 변환 뒤 90MB)과 사진 여러 장을 보낸다. 저장은 기존 `procedure-photos` PVC(`PROC_PHOTO_DIR`) 하위 `chat/` 이다. 지금 값은 신분증 사진 기준이라 동영상이 안 들어간다:
- `charts/cc-prototype/values.yaml` `back.photo.storage: 1Gi`
- `charts/cc-prototype/values.yaml` `ingress.proxyBodySize: "10m"` → 동영상 올리기가 413

## 3. 계약

해당 없음 — 앱 · back 계약은 그대로. infra 값만 바꾼다.

## 4. 할 것

1. `back.photo.storage` 1Gi → **20Gi**. **local-path PVC 는 늘리기(resize)가 안 될 수 있다** — StorageClass `allowVolumeExpansion` · local-path 동작을 확인하고, 이미 있는 PVC 를 어떻게 키우는지(로컬 경로라 크기가 실제 제한이 아닌지 · 다시 만들어야 하는지 · 데이터 보존 `resource-policy: keep`)를 리포트에 사실로 적는다. 다시 만들어야 하면 **하지 말고** 절차만 적어 코디에게 올린다
2. 노드(`lima-worker-1`) 디스크 여유 — 레포 문서 · 값에서 알 수 있는 만큼만(클러스터 접근이 있으면 `kubectl` 읽기만 · 없으면 pending)
3. `ingress.proxyBodySize` "10m" → **"100m"** (values.yaml · values-prod.yaml 에 덮어쓰기가 있으면 거기도)
4. 주석 갱신: `values.yaml` photo 주석(「Small (≤ 5MB per photo)」 → 채팅 사진 · 동영상 포함 · D-58 90MB · Cloudflare 100MB 본문 한도) · `back-photo-pvc.yaml` 머리 주석에 채팅 사진 · 동영상 한 줄(법적 검토 주석 그대로)
5. back 컨테이너 임시 디스크: 동영상 multipart 는 Starlette 임시 파일(컨테이너 `/tmp`)을 쓴다 — `back.yaml` 에 emptyDir · ephemeral-storage 제한이 있는지 보고 문제가 되면 리포트(고치는 건 코디 승인 뒤)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `charts/cc-prototype/`
- `argocd/applications/cc-prototype*.yaml`
- `argocd/projects/cc-prototype.yaml (필요할 때만)`
- `provisioning/secrets/cc-prototype*.env.example`
- `docs/ 의 cc-prototype 문단`


## 6. 하지 말 것

- 커밋 · push · PR 금지 · ArgoCD sync · `kubectl apply` · PVC 삭제 · 재생성 금지(읽기만)
- 다른 앱 차트 무수정 · 시크릿 값 0
- 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/infra-report.md`

## 8. 검증

```
helm lint charts/cc-prototype · helm template … -f values-prod.yaml · kubectl apply --dry-run=client — 각 1회. 다른 앱 차트·앱 무수정. 시크릿 값 0. 클러스터 접근이 없으면 실배포·sync 는 pending 으로 보고
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_61179808-14b1-431b-a85f-619d2c232e8e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "infra 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_61179808-14b1-431b-a85f-619d2c232e8e \
  --text "[worker_done] infra 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_61179808-14b1-431b-a85f-619d2c232e8e --text "[질문] infra: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
