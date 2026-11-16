# WORK-001 WP9 결과 보고 — 우리 용어집 시드(D-33)

## 상태: done

base main `d0a91a7`(배포본) 위 · 커밋 없음 · `back/**` · `.env.example` 만. 워크트리의 `front/**` 변경은 frontend 워커 것이다.
실물 결과 JSON: `orchestration/work/interpret-pwa-poc/live-check-wp9-2026-10-27.json`(키 · 토큰 0 — 대조 확인)

## 수행 — 파일·모듈 목록

| 파일 | 무엇 |
|---|---|
| `back/seed/glossary.json` (새) | **첫 시드** — 가져오기 스크립트 1회 실행 결과 + 코디 처분 ③ 손 편집(아래) · `version` `2026-10-27.2` · 157 term |
| `back/scripts/import_glossary.py` (새) | §4.8 — `--url`(기본 stg matrix · 스크립트 상수) · `--from-file` · `--out` · `--date`(재현용) · 출력 파일이 있으면 안 쓰고 코드 2 · 같은 `ko` 행 합치기 · 괄호 분해 다섯 모양 · zh-Hant = 분해 뒤 zh 의 `s2twp` 초안(`draft-s2twp` · `reviewed:false`) · 결정적 출력 · 끝에 `validate_seed` 통과해야 씀 · 요약 출력 |
| `back/app/service/glossary.py` | 다시 씀 — `SeedError(rule, where, term_id)` · `validate_seed`(검사 1 ~ 5 · 로더 · 시험 · 스크립트 공용) · `load_seed` · `Glossary/Term/Entry` · `ContextParts{general, terms, forward, forward_alias, reverse, reverse_alias}` · `build_context` · `to_soniox` · 줄이기 넷 · `forward_only` · `is_forward_only` · `describe` · 메뉴 행. **삭제**: `load_glossary` · `parse_matrix` · `_fetch` · `LOAD_TIMEOUT` · `context_rows` · `split_translation_terms` |
| `back/app/service/interpret/langs.py` | `GLOSSARY_COLUMN` · `glossary_column` 삭제 · `SIMPLIFY_CONTEXT_LANGS = {yue, zh-Hant}` + `context_norm(lang)`(t2s) — 언어별 선택 한 곳 |
| `back/app/service/interpret/session.py` | context 를 `ContextParts` 로 받음 · Soniox 에는 `to_soniox` · 재연결 = 정방향 기본만 · 로그 칸 수 다섯 |
| `back/app/container.py` · `back/app/main.py` | lifespan 에서 `load_seed`(동기) · `SeedError` → 오류 로그 1줄 + 기동 실패 · 성공 로그 1줄 · `context_for` 정보 로그(묶음별 칸 수 · 뺀 수) · httpx 로거 설정 삭제 |
| `back/app/api/glossary.py` · `back/app/schemas/glossary.py` | 메뉴 `rows: [{id, category, ko, koAliases, term, aliases, reviewed}]` · `count` = 그 언어 행 수 · 런타임 `s2twp` 삭제 · health 는 시드 판 · term 수 |
| `back/app/config.py` | `glossary_matrix_url` · `DEFAULT_GLOSSARY_MATRIX_URL` 삭제 · `SEED_PATH = BACK_DIR/"seed"/"glossary.json"` · `glossary_context_max_chars` **18832 그대로**(⑬ 참고) |
| `back/Dockerfile` | `COPY seed ./seed`(`.dockerignore` 는 `seed/` 를 빼지 않음 — 확인) |
| `.env.example` | `GLOSSARY_MATRIX_URL` 줄 삭제 · 줄이기 기준 주석 문구만 |
| `back/scripts/live_check.py` | 시드 기반으로 다시 씀 — `seed`(⑫) · `ceiling`(⑬) · `thermage`(⑭ ⑮) · `zhhant` · `badseed`(⑯). matrix 시절 ① ~ ⑪ 단계는 뺐다(재료가 바뀌어 다시 돌릴 수 없음 · 결과는 기존 JSON 에) |
| `back/tests/conftest.py` · `test_seed.py`(새) · `test_import_glossary.py`(새) · `test_context.py` · `test_glossary.py` · `test_interpret.py` · `test_auth.py` | 가짜 matrix → 가짜 시드(`write_seed` 임시 파일) · 아래 |

### 첫 시드 — 가져오기 요약 (`uv run python scripts/import_glossary.py` 1회 · matrix `2026-07-01-reviewed-v5` · count 158)

| 항목 | 수 |
|---|---|
| term | **157**(합친 행 1 — `스킨보톡스` 두 행 → yue 「Skin Botox」가 처음 term 의 yue `aliases` 로) |
| entry | en 157 · ja 157 · zh 157 · **zh-Hant 157** · th 157 · vi 157 · yue 157 |
| 괄호 분해 | 괄호 없음 667 · 라틴(현지) 76 · 현지(라틴) 130 · 앞 = 안 15 · **그 밖 60** |
| `reviewed:false` | en 17 · ja 12 · zh 3 · th 2 · vi 23 · yue 3(= 「그 밖」 — SPEC §4.8 참고 수치와 **정확히 같음**) · zh-Hant 157(초안 전부) |

손 편집(코디 처분 ③ — 시드 PR 에 해당): term `ph-130` 써마지FLX `ko_aliases: ["써마지"]` · term `note` 「사용자 지적 2026-10-26 …」 · `version` `.1` → `.2`.

## 검증 — 명령과 수치

| 명령 | 결과 |
|---|---|
| `cd back && uv run ruff check .` | All checks passed |
| `uv run pytest -q tests/test_seed.py tests/test_context.py tests/test_glossary.py tests/test_import_glossary.py tests/test_interpret.py` (WORK 부분 검증) | **183 passed** |
| `uv run pytest -q` (전체 1회 확인) | 239 passed |
| `grep -rn "stg-procedure-hub\|GLOSSARY_MATRIX_URL\|glossary/matrix" back/app` | **0** (시험 `test_runtime_has_no_procedure_hub` 도 같은 것 + `httpx` 0 을 본다) |
| 레포 시드 검사(시험 ①) | 통과 · 파일 모양(indent 2 · 끝 줄바꿈)도 시험 |

새 · 바꾼 시험(§9.1):
- **시드**: 레포 실제 시드 통과 · 검사 위반 28경우 → `SeedError` 의 규칙 · 경로 · id 대조 · 파일 없음 / JSON 아님 · 다른 시술의 같은 현지명 허용 · 깨진 시드로 lifespan 실패 + 오류 로그 1줄 · 성공 로그 1줄 · 런타임에 matrix 없음
- **context**: 순서 넷 · `terms` 대표명 뒤 ko 별칭 · entry 없는 시술 빠짐 · 그 언어 entry 0 → `None` · 역방향 처음 짝(기본이 별칭보다 앞) · zh-Hant 는 zh-Hant entry(t2s — 사람이 고친 「美國熱瑪吉」 → 「美国热玛吉」) · yue t2s · zh 그대로 · 줄이기 순서 넷 단계별 · 정방향 기본 · general 안 줄어듦 · `forward_only` 구조로 · 가짜 Soniox 6건 + α(그대로 통과)
- **메뉴**: 7개 언어 · 필드 일곱 · 시드 원본 그대로(런타임 변환 없음) · `count` 언어별(6 · 5 · 4 …) · source/raw/note 안 냄 · health 시드 판
- **가져오기**: 분해 12경우 · 유효 시드 · 머리 · id 순서 · zh-Hant 초안 · 「激光 → 鐳射」 · 빈 칸 entry 없음 · 같은 ko 합치기 · 덮어쓰기 거부 · 결정적 · 요약

### 실물 ⑫ ~ ⑯

**⑫ 7개 언어 시드 context(기본값 18,832) — 거절 0**

| lang | 글자 수 | terms | 정방향 기본 · 별칭 | 역방향 기본 · 별칭 | 뺀 수 |
|---|---|---|---|---|---|
| en | 16,131 | 158 | 157 · 1 | 155 · 0 | 0 |
| ja | 17,360 | 158 | 157 · 1 | 156 · 56 | 0 |
| zh | 16,464 | 158 | 157 · 1 | 151 · 55 | 0 |
| zh-Hant | 16,464 | 158 | 157 · 1 | 151 · 55 | 0 |
| **th** | **18,828** | **113** | 157 · 1 | 156 · 60 | **`terms` 45**(나머지 0) |
| vi | 16,272 | 158 | 157 · 1 | 157 · 0 | 0 |
| yue | 16,090 | 158 | 157 · 1 | 154 · 36 | 0 |

th 의 전체 context 는 19,340자라 기본값을 넘는다 → 줄이기 1단계(`terms` 뒤에서부터 · ko 별칭 「써마지」가 먼저)로 45개가 빠지고 짝은 전부 남는다.

**⑬ 통과 최대치(짝을 덧붙여 이분 탐색 · 7개 언어 모두 잼)**

| lang | 전체 | 통과 최대치 | 거절 최소치 | error_type |
|---|---|---|---|---|
| en | 16,131 | 26,372 | 26,463 | invalid_request |
| ja | 17,360 | **22,502**(가장 작음) | 22,600 | invalid_request |
| zh | 16,464 | 22,953 | 23,027 | invalid_request |
| **zh-Hant** | 16,464 | **22,842** | 22,917 | invalid_request |
| th | 19,340 | 23,661 | 23,735 | invalid_request |
| vi | 16,272 | 25,843 | 25,950 | invalid_request |
| yue | 16,090 | 23,763 | 23,835 | invalid_request |

- **zh-Hant 22,842 > 20,925 → 처분 ⑤ 대로 기본값을 고치지 않았다(18832 그대로).**
- OQ-013: zh-Hant context(t2s 뒤) 와 zh context 는 짝 359개 중 **22개가 다르다** — s2twp 낱말 바꿈이 t2s 뒤에도 남은 것(예 「点阵镭射 → 프락셔널」 · 「皮秒镭射」 · 「奈米脂肪填充」 · 「特色专案」 — zh 는 激光 · 纳米 · 项目).

**⑭ 정방향 · ⑮ 역방향 — 써마지 · 울쎄라 (zh · zh-Hant · ja)** — 시드 짝은 세 언어 모두 context 안에 있음(정방향 기본 · 별칭 「써마지」 · 역방향 기본, 줄이기로 빠진 것 0)

| lang | ⑭ 「써마지FLX」 | ⑭ 「써마지」(별칭) | ⑭ 「울쎄라」 | TTS 입력 괄호 |
|---|---|---|---|---|
| zh | 美版热玛吉FLX ✓ | 美版热玛吉FLX ✓ | ✗ 「不饱和疗法」 | 0 |
| zh-Hant | 美版熱瑪吉FLX ✓(TTS 간체 美版热玛吉FLX) | ✓ | ✗ 「不飽和療法」 | 0 |
| ja | ✗ 「サーマジFLX」 | ✗ 「サーマジー」 | ウルセラ ✓ | 0 |

| lang | ⑮ 현지명 발화 | ⑮ 영문 상표명 발화 | ⑮ 구어(热玛吉 · 超声刀 / サーマクール · ウルセラ) |
|---|---|---|---|
| zh | 써마지FLX ✓ · 美版超声刀 → ✗ 「슈링크유니버스」 | 써마지 FLX ✓ · Ultherapy → ✗ 「all therapy」 | ✗ 「열마기(热玛吉)」 · ✗ 「슈링크유니버스」 |
| zh-Hant | 써마지FLX ✓ · ✗ 「슈링크」 | ✗ 「thermage FLX」 · ✗ 「O therapy」 | ✗ · ✗ 「초음파 절개」 |
| ja | 써마지FLX ✓ · 울쎄라 ✓ | 써마지FLX ✓ · Ultherapy → ✗ 「올리지오」 | ✗ 「써마쿨」 · 울쎄라 ✓ |

- 써마지 정방향은 zh · zh-Hant 에서 **현지명으로**(영문이 아니라 · D-33) 나왔고 ko 별칭 「써마지」도 통했다. TTS 입력은 현지명 · 괄호 0.
- 실패 원인 셋(판정은 코디 · 사용자):
  1. **시드 데이터 — 비슷한 현지명**: zh 「美版超声刀」(울쎄라) ↔ 「韩版超声刀」(슈링크유니버스) · 「美版热玛吉FLX」(써마지) ↔ 「韩版热玛吉」(올리지오). 구어 「超声刀」 · 「热玛吉」는 두 시술 어느 쪽인지 원래 모호하다 → 역방향이 다른 시술로 간다. 시드 PR 로 별칭(예 울쎄라 zh `aliases` 에 「超声刀」를 넣을지)을 사람이 정해야 한다(우리 코드가 별칭을 짓지 않는다).
  2. **한국어 STT**: 합성 음성 「울쎄라」가 zh · zh-Hant 세션에서 「不饱和疗法」로 번역됐다 — 한국어 전사부터 빗나간 것으로 보인다(ja 세션에서는 ウルセラ ✓).
  3. ja 「써마지FLX」 → 「サーマジFLX」(음역) — 시드 「サーマクールFLX」 짝이 context 에 있는데도 안 잡혔다.
- 표본: 문장 1개씩 · 합성 음성(Soniox TTS) — 사람 목소리 확인은 로컬 E2E 권장.

**zh-Hant 자막(D-28 · D-32 재확인)**: caption 「…美版熱瑪吉FLX的護理…」 번체(s2twp) · TTS 입력 간체 · TTS 언어 `zh` · 오류 0.

**⑯ 깨진 시드로 기동**
- uvicorn(임시 포트 · 실제 시드는 그대로 · 시드 사본의 id 중복): **종료 코드 3** · 0.32초 · 오류 1줄 `glossary seed invalid: id_duplicate at $.terms[1].id (id=ph-001) — 기동을 멈춘다` · 포트 안 열림
- **docker**: `back/` 임시 복사본의 시드를 깨서 `docker build` · `docker run` → **종료 코드 3** · 같은 오류 1줄. `docker compose up` 그대로가 아니라 back 이미지만 띄웠다(compose 는 front 빌드까지 돌고 레포 시드를 바꿔야 해서 — 같은 경로)
- 정상 시드 이미지: `docker run` → `/api/health` `{"ok":true,"glossary":{"loaded":true,"version":"2026-10-27.2","count":157}}` · 기동 로그 1줄 — Dockerfile 이 `seed/` 를 복사함 확인. 띄운 컨테이너 · 이미지는 지웠다

## 계약 대조 — SPEC-001 0.4.0

| SPEC | 판정 | 비고 |
|---|---|---|
| §4.2 위치 · 머리 · term · entry · 검사 1 ~ 5 · 한 함수 | 같음 | **더한 것 둘**: ① 알 수 없는 필드는 오류(`unknown_field` — `ko_alias` 같은 오타가 조용히 무시되지 않게) ② term 에 선택 필드 `note`(처분 ③ 의 출처 메모를 둘 자리 — entry 에만 `note` 가 있었다). planner 가 §4.2 표에 적어야 한다 |
| §4.3 기동 1회 · 성공 로그 1줄 | 같음 | `glossary seed loaded: version=… terms=… entries=en:157 …` |
| §4.4 깨지면 기동 실패 · 오류 1줄 · `loaded` 늘 true | 같음 | 그 언어 entry 0 → context 없이 연결(시험) |
| §4.5 재료 · 순서 넷 · 처음 짝 · zh-Hant entry · t2s · `ContextParts` · `to_soniox` | 같음 | `to_soniox` 는 `terms: []` 도 키를 둔다(0.3.0 과 같은 모양) |
| §4.6 줄이기 넷 · 정방향 기본만 재연결 · 로그 · 기본값 18832 | 같음 | ⑬ zh-Hant 22,842 → 바꾸지 않음 |
| §4.7 메뉴 필드 · count · 런타임 변환 삭제 · health | 같음 | |
| §4.8 가져오기 | 같음 | **더한 것**: `--date`(같은 입력 두 번 → 같은 바이트를 날짜와 무관하게 시험하려고) |
| §4.9 런타임 호출 제거 | 같음 | grep 0 · `httpx` 의존성은 그대로(시험 · 스크립트) |
| §5.5 `GLOSSARY_COLUMN` 삭제 | 같음 | |
| §2.4 `GLOSSARY_MATRIX_URL` 삭제 | 같음 | config · `.env.example` |

## 이슈 · 코디가 확인할 것

1. **th 는 기본값에서 이미 줄인다** — 시드 th 전체가 19,340자(> 18,832) → `terms` 45개(ko 대표명 뒤쪽 + 별칭 「써마지」)가 빠진다. 짝은 모두 남는다. 처분 ⑤ 는 「zh-Hant 가 더 작으면」이라 바꾸지 않았다. 시드 기준 7개 언어 통과 최대치 중 가장 작은 값은 ja 22,502 → ×0.9 = **20,251** 이고, 이 값이면 th 도 줄이기 0 이다. 기본값을 시드 실측으로 다시 정할지 코디 · planner 가 결정한다(바꾸면 `config.py` 한 줄 · `.env.example` 주석).
2. **⑮ 역방향 오답은 시드 데이터 쪽**(비슷한 현지명 美版/韩版) — 사용자 시드 PR 거리. 현지 별명(예 超声刀 · 热玛吉 단독)을 어느 시술의 별칭으로 둘지는 사람이 정해야 한다.
3. ko 표기에 괄호가 있는 term 이 있다(예 「피코초(Picosecond)」) — §4.2 의 괄호 금지는 entry `name` · `aliases` 에만 걸린다(ko 는 정방향 source · TTS 로 가지 않음). 그대로 뒀다.
4. 분해 「그 밖」 중 결과가 어색한 것이 있다(예 vi 「Exosome/(tăng tưởng phục hồi da)」 → 「Exosome/」) — 전부 `reviewed:false` 라 메뉴에 「검수 전」으로 보인다. 사람이 시드에서 고친다.
5. `live_check.py` 의 ① ~ ⑪(matrix 시절) 단계는 뺐다 — 시드로 바뀐 뒤 같은 재료로 재현할 수 없다. 결과는 `live-check-2026-10-26.json` · `live-check-wp6-2026-10-26.json` 에 남아 있다.
6. 시드는 아직 커밋되지 않았다(브리프 「커밋 금지」) — WORK 의 「첫 시드를 만들어 커밋」은 코디가 머지할 때.

## 추가 — 코디 처분(이슈 1 채택 · 2026-10-27)

- `GLOSSARY_CONTEXT_MAX_CHARS` 기본값 **18832 → 20251**(시드 실측 ⑬ 가장 작은 통과 최대치 ja 22,502 × 0.9 · 내림) — `back/app/config.py` 한 줄 · `.env.example` 주석. 이 값을 기대하는 시험은 없었다(수정 0).
- 레포 시드로 다시 조립: 7개 언어 모두 **뺀 수 0**(th 19,340자도 들어감 · 남는 여유는 th 기준 911자).
- `uv run ruff check .` 통과 · `uv run pytest -q` **239 passed**. 실물 재연결은 하지 않았다(⑬ 의 각 언어 통과 최대치가 20,251 보다 크다 — 가장 작은 ja 22,502).
- SPEC §2.4 · §4.6 기본값 갱신은 planner 몫.
