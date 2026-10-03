---
type: work
id: WORK-009
title: "운영 고도화 2차 — AX 초안 저장 · 채팅 단추 상태 · 업무 날짜 넷"
status: done
product: strong-hajin
work_type: improvement
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 100
created_at: 2026-10-02
updated_at: 2026-10-03
tags:
  - product/strong-hajin
  - doc/work
  - status/done
links:
  baselines: []
  decisions: []
  specs:
    - "[[spec-001-work-management|SPEC-001]]"
    - "[[spec-002-action-item-review|SPEC-002]]"
    - "[[spec-003-task-lifecycle-v2|SPEC-003]]"
    - "[[spec-007-task-detail|SPEC-007]]"
  works:
    - "[[work-008-polish|WORK-008]]"
  releases: []
  related:
    - "[[runbook-002-production-deploy|RUNBOOK-002]]"
sources:
  - orchestration/work/strong-hajin-polish2/_RESUME.md
  - orchestration/work/strong-hajin-polish2/be-survey-report.md
  - orchestration/work/strong-hajin-polish2/fe-survey-report.md
---

# 운영 고도화 2차 — AX 초안 저장 · 채팅 단추 상태 · 업무 날짜 넷

2026-10-02 운영(`https://ax.medisolveai.xyz`)을 쓰며 사용자가 낸 요청 다섯(E2E-1~5)을 한 판으로 묶는다.
요청 하나하나가 **사용자와 닫은 계약**이다(`_RESUME.md` §2) — 범위를 넓히지 않는다.

> **SPEC 이 먼저 반영됐다**(Meta). 계약 문장이 이 WP 와 SPEC 사이에서 다르면 **SPEC 이 맞다** — 워커는 코디에게 알린다.
>
> 1 파일 = 1 work. 이 판은 **네 페이지**(Phase 1 BE · 2a FE · 2b FE · 3 BE — E2E-6 은 사용자 E2E 중 추가)로 나뉜다. 2b 는 서버와 파일이 겹치지 않아 Phase 1 과 나란히, 2a 는 Phase 1 커밋 + 스택 재시작 뒤.
> 페이지마다 발주 → 구현 → 검수(reviewer) → 재수정 → 커밋. 세 페이지가 끝나면 PR 하나 → main → 운영 반영(RUNBOOK-002 §1).
> 근거 줄 번호는 조사 시점(코드 `3d47a32`) 값이다. 워커는 **줄 번호가 아니라 심볼로 다시 찾는다.**

## Meta

- **SPEC (정본)** — 계약 본문은 SPEC 이 갖고, 이 WP 는 절로 가리킨다
  - SPEC-001 v0.5.0 — U-3 · U-6-a · U-7 · U-17(신설) · S-9 6·7 · §4 · §5 · §6 · OQ-Q·OQ-R(코디 닫음)
  - SPEC-002 v0.4.0 — §2.9([등록]·[수정]·수정 창 「저장」·저장 뒤·「채팅 서랍 안의 색」) · S-7 · §4 「초안 저장」 · §5 · §6
  - SPEC-003 v0.4.0 — §2.9 · §4 · Data Contract 「업무 날짜」·「날짜 채움」 · §6
  - SPEC-004 v0.3.2 — §5 거는 자리 넷째(완료의 마감일 채움) · OQ-405(코디 닫음: 훅 건다)
  - SPEC-007 v0.4.0 — §2.2 사실 줄 「날짜 넷」·「출처 줄」 간격 · §3 S-1 · §6
  - 검수: `review-spec-report.md`(FAIL→fix1) · `review-spec2-report.md`(WARN 3 → 코디 처리: 시퀀스 문구 형식 · OQ-Q AC · 변경 없는 저장 = 성공)
- Covers: E2E-1 · E2E-2 · E2E-3 · E2E-4 · E2E-5 · E2E-6 (`_RESUME.md` §1·§2)
- 조사: `be-survey-report.md` · `fe-survey-report.md`
- 코드 워크트리: `Strong_hajin/strong-hajin-polish2` (branch `kknaksss/strong-hajin-polish2`, base `origin/main` `3d47a32`)
- External dependency: 없음. 새 외부 API·credential 없음. **스키마 변경 없음**(초안 회차는 기존 Submission·SubjectVersion 을 쓴다 — 아니면 코디에게 먼저 묻는다)
- 데스크톱 셸(`frontend/src-tauri/`)은 바꾸지 않는다 → medi-ax dmg 재빌드 없음

## 이 판의 원칙

| # | 원칙 | 근거 |
|---|---|---|
| P-1 | **AX 초안 = 「새 업무 추가」를 AI 가 채운 것**(1차 유지). 사람이 고치는 길도 새 업무 추가 모달 그대로 | WORK-008 · 사용자 |
| P-2 | **AI 는 제안하고 사람이 확정한다.** 체크리스트·내용은 AI 가 제안으로 채우되, ID·날짜는 근거가 있을 때만. 확정은 카드 「등록」 하나 | 사용자 2026-10-02 |
| P-3 | **채팅 서랍 안 사람 행동 = 검정, 파랑 = AI 진행만**(1차 유지). 모든 상태(hover·진행·disabled)에서. 서랍 밖은 앱 DS | WORK-008 · 사용자 |
| P-4 | **쓰는 곳을 전부 센다.** 이 문서의 파일:줄은 출발점이다. 같은 심볼·패턴을 grep 으로 전부 세고 시작한다 | 오케스트레이션 규칙 |
| P-5 | **디자인 시스템 안에서만.** 기존 부품·토큰. 시안이 없는 자리는 DS-gaps 에 적는다 | WORK-008 P-2 |

## Work Summary

| 페이지 | 요청 | 무엇 | 어디 |
|---|---|---|---|
| 1 | E2E-2 | AX 초안 「저장」 명령 — 확정 없이 회차 +1 · diff | BE |
| 1 | E2E-1 | AX 도구 설명·라우팅 정책 — 체크리스트·내용을 제안으로 채움 | BE |
| 1 | E2E-5 ② | 완료 때 비어 있는 마감일을 실제 종료일로 | BE |
| 2a | E2E-2 | 「수정」 모달 = 저장 모드 · 저장 뒤 카드 갱신 | FE |
| 2a | E2E-3 | 채팅 서랍 안 사람 행동 단추 — 모든 상태 검정 계열 | FE |
| 2b | E2E-4 · E2E-5 ①③ | 상세 메타 간격 · 날짜 넷 · 「마감일」 라벨 · `2026/10/06` 형식 통일 | FE |
| 3 | E2E-6 | AX 가 초안 전에 관련 회의·업무·자료를 찾아 내용·체크리스트의 근거로 | BE |

## Code Surface

- BE: `backend/src/ax_workspace/` · `backend/tests/` (Phase 1)
- FE: `frontend/src/` (테스트 포함). `frontend/src-tauri/` 는 건드리지 않는다 (Phase 2a·2b)

---

## Phase 1 — BE · 초안 저장 · AI 채움 · 완료 시 마감일

- **Status**: DONE — 코드 `6efdac1` · 검수 FAIL(F1 화면 title 「기한」)→fix1→재검수 WARN(W5 자료 ID 순서)→fix2 · 실물: AX 초안 체크리스트 5·내용 채움, save_draft 회차 2·변경 없음·낡음 422·등록=2회차 값, 완료 시 마감일=오늘
- **무엇이 끝나야 시작하나**: SPEC 반영·검수
- **워커**: backend

### 1-1. E2E-2 AX 초안 「저장」 명령 (신규)

- **지금** (`be-survey §2`): AX 초안(`ax.task.create_self`·`ax.work_request.create`)이 받는 명령은 `confirm`·`reject`(+호환 `approve`)뿐(`modules/actions/policy.py:114-128`). 회차 증가·diff 기록은 `confirm` 안에서만, 확정·업무 생성과 같은 transaction. 채팅 뷰·판단 대기는 매번 최신 Submission 스냅샷을 읽는다(메시지에 박힌 스냅샷 없음). 실시간 이벤트 없음
- **계약**:
  - [ ] 두 kind 에 **확정하지 않는 저장 명령**을 더한다(이름은 기존 명령 명명 규칙을 따른다 — 기존 `revise`(업무 요청 판단, `action_center.py:225, 261`)와 겹치는지 먼저 보고 재사용 가능하면 쓴다). 입력 = `{expected_version, base_submission_version, draft, attachment_draft_ids?}` — confirm+draft 와 같은 모양
  - [ ] 저장하면 초안은 **pending 그대로**, **회차 +1**, 사람이 고친 값의 **diff 기록** — confirm+draft 가 지금 남기는 것과 같은 기록을 같은 방식으로. 검증(정규화·필수값)은 confirm+draft 와 같다(P-1)
  - [ ] 저장 뒤 `GET /api/action-items` 와 대화 응답의 `edit_contract.values`·`base_submission_version`·「초안 · N회차」 표시 원천이 **새 회차 값**을 준다
  - [ ] 저장 뒤 카드 「등록」 = 그 최신 회차를 draft 없이 confirm → 그 값으로 업무가 생긴다(회차가 또 늘지 않는다)
  - [ ] confirm+draft 경로(지금)는 **지우지 않는다** — 다른 카드(`ActionTaskCard`·`ActionMeetingCard`)가 쓴다. 두 kind 의 FE 는 2a 에서 저장 명령으로 바꾼다
  - [ ] 낡은 `expected_version`/`base_submission_version` 이면 지금 confirm 과 같은 충돌 오류(`ACTION_VERSION_STALE`)
  - [ ] 고친 값이 하나도 없으면 **회차가 오르지 않고 성공**으로 같은 회차를 돌려준다(SPEC-002 §4 · §6)
  - [ ] 저장은 **effect 가 없다** — 업무·요청 원장이 바뀌지 않고 그 항목의 회차·차이만 쌓인다. 상태는 확인 대기(`awaiting_review`) 그대로
  - [ ] 실시간 이벤트는 만들지 않는다
  - [ ] 정책(`policy.py`)·명령 목록·편집 계약(`ActionPresenter._edit_contract`)·운영 대장(operation inventory)에 새 명령이 실린다 — drift 는 **실패 diff 의 그 항목만** 패치
- **SPEC**: SPEC-002 §2.9 · S-7 · §4 「초안 저장」 · §5 · §6 · SPEC-001 S-9 6 · OQ-R(서버 confirm+draft 유지)

### 1-2. E2E-1 AI 가 체크리스트·내용을 제안으로 채운다

- **지금** (`be-survey §1-2`): 서버는 체크리스트를 어디서도 버리지 않는다. 도구 설명이 「Fill every field the conversation gives you or that lookup confirmed … leave a value empty rather than inventing one」(`modules/ax_execution/tool_catalog.py:546` `task_create_self`, `:648` `work_request_create`)이고 라우팅 정책(`platform/codex_cli.py:464-466`)은 링크만 다룬다. 체크리스트·내용을 제안하라는 문장 0건
- **계약**:
  - [ ] 두 도구 설명과 업무 생성 라우팅 정책이 말하게 한다: **체크리스트(첫 단계들, 순서대로)와 업무 내용(description)은 대화 주제로부터 제안해 채운다** — 사람이 카드에서 검토·수정하는 초안이다
  - [ ] **ID(프로젝트·업무·사람)·날짜는 지금처럼** 대화·조회가 준 것만. 「지어내지 않는다」 문장은 ID·날짜에 한정되게 고친다
  - [ ] 「…는 비워 두었으니 승인 카드에서 보완」 같은 답변이 체크리스트·내용에 대해서는 나오지 않게 — 답변 지침도 같은 기준
  - [ ] Claude 어댑터가 같은 정책을 쓰는지 단언하는 테스트(`tests/unit/test_ax_work_lookup_policy.py`)를 새 문장에 맞춘다
  - [ ] 도구 설명을 쓰는 곳(카탈로그 · MCP 등록 · 정책 6절 · 테스트 단언)을 **전부** 센다
- **SPEC**: SPEC-001 S-9 7 · §5 · §6
- **검증**: 단위 테스트(도구 설명·정책 문장 단언) · 코디가 로컬 스택에서 「…업무 만들어 줘」 한 번 → 초안에 체크리스트·내용이 채워짐(실물 1회, `feedback_real_e2e`) — 로컬 codex 인증은 운영 것을 쓰지 않는다

### 1-3. E2E-5 ② 완료 때 비어 있는 마감일 = 실제 종료일

- **지금** (`be-survey §3-1`): 시작 전이 때 비어 있는 `start_date` 를 오늘로 채운다(`modules/work/lifecycle.py:165-171`, `application.py:2068`). 마감일은 그런 동작이 없다. `completed_at` 이 찍히는 곳 = 직접 완료(`application.py:2077-2078`) · 완료 보고 제출(`:1899-1901`)
- **계약**:
  - [ ] `completed_at` 이 찍히는 순간 `due_date` 가 비어 있으면 **그 날(Asia/Seoul)** 로 채운다 — 직접 완료 · 완료 보고 제출 둘 다. 시작일 채움과 같은 규칙·같은 「오늘」 함수
  - [ ] 보완 요청·재개로 `completed_at` 을 지워도 채운 `due_date` 는 **되돌리지 않는다**
  - [ ] 날짜가 바뀌면 지금 걸려 있는 후속 처리(`_schedule_release_for`, 버전 스냅샷 diff 대상, `task.updated`/`task.state_changed` 이력)가 시작일 채움과 같은 수준으로 돈다 — 시작 전이 경로가 하는 것을 대조해 맞춘다
  - [ ] `completed_at` 을 찍는 곳을 **전부** 센다(조사 4곳: `:1901` `:1935` `:2078` `:2146` 중 찍는 곳)
  - [ ] 채움 자리에도 배정 검증 훅(기간 밖 시간 배정 닫기)을 건다 — SPEC-004 §5 거는 자리 넷째 · OQ-405(코디: 건다)
- **SPEC**: SPEC-003 Data Contract 「날짜 채움」 · §6 · SPEC-004 §5
- **검증**: 마감일 없는 업무 직접 완료 → `due_date` = 오늘 · 요청 업무 완료 보고 → 같음 · 마감일 있던 업무는 그대로 · 보완 요청 뒤 유지

### Phase 1 검증

- [ ] `make test-unit` · `make test-contract` · `tests/architecture` · operation inventory drift(diff 항목만)
- [ ] 코디 `make verify` · 격리 PostgreSQL `make test-postgres` · 커밋 뒤 로컬 스택 재시작

---

## Phase 2a — FE · 수정 모달 저장 · 채팅 단추 상태

- **Status**: DONE — 2a-2 먼저(서버 무관) `d1bb87d` 검수 WARN→fix1 · 2a-1 `4789647` 검수 WARN 4→fix1(낡은 저장 재조회·저장 중 닫힘 잠금·갱신 실패 분리·실배선 테스트) · 코디 화면 확인(카드·창 「저장」·2회차·「등록 중…」 회색)
- **무엇이 끝나야 시작하나**: Phase 1 커밋 + **로컬 스택 재시작**
- **워커**: frontend

### 2a-1. E2E-2 「수정」 모달 = 저장

- **지금** (`fe-survey §2`): 카드 「수정」(`AxDraftCard.tsx:388-401`) → `createPortal(<CreateWorkModal axDraft=… initial=…/>, document.body)`(`:409-453`). 모드는 `axDraft` prop 하나(`WorkModals.tsx:4427-4448`). 하단 주 단추 `Button variant="solid" tone="primary"` 「등록」/「등록 중…」(`:5256-5260`) → `axDraft.onSubmit` → confirm+draft(`AxDraftCard.tsx:424-427`). 모달은 body 포털이라 채팅 검정 규칙 밖 = DS 파랑
- **계약**:
  - [ ] `axDraft` 모드의 하단 주 단추 문구 = **「저장」/「저장 중…」**. 색은 **앱 DS 파랑 그대로**(사용자 「파랑으로 가자」). 왼쪽 「닫기」 그대로
  - [ ] 「저장」 = Phase 1 의 저장 명령(confirm 아님). 성공하면 모달을 닫고, **카드는 서버의 새 회차 값**(제목·날짜·체크리스트·연결·「초안 · N회차」)을 보인다 — 채팅은 대화 재조회, 홈·칩(`AxDraftModal`)은 판단 대기 재조회. 카드는 pending 그대로 [거절][수정][등록]
  - [ ] 저장 실패 문구는 모달 안(`axDraft.error` 자리)에 낸다. 충돌(낡은 버전)이면 지금 confirm 충돌과 같은 문구
  - [ ] 카드 「등록」 = 최신 회차 confirm(draft 없음, 지금 `AxDraftCard.tsx:403`). 저장 뒤 등록하면 고친 값으로 업무가 생긴다
  - [ ] 닫기 = 버림(지금 그대로). 자료 탭은 지금처럼 고르는 즉시 판단 항목 자료 초안으로 올라간다 — 저장/등록 때 `attachment_draft_ids` 가 실린다
  - [ ] 홈 판단 대기·내 업무 「AX 제안」 칩에서 연 `AxDraftModal` 의 「수정」도 같은 저장 동작(`AxDraftCard.tsx:479-514` 경로) — 저장 뒤 그 화면 목록이 새 회차를 보인다
  - [ ] `CreateWorkModal` 을 미리 채운 값으로 여는 다른 자리(하위 업무·재요청·회의 승격·새 업무 — `fe-survey §2-4` 7자리)의 단추·제출은 **바꾸지 않는다** — 전부 세어 확인
- **SPEC**: SPEC-002 §2.9 · S-7 · §6

### 2a-2. E2E-3 채팅 서랍 안 사람 행동 단추 — 모든 상태

- **지금** (`fe-survey §3`): 검정 덮어쓰기 `ax.css:665-673` 은 `.scax-drawer--chat .scax-button--solid-primary:not(:disabled)` 뿐. 진행 중 disabled + 포인터 위 → `components.css:10` `.scax-button:disabled`(0,2,0) 와 `:14` `.scax-button--solid-primary:hover`(0,2,0, `:not(:disabled)` 없음)가 동률, 뒤의 hover 가 이겨 **`accent-strong` 파랑**. `.action-task-card` 계열만 `ax.css:546`(0,4,0)이 회색으로 잡는다
- **계약**:
  - [ ] 채팅 서랍(`.scax-drawer--chat`) 안 solid-primary 단추의 **진행 중·disabled 상태가 hover 와 겹쳐도 파랑이 되지 않는다** — disabled 는 DS disabled 회색(`components.css:10` 값) 또는 검정 계열 중 `.action-task-card` 의 기존 처리(`ax.css:546`)와 **같은 모양**으로 통일
  - [ ] 같은 구조 **전부**: `AxDraftCard` 등록 · `ActionProgressBatchCard`(반영 중…/저장 중…) · `CommandConfirmationForm` 주 단추 · `ActionPreview` 결과 카드 명령 · 그 밖에 grep 으로 나오는 채팅 안 solid-primary — 표(`fe-survey §3-2`)를 출발점으로 다시 센다
  - [ ] outlined-neutral·text-neutral 의 disabled+hover 가 활성처럼 보이는 것(`components.css:18`, `:25`)도 **채팅 서랍 안에서는** 같은 방식으로 disabled 모양 유지
  - [ ] 「근거 N개 더 보기」(`MessageList.tsx:737`, `.scax-sources__more` `ax.css:238` — `accent` 파랑 글자)는 사람 행동 → **검정 계열 텍스트 단추**로(코디 기본값 — P-3)
  - [ ] 범위는 **채팅 서랍 안만**. DS 원본 규칙(`components.css`)은 고치지 않는다 — 앱 전체 동작이 바뀌기 때문. DS 의 hover 에 `:not(:disabled)` 가 없는 것은 DS-gaps 에 적는다
- **SPEC**: SPEC-002 §2.9 「채팅 서랍 안의 색」 · §6
- **검증**: 상태별 계산 스타일 테스트(가능한 범위) · 코디가 로컬에서 AX 카드 등록 누른 채 포인터를 단추 위에 둔 화면 확인

### Phase 2a 검증

- [ ] `make frontend-test`(직렬 `npx vitest run --no-file-parallelism`) · `npx tsc --noEmit` · `make frontend-build`. 날짜 의존 실패 5건은 기준선
- [ ] 코디: 데모 DB(`ax_demo_*`)로 AX 초안 → 수정 → 저장 → 카드에 새 값·2회차 → 등록 → 업무 생성, 홈·칩에서도 한 번

---

## Phase 2b — FE · 업무 상세 날짜 넷 · 메타 간격 · 「마감일」 통일

- **Status**: DONE — 코드 `c64cddf` · 검수 WARN 5→fix1(W2 범위 밖) · 코디 화면 확인(완료 업무 날짜 넷)
- **무엇이 끝나야 시작하나**: SPEC 반영·검수 (서버 변경 불필요 — `_view` 가 `started_at`·`completed_at` 을 이미 준다, `be-survey §3-4`). Phase 1 과 나란히
- **워커**: frontend

### 2b-1. E2E-4 · E2E-5 ① 상세 메타

- **지금** (`fe-survey §4-1`, `WorkModals.tsx:1958-2035`):

```
div.scax-td
└ div.meta[aria-label="업무 메타"]                       task-detail.css:96-99  flex · gap 12 · padding 0 0 14px · border-bottom
  └ div.meta__left                                       :111
    ├ (metaEditing) input.meta__title-input
    ├ div.meta__facts                                    :101-104 flex · wrap · gap 6px 14px · 12px
    │  ├ <span>담당 <b>{ownerName}</b></span>
    │  ├ <span>기한 <b>{formatDate(due_date)}</b></span>      !metaEditing && due_date
    │  ├ <span>시작 <b>{formatDate(start_date)}</b></span>    !metaEditing && start_date
    │  ├ <span>결재 <b>…</b></span>
    │  └ <span>참조 <b>…</b></span>
    ├ p.origin-chip   (task.origin)                      screens-a.css:437 margin 0 0 4px · 12.5px
    │  ├ Badge tone="outline" 「AX 제안에서 생성됨」 등
    │  └ Button variant="inline" {source.title} | small.t-meta
    └ (metaEditing) div.meta__edit — DateField 「시작일」 · DateField 「기한」
```

- **계약**:
  - [ ] `.meta__facts` 의 날짜 칸을 **순서대로 넷**: **시작 예정일**(`start_date`) · **실제 시작일**(`started_at`) · **실제 종료일**(`completed_at`) · **마감일**(`due_date`). 그 앞 「담당」, 뒤 「결재」·「참조」는 지금 자리
  - [ ] 값이 없는 칸은 **서지 않는다**(SPEC-007 §2.2) — 시작 전 업무엔 실제 시작일이, 끝나지 않은 업무엔 실제 종료일이 없다
  - [ ] `started_at`·`completed_at` 은 시각이지만 **날짜(Asia/Seoul)** 로 `2026/10/06` 형식. UTC 로 잘라 하루 밀리지 않는다(지금 「처리일」이 UTC 자름 — `fe-survey §0`)
  - [ ] 편집(「편집」→ `.meta__edit`)은 지금처럼 시작 예정일·마감일 둘. DateField 라벨을 **「시작 예정일」·「마감일」** 로
  - [ ] **E2E-4**: `.meta__facts` 와 `p.origin-chip` 사이에 DS 간격 토큰으로 띄운다(`.origin-chip` 은 전역 규칙 — 이 자리만 `.scax-td` 스코프로). 글자 크기 12 / 12.5 차이도 같은 줄 계층으로 맞춘다. 링크 문구(원 AX 초안 제목)는 그대로
- **SPEC**: SPEC-007 §2.2 「날짜 넷」·「출처 줄」 · §3 S-1 · §6

### 2b-2. E2E-5 ③ 「마감일」 라벨 · `2026/10/06` 형식 통일

- **지금** (`fe-survey §5`): 같은 `due_date` 가 화면마다 기한·마감일·…마감·희망 기한, 형식은 `2026/10/06`·`2026.10.06`·`2026-10-06`·`10월 6일` 이 섞여 있다. 포맷터가 여러 벌
- **계약**:
  - [ ] `due_date` 를 보이는 **화면 라벨 전부**를 「마감일」로 — 「기한 없음」→「마감일 없음」, **「기한 지남」 칩 · 「기한 초과」 배지 포함**(OQ-Q ①). 각 자리를 표로 세어 보고. `labels.ts` 키를 쓰는 곳 + 하드코딩 문자열 전부 grep
  - [ ] **DateField 입력 표기**도 `2026/10/06`(OQ-Q ③) · 캘린더 거절 문구의 날짜도 같은 형식(OQ-Q ⑤)
  - [ ] **유지**: 만들기 창·캘린더의 「시작일」 라벨(OQ-Q ②) · 캘린더 날 머리 「10월 6일 월요일」(OQ-Q ④)
  - [ ] 업무 날짜(`start_date`·`due_date`·실제 두 값)의 **날짜 표시 형식을 `2026/10/06` 하나로** — 포맷터를 하나로 모으고 화면들이 그것을 쓴다. 캘린더 달력 머리·간트 축 같은 **축 눈금**(`10월`, `2` 등)은 날짜 값 표시가 아니므로 바꾸지 않는다 — 판단이 갈리는 자리는 표에 적어 보고
  - [ ] 회의 시각 등 **업무 날짜가 아닌** 표시는 바꾸지 않는다
  - [ ] 「시작」 라벨이 시작 예정일을 뜻하는 자리는 그대로 두되(목록·캘린더·간트 — 사용자 「이게 맞겠다」), 상세만 넷으로
  - [ ] 테스트의 문자열 단언을 함께 고친다. 날짜 의존 실패 5건 기준선은 그대로 분리 보고
- **SPEC**: SPEC-001 U-17 · §6 · OQ-Q(코디 닫음) · SPEC-003 · SPEC-007

### Phase 2b 검증

- [ ] `make frontend-test`(직렬) · `npx tsc --noEmit` · `make frontend-build`
- [ ] 코디: 데모 DB 로 상세(시작 전·진행 중·완료 업무 각 하나) · 내 업무 목록 · 캘린더 · 프로젝트 화면의 라벨·형식 확인

---

## Phase 3 — BE · AX 초안 전 회의·업무·자료 탐색 (E2E-6)

- **Status**: DONE — 코드 `1d4cd1f` · 검수 WARN 4(날짜 기준 이중·호출 상한·예외 꼬리 범위·빈 단언)→fix1 · 실물 2회: 관련 기록 있는 주제 45초(검색 도구별 1회·상세 1·연결 채움·사람·날짜 비움) / 없는 주제 25초(「관련 회의·기존 업무·자료를 찾지 못해 일반 단계로 제안」)
- **무엇이 끝나야 시작하나**: Phase 1 커밋(`6efdac1`) · E2E-6 SPEC 반영
- **워커**: backend
- **요청**: 사용자 2026-10-02 로컬 E2E — 「회의 내용이나 기존 업무 내용들은 안 살펴봐? 그래프 서치 할 때?」 → 「1번만」(사람·날짜 채움은 안 함)
- **지금** (`be-survey2-report.md`): 실물 업무 생성 턴의 도구 호출이 `task_list`·`list_projects`·`task_create_self` 셋. 업무 생성 문장(`tool_catalog.py:546`·`:648`, `codex_cli.py:461-466`)이 이름을 드는 조회는 `list_projects`·`graph_search`·`graph_neighbors`·`task_list` 넷뿐이고 회의(`meeting_get`·`my_meeting_list`)·자료(`material_search`)·업무 상세(`task_get`)는 0. 제동 문장(`codex_cli.py:372-374` graph 안 걷기 · `:381` 일괄 상세 금지 · `:385`/`:395` 회의·자료는 질문일 때만 · `:408`·`tool_catalog.py:568` task_list 명시적일 때만)이 업무 생성 턴에도 실린다. `graph_search` 는 제목 부분 일치(`modules/work/search.py:25-27`). 본문을 주는 도구는 이미 있다
- **계약** (`_RESUME.md` §2 「E2E-6 계약」 ①~⑧):
  - [ ] 업무 생성·요청 초안 전에 **주제 핵심어(짧게)** 로 관련 회의·기존 업무·자료를 찾는다 — `graph_search`·회의 목록·`material_search`. 그중 가장 관련 높은 것만 **상세 최대 3건**(`meeting_get` 회의록·할 일 / `task_get` 내용·체크리스트)
  - [ ] 찾은 내용을 **업무 내용·체크리스트의 근거**로 쓰고, 답변에 출처(회의·업무 이름)를 든다 — 답변 참조로 묶인다(기존 `task`·`meeting`·`material` 종류). 상세 조회가 근거 기억(`_remember`)에 실리는지 확인하고, 빠졌으면 같은 방식으로
  - [ ] 연결(프로젝트·참고·선행·상위)은 지금처럼 한 후보 확정일 때만
  - [ ] 관련 기록을 못 찾으면 일반 제안 + 「관련 회의·업무를 찾지 못해 일반 단계로 제안했다」
  - [ ] **사람·날짜(참조자·결재자·마감일)는 채우지 않는다** — Phase 1 의 「ID·날짜는 대화·조회 근거만」 그대로, 회의 할 일의 담당자·마감 후보를 옮기지 않는다
  - [ ] 제동 문장은 **업무 생성·요청 턴만 예외** — 다른 질문 턴의 동작은 그대로
  - [ ] 검색 엔진·타임아웃(codex 90s)·reasoning 은 바꾸지 않는다. 초안 Submission Evidence 확장 없음
  - [ ] 도구 설명·정책 문장을 쓰는 곳(카탈로그·정책 6절·Claude 어댑터·inventory description·단언 테스트)을 **전부** 센다
- **SPEC**: SPEC-001 S-9 7 · §5 · §6 (E2E-6 반영분)
- **검증**: 정책·도구 설명 단언 테스트 · `make test-unit` · `make test-contract` · inventory drift(그 항목만) · **코디 실물 1회**: 데모 DB 의 회의가 있는 주제로 업무 생성 → 도구 호출에 회의/업무 상세 조회 · 체크리스트가 그 내용을 반영 · 답변 출처 · 90초 안에 끝남

---

## Pre-deploy Check

- [ ] 세 페이지 검수 처리 · 코디 `make verify` 통과 · 사용자 E2E 목록 전달
- [ ] PR 하나(스쿼시) → main 머지
- [ ] 운영 반영: arm64 back·front 이미지 → infra `image.tag` PR → Argo 수동 sync (RUNBOOK-002 §1)
- [ ] 운영에서 `/health` · 로그인 · AX 초안 저장→등록까지 확인

## Rollback

- `values-prod.yaml` 태그를 직전 값(`3d47a32-arm64`)으로 되돌려 머지 → 수동 sync. 스키마 변경이 없으므로 데이터 되돌림은 없다. 단 Phase 1-3 으로 채워진 `due_date` 는 남는다(되돌리지 않는다)

## 반영

- 2026-10-03 운영 반영: kknaks/Strong_hajin#10 squash `d1b5137` → 이미지 `d1b5137-arm64`(back·front) → MediSolveAIDev/k8s_infra_mac#8(태그 한 줄) → Argo 수동 sync Synced/Healthy 8/8. web 200 · /health production · providers 데모 계정 없음 · back·worker 로그 오류 0

## Done Criteria

- 다섯 요청의 계약 체크가 모두 채워졌고 화면 확인 증거가 있다
- 운영에 반영됐다

## Open Issues

| ID | 무엇 | 다음 |
|---|---|---|
| OQ-901 | DS 의 solid/outlined/text hover 에 `:not(:disabled)` 없음(앱 전체 disabled+hover 가 활성처럼 보임) — 이번엔 채팅 서랍 안만 | DS-gaps · 다음 판 |

## Related

- `_RESUME.md` — 요청 원문과 결정 이력
- RUNBOOK-002 — 운영 반영 절차
