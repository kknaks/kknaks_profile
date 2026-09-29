# [frontend] 「추가」 셀렉터 — 진짜 원인은 popover-root 다

같은 워크트리에서 이어서 한다. **세 번째 시도다. 원인을 코디가 끝까지 짚었다.**

## 무엇이 잘못됐나

지난 두 판에서 `.rel__select` 의 flex 를 고쳤는데 **화면은 그대로다.**
`.rel__select` 는 실제로 늘어났다. 그 **안쪽**에서 끊긴다.

```
.rel__select          flex: 1 1 0%      -> 늘어난다 (이미 맞다)
  span.popover-root   display:inline-flex  -> 내용 크기로 쪼그라든다   <- 여기서 끊긴다
    button.select-trigger  width:100%      -> 쪼그라든 부모의 100% = 그대로 좁다
```

근거:

```
styles/meetings.css   .popover-root { position: relative; display: inline-flex; }
ds/Popover.tsx:139    <span className="popover-root" ref={rootRef}>
```

`inline-flex` 라 내용만큼만 넓어진다. 그 안의 `width:100%` 는 좁은 부모를 기준으로 계산되니
아무리 바깥을 늘려도 단추는 안 늘어난다.

## 고칠 것

**「추가」 줄에서만** `popover-root` 를 늘린다. 이 화면 스코프(`.scax-td`) 안이다.

```
.scax-td .rel__addrow .rel__select > .popover-root { display: flex; width: 100%; }
```

**선례가 있다** — 같은 문제를 회의 화면이 이렇게 풀었다:
`meetings.css` 의 `.date-field > .popover-root { width: 100%; }` · `.time-range > .popover-root { flex: 1; }`
같은 모양을 따르되 **공용 CSS 는 건드리지 마라.**

**상위 업무·프로젝트 셀렉터는 그대로 둔다** — 내용 너비가 맞다.

## 확인 — 이번엔 «계산된 값»으로 세라

jsdom 은 CSS 를 계산하지 않아 지금까지 이 실패를 한 번도 못 잡았다.
**테스트로 못 잡으면 최소한 다음을 리포트에 적어라.**

`task-detail.css` 에서 「추가」 줄 셀렉터가 **화면 폭까지 닿는 데 필요한 체인 전부**를 나열하고,
각 단계가 실제로 그 값을 갖는지 CSS 원문으로 보여라.

```
.cell            (폭의 출처)
.rel__addrow     display:flex · 폭
.rel__select     flex:1 1 0% · width:auto · min-width:0
.popover-root    display:? · width:?      <- 이번에 고치는 자리
.select-trigger  width:100%
```

**한 단계라도 inline 계열이거나 폭이 내용 크기로 굳는 곳이 있으면 거기서 끊긴다.**
그 체인에 끊긴 데가 없다는 것을 보인 뒤에 완료를 보고해라.

## 하지 말 것

- 공용 CSS(`meetings.css`·`components.css`·`screens-a.css`) 금지
- `ds/Popover.tsx` 의 `<span>` 을 바꾸지 마라 — 다른 화면 전부에 퍼진다
- 이 밖의 것을 고치지 마라
- `backend/` 금지 · 커밋·push 금지

## 검증

- **직렬로만**: `npx vitest run --no-file-parallelism` (`make frontend-test` 금지)
- `npx tsc --noEmit`
- 스코프 판의 죽은 규칙 0건 유지 — 새 선택자를 손 목록에 더해라
- 브라우저 띄우지 마라. 사용자 포트(8001·5176·54329) 무접촉

## 리포트

`fe-report.md` 에 `## 14. 셀렉터 폭 — popover-root` 절을 더해
체인 표와 `파일:줄` 을 적어라.

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_e622370a-1f3b-4861-b759-daa3584eace0 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 셀렉터 폭(popover-root) 완료: <한 줄>" \
  --body "체인 표 / 파일:줄 / 검증"

orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] frontend 셀렉터 폭(popover-root) 완료" --enter
```
