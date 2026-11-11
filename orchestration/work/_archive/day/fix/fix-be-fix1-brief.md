# [backend] fix 서버 수정 1 — 코드 리뷰 W1 + 참고 R1 ~ R4 · R6

너는 **day `backend` 워커**(WP-BE-1 · BE-2 작성자 · 같은 터미널)다.

- 리뷰 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-be-report.md` (판정 WARN · FAIL 0)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` — `app/` 은 건드리지 마라(mobile 변경이 미커밋으로 있다). `git stash` · `checkout` 금지.

## 고칠 것

1. **W1 접근 로그의 쿼리 문자열** — `common/logs.py` 의 `uvicorn.access` 로거에 쿼리 지우기 필터 하나(원천 interpret-pwa `back/app/main.py` `DropQueryString` 모양 — 경로의 `?` 뒤를 뺀다). 통역 라우터가 아니라 **공용 로그 한 곳**. HTTP · WebSocket 접근 로그 둘 다 걸리는지 확인한다(uvicorn 이 WS 접근 줄을 어느 로거로 내는지 — A-47 때 본 줄은 `uvicorn.error` 였다 — **줄이 나가는 로거를 전부 찾아** 건다). 시험: 쿼리가 있는 HTTP 줄 · WS 줄에서 `?` 뒤가 로그에 없다 · 쿼리가 없는 줄은 그대로. 채팅의 `since` · 페이지 칸처럼 정상 쿼리도 로그에서 빠지는 것은 받아들인다(리뷰 판정).
2. **R1** — `_cleanup` 에서 STT 닫는 중 취소돼도 TTS 가 닫히게(두 닫기를 서로 독립으로). 자리 반납 한 번은 그대로. 시험 1건.
3. **R2** — `day_interpret_max_sessions` 에 위 상한(`le=50`). 설정 시험에 한 줄.
4. **R3** — `dtos/glossary.py` 가 `services` 를 import 하지 않게(`entry_counts(langs)` 로 인자).
5. **R4** — `tests/architecture` 에 「`day/routers` 는 `run_interpret_session` 을 import 하지 않는다」.
6. **R6** — #22 에서 활성 직원 판정(`actor()`)을 길이 검사 앞에(비활성 직원의 41자 = 403).

R5(DB 연결 실패 = 핸드셰이크 500)는 고치지 않는다(앱 결과 같음 · 로그에 원인이 남는 편이 낫다).

새 의존성 0 · migration 0 · 스펙에 없는 동작 추가 0.

## 검증

- 고친 테스트 파일만 `uv run pytest -q <파일들>` · `uv run ruff check <만진 파일>`.
- 마지막에 `uv run pytest -q -m "not infra"` 1회 + **격리 스택**(앞 판과 같은 방식 — 다른 프로젝트 이름 · 다른 포트 · 끝나면 `down -v`)으로 `scripts/test.sh -q` 1회. 사용자 `day-local-*` · 11040 · 11042 · 11043 금지.
- Soniox · KOS · 서버 호출 없음(seed 갈래 재실행도 하지 않는다 — 따로 승인받는다).

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/be-fix1-report.md` — 항목별 고친 자리(`파일:줄`) · 접근 줄이 나가는 로거 목록과 필터를 건 자리 · 시험 이름 · 수치.

끝나면 **두 명령 모두**(핸들은 dispatch preamble 값이 우선):

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_d8e9c610-96b4-482a-9972-365ca65c1084 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 완료: <한 줄>" \
  --body "항목별 결과 / 시험 수치"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] backend: <질문>" --enter`
