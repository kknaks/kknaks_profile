# [frontend] 상위·프로젝트 셀렉터도 «칸 전체 폭»으로 — 코디가 거꾸로 지시했었다

같은 워크트리에서 이어서 한다. **한 건이다. 새로 조사하지 마라.**

## 무엇이 잘못됐나

코디가 사용자 말을 **거꾸로 읽고** 상위·프로젝트 셀렉터를 내용 너비로 줄이라고 시켰다.
사용자는 **칸을 채우라는 뜻**이었다. 지금 833px 짜리 칸에 200px 셀렉터가 혼자 떠 있다.

**워커 잘못이 아니다. 지시가 틀렸다.**

## 고칠 것

`상위 업무` · `프로젝트` 셀렉터를 **칸 전체 폭**으로 세운다.
「추가」 줄과 **같은 모양**이 되면 된다.

```
task-detail.css:153 근처   .scax-td .rel__select { width: fit-content; min-width: 200px; max-width: 100% }
                           -> 칸을 채우게 바꾼다 (width:100%)
```

⚠ **`popover-root` 까지 같이 펴야 한다.** 바깥만 늘리면 지난 세 판처럼 또 안 늘어난다.
지금 그 규칙이 「추가」 줄에만 걸려 있다.

```
지금   .scax-td .rel__addrow .rel__select > .popover-root { display:flex; width:100% }
바꿈   .scax-td .rel__select > .popover-root { display:flex; width:100% }   (두 자리 모두)
```

사슬 일곱(`.cell` → `.rel__addrow`/`.cell` → `.rel__select` → `.popover-root` → `.select-trigger`)이
**두 자리 «모두»에서 끊긴 데 없이** 서야 한다. 네가 §14 에 만든 사슬 판을
상위·프로젝트 자리에도 적용해 **두 곳 다** 세라.

## 하지 말 것

- 공용 CSS(`meetings.css`·`components.css`·`screens-a.css`) 금지
- `ds/Popover.tsx` 금지
- 이 밖의 것을 고치지 마라
- `backend/` 금지 · 커밋·push 금지

## 검증

- **직렬로만**: `npx vitest run --no-file-parallelism` (`make frontend-test` 금지)
- `npx tsc --noEmit`
- **사슬 판을 상위·프로젝트 자리까지 넓혀라** — 「추가」 줄만 세고 있으면 같은 실패가 또 숨는다
- 죽은 규칙 0건 유지
- 브라우저 띄우지 마라. 사용자 포트(8001·5176·54329) 무접촉

## 리포트

`fe-report.md` 에 `## 15. 상위·프로젝트 셀렉터 폭` 절을 더해
**두 자리의 사슬 표**와 `파일:줄` 을 적어라.

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_e622370a-1f3b-4861-b759-daa3584eace0 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 상위·프로젝트 셀렉터 폭 완료: <한 줄>" \
  --body "두 자리 사슬 표 / 파일:줄 / 검증"

orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] frontend 상위·프로젝트 셀렉터 폭 완료" --enter
```
