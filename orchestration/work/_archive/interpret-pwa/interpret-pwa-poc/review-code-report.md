# 리뷰 리포트 — interpret-pwa-poc / code (2026-10-26)

- 대상: 워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc` · `kknaksss/interpret-pwa-poc` vs `origin/main`(뼈대 커밋 `6a03d82`) — untracked 전부(`back/` · `front/` · `docker-compose.yml` · `.env.example`). `node_modules` · `.next` · `.venv` · `.env` 제외(`.env` 열지 않음)
- 기준: SPEC-001 0.2.0 · DEC-001 D-01 ~ D-17 · WORK-001 WP5 행
- 방법: read-only 정적 대조. 시험 · 서버 실행 없음 — 실행 결과는 워커 리포트(wp1 ~ wp4) 인용. 빌드 산출 CSS(`front/.next/static/chunks/*.css`)는 읽기로만 대조

## 판정: FAIL (FAIL 1 · WARN 6)

FAIL 은 하나다(멈춤 뒤 같은 발화 음성 조각이 다시 재생됨). 나머지 계약 항목은 PASS 다. WP6 에서 FAIL-1 을 고치고 WARN 은 코디가 처분한다.

---

## FAIL

### FAIL-1 — 「출력 중」에 멈춤을 누른 뒤에도 같은 발화의 남은 음성 조각이 재생된다 → 반이중이 깨질 수 있다
- 위치: `front/lib/interpret.ts:195-216`(`onAudio` — 막는 조건 없음) · `:236-249`(`stopPlayback`) · `:267-274`(`pause`) · back 은 `back/app/service/interpret/session.py:249-260`(`_tts_worker` — `pause` 와 상관없이 그 발화의 남은 조각과 `audio_end` 를 계속 보냄)
- 근거: SPEC §7.3 #4 「멈춤 중이 아니면 `pause` — **지금 재생을 멈추고 큐를 비운 뒤** `pause` 전송 → 5」 · §7.4 반이중 「멈춤 · 닫기 · 오류 · 언어 바꿈은 재생 큐를 비운다」 · D-03(반이중)
- 무슨 일이 생기나: `pause()` 가 `stopPlayback()` → `gate.reset()` 을 부른다. 그 뒤 back 이 같은 발화의 바이너리를 더 보내면(TTS 가 아직 스트리밍 중일 때) `onAudio` 가 그대로 `schedule()` 한다. `audio_start` 가 다시 오지 않았으니 `gate.speaking` 은 false 다. 그래서
  1. 화면은 「멈춤」인데 스피커에서 번역 음성이 다시 나온다.
  2. 그 소리가 나는 동안 사용자가 원을 다시 누르면(`resume`) `gate.speaking=false` 라 마이크 PCM 이 다시 나간다(`interpret.ts:115`). 그러면 TTS 소리가 STT 로 들어가 에코가 된다. 반이중이 막으려던 상황이다.
- 언제 생기나: `audio_start` 직후, 곧 TTS 조각이 아직 다 오지 않았을 때 원을 누르면 생긴다. 실물에서 재현될 수 있다. 시험이 이 자리를 덮지 않는다 — `halfDuplex.test.ts` 는 gate 만 보고, `onAudio` 를 막는지는 보지 않는다.
- 고칠 방향(제안): `pause()` · `stopPlayback()` 때 「다음 `audio_start` 까지 바이너리를 버림」 플래그를 세우고 `audio_start` 에서 푼다. 시험에 「pause 뒤 같은 id 조각 → 재생 0 · 송신 gate 그대로」 1건을 더한다.

---

## WARN

### WARN-1 — `GLOSSARY_MATRIX_URL` 이 URL 모양부터 틀리면 back 이 아예 뜨지 않는다
- 위치: `back/app/service/glossary.py:61-78` — `httpx.TimeoutException` · `httpx.HTTPError` · `ValueError` 만 잡는다. `httpx.InvalidURL` 은 `Exception` 을 바로 상속한다(`.venv/.../httpx/_exceptions.py:271`, 이 셋 어느 것의 하위도 아니다). 그래서 lifespan 이 예외를 던진다(`back/app/main.py:55-57`).
- 근거: SPEC §4.2 「읽기 실패 = 빈 용어집으로 뜬다 … **back 기동은 막지 않는다**」 · D-14
- 언제 생기나: 비출력 문자 · 빈 호스트처럼 httpx 가 URL 파싱 단계에서 거절하는 값. 호스트만 틀린 값은 `ConnectError` 라 지금도 빈 용어집으로 뜬다. §9.3 ⑥ 「주소를 틀리게 둔 기동」을 이렇게 시험하면 back 이 죽는다.
- 제안: 마지막에 `except Exception` 하나를 두고 「이유 종류만」 남기는 경고를 찍는다.

### WARN-2 — ASCII 가 아닌 토큰이 오면 401 이 아니라 500 이 난다
- 위치: `back/app/service/auth.py:77` `hmac.compare_digest(sig, self._sign(body))` — 둘 다 `str` 이다. ASCII 가 아닌 글자가 섞이면 `TypeError` 가 난다. WS 쪽 `back/app/api/interpret.py:57-61` 은 `DomainError` 만 잡는다.
- 근거: SPEC §3.2 「실패면 401 `unauthorized`」 · §5.2 「실패면 accept 하지 않고 close 1008」
- 언제 생기나: 토큰을 망가뜨린 요청(`?token=a.%C3%A9` · latin-1 헤더)이다. 보통 사용으로는 생기지 않는다. 그래도 거절은 되지만 `/api/auth/me` 는 CORS 헤더 없는 500 이 된다. front 는 이것을 401 로 처리하지 못한다.
- 제안: `sig.encode()` 와 bytes 로 비교하거나 `TypeError` 를 `bad` 로 바꾼다.

### WARN-3 — 「시작 전」 오버레이가 헤더를 덮지 않는다(SPEC 「화면 전체」와 다름)
- 위치: `front/components/interpret/InterpretScreen.tsx:207` · `:259-276` — 오버레이가 헤더 아래 `relative` 컨테이너 안의 `absolute inset-0` 이다.
- 근거: SPEC §7.3 #1 「화면 전체 오버레이 「탭해서 통역 시작」」
- 판단: 워커가 알고 고른 것이다(wp3 이슈 3 — 시작 전에도 햄버거로 로그아웃 · 용어집을 열 수 있게). 원 누름 · 드롭다운을 덮는 조건(§9.2)은 지킨다. **기능 결함은 아니다.** SPEC 을 「헤더 아래 전체」로 고칠지, 코드를 고칠지 코디 · 사용자가 처분한다.

### WARN-4 — 「〈언어〉로 출력 중」 표시가 앞 발화를 재생하는 중에 다음 발화 언어로 바뀐다
- 위치: `front/lib/interpret.ts:177-183` — 이미 재생 구간이면 `audio_start` 를 받자마자 `onOutput(새 발화 side)` 를 부른다. back 은 앞 발화 조각을 **다 보낸 뒤** 다음 `audio_start` 를 보낸다(`session.py:254-257`). TTS 가 실시간보다 빨리 오면 앞 발화가 아직 재생되는 중에 표시가 바뀐다.
- 근거: SPEC §7.3 #4 · D-09 「TTS 재생 중에는 **그 언어 색** + 「〈언어〉로 출력 중」」
- 판단: 워커가 알린 것이다(wp4 이슈 3). 반이중(송신 0)에는 영향이 없다. 양쪽이 번갈아 빠르게 말하면 원 색 · 문구가 실제로 나오는 언어와 잠깐 어긋난다. 고치려면 바꾸는 시점을 재생 시각 기준(`nextTime`)으로 옮긴다.

### WARN-5 — 로그인 env 가 일부 빠졌는데도 「아이디 또는 비밀번호가 맞지 않아요」만 보인다 · 5번째부터는 429
- 위치: `back/app/service/auth.py:56-63` — `configured=False` 여도 실패 수를 센다. 문구는 자격 오류와 같고 back 로그도 남지 않는다.
- 근거: SPEC §2.4 「비면 로그인 불가(**모든 시도 401**)」 — 5회 뒤 429 는 §3.1 잠금 규칙이 먼저 걸린 결과라 계약 해석 차이다.
- 판단: 계약 모양(같은 401)은 지킨다. 다만 사용자가 `.env` 에 `INTERPRET_SESSION_SECRET` 하나만 빠뜨려도 원인을 알 길이 없다(「사용자가 실물에서 만날 자리」 1번). 기동 때 「로그인 env 미설정」 경고 1줄(값 없이 이름만)을 남기기를 권장한다.

### WARN-6 — 용어집 읽기 「10초 시간 초과」가 전체 시간이 아니라 단계마다 10초다
- 위치: `back/app/service/glossary.py:62` `httpx.AsyncClient(timeout=10.0)` — connect · read · write · pool 각각 10초다. 조금씩 흘려 보내는 서버라면 10초를 넘겨도 끊지 않는다.
- 근거: SPEC §4.2 「10초 시간 초과」
- 판단: stg 실물은 빠르다(wp1 · 158행). 기동이 조금 늦어질 수 있을 뿐이다. 엄밀히 맞추려면 `asyncio.wait_for(..., 10)` 으로 감싼다. 낮은 우선순위.

---

## PASS — WORK-001 WP5 항목 전수

| # | 항목 | 판정 | 근거(파일:줄) · SPEC |
|---|---|---|---|
| 1 | 로그인 같은 401 · 상수 시간 | PASS | `back/app/service/auth.py:56-63` — 아이디 · 비번 둘 다 `compare_digest` 뒤 `&` 로 판정 · 같은 `invalid_credentials` 문구 · §3.1 · §3.3 |
| 2 | 잠금 5회 / 60초 · 성공 시 초기화 | PASS | `auth.py:21-22,52-55,60-64` · 시험 `test_auth.py:64-73` 등 · §3.1(5번째 실패는 401 + 잠금 시작, 6번째부터 429 — 원형과 같음) |
| 3 | 토큰 검증(서명 · 만료 · `sub` = 지금 env 아이디) | PASS | `auth.py:70-90` · 401 `unauthorized` 「로그인이 필요해요」 · §3.2 (ASCII 아님 예외는 WARN-2) |
| 4 | 로그인 요청 400 `invalid_request` | PASS | `back/app/schemas/auth.py:6-10`(`extra=forbid` · `StrictStr`) · `main.py:72-76` · §3.3 |
| 5 | 오류 본문 `{error:{code,message}}` | PASS | `main.py:45-80` · §3.3 |
| 6 | 보호 대상 · 인증 없음 | PASS | `/api/auth/me`(`api/auth.py:15`) · `/api/glossary`(`api/glossary.py:12` — 401 먼저, 400 나중) · WS(`api/interpret.py:57-61`) · `/api/health` 인증 없음(`api/glossary.py:21`) · §3.3 |
| 7 | 용어집 기동 1회 · 실패 4종 → 빈 용어집 · 경고 1줄 | PASS (URL 파싱 예외는 WARN-1) | `glossary.py:58-80` · `main.py:55-57` · §4.2 · D-14 |
| 8 | 중복 `ko` 첫 행 · 빈 표기 뺌 | PASS | `glossary.py:87-97` · 시험 `test_context.py:20-33` · §4.2 |
| 9 | context 조립(general 3쌍 · terms ko · translation_terms ko→L · text 없음 · 역방향 없음 · 괄호 그대로) | PASS | `glossary.py:22-27,104-121` · §4.3 · D-05 |
| 10 | 줄이기 순서(`terms` 뒤에서부터 · `translation_terms` · `general` 은 안 줄임 · 다 빼도 넘으면 그대로) | PASS | `glossary.py:119-120` · 시험 `test_context.py:49-64` · §4.4 1 ~ 3 |
| 11 | `invalid_request` → `terms` 빼고 STT 1회 다시 · 두 번 거절 → `soniox_unavailable` · TTS 안 열림 | PASS | `session.py:132-144,116-126` · `glossary.py:124-126` · 시험 `test_context.py:181-200` · §4.4 4 · §4.4.1 |
| 12 | `ready` 앞 2초 확인(오류 · 닫힘 · 무응답 · 토큰 첫 메시지 넘김) · `SonioxError.error_type` | PASS | `session.py:152-176` · `soniox.py:28-34,65-71` · 시험 `test_context.py:174-247` · §4.4.1 |
| 13 | **조용히 통과 — 용어집 없이 몰래 연결** | PASS | 재연결은 `terms` 만 뺀다(`translation_terms` · `general` 은 남는다 — `test_context.py:188-189`). `terms` 가 이미 없으면 같은 설정을 다시 보내지 않고 바로 `soniox_unavailable`(`session.py:138-139` · `test_context.py:251-275`). 빈 용어집 → context 없이 연결은 D-14 가 정한 동작 |
| 14 | **조용히 통과 — `ready` 뒤 거절에 몰래 재연결** | PASS | `session.py:233-240` → `_pump` `soniox_unavailable` 「오류로 끊겼어요」(`:192-194`) · 시험 `test_context.py:222-229` · §4.4.1 |
| 15 | 칸 수 로그 · 용어 문자열 0 · 거절 로그 `error_type` · `request_id` 만 | PASS | `session.py:147-149,120,140,193` · 시험 `test_context.py:278-285` · §4.4 5 |
| 16 | `yue` 매핑(STT `language_b` · hints · TTS = `zh`) · 한 곳 | PASS | `back/app/service/interpret/langs.py:7-21` · `session.py:150` · TTS 언어 = 토큰 언어(`assembler.py:130-133`) · §5.5 · D-04 |
| 17 | 번체 자막(yue 만 · 중국어 쪽 문자열만 `s2tw`) / TTS 간체 / 용어 target `t2s` | PASS | `assembler.py:113-115,131` · `chinese.py:17-22` · `glossary.py:113` · `session.py:128` · 시험 `test_interpret.py:51,346` · §5.6 · §4.3 · D-17 |
| 18 | `start` lang 6개 · `traditional` · `scheduleId` 무시 · 오류 문구 「가능: en, ja, th, vi, yue, zh」 | PASS | `session.py:52-64` · §5.1 · §5.4 |
| 19 | `no_api_key` 문구 「SONIOX_API_KEY 가 .env 에 없어요」 | PASS | `session.py:112-114` · §5.4 |
| 20 | WS accept 전 인증(Origin → 토큰 · 1008) | PASS | `back/app/api/interpret.py:53-62` · 시험 `test_interpret.py:280-306` · §5.2 |
| 21 | Soniox 두 연결 정리(닫기 · stop · 오류 · 브라우저가 그냥 닫음 · 재연결 때 거절된 STT) | PASS | `session.py:129-130,141,279-288` · 시험 `test_interpret.py:230` · `test_context.py:190,200,229` · §5.2 |
| 22 | 영역 배치 D-16 | PASS | `front/lib/view.ts:13-17,39-47` · 시험 `front/tests/view.test.ts:8-29` · §7.5 |
| 23 | 반이중(`audio_start` 부터 송신 0 · 재생 끝 + 400 ms · 새 `audio_start` 면 재개 취소) | PASS (멈춤 뒤 남은 조각은 FAIL-1) | `front/lib/halfDuplex.ts:3-62` · `interpret.ts:115,177-188,219-233` · 시험 `halfDuplex.test.ts` · wp4 #8(재생 중 0 B) · §7.4 |
| 24 | §7.3 판정 순서(출력 중 > 멈춤) · 멈춤 중 출력 | PASS | `front/lib/view.ts:80-89` · 시험 `view.test.ts:41-57` · `halfDuplex.test.ts:50-62` · §7.3 |
| 25 | 「시작 전」 오버레이 · 탭 안에서 AudioContext → 마이크 → WS · `ready` 전 PCM 0 · 깨우는 곳 셋 | PASS (범위는 WARN-3) | `interpret.ts:82-91,115` · `InterpretScreen.tsx:66-95,178-184,245,260-266` · wp4 #1 ~ #4 · §7.4 |
| 26 | 언어 바꿈 stop → 새 start · 자막 지움 · 멈춤이어도 다시 듣기 | PASS | `InterpretScreen.tsx:178-184` · `interpret.ts:286-292` · §7.2 |
| 27 | 백그라운드 → stop → 「시작 전」 · 자동 재연결 없음 | PASS | `InterpretScreen.tsx:106-116` · `interpret.ts:315-323` · §8 |
| 28 | 원 색 = medikit 클래스 · 실재 | PASS | `front/components/interpret/Circle.tsx:7-22` · 빌드 CSS `.next/static/chunks/1e2215lh_dqyt.css` 에 `.bg-red` · `.bg-purple` · `.bg-primary` · `.bg-ms-gray-300/400` · `.bg-ms-overlay` · `.text-typo-*` 등 있음(직접 grep) · wp3 · wp4 대조 스크립트 78개 중 없는 것 0 · §7.3 · §9.2 |
| 29 | **조용히 통과 — 없는 medikit 클래스 · 컴포넌트** | PASS | 컴포넌트 `ComboBox` · `Popover` · `BaseModal` · `Table` · `Button` · `Input` · `ErrorIcon` 은 `@medisolve-ai/medikit@1.4.0` 의 export 다(`ComboBox` 의 `hasAllOption` · `hasCheckIcon` · `size` 는 `dist/index.d.ts:481-512` 에 있음). 햄버거 · 뒤집기 아이콘은 인라인 SVG(`icons.tsx`) · `Select` · `Drawer` · `Menu` 는 쓰지 않음. `check-classes.mjs` 는 음성 대조(일부러 넣은 없는 클래스를 잡는지)까지 했다(wp3) |
| 30 | **조용히 통과 — 빈 단언** | PASS | back 시험 함수 중 `assert` 가 없는 것은 3개뿐(`test_auth.py:64,108` · `test_interpret.py:74`)이고 셋 다 `pytest.raises` 로 단언한다. front 시험은 `it` 마다 `expect` 가 있다. 단언을 늘 참으로 만드는 패턴(`assert True` · `or` 폴백 · skip) 0 |
| 31 | 비밀값 · public 값 | PASS | `.env.example` 9개 이름 · 값 0(`INTERPRET_BACK_PORT` 없음) · 시험 값은 가짜(`conftest.py:13-14`) · 접근 로그 `?token=` 지움(`main.py:24-42` — uvicorn 은 경로를 `/…?qs` 문자열 인자로 찍는다, `uvicorn/protocols/utils.py:58-62`) · 로그 캡처 시험 `test_interpret.py:418,434` · `.gitignore`(루트 `.env` · `.env.*` · `!.env.example`) · `back/.dockerignore` · `front/.dockerignore` 가 `.env*` 를 뺀다 · 코드 grep 에 키 · 실계정 0 |
| 32 | 경계 · allowed_paths | PASS | front 는 back 을 import 하지 않음(HTTP · WS 만) · 변경은 `back/**` · `front/**` · `docker-compose.yml` · `.env.example` 안. `back/.gitkeep` · `front/.gitkeep` 삭제는 뼈대 정리 |

## BE ↔ FE 대조 (SPEC §3 · §4.6 · §5)

| 항목 | back | front | 판정 |
|---|---|---|---|
| 로그인 요청 · 응답 | `{id, password}` → `{token, expiresAt}`(`schemas/auth.py`) | `api.ts:63-71` 같은 이름 · `writeSession` | PASS |
| `/api/auth/me` | `{id}` · 401 `unauthorized` | `api.ts:72` · 401 → `goLogin`(`:56`) | PASS |
| 401 · 429 모양 | `{error:{code,message}}` | `api.ts:52-57` `error.message` 를 그대로 · 로그인 자체 401 은 화면 문구(`auth:false`) | PASS |
| 용어집 | `{loaded, version, count, lang, rows:[{category, ko, term}]}`(`schemas/glossary.py`) | `api.ts:75-87` 같은 필드 · `loaded=false` 문구(`GlossaryModal.tsx:26-27`) | PASS |
| WS 주소 · 토큰 | `/api/interpret` · 헤더 Bearer 또는 `?token=`(`api/interpret.py:42-46`) | `api.ts:90-96` `http→ws` · `?token=encodeURIComponent` | PASS |
| Origin | `INTERPRET_FRONT_ORIGIN` 기본 `http://localhost:3800`(`config.py:26`) | front 출처 `localhost:3800`(`package.json:6,8`) | PASS(127.0.0.1 로 열면 막힘 — SPEC §2.4 에 적힘) |
| 메시지 이름 · 필드 | `start{lang}` · `pause` · `resume` · `stop` / `ready` · `caption{id,side,original,translation,final}` · `audio_start{id,sampleRate}` · `audio_end{id}` · `error{code,message}` | `interpret.ts:140,158-192,271,281,288` 같은 이름 · 같은 필드 · `traditional` · `scheduleId` 안 보냄 | PASS |
| 오디오 | 받기 PCM s16le 16 kHz · 보내기 24 kHz(`soniox.py:23-24`) | worklet 16 kHz · 640샘플(`interpret.ts:28-48`) · `sampleRate` 로 재생(`:178,212`) | PASS |
| 오류 코드 | `bad_request` · `no_api_key` · `soniox_unavailable` | 코드로 분기하지 않고 `message` 를 보여 준다 · 오류면 닫음(`interpret.ts:189-191`). 「알 수 없는 프레임」 `bad_request` 는 back 이 끊지 않는데 front 는 끊는다 — front 는 그런 프레임을 보내지 않으므로 영향 없음 | PASS |
| 핸드셰이크 거절 → 401 확인 | accept 전 1008 | `ready` 전 `closed` → `me()` → 401 이면 로그인(`InterpretScreen.tsx:86`) | PASS |

## compose (읽기만 · SPEC §2.2 · §2.3)

| 항목 | 판정 | 근거 |
|---|---|---|
| back 8800 고정 | PASS | `back/Dockerfile:19` `--port 8800` · `docker-compose.yml:10` |
| front 3800 고정 | PASS | `front/package.json:6,8` · `front/Dockerfile:25,31` · `docker-compose.yml:20` |
| back `env_file: .env` · `required: false` | PASS | `docker-compose.yml:6-8`(Docker Compose 2.24 이상이 필요 — 참고) · 빈 값은 `env_ignore_empty=True` 라 기본값(`config.py:16`) — `.env.example` 을 그대로 복사해도 안전 |
| front `NEXT_PUBLIC_API_BASE_URL` = build.args 치환 · 기본 `http://localhost:8800` | PASS | `docker-compose.yml:14-18` — `:-` 라 빈 값도 기본값 · `front/Dockerfile:13-15,19` ARG → ENV → build · 비면 빌드를 멈춤(`:14`) |
| 둘이 같이 뜨는가 | PASS(읽기 기준) | 브라우저 → `localhost:8800`(호스트 포트) · CORS / Origin 기본값이 `localhost:3800` 과 맞음. 실행 확인은 WP7 |

## OQ-006 — 외국어 영역 문구 6 × 7(`front/lib/langs.ts:42-104`)

- 빈칸 0 — 6개 언어 × 8값(출력 중은 외국어 · 한국어 두 값). 명백한 오역 0.
- **기계 번역 수준 · 원어민 검수 없음 → PoC 범위로 표시.**
- 사소한 것(고치지 않아도 됨): `yue.speakingKorean` 「正以韓文播放」 — 음성 출력이라 「韓語」가 더 정확하다. `yue.speakingForeign` 「正以中文播放」은 TTS 가 만다린이라(OQ-001) 사실대로다.
- 한국어 문구 「〈언어〉로」 조사: 6개 이름이 모두 「어」로 끝나 「로」가 맞다(`phrases.ts:15,21`).

---

## 사용자가 실물에서 만날 자리

1. **`.env` 에 로그인 3개(`INTERPRET_LOGIN_ID` · `INTERPRET_LOGIN_PASSWORD` · `INTERPRET_SESSION_SECRET`)가 다 있어야 로그인된다.** 하나라도 빠지면 「아이디 또는 비밀번호가 맞지 않아요」만 보이고, 5번째 시도부터 1분 잠금이 걸린다(WARN-5).
2. **멈춤을 TTS 시작 직후에 누르면 번역 음성이 다시 나온다.** 그때 다시 듣기를 누르면 에코가 생길 수 있다(FAIL-1).
3. 양쪽이 빠르게 번갈아 말하면 원 색 · 「〈언어〉로 출력 중」이 실제 나오는 음성과 잠깐 어긋난다(WARN-4).
4. `yue`(廣東話)를 고르면 한국어 쪽 문구는 「광둥어로 출력 중」인데 실제 음성은 만다린이다(SPEC §5.5 ⚠ · OQ-001). 외국어 쪽 문구는 「中文」이라 둘이 다르게 말한다.
5. 뒤집힌 외국어 영역에서 언어 목록을 펼치면 목록은 바로 선 채 화면 아래로 펼쳐진다(OQ-010 · wp3 `20-combobox-open-flipped`).
6. `http://127.0.0.1:3800` 으로 열면 로그인부터 「서버에 연결하지 못했어요」가 뜬다(CORS · SPEC §2.4).
7. `NEXT_PUBLIC_API_BASE_URL` 을 바꾸면 front 를 **다시 빌드**해야 한다(`docker compose up --build`).
8. **Soniox 실물은 아직 한 번도 붙지 않았다**(wp2 · wp4 pending — 키 없음). 처음 실발화하는 날 다음 셋을 같이 확인한다: §9.3 ① 6개 언어 context 거절 여부(th 9,900자로 한도에 가장 가깝다) · ⑦ 2초 창 · 반이중 실물 0 B.
9. 시작 전에도 헤더 햄버거(용어집 · 로그아웃)는 눌린다(WARN-3 — 의도된 것).
10. iOS 에서 AudioContext 가 재생 중에 멈추면(전화 등) `onended` 가 오지 않아 「출력 중」에 걸리고 마이크가 막힐 수 있다. 백그라운드로 가면 정리되므로 PoC 범위다. 실기기는 WP8.

## 참고(기존 부채 · 무관 · 기록만)

- `context_rows` 는 고른 언어 표기가 빈 행의 `ko` 를 `terms` 에서도 뺀다(`glossary.py:92-93`). SPEC §4.3 「행의 `ko` 전부」보다 좁다. 실물 158행은 6개 언어가 다 채워져 있어 지금은 차이가 없다.
- Next `16.4.0 → 16.4.3`(wp3 — 보안 경고로 빌드가 멈춰 올림). SPEC 은 「Next.js 16」만 정해서 위반이 아니다. 원형 `procedure/front` 도 같은 경고 대상이다(이 작업 범위 밖).
- `STT_CONFIG_CHECK_SEC` 는 env 가 아니라 코드 상수다(`session.py:31` · SPEC §2.4 에 env 가 없음). §9.3 ⑦ 결과로 값을 바꿀 때 코드를 고친다.
- `back/tests/__pycache__` · `.pytest_cache` · `front/.env.local`(워커가 만든 개발값)이 워크트리에 있다. 모두 gitignore 대상이라 커밋에는 들어가지 않는다.
- 이 리뷰는 시험 · 빌드를 다시 돌리지 않았다. 수치는 워커 리포트 인용이다: back 123 passed · ruff 통과(wp2) / front tsc · lint · build 통과 · vitest 15 · 클래스 78 중 없는 것 0(wp4).
