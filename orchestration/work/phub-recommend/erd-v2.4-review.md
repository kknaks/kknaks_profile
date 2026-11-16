# ERD v2.4 독립 검토 (4차 · 표적 · 동결 판정)

검토 2026-11-04 · 대상 `erd-v2.4.md`(2,896줄) · `erd-v2.4.json` · `erd-v2.4-tuples.json` · 이전 검토서 `erd-v2.3-review.md` ⑥ 의 구조 6건(2-A′ · 2-B′ · 2-C′ · 3-A′ · 3-B′ · 3-C′) · 원장 `complications.json` · `taxonomy.json`(3-B′ 트리 위치 확인). 범위는 6건과 그로 인해 바뀐 §1.1 · §1.5 · §2.4 · §2.5 · §2.14 · §2.15 · R29 · R31 · §5.2 · §9.6 · §11 · §12 뿐이다. 시술 축·결정 구조는 3차 검토 판정을 그대로 두고 다시 보지 않았다. 작성 과정 문서(v1*·v2.0~2.3 본문·발주서·step*·silver-*·DATA-001·_archive)는 열지 않았다. 실측 대조는 tuples.json 의 레코드(spans · candidates · tuples · extra_*)를 원장 이름·표현 원문과 내가 다시 멤버로 갈라 맞춰 봤다(검산 스크립트의 결론을 믿지 않고 재계산).

판단 기준은 정의 2(부작용 = 사건 × 부위 × 경과 · 원인 시술은 엣지 · 표현은 가리키기만)와 원칙 A~D 뿐이다. 미연결 수·사전 크기·후보 단위 수는 근거로 쓰지 않았다.

| 보는 것 | 결과 |
|---|---|
| ⓪ 6건 반영 | **6/6 고침** |
| ① §1.5 vs A~D | B·C·D 문자 그대로. **A 는 명시적 예외 1**(none·미상을 사전 값으로 센다 — 3차 검토가 2-D 결정으로 이관한 자리) |
| ② 실측 | 65 이름 전부 적합 · exact 651 전수 + 표본 30 세 칸 일치 · unlinked 가 만든 단위 0 · 위반 실례 **0** |
| ③ 작성자 읽기 | 「기존 단위 = 65 유래 dict 튜플만」 — **맞다** |
| ④ 3-B′·3-C′ | 실측·출처 표와 일치 (식별자 표기 1 참고) |
| ⑤ 추정 매칭 | **없다** |

어긋남 합계: **규칙 0 · 결정 3 · 참고(문구) 3**.

---

## ⓪ 3차 검토 ⑥ 「동결 전 꼭 고칠 것」 6건 반영 여부

| # | 지적 | v2.4 에서 고친 자리 | 실측 | 판정 |
|---|---|---|---|---|
| 2-A′ | 부작용 site 를 멤버 밖에서 상속·버림 | §1.5 L125 「부위 규칙(v2.4 수정 1)」 — 「사건이 놓인 멤버 안의 부위 조각만 · 멤버 밖(같은 묶음·바깥 묶음·이름 전체)에서 가져오지 않는다 — v2.3 순서는 없앴다」 · 부위 조각만인 멤버가 **바로 앞**이면 한 멤버 · 후보 둘이면 부위마다 튜플 · 붙지 않은 조각은 extra_sites·extra_courses 보존 · §2.14 site_ref_id 같은 문장 · R31 · json `site_rule` = `tuple_rules.adverse.site` · tuples.json `site_member_only:true` | 이름·표현 2,807+65 의 튜플·후보 전부를 내가 다시 멤버로 갈라 대조: 사건 멤버 밖에서 온 site **0**(이마/눈가 합치기 1 건은 규칙이 명시한 모양) · 「두통 × 주사 부위」 튜플·후보 0 · 「이마/눈가 당김감」→ (당김감, 이마)+(당김감, 눈가) 둘 · 「혈관 폐색(미간·코)」류 223 문자열 extra_* 보존 · dict 튜플 39 전부 extra_* [] | **고침** |
| 2-B′ | raw_name 칸의 이름 전체 상속 | §1.5 L127 「raw_name 튜플(v2.4 수정 2)」 — 「course·site 를 주지 않는다 — site=none · course=미상 · v2.3 의 ‘닿은 조각이 하나씩일 때만 그 칸’ 삭제」 · 식별자 `RAW:<anchor>|none|미상|<anchor>`(§1.1 L28 · §1.5 식별자 · json `id_rule.adverse_effect`) · raw 조건에 「붙지 않은 조각 ≥1」 추가 · dict_tuples·extra_* 는 보존만 | raw 18: site none 18/18 · course 미상 18/18 · 3차가 꼽은 셋(육아종/지연성 결절 [M2] · LOP [M14] · 가역적 [M16])의 raw 칸 전부 미상, 사전 분해는 dict_tuples 에 (결절, 지연)·(통증, 지연)·extra_courses [일시] 로 남음 · 주사 부위 반응 [M3]·[M16] site none, extra_sites [주사 부위] | **고침** |
| 2-C′ | 표현이 조각을 버린 채 단위를 세움 | §1.5 L128 「표현(v2.4 수정 3)」 — 「기존 단위 = complications 65 이름에서 생긴 사전 튜플(dict)뿐 · 미등록 0 · 붙지 않은 조각 0 · 후보 전부 세 칸 완전 일치일 때만 R29(exact) · 아니면 unlinked + candidates · 표현에서 새 단위를 만들지 않는다 — raw_name 도 사전 튜플도」 · §2.14 정의·origins(「튜플을 만든 원천 = complications 뿐」) · §2.15 match_status enum(exact\|unlinked)·candidates·unlinked_reasons · R29 attrs match_status enum(exact) · json `expression_rule` · tuples.json `expressions_create_units:false` | 튜플 57 = 65 유래 전부(origins 에 complications 없는 튜플 0) · exact 651 전부 미등록 0·extra 0·후보 전부 exists·unit 세 칸 = 후보 세 칸 · unlinked 2,156 에 tuple_ids 0 · 비-exact 표현을 출처로 가진 튜플 0 · unlinked 후보 would_be_id 가 튜플 목록에 있는 것 = exists=true 인 895 뿐(exists=false 422 는 튜플 없음) · 3차 실례(색전×미간 · 건조×입술 · 두통×주사 부위 · 혈관 폐색×none×지연) 전부 튜플 0 | **고침** |
| 3-A′ | adverse_tuple_assign 대상 = 표현 전부 | §5.2 L1141 「대상 = raw_name 튜플 전부 · 표현 레코드 전부(exact 포함 — linked 인데 틀리거나 조각을 잃은 표현도)」 · §2.15 match_status 규칙 「exact 포함 — 표현 레코드 전부가 대상」 · json `decision_kinds[adverse_tuple_assign].note` 같은 문장 · target 구조체(locator · kind=raw_name\|expression) 그대로 | 문구 확인. 아래 ② 의 「같은 사건 후보 둘」 exact 10 건이 바로 이 대상이다 | **고침** |
| 3-B′ | CAT- 계열 코드 = taxonomy 트리 위치 고정 | §1.1 L28 · §1.4 L93~94 · §2.3 정의 · §2.4 정의·식별자 · §5.2 target 규칙·reclassification 비고 · §9.4 L1599 · json `cat_family_rule`·`id_rule.catalog_item`·`tuple_rules.procedure.cat_family` — 「원장 modality[].id · reclassification 적용 전 · reclassification 은 R2 만 바꾸고 CAT- 를 바꾸지 않는다」 | 원장 taxonomy.json 대조: 소프라노 티타늄 = M9-2-4 (reclassified_to=M8) → tuples.json family M9 · CAT-bd1d93db49 = sha256(norm(`M9\|소프라노 티타늄`)) 재계산 일치 · 볼뉴머 M4(auto-M4-…)·M9(M9-2-3) → CAT-8e550f4613 / CAT-102bed4c6f 각각 재계산 일치 | **고침** (표기 참고 1 — ④) |
| 3-C′ | site_id 출처 | §2.5 site_id 행 출처 = what_id 와 같은 키 19 · json `procedure.attrs[site_id].sources` 19 = `what_id.sources`(동일 비교 True) · §2.14 site_ref_kind·site_ref_id 출처 = `complications.json:categories[].complications[].name` · json 동일 · §11 「column-map 비고 19」 | json 실측 | **고침** |

3차의 「확인」 항목(R15 from 의 `site` 끝)과 「결정으로」 6건은 v2.4 범위 밖이며 §12 에 자리만 있다 — 그대로.

---

## ① §1.5 규칙 문장 vs 원칙 A~D

§1.5 첫 줄(L120)과 json `principles`·tuples.json `principles` 에 발주서 문장 A~D 가 글자 그대로 있다(검산 L-8). 문제는 규칙 본문이 그 네 문장을 **우회 없이** 구현하는가다.

| 원칙 | 규칙 문장(§1.5) | 문자 그대로인가 | 예외·우회 |
|---|---|---|---|
| A 미상 칸이 하나라도 있으면 접지 않는다 | 접힘 조건(L126): 「세 칸 전부 사전 값일 때만 … **site none · course 미상은 v2 그대로 축의 정의값이라 사전 값으로 센다**(2-D 는 §12)」 · 「미등록 조각이 하나라도 있으면 접지 않는다 · 사건에 붙지 않은 조각이 남아도 접지 않는다」 | **아니다 — 명시적 예외 1.** 「미등록·붙지 않은 조각」에는 A 를 그대로 적용하지만, 칸 값 none·미상은 「미상」으로 세지 않는다. 실측: 접힌 튜플 11 전부 site none · 9 는 course 미상 · 2 는 (홍반/감각 이상, none, 일시). A 를 글자 그대로 적용하면(none·미상 = 미상 칸) 65 이름 중 부위·경과가 둘 다 적힌 이름이 0 이라 접힘은 **0** 이 되고, 표현 exact 651 도 0 이 된다(후보 세 칸이 none·미상을 포함) | 3차 검토가 2-D 「none·미상을 식별자 값으로 둘지」를 **동결 후 scope_review 결정**으로 이관했고 v2.4 는 그 처분을 그대로 따랐다(§12). 규칙 문장이 예외를 숨기지 않고 「정의값으로 센다」고 적어 두었다. 이번 범위(6건) 밖 — 다만 동결문에 이 예외가 A 의 예외임을 한 줄 명시해야 한다(⑥) |
| B 조각을 버리지 않는다 · 후보 둘이면 둘 또는 미해결 | 부위 규칙(L125): 「한 멤버에 부위 후보가 둘 이상이면 부위마다 튜플 · 경과도 같은 방식 · 사건에 붙지 않은 부위·경과 조각은 extra_sites·extra_courses 에 보존 · 그 문자열은 접지 않는다 — 이름이면 raw_name · 표현이면 unlinked」 · raw_name 규칙(L127): 「미등록 조각이 하나라도 있거나 붙지 않은 조각이 남으면 raw_name」 · 표현 규칙(L128): 「candidates — 후보 전부」 | **그렇다** | 없음. 괄호 안 부위 나열(「혈관 폐색(미간·코)」)은 「둘로 나눈다」가 아니라 「미해결(extra_sites · raw/unlinked)」 쪽을 택했다 — B 가 허용한 두 길 중 하나 |
| C 수식어는 같은 멤버 안에서 바로 붙은 사건에만 | 경과 규칙(L124 · v2.3) 「같은 멤버 안의 수식어만 · 멤버 밖(같은 묶음·바깥 묶음·이름 전체)의 수식어는 가져오지 않는다」 · 부위 규칙(L125) 같은 문장 · 「부위 조각만으로 된 멤버가 같은 묶음에서 사건 멤버 **바로 앞**이면 한 멤버」 | **그렇다** | 「바로 앞 부위 나열 합치기」는 C 의 「같은 멤버」를 한 칸 넓히는 규칙이지만, 발주서 B 가 「이마/눈가 → 둘」로 바로 그 모양을 지시했고, 조건(사건·경과·미등록 0 · 같은 묶음 · 바로 앞)이 닫혀 있어 추정이 아니다. 실측 1 건(이마/눈가 당김감)뿐. 한 멤버에 사건이 둘이고 수식어가 하나인 경우(「transient stinging and erythema」 — and 는 분리자가 아님) 규칙은 둘 다에 준다 — C 문장의 「같은 멤버 안」과 같고, 실측 1 건·unlinked |
| D 표현은 가리키기만 · 새 단위를 만들지 않는다 | 표현 규칙(L128): 「기존 단위 = 65 유래 dict 튜플뿐 · 세 칸 완전 일치일 때만 R29(exact) · 아니면 unlinked + candidates · raw_name 도 사전 튜플도 만들지 않는다」 · §2.14 origins 「튜플을 만든 원천 = complications 뿐」 · §5.2 「지정 튜플이 기존 단위에 없으면 지정이 단위를 세운다 — **결정으로만**」 | **그렇다** | 없음. 단위를 세우는 주체는 65 이름(기계)과 approved 결정(사람)뿐 |

규칙 문장 안의 추정·유사도 허용은 없다(⑤). **문구 참고**: 경과 규칙(L124)의 분리자 목록은 `· / , + 및 또는`(v2.3 문장 그대로), 부위 규칙(L125)·분해(L123)·json `split` 은 `· / , + 및 또는 — -- :` — 구현은 하나의 멤버 분할이라 결과는 같지만 두 문장이 다르다.

---

## ② 실측 대조

### ②-1 complications 65 이름 전부 → 튜플 (원장 `complications.json` 이름 · 내가 가른 멤버 · tuples.json 결과)

판정 열: 「부위를 버렸거나 잘못 붙인 것」「경과를 멤버 밖에서 끌어온 것」「미상인데 접힌 것(미등록·붙지 않은 조각이 있는데 접힌 것)」 세 가지를 봤다. 65 전부 **적합** — 위반 0.

| # | 원장 | 이름 | 멤버(내 분할) | kind | 튜플 칸 (· raw 는 사전 분해 보존) | 판정 |
|---|---|---|---|---|---|---|
| 1 | M1/0 | 주사 부위 통증 | 주사 부위 통증 | dict | (통증, 주사 부위, 미상) | 적합 |
| 2 | M1/1 | 멍 (타박상) | 멍 ∣ 타박상 | dict | (멍, none, 미상) | 적합 |
| 3 | M1/2 | 주사 부위 홍반·부종 | 주사 부위 홍반 ∣ 부종 | dict | (홍반, 주사 부위, 미상)+(부종, none, 미상) | 적합(C) — 부종은 다른 멤버라 none · 「주사 부위」를 줄지는 §12 결정 |
| 4 | M1/3 | 두통 | 두통 | dict | (두통, none, 미상) | 적합 |
| 5 | M1/4 | 항체 내성 (면역 저항) | 항체 내성 ∣ 면역 저항 | dict | (항체 내성, none, 미상) | 적합 |
| 6 | M1/5 | 독감 유사 증상 | 독감 유사 증상 | dict | (독감 유사 증상, none, 미상) | 적합 |
| 7 | M1/6 | 안면 비대칭 | 안면 비대칭 | dict | (비대칭, none, 미상) | 적합 |
| 8 | M2/0 | 멍 / 반상출혈 (Bruising / Ecchymosis) | 멍 ∣ 반상출혈 ∣ Bruising ∣ Ecchymosis | dict | (멍, none, 미상) | 적합 |
| 9 | M2/1 | 부종 / 종창 (Swelling / Edema) | 부종 ∣ 종창 ∣ Swelling ∣ Edema | dict | (부종, none, 미상) | 적합 |
| 10 | M2/2 | 주사 통증 / 불편감 (Injection Pain / Discomfort) | 주사 통증 ∣ 불편감 ∣ Injection Pain ∣ Discomfort | raw | (raw, none, 미상) · 분해 (통증, none, 미상) · 미등록 ['주사', 'Injection'] | 적합 |
| 11 | M2/3 | 홍반 (Erythema / Redness) | 홍반 ∣ Erythema ∣ Redness | dict | (홍반, none, 미상) | 적합 |
| 12 | M2/4 | 육아종 / 지연성 염증성 결절 (Granuloma / Delayed Inflammatory Nodule) | 육아종 ∣ 지연성 염증성 결절 ∣ Granuloma ∣ Delayed Inflammatory Nodule | raw | (raw, none, 미상) · 분해 (육아종, none, 미상)+(결절, none, 지연) · 미등록 ['염증성', 'Inflammatory'] | 적합 — (결절, 지연) 같은 멤버 · 미등록 → raw · 칸 none/미상 |
| 13 | M2/5 | 감염 (Infection, 기저 위험) | 감염 ∣ Infection ∣ 기저 위험 | raw | (raw, none, 미상) · 분해 (감염, none, 미상) · 미등록 ['기저', '위험'] | 적합 |
| 14 | M2/6 | 비대칭 (Asymmetry) | 비대칭 ∣ Asymmetry | dict | (비대칭, none, 미상) | 적합 |
| 15 | M3/0 | 결절 (Nodule) | 결절 ∣ Nodule | dict | (결절, none, 미상) | 적합 |
| 16 | M3/1 | 육아종 (Granuloma) | 육아종 ∣ Granuloma | dict | (육아종, none, 미상) | 적합 |
| 17 | M3/2 | 이물반응 (Foreign Body Reaction) | 이물반응 ∣ Foreign Body Reaction | dict | (이물반응, none, 미상) | 적합 |
| 18 | M3/3 | 혈관폐색/색전 (Vascular Occlusion/Embolism) | 혈관폐색 ∣ 색전 ∣ Vascular Occlusion ∣ Embolism | dict | (혈관 폐색, none, 미상)+(색전, none, 미상) | 적합 |
| 19 | M3/4 | 주사 부위 반응 (부종·압통·멍·홍반) | 주사 부위 반응 ∣ 부종 ∣ 압통 ∣ 멍 ∣ 홍반 | raw | (raw, none, 미상) · 분해 (부종, none, 미상)+(통증, none, 미상)+(멍, none, 미상)+(홍반, none, 미상) · extra_sites ['주사 부위'] · 미등록 ['반응'] | 적합(B·C) — 바깥 「주사 부위」는 괄호 안 사건에 안 붙음 · extra_sites 보존 · raw |
| 20 | M3/5 | 감염 및 바이오필름 (Infection / Biofilm) | 감염 ∣ 바이오필름 ∣ Infection ∣ Biofilm | dict | (감염, none, 미상)+(바이오필름, none, 미상) | 적합 |
| 21 | M7/0 | 실 노출 (Thread Exposure) | 실 노출 ∣ Thread Exposure | dict | (실 노출, none, 미상) | 적합 |
| 22 | M7/1 | 실 이동 (Thread Migration) | 실 이동 ∣ Thread Migration | dict | (실 이동, none, 미상) | 적합 |
| 23 | M7/2 | 감염 | 감염 | dict | (감염, none, 미상) | 적합 |
| 24 | M7/3 | 비대칭 | 비대칭 | dict | (비대칭, none, 미상) | 적합 |
| 25 | M7/4 | 구형구축 (Capsular Contracture-like Reaction / 섬유성 결절) | 구형구축 ∣ Capsular Contracture-like Reaction ∣ 섬유성 결절 | raw | (raw, none, 미상) · 분해 (구형구축, none, 미상)+(결절, none, 미상) · 미등록 ['Capsular', 'Contracture-like', 'Reaction', '섬유성'] | 적합 |
| 26 | M7/5 | 피부 딤플링/주름짐 (Skin Dimpling/Puckering) | 피부 딤플링 ∣ 주름짐 ∣ Skin Dimpling ∣ Puckering | raw | (raw, none, 미상) · 분해 (딤플링, none, 미상) · 미등록 ['Skin'] | 적합 |
| 27 | M7/6 | 통증·당김감 (Pain / Tightness) | 통증 ∣ 당김감 ∣ Pain ∣ Tightness | dict | (통증, none, 미상)+(당김감, none, 미상) | 적합 |
| 28 | M7/7 | 부종·멍(혈종) (Edema / Bruising / Hematoma) | 부종 ∣ 멍 ∣ 혈종 ∣ Edema ∣ Bruising ∣ Hematoma | dict | (부종, none, 미상)+(멍, none, 미상)+(혈종, none, 미상) | 적합 |
| 29 | M8/0 | PIH (시술 후 과색소침착) | PIH ∣ 시술 후 과색소침착 | raw | (raw, none, 미상) · 분해 (색소침착, none, 미상) · 미등록 ['시술', '후'] | 적합 |
| 30 | M8/1 | 홍반 (Erythema) | 홍반 ∣ Erythema | dict | (홍반, none, 미상) | 적합 |
| 31 | M8/2 | 부종 (Edema) | 부종 ∣ Edema | dict | (부종, none, 미상) | 적합 |
| 32 | M9/0 | 화상 (수포 포함) | 화상 ∣ 수포 포함 | raw | (raw, none, 미상) · 분해 (화상, none, 미상)+(수포, none, 미상) · 미등록 ['포함'] | 적합 |
| 33 | M9/1 | 홍반 (시술 직후 빨개짐) | 홍반 ∣ 시술 직후 빨개짐 | raw | (raw, none, 미상) · 분해 (홍반, none, 미상) · 미등록 ['시술', '직후'] | 적합 |
| 34 | M9/2 | 부종 (붓기) | 부종 ∣ 붓기 | dict | (부종, none, 미상) | 적합 |
| 35 | M9/3 | 통증·열감 (시술 중/후) | 통증 ∣ 열감 ∣ 시술 중 ∣ 후 | raw | (raw, none, 미상) · 분해 (통증, none, 미상)+(열감, none, 미상) · 미등록 ['시술', '중', '후'] | 적합 |
| 36 | M9/4 | 일시적 감각이상 (따끔거림·저림·감각둔화) | 일시적 감각이상 ∣ 따끔거림 ∣ 저림 ∣ 감각둔화 | dict | (감각 이상, none, 일시)+(감각 이상, none, 미상) | 적합(C) — 괄호 안 동의어가 (감각 이상, 미상)을 따로 냄 · 미상 튜플 처분은 §12 결정 |
| 37 | M9/5 | 색소침착 (염증후 과색소침착, PIH) | 색소침착 ∣ 염증후 과색소침착 ∣ PIH | raw | (raw, none, 미상) · 분해 (색소침착, none, 미상) · 미등록 ['염증후'] | 적합 |
| 38 | M11/0 | 반흔 (Scarring) | 반흔 ∣ Scarring | dict | (반흔, none, 미상) | 적합 |
| 39 | M11/1 | PIH (시술 후 과색소침착) | PIH ∣ 시술 후 과색소침착 | raw | (raw, none, 미상) · 분해 (색소침착, none, 미상) · 미등록 ['시술', '후'] | 적합 |
| 40 | M11/2 | 감염 | 감염 | dict | (감염, none, 미상) | 적합 |
| 41 | M11/3 | 화상 (열손상, Thermal Burn) | 화상 ∣ 열손상 ∣ Thermal Burn | dict | (화상, none, 미상) | 적합 |
| 42 | M11/4 | 일시적 홍반·부종 (Transient Erythema/Edema) | 일시적 홍반 ∣ 부종 ∣ Transient Erythema ∣ Edema | dict | (홍반, none, 일시)+(부종, none, 미상) | 적합(C) — 부종은 다른 멤버 → 미상 |
| 43 | M14/0 | PAH (역설적 지방 증식, Paradoxical Adipose Hyperplasia) | PAH ∣ 역설적 지방 증식 ∣ Paradoxical Adipose Hyperplasia | dict | (PAH, none, 미상) | 적합 |
| 44 | M14/1 | 피부 괴사 (Skin Necrosis / 동상·지방괴사, Frostbite·Fat Necrosis) | 피부 괴사 ∣ Skin Necrosis ∣ 동상 ∣ 지방괴사 ∣ Frostbite ∣ Fat Necrosis | dict | (괴사, none, 미상) | 적합 |
| 45 | M14/2 | 일시적 감각저하·저림 (Transient Hypoesthesia / Paresthesia) | 일시적 감각저하 ∣ 저림 ∣ Transient Hypoesthesia ∣ Paresthesia | dict | (감각 이상, none, 일시)+(감각 이상, none, 미상) | 적합(C) — #36 과 같은 모양 · §12 결정 |
| 46 | M14/3 | 일시적 홍반·부종 (Erythema / Edema) | 일시적 홍반 ∣ 부종 ∣ Erythema ∣ Edema | dict | (홍반, none, 일시)+(부종, none, 미상)+(홍반, none, 미상) | 적합(C) — 괄호 안 Erythema 가 (홍반, 미상) · §12 결정 |
| 47 | M14/4 | 멍·타박상 (Bruising) | 멍 ∣ 타박상 ∣ Bruising | dict | (멍, none, 미상) | 적합 |
| 48 | M14/5 | 통증·불편감 및 지연성 통증 (Procedural Pain & Late-Onset Pain, LOP) | 통증 ∣ 불편감 ∣ 지연성 통증 ∣ Procedural Pain & Late-Onset Pain ∣ LOP | raw | (raw, none, 미상) · 분해 (통증, none, 미상)+(통증, none, 지연) · extra_courses ['지연'] · 미등록 ['Procedural', '&'] | 적합(B·C) — raw 칸 미상 · (통증, 지연) 분해 보존 · 「LOP」 단독 멤버의 지연은 extra_courses |
| 49 | M14/6 | 염증후 색소침착 (Post-inflammatory Hyperpigmentation, PIH) | 염증후 색소침착 ∣ Post-inflammatory Hyperpigmentation ∣ PIH | dict | (색소침착, none, 미상) | 적합 |
| 50 | M15/0 | 일시적 홍반 (Transient erythema) | 일시적 홍반 ∣ Transient erythema | dict | (홍반, none, 일시) | 적합 |
| 51 | M15/1 | 자극감·작열감 (Stinging/burning) | 자극감 ∣ 작열감 ∣ Stinging ∣ burning | dict | (자극감, none, 미상)+(작열감, none, 미상) | 적합 |
| 52 | M15/2 | 건조·낙설(각질 박리) (Dryness/desquamation) | 건조 ∣ 낙설 ∣ 각질 박리 ∣ Dryness ∣ desquamation | dict | (건조, none, 미상)+(낙설, none, 미상) | 적합 |
| 53 | M15/3 | 소양감 (Pruritus) | 소양감 ∣ Pruritus | dict | (소양감, none, 미상) | 적합 |
| 54 | M16/0 | 부종·종창 | 부종 ∣ 종창 | dict | (부종, none, 미상) | 적합 |
| 55 | M16/1 | 통증·압통 | 통증 ∣ 압통 | dict | (통증, none, 미상) | 적합 |
| 56 | M16/2 | 멍·혈종 | 멍 ∣ 혈종 | dict | (멍, none, 미상)+(혈종, none, 미상) | 적합 |
| 57 | M16/3 | 감각이상·저림 (표재 감각신경, 가역적) | 감각이상 ∣ 저림 ∣ 표재 감각신경 ∣ 가역적 | raw | (raw, none, 미상) · 분해 (감각 이상, none, 미상) · extra_courses ['일시'] · 미등록 ['표재', '감각신경'] | 적합(B·C) — 「가역적」 단독 멤버 → extra_courses · raw |
| 58 | M16/4 | 경결·딱딱함(일시적 섬유화) | 경결 ∣ 딱딱함 ∣ 일시적 섬유화 | dict | (경결, none, 미상)+(경결, none, 일시) | 적합(C) — 섬유화 = 경결 동의어라 (경결, 일시) 둘째 튜플 · §12 결정 |
| 59 | M16/5 | 홍반·발적·가려움 | 홍반 ∣ 발적 ∣ 가려움 | dict | (홍반, none, 미상)+(소양감, none, 미상) | 적합 |
| 60 | M16/6 | 주사부위 반응 (통증·발적·멍·경결) | 주사부위 반응 ∣ 통증 ∣ 발적 ∣ 멍 ∣ 경결 | raw | (raw, none, 미상) · 분해 (통증, none, 미상)+(홍반, none, 미상)+(멍, none, 미상)+(경결, none, 미상) · extra_sites ['주사 부위'] · 미등록 ['반응'] | 적합(B·C) — #19 와 같은 모양 |
| 61 | M16/7 | 혈관미주신경성 반응·실신 (vasovagal) | 혈관미주신경성 반응 ∣ 실신 ∣ vasovagal | dict | (실신, none, 미상) | 적합 |
| 62 | M16/8 | 정맥염·혈관외유출(extravasation) | 정맥염 ∣ 혈관외유출 ∣ extravasation | dict | (정맥염, none, 미상)+(혈관외유출, none, 미상) | 적합 |
| 63 | M16/9 | 아나필락시스·즉시형 과민반응 (일반 baseline) | 아나필락시스 ∣ 즉시형 과민반응 ∣ 일반 baseline | raw | (raw, none, 미상) · 분해 (아나필락시스, none, 미상) · 미등록 ['일반', 'baseline'] | 적합 |
| 64 | M16/10 | 공기색전·카테터 관련 감염 | 공기색전 ∣ 카테터 관련 감염 | raw | (raw, none, 미상) · 분해 (색전, none, 미상)+(감염, none, 미상) · 미등록 ['카테터', '관련'] | 적합 |
| 65 | M16/11 | 수분·전해질 과부하 (심부전·신부전) | 수분 ∣ 전해질 과부하 ∣ 심부전 ∣ 신부전 | raw | (raw, none, 미상) · 분해 (전해질 과부하, none, 미상) · 미등록 ['수분', '심부전', '신부전'] | 적합 |

세 가지 점검의 결과:
- 부위를 버린 것 **0** — 부위 조각이 사건 멤버 밖에 있는 이름 2(#19 · #60)는 extra_sites 에 보존되고 raw 로 가 접히지 않는다. 부위를 잘못 붙인 것 **0** — site 가 들어간 dict 튜플은 #1 (통증, 주사 부위) · #3 (홍반, 주사 부위) 둘뿐이고 둘 다 같은 멤버.
- 경과를 멤버 밖에서 끌어온 것 **0** — course≠미상 인 dict 튜플은 #36·#42·#45·#46·#50 의 (·, 일시)와 #58 (경결, 일시) 뿐, 전부 수식어와 같은 멤버. raw 의 사전 분해 (결절, 지연)·(통증, 지연)도 같은 멤버이고 튜플 칸에는 들어가지 않는다. #48 의 「LOP」·#57 의 「가역적」(단독 멤버)은 extra_courses.
- 미상인데 접힌 것 **0** — 접힌 튜플 11 에 들어간 이름 전부 미등록 0 · extra 0(dict). raw 18 은 이름 하나씩. (none·미상 칸은 ① A 의 예외.)

### ②-2 exact 651 전수 + 표본 30

전수(스크립트): exact 651 전부 — 미등록 조각 0 · extra_sites/extra_courses 0 · candidates ≥1 · 후보마다 exists=true 이고 unit_id 가 dict 튜플 39 안 · unit 의 (event, site, course) = 후보 세 칸 · tuple_ids = 후보 unit 집합 · 사건 span 집합 = 후보 사건 집합(사건 조각 누락 0) · 후보 site 가 사건과 같은 멤버(site_basis=member 65 전부 「주사 부위」) · course≠미상 후보 82(홍반×일시 73 · 감각 이상×일시 7 · 경결×일시 2) 전부 같은 멤버. **위반 0.**

표본 30(seed 24 · 전수에서 무작위):

| # | 출처 | 원문 | 멤버 | 후보 = 연결된 단위 | 세 칸 |
|---|---|---|---|---|---|
| 1 | tax.item.common[]@M8/121 | 부종 | 부종 | (부종, none, 미상) | 일치 |
| 2 | tax.item.common[]@M16/65 | 부종 | 부종 | (부종, none, 미상) | 일치 |
| 3 | tax.item.common[]@M3/70 | 멍 | 멍 | (멍, none, 미상) | 일치 |
| 4 | tax.item.common[]@M4/26 | 발적 | 발적 | (홍반, none, 미상) | 일치 |
| 5 | tax.item.common[]@M3/41 | 주사 부위 압통 | 주사 부위 압통 | (통증, 주사 부위, 미상) | 일치 |
| 6 | tax.prod.common[]@M3/9 | 부종 | 부종 | (부종, none, 미상) | 일치 |
| 7 | tax.item.common[]@M3/43 | 부종 | 부종 | (부종, none, 미상) | 일치 |
| 8 | tax.prod.common[]@M1/12 | 두통 | 두통 | (두통, none, 미상) | 일치 |
| 9 | tax.item.serious[]@M3/7 | 감염 | 감염 | (감염, none, 미상) | 일치 |
| 10 | tax.mod.common[]@M7/2 | 멍 | 멍 | (멍, none, 미상) | 일치 |
| 11 | ext.common[]@M13/1 | 일시적 홍반 (빨개짐) | 일시적 홍반 ∣ 빨개짐 | (홍반, none, 일시) + (홍반, none, 미상) | 일치 |
| 12 | tax.item.common[]@M9/43 | 부종 | 부종 | (부종, none, 미상) | 일치 |
| 13 | tax.prod.common[]@M9/26 | 부종 | 부종 | (부종, none, 미상) | 일치 |
| 14 | tax.prod.serious[]@M17/4 | 혈종 | 혈종 | (혈종, none, 미상) | 일치 |
| 15 | tax.item.common[]@M2/9 | 주입부위 압통 | 주입부위 압통 | (통증, 주사 부위, 미상) | 일치 |
| 16 | ext.common[]@M4/3 | 멍 | 멍 | (멍, none, 미상) | 일치 |
| 17 | tax.item.common[]@M15/119 | 홍반 | 홍반 | (홍반, none, 미상) | 일치 |
| 18 | tax.item.common[]@M3/42 | 발적 | 발적 | (홍반, none, 미상) | 일치 |
| 19 | tax.prod.common[]@M11/6 | 홍반 | 홍반 | (홍반, none, 미상) | 일치 |
| 20 | tax.item.serious[]@M9/25 | 화상 | 화상 | (화상, none, 미상) | 일치 |
| 21 | tax.item.common[]@M7/38 | 부종 및 멍 | 부종 ∣ 멍 | (부종, none, 미상) + (멍, none, 미상) | 일치 |
| 22 | tax.item.common[]@M12/19 | 따끔거림 | 따끔거림 | (감각 이상, none, 미상) | 일치 |
| 23 | tax.prod.common[]@M1/1 | 두통 | 두통 | (두통, none, 미상) | 일치 |
| 24 | tax.item.common[]@M5/10 | 부종 | 부종 | (부종, none, 미상) | 일치 |
| 25 | tax.item.common[]@M16/143 | 압통 | 압통 | (통증, none, 미상) | 일치 |
| 26 | tax.item.common[]@M3/29 | 주사 부위 발적 | 주사 부위 발적 | (홍반, 주사 부위, 미상) | 일치 |
| 27 | tax.mod.common[]@M8/1 | 부종 (붓기) | 부종 ∣ 붓기 | (부종, none, 미상) | 일치 |
| 28 | tax.item.common[]@M7/46 | 당김감 | 당김감 | (당김감, none, 미상) | 일치 |
| 29 | tax.item.serious[]@M1/44 | 안면 비대칭 | 안면 비대칭 | (비대칭, none, 미상) | 일치 |
| 30 | tax.item.common[]@M15/228 | 자극감 | 자극감 | (자극감, none, 미상) | 일치 |

30/30 세 칸 완전 일치. 표본 #11 「일시적 홍반 (빨개짐)」은 후보 둘((홍반, none, 일시) + (홍반, none, 미상))로 단위 둘에 R29 가 붙는다 — 규칙(괄호 안 동의어 = 다른 멤버 = 수식어 없음 = 미상) 그대로이고 세 칸은 맞지만, 원문은 사건 하나를 말한다. 같은 모양이 exact 안에 **10**(일시적 홍반 (빨개짐) 4 · 주사 부위 홍반 (빨개짐) 4 · 주입 부위 통증 및 불편감 2). 이것이 3-A′ 가 「exact 도 대상」으로 연 자리다 — 결정(adverse_tuple_assign kind=expression).

### ②-3 unlinked 2,156 — 새 단위 흔적

- tuple_ids 가 있는 unlinked **0** · `linked` true **0**. 후보 1,317 중 exists=false 422 의 would_be_id 는 튜플 목록에 **없다**(ADV- 로 계산만 해 둔 값 · §1.1 「튜플이 아니다」). exists=true 895 는 전부 65 유래 dict 튜플을 가리키지만 표현에 미등록·붙지 않은 조각·no_unit 후보가 함께 있어 연결하지 않았다(「하나라도 아니면 연결하지 않는다」 그대로).
- 튜플 57 의 sources 에 들어간 표현 locator 는 전부 그 표현이 exact 이고 그 튜플이 그 표현의 tuple_ids 에 있는 것 — 비-exact 표현이 출처로 들어간 튜플 **0**.
- 표현 원문이 complications 이름과 정규화 완전 일치하는 것 129 — 전부 dict 이름이고 exact. raw_name 이름과 완전 일치하는 표현은 **0**(생기면 raw 지정 → 표현 지정 두 결정으로 닿는다 · 결정).

### ②-4 위반 실례

A~D 위반 실례 **0**. 세 칸은 맞지만 사람이 볼 것(결정): ②-2 의 「같은 사건 후보 둘」 exact 10 · #3 「주사 부위 홍반·부종」의 부종 site · #36/#45/#46/#58 괄호 안 동의어의 미상 튜플 — 전부 §12 에 자리가 있다.

---

## ③ 작성자 읽기 — 「기존 단위 = complications 65 이름에서 생긴 사전 튜플만」

**맞다.** 근거:
1. D 는 표현이 단위를 만들지 않는다고 했고, 정의 2 에서 단위의 원천은 complications 이름(사전 뼈대 + 튜플 ①)뿐이다. 65 이름 밖에서 단위가 생길 길은 approved 결정(adverse_tuple_assign 「지정이 단위를 세운다 — 결정으로만」)뿐이고, 그것은 표현이 아니라 사람이 세우는 것이라 D 와 어긋나지 않는다.
2. raw_name 튜플을 「기존 단위」에서 뺀 것도 맞다. raw 튜플은 세 칸이 (RAW, none, 미상)이라 표현의 후보 (event, site, course)와 「세 칸 완전 일치」가 성립할 수 없다. raw 의 dict_tuples 를 단위로 쓰면 그것이 곧 미등록 조각을 버린 단위 주장(2-B′·2-C′ 가 막은 것)이 된다. 표현 원문이 raw 이름과 완전 일치하는 경우는 지금 0 이고, 생겨도 raw 지정 뒤 표현 지정으로 닿는다(결정).
3. 반대 읽기(「표현이 세 칸 완전 분해되면 단위로 인정」)를 택하면 v2.3 의 complete 17 이 되살아나 「표현에서 새 단위를 만들지 않는다」와 정면으로 부딪친다. 그 17 은 후보 51 안에 candidates 로 보존돼 있어 버린 것이 아니다.

---

## ④ 3-B′ · 3-C′ 확인

**3-B′.** 원장 taxonomy.json 대조 — 소프라노 티타늄: `modality[M9].subcategories[M9-2].items[M9-2-4]` · `reclassified_to: M8` → tuples.json `family: M9` · `CAT-bd1d93db49`. 볼뉴머: M4(auto-M4-1775362490962) · M9(M9-2-3) → `CAT-8e550f4613` · `CAT-102bed4c6f`(다름). 세 id 모두 sha256(norm(`<트리 계열>|<이름>`))[:10] 으로 재계산해 일치. 검산 L-5 「521 전부 위반 0」은 같은 식이다. §1.4 L93 「family = 트리 위치 · CAT- 의 계열 코드와 같다」 · §5.2 reclassification 비고 「R2 만 바꾸고 CAT- 를 바꾸지 않는다」 · §12 1-E·1-G 「anchor(CAT-)로 가리킨다 · 트리 위치 고정」 — 서로 맞는다. **참고 1(문구)**: §1.1·§2.4·json 의 예시 「sha256(`M9|소프라노티타늄`)」은 글자 그대로 넣으면 CAT-6e93269caf 가 나온다. 실제 키는 canonical_key 전체에 norm_v1(casefold 포함)을 건 `m9|소프라노티타늄`(→ CAT-bd1d93db49). 식별자가 안정 키라 재현 식은 글자 그대로여야 한다 — 「sha256(norm_v1(계열 코드|항목 이름))」 한 줄.

**3-C′.** json `entities[procedure].attrs[site_id].sources` = 19 = `what_id.sources`(리스트 동일) = `technique_id.sources`; md §2.5 site_id 행 19 키. `entities[adverse_effect].attrs[site_ref_kind|site_ref_id|event|course].sources` = `complications.json:categories[].complications[].name` 하나 — 단위는 65 이름에서만 생기므로 맞다(표현 출처는 origins 에 「exact 로 가리킨 출처」로만 더해진다 · §2.14 origins 비고). 「(파생/ERD 정의)」가 남은 site 관련 행은 없다(검산 L-6). **참고 2(문구)**: §2.14 `site_basis enum(member|site_list)` — 실측에서 site_list 값은 0 이고 「이마/눈가 당김감」의 이마 후보도 `site_basis=member`(합친 뒤 한 멤버로 세었기 때문). 검산 L-1 의 「site_basis ∈ {member, site_list}」는 그래서 비어 있는 값까지 허용하는 식이다. 규칙 결과에는 영향 없음.

---

## ⑤ 추정·유사도 매칭 지점

| 어디 | 규칙 | 판정 |
|---|---|---|
| §1.1 L23·L33 · json `tuple_rules.adverse.no_similarity:true` | 유사도·추측 매칭 없음(⑦ 은 표시만) | 없음 |
| §1.5 L125 부위 | 멤버 안 조각만 · 바로 앞 부위 나열 합치기(조건 닫힘) | 결정론 — 추정 아님 |
| §1.5 L124 경과 | 멤버 안 수식어만 | 결정론 |
| §1.5 L127 raw | 칸 none/미상 · 분해는 보존만 | 채우지 않음 |
| §1.5 L128 표현 | 세 칸 완전 일치 + 미등록 0 + 붙지 않은 조각 0 + 후보 전부 exists | 완전 일치만 — 추정 아님 |
| §1.5 L126 접힘 | none·미상을 사전 값으로 셈 | 추정은 아니다(값을 지어내지 않음) — A 의 예외(①) |
| §1.5 분해 | 왼쪽부터 가장 긴 구간 · 사전 순서 relative_site → site → course → event | 결정론(탐욕) — 3차와 같이 허용 범위 |

3차 ⑤ 표의 부작용 축 추정 세 줄(L119·L122·L123)은 전부 사라졌다. 바뀐 규칙이 새로 연 추정·유사도 매칭은 **없다**.

---

## ⑥ 동결 판단

**동결 가능 — 6건 전부 §1.5·§2.14·§2.15·R29·§5.2·§2.4·§2.5 의 문장과 실측에서 닫혔고, 부작용 축 규칙은 B·C·D 를 문자 그대로 담으며 추정·버림·표현 유래 단위가 0 이다. 남는 어긋남은 A 의 명시적 예외(none·미상 = 사전 값 · 2-D)뿐이고 이것은 3차가 이미 동결 후 결정으로 이관한 항목이라 동결을 막지 않는다.**

### 동결 전 꼭 고칠 것 — 구조·규칙

없음.

(동결문에 한 줄 확인 — 「부작용 축의 site none · course 미상은 사전 값으로 센다(원칙 A 의 예외 · 2-D 는 동결 후 scope_review)」를 승인 문장에 적는다. 이 예외를 빼면 부작용 접힘 0 · exact 0 이 되므로, 사용자가 A 를 글자 그대로 원한다면 그것은 v2.5 규칙 개정이지 결정 레코드가 아니다.)

### 동결 후 결정으로 (이번 검토가 새로 꼽은 것 · 전부 §12 자리 있음)

1. exact 표현 중 같은 사건 후보 둘(「일시적 홍반 (빨개짐)」 4 · 「주사 부위 홍반 (빨개짐)」 4 · 「주입 부위 통증 및 불편감」 2 = 10) — R29 가 단위 둘에 붙는다. adverse_tuple_assign(kind=expression · 3-A′ 로 exact 도 대상).
2. 「주사 부위 홍반·부종」[M1] 의 부종 site(none → 주사 부위?) · 괄호 안 동의어가 만드는 같은 사건의 미상 튜플(#36 · #45 · #46 · #58) — adverse_tuple_assign(kind=raw_name 아님 · complications 이름 locator). §12 §9.6.2a·§9.6.2b 행.
3. raw_name 이름과 정규화 완전 일치하는 표현이 생길 때의 경로(raw 지정 → 표현 지정 두 결정) — 지금 0 건 · scope_review 메모만.

### 참고 — 동결을 막지 않는 문구 3

- CAT- 예시 식 「sha256(`M9|소프라노티타늄`)」 → 「sha256(norm_v1(`계열 코드|항목 이름`))」(실제 키는 casefold 된 `m9|…`). §1.1 L28 · §2.4 · §5.2 · json `cat_family_rule`·`id_rule.catalog_item`.
- `site_basis` enum 의 site_list 값은 실측 0(합친 멤버는 member 로 기록). 값을 지우거나 합치기 결과를 site_list 로 적거나 하나로.
- 경과 규칙(L124·§2.14 course·§4.2)의 분리자 목록 `· / , + 및 또는` 을 부위 규칙·분해 문장의 `· / , + 및 또는 — -- :` 와 같게.
