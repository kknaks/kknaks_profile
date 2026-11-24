# 부작용 분류 리포트 — 일시적 · 주의 · 위급 + 모달용 칸(silver · gold · 허브)

- 발주: `adverse-class-hub-task.md`(사용자 11-22 「이 정도만 발주」) · 코디 답 11-22 「1A 2받아들임」
- 커밋 0 · push 0 · stg / 원격 DB 0 · 18105 · 18222 손대지 않음 · 서브에이전트 0
- 분류 표 전체: **`$W/adverse-class.csv`**(188 행 · 코드 · 이름 · 대분류 · 분류 · 근거)

## 0. 위급 목록 — 사용자 확인용(13)

| 코드 | 이름 | 대분류 | 근거 |
|---|---|---|---|
| ADV-139 | 아나필락시스 | 과민반응 | 사용자 목록(과민반응 — 아나필락시스) · 원장 대처 level emergency 8 |
| ADV-142 | 혈관부종 | 과민반응 | 사용자 목록(알레르기 중증) · 원장 설명 「응급」 |
| ADV-144 | 스티븐스-존슨 유사 반응 | 과민반응 | 사용자 목록(알레르기 중증) · 원장 대처 「즉시 응급 진료」 · 「즉시 응급대응」 |
| ADV-088 | 실명 | 눈 손상 | 사용자 목록 · 원장 대처 「시간 지체 없이 즉시 응급 내원」 |
| ADV-089 | 시야 장애 | 눈 손상 | 사용자 목록 · 원장 대처 level emergency 5 · emergency_signs 5 |
| ADV-095 | 망막 허혈 | 눈 손상 | **더함** — 실명으로 가는 기전 · 원장 설명 「실명」 |
| ADV-051 | 혈관 폐색 | 혈관 합병증 | 사용자 목록 · 원장 대처 「즉시」 15 · severity critical |
| ADV-052 | 색전 | 혈관 합병증 | **더함** — 혈관 폐색과 같은 기전 · 원장 severity critical · 대처 「즉시」 9 |
| ADV-053 | 지방 색전증 | 혈관 합병증 | **더함** — 색전 하위 · 원장 severity 「생명을 위협할 수 있습니다」 |
| ADV-054 | 공기색전 | 혈관 합병증 | **더함** — 색전 하위 · 원장 severity severe · 대처 「즉시」 |
| ADV-061 | 뇌졸중 | 혈관 합병증 | **더함 · 확인 부탁** — 색전의 뇌 결과. 원장 대처 문장이 없어 이름으로만 올렸다 |
| ADV-130 | 피부 괴사 | 조직 손상 | 사용자 목록 · 원장 severity critical · 대처 level emergency 6 |
| ADV-153 | 호흡곤란 | 전신 반응 | 사용자 목록 · 원장 대처 level emergency 3 · emergency_signs 2 |

- 사용자 목록 8 + 같은 기전 더함 5(망막 허혈 · 색전 · 지방 색전증 · 공기색전 · 뇌졸중).
- 「알레르기 중증」 은 따로 된 코드가 없다. 그래서 혈관부종 · 스티븐스-존슨 유사 반응으로 읽었다. `ADV-138 알레르기 반응`(원장 「심한」 1 · emergency_signs 6)은 **주의**로 두었다.

**검토 후보 — 지금은 주의. 위급으로 올릴지 사용자가 정한다**

원장 문장이 없거나 약해서 올리지 않은 것들이다.

| 코드 | 이름 | 왜 후보인가 |
|---|---|---|
| ADV-170 | 의인성 보툴리즘 | 전신 독소 확산 · 원장 위험 행 0 |
| ADV-078 | 연하곤란 | 원장 대처 emergency 3(일시적 묶음 → 주의로 올림) |
| ADV-185 | 기도·식도 손상 | 위험 행 1 · 대처 문장 없음 |
| ADV-096 | 시신경 압박 · ADV-098 두개내압 상승 | 실명 기전 쪽 · 위험 행 0 ~ 1 |
| ADV-055 | 백색 변화 · ADV-056 청색증 · ADV-057 그물반 | 혈관 폐색의 **징후** · 원장 대처 emergency 4 · 1 · 0. 사건이 아니라 징후라 주의 |
| ADV-157 | 부정맥 · ADV-155 저혈압 · ADV-151 실신 | 전신 반응 · 원장 문장 약함 |
| ADV-128 | 동상 · ADV-131 지방괴사 | 원장 severity critical(냉각 시술 같은 행) · 대처 「즉시 시술 중단」 |

## 1. 분류 기준(build_batch8.py 에 적힌 그대로)

1. **기본 = 대분류 묶음**
   - 일시적: 국소 반응 · 근육 반응 · 결과 불만족 · 색소 변화
   - 주의: 그 밖 대분류 11개
2. **위급** = 위 §0 의 13 행(사용자 목록 + 같은 기전 · 원장 문장).
3. **보정(일시적 → 주의)** = 7 행. 일시적 묶음 안에서 원장 대처나 심한 정도가 병원 대응을 말하는 것이다.

   | 코드 | 이름 | 대분류 | 근거 |
   |---|---|---|---|
   | ADV-010 | 혈종 | 국소 반응 | 원장 대처 level emergency 2 |
   | ADV-068 | 근육 약화 확산 | 근육 반응 | 원장 대처 caution(독소 확산) |
   | ADV-069 | 근육 마비 | 근육 반응 | 원장 대처 level emergency 1 |
   | ADV-078 | 연하곤란 | 근육 반응 | 원장 대처 level emergency 3 · emergency_signs 1 |
   | ADV-086 | 횡문근융해증 | 근육 반응 | 원장 대처 emergency_signs |
   | ADV-101 | 색소탈실 | 색소 변화 | 원장 대처 emergency_signs 1(오래 남을 수 있음) |
   | ADV-182 | 역설적 지방 증식 | 결과 불만족 | 원장 severity severe(수술 교정) |

4. **주의 → 일시적으로 내리는 것은 하지 않았다.** 보수적으로 두고, 「전신 반응 중 위급 아닌 것 = 주의」 라는 사용자 기준 글을 그대로 따랐다. 그래서 두통 · 메스꺼움 · 안구 건조 같은 것도 주의다.
5. 원장 대처의 `level_text = emergency` 는 소음이 많다(예: 비대칭 3 · 미소 비대칭 2). 그래서 이 값을 기계로 따라 올리지 않았다. 원장 문장을 보고 행마다 정했다.
6. 근거는 source_ref `adverse · severity_class → drafts/clinic-supplement/clinic-a-20261119/user.csv:L2232 ~ L2419` 이다.
   - user.csv 줄의 basis 는 「보충 · 분류 기준 2026-11-22 · 대분류 + 원장 문장 · <행 근거>」 이고, 근거 종류는 **사용자 제공**이다.

## 2. 분류 셈

분류별: **일시적 67 · 주의 108 · 위급 13**(사전 188)

| 대분류 | 일시적 | 주의 | 위급 | 계 |
|---|---:|---:|---:|---:|
| 국소 반응 | 32 | 1 | 0 | 33 |
| 염증 반응 | 0 | 15 | 0 | 15 |
| 혈관 합병증 | 0 | 8 | 5 | 13 |
| 신경 손상 | 0 | 4 | 0 | 4 |
| 근육 반응 | 17 | 4 | 0 | 21 |
| 눈 손상 | 0 | 9 | 3 | 12 |
| 색소 변화 | 6 | 1 | 0 | 7 |
| 흉터 | 0 | 4 | 0 | 4 |
| 결절 | 0 | 7 | 0 | 7 |
| 시술물 관련 | 0 | 9 | 0 | 9 |
| 화상 | 0 | 4 | 0 | 4 |
| 조직 손상 | 0 | 8 | 1 | 9 |
| 과민반응 | 0 | 6 | 3 | 9 |
| 전신 반응 | 0 | 27 | 1 | 28 |
| 결과 불만족 | 12 | 1 | 0 | 13 |

gold `g_adverse` 2,923 행 기준: 일시적 1,976 · 주의 818 · 위급 124 · 빈칸 5(adverse_code 없는 위험 행). 대처가 있는 행은 705 이다.

## 3. 허브 응답 칸(`facets?facet=adverse` 행 = `g_adverse`)

| 칸 | 값 |
|---|---|
| `severity_class` | 일시적 · 주의 · 위급(그 행 `adverse_code` 의 silver 값 · 코드 없으면 빈칸) · 자리 = `adverse_top_name` 뒤 |
| `guidance_texts` · `guidance_kinds` · `guidance_timings` · `guidance_levels` | 그 위험(`adverse_risk`)의 `adverse_guidance` 행을 silver 순서 그대로 옮긴 원문 `text` · `kind`(관리 / 예방 / 경고 기준 / 모니터링) · `timing_text` · `level_text` · 줄바꿈 `\n` 하나로 이음 · **넷 같은 순서 · 같은 개수 = `n_guidance`**(대처 0 이면 넷 다 빈칸) · 자리 = `n_guidance` 뒤 |

- 원문 안 줄바꿈은 0 이다(K9 검사). timing · level 은 원문이 빈칸이면 빈 줄로 둔다. 그래서 `split('\n')` 개수 = `n_guidance` 이다.
- `facets?facet=outcome` 은 그대로다(onset · peak · duration 칸이 이미 있음 · 바뀐 칸 0).
- 표본 — `GAD-00036` 필러 · 혈관 폐색 · **위급** · n_guidance 8

  | kind | timing | level | text(앞부분) |
  |---|---|---|---|
  | 경고 기준 | 주사 직후 | emergency | 주사 직후 피부가 하얗게 변하면 혈관이 막혔을 가능성 — 즉시 히알루로니다아제… |
  | 경고 기준 | | emergency_signs | 시술 부위 급격한 백색 변화(blanching) — 혈관폐색 의심 |
  | 경고 기준 | | emergency_signs | 시력 변화 또는 시야 장애 — 안동맥 폐색 의심, 즉시 응급실 |
  | 관리 | | safety_protocol | 혈관폐색 응급 프로토콜 준비 확인 |
  | … | | | (8 줄) |

  - 앱 주의: 대처 원문에는 **시술자용 줄**(예: `safety_protocol` 「비상 비치 확인」)이 섞여 있다. 고객 모달에서 kind · level 로 거를지는 앱(WP) 쪽에서 정한다. 허브는 원문을 거르지 않고 그대로 낸다.

## 4. 바뀐 파일

### silver 작업 사본(`$S` — git 밖 · 앞 판 = `archive/silver-before-clinic-a-20261119-b8/` · 스크립트 앞 판 = `archive/scripts-before-batch8/`)

| 파일 | 바뀜 |
|---|---|
| `drafts/clinic-supplement/clinic-a-20261119/build_batch8.py`(새) | 묶음 8. 분류 규칙(기본 · URGENT 13 · UP_CAUTION 7)을 담았고, 다시 돌려도 같은 바이트다 · A3 재현용 인자 꼴은 묶음 7 과 같다 |
| `silver/adverse.csv` | 끝 칸 `severity_class`(기존 칸 바이트 그대로) |
| `silver/source_ref.csv` | 끝 188 줄 |
| `…/clinic-a-20261119/user.csv` | 끝 188 줄(L2232 ~ L2419 · kind 「부작용 분류」 · status 확인) |
| `…/clinic-a-20261119/batch8-log.json`(새) | 묶음 기록 |
| `drafts/silver-check/silver-schema.json` | adverse 칸 `severity_class`(values 셋 · vocab) |
| `drafts/glossary/glossary-build.py` · `notes/vocabulary.csv` | 값 묶음 「부작용 분류」(adverse · g_adverse · 뜻 = 사용자 결정 11-22) |
| `silver-erd.md` · `silver-tables.md` | `silver-check.py --write-docs` 로 다시 씀 |
| `gold/gold-build.py` | g_adverse 칸 다섯. 기존 칸 · 근거 참조는 그대로 둠 |
| `gold/gold-check.py` | A1 묶음 8 규칙 · A3 묶음 8 재현 · K4 줄바꿈 칸 넷 · `severity_class` 어휘 · 새 **K9**(분류 · 대처 원문 · 개수 다시 지어 대조) · 그림 시드가 없으면 묶음 7 재현만 건너뜀(WARN — 아래 §7) |
| `gold/*.csv` | 재빌드 |

### 허브 워크트리(`$H` — 커밋 안 함)

이 판의 몫:

| 파일 | 바뀜 |
|---|---|
| `backend/app/modules/gold/headers.py` | `GOLD_HEADERS["g_adverse"]` 칸 다섯 · `ADVERSE_EXTRA_COLUMNS` · `SEVERITY_CLASSES`(맞춤 · 셈에 안 듦) |
| `backend/app/modules/gold/silver_contract.py` | `SILVER_HEADERS["adverse"]` 끝 `severity_class` |
| `backend/alembic/versions/b202611220001_adverse_class_columns.py`(새) | ← b202611200001 · `g_adverse` add_column 다섯 + `s_adverse` 하나 · downgrade 여섯 · 앱 import 0 |
| `backend/tests/test_medallion_model.py` | 칸 합 281 → 286(gold) · 400 → 401(silver) · 767 → 773 · head b202611220001 · 새 `test_adverse_class_columns_revision` |
| `backend/tests/test_gold_contract.py` | 덧붙인 칸이 헤더에 있고 맞춤 칸이 아님 · 분류 셋 |

- `git diff --stat` 4 파일 +82 −14 · 새 파일 2 = **WP-H(아직 커밋 전) + 이 판이 함께 든 값**이다(`b202611200001` 은 WP-H 몫).
- `facets.py` · `medallion.py` · 적재기는 확인만 했다(응답 = 행 dict 그대로 · 칸은 계약에서 기계로).
- 미추적 그림 18 파일은 손대지 않았다.

## 5. 시험 · 회귀

| 무엇 | 결과 |
|---|---|
| silver-check | **PASS**(FAIL 0 · WARN 5 = 레포의 작업 사본 밖 변경 — 앞서부터) |
| gold-check | **PASS**(FAIL 0 · 구조 문제 0) · K9 「일시적 1976 · 주의 818 · 위급 124 · 빈칸 5 · 대처 있는 행 705」 · 새 WARN 1 = 묶음 7 재현 건너뜀(그림 시드 없음 · §7). A3 의 묶음 8 재현은 바이트 같음 |
| 묶음 8 재현 | 기준 b8 → scratchpad 로 다시 돌림 → silver 59 · user.csv 바이트 같음 · 두 번 돌려도 같음 |
| 허브 `test_medallion_model` · `test_gold_contract`(합성) | 18 passed · 4 skipped |
| 허브 `tests/test_gold_*.py` + `test_medallion_*.py`(CSV 판 · 실물 env · `test_silver_contract_equals_real_headers` 포함) | 453 passed · 11 failed · 12 skipped. 11 은 WP-H 기준선과 **같은 목록 · 같은 단언 문구**다(실물 수 고정 9 · 그림 시험 2 = 미추적 SVG) — `diff` 결과 소요 시간 한 줄만 다름 |
| 허브 DB 판(`GOLD_REPOSITORY=db`) | 110 passed · 2 failed(T12 · T13 — 기준선과 같은 것) |
| alembic(내 버리는 컨테이너 `postgres:16` · 127.0.0.1:18499 · 끝나고 지움) | `upgrade head` → b202611220001(g_adverse 41 · s_adverse 9 칸) → `downgrade -1`(36 · 8) → `upgrade head` → `load_medallion.py` 적재 성공. 표 76 · 행 170,889 · build gold 51bc4b6b / aux abcce217 · s_adverse 분류 13 / 108 / 67 |
| ruff(바뀐 허브 파일 5) | All checks passed |
| 앱 `test_consult_material.py` | 6 passed |

회귀:

| # | 조건 | 결과 |
|---|---|---|
| ① | gold 파일 바이트 | 바뀜 = `g_adverse`(칸 다섯) + **승인된 근거 종류 번짐**만. `g_entry` 202 · `g_node` 173 · `g_evidence` 375 행의 `evidence_kind` 가 원장 → 원장 + 사용자 제공(전부 adverse 대상 행 · 다른 칸 0). 그 밖 12 파일 바이트 같음 |
| ② | `g_adverse` 기존 칸 | 2,923 행 순서 · 기존 36 칸 값 다른 것 0(evidence_kind 포함) |
| ③ | `facets?facet=adverse` | 노드 10(PRC-001 · M1 · M2 · CAS-013 · CAS-016 · PRD-022 · PRD-001 · adverse:ADV-051 · ADV-139 · ADV-014) 모두 total · 행 순서 · 새 칸 뺀 행 dict 같음. 더해진 것은 칸 다섯뿐 |
| ④ | `facets?facet=outcome` | 노드 7 total · 행 · 칸 전부 같음(새 칸 0) |

- 앞 판 = 이 코드 + `g_adverse` 헤더를 앞 판으로 되돌리고 + 앞 gold · b8 silver 로 돌린 값. 이 판 사이에 바뀐 코드는 헤더 상수뿐이라 같은 비교다.

## 6. 새 해시 · JSON

| 항목 | 앞 판 | 새 판 |
|---|---|---|
| 허브 `build.gold_hash` | `caa035606b1fd99e0431628064a3f9b171d1592468f223ac88c45c429573ee78` | **`51bc4b6b133a850bd8ca87c231688405875322b6dc84d25bc3342496fd87f979`** |
| 허브 `build.aux_hash` | `51e3760a82df45de2011b59868a723532af9c7732163e1eee31472ceb8a93b34` | **`abcce2177755bc0ca196ce1acbff72db7b29a013848ff3c07828e099545f94cc`**(source_ref +188) |
| silver 해시(silver-check · 59표) | — | `980669b8fec02d54a35d613805792e930d515c3908d1d435874475c7040959c3` |
| 매핑 JSON v3 sha256 | `8f4e63935ee1995cc5ae83cd5eb5fa3da2bc96ed554d3264101ea485dd9dd131`(11-22 18:10 판 · sites 92) | **`63f2d952e245ceba3736b078206d3569624a527a029ab70fdf894f6299f54101`** |

- JSON: `build_mapping_json_v3.py 51bc4b6b… abcce217…` 로 다시 지었다.
  - items · groups · sites · products · product_categories 직렬화가 같다(True × 5). 키 순서도 같다.
  - `diff` = meta 세 줄(`hub_gold_hash` · `hub_aux_hash` · `made_at`)뿐이다.
  - 두 경로(앱 워크트리 · `~/git/clinic_chat`) 같은 sha. 앞 판 백업 = scratchpad `v3-before-8f4e6393.json`.

## 7. 18105 다시 띄우기(코디) · 남은 것

```sh
cd /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/backend
S=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/silver-model
GOLD_CSV_DIR=$S/gold \
GOLD_SOURCE_REF_PATH=$S/silver/source_ref.csv \
GOLD_HIERARCHY_DIR=$S/silver \
GOLD_LEDGER_CHECK_PATH=$S/notes/ledger-check-list.csv \
GOLD_EXPECTED_HASH=51bc4b6b133a850bd8ca87c231688405875322b6dc84d25bc3342496fd87f979 \
uv run uvicorn app.gold_main:app --host 127.0.0.1 --port 18105
```

- 확인: `GET /procedure-hub/gold/health` → `build.gold_hash = 51bc4b6b…` · `aux_hash = abcce217…`.
- 작업 사본 gold 는 이미 새 판이다. 그래서 **이 워크트리 코드로만** 뜬다(앞 코드는 g_adverse 헤더 대조에서 시작 실패).
- 18222: `CHAT_KOS_MAP_SHA=63f2d952e245ceba3736b078206d3569624a527a029ab70fdf894f6299f54101`.

남은 것:

1. **사용자 확인**: §0 위급 13(특히 더한 5 — 뇌졸중은 원장 문장 없음)과 검토 후보 표.
   - 바꾸려면 `build_batch8.py` 의 `URGENT` · `UP_CAUTION` 만 고친다. 그다음 묶음 8 → glossary-build → gold-build → gold-check → JSON meta 를 다시 돌린다(허브 코드는 그대로).
2. **그림 시드 폴더가 없어졌다**(`kknaks_profile/프로시저허브-데이터-메달리온/reference/2026-11-17-procedure-images` — 형제 워크트리 지워짐 · WP-H 때는 있었다).
   - 그래서 gold-check A3 의 묶음 7 재현과 silver-check I5 는 건너뛴다(WARN). 묶음 8 재현은 돈다.
   - 다시 돌리려면 `SILVER_IMAGE_SEED=<시드 폴더>` 를 준다.
3. 로컬 `phub-medallion-pg` 컨테이너는 이번에 멈춰 있었다. 손대지 않았다(시험은 내 컨테이너로 했다).
4. WP-H 리포트 §6 의 허브 `data/medallion/` 교체 문제는 그대로다. 이번 판으로 g_adverse 헤더 · s_adverse 칸도 바뀌어서, 배포 전에 통째로 바꿀 범위가 더 커졌다.
5. 대처 원문의 시술자용 줄(`safety_protocol` 등)을 고객 모달에서 거르는 것은 앱 WP 몫이다(§3).
