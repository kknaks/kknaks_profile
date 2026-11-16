# ERD v3 독립 검토 — 동결 여부

검토 2026-11-05 · 대상 `erd-v3.md`(정본) · `erd-v3.json` · `erd-v3-dictionaries.json` · `erd-v3-tuples.json` · 기준 `ERD-FROZEN.md`(v2.4 동결 조건) · `ERD-V3-CANDIDATES.md`(V3-1~8 의 「왜」) · 원장 브론즈 2판 `bronze/phub-ledger/`(21) · 1판 `phub-stg-2026-10-26/`(대조) · `bronze-ledger-column-report.md`. 검토자는 v3 를 쓰지 않았고 발주서·이전 판 본문·검토서·step*·silver-v3/lib 은 열지 않았다. `erd-v3-check.py` 는 읽지 않고 **재실행만** 했다(PASS 재현 · 아래 ②).

---

## ⓪ 동결 조건 유지 여부 (ERD-FROZEN 사용자 정의 3 · 명시 예외)

| 조건 | v3 | 판정 |
|---|---|---|
| 정의 1 — 시술 = (무엇을, 어디에, 어떻게) · 미상이면 접지 않음 · 조각 버리지 않음 · 엣지 끝 = 시술 튜플 | 세 칸·anchor 식별자·fold_condition 「세 칸 전부 사전 값」·technique_inheritance=false 그대로(json `tuple_rules.procedure`). V3-3 stopwords 는 조각을 버리지 않고 `qualifier_text`(참조 레코드 + R9/R12/R17/R18 속성)로 보존(tuples.json 실측 17 단어 전부 보존). V3-4 「부위 여럿」은 튜플 여럿(anchor `#s<i>`)이고 R12 끝은 튜플. V3-5 layer 조각은 `layer_fragments` 보존(칸 아님). V3-2 는 what 을 바꾸되 조각을 버리지 않는다 | **유지** |
| 정의 2 — 부작용 = (사건, 부위, 경과) · 원인 시술은 엣지 · 표현은 가리키기만 | V3-1 로 식별자가 **네 칸**(qualifier · 없음 = none 값)이 됐다. 원인 시술은 여전히 R15 엣지(R15 비고 「끝 튜플의 수식 칸은 튜플의 것 — 엣지에 넣지 않는다」), 표현은 원칙 D 그대로(expressions_create_units=false · 표현 유래 단위 0). 정의 2 를 **뒤집지 않고 확장**했다 — 확장은 사용자가 요구한 것(V3-1 「물질 기전도 하나 더」). 다만 §0 과 ERD-FROZEN 승계 문장은 여전히 「(사건, 부위, 경과)」라 적혀 있어 「그대로」주장이 문자 그대로는 거짓 → R-4 | **유지(확장) · 문장 정정 필요** |
| 정의 3 — 원장 불변 · 충돌 레코드 · 결정은 approved 만 · 안정 키 · 적용 순서 ①~⑦ | 원장: 2판 HASHES 21 재계산 일치 · 1판 대비 바뀐 값 **정확히 6**(CHANGELOG 와 같음). 충돌 ④ 기록·approved 만·적용 순서 ①~⑦(① 에 canonical_rename) 그대로. **안정 키에 구멍** — V3-4 가 만든 새 anchor `REF-…#s<i>` 가 결정 target·fold_approve anchors 목록에 없다 → R-1. 「결정 16 kind」문장도 17 로 바뀌어야 함 → R-4 | **유지 · 규칙 보강 필요(R-1)** |
| 명시 예외 — 부작용 축 none·미상은 값 | 그대로. qualifier none 도 같은 뜻의 값으로 둠(json `qualifier_none_is_value=true`) — 예외의 논리(「적히지 않음 ≠ 모름」)와 일관 | **유지** |
| ERD 를 다시 여는 조건 — 사전 값·동의어는 결정 | v3 가 사전에 직접 손댄 것 셋(조직층 5 · 수식 5 · 「공기색전」 동의어 제거 · 검산 M-11 로 그 밖 불변 확인). 앞 둘은 구조(새 kind·새 사전)가 요구한 값이라 ERD 몫. **동의어 제거 1건**은 결정 kind 로 표현할 수단(동의어 제거)이 없어 ERD 가 대신 한 것 — 뒤집음은 아니고 처리 방식 문제 → D-6 | 유지(관찰 1) |

**새 규칙 10건 중 정의 1~3·명시 예외를 뒤집는 것은 없다.** 구조 어긋남은 「정의 3 안정 키의 누락」(R-1) 하나이고, 나머지는 규칙 문장 불일치(R-2·R-3·R-4)다.

---

## ① 10건이 각각 「왜」를 충족하는가

| # | 한 줄 판정 | 어긋남 |
|---|---|---|
| V3-1 수식 칸 | **충족(구조)**. 「공기색전·카테터 관련 감염」[M16] → dict_tuples (색전, none, 미상, 공기) + (감염, …) — 사건을 쪼개지 않고 물질로 표현. 식별자 네 칸, 멤버 안 수식만(원칙 C), 붙지 않은 수식 extra_qualifiers 보존(원칙 B). | 실데이터에서 qualifier≠none **튜플 0**(카테터 미등록 → raw_name) · 「필러 색전」「지방 색전증」 표현은 후보조차 없음(색전증 미등록 · 필러는 다른 멤버) → **D-3(결정)**. 사건 동의어 「공기색전」 제거를 ERD 가 직접 함 → D-6. R30 규칙 문장이 아직 「세 쌍」 → R-4 |
| V3-2 괄호 안 회사·제품 | **규칙 충족 · 적용 0**. 후보 241 전수 · 회사 사전 닿음 0(「엘러간」≠「앨러간/애브비」) · 제품 닿음 2(쥬베룩볼륨·쥬베룩 — v2.4 와 결과 같음, what_basis 표시만 바뀜). 유사도 없음. | 「보톡스(엘러간)」은 dictionary_add(manufacturer 동의어) 뒤에야 → **D-2**. (a) 는 추정 지점 → ④ |
| V3-3 stopwords | **충족**. 조각을 버리지 않는다 — 19 단어 모두 `qualifier_text` 로 보존(tuples.json 재집계 17 단어 적중 = §9.5.10 표 · 회·차는 규격 정규식이 먼저 잡아 stopword 로 작동한 적 0). 정의 1 「조각 버리지 않음」과의 긴장은 v2.2 의 규격·등급 조각 처리(「튜플 칸이 아니라 수식」)와 같은 선례라 새 긴장이 아님. 통째 일치가 먼저라 「LDM 초음파 관리」(M15 시장가)는 떼지 않음 — 규칙대로. | 분류 항목(①)에 stopword 토큰이 생기면 갈 속성이 없다(지금 0건) → D-8(관찰) |
| V3-4 조합 기호 | **충족(구조)**. 「보톡스 이마+미간」→ product:보톡스×이마 + ×미간 · anchor `#s0/#s1` · R12 member_mode and ✔(두 자리 같은 라벨 → 같은 PRC ✔). 「실리프팅(PDO/PCL)」→ 바깥 하나 + alternatives[PDO, PCL] · or ✔. `+`/`/` 라벨 전수 66 = 내가 원장 참조 자리에서 직접 센 distinct 62 + 자리 중복 4(contraindicated_combos 6 은 package 속성 자리라 범위 밖 — 맞음). 기호 있는데 multi_site 로 남은 참조 0 ✔. | 「HIFU/RF」→ or · 「HIFU(슈링크/울쎄라)」→ 바깥 하나는 **HIFU·RF 미등록이라 지금은 ⑨** — 규칙은 실리프팅(PDO/PCL) 로 동작 확인, 예시는 사전 뒤 → **D-1**. 새 anchor `#s<i>` 가 안정 키 목록에 없음 → **R-1**. tuple_assign_multi 비고가 여전히 「참조 자리면 combo_ref」 → **R-3**. 2판에 부위 나열 `/` 1곳 잔존(「필러(팔자/볼)」) → D-5 |
| V3-5 조직층 kind | **충족**. site 26 = 21 + layer 5(값마다 원장 출처 — 피하 지방층 prevention M3/M7 · 피부 이름 M7/M14 등 grep 확인). 부작용 site 네 kind · 시술 site 는 anatomical·region 만, layer 조각은 `layer_fragments`(시술 site 칸의 layer 0 실측). (괴사, 피부)·(괴사, 피하 지방층) 가 **가능**해졌다. 「엑셀V (혈관/홍조)」의 혈관은 layer 가 아니라 M8 하위분류 「혈관」에 닿음 — layer 가 시술 조각을 흡수한 사례 0. | 자동으로 갈리지 않음(「피부 괴사」「지방괴사」가 사건 동의어) · 「혈관 막힘으로 인한 피부 괴사」→ 후보 (괴사, 혈관) 같은 원인 자리 층 조각 후보 → **D-4** |
| V3-6 canonical_rename | **kind 는 충족 · id 불변 보장이 문장상 없음**. kind 17 · 적용 ① · old_as_synonym(renamed_from) · is_marketing_name. MOD-/CAT-/PRD-/PRC- 는 M 코드·계열 코드로 세워져 정준값과 무관 ✔. | 사전 항목 id 는 실측 **DIC-sha256(사전 이름\|정준값)**(modality 보톡스 = sha256(`modality\|보톡스`)[:10] = d73ced8043 확인) → 「같은 DIC- id 유지」는 현재 유도식과 모순 → **R-2** |
| V3-7 description·media_refs | **충족**. product·technique 에 description(출처 locator 필수)·media_refs[](path·sha256·captured_at·source·kind) · enum media_refs.kind · 새 브론즈 원천은 §5.1 표에 research_artifact 로 등록 후. 지금 null. | 없음(값은 원천 등록 뒤 · §12) |
| V3-8 기법 상속 하위분류 | **충족**. R5 from modality\|modality_subcategory · basis · canonical_mapping from_ref R5:<하위분류 id> · §9.5.6 M16 수액 = R5 intravenous 하나지만 하위분류 7(DCA·LIPO 포함) 로 scope 를 갈라 둠. 자동 상속은 여전히 false. | 없음(값은 결정) |
| V3-9 미해결·조합 anchor 지정 | **충족**. REF-sha256(norm(label)\|hint) 는 분해 결과와 무관한 안정 키 · 「세운다(덮지 않는다)」 · 지정값은 사전 값이어야(아니면 rejected) · 미해결 305 전부 target 후보. | `#m<i>` 는 적었으나 `#s<i>` 는 없음 → **R-1**(V3-4 와 같은 구멍) |
| V3-10 fold_approve 가 ⑦ 닫음 | **충족**. 규칙 ⑦ 문장 · fold_approve 비고 · conflict.status(resolved · decision_id · close_verdict 없음) · 쌍 아닌 ⑦ 은 conflict_close(not_same). 「단계 끝 = open 0」 두 길. | 없음 |

---

## ② 실측 대조 (원장 2판 원문 기준)

- **브론즈 2판**: `HASHES.txt` 21 ↔ `shasum -a 256` 재계산 전부 일치. 1판과 잎 단위 전수 diff → 바뀐 값 정확히 6(treatment-optimization 2 · treatment-sequence 4) = CHANGELOG. 키 구조 차이 0.
- **§9.5.11 `+`/`/` 전수**: 원장 참조 자리(optimal_combo · by_age_group · annual_plans · sequence · incompatible · minimum_intervals · problem-packages name/combo/products · comparison · market-pricing · synergy · taxonomy 항목 · timeline name)에서 기호 든 라벨을 직접 세어 distinct 62 — 표 66 행에서 자리 중복(보톡스 이마+미간 ×2 · HIFU/RF ×2 · 바이오스티뮬레이터/콜라겐부스터 ×3)을 빼면 62 **일치**. 2판 `+` 4곳 결과(multi_tuple 3 + 「필러 팔자+볼」⑨) tuples.json 과 일치 · 접으면 안 되는 것이 접힌 사례 0(모든 multi_tuple 멤버는 technique none 이라 anchor 고유 — 「보톡스 턱선」 단독 참조 PRC-1eda0394ce 와 「보톡스(턱선+광대)#s0」 PRC-493164c2e4 는 다른 튜플 · 규칙대로).
- **§9.5.10 stopwords**: tuples.json 의 멤버별 `stopwords` 를 재집계 → 17 단어 적중 집합이 표와 같음. 회·차 적중 6/8 은 규격 정규식 적중(미등록 0→0)이라 stopword 로 작동한 건 아님 — 표의 locator 는 참값이나 「stopword 적중」 표기는 과장. 미등록 조각에 새어 나온 stopword 0 ✔. 분류 항목·시장가 항목에 독립 stopword 토큰 → 시장가 4(콤보·동시·집중·「LDM 초음파 관리」) 중 앞 셋은 표에 있고 마지막은 통째 일치(CAT LDM초음파관리)라 규칙상 미적용 ✔.
- **§9.5.9 company_paren**: 적용 2 건은 v2.4 와 결과 동일(product 조각 규칙 2 가 이미 what=product) — §9.5.11 「v2.4 와 다른 참조 11」에 없음 ✔. 「엘러간」 9 자리 원문 확인 ✔.
- **§9.6.7 qualifier**: 「공기색전·카테터 관련 감염」 M16 원문 ✔ · 「혈전정맥염」 taxonomy safety 원문 ✔ · 수식≠none 튜플 0 · layer 튜플 0 → 네 칸 키로 바꿔도 분할이 세 칸 키와 같을 수밖에 없다 → **「접힘 39=39 · exact 651 · match_status 변경 0」 은 논리적으로 성립**(재계산 없이도). 접두 가름이 「혈전정맥염」도 가르는 것은 §12 에 적혀 있음.
- **§9.6.8 layer**: 값 5 의 출처 grep 확인 · 시술 site 칸 layer 0 · 부작용 layer 튜플 0 · 후보 23 전부 exists=없음.
- **검산 재현**: `python3 erd-v3-check.py` 재실행 → 종합 PASS(NOTE 0) 재현.
- **주의(문구)**: §9.5.8 「엣지 끝 3,423」은 **자리 수**(multi_tuple 자리 1로 셈)다. R12 는 「각각 붙는다」이므로 실제 엣지는 자리당 2 — 수치 자체는 틀리지 않으나 「엣지 끝 수」로 읽으면 4 적다.

---

## ③ 행선지 표본 20 (seed 31105 · 원장 21 잎 키 573 에서 · 2판 원장으로 경로 존재·횟수 확인 · ERD 표적 존재 확인)

| # | 파일 | 경로 | 타입×횟수 | 표적 | 2판 | 표적 |
|---|---|---|---|---|---|---|
| 1 | products.json | `biostimulator.products[].country` | str×6 | dict:country | 6 ○ | ○ |
| 2 | procedure-profiles.json | `profiles[].createsChannel` | bool×17 | modality.flags.createsChannel | 17 ○ | ○ |
| 3 | anatomy-danger-zones.json | `zones[].vessels[].depth_mm` | float×22 | R21.depth_mm | 22 ○ | ○ |
| 4 | taxonomy.json | `modality[].subcategories[].items[].extracted.indications.extended[]` | str×10 | catalog_item.indications_extended | 10 ○ | ○ |
| 5 | procedure-comparison.json | `comparisons[].procedures[].duration` | str×39 | R12.duration | 39 ○ | ○ |
| 6 | taxonomy.json | `modality[].subcategories[].items[].correction_note` | str×1 | decision.reason | 1 ○ | ○ |
| 7 | consent-checklist.json | `categories[].contraindications[]` | str×105 | person_condition.name | 105 ○ | ○ |
| 8 | combo-recipes.json | `recipes[].subtitle` | str×7 | package.subtitle | 7 ○ | ○ |
| 9 | problem-packages.json | `problems[].complaints[].procedures[].role` | str×254 | R9.role | 254 ○ | ○ |
| 10 | problem-combos.json | `combos[].packages[].clinicalRationale` | str×24 | package.clinical_rationale | 24 ○ | ○ |
| 11 | products.json | `updated` | str×1 | source_file.updated | 1 ○ | ○ |
| 12 | combo-recipes.json | `recipes[].id` | str×7 | package.aliases | 7 ○ | ○(aliases 공통 필드) |
| 13 | anatomy-danger-zones.json | `zones[].danger_level` | int×11 | site.danger_level | 11 ○ | ○ |
| 14 | products.json | `prp_exosome.products[].mfds` | bool×5 | product.mfds | 5 ○ | ○ |
| 15 | taxonomy.json | `modality[].subcategories[].id` | str×74 | modality_subcategory.code | 74 ○ | ○ |
| 16 | extracted.json | `{code}.safety.serious[]` | str×37 | adverse_expression.text | 37 ○ | ○ |
| 17 | complications.json | `categories[].complications[].duration` | str×19 | R15.duration | 19 ○ | ○ |
| 18 | products.json | `stem_cell.category_id` | str×1 | R4.from(modality) | 1 ○ | ○(끝 표기) |
| 19 | pih-risk.json | `procedures[].prevention` | str×26 | R15.prevention | 26 ○ | ○ |
| 20 | anatomy-danger-zones.json | `zones[].filler_specific.preferred_product` | str×11 | R22.preferred_product | 11 ○ | ○ |

20/20 일치(경로·횟수·표적). 미정 0 · v2.4 대비 이동 0 주장은 표본 범위에서 반례 없음.

---

## ④ 추정·유사도 매칭 허용 지점

| 어디 | 무엇 | 성격 |
|---|---|---|
| V3-2 (a) 회사 괄호 | 「X(회사)」→ X 의 계열 안 **그 회사 제품이 정확히 하나일 때** 그 제품 | 결정론(사전 조인)이지만 **원문이 말하지 않은 제품을 고르는 유일한 추론**. 하나가 아니면 ambiguous(company_product). 지금 적용 0 |
| V3-1 접두 가름 | 통째 사전에 없는 토큰을 「수식 사전 접두 + 사건 사전 나머지」로 한 번 가름(공기색전 · 혈전정맥염) | 완전 일치 두 번이지만 **토큰 내부 분할**이라 새 조각을 만든다. 유사도 아님 · 결과는 후보/dict_tuples 에만(단위 0) |
| V3-4 `/` 해석 | 기호 뜻을 양쪽 조각 종류(부위/primary)로 정함 · 괄호 안 대안은 바깥 하나 | 기호 해석 규칙. 한쪽 부위·한쪽 primary 인 `/`(예 「보톡스 이마/필러」)의 처리는 명시 없음(원장에 사례 0) |
| 그 밖 | 정규화 완전 일치·사전 동의어만. 유사도는 ⑦ 후보로만 | v2.4 그대로 |

---

## ⑤ 동결 판단

**동결 가(可) — 정의 1~3·명시 예외를 뒤집는 규칙은 없고, 10건 모두 구조·규칙으로 반영됐다. 단 안정 키 누락 1 과 규칙 문장 불일치 3 은 동결 문서에 넣기 전에 문장으로 닫아야 한다.**

어긋남 집계: **구조·규칙 4**(R-1 안정 키 누락 · R-2 · R-3 · R-4 문장 불일치) · **결정으로 처리 가능 8**(D-1~D-8).

### 동결 전 꼭 고칠 것 (구조·규칙만 · 전부 문장 수정으로 닫힘 · 실측 재실행 불필요)

| # | 어디 | 무엇 | 왜 구조·규칙인가 |
|---|---|---|---|
| R-1 | §1.1 결정 target 규칙 · §5.2 tuple_assign/tuple_assign_multi target · fold_approve anchors · json decision_target_rule/decision_anchor_rule | 허용 anchor 에 **`REF-…#s<i>`**(V3-4 부위별 튜플) 추가 | 정의 3 「안정 키」. 지금 문장대로면 「보톡스(턱선+광대)#s0」와 「보톡스 턱선」(단독 참조)을 fold_approve 로 접을 길이 없고, tuple_assign 으로 그 자리의 technique 을 줄 수도 없다. 결정 레코드로 못 푼다 |
| R-2 | §5.2 canonical_rename · json rename_rule · 사전 id 유도식 | 「같은 DIC- id 유지」가 성립하는 **id 규칙**을 적는다 — 코드 있는 사전(modality 등)은 DIC-sha256(사전\|code), 없는 사전은 최초 발급 id 고정(renamed_from 로 추적) 중 하나 | 지금 실측 id 는 sha256(사전\|정준값)이라 rename 하면 id 가 바뀐다 — V3-6 의 「왜」(id 안 바뀜)가 문장으로 보장되지 않음 |
| R-3 | §5.2 tuple_assign_multi 비고 | 「참조 자리면 package(kind=combo_ref)」→ V3-4 와 맞춘다: 같은 what × 부위 여럿이면 multi_tuple(R12 각각 · member_mode and · anchor #s<i>), primary 둘 이상이면 combo_ref(member_mode 지정 칸 new_value 에 추가) | 같은 결정이 두 모양(combo_ref 패키지 vs 튜플 여럿)으로 적용될 수 있음 — 빌더 해석 갈림 |
| R-4 | §0 · ERD-FROZEN v3 판 승계 문장 · R30 규칙 · §5.2 target 규칙 첫 문장 | 정의 2 를 「(사건, 부위, 경과[, 수식 — 없음은 none 값])」로, 「결정 16 kind」→ 17, R30 edge_create ref 「세 쌍」→ 네 쌍, target 규칙 첫 문장의 「세 쌍」 잔재 삭제 | 동결 문서가 「그대로」라 적어 두고 식별자는 네 칸인 상태 — 다음 검토가 같은 자리를 다시 연다 |

### 동결 후 결정으로 (동결을 막지 않음)

| # | 무엇 | kind |
|---|---|---|
| D-1 | HIFU · RF · 필링 · MTS · LED 등 계열/장비 동의어 — 들어가면 「HIFU/RF」→ combo_ref(or) · 「HIFU(슈링크/울쎄라)」→ 바깥 하나(규칙은 이미 동작 확인) | dictionary_add(modality 동의어) |
| D-2 | 「엘러간」→ 「앨러간/애브비」 동의어 · 「더모톡신」은 회사 아님 | dictionary_add(manufacturer) |
| D-3 | 「카테터」 등록 또는 「공기색전·카테터 관련 감염」 adverse_tuple_assign → (색전, none, 미상, 공기) 단위 세움 · 「색전증」 동의어 · 「혈전정맥염」 가름 결과 승인/반려 · 「섬유화」 기전 이동 여부 | dictionary_add · adverse_tuple_assign · event_split |
| D-4 | 「피부 괴사」「지방괴사」→ (괴사, 피부)·(괴사, 피하 지방층) 지정 · 원인 자리 층 조각 후보(「혈관 막힘으로 인한 피부 괴사」→(괴사, 혈관)) 거름 · region 바디·두피 | adverse_tuple_assign · event_split · dictionary_add(site) |
| D-5 | 2판 원장에 부위 나열 `/` **1곳 잔존**: treatment-optimization annual_plans 「필러(팔자/볼)」(README 규칙 위반 · 「팔자」 미등록이라 지금은 ⑨ · V3-4 는 and 로 읽음) → 브론즈 3판 CHANGELOG 또는 그대로 두고 「팔자」= 팔자주름 동의어 | 원천(브론즈 판) · dictionary_add(site) |
| D-6 | 「공기색전」 동의어 제거를 ERD 가 직접 한 것 — 결정 kind 로 표현할 수단이 없음. 이번 1건은 구조 요구로 받아들이되, 앞으로 같은 일은 event_split 변형(동의어 분리) 또는 기록 결정으로 남길지 | scope_review |
| D-7 | 「엑셀V+」「NAD+」 등 꼬리 `+` 항목(v2.4 1-D 승계) — `+` 「항상 함께」 규칙과 충돌하는 제품명은 통째 일치 사전 값으로 | dictionary_add(product/catalog_item_name) |
| D-8 | 분류 항목(①)에 stopword 독립 토큰이 생길 때 qualifier_text 가 갈 속성이 없음(지금 0건) · market-pricing ③ 의 qualifier_text 보관 속성 명시 | scope_review(다음 판) |

그 밖 관찰(어긋남 아님): §9.5.8 합계는 자리 수(②) · 회·차는 규격 정규식 적중이라 stopword 목록에서 실효 없음 · V3-5 의 layer 가 시술 조각을 흡수한 사례는 0 이나 「혈관」처럼 같은 글자가 하위분류 라벨과 겹치는 값은 사전 우선순위(product → subcategory → … → site)에 기대고 있다.
