# WORK-001 WP6-BE 결과 보고

## 상태: done

부분 검증 통과(ruff 0 · pytest 168 passed) · 실물 ⑧ ~ ⑪ 전부 실행(pending 없음). 커밋 없음(워크트리에 그대로).
실물 결과 JSON: `orchestration/work/interpret-pwa-poc/live-check-wp6-2026-10-26.json` (키 · 토큰 0 — 대조 확인)

## 수행 — 파일·모듈 목록

| 파일 | 무엇 |
|---|---|
| `back/app/service/glossary.py` | ① D-18 `build_context` 역방향 짝(정방향 뒤 · 같은 행 · 같은 순서 · `yue` source `t2s` · 역방향 source 중복은 처음 짝) · 줄이기 `terms` 뒤부터 → 역방향 뒤부터 · 정방향 · `general` 유지 · `report` 로 뺀 수 · `split_translation_terms` · `forward_only` · `is_forward_only` · `describe`(로그 칸 수). `without_terms` 삭제 ③ WARN-1 어떤 예외든 빈 용어집(이유 = 예외 종류 이름 · 주소 값 0) ④ WARN-6 `asyncio.wait_for(…, 10)` 전체 시간 · 「shape」는 JSON 파싱 단계에만 붙인다 |
| `back/app/service/interpret/session.py` | `invalid_request` 재연결 = `forward_only`(정방향만) · 처음부터 정방향만이면 재연결 없음 · STT 열 때 로그 `terms · forward · reverse · chars` · ② TTS 직전 `strip_parens` · 비면 TTS 안 보냄(`audio_start` 없음) |
| `back/app/service/interpret/assembler.py` | ② `strip_parens()` 순수 함수(반각 · 전각 · 섞은 짝 · 겹침은 바깥 짝 · 앞 공백 하나 · 짝 없는 괄호 그대로 · 그 밖 괄호 안 건드림) |
| `back/app/service/auth.py` | ⑤ WARN-2 망가진 토큰(ASCII 아님 · 점 개수 ≠ 1 · base64 · UTF-8 · JSON 모양) → 같은 401 · 서명 비교 bytes · ⑥ `missing_login_envs()` |
| `back/app/main.py` | ⑥ WARN-5 기동 때 빈 로그인 env 경고 1줄(이름만) · 응답은 그대로 |
| `back/app/container.py` | `context_for` 정보 로그 1줄(언어 · terms · 정방향 · 역방향 · 뺀 terms · 뺀 역방향 · 글자 수 — 용어 문자열 0) |
| `back/app/config.py` | `glossary_context_max_chars` 기본값 **10000 → 18832**(⑧ 실측) |
| `.env.example` | 값은 그대로 비움(이름만) · 주석의 기본값만 `(18832 …)` 로 |
| `back/scripts/live_check.py` | ⑧ `limit` · `ceiling` · ⑧ 재확인 `default` · ⑨ `reverse` · ⑩ `parentts` · ⑪ `badurl` · 묶음 `wp6` · `--max-chars` |
| `back/tests/test_context.py` · `test_glossary.py` · `test_auth.py` · `test_interpret.py` | 아래 「검증」 |

`docker-compose.yml` 은 고칠 것이 없어 손대지 않았다.

## 검증 — 명령과 수치

`cd back && uv run ruff check . && uv run pytest -q tests/test_context.py tests/test_glossary.py tests/test_auth.py tests/test_interpret.py`
→ **All checks passed · 168 passed**

추가한 시험(§9.1 0.3.0 항목):
- 로그인: 망가진 토큰 9종 → `Unauthorized`(500 0) · HTTP 헤더 3종 → 401 + CORS 헤더 · WS `?token=` 3종 → 1008 · 로그인 env 빈 채 기동 3경우 → 경고 1줄(이름만 · 값 0) · 응답 같은 401 · env 다 있으면 경고 없음
- 용어집: URL 모양 오류(`InvalidURL` · 빈 호스트 `ValueError`) · 그 밖 예외(`RuntimeError`) → 빈 용어집으로 기동 · 경고에 주소 · 예외 문구 0 · 조금씩 흘려 보내는 응답이 전체 한도를 넘으면 `timeout`(한도 안이면 읽힘)
- context: 역방향이 정방향 뒤 같은 순서 · 역방향 source 중복 처음 짝 · 괄호 그대로(양방향) · `yue` 정방향 target · 역방향 source 간체 · `terms` 뒤부터 → 역방향 뒤부터 · 정방향 · `general` 안 줄어듦 · `forward_only` · §4.4.1 가짜 Soniox ① 정방향만 2번째 연결 → `ready` ⑥ 처음부터 정방향만 → 재연결 없이 `soniox_unavailable` · `terms` 만 빠지고 역방향 남음 → 정방향만 재연결 · 로그 칸 수
- 통역: `strip_parens` 13경우 · ja · en · yue(간체 TTS · 번체 자막) TTS 입력만 괄호 없음 · caption 괄호 그대로 · 괄호뿐이면 `audio_start` · 오디오 0

### 실물 ⑧ — 한도 실측 (용어집 `2026-07-01-reviewed-v5` · 158행)

역방향 포함 **전체** context 는 6개 언어 모두 그대로 통과했다(줄이기 0 · 첫 메시지 0.22 ~ 0.25초). 그래서 실제 한도를 찾으려고 같은 언어 짝을 덧붙여 크기를 늘리며 이분 탐색했다(덧붙인 짝은 중복 — 중복만으로는 거절되지 않음을 따로 확인: 1,928자 중복 context 통과).

| lang | 역방향 포함 전체 | 통과 최대치 | 거절 최소치 | error_type |
|---|---|---|---|---|
| en | 16,689 | 25,922 | 26,009 | invalid_request |
| ja | 16,136 | **20,925 (가장 작음)** | 21,014 | invalid_request |
| zh | 15,265 | 21,643 | 21,729 | invalid_request |
| th | 17,952 | 22,566 | 22,611 | invalid_request |
| vi | 17,366 | 24,778 | 24,902 | invalid_request |
| yue | 15,123 | 22,643 | 22,740 | invalid_request |

- 거절은 모두 오디오 없이 0.41 ~ 0.45초(2초 창 안).
- **기본값 = 20,925 × 0.9 = 18,832**(내림) → `config.py`.
- 그 값으로 6개 언어 다시 연결: **거절 0 · 뺀 terms 0 · 뺀 역방향 0**(정방향 157 · 역방향 en 155 · ja 156 · zh 155 · th 156 · vi 157 · yue 155 — 줄어든 것은 역방향 source 중복뿐).

### 실물 ⑨ — 역방향 적중 (기본값 18,832 · 용어 3개씩 · 2회 실행)

| lang | 외국어 발화 → 한국어(D-18 전) | 1회 | 2회 | 한국어 발화 → 외국어(① ②) | 1회 | 2회 |
|---|---|---|---|---|---|---|
| en | 1/3 | **2/3** | **2/3** | 3/3 | 2/3 | 2/3 |
| zh | 2/3 | **3/3** | 2/3 | 3/3 | 3/3 | 3/3 |
| ja | 1/3 | **3/3** | **3/3** | 2/3 | 1/3 | 0/3 |

- 역방향: 6번 중 5번이 D-18 전보다 높고 1번(zh 2회)은 같다. 줄이기로 빠진 역방향 짝은 없다(용어 9개 모두 context 안에 있음). 남은 오답: en 「쥬베덤」(쥬비덤) · zh 2회 「신珍珠」.
- 정방향: en · ja 가 ① ② 보다 낮다. 원인은 둘이다. ⓐ **한국어 STT 가 「신펄」을 「Syn펄」 · 「シン펄」으로 반쯤만 전사**한다(en · ja 4번 모두). ⓑ ja 「필러」는 번역에 「フィラー」로 바르게 나왔지만, 대조 대상이 괄호까지 든 「フィラー（ヒアルロン酸）」라 글자 대조가 빗나갔다(② 의 「シンパール（Synpurl）」 때와 같은 대조 방식 한계). ja 2회 「ジュビダム」(ジュビダーム)는 진짜로 틀린 것이다. 판정은 코디 · 사용자.

### 실물 ⑩ — TTS 괄호 제거 (ja · ⑤ 와 같은 문장)

- caption 번역: 「…チャウム（補充）と、フィラー（ヒアルロン酸）も…」 — 괄호 그대로(1건)
- TTS 입력: 「…チャウムと、フィラーも…」 — **괄호 0**
- `audio_start` 1 · 417,792 B 수신 · 오류 0

### 실물 ⑪ — URL 모양부터 틀린 주소로 기동

- 앱 lifespan 기동 성공 · 경고 `glossary load failed: InvalidURL` 1줄(주소 값 0) · `/api/health` `loaded=false` · context 비움 · 통역 `ready` · 확정 발화 1 · 오류 0

## 계약 대조 — SPEC 항목별 같음/다름

| SPEC | 판정 | 비고 |
|---|---|---|
| §3.1 로그인 env 빈 채 기동 경고(WARN-5) | 같음 | 이름만 · 응답 같은 401 · 잠금 규칙 그대로 |
| §3.2 망가진 토큰 401 · bytes 비교(WARN-2) | 같음 | HTTP 는 오류 처리기를 거쳐 CORS 헤더 포함 · WS 1008 |
| §4.2 어떤 예외든 빈 용어집(WARN-1) · 10초 전체 시간(WARN-6) | 같음 | 이유 = 예외 종류 이름 |
| §4.3 역방향 짝 규칙 | 같음 | 크기가 §4.3 실물 수치와 같다(en 16,689 … yue 15,123) |
| §4.4 줄이기 순서 · 4번 정방향만 재연결 · 5번 로그 | 같음 | 로그는 두 줄 — `glossary context`(조립 · 뺀 수 포함) · `stt context`(실제로 연 설정 · 재연결 때도) |
| §4.4 기본값 「역방향 포함 통과 최대치 − 10%」 | **해석 확인 필요** | 역방향 포함 전체가 6개 언어 모두 통과해 「전체 크기」로는 최대치를 정할 수 없었다. 같은 언어 짝을 덧붙여 실제 한도(가장 작은 ja 20,925)를 찾고 그 −10% 인 18,832 를 썼다. 문구 그대로 「통과한 최대 크기 중 가장 작은 값」을 쓰면 15,123 × 0.9 = **13,610** 이 되는데, 이 값으로는 거절 없이 통과하는 en · ja · zh · th · vi 에서 `terms` · 역방향을 일부러 빼게 된다 |
| §4.4.1 ⑥ 처음부터 정방향만이면 재연결 없음 | 같음 | 판정은 `is_forward_only`(terms 0 · 역방향 0). 빈 context 도 재연결 없음 |
| §4.5 `build_context` · `forward_only` 순수 함수 | 같음 | 정방향 · 역방향 경계는 「앞 정방향 짝의 거울인 첫 짝」으로 찾는다(정방향은 줄지 않아 늘 앞에 있다) |
| §5.7 TTS 입력 괄호 제거 | 같음 | `_tts_worker` 한 곳 · caption 그대로 · 비면 TTS 안 보냄 |
| §2.4 `.env.example` 이름만 | 같음 | 값은 비워 두고 주석의 기본값만 18832 로. 브리프 「코드 · `.env.example` 에 반영」과 WORK 「`.env.example` 은 이름만」을 둘 다 이렇게 맞췄다 |

## 이슈 · 코디가 확인할 것

1. **기본값 해석(위 표)** — 18,832(실제 한도 기준 · 줄이기 0)를 썼다. planner 가 SPEC §2.4 · §4.4 를 적을 때 「통과 최대치 = 같은 언어 짝을 덧붙여 찾은 실제 한도」라고 함께 적어야 한다. 13,610 이 맞다고 보면 `config.py` 한 줄과 `.env.example` 주석만 바꾸면 된다.
2. 실제 한도 사이 여유: 가장 큰 전체 context 는 th 17,952 이고, 기본값 18,832 까지 880자 남는다. 용어집에 행이 더 늘면 th 부터 `terms` 가 줄기 시작한다.
3. ⑨ 정방향 en · ja 하락은 대부분 한국어 STT 의 「신펄」 반쪽 전사와 괄호 표기 대조 한계에서 온다. 역방향(D-18)을 넣어서 생긴 회귀로 보기 어렵지만, 1회 · 2회 표본뿐이다. 로컬 E2E(§9.4) 때 사람 목소리로 다시 보기를 권한다.
4. 실물 스크립트는 포트를 쓰지 않는다(프로세스 안 실행) — 띄운 서버 없음 · 사용자 포트 손대지 않음.
