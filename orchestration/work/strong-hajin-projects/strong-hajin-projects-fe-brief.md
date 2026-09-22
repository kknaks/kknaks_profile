# [frontend] 프론트 현재 구조 read-only 조사 — 「프로젝트」 시안 대비 무엇이 살아남고 무엇이 버려지나

너는 **strong-hajin `frontend` 워커**다. **너는 이 작업의 맥락이 하나도 없다.** 아래를 먼저 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md` — 이 역할은 이 두 개가 전부다)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/design-read-projects.md` ← **이번 조사의 출발점.** 코디네이터가 시안을 읽고 정리한 틀·부품·상호작용·요구 사실(D-1~D-9)이 여기 있다
- 코드 레포 `AGENTS.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (**이번 작업은 read-only 조사라 PR 없음**)

⚠ **같은 워크트리에 `backend` 워커가 동시에 붙어 있다.** 그쪽은 `backend/` 를 조사한다.
둘 다 **아무 파일도 고치지 않는다.** 서로의 리포트 파일도 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- **시안 정본** (읽기만 — 이 파일들은 다른 레포에 있다. 복사·수정 금지):
  - `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-10-sc-meeting/package 2/Projects.html`
  - 같은 폴더 `handoff/projects/js/projects.v1.jsx` · `handoff/projects/js/data.js` · `handoff/projects/css/projects.css`
  - 공용 `handoff/shell/js/scax-ui.jsx` · `handoff/shell/js/nav.js` · `_ds_bundle.css`
- **계약의 SoT 는 지금 돌아가는 코드다.** 문서와 코드가 다르면 코드를 사실로 적고 차이를 리포트에 남겨라.

**기대는 개념** — 해당 없음 (조사라 구현 판단이 없다).

## 2. 배경 / 무엇을 하나

「프로젝트」 화면을 시안대로 만든다. 사용자 결정이 둘이다:

1. **시안은 레이아웃·색·위치의 정본이다.** 상태값·논리 구조는 **우리 코드가 정본**이다
2. **프론트는 거의 다시 그린다**는 전제로 간다

그래서 이번 조사의 질문은 둘이다:

> **(a) 지금 프론트가 프로젝트/업무를 어떻게 그리고 있고, 시안과 무엇이 다른가?**
> **(b) 시안이 쓰는 부품이 우리 DS 에 이미 있는가, 새로 만들어야 하는가?**

**아무것도 바꾸지 마라.** 산출물은 리포트 파일 하나다.

## 3. 계약 (다른 워커와 합의됨)

해당 없음 — read-only 조사. `backend` 워커가 같은 D-1~D-9 를 **백엔드 쪽에서** 조사한다.
너는 **프론트가 지금 무엇을 받아서 무엇을 그리는지**만 적어라. DB 스키마를 판단하지 마라.

## 4. 조사 항목

### 4-1. 지금 있는 프로젝트 화면

- `frontend/src/features/project/` 가 지금 **무엇을 그리나.** 화면 구조를 시안의 3레일 틀과 나란히 놓고 비교
- 라우팅 — 어느 경로로 들어가고, 내비의 어느 항목인가. 시안 내비(`nav.js`, 9항목)와의 차이
- 테스트 — `ProjectPage.test.tsx` 가 **무엇을 보장하고 있나.** 다시 그리면 **깨질 단언이 무엇인가**

### 4-2. 부품 재고 — 시안 부품 ↔ 우리 `src/ds`

시안이 쓰는 부품마다 **있다/없다/다르다**로 판정하고 근거(`파일:줄`)를 단다:

| 시안 부품 | 쓰이는 곳 |
|---|---|
| `AppShell` · `SideNav` · `AppHeader` · `AppBody`(3레일) | 화면 틀 전체 |
| `GutterList`(헤더+스크롤 바디) | 좌 레일 |
| `scax-inbox-card` | 좌 레일 업무 카드 — **업무 탭 부품 재사용이 시안의 전제다** |
| `Select` | 프로젝트 셀렉터 |
| `Badge`(tone + `variant="count"`) | 상태·건수 |
| `Empty` | 우 레일 미선택 |
| `Icon`(square-check·chevron-down/right·arrow-up/down·check·folder) | 전반 |
| 진행률 미터(track+fill) | 요약 스트립 · 우 레일 |
| **간트**(축·격자·행·바·twisty) | 본문 — **새로 만들 가능성이 높다** |
| **의존선 SVG 오버레이** | 본문 — 같은 판단 |

- **DS 토큰**: `--scax-rail-left-width`(380px) · `--scax-rail-right-width`(342px) ·
  `--scax-color-accent/danger/positive` · `--scax-space-*` · `--scax-radius-*` 가
  **우리 코드에 같은 이름으로 있는가.** `.design-sync/` 와 `src/ds` 어느 쪽이 정본인가
- 시안 CSS 클래스(`scax-pj-*`)는 이 화면 전용이다. 우리 쪽 스타일 작성 방식(CSS 파일? 토큰? 유틸?)이
  **무엇인지** 적어라 — 시안 CSS 를 그대로 옮길 수 있는 구조인지 판단 재료가 된다

### 4-3. 데이터가 프론트까지 어떻게 오나

- `api.ts`(또는 그 역할을 하는 파일) 에서 **업무·프로젝트 관련 호출을 전부** grep 으로 센다.
  「주요 API」 요약 금지 — 전부 나열
- **envelope** 모양과 권한 판단이 어디서 일어나는가
- viewModels / 변환 계층 — 화면이 쓰는 꼴로 바꾸는 자리가 있는가, 시안이 요구하는 사실
  (D-1~D-9, `design-read-projects.md` §8)이 **프론트까지 실제로 내려오는가**
- 상태 표시(배지 라벨·색)가 지금 **어디서 결정되나** — 상수표? 서버 값? 시안은 5종 tone 매핑이다

### 4-4. 다시 그릴 때의 충돌 지점

- 시안 화면에는 **모달·드로어가 없다.** 지금 프로젝트/업무 화면이 모달·드로어에 의존하고 있나
- 시안 상호작용 축은 `project` + `taskId` **둘뿐**이다. 지금 상태 관리가 무엇을 더 들고 있나
- **다른 화면과 공유하는 부품·스타일** — 프로젝트 화면을 다시 그리면 **같이 흔들리는 화면이 어디인가**

## 5. allowed_paths — 이 밖은 건드리지 마라

- **read-only.** 코드·설정·테스트 **어느 것도 수정하지 마라.** 커밋·push 금지.
- 시안 폴더(`reference/.../package 2`)는 **읽기 전용**이다. 거기서 복사해 오지도, 고치지도 마라.
- **쓰는 파일은 정확히 하나**:
  `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-fe-structure.md`
  (scratchpad 에 쓰지 마라 — 터미널이 죽으면 같이 죽는다. 위 절대경로에 직접 써라.)

## 6. 조사 단계

1. 역할 문서 + `design-read-projects.md` + `AGENTS.md` 읽기
2. 시안 원본 4파일 훑기 (틀·부품·상호작용을 눈으로 확인)
3. `frontend/src` 에서 4-1 ~ 4-4 조사 (표면은 grep 으로 센다)
4. 리포트 1개 작성 → 완료 보고

## 7. 범위 제약 — 하지 말 것

- **설계하지 마라.** 「이렇게 만들면 된다」·컴포넌트 트리 제안을 쓰지 마라. 지금 무엇이 있는지만 적는다.
- **고치지 마라.** 버그를 봐도 리포트 말미 「눈에 띈 것」에 한 줄만 남겨라.
- **백엔드를 판단하지 마라** (`backend/` 는 다른 워커 담당). 프론트가 받는 모양까지만.
- **서버·개발 서버를 띄우지 마라.** 사용자 포트·프로세스를 건드리지 않는다. 정적 읽기로 끝낸다.
- 테스트·빌드를 돌리지 마라 — 이번엔 검증할 변경이 없다.

## 8. 검증

이번 작업의 검증은 테스트가 아니라 **근거**다.

- 4-2 의 부품 표는 **한 줄도 빠짐없이** 판정이 있다.
- **모든 판정에 `파일:줄`** 이 붙는다. 근거 없는 문장은 쓰지 마라.
- API 호출·토큰 이름은 **코드에서 복사한 실값**이다 (기억으로 쓰지 마라).
- 표면은 **grep 결과로 센 수**다 (요약 금지 — 전부 나열).
- 마지막에 **「살아남는 것 / 버리는 것 / 새로 만들 것」 세 목록**으로 닫는다. 각 항목에 근거 한 줄.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_00abca9b-d6cb-492d-9d73-04da7f5cc4fb \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: 프론트 현재 구조 조사" \
  --body "리포트 경로 / 부품 재고 요약(있다·없다·다르다 개수) / 살아남는 것·버리는 것·새로 만들 것 / 다시 그릴 때 흔들리는 다른 화면 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] frontend 완료 — 프론트 구조 조사 리포트 작성. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
