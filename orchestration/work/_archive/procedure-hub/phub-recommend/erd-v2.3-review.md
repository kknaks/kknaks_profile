# ERD v2.3 독립 검토 (3차 · 동결 판정)

검토 2026-11-04 · 대상 `erd-v2.3.md`(2,636줄) · `erd-v2.3.json` · `erd-v2.3-dictionaries.json` · `erd-v2.3-tuples.json` · 행선지 대조에 `erd-v2.3-column-map.md` · 원장 21(`phub-stg-2026-10-26/`). 이전 검토서 `erd-v2.2-review.md` 는 ⓪ 대조에만 썼다. 작성 과정 문서(v1·v2·v2.1·v2.2 본문·발주서·step*·silver-*·DATA-001·_archive)는 열지 않았다.
판단 기준은 사용자가 정한 정의 셋뿐이다. 완성도·사전 크기·미상 비율·미해결 수·실버 빌드 때 결정으로 채울 수 있는 것은 근거로 쓰지 않았다.

| 정의 | 구현 위치 | 어긋남 |
|---|---|---|
| 1 시술 = 무엇 × 어디 × 어떻게 · 엣지 끝 = 튜플 | §1.1 L26~27 · §1.4 · §2.5 · §3 머리 L573 · R3·R9·R12·R15~R18 · §9.5.8 | **0 구조 · 3 결정** |
| 2 부작용 = 사건 × 부위 × 경과 · 표현은 원문 | §1.5 · §2.14 · §2.15 · R15 · R29 · R30 · §9.6 | **3 구조 · 3 결정** |
| 3 원장 불변 · 충돌 목록 · 결정 레코드 · 안정 키 · 출처 | §1 · §1.1 L29~30 · §2.20 · §2.21 · §5 · §5.2 · §5.4 · R23~R25 | **3 구조(전부 문구·출처 한 줄) · 1 참고** |

어긋남은 모두 **구조 6 · 결정 6**. 구조 6 중 규칙이 추정·버림을 허용하는 것은 **3**(전부 부작용 축 §1.5), 나머지 3 은 문구·출처를 한 줄씩 고정하는 것이다.

---

## ⓪ 이전 검토 ⑥ 「동결 전 꼭 고칠 것」 (검토 6항 = 발주서 7건) 반영 여부

| 발주 # | 이전 지적 | v2.3 에서 고친 자리 | 판정 |
|---|---|---|---|
| ① | 1-A 엣지의 시술 끝 = procedure 튜플 | §1.4 「엣지 끝(v2.3)」 L113 · §3 머리 L573 · R3 L593 · R9 L628/635 · R12 L656/673 · R15 L700/723 · R16 L730/734 · R17 L743/746 · R18 L767/770 의 target_depth enum(modality\|subcategory\|procedure\|product — catalog_item 삭제) · via_catalog_item · 다이어그램 L39 R3 from=PROCEDURE · json `edge_end_rule`·`proc_axis_edges`·`tuple_rules.procedure.code_references`. 실측 §9.5.8: 자리 30 · 건 3,423 = procedure 1,883 · modality 953 · subcategory 62 · product 318 · unresolved 207 — modality/subcategory 끝은 전부 M 코드·하위분류 id 자리, product 끝은 제품 전용 자리·제품 레코드(아래 ②). M 코드만 적힌 참조 9 는 튜플을 만들지 않고 노드(`node`). 「승격 규칙」 문장 0(검산 H). | **고침** |
| ② | 2-A 부작용 축의 멤버 밖 상속을 끈다 (경과·부위) | **경과만** — §1.5 L120 · §2.14 L433 · §4 L1004 · §4.2 L1056 같은 문장(사건에 바로 붙은 수식어만 · 사건 둘이면 수식어 붙은 사건에만) · json `course_rule` · tuples.json `course_member_only:true` · 실측 §9.6.2a LOP → (통증, 미상)+(통증, 지연). **부위는 v2 그대로** — §1.5 L119 「site 는 v2 그대로 멤버 → 같은 묶음 → outer 묶음 → (이름 전체에 그 축의 값이 하나뿐이면 그 값) 순」 · json `tuple_rules.adverse.tuple` 같은 문장. 이전 검토 ⑥-2 는 「경과·부위는 사건이 놓인 멤버 안의 수식어에서만」이었다 | **절반** → 아래 2-A′ |
| ③ | 2-B 부작용 접힘 조건에 「미등록 조각 0」 | §1.1 L28 · §1.5 L121~123 · §2.14 식별자 L424 · event_kind·anchor·all_dict_values·candidate_name·event_fragments·extra_* 속성 · json `adverse_fold_rule`·`id_rule.adverse_effect`·`tuple_rules.adverse.raw_name`. 실측 §9.6.1·§9.6.6: raw_name 18(이름마다 하나) · 접힌 튜플 11 전부 미등록 0 · 이전 ② 표의 「주사 통증 / 불편감」「공기색전·카테터 관련 감염」「구형구축 (…)」 전부 raw. 표현은 raw 를 만들지 않고 R29 match_status=partial. | **고침** (이름 쪽) — 표현 쪽에 같은 문제가 남는다 → 아래 2-C′ · raw 튜플의 칸 → 2-B′ |
| ④ | 3-A 결정 kind 보강 (edge_assert · tuple_assign 확장 · conflict_dismiss · scope id 목록) | §2.21 enum 16 · §5.2 표: `edge_create`(relation·from_ref·to_ref 구조체 5종) · `tuple_assign_multi`(tuples[]) · `adverse_tuple_assign`(locator raw_name\|expression → tuples[](event_id, site_id, course_id)) · `conflict_close`(verdict not_same\|both_valid\|needs_source → status dismissed · close_verdict 속성 L549) · `canonical_mapping.scope: str[]`(§9.5.6 scope 열 = CAT- 목록) · R30 L877 「edge_create approved 일 때만」 · ⑦⑨ 규칙 L1072/L1074 에 닫는 kind. json `decision_kinds` 16 과 md 표 일치. | **고침** — 대상 문구 하나 남음 → 3-A′ |
| ⑤ | 3-B 결정 대상 id 고정 + 적용 순서 | §1.1 L30 · §5.2 target 규칙 L1114 · json `decision_target_rule`(CAT-/REF-/locator/MOD-SUB-PRD-SIT-TEC-/사전 값/stable_key · PRC-/ADV-/CFL- 금지) · `fold_approve` → anchors/keep_anchor · `conflict_override`/`conflict_close` → conflict_key(stable_key = kind + locators[] · §2.20 L535/L543) · `exclude` → (kind, key) · 원장 locator 정의 L29 · 적용 순서 §5.4 L1170 ①~⑦ + ⓪ 원장 메모 · 같은 단계 decided_at 순 · json `decision_apply_order`. 검산 K-2 결정 24 에 파생 id 0. | **고침** — CAT- 의 「계열 코드」 고정 문구 하나 남음 → 3-B′ |
| ⑥ | 1-B 기법 잔재 문구·출처 (와 site_id 출처) | §2.7 L310 정의에서 상속 문장 삭제 · §2.5 L256 technique_id 출처 = what_id 와 같은 이름·참조 키 19 · json `entities[technique].definition`·`procedure.technique_id.sources` · 검산 K-7 「상속」 0. **site_id 출처는 그대로 「(파생/ERD 정의)」**(§2.5 L255 · json `site_id.sources: None`) — 이전 ⑥-6 「technique_id 출처(와 site_id)는 이름 키로」 중 site_id 미반영 | **절반** → 3-C′ |
| ⑦ | 3-C R29 출처에 taxonomy safety 잎 키 11 | R29 L867 출처 22 = 11 + 11 · json `r29_taxonomy_safety_keys` 11 · 검산 K-8 adverse_expression.text 출처 21 ⊆ R29 출처. | **고침** |

이전 「확인」 항목(R15 from 의 `site` 끝 — 출처 키 없음)은 그대로 남아 §12 scope_review 로 갔다(L2632). 결정으로 처리.

---

## ① 정의별 구현 위치와 어긋남

### 정의 1 — 시술 = 무엇 × 어디 × 어떻게. 같은 세 칸이면 같은 시술, 미상이면 안 접는다. 시술에 걸리는 엣지의 끝은 시술 튜플.

**구현.** 튜플·식별자·접힘 조건은 v2.2 그대로(§1.1 L26~27 · §2.5 L247). 세 칸 전부 사전 값일 때만 anchor 없는 PRC id, 아니면 anchor(CAT-/REF-/…#m<i>)가 식별자에 들어가 항목·참조마다 고유. 실측 585 튜플 전부 anchor(세 칸 전부 사전 값 0 · anchor 둘 이상 0 — tuples.json 재계산 일치). v2.3 이 더한 것은 엣지 끝: 시술 축 7 관계(R3·R9·R12·R15·R16·R17·R18)의 끝은 참조가 튜플로 해결되면 그 튜플(미상 칸이 있는 anchor 튜플도), 노드(MOD/SUB/PRD)는 참조가 그 층까지만 적힌 자리(M 코드·하위분류 id·제품 전용 자리·제품 레코드)뿐. catalog_item 은 끝이 아니다(항목 521 전부 튜플). §9.5.8 실측에서 텍스트 자리의 procedure 끝은 전부 anchor 튜플이고 노드 끝은 코드 자리에서만 나온다. 정의 1 의 세 문장이 모두 구조로 들어 있다.

**어긋남 — 구조 0.** 결정으로 처리할 것 3:

| # | 어디 | 무엇 | 분류 |
|---|---|---|---|
| 1-C | §1.4 what 규칙 6 · §9.5.4 | 「보톡스」 문자열 → PRD-보톡스, 코드 `M1` → MOD-보톡스. 같은 what 에 id 둘. v2.2 와 같고 미상 칸 때문에 접히지 않는다 | 결정(§12 1-C canonical_mapping) |
| 1-D | §1.4 조합 규칙 `+` | `엑셀V+`[M8] → what=product:엑셀V(complete · CAT-af03bac034). `+` 뒤 빈 멤버를 버린 결과. anchor 가 있어 접히지 않는다 | 결정(§12 1-D tuple_assign) |
| 1-E | §1.1 L27 「같은 라벨·같은 힌트의 참조는 자리가 달라도 같은 anchor」 · §9.5.5 | 같은 (what_id, site_id, technique_id) 인데 anchor 가 달라 갈린 튜플 **21 조 · 55 튜플**(tuples.json 집계: `보톡스`@M1 ↔ `보톡스` 무힌트 · `스킨부스터` 힌트 5종 · `스컬트라` CAT ↔ market-pricing REF 2 · `볼뉴머` M4 ↔ M9 등). 세 칸에 미상이 있으니 정의대로 안 접은 것이고, 합칠지는 fold_approve(anchors) 몫 | 결정(fold_approve · §12 1-G 류) |

참고(어긋남 아님): R9 `products[]` 자리의 「보톡스」「쥬비덤」 30 건은 product 노드가 끝이고, 같은 문자열이 `procedures[].name` 자리에서는 튜플(product:보톡스 × none × none)이 끝이다. 「참조가 제품 층까지만 적힌 자리」를 자리 종류로 정한 해석이라 정의 1 의 단서 안이다. `modality.same_session_order`(§2.2 L200 「categories[] 가 가리키는 계열/하위분류에 둔다」)와 R18 pair_rule 의 끝(§9.5.8 `IPL`·`프락셔널`·`혈관` → 튜플)이 서로 다른 층을 가리키는 문구 불일치가 있다 — 속성 쪽 문장을 「튜플로 해결되면 그 튜플」로 맞추면 된다(동결을 막지 않음).

### 정의 2 — 부작용 = 사건 × 부위 × 경과. 원인 시술은 R15 엣지, 등급·빈도·시기·대처는 엣지 속성. 문헌 문장·타임라인 문구·응급 징후는 원문 표현. 미등록 조각이 있는 이름은 접지 않는다.

**구현.** 튜플 (event, site_ref, course) · 식별자 sha(event|site|course) · 원인 시술은 R15 로만 · 속성 20종은 R15 엣지(L700~720) · 원문은 adverse_expression(§2.15) → R29 · 인과는 R30(edge_create 로만). 경과는 같은 멤버 안의 수식어만(L120). 미등록 조각이 있는 complications 이름은 raw_name 튜플(anchor=locator)로 접히지 않는다(L121~122). 큰 틀은 정의 2 대로다.

**어긋남 — 구조 3.**

| # | 어디 | 무엇이 어긋나나 | 분류 |
|---|---|---|---|
| 2-A′ | §1.5 L119 「site 는 v2 그대로 멤버 → 같은 묶음 → outer 묶음 → (이름 전체에 그 축의 값이 하나뿐이면 그 값)」 · json `tuple_rules.adverse.tuple` | **부위를 사건이 놓인 멤버 밖에서 추정해 채운다.** 경과에서 끈 상속이 부위에는 그대로다. tuples.json 으로 멤버(`· / , + 및 또는 — -- :` · 괄호)를 다시 갈라 세면 부위가 사건과 다른 멤버·바깥 묶음에서 온 (표현, 튜플) 쌍이 **119**(같은 멤버 277), complications 이름에서 3. 틀린 사례: `주사 부위 일시적 부종, 멍, 두통, 드물게 눈꺼풀 처짐`(taxonomy item safety) → **두통 × 주사 부위**, `시야 변화/두통 + 주사 부위 변색`(timeline emergency) → **두통 × 주사 부위** — 두 표현이 §9.6.4 #15 튜플 ADV-ef3a30183f 를 만들고 R15 가 거기 붙는다. 반대로 **부위 조각을 버리는 길**도 남아 있다: `이마/눈가 당김감`(timeline normal · 미등록 0 · complete) → 당김감 × **눈가** 하나 — `이마` 는 어느 튜플에도 없고 dict 튜플은 extra_sites=[] 이라 기록도 없다(같은 모양 8 표현: `혈관 폐색(미간·코)` 류는 사건 멤버에 부위가 없어 none 으로 가며 미간·코가 버려진다). 시술 축의 multi_site 가드(§1.4 site: 둘 이상이면 조립하지 않고 extra_sites 에 전부)가 부작용 축에는 없다 | **구조** |
| 2-B′ | §1.5 L122 raw_name 규칙 「site/course 는 닿은 조각이 하나씩일 때만 그 칸」 · json `tuple_rules.adverse.raw_name` | raw_name 튜플에서는 **이름 전체 상속이 되살아난다.** 이름 안 어디에 있든 경과 조각이 하나면 그 칸에 넣는다. 실측 raw 18 중 3: `육아종 / 지연성 염증성 결절 (…)`[M2] → course **지연**(사전 분해는 (육아종, 미상)+(결절, 지연)) · `통증·불편감 및 지연성 통증 (… LOP)`[M14] → course **지연**(사전 분해는 (통증, 미상)+(통증, 지연) — 수정 ② 가 고친 바로 그 이름이 raw 칸에서는 v2.2 값으로 돌아간다) · `감각이상·저림 (표재 감각신경, 가역적)`[M16] → course **일시**(사전 분해는 (감각 이상, 미상) · §9.6.2a #8). 검산 K-6 「미상 아닌 경과가 멤버 밖에서 온 튜플 0」은 dict 튜플만 센 것이다. 이 칸은 식별자(RAW:anchor\|site\|course\|anchor)와 R15 끝에 그대로 실린다 | **구조** (규칙 한 줄 · 영향 3 튜플) |
| 2-C′ | §1.5 L123 「표현이 만든 사전 튜플은 v2 그대로(65 에 없던 새 튜플 §9.6.4)」 · json `tuple_rules.adverse.expressions` ↔ 같은 §1.5 L121·§2.14 L423·§2.15 L462 「표현은 정체성을 만들지 않는다」(5곳) | **표현이 부작용 단위를 만든다 — 미등록 조각을 버린 채로.** §9.6.4: 65 이름에 없던 새 튜플 **57**(partial 40 · complete 17), 그중 **20** 은 미등록 조각이 있는 표현만으로 생겼다(tuples.json 대조). 예: `시야 변화/두통 + 주사 부위 변색` → 두통 × 주사 부위 · `역행성 색전(미간·안동맥 0.04mL 폐색 위험)` → 색전 × 미간(「안동맥」「폐색」 버림) · `건조(입술/피부/점막)` → 건조 × 입술(피부·점막 버림) · `** 지연성 혈관폐색 -- 여전히 골든타임 **` → 혈관 폐색 × none × 지연. 이름 쪽에서 수정 ③ 이 막은 것(모르는 조각을 버리고 세 칸이 같다고 주장)과 같은 경로가 표현 쪽에 열려 있고, 그 튜플에 R15 엣지(frequency_class·reaction_level)가 붙어 실버 adverse_effect 가 된다. 정의 2 는 표현을 「부작용을 가리키는 원문」으로 정했다 — 가리킬 튜플이 없을 때 표현이 (조각을 버린) 튜플을 세우는 것은 구조다. 미등록 0 인 표현이 세운 17 은 조각을 버리지 않았으므로 정의와 충돌하지 않는다(2-A′ 의 `이마/눈가 당김감` 만 예외) | **구조** |

결정으로 처리할 것 3(이전과 같음): 2-C 사건 동의어(과민반응→아나필락시스 · 동상·지방괴사→괴사 · 섬유화→경결 · 공기색전→색전 — §12 event_split) · 2-D none·미상을 식별자 값으로 둘지(§12 scope_review) · §9.6.2a 괄호 안 동의어가 만드는 같은 사건의 미상 튜플(`일시적 감각이상 (따끔거림·저림·감각둔화)` → (감각 이상, 일시)+(감각 이상, 미상) — §12 「수식어가 붙지 않은 사건의 경과」 adverse_tuple_assign).

### 정의 3 — 원장은 안 고친다. 충돌은 기계 목록(④ 자동 해결도 레코드). 사람 판정은 결정 레코드, 빌드는 승인된 결정만 정해진 순서로. 결정은 바뀌는 id 를 가리키지 않는다. 모든 실버 값은 원장 파일·키 경로 출처.

**구현.** 브론즈 sha256 22 일치(검산 D). ④⑥⑦⑧⑨ 전부 conflict · ④ 는 auto_resolved_by_trust 레코드(§5 L1069). 결정 16 kind · approved 만 · 순서 ①~⑦(§5.4). target 은 CAT-/REF-/locator/고정 id/사전 값/stable_key 만(§1.1 L30 · 검산 K-2). conflict 는 CFL- 대신 stable_key(kind + locators[]). 출처는 R25. 정의 3 의 다섯 문장이 구조로 들어 있다.

**어긋남 — 구조 3(전부 한 줄 문구·출처).**

| # | 어디 | 무엇이 어긋나나 | 분류 |
|---|---|---|---|
| 3-A′ | §5.2 `adverse_tuple_assign` 비고 L1122 「partial/unlinked 표현」 · §2.15 match_status L462 「partial … adverse_tuple_assign 의 대상」 · json `decision_kinds[adverse_tuple_assign].note` | 재지정 대상을 partial·unlinked 표현으로 적어 **linked 인데 틀리거나 조각을 잃은 표현**(`이마/눈가 당김감` — 미등록 0 · linked · 이마 유실, 2-A′)을 가리킬 kind 가 없다. target 구조체 자체(locator · kind=expression)는 어느 표현이든 받을 수 있으므로 비고의 대상 조건을 「표현 레코드 전부」로 넓히는 한 줄 | **구조**(문구) |
| 3-B′ | §2.4 L221 catalog_item 식별자 「계열 코드 + 정규화 항목 이름」 · §5.2 `reclassification`(⓪ 원장 적재 때 R2 재배치 · M9-2-4 → M8) · json `id_rule.catalog_item` | CAT- 가 결정 target 의 기준 안정 키인데, 「계열 코드」가 taxonomy 트리 위치인지 reclassification 이 적용된 뒤의 계열인지 적혀 있지 않다. 뒤의 것이면 ⓪ 결정 하나가 CAT- 를 바꾸고(소프라노 티타늄 M9→M8 · 볼뉴머 classification_issue M4→M9 면 M9\|볼뉴머 충돌), 그 CAT- 를 가리키는 모든 결정·R26·anchor 튜플 id 가 흔들린다 — 「결정은 다른 결정 뒤에 바뀌는 id 를 가리키지 않는다」 위반. 실측(tuples.json)은 트리 위치다: `CAT-bd1d93db49` = sha256(`M9|소프라노티타늄`), `CAT-102bed4c6f` = sha256(`M9|볼뉴머`). 문서에 「계열 코드 = taxonomy 트리 위치(원장) · reclassification 은 R2 만 바꾼다」 한 줄 | **구조**(문구) |
| 3-C′ | §2.5 L255 `site_id` 출처 「(파생/ERD 정의)」 · json `procedure.site_id.sources: None` | 부위 칸은 이름·참조 문자열에서 읽는 값인데 출처 키가 없다(what_id·technique_id 는 이름 키 19 를 갖는다). 「모든 실버 값은 (파일, 잎 키 경로) 출처」와 어긋남. 이전 ⑥-6 에 명시된 항목 | **구조**(출처 정정) |

참고 1(어긋남으로 세지 않음): `canonical_mapping.new_value.to_id` 는 「MOD-/SUB-/PRD-/TEC- 고정 id」인데 §9.5.6 의 to_id 는 `DIC-6634bee670`(기법 사전 값 id) — 사전 값은 허용 키 「사전 이름 + 정준값」로 가리킬 수 있으니 표기만 맞추면 된다.
참고 2: 비사건 사전(경과·부위·상대 부위)의 **동의어 제거**를 적을 kind 는 여전히 없다(event_split 은 사건 사전 전용 · exclude dictionary_value 는 정준값 단위 · dictionary_add 는 추가만). §9·§12 의 미룬 결정에는 없으므로 수용성 판단(③)에서 세지 않았다.
참고 3: tuples.json 의 procedure `sources` 는 (origin, label, family, anchor)뿐이고 파일·잎 키 경로가 없다(adverse 쪽은 locator 가 있다). ERD 는 R25 를 실버 빌더 생성으로 두므로 ERD 위반은 아니다(이전과 같음).

---

## ② 접힘·엣지 끝 검토 (§9.5 · §9.6 · §9.5.8 · tuples.json)

### 시술 — 접으면 안 됐던 것

**없다.** 세 칸 전부 사전 값 튜플 0 · anchor 둘 이상인 튜플 0(tuples.json `multi_anchor` 재계산 0). 같은 튜플에 원천이 둘인 경우는 ① 정규화 완전 일치(참조 = 분류 항목 이름 · 같은 라벨·힌트)뿐이다.

### 시술 — 같은 세 칸인데 안 접힌 것

정의상 **없다**(「같은 세 칸」은 세 칸 전부 사전 값일 때만 성립하고 그런 튜플이 0). 정보로 두면: (what_id, site_id, technique_id) 가 같고 anchor 만 다른 묶음 **21 조 · 55 튜플**(1-E). 전부 미상 칸이 있어 안 접는 것이 맞고, fold_approve 의 anchors 목록으로 바로 담긴다.

### 시술 — 끝이 튜플이어야 하는데 노드인 것

**없다.** §9.5.8 자리 30 전부 대조(tuples.json `edge_ends` 30 행 · 합계 재계산 일치 — procedure 1,883 · modality 953 · subcategory 62 · product 318 · unresolved 207, ③ 참고 행 제외). 노드 끝은 전부 (a) M 코드만 적힌 자리(contraindications from/to 54 · combo-recipes 19 · problem-combos 63 · consent/pre-procedure categories[].id 34 · complications categories[].id 10 · timeline category 9 · pih M 코드 3 · sequence_order 코드 7), (b) 실존 하위분류 id(pih 7 · M16-DCA 1 · M15-도포/팩 2 · 타임라인 문구 52), (c) 제품 전용 자리·제품 레코드(R9 products[] 30 · taxonomy products safety 288). 텍스트 자리에서 튜플로 해결된 참조는 예외 없이 튜플 끝(anchor 튜플 포함 · via 항목 표시). catalog_item 끝 0. v2.2 에 있던 M 코드 참조 튜플 9 는 노드로 빠졌다. 미해결 207 은 끝 없음(⑨).

### 부작용 — 접히면 안 됐던 것

이름(complications 65) 쪽: **없다.** 접힌 튜플 11 전부 미등록 0 · dict(§9.6.6 · tuples.json `complications_folded_with_unregistered` 0). 이전 ② 표의 12 튜플은 전부 raw_name 으로 갈렸다.
표현 쪽: **있다(2-C′).** 미등록 조각이 있는 표현이 새 사전 튜플 20 을 세우고(partial 표현만으로), 40 partial 튜플에 R15 가 붙는다. 「접힘」 형태는 아니지만 「모르는 조각을 버리고 세 칸으로 단위를 주장」하는 같은 경로다.

### 부작용 — 같은 세 칸인데 안 접힌 것

raw_name 18 은 정의대로 안 접힌다(미등록 조각). 그중 사전 분해가 기존 dict 튜플과 세 칸이 같은 것(`PIH (시술 후 과색소침착)`[M8]·[M11] → 색소침착 × none × 미상 = M14 의 튜플 · `홍반 (시술 직후 빨개짐)`[M9] → 홍반 × none × 미상 등 다수)은 adverse_tuple_assign 으로 합류할 자리가 있다. 결정.

### 부작용 — 끝

R15 의 부작용 끝은 전부 adverse_effect 튜플(dict 97 + raw 18). R15 from 의 `site` 끝은 출처 키 없이 남아 있다(§12 scope_review · 결정).

---

## ③ 결정 개체(kind 16) 수용성 — §9·§12 에 미룬 결정을 담을 수 있나

| 미룬 결정 | kind | 담기나 |
|---|---|---|
| §9.5.6 R5 계열 기법 후보 9 | canonical_mapping(from_ref=R5:Mx · scope=CAT-[] · to_id) | 담김 — scope 가 id 목록(tuples.json `inheritance_candidates[].scope`). to_id 표기만 참고 1 |
| §12 1-C 보톡스 PRD↔MOD | canonical_mapping | 담김 |
| §12 1-D 엑셀V+ | tuple_assign(target.catalog_item_id) | 담김 |
| §12 1-G 볼뉴머 M4/M9 · 엠페이스/엠페이스(EMFACE) · 라라젯/라라젯 (클렌징) · 1-E 의 21 조 | fold_approve(anchors=CAT-/REF-[] · keep_anchor) 또는 conflict_close(not_same) | 담김 — 「같지 않다」도 conflict_close 로 닫힌다 |
| §9.5.3 ambiguous 3 · §9.5.4 multi_site·multi_primary 미해결(보톡스 이마/미간 · 필러 볼/턱 · 이마 주름 (수입) …) | tuple_assign_multi(tuples[]) · tuple_assign | 담김 — 참조 자리면 combo_ref 로 멤버마다 R12, 분류 항목이면 튜플마다 R26 |
| §9.5.7·§9.6.5 미등록 조각 · §12-3 step1 제품 확장 | dictionary_add | 담김 |
| §12 2-C 사건 동의어 분리 | event_split | 담김 |
| §9.6.6 raw_name 18 재지정(카테터 감염 → 감염×카테터 · 구형구축만 · LOP 둘) · `주사`→주사 부위 | adverse_tuple_assign(locator kind=raw_name · tuples[]) · dictionary_add | 담김 — 지정 튜플이 raw 를 대체하고 locator 가 출처로 남는다 |
| §9.6.3 partial 860 · unlinked 1010 표현 | adverse_tuple_assign(locator kind=expression) | 담김(건수는 수용성 근거 아님). **linked 인데 틀린 표현**은 비고 조건 밖 → 3-A′(문구 한 줄) |
| §9.6.2a 수식어 없는 사건의 경과 | adverse_tuple_assign | 담김 |
| R30 인과 | edge_create(relation=R30 · from_ref/to_ref adverse_tuple) | 담김 |
| §9.3 ⑦ duplicate_candidate 175 「같지 않다」 · ⑨ 「범위 밖」 · ⑥ open 32 · ⑧ 2 | conflict_close(not_same\|both_valid\|needs_source) · conflict_override · dictionary_add | 담김 — 「단계 끝 = open 0」에 닿는 길이 생겼다(L1077) |
| §9.4 원장 메모 11 | reclassification(⓪) · ledger_correction_note · verification_hold · canonical_mapping | 담김 |
| §12 2-D · 조합 `/` 해석 · R15 site 끝 | scope_review | 담김(ERD 개정 기록) |
| DEC-20~24 승인 | status → approved · decided_by · decided_at | 담김 |

**담을 수 없는 종류: 없다.** 이전 ③ 의 「못 담는다」 4 종류가 전부 닫혔다. 남는 것은 adverse_tuple_assign 대상 조건 문구(3-A′)와, 미룬 목록에 없는 비사건 사전 동의어 제거(참고 2)뿐이다.

적용 순서(§5.4)는 결정 간 의존을 덮는다: 사전 → 매핑 → 지정 → 접기/분리 → 엣지 → 충돌 → 제외. ③ 지정이 ① 사전 추가 뒤의 재분해 위에 덮이고, ④ fold 가 anchor 를 받으므로 ③ 뒤 id 변화와 무관하며, ⑥ 충돌은 stable_key(locator 쌍)라 어느 단계에서도 같은 레코드를 가리킨다. 3-B′ 의 CAT- 계열 코드만 문서로 고정하면 「바뀌는 id 를 가리키는 결정」은 없다.

---

## ④ 행선지 표본 20 대조

`erd-v2.3-column-map.md` 의 원장 21 구간(파일별 절 · 573 행)에서 seed **303** 으로 20 행을 뽑았다(이전 seed 20261104·22 와 다름). (a) 원장 실물에서 잎 키 경로를 직접 확인(원장 21 을 걸어 잎 경로 집합을 만든 뒤 `{code}`·`*` 는 패턴 대조), (b) 표적이 `erd-v2.3.json` 개체 속성 / 관계 속성 / 사전 파일에 정의돼 있는지 확인.

| # | 파일:경로 | 표적 | 원장 실물 | ERD 표적 |
|---|---|---|---|---|
| 1 | anatomy-danger-zones.json:zones[].botox_specific.diffusion_range_cm | R22.diffusion_range_cm | 있음 | ok |
| 2 | pih-risk.json:procedures[].pih_risk | R15.pih_risk | 있음 | ok |
| 3 | literature-evidence.json:categories.{code}.effects[].patient_ko | evidence_statement.patient_text.ko | 있음 | ok |
| 4 | complications.json:categories[].complications[].management | R15.management | 있음 | ok |
| 5 | post-procedure-timeline.json:timelines[].phases[].caution[] | adverse_expression.text (kind=symptom_phrase · R29→R15) | 있음 | ok |
| 6 | treatment-optimization.json:by_concern[].severity_levels[].expected_sessions | package.expected_sessions | 있음 | ok |
| 7 | products.json:prp_exosome.products[].country | dict:country | 있음 | ok |
| 8 | literature-evidence.json:categories.{code}.moa[].citations[].journal | citation.journal | 있음 | ok |
| 9 | products.json:stem_cell.products[].type | dict:product_type | 있음 | ok |
| 10 | taxonomy.json:modality[].products[].extracted.onset_duration.duration | product.duration | 있음 | ok |
| 11 | complications.json:categories[].complications[].incidence | R15.incidence | 있음 | ok |
| 12 | post-procedure-timeline.json:timelines[].phases[].normal[] | adverse_expression.text (reaction_level=normal) | 있음 | ok |
| 13 | treatment-optimization.json:by_age_group[].note | person_condition.note | 있음 | ok |
| 14 | treatment-sequence.json:principles[] | clinical_rule.text | 있음 | ok |
| 15 | extracted.json:{code}.aftercare[] | modality.aftercare | 있음 | ok |
| 16 | products.json:energy_device.products[].manufacturer | dict:manufacturer | 있음 | ok |
| 17 | literature-evidence.json:version | source_file.version | 있음 | ok |
| 18 | taxonomy.json:modality[].subcategories[].items[].correction_note | decision.reason | 있음 | ok |
| 19 | problem-packages.json:updated | source_file.updated | 있음 | ok |
| 20 | anatomy-danger-zones.json:critical_safety_facts.blindness_highest_risk_zones | clinical_rule.text | 있음 | ok |

**20/20 일치.** 이 대조는 「잎 키 → 표적」 선언만 보므로 2-A′·2-C′ 같은 분해 규칙 문제나 3-C′ 같은 「표적은 있는데 출처가 비어 있는」 속성은 표본에 걸리지 않는다 — 그것들은 개체 속성 출처와 tuples.json 을 비교해서 찾았다.

---

## ⑤ 추정·유사도 매칭을 허용하는 지점

문자열 유사도 매칭은 없다(§1.1 L23·L31 · json `no_similarity: true` 양쪽 · ⑦ 은 표시만). 남는 것은 원장에 없는 값을 채우거나 해석을 고르는 규칙이다.

| 어디 | 규칙 | 성격 |
|---|---|---|
| §1.5 L119 | 부작용 site 를 멤버 → 같은 묶음 → outer → 이름 전체 유일값 순으로 상속 | **추정** — 두통 × 주사 부위(2-A′) |
| §1.5 (암묵) | 사건 멤버에 없는 부위 조각은 기록 없이 버림 | **버림** — 이마/눈가 당김감 → 눈가만(2-A′) |
| §1.5 L122 | raw_name 튜플의 site/course = 이름 안 어디든 조각이 하나면 그 칸 | **추정** — LOP·육아종/지연성 결절·가역적(2-B′) |
| §1.5 L123 · §9.6.4 | 미등록 조각이 있는 표현이 닿은 조각만으로 새 사전 튜플을 세움 | **정보 삭제 후 단위 생성** — 색전 × 미간 · 건조 × 입술(2-C′) |
| §4 L1003 · §4.1 | 사건 사전 「표기 변형은 동의어」(과민반응·동상·지방괴사·섬유화·공기색전) | 사전 값이 사건을 합침 — 결정(2-C) |
| §1.4 조합 규칙 | `+` 뒤 빈 멤버 버림(엑셀V+) · `/` 를 「함께」로 읽음(실리프팅(PDO/PCL)) | 해석 선택 — 결정(1-D · §12 `/`) |
| §1.4 what 규칙 6 | 계열·제품 양쪽에 닿으면 product | 해석 규칙 — 결정(1-C) |
| §1.3 1단계 | 힌트 없으면 계열 동의어에 닿는 첫 조각의 계열 | 결정론적 「첫」 — 허용 범위 |
| §1.3·§1.4·§1.5 | 왼쪽부터 가장 긴 연속 토큰 구간 | 결정론(탐욕) — 허용 범위 |
| §1.1 L27 | 같은 라벨·같은 힌트 참조는 자리가 달라도 같은 anchor | ① 정규화 완전 일치 — 허용 범위(1-E 는 그 반대 방향의 결정) |
| §1.4 site | 참조가 분류 항목에 닿으면 그 항목 튜플의 site 를 셈 | 같은 것(①)의 값 — 허용 범위 |
| §5 ④ | 신뢰 순위 자동 채택 | 사용자 결정 · 레코드 남음 — 허용 |
| §5 ⑦ | 유사도만 높은 중복 → duplicate_candidate | 표시만 — 허용 범위 |

시술 축(§1.3·§1.4)에는 추정 규칙이 남아 있지 않다. 남은 추정은 전부 부작용 축 §1.5 의 세 줄(L119·L122·L123)이다.

---

## ⑥ 동결 판단

**동결 불가 — 시술 축(정의 1)과 결정 구조(정의 3)는 동결 수준이나, 부작용 축 §1.5 에 「부위 상속·버림」(2-A′) · 「raw 칸 이름 전체 상속」(2-B′) · 「미등록 조각 있는 표현의 단위 생성」(2-C′) 세 규칙이 정의 2 의 「미등록·미상이면 기계가 단위를 주장하지 않는다」와 어긋난 채 남아 있다.** 셋 다 §1.5 안의 문장 교체와 재실측으로 닫히고 개체·관계 구조는 바뀌지 않는다.

### 동결 전 꼭 고칠 것 — 구조만

1. **부작용 site 규칙을 course 와 같은 기준으로** (2-A′ · §1.5 L119 · json `tuple_rules.adverse.tuple`). site 는 사건이 놓인 멤버 안의 조각만. 바깥 묶음이 괄호 안을 설명하는 모양(「주사 부위 반응 (부종·압통…)」)을 남길지는 하나로 정해 문장으로 적는다. 사건 멤버에 부위 조각이 둘 이상이거나 다른 멤버에 부위 조각이 남으면 시술 축의 multi_site 처럼 **버리지 않고** dict 튜플에도 extra_sites 로 보존하고, 그 표현은 match_status=partial(또는 unlinked)로 adverse_tuple_assign 대상에 넣는다. §9.6 재실측.
2. **raw_name 튜플의 site/course 칸** (2-B′ · §1.5 L122). 이름 전체에서 하나라고 그 칸에 넣지 않는다 — 사건 조각마다 §1.5 경과·부위 규칙으로 분해한 결과(dict_tuples)만 event_fragments 옆에 두고, raw 튜플의 칸은 none/미상(식별자 RAW:anchor 만으로 고유). 3 튜플.
3. **표현은 단위를 만들지 않는다** (2-C′ · §1.5 L123 · §2.14/§2.15 의 「정체성을 만들지 않는다」와 한 문장으로). 미등록 조각이 있는 표현은 기존 튜플(65 이름 유래 + 미등록 0 표현 유래)에만 partial 로 연결하고, 닿는 튜플이 없으면 unlinked + 후보 (event, site, course) 를 표현 레코드에 기록 → adverse_tuple_assign 의 재료. 미등록 0 인 표현이 세우는 튜플(17)은 유지해도 정의와 충돌하지 않는다 — 유지한다면 「표현이 만든 튜플」을 §2.14 origins 로 구분할 것. §9.6.3·§9.6.4 재실측.
4. **문구·출처 세 줄** (3-A′ · 3-B′ · 3-C′). §5.2 adverse_tuple_assign 대상 = 「표현 레코드 전부(linked 포함)」 · §2.4 catalog_item 식별자의 계열 코드 = taxonomy 트리 위치(원장) 고정, reclassification 은 R2 만 바꾼다 · §2.5 site_id 출처 = what_id 와 같은 이름·참조 키 19(json `procedure.site_id.sources`).

### 동결 후 결정 레코드로 처리할 것

- 1-C 「보톡스」 PRD ↔ MOD — canonical_mapping
- 1-D 엑셀V+ 의 what — tuple_assign
- 1-E 같은 세 칸·다른 anchor 21 조(보톡스@M1/무힌트 · 스킨부스터 힌트 5 · 스컬트라 CAT/REF · 볼뉴머 M4/M9 …) — fold_approve(anchors) 또는 conflict_close(not_same)
- 2-C 사건 동의어 과민반응·동상·지방괴사·섬유화·공기색전 — event_split
- 2-D 부작용 none·미상을 식별자 값으로 둘지 — scope_review
- §9.6.2a 괄호 안 동의어가 만든 같은 사건의 미상 튜플(감각 이상 × 미상 등) · 수식어 없는 사건의 경과 — adverse_tuple_assign
- raw_name 18 의 (사건, 부위, 경과) 지정 · `주사`→주사 부위 — adverse_tuple_assign · dictionary_add
- partial·unlinked 표현 — adverse_tuple_assign(kind=expression) · dictionary_add
- 기법 상속 후보 9 계열(§9.5.6) — canonical_mapping
- ambiguous 3 · multi_* 미해결 · 미등록 조각 732/1,541 — tuple_assign(_multi) · dictionary_add
- 조합 기호 `/` 「함께」/「또는」 · R15 from 의 `site` 끝 — scope_review
- R30 인과 — edge_create
- ⑥ 32 · ⑦ 175 · ⑧ 2 · ⑨ 332 — conflict_override · conflict_close · dictionary_add
- DEC-20~24 승인 — status approved · decided_by · decided_at
- §12-3 step1 제품 확장 — dictionary_add 묶음
- (참고) `modality.same_session_order` 문구를 R18 끝 규칙에 맞추기 · canonical_mapping to_id 의 TEC-/DIC- 표기 통일 — 동결을 막지 않는 문구
