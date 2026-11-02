# [frontend] 업무 구조 프론트 전수조사 — 무엇을 그리고 무엇을 안 그리나

너는 **strong-hajin `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-design`
base 브랜치: `origin/main`

⚠ **같은 워크트리에 backend 워커가 동시에 탄다.** 둘 다 읽기 전용 조사이고 서로 다른 리포트
파일 하나씩만 쓴다. `backend/` `frontend/` 어느 쪽도 **고치지 마라** — 충돌하면 둘 다 잃는다.

## 0. 이것은 조사다 — 고치지 마라

**읽기 전용 조사다.** 코드를 한 줄도 바꾸지 않는다. 산출물은 리포트 **한 장**뿐이다.
「이렇게 고치면 된다」도 쓰지 마라 — 그건 다음 판이다. **지금 무엇이 어떻게 그려지는지만** 적는다.
테스트·빌드를 돌리지 마라. 읽어서 답할 수 있는 것만 답한다.

## 1. 왜 조사하나

업무 상세 화면을 다시 설계하려 한다. 화면에 **상위·하위**는 있는데 **선행·후행**이 없다.
서버는 선행을 알고 있는 것으로 보인다. 그러면 **프론트가 받고도 안 그리는 것인지**,
**아예 안 받는 것인지**를 갈라야 한다. 그 답이 다음 설계의 출발점이다.

## 2. 조사 범위

`frontend/src/` 전부. 시작점은 이것들이다 — **여기서 멈추지 말고 grep 으로 넓혀라.**

```
features/work/WorkModals.tsx      업무 상세 서랍 · 생성 모달 (가장 크다)
features/work/MyWorkPage.tsx      목록·행
features/project/                 projectModel.ts · ProjectTaskPanel.tsx  ← 트리를 이미 그린다
features/action/ActionTaskCard.tsx
features/graph/RelationGraphPage.tsx   ← 관계를 «그림으로» 그리는 화면
api.ts  types.ts                  계약이 프론트에 들어오는 입구
```

## 3. 관계 다섯 — 각각 이 표를 채운다

1. **상위 ↔ 하위** (`parent_task_id`)
2. **선행 ↔ 후행** (`preceding` · `predecessor`)
3. **참고** (`reference_task_ids`)
4. **프로젝트 소속** (`project_id`)
5. **요청 ↔ 수락으로 생긴 업무**

| 물음 | 답 | 근거(파일:줄) |
|---|---|---|
| `types.ts` 에 타입이 있나 — 필드 이름과 모양 | | |
| `api.ts` 의 어느 함수가 보내고 받나 | | |
| **어느 화면이 그리나** — 화면 이름과 파일:줄 전부 | | |
| 만들 수 있나 (입구가 어디) | | |
| 지울 수 있나 (입구가 어디) | | |
| 읽기만 되는 곳은 어디 | | |
| **받는데 안 그리는 자리가 있나** | | |

## 4. 특별히 답할 것 — 선행·후행

따로 절을 떼어 답한다.

1. `WorkModals.tsx` 의 `blockingPredecessors` · `visiblePredecessors` · `hiddenPredecessors` ·
   `startBlockedByPredecessors` — **각각 어디서 값이 오고 어디에 그려지나.** 안 그려지면 「안 그림」
2. 업무 상세 서랍에 **선행을 보여 주는 자리가 있나.** 있으면 어떤 모양(문장·배지·목록),
   없으면 값만 받고 버리는지
3. 선행을 **만드는 입구**가 어디인가. 생성 모달의 「선행 업무」 표 말고 또 있나
4. **후행**(나를 선행으로 삼는 업무)을 보여 주는 자리가 있나
5. `RelationGraphPage` 는 관계 다섯 중 **무엇을** 그리나. 선행이 거기 있나

## 5. 업무 상세 서랍의 구획 목록 — 순서대로 전부

지금 서랍이 **위에서 아래로** 어떤 구획을 그리는지 표로 만든다. 하나도 빼지 마라.

| 순서 | 구획 (`aria-label`) | 무엇을 보여 주나 | 편집 입구 | 파일:줄 |
|---|---|---|---|---|

다시 설계할 화면의 기준선이라 **빠짐이 곧 다음 판의 구멍**이다.

## 6. 전수조사 — 목록으로 끝내지 마라

다음을 grep 으로 **전부** 센다. 몇 군데인지 숫자로 적는다.

```
preceding   predecessor   successor   parent_task_id   reference_task_ids
blocking    section-row   drawer-section   material-list
```

## 7. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/work/strong-hajin-design/fe-survey-report.md` ← **이 파일 하나만 만든다**

코드 워크트리는 **읽기만** 한다. 커밋·push·PR 금지.

## 8. 하지 말 것

- 코드·테스트·CSS 를 고치지 마라
- **서버·프론트를 띄우지 마라. 사용자 포트와 프로세스를 건드리지 마라** — 8001·5176·54329 가
  지금 떠 있고 사용자가 그 화면을 보고 있다. 재시작하면 사용자 작업을 끊는다
- 브라우저를 열지 마라. 화면 확인은 코디와 사용자가 한다
- 「이렇게 바꾸자」를 쓰지 마라. 조사 리포트에 설계를 섞지 않는다
- 시안·DS 부품을 새로 만들지 마라

## 9. 리포트 형식

위 경로에 쓴다.

```
# 업무 구조 프론트 전수조사

## 0. 한 줄 요약
## 1. 심볼 개수표 (§6)
## 2. 관계 다섯 — 각각 §3 의 표
## 3. 선행·후행 — §4 의 다섯 물음
## 4. 업무 상세 서랍 구획 목록 (§5)
## 5. 받는데 안 그리는 것 / 그리는데 못 고치는 것
## 6. 조사 한계
```

**모든 줄에 `파일:줄` 근거를 단다.** 근거 없는 문장은 쓰지 않는다.

## 10. 검증

읽기 전용이라 테스트·빌드를 돌리지 않는다. 대신 **리포트의 모든 주장에 `파일:줄`이 붙었는지**
스스로 훑고, 근거 없는 줄은 지우거나 「근거 못 찾음」으로 바꾼다.

## 99. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 리포트 파일 하나만 남긴다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_e622370a-1f3b-4861-b759-daa3584eace0 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 조사 완료: <한 줄>" \
  --body "리포트 경로 / 핵심 발견 3~5줄 / 못 찾은 것 / 조사 한계"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] frontend 조사 완료 — <한 줄 요약>. 리포트: <경로>" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
