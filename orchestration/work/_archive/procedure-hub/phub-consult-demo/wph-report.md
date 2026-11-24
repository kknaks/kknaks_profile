# WP-H 리포트 — 허브 칸 셋(method_codes · method_texts · country)

- 정본: `SPEC-010-consult-myeongdong.md` 0.2.2 §13 WH1 ~ WH7 · D-12 · 검수 r2 N1 · r5
- 날짜: 2026-11-20 · 커밋 0 · push 0 · stg / 원격 DB 0 · 18105 · 18222 손대지 않음(18105 는 GET 도 안 함 — 회귀 ③ 은 같은 코드를 프로세스 안에서 돌려 대조)

## 1. 새 해시 · JSON

| 항목 | 앞 판 | 새 판 |
|---|---|---|
| 허브 `build.gold_hash`(gold 폴더 CSV 16 — 허브 `combined_hash`) | `57b420ad10d34ff7d3764fd7afbf7d1d731b1d27a1d29984d011d3a61586ec44` | **`caa035606b1fd99e0431628064a3f9b171d1592468f223ac88c45c429573ee78`** |
| 허브 `build.aux_hash` | `51e3760a82df45de2011b59868a723532af9c7732163e1eee31472ceb8a93b34` | 같음(silver 0 바뀜) |
| `gold-build.py` 출력 「gold 해시」(빌드 스크립트 자체 셈 — 허브 값 아님) | — | `8d741bc5…` |
| 매핑 JSON v3 `myeongdong-mapping-20261120-v3.json` sha256 | `94b88022973805bbdc4b2350972e1e99e61a501e058062dc54753287440643f4` | **`1af2216c5a3ed2806936777314ad4fbdc1ca8e70b78fee99ad387ac5f0e26568`** |

- gold-check 의 H1 줄 「gold 해시 caa03560…」 = 허브 값과 같다.
- JSON(WH5): `build_mapping_json_v3.py caa03560… 51e3760a… <out>` → 두 경로에 같은 바이트로 둠(앱 워크트리 `clinic_chat/phub-consult-demo/data/kos/` · 메인 로컬 `~/git/clinic_chat/data/kos/` — 둘 다 git 무시).
  - items · groups · sites · products · product_categories 다섯 덩이 바이트 같음(직렬화 대조 True × 5) · 최상위 키 · meta 키 순서 같음.
  - `diff` = 두 줄뿐: `meta.hub_gold_hash` 57b420ad → caa03560 · `meta.made_at` 16:11:30 → 16:51:06(+09:00).
  - 앞 판 백업: scratchpad `v3-before-94b88022.json`.

## 2. 바뀐 파일

### 작업 사본(`$W/silver-model/gold/` — git 밖 · 앞 판 23 파일은 scratchpad `gold-before/` 에 복사)

| 파일 | 바뀜 |
|---|---|
| `gold-build.py` | g_profile 헤더에 `method_codes` · `method_texts`(`methods` 뒤) · `country`(`organizations` 뒤). 행 조립은 그대로 두고, 표 끝에서 세 값을 끼워 넣는다 — 케이스 행: `case_method` 행 순서대로 code 를 `SEP`(` · `)로 · 같은 순서 `method.description` 원문을 `\n` 하나로 · 제품 행: `product.country` 원문 · 그 밖 빈칸. g_evidence 는 건드리지 않음(회귀 ① 때문) |
| `gold-check.py` | K4 원자 대조: `method_texts` 는 `\n` 으로 나눠 조각마다 silver 값인지 · 새 **K8**(WP-H 새 칸 셋): 행마다 다시 지어 대조(케이스 = case_method 순서 · 개수 같음 · 원문 이음 · 제품 = country 원문 · 다른 행 빈칸) + method 설명에 `\n` 0 · 코드에 SEP 0 |
| `g_profile.csv` | 재빌드 결과(881 행 · 칸 27 → 30) |

### 허브 워크트리(`$H` — 커밋 안 함 · `git diff --stat`: 3 파일 +42 −9 · 새 파일 1)

| 파일 | 바뀜 |
|---|---|
| `backend/app/modules/gold/headers.py` | `GOLD_HEADERS["g_profile"]` 에 세 칸(CSV 순서 그대로) · 새 상수 `PROFILE_EXTRA_COLUMNS = ("method_codes", "method_texts", "country")` — 정보 종류 셈(`OVERVIEW_COLUMNS` · `MECHANISM_COLUMNS`)과 `ATTR_MATCH` 에 **넣지 않음**(다른 동작 0 · WH3 `ATTR_MATCH["g_profile"]["method"] = ("methods",)` 그대로) |
| `backend/alembic/versions/b202611200001_g_profile_wph_columns.py`(새) | revision `b202611200001` ← `b202611170002` · `g_profile` 에 `add_column` 셋(Text · NULL 허용) · downgrade = `drop_column` 셋 · 앱 import 0 · 인덱스 · 제약 · FK 0 |
| `backend/tests/test_gold_contract.py` | T3: g_profile 헤더 = 식별 + 개요 + 원리 + **덧붙인 칸** · 덧붙인 칸이 셈 · 맞춤에 안 든다 · method 맞춤 = `("methods",)` 단언 · T3 attr 시험에서 덧붙인 칸을 뺌(이름에 method 가 들어도 맞춤 칸 아님) |
| `backend/tests/test_medallion_model.py` | 칸 합 278 → 281 · 764 → 767 · head = `b202611200001` · 새 시험 `test_wph_profile_columns_revision`(down · add/drop 셋 · Text NULL · 옛 고정본 g_profile 칸 + 셋 = 모델 칸) |

- 확인만(고칠 것 0): `facets.py`(응답 = `out_row` 가 행 dict 그대로 → 새 칸이 자동으로 실림) · `app/model/medallion.py`(칸 = `GOLD_HEADERS` 에서 기계로 · `:46` 은 유일키뿐) · 적재기 · DB 판 읽기(칸 이름으로 insert / select — DB 에서 새 칸이 끝에 붙어도 무방).
- 미추적 그림 18 파일(`assets/procedure-images/...`) 손대지 않음.

## 3. 시험

| 무엇 | 결과 |
|---|---|
| `gold-check.py` | **PASS** · FAIL 0 · 구조 문제 0 · K8 「채운 행 procedure_case.method_codes 387 · product.country 108」 · WARN 10 = 레포의 작업 사본 밖 변경(`.gitignore` 등 — 앞서부터 있던 것 · 데이터 아님) |
| 허브 `test_medallion_model.py` · `test_gold_contract.py`(합성) | 17 passed · 4 skipped |
| 허브 `tests/test_gold_*.py` + `tests/test_medallion_*.py` — **CSV 판 · 실물 gold env**(`GOLD_CSV_DIR=$S/gold` 등 · `DATABASE_URL` = 아래 버린 DB) | 452 passed · 11 failed · 12 skipped — 11 은 전부 앞서부터: 실물 수 고정 시험 9(`test_gold_real` T12 · T13 · `v07_descend` T24_T25 · `v07_site` T28 · `holes` T1_real_aux3 · aux3_scale_real · `gold_load` T1 둘 · integrity — 11-16 판 8accbb · 옛 셈에 묶임) + `test_medallion_image` it7 둘(미추적 그림 18 파일 때문 — 121 ≠ 103) |
| 기준선 대조 | HEAD 코드(`git archive`)를 scratchpad 에 풀어 **앞 판 gold(57b420ad)** 로 같은 다섯 파일을 돌림 → 같은 9 실패 · 실패 줄(파일:줄 · 단언 문구) `diff` = 소요 시간 한 줄만 다름. 이미지 둘은 HEAD 에셋(미추적 파일 없음)에서 통과 |
| 허브 DB 판(`GOLD_REPOSITORY=db`) — `test_gold_real` · `test_gold_rest` · `test_gold_mcp` | 110 passed · 2 failed(T12 · T13 — 위 기준선 실패와 같은 것) |
| alembic(로컬 시험 DB) | 로컬 컨테이너 `phub-medallion-pg`(18432) 안에 **버리는 DB `wph_tmp_20261120`** 를 새로 만들어: `upgrade head`(→ b202611200001 · 세 칸 text NULL 허용) → `downgrade -1`(칸 28) → `upgrade head`(칸 31) → `scripts/load_medallion.py`(`GOLD_EXPECTED_HASH=caa03560…`) 적재 성공 · 표 76 · 행 170,701 · `medallion_build` gold caa03560 / aux 51e3760a · DB g_profile 채운 행 case 387 · product 108 → 끝나고 DB 지움. 기존 `phub_medallion` DB 는 손대지 않음(여전히 b202611170002) |
| ruff(바뀐 허브 파일 4) | All checks passed |
| 0.4 앱 `test_consult_material.py`(앱 워크트리) | 6 passed |

## 4. 회귀(WH6) · 표본

| # | 조건 | 결과 |
|---|---|---|
| ① | `g_profile` 밖 gold 파일 바이트 같음 | **같음** — g_* 14 · `questions.csv` cmp 같음 · 다른 것은 `g_profile.csv` 하나 |
| ② | `g_profile` 의 기존 칸 값 같음 · 새 칸만 더해짐 | **같음** — 881 행 gid 순서 같음 · 기존 27 칸 다른 행 0 · 새 칸 채움 = case `method_codes` 387 · `method_texts` 387 · product `country` 108(빈칸 228 그대로) · 계열 · 시술 행 새 칸 0 |
| ③ | `facets profile node=method:<MET>` 응답 행 같음(표본 MET 3) | **같음** — MET-020(2) · MET-004(26) · MET-110(46): total · 행 gid 순서 · 새 칸 뺀 행 dict 전부 같음. 덤으로 node 7(CAS-013 · CAS-016 · CAS-1026 · PRD-001 · PRD-022 · PRD-358 · PRC-001)도 같음. 앞 판 = HEAD 코드 + 앞 gold · 새 판 = 이 워크트리 + 새 gold(같은 서비스 코드 프로세스 안 호출) |
| ④ | 0.4 앱 `test_consult_material.py` · 허브 gold 시험 | 6 passed · 허브 gold 시험은 §3(새 실패 0) |

케이스 표본(silver `case_method` 행 순서 = `method_codes` 순서 · 글 = `method.csv` 원문):

| 표본 | 케이스 | `method_codes` | `method_texts`(줄) |
|---|---|---|---|
| 방법 하나 | CAS-013 네페르티티 리프트 | `MET-020` | 「한 부위를 여러 점에 나눠 조금씩 주입한다. 점당 양은 케이스 칸.」 |
| 방법 둘 | CAS-016 | `MET-025 · MET-004`(silver CME 순서 MET-025 → MET-004) | 2 줄 — MET-025 「약제를 희석해 넓게 얇게 주입한다. 희석 비율·용량은 케이스 칸.」 / MET-004 「피부 안(진피)에 직접 주사한다. 메조테라피·스킨부스터·…」(원문 안 「·」 그대로) |
| 방법 둘(덤) | CAS-1026 물광주사 | `MET-020 · MET-004` | 2 줄 |
| 그림 없던 방법 | CAS-020 · CAS-024 …(MET-110 쓰는 케이스 46) | `MET-110` | 「레이저 빛을 피부에 쬐어 표적을 가열 · 파괴한다(펄스 방식은 하위 방법).」(원문 안 ` · ` 가 있어도 `\n` 로 이어서 안 갈림) |

- 케이스 방법 수 분포: 1 개 376 · 2 개 11 · 0 개 0(→ 빈칸 케이스 0).
- 「그림 없던 방법」 = 허브 미추적 새 그림(MET-008 · MET-110 ~ 125)의 MET-110. 지금 silver `concept_image` 는 방법 66 전부에 그림 행이 있다.

제품 `country` 표본(silver `product.country` 원문): PRD-001 보톡스 = `US` · PRD-022 하이톡스 = `KR` · PRD-129 쥬베룩스킨 = `KR` · PRD-358 포트라 = 빈칸(원문 빈칸 그대로).

## 5. 18105 다시 띄우기(코디) — 필요한 env

18105 는 **이 허브 워크트리**(`$H/backend/.venv` · `app.gold_main` · `--reload` 없음)로 떠 있어 지금은 앞 코드 · 앞 gold 가 메모리에 있다. 작업 사본 gold 를 이미 새 판으로 바꿨으므로 **새 코드(이 워크트리)로만** 다시 뜬다(앞 코드면 헤더 대조에서 시작 실패).

```sh
cd /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/backend
S=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/silver-model
GOLD_CSV_DIR=$S/gold \
GOLD_SOURCE_REF_PATH=$S/silver/source_ref.csv \
GOLD_HIERARCHY_DIR=$S/silver \
GOLD_LEDGER_CHECK_PATH=$S/notes/ledger-check-list.csv \
GOLD_EXPECTED_HASH=caa035606b1fd99e0431628064a3f9b171d1592468f223ac88c45c429573ee78 \
uv run uvicorn app.gold_main:app --host 127.0.0.1 --port 18105
```

- `GOLD_EXPECTED_HASH` 는 앞 기동에 없었다(넣으면 대조 · 빼도 뜸). 확인: `GET /procedure-hub/gold/health` → `build.gold_hash = caa03560…` · `aux_hash = 51e3760a…`.
- 상담 앱(18222)을 다시 띄울 때: `CHAT_KOS_MAP_SHA=1af2216c5a3ed2806936777314ad4fbdc1ca8e70b78fee99ad387ac5f0e26568`(JSON meta `hub_gold_hash` = caa03560 이라 JS4 불일치 표시도 없어짐).

## 6. 남은 것 · 코디가 알 것

1. **허브 레포 `data/medallion/`(stg 반입 원천)는 손대지 않았다**(WH4 「그 밖 허브 파일 0」). 그 폴더는 원래부터 11-16 판(gold 8accbb · g_profile 27 칸)이다. 이 브랜치를 배포하면 새 `headers.py` 와 헤더가 달라 적재기 · CSV 판 시작이 **헤더 대조에서 실패**한다. 그래서 배포 전에 `data/medallion/{gold, silver, notes}` 를 작업 사본 새 판(caa03560)으로 통째로 바꾸고, `data/medallion/README.md` 의 해시 표도 함께 고쳐야 한다. 실물 수 고정 시험 9(§3)도 그때 새 판 수로 다시 고정해야 한다. 할지는 코디가 정한다.
2. 로컬 `phub-medallion-pg` 의 `phub_medallion` DB 는 b202611170002 그대로다. DB 판으로 쓸 거면 `alembic upgrade head` 한 다음 새 gold 를 다시 적재한다.
3. WP-3 기대 표(팔자주름 23 · 턱살 5 · 기미 27): `g_indication` · `g_scope` 바이트가 같아서 다시 세도 같은 값이다. 바뀐 것은 기준 해시 caa03560 뿐이다.
4. 작업 사본 문서(`gold/README.md` · `semantic-map.md`)에는 새 칸 설명을 넣지 않았다. M1 은 통과한다. 필요하면 데이터 쪽에서 한 줄씩 더한다.
5. 허브 `docs/guides/api.md`(응답 칸)도 WH4 범위 밖이라 그대로 두었다. 응답 행에 칸 셋이 더 실리는 것은 더하기만 하는 변경이다.
