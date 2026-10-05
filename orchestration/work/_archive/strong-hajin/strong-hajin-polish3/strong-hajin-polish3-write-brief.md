# [writer] 고도화 3차 결정(a~g · R1~R6)을 SPEC 에 반영한다

너는 **strong-hajin `writer` 워커**다. **너는 이 작업의 맥락이 없다** — 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 위치: **코디 워크트리에 직접** — `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화`
(문서 워커는 workspace=coordinator. 개별 워크트리 없음)

⚠ 이 워크트리의 `orchestration/` 과 `30-work/` 는 코디 것 — 건드리지 마라. 코드 워크트리에는 지금 변경이 없다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/_RESUME.md` §1·§2 ← **이번 결정의 SoT.** §2 의 2026-10-04 행 전부(a~g · R3 · R4 · R5 · 완료 확인창)가 반영할 내용이다. **여기 없는 것은 발명하지 마라**
- 조사 리포트(지금 코드가 어떻게 도나 — SPEC 문장의 사실 근거): 같은 폴더 `fe-survey-report.md`(§3 회의 제목 · §4 업무 상세 구조·편집·진행과 판단 8구획·푸터 매트릭스·출처·입구 16곳·부품 · §5 막힘 · §6 여백) · `be-survey-report.md`(§2 내보내기·Tauri · §3 회의 제목 API · §4 업무 수정 API·버전·담당 변경·전이표·날짜·출처·상세 응답 · §5 선행 게이트)
- 직전 판: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-009-polish2.md` · `work-007-task-detail.md`
- SPEC: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/20-spec/spec-007-task-detail.md`(v0.4.0) · `spec-006-tauri-wrapper.md`(v0.2.3) · 필요하면 `spec-001`·`spec-003`·`spec-002`·`spec-004` · `20-spec/README.md`

**기대는 개념** — 해당 없음

## 2. 반영할 결정 — 사용자와 닫은 계약

**각 결정이 「어느 SPEC 의 어느 절에 이미 있나」를 grep 으로 전부 찾아** 그 자리를 고친다(같은 계약이 여러 SPEC 에 흩어져 있으면 전부 — 예: 업무 상세 푸터·편집·「진행과 판단」·AX 단추·막힘 배너를 말하는 문장은 SPEC-007 밖에도 있을 수 있다). 없으면 그 계약을 소유한 SPEC 에 새 줄을 세우고 판단을 보고한다. 「자리 힌트」는 출발점일 뿐이다.

### 업무 상세 모달 (SPEC-007 중심)

| # | 결정 |
|---|---|
| H | **헤더 = 제목 + `⋯`(조건부) + `×`.** 「업무 상세」 머리글·상태 칩·버전 배지·「편집」·「AX」 단추를 뺀다. 제목은 클릭하면 그 자리 인라인 입력, blur/Enter 저장, Esc 취소, 빈 값은 저장 안 하고 되돌림 |
| M | **「메타 정보」 구역 신설** — 「업무 정보」와 같은 계층, 라벨·값 2열 격자. 행: 진행 상태(셀렉트) · 버전(읽기 전용) · 담당(셀렉트, 아래 c) · 실제 시작일(읽기 전용) · 시작 예정일 · 마감일(날짜 선택 즉시 저장, 시작 예정일>마감일 막음) · 출처(아래 e, 없으면 행 숨김). 현재 메타 줄에 있는 실제 종료일·결재·참조를 어떻게 둘지는 기존 SPEC 계약(E2E-5 날짜 넷 등)을 지키는 쪽으로 정하고 보고한다(빼라는 결정은 없다) |
| I | **편집 모드 폐지 · 인라인 즉시 저장.** 제목·업무 내용(여러 줄, blur 저장)·날짜는 그 자리에서 고쳐 바로 저장. 값이 안 바뀌면 요청 안 함. 실패하면 원래 값 복원 + 필드 옆 표시. 저장은 `PATCH /api/tasks/{id}` 이고 매번 version 이 오르므로 **한 번에 하나씩 직렬로**, 앞 응답의 version 을 이어 싣는다(422 `task version is stale` 처리 문장 포함). 「변경 저장」 단추 없음 |
| F | **푸터 삭제.** 상태 전이는 메타 정보 진행 상태 셀렉트로만 |
| b | **진행 상태 셀렉트 = 상태 전이만** — 현재 상태·역할에서 서버 허용표(be-survey §4-5)상 갈 수 있는 상태만 보인다. 사유가 필요한 전이(막힘 — 사유 필수 · 업무 취소 — 사유 필수, 맨 아래 빨강 · 완료에서 재개 — 사유 선택)는 **작은 모달**로 사유를 받는다(지금 본문 안에 펼쳐지는 막힘 사유 입력도 모달로). 요청받은 업무의 「완료」는 기존 **완료 보고 모달**. 미완 체크리스트가 있을 때 완료는 기존 확인창 「남은 단계가 있습니다」 유지. 요청자의 「취소 제안」·「조건 변경 제안」은 상태가 아니므로 헤더 **`⋯` 메뉴**(요청자에게만 보임) → 작은 모달 |
| c | **담당 셀렉트** — 사람을 고르면 사유(선택) 작은 모달 → `POST /api/tasks/{id}/reassign` **변경 제안**(새 담당 수락 전까지 기존 담당 유지). 담당 칸에 「변경 제안 중」 표시. `task.assign` 이 없으면 읽기 전용(구성원 기본 없음) |
| a | **「진행과 판단」 구역 삭제** — 구역 제목·「담당자 변경」 단추를 없앤다. 그 안의 **걸린 일**(막힘 사유 · 완료 확인 대기 + 「완료 인정」「보완 요청」 · 보완 필요 · 담당 변경 대기 · 취소/조건 변경 제안 + 동의/동의하지 않음/철회 · 미완 하위)은 **있을 때만** 메타 정보 바로 아래 상자로 선다. 없으면 아무것도 안 선다 |
| d | **「AX에게 이 업무 묻기」 삭제** — 대체 입구 없음 |
| e | **출처 행** = 「AX 제안 · 판단 보기」(링크 = 원 AX 초안 판단 상세). 링크를 열 수 없는 화면(홈·캘린더)은 글자만. 요청에서 온 업무 등 다른 출처 문구는 지금 규칙 유지 |
| R5 | **선행 막힘 배너 「시작할 수 없습니다」·푸터 문구 삭제.** 막는 규칙(서버 409)은 유지 — 상태 셀렉트에서 거부되면 서버 문장을 토스트로 내고 셀렉트는 원래 값 |
| RO | **읽기 전용으로 열리는 입구**(fe-survey §4-7 — `canManage=false`·`access=read_only`)에서는 인라인 편집·셀렉트·`⋯` 가 전부 꺼진다(값만 보인다) |
| f/R6 | 헤더→첫 구역 간격을 줄인다 — **업무 상세에만**(공용 모달 규칙 불변) |
| — | 「자료」「이력」 구역·체크리스트·연관 업무는 이번 범위 밖(그대로) |

### 회의 상세 · 로그인 · 데스크톱

| # | 결정 | 자리 힌트 |
|---|---|---|
| R3 | 회의 상세 제목 = 클릭 인라인 수정(H 와 같은 규칙, `PATCH /api/meetings/{id} {title}`). 참석자·「예정」「완료」 회의만 — 그 밖은 읽기 전용. 제목이 비었을 때만 옆에 「제목 후보: … [적용]」, [적용]은 후보를 제목으로 저장 | 회의 화면 계약이 있는 SPEC 을 grep 으로 찾는다. 없으면 보고하고 Open Questions(WP 에만 둘지 코디가 정한다) |
| R2a | 회의 상세 「내보내기」 단추 크기를 옆 단추(sm)와 맞춘다 | 위와 같음 — 화면 픽셀 수준이면 SPEC 에 안 써도 된다(판단 보고) |
| R2b | **데스크톱 앱에서 첨부 응답(회의 내보내기 `.html` 등 `Content-Disposition: attachment`)은 파일로 저장되고 앱 화면은 그대로 남는다.** 지금은 웹뷰가 HTML 을 그려 버려 돌아갈 길이 없다. 업무 자료·요청 첨부의 `_blank` 링크도 같은 경로로 확인한다. 완료 조건 = macOS 실기 확인, Windows 는 pending | SPEC-006 |
| R1 | 로그인 브랜드 h1 = 「메디솔브 AX 프로젝트」, 설명 문장 삭제 | 로그인 화면 계약이 있는 SPEC 이 있으면 그 자리, 없으면 SPEC 에 쓰지 않고 보고 |

## 3. 규칙

- 각 SPEC 의 기존 형식(결정 ID·근거 열·인수조건 번호·버전·changelog)을 따른다. 고친 SPEC 마다 버전을 올리고 변경 이력을 남긴다
- 결정의 근거는 「사용자 2026-10-04 (고도화 3차)」. **사용자 실명·메일을 쓰지 마라**(공개 레포)
- 기존 SPEC 문장과 **충돌**하면 고친다 — 무엇과 충돌했는지 보고한다(특히 상세 「편집」·「변경 저장」·푸터 단추·「진행과 판단」·AX 단추·막힘 배너를 말하는 문장)
- 인수조건이 있는 SPEC 은 바뀐 계약의 인수조건 줄을 고치거나 더한다 — **삭제되는 것(푸터·편집·AX·배너)도 「없다」를 인수조건으로**
- 서버 API·필드는 바꾸지 않는다(이번 판은 서버 변경 없음). API 이름은 조사 리포트의 실제 경로를 쓴다
- 결정되지 않은 것을 메우지 마라. 애매하면 Open Questions 로 남기고 보고한다
- 린트가 있으면 돌린다(role 문서의 방법대로). 0 ERROR

## 4. allowed_paths

- `para/projects/summer-star/strong-hajin/20-spec/` 의 SPEC 파일과 `20-spec/README.md`
- 그 밖(`30-work/`·`10-decision/`·`orchestration/`·코드 레포)은 **읽기만**

## 5. 하지 말 것

- 커밋·push·PR 금지 · WP(`30-work/`) 수정 금지(코디가 쓴다) · 코드 레포 수정 금지(필요하면 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3` 를 읽기만)
- 서버·브라우저 띄우지 마라

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 작성 시점 값이다. preamble 과 다르면 **preamble 이 맞다.**

```bash
orca orchestration send \
  --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer 완료: 고도화 3차 SPEC 반영" \
  --body "고친 SPEC·절·버전 목록 / 결정별 반영 위치 / 충돌·고친 문장 / Open Questions / 린트 결과"

orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 \
  --text "[worker_done] writer 완료 — 고도화 3차 SPEC 반영. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[질문] writer: <질문>" --enter`
