# 검수 — SPEC-005 · WORK-003 (허브 골드 구현 전 게이트)

**FAIL** · FAIL 5 · WARN 9 · **open = 3**(SPEC §7 O-1 · O-2 · O-3 — 셋 다 「안 막음」. F-5 를 열린 것으로 옮기면 4)

- 기준: `_RESUME.md` §2(10-26 경계 · 10-27 W-1 · 10-29 reading_contract · 10-30 전 행) · `semantic.json` · 실버 `step1` ~ `step8` json · `step7-decisions.json` · `gold-research.md/.json` · `quality-eval-set.json` · `quality-report.md`
- 대상: `SPEC-005.md`(13:27) · `WORK-003.md`(13:28) · `SPEC-004.md` · `WORK-002.md`(대체 표시)
- 대조 시점: 2026-10-30 13:30 무렵 실물. 칸 경로 · 셈은 전부 스크립트로 실물 json 을 읽어 확인했다. 쌍 셈은 `step8-apply.py` 의 `UnitSets` 를 import 해서 다시 계산했다(파일은 쓰지 않음)
- 가상 문장 · 미래 원천은 보지 않았다. 지적 근거는 지금 데이터와 결정표뿐이다
- 골격(허브 = 골드 그래프 + 결정론 도구 9 · LLM 0 · 충돌은 resolved 하나 · 안전 늘 동봉 · 빌드 때 펼침 · 해시 가드)은 결정과 맞는다. **FAIL 5 는 모두 문장 몇 줄만 고치면 풀린다.** 그중 F-1 · F-2 · F-3 은 SPEC-004 가 떨어진 것과 같은 꼴(계약 · 가드가 실물과 다름)이다. 이대로 구현하면 Phase 2 빌드가 가드에 걸려 발행되지 않거나 카드 칸이 비게 된다

---

## FAIL

### F-1 · 카드 원문 칸이 실물에 없다 — §2-2 step5 행 · §5-4 카드 칸 대응

- SPEC: §2-2 step5 `extracted[] · taxonomy_products[]` → 「카드 원문(개요 · 기전 · 발현 · 지속 · 사후관리)」. §5-4 overview · method = `extracted[] · taxonomy_products[] source_text.overview · mechanism` · recovery = `extracted source_text.onset_duration.*`
- 실물 `step5-units.json`: `extracted[521].source_text` 칸은 `aftercare` 521 · `safety.common` 521 · `safety.serious` 189 · `safety.note` 4 · `safety.contraindications` 4 · `safety.long_term` 1 **뿐**이다. `taxonomy_products[59].source_text` 도 `aftercare` · `safety.common` · `safety.serious` · `safety.note` · `safety.contraindications` 뿐이다. `overview` · `mechanism` · `onset_duration` 은 **0행**
- 실물에서 그 내용이 있는 곳: `step8 safety.family_text[계열]["환자 설명 가이드(patient-education)"][]` 의 `simple_explanation` · `how_it_works` · `duration_simple` · `pain_level` · `downtime` · `common_concerns`(17계열 전부) · `evidence.statements[].field` moa 50 · effects 37 · adverse_effects 32
- 고칠 것: §2-2 step5 행의 설명을 「aftercare · safety.*(부작용 덮어쓰기 원문)」로 바꾼다. §5-4 overview · method · recovery 에서 `extracted source_text.overview · mechanism · onset_duration` 을 빼고 위 실물 칸만 남긴다. 단위 시술 · 제품마다 개요 문장이 따로 없다는 사실은 「허브 보강 후보」(§3-6)에 넣는다

### F-2 · G9 가드가 지금 실물에서 걸린다

- SPEC G9 가드: 「override 행의 `override_of` 가 실버 계열 부작용에 없는 계열이면 실패」
- 실물: 덮어쓰기 624행(product_links 376 + units 248) 중 **72행**은 `override_of` 가 `step8 safety.side_effects[]` 에 없는 계열이다. family:N1 63 · N4 4 · N5 2 · N2 1 · N6 1 · N7 1. 이 계열들은 `safety.side_effect_gap_families`(N1 · N2 · N3 · N4 · N5 · N6 · N7 · N8 · N9 · N10)다. 계열 부작용이 gap 인 계열에서는 아래 수준 값이 유일한 값이므로 데이터는 맞다. 가드 문장이 틀렸다
- 그대로 구현하면 빌드가 `rejected` 되어 발행 0 → Phase 2 완료 조건을 못 채운다
- 고칠 것: 가드를 「`override_of` 가 계열 노드(27)에 없으면 실패」로 바꾼다. 계열 부작용이 gap 인 계열을 덮은 행은 `override_of` 를 남기고 계열 쪽 상태를 「정보 없음(gap)」으로 둔다

### F-3 · G15b 가드가 지금 실물에서 걸린다(문장 그대로 읽으면)

- SPEC G15b 가드: 「겉 same_day 가 채워졌는데 방향별 값이 다르면 실패」
- 실물: `resolved.by_direction` 이 있는 118개(엣지 56 + resolved_pairs 62) 중 **11개**는 겉 `same_day` 가 채워져 있고, 한쪽 방향은 같은 값 · 다른 쪽은 `None` 이다. 엣지 E8-0061(True · True/None) · E8-0114 · E8-0115(False · False/None) · E8-0184(True · True/None) 등과 쌍 5(False · False/None)
- 8단계 자체 가드(`step8-apply.py:2008`)는 `None` 을 빼고 「값이 둘 이상」일 때만 막는다. SPEC 문장은 `None` 을 다른 값으로 셀 수 있어서, 구현하면 11건으로 빌드가 막힌다
- 고칠 것: 「겉 same_day 가 채워졌는데, `None` 을 뺀 방향별 same_day 값이 둘 이상이면 실패(`step8-apply.py:2008` 과 같은 식)」

### F-4 · T9 vocab 의 메뉴 이름이 G18 · 코디 10-30 결정과 어긋난다 — §5-10

- 결정(_RESUME 10-30 코디 판단): 「판단 ② 메뉴 이름 = 사이트 추천 패키지 라벨 8개 전부」. SPEC G18 · §3-0 도 8개다
- §5-10 출력: 「메뉴 이름(**앵커 없는 조합의 source_label**)」. 실물에서 고민 앵커가 없는 「고민 패키지」 조합은 3개이고 셋 다 `쁘띠시술` 이다. 이대로 만들면 vocab 에는 메뉴가 1개만 나온다. 나머지 7개(주름 · 처짐/탄력 · 피부결/톤/항노화 · 색소/미백 · 모공 · 흉터 · 얼굴윤곽)는 Jev 슬롯 선택지에서 빠진다
- 고칠 것: 「메뉴 이름(G18 라벨 8 — `kind == 고민 패키지` 의 `anchor.source_label`)」

### F-5 · G18 이 사전 mode 를 「후보」로 바꾸는 새 규칙을 「정해진 것」처럼 넣었다 — §3-1 G18

- SPEC G18: 「같은 norm 행이 있으면 대상만 더함(**mode 는 「후보」**)」
- 실물 사전 8개 라벨 행의 지금 mode: `주름` 후보 · `처짐/탄력` **전부**(P3 · P4-1) · `피부결/톤/항노화` **전부**(J10 · P4 · P5) · `쁘띠시술` · `색소/미백` · `모공` · `흉터` · `얼굴윤곽` 하나. 「전부」는 10-29 사용자 결정 「묶음 이름은 각 고민에 모두 붙인다」에서 온 값이다(semantic mode 「전부」 = 갈래 A · I)
- 10-30 코디 판단이 정한 것은 「라벨은 골드 빌드가 resolve 사전에 kind menu(실버 수정 없음) · 고민 id 질의는 그대로」까지다. 기존 고민 대상의 mode 를 「전부 / 하나 → 후보」로 바꾸는 결정은 결정표에 없다
- 영향(지금 데이터): I-01 문항 12개(Q004 · Q005 · Q006 · Q007 · Q012 · Q013 · Q016 · Q017 · Q020 · Q021 · Q024 · Q025)의 `concern_text` 가 라벨이다. mode 가 바뀌면 이 문항들의 T1 결과가 바뀐다. §6-1 은 이 경우를 어떻게 다룰지(I-01 은 menu 후보를 무시하는지 등) 말하지 않는다
- 고칠 것(둘 중 하나 · 코디 판단): ① 고민 대상의 mode 는 그대로 두고 `menu:` 대상은 같은 match 안의 별도 후보로 낸다(mode 를 바꾸지 않음). 또는 ② §7 열린 것으로 옮긴다. 어느 쪽이든 §6-1 I-01 경로에 「T1 후보 중 concern · site 만 쓴다(menu 는 I-11 만)」를 적는다

---

## WARN

| id | 곳 | 무엇 | 실물 근거 | 고칠 것 |
|---|---|---|---|---|
| W-1 | §3-3 가드 문단 | 「엣지가 둘 이상 닿는 단위 쌍 2,048 · 그중 resolved_pairs 100」이 맞는지는 **전역 엣지 E8-0001 을 뺀** 값일 때만이다. 빼지 않으면 2,075 · 105(8단계 summary `unit_pairs_checked` 4,791 · `resolved_pairs` 105). 기준이 적혀 있지 않다 | `UnitSets` 로 다시 셈: 229엣지 → 쌍 4,674 · ≥2 2,048 · rp 100 / 230엣지 → 4,791 · 2,075 · 105 | 「(전역 엣지 G16 제외)」를 붙인다. rp 105 중 5개는 전역 엣지 때문에만 생긴 쌍이라는 점도 적는다 |
| W-2 | §3-3 확인 조건 등급 | 대상 키를 units · product · family · all 로만 적었다. 실물 `conditions.resolved` 에는 `ledger` 3(KR8-0212 ~ 0214 · ledger:auto-6-…)이 있다(§2-2 셈에는 들어 있음). 그리고 ledger 3 · product 7(M1-1-7 · M9-2-3 등)은 단위 시술을 하나도 덮지 않는다(UnitSets 빈 집합) | `conditions.resolved` target 셈 family 195 · units 20 · all 16 · product 7 · ledger 3 | ledger 키를 넣는다. 단위 시술 0 대상 행은 어디에 붙는지(제품 카드 · T5 `id=product` 만) 적는다 |
| W-3 | §3-2 · WORK-003 Phase 2 | §3-2 빌드 순서에 G18 단계가 없다. WORK-003 Phase 2 는 「§3-2 순서 그대로」라면서 facts 뒤에 「메뉴 라벨(G18)」을 끼워 넣었다 | — | §3-2 에 G18 단계를 넣고(사전 적재 단계) WORK 와 맞춘다 |
| W-4 | §6-1 의도 → 도구 | I-09 → T5 만. Q101(「소프웨이브 · 통증 민감」, must_show 「시술 중 열감과 뻐근함이 있음, 부위에 따라 마취 크림 사용」)의 원문은 `family_text.M9["환자 설명 가이드"].pain_level` 에 있다. T5 출력(`not_condition` = 「상담 · 준비 · 고지」 칸)에는 없다. 실버 판에서 맞던 문항이 골드 판에서 틀릴 수 있다 | 문자열 위치: step8-relations.json 환자 설명 가이드 M9 | I-09 중 확인 조건 노드가 없는 문항은 T3 `sections`(overview/ops)로 답한다고 적는다 |
| W-5 | §3-3 · §5-5 | 같은 단위 시술끼리의 쌍(self pair)을 다루는 규칙이 없다. 8단계 쌍 셈은 u == v 를 건너뛴다(`step8-apply.py:2027`). 실물 self_pair 엣지는 4개(E8-0059 M2↔M2 days [14,14] first a · E8-0214 · E8-0225 · E8-0228)이고, 채점 문항 Q091(「필러 · 필러」 min_days 14)이 이것을 쓴다 | `edges[].self_pair` True 4 | T4 에 같은 id 두 번 · self_pair 엣지 값 읽기를 적는다 |
| W-6 | G6 · §5-3 ③ | 부위 층 거르기에서 `step7-decisions site_rules.site_free`(「해당 없음」 · 「병변 단위」) 통과가 빠졌다. 품질 2차가 이것으로 고친 문항이 있다(quality-report §0-1 「점제거 → 병변 레이저」) | `site_rules.site_free = ["해당 없음","병변 단위"]` | ③ 에 「site_free 단위 시술은 층 거르기 통과」를 넣는다 |
| W-7 | G9 우선순위 | `priority` 칸을 어느 방향으로 읽는지(작을수록 먼저)와 `단위 시술 후보` 수준이 빠졌다 | 실물: 0 = 제품 × 계열 × 키 하위 111 · 1 = 제품 × 계열 207(+ taxonomy 58) · 2 = 단위 시술 159 · 3 = 단위 시술 후보 89 | 「priority 작을수록 먼저 · 0 < 1 < 2 < 3 < 계열」 |
| W-8 | 결정 반영 표시 | 머리 표가 「골드 판단 ①~⑤」를 적지만 본문에 ⑤(다파장 4 KTP 보조 하위)를 추적하는 줄이 없다. 데이터는 이미 실버에 들어가 있다(노블린 · 클라리티2 · 아포지 엘리트 플러스 · 디스커버리 피코 `also_sub_families` 에 KTP — G5 로 반영됨) | step2 product_family 4행 | §3-0 또는 G5 에 「⑤ = 실버 step2 반영분을 G5 가 읽음」 한 줄 |
| W-9 | 낡은 문장 · 줄 번호 | §2-1 「`semantic.md` 머리 입력 해시 줄이 step2 · 5 · 7 에서 json 과 다르다」는 지금은 틀리다(13:21 재생성 · 11/11 같음). `semantic-build.py:661` → 실제 662. `step8-apply.py:2022-2050` 의 `covers` 정의는 1976 | semantic.md 5행 | 문장을 지우거나 「md 는 읽지 않는다」만 남긴다. 줄 번호를 고친다 |

---

## 항목별 대조

### 1. 입력 계약 §2 — 실물 대조

| 확인 | 결과 |
|---|---|
| §2-1 파일 12 · version 칸 | 12/12 같음(semantic `semantic-v1` · step1 `2` · … · step3-lexicon `1.1`) |
| §2-1 sha256 앞 16자 11 | 11/11 같음 — `semantic.json inputs{}` 11 = 실물 파일 해시 11 |
| semantic 노드 13 · 합 1,071 · 엣지 21 · 합 3,179 · 사전 2,053 · ids.map 1,071 · string_forms 8 · silver_string_map 41 · flags 12 · gate 3 · inheritance 9 · statements 119 | 전부 같음 · 칸 이름 전부 있음 |
| resolve_rules{normalize, fold, strip_chars, split, order 4, tails 「주사 · 시술」, prefix_min 2, prefix_rule} | 같음 |
| step1 items 395 · active 354 · recommendable 236/118 · lines 11 · line_item 5 · 칸 `ledger_id · 2_names.display_name · search_names · 1_identity · 4_license{status, recommendable, licenses} · 5_spec · 6_companies · evidence · open` | 같음 |
| step2 families 27 · product_family 354 → 엣지 370(semantic) · 칸 | 같음 |
| step3 nodes 53 · step4 nodes 26 · family_defaults 27(family_technique 34) · unit_procedure_attrs{safe_layers, target_muscles, landmarks} | 같음 |
| step5 units 162 · side_effect_override 단위 96 · product_links 354 · inherited_candidates 1,379 · override 제품 316 · uses_product 44 · rules.product_link 5칸 · extracted 521 · taxonomy_products 59 · pih 26 · 해당 없음 77 · gap 63 · dose_range 11 | 셈 · 칸 이름 같음 — **단 `source_text` 안 칸이 다름(F-1)** |
| step6 packages 24(false 2) · contains 49 · slots 8(후보 22) → 엣지 71 | 같음 |
| step7 고민 57(semantic) · 목적 13(`purposes[]` 30행 중 `node: true` 13 — 행 수가 아니라 node 셈) · edges 437 · layer 부위 119 · 상위 35 · null 283 · ccs 180 · combos 79 · 구성 581(462 · 107 · 12) · 라벨 8(4 · 4 · 3 · 3 · 3 · 3 · 2 · 2) | 같음 |
| step7-decisions `site_rules{lowering, climb, concern_region}` | 있음(+ `site_free` — W-6) |
| step8 edges 230 · resolved 230(칸 14 전부) · by_sub_condition 32 · by_direction 56 · resolved_pairs 105 · claims 395 · avoid 5(false 3) · conditions nodes 53 · claims 336 · resolved 241(family 195 · units 20 · all 16 · product 7 · ledger 3) · wait_resolved 1 · not_condition 37 | 같음 |
| step8 safety 35 · 72 · 22 · 10 · 26 · family_text 17 · unit_safety_status 162 · unit_gaps 17 · gap 10 · 12 · family_text 칸 이름 13종 | 같음 |
| step8 evidence 119 · 25 · 29 · 15 | 같음 |
| reading_contract(SPEC §3-3) ↔ step8 · semantic `reading_contract` 원문 | 같은 뜻 |

SPEC-004 꼴(「계약 칸이 실물에 없음」)은 **1곳**(F-1)이 남았다.

### 2. 결정 반영(_RESUME §2)

| 결정 | SPEC 자리 | 판정 |
|---|---|---|
| 10-26 경계 — Hub = 그래프 + 범용 tool · LLM 0 · 안전 늘 동봉 · 노드 검색 결정론 · 후보만 · Jev 선택지 = 노드 목록 · 스키마 | §1-1 B-1 ~ B-5 · §1-2 · G13 · T1 · T9 | 들어감(T9 메뉴 F-4) |
| 10-26 키는 env 로만 | WORK Meta 「실명 · 키 넣지 않음」 · `.env.gold` git 제외(레포 `.gitignore` `.env*` 확인) | 들어감 |
| 10-27 W-1 — 기본 응답 거르기 · 동의어 여러 노드면 후보 전부 | G12 · §5-0 후보 여럿 · T1 mode 후보 | 들어감 · 「미확인」은 상태가 아니라 표시(semantic B12 · D-05)로 바뀐 뒤의 값과 맞음 |
| 10-29 reading_contract | §3-3 · G14 · G15 · G15b · D-10 | 들어감(가드 문장 F-3) |
| 10-29 「처음부터 · 뼈대만 재사용」 | 머리말 · §1-3 · WORK 비목표 | 들어감 |
| 10-30 골드 = 규칙 적용 그래프 + 허브 도구 탐색 | §0 · B-1 · D-01 | 들어감 |
| 10-30 허브 고정 · 병원 무관 · 연결 층 = 앱 · 보강 후보 목록만 | §1-2 · §3-6 · I-12 도구 없음 | 들어감 |
| 10-30 D-13b 충돌 하나로 resolved | §3-0 G14 정정 · §3-3 · G14 가드 | 들어감 |
| 10-30 품질 목표 6 | §6-1 표(목표 · 지금 값 = quality-report 최종 · CC 슬롯 열과 같음 0.991 · 0.984 · 1.0 · 1.0 · 0 · 0 · 98.4 · 0.5) | 들어감 |
| 10-30 골드 판단 ① CC 슬롯 | T2 `cc` · §6-1 | 들어감 |
| ② 메뉴 → 조합 · 코디 「라벨 8 전부」 | G18 · T1 · T7 ② | 들어감 — 단 **mode 변경은 결정 밖(F-5)** · vocab 어긋남(F-4) |
| ③ 추천 패키지 먼저 · 나머지 6종 「참고」 | T7 ③ · §6-1 채점 범위 | 들어감 |
| ④ treats 계열만은 펼치지 않음 | §3-0 G3 · G3 | 들어감 |
| ⑤ 다파장 KTP 보조 | 실버 반영분 G5 로 읽음 | 데이터로 들어감 · 추적 줄 없음(W-8) |
| D-01 ~ D-14(D-08 정정) | D-01 §0 · D-02 G3 · D-03 G5(셈 1,379 로 고침) · D-04 G17 · D-05 G12 · D-06 G13 · §3-4 · D-07 G9(실버에서 읽음 — 정정) · D-08 G14(정정) · D-09 G15 · D-10 §3-3 · D-11 T1(tails 단계 포함 order 4) · D-12 T2 ④ · D-13 G6 · T2 ③ · D-14 §5-0 · §5-11 | 14/14 |
| D-15 · D-16 (결정표 밖) | §7 O-1 · O-3 열린 것 | 맞음 |
| D-17 · D-18 | 10-30 경계 결정과 같다는 근거로 열린 것 아님 | 근거 있음 — 맞음 |
| U-1 = ② | G6 · T2 ③ layer 상위 | 들어감 |
| U-2 · U-3 앱 몫 | §1-2 · §7 끝 · T3 market 「요청 때만 · 표시 여부 앱」 | 들어감 |
| KOS = 기록만 | §1-2 · WORK 비목표 | 들어감 |
| hub-evals 골드 뒤 | §1-2 | 들어감 |

결정에 없는 새 결정을 「정해진 것」으로 넣은 곳: **F-5 하나**. 나머지 새 값(REST 경로 · 포트 · 테이블 이름 · `--gold` 측정 모드 · 재시작 반영)은 구현 세부라 결정이 필요한 자리가 아니다.

### 3. 골드 규칙 §3 — 지금 실버로 셈

| 규칙 | 가드 · 셈 | 실물 | 판정 |
|---|---|---|---|
| G2 합병증 펼침 | = units_inherit 합 285 | 285 | 맞음 |
| G5 I4 | 제품마다 = inherited_candidates · 저장 44 | 1,379 · 44 | 맞음 |
| G9 덮어쓰기 | override_of ∈ 계열 부작용 | 72행 벗어남 | **F-2** |
| G10 | 162 덮음 | 162 · 상태값 3종(값 있음 484 · gap 411 · 해당 없음 77) | 맞음 |
| G14 쌍 | 단위 쌍마다 값 하나 | 8단계 two_value 0 · 셈 기준 W-1 | 맞음(W-1) |
| G14 조건 | 단위 × 조건 등급 하나 | 가장 구체적 대상끼리 등급이 갈리는 단위 × 조건 0 | 맞음(W-2) |
| G15 | 옵션 칸 겉 칸 null · 「조건 모름」 칸마다 1 | by_sub_condition 90(엣지 32 + 쌍 58) — 겉 칸 채워짐 0 · 조건 모름 ≠ 1 0 | 맞음 |
| G15b | 겉 same_day ↔ 방향별 | 11건 문장상 걸림 | **F-3** |
| G16 | 모든 시술 1 · target all 16 | 1 · 16 | 맞음 |
| G17 | = 581 | 581 | 맞음 |
| G18 | 라벨 8 · 라벨마다 패키지 1+ | 8 · 최소 2 | 맞음(F-4 · F-5) |
| §3-0 정정 3곳(G14 · G9 · G17) | gold-research 대비 | G14 = 10-30 D-13b · G9 = 실버 칸 96 · 316 실재 · G17 = semantic 581 실재 | 셋 다 맞음 |

### 4. 도구 §5 — 의도 12 · 문항 111

| 의도 | 문항 수 | 도구 | 문항 슬롯 → 도구 입력 | 판정 |
|---|---|---|---|---|
| I-01 | 31 | T1 + T2 | concern_text → T1 → concerns · site · cc(28) | 덮음(F-5 menu 후보 처리) |
| I-02 | 10 | T1 + T3 | procedure | 덮음(원문 칸 F-1) |
| I-03 | 7 | T1 + T3 | procedure · topic → sections | 덮음 |
| I-04 | 10 | T1 + T3 | procedure → sections=safety | 덮음 |
| I-05 | 5 | T1 + T3 | procedure → recovery | 덮음(F-1 — recovery 칸) |
| I-06 | 7 | T6 | procedures | 덮음 |
| I-07 | 16 | T4 | procedures · same_day · split_note · self_pair | self_pair 7 문항 중 Q091 규칙 없음(W-5) |
| I-08 | 1 | T4 prior | prior · procedure · elapsed_days | 덮음 |
| I-09 | 14 | T1 + T5 | condition_text · procedure · source · source_index | Q101 은 T5 밖(W-4) |
| I-10 | 4 | T1 + T3 | product · amount → dose · products | 덮음 |
| I-11 | 6 | T1 + T7 menu | concern_text → menu | 덮음 — 라벨 경로 + 추천 패키지만으로 Q106 ~ Q111 6/6 계열 집합 = 정답(직접 계산) |
| I-12 | 0 | 없음(연결 층) | — | 결정대로 |
| M2(말 → 노드) | — | T1 | — | 덮음 |
| M3 · M4 | — | gold-export.json | — | 덮음 |

①②③ 경로: ① T2 `cc` · ② T1 `menu:` → T7 `menu`(고민 앵커로 안 넓힘) · ③ T7 `combos[]` / `reference[]` 나눔 — 셋 다 적혀 있다.

### 5. E2E §6 · WORK-003 완료 조건 — 측정 가능한가

| 항목 | 판정 |
|---|---|
| 품질 6/6 · 목표값 · 지금 값 | 숫자로 적힘 |
| Q106 · Q108 · Q109 · Q110 맞음 | 적힘(quality-report §0-3 의 틀린 4문항과 같음) |
| 의료진 5문항 Q042 · Q075 · Q083 · Q084 · Q102 제외 | 적힘(채점 106 = 111 − 5) |
| 실버 대비 회귀 0 · 문항별 대조표 | 적힘(W-4 · W-5 가 위험 문항) |
| 실물 호출 REST 9 · MCP 9 · 같은 JSON · 샘플 흐름 · 원천 없는 값 응답 0 | 적힘 |
| 재시작 뒤 측정 | 적힘 |
| 속도 p50 · p95 · 최대 · 바이트 · 적재 시간 · 통과 기준 O-2 열림 | 적힘 |
| 결정론(리포트 두 번 바이트 같음) | 적힘 |

### 6. WORK-003 Phase

| 항목 | 판정 |
|---|---|
| 순서 0 기준점 · 입력 대조 → 1 적재 → 2 빌드 · 발행 → 3 도구 → 4 E2E | 맞음 |
| Phase 마다 완료 조건 | 0 ~ 4 전부 있음 |
| 관련 시험만 · 전체 검증은 Phase 4 끝 한 번 | Execution 첫 줄 · Phase 4-5 — 맞음 |
| 코드 레포 로컬 전용 · push 금지 | Meta · Rollback · Done — 맞음. 실물: 브랜치 `kknaksss/phub-recommend` · v1 graph 파일 미커밋(`git status` ?? 28) — SPEC §1-3 설명과 같음 |
| v1 뼈대만 재사용 | 실물에 있음: `graph_main.py`(FastAPIBuilder · lifespan · `mcp.session_manager.run()` · `app.mount`) · `modules/graph/config.py` · `container.py` · `graph-local.compose.yml`(55434 · 사용자 포트 주석) · `envs/graph.env.example` · `app/core/tx`(패키지) · `_JSON_DOCUMENT` — 맞음 |
| 키 · 실명 | Meta 「실명 · 키 넣지 않음 · 기대값은 실물 빌드에서」 — 맞음 |
| `$W` 에서 고치는 파일 = `quality-eval.py` 하나 | 맞음(SPEC §6-1 과 같음) |
| §3-2 와 Phase 2 순서 | W-3 |

### 7. SPEC-004 · WORK-002 「대체됨」

- `SPEC-004.md:33` · `WORK-002.md:42` 에 「**SPEC-005 · WORK-003 으로 대체됨(2026-10-30)**」 한 줄씩 있다. frontmatter `status` 는 그대로(draft · todo)
- 두 파일은 git 미추적(`??`)이라 다른 줄이 바뀌었는지는 git 기준선으로 대조할 수 없다. 한 줄만 더해졌다는 반증은 없다

---

## 고치는 순서(코디 제안)

1. F-1 · F-2 · F-3 · F-4 — 문장 수정(실물 칸 · 가드 식 · vocab 라벨). 결정이 필요 없다
2. F-5 — 코디 판단: mode 를 그대로 두고 menu 후보를 따로 낼지(①), §7 로 옮길지(②)
3. W-1 ~ W-9 — 같은 판에 문장 보강
4. 재검수는 F 5개만 확인하면 된다(칸 · 셈은 이번에 전수 대조함)
