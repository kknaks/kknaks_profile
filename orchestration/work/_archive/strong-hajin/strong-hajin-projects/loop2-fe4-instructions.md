# 루프2 Phase FE-4 — 간트 셋: 틀고정 · 첫 진입 오늘 기준 · 좌 레일 자동 스크롤

**allowed_paths**: `frontend/` 만. 커밋·push 금지. **개발 서버를 띄우지 마라** —
`localhost:5173` · `127.0.0.1:8100` 은 **사용자의 E2E 스택**이다(건드리면 사용자 화면이 죽는다).
**`backend/` 0줄** — 다른 워커가 거기서 작업했고 지금 검수 중이다.

## 읽을 것

- 역할: `.../roles/strong-hajin/frontend/role.md` (+ `rules.md`) · 코드 레포 `AGENTS.md`
- **계약**: `spec-005-projects.md` **v0.2.0** — §2.4(간트) · §6 의 **FE-4 몫 8줄**
- **계획**: `work-005-projects.md` **Phase FE-4** (네 몫이다. **FE-5 는 다음 판이니 손대지 마라**)
- **결정**: `decision-004-projects.md` — **D-35 일부 · D-36 · D-37**
- **조사**: `loop2-survey-report.md` **Q1** ← **범위 판정과 「고쳐야 할 넷」이 거기 있다. 반드시 읽어라**
- 1루프: `fe-impl-report.md` · `review-fe-report.md` · `fe-fix-report.md`(공유 자산 지도)

## 무엇을 만드나 — 셋

### ① 업무 이름 칸 틀고정 (가로 스크롤에 고정)

**조사 판정: 된다. 간트 재조립이 아니라 CSS 쪽이다.** `position: sticky; left: 0` 이
`absolute` 행 안에서도 먹는다(스크롤 조상 있음 · 중간에 `overflow` 없음 · 붙을 구간 있음).

⚠ **sticky 한 줄로는 안 된다. 조사가 「고쳐야 할 넷」을 세어 뒀다**:

| | 무엇 | 왜 |
|---|---|---|
| ① | `position:sticky; left:0` | 본체 |
| ② | **`z-index` 양수** | **지금 막대가 이름 위에 그려진다** — 같은 행에서 `__name-cell` 이 `__bar` 보다 DOM 앞이고 둘 다 positioned 다. 고정해도 막대가 덮는다 |
| ③ | **`background`** | 이름 칸에 배경이 없어서 **격자·오늘선·의존선 SVG 가 글자 밑으로 비쳐 지나간다** |
| ④ | **축(머리줄)의 200px 자리를 덮을 sticky 요소** | `.scax-pj-gantt__axis` 는 `paddingLeft:200` 만 두고 **그 자리에 요소가 없다** — 스크롤하면 **날짜 숫자가 이름 칸 위 띠로 그대로 보인다** |

**넷을 다 하지 않으면 「고정됐는데 글자가 안 읽히는」 화면이 된다.**

### ② 첫 진입 시 오늘 날짜가 보이게 스크롤

지금은 간트가 **맨 왼쪽(1일)** 에서 시작한다. 첫 렌더에 **오늘(`--today`)이 보이는 위치**로.
- 프로젝트를 **바꿀 때마다** 다시 맞출지, **첫 진입만**인지 — 계약을 보고 따르고,
  계약에 없으면 **첫 진입 + 프로젝트 전환 시** 로 하고 그 판단을 리포트에 적어라
- 사람이 스크롤한 뒤에 **멋대로 되돌리지 마라**

### ③ 간트에서 업무를 고르면 좌 레일이 자동 스크롤

지금은 카드에 **선택 표시는 되는데 스크롤이 안 된다** — 아래쪽 업무는 거의 안 보인다.
- **반대 방향도 보라** — 좌 레일에서 고르면 간트 행이 보이게 할지. 계약을 따르고, 없으면 리포트에
- **이미 보이는 카드는 움직이지 마라**(불필요한 점프가 더 나쁘다). `block:"nearest"` 같은 선택지를 고려

## ⚠ 공유 자산 — 1루프 조사가 지도를 만들어 뒀다

`research-fe-structure.md` §4-3 을 읽어라. 이번 판에 닿을 만한 것:
- **`projects.css` 는 이 화면 전용**이라 마음껏 고쳐도 된다. **`components.css`·`shell.css`·`src/ds/` 는 공유**다
- **`.scax-pj-gantt__*` 는 이 화면 전용**이다. 반면 `.scax-inbox-card`·`.scax-gutter-list` 는
  수신함·캘린더가 함께 쓴다 — **선택자를 좁혀라**
- ⚠ **`ProjectRail.tsx` 와 `projects.css` 는 다음 판(FE-5)도 만진다.**
  **네가 만든 구조를 다음 판이 이어받는다** — 리포트에 **무엇을 어떻게 바꿨는지** 적어라

## 검증

- `make frontend-test` · `frontend` 에서 `npx tsc --noEmit`. **수치를 재서 리포트에**
- **네가 더한 검사가 실제로 무엇을 지키는지** 적어라. 1루프 교훈: **빈 단언·항상 참인 가드**를 만들지 마라
- 틀고정은 **테스트로 얕게밖에 못 잰다** — 무엇을 테스트로 잡았고 무엇이 **눈으로만 확인되는지**
  갈라서 적어라(사용자가 2차 E2E 에서 그것을 본다)
- **기존 실패와 네 실패를 분리**해 보고. 1루프에서 `MeetingMaterials`·`ActionCenter` 가
  부하로 흔들린 적이 있다(이 판 밖)

## 범위 제약

- **FE-5 몫을 건드리지 마라** — 헤더 생성 버튼·모달 · 우 레일 업무 정보 블록 · 상태 드롭다운 ·
  좌 레일 헤더 한 줄. **그건 다음 판이다**
- `backend/` 0줄 · 개발 서버 금지 · 커밋 금지
- SPEC 에 없는 것을 만들지 마라. 필요하면 리포트에 「막힌 것」으로

## 리포트 (`orchestration/work/strong-hajin-projects/loop2-fe4-report.md`)

- 바꾼 파일과 **각각이 닫는 인수조건 번호(L-)**
- **넷을 다 했는지** 하나씩 (sticky · z-index · background · 축 스페이서)
- **다음 판(FE-5)이 이어받을 구조 변경** — `ProjectRail.tsx`·`projects.css` 에서 무엇이 달라졌나
- 테스트 수치 · **테스트로 잡은 것 / 눈으로만 확인되는 것**
- 막힌 것 · 판단이 필요한 것

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_22d9a6a5-c4ac-4d05-83a4-d4794e1e56fd \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: 루프2 FE-4" \
  --body "바꾼 파일 / 닫은 인수조건 / 넷 다 했나 / FE-5 가 이어받을 구조 변경 / 테스트 수치 / 눈으로만 확인되는 것"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] frontend 완료 — 루프2 FE-4. 상세는 인박스." --enter
```
