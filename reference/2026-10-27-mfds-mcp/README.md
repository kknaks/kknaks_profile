# mfds-mcp — 식약처 허가 정보 조회 MCP 서버

식품의약품안전처가 공공데이터포털(data.go.kr)에 공개한 허가 정보를 **Claude Code / Claude Desktop 의 tool** 로 조회하는 MCP 서버입니다. stdio 로 뜨고, 조회만 합니다.

- **의료기기 품목허가**: 모델명 · 업체 · 품목명으로 검색, 허가번호로 한 건 조회
- **의료기기 업체**: 제조업 / 수입업 허가 업체
- **의약품 허가**: 제품명 · 업체명으로 검색(원어명 `ITEM_ENG_NAME` · `ENTP_ENG_NAME`, 취소 상태), 품목기준코드로 상세(규격 `MATERIAL_NAME` · `PACK_UNIT`, 효능 · 용법, 주성분)
- **DUR(의약품 안전사용)**: 병용금기 · 임부금기 · 특정연령대금기 · 노인주의 · 용량주의 · 투여기간주의 · 효능군중복 · 서방정분할주의 · DUR 품목

API 응답의 **필드 이름과 값을 그대로** 돌려줍니다(대문자 키). 덧붙이는 값은 `is_cancelled`(취소 · 취하 여부)와 `source`(어느 서비스 · 오퍼레이션 · 질의로 받았는지) 둘뿐입니다. 결과는 **후보**이고 매칭 판정이 아닙니다. 모델을 부르지 않고 번역 · 요약도 하지 않습니다.

같은 질의는 로컬 캐시로 답해서 호출 수를 아낍니다. 키는 출력 · 로그 · 캐시 어디에도 남기지 않습니다.

---

## 1. 준비 — 공공데이터포털 키와 활용신청

1. [공공데이터포털](https://www.data.go.kr) 에 가입하고 로그인합니다.
2. 아래 **API 4개를 모두 활용신청**합니다. 각 페이지에서 「활용신청」 → 목적 입력 → 신청. 보통 자동 승인되고, 승인 뒤 **반영까지 1시간 안팎** 걸릴 수 있습니다. 4개 모두 승인돼야 tool 7개가 전부 동작합니다.

   | API | 공공데이터포털 | 쓰는 tool |
   |---|---|---|
   | 식품의약품안전처_의료기기 품목허가 정보 (`MdlpPrdlstPrmisnInfoService06`) | <https://www.data.go.kr/data/15057456/openapi.do> | `mfds_device_search` · `mfds_device_detail` |
   | 식품의약품안전처_의료기기 수입 및 제조허가 상세 (`MdeqMnftPrmsnDtlService01`) | <https://www.data.go.kr/data/15073895/openapi.do> | `mfds_device_company` |
   | 식품의약품안전처_의약품 제품 허가정보 (`DrugPrdtPrmsnInfoService08`) | <https://www.data.go.kr/data/15095677/openapi.do> | `mfds_drug_search` · `mfds_drug_detail` |
   | 식품의약품안전처_의약품안전사용서비스(DUR)품목정보 (`DURPrdlstInfoService03`) | <https://www.data.go.kr/data/15059486/openapi.do> | `mfds_dur_check` |

   링크가 바뀌었으면 포털에서 괄호 안 서비스 이름이나 API 이름으로 검색합니다.

3. 마이페이지 → 「일반 인증키」에서 **Decoding** 키를 복사합니다(Encoding 키가 아닙니다). 키 하나로 4개 API 를 모두 씁니다.

## 2. 설치

[uv](https://docs.astral.sh/uv/) 가 필요합니다(Python 은 uv 가 알아서 받습니다 — 3.11 이상).

```bash
cd mfds-mcp            # 이 폴더
uv sync                # 의존성 설치(uv.lock 고정)
cp .env.example .env   # 그리고 .env 의 MFDS_API_KEY= 뒤에 Decoding 키를 붙여 넣는다
```

확인(선택) — 엔드포인트마다 1~2회 실제로 부릅니다(총 10회 안팎):

```bash
uv run python scripts/smoke.py
```

모두 `[OK ]` 이고 마지막 줄이 `FAIL: 없음` 이면 됩니다.

## 3. 등록

키는 서버가 시작할 때 **이 폴더의 `.env`** 에서 읽습니다. 등록 명령이나 설정 파일에는 키를 넣지 마세요(설정 파일에 키가 남습니다).

### Claude Code

```bash
claude mcp add mfds -- uv run --directory "<이 폴더의 절대 경로>" mfds-mcp
```

`claude mcp list` 에 `mfds` 가 보이고, 새 세션에서 tool 7개(`mfds_*`)가 보이면 됩니다. 모든 프로젝트에서 쓰려면 `claude mcp add --scope user ...`.

### Claude Desktop

설정 파일(macOS `~/Library/Application Support/Claude/claude_desktop_config.json`, Windows `%APPDATA%\Claude\claude_desktop_config.json`)에 추가하고 Claude Desktop 을 다시 켭니다.

```json
{
  "mcpServers": {
    "mfds": {
      "command": "uv",
      "args": ["run", "--directory", "<이 폴더의 절대 경로>", "mfds-mcp"]
    }
  }
}
```

Desktop 이 `uv` 를 못 찾으면 `"command"` 에 `which uv`(Windows 는 `where uv`)로 나온 전체 경로를 넣습니다.

`uv run python server.py` 로도 뜹니다(폴더 안에서). 직접 칠 일은 없습니다 — 클라이언트가 띄웁니다.

## 4. tool

| tool | 무엇 | 주요 입력 | API |
|---|---|---|---|
| `mfds_status` | 키 유무 · 서비스별 상태 · 오늘 호출 수 · 캐시 크기. **먼저 부른다** | `refresh`(서비스마다 1회 확인 호출) | — |
| `mfds_device_search` | 의료기기 품목허가 검색 | `type_name`(모델명) · `entrps`(업체) · `prduct`(품목명 = 일반명칭) 중 하나 이상 · `include_cancelled` | 품목허가 상세 `getMdlpPrdlstPrmisnItem05` |
| `mfds_device_detail` | 의료기기 허가 한 건 | `prmisn_no`(허가번호 `PRDUCT_PRMISN_NO`) | 같음 |
| `mfds_device_company` | 의료기기 제조 · 수입업 업체 | `name`(업체 이름 일부) | `getMdeqMnftPrmsnDtlInq01` |
| `mfds_drug_search` | 의약품 허가 검색 | `item_name`(제품명) · `entp_name`(업체명) 중 하나 이상 · `include_cancelled` | `getDrugPrdtPrmsnInq08` |
| `mfds_drug_detail` | 의약품 허가 상세 한 건 | `item_seq`(품목기준코드 `ITEM_SEQ`) · `include_ingredients`(주성분 상세 덧붙임) | `getDrugPrdtPrmsnDtlInq08` (+ `getDrugPrdtMcpnDtlInq08`) |
| `mfds_dur_check` | DUR 조회 | `kind` · `item_name` 또는 `item_seq` | `DURPrdlstInfoService03` 9개 오퍼레이션 |

공통 입력: `page`(1부터) · `rows`(1~100, 기본 100) · `all_pages`(끝까지 이어 받기, 최대 `MFDS_MAX_PAGES` 페이지 — 넘으면 `truncated: true`) · `no_cache`(캐시 건너뛰고 새로 받기).

`mfds_dur_check` 의 `kind`:

| kind | 뜻 | 오퍼레이션 |
|---|---|---|
| `usjnt` | 병용금기 | `getUsjntTabooInfoList03` |
| `pregnancy` | 임부금기 | `getPwnmTabooInfoList03` |
| `age` | 특정연령대금기 | `getSpcifyAgrdeTabooInfoList03` |
| `elderly` | 노인주의 | `getOdsnAtentInfoList03` |
| `capacity` | 용량주의 | `getCpctyAtentInfoList03` |
| `period` | 투여기간주의 | `getMdctnPdAtentInfoList03` |
| `efficacy_dup` | 효능군중복 | `getEfcyDplctInfoList03` |
| `split` | 서방정분할주의 | `getSeobangjeongPartitnAtentInfoList03` |
| `product` | DUR 품목 목록 | `getDurPrdlstInfoList03` |

### 출력 모양

```json
{
  "service": "MdlpPrdlstPrmisnInfoService06",
  "operation": "getMdlpPrdlstPrmisnItem05",
  "query": {"type": "json", "TYPE_NAME": "Thermage", "numOfRows": 100, "pageNo": 1},
  "total_count": 3,
  "page": 1, "rows": 100,
  "returned": 1,
  "filtered_out_cancelled": 2,
  "truncated": false,
  "from_cache": false,
  "fetched_at": "2026-10-27T06:00:00+00:00",
  "items": [{"ENTRPS": "…", "TYPE_NAME": "…", "PRDUCT_PRMISN_NO": "…", "…": "…", "is_cancelled": false, "source": {"…": "…"}}]
}
```

- `total_count` 는 API 값 그대로입니다. 취소 · 취하를 뺀 수는 `filtered_out_cancelled` 로 따로 나옵니다(취소 거르기는 받은 뒤 이 서버가 합니다).
- 0건은 에러가 아니라 `items: []` 입니다.
- 정렬은 API 순서 그대로입니다.

### 예시 (Claude 에게 이렇게 말하면 됩니다)

- 「`mfds_device_search` 로 모델명 Thermage 찾아 줘」 → total 3 · 유효 1 · 취소 2 (2026-10-27 기준)
- 「업체 이름에 '솔타' 가 들어간 의료기기 업체를 찾아서 제조업인지 수입업인지 알려 줘」 → `mfds_device_company(name="솔타")`
- 「나보타 허가 정보와 원어명 · 포장 단위 알려 줘」 → `mfds_drug_search(item_name="나보타")` 후 `mfds_drug_detail(item_seq=…)` → Nabota Inj / Daewoong Pharmaceuticals / `1바이알/상자[바이알(100유니트)]`
- 「이소트레티노인 임부금기 확인해 줘」 → `mfds_dur_check(kind="pregnancy", item_name="이소트레티노인")` → 41건

### 알아 둘 것 (2026-10-27 실호출로 확인)

- **의료기기 모델명은 대소문자를 가립니다.** `Thermage` 3건, `thermage` 0건. 입력은 바꾸지 않고 그대로 보냅니다.
- 의료기기 품목명(`prduct`)은 「조직수복용생체재료」 같은 **일반명칭**이라 브랜드로는 거의 안 걸립니다. 브랜드는 모델명에 들어 있을 때만 걸립니다. 수입 제품은 모델 코드로만 등록된 경우가 많습니다.
- 업체 · 제품명 필터는 **부분 일치**라 관계없는 업체 · 제품도 섞입니다. 여러 필터를 주면 AND 입니다.
- 공공데이터포털은 **받지 않는 필터를 에러 없이 무시하고 전체를 냅니다**(예: 의료기기 품목일련번호 `MDEQ_PRDLST_SN` → 21만 건). 그래서 한 건 조회 tool(`mfds_device_detail` · `mfds_drug_detail`)은 응답이 정확히 1건이 아니면 `filter_ignored` 에러를 냅니다.
- 의약품 필터는 소문자(`item_name` · `entp_name` · `item_seq`), 의료기기는 대문자(`TYPE_NAME` · `ENTRPS` · `PRDUCT` · `PRDUCT_PRMISN_NO`), DUR 은 `itemName` · `itemSeq` 입니다. 서버가 알아서 맞춥니다.
- 의약품 주성분 상세(`getDrugPrdtMcpnDtlInq08`)는 `item_seq` 를 무시하고 제품명 완전 일치(`Prduct`)만 받습니다. 그래서 `include_ingredients` 는 상세의 `ITEM_NAME` 으로 부르고 `ITEM_SEQ` 가 같은 행만 남깁니다.
- 의약품 취소 판정: `CANCEL_DATE` 가 있거나 `CANCEL_NAME` 이 「정상」이 아니면(예 「취하」 · 「취소」) 취소. 의료기기: `RTRCN_DSCTN_DIVS_CD` 또는 `RTRCN_DSCTN_DT` 가 차 있으면 취소.
- DUR 0건은 「그 DUR 항목의 대상이 아님」이지 안전하다는 판정이 아닙니다.
- `mfds_device_company` 는 업체 주소(`ENTP_ADDR`) · `SRVC_TRGT_*` 를 출력에서 뺍니다(캐시 원본에는 남습니다).
- 의약품 상세의 효능 · 용법 · 주의(`EE_DOC_DATA` · `UD_DOC_DATA` · `NB_DOC_DATA`)는 XML 원문 그대로라 깁니다.

## 5. 한도 · 캐시

| 설정(`.env`) | 기본값 | 뜻 |
|---|---|---|
| `MFDS_API_KEY` | (필수) | 공공데이터포털 일반 인증키 · Decoding |
| `MFDS_DAILY_LIMIT` | 1000 | 하루 실제 HTTP 호출 상한. 캐시 적중은 세지 않습니다. 날짜는 한국 시간 기준. 닿으면 캐시에 있는 질의만 답하고 나머지는 `daily_limit_reached` |
| `MFDS_CACHE_TTL_DAYS` | 7 | 캐시 유효 기간(일). 지나면 다음 호출에서 새로 받습니다 |
| `MFDS_MAX_PAGES` | 10 | `all_pages=true` 일 때 최대 페이지 수 |
| `MFDS_TIMEOUT_SECONDS` | 30 | 요청 시간 초과(초). 재시도하지 않습니다 |
| `MFDS_CACHE_DIR` | 이 폴더의 `cache/` | 캐시 위치 |

공공데이터포털 쪽 일일 트래픽 한도는 API 마다 포털의 「활용신청 상세」에 나옵니다. `MFDS_DAILY_LIMIT` 은 그보다 낮게 둔 안전장치입니다.

- 캐시: `cache/<해시>_p<페이지>.json` — API 원본 응답 그대로 + 받은 시각 + 키 뺀 질의. 파일 이름에 질의 문자열을 쓰지 않습니다.
- 호출 수: `cache/_calls/<YYYY-MM-DD>.json` — 서비스별 실제 호출 수.
- 에러 응답은 캐시하지 않습니다(활용신청이 반영되면 바로 다시 시도할 수 있게).
- 캐시를 비우려면 `cache/` 를 지우면 됩니다.
- `.env` · `cache/` · `.venv/` 는 `.gitignore` 에 들어 있습니다.

## 6. 에러

tool 에러는 JSON 문자열로 오고 `error` 키로 구분합니다.

| `error` | 언제 | 할 일 |
|---|---|---|
| `missing_key` | `.env` 에 `MFDS_API_KEY` 가 없음 | 키를 넣고 클라이언트를 다시 켠다. `mfds_status` 는 이때도 동작 |
| `key_not_registered` | `SERVICE_KEY_IS_NOT_REGISTERED_ERROR` | 그 API 활용신청 · 반영 대기. **키가 틀려도 같은 에러**가 온다 |
| `api_error` | 그 밖의 API 에러(`resultCode` ≠ `00`, HTTP 401 · 500 등) | 원문 코드 · 메시지를 본다 |
| `service_not_found` | HTTP 404 | 서비스 · 오퍼레이션 이름이 바뀌었는지 포털에서 확인 |
| `upstream_unreachable` | 연결 실패 · 시간 초과 | 네트워크 확인. 재시도하지 않는다 |
| `daily_limit_reached` | `MFDS_DAILY_LIMIT` 에 닿음 | 내일 또는 상한을 올린다 |
| `filter_ignored` | 한 건 조회인데 응답이 1건이 아님 | 허가번호 · 품목기준코드 값을 확인 |
| `invalid_input` | 입력 규칙 위반(필터 없음 · `rows` 범위 등) | 메시지대로 고친다 |

## 7. 문제 해결

- **tool 이 안 보인다**: `claude mcp list` 로 상태를 봅니다. `--directory` 경로가 이 폴더의 **절대 경로**인지, 그 폴더에서 `uv sync` 를 했는지 확인합니다. 손으로 띄워 봐도 됩니다: `uv run --directory "<경로>" mfds-mcp` — 에러 없이 입력을 기다리면 정상입니다(Ctrl+C 로 끕니다).
- **전부 `key_not_registered`**: Decoding 키를 넣었는지(Encoding 키는 `%` 가 섞여 있습니다), 활용신청 뒤 1시간쯤 지났는지 확인합니다. 하나만 그렇다면 그 API 만 활용신청이 안 된 것입니다 — `mfds_status(refresh=true)` 로 서비스별 상태를 봅니다.
- **`missing_key` 인데 `.env` 를 채웠다**: `.env` 가 이 폴더 바로 아래에 있는지, 줄이 `MFDS_API_KEY=...` 꼴인지 봅니다. 고친 뒤 클라이언트(Claude Code 세션 / Desktop)를 다시 켭니다.
- **결과가 21만 건처럼 너무 많다**: 그 필터를 API 가 무시한 것입니다(위 「알아 둘 것」).
- **예전 결과가 나온다**: 캐시입니다. `no_cache=true` 로 부르거나 `cache/` 를 지웁니다.
- **Windows**: 경로에 공백이 있으면 따옴표로 감쌉니다. JSON 설정에서는 `\` 를 `\\` 로 씁니다.

## 8. 개발

```bash
uv run pytest            # 실호출 없는 고정 응답 테스트
uv run ruff check .
uv run python scripts/smoke.py   # 실호출 확인(키 필요 · 10회 안팎)
```

| 파일 | 무엇 |
|---|---|
| `src/mfds_mcp/server.py` | MCP 서버 · tool 등록 · 진입점 `mfds-mcp` |
| `src/mfds_mcp/tools.py` | tool 본체 · 입력 검사 · 취소 판정 |
| `src/mfds_mcp/client.py` | HTTP · 키 주입/가리기 · 에러 구분 · 페이지 |
| `src/mfds_mcp/cache.py` | 캐시 · 하루 호출 수 |
| `src/mfds_mcp/config.py` | `.env` · 환경 변수 |
| `NOTES.md` | 실호출 기록(필터 이름 · 대소문자 · 필드) |

키는 요청을 만드는 한 곳에서만 질의에 들어가고, `httpx` 로거는 WARNING 이상만 남기며(INFO 에 URL 전체가 찍힙니다), 에러에는 예외 클래스 이름과 상태 코드만 싣습니다.
