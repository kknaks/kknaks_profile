# ERD v3.2 독립 검토 — 동결 여부

검토 2026-11-05 · 대상 `erd-v3.2.md`(정본) · `erd-v3.2.json` · `erd-v3.2-dictionaries.json` · `erd-v3.2-tuples.json` · `erd-v3.2-seed-candidates.md/.json` · `erd-v3.2-column-map.md` · `ERD-FROZEN.md`(v3.1 절까지) · `erd-v3.2-brief.md` · 원장 브론즈 2판 `bronze/phub-ledger/` · `bronze-ledger-column-report.md`. 그 밖은 열지 않았다. 검산 `erd-v3.2-check.py` 를 읽었고(실행하지 않음) 실측은 tuples.json 을 직접 세어 원장과 대조했다.

기준은 발주서의 둘뿐이다 — ⓪ 사용자 정의 3 유지 · ① 11-05 새 원칙 (a)~(e) 가 구조로 들어갔는가. 어긋남은 **구조·규칙(S)** / **결정으로 처리 가능(D)** 으로 갈랐다.

---

## ⓪ 사용자 정의 유지

| 정의 | 판정 | 근거 |
|---|---|---|
| 1 시술 튜플 · 미상 접지 않음 · 조각 버리지 않음 · 엣지 끝 = 시술 | 유지 | §0 글자 그대로(검산 U). 실측 분류 항목 521 → 튜플 521 접힘 0 · 엣지 끝 3,574 전부 procedure/modality/subcategory/product/unresolved. 떼어낸 조사·어미는 grammar_tokens 로 보존(검산 O 「버림 0」 — 부작용 축 원장 문구 전수 재분해로 확인하는 검산이 실제로 있다) |
| 2 v3.1 개정판 — (사건, 부위, 물질) · 경과 R15 · 조합은 사전 값이면 어느 출처든 | 유지(글자) · **규칙 하나가 뜻을 깎는다 → S-1** | 단위 395 전부 event_kind=dict(원장 노드 포함) · 경과는 edges_with_course 435 로 엣지에만 · 식별자 ADV-sha(event|site|qualifier). 다만 「같은 세 칸은 어느 출처든 같은 단위」가 §0.2 핵심어 규칙 때문에 깨진다(①(b) 참조) |
| 3 원장 불변 · 충돌 레코드 · approved 만 · 안정 키 · 적용 순서 | 유지 | HASHES.txt 21 일치 · 결정 kind 20 그대로 · 적용 순서 ⓪①~⑦ 그대로. fold_approve 비고에 「원장 노드를 기존 사건 동의어로 접으면 단위 id 재계산 · 옛 id alias」가 들어가 안정 키 승계가 끊기지 않는다 |
| 명시 예외(부위 none · 물질 none 은 값) | 유지 | §0 그대로 · 단위 (부종, none, none) 에 「경미한 부종」「부종(5-7일)」 등 20 표면형이 접힘 |

---

## ① 새 원칙 (a)~(e) — 구현 위치와 어긋남

### (a) 문구 종류 먼저 분류 · 부작용 단위에는 부작용 문구만 · 다른 종류는 자기 테이블 + 참조

- **구현**: §0.1 표 5종(부작용 문구 / 시술 후 경과 / 동의서 / 시술 전 확인 / 메모·설명문·문헌) · json `rule_zero`·`phrase_kind_table`. 실측 §9.9: 단위를 세운 원천은 {complications 47, safety_phrase 377} 뿐(검산 O) · 타임라인 435 줄 · 응급 징후 52 · 고지 109 · 문헌 32 는 자기 테이블에서 adverse_ref 로 **이미 있는** 단위만 가리킴(참조 541 · 세운 단위 0 · 검산 O). 원장 대조: safety.* 자리 2,285 = extracted 143 + taxonomy 2,142(taxonomy items safety.contraindications 12 는 조건 축으로 빠짐 — 맞다) · 타임라인 줄 435 · 응급 징후 55 · 고지 109 · complications 65 — 전부 일치.
- **어긋남 S-3(문장 잔재)**: 본문·실측은 (a) 대로인데 **개체 정의 표가 옛 구조를 말한다.**
  - §2.14 `adverse_effect.origins` 의 「출처 원장 키」에 timeline normal/abnormal/caution/emergency · emergency_signs · literature statement/patient_ko 가 그대로 — 「이 단위를 만든 원천」 칸이 (a) 와 정면 충돌(실측 origins 는 complications·safety_phrase 뿐).
  - §2.14 `event` 타입 `dict|str(raw_name)` · `status` enum `complete|partial|unresolved`(partial/unresolved = raw_name) · `unregistered_fragments`/`event_fragments`/`extra_sites`/`extra_qualifiers` 규칙 칸 「raw_name 만」 · 식별자 줄 「raw_name 단위는 sha256(RAW:…)」 · §3.1 열거형 `adverse_effect.status` `adverse_effect.raw_reason` · `adverse_expression.kind/match_status/unlinked_reason`(개체는 v3.1 에서 삭제) · §5 `adverse_tuple_assign` target `kind: raw_name`(비고만 v3.2) · R15 규칙 「타임라인 normal 문구는 reaction_level=normal 로 표시」(v2 문장 · R15 에서 속성은 빠짐).
  - 검산은 실측(raw_name 0 · unlinked 없음)만 보고 정의 표는 보지 않는다. v3 때 R-1~R-4 로 닫은 것과 같은 종류.

### (b) 사건이 사전에 없으면 그 말로 새 노드 · 비슷한 건 ⑦ · 추정 매칭 0 · unlinked 없음 · 시술 축과 대칭

- **구현**: §0.2 노드 원칙 · json `node_rule` · 사전 adverse_event_type 파생 항목 335(origin=ledger · unreviewed · locators · contexts 전부) · ⑦ 157(규칙 근거만 · 점수 없음) · 부작용 문구 2,285 = exact 1,331 + new 915 + note 28 + sentence 11 · unlinked 0 · raw_name 0(검산 O 여섯 줄).
- **어긋남 S-1(규칙 틈 · 핵심)**: §0.2 는 핵심어를 **「사건 조각 + 미등록 토큰 + 대체 수식어, 원문 순서」로 멤버 통째**로 정하고, exact 는 「사전 밖 토큰 0」일 때만이다. 그래서 멤버에 사전 사건이 있어도 미등록 토큰이 하나만 섞이면 **사전 사건이 새 노드에 흡수**된다.
  - 실측: 원장 노드 335 중 **68 개(20%)** 가 사전 사건 정준값·동의어를 낱말로 품고 있다 — 「시술 후 일시적인 홍조와 부종」→ 단위 (홍조 부종, none, none) 하나 · 부종 단위 없음 · 경과 일시 소실 / 「지방흡입 부위의 일시적 통증과 멍」→ (지방흡입 부위 통증 멍) / 「이식 부위의 약간의 부종」→ (이식 부위 부종) / 「두피 통증」「국소 홍반」「두피 발적」「카테터 감염」「바이러스 감염」「이물 육아종」「비후성 반흔」「저온 화상」 …(전수는 tuples.json adverse.ledger_events 에서 사전 사건 낱말 포함으로 재현 가능).
  - 왜 구조인가: 사용자 문장은 「**사건이** 사전에 없으면」이다 — 부종·통증·홍반은 사전에 있다. 정의 2 「같은 세 칸은 어느 출처든 같은 단위」(부종 ≠ 홍조 부종) · 원칙 D 「기존 단위에 exact 로 붙거나」 · 시술 축 대칭(시술 축은 primary 가 닿으면 미등록 조각이 있어도 **그 what 을 유지**하고 anchor 튜플로 두지, 「항목 자신」으로 보내지 않는다)과 어긋난다. 결과로 R15 가 부종·통증 단위에 닿지 않고(상속 §9.15 에서 홍조·건조감·알레르기 반응 등 family 0/none 100% 인 이유의 일부), ⑦ contains 97 쌍의 대부분이 이 합성 노드 → 구성 사건 쌍이다(두피 통증→통증 · 이식 부위 부종→부종 · 들어가 괴사→괴사). phrase_map 68 건으로 하나씩 고칠 수는 있으나 규칙이 계속 만들어내므로 결정이 아니라 규칙이다.
  - 고칠 문장: 멤버 안 사전 사건 조각은 각각 exact 단위(부위·경과·물질은 원칙 C 그대로), **사건 조각이 0 인 멤버만** 핵심어 새 노드, 사건 옆의 미등록 토큰은 parsed.unregistered 로 보존(원칙 B). 이러면 335 → 약 267, ⑦ contains 대부분 소멸.
- **어긋남 S-2(규칙 범위)**: ⑦ 은 「새 노드 ↔ 기존 사전 값」만 돈다. 원장 노드끼리는 0 — 「안검하수」(19) ↔ 「눈꺼풀 처짐」(6 · 원장이 괄호로 병기한 같은 말) · 건조감↔건조증 · 색소이상↔색소침착이상↔색소 변화 · 알레르기↔알레르기 반응↔전신 알레르기 반응 · 실의 이동↔실이 밖으로 튀어나오는. 같은 규칙을 노드끼리 돌리면 323 쌍. (b) 「비슷한 건 ⑦ 로 사람에게」가 반쪽이고, 시술 축 ⑦(taxonomy 항목 이름 중복)과도 비대칭. §12 에 「다음 판 결정」으로 적혀 있으나 이것은 규칙 범위 한 줄이다.
- **어긋남 S-4(토큰화 목록 틈)**: V3.2-1 용언 어미 18 은 하다/되다 활용뿐이라 관형형(-는/-지는/-은/-ㄴ)·「~시」·「~하므로」가 핵심어에 남고, 어간이 원장 독립 토큰이 아니면 조사도 안 뗀다. 노드 예: 만져지는(2) · 어두워지는 · 눈이 건조해지는 · 표정 어색해지는 · 주름 덜 펴지는 · 윗눈꺼풀이나 눈썹이 처지는 · 실이 밖으로 튀어나오는 · 고름이 차는 감염 · 들어가 괴사 · 당기는 냉감 · 부은 · 뻣뻣한 · 지나면 · **거부반응이** · **TGF-beta1에** · 본인 혈액 사용하므로 알레르기 · 접촉시/응고시/사용시/주사시 X. 정규식으로 45 후보, 눈으로 명백한 것 약 22. 목록은 ERD §1.3 본문이므로 규칙(문장)이다 — 비용은 목록 몇 줄.
- 추정 매칭: 단위 사건 전부 사전 값 또는 원장 노드(검산 O) — 맞다. 유사도 점수 없음. ⑦ first_syllable(「둘 다 2자 이하 · 첫 음절 같음」)은 유사도의 대용이지만 후보만 내므로 (b) 안이다.
- unlinked 없음: 문구 사전 status ∈ {exact, new, note, sentence} · 타임라인 등은 ref/ref_partial/none/normal_memo — 맞다.
- 시술 축 대칭: 항목 자신 477 → 324 · 장비 승격 150 + 성분 3 = 153 ✓(151 등록 중 1 은 제외 합침). 대칭이 깨지는 지점은 S-1 뿐.

### (c) 씨앗은 원장 전체 · 부위 전수(바디) · 장비 = 제품 자동 · 성분 · 토큰화·변형은 목록 · 조각 보존

- **구현**: §1.7 · §4 `closed` · 씨앗 파일(site 42 · ingredient 28 · site_fragments 19 · procedure_term 514 · product_abbrev 42 · variant_pairs 176 · gloss 62) 전부 proposed · 적용 0(검산 B·O). 부위 닫힌 목록 42 = 발주서 V3.2-4 전부 + kind + parent(제안만 · 사전 parent 는 null) ✓ · 가슴·손·발은 원장에 없음으로 정직하게 표시. 장비 제품 151 origin=taxonomy · license_status=미확인 ✓(제외 25 건 사유 전부 적힘). 변형 쌍은 목록(applied=false) ✓. locator 는 11 파일에 걸쳐 있어 「특정 파일 아님」 ✓.
- 어긋남 없음. 결정 비고만: **D-5** 「빈도 ≥2 또는 locator ≥2」문턱이 extracted.json ↔ taxonomy modality[].extracted 복제(질문 2 · 같은 문장 두 자리)로 부풀어 있다 — 원장 노드 n=2 인 83 중 52 가 같은 문구의 복제 쌍이고, 씨앗 문턱도 같은 식으로 통과한다. 셈 단위(복제 쌍 = 1)를 정해야 승인 묶음의 「빈도 1」경계가 맞다. **D-10** 성분 문맥 추정(바로 옆 토큰)이 심부·동일·딥·별도·약한·얕은·자연스러운·주입·코그 를 proposed 로 올림(17 중 9) — ERD 가 「추정 · 승인」이라고 밝혔으므로 승인에서 거르면 된다.

### (d) R15 속성 3층 상속(단위 → 계열 → 항목 · basis · 참조)

- **구현**: §1.5·R15 `inheritance[]`(attr, basis, ref, ref_locator) · `layer` · 단위 `general_description`/`general_management` · 실측 §9.15 항목 엣지 2,177 · basis 없음 0 · 복사 0(검산 O 두 줄). 엣지 표본에서 family 참조가 complications 속성 locator 로 닿음 ✓.
- 어긋남 없음. 관찰: 8 속성 전부 item basis 0(항목 고유 값은 frequency_class·parsed 뿐이라 설계대로) · family 936 / none 1,241 — none 이 많은 이유 절반은 S-1(홍조·건조감·알레르기 반응·신경 손상이 계열 표 행에 닿을 길이 없음)이고 나머지는 complications 표가 65 행뿐이기 때문.

### (e) 타임라인은 자기 개체(시술축 → 시기 → 줄) · 부작용은 줄이 참조

- **구현**: §2.21 post_procedure_timeline(TML- · phases · lines) · R33 has_timeline(끝 procedure 4 · modality 6) · R34 timeline_refers 364 · 응급 징후 §2.22 + R35 65 · R15 는 timeline_refs/emergency_sign_refs 로 참조 · R15 의 period/phase_label/reaction_level 속성 제거(검산 O). 행선지 이동 18 = 타임라인 9 + 응급 1 + 문헌 8 ✓.
- 어긋남 없음. 정상 줄 처리는 ②(ⅳ).

---

## ② 실측 대조 (ⅰ)~(ⅳ)

### (ⅰ) 새 노드 335 중 사건이 아닌 것 — 원인별

| 부류 | 수(노드) | 예 | 성격 |
|---|---|---|---|
| β 사전 사건을 품은 합성 노드 | **68** | 홍조 부종 · 두피 통증 · 이식 부위 부종 · 국소 홍반 · 카테터 감염 · 비후성 반흔 · 염증성 결절 | **규칙 틈(S-1)** — 사용자 (b) 와 정의 2 위반 |
| α 용언·조사 잔재 | ~22(후보 45) | 만져지는 · 들어가 괴사 · 눈이 건조해지는 · 거부반응이 · TGF-beta1에 · 접촉시 화학화상 | **규칙 목록 틈(S-4)** |
| γ 설명·수치 조각 | ~12 | CO2 · 대비 수준 · 제품 최저 수준 · 색소침착 낮음 · 합병증 · 최소 · 반드시 사전 고지 · 세포 배양 불순물 · 마늘 냄새 입냄새 | 결정(**D-4** phrase_map units [] 또는 note_words 추가) — 소수 |
| δ 수식어 목록 밖 수식 | ~12 | 최소 부종 · 미약한 부종 · 연장된/지속적인 부종 · 임시적 색소침착 · 장기간 홍조 · 중등도 박리 · 활성 감염 부위 · 묘한 따끔거림 | 결정(**D-3** adverse_stopword 규칙 데이터) — S-1 이 닫히면 절반은 자연 해소 |
| ε 조직층 분리로 빈 핵심어 | 37 단위(노드 ~10) | (막힘, 혈관) (손상, 혈관) (약화, 근육) (이완, 근육) (마비, 근육) (합병증, 혈관) (자극, 피부) (수축감, 근육) | 정의 2 대로 분리된 결과. 「혈관 폐색」은 사전 통째 값이라 안 갈리고 「혈관 손상」은 갈린다 — 결정(**D-2** dictionary_add 통째 값 또는 fold) |

좋은 노드(홍조 90 · 알레르기 반응 45 · 건조감 42 · 신경 손상 37 · 딱지 23 · 흉터 23 · 경결감 22 · 안검하수 19 · 따가움 16 · 실명 15 · 근력 약화 14 · 연하곤란 · 하악변연신경 손상 · 호흡곤란 · 물집 · 가피 · 광과민성 · 접촉성 피부염 …)는 발주서가 「사전에 없던 진짜 사건」으로 꼽은 것을 전부 덮는다. 어색한 것은 거의 n≤2 이고, 그 n=2 의 다수가 D-5 복제 쌍이다. 결론: **어색함의 주원인은 규칙 틈(S-1·S-4) 둘**이고 소수 예외(γ·δ·ε)는 결정이다.

### (ⅱ) ⑦ 후보 규칙이 너무 넓은가 — 157 쌍

| 규칙 | 쌍 | 눈으로 「같은 것 아님」 | 예 |
|---|---|---|---|
| contains/contained | 108 | 대부분은 「합성 ⊃ 구성 사건」(S-1 산물) · 같은 것은 건조감↔건조 · 경결감↔경결 · 수포형성↔수포 · 결절형성↔결절 · 반흔형성↔반흔 정도 | 두피 통증→통증 · 들어가 괴사→괴사 · 각질→낙설(각질박리) · 출혈→멍(반상출혈) · 손상→화상(열손상) |
| prefix2/3 | 35 | **~22** | 색소탈실→색소침착(반대) · 색소 변화→색소침착 · 염증 반응→색소침착(염증후색소침착) · 혈관염→실신(혈관미주신경성반응)·혈관 폐색·혈관외유출 · 피부건조/피부화상/피부위축/피부색소침착→괴사·딤플링(피부괴사·피부딤플링) · 바이러스 감염→바이오필름 · 안면신경 손상→비대칭 |
| first_syllable | 14 | **~9** | 실명↔실신 · 감기↔감염 · 경련↔경결 · 결막↔결절 · 수분↔수포 · 실밥↔실신 · 실의↔실신 · 경직↔경결 / 홍조↔홍반·부은↔부종·건성↔건조는 볼 만함 |
| suffix_감 | 7 | 0 | 건조감↔건조 · 통증감↔통증 · 화상감↔화상 |

판정: 넓다. prefix2·first_syllable 은 잡음이 신호보다 많다(~31/49). 그러나 ⑦ 은 후보만 내고 접기는 fold_approve · 닫기는 conflict_close 라 **결정으로 처리 가능(D-1)** — 단 「단계 끝 = open 0」 규칙상 157(+장비 ⑦ 13) 건을 전부 닫는 결정 묶음이 빌드 전에 필요하다. S-1 을 닫으면 contains 97 의 대부분이 사라져 남는 ⑦ 은 ~60 이다. 규칙 데이터(dup_rules 에서 prefix2 를 prefix3 로, first_syllable 삭제)를 좁히는 것은 선택.

### (ⅲ) 접으면 안 되는 것이 접혔는가

- exact 1,331 자리 · 항목 174 를 봤다. 접힘은 사전 동의어·수식어 제거·괄호 설명 보존(parsed.explanation) 안에서만 일어난다 — 「색소침착 (박피나 레이저 시술에 비해 위험이 매우 작음)」→ 색소침착 + explanation[박피, 레이저, 작음] · 「압통 (누르면 아픈 느낌)」→ 통증(압통은 v2.4 사전 동의어) · 「붓기 (2-4주)」→ 부종 + 기간 조각. **잘못 접힌 것 0**.
- 반대 방향이 문제다(S-1): 접혀야 할 「시술 후 일시적인 홍조와 부종」의 부종, 「두피 통증」의 통증이 **접히지 않고** 새 노드로 갔다. 접힘 과잉이 아니라 접힘 부족.
- 부위 칸: 멤버 밖 부위 0 · site_basis member/site_list 만(v2.4 검산 승계). 단위 (부종, 눈가)·(비대칭, 얼굴)·(홍반, 피부) 등 사전 사건 + 부위 7 건은 모두 멤버 안 조각 — 맞다.

### (ⅳ) 타임라인 정상 줄 처리 — (a)(e) 에 맞는가

- 정상 162 줄: ref 49 · ref_partial 32 · normal_memo 81. 81 메모는 「시술 후 과도한 표정 자제」류(사건 0)이고 참조 81 은 「주사 부위 약간의 붓기 (1-2일 소실)」→ 부종 · 「멍 거의 소실」→ 멍 · 「홍반 소실」→ 홍반 처럼 **이미 있는 단위에 닿을 때만** 가리킨다. 단위를 세우지 않고(검산 O) R34 에 reaction_level=normal 이 붙으므로 (a)(e) 에 맞다. §12 의 「정상 줄은 늘 참조하지 않는 쪽이 맞다면 결정」은 결정(D-7)으로 두면 된다 — 지금 쪽이 골드 「시술 후 안내」(정상 경과에 부종·멍이 등장)에 더 맞다.
- 비정상 none 57 은 발열(5) · 가피 조기 탈락 · 재상피화 지연 · 안면 함몰 · 시야 장애 · 켈로이드 · 혈관부종처럼 **사전에 없는 사건**이다 — (b) 가 부작용 문구에서만 노드를 세우므로 타임라인에서는 참조 없음으로 남는다. 이것은 설계대로이며(타임라인은 자기 테이블) 원장이 그 사건을 safety.* 에 쓰지 않은 것이 원인이다. 발열·켈로이드·혈관부종은 dictionary_add 후보로 §12 에 적을 만하다(결정).
- 관찰 **D-6**: 참조 판정이 토큰 포함만 본다 — 「시술 부위 부드러운 스무딩 (결절 예방 효과는 미입증)」→ 결절 참조 · 「가피 건조/갈색 변화」→ 건조(피부 건조) 참조. 이 참조가 R15 timeline_refs 로 올라가 계열 → 단위 엣지를 만든다(M3 → 결절). 줄 단위 exclude 밖에 수단이 없으므로 결정 kind 보강(ref 제외)은 다음 판 후보.

---

## ③ 행선지 · 추정 · 열거기

- **행선지 표본 20**(seed 32 무작위): literature moa → evidence_statement.statement(kind=moa) · taxonomy items[].name → catalog_item.name · step1 7_site_use.photos → 브론즈(사진 자산 범위 밖) · anatomy tissue_data.*_source → citation.text · combo-recipes analogy → package.analogy · contraindications rules[].note → R18.note · step1 licenses[].key → product.licenses.* · timeline category → R33 … 20 전부 표적이 ERD 개체·관계·사전에 있고 비고가 판 이력을 품는다. 이동 18 행은 검산 A 가 v3.1 표와 실제 diff 로 확인. complications name · emergency_signs · mandatory_disclosures · literature adverse_effects 행의 비고가 v3.2 문장으로 끝난다 ✓. 미정 0 ✓.
- **추정 매칭 지점**(ERD 가 「0」이라 쓴 뜻은 「사전 매칭에 유사도 없음」이고 그 뜻으로는 맞다). 추정이 남는 자리 셋 — (1) 참조 테이블 ref/ref_partial 은 토큰 포함(부정·예방 문맥 무시 · D-6) (2) 성분 씨앗의 문맥 추정(ERD 가 「추정 · 승인」이라 명시 · D-10) (3) ⑦ first_syllable(후보만). 셋 다 단위를 세우지 않는다.
- **열거기(json 구조)**: 규칙은 `rule_zero`·`node_rule`·`tokenize_rule`(particles/endings/words 목록)·`phrase_kinds`(note_words 35 · 문턱 3 · fallback_core 7 · core_exclude 7 · dup_rules)·`inherit_rule`·`timeline_rule`·`seed_rule`·`closed_dictionaries` 로 기계가 읽을 수 있고 §9 실측이 그 키를 쓴다 ✓. 열거형 결함(S-3 에 포함): 죽은 열거 3(`adverse_expression.kind/match_status/unlinked_reason`) · 낡은 열거 2(`adverse_effect.status` partial|unresolved · `adverse_effect.raw_reason`) · 이름이 어긋난 열거 1(`reference.ref_status` = 타임라인·응급·고지의 ref_status 인데 `reference` 는 시술 참조 객체의 접두). `tuple_rules.adverse.raw_name = 없음` · `unlinked_status = False` 는 기록으로 맞다.

---

## ④ 동결 판단

**동결 불가 — §0.2 핵심어 규칙(S-1) 한 문장이 사용자 (b) 「사건이 사전에 없으면」과 정의 2 「같은 세 칸은 같은 단위」를 깎고 있어, 이것과 규칙 범위 두 줄(S-2 · S-4) · 정의 표 잔재(S-3)를 닫은 뒤 동결 가.**

근거는 ⓪·① 과의 일치뿐이다: (a)(c)(d)(e) 는 구조로 들어갔고 실측이 원장과 맞는다. (b) 는 「새 노드 · ⑦ · unlinked 없음 · 추정 0」 네 요소 중 노드 규칙의 적용 범위가 넓어(사전 사건이 있는 멤버까지) 335 중 68 이 사용자 원칙 밖의 노드이고, ⑦ 범위가 좁아(노드끼리 0) 같은 원칙의 뒷절이 비어 있다.

### 동결 전 꼭 고칠 것(구조·규칙 4)

| # | 어디 | 무엇 |
|---|---|---|
| S-1 | §0.2 · 원칙 A · json node_rule · tuples.py | 핵심어 새 노드는 **사전 사건 조각이 0 인 멤버**에서만. 멤버 안 사전 사건은 각각 exact 단위(원칙 C 그대로), 옆의 미등록 토큰은 parsed.unregistered 보존(원칙 B). 실측·⑦·상속 표 재생성 |
| S-2 | §0.2 ⑦ 문장 | ⑦ 를 원장 노드끼리에도 돌린다(같은 규칙 · 후보만). 시술 축 ⑦ 과 대칭 |
| S-4 | §1.3 토큰화 목록 | 용언 관형형(-는/-지는/-은/-ㄴ) · 「~시」 · 「~하므로」를 어미·문법 낱말 목록에 locator 와 함께 추가. 어간이 독립 토큰이 아니어도 조사 뒤 어간이 2자 이상 한글이면 떼되 grammar 로 보존(「거부반응이」) |
| S-3 | §2.14 속성 표·식별자 · §3.1 열거형 · §5 adverse_tuple_assign target · R15 규칙 문장 · json entities/enums/id_rule | raw_name · RAW: · unlinked · adverse_expression · 타임라인/응급/문헌 「출처 원장 키」 · reaction_level=normal 잔재 제거(또는 「v3.1 까지」로 명시) · `reference.ref_status` 이름 교정. 검산에 「정의 표에 raw_name/unlinked 없음」 한 줄 추가 |

### 동결 후 결정으로(동결을 막지 않음 · 11)

| # | 무엇 | kind |
|---|---|---|
| D-1 | ⑦ 157(+장비 13) 닫기 — prefix2·first_syllable 잡음 ~31 은 conflict_close(not_same) · suffix_감·형성류는 fold_approve. dup_rules 좁히기는 선택 | fold_approve · conflict_close |
| D-2 | 조직층 분리로 빈 핵심어(막힘·손상·약화·이완·마비·합병증 ×혈관/근육) — 「혈관 손상」「근육 약화」 통째 값 추가 또는 접기 | dictionary_add · fold_approve |
| D-3 | 수식어 목록 밖(국소·최소·미약한·연장된·지속적인·임시·활성·중등도·장기간·묘한) — 규칙 데이터 | adverse_stopword 개정 |
| D-4 | 설명·수치 조각 노드 ~12(CO2 · 대비 수준 · 제품 최저 수준 · 합병증 · 반드시 사전 고지 …) | phrase_map(units []) · note_words |
| D-5 | 빈도·locator 셈 단위 — extracted/taxonomy 복제 쌍은 1 로(노드 n=2 의 52/83 · 씨앗 문턱 동일) | scope_review |
| D-6 | 참조 테이블의 예방·부정 문맥 참조(「결절 예방」→ 결절) — ref 제외 결정 kind 는 다음 판 | scope_review |
| D-7 | 정상 줄 참조 유지/중단(§12) — 현행 유지 추천 | scope_review |
| D-8 | 타임라인 none 57 의 사전 밖 사건(발열 · 켈로이드 · 혈관부종 · 재상피화 지연) 사전 추가 여부 | dictionary_add |
| D-9 | R33 끝 modality 6(HA 필러 · HIFU/RF 리프팅 · 프락셔널 CO2 레이저 · DCA · 니들RF · 케미컬 필링) 튜플 지정 | tuple_assign |
| D-10 | 성분 씨앗 17 중 문맥 추정 9(심부·동일·딥·별도·약한·얕은·자연스러운·주입·코그) 거름 · 변형 쌍 176 승인 | dictionary_add |
| D-11 | 줄임말 다중 후보(울트라 → 4 · 피코 → 7 · 리쥬란 → 3) · 장비 ⑦ 13 | fold_approve · dictionary_add |

어긋남 합계: **구조·규칙 4 / 결정 11**.
