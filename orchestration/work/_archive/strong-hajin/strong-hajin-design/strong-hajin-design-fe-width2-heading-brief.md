# [frontend] 두 건 — 「추가」 셀렉터가 안 늘어난다 · 구획 제목이 회색이다

같은 워크트리에서 이어서 한다. **원인은 코디가 찾아 놨다. 그대로 고쳐라.**

## 1. 「추가」 줄 셀렉터가 안 늘어난다

사용자가 화면에서 짚었다 — 지난 판에서 「늘어난다」고 보고했는데 **실제로는 200px 에 머문다.**

원인:

```
task-detail.css   .scax-td .rel__select          { width: fit-content; min-width: 200px; }
task-detail.css   .scax-td .rel__addrow .rel__select { flex: 1 1 auto; min-width: 0; }
```

`flex: 1 1 auto` 는 **flex-basis 를 `width` 에서 가져온다.** 그 `width` 가 `fit-content` 라
기준 폭이 내용 크기로 굳고, 남은 공간을 받아도 눈에 띄게 늘지 않는다.

**고칠 것** — 「추가」 줄에서만 기준을 0 으로 바꾼다.

```
.scax-td .rel__addrow .rel__select { flex: 1 1 0%; width: auto; min-width: 0; }
```

`flex-basis: 0%` 이면 내용 크기를 무시하고 남은 폭 전체로 늘어난다.
`width: auto` 로 바깥 규칙의 `fit-content` 를 이 자리에서만 되돌린다.

**상위 업무·프로젝트 셀렉터는 지금처럼 내용 너비로 둔다.** 그건 맞게 됐다.

**확인 방법**: 「추가」 줄의 셀렉터가 **바로 위 빈 상태 상자와 같은 폭**으로 서야 한다.
지금은 그 상자만 칸을 채우고 셀렉터는 짧아서 어긋나 보인다.

## 2. 구획 제목 「막힘 사유」가 회색이다

지난 판에서 **본문**만 검정으로 바꿨다. 사용자가 말한 것은 **제목**이다.

```
screens-a.css   .drawer-section h4 { color: var(--scax-color-ink-assistive); }   <- 회색
```

**이 화면 안에서만**(`.scax-td` 스코프) `.drawer-section h4` 를 **검정**(`--scax-color-ink`)으로 덮어라.

- `screens-a.css` 를 고치지 마라 — 공용이라 다른 화면이 같이 바뀐다
- **`.drawer-section.notice.danger h4` 의 빨강은 그대로 둔다** — 시작 막힘 배너 제목이다.
  덮는 규칙이 그것까지 먹지 않게 해라
- 같은 화면의 다른 `.drawer-section h4` 도 함께 검정이 된다. **그게 맞다** —
  칸 제목(`.cell__head h5`)이 이미 검정이라 둘이 어긋나 있었다

## 하지 말 것

- 공용 CSS(`screens-a.css`·`components.css`) 금지
- 이 둘 밖의 것을 고치지 마라
- `backend/` 금지 · 커밋·push 금지

## 검증

- **테스트는 직렬로만**: `npx vitest run --no-file-parallelism` (`make frontend-test` 금지)
- `npx tsc --noEmit`
- 스코프 판의 죽은 규칙 0건 유지 — 새 선택자를 손 목록에 더해라
- 브라우저 띄우지 마라. 사용자 포트(8001·5176·54329) 무접촉

## 리포트

`fe-report.md` 에 `## 13. 셀렉터 폭 · 구획 제목 색` 절을 더해 `파일:줄` 로 적어라.
**지난 판에서 「늘어난다」고 보고한 것이 왜 틀렸는지도 한 줄 적어라.**

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_e622370a-1f3b-4861-b759-daa3584eace0 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 셀렉터 폭·제목 색 완료: <한 줄>" \
  --body "둘 각각 파일:줄 / 지난 보고가 틀린 이유 / 검증"

orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] frontend 셀렉터 폭·제목 색 완료" --enter
```
