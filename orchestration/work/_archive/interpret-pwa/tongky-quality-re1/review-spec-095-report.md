# 리뷰 리포트 — tongky-quality-re1 / doc (2026-11-16)

- 대상: SPEC-001 0.9.5(`git diff` — §1 · §2.4 · §5.1 · §5.3 · §5.10 · §5.13 · §7.3 · §7.4 · §7.7 · §8 · §9.1 · §9.2 · §9.3 ㉘ · §9.4 · §9.6 · §10 · 부록 A) · WORK-001 WP30 ~ WP32
- 대조 기준: DEC-001 D-67 ~ D-70 · OQ-034 ~ 036 · `research-turn-taking-report.md` · 공식 문서(2026-11-16 직접 읽음 — `stt/rt/agent-text-input.mdx` · `tts/rt/timestamps.mdx` · `api-reference/tts/websocket-api.mdx`)
- 코드(읽기만): `interpret-pwa/tongky-quality-re1` @ `fe375ad` — `back/app/service/interpret/{session,soniox,assembler}.py` · `front/lib/{interpret,halfDuplex,output,ptt}.ts`
- 줄 번호: `spec` = `para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` · `work` = `…/30-work/work-001-interpret-pwa.md` · `dec` = `…/10-decision/decision-001-interpret-pwa.md`
- 수정 0 · 생성 파일은 이 리포트 1개.

## 판정: FAIL

FAIL 1 · WARN 8. FAIL 은 한 줄로 고칠 수 있는 자기모순이지만, 누르고 말하기의 기본 흐름에서 대답 첫머리가 버려지는 쪽으로 읽힐 수 있어 발주 전에 닫아야 한다. 나머지 계약(메시지 모양 · 순서 · 숫자 · agent text)은 DEC · 리포트 · 공식 문서와 맞는다.

| 볼 것 | 결과 |
|---|---|
| 1. 근거(DEC · 리포트 · 공식) | 대체로 맞음 — D-70 미반영(WARN-1) · 리포트에 없는 수치 1(WARN-7) · DEC 밖 기본값 목록(WARN-8). 새 화면 문구 0 확인(`spec:1791` · `spec:1916` ⓓ) |
| 2. back ↔ front 계약 | 모양 · 방향 · 이미 받은 PCM · 재생 큐 · 원 표시 · 언어 바꿈 · 오류는 닫힘. 구멍: FAIL-1 · WARN-2 · WARN-3 · WARN-4 |
| 3. agent text ↔ 공식 문서 | **같음** — 아래 표 |
| 4. 반이중 전제 문장 | 계약을 뒤집는 잔재 0. 옛 문장에 「(0.9.5) 이렇게 읽는다」 를 덧붙인 자리 3(WARN-6) |
| 5. 시험 · 실물 | 규칙 ① ~ ④ · D-69 숫자 · D-70 ① ③ 고정됨. 「가짜만으로 done 금지」 있음(`work:178` · `work:119` 완료 조건 · `spec:2308`). 빠진 것: FAIL-1 · WARN-2 · WARN-5 |
| 6. 코드에 비춰 만들 수 있나 | 만들 수 있다 — back 은 재생 구간을 「보낸 오디오 길이 + 서버 시계」 로 어림(`spec:1606` · 공식 문서가 허용). 걸리는 곳: WARN-2 · WARN-5 |

**agent text 대조(볼 것 3)**

| 항목 | SPEC | 공식 문서 | 판정 |
|---|---|---|---|
| 켜는 키 | `enable_agent_text_input: true` · start 요청(`spec:1638`) | 「Enable it in the start request」 · 같은 키 | 같음 |
| 메시지 | `{"type":"agent_text","text":…}` · 같은 STT 연결 · 텍스트 프레임(`spec:1639`) | 같음 · `text` 는 「Can be empty」 | 같음 |
| 끝내는 법 | `end_of_segment: true` — 마지막 조각에 싣거나 빈 `text` 로 따로(`spec:1639` · `spec:1644`) | 「either on its own or with the last piece of text」 · 「Always end a turn with `end_of_segment`」 | 같음 |
| 순서 · 때 | 재생 0.7초 앞 · 시작 시각 기준 · 50 ms 틱(`spec:1642` · `spec:1608`) | 「about 500 ms to 1 second ahead」 · 「Go by start times」 · `LEAD_S = 0.7` · 「A separate timer every 50 ms or so works too」 | 같음 |
| 끼어들기 | 재생된 것 중 안 보낸 글 → `end_of_segment` → 남은 글 안 보냄(`spec:1645`) | 「When the user interrupts」 1 ~ 3 그대로 | 같음 |
| 한 덩이 | 통키 차례 = segment 하나(`spec:1643`) | 「One segment per agent turn」 | 같음(재생 쪽이 바뀌면 끊는 것은 문서에 없음 — SPEC 이 기본값으로 표시) |
| 서버 어림 | 보낸 시간으로 어림 · 보낸 오디오를 넘지 않음(`spec:1606`) | 「estimate the position from the time since you started sending…」 · `min(elapsed, audio_sent_s)` | 같음 |
| 모델 · 오류 · 요금 | `stt-rt-v6` 만 · 오류는 스트림 끝 · 입력 토큰 요금(`spec:1638` · `spec:1647` · `spec:1648`) | 같음 | 같음 |
| TTS 글자 시각 | `return_timestamps: true` · `timestamps.characters` · `character_start_times_seconds`(`spec:1641`) | `tts/rt/timestamps` 같은 이름 · 「clients must handle audio frames both with and without alignment data」 · 전처리된 글 기준 | 같음 |
| TTS 취소 | `{"stream_id":…,"cancel":true}` → `terminated`(`spec:1628`) | 「Client-initiated cancellation」 같은 모양 | 같음 |

## FAIL

### FAIL-1 멈춤 중에 끝난 재생 구간 — 「길이 0」 과 「끝 = `sent_ms` + 500」 이 서로 어긋난다

- 자리: `spec:1616`(재생 구간 「끝 = 재생이 끝난 틱의 `sent_ms` + `ECHO_TAIL_MS` = 500」) ↔ `spec:1620`(「멈춤 중 … `sent_ms` 가 흐르지 않고 되울림도 없다 — 재생 구간은 길이 0 이 된다」) · 시험 `spec:1907` ④ · ⑰ 에 이 경우 없음.
- 무엇: 멈춤 중에는 `sent_ms` 가 X 에 멈춰 있다. `spec:1616` 의 식대로면 구간은 `[X, X+500)` 이고, `spec:1620` 대로면 `[X, X)` 다. 둘 중 어느 쪽인지 문서가 고르지 않았다.
- 왜 FAIL: 누르고 말하기의 기본 흐름이 정확히 이 경우다 — 손님이 말함 → 뗌(`pause`) → 통키가 한국어로 재생(멈춤 중 · `spec:1665`) → 직원이 원을 누르고 한국어로 대답. 직원의 대답은 **재생 쪽 언어**이고, `resume` 뒤 처음 500 ms 의 `start_ms` 가 `[X, X+500)` 에 든다. 식대로 만들면 대답 첫머리 토큰이 되울림으로 버려진다(`spec:1617` 「언제 도착했든」). 마이크가 닫혀 있던 구간이라 실제 되울림은 없었다. 자동 듣기에서 원을 눌러 멈춘 뒤 다시 들을 때도 같다.
- 근거: D-68 「누르고 말하기(D-36)는 그대로」(`dec:124`) · D-70 ② 의 여유 500 ms 는 「재생 끝 여유」 다(`dec:126`) — 마이크가 닫힌 채 끝난 재생에는 여유가 가릴 소리가 없다. rules.md 「워커가 추측으로 메워야 하는 빈칸」.
- 같이 볼 것: 지난 구간을 「끝난 뒤 30초 동안 들고 있는다」(`spec:1616`)의 30초가 서버 시계인지 `sent_ms` 인지도 적혀 있지 않다 — 멈춤이 길면 답이 갈린다.
- 닫는 길(결정은 코디): 「멈춤 중에 끝난(또는 멈춘) 구간은 여유 없이 끝 = 시작」 으로 못 박거나, 여유를 `sent_ms` 가 아니라 서버 시계로 잰다고 적는다. 어느 쪽이든 `spec:1907` 에 「멈춤 중 재생이 끝난 뒤 `resume` — 재생 쪽 언어 첫 토큰이 남는다」 시험 한 줄.

## WARN

### WARN-1 D-70 이 SPEC · WORK 에 없다 — OQ-037 ~ 039 가 DEC 에서는 닫혔고 SPEC · WORK 에서는 열려 있다

- 자리: `dec:126`(D-70 — OQ-037 · 038 · 039 를 코디 기본값으로 닫음) ↔ `spec:25` · `spec:72`(「D-01 ~ D-69」) · `spec:1550`(§5.13 제목 「D-68 · D-69」) · `spec:1597`(「DEC 는 이 경우를 정하지 않았다 — 기본값 · OQ-037」) · `spec:2496` ~ `spec:2498`(열린 것으로 굵게) · 부록 A `spec:2602` ~ `spec:2603`(D-70 행 없음) · `work:55` · `work:196` ~ `work:198`(「WP32 뒤 사용자」).
- 값은 같다 — D-70 ① = `spec:1597` · ② = `spec:1616`(500 ms · `start_ms`) · ③ = `spec:1594` · `spec:1665`. 워커가 틀리게 만들 일은 없고 근거 표기만 낡았다(SPEC 이 D-70 보다 먼저 쓰였다).
- DEC 쪽 낱말 하나: D-70 ① 은 「**통키 차례 중** 반대쪽이 말을 시작하면」 이라고 적었는데(`dec:126`), 통키 차례 중의 반대쪽 말은 D-68 ④ 끼어들기다. SPEC OQ-037 이 다루는 것은 「**말하던 사람의 차례 중**」(`spec:2496`)이다. DEC 문장을 그대로 읽으면 규칙 ④ 와 겹친다 — 맞추는 쪽은 코디가 정한다.

### WARN-2 재생 멈춤 절차 — `audio_stop` 이 TTS `terminated` 뒤에 있고, 기다리는 한도가 없고, 스트림이 이미 끝난 경우가 없다

- 자리: `spec:1628`(「순서대로: ① `cancel` → `terminated` 까지 읽어 버린다 … ③ front 로 `audio_stop`」) · `spec:2315`(㉘-4 통과 조건 「TTS `cancel` 뒤 `terminated` 를 받고」) · `spec:1907` ⑨(「Soniox TTS 에 `cancel` 1번」).
- ⓐ 순서를 글자대로 만들면 front 의 멈춤이 Soniox 왕복 하나만큼 늦는다 — D-68 ④ 「재생을 **바로** 멈추고」(`dec:124`)와 어긋나는 쪽이다. ①(읽어 버리기)을 기다리지 않고 ③ 을 먼저 보내도 되는지 문서가 말하지 않는다.
- ⓑ `terminated` 가 오지 않을 때의 한도가 없다. 지금 `speak()` 는 `terminated` 까지 도는 제너레이터다(`back/app/service/interpret/soniox.py` `SonioxTts.speak`) — 안 오면 TTS 작업이 오류 없이 멈춘다.
- ⓒ 공식 문서: 「TTS also generates audio faster than real time」(`agent-text-input` 「Send the text in time with the audio」). back 은 받은 조각을 곧바로 front 로 넘기므로(`session.py` `_tts_worker`), 끼어들기가 오는 재생 한가운데에는 그 차례의 TTS 스트림이 **이미 다 끝나 있는 것이 보통**이다. 그때 ① 을 건너뛰는지(「진행 중인」 이라는 낱말뿐) · 끝난 `stream_id` 에 `cancel` 을 보내면 안 되는지가 적혀 있지 않고, ㉘-4 의 「`cancel` 뒤 `terminated`」 는 실물에서 그 조건이 만들어지지 않을 수 있다(「재생 한가운데」 에 섞으므로).
- 같은 이유로 「읽을 큐를 비운다」(②)는 실물에서 대개 빈 큐다 — 멈춤의 실제 일은 front 의 버림(`spec:1174`)이 한다. 계약은 맞고, 시험 · 실물 조건만 이 사실에 맞춰야 한다.

### WARN-3 `playback_stopped` 가 날아가는 동안 back 이 보낸 다음 발화 — front 가 다시 재생한다

- 자리: `spec:1657` · `spec:1659`(「큐를 비운 뒤 다음 `audio_start` 까지 오는 조각은 버린다 — back 이 알림을 받기 전에 이미 보낸 조각이 여기에 걸린다」) · `spec:1167` · `spec:1801`.
- 버림 표시는 「다음 `audio_start`」 에 풀린다. 한 차례에 발화가 여럿이면(`spec:1179`) back 이 알림을 받기 전에 **다음 발화의 `audio_start` + 조각**을 이미 보냈을 수 있고, front 는 그것을 새 발화로 받아 재생한다. back 은 그 사이 재생 구간 · agent text 를 닫았으므로(`spec:1658`) 그 소리는 걸러지지 않는다. `spec:1659` 의 설명은 「같은 발화의 남은 조각」 만 덮는다.
- 창은 좁다(차례 시작 직후 back 이 조각을 넘기는 동안 사용자가 원을 누른 경우). 0.9.4 에도 같은 길이 있었으나 그때는 back 이 재생 상태를 들고 있지 않았다. `audio_stop` 쪽(back 이 멈춤)은 WS 순서가 지켜져 이 문제가 없다.
- 닫으려면 메시지 모양이 바뀐다(예: front 가 멈춘 뒤 back 의 확인을 받을 때까지 버림) — 결정 사항이라 적어만 둔다. 감수라면 `spec:1659` 에 그렇게 적는 것이 맞다.

### WARN-4 낱말 「끝」 이 여유를 품은 뜻과 안 품은 뜻으로 섞여 쓰인다

- 자리: `spec:1616`(「끝 = … `sent_ms` + `ECHO_TAIL_MS`」 — 여유 포함) · `spec:1617`(판정 `시작 ≤ start_ms < 끝` — 포함된 끝 · 같은 칸 뒤쪽 「(끝 + 여유 전)」 — 한 번 더 더함) · `spec:1628` ⑤(「끝 = 지금 `sent_ms` + 여유」) · `spec:1907` ④(「`시작 ≤ start_ms < 끝 + 여유`」 · 「끝 + 500 ms 뒤 = 남김」).
- 정의를 따라 읽으면 `spec:1617` 뒤쪽 · `spec:1907` ④ 는 여유가 두 번(1,000 ms) 들어간다. 시험 문장의 「끝 + 500 ms 뒤 = 남김」 으로 500 이 맞다는 것은 짐작되지만, 시험을 먼저 쓰는 워커와 로직을 먼저 쓰는 워커가 다르게 읽을 수 있다. D-70 ② 는 500 ms(`dec:126`).

### WARN-5 agent text 를 보낼 글자 — 「지금 읽는 발화」 로 좁혀져 있다

- 자리: `spec:1642`(「지금 읽는 발화의 아직 안 보낸 글자 가운데 `시작 시각 ≤ 재생 위치 + 0.7`」) ↔ `spec:1606`(「앞 발화가 아직 재생 중이면 음수」).
- 한 차례에 발화가 여럿이면 다음 발화의 첫 0.7초 분량은 **앞 발화가 끝나기 전**에 나가야 0.7초 앞섬이 지켜진다. `spec:1606` 은 음수 재생 위치를 정의해 그 셈을 열어 두었지만 `spec:1642` 는 대상을 「지금 읽는 발화」 로 적었다 — 글자대로면 발화가 바뀔 때마다 첫 글자가 늦는다(공식 「about 500 ms to 1 second ahead of playback」). 「지금 읽는 발화」 가 TTS 를 받는 발화인지 재생 위치의 발화인지도 적혀 있지 않다(WARN-2 ⓒ — 둘은 보통 다르다). 시험 `spec:1907` ⑫ 는 발화 둘의 경계를 보지 않는다.

### WARN-6 반이중 문장에 「이렇게 읽는다」 를 덧붙인 자리

- `spec:1801` — 「다음 `audio_start` 가 오면 … (그 발화는 재생 · **반이중 막음 시작**)」 · 「**반이중 게이트(`speaking`)** 는 열지 않은 상태 그대로 — 버린 조각이 **송신 재개 타이머**를 건드리지 않는다」 · 「back 은 `pause` 와 상관없이 그 발화의 남은 음성 조각과 `audio_end` 를 끝까지 보낸다 … back 은 바꾸지 않는다」 가 그대로 있고 끝에 「(0.9.5) 출력 구간으로 읽는다」 가 붙었다. 뒤 문장은 `spec:1174`(끼어들기 뒤 PCM · `audio_end` 없음) · `spec:1658` 과 겹쳐 읽어야 뜻이 맞는다.
- `spec:1852` — §7.7 머리말 「**back 무변경 · WS 메시지 그대로**」 가 그대로 있고 `spec:1867` 이 「그때의 말」 이라고 풀었다.
- `spec:1383` — 「반이중(재생 중 마이크 안 보냄)은 그대로」 뒤에 0.9.5 괄호.
- 계약이 뒤집히지는 않는다(덧붙인 문장이 이긴다). WP31 이 §7.4 만 읽고 만들므로 `spec:1801` 은 취소선으로 바꾸는 편이 안전하다.

### WARN-7 리포트에 없는 수치

- `spec:1641` — 「리포트 Q2 의 시험이 이 방법이었다 · **14 세션 중 13 성공**」. 리포트(`research-turn-taking-report.md:86` ~ `:87`)는 되울림만 8 세션 중 7 이 재생 쪽 0(1 세션 0.95 남음) · 겹침 6 세션 중 재생 쪽 5 세션 0 · **1 세션 0.30** 이다. 「13」 은 리포트에 없는 셈이다(재생 쪽이 남은 세션은 둘).

### WARN-8 DEC 에 없는 기본값 — SPEC 이 「기본값」 으로 표시해 둔 것(값을 정한 사람 확인만)

- D-70 이 닫은 셋 밖에 남은 것: `language` 없는 원문 토큰은 셈에서 뺀다(`spec:1571`) · 「새 말」 글 비교 방법(`spec:1574`) · 차례 끝에 `finalize` 를 보내지 않는다(`spec:1593`) · 통키 차례 중 확정된 짧은 말은 같은 차례에 이어 읽는다(`spec:1598`) · 지난 구간 30초 보관(`spec:1616`) · 글자 시각이 없으면 고르게 나눠 보낸다(`spec:1641`) · 재생 쪽이 바뀌면 segment 를 끊는다(`spec:1643`) · 멈춤 중 agent text 안 보냄(`spec:1646`) · 새 WS 메시지 둘(`spec:1563` 「기본값(D-68 ④ 를 나르는 길)」) · `PLAY_TICK_MS` 50 · `AGENT_TEXT_LEAD_SEC` 0.7(공식 예시 값).
- 모두 표시가 붙어 있고 근거(리포트 · 공식)가 달려 있다 — 지어낸 정책은 아니다. 다만 「멈춤 중 agent text 안 보냄」 과 「재생 쪽이 바뀌면 끊는다」 는 공식 문서에 없는 판단이고 ㉘-5 · ㉘-6(`spec:2316` ~ `spec:2317`)이 그 값을 실물로 본다.

## 고객이 실물에서 만날 자리

- **누르고 말하기로 통역 음성을 듣고 바로 대답할 때 첫머리** — FAIL-1. 식대로 만들어지면 대답 앞 0.5초 분량이 자막에서 빠진다.
- **끼어든 뒤 재생이 멈추기까지** — 합성 조건 1.3 ~ 1.9초(`spec:1627`) + 전달. 상대 말이 2초 가까이 통역 음성과 겹친다(§9.6 ③ⓒ 가 본다).
- **말 끝 → 음성 시작이 약 2초 + TTS** — 0.9.4 보다 늦다(`spec:1596` · §9.6 ③ⓔ).
- **통역 음성과 같은 언어로 끼어든 말은 사라진다** — 감수(`spec:1618` · D-68 ③). 직원이 한국어 통역 음성 도중 한국어로 말하면 자막도 없다.
- **재생 직후 0.5초 안에 같은 언어로 시작한 대답의 첫머리** — 여유 500 ms(D-70 ② · OQ-038).
- **재생 중 상대가 말을 시작해도 원은 「출력 중」** — `audio_stop` 이 올 때까지(`spec:1791`).
- **누르고 말하기 — 누른 채 말을 멈췄다가 통역 음성이 나오는 중에 떼면** 그 음성이 끊기고 남은 번역은 자막만 남는다(`spec:1800` 「뗌(`pause`)」 · `front/lib/interpret.ts` `pause()` 가 늘 재생을 멈춘다). 0.9.4 에도 문장 확정이 누르는 중에 나면 같았다.
- **배포 순서** — 새 front + 옛 back 이면 원을 누르는 순간 오류 화면(`spec:1180` · `spec:2454` · `work:121`). 홈 화면 앱이 옛 껍데기를 들고 있는 경우도 적혀 있다.
- **재생 소리가 목소리보다 크면 진짜 말이 묻힌다** — 숫자로 못 푼다(`spec:2471` · 리포트 Q2 #6 · OQ-035).

## 참고(기존 부채)

- 무관 · 기존: `spec:1765` #4 「멈춤 중이면 `resume` → 8」 — 재생이 이어지는 동안은 판정 순서상 #4 가 그대로 보인다(0.9.4 이전부터의 표기). 0.9.5 에서는 이 길이 「재생 도중 `resume`」(`spec:1646` · ㉘-6)과 만난다 — 계약은 맞다.
- 코드 주석의 「반이중」 · 「마이크 막음」(`front/lib/output.ts:2` ~ `:4` · `interpret.ts:71` · `halfDuplex.ts:1` ~ `:2`)은 WP31 ② 가 고치도록 적혀 있다(`work:120`).
- WP30 의 「기존 시험 가운데 확정 즉시 `audio_start` 를 전제한 것」 — `back/tests/test_interpret.py` · `test_context.py` · `test_quality.py` · `scripts/quality_check.py` · `scripts/live_check.py` 가 `audio_start` · `speak` 를 본다(파일 수만 확인 · 실행하지 않음). `work:119` ⑥ 이 「전부 grep 해서 센다」 로 적어 두었다.
- allowed_paths 이탈 0(이 리포트 파일만 생성 · 코드 레포는 읽기만).
