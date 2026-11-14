# WP21 backend 결과 보고 — 품질 개선 코드 · 품질 시험 스크립트 (SPEC-001 0.8.1)

## 상태: done (커밋 · push · PR 없음 — 워크트리 `interpreter-idea` 에 변경만)

## 수행 — 파일 · 모듈 목록

| 파일 | 무엇 |
|---|---|
| `back/app/service/interpret/soniox.py` | ① `STT_MODEL = "stt-rt-v6"` · 그 밖 STT 설정 키 · 값 그대로(`max_endpoint_delay_ms` 1000 → 상수 `MAX_ENDPOINT_DELAY_MS`) · `stt_config(…, *, model, endpoint_config)` 선택 인자(끊김 키 3개 밖은 `ValueError`) · `SonioxStt.open(…, **options)` |
| `back/app/service/glossary.py` | ② `CONTEXT_TEXT`(S1 ~ S4 · 424자 · json 429자 · 줄바꿈 3 — SPEC §4.5 블록과 글자 그대로 대조함) · `ContextParts.text` · `to_soniox` 키 순서 `general → text → terms → translation_terms`(text 비면 키 없음) · `context_size` 에 포함 · 줄이기 대상 아님 · `forward_only` 에 남김 · `is_forward_only` 그대로 · `describe` 에 `text` 글자 수 · `build_context(…, *, with_text=True, drop_reverse=())` 선택 인자 · `GENERAL` · `TRIM_ORDER` 무변경 |
| `back/app/service/interpret/assembler.py` | ③ `is_blank()` — 판정 함수 한 곳(`strip_parens` 옆 · 범주 L · N 0 이면 빈 원문) |
| `back/app/service/interpret/session.py` | ③ `_emit` 한 곳에서 막기(`_blank_filter`) · `final:false` 빈 원문 안 보냄 · 이미 나간 `id` 면 둘 다 빈 `final:true` 1번 · TTS 큐 전에 거름(`_tts_worker` 무변경) · 로그 1줄 `interpret blank original dropped: id · side · original=<n> · translation=<n>` · 선택 인자 `block_blank=True` · `stt_model=STT_MODEL` · `endpoint_config=None`(기본값이면 `open_stt` 에 아무것도 더 안 넘김) · 막은 수 `blank_dropped` · 로그에 `text=<n>` |
| `back/app/container.py` | 로그에 `text=<n>` 만(인자 넘기지 않음) |
| `back/tests/test_context.py` | 뜻이 바뀐 줄만 — `to_soniox` · `forward_only` 기대값에 `text` · `describe` 에 `text` (5곳) |
| `back/tests/test_quality.py`(새) | §9.1 「STT 설정」 · 「context `text`」 · 「빈 원문」 ① ~ ⑨ · 「기본값 = 켬」 |
| `back/tests/test_quality_script.py`(새) | 스크립트의 목록 · 규칙 읽기 · 규칙 4종 판정 · 조합 · 레포 밖 경로 · 결과 문장 대조 — 가짜 목록 · 규칙(시험 문장 0) |
| `back/scripts/quality_check.py`(새) | ⑤ 품질 시험 스크립트 — `audio` · `run` · `context`(㉒) · `calc` |

변경 없음: `back/seed/`(읽기만) · `langs.py`(`CONTEXT_MAX_CHARS`) · `config.py` · `api/interpret.py` · `live_check.py` · front · infra · `.env.example`.

### 스크립트(⑤) 요약
- 인자: `--list` · `--rules` · `--audio-dir` · `--out-repo` · `--out-local` — 목록 · 규칙 경로는 인자로만 · 음성 폴더 · 로컬 결과가 레포 안이면 거절.
- 음성: Soniox TTS(`tts-rt-v2` · Jiwoo · 16 kHz s16le) · 문장마다 `<T>.pcm` + `manifest.json`(sha256 · 길이 · 합성 언어 · 쉼 수) · 이미 있으면 다시 안 만듦(`--force` 만) · 3절 = 조각 따로 합성 + 무음 1.0초 · 말 없음 = 5초 무음(PCM 0 · 결과에 `silent_audio: zeros`) · 합성 언어 = 말할 문장의 언어(한→외 `ko` · 외→한 Soniox 코드 · zh-Hant · yue 는 간체로 `zh`).
- 재생: back `InterpretSession` 프로세스 안 · 실시간 40 ms(절대 시각 기준) · pause 안 보냄 · 무음 꼬리 최소 3초 · 발화 정리될 때까지 · 최대 15초 → stop · 문장마다 새 세션 · 세션 `lang` = 목록 「언어」.
- 조합: A(`stt-rt-v5` · 문안 뺌 · 막기 끔) · B(기본 모델 · 문안 뺌 · 막기 끔) · C(전부 기본) — **운영 함수의 선택 인자로만**(`build_context` with_text · drop_reverse / `InterpretSession` block_blank · stt_model · endpoint_config) · `--seed`(load_seed) · `--drop-reverse` · `--endpoint k=v` · `--model` · `--no-text` · `--no-block` · `--repeat` · `--only` · `--label`.
- 판정: 규칙 종류 넷(literal ① · regex ② · count ③ · none ④ — 그 밖은 오류) · 확정 발화마다 · zh 계열은 t2s 뒤 · 발화 수 · 막힌 빈 원문 수 · 번역 줄 수 · 조각 수(실제 − 기대) · 지연(마지막 소리 조각 보낸 때 → 마지막 확정 caption ms) · 걸린 term id(records.hit_terms).
- 결과: 레포용(번호 · 수치만 · 쓰기 전에 목록 문장 · 원문 · 번역 · 규칙 문구를 스스로 대조해 하나라도 있으면 안 씀) · 로컬용(원문 · 번역 포함).

## 검증 — 명령과 수치

| 명령 | 결과 |
|---|---|
| `cd back && uv run ruff check .` | All checks passed |
| `cd back && uv run pytest -q`(전체) | **407 passed**(기존 338 + 새 69) · 실패 0 · 경고 1(starlette httpx — 기존 · 무관) |
| `quality_check.py calc`(시드 `.6` · 키 없음) | 아래 표 — SPEC §4.6 추정과 같음 |
| **실물 ㉒** `quality_check.py context --combo C`(v6 · 문안 포함 · 시드 `.6`) | **7개 언어 거절 0** · 정방향 뺀 수 0 · 첫 메시지 = 오류 아님(키 `final_audio_proc_ms` · `tokens` · `total_audio_proc_ms` · 토큰 0) |
| 연기 시험 1회(지어낸 문장 3개 · 목록 문장 아님) `audio` → `run --combo C` · `run --combo A --only` | 둘 다 끝까지(exit 0 · 오류 0) · C: model v6 · text 424 · 막기 켬 / A: model v5 · text 0 · 막기 끔 · A 의 zh context 18,565자(= SPEC §4.6 「줄이기 없는 전체 `.6`」) |

### ㉒ — 언어별 수치(v6 · 문안 포함 · 시드 `2026-10-27.6`)

| lang | 기준 | 보낸 글자 | `text` | 전체(문안 포함) | 전체(문안 없음) | 여유(문안 포함) | 묶음별 뺀 수 | 문안 때문에 더 빠진 수 | 거절 |
|---|---|---|---|---|---|---|---|---|---|
| en | 23,424 | 18,028 | 424 | 18,028 | 17,589 | 5,396 | 0 | 0 | 0 |
| ja | 20,419 | 19,847 | 424 | 19,847 | 19,408 | 572 | 0 | 0 | 0 |
| zh | 20,933 | 19,004 | 424 | 19,004 | 18,565 | 1,929 | 0 | 0 | 0 |
| zh-Hant | 21,689 | 21,651 | 424 | 25,189 | 24,750 | 없음 | `terms` 170 · 역방향 별칭 44 | **역방향 별칭 +11**(33 → 44) | 0 |
| th | 21,343 | 21,243 | 424 | 21,243 | 20,804 | **100** | 0 | 0 | 0 |
| vi | 22,891 | 18,035 | 424 | 18,035 | 17,596 | 4,856 | 0 | 0 | 0 |
| yue | 21,123 | 18,075 | 424 | 18,075 | 17,636 | 3,048 | 0 | 0 | 0 |

- 문안 칸 = 429 + 10 = **439자**(7개 언어 모두 전체 차이 439).
- 완료 조건 대조: zh-Hant 뺀 수 = 추정(역방향 별칭 44 안팎) **같음** · th 여유 100 = 추정 **같음** · 정방향 뺀 수 0 · 거절 0 → OQ-028 멈춤 조건 해당 없음.

## 계약 대조 — SPEC 항목별

| SPEC | 같음 / 다름 |
|---|---|
| §5.10 모델 `stt-rt-v6` · 그 밖 키 · 값 0.7.0 그대로 · 끊김 새 키 · `enable_agent_text_input` 없음 | 같음(시험: 키 집합 · 값 · 순서) |
| §9.1 「`stt-rt-v5` 문자열은 스크립트 조합 A 인자 말고 0」 | 같음(시험: `app` · `tests` · `scripts` 검색 → `scripts/quality_check.py` 만) |
| §4.5 문안 S1 ~ S4 글자 그대로 · 424자 · 상수 한 곳 · 7개 언어 같은 문자열 | 같음 |
| §4.5 키 순서 · `forward_only` 에 text · `is_forward_only` 그대로 · entry 0 → context 없음 | 같음 |
| §4.6 text 줄이지 않음 · 크기에 포함(기준 − 439 와 묶음별 뺀 수 같음) | 같음(시험) |
| §4.5 `translation_terms` 짝 전부 시드에서 · 일반 낱말 짝 0 | 같음(레포 시드 7개 언어 시험) |
| §5.11 판정 · 동작 · 로그 · WS 모양 · 기록(막힌 발화 줄 없음 · `utterances` 안 셈) · pause · stop flush | 같음(시험 ① ~ ⑨) |
| §9.3 「조합을 바꾸는 길」 — 선택 인자만 · 기본 = 켬 · API 경로 · `config.py` · `.env.example` 에 이름 0 · WS `start` 키 무시 | 같음(시험 「기본값 = 켬」) |
| §9.3 입력 · 재생 · 판정 · 결과 | 같음 — 단 아래 이슈 1 · 2 |
| `GENERAL` · `TRIM_ORDER` · `CONTEXT_MAX_CHARS` · 시드 · front · infra | 무변경 |

## 이슈 · 코디가 확인할 것

1. **규칙 파일 형식은 스크립트가 정했다** — SPEC §9.3 은 종류 넷과 적을 칸만 정하고 파일 모양은 없다. JSON(`format: 1` · 문장마다 `expected_finals` + `rules[{no, kind: literal|regex|count|none, …}]`) — 스크립트 docstring 에 예시. WP22 ① 이 이 모양으로 쓴다. 손님 쪽(WP24)의 「뒤집은 꼴」 은 literal `negate: true` 로 받는다.
2. **3절 쉼 길이** — 조각을 따로 합성해 무음 1.0초로 이었다. TTS 조각 자체의 앞뒤 무음은 그대로라 실제 쉼은 1.0초보다 조금 길다(조각 앞뒤를 자르지 않음 — 결과 manifest 에 `pause_ms: 1000`).
3. **지연 정의** — 「마지막으로 소리 있는 조각(진폭 > 500)을 보낸 때 → 마지막 비지 않은 확정 caption」. 무음 꼬리는 최소 3초 · 최대 15초(`--tail-min` · `--tail-max`).
4. 레포용 결과에는 `drop_reverse` 의 source 문자열 대신 **개수 + `--label`** 만 남긴다(울쎄라 가르기는 `--label` 로 변형 이름을 적어 구분).
5. v6 는 설정 직후 오류 아닌 빈 `tokens` 메시지를 먼저 보낸다(토큰 0) — 세션의 설정 확인(§4.6.1)은 「오류 아님 = 통과」 라 동작 그대로 · 그 메시지는 중계돼도 caption 이 생기지 않는다.
6. 품질 시험 전체(WP22) · 규칙 파일 · 목록 문장 음성은 **이번에 돌리지 않았다**. 연기 시험은 지어낸 문장 3개(목록 문장 아님 · 결과 문장 보고 0) · 파일은 레포 밖 scratchpad.
7. 키는 사용자 `.env` 에서 프로세스 env 로만 넘김 — 워크트리에 복사 · 출력 · 로그 0.

---

# 수정 1 — 품질 시험 스크립트 판정 3건 · v6 거절 순서 측정 (코드 검수 W-1 ~ W-4)

## 상태: done (커밋 · push · PR 없음 · 운영 `app/` 무수정)

## 수행

| # | 파일 | 무엇 |
|---|---|---|
| W-1 | `back/scripts/quality_check.py` | `row_verdict()` — 실행이 `failed` 이거나 `errors`(세션 `error` 종료 포함)가 있으면 `machine = "error"` · `hit_rules = []`. `summarize()` 의 `machine` 집계 = pass · fail · none · **error** 따로 · `errors` = error 행 수 |
| W-2 | 같은 파일 | `check_rule_coverage()` — `--rules` 를 주면 목록(`--only` 뒤)의 T 번호 ⊆ 규칙 파일 번호. 빠지면 `규칙 파일에 없는 번호: T02, T03` 로 `SystemExit`(실행 전) |
| W-3 | 같은 파일 | `cmd_run` 이 **로컬 결과(레포 밖 확인 끝)를 먼저** 쓰고 그다음 레포용을 대조 · 씀. `guard_repo_json(repo dict, …)` 은 `repo_strings()` — **문자열 값만** 대조(키 제외 · 코드 값 키 `no` · `lang` · `direction` · `section` · `machine` · `kinds` · `combo` · `stt_model` · `seed_version` · `at` · `audio_sha256` · `silent_audio` · `errors` · `failed` · `terms`(term id) 제외). 대조가 멈추면 「레포용은 쓰지 않았어요(로컬 결과는 썼어요)」 |
| 참고 | 같은 파일 | 결과 머리 기본 끊김 값 `1000` 리터럴 → `MAX_ENDPOINT_DELAY_MS` 상수 |
| W-4 | 같은 파일 | `reject` 하위 명령(측정만) — `reject_trial()` 이 설정을 보낸 뒤 6초 동안 오는 메시지를 차례로(ms · 종류 · 토큰 수 · error_type — 값 0) 적는다. 3초까지 오류가 없으면 무음 오디오를 보낸다(오디오가 와야 거절하는지 보려고) |
| 시험 | `back/tests/test_quality_script.py` | 수정 1 · 새 5: W-1(`row_verdict` · `summarize` — 오류 행 error · 집계 밖) · W-2(빠진 번호 메시지) · W-3 ×2(`no` · `pass` · `zh` · term id 발화 헛걸림 없음 / 대조가 멈춰도 로컬 파일은 있고 레포 파일은 없음 · 정상 label 이면 둘 다) · `oversize_context` / 기존 대조 시험은 새 시그니처(dict)로 |

## 검증

| 명령 | 결과 |
|---|---|
| `cd back && uv run ruff check .` | All checks passed |
| `cd back && uv run pytest -q` | **412 passed**(앞 판 407 + 새 5) · 실패 0 · 경고 1(starlette httpx — 기존 · 무관) |
| 실물 W-4 `quality_check.py reject`(키 = 사용자 `.env` → 프로세스 env 만) | 아래 표 · 결과 JSON = scratchpad `w4-reject.json`(레포 밖 · 문장 0) |

### W-4 측정 — 거절이 오는 순서 · 시각 (zh-Hant · Soniox `zh` · 시드 `2026-10-27.6` · 문안 포함)

| 변형 | 모델 | 회 | 보낸 글자 | 거절 위치 | 거절까지(ms · 설정 보낸 뒤) | 2초 안 | 그 앞 메시지 |
|---|---|---|---|---|---|---|---|
| 줄이기 없음(전체) | `stt-rt-v6` | 1 · 2 · 3 | 25,189 | **첫 메시지** ×3 | 433 · 374 · 446 | 예 ×3 | 없음 |
| 부풀림(짝 되풀이) | `stt-rt-v6` | 1 · 2 · 3 | 48,021 | **첫 메시지** ×3 | 474 · 469 · 403 | 예 ×3 | 없음 |
| 줄이기 없음(전체) | `stt-rt-v5` | 1 | 25,189 | 첫 메시지 | 371 | 예 | 없음 |
| 부풀림 | `stt-rt-v5` | 1 | 48,021 | 첫 메시지 | 397 | 예 | 없음 |
| 대조 — 실제 보낼 모양 | `stt-rt-v6` | 1 | 21,651 | 거절 없음 | — | — | 빈 `tokens`(토큰 0) 228 ms → 오디오 뒤 빈 `tokens` 3,294 · 4,370 · 5,482 ms |

- 오류는 모두 `error_type = invalid_request` · 그 뒤 Soniox 가 닫음(close 1000).
- **판정: ①(첫 메시지로 온다)** — v6 도 v5 와 같이 거절을 첫 메시지로, 설정 뒤 0.37 ~ 0.47초에 보낸다(§4.6.1 의 2초 창 안). 받아들여진 설정은 첫 메시지가 빈 `tokens` 다. 따라서 지금 `_check_config`(첫 메시지 하나로 판정)는 v6 에서도 거절을 잡고, ㉒ 「거절 0」 은 「거절됐다면 첫 메시지가 오류였을 것」 으로 읽어도 된다. **`_check_config` 수정 · SPEC 개정 필요 없음**(②가 아니었다).
- 덤: zh-Hant 줄이기 없는 전체(문안 포함 25,189자)는 v6 에서도 거절 — v5 거절 최소치(24,142)와 같은 쪽. 줄이기(기준 21,689)가 v6 에서도 필요하다. 한도 재측정(⑬′)은 WP23.
- 부풀림 목표는 40,000자였지만 짝 묶음을 통째로 되풀이해 48,021자가 됐다(수치는 실제 보낸 길이).

## 계약 대조

- 운영 `app/` · 시드 · front · infra 무수정(`git status` — 이번 수정은 `back/scripts/quality_check.py` · `back/tests/test_quality_script.py` 만).
- 레포용 결과 「번호 · 수치만」(§9.3) — 대조 범위를 좁혔지만 문장이 들어갈 수 있는 자리(키 밖 · 코드 값 밖 문자열 — 지금은 `label` 뿐)는 그대로 막는다.

## 이슈 · 코디가 확인할 것

1. W-4 는 ① — 남은 할 일 없음. 검수 리포트의 「WP25 배포 때 zh-Hant 1회 연결 확인」 은 그대로 두는 편이 좋다(한도 여유 38자 · v6 한도는 WP23 에서 잰다).
2. 검수 「참고」 가운데 이번에 안 한 것: 정규식 ②의 pattern 은 `t2s` 하지 않음(규칙 파일 작성 때 「정규식은 간체로」 — WP22 ① 메모) · stop flush 로 확정된 행 구분 칸 · `OpenStt` 타입 · `_blocked` 잔여 id(운영 코드 — 이번 범위 밖).
