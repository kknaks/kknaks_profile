# 리뷰 리포트 — day-procedure-board-2 / code — `seed_demo_board.py` 반영 1차 재리뷰 (2026-11-09)

대상: 미추적 `scripts/seed_demo_board.py`(661줄) · `backend/tests/scripts/test_seed_demo_board.py`(331줄)
근거: 앞 리포트 `review-seed-demo-board-report.md` · 반영 지시 `be-fix1-brief.md` · 원 be 브리프 §3 · §6 · §7
실행: KOS 호출 0회. `uv run pytest -q backend/tests/scripts` **28 passed**(앞 14 → 28) · `ruff check` 통과 · `ruff format --check` 통과. 워크트리는 미추적 2개 그대로(리포 수정 없음).
W4(국적 alpha-2)는 사용자 승인 대기라 판정에서 뺐다.

## 판정: PASS — 지적 8건 모두 닫힘. 새 FAIL 없음. 참고 2건

---

## 지적별

| 지적 | 판정 | 근거 |
|---|---|---|
| **F1** 공개 키 테넌트 | **닫힘** | `check_open_key_is_demo`(`seed_demo_board.py:115-131`). 공개 `get-zones` 의 기본 구역 id 가 데모 내부 예약 그룹 `intervalCapacities[].zoneId` 에 없으면 `SystemExit` 로 멈춘다. 이 확인은 `masters()` 의 두 번째 조회 바로 뒤(`:265-267`)에서, 방 · 옵션 조회와 모든 쓰기보다 먼저 돈다. dry-run 판단(`:626`)보다도 앞이다. 구역 id 가 비어도 멈춘다(fail-closed, `:127`). 테스트 `test_open_key_of_other_hospital_stops_before_writes`(dry-run 과 실제 실행 둘 다)가 부른 경로가 정확히 `[get-zones, get-reservation-groups]` 인지 단언한다(`test:288`) |
| **W1** 남았을 수 있음 | **닫힘** | 실패 줄(`:580-585`)에 「KOS 에 남았을 수 있음(이름 접미어 `{tag}-{nn}` 로 찾기)」가 붙는다. 실행 접미어는 첫 줄(`:611-613`)에도 찍힌다. 이름 전체는 찍지 않는다 |
| **W2** 재실행 중복 | **닫힘** | `run_tag()`(`:140-142`, `secrets.token_hex(2)`)가 이름에 들어간다(`:173-175`). 같은 칸에서 충돌할 확률은 1/65536. 테스트 `:69-79` |
| **W3** 비-KosError 로 전체 중단 | **닫힘** | `except Exception`(`:635`). 기록은 `error_text`(`:571-573`)로 하는데, `KosError` 면 상태와 오류 이름만, 그 밖은 예외 이름만 남긴다. 쓰기 전 필터도 넓혔다: `option_usable` 가 procedure id · name 을 확인하고(`:211-224`), 방 · 기타 작업도 id · title 이 있는 것만 쓴다(`:271-280`). 그래서 `initialize-purchase` 다음에 `KeyError` 로 멈추는 자리가 없어졌다. 테스트 `:143-169 · 292-305`(「고객 값」이 출력에 없는지도 단언) |
| **W5** 가드 순서 테스트 | **닫힘** | `run()` 이 `client_factory` · `now` 를 주입받는다(`:589-593`). 테넌트 가드(`:601`)와 인자 검사(`:603-609`)는 둘 다 client 를 만들기(`:615`) 전에 돈다. 테스트 `test_run_stops_before_client_on_wrong_tenant`(`:261-266`)와 `test_run_rejects_bad_args_before_client`(`:269-276`)는 factory 가 한 번도 불리지 않았는지 단언한다. 토큰 교환이 0회라는 증명이다 |
| **W6** detail 재시도 테스트 | **닫힘** | 세 경우를 테스트한다: 404 두 번 뒤 성공(`:308-313`), 400 이면 바로 실패(`:316-322`), 마지막 404 는 포기(`:325-331`). 이제 `exc.args` 회귀가 다시 들어오면 테스트가 깨진다 |
| **W7** 지난 칸 · 상한 | **닫힘** | `check_future`(`:134-137`, 시작한 칸도 거부)와 `MAX_COUNT = 30`(`:54 · 168-169`). 앞 리포트의 「23:45 에 `--date <오늘>`」 경우는 오늘 00:00 이 되는데, 지난 칸이라 이제 exit 2 로 거부된다. 잘못된 날짜 · 시각 문자열도 traceback 대신 exit 2 로 끝난다(`:607-609`). 테스트 `:82-93 · 269-276` |
| **W8** 끝 요약 사유 | **닫힘** | 끝 요약(`:643-644`)에 실패한 사람의 번호 · 국적 · 단계 · 사유가 다시 찍힌다. 테스트 `:304` |

## 새로 생긴 「조용히 통과하는 자리」 확인

- **테넌트 가드가 모든 KOS 호출 전인가** — 그렇다. `:601` 은 `client_factory`(`:615`) 전이다. KOS 요청은 전부 client 를 통해 나가므로 그 전에는 요청이 하나도 없다. 테스트가 막는다.
- **F1 확인이 모든 쓰기 전인가** — 그렇다. 쓰기는 `seeder.one()`(`:634`) 안에서만 나가고, `masters()`(`:621`)가 그 전에 끝나야 한다. F1 전에 나가는 요청은 3가지다:
  - `internal_token()` — 내부 sign-in · get-user-account. 데모 테넌트로 간다.
  - 공개 `exchange-token` · `get-zones` — 공개 키의 병원으로 간다.
  - 내부 `get-reservation-groups` — 데모 테넌트로 간다.

  모두 조회이고, 공개 키가 다른 병원 것이면 그 병원에 닿는 요청은 토큰 교환과 구역 조회 2개뿐이다. 그 병원 것인지 증명하려면 조회는 해야 하므로 피할 수 없는 최소치다. PASS.
- **`except Exception` 이 만들다 만 방문을 숨기나** — 숨기지 않는다. `res.stage` 가 단계마다 먼저 갱신되고(`:319 · 347 · 353 · 356 · 376 · 380 · 383 · 452 · 463 · 468 · 471`), `schedule_id` 는 reserve 응답 직후 저장된다(`:338`). 그래서 어느 단계에서 실패하든 줄에 id 끝 4자리 · 단계 · 사유 · 「남았을 수 있음」이 찍히고, 끝 요약에 다시 찍힌다. `SystemExit` · `KeyboardInterrupt` · `CancelledError` 는 `BaseException` 이라 잡히지 않는다. F1 · 가드의 멈춤이 삼켜지지 않는다.
- **예외 메시지로 값이 새나** — 새지 않는다. 비-KosError 는 이름만 남기고(`:573`), 테스트가 「고객 값」이 없는지 단언한다(`test:305`).
- **재시도가 쓰기를 두 번 보내나** — 바뀐 곳이 없다. 재시도는 여전히 `detail` · `tickets` · verify 같은 조회에만 있다. PASS.

## 참고(판정 무관 · 낮음)

1. **실패 보고 테스트가 reserve 단계 실패만 본다**. `test_one_failure_does_not_stop_others` 는 `reserve` 에서 `KeyError` 를 내서 id 가 없는(`----`) 경우만 확인한다. 중간 단계(예: `recept` 다음 실패)에서 id 끝 4자리와 그 단계가 찍히는지는 테스트가 없다. 코드는 맞다(위 근거). FakeKos 의 `internal` 은 쓰기 경로에서 `AssertionError` 를 내므로, reserve 가 성공하게 두면 바로 `detail` → `recept` 실패 경우를 만들 수 있다.
2. **Ctrl-C 로 중간에 끊으면** 끝 요약이 찍히지 않는다. 이미 찍힌 사람별 줄(`:638`, `flush=True`)은 남지만, 끊긴 그 사람의 줄은 없다. 그 사람의 방문은 KOS 에 반쯤 남는다. 사람이 직접 끊는 경우라 WARN 으로 올리지 않았다.

- `test:246` 의 `WRITE_PATHS` 에 쓰기 경로 일부(ROOM · FLOW_STEP · ADD_ITEMS 등)가 빠져 있다. 하지만 바로 위 단언(`:288`)이 부른 경로 목록 전체를 정확히 비교하므로 빈틈은 아니다.
- 실물 재실행(be-fix1 브리프의 「새 칸에서 한 번에」) 결과는 이 리뷰 범위 밖이다(KOS 호출 금지). 워커 보고를 기준으로 본다.
- W4 · 브리프 §2 문구(「공개 change-flow-step」) 건은 앞 리포트 그대로 열려 있다.
