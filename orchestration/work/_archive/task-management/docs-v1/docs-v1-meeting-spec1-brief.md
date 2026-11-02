# [architect] 회의록 SPEC 재작성 1 — 회의록 생성 · 시작 전

너는 **task-management `architect` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/architect/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app` (코디 워크트리 · 문서 레포)

---

## 0. 왜 다시 쓰나

**지금 `spec-006-meeting-setup.md` 은 버린다. 처음부터 다시 쓴다.**

이 SPEC 은 **시안(`.dc.html`)을 한 번도 열지 않고** 쓰였다. 코디가 디자이너의 글 요약본(`00-design/*.md`)만 읽고 썼고,
그 결과 **어긋남 66건**이 나왔다(리뷰어 3명이 시안 전체를 대조했다). 같은 원인으로 **이미 화면 7개를 버린 적이 있다**(`32f8357`).

**시안에 있는데 SPEC 에 없어서 구현이 막히는 자리**가 여럿이다 — 회의 「장소」 필드가 네 문서에 grep 0건, 첨부 POST 규격 부재,
통합본 생성 시각이 응답 계약에 없음, 취소된 회의가 status enum 에 없음. **시안을 빼고 봐도 못 만드는 상태**다.

**이번엔 시안이 정본이다. 전 화면을 열고 쓴다.**

## ⛔ 1. 절대 규칙

1. **`00-design/*.md` 요약본을 열지 마라.** `12-meeting-notes.md` 가 이 사고의 원인이다. **`.dc.html` 만 본다**
2. **네 담당 시안 화면을 전부 연다.** 하나도 빠뜨리지 마라
3. **모든 화면 계약에 시안 줄 번호를 단다** — 「시안 L1234」. **줄 번호를 못 대는 값을 쓰지 마라**
4. **시안에 없는 자리는 지어내지 말고 §Open Questions 에 남긴다.** 「이렇게 하는 게 낫다」로 채우지 마라
5. **정책서(DEC-003)를 뒤집지 마라.** 정책은 논의로 확정됐고 시안과 무관하다. 충돌하면 **고치지 말고 OQ 로 올려라**
6. **구현이 물을 것을 남기지 마라** — 화면에 값이 있으면 **그 값의 출처(컬럼·API 필드)를 §4 에 반드시 정의한다**

## 2. 입력 — 이것들을 전부 읽어라

| 무엇 | 경로 | 성격 |
|---|---|---|
| **시안** | `para/projects/summer-star/task-management/00-design/회의록.dc.html` **L24~760** | **시각 정본** |
| **디자인 시스템** | 같은 폴더 `디자인 시스템.dc.html` **09 MEETING NOTE**(L649~755) + 05·06·07·10 | 공통 규격 |
| **대조 리포트** | `orchestration/work/docs-v1/meeting-review1-report.md` | **어디가 왜 틀렸는지 이미 정리돼 있다. 먼저 읽어라** |
| 정책서 | `para/.../10-decision/decision-003-meeting-notes.md` | **동작 정본. 뒤집지 마라** |
| 기획서 | `para/.../00-baseline/baseline-003-meeting-notes.md` | 왜 만드나 |
| ERD | `para/.../40-architecture/database/domains/meeting.md` | 스키마 |
| 백엔드 아키텍처 | `para/.../40-architecture/backend/README.md` | 계층·에러 규약 |
| 프론트 아키텍처 | `para/.../40-architecture/frontend/README.md` | 라우트·상태·토큰 |
| 정정 목록 | `orchestration/work/docs-v1/design-requests.md` §A | **A-5·A-6·A-7·A-8·A-11 이 회의록. 시안보다 우선한다** |
| 기존 SPEC | `para/.../20-spec/spec-006-meeting-setup.md` | **참고만. 근거로 쓰지 마라** |
| 같은 계열 표본 | `para/.../20-spec/spec-003-tasks-crud.md` · `spec-004-tasks-status-views.md` | **형식·깊이의 기준** |

### 담당 시안 화면 (4개 · 전부 열어라)

| 화면 | 줄 |
|---|---|
| 회의록(목록) | **24~231** |
| 회의록 · 새 회의록 드로어 | **232~541** |
| 회의 시작 전 | **542~649** |
| 회의 시작 전 · 첨부 파일 | **650~760** |

## 3. 산출물

**`para/projects/summer-star/task-management/20-spec/spec-006-meeting-setup.md` 를 덮어쓴다.**

구조는 **SPEC-003·004 와 같게** 한다(그 둘이 지금 레포에서 가장 정확한 SPEC 이다) —

```
1. Context     — Meta(근거 문서) · Business Requirement · Scope(In/Out)
2. UX Contract — Placement + U-1..U-n (화면마다 상태·문구·CTA·기대 결과)
3. Scenarios   — S-1.. 사용자 시나리오
4. Data Contract — API 표 · Request/Response · Validation · **Case Matrix(에러)**
5. Flow        — mermaid
6. Acceptance  — 체크리스트
7. Open Questions — 시안·정책에 답이 없는 것
8. 근거 표     — 「이 결정이 어디서 왔나」
```

**§2 UX Contract 규칙**
- 화면 하나 = U-n 하나. **네 담당 시안 화면 전부가 U-n 을 갖는다**
- 각 U-n 에 **시안 줄 번호**를 단다
- **상태**(로딩·빈·실패·전이 중) · **문구**(실제 한국어) · **CTA** · **기대 결과** 넷을 반드시 쓴다
- 값은 **실측**을 적는다 — 「h42 · r12 · 13/700 · 우측 힌트 12px \`#9EA2AE\`」처럼

**§4 Data Contract 규칙 — 여기가 이번 재작성의 핵심이다**
- **화면에 나오는 모든 값의 출처를 정의한다.** 컬럼이 없으면 **ERD 에 필요하다고 §7 에 올려라**
- API 표 · 요청/응답 JSON 예시 · Validation 표 · **Case Matrix(에러코드·detail·화면 표시·위치)**
- **에러코드를 발명하지 마라** — 기존 코드를 재사용하거나 **새로 필요하면 Case Matrix 에 행을 추가하고 근거를 적어라**
- 백엔드 계층 규약(`backend/README.md`)을 어기지 마라

## 4. 지킬 것

1. **시안 전 화면을 열고 줄 번호를 단다**
2. **정책을 뒤집지 마라.** 충돌은 OQ 로
3. **시안에 없는 것을 지어내지 마라.** OQ 로
4. **화면에 있는 값의 출처를 §4 에 반드시 정의한다** — 구현이 물을 것을 남기지 않는다
5. **네 SPEC 파일 1개만 고친다.** 정책서·기획서·ERD·다른 SPEC 을 건드리지 마라
6. **커밋·push 하지 마라**
7. 막히면 물어라 — `orca terminal send`. `orca orchestration ask` 는 답이 안 닿는다

## 5. Done Criteria

- [ ] 담당 시안 화면을 **전부** 열었고, **모든 U-n 에 시안 줄 번호**가 있다
- [ ] 대조 리포트의 어긋남을 **전부 반영**했다(반영 못 한 것은 OQ 에)
- [ ] **화면에 나오는 모든 값의 출처가 §4 에 있다** — 없는 컬럼·필드는 §7 에 「ERD 변경 필요」로
- [ ] Case Matrix 가 있고 **에러코드마다 detail·화면 문구·표시 위치**가 있다
- [ ] 정책서를 뒤집은 곳이 **없다**(충돌은 OQ)
- [ ] SPEC-003·004 와 **같은 구조·같은 깊이**다
- [ ] 파일 1개 외에 **아무것도 만들거나 고치지 않았다**

---

## 6. 질문하는 법

```bash
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \\
  --text "[질문] architect1: <질문>" --enter
```

## 7. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \\
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \\
  --type worker_done \\
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \\
  --subject "architect1 완료: spec-006-meeting-setup.md 재작성" \\
  --body "U-n 개수와 시안 줄 / 리포트 반영 건수 / §4 에서 새로 정의한 계약 / ERD 변경 필요 목록 / Open Questions / 정책 충돌"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \\
  --text "[worker_done] architect1 완료 — spec-006-meeting-setup.md 재작성. 상세는 인박스." --enter
```
