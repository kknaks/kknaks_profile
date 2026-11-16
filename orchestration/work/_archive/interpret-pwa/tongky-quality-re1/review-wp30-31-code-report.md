# 리뷰 리포트 — tongky-quality-re1 / code WP30 · WP31 세 참여자 (2026-11-16)

- 대상: 워크트리 `interpret-pwa/tongky-quality-re1` — HEAD `fe375ad` + 미커밋 변경(back `turn.py`(새) · `session.py` · `soniox.py` · `assembler.py` · `scripts/live_check.py` · 시험 5 / front `outputWindow.ts`(새) · `halfDuplex.ts`(삭제) · `interpret.ts` · `output.ts` · `ptt.ts` · `view.ts` · 시험 5)
- 대조 기준: SPEC-001 0.9.5 §5.3 · §5.10 · §5.13 A ~ J · §7.3 · §7.4 · §9.1 「세 참여자」 ① ~ ㉔ · §9.2 · DEC D-68 · D-69 · D-70(④ 리뷰 · 재검수 처분) · `review-spec-095-r2-report.md`(문서 단계 위험 자리)
- 줄 번호: 레포 기준 상대 경로 · 미커밋 작업 트리 그대로
- 수정 0 · 커밋 0 · Soniox 실물 호출 0. 이 리포트 1개만 썼다. 프로브 시험 1개는 레포 밖 스크래치에서 레포의 시험 하니스(`tests/test_turn.py` `H`)를 import 해 돌렸다(레포 파일 변경 없음).

## 판정: FAIL

FAIL 1 · WARN 4 · 참고 5. 계약(메시지 이름 · 키 · 방향 · 순서 · `audio_end` 처리 · 버림 · 출력 구간)은 back과 front가 서로 맞는다. 다만 **끼어들기나 `playback_stopped` 로 멈춘 뒤, back의 재생 어림(`Playback.play_end`)이 멈춘 발화의 원래 끝 시각에 그대로 남는다.** 그래서 다음 통키 차례의 재생 시작 · 되울림 구간 · agent text · 차례 끝이 모두 늦게 잡힌다(재현함 — FAIL-1). 시험 518개 · front 43개는 모두 초록이지만, 이 경우를 보는 시험은 없다.

### 검증(각 1회)

| 명령 | 결과 |
|---|---|
| back `uv run pytest -q` | **518 passed** · 1 warning(starlette `httpx` 폐기 예고 — 무관 · 기존) · 52.1 s |
| back `uv run ruff check .` | All checks passed |
| front `npx tsc --noEmit` | 0 오류 |
| front `npm run lint` | 0 오류 |
| front `npx vitest run` | **10 files · 43 passed** |
| 프로브(스크래치 · 레포 밖) | FAIL-1 재현 — 아래 |

### 볼 것 결과 요약

| # | 볼 것 | 판정 |
|---|---|---|
| 1 | back ↔ front 계약 | **PASS** — 아래 표. 좁은 창 하나는 WARN-2 |
| 2 | §5.13 규칙이 코드에 그대로인가 | **FAIL**(재생 어림 · FAIL-1) · 나머지 PASS |
| 3 | 조용히 통과하는 자리 | FAIL-1이 그 자리다(시험 초록 · 계약 깨짐). WARN-3 · WARN-4 |
| 4 | backend 미결 ① · ⑤ | ① **PASS**(SPEC과 맞음) · ⑤ **WARN-1**(SPEC 문구와 다름 · 결과는 같음) |
| 5 | 검증 명령 | 전부 통과(위 표) |

## FAIL

### FAIL-1 멈춘 뒤 `play_end` 가 리셋되지 않는다 — 다음 차례의 재생 어림이 멈춘 발화의 남은 길이만큼 밀린다

- 자리: `back/app/service/interpret/turn.py:309-310`(`Playback.reset()` 이 `items` 만 비우고 `play_end` 는 둔다) · `turn.py:320`(`start = max(self.clock(), self.play_end)`) · `back/app/service/interpret/session.py:524`(`_stop_playback` 이 `self._play.reset()` 만 부른다). 비교: front는 멈출 때 `nextTime = 0`(`front/lib/interpret.ts:267`).
- 근거: §5.13 D 「back 은 **같은 셈**을 서버 시계로 따라 한다 — `시작 = max(지금, 재생 끝 예정)`」. front는 `audio_stop` · `playback_stopped` 때 재생 큐를 비우고 이어 붙이기 기준을 0으로 돌린다(§7.4). back이 「재생 끝 예정」을 그대로 두면 더 이상 같은 셈이 아니다. 여기에 걸려 E(재생 구간 `시작` = 재생이 시작된 틱의 `sent_ms`) · G(「Follow the playback」) · D(통키 차례 끝 = `지금 ≥ 재생 끝 예정`)가 함께 틀어진다. D-68 ③ · D-69 · D-70 ②.
- 재현(프로브 · 가짜 시계): 손님(zh) 말 → 한국어 번역 4.0 s. 스트림은 다 받음(TTS가 실시간보다 빠름 — §5.13 F의 「보통」 경우). T+0.5 s에 반대 언어 토큰 2개 → `audio_stop` → 끼어든 말 확정 → T+1.5 s에 새 통키 차례.
  ```
  play_end after barge-in (rel T): 4.0  before: 4.0
  new turn: now(rel T)= 1.5  play_start(rel T)= 4.0  window= None
  ```
  front는 T+1.5 s에 바로 재생하는데, back은 그 발화가 **T+4.0 s에 시작한다고 본다**(2.5 s 밀림 = 멈춘 발화의 남은 길이).
- 고객이 실물에서 만나는 결과(자동 듣기 · 마이크 열림):
  1. **통키가 자기 목소리를 통역한다.** 밀린 동안 재생 구간이 열리지 않는다(`session.py:455` 은 `now >= sp.play_start` 일 때 연다). agent text도 나가지 않는다(`turn.py:353` — 재생 위치가 음수). 그래서 새 재생의 첫 2.5 s 되울림이 E · G 둘 다를 빠져나간다. 그 토큰은 `start_ms < base_ms` 라 끼어들기로 세지도 않는다(`turn.py:242`). 결국 남긴 토큰으로 조립돼 자막이 되고, 읽을 큐에 들어가 다음 차례에 통역된다(D-68 ③ 위반).
  2. **재생이 끝난 뒤 대답의 첫머리가 사라진다.** 구간이 실제 재생 끝보다 2.5 s + 여유 500 늦게 닫힌다. 그동안 재생 언어로 한 진짜 대답(직원의 한국어 · 손님의 중국어)이 되울림으로 버려진다.
  3. 그동안 back은 통키 차례로 남는다. 반대 언어 말 2토큰이면 front가 이미 다 재생한 뒤에도 `audio_stop` 이 나가고, 다음 차례 끝 시계도 늦어진다.
  - 누르고 말하기(`playback_stopped` → `resume` · 뗌 → `pause` → 바로 차례 끝, §5.13 I)에서도 똑같이 밀린다. 멈춤 중에는 구간 여유가 0이라 1번은 약하다. 하지만 `resume` 뒤에도 구간이 열려 있어 2번은 그대로 남는다.
- 왜 시험이 초록인가: ⑨ⓐ ~ ⓒ · ⑯ · ㉔는 멈춘 차례까지만 본다. ⑨ⓒ 「그 뒤 끼어든 사람의 발화는 다음 차례 끝에 정상 재생」은 `audio_start` 가 나가는지만 본다. **다음 차례의 `play_start` · 재생 구간 시작 · agent text 시각**은 어느 시험도 보지 않는다.
- 닫는 길(정하는 것은 코디 → backend): 멈춤 절차(F · H)에서 `play_end` 를 「지금」으로 되돌린다. 예: `Playback.reset()` 에서 `self.play_end = min(self.play_end, self.clock())` 로 하거나, `_stop_playback` 에서만 따로 한다. 시험 한 줄도 더한다: 「끼어들기 뒤 다음 차례의 첫 발화 `play_start` = 그 차례 첫 조각을 보낸 때 · 재생 구간 시작 = 그 틱의 `sent_ms` · 첫 `agent_text` ≤ 재생 시작 + 0.7초」. `playback_stopped` 쪽도 같이 본다.

## WARN

### WARN-1 (미결 ⑤) 기존 세션 시험 일부가 실제 1초를 기다린다 — SPEC §9.1은 「가짜 시계」

- 자리: `back/tests/test_interpret.py` · `back/tests/test_records.py` 의 세션 시험은 `InterpretSession(clock=…)` 을 넘기지 않아 기본 `time.monotonic`(`session.py:103`)을 쓴다. 그래서 차례 끝 1초를 실제로 기다린다. `--durations`: `test_interpret.py::test_full_flow` 1.12 s · `test_records.py::test_session_lines_shape` 1.10 s · `test_keep_days_invalid_warns_and_keeps[…]` 1.09 ~ 1.11 s 등. `test_correct.py` · `test_quality.py` 는 `fast_clock()`(20배 · `test_quality.py:200-203`)을 쓴다. `test_turn.py` 만 순수 가짜 시계다.
- 근거: §9.1 「세 참여자」 끝 문장 「기존 시험 가운데 「확정 즉시 `audio_start`」 를 전제한 것은 **가짜 시계를 1초 넘기거나 `pause` 를 보내** 차례 끝을 만든 뒤 보도록 고친다 — 기대값은 그대로다」.
- 판단: 기대값(자막 · TTS 입력 · 기록)은 그대로 지켜진다. 계약 위반이 아니라 시험 방식이 SPEC 문구와 다른 것이다. 걸리는 것은 둘이다. 전체 시간이 52 s로 늘었다. 그리고 실제 시간에 묶인 시험은 느린 CI에서 기다림 한도(각 시험 하니스의 타임아웃)에 걸릴 수 있다. backend가 보고한 「시험이 실제 1초를 기다림」은 SPEC과 **다르다** — 고치거나, SPEC 문구에 「실제 1초 대기도 허용」을 적어 맞춘다(코디 판단).

### WARN-2 끼어들기가 `audio_start` 를 보내는 순간과 겹치면 `audio_stop` 의 `id` 가 앞 발화이고, 새 스트림에 `cancel` 이 나가지 않는다

- 자리: `session.py:506`(`playing = self._last_start` 를 잠금 밖에서 읽는다) ↔ `session.py:548-551`(`_send_play(audio_start)` 가 잠금을 쥐고 보낸 **뒤에** `_last_start` · `_turn_ids` · `_stream_task` 를 정한다) · `session.py:512-517`(`_stream_task` 가 아직 없으면 `cancel` 하지 않는다).
- 경우: 플레이어가 `audio_start{u4}` 를 보내는 `await` 사이에 STT 쪽에서 `k ≥ 2` 가 된다 → `_cut=True` · `playing=u3` → `audio_stop{u3}` 이 `audio_start{u4}` 뒤에 나간다. 그다음 u4 스트림이 만들어지지만 `_cancel_at` 이 없어 끝까지 생성된다(PCM은 `_ok` 로 막혀 나가지 않는다). `_play.begin` 은 `reset()` 뒤에 붙는다(다음 `_start_turn` 이 지운다).
- 근거: §5.3 `audio_stop` 「`id` = 마지막으로 `audio_start` 를 보낸 발화」 · §5.13 F ③ 「진행 중인 스트림은 취소」.
- 영향: front는 `audio_stop` 의 `id` 를 보지 않고 멈춘다(`front/lib/interpret.ts:187-191`). 그래서 **화면 · 소리는 맞다** — 버림이 서고, u4의 `audio_end` 는 오지 않으며, 출력 구간은 닫힌다. 남는 것은 TTS 한 스트림을 쓸데없이 끝까지 만드는 것뿐이다. 창이 `send_json` 한 번만큼 좁아 WARN으로 둔다. 닫는 길: `_last_start` · `_open_audio` 를 `_send_play` 잠금 안(보내기 직후)에서 정한다. 또는 `_play_one` 이 `audio_start` 를 보낸 뒤 `_cut` 을 다시 보고 바로 끝낸다.

### WARN-3 `playback_stopped` 의 `id` 가 해시할 수 없는 값(배열 · 객체)이면 세션이 끊긴다

- 자리: `session.py:346` — `msg.get("id") in self._turn_ids` 에서 `id` 가 리스트 · 딕셔너리면 `TypeError` 가 난다. 그러면 `_client_reader` 태스크가 끝나고, `_pump` 가 `interpret relay error` → `error soniox_unavailable`(「통역 연결이 끊겼어요」)로 세션을 닫는다. 확인: `[1] in set()` → `TypeError: cannot use 'list' as a set element`.
- 근거: §5.3 · §5.13 H 「그 가운데 없는 `id` 면 back 은 무시한다(`bad_request` 아님)」 · §5.4(알 수 없는 프레임은 끊지 않는다).
- 영향: 우리 front는 늘 문자열을 보내므로(`String(m.id)` · `front/lib/interpret.ts:182`) 실물에서는 나지 않는다. 손으로 만든 클라이언트만 걸린다. 닫는 길: `isinstance(msg.get("id"), str)` 를 먼저 본다.

### WARN-4 되울림 로그 ⓓ가 차례가 끝날 때만 나간다 — 마지막 차례 뒤에 버린 토큰은 로그에 남지 않는다

- 자리: `session.py:495-497`(`_log_turn_end` — `_end_turn` · `_stop_playback` 에서만 부른다) · `turn.py:191-194`(`take_stats`).
- 경우: 재생이 끝난 뒤 30 s 보관 동안 늦게 확정된 되울림 토큰이 버려진다(E 「언제 도착했든」). 이 수는 **다음** 통키 차례의 로그 줄에 섞이고, 다음 차례가 없으면(세션이 끝나면) 어디에도 남지 않는다. `_cleanup` 에서 내보내지 않는다.
- 근거: §5.13 J ⓓ 「통키 차례가 끝날 때 그 차례 몫을 한 줄로」 · 「§9.6 의 수치는 이 로그로 센다」 — 실기기에서 되울림 수(OQ-035)를 셀 때 과소 · 다른 차례에 붙음.
- 판단: 계약 문구(「끝날 때 한 줄」)는 지켰다. 하지만 「그 차례 몫」이 정확하지 않아 §9.6 수치가 틀어질 수 있다. 닫는 길: 정리(`_cleanup`) 때 남은 몫을 한 줄 더 쓰거나, 문서에 「늦게 버린 것은 다음 줄에 섞인다」를 적는다.

## back ↔ front 계약 대조 (볼 것 1)

| 항목 | back | front | 판정 |
|---|---|---|---|
| `audio_stop{type,id}` 이름 · 키 | `session.py:508` `{"type":"audio_stop","id":playing}` | `interpret.ts:187` `case 'audio_stop'` | PASS |
| `audio_stop` 보내는 때 · 순서 | `_cut=True` 뒤 ① 먼저(`session.py:504-508`) → `cancel`(진행 중만 · `:512-517`) → agent 끝(`:518`) → 구간 닫음(`:519`, 끝 = 절차 시작 때 `sent_ms` · `:502`) → 상태(`:521`) → 로그(`:525-528`) | — | PASS(§5.13 F ① ~ ⑦) |
| `audio_stop` 뒤 PCM · `audio_end` 0 | `_ok(gen)` 가 `_cut` 을 본다(`:422-424`) · `_consume` 은 잠금 안에서 다시 본다(`:571-573`) · `_open_audio=None`(`:511`) | 받으면 `stopPlayback()` — 큐 버림 · 버림 표시 · 출력 구간 즉시 닫힘(`output.ts` `clear` → `gate.reset()`) · back으로 보내는 것 0 | PASS |
| `playback_stopped{type,id}` 이름 · 키 | `session.py:344` | `interpret.ts:251-254` `{type:'playback_stopped', id:lastAudioId}` | PASS |
| `playback_stopped` 보내는 때 | — | 출력 구간이 참일 때만 · `pause()`(원 누름 · 뗌 · 모드 바꿈) · `clearPlayback()`(누름 · 초기화) · `pause` · `resume` 보다 먼저(`interpret.ts:291-292` · `ptt.ts` `pressDown`) · `close()` · `fail()` · `audio_stop` 은 `stopPlayback()` 직접 호출이라 보내지 않음 | PASS(§7.4 · §5.13 H) |
| `id` 맞춤 | 이 차례에서 `audio_start` 를 보낸 id 집합(`_turn_ids` · `:134` · `:475` · `:550`) · 지난 차례 · 차례 아님 → 무시 · `bad_request` 아님 | `lastAudioId` = 마지막 `audio_start` id(`interpret.ts:182`) | PASS(D-70 ④ 재검수 · 시험 ⑯ 두 경우) — 값 모양은 WARN-3 |
| `playback_stopped` 뒤 `audio_end` | 보내던 발화가 있으면 `audio_end{그 id}` 1번(`:509-510`) · PCM 끊음 · 다 보낸 뒤면 0 | 버리는 중이면 무시(`output.ts` `audioEnd`) · 창에서 다음 발화 재생 중이면 출력 구간이 닫힘 | PASS(§5.13 H · r2 WARN-1 닫힘) |
| 버림 표시 | — | `clear()` → `discarding=true` · 다음 `audio_start` 에 풀림 · 버리는 동안 `audio_end` · 조각이 타이머를 건드리지 않음 | PASS(§7.4 FAIL-1 길) |
| 원 표시 `outputting` | — | `OutputWindow` — `audio_start` 에 참 · `audio_end` + 재생 끝 + 400 ms 에 거짓 · `reset()` 은 즉시. 표시 · 누름 판정 · `playback_stopped` 판정에만 씀. **PCM 송신 조건은 `ready ∧ ¬paused ∧ ¬closed ∧ WS OPEN`**(`interpret.ts:245-247`) | PASS(§7.3 0.9.5 ⓐ ~ ⓒ · §7.4 · §5.13 I) |
| 새 화면 문구 | — | 0(`FOREIGN_PHRASES` 키 수 시험 ⓓ) | PASS |
| 옛 front 호환 | `playback_stopped` 를 아는 back이 먼저 떠야 함(§5.3) — back은 처리함 | 옛 front는 `audio_stop` 을 무시(`default` 없음) | PASS(문서대로) |

## §5.13 규칙 대조 (볼 것 2)

| 규칙 | 자리 | 판정 |
|---|---|---|
| 차례 끝 시계 1초 · back 시계 · 응답에 묶지 않음 | `turn.py:261-267` · `session.py:443-450`(50 ms 틱) | PASS |
| 새 말 = 남긴 원문 글이 바뀌고 앞부분으로 줄기만 한 것이 아님 · 시각만 바뀐 것 · 비확정 → 확정 · 사라짐 제외 · 번역 · 끝 · `language` 없는 토큰 제외 | `turn.py:222-232` · `_counted` `:52-54` | PASS(시험 ①) |
| 재생 언어 토큰은 차례 끝 시계에서 빠짐 | 버린 토큰은 `kept` 에 들지 않음(`session.py:367-377`) | PASS(시험 ⑩) |
| 열린 발화를 기다림 · `finalize` 로 앞당기지 않음 · 멈춤 중이면 1초 안 기다림 | `turn.py:263-266` · `session.py:336-341` | PASS(②⑰) |
| 반대쪽이 차례 중에 말함 → 시계 다시 · 확정 순서대로 이어 읽음 | `Turn.queue` 하나 · 새 말이면 `last_new` 갱신 | PASS(③) |
| 통키 차례 중 확정된 짧은 말 → 같은 차례 끝에 붙음 | `_emit` → `turn.push` · `_wake` (`session.py:396-398`) · 플레이어가 같은 `gen` 으로 이어 읽음 | PASS |
| 재생 구간: 끝은 여유 없는 값 · 여유 500 한 번 · 멈춤 중 끝/멈춤 → 여유 0 · `pause` 때 여유 잘림 · 보관 30 s 서버 시계 | `turn.py:60-114`(`covers` · `close` · `on_pause` · `prune`) · `session.py:339` | PASS(④㉑㉒㉓) — 단 구간 **시작 시각**이 FAIL-1로 밀릴 수 있다 |
| 되울림 판정 `시작 ≤ start_ms < 끝 + 여유` · 도착 시각 무관 · `start_ms` 없으면 도착 때 | `turn.py:97-110` | PASS |
| 남긴 원문 0인 발화 통째로 버림 · 번역 토큰 원문 쪽 판정 · 섞이면 둠 | `turn.py:145-189` · `assembler.py` `drop_open` · `session.py:369-374` | PASS(⑪ · 이미 보인 말풍선은 둘 다 빈 final로 지움 — §5.11 모양) |
| 끼어들기 `k ≥ 2` · `start_ms ≥ 첫 재생 구간 시작` · 비확정 포함 · 시간 문턱 없음 | `turn.py:234-248` · `session.py:377-379` | PASS(⑤⑨) — `start_ms` 없는 토큰은 「처음 나타났으면」 대신 「나올 때마다」 센다(`_barge_nf_none` 은 만들기만 하고 안 씀 · 참고 1) |
| 멈춤 절차 순서 · 진행 중만 `cancel` · 기다림이 다른 처리를 막지 않음 · TTS 연결 안 닫음 · 3 s 한도 경고 1줄 | `session.py:499-528` · `_wait_stream` `:578-588`(플레이어 태스크가 기다림 · 리더는 막히지 않음) | PASS(⑨ⓐⓑⓒ · ㉔) |
| agent text: v6만 · 키 `enable_agent_text_input` · TTS 글자 시각 · 없으면 고르게 나눔 · 재생 위치 기준 0.7 s 앞 · 다음 발화도 · 보낸 오디오 넘지 않음 · 쪽이 바뀌면 끊고 새로 · 정상 끝 / 끼어들기 `end_of_segment` · 멈춤 중 안 보냄 · 한 번도 안 보냈으면 `end_of_segment` 없음 | `soniox.py:71-72` · `:91` · `:201-205` · `turn.py:331-362` · `session.py:592-622` | PASS(⑫ ~ ⑮ · ⑰) — 발화 경계 시각은 FAIL-1의 경우에 함께 밀린다 |
| 로그 다섯 종 · 수 · 길이 · 시각만 | `session.py:470` · `:497` · `:526` · `:528` · `:622` | PASS(⑲) — 몫 귀속은 WARN-4 |
| 상수 한 곳 · env 아님 | `turn.py:19-25`(여섯 + `ECHO_KEEP_SEC` 30) · `config.py` · `.env.example` 에 0(시험 ⑥) | PASS |
| 기록 그대로(`caption` 만) | `_emit` 의 `record.caption` 그대로 · `drop_open` 의 빈 final은 `_send` 직접이라 기록 0 | PASS(⑳) |

## 조용히 통과하는 자리 (볼 것 3)

| 자리 | 판정 · 근거 |
|---|---|
| **멈춘 뒤 다음 차례** | **FAIL-1** — 시험 초록 · 계약(§5.13 D 「같은 셈」) 깨짐 |
| 언어 바꿈 · `stop` | front `close()` → `stop` 먼저 · `stopPlayback()`(`playback_stopped` 0). back `stop` → `turn.clear()` · `stopping` 이면 틱이 차례를 안 열고(`:448`) · `_emit` 이 큐에 안 넣고(`:396`) · 플레이어 멈춤(`:536`) | PASS(⑱) |
| 연결 끊김 · 오류 | `_pump` finally가 리더 · STT · 플레이어 · 틱 · keepalive · **진행 중 스트림 태스크**까지 취소(`session.py:310-315`) → `_cleanup` 이 두 연결을 닫음 · front `fail()` → `stopPlayback()` · `playback_stopped` 0 | PASS |
| 타이머 · 태스크 | 틱 태스크는 `_pump` 하나 · front 출력 구간 타이머는 `reset()` 에서 지움 · 표시 전환 타이머는 `cancelSwitches` | PASS |
| TTS 스트림 정리 | 멈춘 차례의 스트림은 `terminated` 까지 읽어 버림(`_consume` `:572-573`) · 3 s 한도 뒤 태스크 취소 · 늦은 메시지는 다음 `speak` 의 「다른 `stream_id`」 로 버림(`soniox.py:193-199`) | PASS — 좁은 창은 WARN-2 |
| 누르고 말하기 | 누름: 출력 중이면 `clearPlayback` → `playback_stopped` → `resume` · 뗌: `pause()` 가 출력 중이면 `playback_stopped` → `pause` · 누르는 동안 송신 막지 않음 | PASS(§7.4 · §5.13 I · ㉑㉒㉔) |
| `pause` / `resume` | back `pause` 는 `on_pause` → `finalize` · `resume` 은 플래그만 · 멈춤 중 PCM은 `sent_ms` 에 안 셈(`:324-326`) · agent text 멈춤 중 0 | PASS |
| 빈 원문 막기 | `_blank_filter` 그대로 · 막은 발화는 읽을 큐에 안 넣음(`:393-395` · §5.11 「자리」 0.9.5 문장) | PASS |
| 바로잡기 | 조립기 안 그대로 → 확정 `Utterance.text` 가 고친 글 → 읽을 큐 · TTS 입력 = 고친 글 · 괄호 제거는 TTS 직전 한 곳(`:540`) | PASS(test_correct 그대로 통과) |
| 기록 | 그대로 · 통째로 버린 발화 0줄 · 끼어들기로 음성이 끊긴 발화도 줄 있음 | PASS(⑳) |
| 경계 | front가 back 내부를 import 하지 않음 · 변경은 `back/` · `front/` 안뿐 · 비밀값 · 주소 하드코딩 0 | PASS |

## 미결 대조 (볼 것 4)

- **① 멈춤 중 차례 끝에 글 없는 `end_of_segment`** — `session.py:614-620`: 멈춤 중에는 글을 싣지 않는다. 다만 그 차례에 이미 연 segment(`_seg_pieces > 0`)가 있으면 `{"text":"","end_of_segment":true}` 로 닫는다. 한 번도 안 보냈으면 아무것도 보내지 않는다. SPEC G 「`pause` 상태에서는 agent text 를 보내지 않는다」 · 「이 통키 차례에 `agent_text` 를 한 번도 보내지 않았으면 `end_of_segment` 도 보내지 않는다」 · 공식 「Always end a turn with `end_of_segment`」(G 「정상 끝」)을 함께 읽으면, **이미 열린 segment는 닫는 것이 맞다**. 시험 ⑰(멈춤 중에 처음부터 끝까지 간 차례 → `agent_text` 0 · `end_of_segment` 0)도 맞다. **PASS.** 이 경우는 front 출력 구간이 이미 닫힌 뒤(재생 끝 + 400 ms) back이 아직 차례인 짧은 틈에 `pause` 가 올 때만 생긴다(그 밖에는 `playback_stopped` 가 먼저 와서 끼어들기 길로 간다).
- **⑤ 시험이 실제 1초를 기다림** — **WARN-1**(SPEC §9.1 문구와 다름 · 기대값은 그대로).

## 고객이 실물에서 만날 자리

- **끼어든 뒤(또는 원을 눌러 멈춘 뒤) 다음 통역에서 통키가 자기 목소리를 다시 통역한다 · 재생 직후 대답 첫머리가 몇 초 사라진다** — FAIL-1. 멈춘 발화가 길수록(긴 번역 한가운데 끼어들기) 심해진다. 끼어들기가 오는 「보통」 경우(스트림이 다 와 있고 재생 한가운데 — §5.13 F)에 그대로 걸린다.
- r2 리포트의 감수 자리는 코드가 문서대로 만들었다: 끼어든 뒤 멈추기까지 1.3 ~ 1.9 s + 전달 · 말 끝 → 음성 약 2 s + TTS · 같은 언어로 끼어든 말은 사라짐 · 재생 직후 0.5 s 안 같은 언어 대답 첫머리(자동 듣기) · 누른 채 음성 중에 떼면 끊김 · 새 front + 옛 back이면 오류 화면 · 좁은 창의 다음 발화 재생(출력 구간은 `audio_end` 로 닫힘 — r2 WARN-1 닫힘 확인).
- r2 WARN-2(멈췄는데 남은 번역이 계속 나옴) — **닫힘.** 이 차례의 id 아무거나 받으면 멈춘다(`_turn_ids` · 시험 ⑯).
- r2 WARN-3(누르고 한 대답의 첫머리) — **닫힘.** 기다림이 리더를 막지 않고 끝은 절차 시작 때다(`session.py:502` · `:519` · 시험 ㉔). 단 FAIL-1이 같은 증상을 다른 길로 다시 만든다.

## 참고(기존 부채 · 낮음)

1. `turn.py:214` `_barge_nf_none` 은 만들기만 하고 쓰지 않는다. `start_ms` 없는 토큰은 「통키 차례가 시작된 뒤 처음 나타났으면 센다」(§5.13 F)가 아니라, 나올 때마다(차례 전부터 있던 비확정 포함) 센다. Soniox 원문 토큰은 실제로 `start_ms` 를 늘 싣는 것으로 보여 영향은 거의 없다. 죽은 필드만 남았다.
2. `back/tests/test_context.py:177-180` · `:212-215` · `back/tests/test_interpret.py:136-139` · `:166-169` — 가짜 메서드 안의 빈 줄 모양이 어색하다(`def …:` 다음 빈 줄 · 뒤에 빈 줄 둘). ruff는 통과한다. 취향 수준이라 지적하지 않는다.
3. 시험 전체 52 s — 대부분 WARN-1의 실제 1초 대기다.
4. `session.py:118-119` 의 keepalive · `last_audio` 는 실제 시계(`time.monotonic`)를 쓰고, 차례 판정은 주입 시계를 쓴다 — 의도대로다(§5.13 J 「시계를 주입받는 순수 로직」). 무관.
5. 무관 · 기존: pytest 경고 1개(starlette `httpx` 폐기 예고).

- allowed_paths 이탈 0 — 이 리포트 파일만 만들었다. 레포 · SPEC · DEC는 읽기만 했다. 프로브는 스크래치(`/private/tmp/claude-501/…/scratchpad/probe/test_probe_skew.py`)에 있다.
