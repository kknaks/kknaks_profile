# 리뷰 리포트 — tongky-quality-re1 / code 재검수 r2 · WP30 · WP31 세 참여자 (2026-11-16)

- 대상: 워크트리 `interpret-pwa/tongky-quality-re1`. HEAD `fe375ad` 에 미커밋 변경이 얹혀 있다. 앞 리포트 뒤로 back 만 바뀌었다: `session.py` · `turn.py` · `tests/test_turn.py` · `tests/test_interpret.py` · `tests/test_records.py`. front 는 앞 리포트 때와 같다.
- 대조 기준: SPEC-001 0.9.5 §5.3 · §5.13 C ~ J · §7.4 · §9.1 「세 참여자」 · DEC D-68 ~ D-70(④ 처분) · 앞 리포트 `review-wp30-31-code-report.md` 와 코디 처분(FAIL-1 · WARN-1 ~ 4)
- 수정 0 · 커밋 0 · Soniox 실물 호출 0. 만든 파일은 이 리포트 1개다. 앞 리포트의 프로브는 레포 밖 스크래치에 있다. 거기에 `playback_stopped` 경우를 더해 다시 돌렸다.

## 판정: PASS

FAIL 0 · WARN 0 · 참고 3. 앞 리포트의 FAIL-1 과 WARN-1 ~ 4 는 모두 닫혔다. 수정이 새로 연 구멍(새 잠금 · 「스트림을 안 만드는」 길 · 차례별 로그)은 찾지 못했다.

### 검증(각 1회)

| 명령 | 결과 |
|---|---|
| back `uv run pytest -q` | **525 passed**(앞 518 + 처분 시험 7) · 1 warning(starlette `httpx` 폐기 예고 — 무관 · 기존) · **26.1 s**(앞 52.1 s) |
| back `uv run ruff check .` | All checks passed |
| front `npx tsc --noEmit` · `npm run lint` | 0 · 0 |
| front `npx vitest run` | 10 files · **43 passed** |
| 프로브(스크래치 · 레포 밖) | 끼어들기 · `playback_stopped` 두 경우 모두 다음 차례 밀림 0. 아래 FAIL-1 |

## 앞 지적 — 닫힘 판정

| 앞 지적 | 처분 | 판정 | 자리 · 근거 |
|---|---|---|---|
| **FAIL-1** 멈춘 뒤 `play_end` 가 남음 | 멈추면 재생 어림을 멈춘 때로 되돌린다 | **닫힘** | `turn.py:326-332` `Playback.cut()` — `play_end = min(play_end, 지금)` · `items` 비움. `session.py:541` 멈춤 절차가 `cut()` 을 부른다. 순서는 ④ agent text 끝(`:535`, 재생 위치까지 보냄) → ⑤ 구간 닫음(`:536`) → `cut()` 이라 끝내기 전에 글자를 잃지 않는다. 프로브: 4 s 번역을 0.5 s 에 끊고 T+1.5 s 에 다음 차례를 열었다. 끼어들기 `play_start = 1.5` · `playback_stopped` `play_start = 1.5`(앞에서는 4.0). 구간도 그 틱에 열렸다. 시험 `test_next_turn_not_delayed_after_stop[barge·playback_stopped]`(`tests/test_turn.py:766-797`)이 재생 시작 · 구간 시작(= 그 틱 `sent_ms`) · 첫 `agent_text` ≤ 재생 시작 + 0.7 s · 제 길이로 끝남을 본다. §5.13 D 「같은 셈」 · E · G |
| **WARN-1** 기존 세션 시험이 실제 1초를 기다림 | 가짜 시계 | **닫힘** | `test_interpret.py:32-37` autouse 픽스처가 `turn_mod.TURN_END_SEC` 를 0.01 로 줄인다. `test_records.py` 도 같은 픽스처를 import 한다. `test_correct` · `test_quality` 는 `fast_clock`. 이제 가장 오래 걸리는 시험 다섯은 `test_turn` · `test_correct` · `test_quality` 의 것이고, 1 s 짜리는 0이다. 기대값은 그대로다. 참고 1 |
| **WARN-2** `audio_start` 를 보내는 순간에 멈춤이 겹침 | id · 스트림 | **닫힘** | `session.py:439-442` 는 `_turn_ids` · `_last_start` · `_open_audio` 를 `audio_start` 를 보낸 직후, 같은 잠금 안에서 정한다. `:520-528` 멈춤 절차는 id 를 잠금 안에서 읽고, `audio_stop` · `audio_end` 도 잠금 안에서 보낸다. `:567-568` 은 `audio_start` 를 보낸 뒤 멈췄으면 그 발화의 TTS 스트림을 만들지 않는다. 시험 `test_stop_while_audio_start_in_flight[barge·playback_stopped]`(`:800-833`): 끼어들기면 `audio_stop{u2}`, `playback_stopped` 면 `audio_end{u2}` · u2 스트림 0, 둘 다 그 뒤 PCM · `audio_end` 0. `test_barge_cancels_new_stream_in_progress`(`:836-849`): 진행 중 스트림에 `cancel` 1. §5.3 「`id` = 마지막으로 `audio_start` 를 보낸 발화」 · §5.13 F ③ · H |
| **WARN-3** id 가 문자열이 아니면 세션이 끊김 | 무시 | **닫힘** | `session.py:346-350` — `str` 이 아니면 정보 로그 1줄(`id_type=` 종류 이름만 — 값 0 · §5.13 J)을 남기고 무시한다. 시험 `test_playback_stopped_bad_id_ignored`(`:852-868`): list · dict · int · None 넷 → 세션 유지 · `error` 0 · `relay error` 0 · 그 뒤 맞는 id 로 멈춘다. §5.13 H 「없는 `id` 면 아무것도 하지 않는다(`bad_request` 아님)」 |
| **WARN-4** 되울림 로그 몫 | 차례 몫 + 세션 끝 한 줄 | **닫힘** | `turn.py:60-69` · `:79-82` — 구간에 그 구간을 연 차례 번호(`turn`)를 적는다. `TokenGate` 는 그 토큰을 덮은 구간의 차례별로 센다(`stats` · `take_stats(turn)`). `session.py:502-505` 차례 끝에는 그 차례 몫만 쓴다. `:507-511` · `:673` 세션 정리 때는 나머지(차례 끝 뒤에 늦게 버린 몫)를 한 줄로 쓰고, 차례가 한 번도 없었으면 쓰지 않는다. 시험 `test_echo_log_per_turn_and_rest_at_session_end`(`:871-885`): 「1 · 1」 다음 「2 · 1」. §5.13 J ⓓ |

## 수정이 새 구멍을 만들었나 (볼 것 0)

| 자리 | 판정 · 근거 |
|---|---|
| 새 잠금 — `_stop_playback` 이 `_send_lock` 을 잡고 `client.send_json` 을 직접 부름(`session.py:520-528`) | **PASS** — 잠금 안에서는 `_send` · `_send_play` 를 다시 부르지 않는다(재진입 없음). `_consume` 은 조각마다 잠금을 잡았다 놓는다(`:588-593`). 그래서 멈춤 절차는 많아야 조각 하나만 기다린다. `audio_stop` 은 그 조각 뒤 · `cancel` 앞에 나가므로 ① 의 순서가 지켜진다. 닫힌 연결이면 아무것도 보내지 않는다(`:522-523`) |
| 「스트림 안 만듦」 길(`session.py:567-568`) | **PASS** — `_stream_task` 는 앞 발화의 `finally`(`:580`)에서 이미 None 이라 `cancel` 대상이 없다. `finally` 가 `_streaming` · `speaking` 을 되돌린다. 플레이어는 `_ok(gen)` 이 거짓이라 바깥 반복에서 빠진다(`:553`). front 쪽: 끼어들기면 `audio_start{u2}` → `audio_stop{u2}` → 버림 · 출력 구간 닫힘. `playback_stopped` 면 `audio_start{u2}`(버림 해제 · 출력 중) → `audio_end{u2}` → 재생 조각 0 · 400 ms 뒤 닫힘(`front/lib/outputWindow.ts:24-27` · `:49-57`). 「출력 중」 이 소리 없이 붙어 남지 않는다(§5.13 H 감수 문장과 같다) |
| `cut()` 과 남아 있는 옛 스트림 | **PASS** — `cancel` 을 기다리는 옛 `_consume` 은 `_ok(gen)` 이 거짓이라 `Playback.audio()` 를 부르지 않는다(`:589-590`). 그래서 `cut()` 뒤의 `play_end` 를 다시 밀지 않는다. 옛 `stream_done(sp)` 는 이미 `items` 밖의 객체다 |
| 차례별 로그 사전 | **PASS** — 지난 차례 몫은 세션 끝까지 남았다가 한 줄로 나간다. 크기는 차례 수만큼이고 수만 담는다 |

## back ↔ front 계약 · §5.13 · 조용히 통과하는 자리 (볼 것 1 ~ 3 — 바뀐 곳 위주)

- 계약(§5.3 `audio_stop{type,id}` · `playback_stopped{type,id}` · 보내는 때 · id · `audio_end` · 버림 · `outputting`): front 는 바뀌지 않았다. back 은 id 를 정하는 때만 앞당겼다(잠금 안). 앞 리포트의 대조표가 그대로 맞다 — **PASS.** 겹치는 창에서 나가는 id 가 이제 「방금 `audio_start` 를 보낸 발화」 다. 문서 문구와 더 잘 맞는다.
- §5.13: 차례 끝 시계(`turn.py:275-281` — 상수는 1.0 그대로) · 되울림 구간 · 끼어들기 2 · 멈춤 절차 순서 ① ~ ⑦ · agent text 시점 · `end_of_segment` 는 앞 리포트 판정 그대로다. 재생 어림(D)은 FAIL-1 이 닫히면서 맞아졌다 — **PASS.**
- 조용히 통과하는 자리(언어 바꿈 · `stop` · 끊김 · 오류의 태스크 · 스트림 정리 · 누르고 말하기 · `pause`/`resume` · 빈 원문 · 바로잡기 · 기록): 바뀐 곳은 `_cleanup` 앞머리의 로그 한 줄(`:673`)뿐이다. 그 뒤 기록 · 연결 닫기 순서는 그대로다 — **PASS.** 시험은 전부 초록이다(`test_records` · `test_correct` · `test_interpret` 포함).

## 미결 대조 (볼 것 4)

- ① 멈춤 중 차례 끝에 글 없는 `end_of_segment`: 이미 연 segment 만 닫고, 한 번도 안 보냈으면 보내지 않는다(`session.py` `_agent_finish`). 코드는 바뀌지 않았다. 앞 판정 그대로 **PASS**(§5.13 G 「정상 끝」 · 「멈춤 중」).
- ⑤ 시험이 실제 1초를 기다림: **닫힘**(위 WARN-1).

## 고객이 실물에서 만날 자리

- 앞 리포트의 FAIL-1 자리(멈춘 뒤 통키가 자기 목소리를 통역함 · 대답 첫머리가 사라짐)는 **닫혔다.**
- 남은 것은 모두 문서가 감수로 적은 자리이고, 실기기(§9.6 · ㉘)에서 본다: 끼어든 뒤 멈추기까지 1.3 ~ 1.9 s + 전달 · 말 끝 → 음성 약 2 s + TTS · 같은 언어로 끼어든 말은 사라짐 · 재생 직후 0.5 s 안의 같은 언어 대답 첫머리(자동 듣기) · 누른 채 음성 중에 떼면 끊김 · 새 front + 옛 back 이면 오류 화면 · 좁은 창의 다음 발화 재생.
- 새로 보이는 것: **`playback_stopped` 와 그 창이 겹치면 그 발화가 소리 없이 「출력 중」 으로 약 0.4 s 보였다가 닫힌다.** `audio_start` 뒤 조각 0 · `audio_end` 로 바로 닫히기 때문이다. 문서가 감수한 「다음 발화가 재생될 수 있다」 보다 짧고 조용한 쪽이다.

## 참고(낮음)

1. WARN-1 은 「가짜 시계를 1초 넘김」 이 아니라 **시험 안에서 `TURN_END_SEC` 상수를 0.01 로 덮어써서** 닫았다(`test_interpret.py:32-37` — TestClient 경로는 세션에 시계를 넘길 자리가 없다는 이유가 주석에 있다). 기대값은 그대로다. 1초 자체는 `test_turn` ② 「0.99 = 아님 · 1.0 = 참」 과 ⑦ 이 가짜 시계로 본다. 상수 값 · 자리는 ⑥ 이 본다(덮어쓰기는 그 시험 모듈 안에서만 쓰인다). §9.1 문구(「가짜 시계를 1초 넘기거나 `pause`」)와 글자로는 다르다. 고칠지는 코디 판단이다 — 바꾸려면 SPEC 에 「상수를 줄여도 된다」 를 한 줄 넣는 쪽이 싸다.
2. 앞 리포트 참고 1(`turn.py` `_barge_nf_none` 이 안 쓰이는 필드) · 참고 2(`test_context.py` · `test_interpret.py` 가짜 메서드의 빈 줄 모양)는 그대로 남아 있다 — 무해하다.
3. 무관 · 기존: pytest 경고 1개(starlette `httpx` 폐기 예고).

- allowed_paths 이탈 0 — 이 리포트 파일만 만들었다. 레포 · SPEC · DEC 는 읽기만 했다.
