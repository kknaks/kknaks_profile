# ERD v3.1 독립 검토 — 동결 여부

검토 2026-11-05 · 대상 `erd-v3.1.md`(5,050줄) · `erd-v3.1.json` · `erd-v3.1-dictionaries.json` · `erd-v3.1-tuples.json` · 기준 `ERD-FROZEN.md`(v2.4·v3 동결 조건) · `ERD-V3-CANDIDATES.md` v3.1 후보 · `erd-v3.1-brief.md` · 원장 브론즈 2판 21 · `bronze-ledger-column-report.md` · 추가 `silver-v3/decisions/batch3/DEC-2026-11-05-B3-DICT-COURSE-01.json`. 작성자 의도를 모르는 전제로 읽었다. 그 밖(이전 판 본문·검토서·step*·silver-v3/lib·check.py 본문)은 열지 않았다.

원장 대조는 원장을 직접 세어 했다: complications 이름 65 · consent 고지 109(계열 17 · 중복 문장 0) · 응급 징후 55 · 문헌 adverse_effects 32 · 타임라인 normal 162/abnormal 86/caution 93/emergency 94 · extracted safety 143 · taxonomy safety 계열 141/항목 1,713/제품 288 → 합 2,839 + 번역 96 = **2,935**, + 고지 109 = 3,044. ERD §9.6.3 과 같다.

표기: **S-#** = 구조·규칙(문장·실측으로 닫아야 동결) · **D-#** = 결정으로 처리 가능(동결을 막지 않음).

---

## ⓪ 정의 유지 · 개정 정합성

### 정의 1(시술 튜플) — 유지 ○
§0 v3.1 문장 글자 그대로. §1.1 접힘 조건·§1.4·R12 member_mode·session_count 는 칸이 아니라 속성(V3.1-5). §9.5 실측은 v3 과 같다(521 → 521 · 튜플 598 · 엣지 끝 3,423). 어긋남 없음.

### 정의 3(원장 불변·충돌 레코드·approved·안정 키·적용 순서) — 유지 ○ (캐비앳 하나)
- 원장 불변: 브론즈 2판 HASHES 21 일치(§10 D). 충돌 레코드·approved 만 읽음·적용 순서 ⓪①~⑦ 은 §5.2/§5.4 와 JSON `decision_apply_order` 가 같다(① 안 kind 순서 dictionary_add → canonical_rename → dictionary_remove → phrase_map 명시).
- 안정 키: PRD- 는 「원장에서 직접 나온 고정 id」였는데 V3.1-1 로 **결정이 바꾸는 id** 가 됐다. ERD 는 옛 id 를 alias(reclassified_from)로 두고 결정 target 규칙(§1.1 · §5.2)에 「옛 id 로 닿는다」를 적었으며 ⓪ 단계라 뒤 단계 결정은 전부 새 id 를 본다. 충돌 안정 키는 locator 쌍이라 영향 없다. → 정의 3 과 충돌하지 않는다(alias 경유가 안정 키의 조건이 된다는 점만 §0 정의 3 문장에 이미 있음).
- CND- 는 v3 문자열 유도 → v3.1 사전 정준값(+kind)·raw 는 RAW:kind|원문. 결정 target 은 사전 값 또는 locator 라 파생 id 를 가리키지 않는다. ○
- PHR- 안정 키 조건이 **불완전**하다 — S-5 로.

### 정의 2(v3.1 개정) — 개정 문장은 §0·§1.1 id_rule·§1.5 단위/접힘·§2.14 정의/식별자·R15.course·R31·§5.2(edge_create·adverse_tuple_assign·phrase_map 세 칸)·JSON `unit_rule`·`adverse_fold_rule`·`fold_condition`·`id_rule.adverse_effect`·`tuple_rules.adverse.{unit,fold_condition,course_is_edge_attribute,relative_site_is_none}` 에 일관되게 들어갔다. 실측도 세 칸(§9.6.1 부위 none=49 · 수식 none=49 · 경과는 엣지). **그러나 옛 네 칸 잔재가 규칙 문장 안에 남아 있다**:

| # | 어디 | 무엇 | 왜 문제 |
|---|---|---|---|
| S-2 | §1.5 「수식(qualifier) 규칙(v3 · V3-1)」(md 167줄) · `erd-v3.1.json` `qualifier_rule` · `tuple_rules.adverse.qualifier` | 「부작용 튜플은 (event, site, course, qualifier?)」 · 「식별자 ADV-sha256(event_id\|site_id\|**course_id**\|qualifier_id)」 · 「(색전, none, 미상, 공기)」 · 「접힘 조건은 세 칸 + 수식 칸」 · 「표현 연결은 후보 **네 칸** … exact」 — v3.1 주석이 하나도 없는 v3 원문 그대로 | 같은 §1.5 의 「단위」「식별자」 항과 §1.1 id_rule 이 세 칸·course 없음이라고 말한다. **JSON 은 빌더 입력**이라 두 식별자 공식이 공존한다 |
| S-3 | §1.5 타임라인 normal(174줄) · JSON `tuple_rules.adverse.normal_phrases` | 「닿으면 **R29** + R15」 | R29 는 삭제됐다(§3 머리 · §11) |
| S-3 | §1.2 다이어그램 92줄 | `PHRASE_DICTIONARY }o--o\| ADVERSE_EFFECT : "R29 expresses"` 선이 그대로 | 107줄 주석은 「R29 삭제」 — 다이어그램이 자기 주석과 모순 |
| S-3 | §2.14 aliases(489줄) | 「표면형은 … adverse_expression.text」 | 개체가 없다 |
| S-3 | §2.14 site_ref_id(496줄) | 「site 개체 id **또는 relative_site 사전 id** 또는 none」 · 끝에 「없으면 site=none, **course=미상**(축의 정의값)」 | 바로 윗줄 site_ref_kind(495)는 「상대 부위는 none」 · 경과는 칸이 아니다 |
| S-3 | §2.14 all_dict_values(504줄) | 「site none · **course 미상**은 축의 정의값으로 센다」 | 같다 |
| S-4 | §0 명시 예외(v3.1 개정 · 31줄) · JSON `explicit_exception_v31` | 「**(부종, none, none)** 은 하나의 단위라 **「멍 (타박상)」「멍 / 반상출혈」**「주사 부위 부종」「일시적 부종」「경미한 부종」이 전부 같은 단위에 닿는다」 | 멍 이름은 (멍, none, none) 에 닿는다(§9.6.2 #3). 사용자 정의 문장 자리의 오문 — 동결 원문이 될 텍스트라 그대로 둘 수 없다 |

그 밖(§1.5 165·166줄 「수식어가 없으면 미상」「course=미상」 뒤에 v3.1 주석이 붙은 곳 · §4.2 · R15 규칙 803줄 「경과 칸을 정하지 않는다」 · 사전 JSON `course.note`)은 v3.1 주석이 따라붙어 있어 읽을 수는 있으나 S-2·S-3 를 고칠 때 같이 정리하는 편이 맞다. §5.2 dictionary_remove 의 in_use 열거 「… event/**course**/qualifier/조건 **칸**」도 「R15.course 속성」으로. §2.15 본문이 person_condition 을 「§2.16」이라 부른다(번호 밀림).

명시 예외의 논리(부위 none·물질 none 은 값 · 경과 미상은 엣지 null)는 v2.4 와 같은 이유로 세워져 있고 정의 1 의 「미상이면 접지 않음」과 구분된다. ○

---

## ① 10건 「왜」 충족 여부

| # | 원래 요구(CANDIDATES·brief) | 반영 | 충족 | 비고 |
|---|---|---|---|---|
| V3.1-1 product_reclassify | 제품 계열 교체(PRD- 재계산 · alias · R4 이동) | §5.2 kind · ⓪ · §2.6 reclassified_from · §9.7.1 예 2(ASCEplus PRD-be57673deb → PRD-e45033395c · 충돌 없음) | ○ | 정의 3 과 충돌 없음(⓪ 참조) · 합침 규칙(같은 이름이 새 계열에 있을 때)까지 있음 |
| V3.1-2 R32 | clinical_rule → 제품·기법·시술 축 · 값은 edge_create 만 · 제품 note 문장은 출처 후보로 열거 | R32(scope·severity·source_locator·decision_id·basis·target_depth) · §9.7.2 후보 14(제품 5 · 「주사/주입 사용 금지」 4건 포함) · edge_create ref 구조체에 locator | ○ | severity 열거는 ERD 기본값 · 어느 문장이 규칙인지는 결정(§12 에 있음) — D-7 |
| V3.1-3 dictionary_remove | 동의어/값 제거 · 이력 보존 | kind · ① 끝(add·rename 뒤) · in_use 거부 · 사전 49 전부 removed_synonyms/removed_entries · 「공기색전」 이력 1 | ○ | in_use 문장의 「course 칸」만 손질(⓪) |
| V3.1-4 조건 사전 | 이소트레티노인 12 문장 흩어짐 → 조건 접기 · 금기 엣지 끝 통일 · **초기값은 완전 일치만** | 사전 person_condition 98(출처 derived 100%) · 표지어 14 · 298 → 312(사전 96 + raw 216) · 문장 471 부록 · R16/17/18 끝 = 단위 id | △(원칙의 정당한 결과) | 이소트레티노인·레티노이드 15 문장 중 사전 단위 1(「이소트레티노인 복용력」 exact) · 나머지 14 raw. 사전에 「이소트레티노인 복용」(n 7)·「레티노이드」·「임신」·「수유」가 있어도 문장에 「후 6개월 이내」「여부/중단 시점 확인 —」 같은 미등록 토큰이 있으면 원칙 A 로 raw 가 된다 — 발주서가 「완전 일치만 · 나머지 raw」라고 했으므로 **원칙의 결과이지 ERD 결함이 아니다**. 초기값이 좁은 것은 결정(dictionary_add · 동의어 = 원문 전체)으로 풀린다 — D-3. 단, 「이소트레티노인 복용」과 「이소트레티노인 복용력」이 정준값 둘로 서 있고 kind 가 식별자에 들어가 같은 조건이 condition/check 단위 둘로 갈린다(§12 에 사용자 결정으로 열려 있음) |
| V3.1-5 회·차 | R12 session_count·session_index · R9/17/18 는 qualifier_text | R12 속성 2 · §9.5.12 토큰 14 → R12 11 · qualifier_text 3 · 둘 이상이면 첫 값 | ○ | — |
| V3.1-6 stopwords 겹침 | 「관리」 겹침 규칙 명시 · 검산이 목록을 셈 | 「통째 일치 먼저 · stopword 는 남은 토큰에만」 · §9.5.13 겹침 1(관리↔modality_group) · N-6 | ○ | 부작용 축에는 같은 종류의 겹침(수식 사전 「필러」「지방」 ↔ 시술명)이 규칙 없이 남아 있다 — D-6 |
| V3.1-7 필수 고지 | 고지 → clinical_rule(disclosure) + R32 계열 · 동의서 뷰는 골드 | clinical_rule 109(중복 0) · R32(basis=ledger) 109 · 문구 사전 항목 109 · modality 속성 삭제 · column-map 이동 1 | ○ | 동의서 뷰 = R32 + R16 + emergency_signs 의 R15 로 조립 가능하나, **응급 징후 55 중 shape unresolved 42**(§9.6.11)라 R15 가 닿는 것은 일부 — 뷰의 응급 다리는 phrase_map 진행에 따라 채워진다. 고지 109 는 전부 unlinked(긴 문장)라 「고지 안 부작용 조각 연결」도 phrase_map 몫 — D-4 |
| V3.1-8 수식어 목록 | 미연결 1,150 의 원인인 수식어를 조각 아닌 parsed 로 | 단어 138(class 6 · 전부 v3 빈도 ≥4 · locator) · 패턴 5 · 토큰 6,222 전부 class 분류(분류 밖 0) · 미등록 총 5,596 → 4,189 | ○ | 조각 버림 0 — 표본 확인: PHR-8e67334ed3(지속적 경결 …) parsed.timing [지속적, 내, 소실, 지속] · misc [수, 위험이, 금기, 악화] 보존. 「지속」「지속적」이 timing 에 있다 — ③ 참조 |
| V3.1-9 정의 2 개정 | 부종이 표기 차이로 3 단위 → 하나 · 경과는 엣지 · 상대 부위 none | 65 → 49(사전 35 + raw 14) · 원장 「부종」 이름 9 중 8 이 (부종, none, none) 하나(나머지 1 은 raw 「주사 부위 반응 (부종·압통·멍·홍반)」 · 미등록 「반응」) · 멍 5 → 1 · 홍반 8 → 1 · 통증 4 → 1 · 상대 부위 보존 10 · 경과 엣지 302 | ○(이름) / △(문구) | 문구가 절대·조직층 부위로 **(부종, 눈가)·(홍반, 피부)·(자극감, 피부)·(당김감, 피부)·(비대칭, 얼굴)** 을 세워 사건별 조합이 부종 2·홍반 2·비대칭 2 가 됐다(§9.6.10). 규칙(layer·anatomical·region 은 칸)의 결정론적 결과이고 §12 가 「시술 자리와 같은 절대 부위를 none 으로 접을지는 결정」으로 열어 뒀다 — D-1. 그리고 **R15.course 귀속이 원칙 C 를 어긴다** — S-1 |
| V3.1-10 문구 사전 | 정규화형 1줄 = 변형들 + 단위 지도 + parsed + status · 표현 개체·R29 삭제 · 같은 문구 재등장 시 자동 · 부록 | 항목 1,218(자리 2,948 + 고지) · PHR- = sha256(normalized) · status auto/approved/unlinked · phrase_map(① 끝) · 개체 20 · 관계 31 · 부록 합 1,298 + 0 + 1,637 = 2,935 | ○ | 「재등장 시 자동」은 구조로 보장된다: 같은 정규화형 = 같은 PHR- = 같은 항목(raw_variants·locators 만 는다) · 「같은 정규화형인데 판정이 다른 자리 0」 · approved 는 phrase_map 레코드(target = PHR- 또는 normalized)가 ① 에서 재적용. **조건**은 정규화형이 안정할 때뿐인데 그 조건이 덜 적혀 있다 — S-5. 부록 합은 원장 자리 수와 같다(위 대조) |

---

## ② 실측 대조

- **단위 49 → 61 · 문구 1,218 · auto 185 / unlinked 1,033 · R15 1,342**: `erd-v3.1-tuples.json` 과 md 가 같다(tuples 61 = dict 47 + raw 14 · phrase_dictionary 1,218 · occurrences 3,044(bucket edge_attachment 1,298 · gate 1,746 = 1,637 + 고지 109) · edges 1,342 · course 있음 302 = 일시 287·지연 15·재발 3·영구 1).
- **「세 칸 전부 사전 값」이 아닌 단위**: 0. dict 단위 47 전부 status complete · 미등록 0 · 문구가 세운 12 전부 세 칸 사전 값(§9.6.10 · created_units 대조).
- **조각 버림**: 수식어 138 은 parsed(degree·timing·incidence·condition·connector·misc)에, 상대 부위는 relative_site_text/parsed.relative_sites 에, 붙지 않은 부위·경과·수식은 extra_* 에(raw 14: extra_sites 2 · extra_courses 3 · extra_qualifiers 1). 미등록 조각도 unregistered 에 남는다. 버려진 자리는 못 찾았다.
- **접으면 안 되는 것이 접혔는가**:
  - 「피부 괴사 (Skin Necrosis / 동상·지방괴사 …)」[M14] → (괴사, none, none) 로 접힘 — 「피부 괴사」가 괴사의 **사전 동의어**라 가장 긴 구간이 사건으로 잡혀 조직층 「피부」가 칸에 가지 않는다. 사전 내용(v3 불변)의 결과이고 ERD §5.2 가 D-6(dictionary_remove 뒤 (괴사, 피부))으로 적어 뒀다 — 결정.
  - 「안면 비대칭」[M1] → (비대칭, none, none) — 「안면 비대칭」이 동의어. 그런데 문구 「얼굴 비대칭」은 (비대칭, 얼굴:region) 을 **새로 세운다**. 같은 뜻이 사전 동의어냐 부위 칸이냐로 갈린 것 — V3.1-9 의 「표기 차이」와 같은 종류. 결정(D-1).
  - raw 14 는 전부 이름 하나씩 · 미등록 섞인 접힘 0. ○
- **S-1 · R15.course 귀속(원칙 C) — 구조·규칙**. §1.5 는 「경과는 같은 멤버 안에서 사건에 바로 붙은 수식어만 · 멤버 밖 금지」, R15.course 는 「이름·문구에서 **사건에 붙은** 경과 조각」이라고 쓴다. 그런데 R15.course 는 「문구 유래면 source_phrases 항목의 **parsed.courses** 를 가리킨다」로 정의돼 있고 parsed.courses 는 **항목 전체** 값이다. 실측이 그대로다:
  - PHR-bc0a86a830 「주사 부위 일시적 부종 **및** 멍」 → candidates 는 부종 courses [일시] · 멍 courses [] (멤버 수준은 맞다) — 그런데 엣지 (M1/톡스온 → 멍) 의 courses 가 **[일시]**(출처 문구 이 하나뿐).
  - 같은 꼴: 「일시적 홍반 및 부종」(부종 엣지 일시) · 「주사부위 일시적 부종, 발적, 압통, 멍」(홍반·통증·멍 전부 일시) · 「지연성 과민반응 (부종/발적 재발)」(부종에 지연·재발) …  auto 이고 단위 ≥2 이고 경과가 있는 문구 19 전부 후보 간 경과가 다른데 엣지는 항목 전체 값을 받는다. **문구 유래 엣지 298 중 57** 이 그 사건의 어느 출처 후보에도 없는 경과를 들고 있다. 이름 유래도 「일시적 홍반·부종」[M11/M14] 의 부종 엣지가 일시(dict_tuples 는 부종 미상)로 나온다(엣지가 (from, 단위) 로 합쳐져 이름·문구 출처가 섞이므로 이름 쪽은 10 쌍이 의심).
  - 검산 N-9 「경과 302 전부 경과 사전 값이고 문구/이름에서 온다(위반 0)」는 **문구 전체** 기준이라 이 위반을 잡지 못한다.
  - 왜 구조·규칙인가: 정의 2 개정이 경과를 「어느 시술 뒤 얼마나 가나」의 엣지 속성으로 만든 바로 그 값이 잘못 귀속되면 보톡스 부종/필러 부종의 지속 기간 구분(개정 사유)이 틀린다. 고칠 것은 R15.course 정의 문장(= `parsed.candidates[단위].courses`) · 실측 생성 · N-9 에 멤버 수준 검사 추가. 개체·관계는 안 바뀐다.
- **§9.7 조건**: 471 자리 · 298(299) → 312 · 사전 96 + raw 216 · 문장 부록 471 · 문장이 세운 단위 0 — tuples.json summary 와 같다. 이소트레티노인 15 문장 표(§9.7.0)는 원장 9 키 그대로(중복 문장 포함).
- **§9.8 고지**: 109/17 · auto 0 · unlinked 109 · R15 disclosure 유래 0 — 원장과 같다. 후보 표 #11 「필러 주입 후 결절 …」이 (결절, none, **필러**) 후보를 낸다 — 「필러」가 시술명인데 수식(물질) 사전 값이라 같은 멤버에서 붙었다. unlinked 라 단위는 안 생겼고 현재 auto 단위의 qualifier 는 역행성·혈전 둘뿐(영향 0) — D-6.

---

## ③ 경과 값 「지속」 판단

**있어야 한다.** 근거:
1. 원장: 타임라인·응급 징후에 「지속」이 경과로 쓰인 문구가 20 이상(「지속 홍반 (3일 이상)」「지속적 홍반 (예상보다 진함)」「지속적 감각 둔화」「안면 비대칭 지속」「눈꺼풀 처짐 지속」「잔여 경결」 …). 일시/영구 사이의 임상 구분이고 DICT-COURSE-01 의 locator 4 곳(지속적 경결 · 잔여 경결 · 경결감 지속 · 점진적으로 커지는 경결/결절)이 그 중 일부다.
2. v3.1 은 「지속」「지속적」을 **시간 수식어(timing)** 로 둔다. 수식어는 정규화형에서 **제거**되므로 「안면 비대칭 지속」과 「안면 비대칭」이 **한 항목**(PHR-cd094680a7)으로, 「심한 부종 지속」과 「부종」이 한 항목(PHR-bb03f40e8a)으로 합쳐지고 엣지 경과는 null 이 된다 — 경과 정보가 항목 병합에서 사라진다. 경과가 엣지 속성이 된 지금 이것은 손실이다.
3. 길은 ERD-FROZEN 대로 **결정**이다: DICT-COURSE-01(dictionary_add · course · 승인됨 · 적용 ①)이 이미 있고, §1.5 규칙 「경과 사전에 완전 일치하는 말은 경과로 먼저 잡힌다(사전 순서가 먼저)」가 있어 빌드 ① 뒤 「지속」「지속적」「잔여」「점진적으로 커지는」은 수식어가 아니라 경과로 읽힌다. **ERD 사전에 넣을 일은 아니다**(사전 값은 결정 · v3 47 사전 값 불변 유지). 
4. 다만 ERD 문장이 낡았다 — S-5: §1.5·§12 가 「지속은 경과 값이 아니다 · 추가는 결정(미정)」이라 쓰는데 결정은 승인돼 있다. 그리고 경과 사전이 바뀌면 정규화형(= PHR- id)이 바뀐다(「안면 비대칭 지속」이 별 항목으로 갈린다) — §1.1 은 「수식어 목록이 바뀌면」만 적어 안정 키 조건이 빠져 있다. 지금은 approved phrase_map 이 없어 이관 문제는 없지만 조건 문장은 동결 전에 있어야 한다.
5. 결정 쪽 메모(ERD 아님): 「경결감」은 경결의 동의어가 아니라 DICT-COURSE-01 의 세 번째 locator 「경결감 지속 (정상)」은 결정 적용 뒤에도 unlinked 다(dictionary_add 필요) · 경과 사전의 「미상」 값은 이제 뜻이 없다(엣지 null) — dictionary_remove 후보 · 수식어 목록의 「지속」「지속적」은 규칙 데이터에서 빼는 편이 순서 의존을 없앤다(규칙 데이터 개정 · 사전 우선 규칙이 있으니 동결 조건은 아님) · 결정 레코드 locator 형식(`@5/3/0`)이 ERD locator(`@M16/12`)와 다르다.

---

## ④ 행선지 표본 · 추정 매칭 · 열거기 형식

- **행선지 표본 20(새 seed)**: `erd-v3.1.md`·`erd-v3.1-column-map.md`·`erd-v3.1.json` 어디에도 「표본」「seed」가 없다(grep 0 · §10 A 에도 표본 항목 없음). v2.4 동결 때의 「표본 대조 4회」에 해당하는 것이 v3.1 산출물에는 **없다** — 확인 불가. 행선지 자체는 §10 A 가 1,072/1,072 · 이동 29(고지 1 + 표현 28) · 미정 0 으로 닫혀 있고 column-map 머리와 JSON `column_map_moves_v3_1` 29 가 같다.
- **추정 매칭 지점**: 0. §1.1 「유사도·추측 매칭은 ⑦ 후보로만」 · 조건 축 「유사도 True 금지 · 조사 분리 False」 · 문구 auto 는 조각 전부 사전 값일 때만 · tuples.json `rules`/`no_similarity` 플래그. 「이소트레티노인 복용 중 …」류가 raw 로 남은 것이 그 증거다.
- **적합성 열거기 형식(JSON 구조만)**: `decision_kinds[]` 20 (항목 = kind · build_reads · target · new_value · note · new_in_v3_1 …) 에 product_reclassify·dictionary_remove·phrase_map 이 같은 모양으로 · `relations[]` 31 (id · name · from · to · card · attrs[]{name,type,note} · sources · note) 에 R32 가 같은 모양으로, R29 없음 · `enums['decision.kind']` 20 · `decision_apply_order` 단계 ⓪①~⑦ 에 새 kind 포함 · `adverse_expression.*` 열거 키는 열거기 정적 목록 호환용으로만 남겼다고 §3.1 이 밝힌다(§12 「열거기 개정 몫」). v3 과 같은 형식이라 열거기가 읽는다는 §10 N-13 주장과 구조가 맞는다.

---

## ⑤ 동결 판단

**동결 가 — 단, 아래 S-1~S-5 를 문장·실측 수정으로 닫은 뒤**(v3 동결 때 R-1~R-4 와 같은 방식 · 개체·관계·결정 kind 는 바꾸지 않는다). 근거: 정의 1·3 유지, 정의 2 개정이 구조(개체 20 · 관계 31 · id_rule · 사전 49 · kind 20)에 일관되게 들어갔고, 10건이 각자의 「왜」를 충족하거나 결정으로 풀린다. 어긋남은 **구조·규칙 5(전부 문장·실측 수정)** · **결정 7**.

### 동결 전 꼭 고칠 것 (S · 구조·규칙 — 문장·실측)
| # | 고칠 것 | 어디 |
|---|---|---|
| S-1 | R15.course 는 항목 전체 `parsed.courses` 가 아니라 **그 단위의 후보 `parsed.candidates[].courses`**(이름은 그 사건 멤버의 dict_tuples 경과)에서 온다고 쓰고, 실측 재실행 · N-9 에 「엣지 경과 ∈ 그 사건 후보의 경과」 멤버 수준 검사 추가(지금 문구 엣지 57/298 위반) | R15 course 행 · §1.5 문구 사전 auto 문장 · `erd-v3.1-tuples.py`/json · §9.6.4/§9.6.10 수치 · check N-9 |
| S-2 | §1.5 수식 규칙과 JSON `qualifier_rule`·`tuple_rules.adverse.qualifier` 를 세 칸으로(네 칸 · course_id · (색전, none, 미상, 공기) · 「네 칸 exact」 삭제) | md 167줄 · erd-v3.1.json |
| S-3 | 삭제된 R29·adverse_expression·경과 칸 잔재: 다이어그램 92줄 R29 선 · §1.5 174줄 「R29 + R15」 · §2.14 489/496/504줄 · JSON `normal_phrases` · dictionary_remove in_use 「course 칸」 · §2.15 「§2.16」 | md · json |
| S-4 | §0 명시 예외(v3.1) 예문 — (부종, none, none) 에 멍 이름을 넣은 오문 수정(멍은 (멍, none, none)) | md 31줄 · JSON `explicit_exception_v31` |
| S-5 | PHR- 안정 키 조건에 「경과 사전(및 분해 사전) 값이 바뀌면 정규화형이 바뀔 수 있다」 추가 · §1.5/§12 의 「지속 결정 미정」을 「DICT-COURSE-01 approved · ① 적용 · 그 뒤 지속·지속적·잔여·점진적으로 커지는 은 경과」로 갱신 | §1.1 · §1.5 수식어 목록 · §12 |

### 동결 후 결정으로 (D)
| # | 무엇 | kind |
|---|---|---|
| D-1 | 부위 kind 기계 적용이 세운 (부종, 눈가)·(홍반, 피부)·(자극감, 피부)·(당김감, 피부)·(비대칭, 얼굴) 을 none 단위로 접을지 · 「안면 비대칭」(동의어) ↔ 「얼굴 비대칭」(부위) 불일치 | phrase_map · adverse_tuple_assign · dictionary_add/remove |
| D-2 | 「피부 괴사」 동의어 → (괴사, 피부)(ERD D-6 그대로) | dictionary_remove |
| D-3 | 이소트레티노인·레티노이드 raw 14 → 사전 단위(동의어 = 원문 전체/조각) · 「이소트레티노인 복용」/「복용력」 병합 · kind 를 식별자에서 뺄지 | dictionary_add(person_condition) · scope_review |
| D-4 | 고지 109 · 응급 징후 42 의 단위 연결 — 동의서 뷰의 응급 다리가 이것에 달려 있다. 응급 징후를 고지처럼 clinical_rule(kind) + R32(ledger) 로도 둘지는 다음 판 후보 | phrase_map · scope_review |
| D-5 | 「지속」 적용 뒤 남는 것: 「경결감」 동의어 · course 「미상」 값 제거 · 수식어 목록에서 지속/지속적 제거 | dictionary_add · dictionary_remove · 규칙 데이터 |
| D-6 | 수식 사전 「필러」「지방」 ↔ 시술명 겹침(§9.8 #11 (결절, none, 필러) 후보 · 현재 auto 영향 0) — V3.1-6 과 같은 겹침 규칙을 부작용 축에 둘지 | scope_review(다음 판) |
| D-7 | R32 제품 note 후보 14 중 규칙 판정 · severity 확인(ERD §12 그대로) | edge_create |

보류 메모(결정 아님): 행선지 표본 20 은 v3.1 산출물에 없어 대조하지 못했다 — 동결 기록(ERD-FROZEN v3.1 절)에 표본 대조를 남길지는 코디 판단.
