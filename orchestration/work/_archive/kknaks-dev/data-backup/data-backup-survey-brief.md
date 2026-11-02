
# [surveyor] k8s_infra_mac 인프라 조사 — 네트워크·배포·스토리지

너는 **kknaks-dev `surveyor` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/data-backup/orchestration/roles/kknaks-dev/surveyor/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/data-backup`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ 이 워크트리는 **코디네이터와 공유**한다. `reference/2026-09-19-data-backup/architecture.md` 는 코디네이터가 작업 중이다 — 열어보는 것은 되지만 **수정 금지**.

## 1. SSOT — 먼저 읽을 것

- **조사 대상**: `/Users/kknaks/git/harness_works/k8s_infra_mac` — **read-only.** 이 레포의 파일을 절대 수정하지 마라.
- 참고(배경 파악용, 수정 금지): `/Users/kknaks/orca/workspaces/kknaks_profile/data-backup/reference/2026-09-19-data-backup/architecture.md`

기대 개념: 해당 없음.

## 2. 배경

사내 8개 서비스의 운영 DB(MySQL·PostgreSQL)를 맥스튜디오 백업 서버로 상시 수집하는 시스템을 설계 중이다.
수집 방식은 복제 프로토콜 스트리밍(`pg_receivewal` · `mysqlbinlog`)으로 확정됐고, 수집 프로세스는 맥스튜디오의 k8s에 파드로 띄울 계획이다.

지금 필요한 것은 **그 맥스튜디오 k8s가 실제로 어떻게 구성돼 있는지에 대한 사실**이다.
설계 문서의 통신 구간·배포 방식·테스트 방법을 이 조사 결과 위에 쓴다.

**너는 사실만 수집한다.** 제안·개선안·설계는 쓰지 마라 — 코디네이터가 판단한다.

## 3. 계약

해당 없음.

## 4. 조사 항목 — 이 7가지에 답하라

각 항목마다 **근거를 `파일:줄`로 인용**한다. 확인 못 한 것은 「확인 불가」라고 쓴다. 추측 금지.

1. **k8s 구성** — 배포판(k3s / k8s / Docker Desktop / minikube / kind 등), 버전, 노드 수, 매니페스트 형태(raw yaml · helm · kustomize), 네임스페이스 구조
2. **현재 워크로드** — 무엇이 떠 있나. 특히 **DB(PostgreSQL · MySQL)** 가 있으면 어떤 리소스(StatefulSet/Deployment)로, 어떤 이미지·버전으로, 어떤 포트로 떠 있는지
3. **네트워크 / 외부 노출** — Service 타입, Ingress 컨트롤러, **Cloudflare 관련 설정(cloudflared · Tunnel · Access · 토큰)** 유무와 형태, 외부에서 클러스터 안으로 들어오는 경로, 클러스터에서 밖으로 나가는 경로에 제약이 있는지
4. **스토리지** — StorageClass, PV/PVC 구성, 호스트 경로 마운트 여부, 용량 설정
5. **시크릿 관리** — Secret 생성 방식(수동 · sealed-secrets · SOPS · 외부 저장소), 레포에 커밋돼 있는지
6. **배포 흐름** — 이미지 빌드 방법, 레지스트리(로컬/원격), 배포 명령(Makefile · 스크립트 · CI), 로컬에서 맥스튜디오로 올리는 절차가 문서화돼 있는지
7. **아키텍처 / 플랫폼** — arm64 전제인지, 이미지에 `platform` 지정이 있는지, x86_64 이미지를 돌리는 흔적이 있는지

추가로, **로컬 개발 환경**에 대한 기록(README·docs·Makefile 등)이 있으면 그대로 옮겨 적어라.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `reference/2026-09-19-data-backup/survey-k8s-infra-mac.md (이 파일 1개만 생성·수정. 조사 대상 레포는 read-only)`

## 6. 산출물

`reference/2026-09-19-data-backup/survey-k8s-infra-mac.md` 파일 **1개**를 생성한다.

구성:

```
# k8s_infra_mac 조사 리포트

## 0. 조사 범위와 방법
(무엇을 읽었는지 — 디렉토리 구조 요약)

## 1. k8s 구성
## 2. 현재 워크로드
## 3. 네트워크 / 외부 노출
## 4. 스토리지
## 5. 시크릿 관리
## 6. 배포 흐름
## 7. 아키텍처 / 플랫폼

## 8. 확인 불가 항목
(조사 항목 중 레포에서 근거를 찾지 못한 것을 전부 나열)
```

- 각 절은 **개조식**으로. 서술형 문단 금지
- 모든 사실 뒤에 `파일:줄` 근거를 붙인다
- 레포에 없는 내용은 §8에 모은다. 본문에 추측을 섞지 마라

## 7. 범위 제약 — 하지 말 것

- 조사 대상 레포(`/Users/kknaks/git/harness_works/k8s_infra_mac`)의 파일을 **생성·수정·삭제하지 마라.** `git` 명령으로 상태를 바꾸지 마라
- `kubectl` 로 **실제 클러스터에 접속하지 마라.** 레포에 있는 파일만 읽는다
- 제안·개선안·설계안을 쓰지 마라. 「~하는 것이 좋다」 류의 문장 금지
- `architecture.md` 를 포함해 `reference/2026-09-19-data-backup/survey-k8s-infra-mac.md` 외 어떤 파일도 수정하지 마라
- 커밋·push 하지 마라

## 8. 검증

```
조사는 read-only — 대상 레포 파일을 고치지 않는다. 산출물은 리포트 1개. 모든 서술에 파일:줄 근거를 붙이고, 확인 못 한 것은 「확인 불가」로 남긴다
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
  --to term_7af47b78-7f02-4497-87f4-447855ab720f --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "surveyor 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_7af47b78-7f02-4497-87f4-447855ab720f \
  --text "[worker_done] surveyor 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_7af47b78-7f02-4497-87f4-447855ab720f --text "[질문] surveyor: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
