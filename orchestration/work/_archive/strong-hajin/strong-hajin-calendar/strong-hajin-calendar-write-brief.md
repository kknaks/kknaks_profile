# [writer] SPEC-004 — 캘린더 시간 배정. DEC-003 을 외부 계약으로 내린다

너는 **strong-hajin `writer` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin` ← **코디네이터 워크트리에 직접 탄다**
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

> ⚠ **코디 워크트리 공유.** 네가 쓰는 파일은 코디네이터가 보는 그 파일이다. **§5 가 허락한 파일 밖은 열지도 고치지도 마라.**
> ⚠ BASE-003 · DEC-003 은 방금 커밋됐다(`e6af151`). **네 산출물만 uncommitted 로 남아야** 코디가 `git diff` 로 검증한다. **커밋·push 하지 마라.**

## 1. SSOT — 먼저 읽을 것

**DEC-003 이 계약의 SoT 다. 여기 없는 것을 발명하지 마라. 여기 있는 것을 다시 정하지도 마라.**

- `para/projects/summer-star/strong-hajin/10-decision/decision-003-calendar.md` ← **정본.** 채택 A~J · 기각 · 보류 · 미결 0건
- `para/projects/summer-star/strong-hajin/00-baseline/baseline-003-calendar.md` ← 입력과 관측. 특히 「원문이 확정한 것」의 R1~R9 와 「조사가 뒤집은 전제 둘」
- `orchestration/work/strong-hajin-calendar/be-survey-report.md` (764줄) ← 백엔드 지형. 파일:줄 근거가 여기 있다
- `orchestration/work/strong-hajin-calendar/fe-survey-report.md` (727줄) ← 프론트 지형·상호작용 명세·DS-gaps

**형식의 본보기** (내용이 아니라 **형식**을 본다):

- `para/projects/summer-star/strong-hajin/20-spec/spec-003-task-lifecycle-v2.md` — 절 구성 `1. Context / 2. UX Contract / 3. User Scenario / 4. Interface Contract / 5. Implementation Rules / 6. Verification / 7. Open Questions`
- `para/projects/summer-star/strong-hajin/20-spec/README.md` — **§Data / Domain Boundary 를 반드시 읽어라.** 무엇을 spec 에 두고 무엇을 두지 않는지가 거기 있다

**기대는 개념**

- 해당 없음 — DEC-003 의 「근거 개념」(`soft-delete` · `single-source-of-truth`)을 그대로 인용하면 된다

## 2. 배경 / 무엇을 쓰나

업무는 **날짜 단위**로 산다(`start_date` · `due_date`). 시안은 그 위에 **시간 단위**를 얹는다 —
월~수짜리 업무에 「월요일 오전 10시 · 화요일 오후 2시 · 수요일 오전 9시」처럼 **그 기간 안에서**
시간을 배분하는 것이다. 회의는 이미 시간 축을 갖고 있고(`meetings`), 업무의 시간 배정만 없다.

**너는 SPEC-004 한 장을 쓴다.** DEC-003 이 정한 것을 client · QA · 외부 통합이 **이 문서만 읽고
따를 수 있는 외부 계약**으로 내리는 일이다. 새 판단을 하는 자리가 아니다.

## 3. 계약 (DEC-003 이 이미 정한 것 — 이대로 내려라)

각 항목의 **근거까지** DEC-003 본문에 있다. 요약만 옮기지 말고 계약 문장으로 펴라.

| DEC-003 | 무엇 |
|---|---|
| §A | 저장은 `meetings`(그대로) + `task_schedules`(새 표). 범용 schedules 표 없음. 제목·담당은 조인. 시각은 `Date` + `Time` + `Time`. 하루 한 칸(부분 unique) |
| §B | **배정이 사라지는 두 이유를 갈라서 건다** — 기간 밖은 **쓰기**(`released_at`), 업무 종료는 **읽기**(조회 필터) |
| §C | D5 의 「done」은 **내부 `DONE` 만**. `COMPLETION_SUBMITTED` 는 미완으로 보고 배정을 살린다 |
| §D | 가시성 **「내 것만」** — 업무 `my_work`(활성 담당) · 회의 `board`(참석·공유) |
| §E | 시안 R1~R9 를 그대로 계약으로 (BASE-003 「원문이 확정한 것 — 시간 배정」 표) |
| §F | 회의는 캘린더에서 **읽기 전용** — 끌 수도 늘릴 수도 없다 |
| §G | 날짜는 **ISO**. 달 경계 넘는 이동·조정 허용 |
| §H | `GET /api/meetings` 에 `from`/`to` 파라미터 추가 |
| §I | 금지는 **말로** 한다 (조용한 거절 금지, 선례 `WorkViews.tsx:520-522`) |
| §J | 실무 판정 16건 — 운영 대장 등록 · MCP 미노출(`excluded`/`E2`) · D1 세 자리 · `released_reason` 두 값 · 30분 CHECK 없음 · local-stack 표지 등록 등 |

**기각·보류도 읽어라.** 왜 그 길로 안 갔는지가 계약의 경계를 정한다.

## 4. 이 spec 이 반드시 담아야 하는 것

### 4-1. 두 소멸 경로를 **같은 절에 나란히** 적는다

DEC-003 §B 가 인정한 대가다 — 「왜 안 보이나」의 답이 둘이다. 읽는 사람이 헷갈리지 않게
**한 자리에서 가른다.** 각각 무엇이 트리거이고, 되돌릴 수 있는지, 화면에 어떻게 보이는지.

### 4-2. 상호작용 넷의 계약 (R1~R4)

`fe-survey-report.md` §1 이 시안 코드에서 뽑아 둔 명세가 있다. **금지 규칙까지** 계약으로 올려라 —
「업무 기간 밖에는 배정할 수 없다」가 UX 문구까지 포함해 계약이다(§I).

### 4-3. Interface Contract

- 배정 CRUD (생성·시각 변경). **삭제는 없다**(DEC-003 보류)
- 캘린더 조회 — 업무 + 회의 합본. 응답에서 `kind: 'meeting' | 'task'` 로 가른다
- `GET /api/meetings` 의 `from`/`to`
- 에러 코드와 그 문구 — 기간 밖 드롭, 낙관적 잠금 충돌, 권한

각 엔드포인트에 **운영 대장 등록 요구**를 명시하라(§J) — `status: excluded` · `policy: E2` ·
`exclusion.reason`·`reconsider_when` 까지. 선례는 `be-survey-report.md` 와 저장소의 excluded 6건.

### 4-4. Verification

무엇이 참이어야 이 계약이 선 것인지. 특히 **부분 unique 가 실제 PostgreSQL 에 선다**는 증명 —
`tests/integration/postgres/test_task_lifecycle_v2_schema_postgres.py` 의 선례를 따른다
("선언했다"가 아니라 "선다"를 증명한다).

## 5. allowed_paths — 이 밖은 건드리지 마라

쓰기가 허용된 파일은 **둘뿐**이다.

- `para/projects/summer-star/strong-hajin/20-spec/spec-004-calendar-scheduling.md` ← **새로 만든다**
- `para/projects/summer-star/strong-hajin/20-spec/README.md` ← Spec List·Bundle 표에 SPEC-004 **한 줄만** 추가

**절대 건드리지 마라**: `00-baseline/` · `10-decision/` · `30-work/` · `log.md` · `orchestration/` ·
그 밖의 모든 파일. DEC-003 에서 모순을 발견해도 **고치지 말고 §7 Open Questions 에 적어라.**

## 6. 진행 단계

1. 역할 문서 → `20-spec/README.md` §Data / Domain Boundary → DEC-003 → BASE-003 → 조사 리포트 둘
2. `spec-003` 의 **절 구성과 frontmatter 형식**을 그대로 따라 뼈대를 세운다 (id `SPEC-004`, version `0.1.0`, status `draft`, links 에 BASE-003·DEC-003)
3. §1~§7 을 채운다
4. `20-spec/README.md` 에 한 줄 추가
5. 완료 보고

## 7. 범위 제약 — 하지 말 것

- **DEC-003 을 다시 정하지 마라.** 모순은 고치지 말고 §7 에 적는다
- **스키마 전문을 spec 에 쓰지 마라.** `20-spec/README.md` 가 못 박았다 — column·index·FK·ORM 모델·repository 구조는 **WORK 문서의 Domain / Schema 절** 몫이다. spec 은 **외부에 드러나는 것**만 — 리소스·상태·enum·API 계약·인수조건
- **WP(30-work)를 쓰지 마라.** 별도 발주다
- **코드를 보지 마라.** 조사 리포트 둘이 이미 파일:줄로 떠 왔다. 코드 레포 워크트리를 열 필요가 없다
- **시안을 깎지 마라.** 구현이 어려워 보여도 계약에서 빼지 않는다
- 커밋·push 금지

## 8. 검증

- `spec-004-calendar-scheduling.md` 가 `spec-003` 과 **같은 절 구성·frontmatter 형식**을 갖는다
- DEC-003 채택 **A~J 가 모두** 계약 문장으로 내려왔다. 빠진 항목이 없다
- 모든 계약 문장에 **근거**가 붙는다 (DEC-003 절 번호 · 조사 리포트 파일:줄 · 시안 파일:줄)
- **스키마 전문이 없다** — column/index/FK 나열이 spec 본문에 없다
- 정하지 못한 것은 §7 Open Questions 로 남겼고, **임의 결정이 없다**
- `git status --short` 에 **위 두 파일만** 뜬다. 다른 파일이 뜨면 즉시 되돌리고 보고하라.
  이 명령의 출력을 완료 보고에 붙여라

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_a9d49810-1ce8-4885-8c5f-b93200c501ac --from term_95d88d2b-e9e6-4e4a-a031-3b247f4d99b1 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
