# [architect] 회의록 아키텍처 반영 — ERD · 코드표 · 시스템 흐름

너는 **task-management `architect` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/architect/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app` (문서 레포 · 코디 워크트리)

**산출물 — `40-architecture/` 아래 4파일만**
```
40-architecture/database/domains/meeting.md
40-architecture/database/README.md
40-architecture/backend/README.md
40-architecture/system/README.md
```
**SPEC·WP·기획·정책·시안을 건드리지 마라.** 지금 다른 워커 3명이 SPEC·WP 를 동시에 고치고 있다.

## 0. 지금 어디까지 왔나

2026-09-06, 회의록 SPEC 3개를 **폐기하고 다시 썼다.** 이전 판이 죽은 이유는 브리프가 **「시안이 정본」**을 박아서
워커가 **시안에 그려진 것을 전부 계약으로 옮겼기** 때문이다(AI 안건 생성기 · 되돌리기 · 파형 · 취소된 회의 · 내 목소리).

**재작성분은 검수를 통과했다** — SPEC-006(741줄) · SPEC-007(737줄) · SPEC-008(782줄), **OQ 0·0·2건**.
그 OQ 2건에 **사용자 결정이 내려졌고 정책 DEC-003 에 반영됐다.** 이 발주는 그 결정을 SPEC 에 반영하고, **WP 를 쓰는 것**이다.

## ⛔ 1. 정본 — 축을 나눈다 (지난 발주와 같다)

| 무엇 | 정본 |
|---|---|
| **기능** — 어떤 화면·필드·상태·흐름·문구·API 가 있나 | **기획 BASE-003 + 정책 DEC-003** |
| **시각** — 색·크기·간격·배치 | **디자인 시스템 + 시안 `.dc.html`** |

**판정은 기획·정책 한 축뿐이다.**

| 기획·정책 | 판정 |
|---|---|
| **있다** | **만든다.** 시안에 화면 없으면 **디자인 시스템 컴포넌트로 조립** |
| **없다** | **안 만든다.** 시안에 그려져 있어도 — §7 에 「시안 L### 에 있으나 기획·정책에 없어 제외」로 |

## ⛔ 2. 새로 내려온 사용자 결정 2건 — `DEC-003` 에 이미 반영돼 있다

**결정 ①  AI 한 줄 요약 바 — v1 에 넣는다** (`DEC-003` §1 표 · §4 종료 파이프라인)

```
언제 만드나   최종 배치가 끝나고 통합본을 만들 때 한 줄 요약까지 함께 받는다
              → 통합 출력에 필드 하나가 더 붙는 것이다. 별도 호출을 만들지 마라
저장          meeting.ai_headline  (database/README.md L202 에 컬럼이 이미 있다)
표시          디자인 시스템 [09] L727~733 그대로
              상세 상단 top 150 · 1640×56 한 개
              #EEF1FE / 테두리 #C9D1FB / 배지 「AI 한 줄 요약」 + 한 문장(넘치면 말줄임)
              + 우측 「안건 n · 결정 n · 액션 n」
자리          회의 중 회색 상태 바와 **같은 자리**를 쓴다
```

**결정 ②  종료 후 편집에 「줄 삭제」와 「안건 이름 수정」을 넣는다** (`DEC-003` §1 표 · §5 수정(U))

```
넣는 것       줄 삭제 · 안건 이름 수정
안 넣는 것    줄 순서 변경 (여전히 없다)

경계 셋 — 기존 정책에서 따라온 것이다. 뒤집지 마라
  ① 삭제는 회의록 탭(통합본)에서만.
     AI 탭·트랜스크립트·녹음은 그대로 남는다(§6 「AI 탭은 통합본과 별개로 남는다」)
     — 근거 칩이 가리킬 원본이 있어야 한다
  ② 업무가 생성된 줄을 지워도 업무는 지우지 않는다(§8 「회의록은 업무를 만들고 갱신만」)
  ③ 안건은 이름만 고친다. 안건 삭제는 없다 —
     줄은 항상 안건에 속하므로(§3) 안건을 지우면 딸린 줄이 갈 곳이 없다
```

## ⛔ 3. OQ 규칙 — 지난 발주와 같다

**0 으로 맞추려고 덮지 마라. 대신 가짜 OQ 를 쓰지 마라.**

| 종류 | 무엇 | 처리 |
|---|---|---|
| **가짜** | 기획·정책·다른 DEC·기존 SPEC 에 답이 있는데 못 찾음 / **SPEC·WP 가 정하면 되는 것**(API 경로·에러코드·검증·수치·Phase 분할·파일 배치) | **쓰지 마라** |
| **진짜** | 기획·정책에 정말 없다 / 서로 충돌한다 | **§7 (WP 는 Open Issues) 에 올린다** |

**OQ 를 쓸 거면 항목마다 「어디를 찾았나 — 파일·섹션·grep 문자열·결과 건수」를 함께 적어라.** 없으면 반려한다.

## 4. 반영할 것 — 재작성된 SPEC 3개가 「ERD 변경 필요」로 올린 것

**출처를 반드시 열어라** — `20-spec/spec-006-meeting-setup.md` §7 · `spec-007-meeting-live.md` §7-C·§7-D · `spec-008-meeting-close.md` §7.
아래 표는 요약이다. **본문의 근거를 읽고 반영해라.**

### 4-1. `database/domains/meeting.md` · `database/README.md` — 컬럼

| 대상 | 변경 | 올린 곳 |
|---|---|---|
| `meeting.recording_started_at timestamptz NULL` | `/start` 성공 시각. **경과 시간의 기준이자 M-11 「`at_ms` 는 회의 시작 기준 오프셋」의 그 기준점.** `start_at`(예정)과 다르다 | SPEC-007 §7-C |
| `meeting_agenda.state` CHECK 에 **`active`** 추가 (`next \| active \| done`) | 「논의 중」 배지 · 프롬프트 바 활성 안건 · **안건 전환 배치 트리거**의 원천. 사람 트랙에 `active` 최대 하나 | SPEC-007 §7-C |
| `meeting_agenda.state` **NULL 허용** | 시작 전 안건은 상태가 없다 | SPEC-006 §7 |
| `meeting_agenda.source_agenda_id bigint NULL` (self FK) | `track='ai'` 안건이 미러하는 **사람 안건**. `NULL` = AI 신설 안건. 통합(`merged`)에서도 쓴다 | SPEC-007 §7-C · SPEC-008 §7 |
| `meeting_attachment` | `kind varchar CHECK (doc\|link)` · `url` · `label` 추가 · `document_id` **NULL 허용**. **M-17 「첨부는 자료함 문서 참조뿐」을 「md 문서 · URL 링크 두 갈래」로 갱신** | SPEC-006 §7 · SPEC-007 §7-C |
| `meeting_attachment` | `UNIQUE (meeting_id, document_id) WHERE document_id IS NOT NULL` | SPEC-006 §7 |
| `meeting_line.source_human_line_id` · `source_ai_line_id` (self FK, `track='merged'` 만) | 통합 계승. **`UNIQUE` 로 한 사람 줄의 이중 계승을 막는다**(DEC-003 OQ-7 「구조로 판정」) | SPEC-008 §7 |
| `meeting` 인덱스 | `(account_id, start_at) WHERE deleted_at IS NULL` 추가 | SPEC-006 §7 |
| `job` | `progress{phase, attempt}` · `errorCode` 3종 | SPEC-008 §7 · BE §6 |

**그리고 사용자 결정 2건이 낳는 것(§2)**

| 대상 | 변경 |
|---|---|
| `meeting.ai_headline` | **컬럼은 `database/README.md` L202 에 이미 있다.** `domains/meeting.md` 에 **M-n 규칙으로 올려라** — 언제 채워지나(종료 파이프라인 ② 통합본 생성과 **같은 응답**), 통합 실패 시 어떻게 되나, 재생성 없음(DEC-003 §4) |
| `meeting_line` 삭제 | **종료 후 `merged` 트랙에서만 줄을 지운다.** `human`·`ai`·`transcript`·녹음은 남는다. **`source_human_line_id`·`source_ai_line_id` 로 이어진 원본을 지우지 않는다**(근거 칩이 죽는다). 하드 딜리트인지 소프트인지 **결정하고 근거를 적어라** — 회의는 소프트 딜리트다(§4) |
| `meeting_agenda.title` | **종료 후 이름 수정이 생겼다.** 쓰기 경로가 시작 전·회의 중·종료 후 셋인지 확인하고 규칙으로 적어라 |
| **안건 삭제는 없다** | 줄은 항상 안건에 속한다(DEC-003 §3). 불변식으로 적어라 |

### 4-2. `database/domains/meeting.md` M-6 — **문구 정정**

```
지금   「사람 줄·사람 안건을 읽지도 고치지도 않고」
바꿈   「사람 줄·사람 안건을 고치지도 제안하지도 않는다」
```

**읽기(컨텍스트)는 기획·정책이 요구한다.**
- BASE-003 L36 「백엔드가 **사람 입력 + 트랜스크립트**를 워커로」
- BASE-003 L38 「사람이 적은 안건이 DB 에 있으니 **컨텍스트로 같이 전달**」
- DEC-003 §4 L96 「사람이 만든 안건을 **컨텍스트로 받아** 거기에 맞춰 채운다」
- DEC-003 §8 L149 웜스타트 = 「선택 프로젝트 + 그 프로젝트의 업무 + **미리 작성된 안건**」

`grep -n "읽지도" database/domains/meeting.md` → 1건. **기획·정책이 이긴다.**

### 4-3. `backend/README.md` §8-2 — 에러코드 표

| 코드 | 상태 | 올린 곳 |
|---|---|---|
| `invalid_meeting_status` | 409 | SPEC-006 · SPEC-009 |
| `meeting_not_recording` | 409 | SPEC-007 |
| `meeting_stream_active` | WS 4409 | SPEC-007 |
| `meeting_stream_disconnected` | 부기 `reason ∈ {upstream, write_failed}` | SPEC-007 |

> **주의** — SPEC-006·007·008 워커가 지금 **`invalid_meeting_status` 와 `meeting_not_recording` 이 같은 상황인지** 판단 중이다.
> **네가 결론내지 마라.** 표에는 **넷 다 넣되**, 「SPEC 이 통합 판정 중」이라고 각주를 달아라. 코디가 마감 때 정리한다.

### 4-4. `system/README.md` 흐름 ③

| # | 무엇 |
|---|---|
| 1 | **L230 「첫 프레임으로 access 토큰 인증」에 `audio{format, sampleRate, channels}` 선언이 함께 간다** (SPEC-007 §4 WS 계약) |
| 2 | **L243 배치 입력**이 「미처리 구간 + 안건 + 화이트리스트」로 돼 있다 — **사람 줄이 빠져 있다.** BASE-003 L36 대로 **사람 입력(줄) + 사람 안건**을 읽기 전용 컨텍스트로 넣어라 |

## 5. 지킬 것 — 이 워커 전용

1. **`40-architecture/` 아래 4파일만 고친다.** SPEC·WP·기획·정책·인덱스·시안 금지
2. **SPEC 이 올린 근거를 확인하고 반영한다.** 네가 새 구조를 발명하지 마라
3. **정책(DEC-003)을 뒤집지 마라.** 충돌하면 고치지 말고 보고에 적어라
4. **컬럼마다 「어느 SPEC 이 왜 요구했나」를 근거로 남겨라** — 나중에 왜 있는지 몰라 지우는 일이 없어야 한다
5. **커밋·push 하지 마라**

## 6. Done Criteria

- [ ] §4-1 컬럼 변경 **전부** 반영. 각각 근거(SPEC · 절) 병기
- [ ] `ai_headline` · `meeting_line` 삭제 · `meeting_agenda.title` 쓰기 경로 · 안건 삭제 없음 **4건이 규칙으로** 올라갔다
- [ ] M-6 문구가 정정됐다
- [ ] `backend/README.md` §8-2 에 코드 4건(각주 포함)
- [ ] `system/README.md` 흐름 ③ 두 곳
- [ ] **아키텍처 4파일 외에 아무것도 고치지 않았다**
- [ ] 정책을 뒤집은 곳이 없다

## 7. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_2dc83886-b1dd-4211-9f17-3058f4434623 \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "회의록 아키텍처 반영 완료" \
  --body "컬럼 변경 목록과 각각의 근거 SPEC / 새로 올린 규칙 4건 / M-6 정정 전후 / §8-2 코드 4건 / system 흐름 ③ 두 곳 / SPEC 과 어긋나 반영하지 못한 것 / 정책 충돌"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] 회의록 아키텍처 반영 완료. 상세는 인박스." --enter
```
