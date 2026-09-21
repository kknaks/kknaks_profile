# [frontend] 캘린더 시안 대비 현 구현 차이 — 전수조사 (read-only)

너는 **strong-hajin `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

> ⚠ **이번 발주는 조사다. 코드를 한 줄도 고치지 마라.** 산출물은 리포트 파일 하나뿐이다.
> ⚠ 같은 워크트리에 `backend` 워커가 동시에 조사로 타 있다. 둘 다 read-only 라 충돌하지 않는다 — **그쪽도 파일을 안 고친다.** 네가 고치면 그 전제가 깨진다.

## 1. SSOT — 먼저 읽을 것

**확정 시안이 정본이다.** 기획과 다르면 시안이 이긴다. 시안을 「참고」로 깎지 마라.

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-10-sc-meeting/package 2/Calendar.html` — 화면 껍데기·로딩 순서
- `…/package 2/handoff/calendar/js/calendar.v1.jsx` — **화면 본체.** 3분할·월 뷰·좌측 레일
- `…/package 2/handoff/calendar/js/week.jsx` — 주 뷰. 종일 + 0~24시 시간 격자
- `…/package 2/handoff/calendar/js/data.js` · `…/handoff/shared/js/work-data.js` — 시안이 가정한 데이터 모양
- `…/package 2/handoff/calendar/css/calendar.css` · `…/handoff/my-work/css/components.css` — 시안 스타일
- `…/package 2/handoff/shell/js/scax-ui.jsx` — 시안이 쓰는 공용 부품 구현

(`…` 은 `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-10-sc-meeting` 이다. 경로에 **공백이 있다** — `package 2`. 따옴표를 씌워라.)

### 코디네이터가 이미 닫은 결정 (이대로 전제하고 조사하라 — 다시 정하지 마라)

```
D4  업무 상태값의 정본은 백엔드다. `TaskState` 6종 —
    open · in_progress · blocked · completion_submitted · done · cancelled
    시안 work-data.js 의 status 5종(not-started·progress·blocked·done·cancelled)은 폐기한다.
    시안에 없는 completion_submitted 는 미완으로 취급해 캘린더에 계속 낸다
D5  시간 배정은 업무에 완전히 종속. 업무가 done·cancelled 로 가면 배정도 같이 접는다
D9  회의가 캘린더로 돌아온다. 현재 CalendarPage.tsx 주석이 "이 화면은 업무만 낸다" 고
    적어 둔 결정을 시안이 뒤집는다 — 탭(전체·회의·업무)으로 회의를 같이 낸다
```

## 2. 배경 / 무엇을 조사하나

시안은 캘린더를 **3분할**로 다시 세운다 — `[사이드바][좌측 일정 목록][월·주 캘린더]`. 그리고 데이터 축이 둘이다: **날짜 단위 업무**(기간 띠)와 **시간 단위 스케쥴**(회의 + 업무의 그날 몇 시 배정).

현재 `features/calendar/CalendarPage.tsx` 는 128줄이고 `features/work/WorkViews.tsx` 의 `TaskCalendar` 를 그대로 쓴다. 주·월 토글은 있지만 **둘 다 날짜 격자**이고, 시간 격자·종일 구분·좌측 레일·드래그·리사이즈가 전부 없다. 회의도 화면에서 빠져 있다.

**즉 이 화면은 거의 재작성이다.** 이번 발주는 그 재작성을 **하는** 일이 아니라, 무엇이 있고 무엇이 없는지를 **빠짐없이 세는** 일이다. 다음 판의 spec·WP 가 이 리포트를 재료로 쓴다.

## 3. 계약 (다른 워커와 합의됨)

해당 없음 — 조사 단계다. BE 워커가 같은 시각에 **저장·API 쪽**을 따로 조사한다. 계약은 두 리포트를 받아 spec 이 쓴다.

## 4. 조사 항목 — 여섯 가지. **목록이 아니라 전수조사다**

각 항목의 답은 **`파일:줄` 근거와 함께** 낸다.
그리고 **「N개 있다」로 끝내지 마라** — 세는 방법(실제로 돌린 `grep`/`rg` 명령)을 리포트에 그대로 적어라.

### 4-1. 시안이 요구하는 상호작용 명세를 뽑아낸다

시안 JSX 를 읽고 **동작 규칙**을 코드 근거와 함께 문장으로 옮긴다. 최소 아래 넷 + 시안에 있는데 여기 안 적힌 것이 있으면 그것까지.

1. 좌측 카드 → 날짜 칸 드롭 = 기간 이동(길이 유지). 기한 없는 업무는 그날 하루가 된다
2. 띠 좌우 손잡이 = 시작·마감일 조정. 마감만 있던 업무가 이때 기간을 갖는다
3. 좌측 카드 → 시간 격자 드롭 = 시간 배정 생성(30분 스냅, 기본 1시간). **업무 기간 밖에는 못 넣는다**
4. 시간 블록 세로 손잡이 = 시작·종료 시각 조정

각각 **무엇이 금지되어 있는지**까지 적어라 — 시안은 금지를 `canDrop` 같은 조용한 가드로 표현한다.

### 4-2. 현 캘린더 표면 전수 — 고칠 수 있나, 새로 세워야 하나

**이게 이번 조사에서 제일 중요하다.**

- `TaskCalendar` 를 **쓰는 곳을 전부 grep** 한다. 캘린더 화면 말고 누가 또 쓰는가
- 쓰는 곳이 둘 이상이면 **고치면 남의 화면이 깨진다.** 그 경우 새 부품을 세우고 기존은 두는 판단의 근거를 적는다
- `weekSegments` 등 `TaskCalendar` 가 딸고 있는 보조 함수도 같은 방식으로 센다
- `.calendar-*` CSS 클래스를 **쓰는 곳을 전부** 센다. `CalendarPage.tsx` 주석이 "8-B 가 `.calendar-*` 를 이 화면 안에 가두려고 붙인 울타리를 8-C 가 뗐다" 고 한다 — **지금 그 클래스들이 어디까지 새는지**를 확인하라

### 4-3. DS 부품 대조 — 있는 것과 없는 것(DS-gaps)

시안 `calendar.v1.jsx:6` 이 쓰는 부품은 이 열둘이다.

```
AppShell · SideNav · AppHeader · AppBody · Badge · Button
Icon · IconButton · SegmentedControl · GutterList · Empty · TaskCreateModal
```

각각에 대해 `frontend/src/ds`(및 `frontend/src/shell`)에 **같은 것이 있는가 / 이름만 다른가 / 없는가**를 판정한다. 없는 것은 **DS-gaps 로 따로 모아라** — 그게 다음 판에 디자이너에게 넘어갈 목록이다. 「비슷한 걸로 대체 가능」 같은 판단은 여기서 하지 말고 사실만 적는다.

### 4-4. 데이터 — 무엇을 부를 수 있고 무엇이 모자란가

- `frontend/src/lib/api.ts` 에서 캘린더가 쓸 수 있는 호출을 전부 추린다 (업무·회의 양쪽)
- `frontend/src/lib/viewModels.ts` 의 `DirectTask` 필드와 **시안 `work-data.js` 의 필드를 1:1 대조표**로 만든다. 시안에만 있는 필드, 코드에만 있는 필드를 양쪽 다 적는다
- 시간 배정은 백엔드에 **아직 없다**(BE 워커가 그쪽을 조사 중이다). 프론트가 그걸 부르려면 **무엇이 필요한지**를 적어라 — 이게 다음 판 계약의 초안 재료다
- `api.ts` 밖에서 `fetch` 를 부르는 곳이 있는지 확인한다 (규칙 위반 자리)

### 4-5. 상태값 — D4 를 걸 자리

- 현재 프론트가 업무 상태를 **어떻게 표시하는가**. 라벨·색·배지를 만드는 자리를 전부 센다
- `completion_submitted` 를 지금 화면이 어떻게 내고 있는가. 캘린더가 이걸 어떻게 내야 하는지 근거 있는 제안을 **Open Question 으로** 남긴다
- 권한 envelope 으로 「할 수 있나」를 판단하는 자리를 짚는다 — 캘린더의 드래그·리사이즈는 **쓰기 동작**이라 여기 걸린다

### 4-6. 스타일 — 시안 CSS 를 얼마나 그대로 가져올 수 있나

시안은 `--scax-*` 토큰과 `.scax-*` 클래스를 쓴다. 코드 레포에 **같은 토큰 체계가 있는가**. `_ds_bundle.css` 의 토큰과 레포의 토큰이 같은 이름인가 다른가. 시안 `calendar.css` 103줄 중 **그대로 쓸 수 있는 것과 다시 써야 하는 것**을 가른다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- **(read-only) 코드 레포의 어떤 파일도 수정·생성·삭제하지 않는다**
- 쓰기가 허용된 파일은 **아래 리포트 하나뿐**이다:
  `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-calendar/fe-survey-report.md`

## 6. 진행 단계

1. 역할 문서 → 코드 레포 `AGENTS.md` → 시안 파일 전부를 읽는다
2. 4-1 ~ 4-6 을 순서대로 조사한다. 각 항목마다 **실제로 돌린 검색 명령**을 기록한다
3. 리포트를 쓴다. 절마다 「사실(근거) / 해석 / 모르는 것」을 가른다
4. **정하지 못한 것은 Open Questions 로 남긴다.** 임의로 결정하지 마라

## 7. 범위 제약 — 하지 말 것

- **코드를 고치지 마라.** 컴포넌트도, CSS 도, 스텁도 만들지 않는다
- **설계를 정하지 마라.** "이렇게 만들면 된다" 가 아니라 "이 자리가 이렇게 생겼다" 를 낸다
- **시안을 깎지 마라.** "이건 구현이 어려우니 빼자" 는 네 판단이 아니다. 어려우면 **어렵다는 사실과 이유**를 적어라
- D4·D5·D9 를 다시 논의하지 마라. **모순을 발견하면 고치지 말고 리포트에 적어라** — 그게 제일 값진 결과다
- 백엔드(`backend/`)는 보지 마라. 다른 워커가 맡았다
- 테스트·빌드를 돌리지 마라 — 고친 게 없으니 돌릴 이유가 없다

## 8. 검증

조사 발주라 테스트 실행이 없다. 대신 리포트가 아래를 만족해야 한다.

- 4-1 ~ 4-6 **여섯 항목이 모두** 답을 갖는다. 못 찾았으면 "못 찾았다 + 어떻게 찾아봤나" 를 적는다
- 모든 주장에 `파일:줄` 근거가 붙는다. 근거 없는 문장은 쓰지 않는다
- 「전부 세라」고 한 항목(4-2·4-3·4-4)은 **실제로 돌린 검색 명령**이 리포트에 있다
- DS-gaps 가 **따로 모인 절**로 있다
- `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar status --short` 가 **비어 있다** (아무것도 안 고쳤다는 증거). 이 명령의 출력을 리포트 끝에 붙여라

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_a9d49810-1ce8-4885-8c5f-b93200c501ac --from term_49972e50-eed3-461b-8174-fc4f61de218d \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
