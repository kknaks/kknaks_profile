# [frontend] 셀렉터 너비 · 「추가」 워딩

같은 워크트리에서 이어서 한다. **작은 것 둘이다. 새로 조사하지 마라.**

## 1. 상위·프로젝트 셀렉터가 칸을 꽉 채운다

사용자: 「이거 너비 왜 이래 다 셀렉터 이상하잖아」

```
styles/task-detail.css   .scax-td .rel__select { width: 100%; }   <- 405px 까지 늘어난다
```

「— 없음 —」 한 단어짜리 드롭다운이 칸 전체를 먹는다. 옆 칸들은 이제 테두리 없이
이어진 부품인데 **상위·프로젝트만 큰 상자**라 혼자 튄다.

**내용 너비로 줄인다.** 다만 고를 때마다 폭이 튀지 않게 최소 폭을 준다.

- `width: 100%` 를 걷고 내용에 맞춘다
- `min-width` 는 200px 안팎 · `max-width: 100%`
- **연결 편집의 「추가」 줄(`.rel__addrow .rel__select`)은 지금처럼 남은 폭을 채운다** —
  거기는 라벨 옆이라 늘어나는 게 맞다. 그 규칙을 건드리지 마라

## 2. 하위 업무 칸의 「추가」 워딩

사용자: 「이거는 하위업무 생성이잖아 워딩 바꿔」

`연관 업무 > 하위 업무` 칸 머리의 단추는 **새 업무를 만드는** 입구다(생성 모달을 연다).
그런데 문구가 「추가」라서 **기존 것을 붙이는 것**처럼 읽힌다 —
연결 편집의 「추가 [업무 고르기]」(진짜로 기존 것을 붙인다)와 헷갈린다.

**「하위 업무 생성」으로 바꾼다.**

- 문구는 `lib/labels.ts` 에 둔다. 하드코딩하지 마라
- **연결 편집의 「추가」는 그대로 둔다** — 거기는 실제로 붙이는 것이다
- 다른 칸(체크리스트·참고 자료·결과 자료)의 「추가」는 **이번에 건드리지 마라**

## 하지 말 것

- 공용 CSS(`components.css`·`screens-a.css`) 금지
- 이 둘 밖의 것을 고치지 마라
- `backend/` 금지 · 커밋·push 금지

## 검증

- **테스트는 직렬로만**: `npx vitest run --no-file-parallelism` (`make frontend-test` 금지)
- `npx tsc --noEmit`
- 문구를 바꿨으니 그 문구를 찾는 기존 테스트가 있으면 같이 고쳐라
- 스코프 판의 죽은 규칙 0건 유지
- 브라우저 띄우지 마라. 사용자 포트(8001·5176·54329) 무접촉

## 리포트

`fe-report.md` 에 `## 12. 셀렉터 너비 · 「추가」 워딩` 절을 더해 `파일:줄` 로 적어라.

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_e622370a-1f3b-4861-b759-daa3584eace0 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 셀렉터 너비·워딩 완료: <한 줄>" \
  --body "둘 각각 파일:줄 / 검증"

orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] frontend 셀렉터 너비·워딩 완료" --enter
```
