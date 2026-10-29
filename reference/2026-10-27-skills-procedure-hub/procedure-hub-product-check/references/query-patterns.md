# 질의 패턴 — 1단계에서 실제로 쓴 호출

원본 기록: `reference/2026-10-27-mfds-mcp/NOTES.md` · `reference/2026-10-28-kpic-mcp/NOTES.md`.
키는 `reference/2026-10-27-mfds-mcp/.env` 의 `MFDS_API_KEY` — 읽기만, 출력 · 커밋 금지.
질의는 「질의 → 건수」로 전부 행의 `evidence` · `recheck.queries` 에 남긴다(0건도).

## 1. 식약처 API (MFDS MCP tool)

| tool | 입력 | 쓰는 곳 |
|---|---|---|
| `mfds_status` | `refresh?` | 먼저 부른다 — 키 · 서비스 상태 · 오늘 호출 수 |
| `mfds_device_search` | `type_name`(모델명 · 부분 · **대소문자 구분**) · `entrps`(업체 · 부분) · `prduct`(품목 일반명칭) · `include_cancelled` · `all_pages` | 이름 · 모델 · **업체 단위 전체 목록**. 브랜드는 모델명에 있을 때만 걸린다 |
| `mfds_device_detail` | `prmisn_no`(「제허 14-1422 호」 — 띄어 쓴 API 표기) | 허가 한 건 — 취소(`RTRCN_DSCTN_DIVS_CD/DT`) · `MDEQ_PRDLST_SN`(emedi 상세 키) · `USE_PURPS` · `MANUF_NM` |
| `mfds_device_company` | `name`(업체 일부) | 업체가 제조업 / 수입업인지 · 휴폐업 |
| `mfds_drug_search` | `item_name` · `entp_name`(소문자 필터 · 부분) · `include_cancelled` | 의약품 — `ITEM_SEQ` · 영문명 · 업체 원어명 · `CANCEL_NAME/DATE` |
| `mfds_drug_detail` | `item_seq` · `include_ingredients?` | 규격(`MATERIAL_NAME` · `PACK_UNIT`) · 효능 · 위탁 제조원. 품목명에 「(수출용)」 |
| `mfds_dur_check` | `kind` · `item_name`/`item_seq` | 1단계에서는 안 씀(안전 엣지는 8단계) |

함정(실호출로 확인):
- 의료기기 **목록** API 는 소문자 필터(`prduct` · `entrps`), **상세** API 는 대문자(`TYPE_NAME` · `ENTRPS`)만 먹는다. 틀리게 보내면 **에러 없이 필터가 무시**되고 전체 건수가 나온다 → `total_count` 로 확인 (MCP 가 처리함)
- 0건이면 응답에 `items` 키가 없다
- 품목명(`PRDUCT`)은 「조직수복용생체재료」 같은 일반명칭 — 브랜드로는 안 걸린다
- `MANUF_NM` 표기가 갈린다(「Inc.」 / 「, Inc.」)
- 틀린 키는 403 `SERVICE_KEY_IS_NOT_REGISTERED_ERROR` — 미등록과 구분 안 됨
- 한도: 오퍼레이션당 일 10,000회(MCP `MFDS_DAILY_LIMIT`)

## 2. emedi (의료기기 전자민원) — API 에 없는 칸

### 품목 검색 목록 — `POST https://emedi.mfds.go.kr/search/data/list`

먼저 `GET https://emedi.mfds.go.kr/search/data/MNU20237` 로 쿠키를 받고, form 으로:

```
<field>=<값>  &tabGubun=1&chkList=1&pageNum=<p>&nowPageNum=<p>&searchYn=true(1쪽만)&searchOn=Y&grade=0&indtyCd=
```

| field | 무엇 |
|---|---|
| `query2` | 제품명 / 품목명 / 모델명 **전체** 검색 — 이름 · 영문 · 모델 변형을 여기로 |
| `entpName` | 업체명 — **업체 단위 전체 허가 목록**(수입사 교체 · 내수 허가 재탐색) |

응답은 HTML 표 — 행마다 칸 28개 이상. 1단계 파서가 쓴 칸 번호: 2 업체 · 3 품목 · 4 허가번호 · 6 상태 · 7 취소 ·
9 제품명 · 10 모델명 · 11 허가일 · 12 품목일련번호 · 15 업종 · 24 제조국 · 25 제조원 · 27 영문. 한 허가가 모델 수만큼 여러 행.
「총 N」 으로 전체 건수 확인 후 페이지 순회.

### 품목 상세 — `POST https://emedi.mfds.go.kr/search/data/item`

헤더 `X-Requested-With: XMLHttpRequest` · `Content-Type: application/json;charset=utf-8` · `Referer: …/MNU20237`. 본문:

```json
{"chkGroup1":"","meddevItemSeq":"<품목일련번호>","typeName":"","isUdiCodeSearch":"N","udidiCode":"","udiIsFirst":"Y","searchUdiCode":"","seq":"","seqGroup":""}
```

`mebItemInfo` 에서 본다:

| 칸 | 값 (10-28 실호출) |
|---|---|
| `xprtppYn` | 「예」 = 수출용에 한함(품목 단위) · 「아니오」 = 내수 |
| `remark` | 「수출용에 한함」 · 「동일제품(수허14-2649호)」 등 |
| `cancelwithdwCode` · `cancelwithdwDate` | 「아니오」 / 「취소」 / 「취하」 + 날짜 |
| `validDate` | 「2020-10-08 ~ 2028-04-30」 — 끝 날짜가 오늘 이전이면 만료 |
| `mebTypeName` · `brandName` · `usePurpose` · `manufReqName` | 모델 · 브랜드 · 사용목적 · 제조원 |

`meaCompanyInfo.cobFlagName` = 제조업 / 수입업.

## 3. KPIC (약학정보원) — 의약품만

`reference/2026-10-28-kpic-mcp/` (검색 수정본 · 실행 `node dist/index.js` · 실호출 `node scripts/probe.mjs …`)

| tool | 입력 | 쓰는 곳 |
|---|---|---|
| `search_drugs_by_name` | `{ drugname }` | 한글 · 영문 제품명(부분 일치 — 「라이넥」 1위가 라이넥스나잘스프레이) |
| `search_drugs_by_ingredient` | `{ ingredient }` | 성분 → 제품 역조회(정확 → 부분 폴백). 이소트레티노인 49건 · 데옥시콜산 11건 |
| `get_drug_detail_by_id` | `{ drugcode }` | ATC · KPIC 약효 · 보험(급여가 · 심평원 코드 / 비급여) · 허가일 · 취소일 |

- 의료기기는 안 된다. 식약처와 같은 원천이라 식약처 0 을 뒤집지 못한다(리포린 · 벨카이라 · 아큐탄 오리지널)
- 수출용 판정은 **식약처 품목명** 기준, KPIC 제품명은 보조(제테마더톡신 200U — KPIC 「(수출용)」은 변경 전 이름)

## 4. 국내 유통 · 해외 공식

| 출처 | 무엇 | 예 |
|---|---|---|
| 피부과 · 병원 홈페이지 · 비급여표 | 국내에서 실제로 쓰나 | 데이뷰의원 · 세라미크의원 |
| 병원 가격 자료 `/Users/kknaks/Downloads/data-anyang`(read-only) | 가격표 항목 이름 · 수집일 | 알라딘필링 4곳 |
| 제조 · 수입사 공식 | 모델 구성 · **허가번호 표기** | 젠틀맥스 공식 18-338 · Sciton 브로슈어 · classys IR |
| 보도 | 수입 · 유통 · 허가 소식 | 라라젯 2026-09 유통 보도 |
| FDA(Purple Book · 510k) | 성분 공식명 · 장비 등급 — **국내 허가 증거 아님** | BLA 125274 · K233766 |

URL 없이 칸을 채우지 않는다.
