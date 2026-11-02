# [backend] 업무 구조 백엔드 전수조사 — 관계 다섯의 실제 계약

너는 **strong-hajin `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-design`
base 브랜치: `origin/main`

⚠ **같은 워크트리에 frontend 워커가 동시에 탄다.** 둘 다 읽기 전용 조사이고 서로 다른 리포트
파일 하나씩만 쓴다. `backend/` `frontend/` 어느 쪽도 **고치지 마라** — 충돌하면 둘 다 잃는다.

## 0. 이것은 조사다 — 고치지 마라

**읽기 전용 조사다.** 코드를 한 줄도 바꾸지 않는다. 산출물은 리포트 **한 장**뿐이다.
「이렇게 고치면 된다」도 쓰지 마라 — 그건 다음 판이다. **지금 무엇이 어떻게 도는지만** 적는다.
테스트도 돌리지 마라. 읽어서 답할 수 있는 것만 답한다.

## 1. 왜 조사하나

업무 상세 화면을 다시 설계하려 한다. 화면에 **상위·하위**는 있는데 **선행·후행**이 없다.
그런데 `preceding` · `predecessor` 가 백엔드 20여 파일에 깔려 있다. 계약이 어디까지 서 있는지
모른 채로 화면을 그리면 없는 것을 그리거나 있는 것을 또 만든다.

## 2. 조사 범위

`backend/src/ax_workspace/` 전부. 시작점은 이것들이다 — **여기서 멈추지 말고 grep 으로 넓혀라.**

```
modules/work/application.py        관계 판정·검증의 본체
modules/work/task_creation.py      생성 입력 계약
modules/work/creation_commands.py  · task_commands.py · requests.py · assignments.py
modules/work/task_results.py       · request_results.py · project_results.py  ← 응답 shape
modules/work/lifecycle.py          상태 전이와 blocking
platform/work_tasks.py             · persistence.py  ← 저장 모양
entrypoints/http.py                HTTP 표면
entrypoints/mcp.py                 MCP 표면
```

## 3. 관계 다섯을 각각 — 이 표를 채운다

1. **상위 ↔ 하위** (`parent_task_id`)
2. **선행 ↔ 후행** (`preceding_task_ids`)
3. **참고** (`reference_task_ids`)
4. **프로젝트 소속** (`project_id`)
5. **요청 ↔ 수락으로 생긴 업무** (`source_work_request_id` · `supersedes_request_id`)

| 물음 | 답 | 근거(파일:줄) |
|---|---|---|
| 저장 모양 (테이블·컬럼·조인테이블) | | |
| 어느 엔드포인트가 **받나** (생성·수정 각각) | | |
| 어느 응답이 **내보내나** — 필드 이름과 shape 그대로 | | |
| 검증 규칙 — 무엇을 거절하나 | | |
| 오류 코드·예외 클래스·사람이 읽는 메시지 | | |
| 방향이 양쪽인가 한쪽인가 (후행을 **직접** 조회할 수 있나) | | |
| 깊이·개수 제한이 있나 | | |
| 권한 — 누가 만들고 누가 읽나 | | |

## 4. 특별히 답할 것 — 선행·후행

따로 절을 떼어 답한다.

1. **후행(successor)을 조회하는 길이 있나.** 선행은 `preceding_task_ids` 로 저장되는데,
   「나를 선행으로 삼는 업무들」을 내주는 엔드포인트·필드가 **있나 없나**
2. **blocking 계산이 어디서 나나.** 프론트가 쓰는 `blockingPredecessors` ·
   `startBlockedByPredecessors` 에 대응하는 서버 값이 무엇이고 어느 응답에 실리나
3. **선행이 업무 상세 응답에 실리나.** 실린다면 어느 필드에 어떤 shape 으로,
   안 실린다면 어디서 따로 받아야 하나
4. **순환·자기참조를 막나.** 상위는 `TaskParentCycle` 이 있다. 선행에도 같은 가드가 있나
5. **끝난 업무·취소된 업무**가 선행으로 남아 있을 때 어떻게 되나

## 5. 전수조사 — 목록으로 끝내지 마라

위 §2 는 **시작점**이다. 다음을 반드시 grep 으로 **전부** 센다.

```
preceding   predecessor   successor   parent_task_id   reference_task_ids
project_id  source_work_request_id    supersedes       blocking
```

각 심볼이 **몇 군데** 나오는지 숫자로 적고, 표면(HTTP·MCP·워커·부트스트랩)별로 나눈다.
「주요한 것 몇 개」로 줄이지 마라 — 빠진 자리에서 다음 판이 깨진다.

## 6. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/work/strong-hajin-design/be-survey-report.md` ← **이 파일 하나만 만든다**

코드 워크트리는 **읽기만** 한다. 커밋·push·PR 금지.

## 7. 하지 말 것

- 코드·테스트·마이그레이션을 고치지 마라
- 서버·DB 를 띄우지 마라. **사용자 포트와 프로세스를 건드리지 마라** (8001·5176·54329 가 떠 있다)
- 「이렇게 바꾸자」를 쓰지 마라. 조사 리포트에 설계를 섞지 않는다
- 없는 것을 있다고 쓰지 마라. 못 찾았으면 「못 찾음」으로 적는다

## 8. 리포트 형식

위 경로에 쓴다.

```
# 업무 구조 백엔드 전수조사

## 0. 한 줄 요약
## 1. 심볼 개수표 (§5)
## 2. 관계 다섯 — 각각 §3 의 표
## 3. 선행·후행 — §4 의 다섯 물음
## 4. 응답 shape 원문
   업무 상세·목록 응답에서 관계가 실리는 부분을 «그대로» 붙인다 (요약하지 말 것)
## 5. 계약과 문서가 어긋나 보이는 곳
   판정하지 말고 «이렇게 보인다» 로만 적는다
## 6. 조사 한계
```

**모든 줄에 `파일:줄` 근거를 단다.** 근거 없는 문장은 쓰지 않는다.

## 9. 검증

읽기 전용이라 테스트를 돌리지 않는다. 대신 **리포트의 모든 주장에 `파일:줄`이 붙었는지**
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
  --subject "backend 조사 완료: <한 줄>" \
  --body "리포트 경로 / 핵심 발견 3~5줄 / 못 찾은 것 / 조사 한계"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] backend 조사 완료 — <한 줄 요약>. 리포트: <경로>" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
