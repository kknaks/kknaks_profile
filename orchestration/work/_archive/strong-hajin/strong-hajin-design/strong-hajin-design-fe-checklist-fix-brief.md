# [frontend] 체크리스트 칸 구조 수정 — 스크롤 통이 빈 상태와 입력폼을 삼켰다

같은 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-design` 에서 이어서 한다.
**사용자가 실물 화면에서 짚었다.** 작은 수정 한 건이다. 새로 조사하지 마라.

## 1. 무엇이 잘못됐나

`WorkModals.tsx:2022` 의 체크리스트 칸이 스크롤 통 안에 **전부**를 넣었다.

```
:2022   <div className="scroll scroll--tall">        <- 스크롤 통 (실선 테두리)
:2023     <section className="drawer-section">        <- margin-top:24px 이 통 «안»에서 붙는다
:2092       <div className="empty">단계가 없습니다.</div>   <- 점선 테두리 상자
:2094       <div className="inline-reason"> input + [추가]  <- 입력폼까지 통 안
```

실제 화면에서 이렇게 보인다 — 사용자 보고:

- **상자 안의 상자**: `.empty`(점선)가 `.scroll`(실선) 안에 들어가 테두리가 두 겹이다
- **입력폼이 스크롤에 갇혔다**: 목록이 길면 스크롤해야 입력칸이 보인다
- 빈 상태인데도 105px 짜리 빈 상자가 서 있다

## 2. 올바른 모양은 이 파일 «안»에 이미 있다

같은 파일의 공용 헬퍼와 자료 칸은 **제대로** 한다. 그대로 따라라.

```
:480-491   공용 헬퍼 — rows 가 0 이면 .empty 를 «통 없이» 내고,
           있을 때만 .scroll 로 감싼다. {after}(추가 줄)는 «통 밖»
:1650-1656 자료 칸 — 같은 모양. .empty 가 .scroll 밖에 있다
```

체크리스트 칸도 **같은 규칙**으로 바꿔라.

- 항목이 **있을 때만** `.scroll.scroll--tall` 로 감싼다. 통 안에는 **목록만**
- **빈 상태(`.empty`)는 통 밖**
- **추가 입력폼(`.inline-reason`)도 통 밖**, 목록 아래
- 통 안의 `<section className="drawer-section">` 을 걷어라 — 칸이 이미 이름(`aria-label`)을 들고 있고,
  그 `margin-top:24px` 이 통 안에서 여백을 만든다

시안은 `TaskDetail.html` 의 체크리스트 칸이다(스크롤 통 안에 `ul.check` 하나뿐).

## 3. 입력칸 하나 더

`.inline-reason` 안의 `<input>` 에 `type` 이 없어 전역 폼 기본값
(`input:not([type])`)이 테두리를 그린다. **DS 껍데기를 쓰거나 `type="text"` 를 주어라** —
같은 서랍의 다른 입력칸과 모양이 맞아야 한다. 어느 쪽이든 **테두리는 한 겹**이다.

## 4. 하지 말 것

- 체크리스트의 **읽기·쓰기 동작을 바꾸지 마라.** 구조와 모양만이다
- 다른 칸(하위·선행·참고·후행·자료)은 **이미 맞다.** 건드리지 마라
- `backend/` 금지
- 시안에 없는 UI 를 만들지 마라
- 커밋·push·PR 금지

## 5. 검증

- `npx tsc --noEmit`
- `make frontend-test` — 병렬 간헐 실패는 알려져 있다. `--no-file-parallelism` 으로 갈라 확인해라
- **스코프 테스트가 여전히 초록인지** 확인해라(`TaskDetailRelations.test.tsx:621-694`)
- 체크리스트가 **0건일 때와 N건일 때** 각각 어떤 요소가 서는지 세는 테스트를 한 건 더해라 —
  0건이면 `.scroll` 이 **없어야** 한다
- 브라우저를 띄우지 마라. 사용자 포트(8001·5176·54329) 무접촉 —
  **지금 사용자가 그 화면을 보고 있다**

## 6. 리포트

`fe-report.md` 에 `## 9. 체크리스트 칸 구조 수정` 절을 더해 무엇을 어떻게 고쳤는지 `파일:줄` 로 적어라.

## 7. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_e622370a-1f3b-4861-b759-daa3584eace0 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 체크리스트 칸 수정 완료: <한 줄>" \
  --body "무엇을 고쳤나 / 파일:줄 / 검증 수치"

orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] frontend 체크리스트 칸 수정 완료 — <한 줄>" --enter
```
