# 검수 — 식약처 MCP 코드 (공유 전 마지막 게이트)

**판정: WARN** — FAIL 0 · WARN 4 · 참고 5

- 대상: `reference/2026-10-27-mfds-mcp/` — git 에 올라갈 파일 16개(`git status --untracked-files=all`) + gitignore 된 `.env` · `cache/` · `.venv/` · `.pytest_cache/` · `.ruff_cache/` · `__pycache__/`
- 기준: SPEC-002 v0.2.0 · `phub-recommend-tool-brief.md` §3 · 코디 추가 지시(DUR 실제로 동작) · `NOTES.md` · `review-spec-002-003-report.md` W-13
- 실행: `uv run --offline pytest -q` 1회만 돌렸다(키 env 를 비우고 `MFDS_ENV_FILE` 을 없는 경로로 두어 실제 키가 읽히지 않게 했다) → **25 passed**. 실호출 · smoke · 서버 기동은 하지 않았다

---

## 1. 키 누출 — 0건

| 확인 | 결과 |
|---|---|
| `.env` 의 실제 키 값(64자)으로 폴더 전체를 검색(파일 내용 + 경로 이름). 원문 · `quote` · `quote_plus` · `unquote` 네 가지 형태, `.env` 만 빼고 | **0** |
| 같은 검색을 `.venv/` 에도 | **0** |
| `cache/` 파일 이름 9개 + `_calls/2026-10-27.json` | 파일 이름이 sha256 해시 + `_p1` 뿐이고, 내용에도 키가 없다(위 검색에 포함) |
| `serviceKey` 문자열 | 쓰는 곳은 `client.py:113` 한 곳뿐이다(요청을 만드는 곳). 나머지는 주석(`client.py:21`)과 테스트 단언(`test_tools.py:38` · `:255`)이다 |
| `.gitignore` | `.env` · `.env.*`(`.env.example` 은 예외로 둠) · `cache/` · `.venv/` · `__pycache__/` · `.pytest_cache/` · `.ruff_cache/` — `git check-ignore -v` 로 여섯 경로 모두 막혀 있는 것을 확인했다 |

W-13 반영 여부:

- httpx 로거 — `httpx` · `httpcore` · `httpx2` · `httpcore2` 를 WARNING 으로 둔다(`client.py:22-23`, `server.py:179-180`). `mcp` 2.3 이 `httpx2` 를 끌어오므로 함께 막은 것이 맞다. 로그는 stderr 로만 나간다(`server.py:178`)
- 예외 — `TimeoutException` · `HTTPError` 는 클래스 이름만 싣고 `from None` 으로 끊는다(`client.py:116-121`). 그 밖의 예외도 클래스 이름만 싣는다(`server.py:49-51`)
- 응답 본문 — `scrub()` 이 키 세 형태(원문 · quote · quote_plus)를 지운 뒤에 파싱 · 캐시 · `body_head` 에 쓴다(`client.py:82-88` · `:126` · `:182`). httpx 는 질의를 `urllib.parse.urlencode`(= quote_plus) 로 만든다(`.venv/.../httpx/_urls.py:624`). 그래서 서버가 URL 을 그대로 되돌려 보내는 최악의 경우도 지울 수 있다. `test_key_never_leaks` 는 `+ / =` 가 섞인 가짜 키로 이 경우를 시험한다
- `Config.__repr__` 는 키를 `<set>` 으로 가린다(`config.py:44-51`)

## 2. WARN

### W-1 · 「폴더째 첨부」로 보내면 실제 키 · 캐시 · .venv 가 따라간다 — 사용자가 실물에서 가장 먼저 만날 자리

- 근거: 사용자는 「코드를 첨부 파일로 공유」한다(브리프 §2). 그런데 지금 폴더 안에 실제 키가 든 `.env`(200B)와 실제 API 응답(업체 주소 `ENTP_ADDR` 원본 포함 · `cache/`)이 있다. `.venv/` 는 editable 설치라 이 컴퓨터의 절대 경로를 가리킨다. `.gitignore` 는 git 에만 걸린다. zip 으로 묶거나 Finder 에서 복사하면 세 가지 모두 그대로 간다
- 받는 사람 쪽: `.venv` 가 함께 가면 `uv run` 이 그 환경을 다시 만들기는 한다. 하지만 키가 넘어간 것은 되돌릴 수 없다
- 고칠 것(코드는 그대로 둔다 — 공유하는 방법만 정한다): `git archive` 로 묶거나(커밋 뒤 `git archive HEAD:reference/2026-10-27-mfds-mcp -o mfds-mcp.zip`), 묶기 전에 `.env` · `cache/` · `.venv/` · `.pytest_cache/` · `.ruff_cache/` · `__pycache__/` 를 뺀다. README 맨 위에 「공유하기 전에 위 폴더 · 파일을 빼라」 한 줄을 두면 받는 사람이 다시 퍼뜨릴 때도 막힌다

### W-2 · DUR 9종 가운데 6종은 필터 이름을 실제로 확인하지 않았다 — 무시되면 관계없는 행이 「금기」로 나온다

- 근거: NOTES 에서 `itemName` 이 먹는 것을 확인한 오퍼레이션은 3개뿐이다 — pregnancy(:63 · 41건) · usjnt(:66 · 1,189건) · product(:67 · 41건). `itemSeq` 는 pregnancy 하나만 확인했다(:65). age · elderly · capacity · period · efficacy_dup · split 6종은 부르지 않았다(`tools.py:22-32` 는 9종 모두 같은 `itemName` · `itemSeq` 를 보낸다)
- 왜 문제인가: 이 포털은 받지 않는 필터를 에러 없이 무시하고 전체를 낸다(NOTES :52 · :64 — 대문자 `ITEM_NAME` 을 보내면 16,063건). 의료기기 · 의약품의 한 건 조회 tool 은 `filter_ignored` 로 막았지만 `mfds_dur_check` 에는 이런 가드가 없다. 그래서 필터가 무시되면 관계없는 약 100행이 「노인주의」 같은 결과로 나간다. tool description(`server.py:144-147`)은 「0건 ≠ 안전」만 경고하고, 반대 방향(무시된 필터)은 말하지 않는다. 나중에 상담 에이전트가 이것을 그대로 읽는다(SPEC-002 §1)
- 고칠 것(둘 중 하나): ① 6종을 `itemName=이소트레티노인`(또는 해당 종류에 있는 약)으로 1회씩 불러 total 이 줄어드는지 보고 NOTES 에 적는다(6회). ② 가드를 둔다 — `item_seq` 로 부를 때는 받은 행의 `ITEM_SEQ` 가 모두 같아야 하고, `item_name` 이면 `ITEM_NAME` 에 그 문자열이 들어 있어야 한다. 어긋나면 `filter_ignored`

### W-3 · 틀린 키와 미등록을 구분하지 못한다 — 구현 미결로 남음

- 근거: NOTES :70 · `client.py:144-154`. 둘이 HTTP 403 · `SERVICE_KEY_IS_NOT_REGISTERED_ERROR` 로 똑같이 온다
- 처리는 맞다: 메시지에 「키 값 자체가 틀려도 같은 에러가 온다」를 적었고(`client.py:148`), README §6 · §7 이 Decoding / Encoding 키를 구분하는 법(Encoding 키에는 `%` 가 섞인다)과 `mfds_status(refresh=true)` 로 서비스별 상태를 보는 법을 안내한다. 남은 것은 사람 쪽 판단이다. **네 서비스가 모두 `not_registered` 면 키가 틀린 것, 하나만 그렇다면 그 API 만 활용신청이 안 된 것**이다. README §7 둘째 줄에 이미 같은 뜻이 있다. 코드에서는 더 할 것이 없다

### W-4 · 출력이 크다 — 작업자의 Claude 컨텍스트를 빨리 먹는다

- 근거: 기본값이 `rows=100`(`server.py:71` 등)이다. 항목마다 `source`(서비스 · 오퍼레이션 · query 전체)가 반복해서 붙는다(`tools.py:83` · `:93`). `mfds_drug_detail` 은 효능 · 용법 · 주의 XML 원문(`EE/UD/NB_DOC_DATA`)을 통째로 낸다. 업체 이름으로 18건만 받아도 수천 토큰이고, 의약품 상세 한 건은 주의사항만으로 수만 자가 될 수 있다
- SPEC 위반은 아니다(SPEC §4 「필드 이름 · 값 그대로」 · 「`source` 를 항목마다」). 원장 초안을 만들 때 수백 번 부르면 바로 체감된다. README 「알아 둘 것」에 「작은 `rows` 로 먼저 본다」 한 줄을 두거나, 기본 `rows` 를 낮추는 것은 사용자가 정할 일이다

## 3. SPEC 대조

### 맞는 것

| 항목 | 근거 |
|---|---|
| tool 7개 이름 · 순서 | `server.py:55-172` · `test_mcp_tool_error_has_code_and_no_key` |
| T-1: 대문자 `TYPE_NAME` · `ENTRPS` · `PRDUCT` 를 한 요청에 · 상세 오퍼레이션만 · 목록 오퍼레이션 · 소문자 `entrps` 를 쓰지 않음 | `tools.py:13` · `:138-143` · 테스트 `test_device_search_uppercase_params_and_one_request` |
| 입력을 바꾸지 않음(앞뒤 공백만 자름) | `tools.py:47-52` · `test_device_search_case_sensitive_empty_not_error` |
| 품목허가 items 를 한 겹 벗김 · 캐시는 원본 `{"item":…}` 그대로 | `client.py:43-64` · `test_device_search_filters_cancelled_and_caches` |
| 취소를 받은 뒤 서버에서 거름 · `total_count` 는 API 값 그대로 · `filtered_out_cancelled` · `include_cancelled` 는 캐시 키에 넣지 않음 | `tools.py:77-108` · `cache.py:23-26` |
| T-2: 허가번호만 받음 · `total_count≠1` 이면 `filter_ignored` | `tools.py:111-118` · `:146-152` |
| T-3: `BSSH_NM` · `ENTP_ADDR` · `SRVC_TRGT_*` 를 뺌 · `include_cancelled` 없음 | `tools.py:43` · `:154-161` |
| 공통 출력 키 12개 | `tools.py:95-108` |
| 빈 결과(`items` 키 없음) → `[]` · 에러 아님 | `client.py:51-53` |
| 에러 코드: `missing_key` · `key_not_registered` · `api_error` · `service_not_found` · `upstream_unreachable` · `daily_limit_reached` · `filter_ignored` · `invalid_input` · 에러는 캐시하지 않음 | `client.py:102-196` · `test_error_mapping` 6건 |
| 캐시: sha256(서비스\|오퍼레이션\|정렬한 질의, 키 뺌) · 파일 이름은 해시 + 페이지 · `fetched_at` + query + 원본 · TTL 7 · `no_cache` 이면 덮어씀 | `cache.py:23-65` |
| 일일 상한: 실제 HTTP 만 셈 · 캐시 적중은 상한에 닿아도 답함 | `client.py:105-122` · `test_daily_limit` |
| `all_pages` · `MFDS_MAX_PAGES` · `truncated` | `client.py:232-240` · `test_all_pages_truncates` |
| 키 없음이면 조회 tool 은 `missing_key`(캐시가 있어도) · `mfds_status` 는 동작하고 `key_present=false` | `client.py:224-225` · `test_missing_key` |
| `mfds_status` 는 API 를 부르지 않음 · `refresh=true` 일 때만 서비스마다 `rows=1` 로 1회 | `tools.py:219-245` |
| env: 프로세스 env 가 `.env` 보다 먼저 · 선택 env 4개 + `MFDS_CACHE_DIR` | `config.py:53-79` · `.env.example` |

### SPEC 과 다른 점 — 판정

| # | 다른 점 | 판정 | 근거 |
|---|---|---|---|
| ① | 의약품 07 → `DrugPrdtPrmsnInfoService08`(목록 · 상세 · 주성분) | **수용** | 브리프 §3-1 이 SPEC 보다 우선한다. NOTES :32-38 실호출 |
| ② | DUR `not_available_yet` 를 없애고 실제로 조회 | **수용** | 코디 추가 지시 · NOTES :40-43(사용자 신청 직후 동작 확인). 미등록이면 `key_not_registered` 로 구분한다(`test_dur_not_registered`). README §1 이 DUR 을 활용신청 API 4개에 넣었다(브리프 §3-2). 단 6종은 확인하지 않았다 → **W-2** |
| ③ | `drug_search` 에서 `ingredient` 입력을 뺌 | **수용** | NOTES :56 — `item_ingr_name` 은 0건이라 받는지 판단할 수 없다. 받지 않는 필터를 두지 않는 것이 SPEC 의 「무시된 필터」 원칙에 맞다. 성분은 출력 `ITEM_INGR_NAME` 으로 본다 |
| ④ | `drug_detail` 은 `item_seq` 만 · `not_in_cache` 경로 없음 | **수용** | NOTES :58 — 상세가 `item_seq` 를 받는다(1건 · 없는 값이면 0). SPEC T-5 의 「받으면 T-2 와 같은 규칙」 갈래다(`tools.py:184-185`) |
| ⑤ | `include_ingredients` 입력 추가(Mcpn) | **수용** | 기본값 false 라 덧붙이기만 한다. NOTES :60-62 — Mcpn 은 `item_seq` 를 무시하고 `Prduct` 완전 일치만 받는다. 그래서 받은 뒤 `ITEM_SEQ` 로 고르는 방식(`tools.py:187-192`)이 맞다 |
| ⑥ | ruff line-length 140 | **수용** | 동작과 관계없다 |
| ⑦ | (보고에 없음) DUR `kind` 3 → 9, `item_seq` 입력 추가 | **수용 + W-2** | SPEC 은 「자리만 둔다」였다. 덧붙이기만 했다 |
| ⑧ | (보고에 없음) `state: "not_applied"` 를 내지 않음 | **수용** | 미등록과 신청 전이 같은 에러로 와서 구분할 수 없다(W-3) |
| ⑨ | (보고에 없음) 등록 명령이 SPEC §5.3 `python server.py` 대신 스크립트 `mfds-mcp` 이고 경로는 절대 경로 | **수용** | `pyproject.toml:12-13`. `server.py` 를 남겨 두어 SPEC 명령도 뜬다. 받는 사람에게는 절대 경로가 맞다 |

SPEC 위반으로 틀린 결과가 나오는 자리는 없다.

## 4. 받는 사람 기준 — 폴더 하나로 돌아가나

| 확인 | 결과 |
|---|---|
| 이 프로젝트에 기대는 것 | 코드 · README · pyproject 에 `/Users/` · `kknaks` · orca · Procedure Hub 경로가 없다. 남은 것은 `NOTES.md:25` 의 「SPEC-002 작성 중 writer 재호출」 한 줄뿐이다(내부 용어지만 동작과 관계없다 → 참고 R-2) |
| 빠진 파일 | `pyproject.toml` · `uv.lock`(패키지 41개 · 출처는 모두 PyPI · 자기 패키지는 `editable = "."`) · `.env.example` · `README.md` · `scripts/smoke.py` · `tests/` 모두 있다. LICENSE 는 없다(브리프 §3-3 — 사용자가 정하기 전) |
| 설치 | `uv sync` → hatchling 이 `src/mfds_mcp` 를 editable 로 설치한다. `config.py:10` 의 `PROJECT_DIR = parents[2]` 는 editable 이라 폴더 루트를 가리키므로 `.env` · `cache/` 를 제자리에서 찾는다. Python 3.11 이상 · `datetime.UTC` 를 쓰므로 3.11 미만은 안 된다(pyproject 가 막는다) |
| README 명령과 실제 일치 | `uv run --directory "<절대경로>" mfds-mcp`(entry point 있음) · Claude Desktop JSON · `uv run python server.py`(`server.py` 가 넘겨줌) · `uv run python scripts/smoke.py` · `uv run pytest` · `uv run ruff check .` — 모두 실제 파일과 맞는다 |
| README 예시 수치 | Thermage 3 / 1 / 2 · 이소트레티노인 임부금기 41 · 나보타 원어명 · 포장 단위 — NOTES 와 맞는다 |
| README 활용신청 링크 4개 | 15057456 · 15073895 · 15095677 · 15059486 — 앞의 셋은 NOTES · SPEC 의 번호와 같다. DUR(15059486)은 NOTES 에 번호가 없어 대조하지 못했다(→ 참고 R-3) |

## 5. 테스트 · smoke

- **pytest 25 passed(0.38s)**. 모든 요청이 `httpx.MockTransport` 로 가고(`conftest.py:153`) 캐시는 `tmp_path` 에 둔다. 실호출 0 · 실제 `cache/` 를 건드리지 않는다
- 시험하는 것: 항목 모양 5가지 · S-1(취소 거르기 · 캐시 · 원본 보존) · 대소문자를 그대로 보냄 · 대문자 · 한 요청 · 입력 검사 · `all_pages` 잘림 · T-2 `filter_ignored` · 주소 제외 · 의약품 소문자 · 취소 · 상세 + 주성분 고르기 · DUR · 미등록 → 상태 · 에러 6종 · 키 없음 · 일일 상한 · 상태 · **키 누출(URL 을 되돌려 주는 500 · URL 이 든 ConnectError · 403 → 에러 dict · repr · 캐시 · 로그 · stdout · stderr)** · tool 7개 목록 · env 우선순위 · MCP `call_tool` 에러 코드
- 시험하지 않는 것: 실제 응답 모양은 NOTES 를 보고 흉내 냈다(conftest :1). DUR 6종 필터(W-2) · TTL 만료 · `no_cache` 덮어쓰기는 단위 테스트가 없다(코드는 단순하다)
- `scripts/smoke.py` 가 확인하는 것: 실호출 약 8회 — device_search(Thermage · `no_cache`) · 두 번째는 캐시 · device_detail 1건 · device_company(솔타) · 주소 제외 · drug_search(나보타) · drug_detail + 주성분 · DUR 임부 · 병용(이소트레티노인) · 상태. 판정이 느슨하다(`total ≥ 1`). SPEC 수치 3 / 1 / 2 를 단언하지 않는다. 데이터가 바뀌어도 깨지지 않게 한 것으로 보고 받아들인다. README 의 「10회 안팎」과 맞다. `cache/_calls/2026-10-27.json` 의 오늘 총 9회와도 맞다(stdio e2e 1회 포함으로 보인다)

## 6. 참고 (판정에 영향 없음)

- R-1 · README §2 의 `cd mfds-mcp # 이 폴더` — 실제 폴더 이름은 `2026-10-27-mfds-mcp` 다. 받는 사람은 「이 폴더」로 읽으면 된다. 공유할 때 폴더 이름을 `mfds-mcp` 로 바꾸면 그대로 맞는다
- R-2 · `NOTES.md` 에 내부 작업 용어(「writer 재호출」 · 「SPEC-002」 · 「tool_dev」 · 「사용자 신청」)와 SPEC 작성 단계의 옛 기록(의약품 07 · DUR 미등록, :17-19 · :30)이 남아 있다. 뒤쪽 절에서 정정되므로 틀린 정보는 아니다. 받는 사람에게 읽히는 문서라 맨 위에 「아래로 갈수록 최신 — 07 · DUR 미등록 기록은 08 · 03 절에서 정정됐다」 한 줄이 있으면 덜 헷갈린다
- R-3 · DUR 링크 `15059486` 은 이번에 대조할 근거가 없었다. 코드 실행 금지라 열어 보지 않았다. 공유 전에 한 번 클릭해 보면 된다
- R-4 · 서버 버전 문자열 `version="0.1.0"`(`server.py:38`)과 pyproject `0.1.0` 은 같다. SPEC 의 0.2.0 은 문서 버전이라 관계없다
- R-5 · `mfds_status` 의 상태는 프로세스 안에서만 기억한다. Claude Code 세션을 새로 열면 다시 `unknown` 이다. SPEC §4 State 의 정의대로이고, README 의 tool 설명도 「이 프로세스의 마지막 실제 호출 기준」이라고 적었다

## 7. 사용자가 실물에서 만날 자리

1. **공유 파일을 묶는 순간**(W-1) — 폴더를 그냥 zip 으로 묶으면 실제 키가 든 `.env` 가 들어간다. 묶을 때 `git archive` 를 쓰거나 위 6개를 뺀다
2. **받는 사람의 첫 실행** — 활용신청한 뒤 반영(1시간 안팎)되기 전에는 전부 `key_not_registered` 다. 키가 틀려도 같은 에러가 온다(W-3). README §7 이 안내한다
3. **`.env` 를 고친 뒤** 클라이언트를 다시 켜야 반영된다(서버가 시작할 때 한 번만 읽는다). README §7 에 있다
4. **DUR 의 노인 · 용량 · 기간 · 중복 · 분할 · 연령** — 확인하지 않은 6종이다. total 이 1만 건대로 나오면 필터가 무시된 것이다(W-2)
5. **의약품 상세 · 넓은 업체 검색은 출력이 길다**(W-4) — 처음에는 `rows` 를 작게 준다
6. **「Thermage」 유효 1건** — 정품 수입 허가 둘이 취소라 기본값에서 빠진다. 「써마지가 없다」로 읽히지 않게 `include_cancelled=true` 를 함께 본다(SPEC S-1 · 검수 R1 과 같다)
