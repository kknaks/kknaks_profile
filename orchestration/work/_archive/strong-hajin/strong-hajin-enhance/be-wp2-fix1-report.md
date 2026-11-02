# WP2 수정 1 결과 보고 — 코드 검수 FAIL 2 · WARN 반영

## 상태: done (커밋하지 않음 · `e51fe3b` 위 워크트리 변경에 이어서)

- 근거: `be-wp2-fix1-instructions.md` · `review-wp2-code-report.md` §4 F-1·F-2 · §5·§7 W-1·W-2·W-4
- 경로 약어: `B/` = `backend/src/ax_workspace/` · `T/` = `backend/tests/`

## 1. F-1 + W-3 — 합성 잡 lease

**고른 것: heartbeat 연장(주) + 루프 상수에서 셈한 바닥(안전판), 둘 다.**

이유:
- 저장소에 이미 같은 패턴이 있다. report 워커(`bootstrap/report_worker.py:132,151`)와 material 워커(`material_worker.py:155,175`)가 `DurableJobQueue.extend_lease` 로 연장한다.
- 최종 900초 × 최대 5회 + 재전사 1200초면 한 배달이 1시간 30분까지 갈 수 있다. 바닥만 키우면 워커가 죽었을 때 그만큼 오래 기다린 뒤에야 다른 워커가 회의를 집는다.
- heartbeat 는 정상일 때 lease 를 계속 이어 주고, 바닥은 연장이 끊겨도 한 배달의 최악이 lease 안에 들게 한다.

| 무엇 | 위치 |
|---|---|
| **루프의 실제 최대 호출 수** 상수 `FINAL_MAX_PROVIDER_CALLS = FINAL_ATTEMPTS + 2` | `B/modules/meetings/finalize.py:49`. 내역: 시도 3 + 세션 유실 콜드 폴백 1(첫 resume 이 「세션 없음」 이면 같은 시도 안에서 한 번 더 부르고, 그 뒤 시도는 세션 없이 돈다) + timeout 뒤 새 세션 1(상한과 무관하게 보장) = **5**. 검수가 센 4회에 세션 유실 폴백 1회를 더했다 |
| 바닥 셈 | `Settings.effective_meeting_finalize_lease_seconds` `B/bootstrap/settings.py:203` = 재전사 `retranscribe.TIMEOUT_SECONDS`(1200, 상수를 import — 중복값 삭제) + `FINAL_MAX_PROVIDER_CALLS` × 최종 상한 + 300 → 기본 **6000초**(설정값이 더 크면 그 값) |
| heartbeat | `B/bootstrap/meeting_worker.py` — `_handle_with_heartbeat` `:84`: 합성은 `asyncio.to_thread` 로 돌고, 그동안 `heartbeat_seconds`(기본 lease/3)마다 `_heartbeat` `:100` 가 `extend_lease(job, token, lease)` 를 부른다. 연장 실패(lease 를 이미 잃음)는 경고 로그만 남긴다 — 도는 합성은 멈출 수 없고, 완료·실패 처리는 lease token 으로 fenced 되어 있다. 생성자 `heartbeat_seconds` 인자 `:38`(시험용) |
| **시험 — 루프와 셈을 대조** | `T/unit/test_meeting_finalize_service.py::test_the_worst_delivery_never_calls_the_provider_more_than_the_lease_budget` — 최악 대본(resume 세션 없음 → 콜드 형식 위반 ×2 → timeout → 새 세션 형식 위반)으로 **루프를 실제로 돌려 센 호출 수**가 `FINAL_MAX_PROVIDER_CALLS`(=5)와 같은지 보고, `effective_meeting_finalize_lease_seconds ≥ 재전사 + 센 수 × 최종 상한` 을 단언한다(셈식을 그대로 베끼지 않는다). `T/unit/test_meeting_worker_heartbeat.py` — 합성이 heartbeat 간격보다 오래 돌면 그 lease 값으로 연장하고 끝나면 complete. 옛 셈식 단언(`≥1200+900+900`)은 「최종 상한에 따라 바닥이 움직인다」 로 바꿨다(`test_ai_stage_timeouts.py`) |

## 2. F-2 — 세션 없는 배치 ↔ 진행 중 웜스타트 경주

**고른 것: 둘 다** — ① 웜스타트를 회의당 락 안에서 돌린다 ② 세션 기록을 CAS 로 바꾼다.

| 무엇 | 위치 |
|---|---|
| 웜스타트 = 회의당 락 안 | `B/modules/meetings/batch_service.py` `warm_start` `:189` → 락 안의 `_warm_start_locked` `:201` → 락을 놓은 자리에서 `_repay_deferred` `:299`. 웜스타트가 도는 동안 온 트리거는 `evaluate` 가 「도는 중」 으로 보고 미뤄 두고(`:239`), 웜스타트가 끝나면 그 자리에서 갚는다. 그래서 세션 없는 배치가 자기 세션을 따로 열 틈이 없다. 판정과 락 잡기 사이에 엇갈린 `run` 도 트리거를 미루고 시간 트리거를 건다(`:289`) — 잃지 않는다 |
| 세션 기록 = compare-and-set | 저장소 `record_ai_session(…, expected)` `B/platform/meetings.py:957` — 회의 행을 `FOR UPDATE` 로 잠그고, 지금 참조가 `expected` 일 때만 갈아 끼운다. 돌려주는 값은 남은 참조다. 적용 `mtg/application.py:1483` · 게이트웨이 `bootstrap/application.py`(`record_session`). 웜스타트는 `expected=None`(`batch_service.py:221`), 새 세션 배치는 `expected=batch.session_ref`(`:386`) — 진 쪽 세션은 버리고 경고 로그를 남긴다 |
| **경주 시험** | `T/contract/test_meeting_minutes_enhance.py::test_a_batch_arriving_during_a_slow_warm_start_waits_and_uses_that_session` — 웜스타트를 붙잡은 채 배치를 냄 → 배치는 서지 않고 미뤄짐(새 세션 0) → 풀면 미룬 배치가 웜스타트 세션 `session-1` 을 이어 씀 · `fresh == []`(이중 provider 호출 없음) · 세션 하나. `test_recording_a_session_is_compare_and_set` — 늦은 웜스타트(`expected=None`)는 덮어쓰지 못하고, 이어 쓰던 쪽은 자기가 본 참조를 기대하고 갈아 끼운다 |

## 3. W-2 — 보정 표 칸이 없으면 `null`

- `parse_term_corrections` 는 칸이 없거나 배열이 아니면 `None` 을 돌려준다(`B/modules/meetings/finalize.py:140-155`). `FinalNotes.term_corrections` 의 기본값도 `None` 이다.
- 적재: `None` 이면 `replace_term_corrections(rows=None)` 이 표를 비우고 `term_corrected_at` 을 걷는다(`B/platform/meetings.py:830`, 호출 `mtg/application.py` `commit_finalized`) → 응답 `null`. `[]` 는 「돌았는데 없음」 으로 그대로 시각을 찍는다.
- 시험:
  - `test_a_final_answer_without_the_term_table_is_null_not_an_empty_table`
  - `test_a_final_answer_whose_term_table_is_not_a_list_is_null`
  - 도메인 `test_a_missing_or_malformed_term_table_is_none…`(`[]` 는 `[]`)

## 4. W-4 — AI 벌 조립은 새 세션 갈래에서만

- `batch_input` 에서 `ai_track` 조립을 뺐다. `BatchInput.ai_track` 칸도 지웠다.
- 새 세션 갈래 `_run_in_new_session` 만 게이트웨이 `ai_track(meeting_id)` 를 부른다(`batch_service.py` · `bootstrap/application.py:600` → `mtg/application.py:1462` `ai_track_material`). 이어 쓰는 배치는 이제 매 회차 AI 벌을 조립하지 않는다.

## 5. W-1 — 프롬프트 argv 한 칸 (운영 장애 위험)

### ① 최악 바이트 — 셈 (실제 조립 함수 `build_final_prompt` + `render_ai_context_catalog` + Codex 대화 감싸기에 합성 데이터를 넣어 UTF-8 바이트를 쟀다)

- 전사: 운영 회의 23.5분 = 8,882자 → **1시간 ≈ 22,677자**. 블록 60자 단위 · 화자 4.
- 두 벌: 안건 8 × 줄 8 씩.
- 맥락 목록의 운영 규모는 **가정**이다(운영 DB 를 보지 않았다 — 코디 확인 필요). 이름·제목은 한국어 10~20자.

| 경우 | 맥락 목록 | 최종 프롬프트 | **argv 한 칸(정책 6종 포함)** | 리눅스 한 인자 128KiB 대비 |
|---|---|---|---|---|
| 이번 운영 회의(23.5분) · 소규모 가정(프로젝트 30 · 열린 업무 300 · 구성원 60) | 67,882B | 151,197B | **169,091B** | **129%** |
| 1시간 · 가정(프로젝트 50 · 열린 업무 500 · 구성원 100) | 112,962B | 258,733B | **276,627B** | **211%** |
| 2시간 · 큰 조직 가정(100 · 1,500 · 300) | 334,262B | 582,840B | **600,734B** | **458%** |

→ **이번 운영 회의 크기에서도 이미 128KiB 를 넘는다.** argv 그대로 운영(리눅스 파드)에 나가면 `E2BIG` → `OSError` → `ProviderUnavailable` → 시도 3회 → 「실패」 다.

참고:
- 셈 스크립트는 워커 스크래치에만 있다(레포 밖).
- 전사 JSON 의 들여쓰기(`indent=2`)가 바이트의 큰 몫이다. 맥락 목록은 공백 없는 JSON 이다.
- macOS 는 한 인자 상한이 없어 로컬에서는 드러나지 않는다.

### ② CLI 가 stdin 을 받는가 — 확인

| CLI | 버전(이 기계) | 근거 | 결론 |
|---|---|---|---|
| Codex | `codex-cli 0.160.1` | `codex exec --help`: 「[PROMPT] … If not provided as an argument (or if `-` is used), instructions are read from stdin」 · `codex exec resume --help`: 「[PROMPT] … If `-` is used, read from stdin」 | **받는다**(새 세션 · resume 모두) |
| Claude Code | `2.1.284` | `--help` 에는 명시가 없다. 설치 번들(`bin/claude.exe`)의 소스 `getInputPrompt`: `--print` 에서 stdin 이 TTY 가 아니면 파이프 입력을 읽어(상한 10MB, 넘으면 오류) 프롬프트 인자 뒤에 붙인다. 인자가 없으면 stdin 이 곧 프롬프트다 | **받는다** |

운영 이미지의 CLI 버전은 확인하지 않았다(코디 확인 필요). Codex 는 0.153.0 주석이 남아 있는데, `-`/stdin 은 그 이전부터 있던 동작이다.

### ③ stdin 전달로 바꿨다 — argv 에서 프롬프트를 뺐다

| 자리 | 바뀐 것 |
|---|---|
| 러너 `B/platform/cli_process.py` | `subprocess_runner(…, stdin_text=None)` — 있으면 `stdin=PIPE` 로 열고 **따로 도는 쓰기 스레드**가 흘린 뒤 닫는다(stdout 이 먼저 쏟아져도 파이프가 서로 막히지 않는다). 없으면 지금처럼 `/dev/null`. `invoke_runner(…, stdin_text=)` · 새 `invoke_plain_runner`(단발 생성용) — 그 키워드를 모르는 옛 시험 러너는 옛 호출로 내려간다 |
| Codex | 대화(`exec`·`exec resume`) · 단발 생성 모두 프롬프트 자리에 `STDIN_PROMPT = "-"`(`codex_cli.py:94`)를 넣고, 프롬프트는 `stdin_text` 로 넘긴다(`:143`, `:234`) |
| Claude | 대화·단발 생성 모두 argv 에서 프롬프트를 뺐다. 프롬프트는 `stdin_text` 로 넘긴다(`claude_cli.py:111`, `:187`). `--json-schema`(스키마 JSON)는 argv 에 남는다 — 최종 스키마가 수 KB 라 상한과 멀다 |

**시험** `T/contract/test_cli_prompt_stdin.py`(6)
- **실제 자식 프로세스**로 600KB(128KiB 의 4배+) 프롬프트가 stdin 으로 다 닿는다 · 프롬프트가 없으면 빈 stdin — 둘 다 `@pytest.mark.serial`(자식 프로세스 규칙)
- Codex 대화 argv 끝 = `-` · resume 도 · stdin 에 프롬프트 · argv 의 어떤 칸도 128KiB 미만
- Codex 단발 생성도 stdin
- Claude 대화·생성 모두 argv 에 프롬프트 없음 · stdin 에 있음 · `--resume` 유지

기존 `test_codex_cli.py::test_codex_cli_conversation_injects_only_server_bound_scax_mcp_context` 는 `arguments[-1]` 대신 stdin 에서 프롬프트를 읽도록 고쳤다(argv 끝은 `-`).

## 6. 검증 수치

**범위 변경(코디 지시 2026-10-07)** — 전체 시험(`make test`·`make verify`·`make test-contract` 전체)은 돌리지 않는다. 바꾼 파일과 관련된 시험만 지정해서 돌렸다. 처음에 띄운 전체 묶음(contract → postgres → `make test`)은 지시를 받고 **도중에 멈췄다**(결과를 쓰지 않음). 그 직후 실수로 `make test-postgres`(전체)를 한 번 불렀지만, 파이프가 바로 끊겨 즉시 종료됐다(시험이 돌지 않았다 · 남은 프로세스 없음을 확인).

| 명령 | 시험 파일 | 결과 |
|---|---|---|
| `make test-unit`(지시 전 · 한 번) | `tests/unit` + `tests/architecture` | **528 passed** · 0 failed |
| `make test-contract-serial FILES="…"`(지정 파일 · `-n0`) | unit: `test_meeting_finalize_service.py` · `test_meeting_worker_heartbeat.py`(새) · `test_ai_stage_timeouts.py` · `test_meeting_domain.py` · `test_codex_stream_adapter.py` · `test_claude_stream_adapter.py` / `tests/architecture`(계층·인벤토리 drift) / contract: `test_meeting_minutes_enhance.py` · `test_cli_prompt_stdin.py`(새 · serial 2건 포함) · `test_codex_cli.py` · `test_claude_cli.py` · `test_codex_stream_ingest.py` · `test_meeting_memo_batch.py` · `test_meeting_finalize.py` | **253 passed** · 0 failed · 1 deselected |
| `AX_POSTGRES_TEST_URL=… uv run pytest -m integration -n0`(Makefile 에 파일 지정 postgres 타깃이 없어 직접 지정) | `tests/integration/postgres/test_meeting_term_corrections_postgres.py` | **2 passed** · 0 failed |

- 인벤토리 drift 없음(`tests/architecture` 통과 — HTTP·MCP 시그니처 변화 없음)
- 기준선(`be-baseline.md` WP2 — 기존 실패 0)과 겹치는 범위에서 새 실패는 없다
- 전체 회귀는 코디의 마지막 전체 검증 몫이다

## 7. 미결 · 주의점

1. **실물 CLI 로 stdin 을 1회 확인해야 한다(코디 E2E)** — 시험은 대역 러너와 실제 python 자식 프로세스로 했고, 실물 `codex`·`claude` 는 부르지 않았다. 운영 이미지의 CLI 버전이 `-`/파이프 입력을 받는지도 함께 본다
2. heartbeat 연장이 실패해도 도는 합성은 멈추지 않는다(스레드). 그 사이 다른 워커가 같은 회의를 집으면 겹쳐 돌 수 있다 — 바닥 6000초가 그 창을 정상 최악보다 뒤로 미룬다
3. 웜스타트가 락을 쥐는 동안(최대 웜스타트 상한 × 2 = 480초) 그 회의의 배치·최종 합성은 기다린다. 회의를 시작하자마자 종료하면 최종이 웜스타트를 기다린다(옛 경주보다 안전한 쪽을 골랐다)
4. 맥락 목록의 운영 실제 크기는 여전히 가정이다 — `AI 맥락 목록: … n자` 로그로 실측한다(I-6). stdin 으로 바뀌어 argv 한도는 사라졌지만, Claude 는 파이프 입력 10MB 상한이 있다
5. 리뷰 H-3(「정리 중」 최대 1시간 이상)은 그대로다 — 최악 = 재전사 + 최종 × 5
