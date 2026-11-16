# ERD v2.2 독립 검토

검토 2026-11-04 · 대상 `erd-v2.2.md`(2,537줄) · `erd-v2.2.json` · `erd-v2.2-dictionaries.json` · `erd-v2.2-tuples.json` · 행선지 대조에 `erd-v2.2-column-map.md` · 원장 21 (`phub-stg-2026-10-26/`). 이전 검토서 `erd-v2.1-review.md` 는 ⓪ 대조에만 썼다. 작성 과정 문서(v1·v2·v2.1 본문·발주서·step*·silver-*·DATA-001·_archive)는 열지 않았다.
판단 기준은 사용자가 정한 정의 셋뿐이다. 완성도·사전 크기·미상 비율·미해결 수는 근거로 쓰지 않았다.

| 정의 | 구현 위치 | 어긋남 |
|---|---|---|
| 1 시술 = 무엇 × 어디 × 어떻게 | §1.1 L26~27 · §1.4 · §2.4 · §2.5 · R26~R28 | **4** (구조 2 · 결정 2) |
| 2 부작용 = 사건 × 부위 × 경과 | §1.5 · §2.14 · §2.15 · R15 · R29~R31 · §4 | **4** (구조 2 · 결정 2) + 확인 1 |
| 3 원장 불변 · 충돌 목록 · 결정 레코드 · 출처 | §1 · §2.20 · §2.21 · §5 · §5.2 · §5.3 · R23~R25 · R29 · R30 | **3** (구조 3) |

어긋남은 모두 11건이다. **구조** 7건(동결 전 고칠 것)과 **결정** 4건(동결 후 결정 레코드로)으로 나뉜다.

---

## ⓪ 이전 검토 ⑤ 「동결 전 꼭 고칠 것」 6건의 반영 여부

| # | 이전 지적 | v2.2 에서 고친 자리 | 판정 |
|---|---|---|---|
| 1 | 미상을 식별자 값으로 씀 (1-A) | §1.1 L26 식별자 · L27 접힘 조건 「세 칸 전부 사전 값일 때만」 · §1.4 what 규칙 1 · §2.5 식별자와 속성 `anchor`·`all_dict_values` · §5 L1049 · json `fold_condition`·`id_rule.procedure`. 실측을 보면 v2.1 에서 접혔던 분류 항목 3건과, 미상 칸이 있는데도 라벨이 합쳐졌던 튜플 18개가 전부 갈라졌다(§9.5.2 표, tuples.json `v21_none_fold_split`). 「세 칸 전부 사전 값」인 튜플은 0개이고, anchor 가 둘 이상 섞인 튜플도 0개다(§9.5.5). | **고침** |
| 2 | 세 칸 밖으로 조각을 버리고 접음 (1-B·1-C) | §1.4 what 규칙 7·8(v2.1 규칙 8 삭제) · site/technique 둘 이상이면 분류 항목은 ambiguous, 참조는 ⑨ · 조합 규칙 `combo_outside_fragment` · extra_* 에 실제 값. 예로 든 「IPL 제모」「사각턱 (수입)」「필러 볼/턱」「보톡스(턱선/광대)」는 모두 미해결로 갔다(검산 J-2). 클라리티2 (혈관)·피코슈어 프락셀은 ambiguous 로 바뀌었다. | **고침** (남은 것은 1-D: `+` 뒤의 빈 멤버를 버림 — 결정으로 처리) |
| 3 | 기법 상속 (1-D·3-D) | §1.4 technique 규칙 · §2.5 technique_id/technique_origin(enum 에서 inherited 삭제) · json `technique_inheritance:false`. 상속 후보는 §9.5.6 에 canonical_mapping 후보로 내렸다. | **규칙은 고침 · 문구 잔재 2** — §2.7 L301 정의(json `entities.technique.definition` 도 같음)가 아직 「R5 의 계열 기법을 상속하되…」라고 적고 있고, §2.5 L247 `technique_id` 의 출처가 아직 `procedure-profiles.json:profiles[].mechanism[]`(상속의 원천)이다 → 아래 1-B |
| 4 | 규칙 ④ 자동 확정 (3-A · 사용자 결정으로 「유지 + 충돌 레코드 + 뒤집는 kind」) | §5 ④ L1040·L1051 · §2.20 정의(L518) · `status` 에 auto_resolved_by_trust(L532) · `rule_ref`·`chosen_value` · `values[].trust_tier` 필수 · 뒤집기는 decision `conflict_override`(target.conflict_id → new_value.chosen_value, approved 만) · §9.3 rule_ref 열과 「④ 는 빌드가 레코드마다 남긴다」 문단. 사용자가 정한 세 요소가 모두 들어 있다. | **고침(사용자 결정 형태대로)** |
| 5 | decision 이 빌드가 읽을 수 없는 모양 (3-B) | §2.21 · §5.2 표: 공통 필드 9개, target·new_value 는 kind 별 구조체, kind 7개 신설·재정의(dictionary_add · tuple_assign · fold_approve · event_split · canonical_mapping · conflict_override · exclude), build_reads, 빌드는 approved 만 읽음, 기존 22건 이관. | **대부분 고침 · 수용 못 하는 종류가 남음** → 아래 3-A·3-B |
| 6 | course 출처가 세 군데에서 다름 (2-A) | §1.5 L115 · §2.14 course 행 · §4 L82/L134 를 같은 문장으로 맞췄다(json `course_rule` 도 같음). duration·incidence 는 R15 엣지 속성으로만 쓴다(R15 끝 문장). 경과 사전 동의어 2개를 뺐다. | **고침** (다만 같은 §1.5 L114 의 「상속」 규칙이 경과 값을 추정해서 채운다 → 2-A) |

같이 고친 것: 이전 3-E 에서 사용자가 아직 승인하지 않은 결정이 `who: 사용자` 로 적재돼 있던 문제는, DEC-20·21·22·23 을 `proposed` 에 decided_by·decided_at null 로 둬서 고쳤다(§5.3).

---

## ① 정의별 구현 위치와 어긋남

### 정의 1 — 시술 = 무엇(계열|제품) × 어디(부위) × 어떻게(기법). 같은 세 칸이면 같은 시술. 다르거나 하나라도 미상이면 기계가 접지 않는다.

**구현.** `procedure` 는 튜플 (what, site, technique)이다. 식별자는 세 칸이 전부 사전 값일 때만 `sha256(what|site|technique)` 이고, 아니면 anchor(CAT-/REF-/#m<i>)가 섞여 항목·참조마다 고유해진다(§1.1 L26, §2.5). 이것으로 정의 1 의 두 문장 「같은 세 칸 = 같은 시술」과 「미상이면 안 접는다」가 식별자 수준에서 그대로 구현된다. 조각을 버리고 조립하는 경로는 막혀 있다(what 규칙 7·8, site·technique 의 multi_* 처리). 미등록 조각이 있는 이름은 항목 자신이 what 이다(규칙 9). 「무엇」을 정하지 못한 항목은 catalog_item 자신이 자리를 지키고, 이 경우 anchor 가 있어 접히지 않는다. 이것은 「미상 what」의 자리표시로 정의와 충돌하지 않는다.

**어긋남.**

| # | 어디 | 무엇이 어긋나나 | 분류 |
|---|---|---|---|
| 1-A | §3 머리 L555 「참조 끝점은 §1.3 규칙으로 정해지고 … 승격 규칙: 분류 항목에 닿으면 … complete 이면 procedure 로 승격」 · R9 L605/612 · R12 L633/650 · R15 L677/700 · R16 · R17 · R18 의 `target_depth enum(modality\|subcategory\|catalog_item\|procedure\|product)` | §1.4 는 참조 자리 ②③ 를 **procedure 튜플로 만든다**(§9.5.4: ② 157 튜플 · ③ 16 · 예 synergy `보톡스`@M1 → PRC-c8e0f36ef6). 그런데 엣지 규칙은 v2 그대로라 통째로 일치하는 참조의 끝을 **그 깊이의 노드(PRD-보톡스·MOD-필러 …)** 에 둔다. procedure 로 승격되는 길은 「분류 항목 경유 + complete」 하나뿐이다. 그래서 같은 참조 하나에 PRC 튜플과 PRD/MOD 끝이라는 두 표현이 생기고, 그 튜플을 가리키는 엣지는 없다. 결과적으로 시너지·순서·금기(R18)와 원인 시술(R15)이 「시술 단위」가 아닌 계열·제품 노드에 붙는다. 또 complications·consent·pih 의 M 코드 끝(R15 `complications.json:categories[].id` 등)은 튜플 입력에서 아예 빠져 있다(§1.4 입력 「pih id … 제외」). | **구조** (정의 2 와 함께) |
| 1-B | §2.7 L301 정의(json `entities[technique].definition` 동일) · §2.5 L247 `technique_id` 의 출처 원장 키 | 정의 문장에 「이름 조각이 닿지 않으면 R5 의 계열 기법을 상속하되…」가 남아 §1.4·§2.5 규칙과 정면으로 어긋난다. `technique_id` 의 출처가 `procedure-profiles.json:profiles[].mechanism[]` 로 적혀 있어, 이 json 을 읽는 빌더는 상속의 원천을 그 값의 출처로 달게 된다. 이제 기법은 이름 조각에서만 나오므로 출처는 what_id 와 같은 이름 키 목록이어야 한다(site_id 도 지금은 「파생」뿐이다). | **구조** (문구·출처 정정) |
| 1-C | §1.4 what 규칙 6 · §9.5.4 | 「보톡스」라는 문자열은 PRD-보톡스로, 코드 `M1` 은 MOD-보톡스로 간다. 같은 「무엇」이 두 what_id 를 받는다(tuples.json PRC-c8e0f36ef6 / PRC-82c1b73aa9). 지금은 미상 칸 때문에 어차피 접히지 않으므로 기계가 잘못 접는 일은 없다. | 결정 (§12 1-E · canonical_mapping) |
| 1-D | §1.4 조합 규칙 `+` | 분류 항목 `엑셀V+`[M8] 가 what=product:엑셀V(complete, PRC-d6bc69c63b)로 조립됐다. `+` 를 조합 기호로 보고 빈 멤버를 버린 결과다. 다른 기기인데 「무엇」 칸에 틀린 값이 들어갔다. anchor 가 있어 접히지는 않는다. 모양이 같은 `젠틀맥스프로+` 는 unusable_primary(ambiguous)로 갔다. | 결정 (§12 1-F · tuple_assign) |

### 정의 2 — 부작용 = 사건 × 부위 × 경과. 원인 시술은 엣지(R15)로, 등급·빈도·시기·대처는 엣지 속성으로. 문헌 문장·타임라인 문구·응급 징후는 원문 표현.

**구현.** `adverse_effect` 는 튜플 (event, site_ref, course)이고 식별자는 `sha256(event|site|course)` 다(§2.14). 원인 시술은 튜플에 들어가지 않고 R15 may_cause 로만 이어진다. 등급·빈도·발생 시기·지속·대처·예방·위험 요인·예상/이상/주의/응급 표시는 전부 R15 엣지 속성이고(L679~697), duration·incidence 가 경과를 정하지 않는다는 문장도 들어갔다(L700). 원문 문장·타임라인 문구·응급 징후·환자 설명은 `adverse_expression`(§2.15)이며 R29 로 튜플을 가리킨다. 인과는 R30 이다. 큰 틀은 정의 2 와 맞는다.

**어긋남.**

| # | 어디 | 무엇이 어긋나나 | 분류 |
|---|---|---|---|
| 2-A | §1.5 L114 「site·course 는 멤버 → 같은 묶음 → outer 묶음 → (이름 전체에 그 축의 값이 하나뿐이면 그 값) 순으로 상속」 | 경과·부위를 **그 사건이 놓인 멤버 밖에서 추정해 채운다**. 시술 축에서 끈 기법 상속과 같은 성격이다. 실제로 틀린 사례가 있다. 원장 M14 `통증·불편감 및 지연성 통증 (Procedural Pain & Late-Onset Pain, LOP)` 는 onset 이 「시술 중~직후; 지연성 통증은 3-4일 후」로 두 통증을 구분해 적었다. 그런데 이 이름은 튜플이 **통증 × none × 지연 하나뿐**이다(tuples.json complications). 시술 중 통증의 경과(미상, 즉시)가 지연으로 덮였다. 「경결·딱딱함(일시적 섬유화)」 → 경결 × 일시도 괄호 안 수식어를 바깥 사건에 붙인 같은 경로다. | **구조** |
| 2-B | §1.5 튜플 규칙(미등록 조각이 있어도 튜플을 만들고 접는다) · §9.6.6 12튜플 · §12 2-C 를 scope_review 로 미룸 | 아래 ②에서 판단한다. 요지: 미등록 조각은 **어느 축인지 모르는 조각**이다. 그것을 버린 뒤 세 칸이 같다고 접으면 「같은 단위」라는 주장을 근거 없이 하게 된다. 12건 중 최소 3건은 실제로 부위나 사건을 잃었다(`주사 통증` 의 「주사」 = 주사 부위, `카테터 관련 감염` 의 「카테터」, `구형구축 (… 섬유성 결절)` 의 사건). | **구조** |
| 2-C | §4 L81 · 사건 사전 동의어(과민반응→아나필락시스 · 동상·지방괴사→괴사 · 섬유화→경결 · 공기색전→색전) | 이전 2-B 와 같고 v2.2 에서 바뀌지 않았다. 이것은 사전 값이 정하는 문제다. | 결정 (§12 2-B · event_split) |
| 2-D | §5 L1049 | 부작용 쪽 site none·course 미상은 지금도 식별자 값이다. 정의 2 는 「미상이면 접지 말라」를 명시하지 않았고, 조각이 전부 사전에 닿은 이름(예: 멍 5건)은 원장이 부위를 말하지 않은 것뿐이다. | 결정 (§12 2-D · scope_review) |
| 확인 | R15 `from: proc_axis\|site` (L673, 다이어그램 L56) | 부위가 원인인 끝은 출처 키가 하나도 없다(sources 에 부위 원천 없음). 정의 2 는 원인을 「시술」로 정했다. 실제로 쓸 출처가 없다면 끝에서 빼는 편이 정의와 맞는다. 이전 검토 때도 정의되지 않은 끝이었다. | 확인 |

### 정의 3 — 원장은 안 고친다. 충돌은 기계가 목록으로(④ 자동 해결도 레코드로). 판정은 결정 레코드. 빌드는 승인된 결정만 적용. 모든 실버 값은 원장 파일·키 경로 출처.

**구현.** 브론즈 바이트를 보존한다(§1, 검산 D 22파일 sha256 일치). 실버 값은 전부 (파일, 잎 키 경로) 출처를 갖는다(§1 L15, R25). 충돌은 ④⑥⑦⑧⑨ 를 전부 conflict 로 만들고, ④ 도 auto_resolved_by_trust 레코드로 남긴다. 결정은 kind 별 구조체이고 빌드는 approved 만 읽는다. 원장 메모는 `원장 작성자` 결정으로 적재한다(§5.3 끝). 틀은 정의 3 대로다.

**어긋남.**

| # | 어디 | 무엇이 어긋나나 | 분류 |
|---|---|---|---|
| 3-A | §5.2 kind 표 L1088~1100 · §2.20 status L532 · R30 L853 | **사람의 판정 중 결정 레코드로 적을 수 없는 종류가 남아 있다**(자세한 내용은 ③). (1) R30 leads_to 는 「결정 개체로만 값이 생긴다」고 적었는데, 엣지를 만드는 kind 가 없다. (2) `tuple_assign` 의 new_value 는 세 칸 하나뿐이다. 그래서 v2.2 가 직접 만든 multi_site·multi_primary 미해결(「보톡스 이마/미간」「필러 볼/턱」 = 시술 둘)을 튜플 둘이나 combo 로 지정하지 못한다. 대상도 CAT/REF 뿐이라 부작용 쪽(complications 이름·AEX → (event, site, course)[])은 지정할 수 없다. (3) conflict.status `dismissed` 로 바꾸는 kind 가 없다. 「⑦ 후보는 같지 않다」「⑨ 는 범위 밖」 같은 판정을 적을 곳이 없어서, 「단계 끝 = open 0」(L1049)에 구조적으로 닿을 수 없다. | **구조** |
| 3-B | §5.2 `fold_approve`(target.procedure_ids) · `exclude`(target.id 아무 id) · `conflict_override`(target.conflict_id, CFL = 대상 id + 속성 + 출처 해시, json `id_rule.conflict_decision_ids`) | 결정의 대상이 **다른 결정을 적용하면 바뀌는 파생 id**(PRC-/ADV-/CFL-)다. dictionary_add·tuple_assign·canonical_mapping 이 적용되면 what_id 나 anchor 가 바뀌고 PRC id 도 바뀐다(식별자에 what_id 가 들어감). 그러면 앞서 승인된 fold_approve·exclude·conflict_override 가 허공을 가리킨다. 결정 사이의 **적용 순서도 정의돼 있지 않다**(문서 어디에도 없음). 「빌드가 승인된 결정만 읽어 적용」의 결과가 결정 순서와 사전 상태에 따라 달라진다. | **구조** |
| 3-C | R29 출처 L843 (json R29.sources) | `adverse_expression.text`·`adverse_effect.origins` 에 있는 **taxonomy.json safety 잎 키 11개**(modality 3 · items 5 · products 3)가 R29 출처에 없다. 그런데 R29 연결 1,797건 중 1,405건이 taxonomy 표현이다(§9.6.3: 81 + 1,114 + 210). ERD 가 선언한 엣지 출처가 실제 값의 대부분을 덮지 못한다. | **구조** (출처 정정) |

참고 1(어긋남으로 세지 않음): tuples.json 의 procedure `sources` 는 지금도 (origin, label, family, anchor)뿐이고 파일·잎 키 경로가 없다(adverse 쪽에는 file/path/record 가 있다). R25 가 「실버 빌더 생성」이라 ERD 위반은 아니다.
참고 2: ④ 의 골드 반영(chosen_value)은 사용자 결정 그대로다.

---

## ② 접힘 표 검토 (§9.5 · §9.6 · tuples.json)

### 시술 — 접으면 안 됐던 것

**없다.** 세 칸 전부 사전 값인 튜플이 0개이므로 서로 다른 항목·참조가 한 튜플에 들어간 경우가 0이다(검산 J-1, tuples.json `multi_anchor` 0). 한 튜플에 두 원천이 함께 있는 경우는 규칙 ①(정규화 완전 일치) 하나뿐이다. 참조가 분류 항목 이름과 똑같으면 그 항목의 anchor 를 쓰고(`스컬트라`·`PRP`·`IPL`), 라벨과 힌트가 같은 참조끼리는 같은 REF 를 쓴다. 이것은 「같은 문자열 = 같은 것」이지 미상인 채로 접은 것이 아니다.
한 가지 비대칭이 있다. `바이오스티뮬레이터(스컬트라/엘란쎄)` 의 멤버는 분류 항목 스컬트라·엘란쎄의 anchor(…bf5d, …62fe)를 공유한다. 반면 `바이오스티뮬레이터(쥬베룩)` 는 자기 anchor(…46b1)를 받아 분류 항목 쥬베룩(…dd15)과 갈린다. 두 규칙 모두 문자 그대로는 맞다(멤버 문자열 일치 / 계열명 조각이 붙은 라벨). 다만 같은 문맥에서 결과가 갈린다. 정의를 어기지는 않으므로 결정에서 같이 보면 된다.

### 시술 — 같은 세 칸인데 안 접힌 것

**없다.** 세 칸이 모두 사전 값인 튜플이 없으니(기법 조각이 닿은 튜플 0/594), 정의상 「같은 세 칸」인 쌍이 존재하지 않는다. 같은 라벨인데 힌트가 달라 갈린 경우(`보톡스`@M1 …9a0f / `보톡스` 무힌트 …2360, `필러`@M2 / `필러`)는 미상 칸이 있어 안 접는 것이 맞다. 그 결과 「같은 세 칸이면 같은 시술」은 지금 결정(canonical_mapping·tuple_assign·dictionary_add)을 거쳐야만 생긴다. 사전 크기의 문제이고 구조 문제는 아니다.

### 부작용 — 12튜플(미등록 조각이 있는 이름이 접힘) 판단

**판단: 구조 문제다.** 근거는 정의 2 하나다. 부작용의 단위는 사건 × 부위 × 경과다. 미등록 조각은 분해기가 **어느 축인지 모르는** 조각이다. 그것을 버리고 「세 칸이 같다」며 접으면, 버린 조각이 부위·경과·사건이 아니었다는 보장 없이 같은 단위라고 주장하는 셈이다. 실제로 그랬다.

| §9.6.6 # | 접힌 이름 | 버린 조각의 실제 축 | 결과 |
|---|---|---|---|
| 2 | `주사 통증 / 불편감 (Injection Pain…)` [M2] | 「주사」 = 주사 부위(원장 mechanism 「모든 주입 부위 공통」) | 통증 × **none** 으로 가서 M7·M9·M16 의 일반 통증과 접힘. 같은 뜻인 `주사 부위 통증` [M1] 은 통증 × 주사 부위로 따로 감 → 접으면 안 될 것을 접었고, 접어야 할 것은 갈랐다 |
| 1 · 12 | `공기색전·카테터 관련 감염` [M16] | 「카테터」 = 부위·경로(원장 mechanism 「카테터 관련 혈류감염」) | 감염 × none (필러·실 감염과 접힘), 색전 × none (필러 동맥 색전과 접힘) |
| 8 | `구형구축 (Capsular Contracture-like Reaction / 섬유성 결절)` [M7] | 괄호 안이 사건 설명 | 결절 × none 에서 M3 `결절 (Nodule)` 과 접힘 |
| 3·4·5·6·9·10·11 | `기저 위험` · `시술 직후` · `시술 후` · `반응` · `포함` | 시기·설명 — R15 속성 또는 무의미 | 접혀도 정의 2 위반 아님 |
| 7 | `(표재 감각신경, 가역적)` [M16] | 「표재 감각신경」 = 해부 구조(부위 후보) | 감각 이상 × none × 일시로 접힘 — 부위를 잃었을 가능성 |

일부(설명·시기 조각)는 무해하다. 그러나 무해한지 아닌지는 사람이 조각을 보고 나서야 안다. 기계 규칙이 접힘을 허용하는 것 자체가 정의 2 와 맞지 않는다. 그래서 2-B 는 결정이 아니라 접힘 조건의 문제다. 정의 1 에서 「미등록이면 항목 자신(anchor)」으로 고친 것과 같은 자리다. 반대로 2-D(조각이 전부 사전에 닿았고 원장이 부위를 말하지 않은 경우)는 버린 정보가 없으므로 결정 사항으로 둔다.

### 부작용 — 그 밖의 접힘

- 9.6.2 #19 · R29 「지연성 과민반응」→아나필락시스, 「교근 섬유화」→경결: 사전 동의어 때문에 생겼고, v2.1 과 같다(2-C · 결정).
- 9.6.2 #40 · LOP: 이름 하나 안에서 두 통증이 한 튜플(통증 × 지연)로 합쳐졌다. 경로가 접힘이 아니라 상속이라 2-A 로 셌다.
- 같은 세 칸인데 안 접힌 것: `주사 통증 / 불편감` [M2] ↔ `주사 부위 통증` [M1] (위 표). 원인은 「주사」가 미등록인 것이므로 2-B 를 고치면 접히지 않은 채로 남는다. 같게 볼지는 dictionary_add(주사 → 주사 부위)로 정할 결정이다.

---

## ③ 결정 개체 수용성 — §9·§12 에 미룬 결정을 담을 수 있나

| 미룬 결정 | 갈 kind | 담기나 |
|---|---|---|
| §9.5.6 기법 상속 후보 9계열 | canonical_mapping (from_ref R5:Mx, scope, to_id) | 담김. 다만 `scope: str` 은 자유 문자열이다. §9.5.6 은 「아래 항목 목록이 그 scope」라고 했으니 id 목록(CAT-/REF-[])이어야 빌드가 읽을 수 있다 |
| 1-E 보톡스 PRD↔MOD | canonical_mapping | 담김 |
| 1-F 엑셀V+ | tuple_assign (CAT- → what) | 담김 |
| 1-G 볼뉴머 M4/M9 | fold_approve | 모양은 담기지만 target 이 PRC id 라 불안정하다(3-B). 「같지 않다」로 판정하면 담을 kind 가 없다(3-A-3) |
| §9.5.3 엠페이스/엠페이스(EMFACE) 류 | dictionary_add → fold_approve / tuple_assign | 담김(fold_approve 는 3-B 와 같은 문제) |
| §9.5.3 ambiguous 3 | tuple_assign | 담김 |
| §9.5.4 multi_site·multi_primary 미해결 (보톡스 이마/미간, 필러 볼/턱, 이마 주름 (수입) …) | tuple_assign | **못 담는다** — new_value 가 세 칸 하나뿐이라 「시술 둘(combo)」 또는 「튜플 + 수식(수입/국산)」을 적을 수 없다 |
| §12 2-B 사건 동의어 분리 | event_split | 담김 |
| §12 2-C · 2-B(위 ②) 개별 이름 재지정(구형구축 → 구형구축만, 카테터 감염 → 감염 × 카테터) | — | **못 담는다** — tuple_assign 은 시술 전용(CAT/REF)이다. 부작용 원천(complications 레코드·AEX)을 대상으로 (event, site, course)[] 를 지정하는 kind 가 없다 |
| R30 leads_to (인과) | — | **못 담는다** — 「결정 개체로만 값이 생긴다」(L853)고 했지만 엣지를 만드는 kind 가 없다 |
| ⑦ duplicate_candidate 「같지 않음」 · ⑨ 「범위 밖」 | — | **못 담는다** — conflict.status dismissed 로 가는 길이 없다(exclude 는 개체를 지우는 것이지 충돌을 닫는 것이 아니다) |
| 비사건 사전의 잘못된 동의어 제거(예: 경과 `가역적`→일시, 부위 동의어) | — | 못 담는다(event_split 은 사건 사전 전용, exclude 는 값 단위). 지금 미룬 목록에는 없으므로 참고로만 둔다 |
| §12-3 step1 제품 확장 395 | dictionary_add 묶음 | 담김(product id 의 계열 코드는 category 칸으로 대신 — 필드 이름만 정하면 된다) |
| 2-D · 부작용 접힘 원칙 | scope_review | 담김(ERD 개정 기록) |
| DEC-20~23 승인 | 같은 레코드 status → approved | 담김 |

**빠진 kind 의 최소 집합:** `edge_assert`(R30 등 결정으로만 생기는 엣지) · tuple_assign 확장(new_value 를 튜플 목록 또는 combo 로 받고, target 에 부작용 원천 complications 레코드·AEX 추가) · `conflict_dismiss`(→ status dismissed). 그리고 3-B 대로 모든 build_reads kind 의 target 을 원장에서 나온 고정 id(CAT-/REF-/AEX-/complications 레코드·사전 DIC-)로 정하고 적용 순서를 하나로 정한다. 예: 사전(dictionary_add·event_split) → 재분해 → tuple_assign → canonical_mapping → fold_approve → exclude → conflict_override/dismiss.

---

## ④ 행선지 표본 20 대조

`erd-v2.2-column-map.md` 의 원장 21 구간 573행에서 20행을 뽑았다. 이전 검토의 seed(20261104)로 뽑으면 이전과 같은 20행이 나와서 seed 22 로 다시 뽑았다. (a) 원장 실물에서 그 잎 키 경로를 직접 확인했고(원장 21 파일을 걸어 잎 경로 집합을 만든 뒤 대조), (b) 표적(개체.속성 / dict / R#.속성)이 `erd-v2.2.json`·사전 파일에 정의돼 있고 그 출처 키를 갖고 있는지 확인했다. step1 행은 지시대로 원천 파일을 열지 않아 제외했다.

| # | 파일:경로 | 행선지 → 표적 | 원장 실물 | ERD 표적·출처 |
|---|---|---|---|---|
| 1 | literature-evidence.json:source_method | 개체 → source_file.method | 있음 | ok |
| 2 | pih-risk.json:procedures[].risk_factors[] | 엣지 → R15.risk_factors | 있음 | ok |
| 3 | anatomy-danger-zones.json:zones[].tissue_data.frontalis_thickness.lateral_canthus_mm | 개체 → site.tissue_data.* | 있음 | ok (`tissue_data.*` 키 보존 obj) |
| 4 | taxonomy.json:modality[].subcategories[].items[].extracted.onset_duration.maintenance | 개체 → catalog_item.maintenance | 있음 | ok |
| 5 | literature-evidence.json:categories.{code}.adverse_effects[].patient_ja | 개체 → adverse_expression.patient_text | 있음 | ok |
| 6 | extracted.json:{code}.overview | 개체 → modality.overview | 있음 | ok |
| 7 | procedure-profiles.json:profiles[].prepNotes | 개체 → modality.prep_notes | 있음 | ok |
| 8 | combo-recipes.json:recipes[].followUp[].action | 개체 → package.follow_up.action | 있음 | ok |
| 9 | pih-risk.json:risk_levels.moderate | 사전 → dict:pih_risk_level | 있음 | ok |
| 10 | pre-procedure-checklist.json:category_specific[].checks[].label | 개체 → person_condition.name | 있음 | ok |
| 11 | anatomy-danger-zones.json:zones[].tissue_data.nasal_tip_skin_thickness_mm | 개체 → site.tissue_data.* | 있음 | ok |
| 12 | procedure-comparison.json:comparisons[].procedures[].cost_range | 엣지 → R12.cost_range | 있음 | ok |
| 13 | literature-evidence.json:categories.{code}.adverse_effects[].accuracy_score | 개체 → adverse_expression.accuracy_score | 있음 | ok |
| 14 | treatment-sequence.json:common_combos[].total_time | 개체 → package.total_duration | 있음 | ok |
| 15 | taxonomy.json:modality[].subcategories[].items[].extracted.mechanism | 개체 → catalog_item.mechanism | 있음 | ok |
| 16 | anatomy-danger-zones.json:zones[].tissue_data.rhinion_data_source | 개체 → citation.text | 있음 | ok |
| 17 | anatomy-danger-zones.json:zones[].nerves[].significance | 엣지 → R21.significance | 있음 | ok |
| 18 | pre-procedure-checklist.json:universal_checks[].label | 개체 → person_condition.name | 있음 | ok |
| 19 | procedure-comparison.json:comparisons[].subtitle | 개체 → package.subtitle | 있음 | ok |
| 20 | taxonomy.json:modality[].category | 개체 → modality.name | 있음 | ok |

**20/20 일치.** 이 방식의 대조는 「잎 키 → 표적 속성」의 선언만 본다. 그래서 3-C(R29 엣지 출처 누락)처럼 **엣지 쪽 출처 목록이 비어 있는 것**은 표본에 걸리지 않는다. 3-C 는 개체 속성 출처와 관계 출처를 비교해서 찾았다.

---

## ⑤ 추정·유사도 매칭을 허용하는 지점

문자열 유사도 매칭은 없다(§1.1, json `no_similarity: true`, ⑦ 은 표시만 한다). 남아 있는 것은 **원장에 없는 값을 추정해 채우거나, 해석을 고르는 규칙**이다.

| 어디 | 규칙 | 성격 |
|---|---|---|
| §1.5 L114 | 부작용 site·course 를 멤버 → 같은 묶음 → outer → 「이름 전체에 하나뿐이면」 순으로 상속 | **추정** — LOP 시술 중 통증이 지연이 됨(2-A) |
| §1.5 분해 · 9.6.6 | 미등록 조각을 버리고 남은 조각으로 튜플을 만들어 접음 | **정보 삭제 후 일치** (2-B) |
| §4 L81 사건 사전 「표기 변형은 동의어」 | 과민반응·동상·지방괴사·섬유화·공기색전 | 사전이 사건을 합친다. 매칭은 완전 일치지만 사전 값 자체가 판단이다(2-C · 결정) |
| §2.7 L301 · L247 | 기법 상속 문구·출처 잔재 | 규칙은 꺼졌지만 계약 문서에 추정의 원천이 남아 있다(1-B) |
| §1.4 조합 규칙 | `+` 뒤 빈 멤버를 버림(엑셀V+ → 엑셀V) · `/` 를 조합(combo_ref, 함께 받는 묶음)으로 읽음 — `실리프팅(PDO/PCL)`·`바이오스티뮬레이터(스컬트라/엘란쎄)` 는 원문상 「또는」에 가까움 | 해석 선택. 튜플 칸은 버리지 않으므로 정의 1 위반은 아니지만, package 의미는 추정이다 |
| §1.4 what 규칙 6 | 계열과 제품 양쪽에 닿으면 product | 해석 규칙(1-C · 결정) |
| §1.3 1단계 | 힌트가 없으면 「계열 동의어에 닿는 첫 조각」의 계열 | 결정론적인 「첫」 선택 |
| §1.3 · §1.4 · §1.5 | 왼쪽부터 가장 긴 연속 토큰 구간 | 결정론(탐욕) — 허용 범위 |
| §1.4 site | 참조가 분류 항목에 닿으면 그 항목 튜플의 site 를 셈 | 같은 것(①)의 값이라 허용 범위 |
| §5 ④ | 신뢰 순위 자동 채택 | 사용자 결정 — 레코드가 남으므로 허용 |
| §5 ⑦ | 유사도만 높은 중복 → duplicate_candidate | 표시만 하고 병합하지 않음 — 허용 범위 |

---

## ⑥ 동결 판단

**동결 불가.** 정의 1·2 가 말하는 「시술」이 관계의 끝에 오지 않고(1-A), 부작용 축에 「추정 상속」(2-A)과 「모르는 조각을 버리고 접기」(2-B)가 남아 있다. 정의 3 의 「사람 판정 → 결정 레코드 → 빌드 적용」은 담을 수 없는 판정 종류(3-A)와 바뀌는 대상 id·순서 부재(3-B) 때문에 끝까지 닫히지 않는다.

### 동결 전 꼭 고칠 것 — 구조만

1. **엣지의 시술 끝 = procedure 튜플** (1-A · L555 · R9/R12/R15~R18). 참조 ②③ 가 만든 PRC 튜플을 그 참조 엣지의 끝으로 정한다. target_depth·what 은 엣지 속성으로 남긴다. M 코드 끝(complications/consent/pih/sequence 의 categories[].id·procedure_ref)도 what=계열(·하위분류·항목) × none × none 의 anchor 튜플로 받거나, 「계열 수준 진술」이라는 예외를 문장으로 명시한다. 이렇게 하면 R15 「원인 시술」이 정의 2 와 맞는다.
2. **부작용 축의 멤버 밖 상속을 끈다** (2-A · §1.5 L114). 경과·부위는 사건이 놓인 멤버 안의 수식어에서만 읽는다. 바깥 묶음이 괄호 안을 설명하는 경우(「주사 부위 반응 (부종·…)」)만 남길지는 하나로 정해서 적는다. 멤버 밖 상속 후보는 시술의 §9.5.6 처럼 목록으로 내고, 적용은 결정으로 한다.
3. **부작용 접힘 조건에 「미등록 조각 0」을 넣는다** (2-B · §1.5 · §9.6.6). complications 이름에 미등록 조각이 있으면 그 이름의 튜플에 anchor(레코드 id)를 섞어 고유하게 한다. 표현(AEX)은 정체성을 만들지 않으니, 미등록 조각이 있는 표현은 R29 match_status 로 구분(partial)만 한다.
4. **결정 kind 보강** (3-A · §5.2). edge_assert(R30) · tuple_assign 확장(튜플 목록·combo, 부작용 원천 대상) · conflict_dismiss(status dismissed). canonical_mapping.scope 는 id 목록으로 한다.
5. **결정 대상 id 고정 + 적용 순서** (3-B · §5.2 · json id_rule). build_reads kind 의 target 은 원장에서 나온 고정 id(CAT-/REF-/AEX-/complications 레코드/DIC-)만 쓴다. fold_approve 는 PRC 가 아니라 anchor 목록을 받는다. conflict 식별자에는 파생 id 대신 anchor 를 쓴다. 결정 적용 순서는 한 줄로 고정한다.
6. **계약 문구·출처 정정** (1-B · 3-C). §2.7 L301·json `entities.technique.definition` 에서 상속 문장을 지운다. §2.5 L247 technique_id 출처(와 site_id)는 이름 키로 바꾼다. R29 출처(L843)에 taxonomy.json safety 잎 키 11개를 넣는다.

### 동결 후 결정 레코드로 처리할 것

- 1-C 「보톡스」 PRD ↔ MOD — canonical_mapping
- 1-D 엑셀V+ 의 what — tuple_assign(항목 자신 또는 별도 제품)
- 2-C 사건 동의어 과민반응·동상·지방괴사·섬유화·공기색전 — event_split
- 2-D 부작용 none·미상을 식별자 값으로 둘지 — scope_review
- 볼뉴머 M4/M9 · 엠페이스/엠페이스(EMFACE) · 라라젯/라라젯 (클렌징) 류 — fold_approve 또는 conflict_dismiss(위 4·5 가 들어간 뒤)
- 기법 상속 후보 9계열(§9.5.6) — canonical_mapping
- ambiguous 3 · multi_* 미해결 · 미등록 조각 — tuple_assign(확장형) · dictionary_add
- `주사` → 주사 부위 같은 부위 동의어(9.6.6 #2) — dictionary_add
- 조합 기호 `/` 를 「함께」로 읽을지 「또는」으로 읽을지(실리프팅(PDO/PCL) 등) — scope_review
- R15 끝의 `site` 를 남길지 — scope_review(확인 항목)
- DEC-20~23 승인 — status approved · decided_by · decided_at 채움
- §12-3 step1 제품 확장 — dictionary_add 묶음
