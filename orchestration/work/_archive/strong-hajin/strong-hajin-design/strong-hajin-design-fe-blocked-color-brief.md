# [frontend] 막힘 사유가 아직 «회색»이다 — 검정으로

같은 워크트리에서 이어서 한다. **한 줄짜리다. 새로 조사하지 마라.**

## 무엇이 잘못됐나

지난 판에서 막힘 사유 본문을 `.danger-text`(빨강) → `.prewrap` 으로 바꿨다.
그런데 **`.prewrap` 에는 색이 없다.** 그래서 부모 규칙의 회색이 그대로 남았다.

```
styles/screens-a.css   .drawer-section p { color: var(--scax-color-ink-alt); }   <- 회색
styles/screens-a.css   .prewrap          { white-space: pre-wrap; }              <- 색 없음
```

실제 마크업: `<section class="drawer-section"><h4>막힘 사유</h4><p class="prewrap">…</p></section>`

**사용자가 화면에서 「지금 왜 회색 글씨야」라고 짚었다.**

## 고칠 것

막힘 사유 본문을 **일반 본문 검정**(`--scax-color-ink`)으로 세운다.

- **`styles/screens-a.css` 를 고치지 마라** — 공용 규칙이라 다른 화면이 같이 바뀐다
- `styles/task-detail.css` 에서 **이 화면 안에서만**(`.scax-td` 스코프) 덮어라
- 막힘 사유 문단을 겨눌 수 있게 클래스를 하나 주는 편이 낫다
  (예: `.blocked-reason` — 이름은 네가 정하되 스코프 안이어야 한다)

## 하지 말 것

- 시작 막힘 «배너»의 빨강은 그대로 둔다 — 그건 경고다
- `screens-a.css` · `components.css` 등 공용 CSS 금지
- 이 밖의 것을 고치지 마라
- `backend/` 금지 · 커밋·push 금지

## 검증

- **테스트는 직렬로만**: `npx vitest run --no-file-parallelism`
  (병렬 vitest 가 메모리를 밀어내 사용자 스택이 세 번 죽었다. `make frontend-test` 부르지 마라)
- `npx tsc --noEmit`
- **스코프 판의 손 목록에 새 이름을 더해라** — 안 그러면 「죽은 규칙 0건」이 또 거짓이 된다
- 브라우저 띄우지 마라. 사용자 포트(8001·5176·54329) 무접촉

## 리포트

`fe-report.md` 에 `## 11. 막힘 사유 색` 절을 더해 `파일:줄` 로 적어라.

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_e622370a-1f3b-4861-b759-daa3584eace0 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 막힘 사유 색 수정: <한 줄>" \
  --body "무엇을 고쳤나 / 파일:줄 / 검증"

orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] frontend 막힘 사유 색 수정 완료" --enter
```
