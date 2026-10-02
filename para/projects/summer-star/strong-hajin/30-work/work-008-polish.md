---
type: work
id: WORK-008
title: "운영 고도화 1차 — 화면 손질 · 깜박임 · AX 제안 카드"
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
created_at: 2026-10-01
updated_at: 2026-10-02
tags:
  - product/strong-hajin
  - doc/work
  - status/done
links:
  baselines: []
  decisions:
    - "[[decision-007-production-deploy|DEC-007]]"
  specs:
    - "[[spec-001-work-management|SPEC-001]]"
    - "[[spec-002-action-item-review|SPEC-002]]"
    - "[[spec-005-projects|SPEC-005]]"
    - "[[spec-007-task-detail|SPEC-007]]"
  works: []
  releases: []
  related:
    - "[[runbook-002-production-deploy|RUNBOOK-002]]"
sources:
  - orchestration/work/strong-hajin-polish/_RESUME.md
  - orchestration/work/strong-hajin-polish/fe-survey-report.md
  - orchestration/work/strong-hajin-polish/be-survey-report.md
---

# 운영 고도화 1차 — 화면 손질 · 깜박임 · AX 제안 카드

2026-10-01 운영(`https://ax.medisolveai.xyz`)을 쓰며 사용자가 낸 수정 요청 여덟 건을 한 판으로 묶는다.
요청 하나하나가 **사용자와 닫은 계약**이다 — 범위를 넓히지 않는다.

> **SPEC 이 먼저 반영됐다**(Meta). 계약 문장이 이 WP 와 SPEC 사이에서 다르면 **SPEC 이 맞다** — 워커는 코디에게 알린다.
>
> 1 파일 = 1 work. 이 판은 **세 페이지**(Phase 1 · 2 · 3)로 나뉘고 **순서대로** 발주한다.
> 한 페이지가 검증·화면 확인을 마쳐야 다음 페이지를 연다. 세 페이지가 끝나면 PR 하나 → main → 운영 반영(RUNBOOK-002 §1).
> 근거 줄 번호는 조사 시점(코드 `015bed2`) 값이다. 워커는 **줄 번호가 아니라 심볼로 다시 찾는다.**

## Meta

- **SPEC (정본, 2026-10-01 반영·검수 PASS/WARN 처리)** — 계약 본문은 SPEC 이 갖고, 이 WP 는 절로 가리킨다
  - SPEC-001 v0.4.0 — U-2(「AX 제안 N」 칩) · U-6-a(담당자 초깃값·참조자 후보) · U-16(내 업무 타임라인) · S-9 · §4 Validation · §6
  - SPEC-002 v0.3.0 — §2.4(AX 초안이 보이는 자리) · §2.9(AX 업무 초안 카드) · S-7 · §4 · §6
  - SPEC-005 v0.3.0 — §2.4(간트 기본 범위 — 범위 규칙 정본) · §6 L-53~L-56
  - SPEC-007 v0.3.0 — §2.9(담당자 변경 작은 모달) · §6
  - SPEC-003 v0.3.2 — §4 `reassign` reason 선택
  - 검수: `orchestration/work/strong-hajin-polish/review-spec-report.md`(FAIL→fix1) · `review-spec2-report.md`(WARN→코디 처리)
- Covers: 요청 B-02 · F-01 · F-02 · F-03 · D-01 · B-01 · D-02 · A-01 (`_RESUME.md` §1)
- 조사: `fe-survey-report.md`(프론트 8건) · `be-survey-report.md`(A-01 · B-01 · B-02)
- 코드 워크트리: `Strong_hajin/strong-hajin-polish` (branch `kknaksss/strong-hajin-polish`, base `origin/main`)
- External dependency: 없음. 새 외부 API·credential 없음
- 데스크톱 셸(`frontend/src-tauri/`)은 바꾸지 않는다 → medi-ax dmg 재빌드 없음(RUNBOOK-002 §3). 바뀌게 되면 코디에게 먼저 묻는다

## 이 판의 원칙

| # | 원칙 | 근거 |
|---|---|---|
| P-1 | **AX 업무 생성 = 「새 업무 추가」를 AI 추천으로 채운 것.** 필드·필수값·검증·저장 규칙은 새 업무 추가와 같다. 다른 것은 채우는 주체(사람/AI)뿐 | 사용자 2026-10-01 |
| P-2 | **디자인 시스템 안에서만.** 기존 DS 부품·토큰을 쓴다. 혼자 새 모양을 만들지 않는다. 시안이 없는 자리는 DS-gaps 에 적는다 | 사용자 2026-10-01 (F-01) |
| P-3 | **쓰는 곳을 전부 센다.** 이 문서의 파일:줄은 출발점이다. 같은 심볼·패턴을 grep 으로 전부 세고 시작한다 | 오케스트레이션 규칙 |

## Work Summary

| 페이지 | 요청 | 무엇 | 어디 |
|---|---|---|---|
| 1 | B-02 | 새 업무 추가 › 참조자 후보에서 한 명이 빠지는 버그 | FE |
| 1 | F-01 | 업무 상세 › 담당자 변경 → 작은 모달 | FE |
| 1 | F-02 | AX 대화 › 「대화 검색」 입력 DS 스타일(웹·앱 동일) | FE |
| 1 | F-03 | 프로젝트 간트 기본 범위 W-1 ~ W+3 | FE |
| 1 | D-01 | 내 업무 › 타임라인 여백·범위·이동 | FE |
| 2 | B-01 | 탭 이동 때 깜박임 — 받아 둔 데이터를 먼저 보여 준다 | FE |
| 3a | D-02 · A-01 | AX 초안 = 새 업무 추가 필드 객체 · 기한 필수 제거 · 목록 응답 보강 | BE |
| 3b | D-02 · A-01 | AX 요약 카드(좌우 넘김) · 「수정」= 새 업무 추가 모달 · 「AX 제안」 칩 | FE |
| 4 | B-03 | 운영 회의 요약(종료 합성) 실패 — resume 실패 시 콜드스타트 | BE |
| 6 | B-04 | ~~핫픽스 — 대화·회의 배치 세션 잃으면 새 세션으로 이어 감~~ 취소 | BE |
| 5 | E2E-12 | AX 업무 생성이 프로젝트·업무를 찾아 채운다 · 프로젝트 근거 턴 실패 | BE |

## Code Surface

### FE allowed paths
- `frontend/src/` (테스트 포함). `frontend/src-tauri/` 는 건드리지 않는다

### BE allowed paths (Phase 3a)
- `backend/src/ax_workspace/` · `backend/tests/`

---

## Phase 1 — FE · 화면 손질 다섯

- **Status**: DONE
- **무엇이 끝나야 시작하나**: 없음. 첫 페이지다
- **워커**: frontend

### 1-1. B-02 참조자 후보 누락 (버그)

- **원인**: 「새 업무 추가」의 담당자 값이 열 때 담당 후보 첫 사람으로 미리 채워진다
  (`WorkModals.tsx:4387` `useState(initial ? … : assigneeCandidates[0]?.id ?? "")`).
  내 업무 갈래에는 담당자 칸이 없는데도 이 값이 참조자 칩을 거른다(`:5227-5228`). 서버는 본인만 빼고 전원을 준다(`organization_access.py:876-889`)
- **계약**:
  - [ ] 내 업무 갈래의 담당자는 **로그인 정보(본인)**다. 숨은 담당 후보 값을 두지 않는다
  - [ ] 요청 갈래의 담당자는 **처음에 빈칸**이다. 아무도 미리 고르지 않는다(필수 검사는 기존 `:4648` 그대로)
  - [ ] 처음 열면 **두 갈래 모두** 참조자 후보 전원(본인 제외)이 뜬다
  - [ ] 요청 갈래에서 담당자를 고르면 **그 사람만** 참조자 후보에서 동적으로 빠진다. 담당자를 바꾸면 이전 사람은 돌아온다
  - [ ] 이미 참조자로 체크한 사람을 담당자로 고르면 그 참조자 체크도 풀린다
  - [ ] 미리 채운 값(`initial`)으로 여는 자리(하위 업무·회의 승격·재요청)의 동작은 바꾸지 않는다 — 전부 세어 확인한다
- **범위 밖**: 결재자 목록이 담당자를 거르지 않는 것(`:4966-4969`)
- **SPEC**: SPEC-001 U-6-a · §6 만들기 창 AC

### 1-2. F-01 담당자 변경 → 작은 모달

- **지금**: `TaskDetailDrawer` 안의 인라인 폼 `.handover > .form-stack.link-draft`(`WorkModals.tsx:2324-2366`). 제출 `reassignTask` → `POST /api/tasks/{id}/reassign`
- **계약**:
  - [ ] 「담당자 변경」을 누르면 **기존 `Modal size="sm"`** 을 업무 상세 위에 겹쳐 띄운다. 모달-위-모달은 기존 선례(형제 렌더 + `useEscape` 스택)를 그대로 쓴다
  - [ ] 내용은 지금 폼 그대로: 대상 담당자(빈칸 시작) · 사유(**선택** — SPEC-007 OQ-710 닫힘) · 변경/취소
  - [ ] ESC·바깥 클릭은 작은 모달만 닫는다. 업무 상세는 남는다
  - [ ] 변경 성공 → 작은 모달을 닫고 **상세를 다시 읽어 서버 값대로** 보인다. `reassign` 은 담당 변경 **제안**이라(SPEC-003 §4) 기존 담당이 유지되고 「담당 변경 대기」로 설 수 있다. 실패 문구는 모달 안에 낸다
  - [ ] SPEC: **SPEC-007 §2.9 · §6**
  - [ ] **P-2** — DS 부품·토큰만. 새 모양 금지
- **범위 밖**: 같은 인라인 패턴인 「자료 링크 추가」

### 1-3. F-02 「대화 검색」 입력

- **원인**: 전역 입력 규칙(`styles/components.css:737`)이 `input[type="search"]` 를 셀렉터에서 뺐다. `.search-input-box`(`components.css:487`)·`.scax-chat__search`(`ax.css:116`)에 테두리·반경·appearance 가 없다. 앱 유일의 search 입력(`ChatDrawer.tsx:258`)이 브라우저 기본 모양 — 웹은 2px inset·각진 모서리, Tauri(WebKit)는 얇은 네이티브 검색칸
- **계약**:
  - [ ] 다른 입력칸과 같은 DS 스타일(테두리·반경·높이·글자)을 받는다. DS 검색 부품이 있으면 그것을 쓴다
  - [ ] WebKit 기본 꾸밈(`appearance`·`::-webkit-search-*`)을 걷어 웹 = 앱
  - [ ] `type="search"` 와 검색칸 클래스를 쓰는 곳을 **전부** 세고, 같은 문제가 있는 자리는 함께 맞춘다
- **완료 조건**: 웹(Chrome) **과** Tauri 앱(`make tauri-local`) 스크린샷 둘

### 1-4. F-03 프로젝트 간트 기본 범위

- **지금**: `ganttAxis`(`features/project/projectModel.ts:237-248`)가 업무 `span_from` 최소 ~ `span_to` 최대만 그린다. 하루 34px·이름 열 200px 은 `GANTT` 상수(`:20-36`)
- **계약**:
  - [ ] 기본 범위 = 오늘 기준 **W-1 ~ W+3** — 월요일 시작 달력 주, 이번 주가 W0, 5주(오늘 10/01 이면 9/21 ~ 10/25)
  - [ ] 업무가 범위 밖이면 범위를 넓혀 **자르지 않는다**
  - [ ] 하루 34px 유지. 넘치면 가로 스크롤, **처음 열 때 오늘이 보이게** 스크롤
  - [ ] 업무 0건이면 지금처럼 간트를 숨긴다
  - [ ] 범위 밖 업무로 넓힐 때는 **주 경계**(시작날이 속한 주 월요일 ~ 끝날이 속한 주 일요일) — SPEC-005 OQ-608 닫힘
  - [ ] 범위 계산은 **기준 주를 인자로 받는 함수 하나** — 1-5 타임라인이 같은 함수를 쓴다
  - [ ] SPEC: **SPEC-005 §2.4(정본) · §6 L-53~L-56**

### 1-5. D-01 내 업무 › 타임라인

- **지금**: `TaskTimeline`(`features/work/WorkViews.tsx:387-482`) — 오늘-7일부터 14일 고정, 2주 스테퍼, 「오늘」 없음. 칩 바 아래 큰 여백(`.timeline.work-timeline` padding 등)으로 목록 보기와 시작 높이가 다르다
- **계약**:
  - [ ] 칩 바 아래 **시작 높이를 목록 보기와 맞춘다**
  - [ ] 범위는 **1-4 와 같은 규칙**(W-1 ~ W+3 · 오늘 보이게 스크롤 · 범위 밖 업무면 넓힘). 범위 계산은 두 화면이 **같은 함수**를 쓴다
  - [ ] ‹ › 는 5주 창을 **1주씩 민다**. 「범위 밖 업무면 넓힘」은 **오늘 기준 첫 화면에만** 적용(SPEC-001 OQ-P 닫힘). 「오늘」 버튼을 더한다
  - [ ] SPEC: **SPEC-001 U-16 · §6**
  - [ ] 막대·범례·업무명 열은 지금 DS 그대로

### Phase 1 검증

- [ ] `make frontend-test` · `npx tsc --noEmit` · `make frontend-build`
- [ ] 바뀐 동작마다 테스트 — 특히 B-02(두 갈래 × 담당자 선택 전후 참조자 목록), F-03·D-01 범위 계산(월요일 경계·범위 밖 업무)
- [ ] 코디가 로컬 스택에서 다섯 화면을 직접 확인하고 사용자에게 보인다(F-02 는 Tauri 포함)
- **완료 증거**: 코드 `9255028` · 검수 WARN→fix1 · 코디 화면 확인→fix2(타임라인 업무명 열 고정)

---

## Phase 2 — FE · 탭 이동 깜박임

- **Status**: DONE
- **무엇이 끝나야 시작하나**: Phase 1 화면 확인
- **워커**: frontend
- **원인**: 탭 전환이 `useState` surface + 조건부 렌더라 페이지·레일이 매번 언마운트된다(`App.tsx:75, 476-575`). `request()` 는 캐시 없는 fetch(`lib/api.ts:127-144`). 진입마다 상태가 `"loading"` 으로 돌아가 지연 없는 스켈레톤이 뜬다(`MyWorkPage.tsx:354`, `CalendarPage.tsx:158`). 내 업무는 진입 때 최대 9콜
- **계약**:
  - [ ] 한 번 받은 화면 데이터를 기억해 두고, 다시 들어가면 **이전 데이터를 즉시 보여 준 뒤 뒤에서 갱신**한다
  - [ ] 스켈레톤은 **데이터가 하나도 없는 첫 진입**에만 뜬다
  - [ ] 사이드 메뉴 화면 **전부**(홈·내 업무·캘린더·조직·프로젝트·보고·회의)를 세고 같은 규칙을 건다. 빠진 화면은 이유를 적는다
  - [ ] 쓰기(생성·변경) 뒤에는 그 화면 데이터가 갱신된다 — 옛 데이터가 남지 않는다
  - [ ] 권한(envelope) 판단은 갱신된 응답 기준이다
- **범위 밖**: 서버(N+1 · 요청마다 인증 재계산 · 캐시 헤더 — `be-survey-report.md` §2). 체감을 본 뒤 따로 정한다
- **검증**: `make frontend-test` · `npx tsc --noEmit` · 코디가 로컬에서 탭을 오가며 깜박임이 없는지 확인
- **완료 증거**: 코드 `1ef8db0` · 검수 FAIL(늦은 응답 누설)→세대 토큰 · 재검수 WARN→fix2

---

## Phase 3 — AX 제안 카드 (3a BE → 3b FE 직렬)

**지금**: AX 가 「업무 만들어 줘」를 받으면 `task_create_self`(`entrypoints/mcp.py:1977`)가 **초안**만 만든다
(`action_items` pending + 같은 id 의 `decision_items` kind `ax.task.create_self`). 업무(`TaskRecord`)는 「등록」(confirm) 때 처음 생긴다(`platform/actions.py:824-834`).
초안은 홈 판단 대기(`GET /api/action-items`)와 채팅에만 보이고, 만료가 없다. 채팅 카드(`features/action/ActionTaskCard.tsx:464`)는 제목·담당자만 보여 준다.
AX 경로에만 「기한 필수」 검사가 있다(`platform/action_center.py:596`, 2026-09-11 #3).

**대상 kind**: `ax.task.create_self`(업무 생성) · `ax.work_request.create`(업무 요청). 다른 AX 카드(회의실 예약 등)는 범위 밖.

### Phase 3a — BE · 초안 객체와 목록 응답

- **Status**: DONE
- **무엇이 끝나야 시작하나**: Phase 2 확인
- **워커**: backend
- **계약**:
  - [ ] **P-1** — 두 kind 의 초안 객체는 「새 업무 추가」 생성 명령과 **같은 필드·같은 필수값·같은 검증**이다. 필드 목록은 생성 명령(`modules/work/creation_commands.py`)이 정본이다 — 초안 정규화(`_normalize_ax_draft`)·스냅샷·편집 계약(`ActionPresenter._edit_contract`)이 그 필드를 **빠짐없이** 싣는지 전부 대조한다
  - [ ] AX 경로에만 있는 기한 필수 검사(`action_center.py:596`)를 **뺀다**. 필수는 새 업무 추가와 같다(제목, 요청이면 담당자)
  - [ ] confirm + `draft` 로 사람이 고친 값을 등록하는 경로는 지금 그대로다(회차 증가·diff 기록 유지)
  - [ ] 판단 대기 응답(`GET /api/action-items`)이 카드에 필요한 것을 싣는다: 초안 **필드 전체** · **만든 시각**. 없는 것만 더한다
  - [ ] MCP 도구 설명이 「필드를 채워 초안을 만든다」를 말하게 한다 — AI 가 객체를 다 채우도록. 새 도구는 내지 않는다
  - [ ] 운영 대장(operation inventory) drift 는 **실패 diff 의 그 항목만** 패치
- **SPEC**: **SPEC-001 S-9 · §4 Validation · §5** · **SPEC-002 §4**(confirm 의 고친 초안 예외) · **SPEC-002 §2.4**(만든 시각)
- **검증**: `make test-unit` · `make test-contract` · 기한 없는 초안 confirm 이 통과 · 고친 draft 가 회차 2 로 남음 · 코디 `make verify`
- **완료 증거**: 코드 `4a89650` · 검수 WARN(테스트 정밀도)

### Phase 3b — FE · 요약 카드 · 수정 모달 · 「AX 제안」 칩

- **Status**: DONE
- **무엇이 끝나야 시작하나**: Phase 3a 커밋 + **로컬 스택 재시작**
- **워커**: frontend
- **카드 와이어프레임** (채팅 서랍 폭 380px · 높이 고정):

```
┌──────────────────────────────────────┐
│ [AX] [초안 · 1회차]        업무 생성 │  ← 배지 「SC AX」→「AX」
│ KPI 설정                             │  ← 제목
│ ▬▬▬▬▬▬ ────── ────── ──────          │  ← 4칸 바 · 현재 칸 검정 · 누르면 이동
│ 기본 정보                            │  ← 현재 페이지 이름
├──────────────────────────────────────┤
│ ‹  내 업무 · 10/01 → 10/06         › │  ← 본문: 읽기 전용 요약
│    참조자 A, B · 결재자 C            │     ‹ › 는 호버 때만, 본문 위에 겹침
│    "내용 두 줄까지…"                 │
├──────────────────────────────────────┤
│              [거절]  [수정]  [등록]  │
└──────────────────────────────────────┘
```

- **계약**:
  - [ ] 카드 본문 = 「새 업무 추가」 모달 탭 4개(`CreateTab` = 기본 정보 · 체크리스트 · 업무 연결 · 자료, `WorkModals.tsx:4165`)의 **읽기 전용 요약**. 페이지·필드는 모달과 **1:1**. 빈 페이지는 「없음」 한 줄
    - 기본 정보: 갈래 · 시작일/마감일 · 담당 후보(요청) · 내용(두 줄) · 참조자 · 결재자
    - 체크리스트: 「N개 · 첫 항목…」 / 업무 연결: 상위 · 프로젝트 · 참고 · 선행 / 자료: 「파일 N · 링크 N」
  - [ ] 페이지 이동: 헤더 4칸 바 클릭 · 본문 호버 ‹ ›(첫/끝 페이지에서 해당 화살표 숨김) · 트랙패드 좌우 스와이프 · 키보드 ← →
  - [ ] 「수정」= AI 초안이 채워진 **「새 업무 추가」 모달 그대로** 연다. 탭·필드·검증 모두 모달 것. 모달의 「등록」= 고친 값으로 confirm(+draft). 닫으면 고친 것을 버리고 카드는 초안 그대로
  - [ ] 「등록」(카드) = 초안 그대로 confirm. 「거절」= 기존 reject
  - [ ] 등록 뒤 카드는 한 줄 요약(제목 · 기한 · 담당)과 [업무 열기] 로 접힌다
  - [ ] 배지 「SC AX」→「AX」. `SC AX` 문자열이 화면에 나가는 곳을 전부 센다(조사 시 2곳: `ActionTaskCard.tsx:467`·`:934`)
  - [ ] **A-01 — 보이는 곳**
    - 홈 판단 대기: 그대로 두되, 누르면 같은 요약 카드를 띄워 거절·수정·등록
    - 내 업무 칩 바에 **「AX 제안 N」 칩** — 대상 두 kind 만. **다른 칩과 같은 필터 칩**(하나만 켜짐). 자리는 **현행 칩 바의 `받은 요청` 바로 뒤**, `기한 지남` 은 맨 끝. **0건이어도 「AX 제안 0」** 으로 선다
    - 칩을 켜면 목록이 **AX 초안 줄**로 좁아지고, 줄을 누르면 같은 요약 카드. **AX 초안 줄은 이 칩을 켰을 때만** — 「전체」·다른 칩에는 섞이지 않는다
    - 초안 줄의 모양: 업무 행과 같은 열 틀을 쓰되(업무명 · 요청자 자리 「AX」 · 기한 · 상태 「초안」 · 만든 지 며칠), 행 액션 칸은 비운다 — 처리는 카드에서 한다(코디 기본값)
    - 「받은 요청」 수신함에는 섞지 않는다(기존 단언 `MyWorkPage.test.tsx:349-370` 유지)
    - 자동 만료 없음. 「만든 지 며칠」 표시
  - [ ] **P-2** — DS 부품·토큰. 시안 없는 자리는 DS-gaps
- **SPEC**: **SPEC-002 §2.4 · §2.9 · S-7 · §6** · **SPEC-001 U-2 · §6**
- **검증**: `make frontend-test` · `npx tsc --noEmit` · `make frontend-build` · 코디가 로컬에서 AX 채팅으로 초안 생성 → 카드 넘김 → 수정 모달 → 등록 → 홈·칩에서 사라짐까지 확인
- **완료 증거**: 코드 `8700bd0` · 검수 FAIL(참고 업무 유실)→fix1(+자료 첨부 되살림·채팅 created_at)→재검수 WARN→fix2 · 사용자 E2E 2루프 `dc4fe90`·`94cacfd`

---

## Phase 4 — BE · 운영 회의 요약(종료 합성) 실패 (B-03)

- **Status**: DONE
- **무엇이 끝나야 시작하나**: 없음(3b 와 파일이 겹치지 않으면 병렬)
- **워커**: backend
- **요청**: 사용자 2026-10-01 — 운영 회의 둘이 「회의 내용은 저장됐지만 글로 옮기지 못했습니다」로 실패, AI 회의록 없음. 「서버에서 확인하고 버그픽스」
- **원인** (`orchestration/work/strong-hajin-polish/research-meeting-summary.md`): 회의 중 Codex 세션은 `back` 파드에서 열리고, 종료 합성은 `worker-meeting` 파드에서 `codex exec resume <id>` 로 그 세션을 잇는다. 세션 파일이 사는 런타임 홈(`/app/.scax/codex-runtime`)이 파드 로컬이라 worker-meeting 에 세션이 없어 3회 모두 즉시 실패(`FAILURE_UNFINISHED`). 재전사·녹음·인증은 정상
- **계약 (2026-10-01)** — ~~인프라 변경 없이 코드로 닫는다~~ → **뒤집음(사용자)**: 세션 런타임 홈을 녹음처럼 **Mac 호스트 hostPath `/mnt/mac/strong-hajin/codex-runtime`** 에 두고 앱 기본 경로 `/app/.scax/codex-runtime` 에 back·워커 4개가 공유(인프라 `charts/strong-hajin/`). 코드는 안전장치
  - [ ] 종료 합성이 이전 세션을 **이어 갈 수 없으면(세션 없음 등 resume 실패) 콜드스타트로 합성**한다 — 저장된 전사 전문으로 새 세션을 열어 같은 결과물을 만든다. 일반 재시도 3회와 구분한다
  - [ ] 런타임 홈 경로를 **설정(env)으로 받을 수 있게** 한다 — 기본값은 지금과 같다(배포 변경 없이 동작)
  - [ ] codex 실패 시 **stderr 요약을 로그에 남긴다**(비밀값 마스킹) — 다음 장애의 원인을 로그로 본다
  - [ ] 이미 실패한 회의는 배포 뒤 사용자의 [다시 시도]로 회의록이 생긴다(새 경로를 탄다)
- **검증**: resume 실패 → 콜드스타트 성공 테스트 · 콜드스타트도 실패하면 지금처럼 실패 상태 · `make test-unit` · `make test-contract` · 운영 반영 뒤 실패 회의 [다시 시도] 확인(사용자 E2E)
- **인프라**: `charts/strong-hajin/` `_helpers.tpl`·values — 다섯 deployment 에 hostPath(type Directory) 마운트. **sync 전 노드에서 `limactl shell worker-1 -- sudo mkdir -p /mnt/mac/strong-hajin/codex-runtime`**
- **반영 뒤 볼 것**: 다섯 파드의 sqlite(state·logs) 오류 0 — 보이면 파드별 홈 + `sessions/` 만 공유로 바꾼다(검수 `review-p4-report.md`) · 기존 실패 회의 둘 [다시 시도]
- **범위 밖**: 웜스타트 구조 변경 · 파드 간 같은 세션 동시 resume 상호배제(확률 낮음, 검수 WARN)
- **완료 증거**: 코드 `dd4bd7c` + 인프라 MediSolveAIDev/k8s_infra_mac#7(codex-runtime hostPath) · 검수 WARN

---

## Phase 5 — BE · AX 업무 생성이 프로젝트·업무를 찾지 않는다 (E2E-12)

- **Status**: DONE
- **워커**: backend
- **요청**: 사용자 2026-10-01 E2E — 「`graph_search` 실패 … 왜 프로젝트 연결이 안 돼? 업무 만들 때 프로젝트·업무들 탐색 안 해?」
- **원인** (`orchestration/work/strong-hajin-polish/research-graph-search.md`)
  - (B) 업무 생성 때 탐색을 **하지 않는다**: 생성 도구 설명은 「대화가 준 필드만 채워라」, 라우팅 정책은 오히려 graph_search 를 먼저 부르지 말라고 하고, `project_list` 는 「회의용」으로 적혀 있다 → project_id 없이 생성
  - (A) 프로젝트를 답변 근거로 가리키면 **턴 전체가 실패**: 답변 참조 형식에 `project` 종류가 없고, graph 도구로 본 대상은 근거로 묶이지 않는다
  - (C) `graph_search` 22ms × 는 모델이 없는 인자(`kinds`)를 지어내 거절된 것 — 같은 턴에서 다시 불러 성공(무해)
- **계약 (코디 결정 2026-10-01 — P-1 「AX 초안 = 새 업무 추가를 AI 가 채운 것」의 연장: 사람이 창에서 프로젝트·선행·참고를 고르듯 AI 도 찾아서 채운다)**
  - [ ] 업무 생성·요청 초안을 만들기 전에 AX 가 **관련 프로젝트·기존 업무를 찾아** project_id·parent·reference·preceding 을 채울 수 있게 — 도구 설명·라우팅 정책·`project_list` 설명을 고친다. 못 찾거나 모호하면 비우고 답변에 「연결할 프로젝트를 찾지 못했다」고 말한다(지어내지 않는다)
  - [ ] 답변 참조에 **`project` 종류**를 더하고, graph 도구로 본 대상도 근거로 묶일 수 있게 — 프로젝트를 가리킨 답변이 턴 실패가 되지 않는다. FE 가 project 참조를 그리는지 확인(못 그리면 FE 몫으로 보고)
  - [ ] `graph_search` 인자 설명을 실제 스키마와 맞춰 지어낸 인자를 줄인다
- **검증**: 프로젝트 이름이 들어간 업무 생성 요청 → 초안에 project_id · 프로젝트를 가리킨 답변이 턴 성공 · `make test-unit` · `make test-contract`
- **범위 밖**: 실행 단계 UI 에서 자가 수정된 인자 오류의 표시 방식
- **완료 증거**: 코드 `33e8f1b` · 검수 FAIL(회의 causation UUID)→fix1

---

## Phase 6 — BE · 핫픽스: AX 대화·회의 배치가 세션을 잃으면 새로 이어 간다 (B-04)

- **Status**: **취소(2026-10-02)** — 사용자 「핫픽스 안 해도 돼 · 버리자」. 원인은 배포 전 세션이 옛 파드 로컬에 있던 일회성이고, 공유 hostPath 이후 세션은 재배포에도 남는다. 구현했던 코드는 버렸다(브랜치 미푸시·삭제). 남은 위험: 공유 디렉터리 밖에서 세션을 잃으면 대화·회의 배치는 대비가 없다
- **요청**: 사용자 2026-10-02 운영 — 배포 전에 시작한 AX 대화가 「Codex CLI session to resume is not available here」로 매번 실패
- **원인**: 그 대화의 codex 세션은 옛 `worker-conversation` 파드 로컬에만 있었고 재배포로 사라졌다(`no rollout found for thread id …`). 대화 turn 에는 세션 없음 대비가 없다(Phase 4 조사에서 남은 위험으로 기록). 공유 hostPath 는 이번 배포부터라 이후 세션은 남는다
- **계약 (코디 결정)**
  - [ ] 대화 turn 이 resume 불가(세션 없음)면 그 대화의 provider 세션을 버리고 **최근 대화 기록을 담아 새 세션으로** 이어 간다 — 같은 turn 안에서, 사용자는 실패를 보지 않는다
  - [ ] 회의 배치(웜스타트 세션 resume)도 같은 대비
  - [ ] 세션 없음 판정은 Phase 4 의 판정을 재사용
- **검증**: 세션 없는 대화 turn 성공 · 회의 배치 성공 · `make test-unit` · `make test-contract` · 운영 반영 뒤 사용자 대화로 확인

---

## Pre-deploy Check

- [ ] 세 페이지 화면 확인을 사용자가 봤다
- [ ] 코디 `make verify` 통과 · PR 하나 → main 머지
- [ ] 운영 반영: arm64 back·front 이미지 → infra `image.tag` PR → Argo 수동 sync (RUNBOOK-002 §1)
- [ ] 운영에서 `/health` · 로그인 · AX 초안 하나 등록까지 확인

## Rollback

- `values-prod.yaml` 태그를 직전 값(`cdb0f3f-arm64`)으로 되돌려 머지 → 수동 sync. 스키마 변경이 없으므로 데이터 되돌림은 없다

## 반영

- 2026-10-02 운영 반영: kknaks/Strong_hajin#9 squash `3d47a32` → 이미지 `3d47a32-arm64` → k8s_infra_mac#7 → 노드 디렉터리 → Argo 수동 sync Synced/Healthy 8/8. web 200 · /health production · codex-runtime 공유 마운트 확인 · 로그 오류 0

## Done Criteria

- 여덟 요청의 계약 체크가 모두 채워졌고 화면 확인 증거가 있다
- 운영에 반영됐다

## Open Issues

| ID | 무엇 | 다음 |
|---|---|---|
| ~~OQ-801~~ | ~~SPEC 환류~~ — **닫힘(2026-10-01)**: 코드 전에 SPEC-001/002/003/005/007 에 반영·검수 | — |
| OQ-802 | 서버 성능(N+1·인증 재계산) — B-01 Phase 2 체감 뒤 결정 | Phase 2 후 |

## Related

- `_RESUME.md` — 요청 원문과 결정 이력
- RUNBOOK-002 — 운영 반영 절차
