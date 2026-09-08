# [architect] SPEC-007 결정 반영 + WORK-007 작성

너는 **task-management `architect` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/architect/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app` (문서 레포 · 코디 워크트리)

**산출물 2개**
1. `para/projects/summer-star/task-management/20-spec/spec-007-meeting-live.md` — **수정**(네가 방금 쓴 것)
2. `para/projects/summer-star/task-management/30-work/work-007-meeting-live.md` — **신규 작성**

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

## 4. SPEC-007 에 반영할 것

**결정 ① AI 한 줄 요약 바** — 네 U-1 상태 바와 **같은 자리**를 쓴다(`top 150 · 1640×56`).
회의 중에는 회색 상태 바, 종료 후에는 파란 한 줄 요약 바다. **U-1 에 「이 자리는 종료 후 SPEC-008 의 한 줄 요약 바로 바뀐다」를 명시**하고, 규격 충돌이 없는지 확인해라. 회의 중 화면에 한 줄 요약을 그리지는 않는다.

**결정 ② 줄 삭제·안건 이름 수정** — 종료 후 편집이라 SPEC-008 소관이다. **다만 확인할 것 둘**:
- **회의 중에는 줄 삭제가 없다**(정책은 「종료 후 편집」에만 넣었다). 네 U-2 사람 트랙이 그렇게 돼 있는지 보고, 시안에 삭제 UI 가 있으면 §7-B 에 적어라
- 회의 중 안건 이름 수정 가능 여부 — `PATCH …/agendas/{id}` 가 지금 `state` 만 받는다. **`title` 도 받는지**를 SPEC-006(시작 전 안건 수정) 및 SPEC-008(종료 후)과 맞춰 하나로 정하고 §7-D 에 적어라

**정합 — 네가 §7-D 에 올린 것 중 네가 처리할 것**

| # | 무엇 | 어떻게 |
|---|---|---|
| D-3 | **`/end` 사전 조건** — `paused_stream`(WS 없음)에서 「회의 종료」를 **비활성**으로 두었다 | SPEC-008 워커가 같은 규칙으로 쓴다. 네 U-1 에 **「재개하지 않으면 종료할 수 없다」**가 명시돼 있는지 확인해라. **SPEC-008 이 「paused_stream 에서 재개 불가 시 회의를 닫을 길이 없다」를 정합 표에 올렸다** — 이게 실제로 막다른 길인지 판단해서, 막다른 길이면 §7-E 에 진짜 OQ 로 올려라 |
| D-4 | 상세 응답 필드 이름 | **`MeetingDetail` 의 정본은 SPEC-006 이다.** SPEC-006 워커가 `tracks.human/ai` · `aiBatchSeq` 로 맞춘다. 네 §4 가 그 이름을 쓰는지 확인해라 |
| — | `meeting_not_recording`(네 신설) vs `invalid_meeting_status`(SPEC-006) | **둘이 같은 상황인지** 판단해서, 같으면 하나로 줄이고 §7 에 적어라 |
| — | 안건 `next` 배지 문구 「다음으로」 vs 「대기」(SPEC-008) | 하나로 맞추고 §7 에 적어라 |

**D-1 · D-2 · D-7(아키텍처 문서 정정)은 네가 하지 마라** — 별도 워커가 같은 시각에 `40-architecture/` 를 고치고 있다.

## 5. WORK-007 에 담을 것

- **Covers spec: SPEC-007**(회의록 — 회의 중 · STT 중계 · 2트랙 · AI 배치 · 일시정지)
- **Depends on work**: **WORK-006**(`meeting` 도메인 · `MeetingDetail` · 첨부 팝오버·드로어 · 안건 표면) · **아키텍처 반영분**(ERD — `recording_started_at` · `agenda.state active` · `source_agenda_id`)
- **Follow-up**: WORK-008(종료·통합·편집)
- **이 WP 가 제품에서 기술 난도가 가장 높다**(BASE-003 L53) — WS 2단 중계 · 배치 세션 유지 · 화자 분리 · 실패 처리. **Phase 를 그에 맞게 쪼개라**
- **환경 변수** — `SONIOX_API_KEY` 가 `.env` 에 이미 들어와 있다. **`.env.example` 에 자리를 추가하는 것**을 Phase 에 넣어라. **값을 문서에 쓰지 마라**
- **넘겨줄 내부 접점** — WS 엔드포인트 · Soniox 중계 · 녹음 적재 · 배치 트리거·세션 · `AgendaLineTree`(**회의록 탭과 AI 탭이 같은 컴포넌트**, 차이는 props 로만 — WORK-008 통합본 탭도 같은 것) · 근거 칩 스크롤·하이라이트
- **일시정지가 마이크 실패·스트림 끊김의 처리 경로**다(DEC-003 §1 표) — Phase 에 그렇게 담아라

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
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_95f47648-153b-4ec8-a4e4-97e9d0bebae3 \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "<네 SPEC> 반영 + <네 WP> 작성 완료" \
  --body "결정 ①·② 를 SPEC 어디에 어떻게 넣었나(U-n·§4·§6) / 제외 목록에서 살아난 항목 / 정합 반영분 / WP 의 Phase 구성과 Done Criteria 수 / OQ 건수와 각각의 「어디를 찾았나」 / 정책 충돌"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] <네 SPEC> + <네 WP> 완료. 상세는 인박스." --enter
```
