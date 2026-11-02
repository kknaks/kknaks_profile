# [writer] task-management 참조 조사 — Strong Hajin Tauri 래핑·배포 구조의 입력

너는 조사 워커다. 이전 세션 맥락은 없다. 역할 문서는 orchestration/roles/strong-hajin/planner/의 role.md, rules.md, skills.md, tools.md, workflow.md를 읽어라.
현재 코디 워크트리를 공유한다. 다른 코디와 FE 작업이 진행 중이다. 아래 보고서 하나 외에는 수정하지 않는다.

## 1. SSOT — 먼저 읽을 것

- 사용자 목적: 기존 Strong Hajin 웹 프로젝트를 Tauri로 래핑해 앱으로 배포하려 한다. 유사 프로젝트 task_management의 코드·문서를 먼저 조사하여 구조 설계의 입력을 마련한다. 이번에는 조사만 한다.
- 참조 코드: /Users/kknaks/git/toy_pr2/task_management (AGENTS.md부터)
- 참조 문서: /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/task-management (README와 관련 architecture/spec/work/runbook)
- 비교 코드: /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects (AGENTS.md부터, 미커밋 작업 중임)
- 비교 문서: para/projects/summer-star/strong-hajin
- 기대는 개념: 해당 없음. 코드에서 확인된 사실과 문서의 의도, 제안과 미결을 구분한다.

## 2. 배경 / 무엇을 바꾸나

사용자는 두 제품의 내용이 비슷하고 Strong Hajin을 웹 래퍼 앱으로 만들려는 차이가 있다고 설명했다. task_management가 이미 Tauri라고 전제하지 말고 실제 스택을 확인한다. 현재 프로젝트 화면 구현과 독립된 읽기 전용 조사다.

## 3. 계약

제품 변경 없음. 조사 보고서만 제공한다. OS 대상, 원격 서버 접속형/백엔드 동봉형, 오프라인 요구 등 사용자가 정하지 않은 것은 결정하지 않는다.

## 4. 먼저 읽을 핵심 파일

각 레포 AGENTS.md, README, package/pyproject/Cargo manifest, 실행·compose·배포 설정, CI, 아키텍처·배포 문서부터 탐색한다. .env/인증서/키 등 비밀값은 열거나 보고서에 쓰지 않는다.

## 5. allowed_paths

orchestration/work/strong-hajin-projects/research-task-management-tauri.md 하나만 작성 가능. 모든 다른 파일은 읽기 전용.

## 6. 조사 단계

1. task_management 제품 목적·주요 기능·현재 구현 범위, 문서와 코드의 어긋남을 파악한다.
2. FE/BE/DB/파일·자료 저장소/인증/AI·외부 프로세스 구조와 실행 흐름을 그린다. 브라우저에서 서버까지 연결, URL·쿠키·WebSocket/SSE·업로드/다운로드 등을 추적한다.
3. Tauri/desktop/배포 구성의 존재 여부를 확인한다. 있으면 버전·Rust/JS 경계·권한·sidecar·앱 수명주기·업데이트·서명·CI·배포 산출물까지 추적한다. 없으면 없다고 밝힌다.
4. Strong Hajin과 구조를 비교한다. 재사용 가능한 패턴, 바꿔야 하는 경계, 원격 웹 URL 래퍼와 FE 번들+원격 API 및 로컬 백엔드 동봉 방식의 차이를 현 코드 근거로 설명한다. 아직 특정 구조를 확정하지 않는다.
5. 다음 설계를 위해 사용자에게 확인할 핵심 질문 3~5개와 조사로 이미 답이 난 것을 구분한다.

## 7. 범위 제약

코드 수정·설치·빌드·테스트·서버/컨테이너 기동·중단·git 변경·커밋·push·PR·다른 워커 발주 금지. 기존 작업과 전역 orchestration 상태에 손대지 않는다. 로컬 저장소 조사 중심. Tauri의 현재 동작에 관한 외부 주장이 필요하면 공식 문서로 확인하되 광범위한 웹 리서치로 확장하지 않는다.

## 8. 검증

핵심 주장에 절대경로:줄 근거. 조사한 체크아웃의 branch/HEAD/dirty 여부 기록(기존 변경은 건드리지 않음). 부재 주장은 검색 범위 기재. 보고서 머리에 10줄 이내 요약, 이후 구조도·비교표·미결. 완료 시 보고서 경로와 가장 중요한 차이 3개를 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_2ae8654e-00e2-4649-ab7c-cb3b5e02b995 --from term_ac487857-29d3-49b9-9ba8-8c5ad386e21b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_2ae8654e-00e2-4649-ab7c-cb3b5e02b995 \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_2ae8654e-00e2-4649-ab7c-cb3b5e02b995 --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
