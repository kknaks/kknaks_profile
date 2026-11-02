# [reviewer] 회의록 시안 대조 3 — 회의록 상세 · 편집

너는 **task-management `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app` (코디 워크트리 · **문서 레포**)

---

## 0. 왜 이 일을 하나

**이 프로젝트의 SPEC 은 시안(`.dc.html`)을 한 번도 열지 않고 쓰였다.**
코디가 디자이너의 글 요약본만 읽고 SPEC 을 썼고, 그 결과 만든 화면 7개를 전부 버린 적이 있다(`32f8357`).
로그인·내 업무는 시안으로 다시 맞췄고, **회의록은 아직 손대지 않았다.**

회의록 구현에 들어가기 전에 **SPEC 이 시안과 얼마나 어긋나는지** 먼저 안다.

## ⛔ 1. 네가 하는 일 — **찾기만 한다. 고치지 않는다**

- **문서를 수정하지 마라.** SPEC·정책서·기획서·ERD 어느 것도 고치지 않는다
- **코드를 만들지 마라**
- **어느 쪽이 맞는지 판정하지 마라** — 시안이 낡았을 수도, SPEC 이 틀렸을 수도 있다. **그건 사용자가 정한다**
- 네 산출물은 **리포트 파일 하나**뿐이다

**「이건 이렇게 하는 게 낫다」를 쓰지 마라.** 제안이 아니라 **대조 결과**를 낸다.

## 2. 대조할 것

### 시안 — **여기가 정본이다. 전부 열어라**

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/00-design/회의록.dc.html
```

**네 담당 줄 범위: 1403 ~ 2939**

| 시안 화면 | 줄 |
|---|---|
| 회의록 · 상세 | **1403~1607** |
| 상세 · 근거 펼침 | **1608~1823** |
| 상세 · 편집 중 | **1824~2041** |
| 편집 중 · 논의 · 결정 추가 | **2042~2305** |
| 편집 중 · 연관 업무 추가 | **2306~2599** |
| 편집 중 · 액션 아이템 추가 | **2600~2939** |

> **다른 담당자가 나머지를 본다. 네 범위 밖은 읽지 마라**(중복 보고를 만들지 않는다).
> 단 **디자인 시스템**은 봐야 한다 — `00-design/디자인 시스템.dc.html` 의 **09 MEETING NOTE**(651~755줄)가 회의록 전용 패턴(줄 종류 4종 · 근거 아코디언 · 탭 dot · AI 요약 바)을 정의한다.

### 문서 — 이것과 대조한다

| 문서 | 경로 |
|---|---|
| **담당 SPEC** | `20-spec/spec-008-meeting-close.md` (542줄) |
| 정책서 | `10-decision/decision-003-meeting-notes.md` |
| 기획서 | `00-baseline/baseline-003-meeting-notes.md` |
| ERD | `40-architecture/database/domains/meeting.md` |
| 프론트 아키텍처 | `40-architecture/frontend/README.md` |
| **정정 목록** | `orchestration/work/docs-v1/design-requests.md` §A |

> **⚠ `00-design/*.md` 요약본(`12-meeting-notes.md` 등)을 열지 마라.** 그것이 이 사고의 원인이다.
> **⚠ 정정 A-5·A-6·A-7·A-8·A-11 은 회의록 항목이다.** 이미 승인된 정정이므로 **그 자리는 「시안이 낡은 것」**이다. 어긋남으로 보고하되 **「정정 A-x 로 이미 닫힘」**이라고 표시해라.

## 3. 리포트 — 이 형식으로만

산출물: `orchestration/work/docs-v1/meeting-review3-report.md`

```markdown
# 회의록 시안 대조 3 — 회의록 상세 · 편집

## 요약
- 화면 n개 · 대조 항목 n건
- 어긋남 n건 (신규 n · 정정으로 닫힘 n)
- **시안에 있는데 SPEC 에 없음** n건
- **SPEC 에 있는데 시안에 없음** n건

## 어긋남 목록

### M-1. <한 줄 제목>
| | |
|---|---|
| 시안 | `회의록.dc.html` L1234 — <실제로 그려진 것. 값까지> |
| 문서 | `spec-00x.md` L56 — <적힌 것> |
| 종류 | 시안에만 있음 / 문서에만 있음 / 값이 다름 / 정정으로 닫힘(A-x) |
| 영향 | <이대로 구현하면 무슨 일이 나는가. 한 줄> |

(M-2, M-3 … 심각한 것부터)

## 시안에 없어서 정해야 하는 자리
- <시안에도 문서에도 답이 없는 것>

## 판단하지 않은 것
- <애매해서 넘긴 것과 그 이유>
```

**규칙**
- **모든 항목에 시안 줄 번호와 문서 줄 번호를 단다.** 못 대면 쓰지 마라
- **값을 적어라** — 「색이 다르다」가 아니라 「시안 `#7181F8` / SPEC 「선택색」」
- **추측을 쓰지 마라.** 애매하면 §「판단하지 않은 것」에 넣어라
- 심각도 순으로 정렬 — **구현이 통째로 달라지는 것**이 위, 색·간격이 아래

## 4. 지킬 것

1. **찾기만 한다.** 문서·코드를 고치지 마라
2. **네 시안 줄 범위 밖을 보지 마라**(디자인 시스템 09 는 예외)
3. **줄 번호 없는 항목을 쓰지 마라**
4. **커밋·push 하지 마라**
5. 막히면 물어라 — `orca terminal send`. `orca orchestration ask` 는 답이 안 닿는다

## 5. Done Criteria

- [ ] 담당 시안 화면을 **전부** 열었다
- [ ] 담당 SPEC 을 **전부** 읽었다
- [ ] 정책서·기획서·ERD 와도 대조했다
- [ ] 모든 어긋남에 **시안 줄 + 문서 줄**이 달려 있다
- [ ] 정정 A-5~A-8·A-11 에 해당하는 것은 **「정정으로 닫힘」** 표시
- [ ] 리포트 파일 1개 외에 **아무것도 만들지 않았다**

---

## 6. 질문하는 법 — **`orca orchestration ask` 를 쓰지 마라**

```bash
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \\
  --text "[질문] reviewer3: <질문>" --enter
```

## 7. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \\
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \\
  --type worker_done \\
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \\
  --subject "reviewer3 완료: <어긋남 n건>" \\
  --body "리포트 경로 / 어긋남 건수(신규·정정닫힘) / 가장 심각한 3건 요약 / 정해야 할 자리 / 판단 안 한 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \\
  --text "[worker_done] reviewer3 완료 — 어긋남 <n>건. 상세는 인박스." --enter
```
