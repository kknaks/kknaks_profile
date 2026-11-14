# 리뷰 리포트 — interpret-pwa WP21 / code (2026-11-14)

- 대상: 워크트리 `interpreter-idea` · base `origin/main` `e0fbda8` · `git diff`(수정 6) + 새 파일 3(`back/scripts/quality_check.py` · `back/tests/test_quality.py` · `back/tests/test_quality_script.py`)
- SSOT: SPEC-001 **0.8.1**(코디 커밋 `b0892cbb` 의 파일로 대조) §4.5 · §4.6 · §5.10 · §5.11 · §9.1 · §9.3 「6차」 · WORK WP21 행 · D-43 · D-45 · D-47 · D-48 · D-49 · backend 보고 `wp21-be-report.md`
- 관문을 직접 1회 돌림: `cd back && uv run ruff check . && uv run pytest -q` → **All checks passed · 407 passed · 1 warning**(starlette httpx 폐기 예고 — 기존 · 이번 변경과 무관). 보고 수치(407)와 같음.
  - 역할 문서 `tools.md` 는 「시험 실행 금지」 지만 이번 브리프 §2-7 이 직접 1회를 지시해 브리프를 따랐다. 레포 파일은 고치지 않았다.

## 판정: **WARN**

운영 코드(v6 · 문안 · 빈 원문 막기 · 기본값 = 켬)는 SPEC 0.8.1 과 항목마다 **같음**이고 FAIL 은 없다. WARN 은 넷이다. 셋은 **품질 시험 스크립트의 판정 · 출력에서 조용히 통과하거나 결과를 잃는 자리**(W-1 ~ W-3, WP22 조합 A 를 돌리기 전에 고칠 것)이고, 하나는 **v6 의 첫 빈 메시지 때문에 설정 거절 확인(§4.6.1)과 ㉒ 의 「거절 0」 이 아직 증명되지 않았다는 것**(W-4)이다.

---

## FAIL

없음.

## WARN

### W-1 연결 실패 · 오류로 끝난 문장이 기계 판정 `pass` 로 셈된다
- `back/scripts/quality_check.py:534-539` — `run_one` 이 예외로 끝나면 `local = {"finals": []}` 인데도 `judge()` 를 그대로 부른다. `back/scripts/quality_check.py:238-242` 는 literal(①, 뒤집지 않은 꼴)에서 「확정 발화에 없음」 을 「안 걸림」 으로 본다. 그래서 **발화가 0 이면 ①·② 만 있는 문장은 `pass`** 가 된다. 세션이 `error`(soniox_unavailable)로 끝나 finals 가 0 인 경우도 같다(`client.errors()` 는 수치로만 남고 판정에는 들어가지 않는다).
- 재현(이 리뷰에서 직접): `q.judge({"expected_finals":1,"rules":[{"kind":"literal",…}]}, "zh", [], {"finals":0,"translations":0})["machine"] == "pass"`.
- 근거: SPEC §9.3 「판정」(규칙에 걸리면 FAIL · 비교 표는 절마다 기계 FAIL 수 / 기계 판정이 있는 문장 수) · ㉓ 「33문장 × 2조합이 **오류 없이** 끝남」. 오류로 끝난 문장이 `summary.machine.pass` 에 들어가면 A 의 FAIL 수가 실제보다 적게 나오고, 전후 비교(D-44)가 C 쪽에 불리하게 기운다. `summary.errors` 가 따로 있긴 하지만 `machine` 집계(`:549`)는 오류 행을 빼지 않는다.
- ③(발화 수) 규칙이 있는 문장은 `0 ≠ 기대` 로 걸려 드러난다. 다만 ③ 을 넣을지는 규칙 파일이 정하므로, 이것만으로는 막히지 않는다.
- 권고: `failed` 또는 `errors` 가 비지 않은 행은 `machine = None`(또는 `"error"`)으로 두고 pass · fail · none 집계에서 뺀다. 시험 1건을 더한다.

### W-2 규칙 파일에 없는 번호는 판정 없이 조용히 넘어간다
- `back/scripts/quality_check.py:195-214` 의 `load_rules` 는 각 항목의 모양만 검사한다. **목록의 모든 T 번호에 규칙이 있는지는 보지 않는다.** `:531` 에서 번호를 못 찾으면 `srules = None` → `judge` 가 `machine: None` · `expected_finals: None` · `fragments: None`(`:223-226` · `:543`)을 낸다. `summary.machine`(`:549`)은 pass · fail · none 만 세므로 그 문장은 **어느 칸에도 안 잡힌다.** 번호 오타(`T1` · `T 01`) 하나로 그 문장의 판정과 조각 수가 사라져도 오류가 나지 않는다.
- 근거: SPEC §9.3 「판정 — 발화 수」 「규칙 파일에 **문장마다** 기대 확정 발화 수를 적고(**33문장 전부**)」 · 「규칙 파일은 코디가 확인한 뒤 조합 A」(확인은 사람이 보는 것이라 번호 대조는 기계로 막는 편이 맞다).
- 권고: `--rules` 를 주면 `items` 의 번호 집합과 `rules["sentences"]` 의 키 집합이 같은지(적어도 `items ⊆ rules`) 확인하고, 다르면 `SystemExit`.

### W-3 레포용 결과 대조가 헛걸리면 로컬 결과까지 같이 잃는다
- `back/scripts/quality_check.py:555-562` — `guard_repo_json` 이 `SystemExit` 를 내면 **`--out-repo` 와 `--out-local` 둘 다 쓰지 않고** 끝난다(로컬 쓰기가 대조 뒤에 있다). 대조(`:492-506`)는 원문 · 번역 · 규칙 문구 가운데 **2글자 이상이면 무엇이든** JSON 전체에서 부분 문자열로 찾는다. 그래서 짧은 발화가 JSON 의 키 · 값과 우연히 겹치면 헛걸린다.
- 재현(이 리뷰에서 직접): 원문 `"no"` 인 확정 발화 하나로 `guard_repo_json('{"no": "T01", …}', …)` → 「1개 들어갈 뻔했어요 — 쓰지 않았어요」. 그 밖에 걸릴 수 있는 낱말: `"run"` · `"lang"` · `"pass"` · `"fail"` · `"none"` · `"zh"` · `"en"` · `"ja"` · `"label"` 같은 키 · 값과 같은 2 ~ 4글자. 반대로 한 글자 발화(예 중국어 「好」)는 대조에서 빠지지만, 레포 JSON 에는 문장을 넣는 필드가 없어 실제로 새는 곳은 없다.
- 영향: 대조는 **새지 않는 쪽으로 실패**하므로 계약(§9.3 「결과 — 레포에는 번호 · 수치만」)은 지킨다. 하지만 조합 A 는 **2026-12-15 전에만** 돌릴 수 있고(§9.3 · §5.10) 33문장 × 실시간 재생 + 꼬리 3 ~ 15초가 걸린다. 헛걸림 한 번에 사람 판정용 로컬 결과까지 사라지면 다시 돌려야 한다.
- 권고: 로컬 결과(레포 밖 · `outside_repo` 확인 끝)를 **먼저** 쓰고, 그다음 레포용을 대조해서 쓴다. 대조는 JSON 의 **문자열 값만**(키 제외, `terms` id · 코드 값 제외) 보게 좁힌다.

### W-4 v6 는 오류가 아닌 첫 메시지를 먼저 보낸다 — 설정 거절 확인(§4.6.1)과 ㉒ 「거절 0」 이 첫 메시지 하나에 기대고 있다
- `back/app/service/interpret/session.py:197-210` `_check_config` 는 **첫 메시지 하나만** 본다. 오류면 거절, 오류가 아니면 통과다. ㉒ 를 잰 `back/scripts/quality_check.py:594-621` `probe` 도 같은 방식이다.
- backend 보고 이슈 5: v6 는 설정 직후 **오류 아닌 빈 `tokens` 메시지**(`final_audio_proc_ms` · `tokens` · `total_audio_proc_ms`)를 먼저 보낸다. v5 에서 ⑬ 이 거절을 실제로 잡았으니 v5 는 거절을 첫 메시지로 보냈다. 하지만 **v6 가 한도 초과 설정을 거절할 때 오류를 첫 메시지로 보내는지, 빈 메시지 뒤에 보내는지는 아무도 재지 않았다.** ㉒ 는 7개 언어 모두 통과(거절 사례 0)라서 이 경로가 한 번도 돌지 않았다.
- 뒤에 보내는 쪽이라면 두 가지가 **조용히 통과**한다. ① ㉒ 의 `rejected: false` 가 실제 거절을 놓친다. ② 운영에서 `invalid_request` 가 `ready` 뒤에 와 §4.6 4번(정방향 기본만으로 1회 재연결)이 돌지 않고 `soniox_unavailable`(MSG_RELAY)로 끊긴다. 4.6.1 「`ready` 뒤 거절은 재연결 없음」 이 그대로 적용된다.
- 근거: SPEC §4.6.1(설정 뒤 `ready` 전 최대 2초 · `invalid_request` 만 재연결) · §5.10(「v6 는 v5 와 완전히 호환」 은 공식 문구이고 거절 메시지 순서는 확인한 적 없음) · §4.6 「이 표의 기준은 v5 로 잰 값 — v6 에서 다시 잰다(OQ-028)」.
- 가장 위험한 언어: zh-Hant(보낸 21,651자 · 기준 21,689 — 여유 38자 · v5 통과 최대치 24,099) · th(여유 100자).
- 권고(코드 수정이 아니라 측정): WP23 ⑬′ 재측정 때 **v6 로 일부러 한도를 넘는 context 를 보내**, 거절이 첫 메시지로 오는지 · 빈 메시지 뒤에 오는지 · 2초 안에 오는지를 결과 JSON 에 남긴다. 빈 메시지 뒤에 온다면 `_check_config` 를 「빈 `tokens` 메시지는 건너뛰고 2초 창 안에서 다음 메시지를 본다」 로 고치는 작은 수정이 필요하다(코디 → planner → backend · §4.6.1 문구 포함). 그 전까지 ㉒ 「거절 0」 은 「첫 메시지가 오류가 아니었다」 로 읽어야 한다.

---

## 대조 결과 — 브리프 §2 항목별(같음 = 문제 없음)

1. **운영 기본값 = 고친 동작 · 조합을 바꾸는 길** — 같음
   - `InterpretSession(…, *, block_blank=True, stt_model=STT_MODEL, endpoint_config=None)`(`session.py:84-85`) · `build_context(…, *, with_text=True, drop_reverse=())`(`glossary.py:247-248`) · `STT_MODEL = "stt-rt-v6"`(`soniox.py:23`).
   - 통역 API 경로 `app/api/interpret.py:63-65` 는 `context_for` · `config_check_sec` · `recorder` 만 넘긴다. `container.py:51` 의 `build_context` 호출도 인자를 더하지 않는다. `config.py` · `.env.example` 에 조합 이름 0(grep · 시험 `test_api_path_env_and_config_have_no_combo_names`). WS `start` 는 `parse_start`(`session.py:64-76`)가 `lang` 만 돌려줘서 다른 키는 버려진다(시험 `test_ws_start_extra_keys_ignored`).
   - 기본값일 때 `open_stt` 에 키워드를 더 넘기지 않는다(`session.py:116-121` · 시험 `kw == [{}]`).
   - `stt_config` 는 모델 이름 말고 0.7.0 과 같다. 키 집합 · 값 · 순서를 시험(`test_stt_config_v6_rest_same_as_070`)이 상수로 박아 대조한다. `endpoint_config` 를 주면 `ENDPOINT_KEYS` 3개만 받는다(`soniox.py:63-67`).
2. **§4.5 문안** — 같음
   - `CONTEXT_TEXT`(`glossary.py:41-48`)를 SPEC 0.8.1 코드블록에서 **직접 뽑아** 대조했다 → 같음 · 424자 · `\n` 3. 시험의 `SPEC_TEXT` 도 코드에서 다시 계산하지 않고 글자로 박아 두었다.
   - `to_soniox` 키 순서 `general → text → terms → translation_terms`(`glossary.py:234-240`). `text` 는 `TRIM_ORDER` 에 없어 줄지 않는다(`TRIM_ORDER` 는 주석만 바뀜). `forward_only` 에 `text` 가 남고(`:290-293`), `is_forward_only` 판정은 그대로다. `describe` 는 `text` 글자 수만 낸다.
   - 일반 낱말 짝 0: `translation_terms` 재료는 시드 term 뿐이다. 레포 시드 7개 언어 대조 시험이 있다(`test_translation_terms_all_from_seed_real_seed`).
   - `drop_reverse`(`:271`)는 뺄 source 를 `seen` 에 미리 넣는 방식이다. 그 source 의 역방향 짝(기본 · 별칭)만 빠지고 나머지 순서는 같다(시험 · zh-Hant `t2s` 뒤 대조 포함).
3. **§5.11 빈 원문 막기** — 같음
   - 판정 `is_blank`(`assembler.py:60-65`)는 `unicodedata.category(ch)[0] in "LN"` 이 하나도 없으면 참이다. 문장부호(P) · 기호(S · 이모지 포함) · 보이지 않는 글자(Cf) · 결합 부호(M) · 공백(Z)은 빈 원문이다. 전각 숫자(Nd)와 한자 · 가나 · 한글(Lo)은 글자로 본다. 시험이 반각 · 전각 · CJK 문장부호 · `~` · `♪` · U+200B · 결합 부호 단독 · 아라비아 숫자를 다룬다.
   - 거는 자리는 `_emit` → `_blank_filter` 한 곳이다(`session.py:290-323`). `final:false` 빈 원문은 보내지 않는다. 이미 나간 `id` 면 둘 다 빈 `final:true` 를 1번 보낸다. 막은 `id` 의 `Utterance` 는 큐에 넣지 않는다(`:300-302` — `_close` 가 caption 과 utt 를 같은 호출에 내므로 순서가 맞다). `_tts_worker` 는 바뀌지 않았다.
   - 기록: 막힌 발화는 보내지 않으니 줄이 없다. 둘 다 빈 `final:true` 는 `records.py:222-228` 이 쓰지 않고 `utterances` 에도 세지 않는다(시험 `test_blocked_utterance_not_recorded`).
   - 로그 1줄은 `id · side · original=<n> · translation=<n>` 이고 문장은 0이다(시험이 번역 문자열 부재를 확인). WS 메시지 모양은 그대로다.
   - pause · stop flush 도 같은 규칙을 탄다(시험 ⑨).
   - front 무변경 전제 맞음: `front/lib/view.ts:27-30` 의 `applyCaption` 은 같은 key 를 갈아 끼우고, `:48-49` 는 `trim()` 뒤 빈 글을 그리지 않는다. `openSide`(`:55-61`)는 `final:true` 를 열린 것으로 보지 않는다 → 둘 다 빈 `final:true` 를 받으면 말풍선이 사라진다.
4. **조용히 통과하는 자리** — 운영 코드 · 시험에서는 못 찾았다. 기대값은 상수로 박혀 있다(문안 · `GENERAL_070` · `stt_config` dict · 439). `final:false` 도 막는다. v6 첫 빈 메시지는 W-4, 스크립트 판정은 W-1 · W-2 를 보라.
5. **품질 시험 스크립트**
   - 레포에 목록 문장 0: 목록 · 규칙 경로는 인자로만 받고 기본 경로가 없다. 시험의 가짜 목록 · 규칙은 지어낸 문장이다. `test-sentences*` 파일 부재 시험도 있다.
   - 음성 · 로컬 결과가 레포 안이면 거절한다(`outside_repo` `:120-125` · 시험). `--out-repo` 는 코디 작업 폴더로 가야 하므로 막지 않는다(맞음).
   - 키: `Settings().soniox_api_key` 로만 읽고 출력 · 로그 0. 실패 행에는 예외 **종류 이름**과 `error_type` 만 남는다.
   - 규칙 4종(`:112` · `:195-259`)은 SPEC §9.3 표와 같다. ① 글자 그대로 + 찾을 쪽 · 대소문자 · zh 계열 `t2s`, ② 정규식 + 건너뛸 낱말, ③ 발화 수 · 번역 줄 수, ④ 없음. ④ 만 있으면 `none` 이다. 다른 종류는 오류다. 손님 쪽 「뒤집은 꼴」 은 ① 의 `negate` 로 받는다(§9.3 「손님 쪽」 문구와 같음).
   - 조각 수 = 실제 − `expected_finals`(§9.3 W-2 와 같음). 조합 A · B · C 와 `--drop-reverse` · `--endpoint` 는 운영 함수의 선택 인자로만 넘기고, 조립 결과를 손으로 고치지 않는다(`:464-476`).
   - 보고 이슈 1 ~ 4 는 SPEC 과 어긋나지 않는다.
     - 1(규칙 파일 JSON): SPEC 은 종류 · 적을 칸만 정했다.
     - 2(쉼 = 조각 사이 무음 1.0초 · TTS 앞뒤 무음은 그대로): SPEC 「무음 1.0초를 넣은 파일(조각을 따로 합성해 이어 붙임)」 그대로다. 실제 쉼이 조금 더 길다는 점은 결과 해석 때 참고할 일이다.
     - 3(지연 = 마지막 소리 조각을 보낸 때 → 마지막 비지 않은 확정 caption): §9.3 「파일의 말이 끝난 때 → 마지막 확정 caption」 과 같다.
     - 4(`drop_reverse` 는 개수 + `--label`): §9.3 결과 필드 목록에 그 칸이 없고, 가르기 8칸을 구분하는 데는 충분하다.
6. **범위** — 변경은 `back/` 안뿐이다(`git status`). `back/seed/` · `langs.py`(`CONTEXT_MAX_CHARS`) · `config.py` · `api/` · front · infra 는 무변경이다. `GENERAL` 은 무변경, `TRIM_ORDER` 는 주석 한 줄만 바뀌었다.
7. **관문** — 위에 적은 대로 ruff 통과 · 407 passed.

## 고객이 실물에서 만날 자리 (WP25 배포 때 볼 곳)

- **zh-Hant 연결**: 보낸 context 21,651자가 v5 로 잰 기준 21,689 바로 아래다. v6 에서 거절되면(W-4) 정방향 기본만으로 다시 붙지 못하고 「연결 안 됨」 으로 끊길 수 있다. 배포 뒤 zh-Hant 로 1회 연결해 `stt context: lang=zh-Hant … text=424 chars=21651` 로그와 `ready` 뒤 30초 안에 `soniox error` 경고가 없는지 본다.
- **빈 원문 막기**: 회색(말하는 중) 말풍선이 떴다가 확정 때 **사라지는** 일이 생긴다(이미 보인 `final:false` → 둘 다 빈 `final:true`). 운영 로그 `interpret blank original dropped` 줄 수가 하루 발화 수에 견줘 크면(짧은 감탄 · 잡음이 많은 환경) 사용자에게 「말풍선이 사라졌다」 는 체감으로 나타난다. 막힌 발화는 기록에도 남지 않으니(OQ-026) 로그 줄 수만이 단서다.

## 참고(기존 부채 · 사소한 것)

- `back/app/service/interpret/session.py:62` `OpenStt = Callable[..., Awaitable[SttConn]]` 로 넓혀 타입 검사가 약해졌다. `container.py:26` 의 `open_stt` 필드 주석 타입은 옛 3인자 그대로라 둘이 어긋난다(동작 영향 없음).
- `session.py:318` `_blocked` 에서 utt 가 없는 막힌 id(번역이 빈 막힌 발화)는 세션 끝까지 남는다. 세션당 몇 개라 무시할 만하다.
- `quality_check.py:244-253` 정규식(②)은 hay 만 `t2s` 하고 pattern 은 그대로다. zh-Hant · yue 문장에 **번체 글자가 든 정규식**을 쓰면 늘 안 걸린다(조용히 pass). 지금 T01 ~ T33 은 zh · en · ja 라 해당이 없지만, 규칙 파일 작성(WP22 ①) 때 「정규식은 간체로」 를 적어 두는 편이 낫다. 같은 자리의 건너뛸 낱말 지우기는 `case_sensitive` 와 무관하게 늘 대소문자를 가리지 않는다.
- `quality_check.py:523` 결과 머리의 기본 끊김 값이 `1000` 리터럴이다(`MAX_ENDPOINT_DELAY_MS` 를 쓰면 상수 한 곳 원칙에 맞음).
- 지연(`:480-481`): 발화가 Soniox 끊김이 아니라 `stop` flush 로 확정되면 지연에 꼬리 대기(3 ~ 15초)가 들어간다. 3절 해석(OQ-027) 때 「stop 으로 확정된 행」 을 구분할 칸이 있으면 오독을 줄인다.
