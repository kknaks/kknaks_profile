# [backend] 데이터 판 구현 보고 — WORK-015 WP ① ~ ④

- 작업: concern_site 보강(7고민 8행 · 근거 19행) + 그림 데이터(silver 표 2 → DB 테이블 2 · 에셋 103) · 재빌드 한 번 · 로컬 DB 재적재
- 허브 HEAD `3a5da4a` 위 · **커밋 0** · 18105 안 건드림(GET 만) · 18107 띄웠다 내림
- 시험은 WP 마다 그 WP 것만(전체 pytest 0)

## 0. 결과 한눈

| WP | 결과 |
|---|---|
| ① silver | concern_site 95 → **103**(고민 92 · 부위 52) · source_ref 48,094 → **48,113** · `concept_image` 103 · `concept_image_label` 787 · silver **59표 · 67,853행** · silver-check G3 밖 FAIL 0 · WARN 0 · I1 ~ I5 통과 · `--negative` I 다섯 「잡음」 · 새 `silver_sha256` `07ee9495…2638ac38` |
| ② gold | gold 16 파일 **바이트 불변** · `gold_hash` `8accbb21…f6228c` 그대로 · gold-check A1 · A3 · V1 · H1 · K · M · Q 통과(A2 · G1 만 git 필터) · 구조 문제 0 · 역검증 둘 잡음 |
| ③ 허브 | 계약 상수 · 모델(76) · revision `b202611170002` · 적재기 V13 · `LOADER_VERSION` 0.2.0 · 에셋 SVG 103 + README · ruff 통과 |
| ④ DB | alembic +2 왕복 · dry-run · 적재 exit 0(76 테이블 · 130,446행 · 약 3초) · 18107 health · 실물 3 파일 97 passed |

## 1. WP-1 silver

### 사본
`$SM/archive/silver-before-data-v07/` — silver 57 · gold 16 · notes 4 · scripts 7 = **84 파일** · 사본 때 `silver_sha256` = `2471b2f1e04cb0b3a3a2068523e6223920621b39acadc14f78b749e1cffc6918`(check-stats 값과 같음).

### 고친 · 만든 것(`$SM`)
| 파일 | 무엇 |
|---|---|
| `gold/silver-supplement.py` | **5번째 단계** — 상수 `CONCERN_SITE_ADD`(8행 · 경로 19 · WORK §3-2 표 그대로) · 쓰기 전 확인(중복 0 · 사전 코드 · `resolve()` 19/19 글자) · `concern_site.csv` = 기준 바이트 + 8줄 · `source_ref.csv` 덧붙임 맨 끝 + 19줄 · 끝 줄 `concern_site +8 · source_ref +19` |
| `gold/silver-image.py`(새) | 인자 꼴 `[--seed <시드>] [<출력 폴더>]`(시드 기본 = env `SILVER_IMAGE_SEED` → 프로필 `reference/2026-11-17-procedure-images`) · 출력 폴더를 주면 `<폴더>/silver` 에만 · K1 ~ K6 · BOM · `\n` · 재현 같은 바이트 |
| `drafts/glossary/schema-edit.py` → `silver-schema.json` | 층 ⑤ 매체 · 두 표 · docs 키 `image` · vocab 3칸(스크립트 안에 넣음 — 손 편집 0 · 다시 돌려 같은 결과) |
| `drafts/silver-check/silver-check.py` | ⑤ 는 D5 대상 밖 · I1 ~ I5(I5 = 임시 폴더 재현 · 시드 없으면 「건너뜀」) · LAYER_TEXT ⑤ · `--negative` I 다섯 · 머리말 59표 |
| `drafts/glossary/glossary-build.py` → `notes/vocabulary.csv` | 「번역 언어」 += `concept_image_label.lang` · 새 묶음 「그림 검수 상태」(뜻 = SPEC-007 §2-2 문장) · 「표 이름」 은 vocab 칸으로 자동 |
| `notes/silver-erd.md` · `silver-tables.md` | `--write-docs` 로만 |
| `notes/glossary.md` | §0 ⑤ 줄 · §4b 그림 · 그림 라벨(`CIM-` · `CIL-`) |
| `gold/gold-check.py` | A1(concern_site = 기준 + 8줄 CSI-0099~0106 · source_ref 허용 (concern_site, field 빈칸) 8 id · 표 목록 + 그림 2) · A3 대상 4 파일 · docstring |

### 확인
- IS1: 바뀐 기존 파일 = `concern_site.csv` · `source_ref.csv` 둘뿐(55 파일 사본과 바이트 같음) · 앞쪽 바이트 불변(prefix) + 8줄 / + 19줄 · 두 스크립트 두 번 돌려 같은 바이트(임시 폴더).
- IS2(스크래치 폴더 사본): K1 코드 중복 · K2 kind 뒤집음 · K3 SVG 1바이트 · K4 `production_status` · K5 `ko` 빈칸 · K6 `;` → **6 / 6 exit 1 · 출력 폴더 안 생김**.
- IS3: `silver-check.py --write-docs` · `silver-check.py`(따로 한 번 더) — 둘 다 **FAIL 99 = 전부 G3**(git 필터 · 산출물 밖 미추적 문서) · 그 밖 FAIL 0 · WARN 0 · G1 통과 · V3 통과 · I1 ~ I5 통과 · `--negative` PASS(놓침 0 · 54 기준) · `glossary-build.py --check` PASS.
- 키 접두어(N-5): 스키마 id_pattern 접두어 57종 · 겹침 0 · `CIM` · `CIL` 새로.

## 2. WP-2 gold
- `gold-build.py` → gold 16 파일 사본과 **바이트 같음** · `gold_hash` = `8accbb213ac5327d8675f8156bc57d87c12a3245c383c8239074444da7f6228c`(불변 · 멈출 일 없음).
- `gold-check.py`: A1 · A3 · K1 ~ K7 · M1 · V1 · Q1 · H1 통과 · 구조 문제 0 · FAIL = A2 1(silver-check 끝 줄이 G3 탓 「FAIL 99」) + G1 99(git 필터).
- 역검증(임시 사본 · 하네스로 a1 · a3 만): 9번째 줄 → A1 「기준 바이트 + 끝 8줄 아님」 · 상수 1행 뺀 사본 → A3 「source_ref · concern_site 재현 다름」 · 원래대로 둘 다 통과.

| 값 | 앞 | 뒤 |
|---|---|---|
| `gold_hash` | `8accbb21…f6228c` | 같음 |
| `aux_hash`(허브 `combined_hash` 식으로 셈 · dry-run 이 같은 값) | `6435fe41f3851574729ef7aa7e108afb5cf7601c1764c160496a9e49aa1803a3` | **`93ec89fdd7d66781cdf18025c4698cc31a543fe252ebb1f16948fc0876ae0eeb`** |
| `concern_site.csv` sha | `93c921ae…` | `003d89fa…` |
| `source_ref.csv` sha | `afc28636…` | `d09e9d26…` |
| `concept_image.csv` · `concept_image_label.csv` | — | `a9e41fc0…` · `ca5f15ff…` |
| silver 폴더 해시 | `2471b2f1…` | `07ee9495…` |

## 3. WP-3 허브(`git status` — 수정 16 · 새 3)
`backend/app/modules/gold/{silver_contract,config,medallion_load,db_inputs}.py` · `backend/app/model/{medallion,__init__}.py`(`__init__` 은 주석 수 74 → 76 한 줄) · `backend/scripts/load_medallion.py` · `backend/README.md` · `backend/envs/.env.example` · 새 `backend/alembic/versions/b202611170002_medallion_concept_image.py` · 시험 `tests/{medallion_fixture,test_medallion_model,test_medallion_load,test_medallion_repo}.py` · 새 `tests/test_medallion_image.py` · 실물 기대값 `tests/{test_gold_holes,test_gold_v07_site,test_gold_v07_descend}.py` · 새 `assets/procedure-images/`(SVG 103 + README).

- V13: env 있으면 표 경로 집합 = 폴더 `images/**/*.svg` 집합을 먼저 보고(표 값으로 폴더 밖을 열지 않음) 같으면 sha256 · 어긋나면 exit 2 · env 없으면 `image_files unchecked(GOLD_IMAGE_DIR 없음)` · dry-run 에서도 돈다. `loaded tables` 를 상수 74 → 실제 수로.
- 에셋: `$I` 에서 `(MEC|MET)-\d{3}\.svg` 만 · 54 + 49 · 6,886,445 바이트 · sha 103 / 103 일치 · `.dockerignore` · `.gitignore` 안 고침.

시험(그 WP 것만):
| 명령 | 결과 |
|---|---|
| `uv run ruff check app tests scripts` | All checks passed |
| `pytest tests/test_medallion_{model,load,repo,image}.py` | **80 passed · 1 skipped**(실물 헤더 대조 — silver env 없음) |
| W-2: `pytest tests/test_gold_{tools_synthetic,rest,mcp,v07_resolve}.py` | **261 passed · 1 skipped** |
| `uv run alembic heads` | `b202611170002 (head)` 하나 |

IT1(76 · 59 · 칸 764 · FK 83 · 유일 5 · 인덱스 30 · 이름 ≤ 63) · IT2(새 test — down · 옛 3 id · create_table 2 · 지연 FK 1 · 고정본 ↔ 모델 칸 · 제약 이름) · IT3(빌드 기록 76 · silver 54 · 그림 2표 되읽기) · IT4(V2 · V5 · V6 유일 둘 · NOT NULL · V7) · IT5(일치 · 바이트 · 빠짐 · 더 있음 · 폴더 없음 · env 없음 · dry-run DB 0) · IT6(DT15 에 그림 2표 안 읽음 단언 · files 22) · IT7(103 · 54 · 49 · README 만 · 금지 요소 0 · 바깥 주소 0 · viewBox 103).

빈 SQLite 에 `alembic upgrade head` 는 **원래 안 된다**(첫 revision 이 `CREATE EXTENSION pg_trgm` — 이번 변경과 무관). 빈 DB 확인은 CI(PostgreSQL) 몫 · 로컬 PG 왕복은 ④.

### W-1 — 실물 기대값(시험 전에 재셈 · 옛 → 새)
재셈 두 가지: ⓐ 표준 라이브러리 스크립트(CSV 만 — 집합 셈) ⓑ 허브 서비스를 CSV 판으로 세워 같은 정의로 부르는 스크립트(시험 파일 import 0). **둘 다 앞(사본 silver) 값이 지금 시험의 수와 전부 같았다** → 스크립트 확인 뒤 뒤 값으로 고침.

| 자리 | 옛 | 새 | 셈 |
|---|---|---|---|
| `test_gold_holes.py` T1 행 · aux3 규모 · health | 95 · 85 · 51 | **103 · 92 · 52** | ⓐ |
| `test_gold_v07_site.py` applied | filter 191 · prefer 22,949 | **200 · 22,940** | ⓐ |
| 같은 곳 filt_kind · 거르는 고민 | 95 · 96 · 100 | **103 · 97 · 106** | ⓐ |
| unbound | 14,240 · 14,008 · 646 · 232 | **13,706 · 13,477 · 673 · 229** | ⓐ pairs · ⓑ 나머지 |
| outside | 8,709 · 8,444 · 971 · 265 | **9,234 · 8,969 · 966 · 265** | ⓐ pairs · ⓑ 나머지 |
| 표지 합 · 표지 짝 합 | 1,617 · 497 | **1,639 · 494** | ⓑ |
| zero_auto 5 · inherited 9 · inherited_bound 4 | — | 그대로 | ⓑ |
| `test_gold_v07_descend.py:283` | (100, 85, (23, 18)) | **(106, 92, (23, 18))** | ⓐ |
| `test_gold_holes.py` T22 pairs · zero_col · zero_col − stay | 97 · 40 · 37 | **99 · 41 · 38**(주석 91 → 99) | ⓑ |
| T22 stay 3 · over 4(CSI-0007 · 0047 · 0079 · 0083) · e2e CON-001 × SITE-014(73 · 16 · 24 · 54) | — | 그대로 | ⓑ |

- **SPEC-001 되적기 후보**: 0.7.2 「표지 1,617 = 646 + 971」 → 보강 뒤 **1,639 = 673 + 966**(짝 497 → 494). T22 의 97 · 40 · 37 도 99 · 41 · 38. WORK §5-3 · 검수 W-1 표 밖이던 T22 수는 위처럼 재셈으로 고쳤다.
- SP 재셈(코디 (마)용 · CSV 판 ⓑ): 흉터 + 볼(CON-140 × SITE-051) = prefer 113행 · 묶음 40 · sites 0 · CON-193 × SITE-103 = **filter 6 · 묶음 4**(앞 prefer) · CON-193 × SITE-110 = prefer 6.

## 4. WP-4 DB 재적재(로컬 `127.0.0.1 18432 phub_medallion`)
- ⓪ 앞: `b202611170001` · public 242 · 빌드 기록 74(0.1.0 · aux `6435fe41` · gold `8accbb21`).
- **⚠ 사고 1건**: 첫 왕복을 셸 반복문으로 돌리다 인자 따옴표 탓에 `upgrade head` 가 안 돌고, 뒤따른 `downgrade -1` 이 **`b202611170001`(74 테이블)을 내렸다** — 옛 판 데이터가 지워지고 `upgrade head` 로 76 테이블이 빈 채 다시 섰다(b202610300001 → 0001 → 0002). 곧바로 적재로 채웠다(전체 교체라 결과는 같다). 그 사이 18105 는 메모리 판이라 영향 없음. 되돌릴 일이 생기면 코디 dump `medallion-pre-v07data-20261117.dump` 가 그 앞 판이다.
- ① IE1: `alembic check` 차이 0 · `downgrade -1` → public 242(241) · `upgrade head` → 244(243) · `check` 다시 0.
- ② IE2 dry-run(exit 0 · DB 접속 0): `gold_hash` = 기대 · `aux_hash` = **`93ec89fd…6ae0eeb`(WP-2 셈과 같다)** · `tables 76 · rows 130,446 (data 130,097 · ledger_check 273 · build 76)` · `s_concept_image` 103 · `s_concept_image_label` 787 · `s_concern_site` 103 · `s_source_ref` 48,113 · poly_unresolved 16 줄 전부 0 · `image_files 103 checked`.
- IE3 적재: exit 0 · `loaded tables 76 · rows 130446 · insert_ms_total 1469.0`(벽시계 2.95초) · 빌드 기록 76행 · `load_medallion 0.2.0` · silver kind 54 · aux_hash 한 값 · 되읽기(L5) · 커밋(지연 FK) 통과.
- IE4 SQL: 그림 코드 103 = mechanism ∪ method(빠짐 0 · 남음 0) · 라벨 없는 그림 0 · 그림 없는 라벨 0 · 새 8 id(CSI-0099 ~ 0106) · concern_site 103 / 92 / 52.
- ③ IE5 18107(DB 판 · 띄우기 전 lsof 빔): `gold_hash` 불변 · `aux_hash` 새 값 · `files[]` 22 · `aux.concern_site` = 103 · 92 · 52 · 열쇠 집합 = 18105 health. 조회: 턱살 CON-168 → total 0 · descended M18 · sites SITE-072(CSI-0054) / 볼 + 탄력 저하(CON-048 · `site=볼`) → prefer 105행 · 묶음 55 / 흉터 + 볼(CON-140) → prefer **113행** · 묶음 40 · sites [] — 셋 다 18105(옛 판) 응답과 build 빼고 같다 · CON-193 + 허벅지 → filter 6 · 묶음 4. **18107 내림**(lsof 0 · 프로세스 0).
- ④ 실물 pytest(`GOLD_REPOSITORY=db` · PG): `tests/test_gold_holes.py tests/test_gold_v07_site.py tests/test_gold_v07_descend.py` → **97 passed · skip 0**.

## 5. 커밋 후보 점검(§10)
`*.csv` · `*.dump` · `*.db` 0 · 에셋 54 · 49 · 그 밖 파일 0 · 비밀값 · 접속 문자열 grep 0 · 홈 경로 grep 0 · `main.py` · `core` · `.dockerignore` · `.gitignore` · `pyproject` · `uv.lock` · Dockerfile 변경 0 · 프로필 `_archive` 변경 = 코디 백업 폴더(미추적)만.

## 6. 남은 것 · 코디
- **18105 재시작(새 코드 · DB 판) · 37 키 대조 필요** — 기준 키 `data/eval-set/_v072_pre_data/` · 기대 = 행 37/37 같음 · `aux_hash` 만 다름. 18105 는 지금 옛 코드 · 옛 메모리(aux `6435fe41`).
- SPEC-001 되적기 후보: 표지 1,617 → 1,639(673 + 966) · 짝 497 → 494 · T22 97 · 40 · 37 → 99 · 41 · 38.
- 위 ⚠ 사고(옛 판 테이블을 한 번 내렸다 다시 올림) — 지금 DB 는 새 판이 정상 적재된 상태.
- silver-check G3 · gold-check G1 · A2 는 git 필터 탓(B-1 답대로 안 고침).
