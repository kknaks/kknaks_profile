# 재검수 r2 — WORK-012 WP2 수정 1

- 검수자: reviewer(read-only) · 2026-10-07
- 대상: `be-wp2-fix1-report.md` 가 적은 변경(코드 워크트리 미커밋 diff 중 WP2 수정분)
  - lease(`settings.py` · `meeting_worker.py` · `finalize.py` 상수)
  - 웜스타트 락 · CAS(`batch_service.py` · `platform/meetings.py` · `mtg/application.py` · 게이트웨이)
  - 보정 표 `null`(`finalize.py` · `platform/meetings.py`)
  - AI 벌 조립 위치
  - stdin 전달(`cli_process.py` · `codex_cli.py` · `claude_cli.py`)
  - 새 시험 `test_meeting_worker_heartbeat.py` · `test_cli_prompt_stdin.py` · 추가분
- 기준: 1차 리포트 `review-wp2-code-report.md` §8
- 한 일: 코드 읽기 · `rg` 재확인. **시험·빌드·실물 CLI 는 돌리지 않았다** — 수치는 워커 값(지정 파일 253 passed · postgres 2 passed)
- 약어: `B/` = `backend/src/ax_workspace/` · `T/` = `backend/tests/`

---

## 0. 판정 — **WARN**

1차의 F-1 · F-2 · W-1 · W-2 · W-3 · W-4 는 **모두 고쳐졌다**(§1). 고치면서 교착이나 새 경주는 생기지 않았다(§2).
**FAIL 0 · WARN 6.** 그중 둘은 운영 반영 전에 확인해야 한다.

1. **실물 CLI 확인** — 운영 이미지의 `codex`·`claude` 가 stdin 프롬프트를 받는지 1회(W-r2-1)
2. **heartbeat 예외 처리** — heartbeat 가 예외(DB 끊김)로 죽으면 연장이 멈춘 채 합성 스레드만 고아로 남고, 워커는 다음 잡을 집는다(W-r2-2)

---

## 1. 1차 지적 — 항목별

| # | 1차 지적 | 지금 | 판정 |
|---|---|---|---|
| F-1 | lease 바닥 3300초가 최종 호출 최대 4회(4800초)를 못 담음 · 연장 없음 | **최대 호출 수를 상수로**: `FINAL_MAX_PROVIDER_CALLS = FINAL_ATTEMPTS + 2 = 5` `B/modules/meetings/finalize.py:49`<br>— 시도 3 + 첫 resume 세션 유실의 콜드 폴백 1 + timeout 뒤 새 세션 1. 내가 센 4회보다 정확하다. 다시 세어도 5가 최악이다(유실 폴백은 첫 resume 에만 · 새 세션은 `session_ref=None` 이라 유실이 없다)<br>**바닥** `B/bootstrap/settings.py:203-218` = 재전사 `retranscribe.TIMEOUT_SECONDS`(상수 import) + 5×최종 + 300 = **6000초**<br>**heartbeat** `B/bootstrap/meeting_worker.py:84-106`: 합성은 `to_thread`, lease/3(2000초)마다 `extend_lease(…, 6000)` — report·material 워커와 같은 결 | **PASS** |
| F-2 | 세션 없는 배치가 락 밖 웜스타트와 경주 | **웜스타트를 회의당 락 안으로** `B/modules/meetings/batch_service.py:189-200`. 도는 동안 온 트리거는 `evaluate` 가 `is_running` 으로 미루고(`:237-240`), 판정과 잡기 사이에 엇갈린 `run` 도 미루고 시간 트리거를 건다(`:284-292`) → 락을 놓은 자리에서 `_repay_deferred`(`:299-308`)<br>**기록 CAS** `B/platform/meetings.py:957-986`: 회의 행 `FOR UPDATE` 뒤 `expected` 일 때만 교체, 남은 참조를 돌려준다. 웜스타트 `expected=None`(`batch_service.py:221`) · 새 세션 배치 `expected=batch.session_ref`(`:383-388`) | **PASS** |
| W-1 | 프롬프트 argv 한 칸(리눅스 128KiB) | **stdin 으로**<br>— 러너 `B/platform/cli_process.py:106-130,143-205`: `stdin=PIPE` + 별도 쓰기 스레드 + `BrokenPipe/OSError` 흡수 + 닫기<br>— Codex 대화·resume·단발 생성 argv 끝 `"-"`(`codex_cli.py:94,334,336,618`) + `stdin_text=prompt`(`:143,234`)<br>— Claude argv 에서 프롬프트 제거(`claude_cli.py:287`) + `stdin_text`(`:111,187`) · `--json-schema` 는 argv(수 KB)<br>워커가 실제 조립 함수로 잰 바이트: 이번 운영 회의 크기에서도 169KB(129%) → stdin 이 맞는 선택이다 | **PASS**(실물 확인 W-r2-1) |
| W-2 | 표 칸이 없어도 `[]` 로 기록 | `parse_term_corrections` 가 칸 없음·배열 아님이면 `None`(`finalize.py:140-155`) → `replace_term_corrections(rows=None)` 이 표를 비우고 `term_corrected_at` 을 걷는다(`platform/meetings.py:820-834`) → 응답 `null`. `[]` 는 시각을 찍는다 | **PASS** |
| W-3 | lease 시험이 셈식만 단언 | `T/unit/test_meeting_finalize_service.py::test_the_worst_delivery_never_calls_the_provider_more_than_the_lease_budget` — 최악 대본으로 **루프를 실제로 돌려 센 호출 수 == `FINAL_MAX_PROVIDER_CALLS`** · `lease ≥ 재전사 + 센 수 × 최종 상한` | **PASS** |
| W-4 | 배치마다 AI 벌 조립 | `batch_input` 에서 뺐다 · 새 세션 갈래만 `gateway.ai_track(meeting_id)`(`batch_service.py:375` → `bootstrap/application.py:600` → `mtg/application.py:1462`) | **PASS** |

---

## 2. 새로 생긴 위험

### 2-1 lease heartbeat

| 물음 | 본 것 | 판정 |
|---|---|---|
| 연장이 `False`(lease 를 잃음) | 경고 로그만 · 합성은 계속 · 완료/실패는 lease token 으로 fenced | PASS — 바닥 6000초가 정상 최악 뒤로 밀어 둔다 |
| **연장이 예외**(DB 끊김 · `SQLAlchemyError`) | `_handle_with_heartbeat` `meeting_worker.py:92-99` 는 `_heartbeat` 예외를 잡지 않는다. 그래서 루프를 빠져나가고 `run_once` 도 예외로 끝난다. 그런데 `asyncio.to_thread` 로 띄운 합성(`work`)은 **취소되지 않고 계속 돈다**(스레드는 취소 불가). 다음 일이 이어진다:<br>— `run()`(`:57-66`)이 `SQLAlchemyError` 를 잡고 짧게 쉰 뒤 **다음 잡을 claim** → 한 워커 안에서 합성이 둘 겹친다<br>— 고아 합성 쪽은 더는 연장되지 않는다(바닥 6000초가 그나마 막는다)<br>— DB 가 잠깐만 끊겨도 생긴다 | **WARN(W-r2-2)** — `_heartbeat` 를 `try/except Exception` 으로 감싸 로그만 남기고 루프를 이어 가게 한다(report 워커 패턴 확인 권장) · 시험: 연장 실패(`False`)·예외 두 갈래 |
| 스레드 정리·종료 | `stop()` 뒤 `run()` 이 끝나도 도는 합성 스레드는 `asyncio.run` 종료 때 기본 executor 를 기다린다(최대 한 배달) — 옛 동작(합성을 이벤트 루프에서 동기 실행)과 같은 결 | PASS |
| 시험 | `T/unit/test_meeting_worker_heartbeat.py` — 0.4초 합성 · 0.05초 간격으로 연장이 «있었나» 만 본다(창을 재지 않는다 — serial 대상 아님 · 판단 맞음) · 실패 갈래 시험 없음 | WARN(W-r2-2 와 함께) |

### 2-2 웜스타트를 락 안으로 — 락 보유 시간 · 교착

| 물음 | 본 것 | 판정 |
|---|---|---|
| 락을 쥐는 시간 | 웜스타트 상한 × 2(timeout 뒤 1회 더) = 최대 480초. 그동안 그 회의의 **배치만** 미뤄진다(`evaluate`·`run` 모두 기다리지 않고 미룸 · 90초 타이머가 다시 미룸). 미룬 것은 락을 놓을 때 갚는다 | PASS — 회의 중 AI 탭이 그만큼 늦게 서는 것은 받아들인 비용 |
| 회의 종료·재시도와 교착 | 최종 합성의 락은 **다른 것**이다 — `finalize_service.py:141` 의 자기 `_lock_for`. 합성은 **워커 프로세스**에서 돌고, 웜스타트는 API 프로세스에 있다. 두 락을 함께 쥐는 경로가 없다 → 교착 없음<br>종료 뒤 미룬 배치를 갚아도 `batch_input` 이 「진행 중」 이 아니면 `None` 이다 | PASS |
| BE 리포트 미결 3 「회의를 시작하자마자 종료하면 최종이 웜스타트를 기다린다」 | **사실과 다르다** — 위처럼 락이 달라 기다리지 않는다. 최종은 그때 원장에 세션이 없으면 콜드로 돈다(전사 전량을 매번 실으니 결과는 같다). 늦게 끝난 웜스타트가 종료된 회의에 세션을 CAS 로 기록하는 일은 무해하다 | 참고(W-r2-5 — 리포트 문구만) |
| 같은 회의에 웜스타트가 둘 | 시작 입구 넷(`bootstrap/application.py:1787,1821,3799,3905`) — 락으로 줄 서고 둘째는 CAS 에서 진다 → 세션 하나 · provider 호출은 두 번(드묾) | PASS |

### 2-3 세션 CAS 실패 갈래

| 갈래 | 본 것 | 판정 |
|---|---|---|
| 웜스타트가 짐(`expected=None` 인데 이미 있음) | 웜스타트 세션 버림 + 경고 — 그 세션은 provider 쪽에 남는다(무해) | PASS |
| 새 세션 배치가 짐(그 사이 다른 쪽이 교체) | 참조는 버리되 **본문은 적재한다** — 그 본문은 「지금까지의 AI 벌 + 이번 구간」 을 다 받아 쓴 것이라 맞다. 다음 배치는 원장의 이긴 세션을 이어 쓴다 | PASS |
| 행 잠금 | 회의 행 `FOR UPDATE` 는 짧다(읽고 한 행 쓰기) — 회의 수정과 잠깐 줄 설 뿐 | PASS |
| 시험 | `test_a_batch_arriving_during_a_slow_warm_start_waits_and_uses_that_session` · `test_recording_a_session_is_compare_and_set` | PASS |

### 2-4 stdin 전달

| 물음 | 본 것 | 판정 |
|---|---|---|
| 쓰기 스레드 | `feed_stdin` 데몬 스레드가 쓰고 `finally` 에서 닫는다. stdout·stderr 는 각자 스레드가 비우므로 큰 입력과 큰 출력이 서로 막지 않는다 | PASS |
| 자식이 일찍 죽음 | 쓰기 중 `BrokenPipeError`/`OSError` 를 삼킨다(파이썬은 SIGPIPE 를 무시하므로 예외로 온다). 결과는 returncode·stderr 가 말한다 | PASS |
| timeout | 기한을 넘기면 프로세스 그룹을 멈추고(`_stop_process_group`) 세 스레드를 `join(2)` 한 뒤 `TimeoutExpired` → `ProviderTimedOut`. 쓰기 스레드는 파이프가 닫혀 깨어난다 | PASS |
| 취소 | `should_cancel` → 그룹 정지 → 같은 길 | PASS |
| 큰 입력 교착 | 쓰기와 읽기가 다른 스레드라 없다 · 600KB 실제 자식 프로세스 시험(`test_cli_prompt_stdin.py:23` · `@pytest.mark.serial` — 자식 프로세스 규칙 지킴) | PASS |
| **옛 러너 되돌이** | `invoke_runner`(`cli_process.py:115-123`)가 `stdin_text` 호출에서 `TypeError` 를 잡는다. 메시지에 `"positional"`·`"on_line"`·`"should_cancel"`·`"stdin_text"` 중 하나가 있으면 **stdin 없이 다시 부른다**. 이때 걸리는 일이 둘이다:<br>— ① 제품 러너 안에서 다른 이유로 난 `TypeError` 가 그 낱말을 품으면 → **프로세스를 두 번 띄운다**<br>— ② 되돌이 호출에서 Codex 는 argv 가 `-` 인데 stdin 이 `/dev/null` → **빈 프롬프트로 돈다**(조용한 오동작)<br>지금 제품 러너(`subprocess_runner`)는 키워드를 다 받아 실제로 걸릴 가능성은 낮다 | **WARN(W-r2-3)** — 되돌이를 「러너 시그니처에 `stdin_text` 가 없을 때」(`inspect.signature`)로 좁히거나, stdin 을 못 넘기는 러너면 예외로 끝낸다 |
| 인코딩 | `Popen(text=True)` 에 `encoding` 이 없다 → stdin 쓰기도 로케일 인코딩이다. 컨테이너가 C/POSIX 로케일이면 파이썬 UTF-8 모드라 괜찮지만, 다른 비 UTF-8 로케일이면 한국어 프롬프트가 `UnicodeEncodeError`(→ 쓰기 스레드가 `OSError` 가 아니라 그 예외로 죽고, 자식은 빈 입력)다. stdout 읽기도 이미 같은 가정이다 | WARN(경미 · W-r2-4) — `encoding="utf-8"` 명시 |
| 실물 CLI | 워커가 `codex-cli 0.160.1`(`exec`·`exec resume` 의 `-` = stdin) · Claude Code `2.1.284`(`--print` 에서 파이프 입력)를 이 기계에서 확인했다. **운영 이미지 버전은 확인하지 않았다** — 거기서 `-` 를 모르면 Codex 가 「-」 를 프롬프트 글자로 받는다 | **WARN(W-r2-1)** — 운영 반영 전 실물 1회(코디) |

---

## 3. FAIL / WARN 목록(재발주용)

### FAIL — 없음

### WARN (6)

| # | 팀 | 자리 | 무엇 | 권장 |
|---|---|---|---|---|
| W-r2-1 | 코디(실물) | 운영 이미지의 `codex` · `claude` | stdin 프롬프트(`exec … -` · `--print` 파이프)를 받는지 미확인 | 운영 이미지에서 최종 합성 1회 · 짧은 대화 1회 |
| W-r2-2 | BE | `B/bootstrap/meeting_worker.py:92-106` | heartbeat 예외가 루프를 끊는다 → 연장 멈춤 + 합성 스레드 고아 + 워커가 다음 잡을 집어 한 워커에서 합성 둘 | `_heartbeat` 를 잡아 로그만 · 실패(`False`)·예외 시험 두 갈래 |
| W-r2-3 | BE | `B/platform/cli_process.py:115-123` | `TypeError` 낱말 맞추기로 stdin 없는 옛 호출로 되돌아감 — 프로세스 이중 실행 · Codex 빈 프롬프트 가능 | 시그니처 확인으로 좁히거나 되돌이 금지 |
| W-r2-4 | BE | `B/platform/cli_process.py` `Popen(text=True)` | 인코딩 미지정(로케일 의존) | `encoding="utf-8"` |
| W-r2-5 | BE(리포트 문구) | `be-wp2-fix1-report.md` §7-3 | 「종료하면 최종이 웜스타트를 기다린다」 — 실제로는 기다리지 않는다(다른 락 · 다른 프로세스). 동작은 안전하다 | 문구 정정만 |
| W-r2-6 | 코디 | 1차 W-8 | 새 표·칸 → `make sync-demo-schema` 뒤 `make local-stack` 재시작 · 운영 SQL 은 이미지보다 먼저 | 그대로 유효 |

### 확인한 것 / 확인 안 한 것

- **확인한 것**
  - 수정분 코드 전부
  - 최대 호출 수 5 를 루프 갈래로 다시 셈
  - 락 경로(배치·웜스타트·최종 — 서로 다른 락·프로세스)
  - CAS 두 갈래
  - stdin 러너의 쓰기·timeout·취소·되돌이
  - 새 시험의 단언과 serial 마커
- **확인 안 한 것**
  - 시험 실행 · 실물 CLI · 운영 이미지 로케일·CLI 버전
  - `report_worker` 의 heartbeat 예외 처리 패턴(비교 권장만)
