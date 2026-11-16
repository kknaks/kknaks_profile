# KPIC MCP 검증 노트 (2026-10-28)

- 원본: https://github.com/antegral/kpic-mcp (HEAD `4a714a3`, v1.0.1, MIT)
- clone 위치: 이 폴더. 의존성 설치·빌드도 이 폴더 안에서만(`node_modules/`, `dist/` — 레포 자체 `.gitignore` 에 포함)
- 추가한 파일: `scripts/probe.mjs`(stdio 클라이언트 — tool 목록·검색·상세 덤프), 이 `NOTES.md`

## 결론

**10-28 2차: 검색을 고쳤다. 이제 search → detail 이 MCP tool 만으로 한 번에 된다.**

- `search_drugs_by_name` — health.kr 새 API `GET /api/searchDrug?drugName=` 로 교체(아래 「바꾼 곳」)
- `search_drugs_by_ingredient` — **새 tool.** 성분 → 제품 역조회
- `get_drug_detail_by_id` — 그대로(옛 `ajax_result_drug2.asp` 가 아직 살아 있음)
- 의료기기는 여전히 안 된다(약학정보원은 의약품 DB)

1차(검증) 때의 상태: health.kr 이 Next.js 로 개편돼 옛 ASP 검색 페이지가 `/searchResult` 로 301,
CSRF 토큰이 없어져 검색이 전부 `Failed to obtain CSRF token` 으로 실패했다.

## 바꾼 곳 (2차)

| 파일 | 변경 |
|---|---|
| `src/kpic-api.ts` | CSRF 세션(`fetchSearchSession`)·POST 검색 제거. `getJson()`(GET+파싱+에러 래핑) · `searchDrugPages()`(`/api/searchDrug` 페이지 순회 — 서버 상한 100건/쪽, 최대 5쪽=500건) · `toDrugSearchResult()`(새 항목 → 기존 형태) 추가. `search_drugs_by_ingredient()` 추가 |
| `src/types.ts` | `DrugSearchResult` 에 `cls_name`·`dosage_route_name`·`boh_code` 추가. 새 API 응답 타입 `SearchDrugItem`·`SearchDrugPage`·`IngredientItem`·`IngredientPage`, 결과 타입 `IngredientSearchResult` |
| `src/index.ts` | tool `search_drugs_by_ingredient` 등록·핸들러 |
| `src/__tests__/kpic-api.test.ts` | 검색 테스트를 새 API mock 으로 교체, 페이지 순회·성분 검색(정확→부분 폴백, 성분 없으면 제품 검색 안 부름) 추가 — **18/18 통과**, lint 통과 |
| `scripts/probe.mjs` | 검색 → 첫 결과 상세까지 MCP 로 잇는 실호출 스크립트 |

출력 형태: 기존 `DrugSearchResult` 필드를 그대로 유지한다. 새 API 에 없는 `effect`·`dosage` 는 빈 문자열
(상세에 있음), `total_cnt` 는 이번 결과 건수, 옛 `cls_code` 자리에는 분류명(`cls_name` 과 같은 값).
`drug_code`·`drug_name`·`upso_name_kfda`(업체)·`list_sunb_name`(성분)·`drug_class`(전문/일반)·
`cls_name`(분류)·`kfda_code`·`boh_code`/`boh_price` 가 채워진다.

성분 검색: `/api/ingredient?keyword=&match=1`(정확 일치) → 없으면 `match=0`(부분 일치, 최대 5개 성분)
→ 성분마다 `/api/searchDrug?ingdcode=`. 결과는 `[{ ingd_code, ingd_name, ingd_ename, match_type, drug_count, drugs[] }]`.
성분이 하나도 없으면 제품 검색을 부르지 않는다(모르는/빈 필터면 서버가 전체 44,741건을 주기 때문).

## 보안 검토

| 항목 | 결과 |
|---|---|
| 네트워크 호스트 | `https://health.kr` **하나뿐** (`src/kpic-api.ts` `BASE_URL` — 2차 수정 후에도 같음). 응답 안 이미지 URL 은 `common.health.kr` 이지만 서버가 받으러 가지 않는다 |
| 키·토큰 | 요구 없음. (1차 원본의 세션 쿠키·CSRF 처리는 2차에서 제거 — 새 API 는 쿠키 없이 GET) |
| 로컬 파일 읽기/쓰기 | 없음(`fs` 미사용) |
| 셸 실행 | 없음(`child_process` 미사용) |
| 텔레메트리·외부 전송 | 없음. stdout 은 MCP stdio, 로그는 stderr 한 줄 |
| 런타임 의존성 | `@modelcontextprotocol/sdk ^1.26.0`, `zod ^3.23.8` 두 개 |
| lockfile | 전부 `registry.npmjs.org` · integrity 해시. install 스크립트 있는 건 `fsevents`(옵션) · `uglify-js`(dev) 둘 — 그래도 `--ignore-scripts` 로 설치함 |
| 기타 | `.github/workflows/` 는 CI·CodeQL·npm publish — 로컬 실행과 무관 |

의심스러운 것 없음 → 설치·실행 진행.

## 설치 · 실행

```bash
cd reference/2026-10-28-kpic-mcp
pnpm install --frozen-lockfile --ignore-scripts   # node 20.20, pnpm 8.15
pnpm build                                        # → dist/
node dist/index.js                                # stdio MCP 서버
node scripts/probe.mjs --tools                    # tool 목록
pnpm test                                         # 18/18
node scripts/probe.mjs 디스포트 티엠버스          # 제품명 검색 → 첫 결과 상세
node scripts/probe.mjs --ingredient 데옥시콜산    # 성분 검색 → 첫 제품 상세
node scripts/probe.mjs --detail A11AGGGGG7051     # 상세만
```

## tool 목록

| tool | 입력 | 하는 일 | 상태 |
|---|---|---|---|
| `search_drugs_by_name` | `{ drugname: string }` (필수) | 제품명(한글·영문, 부분 일치) → `drug_code`·제품명·업체·성분·분류·보험코드 목록 | ○ (2차 수정) |
| `search_drugs_by_ingredient` | `{ ingredient: string }` (필수) | 성분명(한글·영문) → 성분별 제품 목록 | ○ (2차 신설) |
| `get_drug_detail_by_id` | `{ drugcode: string }` (필수) | 상세 — 성분·업체·`atc_cd`·`kpic_atc`(약효 트리)·`boh`(보험가/「비급여」)·`boh_hiracode`·허가일·취소일·효능·용법·주의·DUR·첨가제 | ○ |

## 실호출 재검증 (10-28 2차 — MCP stdio, search → detail)

`node scripts/probe.mjs …` 로 MCP tool 만 써서 검색하고, 그 결과의 `drug_code` 로 상세를 불렀다.

| 대상 | tool | search | → detail |
|---|---|---|---|
| 디스포트 | name | 1건 `A11AGGGGG7051` 디스포트주 · 입센코리아 · toxin A–HA complex 500U · 독소류 · boh `681400011` 179,792원/병 | ATC M03AX01 · 179792원/1병 · hira 681400011 · 허가 1999-07-13 ○ |
| 티엠버스 | name | 2건 100단위 `2025040100014`·200단위 `2025091700003` · 종근당바이오 · toxin A · 독소류 | 100단위: M03AX01 · 비급여 · 허가 2025-03-31 ○ |
| 라이넥 | name | 5건 — 1위는 라이넥스나잘스프레이(삼일, 모메타손 — 부분 일치), 라이넥주 `A11AOOOOO6804`·바이알·피오정/캡슐(수출용) · 녹십자웰빙 · 장기제제 | 라이넥주: A05BA 간 치료제 · 비급여 · 허가 2005-04-13 ○ |
| 콘투락투벡스 | name | 1건 `A11AOOOOO9487` 콘투락투벡스겔 · 메디팁 · Allantoin 10mg/g · 일반 | D03AX 흉터 치료제 · 비급여 · 허가 2001-04-06 ○ |
| 리포린 | name | 1건 — 글리포린정2/500mg(당뇨, 부분 일치)만. **리포린 제품 없음** | (글리포린) A10BD02 — 무관 |
| 이소트레티노인 | ingredient | 성분 `I005045` exact · 제품 49건(니메겐·레씨범·로이탄·이소티논… 수출용 포함) | 니메겐연질캡슐: D10BA01 · 305원/캡슐 · hira 646000210 ○ |
| 데옥시콜산 | ingredient | 성분 `I007305` exact · 제품 11건 — 밀리핏·바이블·벨라콜린·브이렛·브이벨라·브이올렛·올리핏·원더브이·펜카이라 + 인포리바·토니바(수출용 비타민 복합제, 첫 성분이 Ascorbic Acid 로 표시) | 밀리핏주사: D11AX24 · 비급여 · 허가 2025-07-25 ○ |

주의: 제품명 검색은 부분 일치라 짧은 이름은 엉뚱한 1위가 나온다(라이넥 → 라이넥스, 리포린 → 글리포린).
결과 목록에서 이름을 골라 상세로 가야 한다.

## 실호출 기록 (10-28 1차 — 검증, 검색은 새 API 를 curl 로 직접)

검색은 새 API `GET https://health.kr/api/searchDrug?drugName=<q>` · 성분별은
`?ingdcode=<성분코드>`(성분코드는 `GET /api/ingredient?keyword=<영문성분>&match=0&hasDrug=1`).
상세는 MCP `get_drug_detail_by_id`.

| 대상 | 결과 |
|---|---|
| 리포린(삼익제약) | **없음.** 「리포린」·「리포린주」·「Liporin」 → 글리포린정(당뇨약)만. 데옥시콜산 성분 제품 11건에도 없음 → 식약처 0 과 같음 |
| 벨카이라 / 카이벨라 | **없음**(한글·Kybella·Belkyra 모두 0). 데옥시콜산(`I007305`) 국내 제품은 11건 — 벨라콜린주(엘지화학, 2024-01-25), 브이올렛주(대웅, 2021-08-06), 올리핏주(휴메딕스), 바이블주(한국비엠아이), 밀리핏주사(동국), 브이렛주(코오롱), 원더브이주(종근당), 펜카이라주(펜믹스), 브이벨라주(대한뉴팜, 2026) 등. 상세: ATC `D11AX24` · KPIC 피부/피하조직질환>기타 · 「대사성 의약품」 · 비급여 · 턱밑지방 개선 |
| 아큐탄 | **제품명으로 없음**(아큐탄·로아큐탄·Roaccutane 0 — 오리지널 국내 미유통). 성분 이소트레티노인(`I005045`) 49건 — 이소티논(한미)·트레틴(코오롱)·제로큐탄·로이탄 등. 상세(이소티논10mg): ATC `D10BA01` · KPIC 여드름 치료>비타민A 제제 · 270원/캡슐 · 심평원 `643502190` · 허가 2003-10-31 |
| 컨트라투벡스 | 한글 표기는 **「콘투락투벡스겔」**(메디팁, `A11AOOOOO9487`). 성분 Allantoin 10mg/g(+Heparin 분류 함께) · ATC `D03AX` 흉터 치료제 · 일반 · 비급여 · 허가 2001-04-06 · 흉터·켈로이드 |
| 라엔넥 | 한글 표기는 **「라이넥주」**(녹십자웰빙, `A11AOOOOO6804`). Human Placenta Hydrolysate · 장기제제 · ATC `A05BA` 간 치료제 · 비급여 · 허가 2005-04-13 · 「만성 간질환 간기능 개선」(미용 적응증 없음). 바이알·피오정/캡슐(수출용)도 있음 |
| 디스포트 | 디스포트주(입센코리아, `A11AGGGGG7051`). Clostridium Botulinum Toxin Type A–Haemagglutinin Complex 500U · 독소류 · ATC `M03AX01` · KPIC 근이완제>말초성 · **급여 179,792원/병, 심평원 `681400011`** · 허가 1999-07-13 · 적응증에 성인 미간주름 포함. 「abobotulinumtoxinA」 영문 검색은 0 — 성분명이 INN 이 아니라 위 표기 |
| 티엠버스주 | 100단위(`2025040100014`, 허가 2025-03-31)·200단위(`2025091700003`) — 종근당바이오. Botulinum Toxin Type A · 독소류 · ATC `M03AX01` · 비급여 · 미간주름 |
| 셀엑소좀 (의료기기) | 0 — 의료기기 미수록 |
| 모르페우스8 (의료기기) | 0 — 의료기기 미수록 |

## 할 수 있는 것 / 없는 것

**된다**
- 식약처 허가 의약품의 한글 제품명·영문명·주성분 함량·업체·제형·투여경로·허가일·취소일
- 분류 세 갈래: 식약처 분류(`cls_code`), ATC(`atc_cd`), KPIC 약효 트리(`kpic_atc`)
- 보험: 급여면 보험가 + 심평원 코드, 아니면 「비급여」
- 성분 → 제품 목록 역조회(새 API `ingdcode`). 식약처 MCP 에서 성분으로 못 찾은 국내 동일성분 제품을 찾는 데 쓸모가 있다
- 외래어 표기가 식약처 등록명과 다를 때(컨트라투벡스→콘투락투벡스, 라엔넥→라이넥) 영문명 검색으로 찾힘

**안 된다**
- 의료기기(장비·필러 중 기기 허가품·엑소좀 화장품 등)
- 미허가·미유통 제품(리포린·벨카이라·아큐탄 오리지널) — 식약처와 같은 원천이라 식약처 0 을 뒤집지 못한다

## 고치는 법 → 2차에서 적용함(사용자 승인 10-28)

이 사본에서만 고쳤다. 원 레포(antegral/kpic-mcp)에는 PR 을 보내지 않았다.

⚠ `/api/searchDrug` 는 모르는 파라미터를 주면 필터 없이 전체(44,741건)를 돌려준다 — 파라미터는
`drugName`·`ingdcode` 두 개만 쓴다.

## 등록 명령 (실행하지 않음)

사용자 설정은 건드리지 않았다. 등록하려면(먼저 `pnpm build` 로 `dist/` 가 최신인지 확인):

```bash
# 전역(user)
claude mcp add kpic --scope user -- node /Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-28-kpic-mcp/dist/index.js
# 또는 이 프로젝트만
claude mcp add kpic --scope project -- node reference/2026-10-28-kpic-mcp/dist/index.js
```

## 커밋 시 주의

- **커밋 전 처리 필요.** 이 폴더에 clone 의 `.git/` 이 그대로 있다(2차 수정분은 그 clone 의 작업 트리 변경으로만 있음, 커밋 안 함) — 부모 레포에 `git add` 하면 embedded repo(gitlink)로
  잡힌다. 소스째 올릴 거면 `.git/` 을 지우고, 안 올릴 거면 부모 `.gitignore` 에 이 폴더를 추가
- `node_modules/` · `dist/` 는 레포 자체 `.gitignore` 로 제외된다
- 키·`.env` 없음
