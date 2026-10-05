---
type: work
id: WORK-010
title: "운영 고도화 3차 — 업무 상세 인라인 개편 · 회의 제목 · 데스크톱 첨부 저장"
status: review
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
progress: 90
created_at: 2026-10-04
updated_at: 2026-10-05
tags:
  - product/strong-hajin
  - doc/work
  - status/review
links:
  baselines: []
  decisions: []
  specs:
    - "[[spec-007-task-detail|SPEC-007]]"
    - "[[spec-006-tauri-wrapper|SPEC-006]]"
    - "[[spec-001-work-management|SPEC-001]]"
    - "[[spec-005-projects|SPEC-005]]"
  works:
    - "[[work-009-polish2|WORK-009]]"
    - "[[work-007-task-detail|WORK-007]]"
  releases: []
  related:
    - "[[runbook-002-production-deploy|RUNBOOK-002]]"
sources:
  - orchestration/work/strong-hajin-polish3/_RESUME.md
  - orchestration/work/strong-hajin-polish3/be-survey-report.md
  - orchestration/work/strong-hajin-polish3/fe-survey-report.md
---

# 운영 고도화 3차 — 업무 상세 인라인 개편 · 회의 제목 · 데스크톱 첨부 저장

2026-10-04 운영(`https://ax.medisolveai.xyz`)을 쓰며 사용자가 낸 요청 여섯(R1~R6)과 업무 상세 개편 결정(a~g)을 한 판으로 묶는다.
요청 하나하나가 **사용자와 닫은 계약**이다(`_RESUME.md` §2) — 범위를 넓히지 않는다.

> **SPEC 이 먼저 반영됐다**(Meta). 계약 문장이 이 WP 와 SPEC 사이에서 다르면 **SPEC 이 맞다** — 워커는 코디에게 알린다.
>
> 1 파일 = 1 work. 이 판은 **네 페이지**로 나뉜다: Phase 1(FE 작은 것) · Phase 2a·2b(FE 업무 상세) · Phase 3(데스크톱 셸).
> Phase 3 은 `frontend/src-tauri/` 만 건드려 Phase 1·2 와 파일이 겹치지 않는다 → **Phase 1 과 나란히**. 2a → 2b 는 같은 파일이라 직렬.
> 페이지마다 발주 → 구현 → 검수(reviewer) → 재수정 → 코디 커밋. 끝나면 사용자 E2E → PR 하나 → main → 운영 반영(RUNBOOK-002 §1).
> 근거 줄 번호는 조사 시점(코드 `d1b5137`) 값이다. 워커는 **줄 번호가 아니라 심볼로 다시 찾는다.**

## Meta

- **SPEC (정본)**
  - SPEC-007 v0.5.1 — **§2.10 전부**(2.10.1 헤더 · 2.10.2 메타 정보 · 2.10.3 걸린 일 · 2.10.4 인라인 저장 · 2.10.5 진행 상태 셀렉트 · 2.10.6 담당 셀렉트 · 2.10.7 읽기 전용 · 2.10.8 출처 · 2.10.9 지우는 것) · §3 S-1·S-2·S-9~S-11 · §6 「고도화 3차」 AC · §7.2 ⑨~⑬ · §7.3 OQ-711·712(코디 닫음)
  - SPEC-001 v0.5.2 · SPEC-005 v0.3.1 — 정정(상세 상단 단추 문장 · `WORK_VERSION_STALE` = 422)
  - SPEC-006 v0.3.1 — U-5 · S-14 · E-15 · §5 · AC-T44~48 · M-15 · OQ-T12·T13(코디 닫음)
  - R1·R2a·R3 은 해당 화면 계약을 가진 SPEC 이 없어 **이 WP 가 계약**이다(코디 판단 2026-10-04)
  - 검수: `review-spec-report.md`(FAIL 0 · WARN 12 → writer fix1 · 코디 답 W3 서버 값 · W7 확인 대기 글자만 · W8 업무 상세만 · OQ 전부 닫음)
- Covers: R1 · R2 · R3 · R4(a~f) · R5 · R6 · g (`_RESUME.md` §1·§2)
- 조사: `be-survey-report.md` · `fe-survey-report.md` · 기준선 `flaky-baseline-evidence.md`(FE 기존 실패 5건)
- 코드 워크트리: `Strong_hajin/strong-hajin-polish3` (branch `kknaksss/strong-hajin-polish3`, base `origin/main` `d1b5137`)
- **서버 변경 없음**(조사 결론 — 필요한 API·필드가 다 있다). 백엔드 파일을 바꿔야 할 것 같으면 **먼저 코디에게 묻는다**
- 데스크톱 셸(`frontend/src-tauri/`)은 Phase 3 에서만 바뀐다 → medi-ax dmg 재빌드 필요(반영 절)

## 이 판의 원칙

| # | 원칙 | 근거 |
|---|---|---|
| P-1 | **보고 닫으려다 상태를 바꾸지 않는다.** 상세에는 푸터가 없고, 상태는 메타 정보의 셀렉트로만 바꾼다 | 사용자 「조회하고 닫을 때 계속 완료 처리」 |
| P-2 | **값은 그 자리에서 고치고 바로 저장한다.** 편집 모드·저장 단추가 없다. 안 바뀌면 보내지 않고, 실패하면 되돌린다 | 사용자 「굳이 편집을 나눠야 해?」 |
| P-3 | **서버 규칙을 화면이 앞지르지 않는다.** 갈 수 있는 상태는 서버 허용표, 막힘은 서버 409 문장. 화면은 새 규칙을 만들지 않는다 | 조사 · SPEC-007 §2.10.5 |
| P-4 | **쓰는 곳을 전부 센다.** 이 문서의 파일:줄은 출발점이다. 같은 심볼·패턴을 grep 으로 전부 세고 시작한다 | 오케스트레이션 규칙 |
| P-5 | **디자인 시스템 안에서만.** 기존 부품(`InlineText`·`Select`·`DateField`·`ConfirmModal`·`ReasonPrompt`·`Toast`)·토큰. 시안이 없는 자리는 DS-gaps 에 적는다 | WORK-008 P-2 |

## Work Summary

| 페이지 | 요청 | 무엇 | 어디 |
|---|---|---|---|
| 1 | R1 | 로그인 브랜드 문구 | FE |
| 1 | R2a | 회의 「내보내기」 단추 크기 | FE |
| 1 | R3 | 회의 제목 인라인 수정 · 제목 후보 [적용] | FE |
| 2a | R4 H·M·I·e·RO · R6 · R5 배너 | 업무 상세 헤더 · 메타 정보 · 인라인 저장 · 출처 · 읽기 전용 · 여백 · 편집 모드/AX/막힘 배너 삭제 | FE |
| 2b | R4 F·b·c·a · R5 토스트 | 진행 상태 셀렉트 · 사유 작은 모달 · `⋯` 제안 메뉴 · 담당 제안 · 걸린 일 상자 · 푸터·「진행과 판단」 삭제 | FE |
| 3 | g · R2b | 데스크톱 첨부 응답을 파일로 저장 · 앱 화면 유지 | 셸(Rust) |

## Code Surface

- FE: `frontend/src/` (테스트 포함) — Phase 1·2a·2b
- 셸: `frontend/src-tauri/` — Phase 3 만(+ 저장 결과 토스트 수신부 `frontend/src/lib/shell.ts`·`App.tsx`)
- BE: 없음

---

## Phase 1 — FE · 로그인 문구 · 내보내기 단추 · 회의 제목

- **Status**: DONE — 코드 `7f01c5b` · 검수 WARN 4 → fix1(W4 긴 제목 줄바꿈은 E2E)
- **무엇이 끝나야 시작하나**: SPEC 검수
- **워커**: frontend

### 1-1. R1 로그인 브랜드

- **지금**: `features/auth/LoginPage.tsx:68-69` — h1 「기록 → 판단 → 수행 → 보고를 한 흐름으로」 · p 「조직의 업무를 하나의 원장에서…」. 같은 문구는 저장소에 각 1건(`fe-survey §1`)
- **계약**:
  - [ ] h1 = **「메디솔브 AX 프로젝트」**
  - [ ] 설명 `p` 를 **지운다**(빈 요소도 남기지 않는다). 워드마크 「M MEDISOLVE」·레이아웃·900px 이하 숨김은 그대로
  - [ ] 문서 title·Tauri 창 제목은 바꾸지 않는다

### 1-2. R2a 회의 「내보내기」 단추 크기

- **지금**: `features/meetings/MeetingDetailPage.tsx:1003-1007` `<a className="scax-button scax-button--outlined-neutral">` — `scax-button--sm` 이 없어 39px, 옆 「공유」「다음 회의 예약」은 `<Button size="sm">` 32px(`fe-survey §2-1`)
- **계약**:
  - [ ] 「내보내기」가 옆 단추와 **같은 크기(sm)·같은 변형**으로 선다. 동작(같은 탭 이동 → 서버 첨부)은 바꾸지 않는다 — 데스크톱 저장은 Phase 3 몫
  - [ ] `<a>` 에 `scax-button` 을 쓰는 다른 두 자리(`MaterialDrawer.tsx:66` lg · `MessageList.tsx:782` sm)는 의도된 크기라 그대로

### 1-3. R3 회의 제목 인라인 수정

- **지금** (`fe-survey §3`, `be-survey §3`): 상세 `h2.scax-detail__title` = `meeting.title ?? "제목 없는 회의"`(`MeetingDetailPage.tsx:962`), 제목이 없고 `title_candidate` 가 있으면 옆 `span.t-meta` 「제목 후보 …」(`:964-967`). 제목을 고치는 입구는 목록 [수정](`scheduled` 만) 하나. 서버 `PATCH /api/meetings/{id}` 는 `{title}` 하나만 받아도 되고, **참석자 + 「예정」·「완료」** 만 받는다(`can_edit_info`). 버전 잠금 없음. 인라인 부품 `ds/InlineText.tsx`(CMP-118)가 있다
- **계약**:
  - [ ] `can_edit_info` 일 때 상세 제목을 **클릭하면 그 자리 인라인 입력**(`InlineText` 재사용). Enter·blur 저장 · Esc 취소 · 빈 값/안 바뀐 값은 보내지 않고 원래 값 · 실패하면 원래 값 + 서버 문장을 오류 토스트
  - [ ] `can_edit_info` 가 아니면(참석자 아님 · 진행 중 · 정리 중 · 실패 · 취소) 지금처럼 글자만
  - [ ] 제목이 비어 있으면 표시는 「제목 없는 회의」(입력을 열면 빈 칸에서 시작)
  - [ ] **제목 후보**: 제목이 없고 `title_candidate` 가 있을 때만 「제목 후보: {후보} **[적용]**」. [적용] = 후보를 제목으로 저장(`PATCH {title: 후보}`). `can_edit_info` 가 아니면 [적용] 없이 지금처럼 글자만. 제목이 생기면 후보 줄은 사라진다(서버가 후보를 지우지 않아도 화면은 `title` 이 있으면 안 그린다)
  - [ ] 저장 뒤 상세·상위로 넘기는 제목(`onTitleChange` `:299`)·목록·캘린더 레일이 새 제목을 보인다 — 「제목 없는 회의」 대체를 쓰는 5곳(`fe-survey §3-1`)에서 다시 읽기 경로 확인
  - [ ] `MeetingDetailPage.tsx:23` 의 쓰지 않던 `updateMeetingInfo` import 를 실제로 쓴다. 목록 [수정] 모달은 그대로

### Phase 1 검증

- [ ] `make frontend-test`(직렬 `npx vitest run --no-file-parallelism`, 기존 실패 5건 분리) · `npx tsc --noEmit` · `make frontend-build`
- [ ] 바뀐 계약마다 테스트(제목 인라인 저장·Esc·빈 값·권한 없음·후보 [적용]·로그인 문구)

---

## Phase 2a — FE · 업무 상세 헤더 · 메타 정보 · 인라인 저장

- **Status**: DONE — 코드 `cc64d18` · 검수 WARN 6 → W1~W5 를 2b 에 합침
- **무엇이 끝나야 시작하나**: Phase 1 커밋
- **워커**: frontend
- **대상**: `features/work/WorkModals.tsx` `TaskDetailDrawer`(`:606-3039`) · `styles/task-detail.css` · 호출부 3곳(`MyWorkPage.tsx:1297` · `TodayPage.tsx:418` · `CalendarPage.tsx:701`)

### 2a-1. 헤더 (SPEC-007 §2.10.1)

- **지금** (`fe-survey §4-1`): `Modal` 머리 = kicker 「업무 상세」 · `h3` 제목 · ChipRow(상태 글자 · 「마감일 초과」 · `v{n}` · 「편집」 · ✦「AX」) · ×. 겹이 2개 이상이면 왼쪽 「뒤로」
- **계약**:
  - [ ] 머리 = **(겹일 때) 뒤로 · 제목 · (2b 에서) `⋯` · ×**. kicker·ChipRow 를 지운다(상태 → 메타 정보, 버전 → 메타 정보, 마감일 초과 → 메타 정보 마감일 행)
  - [ ] **「AX」 단추 삭제** — `onAskAx`/`onAskAboutTask` prop·`askAboutTask`(`App.tsx:313-327`)까지 쓰는 곳이 0 이 되면 함께 지운다. 대체 입구 없음(결정 d)
  - [ ] 제목 = 클릭 인라인(2a-3 규칙). 읽기 전용이면 글자만. 모달 `aria-label` 은 「업무 상세」 유지(접근성 이름)
  - [ ] `Modal` 공용 부품을 바꿔야 하면 **업무 상세에서만** 쓰는 prop/className 으로 — 다른 12 표면(`fe-survey §6-2`)의 머리를 바꾸지 않는다

### 2a-2. 메타 정보 구역 (§2.10.2 · §2.10.8)

- **지금**: `div.meta` 한 줄 사실(담당 · 날짜 넷 · 결재 · 참조) + `p.origin-chip` + (편집 중) `meta__edit` DateField 둘
- **계약**:
  - [ ] 「업무 정보」와 같은 계층의 구역 **「메타 정보」**, 라벨·값 **2열 격자**. 행과 순서는 SPEC-007 §2.10.2 그대로 — 진행 상태 · 버전 · 담당 · 시작 예정일 · 실제 시작일 · 실제 종료일 · 마감일 · 결재 · 참조 · 출처(날짜 순서 = OQ-712 E2E-5)
  - [ ] 2a 에서 **진행 상태 행은 지금 상태 글자(읽기)** 로 둔다 — 셀렉트는 2b. **담당 행도 이름(읽기)** — 셀렉트는 2b
  - [ ] 시작 예정일·마감일 = `DateField` 인라인, **고르는 즉시 저장**(2a-3). 비어 있어도 행이 선다(처음 정할 자리). 시작 예정일 > 마감일이면 보내기 전에 막고 필드 옆 문장
  - [ ] 실제 시작일·실제 종료일·버전·결재·참조 = 읽기 전용. 값이 없는 읽기 전용 행의 처리는 SPEC §2.10.2 대로
  - [ ] **「마감일 초과」** = 마감일 행 값 옆 danger 배지(OQ-711)
  - [ ] **출처 행**(§2.10.8 · 결정 e): AX 제안 출처 = 「AX 제안 · **판단 보기**」 — 링크 글자를 업무 제목(`source.title`)에서 「판단 보기」로. `onOpenSource` 가 없는 화면(홈·캘린더)은 「AX 제안」 글자만. 요청에서 온 업무·직접 배정 문구는 지금 규칙. origin 이 없으면 행이 없다
  - [ ] 「업무 내용」 = 클릭 인라인 여러 줄, **blur 저장**(Enter 는 줄바꿈). 칸 머리 「업무 내용」은 하나만(지금 두 번 나오는 원인 `:2068`·`:2071`)

### 2a-3. 인라인 즉시 저장 (§2.10.4)

- **지금**: `metaEditing` 토글 + 푸터 「변경 저장」 → `save()` → `onUpdate(current, patch)` → 호출부 3곳 `updateTask(task_id, version, patch)` = `PATCH /api/tasks/{id}` `{expected_version, …}`(`fe-survey §4-2`). 서버는 저장마다 version +1, 어긋나면 **422 `task version is stale`**(`be-survey §4-3`)
- **계약**:
  - [ ] **편집 모드 폐지**: `metaEditing`·「편집」/「편집 끝내기」·「변경 저장」·`dirty` 를 지운다(쓰는 곳 전부 — `metaEditing` 읽는 자리 6)
  - [ ] 필드 하나 = 저장 하나. 안 바뀌면 요청 없음. **한 번에 하나씩 직렬** — 앞 저장이 끝나기 전 다음 저장은 대기열, **앞 응답의 `version` 을 다음 요청의 `expected_version` 으로**
  - [ ] 성공: 그 필드 값·버전 갱신. 호출부의 목록·캘린더도 새 값(지금 `reload` 경로 재사용). 성공 토스트를 저장마다 띄우지 않는다(조용히 — 실패만 알린다. SPEC §2.10.4 의 표시 규칙 우선)
  - [ ] 실패: 그 필드를 **원래 값으로 되돌리고 필드 옆 실패 표시**. **422 stale 은 자동 재전송 없이 상세를 다시 읽고, 그 필드는 다시 읽은 서버 값으로** + 필드 옆 「다른 곳에서 바뀌어 최신 값으로 다시 불렀습니다」 류 표시(SPEC §2.10.4 · 코디 W3)
  - [ ] 저장 중 표시·포커스 이동·IME 조합 중 Enter 무시(체크리스트 단계 수정 `:2139-2159` 의 규칙과 같게)
  - [ ] 호출부 3곳의 `onUpdate` 가 **새 version 을 돌려주도록**(지금은 `reload` 후 prop 으로만 온다) — 직렬 저장이 그 값을 쓸 수 있게. 형태는 워커 판단, 보고

### 2a-4. 읽기 전용 · 막힘 배너 · 여백 (§2.10.7 · R5 · R6)

- **계약**:
  - [ ] `canManage=false`·`access=read_only`·`cancelled` 이면 제목·내용·날짜가 **글자만**(클릭해도 안 열린다). 입구 16곳 중 읽기 전용 10곳(`fe-survey §4-7`)
  - [ ] **「시작할 수 없습니다」 배너**(`:2054-2059`) 삭제 · `blockedBanner` 등 쓰는 곳이 0 이 되는 심볼 정리. 「연관 업무」 선행 칸의 미완 배지는 그대로. 푸터 `scax-blocked-note` 와 목록 행 `TaskQuickActions` 의 같은 문구는 2b 에서
  - [ ] **R6 여백**: 머리 아래 ~ 메타 정보 첫 행 간격을 줄인다(지금 41px — 머리 padding-bottom 20 + border 1 + 본문 padding-top 20). **`.scax-td`/업무 상세 스코프에서만** — `components.css:257,263` 공용 규칙은 그대로. 값은 DS 토큰, 보고

### Phase 2a 검증

- [ ] `make frontend-test`(직렬, 기준선 5건 분리) · `npx tsc --noEmit` · `make frontend-build`
- [ ] 테스트: 헤더에 kicker·상태·버전·편집·AX 가 **없다** · 인라인 저장(안 바뀜=요청 없음 · 직렬 · version 이어받기 · 422 → 다시 읽기+되돌림) · 날짜 즉시 저장·뒤집힘 막음 · 읽기 전용 입구에서 안 열림 · 배너 없음 · 출처 「판단 보기」
- [ ] 프로젝트 우 패널(`ProjectTaskPanel`)·목록처럼 **같은 부품·라벨을 함께 쓰는 자리**가 깨지지 않았는지(회귀) — 바꾼 공용 심볼을 쓰는 곳 전부

---

## Phase 2b — FE · 진행 상태 셀렉트 · 담당 제안 · 걸린 일 · 푸터 삭제

- **Status**: DONE — 코드 `58e591a` · 검수 WARN 4 → fix1 (+2a W1~W5)
- **무엇이 끝나야 시작하나**: Phase 2a 커밋
- **워커**: frontend

### 2b-1. 진행 상태 셀렉트 (§2.10.5 · 결정 b · R5)

- **지금**: 푸터 단추 최대 11종(`fe-survey §4-4` 매트릭스). 목록에는 상태 드롭다운 선례 `TaskStateCell`(`MyWorkPage.tsx:1483-1567`, `Select` + 톤 트리거) · `ProjectTaskPanel` `TaskStateValue`. 서버 허용표 `be-survey §4-5`, 전이는 **활성 담당자만**
- **계약**:
  - [ ] 메타 정보 「진행 상태」 = **셀렉트**. 단 **완료(확인 대기 — `derived.approval=awaiting_review`)는 셀렉트 없이 상태 글자만**(업무 취소도 없음 — SPEC-005 관문 다 계승, 코디 W7). 옵션 = SPEC-007 §2.10.5 의 상태×역할 표 그대로(서버 허용표를 따른다 — 완료 업무에 「업무 취소」 없음, 요청자에게 시작·막힘·완료 없음). 트리거 톤은 목록 선례와 같게. 상태 셀렉트 부품을 목록 선례와 **나눠 쓸 수 있으면 나눠 쓴다**(새로 만들지 않는다 — 판단 보고)
  - [ ] **막힘**(사유 필수) · **업무 취소**(사유 필수, 맨 아래 빨강) · **완료에서 재개**(사유 선택) = **작은 모달**(`ReasonPrompt`/`BlockReasonPrompt` 재사용). 지금 「진행과 판단」 안에 펼쳐지는 막힘 사유 입력(`isBlocking` `:2391-2425`)을 모달로 바꾼다
  - [ ] 요청받은 업무의 「완료」 = 기존 **완료 보고 모달**(`CompletionReportModal`). 미완 체크리스트가 있는 직접 완료 = 기존 확인창 「남은 단계가 있습니다」
  - [ ] 서버 거절(선행 409 등) = **서버 문장을 공통 오류 토스트**로, 셀렉트는 원래 값. 화면은 선행 막힘을 미리 막지 않는다(OQ-709) — 상세 `startBlocked` disabled 경로 삭제
  - [ ] 전이 성공 토스트·다시 읽기는 지금 호출부(`transitionTask` 등) 경로 재사용
- **`⋯` 메뉴** (§2.10.1):
  - [ ] 요청 업무의 요청자(지금 「취소 제안」·「조건 변경 제안」이 서는 조건 `:1806,1813`)에게만 머리에 `⋯`. 항목 = 「취소 제안」·「조건 변경 제안」 → 지금 모달(`ReasonPrompt`·`TermsChangePrompt`). 그 밖의 사람에게는 `⋯` 자체가 없다

### 2b-2. 담당 셀렉트 (§2.10.6 · 결정 c)

- **지금**: 「진행과 판단」 안 「담당자 변경」(`:2362-2369`, `canAssign && !readOnly`, `canAssign` 은 내 업무에서만) → `Modal sm` 대상 `Select` + 사유 → `POST /api/tasks/{id}/reassign`
- **계약**:
  - [ ] 메타 정보 「담당」 = `canAssign && !readOnly` 일 때 **셀렉트**(후보 `GET /api/task-assignment-candidates`). 사람을 고르면 **사유(선택) 작은 모달** → 「변경」 → `/reassign`. 그 밖은 이름 글자
  - [ ] 성공 뒤 담당 칸에 **「{대상}에게 변경 제안 중」**(수락 전까지 기존 담당 유지 — 지금 토스트 문장 유지). 대기 제안이 있으면 셀렉트를 다시 열지 않는다(서버 409) — 표시 규칙은 SPEC §2.10.6
  - [ ] 「담당자 변경」 단추와 그 겹 `Modal`(`:2811-2865`)은 새 작은 모달로 대체 — 남는 코드 정리

### 2b-3. 걸린 일 상자 · 「진행과 판단」·푸터 삭제 (§2.10.3 · §2.10.9 · 결정 a · F)

- **계약**:
  - [ ] 「진행과 판단」 **구역 제목·덩어리 삭제**. 안의 구획(`fe-survey §4-3` 표 1~5·7 — 완료 확인 대기+완료 인정/보완 요청 · 보완 필요 · 담당 변경 대기 · 응답 대기 제안+동의/동의하지 않음/철회 · 미완 하위 · 막힘 사유)은 **조건이 참일 때만 메타 정보 바로 아래 상자**로. 6(담당자 변경 단추)은 2b-2, 8(막힘 사유 입력)은 2b-1 모달. 상자 안 단추의 조건은 지금 그대로
  - [ ] **푸터 전부 삭제** — 업무 취소 · 취소 제안 · 조건 변경 제안 · 막힘 · 시작 · 완료 처리 · 완료 보고 · 재개(둘) · 닫기 · `scax-blocked-note`. `Modal` 에 footer 를 넘기지 않는다(빈 footer 줄이 남지 않게)
  - [ ] 목록 행 `TaskQuickActions` 의 `scax-blocked-note`(`:3515`)·`startBlocked` disabled 는 **그대로**(R5 는 업무 상세만 — 코디 W8). 공용 CSS `.scax-blocked-note` 를 지우지 않는다
  - [ ] SPEC-007 §2.10.9 「지우는 것 — 전수」 목록과 1:1 대조표를 보고에 붙인다

### Phase 2b 검증

- [ ] `make frontend-test`(직렬, 기준선 5건 분리) · `npx tsc --noEmit` · `make frontend-build`
- [ ] 테스트: 상태×역할 옵션(§2.10.5 표 각 행) · 사유 필수 모달(빈 사유 막음) · 완료 보고 모달 · 남은 단계 확인창 · 409 토스트+원래 값 · `⋯` 는 요청자만 · 담당 셀렉트 권한·제안 중 표시 · 걸린 일 상자 각 조건 · **푸터 없음** · 「진행과 판단」 없음
- [ ] 코디: 데모 DB 로 상세(시작 전·진행 중·막힘·완료·요청 업무·읽기 전용 각 하나) 화면 확인

---

## Phase 3 — 데스크톱 셸 · 첨부 응답 저장 (g · R2b)

- **Status**: DONE(코드) — `9c15934` · 방식 B(`fe-p3-decision.md` — wry 가 text/html 첨부에 download handler 를 안 부름 → 셸이 `/api/` 를 가로채 직접 받음) · inline = X · 검수 WARN 7 → fix1 · **macOS 실기 pending** · Windows pending
- **무엇이 끝나야 시작하나**: SPEC 검수. **Phase 1 과 나란히**(파일 겹침 없음 — `frontend/src-tauri/` + 토스트 수신부 `lib/shell.ts`·`App.tsx`. Phase 1 은 `LoginPage`·`MeetingDetailPage`)
- **워커**: frontend(셸)
- **지금** (`fe-survey §2-3` · `be-survey §2`): 셸에 다운로드 핸들러 0건 · dialog/fs 플러그인 없음 · `on_navigation` 은 같은 origin 이동을 허용. 서버는 `text/html` + `Content-Disposition: attachment`. wry(macOS)는 핸들러가 없으면 표시 가능한 MIME 을 **Allow** — 내보낸 HTML 이 앱 창에 그려지고 돌아갈 길이 없다(사용자 확인)
- **계약** (SPEC-006 U-5 · E-15 · OQ-T12):
  - [ ] 웹뷰의 첨부 응답(`Content-Disposition: attachment`)은 **파일로 저장**되고 **창의 문서는 바뀌지 않는다**. 같은 origin 이동(회의 내보내기)과 `_blank` 링크(업무 자료·요청 첨부) 둘 다
  - [ ] 저장 위치 = **OS 다운로드 폴더, 대화상자 없음**. 파일명 = 서버 `filename*`(UTF-8 한글). 같은 이름이 있으면 덮지 않고 번호를 붙인다
  - [ ] 성공(파일 이름)·실패를 알린다 — **셸은 문구를 그리지 않는다.** 셸이 웹 앱에 저장 결과를 알리고(이벤트), **웹 앱이 기존 공통 토스트**(`App.tsx` `putNotice`)로 보인다(SPEC-006 U-1·§2.5 · OQ-T12 코디). 그래서 이 페이지는 `frontend/src/lib/shell.ts`·`App.tsx` 의 수신부도 건드린다 — Phase 1 이 이 두 파일을 건드리지 않음을 확인하고, 겹치면 코디에게. **새 권한·플러그인은 최소로** 하고 capabilities 변경을 보고(지금 `product-shell.json` 은 파일 권한 0 — 그 원칙을 깨면 근거)
  - [ ] wry/tauri 에서 응답 헤더(`Content-Disposition`)로 첨부를 가를 수 없으면 **그 사실과 대안을 먼저 코디에게 묻는다**(예: 웹 쪽에서 `download` 속성·fetch+blob — 그러면 Phase 1/2 와 파일이 겹친다)
  - [ ] 인라인 `_blank`(채팅 근거·AX 링크·표시 가능한 회의 자료)는 이번 범위 밖(OQ-T13) — 바꾸지 않는다. 실기 확인 때 앱 화면을 덮는지만 본다
  - [ ] medi-ax·strong-hajin 두 판 모두에 적용(판별 설정 차이 확인)
- **검증**:
  - [ ] `frontend/src-tauri` 에서 `cargo check` · 핵심 로직 `cargo test` · `cargo clippy -- -D warnings`
  - [ ] **코디 macOS 실기**(AC-T44·45): `make local-stack` + `make tauri-local` 로 회의 내보내기 → 다운로드 폴더에 `.html` · 앱 창은 회의 상세 그대로 · 업무 자료 첨부 `_blank` 도 같은 결과 · 인라인 `_blank` 의 현재 동작 기록
  - [ ] Windows(WebView2)는 **pending** — 실기 전에는 통과로 적지 않는다

---

## 2루프 — 사용자 E2E (2026-10-05)

- **E2E-1** 메타 정보 한 줄에 두 항목(진행 상태|버전 · 담당|출처 · 시작 예정일|실제 시작일 · 마감일|실제 종료일 · 결재|참조) · 900px 이하 한 줄 하나 — SPEC-007 v0.5.2
- **E2E-2** 시작 예정일·마감일 날짜칸 폭 통일(같은 구조 · 140px, 마감일 초과 배지는 오른쪽)
- 코드 `53c9c20` · PR kknaks/Strong_hajin#11 squash → main `202078b`

## Pre-deploy Check

- [ ] 네 페이지 검수 처리 · 코디 `make verify` 통과 · 사용자 E2E(웹 + macOS 앱)
- [ ] PR 하나(스쿼시) → main 머지 · 문서 PR 따로
- [ ] 운영 반영: arm64 front 이미지(백엔드 변경 없음 — back 이미지 태그는 그대로 두거나 같은 sha 로 맞춘다, RUNBOOK-002 판단) → infra `image.tag` PR → Argo 수동 sync
- [ ] medi-ax 데스크톱: Phase 3 이 들어갔으므로 **dmg 재빌드·서명·공증** 후 사용자에게 전달(RUNBOOK-002 데스크톱 절)
- [ ] 운영에서 로그인 문구 · 회의 제목 인라인 · 업무 상세 인라인 저장·상태 셀렉트 확인

## 반영

- 2026-10-05 운영 반영: kknaks/Strong_hajin#11 squash `202078b` → 이미지 `202078b-arm64`(front·back) → MediSolveAIDev/k8s_infra_mac#9(태그 한 줄, merge `a626312`) → Argo 수동 sync Synced/Healthy 8/8. web 200 · /health production · providers 데모 계정 없음 · 새 번들 로그인 문구 확인 · back 로그 오류 0
- 데스크톱(medi-ax dmg): **pending** — macOS 실기(AC-T44·45·49 · 회의 자료 PDF 미리보기) 확인 뒤 재빌드·서명·공증(RUNBOOK-002 §3). Windows pending

## Rollback

- `values-prod.yaml` 태그를 직전 값(`d1b5137-arm64`)으로 되돌려 머지 → 수동 sync. 스키마·서버 변경이 없으므로 데이터 되돌림 없음
- 데스크톱: 직전 dmg 를 다시 설치

## Done Criteria

- R1~R6 · g 의 계약 체크가 모두 채워졌고 화면 확인 증거가 있다(macOS 앱 포함, Windows 는 pending 표시)
- 운영에 반영됐다

## Open Issues

| ID | 무엇 | 다음 |
|---|---|---|
| — | (진행 중 생기면 적는다) | — |

## Related

- `_RESUME.md` — 요청 원문과 결정 이력
- RUNBOOK-002 — 운영 반영 절차
