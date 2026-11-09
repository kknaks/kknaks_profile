# 피드백 묶음 검수 WARN 반영 — 백엔드 몫 (W1 · W2 · W3 · W5 · W6)

`4c2cebab` 위 미커밋. 템플릿 · `day.js` · `web.py` · `tests/day/web/` · `test_web_login.py` 는 frontend 몫이라 건드리지 않았다(diff 에 보이는 그 파일들은 frontend 변경).

## #231 영향
- 시술 줄 `doctor` 가 바뀐다. 유효 호출이 있으면 **그 호출을 수락한 의사만** 보이고, 다시 호출한 뒤 아직 수락이 없으면 null 이다(W2).
- 호출이 없는 줄은 전처럼 KOS 집도의다. 화면 변경은 필요 없다(값 그대로 그리면 된다).

## W1 바로 보내기 시간 상한(머지 전 필수)
- `outbox_kick.send_now` 를 `asyncio.timeout(OUTBOX_KICK_TIMEOUT_SECONDS)`(설정 · 기본 **1.0초** · 0 < x ≤ 10)로 감쌌다.
  - 넘으면 `outbox kick timed out hospital=… after 1.0s` 로그를 남기고 `False` 를 돌려준다. 조작 응답은 성공이다(10초 주기가 메운다).
- 테스트(DB 없이): 멈추는 가짜 broker(`kick` 이 영원히 기다림).
  - `send_now(timeout=0.2)` 가 1초 안에 False 로 끝난다.
  - `_finish` 도 상한 안에 결과를 돌려준다(commit 1 · 발행 0).

## W2 다시 호출 확인 조건 · 줄에 보이는 의사
- 데모 실물 기록을 다시 봤다. 이미 수락된(KOS READY) 시술을 다시 부른 실물은 아직 없다. 지금까지의 `call-tasks-doctors` 6건은 모두 처음 호출이었다(상태 · 순서만 확인).
  - KOS 가 READY 를 유지하는지는 미확인이다. 그래서 다시 호출의 확인 조건을 **`status_in = [waiting, ready]`**(새 확인 키)로 바꿨다.
  - 이유: `waiting` 만 기다리면 끝내 안 맞아 stale → failed 로 그 방문의 뒤 쓰기까지 막힌다. 보냈다는 증거는 2xx(sent)다.
  - 처음 호출은 그대로 `status = waiting` 이다.
  - **데모 실물에서 수락된 시술을 다시 호출해 KOS 상태를 보면 조건을 좁힐 수 있다** — 코디 몫으로 남김.
- 줄 의사(`board_rules.task_doctor`): 유효 호출이 있으면 그 호출의 수락 의사(없으면 null)를 보인다. 유효 호출이 없을 때만 KOS 집도의다.
  - 다시 호출 뒤 KOS `doctorIds` 에 남은 앞 의사가 보이지 않는다.
  - [시작] 조건(`start_block`)은 원래 유효 호출 수락만 봐서 바뀌지 않았다.

## W3 섞어 고르기
- `_call_intents(again=…)` 가 **처음 호출분 → 다시 호출분**으로 `call_doctors` 를 둘로 계획한다(`rules.called_ids`).
- 운영 연결(cc 근거 쓰기 꺼짐)에서는 다시 호출분만 `not_supported` 로 드러나고, 처음 호출분은 KOS 로 나간다.

## W5 「조용히 통과」 보강(백엔드 테스트)
| 자리 | 보강 |
|---|---|
| `test_outbox_kick` commit 뒤 발행 | 발행 순간의 commit 수를 기록해 `[1]` 로 단언한다(발행을 commit 앞에 두면 깨진다) |
| `test_cc_근거_쓰기는_trial_에서만_열린다` | `[1:]` 를 뺐다. 다시 호출 경로 · 본문 · 확인 조건(`status_in`)까지 단언한다 |
| 운영 연결 API 경로 | `test_운영_연결은_다시_호출분만_닫히고_처음_호출분은_나간다` — `services.board.trial_writes` 를 False 로(운영과 같음) 두고 API 로 섞어 고르기 → 처음 호출 1건만 적재 + `call_doctors not_supported`. 시작 취소 op 0 + `not_supported`. `trial_writes` 를 True 로 바꾸면 깨진다 |
| W3 데모 | `test_섞어_고르면_처음_호출분과_다시_호출분을_따로_보낸다` — 두 op 의 sequences · 확인 조건 |
| W2 | `test_다시_호출_확인은_WAITING_또는_READY`(계약) · `test_다시_호출한_줄은_KOS_의_앞_의사를_보이지_않는다`(규칙) |
| `test_board_page.py` F5 `== []` | frontend 몫(화면 테스트) — 건드리지 않음 |

## W6 (백엔드 몫)
- 주석을 고쳤다: `services/board.py` 시작 취소 「KOS 쓰기는 닫혀 있다」 · 귀가 대기 「둘 다 닫혀 있다」 → 「cc 근거 쓰기 — 데모 연결에만」.
- `cancel-flow-tasks` 본문 `reason=CANCEL` 은 cc 모양 그대로다. 데모 실물 2회 confirmed(피드백 2차 리포트)로 KOS 가 받는 것은 확인됐다. HAR 은 여전히 없다.
- `test_web_login.py` 테스트 이름 · `test_board_page.py` 주석 · 팝오버 · CSS 는 frontend 몫이다.

## W4 (참고 · 백엔드 손 안 댐)
- `asset_v` = 파일 mtime(`web.py`)은 배포 Delivery 에서 빌드 값으로 바꿀 것 — 리뷰 그대로 남김.

## 검증
| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | 303 passed |
| `scripts/test.sh -q` | **460 passed** — 첫 실행은 다른 작업(frontend)의 테스트가 같은 `day_test` 스키마를 동시에 지워 오류. 그 실행이 끝난 뒤 다시 돌려 통과 |
| ruff check · format --check | 통과 |
| compose | down 안 함 · `--profile app up -d --build --wait api worker scheduler` · `/health/ready` ok |

## 남은 것
- 데모 실물: 수락된 시술 다시 호출 → KOS 상태(READY 유지 / WAITING) 확인 뒤 W2 확인 조건 좁히기 · 「시작 취소」 `PROCEDURE_WAITING` 1회(2차 리포트 그대로).
- 같은 워크트리에서 두 작업이 `scripts/test.sh` 를 동시에 돌리면 `day_test` 가 서로 지워진다 — 테스트 스키마를 작업마다 나누는 것(AGENTS 「xdist · 워커마다 스키마」)은 별도 결정.
