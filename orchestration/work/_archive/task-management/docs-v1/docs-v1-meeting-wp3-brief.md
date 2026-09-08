# [architect] SPEC-008 결정 반영 + WORK-008 작성

너는 **task-management `architect` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/architect/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app` (문서 레포 · 코디 워크트리)

**산출물 2개**
1. `para/projects/summer-star/task-management/20-spec/spec-008-meeting-close.md` — **수정**(네가 방금 쓴 것)
2. `para/projects/summer-star/task-management/30-work/work-008-meeting-close.md` — **신규 작성**

**네가 올린 OQ 2건에 사용자 결정이 내려졌다. 아래 §2 가 그 답이다. 둘 다 「넣는다」로 닫혔다.**

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

## 4. SPEC-008 에 반영할 것 — **네 OQ 2건이 여기서 닫힌다**

### 4-1. 결정 ① AI 한 줄 요약 바 (`S008-OQ-1` 닫힘)

- **U-1 「생성중」** — 스피너 단계 문구에 한 줄 요약 생성이 ② 통합본 생성 안에 포함됨을 반영
- **U-3 상세 페이지** — **상단 `top 150 · 1640×56` 자리에 한 줄 요약 바를 그린다.**
  회의 중에는 SPEC-007 U-1 의 회색 상태 바가 있던 그 자리다. 규격은 디자인 시스템 **[09] L727~733**
- **U-4 회의 상세 드로어** — 드로어에도 한 줄 요약을 보여줄지 판단해서 U-4 에 명시해라(840 폭 안에서의 배치)
- **§4** — `POST /integrate` 의 통합 출력에 **`headline`** 필드를 더한다.
  **별도 호출·별도 엔드포인트를 만들지 마라** — 통합 응답에 필드 하나가 붙는 것이다
  - `MeetingDetail.headline` (SPEC-006 이 정본 스키마를 갖는다 — 필드 존재만 맞추고 정의는 SPEC-006 에 맡겨라)
  - **우측 카운트 「안건 n · 결정 n · 액션 n」의 출처**를 §4 에 정의해라(파생인지 저장인지)
  - **통합 실패 시 `headline` 은 어떻게 되나** — DEC-003 §7 「통합본 생성 실패 → 사람 원본 노출 + 배너」와 맞춰라
- **§6 Acceptance** 에 한 줄 요약 항목 추가
- **§7 제외 목록에서 「요약 문단」과 「한 줄 요약」을 구분**해라 — 한 줄은 살았고 **문단 요약은 계속 제외**다

### 4-2. 결정 ② 줄 삭제 · 안건 이름 수정 (`S008-OQ-2` 닫힘)

**§7 제외 목록에서 「편집 중 안건 제목 입력 상자 L1894 · L1924 · L1959(+복제 9곳)」를 빼내 계약으로 올려라.** 시안이 맞았다.

- **U-7 편집 모드** — 줄 우측 **「제거」** + **안건 제목 인라인 입력**. 규격은 시안 L1894 계열 + 디자인 시스템.
  **포커스 해제 자동 저장**(DEC-003 §5)이 삭제에도 적용되는지 판단해서 명시해라 — 삭제는 확인이 필요한 동작일 수 있다
- **§4** — 줄 삭제 `DELETE …/lines/{id}` · 안건 이름 `PATCH …/agendas/{id} { title }`
  (SPEC-006·007 의 안건 표면과 **한 계약**이어야 한다 — 이름이 갈리면 §7 에 적어라)
- **경계 셋을 §4·§5 에 못박아라** — §2 결정 ② 의 ①②③. 특히
  - **삭제는 `merged` 트랙만.** `human`·`ai` 줄과 트랜스크립트·녹음은 남는다
  - **`source_human_line_id`·`source_ai_line_id` 로 이어진 원본은 지우지 않는다** — 근거 칩이 죽지 않아야 한다
  - **업무가 생성된 줄을 지워도 `task` 는 남는다.** `POST /lines/{id}/task` 로 만든 업무와의 연결이 끊어질 때 무엇이 남는지 §4 에 정의해라
- **「되돌리기」는 계속 제외**다(L1883 계열) — 삭제가 생겼다고 이력을 만들지 마라. 정책은 여전히 자동 저장이다
- **줄 순서 변경은 계속 없다**
- **§6 Acceptance** 에 삭제·안건 이름 항목 추가

### 4-3. 정합 — 네가 §7 정합 표에 올린 12건

- **`SPEC-009` L41·L166·L282·L429·L474 는 코디가 이미 U-4 로 고쳤다.** 네가 다시 만지지 마라
- **`SPEC-006` L40·L72·L177·L666·L697(U-8→U-4) · L252(U-2→U-1) 는 SPEC-006 워커가 고친다.** 만지지 마라
- **네가 처리할 것**
  - `MeetingDetail` 필드 이름 — **정본은 SPEC-006** 이다. 네가 더한 `durationMinutes`·`activeJobId`·`finalBatchState`·`mergedSummary` 가 SPEC-006 의 `tracks.human/ai`·`aiBatchSeq` 와 한 벌이 되게 맞춰라
  - `invalid_meeting_status` vs `meeting_not_recording` — SPEC-006·007 워커가 판단 중이다. **네 §4 가 어느 쪽을 쓰는지 §7 에 적어라**
  - 안건 `next` 배지 「대기」 vs 「다음으로」 — 하나로 맞추고 §7 에 적어라
  - **`paused_stream` 에서 재개 불가 시 회의를 닫을 길이 없다** — 네가 인지로 올린 것이다.
    **실제로 막다른 길이면 §7 에 진짜 OQ 로 올려라.** SPEC-007 워커도 같이 보고 있다

## 5. WORK-008 에 담을 것

- **Covers spec: SPEC-008**(회의록 — 종료 · 통합 · 편집 · 업무 연동)
- **Depends on work**: **WORK-006**(`meeting` 도메인 · `MeetingDetail`) · **WORK-007**(AI 배치 · `AgendaLineTree` · 근거 칩 · 트랜스크립트) · **WORK-005**(`PATCH /api/tasks/{id}/status` · 완료 게이트) · **WORK-004**(`task_service` 생성·부분 수정 · `task_memo`) · **아키텍처 반영분**(ERD — `source_human_line_id`/`source_ai_line_id` · `job`)
- **선행 WP 가 이미 못박은 것 — 지켜라**
  ```
  work-005 L137  회의록의 「업무 갱신」이 상태를 완료로 보낼 때 PATCH /api/tasks/{id}/status
                 하나를 지난다 — 회의록 쪽에 판정 코드를 두지 않는다(BE §8-3)
  work-005 L147  task.status 를 대입하는 코드는 task_service.change_status() 안에만 있다
  work-004 L156  회의록의 「업무 생성」·「업무 갱신」이 task_service 를 그대로 부른다
  ```
- **`AgendaLineTree` 는 WORK-007 것이다** — 통합본 탭도 **같은 컴포넌트**를 쓴다. 두 번째 구현을 만들지 마라
- **넘겨줄 내부 접점** — `job` 테이블·폴링 · 통합 규칙 구조 검증 · 편집 모드 · 추가 드로어 3종 · 회의 상세 드로어(**캘린더가 재사용한다** — DEC-005 §2)
- **Phase 에 「업무 연동」을 독립으로 두어라** — 완료 게이트를 우회하지 않는지 **검증 항목**으로 확인해야 한다(`work-005` L294)

## 6. WP 작성 규칙

**템플릿은 `30-work/work-004-tasks-crud.md` · `work-005-tasks-status-views.md` 다.** 섹션 구성을 그대로 따른다 —

```
frontmatter(type/id/title/status/product/work_type/roles/progress/links)
Meta · Work Summary · Role Assignment · Scope · Code Surface · Domain / Schema
Dependency · Internal Interface Contract · Execution(Phase) · Pre-deploy Check
Rollback · Done Criteria · Open Issues · Related
```

- **SPEC 의 외부 계약 본문을 복제하지 마라.** `links.specs` 로 연결하고, WP 는 **빌드 계획**만 담는다
- **Internal Interface Contract 에는 후속 WP 가 의존하는 내부 접점만** 적는다(컴포넌트·서비스 함수·테이블)
- **Execution 은 Phase 로 쪼개고** 각 Phase 에 `be`/`fe` 담당과 검증 방법을 적는다
- **Code Surface 는 실제 경로**로 적는다 — 백엔드 `app/back/{api,service,repository,schemas,dto,models}`, 프론트 `app/front/src/{app,features,components,lib}`.
  코드 레포는 **별도**다: `github.com/kknaks/task_management`
- **Done Criteria 는 SPEC §6 Acceptance 항목 수와 맞춘다**

## 7. 지킬 것

1. **기획·정책에 없으면 만들지 마라.** 시안에 있어도
2. **기획·정책에 있으면 만들어라.** 시안에 없어도 — 디자인 시스템으로 조립
3. **정책을 뒤집지 마라.** 충돌은 OQ 로
4. **네 담당 파일 2개(SPEC 1 · WP 1)만 고친다.** 다른 SPEC·WP·기획·정책·아키텍처·인덱스·시안을 건드리지 마라
   — 워커 4명이 같은 워크트리에서 **동시에** 돈다. 남의 파일을 만지면 덮어쓴다
5. **커밋·push 하지 마라**
6. 막히면 물어라 — `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "..." --enter`

## 8. Done Criteria — 코디가 이걸로 검수한다

- [ ] **결정 ①·② 가 SPEC 에 반영**됐다 — 해당 U-n · §4 계약 · §6 Acceptance 세 곳 전부
- [ ] §7 의 「기획·정책에 없어 제외」 목록에서 **결정으로 살아난 항목을 옮겼다**(제외 → 계약)
- [ ] **기획·정책에 없는 기능이 계약에 0건**이다
- [ ] **OQ 마다 「어디를 찾았나」가 있다.** 가짜 OQ 0건
- [ ] WP 가 **템플릿 섹션 전부**를 갖고 있고 **Phase 마다 검증 방법**이 있다
- [ ] WP 의 Done Criteria 수 = SPEC §6 Acceptance 수
- [ ] **네 파일 2개 외에 아무것도 고치지 않았다**

## 9. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_e9fc284a-afbb-442b-aa52-8c3e2cd070fe \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "<네 SPEC> 반영 + <네 WP> 작성 완료" \
  --body "결정 ①·② 를 SPEC 어디에 어떻게 넣었나(U-n·§4·§6) / 제외 목록에서 살아난 항목 / 정합 반영분 / WP 의 Phase 구성과 Done Criteria 수 / OQ 건수와 각각의 「어디를 찾았나」 / 정책 충돌"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] <네 SPEC> + <네 WP> 완료. 상세는 인박스." --enter
```
