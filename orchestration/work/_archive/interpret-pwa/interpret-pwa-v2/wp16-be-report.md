# WP16 backend 결과 보고 — 시드 `.6` · 통역 기록(D-39 ~ D-41)

## 상태: done

워크트리 `interpret-pwa-v2`(base main 2a9d5a5) · 커밋 · push 안 함 · SPEC-001 0.6.0 · WORK WP16 행 · 처분(`research-dispositions.md` · OQ-018 포함)

## 수행 — 파일 · 모듈

| 파일 | 무엇 |
|---|---|
| `back/seed/glossary.json` | `2026-10-27.5` → **`2026-10-27.6`** · 157 → **170 term**(`kr-001` ~ `kr-013` 배열 맨 뒤) · §4.2.3 A(zh 30 entry) · B(th 2) · C(yue 1 · vi 3) · ph-130 zh-Hant `熱瑪吉` 지움 · OQ-018 처분 ① ② ③(5 entry) · `白毒` 뒤 U+200C 지움 |
| `back/app/service/glossary.py` | 검사 7 `invisible_char` — `ko` · `ko_aliases` · `name` · `aliases` 에 유니코드 범주 `Cf` 0 |
| `back/app/service/records.py`(새) | §5.9 — `open_records`(끔/켬 · mkdir · 쓰기 확인 · 실패면 경고 뒤 끔 · 기동 삭제 1회) · `Recorder`(날짜별 JSONL · KST · 7일 삭제 · 24시간 배경) · `SessionRecord`(start · utterance · end · 같은 id 1번 · 빈 caption 안 씀 · 쓰기 실패 경고 세션당 1) · `hit_terms`(정규화 t2s+casefold · 라틴 경계 · 공백 무시 · 더 긴 일치) |
| `back/app/service/interpret/session.py` | `recorder` 인자 — start 뒤(Soniox 전) `session_start` · `_emit` 의 final caption 마다 `utterance` · `_cleanup` 에서 `session_end`(error 코드 → `error` · stop → `stop` · 그 밖 `close`). 세션 중 `bad_request`(알 수 없는 프레임)는 끝 사유로 치지 않음 |
| `back/app/{config,container,main}.py` · `api/interpret.py` | `INTERPRET_RECORD_DIR`(기본 빈 값 = 끔) · lifespan: 시드 → `open_records` → 24시간 삭제 작업(종료 때 취소) · WS 가 기록기를 세션에 넘김. **새 경로 0** |
| `back/tests/seed_tables.py`(새) · `test_seed.py` · `test_records.py`(새) | §4.2.2 · §4.2.3 표 상수 대조 · 모호어 · 검사 7 · 기록 ① ~ ⑩ |
| `back/scripts/live_check.py` | `newterms`(⑳ + TTS wav 저장) · `records`(㉑) 추가 · 결과 JSON 머리 키 `seed` → `seed_file`(⑲ 결과 `seed` 와 겹쳐 덮이던 것) |
| `.env.example` · `docker-compose.yml` · `back/Dockerfile` | `INTERPRET_RECORD_DIR=`(이름만 · 주석) · back 에 이름 볼륨 `interpret-records:/data`(레포 밖 · 켜려면 `.env` 에 `/data/records`) · 이미지에 `/data`(소유 10001 — 이름 볼륨이 소유자를 물려받게) |

`test_api_surface.py` 는 고치지 않았다(변경 없이 통과).

## 검증

| 명령 | 결과 |
|---|---|
| `cd back && uv run ruff check .` | All checks passed |
| `uv run pytest -q`(전체) | **291 passed** (이전 257 + 기록 34 · 시드 시험 갱신) |
| `uv run pytest -q tests/test_seed.py tests/test_records.py tests/test_api_surface.py tests/test_interpret.py tests/test_context.py` | 215 passed |
| `test_records.py` 3회 반복 | 34 passed × 3(흔들림 없음) |
| 실제 uvicorn(임시 포트 18931 · 기록 폴더 scratchpad) | `glossary seed loaded: version=2026-10-27.6 terms=170 entries=en:170 … yue:170` · `interpret records: on dir=… keep_days=7` · `sweep: deleted=1`(10-19 지움 · 10-21 · keep.txt 남음) |

### 실물 ⑲ — `live-check-wp16-seed.json`(기본값 20,251 · 거절 0)

| lang | 글자 | terms | 정방향 기본/별칭 | 역방향 기본/별칭 | 뺀 수 | 거절 |
|---|---|---|---|---|---|---|
| en | 17,641 | 171 | 170 / 1 | 168 / 4 | 0 | 0 |
| ja | 19,457 | 171 | 170 / 1 | 169 / 75 | 0 | 0 |
| zh | 18,611 | 171 | 170 / 1 | 163 / 76 | 0 | 0 |
| **zh-Hant** | 20,241 | **0** | 170 / 1 | 157 / **169** | **terms 171 · 역방향 별칭 68** | 0 |
| th | 20,241 | 114 | 170 / 1 | 169 / 65 | terms 57 | 0 |
| vi | 17,648 | 171 | 170 / 1 | 170 / 0 | 0 | 0 |
| yue | 17,682 | 171 | 170 / 1 | 167 / 44 | 0 | 0 |

→ **통과**(§4.6 0.6.0 판정: 거절 0 · 정방향 기본/별칭 뺀 수 0). 단 zh-Hant 는 줄이기 **2단계(역방향 별칭)가 시작**됐다 — 아래 이슈 1.

### 실물 ⑳ — `live-check-wp16-newterms.json`(한국어 합성 음성 3문장 × 3언어)

| lang | 적중/시도 | 메모 |
|---|---|---|
| zh-Hant | **1/7** | ① 「써마지 CPT」 → **`鳳凰電波`**(ph-130 FLX 이름) · 소프웨이브 ✓ ② 프로파일로 → 「這個檔案」(STT 가 「프로파일」로 들음) · 뉴라미스 → 「優美思」(시드 優美施와 한 글자 다름) ③ `Exion` · `density` · `Mfase` 영문 그대로 |
| ja | 3/7 | 「サーマジCPT」 · 「プロファイル」 · 「デンソティ」 · 「エンペイス」 로 빗나감 · ソフウェーブ · ニューラミス · エクシオン ✓ |
| en | 6/7 | 「Thermage CPT」 · 「Sofwave」 · 「Neuramis」 · 「Exion, DENSITY, and EMFACE」 ✓ · 프로파일로 → 「right profile」 |

- 오류 0 · TTS 입력 괄호 0 · TTS 입력 문자열은 JSON `tts_inputs` 에.
- 적중은 판정 기준이 아니다(SPEC) — 기록만. 프로파일로는 3개 언어 모두 STT 단계에서 「프로파일」로 들렸다(번역 전).
- **TTS 소리 파일**(OQ-019 — 코디가 들을 것): `orchestration/work/interpret-pwa-v2/tts-samples/` — `EXION|DENSITY|EMFACE` × `en|zh|th|vi` 12개(단어만 · 24 kHz mono wav) + `session-en-sentence3.wav`(통역 세션 en 문장 ③ TTS 그대로). 길이는 en 0.77 ~ 0.94초 · **`EMFACE-zh` 2.39초**(다른 것보다 확연히 김 — 글자 읽기일 수 있음). 글자 읽기 / 낱말 읽기 판정은 내가 듣지 못해 **코디가 한 줄로 기록**해 주세요.

### 실물 ㉑ — `live-check-wp16-records.json`(⑳ 9세션을 기록 켠 채로 · 폴더 = scratchpad · 레포 밖)

- 오늘 파일 1개(`2026-10-27.jsonl`) · 27줄 = 9 세션 × start · utterance · end · 모두 `reason=stop`
- `terms` 에 걸린 `kr-`: kr-001 · 002 · 003 · 004 · 005 · 007 · 008(⑳ 번역에 실제 나온 것과 일치)
- 파일 grep: 키 · `Bearer` · `token` · IP 꼴 · `http` **0**
- **권한 뺀 폴더 1회**(켬으로 뜬 뒤 폴더 0500): 통역 끝까지(final 1 · audio_start 1 · error 0) · 경고 1줄 `interpret record write failed: PermissionError` · 파일 0
- 문장이 든 기록 파일은 보고 · 레포에 붙이지 않았다(scratchpad 에만).

## 계약 대조

| SPEC | 같음/다름 |
|---|---|
| §4.2 검사 7 `invisible_char`(Cf) · 가짜 시드 U+200C → `invisible_char` | 같음(+ U+200B · U+2060 · U+FEFF · ko · ko_aliases 시험) |
| §4.2.2 13 term × 7 언어 표(name · aliases 순서 · reviewed · source · note) | 같음 — 시험이 표 상수와 대조 |
| §4.2.3 A · B · C | 같음 — C 는 `manual` · 옛 값 지움 · `raw` 그대로 |
| §4.2.1 모호어 목록 금지 자리 0 | 같음(시험 · 가짜 시드로 잡히는지도 확인) |
| §4.2.2 순서 · 기존 157 id 순서 | 같음 |
| §5.9 폴더 · 기동 로그 · 날짜(KST) · 줄 모양 · 키 순서 · 언제 쓰나 · 판정 · 넣지 않는 것 · 7일 삭제 · 쓰기 실패 · 화면 · API 없음 | 같음 |
| §2.4 `.env.example` 이름만 | 같음 |
| §9.1 「시드」 ⑥ · 「기록」 ① ~ ⑩ | 같음 |
| §9.3 ⑲ ⑳ ㉑ | ⑲ 통과 · ⑳ 기록 · ㉑ 통과 |

**SPEC 에 없어 내가 정한 것(확인 부탁)**

1. **note URL 고르기**: 리포트 칸의 첫 URL(열람 표시 우선) · 스킴 없는 것은 `https://` 를 붙였고 · 대만 약어 `T:` = `https://tresure-clinic.com` · `K:` = koreabeautydream · 리포트가 `…` 로 줄인 URL 은 그대로 옮김(kr-003 ja · kr-004 en · kr-006 en · kr-008 zh-Hant). **kr-013 en** 은 첫 URL 이 제조사(iskramedical)라 「현지 출처 1개 = 그 URL」 규칙대로 클리닉 체인 기사(graziamagazine · 열람)로 적었다.
2. **zh 의 영문 칸 note**: r1 이 「현지에 없음 — 영문」으로 적은 kr-003 · 004 · 007 · 008 · 009 · 013 은 출처 수(0 ~ 2 · 비현지 · 접수만)와 관계없이 `현지 출처 없음 — research-r1-zh-report.md`. kr-006 · kr-012(중문명 있음 · 출처 1)은 URL.
3. **OQ-018 처분의 source**: ① ph-123 · ph-126 zh(`Oligio` · `Shurink Universe` · aliases `[]`) · ③ ph-113 zh · th(`Juvelook Volume` · 옛 값 alias) = `manual` · `reviewed:false` · note 에 처분 번호. ② ph-121 yue `美版超聲刀`(alias `Ultherapy` · `超聲刀` 지움) = `web-research 2026-10-27` · note `https://margo.hk`(r3 표 B-2) · `reviewed:false`(리포트 문자열이 「美版超聲刀二代」 · 「美國超聲刀2代」 라 name 과 글자 그대로 같은 출처는 0).
4. ph-042 zh `raw` 의 U+200C 는 「`raw` 는 그대로」 대로 남겼다(검사 7 대상 밖).
5. compose: 기록은 기본 끔 그대로(이름 볼륨만 붙임) — `.env` 에 `INTERPRET_RECORD_DIR=/data/records` 를 넣어야 켜진다. 이미지에 `/data`(10001 소유)를 만들었다(이름 볼륨 첫 마운트가 root 소유가 되지 않게 · k8s 는 fsGroup 이라 무관).

## 이슈 · 코디가 확인할 것

1. **zh-Hant 줄이기 2단계 시작**(⑲) — `terms` 171 전부 + **역방향 별칭 68개**가 빠진다(20,241자). 정방향은 그대로라 §4.6 판정은 통과지만, 대만 현지 별칭(예 `CPT黃金電波` · 대만 2차 별칭 등 뒤쪽 68개)이 역방향에서 빠졌다. 한도 재측정(⑬ 방법 · zh-Hant 통과 최대치 22,842 기록)으로 기본값을 올릴지는 코디 · 사용자 몫 — 워커는 기본값을 바꾸지 않았다. th 도 `terms` 57 빠짐(1단계).
2. **「써마지 CPT」 → 대만어 `鳳凰電波`**(⑳ zh-Hant) — ko 별칭 「써마지」(ph-130 · OQ-018 ⑤ 그대로)의 정방향 짝 `써마지 → 鳳凰電波` 가 「써마지 CPT → 黃金電波」 보다 이긴 것으로 보인다(같은 문장 en 은 Thermage CPT 로 맞음). ja 도 「サーマジCPT」. CPT 를 FLX 로 통역하는 오역이라 OQ-018 ⑤ 재검토 권장.
3. **OQ-019 TTS** — `tts-samples/` 의 wav 13개를 들어 보고 글자 읽기 / 낱말 읽기 한 줄 기록. en 번역문은 `Exion`(대소문자 섞임) · `DENSITY` · `EMFACE` 로 나왔다.
4. 프로파일로 · 뉴라미스(zh-Hant 「優美思」) · 덴서티 · 엠페이스(ja) 미적중은 STT · 번역 쪽 — 시드 짝은 context 에 있다(정방향 뺀 수 0).
5. WORK 「열린 것」 OQ-018 줄은 「WP16 은 건드리지 않는다」 였지만 브리프 · 처분 파일이 ① ~ ⑤ 반영을 지시해 처분대로 반영했다 — WORK 문구 정리 필요.

---

## 처분 2 (코디 · 2026-10-27) — 결과

### 상태: done

| # | 처분 | 한 일 |
|---|---|---|
| ① | OQ-018 ⑤ 뒤집음 — ph-130 ko 별칭 「써마지」 지움 | `seed/glossary.json` ph-130 `ko_aliases: []` · term `note` 에 처분 기록(옛 근거 함께). 판 번호는 `.6` 그대로(같은 PR). 시험: `test_repo_seed_v6_changed_entries` 에 「ph-130 ko_aliases == []」 + **「어느 term 에도 ko 별칭 「써마지」 0」** · 기록 판정 시험은 「써마지 하실래요 → []」 · ko 별칭 판정은 가짜 시드로(실제 시드는 이제 ko 별칭 0개 → 7개 언어 모두 정방향 별칭 0) |
| ② | `.6` 으로 7개 언어 한도 재측정(⑬) | 아래 표 · **기본값 20,251 → 20,419**(`config.py` · `.env.example` 주석) |
| ③ | ⑳ zh-Hant · ja 다시 | 아래 표 · `live_check.py newterms --new-langs` 옵션 추가 |

### ② 한도 — `live-check-wp16-ceiling.json`

| lang | 줄이기 없는 전체 | 통과 최대치 | 거절 최소 | 방법 |
|---|---|---|---|---|
| en | 17,589 | 26,027 | 26,069 | ⑬ padding |
| **ja** | 19,408 | **22,688(가장 작음)** | 22,771 | ⑬ padding |
| zh | 18,565 | 23,259 | 23,347 | ⑬ padding |
| zh-Hant | **24,750 — 그대로는 거절**(`invalid_request`) | **24,099** | 24,142 | **줄이기 이분 탐색**(전체가 거절돼 padding 불가 · `build_context(max_chars=m)` 로 실제 보낼 모양을 잼 · 같은 파일 `trim_search`) |
| th | 20,804 | 23,715 | 23,833 | ⑬ padding |
| vi | 17,596 | 25,435 | 25,512 | ⑬ padding |
| yue | 17,636 | 23,471 | 23,557 | ⑬ padding |

- 22,688 × 0.9 = 20,419.2 → **20,419**(내림) > 20,251 → 올렸다.
- **20,419 로도 넘는 언어(수치만)** — `live-check-wp16-seed-2.json`(⑲ 다시 · 거절 0 · 정방향 뺀 수 0):
  - **zh-Hant**: 전체 24,750 → 보냄 20,401 · `terms` 170 전부 · **역방향 별칭 63**(20,251 때 68 → 63) 빠짐
  - **th**: 전체 20,804 → 보냄 20,416 · `terms` 38 빠짐(20,251 때 57)
  - 나머지 5개 언어 뺀 수 0
- 참고: zh-Hant 전체(24,750)는 실제로 거절되므로 줄이기가 필요하다. zh-Hant 만 기준으로 하면 24,099 × 0.9 = 21,689 지만 ja(22,688)가 더 작아 공통 기본값은 20,419.

### ③ ⑳ 다시 — `live-check-wp16-newterms-2.json`(기본값 20,419 · ko 별칭 「써마지」 없음)

| lang | 적중(전 → 후) | 「써마지 CPT」 |
|---|---|---|
| zh-Hant | 1/7 → **2/7** | **`鳳凰電波`(FLX · 오역) → `黃金電波`(kr-001 · 맞음)** · 기록 판정도 `kr-001` |
| ja | 3/7 → 4/7 | 「サーマジCPT」 그대로(시드 name `サーマクールCPT` 와 다름 — 번역이 음역 · ko 별칭과 무관) |

- zh-Hant 나머지 미적중: 프로파일로 → 「檔案」(STT 가 「프로파일」) · 뉴라미스 → 「優美思」 · `Exion` · `density` · `Memphis`(엠페이스) 영문.
- ja: プロファイル(같은 STT 문제) · デンソティ 미적중 · エムフェイス 는 이번엔 적중(합성 음성 · Soniox 비결정이라 한 번 차이는 의미 작음).
- 오류 0.

### 검증

- `uv run ruff check .` — All checks passed
- `uv run pytest -q` — **292 passed**(처분 1 회 291 + 가짜 시드 ko 별칭 판정 1)
- 결과 JSON 3개(ceiling · seed-2 · newterms-2)에 키 문자열 0(grep)

### 코디가 확인할 것

1. **SPEC 문구** — §2.4 · §4.6 의 기본값 20,251(근거 ja 22,502)을 20,419(ja 22,688 · `.6`)로 · OQ-018 ⑤ 줄 · §4.2.2 「써마지 단독은 OQ-018」 문구 · §9.1 시드 시험의 「써마지 ko 별칭」 줄 — planner 몫.
2. zh-Hant 는 20,419 에서도 역방향 별칭 63개가 빠진다(뒤쪽 = 새 시술 · 대만 2차 별칭). 더 살리려면 언어별 기본값이나 줄이기 순서 변경이 필요 — 계약 변경이라 손대지 않았다.
3. ja 「サーマジCPT」 는 시드 밖 음역 — ja alias 로 넣을지는 조사 · 처분 몫(R4 · R5 상 근거 없음).

---

## 처분 3 (코디 · 2026-10-27 · 마지막) — 언어별 줄이기 기준

### 상태: done

| 파일 | 한 일 |
|---|---|
| `back/app/service/interpret/langs.py` | **표 한 곳** `CONTEXT_MAX_CHARS` = en 23,424 · ja 20,419 · zh 20,933 · zh-Hant 21,689 · th 21,343 · vi 22,891 · yue 21,123(처분 2 통과 최대치 × 0.9 내림) + `context_max_chars(lang, override)` |
| `back/app/config.py` | `glossary_context_max_chars: int \| None = None` — **비면 언어별 표 · 값이 있으면 모든 언어를 그 값 하나로 덮어씀**(이전과 같은 env 하나 · 언어별 값보다 작든 크든 그 값) |
| `back/app/container.py` | `context_for` 가 `context_max_chars(lang, env)` 로 · 정보 로그 끝에 `max=<그 언어 기준>` |
| `back/scripts/live_check.py` | 같은 함수 사용(`--max-chars` 주면 덮어씀) · 결과 JSON `max_chars` = 언어별 표 |
| `back/tests/test_context.py` | 표 값 · 7개 언어 키 · env 없으면 언어마다 표 값으로 조립 · env `15000` 이면 7개 언어 모두 15000(레포 시드 · `build_context` 결과와 같은지) |
| `.env.example` | `GLOSSARY_CONTEXT_MAX_CHARS` 주석 — 비면 언어별 표 · 넣으면 모든 언어 하나로 |

### ⑲ 다시 — `live-check-wp16-seed-3.json`(env 없음 = 언어별 표 · 거절 0)

| lang | 기준 | 보낸 글자 | 뺀 수 | 거절 |
|---|---|---|---|---|
| en | 23,424 | 17,589 | 0 | 0 |
| ja | 20,419 | 19,408 | 0 | 0 |
| zh | 20,933 | 18,565 | 0 | 0 |
| **zh-Hant** | 21,689 | 21,658 | `terms` 170 · **역방향 별칭 33**(처분 2 의 63 → 33) | 0 |
| th | 21,343 | 20,804 | **0**(처분 2 의 `terms` 38 → 0) | 0 |
| vi | 22,891 | 17,596 | 0 | 0 |
| yue | 21,123 | 17,636 | 0 | 0 |

- 7개 언어 모두 정방향 기본 170 · 뺀 정방향 0 · **거절 0**.
- 남는 손실은 **zh-Hant 역방향 별칭 33개**(시드 맨 뒤 쪽 — 새 시술 · 대만 별칭)와 zh-Hant `terms` 전부. zh-Hant 전체(24,750)는 실제 한도(24,099)를 넘으므로 줄이기가 없으면 거절된다 — 더 줄일 수 없는 손실(별칭 정리나 줄이기 순서 변경은 시드 · 계약 몫).
- 사용자 `.env` 에 `GLOSSARY_CONTEXT_MAX_CHARS` 값 없음(확인) → 운영 ConfigMap · Secret 에도 없어야 언어별 표가 쓰인다(WP17 · 코디 확인).

### 검증

- `uv run ruff check .` — All checks passed
- `uv run pytest -q` — **295 passed**(처분 2 의 292 + 언어별 기준 시험 3)
- 결과 JSON 에 키 문자열 0

### 코디가 확인할 것

1. **SPEC §2.4 · §4.6** — 단일 기본값 20,251 → 언어별 표(이 절 수치) · env 는 모든 언어 덮어쓰기. planner 몫.
2. infra(WP17): ConfigMap · Secret 에 `GLOSSARY_CONTEXT_MAX_CHARS` 를 넣지 않는다(넣으면 언어별 표가 꺼진다).
