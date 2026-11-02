# [architect] SPEC-006 결정 반영 + WORK-006 작성

너는 **task-management `architect` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/architect/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app` (문서 레포 · 코디 워크트리)

**산출물 2개**
1. `para/projects/summer-star/task-management/20-spec/spec-006-meeting-setup.md` — **수정**(네가 방금 쓴 것)
2. `para/projects/summer-star/task-management/30-work/work-006-meeting-setup.md` — **신규 작성**

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

## 4. SPEC-006 에 반영할 것

**결정 ① AI 한 줄 요약 바**
- **U-8 우측 미리보기 패널**(L148~228) — 종료된 회의(`status='ended'`)를 미리보기할 때 **한 줄 요약 바**가 보이는 자리다.
  네가 §7 에서 **「요약 문단 + AI 생성 배지」(L167~174 · L375~382)를 제외**했는데, 그 이유가 「ERD 는 `ai_headline` **한 줄**뿐」이었다.
  이제 **한 줄 요약은 확정됐다** — **한 줄 바는 넣고, 문단 요약은 계속 제외**한다. 두 개를 구분해서 §7 표를 고쳐라
- **§4 `MeetingDetail`** 에 `headline` 필드를 명시한다(생성 시점은 SPEC-008 종료 파이프라인 ②)
- **목록 `items[]`** 에도 한 줄 요약이 필요한지 시안 L167~174 를 보고 판단해 계약에 담아라

**결정 ② 줄 삭제·안건 이름 수정** — SPEC-006 범위 밖이다(종료 후 편집은 SPEC-008). **다만 확인할 것 하나**:
시작 전 안건은 이미 수정·삭제가 되는지 네 U-4 를 다시 보고, **종료 후와 규격이 갈리면** §7 에 적어라.

**정합 — SPEC-007·008 이 올린 것**

| # | 무엇 | 어떻게 |
|---|---|---|
| D-4 | **상세 응답 필수 필드** — SPEC-007 이 읽는 것: `status` · **`recordingStartedAt`** · `title` · `startAt` · `workType{name,colorToken}` · `tracks.human{agendas[],lines[]}` · `tracks.ai{...}` · **`aiBatchSeq`** · `attachments[]`(`kind`·`name`·`documentId`·`folderPath`·`url`·`sizeBytes`·`updatedAt`) | 네 §4 는 `agendas.{human,ai,merged}` · `latestBatchSeq` 로 썼다. **이름이 갈렸다** — 하나로 맞춰라. SPEC-008 은 여기에 `durationMinutes`·`activeJobId`·`finalBatchState`·`mergedSummary` 를 더한다. **`MeetingDetail` 의 정본은 SPEC-006 이다** |
| D-5 | **안건 `POST …/agendas { title }` 를 회의 중에도 재사용**(SPEC-007 U-3) · **첨부 드로어를 시작 전 화면에서도 같은 것으로** | 네 §4·U-7 에 「회의 중에도 이 표면을 쓴다」를 명시 |
| — | **`SPEC-008 U-8` 참조 5곳(L40 · L72 · L177 · L666 · L697) → `U-4`** | SPEC-008 의 회의 상세 드로어는 **U-4** 다. 코디가 SPEC-009 는 이미 고쳤다 |
| — | **`SPEC-006 L252` 의 `U-2` → `U-1`** | SPEC-008 이 올린 것. 확인하고 맞다면 고쳐라 |
| — | `invalid_meeting_status`(네 것) vs `meeting_not_recording`(SPEC-007 신설) | **둘이 같은 상황을 가리키는지** 판단해서, 같으면 하나로 줄이고 §7 에 적어라 |
| — | 안건 `next` 배지 문구 「대기」(SPEC-008) vs 「다음으로」(너) | 하나로 맞추고 §7 에 적어라 |

## 5. WORK-006 에 담을 것

- **Covers spec: SPEC-006**(회의록 — 목록 · 생성 · 시작 전 · 첨부 · 삭제)
- **Depends on work**: WORK-003(동적 유형) · WORK-004(`DrawerFrame` · `Selector` · 첨부 팝오버 `SPEC-003 U-7` · `schedule_service`) · **아키텍처 반영분**(ERD 5건 — 별도 워커가 같은 시각에 반영 중)
- **Follow-up**: WORK-007(회의 중) · WORK-008(종료·편집) · 캘린더 그룹
- **넘겨줄 내부 접점** — `meeting` 도메인 · `meeting_router` · `MeetingDetail` 스키마 · 셀렉터 하단 「+ 새 프로젝트」 인라인 행(**전 영역 공통 규격, SPEC-006 이 정본**) · 첨부 팝오버·파일 드로어 · 삭제 모달
- **`work-004-tasks-crud.md` L155 가 이미 못박은 것** — 「WORK-006 이 `schedule_service`(겹침 검사 + 파생)를 그대로 쓴다. **두 번째 구현을 만들지 않는다**」

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
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_3e6440a0-ca97-418b-b8f4-f4c32e53a5a8 \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "<네 SPEC> 반영 + <네 WP> 작성 완료" \
  --body "결정 ①·② 를 SPEC 어디에 어떻게 넣었나(U-n·§4·§6) / 제외 목록에서 살아난 항목 / 정합 반영분 / WP 의 Phase 구성과 Done Criteria 수 / OQ 건수와 각각의 「어디를 찾았나」 / 정책 충돌"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] <네 SPEC> + <네 WP> 완료. 상세는 인박스." --enter
```
