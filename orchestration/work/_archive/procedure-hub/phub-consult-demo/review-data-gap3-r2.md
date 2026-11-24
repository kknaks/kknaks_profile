# 재검수 r2 — 허브 데이터 구멍 3 고침 1(`data-gap3-report.md` v1.1 · 묶음 9) · 2026-11-23

검수 워커(읽기만). 대상은 아래와 같다.
- `data-gap3-report.md` v1.1
- `silver-model/drafts/clinic-supplement/clinic-a-20261119/{build_batch9.py, gap3_survey.py, batch9-log.json, user.csv, gap3-survey-a/b.json}`
- `silver-model/silver` · `gold`

기준은 `data-gap3-task.md` · 앞 검수 `review-data-gap3.md`(FAIL · P1 1 · P2 5)다.

지킨 것:
- silver · gold · 스크립트 · 허브 · 앱 수정 0 · 커밋 0 · LLM 0 · 서브에이전트 0
- 작업 사본 md5(silver · gold · 묶음 폴더)가 전 · 뒤 같다(`27cb55e1…`).
- 18105 · 18222 손대지 않음. 새 gold 는 허브 코드(`app.gold_main`)를 **프로세스 안 TestClient** 로 적재해 읽었다(포트 0). 허브 레포 `git status` 24 줄은 전 · 뒤 같다.
- silver-check · gold-check 는 다시 돌리지 않았다(발주 주의). 대신 아래를 직접 했다:
  - `build_batch9.py` 바이트 대조
  - `gap3_survey.py` 를 스크래치 복사본으로 돌림(스크립트가 출력을 자기 폴더에 쓰기 때문)
  - 데이터 워커가 남긴 `drafts/silver-check/check-stats.json`(19:17) · gold 행 수를 대조

## 판정: **PASS** — P0 0 · P1 0 · P2 5(새 5)

- 앞 P1-1 은 닫혔다. OUT-1622(근적외선 타이트닝)가 빠져 PRC-007 × 타이트닝 줄은 0 이고, 티타늄리프팅 · 포트라 · BBL HERO 페이스가 타이트닝 목록에서 빠졌다.
- 앞 P2 5 개도 모두 닫혔다.
- 재현은 모두 같다: 바이트 · 59 표 · 전수 셈 수 · gold_hash `ab5eebc9…` · aux `1f666235…` · §6 여섯 목록.
- 원문 대조: 효과 9 줄은 전부, 고민 37 줄은 전부(포인터 179 개를 분류하고 줄마다 앞 포인터 원문을 읽음) 열어 보았다. 지어낸 줄은 없다.
- 새로 찾은 것은 근거 포인터 품질 · 표 분류 · 재현 안정성 수준(P2)이다. 화면 목록에 근거 없는 진료항목이 드는 꼴은 없다.

## 1. 앞 검수 지적 — 닫힘 / 열림

| 지적 | 상태 | 근거 |
|---|---|---|
| P1-1 OUT-1622 제품 문장 → 시술 줄 | **닫힘** | 확인한 것:<br>• `silver/outcome.csv` 에 PRC-007 × EFF-021 0 줄이고, 새 outcome 9 줄은 시술 5 · 케이스 4 다(`build_batch9.py` `EFFECT`).<br>• 원장 전체 json 을 「타이트닝 × 티타늄 · 포트라 · 스킨타이트 · 근적외선」 으로 찾으면 2 곳뿐이다(`taxonomy.json:/modality/7/subcategories/2/items/4` BBL스킨타이트 detail · overview). 그래서 J27 「안 이음」 은 원장과 맞다.<br>• §6 타이트닝은 8 이다(아래 §3) |
| P1-1 같은 꼴 전수(`keep_ref`) | **닫힘**(남은 틈은 새 P2-1) | `keep_ref`(`build_batch9.py:132-158`)가 다른 계열 원장 자리 · 제품 항목 자리를 뺀다. 내 분류에서 새 고민 줄 포인터 가운데 **제품 항목 0 · 다른 계열 extracted / taxonomy modality 0** 이다. 다만 제품 목록에 없는 「프로그램(묶음 상품)」 항목은 거르지 못했다(P2-1) |
| P2-1 CAS-1046 × 눈 꺼짐 빠짐 | **닫힘** | IND-3271 이 있다. 근거는 좁은 케이스 CAS-1006 · 1048 · 1049, 포인터는 `extracted.json:/M2/indications/extended/0` 「꺼진 눈 교정」(원문 확인)이다. W2 셈 37 = 반영 37 |
| P2-2 약한 근거 표 | **닫힘**(분류 1 곳 틀림 → 새 P2-2) | §3 표(직접 19 · 묶음 · 계열 ref 18)와 18 줄 목록이 있다 |
| P2-3 조합 문장 규칙 | **닫힘** | 「시술 몫을 괄호 · 주어로 따로 적으면 근거 · `A + B = 효과` 는 아님」 규칙을 적었다. OUT-1621 원문 셋이 모두 「HIFU(타이트닝)」 · 「HIFU(열 타이트닝·고정)」 · 「울쎄라(HIFU) … 턱선을 타이트닝」 으로 시술 몫을 따로 적는다 |
| P2-4 전수 셈 스크립트 · J5b | **닫힘**(재현 안정성 → 새 P2-4) | `gap3_survey.py` 를 다시 돌리면 §2(a) 수가 다 같다(아래 §3). `gap3-survey-b.json` 은 바이트도 같다. J5b(바디보톡스 × 턱선 처짐 · 방법 다름)가 규칙 R3 에 있다 |
| P2-5 기계가 정할 판단 | **닫힘** | 규칙으로 정함 12(R1 ~ R6 · J5b 포함) · 사람 판단 21 + J27 로 나눴다. 셈(10 + 1 + 2 + 3 + 3 + 2 = 21)이 맞고, J17 은 기계 반영 후보로 표시만 했다 |

## 2. 원문 대조(bronze `_archive/procedure-hub/phub-recommend/bronze/phub-ledger` — `PROCEDURE-HUB/…/bronze/phub-ledger` 와 파일 전부 같음)

### 2-a 효과 9 줄(전부)

| 줄 | 대상 | 효과 | 원문 | 판정 |
|---|---|---|---|---|
| OUT-1621 | PRC-311 HIFU | 피부 타이트닝 | `problem-combos.json:/combos/2/packages/2/clinicalRationale` 「**HIFU(타이트닝)** + 보톡스(근이완) …」 · `/2/packages/3` 「HIFU(**열 타이트닝**·고정)」 · `/7/packages/1/salesPitch` 「울쎄라(HIFU) … **턱선을 타이트닝**」 | 맞음(시술 몫을 따로 적음 · P2-3 규칙) |
| OUT-1622 · 1623 | PRC-311 · PRC-312 | 탄력 개선 | `patient-education.json:/categories/8/how_it_works` 「에너지(**초음파 또는 고주파**)가 … 새로운 콜라겐이 만들어져 **탄력이 개선**됩니다」 | 맞음 |
| OUT-1624 · 1625 | PRC-311 · PRC-312 | 피부 처짐 개선 | `…/categories/8/simple_explanation` 「**초음파나 고주파** 에너지로 … **처짐을 개선**」 | 맞음 |
| OUT-1626 · 1627 | CAS-3051 · 3052 | 리프팅 | `taxonomy.json:/modality/8/subcategories/2/items/0`(M9-3 › **온다**) overview 「비침습적 **리프팅** 기기」 · mechanism 「… **리프팅 효과**」 · 두 케이스 제품 = PRD-433 온다 하나(`case_product` CPR-0467 · 0468) | 맞음 |
| OUT-1628 · 1629 | CAS-3051 · 3052 | 탄력 개선 | 같은 mechanism 「피부 **탄력 회복** 및 리프팅 효과」 | 맞음 |

v1.1 은 OUT 번호를 하나씩 당겼다. 그래서 v1 의 OUT-1622(근적외선 타이트닝)와 v1.1 의 OUT-1622(HIFU 탄력)는 다른 줄이다. v1 은 18105 에 올라간 적이 없어 실제 해는 없다. 다만 앞 검수 · 리포트를 읽을 때 헷갈릴 수 있다(참고).

### 2-b 새 고민 37 줄(전부 · 포인터 179 분류 · 줄마다 원문 읽음)

| 줄 | 넓은 케이스 × 고민 | 원문(포인터 → 글) | 판정 |
|---|---|---|---|
| IND-3235 | CAS-015 보톡스 · 얼굴 × 콧등 주름 | `extracted.json:/M1/indications/extended/4` 「콧등 잔주름 (토끼주름)」 · `taxonomy …/modality/0/…/items/0`(보톡스 › 주름) 「콧등 주름」 | 맞음 |
| IND-3236 | CAS-015 × 윗입술 세로주름 | `extracted.json:/M1/indications/extended/3` 「윗입술 세로주름」 | 맞음 |
| IND-3238 | CAS-015 × 팔자주름 | `extracted.json:/M1/indications/extended/9` 「팔자주름」 | 맞음 |
| IND-3239 | CAS-015 × 눈밑주름 | `/M1/indications/extended/1` 「눈밑주름」 | 맞음 |
| IND-3240 · 3243 | CAS-015 × 하안면 처짐 · 턱선 처짐 | `taxonomy …/modality/0/subcategories/2/items/7`(턱선보톡스) 「하안면 처짐으로 인한 미니리프팅」 · 「턱선 처짐 및 정의 부족」 · items/11 · 12 넥 · 페이스앤넥큐레이션 「턱선 처짐」 | 맞음(보톡스 계열 용도 항목 · 제품 아님) |
| IND-3241 · 3242 | CAS-015 × 입꼬리 처짐 · 코끝 처짐 | items/6(입꼬리/잇몸미소/코끝) 「입꼬리 처짐 교정」 · 「코끝 처짐 교정」 | 맞음 |
| IND-3244 | CAS-096 바디보톡스 × 어깨라인 처짐 | items/2(승모근) 「목 긴장으로 인한 어깨라인 처짐」 | 맞음 |
| IND-3245 ~ 3247 | CAS-1046 풀페이스필러 × 이마 · 미간 · **입꼬리주름** | `extracted.json:/M2/indications/primary/0` 「주름치료 — 이마주름, 미간주름, 눈가주름, 팔자주름, **입꼬리주름** …」 | 맞음 |
| IND-3249 | CAS-1046 × **팔자주름** | `procedure-comparison.json:/comparisons/1/procedures/1/best_for` 「팔자, 마리오넷, 정적 주름」(히알루론산 필러) · M2 primary/0 · 포인터 64 → 10(보톡스 제품 항목 39 등이 빠짐) | 맞음 |
| IND-3250 · 3251 | CAS-1046 × 볼 꺼짐 · 관자놀이 꺼짐 | `taxonomy.json:/problem/10/subcategories/4/items/0 · 1` 볼볼륨충전 [M2, M3, M6] · 관자놀이충전 [M2, M6] | 근거 있음(계열 ref) |
| IND-3252 · 3253 | CAS-1046 × 눈밑 꺼짐 · 다크서클 | `problem-packages …/problems/0/complaints/10/procedures/0` 필러 「볼륨 충전」 · `extracted.json:/M2/indications/extended/1` 「다크서클 교정 (눈밑 꺼짐)」 | 맞음 |
| IND-3257 | CAS-1053 PLLA × 볼 지방위축증 | `extracted.json:/M3/indications/extended/3` 「뺨 지방위축증 (뺨 볼륨 감소)」 | 맞음 |
| IND-3256 | CAS-1053 × 관자놀이 꺼짐 | `problem-packages …/problems/10/complaints/6/procedures/1` 「바이오스티뮬레이터/콜라겐부스터 — 장기 콜라겐」 | 근거 있음(묶음 역할) |
| IND-3258 | CAS-1055 PN × 눈밑주름 | `procedure-comparison …/comparisons/1/procedures/3` 「**리쥬란 (PN주사)** — best_for 눈밑 잔주름, 피부 탄력」 | 맞음(시술 이름 · 고민을 직접 적음) |
| IND-3259 · 3260 | CAS-1055 × 눈가주름 · 눈꺼풀 처짐 | `problem-packages …/procedures/2` 「스킨부스터 — role 피부 재생」 | 근거 있음(묶음 역할) |
| IND-3261 · 3265 · 3267 | HIFU · 고주파 얼굴 × 눈가주름 | `problem-packages …/problems/1/complaints/2/procedures/1` 「리프팅기기 — role 피부 타이트닝」 | 근거 있음(묶음 역할) |
| IND-3262 · 3266 · 3270 | HIFU · 고주파 얼굴 × 눈꺼풀 처짐 | `taxonomy.json:/problem/2/subcategories/1/items/0` 눈꺼풀쳐짐 · modality_ref/0 **M9** · 묶음 「리프팅기기」 | 근거 있음(계열 ref) — 같은 항목 `modality_ref/1 → M7` 포인터도 함께 남음(P2-3) |
| IND-3268 | CAS-3048 고주파 얼굴 × 턱선무너짐 | `taxonomy.json:/problem/2/subcategories/0/items/1` · modality_ref/1 M9 · 묶음 「리프팅기기」 | 근거 있음 — `modality_ref/0 → M7` 함께 남음 |
| IND-3263 | CAS-3027 고주파 전신 × 목주름 | `taxonomy.json:/problem/1/subcategories/1/items/2` 목주름 · modality_ref/1 M9 | 근거 있음(계열 ref) |
| **IND-3264** | CAS-3027 고주파 전신 × **목 처짐** | 포인터 1 개뿐: `taxonomy.json:/modality/8/subcategories/4/items/0/extracted/indications/primary/2` = M9-SIG › **셀리부트프로그램**(detail 「써마지600+BBL+튠+줄기세포 · 950만원」) 「턱선 및 목 처짐」 | **P2-1** — 묶음 상품 문장(시술 몫 없음) |
| **IND-3269** | CAS-3048 고주파 얼굴 × **턱선 처짐** | 같은 포인터 1 개뿐 | **P2-1** |
| IND-3271 | CAS-1046 × 눈 꺼짐 | `extracted.json:/M2/indications/extended/0` 「꺼진 눈 교정」 | 맞음 |

넓은 케이스 규칙(같은 시술 · 방법 · 조직 · 재료)은 `build_batch9.py` 가 `assert sig(s) == sig(wide)` 로 37 쌍마다 확인한다. 다시 돌려서 통과했다. 「얼굴 전체 케이스에 붙은 부위 고민이 실제로 그 시술로 하는 것인가」 는 계열별로 다르다:
- 필러 · 보톡스 · PLLA 는 계열 원장이 그 부위 고민을 직접 적는다.
- HIFU · 고주파 · PN 의 눈가 · 눈꺼풀은 묶음 역할 · 계열 ref 근거다. 리포트 §3 이 그렇게 표시했고, 코디 결정 거리로 올렸다.

## 3. 재현

| 항목 | 리포트 v1.1 | 다시 돌림 | 같음 |
|---|---|---|---|
| `build_batch9.py <b9 silver> <b9 user.csv> <스크래치>` | +37 · +9 · +192 · user +37 | `{'indication_added': 37, 'outcome_added': 9, 'source_ref_added': 192, 'user_lines': 37}` | ✓ |
| 바이트 | 같은 바이트 | indication · outcome · source_ref · `user.csv` · `batch9-log.json` `cmp` 같음 · silver **59 표 다름 0** | ✓ |
| 케이스 코드 | 바뀜 0 | `procedure_case.csv` ↔ b9 `cmp` 같음 | ✓ |
| silver 행 수 | 2596 · 1613 · 56567 | 데이터 워커 `check-stats.json`(19:17) rows = indication 2596 · outcome 1613 · source_ref 56567 · procedure_case 387 | ✓ |
| gold 행 수 | g_indication 14002 · g_outcome 1613 · g_edge 14246 · g_evidence 41078 | 같음 | ✓ |
| gold_hash · aux_hash | `ab5eebc9…02502c` · `1f666235…652be` | 프로세스 안 적재(`GOLD_EXPECTED_HASH` 통과) → `health.build` 같은 두 값 | ✓ |
| `gold-check.py` 묶음 9 블록 | 「v1 블록 그대로 통과」 | 블록(`:282-296` · `:408-416`)에 행 수를 박지 않았다 — 기존 바이트 앞부분 · 덧붙인 표 · 줄 종류 · 재현 바이트만 본다. 그래서 v1.1 에도 맞다 | ✓ |
| silver-check · gold-check | PASS · PASS(WARN 5 · 11) | 다시 돌리지 않음(발주 주의) — check-stats 행 수 대조로 갈음 | — |
| `gap3_survey.py`(스크래치 복사 · 기준 b9) | §2(a) | 있음 32 · 21 · 2 / W 26 · 18 · 7 / 같은 시술 다른 케이스 1 · 0 · 0 / 계열 원장 21 · 21 · 16 / 근거 없음 470 · 828 · 294 / cases 90 / W2 37 — **다 같음** · `-b.json` 바이트 같음 · `-a.json` 은 줄 차례만 다름(P2-4) | ✓ |
| §6 전 → 후(`quality/build_answers.py` `r2_concern` · `r3_effect` 를 프로세스 안 허브에 물림) | 1 · 12 · 8 · 10 · 11 · 21 | 입꼬리주름 1(풀페이스필러) · 팔자주름 12 · **타이트닝 8**(볼뉴머 · 소프웨이브 · 슈링크유니버스 · 더마 · 아이 · 써마지FLX · 아이써마지 · 울쎄라피 프라임 — 티타늄 · 포트라 · BBL 없음) · 미간 10 · 눈가 11 · 탄력 21 — **여섯 다 같은 묶음 · 같은 수** | ✓ |

## 4. 전수 셈 · 「근거 없음」 표본

- (a) 표의 수는 §3 대로 다 같다.
- 「근거 없음」 1,592 행에서 그 케이스 계열의 `extracted.json` indications 글이 고민 이름을 그대로 품는 것을 찾았다. **5 쌍**이 걸렸다(P2-5):
  - CAS-1053 PLLA · 1020 PDLLA · 1021 무세포동종진피 · 1054 CaHA × **볼 주름**: M3 「깊은 주름 (팔자주름, **볼 주름** 등)」
  - CAS-1056 PRP × 볼 × **팔자주름**: M5 「꺼진 부위 볼륨 회복 (꺼진 볼, 꺼진 눈밑, **팔자주름** 등)」
  - silver 계열 줄이 없어 「계열 원장 줄」 꼴로도 안 잡혔다. 같은 M3 문장의 「팔자주름」 은 CAS-1053 에 W 로 붙었다.
- (b) 는 `-b.json` 이 바이트까지 같다. 반영 9 는 §2-a 대로다.

## 5. 사람 판단(J1 ~ J27)

| 묶음 | 대조 | 결과 |
|---|---|---|
| 규칙으로 정함 12(R1 ~ R6) | 앞 검수 §6 에서 원장과 맞춘 줄 그대로 · J5b 는 방법 MET-020 ↔ 002 다름(W 규칙) | 맞음 · 사람 확인 불필요 판단 맞음 |
| 사람 판단 21 | J6 ~ J15 온다 원장 「얼굴 처짐 및 탄력 저하」 · J17 온다 「목 주름 및 이중턱」 · J24 `extracted.json:/M11/indications/primary/1` 「리프팅/타이트닝」 — 앞 검수와 같음 | 추천이 원장과 맞음 · 기계로 정할 수 있는데 올린 것 0(J17 은 후보 표시) |
| J27 PRC-007 × 타이트닝 | 원장 전체에서 근적외선 타이트닝 문장은 BBL스킨타이트 항목 하나뿐(§1) | 「안 이음」 맞음 — 다만 규칙(「제품 셋 시술에 제품 하나 문장 = 안 올림」 · 이번 리포트 §2(b) 기준)으로 정해지는 것이라 사람 판단보다 「규칙으로 정함」 칸이 맞다(참고) |

## 6. 새 지적(P2)

| # | 지적 | 근거 | 고칠 방향 |
|---|---|---|---|
| P2-1 | **묶음 상품(프로그램) 문장 하나가 유일 근거인 넓은 케이스 고민 2 줄** | IND-3264(CAS-3027 고주파 전신 × 목 처짐) · IND-3269(CAS-3048 고주파 얼굴 × 턱선 처짐)의 원장 포인터는 각 1 개다. 그 포인터는 `taxonomy.json:/modality/8/subcategories/4/items/0` = M9-SIG **셀리부트프로그램**(「써마지600+BBL+튠+줄기세포 · 950만원」)의 indications 「턱선 및 목 처짐」 이다.<br>이 문장은 리포트 P2-3 규칙의 「몫이 따로 없는 A + B = 효과」 꼴이다. `keep_ref` 는 제품 항목만 빼고(`prod_items` = 제품 source_ref 가 가리키는 항목), 이 프로그램 항목은 제품 줄이 없어 남았다.<br>좁은 케이스 IND-2946 · 2948 · 2949(앞 묶음)도 같은 포인터 하나뿐이다.<br>다만 결론 자체에는 다른 원장 근거가 있다:<br>• 턱선 → M9 계열 「리프팅 (처진 볼살, **턱선 리프팅**)」<br>• 목 → 써마지FLX 항목 「목 및 턱선 처짐」 · 볼뉴머 「얼굴 및 목 처짐」<br>그래서 화면에 근거 없는 진료항목이 드는 꼴은 아니다 | `keep_ref` 에서 프로그램 · 묶음 상품 항목(M*-SIG · detail 에 「+」 결합)도 뺀다.<br>• IND-3269 는 M9 계열 줄 포인터로 바꾼다.<br>• IND-3264 는 「케이스 제품이 그 문장을 가진 제품」 규칙을 적고 제품 항목을 근거로 쓰거나, 사람 판단 표로 올린다.<br>• 좁은 케이스 3 줄도 같이 본다 |
| P2-2 | §3 근거 꼴 분류 2 곳 틀림 | P2-1 의 두 줄이 「직접 적응증」(CAS-3048 직접 1 · CAS-3027 직접 1)으로 셌다. 실제는 묶음 상품 문장이다. 직접 19 → **17** · 묶음 · 계열 ref 18 → 20 | 표를 고친다(P2-1 과 함께) |
| P2-3 | 다른 계열을 가리키는 포인터가 남음 | `keep_ref` 의 문제 항목 판정은 항목의 modality_ref 목록에 이 계열이 있는지만 본다. 그래서 같은 항목의 다른 원소 포인터 `…/modality_ref/1 → M7`(IND-3262 · 3266 · 3270) · `…/modality_ref/0 → M7`(IND-3268)도 근거로 남았다. 같은 줄에 M9 원소 포인터가 따로 있어 근거는 성립한다 | 포인터 끝이 `modality_ref/<k>` 면 그 값이 이 계열일 때만 남긴다 |
| P2-4 | `gap3-survey-a.json` 이 실행마다 줄 차례가 다름 | 같은 입력으로 두 번 돌리면 md5 `9d2dc546…` ↔ `fee1adec…` 다. 내용(정렬 뒤)은 원본과 같고, 셈 출력도 같다. 집합 순회 차례(PYTHONHASHSEED) 탓으로 보인다 | 출력 전에 정렬하거나 `sorted()` 로 순회한다. 그래야 바이트 재현이 된다 |
| P2-5 | 「근거 없음」 에 계열 원장 문장이 고민을 직접 적은 쌍 5 | M3 「깊은 주름 (팔자주름, 볼 주름 등)」 × 명동점 PLLA · PDLLA · 무세포동종진피 · CaHA 얼굴 케이스 × 볼 주름 4 · M5 「꺼진 부위 … 팔자주름 등」 × CAS-1056 PRP 볼 × 팔자주름 1. silver 에 그 계열 줄이 없어 「계열 원장 줄」 꼴로 안 잡혔다(같은 M3 문장의 팔자주름은 CAS-1053 에 W 로 붙음) | 전수 꼴에 「bronze 계열 문장에만 있음(silver 계열 줄 없음)」 을 더해 센다. 이 5 쌍은 계열 줄 내림 판단(J6 ~ J22 와 같은 꼴)이라 사람 판단 표로 올린다 |

## 7. 한 줄

P1-1 과 앞 P2 5 는 모두 닫혔고, 재현(바이트 · 해시 · 전수 수 · §6 목록)은 다 같다. 새 지적은 근거 포인터 품질 · 분류 · 재현 안정성 P2 5 개다. 18105 를 새 gold(`ab5eebc9…`)로 재기동하는 것을 막을 지적은 없다.
