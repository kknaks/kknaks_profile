# [writer] 업무 구조 스펙 전수조사 — 상위·하위·선행·후행·참고

너는 **strong-hajin `writer` 워커**다. 먼저 역할 문서를 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인` (코디 워크트리 — 너는 여기 직접 탄다)

⚠ 같은 워크트리에 코디네이터가 앉아 있다. **네 리포트 파일 하나 말고는 아무것도 쓰지 마라.**

## 0. 이것은 조사다 — 고치지 마라

**읽기 전용 조사다.** 문서를 고치거나 새 스펙을 쓰지 않는다. 산출물은 리포트 **한 장**뿐이다.
무엇을 바꿔야 하는지도 쓰지 마라 — 그건 다음 판이다. **지금 무엇이 어떻게 정해져 있는지만** 적는다.

## 1. 왜 조사하나

업무 상세 화면을 다시 설계하려 한다. 지금 화면에는 **상위·하위**는 있는데 **선행·후행**이 없다.
그런데 코드에는 `preceding_task_ids` · `predecessor` 가 백엔드 20여 파일에 깔려 있다.
그래서 「없다」가 아니라 **「어딘가 정해져 있는데 화면이 안 쓴다」** 로 보인다.

무엇이 계약으로 정해져 있는지를 먼저 세워야 화면을 다시 그릴 수 있다.

## 2. 조사 범위 — 문서만

`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/para/projects/summer-star/strong-hajin/` 아래 전부:

- `00-baseline/` 넷 · `10-decision/` 다섯 · `20-spec/` 여섯 · `30-work/` 여섯 · `40-architecture/`
- `log/` 회고 둘

그리고 개념: `para/areas/concept/` 에서 업무 구조에 걸리는 것.

**회사에서 가져온 원본**도 본다 — mediness 리포 `products/sc-ax/` 의 SPEC-004 v0.6.1 이 마지막이다.
경로가 없으면 「접근 못 함」으로 적고 넘어가라. 찾아 헤매지 마라.

## 3. 무엇을 뽑아 오나 — 관계 다섯을 각각

업무 사이의 관계를 **다섯 갈래**로 나눠 각각 적는다.

1. **상위 ↔ 하위** (`parent_task_id`)
2. **선행 ↔ 후행** (`preceding_task_ids` · predecessor)
3. **참고** (`reference_task_ids`)
4. **프로젝트 소속** (`project_id`)
5. **요청 ↔ 수락으로 생긴 업무** (`source_work_request_id` · 재요청 `supersedes`)

관계마다 이 표를 채운다.

| 물음 | 답 | 근거(파일:줄) |
|---|---|---|
| 계약 이름은 무엇인가 | | |
| 어느 문서가 이것을 정하는가 (SoT) | | |
| 정책 번호가 붙어 있나 (V-·L-·P-·E- 등) | | |
| 무엇을 허용하나 | | |
| 무엇을 거절하나 · 오류 코드는 | | |
| 화면에 어떻게 보이라고 쓰여 있나 | | |
| **미정으로 남은 것이 있나** | | |

## 4. 특별히 답할 것 — 선행·후행

이 셋은 리포트에 **따로 절을 떼어** 답한다.

1. 선행·후행이 **스펙에 어느 수준까지** 정해져 있나 — 저장만인가, 화면 표시까지인가, 아니면 미정인가
2. 「완료를 막는다」(blocking)가 선행과 어떻게 연결되나 — 화면에서 본 `blockingPredecessors` ·
   `hiddenPredecessors` · `startBlockedByPredecessors` 의 **계약상 근거**가 어느 문서 어느 줄인가
3. 업무 상세 화면에 선행·후행을 **그리라고 한 문서가 있나, 없나**. 있으면 어디, 없으면 「없다」

## 5. allowed_paths — 이 밖은 건드리지 마라

- `orchestration/work/strong-hajin-design/spec-survey-report.md` ← **이 파일 하나만 만든다**

읽기는 위 §2 전부 자유. 쓰기는 이 한 파일뿐이다. index·log 수정 금지, 커밋·push 금지.

## 6. 하지 말 것

- 문서를 고치지 마라. 오타도 고치지 마라
- **정해지지 않은 것을 정하지 마라.** 「아마 이런 의도일 것」 금지. 미정은 미정으로 적는다
- 새 스펙·결정·WP 를 쓰지 마라
- `_archive/` 에서 끌어오지 마라 — 지금 새 구조에 올라와 있는 것만 본다

## 7. 리포트 형식

`orchestration/work/strong-hajin-design/spec-survey-report.md`

```
# 업무 구조 스펙 전수조사

## 0. 한 줄 요약
## 1. 읽은 문서 목록 (경로 · 읽음/접근못함)
## 2. 관계 다섯 — 각각 §3 의 표
## 3. 선행·후행 — §4 의 세 물음
## 4. 서로 어긋나는 곳
   같은 사실을 두 문서가 다르게 말하는 자리. 어느 쪽이 맞는지 «판정하지 말고» 둘 다 인용한다
## 5. 미정 목록
   문서가 스스로 「미정」·「아직 안 정한 것」으로 둔 것 전부. 번호(M-·OQ-·EU-)가 있으면 그대로
## 6. 조사 한계
   못 읽은 것 · 확인 못 한 것
```

**모든 줄에 `파일:줄` 근거를 단다.** 근거 없는 문장은 쓰지 않는다.

## 8. 검증

산출물은 브리프가 지정한 파일 하나뿐. 정하지 못한 것은 Open Questions 로 남기고 임의 결정 금지.
모든 결정에 근거 병기.

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
  --subject "writer 조사 완료: <한 줄>" \
  --body "리포트 경로 / 핵심 발견 3~5줄 / 못 찾은 것 / 조사 한계"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] writer 조사 완료 — <한 줄 요약>. 리포트: <경로>" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
