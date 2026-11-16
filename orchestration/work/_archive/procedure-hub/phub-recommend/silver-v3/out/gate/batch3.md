# 결정 묶음 3 — 게이트 자료(proposed 를 사용자가 고른다)

상위 5 · 고를 자리(하위 항목 · 하위 없는 항목) 15 · 추천 있음 5 · 추천 없음 10.
원문은 브론즈 원장에서 locator 로 직접 읽었다. 추천은 원장 문장이 명시할 때만 — 없으면 「—」. 고른 결과는 `python3 apply_gate.py --gate out/gate/batch3.json --out decisions/batch3b/ --answers answers.json` 으로 결정 파일이 된다(answers = {항목 id 또는 하위 id: 옵션 key}).

| 자리 | 질문 | 추천 |
|---|---|---|
| m5-rename | 계열 M5 정준 이름을 「자가혈 유래 시술」로 바꿀까? | — |
| m16-technique/M16-1 | M16 하위분류 M16-1 「미백/항산화」 항목 7 의 기법을 무엇으로 둘까? | intravenous_stated |
| m16-technique/M16-2 | M16 하위분류 M16-2 「피로회복」 항목 8 의 기법을 무엇으로 둘까? | intravenous_stated |
| m16-technique/M16-3 | M16 하위분류 M16-3 「재생/면역」 항목 9 의 기법을 무엇으로 둘까? | intravenous_stated |
| m16-technique/M16-4 | M16 하위분류 M16-4 「영양보충」 항목 5 의 기법을 무엇으로 둘까? | intravenous_stated |
| m16-technique/M16-DCA | M16 하위분류 M16-DCA 「DCA (지방세포파괴)」 항목 11 의 기법을 무엇으로 둘까? | — |
| m16-technique/M16-LIPO | M16 하위분류 M16-LIPO 「지방분해주사 (마케팅명)」 항목 9 의 기법을 무엇으로 둘까? | — |
| site-synonyms/01 | 해부 이름 「턱라인」 를 부위 「턱선」로 읽을까? | — |
| site-synonyms/02 | 해부 이름 「코끝」 를 부위 「코」로 읽을까? | propose |
| site-synonyms/03 | 해부 이름 「눈밑」, 「눈꺼풀」 를 부위 「눈 주변」로 읽을까? | — |
| site-synonyms/04 | 해부 이름 「턱밑」, 「이중턱」 를 부위 「이중턱/턱밑」로 읽을까? | — |
| site-synonyms/05 | 해부 이름 「광경근」 를 부위 「목」로 읽을까? | — |
| site-synonyms/06 | 부위 사전에 region 「바디」을 세울까? | — |
| air-embolism-qualifier | complications 「공기색전·카테터 관련 감염」[M16]에 (색전, none, 공기) 수식 단위를 세울까? | — |
| records/NEC-01 | 피부 괴사 → (괴사, 피부) — 기록으로 남길까? | — |

## m5-rename — 계열 M5 정준 이름을 「자가혈 유래 시술」로 바꿀까?

원장 taxonomy 의 M5 이름은 「PRP/자가혈」이고 하위분류가 PRP·PRF(CGF)·MCT·ACT 등이다. 다른 원장은 M5 를 「PRP 피부재생술」(extracted)·「PRP/엑소좀」(market-pricing · procedure-profiles)·「Platelet-rich plasma (PRP) and exosome therapies」(literature) 로 적는다. M1·M3 와 같은 V3-6 이름 바꾸기 후보(사용자 「자가혈이 더 넓은 개념」 · 추천·미확정).

**원장 원문**

- `taxonomy.json:modality[].category@4` — 「PRP/자가혈」 (taxonomy M5 계열 이름·하위분류)
- `taxonomy.json:modality[].category_en@4` — 「PRP / Autologous Blood」 (taxonomy M5 계열 이름·하위분류)
- `taxonomy.json:modality[].name@4` — 「PRP/자가혈」 (taxonomy M5 계열 이름·하위분류)
- `taxonomy.json:modality[].subcategories[].label@4/0` — 「PRP (혈소판풍부혈장)」 (taxonomy M5 계열 이름·하위분류)
- `taxonomy.json:modality[].subcategories[].label@4/1` — 「PRF (피브린풍부혈장)」 (taxonomy M5 계열 이름·하위분류)
- `taxonomy.json:modality[].subcategories[].label@4/2` — 「MCT (메타셀)」 (taxonomy M5 계열 이름·하위분류)
- `taxonomy.json:modality[].subcategories[].label@4/3` — 「ACT」 (taxonomy M5 계열 이름·하위분류)
- `literature-evidence.json:categories.{code}.name@M5` — 「Platelet-rich plasma (PRP) and exosome therapies」 (다른 원장의 M5 이름)
- `extracted.json:{code}.name@M5` — 「PRP 피부재생술」 (다른 원장의 M5 이름)
- `market-pricing.json:categories[].name@4` — 「PRP/엑소좀」 (다른 원장의 M5 이름)
- `procedure-profiles.json:profiles[].name@4` — 「PRP/엑소좀」 (다른 원장의 M5 이름)

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| rename | 「자가혈 유래 시술」로 바꾼다 | modality 사전 M5 정준값 「PRP/자가혈」→「자가혈 유래 시술」 — MOD-M5·CAT-·PRD- id 는 그대로(코드 기반) · 사전 항목 id(DIC-)는 재계산되고 옛 id DIC-e766b41d53 는 renamed_from · 옛 정준값은 동의어로 내린다. 지금 동의어 9(M5, PRP / Autologous Blood, 내 혈액 재생 주사 (PRP), PRP/Exosome, PRP 피부재생술, Platelet-Rich Plasma Therapy …)는 그대로 | canonical_rename `DEC-2026-11-05-B3B-REN-03` | 적용 |
| keep | 지금대로 「PRP/자가혈」 | 결정 없음 | 결정 없음 | — |

추천: **—** — 원장 어디에도 「자가혈 유래 시술」라는 이름이 없다 — 새 이름은 사람이 정한다(추천 없음). 엑소좀이 섞인 이름(「PRP/엑소좀」)의 동의어 제외는 6차에서 적용됐다(EXO-06 · dictionary_remove).

## m16-technique — M16 수액치료 하위분류별 기법 지정(하위 6)

V3-8 — 하위분류 단위 기본 기법(canonical_mapping R5:<하위분류 id>). 하위 항목마다 고른다. 기법 후보 = 계열 R5 기법 · 제안 기법 · 항목 원장이 적은 기법.

### m16-technique/M16-1 — M16 하위분류 M16-1 「미백/항산화」 항목 7 의 기법을 무엇으로 둘까?

계열 M16 의 R5 기법은 intravenous 하나지만 DCA·지방분해주사처럼 정맥이 아닌 항목이 있어 계열 일괄 상속을 하지 않는다(ERD §9.5.6). V3-8 은 하위분류 단위로 기본 기법을 지정한다 — 항목마다 원장이 적은 기법 표기를 같이 본다.

**원장 원문**

- `taxonomy.json:modality[].subcategories[].label@15/0` — 「미백/항산화」 (하위분류)
- `procedure-profiles.json:profiles[].mechanism[]@15/0` — 「intravenous」 (계열 M16 기법(R5)·기전)
- `taxonomy.json:modality[].extracted.mechanism@15` — 「영양 성분을 정맥을 통해 직접 혈류에 투여하면, 소화기관을 거치지 않으므로(위장관 초회통과효과 회피) 생체이용률(몸이 실제로 사용하는 비율)이 거의 100%에 가깝다. 경구 복용 시 흡수율이 10~30%에 불과한 비타민C 같은 성분도, 정맥주사로는 훨씬 높은 혈중 농도를 달성할 수 있다」 (계열 M16 기법(R5)·기전)
- `taxonomy.json:modality[].subcategories[].items[].name@15/0/0` — 「백옥주사」 (항목 이름 — 기법 표기 intravenous: 「제 성분은 글루타치온 IV」 / 「치료 > 항산화·미백 IV」 / 「. 고용량 글루타치온 IV의 미백 효과는 제한된」 / 「글루타치온 정맥주사로 항산화·미백」 / 「 멜라닌 합성 억제. 정맥주사를 통해 높은 생체이용」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/0/0` — 「글루타치온의 강력한 항산화 작용으로 활성산소 제거 및 멜라닌 합성 억제. 정맥주사를 통해 높은 생체이용률로 직접 혈류 전달되어 전신 항산화 효과 제공.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].detail@15/0/0` — 「마케팅 명칭 — 실제 성분은 글루타치온 IV」 (기법 표기가 나오는 문장)
- `taxonomy.json:modality[].subcategories[].items[].canonical_category@15/0/0` — 「M16 수액치료 > 항산화·미백 IV」 (기법 표기가 나오는 문장)
- `taxonomy.json:modality[].subcategories[].items[].naming_caveat@15/0/0` — 「'하얗게 된다'는 효과 기반 마케팅명. 고용량 글루타치온 IV의 미백 효과는 제한된 임상 근거이며 FDA·식약처의 미백 목적 공식 허가 적응증 아님. 의료광고 표현 주의 필요」 (기법 표기가 나오는 문장)
- `taxonomy.json:modality[].subcategories[].items[].extracted.overview@15/0/0` — 「글루타치온 정맥주사로 항산화·미백」 (기법 표기가 나오는 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/0/1` — 「고농도C」 (항목 이름 — 기법 표기 intravenous: 「비타민C 메가도스 정맥주사」 / 「 및 활성산소 제거. 정맥주사를 통해 경구 투여 불」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/0/1` — 「고용량 비타민C의 강력한 항산화 작용으로 콜라겐 합성 촉진 및 활성산소 제거. 정맥주사를 통해 경구 투여 불가능한 고농도 도달로 피부 항노화 효과.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].extracted.overview@15/0/1` — 「비타민C 메가도스 정맥주사」 (기법 표기가 나오는 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/0/2` — 「셀디톡스수액」 (항목 이름 — 기법 표기 intravenous: 「내 독소 배출 촉진. 정맥주사를 통해 높은 생체이용」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/0/2` — 「항산화제 및 간 해독 성분의 복합작용으로 활성산소 제거 및 체내 독소 배출 촉진. 정맥주사를 통해 높은 생체이용률로 전신 해독·항산화 효과 제공.」 (항목 기전 문장)
- … 외 10 곳(batch3.json evidence 전부)

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| intravenous_all | intravenous — 하위분류 항목 전부(7) | scope 7 항목 중 지금 technique=none 인 7 튜플의 technique 칸이 TEC-428b9bd04a(intravenous) 로 · R5 하위분류 M16-1 → intravenous 엣지(basis canonical_mapping)가 생긴다. 원장이 다른 기법이라 적은 항목도 들어간다: 비타민D주사(injection). 원장이 기법을 적지 않은 항목 2: 알파리포산주사, 스노우주사. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-1` | 적용 |
| **intravenous_stated** | intravenous — 원장이 그렇게 적은 항목만(4) | scope 4 항목 중 지금 technique=none 인 4 튜플의 technique 칸이 TEC-428b9bd04a(intravenous) 로 · R5 하위분류 M16-1 → intravenous 엣지(basis canonical_mapping)가 생긴다. 나머지 3(알파리포산주사, 비타민D주사, 스노우주사)은 technique 그대로. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-1` | 적용 |
| injection_all | injection — 하위분류 항목 전부(7) | scope 7 항목 중 지금 technique=none 인 7 튜플의 technique 칸이 TEC-545a700199(injection) 로 · R5 하위분류 M16-1 → injection 엣지(basis canonical_mapping)가 생긴다. 원장이 다른 기법이라 적은 항목도 들어간다: 백옥주사(intravenous), 고농도C(intravenous), 셀디톡스수액(intravenous), 멀티비타민수액(intravenous). 원장이 기법을 적지 않은 항목 2: 알파리포산주사, 스노우주사. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-1` | 적용 |
| injection_stated | injection — 원장이 그렇게 적은 항목만(1) | scope 1 항목 중 지금 technique=none 인 1 튜플의 technique 칸이 TEC-545a700199(injection) 로 · R5 하위분류 M16-1 → injection 엣지(basis canonical_mapping)가 생긴다. 나머지 6(백옥주사, 고농도C, 셀디톡스수액, 알파리포산주사, 멀티비타민수액, 스노우주사)은 technique 그대로. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-1` | 적용 |
| keep | 지금대로(technique none) | 결정 없음 | 결정 없음 | — |

추천: **intravenous_stated** — 원장 문장이 intravenous 를 명시한 항목 4 만 — 백옥주사, 고농도C, 셀디톡스수액, 멀티비타민수액. 나머지는 알파리포산주사(기법 표기 없음), 비타민D주사(injection), 스노우주사(기법 표기 없음) 라 넣지 않는다.

### m16-technique/M16-2 — M16 하위분류 M16-2 「피로회복」 항목 8 의 기법을 무엇으로 둘까?

계열 M16 의 R5 기법은 intravenous 하나지만 DCA·지방분해주사처럼 정맥이 아닌 항목이 있어 계열 일괄 상속을 하지 않는다(ERD §9.5.6). V3-8 은 하위분류 단위로 기본 기법을 지정한다 — 항목마다 원장이 적은 기법 표기를 같이 본다.

**원장 원문**

- `taxonomy.json:modality[].subcategories[].label@15/1` — 「피로회복」 (하위분류)
- `procedure-profiles.json:profiles[].mechanism[]@15/0` — 「intravenous」 (계열 M16 기법(R5)·기전)
- `taxonomy.json:modality[].extracted.mechanism@15` — 「영양 성분을 정맥을 통해 직접 혈류에 투여하면, 소화기관을 거치지 않으므로(위장관 초회통과효과 회피) 생체이용률(몸이 실제로 사용하는 비율)이 거의 100%에 가깝다. 경구 복용 시 흡수율이 10~30%에 불과한 비타민C 같은 성분도, 정맥주사로는 훨씬 높은 혈중 농도를 달성할 수 있다」 (계열 M16 기법(R5)·기전)
- `taxonomy.json:modality[].subcategories[].items[].name@15/1/0` — 「마늘주사」 (항목 이름 — 기법 표기 intravenous: 「에너지 생성 활성화. 정맥주사를 통해 빠른 흡수로 」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/1/0` — 「비타민B1과 마늘 추출물의 협력작용으로 탄수화물 대사 촉진 및 에너지 생성 활성화. 정맥주사를 통해 빠른 흡수로 급성 피로 회복 및 신경 기능 개선.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/1/1` — 「신데렐라주사」 (항목 이름 — 기법 표기 intravenous: 「 수액치료 > 항산화 IV」 / 「 에너지 생성 촉진. 정맥주사를 통해 세포 대사 활」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/1/1` — 「알파리포산의 강력한 항산화 작용으로 활성산소 제거 및 미토콘드리아 에너지 생성 촉진. 정맥주사를 통해 세포 대사 활성화 및 피부 항노화 효과 동시 달성.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].canonical_category@15/1/1` — 「M16 수액치료 > 항산화 IV」 (기법 표기가 나오는 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/1/2` — 「에너지부스트수액」 (항목 이름 — 기법 표기 intravenous: 「 및 피로물질 제거. 정맥주사를 통해 높은 생체이용」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/1/2` — 「비타민B군, 미네랄, 항산화제의 복합작용으로 세포 에너지 생성 촉진 및 피로물질 제거. 정맥주사를 통해 높은 생체이용률로 빠른 피로회복 및 신진대사 활성화.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/1/3` — 「아르기닌주사」 (항목 이름 — 기법 표기 intravenous: 「이완 및 혈류 개선. 정맥주사를 통해 직접 혈류 전」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/1/3` — 「아르기닌의 일산화질소(NO) 생성 촉진으로 혈관 이완 및 혈류 개선. 정맥주사를 통해 직접 혈류 전달로 빠른 혈류 개선, 조직 산소공급 증가 및 체력 회복 촉진.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/1/4` — 「징크주사」 (항목 이름 — 기법 표기 intravenous: 「아연을 정맥 또는 근육 주사로 투여하여」; injection: 「아연을 정맥 또는 근육 주사로 투여하여 면역력 강」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/1/4` — 「아연이 콜라겐 합성과 단백질 대사에 필수적인 보조인자로 작용하여 상처 치유와 피부 재생을 촉진합니다. 또한 항산화 효소의 활성을 높이고 면역세포 기능을 강화하여 전반적인 피부 건강을 개선합니다.」 (항목 기전 문장)
- … 외 10 곳(batch3.json evidence 전부)

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| intravenous_all | intravenous — 하위분류 항목 전부(8) | scope 8 항목 중 지금 technique=none 인 8 튜플의 technique 칸이 TEC-428b9bd04a(intravenous) 로 · R5 하위분류 M16-2 → intravenous 엣지(basis canonical_mapping)가 생긴다. 원장이 다른 기법이라 적은 항목도 들어간다: 징크주사(both).  | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-2` | 적용 |
| **intravenous_stated** | intravenous — 원장이 그렇게 적은 항목만(7) | scope 7 항목 중 지금 technique=none 인 7 튜플의 technique 칸이 TEC-428b9bd04a(intravenous) 로 · R5 하위분류 M16-2 → intravenous 엣지(basis canonical_mapping)가 생긴다. 나머지 1(징크주사)은 technique 그대로. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-2` | 적용 |
| keep | 지금대로(technique none) | 결정 없음 | 결정 없음 | — |

추천: **intravenous_stated** — 원장 문장이 intravenous 를 명시한 항목 7 만 — 마늘주사, 신데렐라주사, 에너지부스트수액, 아르기닌주사, 비오틴주사, 마이어스칵테일, 종합아미노산수액. 나머지는 징크주사(정맥·근육 둘 다) 라 넣지 않는다.

### m16-technique/M16-3 — M16 하위분류 M16-3 「재생/면역」 항목 9 의 기법을 무엇으로 둘까?

계열 M16 의 R5 기법은 intravenous 하나지만 DCA·지방분해주사처럼 정맥이 아닌 항목이 있어 계열 일괄 상속을 하지 않는다(ERD §9.5.6). V3-8 은 하위분류 단위로 기본 기법을 지정한다 — 항목마다 원장이 적은 기법 표기를 같이 본다.

**원장 원문**

- `taxonomy.json:modality[].subcategories[].label@15/2` — 「재생/면역」 (하위분류)
- `procedure-profiles.json:profiles[].mechanism[]@15/0` — 「intravenous」 (계열 M16 기법(R5)·기전)
- `taxonomy.json:modality[].extracted.mechanism@15` — 「영양 성분을 정맥을 통해 직접 혈류에 투여하면, 소화기관을 거치지 않으므로(위장관 초회통과효과 회피) 생체이용률(몸이 실제로 사용하는 비율)이 거의 100%에 가깝다. 경구 복용 시 흡수율이 10~30%에 불과한 비타민C 같은 성분도, 정맥주사로는 훨씬 높은 혈중 농도를 달성할 수 있다」 (계열 M16 기법(R5)·기전)
- `taxonomy.json:modality[].subcategories[].items[].name@15/2/0` — 「태반주사(라엔넥)」 (항목 이름 — 기법 표기 injection: 「 항노화 효과 제공. 근육/피하주사로 천천히 흡수되어 지」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/2/0` — 「라엔넥의 효소처리 인태반 추출물(저·중분자 단백질 포함)에 포함된 필수 아미노산, 펩타이드, 비타민, 미네랄, 핵산, 성장인자가 세포 재생 촉진 및 항노화 효과 제공. 근육/피하주사로 천천히 흡수되어 지속적 효과 유지.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/2/1` — 「NAD+」 (항목 이름 — 기법 표기 intravenous: 「 핵심 코엔자임으로, 정맥주사를 통해 직접 혈류 전」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/2/1` — 「NAD+(nicotinamide adenine dinucleotide)는 세포 에너지(ATP) 생성의 핵심 코엔자임으로, 정맥주사를 통해 직접 혈류 전달되어 미토콘드리아 기능 활성화, DNA 손상 복구 및 장수 유전자 활성화로 항노화 효과 제공.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/2/2` — 「이뮨코어수액」 (항목 이름 — 기법 표기 intravenous: 「자연살해세포 활성화. 정맥주사를 통해 높은 생체이용」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/2/2` — 「비타민C, 아연, 셀레늄, 항산화제 등의 복합작용으로 면역세포 기능 촉진 및 자연살해세포 활성화. 정맥주사를 통해 높은 생체이용률로 빠른 면역력 강화 및 항바이러스·항감염 효과.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/2/3` — 「NAD+ 주사」 (항목 이름 — 기법 표기 intravenous: 「 재생을 목표로 하는 정맥주사 치료」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/2/3` — 「NAD+는 미토콘드리아 내 ATP 생성 과정에서 필수적인 보조효소로 작용하여 세포 에너지 생산을 증진시킵니다. 또한 SIRT1 등의 장수 유전자를 활성화하고 DNA 손상 복구 과정을 촉진하여 세포 노화를 지연시킵니다.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].extracted.overview@15/2/3` — 「세포의 에너지 대사와 DNA 복구를 촉진하여 노화 방지와 피부 재생을 목표로 하는 정맥주사 치료」 (기법 표기가 나오는 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/2/4` — 「셀레늄 주사」 (항목 이름 — 기법 표기 intravenous: 「셀레늄을 정맥 또는 근육 주사로 투여하여」; injection: 「셀레늄을 정맥 또는 근육 주사로 투여하여 항산화 효」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/2/4` — 「셀레늄은 글루타치온 퍼옥시다제의 필수 보조인자로 작용하여 세포막의 과산화지질을 제거하고 활성산소를 중화시킵니다. 또한 면역세포의 기능을 향상시키고 갑상선 호르몬 대사를 조절하여 전반적인 신진대사를 개선합니다.」 (항목 기전 문장)
- … 외 12 곳(batch3.json evidence 전부)

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| intravenous_all | intravenous — 하위분류 항목 전부(9) | scope 9 항목 중 지금 technique=none 인 9 튜플의 technique 칸이 TEC-428b9bd04a(intravenous) 로 · R5 하위분류 M16-3 → intravenous 엣지(basis canonical_mapping)가 생긴다. 원장이 다른 기법이라 적은 항목도 들어간다: 태반주사(라엔넥)(injection), 셀레늄 주사(both). 원장이 기법을 적지 않은 항목 1: 태반주사멜스몬. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-3` | 적용 |
| **intravenous_stated** | intravenous — 원장이 그렇게 적은 항목만(6) | scope 6 항목 중 지금 technique=none 인 6 튜플의 technique 칸이 TEC-428b9bd04a(intravenous) 로 · R5 하위분류 M16-3 → intravenous 엣지(basis canonical_mapping)가 생긴다. 나머지 3(태반주사(라엔넥), 셀레늄 주사, 태반주사멜스몬)은 technique 그대로. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-3` | 적용 |
| injection_all | injection — 하위분류 항목 전부(9) | scope 9 항목 중 지금 technique=none 인 9 튜플의 technique 칸이 TEC-545a700199(injection) 로 · R5 하위분류 M16-3 → injection 엣지(basis canonical_mapping)가 생긴다. 원장이 다른 기법이라 적은 항목도 들어간다: NAD+(intravenous), 이뮨코어수액(intravenous), NAD+ 주사(intravenous), 셀레늄 주사(both), 고용량 비타민C 주사(intravenous), 오메가3수액(intravenous), 콜라겐수액(intravenous). 원장이 기법을 적지 않은 항목 1: 태반주사멜스몬. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-3` | 적용 |
| injection_stated | injection — 원장이 그렇게 적은 항목만(1) | scope 1 항목 중 지금 technique=none 인 1 튜플의 technique 칸이 TEC-545a700199(injection) 로 · R5 하위분류 M16-3 → injection 엣지(basis canonical_mapping)가 생긴다. 나머지 8(NAD+, 이뮨코어수액, NAD+ 주사, 셀레늄 주사, 고용량 비타민C 주사, 오메가3수액, 콜라겐수액, 태반주사멜스몬)은 technique 그대로. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-3` | 적용 |
| keep | 지금대로(technique none) | 결정 없음 | 결정 없음 | — |

추천: **intravenous_stated** — 원장 문장이 intravenous 를 명시한 항목 6 만 — NAD+, 이뮨코어수액, NAD+ 주사, 고용량 비타민C 주사, 오메가3수액, 콜라겐수액. 나머지는 태반주사(라엔넥)(injection), 셀레늄 주사(정맥·근육 둘 다), 태반주사멜스몬(기법 표기 없음) 라 넣지 않는다.

### m16-technique/M16-4 — M16 하위분류 M16-4 「영양보충」 항목 5 의 기법을 무엇으로 둘까?

계열 M16 의 R5 기법은 intravenous 하나지만 DCA·지방분해주사처럼 정맥이 아닌 항목이 있어 계열 일괄 상속을 하지 않는다(ERD §9.5.6). V3-8 은 하위분류 단위로 기본 기법을 지정한다 — 항목마다 원장이 적은 기법 표기를 같이 본다.

**원장 원문**

- `taxonomy.json:modality[].subcategories[].label@15/3` — 「영양보충」 (하위분류)
- `procedure-profiles.json:profiles[].mechanism[]@15/0` — 「intravenous」 (계열 M16 기법(R5)·기전)
- `taxonomy.json:modality[].extracted.mechanism@15` — 「영양 성분을 정맥을 통해 직접 혈류에 투여하면, 소화기관을 거치지 않으므로(위장관 초회통과효과 회피) 생체이용률(몸이 실제로 사용하는 비율)이 거의 100%에 가깝다. 경구 복용 시 흡수율이 10~30%에 불과한 비타민C 같은 성분도, 정맥주사로는 훨씬 높은 혈중 농도를 달성할 수 있다」 (계열 M16 기법(R5)·기전)
- `taxonomy.json:modality[].subcategories[].items[].name@15/3/0` — 「비타민D」 (항목 이름 — 기법 표기 intravenous: 「성화로 골밀도 증가. 정맥주사를 통해 근육 단백질 」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/3/0` — 「비타민D의 칼슘 흡수 촉진 및 골아세포 분화 활성화로 골밀도 증가. 정맥주사를 통해 근육 단백질 합성 촉진 및 근력 개선으로 근골격계 건강 강화.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/3/1` — 「종합비타민수액」 (항목 이름 — 기법 표기 intravenous: 「비타민·미네랄 종합 정맥수액」 / 「역 기능 종합 강화. 정맥주사를 통해 높은 생체이용」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/3/1` — 「비타민B군, 비타민C, 마그네슘, 칼슘 등 다양한 미네랄의 복합작용으로 세포 에너지 생성, 신경 기능, 면역 기능 종합 강화. 정맥주사를 통해 높은 생체이용률로 전신 영양 보충 및 피로회복 동시 달성.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].extracted.overview@15/3/1` — 「비타민·미네랄 종합 정맥수액」 (기법 표기가 나오는 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/3/2` — 「멀티미네랄」 (항목 이름 — 기법 표기 intravenous: 「필수 미량원소 정맥 공급」 / 「정맥 주사를 통해 아연, 철, 」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/3/2` — 「정맥 주사를 통해 아연, 철, 구리, 망간 등 필수 미량원소를 혈류에 직접 전달하여 생체이용률을 극대화합니다. 미량원소는 항산화 효소의 보인자로 작용하여 산화적 스트레스를 감소시키고 피부 대사를 촉진합니다.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].extracted.overview@15/3/2` — 「필수 미량원소 정맥 공급」 (기법 표기가 나오는 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/3/3` — 「철분주사」 (항목 이름 — 기법 표기 intravenous: 「정맥내 철분이 직접 혈액으로」)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/3/3` — 「정맥내 철분이 직접 혈액으로 공급되어 헤모글로빈 합성을 돕습니다. 산소운반능력 향상으로 피부색조와 전반적인 컨디션이 개선됩니다.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/3/4` — 「칼슘주사」 (항목 이름 — 기법 표기 없음)
- … 외 1 곳(batch3.json evidence 전부)

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| intravenous_all | intravenous — 하위분류 항목 전부(5) | scope 5 항목 중 지금 technique=none 인 5 튜플의 technique 칸이 TEC-428b9bd04a(intravenous) 로 · R5 하위분류 M16-4 → intravenous 엣지(basis canonical_mapping)가 생긴다. 원장이 기법을 적지 않은 항목 1: 칼슘주사. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-4` | 적용 |
| **intravenous_stated** | intravenous — 원장이 그렇게 적은 항목만(4) | scope 4 항목 중 지금 technique=none 인 4 튜플의 technique 칸이 TEC-428b9bd04a(intravenous) 로 · R5 하위분류 M16-4 → intravenous 엣지(basis canonical_mapping)가 생긴다. 나머지 1(칼슘주사)은 technique 그대로. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-4` | 적용 |
| keep | 지금대로(technique none) | 결정 없음 | 결정 없음 | — |

추천: **intravenous_stated** — 원장 문장이 intravenous 를 명시한 항목 4 만 — 비타민D, 종합비타민수액, 멀티미네랄, 철분주사. 나머지는 칼슘주사(기법 표기 없음) 라 넣지 않는다.

### m16-technique/M16-DCA — M16 하위분류 M16-DCA 「DCA (지방세포파괴)」 항목 11 의 기법을 무엇으로 둘까?

계열 M16 의 R5 기법은 intravenous 하나지만 DCA·지방분해주사처럼 정맥이 아닌 항목이 있어 계열 일괄 상속을 하지 않는다(ERD §9.5.6). V3-8 은 하위분류 단위로 기본 기법을 지정한다 — 항목마다 원장이 적은 기법 표기를 같이 본다.

**원장 원문**

- `taxonomy.json:modality[].subcategories[].label@15/4` — 「DCA (지방세포파괴)」 (하위분류)
- `taxonomy.json:modality[].subcategories[].description@15/4` — 「데옥시콜산(DCA) / 콜산(CA) 기반 지방세포파괴 주사제. FDA(2015 카이벨라) 및 한국 식약처 허가 제품군. DCA는 유일하게 턱밑 지방 적응증으로 허가된 성분. PPC(포스파티딜콜린)와 완전히 다름 — PPC는 한국에서 미용목적 사용 금지(2014). DCA: 지방세포막 직」 (하위분류)
- `procedure-profiles.json:profiles[].mechanism[]@15/0` — 「intravenous」 (계열 M16 기법(R5)·기전)
- `taxonomy.json:modality[].extracted.mechanism@15` — 「영양 성분을 정맥을 통해 직접 혈류에 투여하면, 소화기관을 거치지 않으므로(위장관 초회통과효과 회피) 생체이용률(몸이 실제로 사용하는 비율)이 거의 100%에 가깝다. 경구 복용 시 흡수율이 10~30%에 불과한 비타민C 같은 성분도, 정맥주사로는 훨씬 높은 혈중 농도를 달성할 수 있다」 (계열 M16 기법(R5)·기전)
- `taxonomy.json:modality[].subcategories[].items[].name@15/4/0` — 「브이올렛」 (항목 이름 — 기법 표기 없음)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/4/0` — 「데옥시콜산(DCA)이 지방세포막을 직접 파괴하여 지방세포를 영구 제거한다. 동시에 콜라겐 합성을 유도하여 파괴된 지방 부위의 피부 탄력을 유지한다.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/4/1` — 「벨카이라」 (항목 이름 — 기법 표기 없음)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/4/1` — 「합성 데옥시콜산(DCA)이 지방세포막의 지질 이중층을 직접 파괴(cytolysis)하여 세포 내용물을 방출시킨다. 파괴된 지방세포는 대식세포에 의해 탐식되어 영구적으로 제거된다. 담즙산의 천연 지방 유화 기능을 활용한 메커니즘.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/4/2` — 「벨라콜린」 (항목 이름 — 기법 표기 없음)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/4/2` — 「데옥시콜산이 지방세포의 세포막 인지질을 유화(emulsification)하여 세포를 비가역적으로 파괴한다. 파괴된 지방은 대식세포 탐식 → 림프 배출 경로로 체외 제거된다.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/4/3` — 「카이벨라」 (항목 이름 — 기법 표기 없음)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/4/3` — 「데옥시콜산(DCA)이 지방세포막의 인지질 이중층을 직접 파괴(cytolysis)하여 지방세포를 비가역적으로 제거한다. 파괴된 세포 내용물은 대식세포에 의해 탐식되어 체외로 배출되며, 동시에 콜라겐 신생을 유도한다.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/4/4` — 「올리핏주」 (항목 이름 — 기법 표기 없음)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/4/4` — 「데옥시콜산(DCA)이 지방세포막의 인지질 이중층을 직접 파괴(cytolysis)하여 지방세포를 비가역적으로 제거한다. 파괴된 세포 내용물은 대식세포에 의해 탐식되어 체외로 배출되며, 동시에 콜라겐 신생을 유도한다.」 (항목 기전 문장)
- … 외 12 곳(batch3.json evidence 전부)

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| intravenous_all | intravenous — 하위분류 항목 전부(11) | scope 11 항목 중 지금 technique=none 인 11 튜플의 technique 칸이 TEC-428b9bd04a(intravenous) 로 · R5 하위분류 M16-DCA → intravenous 엣지(basis canonical_mapping)가 생긴다. 원장이 기법을 적지 않은 항목 11: 브이올렛, 벨카이라, 벨라콜린, 카이벨라, 올리핏주, 펜카이라주, 바이블주, 밀리핏주사, 원더브이, 리포린, 뉴비쥬. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-DCA` | 적용 |
| injection_all | injection — 하위분류 항목 전부(11) | scope 11 항목 중 지금 technique=none 인 11 튜플의 technique 칸이 TEC-545a700199(injection) 로 · R5 하위분류 M16-DCA → injection 엣지(basis canonical_mapping)가 생긴다. 원장이 기법을 적지 않은 항목 11: 브이올렛, 벨카이라, 벨라콜린, 카이벨라, 올리핏주, 펜카이라주, 바이블주, 밀리핏주사, 원더브이, 리포린, 뉴비쥬. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-DCA` | 적용 |
| keep | 지금대로(technique none) | 결정 없음 | 결정 없음 | — |

추천: **—** — 항목 원장 문장이 기법(정맥·근육·피하 주사)을 적지 않는다 — 하위분류 라벨·설명만으로는 기법을 정하지 않는다(추천 없음).

### m16-technique/M16-LIPO — M16 하위분류 M16-LIPO 「지방분해주사 (마케팅명)」 항목 9 의 기법을 무엇으로 둘까?

계열 M16 의 R5 기법은 intravenous 하나지만 DCA·지방분해주사처럼 정맥이 아닌 항목이 있어 계열 일괄 상속을 하지 않는다(ERD §9.5.6). V3-8 은 하위분류 단위로 기본 기법을 지정한다 — 항목마다 원장이 적은 기법 표기를 같이 본다.

**원장 원문**

- `taxonomy.json:modality[].subcategories[].label@15/5` — 「지방분해주사 (마케팅명)」 (하위분류)
- `taxonomy.json:modality[].subcategories[].description@15/5` — 「다양한 약물 혼합 지방분해 주사. 병원마다 성분/배합/명칭이 상이. DCA 제품과 달리 식약처 개별 허가는 없으며, 의사 재량으로 약물 혼합 사용.」 (하위분류)
- `procedure-profiles.json:profiles[].mechanism[]@15/0` — 「intravenous」 (계열 M16 기법(R5)·기전)
- `taxonomy.json:modality[].extracted.mechanism@15` — 「영양 성분을 정맥을 통해 직접 혈류에 투여하면, 소화기관을 거치지 않으므로(위장관 초회통과효과 회피) 생체이용률(몸이 실제로 사용하는 비율)이 거의 100%에 가깝다. 경구 복용 시 흡수율이 10~30%에 불과한 비타민C 같은 성분도, 정맥주사로는 훨씬 높은 혈중 농도를 달성할 수 있다」 (계열 M16 기법(R5)·기전)
- `taxonomy.json:modality[].subcategories[].items[].name@15/5/0` — 「V라인주사」 (항목 이름 — 기법 표기 없음)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/5/0` — 「데옥시콜산(deoxycholic acid) 등의 지방분해 성분이 지방세포막을 파괴하여 세포 내용물을 유출시킵니다. 파괴된 지방세포는 대식세포에 의해 제거되고 림프계를 통해 체외로 배출됩니다.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/5/1` — 「슈퍼투턱주사」 (항목 이름 — 기법 표기 없음)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/5/1` — 「지방분해 성분이 이중턱 부위의 지방세포막을 파괴하여 지방을 분해합니다. 분해된 지방은 림프순환을 통해 체외로 배출되어 턱선이 개선됩니다.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/5/2` — 「팻킬주사」 (항목 이름 — 기법 표기 없음)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/5/2` — 「지방세포막을 직접적으로 파괴하여 지방분해를 촉진하고 리폴리시스 과정을 활성화합니다. 동시에 림프순환을 개선하여 분해된 지방의 배출을 촉진하고 부종을 감소시킵니다.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/5/3` — 「코조각주사」 (항목 이름 — 기법 표기 없음)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/5/3` — 「지방분해 성분(주로 데옥시콜산)이 콧망울 부위의 지방세포막을 파괴하여 지방을 분해시킵니다. 분해된 지방은 림프계를 통해 자연스럽게 배출되어 코의 윤곽이 날렵해집니다.」 (항목 기전 문장)
- `taxonomy.json:modality[].subcategories[].items[].name@15/5/4` — 「매끈V주사」 (항목 이름 — 기법 표기 없음)
- `taxonomy.json:modality[].subcategories[].items[].extracted.mechanism@15/5/4` — 「지방분해 성분이 턱 아래와 하관 부위의 지방세포막을 파괴하여 지방을 분해합니다. 동시에 콜라겐 생성을 촉진하여 피부 탄력을 개선하고 페이스 라인을 정돈합니다.」 (항목 기전 문장)
- … 외 8 곳(batch3.json evidence 전부)

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| intravenous_all | intravenous — 하위분류 항목 전부(9) | scope 9 항목 중 지금 technique=none 인 9 튜플의 technique 칸이 TEC-428b9bd04a(intravenous) 로 · R5 하위분류 M16-LIPO → intravenous 엣지(basis canonical_mapping)가 생긴다. 원장이 기법을 적지 않은 항목 9: V라인주사, 슈퍼투턱주사, 팻킬주사, 코조각주사, 매끈V주사, 다빼주사, 아큐주사, GPC주사, 빼당주사. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-LIPO` | 적용 |
| injection_all | injection — 하위분류 항목 전부(9) | scope 9 항목 중 지금 technique=none 인 9 튜플의 technique 칸이 TEC-545a700199(injection) 로 · R5 하위분류 M16-LIPO → injection 엣지(basis canonical_mapping)가 생긴다. 원장이 기법을 적지 않은 항목 9: V라인주사, 슈퍼투턱주사, 팻킬주사, 코조각주사, 매끈V주사, 다빼주사, 아큐주사, GPC주사, 빼당주사. | canonical_mapping `DEC-2026-11-05-B3B-TEC-M16-LIPO` | 적용 |
| keep | 지금대로(technique none) | 결정 없음 | 결정 없음 | — |

추천: **—** — 항목 원장 문장이 기법(정맥·근육·피하 주사)을 적지 않는다 — 하위분류 라벨·설명만으로는 기법을 정하지 않는다(추천 없음).

## site-synonyms — 해부 이름 → 부위 동의어(하위 6)

사용자 2026-11-05 「광경근→목 · 코끝→코 등」 — 미등록 조각에서 추출한 제안. 하위 항목마다 고른다.

### site-synonyms/01 — 해부 이름 「턱라인」 를 부위 「턱선」로 읽을까?

해부 이름·부위 조각이 부위 사전에 없어 미등록(⑧)이거나 사전 정합이 안 맞는다. 「교근 → 사각턱」(B3-SIT-01)과 같은 원칙으로 부위 동의어를 더할지 사람이 정한다.

**원장 원문**

- `market-pricing.json:categories[].items[].name@8/1` — 「울쎄라 (턱라인)」 (조각이 나오는 원장 자리(미등록 ⑧))
- `market-pricing.json:categories[].items[].name@8/3` — 「슈링크 유니버스 (턱라인)」 (조각이 나오는 원장 자리(미등록 ⑧))

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| propose | 「턱선」의 동의어로 턱라인 | 부위 사전 「턱선」(anatomical)에 동의어 턱라인 를 더한다 · 그 조각이 나오는 자리(시술 축 2)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-01` | 적용 |
| alt:턱 | 「턱」의 동의어로 턱라인 | 부위 사전 「턱」(anatomical)에 동의어 턱라인 를 더한다(후보 근거 — 부위 이름이 조각 안에 있음) · 그 조각이 나오는 자리(시술 축 2)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-01` | 적용 |
| alt:턱/턱선 | 「턱/턱선」의 동의어로 턱라인 | 부위 사전 「턱/턱선」(anatomical)에 동의어 턱라인 를 더한다(후보 근거 — 부위 이름이 조각 안에 있음) · 그 조각이 나오는 자리(시술 축 2)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-01` | 적용 |
| alt:이중턱/턱밑 | 「이중턱/턱밑」의 동의어로 턱라인 | 부위 사전 「이중턱/턱밑」(anatomical)에 동의어 턱라인 를 더한다(후보 근거 — 부위 이름이 조각 첫 글자로 시작) · 그 조각이 나오는 자리(시술 축 2)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-01` | 적용 |
| keep | 지금대로(미등록 유지) | 결정 없음 — ⑧ open 유지 | 결정 없음 | — |

추천: **—** — 해부 문서(anatomy-danger-zones)에 「턱라인」 가 없다 — 어느 부위인지 원장이 말하지 않는다(추천 없음).

### site-synonyms/02 — 해부 이름 「코끝」 를 부위 「코」로 읽을까?

해부 이름·부위 조각이 부위 사전에 없어 미등록(⑧)이거나 사전 정합이 안 맞는다. 「교근 → 사각턱」(B3-SIT-01)과 같은 원칙으로 부위 동의어를 더할지 사람이 정한다.

**원장 원문**

- `anatomy-danger-zones.json:zones[].nerves[].significance@4/0` — 「코끝, 코등 하부 감각」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `anatomy-danger-zones.json:zones[].botox_specific.target_muscle@4` — 「비근근 (Nasalis) — bunny lines, 코끝 처짐(depressor septi nasi)」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `extracted.json:{code}.indications.extended[]@M7/6` — 「코 리프팅 (코끝 올리기)」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `problem-packages.json:problems[].complaints[].cc_detail@0/0` — 「콧대/코끝」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `problem-packages.json:problems[].complaints[].cc_detail@0/1` — 「코끝 거상」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `synergy.json:links[].to@34` — 「M1-보톡스(코끝)」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `synergy.json:links[].reason@34` — 「코필러로 콧대 높이고 코끝 보톡스로 코끝 올려 세련된 코 라인」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `taxonomy.json:modality[].subcategories[].items[].name@0/2/6` — 「입꼬리/잇몸미소/코끝」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `taxonomy.json:modality[].subcategories[].items[].extracted.indications.primary[]@0/2/6/2` — 「코끝 처짐 교정」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `taxonomy.json:modality[].subcategories[].items[].extracted.indications.primary[]@6/2/11/2` — 「코끝 모양 개선」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `taxonomy.json:modality[].extracted.indications.extended[]@6/6` — 「코 리프팅 (코끝 올리기)」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `taxonomy.json:modality[].subcategories[].items[].extracted.indications.primary[]@15/5/3/1` — 「코끝이 뭉툭한 경우」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `taxonomy.json:problem[].subcategories[].items[].detail@0/0/0` — 「콧대/코끝」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `taxonomy.json:problem[].subcategories[].items[].detail@0/0/1` — 「코끝 거상」 (원장에 그 말이 나오는 자리(미등록 조각 아님))

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| **propose** | 「코」의 동의어로 코끝 | 부위 사전 「코」(anatomical)에 동의어 코끝 를 더한다 · 그 조각이 나오는 자리(미등록 조각 0)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-02` | 적용 |
| alt:코끝 | 「코끝」의 동의어로 코끝 | 부위 사전 「코끝」(anatomical)에 동의어 코끝 를 더한다(후보 근거 — 부위 이름이 조각 안에 있음) · 그 조각이 나오는 자리(미등록 조각 0)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-02` | 적용 |
| keep | 지금대로(미등록 유지) | 결정 없음 | 결정 없음 | — |

추천: **propose** — anatomy-danger-zones 의 「코」 zone 문장이 「코끝」 를 그 zone 안에서 적는다(다른 zone 에는 안 나온다).

### site-synonyms/03 — 해부 이름 「눈밑」, 「눈꺼풀」 를 부위 「눈 주변」로 읽을까?

해부 이름·부위 조각이 부위 사전에 없어 미등록(⑧)이거나 사전 정합이 안 맞는다. 「교근 → 사각턱」(B3-SIT-01)과 같은 원칙으로 부위 동의어를 더할지 사람이 정한다.

**원장 원문**

- `anatomy-danger-zones.json:zones[].botox_specific.target_muscle@3` — 「안륜근 (Orbicularis oculi) — 까마귀발, 눈밑 주름」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `anatomy-danger-zones.json:zones[].botox_specific.dose_range@3` — 「까마귀발 4-12U/측 (2-4포인트), 눈밑 1-2U (1포인트)」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `anatomy-danger-zones.json:zones[].botox_specific.risk@0` — 「눈꺼풀 처짐 (보톡스 확산 시 상안검거근 영향)」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `complications.json:categories[].complications[].mechanism@1/1` — 「주입 자체의 기계적 조직 확장 + 국소 염증반응 + HA의 친수성으로 인한 수분 유입. 모든 부위 공통이나, 눈밑·입술처럼 조직이 성긴 부위에서는 과다 부종으로 별도 부위특이 항목화(site_specific 참조).」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `complications.json:categories[].complications[].prevention@2/0` — 「PLLA: 적정 희석량(안면 8mL SWFI 이상, 필요 시 리도카인 추가)과 최소 라벨 기준 수화(부족 시 결절 위험), 균질 혼합, 심부(피하지방층/골막 상방) 분산 주입이 결절 예방의 핵심이며 24시간 이상 수화가 필수인 것은 아님. CaHA: 적절한 희석 비율. 얇은 피부 부위(」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `complications.json:categories[].complications[].mechanism@4/2` — 「열손상에 의한 혈관 투과성 증가로 간질액 저류. 모든 레이저 시술에서 공통으로 나타나는 급성 염증성 반응. 다만 눈꺼풀·입술 등 성긴 결합조직 부위에서 더 눈에 띄게 나타남」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `consent-checklist.json:categories[].mandatory_disclosures[]@0/2` — 「드물게 안검하수(눈꺼풀 처짐), 표정 비대칭이 발생할 수 있습니다」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `consent-checklist.json:categories[].contraindications[]@2/5` — 「입술, 눈꺼풀 등 얇은 피부 부위(PLLA)」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `extracted.json:{code}.indications.extended[]@M1/1` — 「눈밑주름」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `extracted.json:{code}.indications.extended[]@M2/1` — 「다크서클 교정 (눈밑 꺼짐)」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `extracted.json:{code}.indications.primary[]@M5/2` — 「꺼진 부위 볼륨 회복 (꺼진 볼, 꺼진 눈밑, 팔자주름 등)」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `extracted.json:{code}.indications.primary[]@M6/0` — 「얼굴 볼륨 회복 (나이가 들면서 꺼진 볼, 관자놀이, 눈밑 등)」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `extracted.json:{code}.safety.uncommon[]@M1/2` — 「윗눈꺼풀이나 눈썹이 처지는 현상」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `market-pricing.json:categories[].items[].name@1/6` — 「눈밑 꺼짐 (HA 1cc)」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- … 외 35 곳(batch3.json evidence 전부)

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| propose | 「눈 주변」의 동의어로 눈밑, 눈꺼풀 | 부위 사전 「눈 주변」(anatomical)에 동의어 눈밑, 눈꺼풀 를 더한다 · 그 조각이 나오는 자리(미등록 조각 0)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-03` | 적용 |
| alt:이마 | 「이마」의 동의어로 눈밑, 눈꺼풀 | 부위 사전 「이마」(anatomical)에 동의어 눈밑, 눈꺼풀 를 더한다(후보 근거 — zone 문장: 「눈꺼풀」) · 그 조각이 나오는 자리(미등록 조각 0)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-03` | 적용 |
| alt:눈가 | 「눈가」의 동의어로 눈밑, 눈꺼풀 | 부위 사전 「눈가」(anatomical)에 동의어 눈밑, 눈꺼풀 를 더한다(후보 근거 — 부위 이름이 조각 첫 글자로 시작) · 그 조각이 나오는 자리(미등록 조각 0)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-03` | 적용 |
| alt:눈밑 | 「눈밑」의 동의어로 눈밑, 눈꺼풀 | 부위 사전 「눈밑」(anatomical)에 동의어 눈밑, 눈꺼풀 를 더한다(후보 근거 — 부위 이름이 조각 첫 글자로 시작) · 그 조각이 나오는 자리(미등록 조각 0)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-03` | 적용 |
| keep | 지금대로(미등록 유지) | 결정 없음 | 결정 없음 | — |

추천: **—** — zone 문장이 「눈 주변」 zone 에 「눈밑」; 「이마」 zone 에 「눈꺼풀」 — 제안 부위 하나로 모이지 않는다(추천 없음).

### site-synonyms/04 — 해부 이름 「턱밑」, 「이중턱」 를 부위 「이중턱/턱밑」로 읽을까?

해부 이름·부위 조각이 부위 사전에 없어 미등록(⑧)이거나 사전 정합이 안 맞는다. 「교근 → 사각턱」(B3-SIT-01)과 같은 원칙으로 부위 동의어를 더할지 사람이 정한다.

**원장 원문**

- `market-pricing.json:categories[].items[].name@13/2` — 「쿨스컬프팅 (턱밑 이중턱)」 (조각이 나오는 원장 자리(미등록 ⑧))

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| propose | 「이중턱/턱밑」의 동의어로 턱밑, 이중턱 | 부위 사전 「이중턱/턱밑」(anatomical)에 동의어 턱밑, 이중턱 를 더한다 · 그 조각이 나오는 자리(시술 축 2)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-04` | 적용 |
| alt:턱 | 「턱」의 동의어로 턱밑, 이중턱 | 부위 사전 「턱」(anatomical)에 동의어 턱밑, 이중턱 를 더한다(후보 근거 — 부위 이름이 조각 안에 있음) · 그 조각이 나오는 자리(시술 축 2)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-04` | 적용 |
| alt:턱/턱선 | 「턱/턱선」의 동의어로 턱밑, 이중턱 | 부위 사전 「턱/턱선」(anatomical)에 동의어 턱밑, 이중턱 를 더한다(후보 근거 — 부위 이름이 조각 안에 있음) · 그 조각이 나오는 자리(시술 축 2)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-04` | 적용 |
| keep | 지금대로(미등록 유지) | 결정 없음 — ⑧ open 유지 | 결정 없음 | — |

추천: **—** — 해부 문서(anatomy-danger-zones)에 「턱밑」, 「이중턱」 가 없다 — 어느 부위인지 원장이 말하지 않는다(추천 없음).

### site-synonyms/05 — 해부 이름 「광경근」 를 부위 「목」로 읽을까?

해부 이름·부위 조각이 부위 사전에 없어 미등록(⑧)이거나 사전 정합이 안 맞는다. 「교근 → 사각턱」(B3-SIT-01)과 같은 원칙으로 부위 동의어를 더할지 사람이 정한다.

**원장 원문**

- `anatomy-danger-zones.json:zones[].botox_specific.target_muscle@9` — 「교근 (Masseter) — 사각턱, 광경근 (Platysma) — 턱선 리프트」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `anatomy-danger-zones.json:zones[].botox_specific.dose_range@9` — 「교근 25-50U/측, Nefertiti lift (광경근) 2-4U x 4-6포인트」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `anatomy-danger-zones.json:zones[].safe_injection_depth@10` — 「광경근(Platysma) 내 또는 피내 (진피층)」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `anatomy-danger-zones.json:zones[].tissue_data.platysma_coverage@10` — 「광경근은 쇄골~하악연까지, 정중선에서 결손 부위 있음」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `anatomy-danger-zones.json:zones[].tissue_data.notes@10` — 「광경근(Platysma) 하방에 외경정맥 등 주요 혈관 — 광경근 관통 주사 주의」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `anatomy-danger-zones.json:zones[].clinical_pearls[]@10/0` — 「광경근(Platysma) 하방에 주요 혈관/신경 → 피내 또는 광경근 내 주사」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `anatomy-danger-zones.json:zones[].clinical_pearls[]@10/2` — 「목 보톡스(Nefertiti lift)는 광경근 band에 소량 다점 주사」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `anatomy-danger-zones.json:zones[].botox_specific.target_muscle@10` — 「광경근 (Platysma) — platysmal bands, 목 주름」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `anatomy-danger-zones.json:zones[].botox_specific.safe_zone@10` — 「광경근 band 직상, 피하 표재성」 (원장에 그 말이 나오는 자리(미등록 조각 아님))
- `problem-combos.json:combos[].packages[].clinicalRationale@2/1` — 「HIFU(SMAS 열응고) + 보톡스(광경근 이완) = 올리는 힘 + 당기는 힘 제거. 가장 검증된 비수술 리프팅 조합」 (원장에 그 말이 나오는 자리(미등록 조각 아님))

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| propose | 「목」의 동의어로 광경근 | 부위 사전 「목」(anatomical)에 동의어 광경근 를 더한다 · 그 조각이 나오는 자리(미등록 조각 0)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-05` | 적용 |
| alt:턱선 | 「턱선」의 동의어로 광경근 | 부위 사전 「턱선」(anatomical)에 동의어 광경근 를 더한다(후보 근거 — zone 문장: 「광경근」) · 그 조각이 나오는 자리(미등록 조각 0)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-05` | 적용 |
| alt:볼/광대 | 「볼/광대」의 동의어로 광경근 | 부위 사전 「볼/광대」(anatomical)에 동의어 광경근 를 더한다(후보 근거 — 부위 이름이 조각 첫 글자로 시작) · 그 조각이 나오는 자리(미등록 조각 0)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-05` | 적용 |
| alt:광대 | 「광대」의 동의어로 광경근 | 부위 사전 「광대」(anatomical)에 동의어 광경근 를 더한다(후보 근거 — 부위 이름이 조각 첫 글자로 시작) · 그 조각이 나오는 자리(미등록 조각 0)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-05` | 적용 |
| keep | 지금대로(미등록 유지) | 결정 없음 | 결정 없음 | — |

추천: **—** — zone 문장이 「턱선」 zone 에 「광경근」; 「목」 zone 에 「광경근」 — 제안 부위 하나로 모이지 않는다(추천 없음).

### site-synonyms/06 — 부위 사전에 region 「바디」을 세울까?

해부 이름·부위 조각이 부위 사전에 없어 미등록(⑧)이거나 사전 정합이 안 맞는다. 「교근 → 사각턱」(B3-SIT-01)과 같은 원칙으로 부위 동의어를 더할지 사람이 정한다.

**원장 원문**

- `market-pricing.json:categories[].items[].name@9/5` — 「EMS 바디 (팔뚝/허벅지)」 (조각이 나오는 원장 자리(미등록 ⑧))
- `procedure-comparison.json:comparisons[].procedures[].name@6/3` — 「바넬라 (고주파 바디)」 (조각이 나오는 원장 자리(미등록 ⑧))
- `synergy.json:links[].to@20` — 「HIFES/EMS 바디」 (조각이 나오는 원장 자리(미등록 ⑧))
- `synergy.json:links[].to@21` — 「M9-인모드(바디)」 (조각이 나오는 원장 자리(미등록 ⑧))
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@7/0/1` — 「고주파 바디 RF」 (조각이 나오는 원장 자리(미등록 ⑧))
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@7/1/2` — 「바디 RF」 (조각이 나오는 원장 자리(미등록 ⑧))
- `treatment-optimization.json:by_concern[].severity_levels[].optimal_combo[]@7/2/1` — 「바디 HIFU(리포셀)」 (조각이 나오는 원장 자리(미등록 ⑧))

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| propose | 새 부위 「바디」(kind region) | 부위 사전에 새 값 「바디」(kind region · site_kind taxonomy_site_label)을 세운다 — SIT- 개체가 하나 는다 · 그 조각이 나오는 자리(시술 축 7)가 다시 분해된다 | dictionary_add `DEC-2026-11-05-B3B-SIT-06` | 적용 |
| keep | 지금대로(미등록 유지) | 결정 없음 — ⑧ open 유지 | 결정 없음 | — |

추천: **—** — 새 region 값(ERD §12 후보)이다 — 원장은 「바디」를 고민(problem P12)·목적 라벨로만 갖고 부위로 정하지 않는다(추천 없음).

## air-embolism-qualifier — complications 「공기색전·카테터 관련 감염」[M16]에 (색전, none, 공기) 수식 단위를 세울까?

V3-1 수식 칸으로 「공기색전」은 (색전 · 수식 공기)로 읽힌다(문구 「공기색전 의심」은 이미 그렇게 갈린다). 이 이름은 「카테터 관련」 조각 때문에 사건 하나로 다 읽히지 않는다 — 「카테터 관련」은 감염의 원인 문맥이고 사전 밖 조각이라 버릴지·사전에 넣을지는 사람이 정한다.

**원장 원문**

- `complications.json:categories[].complications[].name@M16/10` — 「공기색전·카테터 관련 감염」 (대상 complications 이름)
- `consent-checklist.json:categories[].emergency_signs[]@15/2` — 「흉통, 호흡곤란(수분 과부하 또는 공기색전 의심)」 (제안 근거)

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| assign | 지정 → (색전, none, 공기) + (감염, none, none) | 이 이름의 단위가 (색전, none, 공기) + (감염, none, none) 로 바뀐다((색전, none, 공기) 있는 단위, (감염, none, none) 있는 단위) · 「카테터 관련」 조각은 이 이름의 단위에 남지 않는다. 지금 (색전, none, 공기) + (감염, none, none) | adverse_tuple_assign `DEC-2026-11-05-B3B-ADV-01` | 적용 |
| keep | 지금대로((색전, none, 공기) + (감염, none, none)) | 결정 없음 | 결정 없음 | — |

추천: **—** — 원장은 「카테터 관련」을 어떻게 다룰지(버림·부위·수식) 말하지 않는다 — 감염 단위에서 그 조각을 빼는 판단이 남아 있다(추천 없음).

## records — 그 밖 기록·제안(하위 1)

빌더가 값을 바꾸지 않는 기록만 kind — 확인하면 결정 저장소에 approved 로 남는다.

### records/NEC-01 — 피부 괴사 → (괴사, 피부) — 기록으로 남길까?

표현 「피부 괴사 …」(post-procedure-timeline · taxonomy safety 등 20 남짓)도 (괴사, 피부)로 읽으려면 사건 사전 동의어 「피부 괴사」를 빼야 한다(그러면 「피부」 layer + 「괴사」로 갈린다) — 동의어 제거 kind 가 없다. 이번 묶음은 complications M14 이름만 지정(ADV-04)

**원장 원문**

- `post-procedure-timeline.json:timelines[].phases[].emergency[]@5/2/0` — 「피부 괴사」 (제안 근거)
- `complications.json:categories[].complications[].name@7/1` — 「피부 괴사 (Skin Necrosis / 동상·지방괴사, Frostbite·Fat Necrosis)」 (「피부 괴사」가 든 이름·표현)
- `extracted.json:{code}.safety.serious[]@M2/0` — 「혈관 막힘 (필러가 혈관에 들어가 피부 괴사를 일으킬 수 있음 — 드물지만 위험)」 (「피부 괴사」가 든 이름·표현)
- `extracted.json:{code}.safety.serious[]@M2/1` — 「시술 부위 피부 괴사 (혈류 차단으로 피부 조직이 죽는 것)」 (「피부 괴사」가 든 이름·표현)
- `extracted.json:{code}.safety.serious[]@M6/2` — 「혈관 막힘으로 인한 피부 괴사 (극히 드묾)」 (「피부 괴사」가 든 이름·표현)
- `taxonomy.json:modality[].extracted.safety.serious[]@1/0` — 「혈관 막힘 (필러가 혈관에 들어가 피부 괴사를 일으킬 수 있음 — 드물지만 위험)」 (「피부 괴사」가 든 이름·표현)
- `taxonomy.json:modality[].extracted.safety.serious[]@1/1` — 「시술 부위 피부 괴사 (혈류 차단으로 피부 조직이 죽는 것)」 (「피부 괴사」가 든 이름·표현)
- `taxonomy.json:modality[].extracted.safety.serious[]@5/2` — 「혈관 막힘으로 인한 피부 괴사 (극히 드묾)」 (「피부 괴사」가 든 이름·표현)
- `taxonomy.json:modality[].subcategories[].items[].extracted.safety.serious[]@15/4/0/1` — 「피부 괴사」 (「피부 괴사」가 든 이름·표현)
- `taxonomy.json:modality[].subcategories[].items[].extracted.safety.serious[]@15/4/1/2` — 「피부 괴사(드묾)」 (「피부 괴사」가 든 이름·표현)
- `taxonomy.json:modality[].subcategories[].items[].extracted.safety.serious[]@15/4/3/2` — 「피부 괴사(드묾)」 (「피부 괴사」가 든 이름·표현)
- `taxonomy.json:modality[].subcategories[].items[].extracted.safety.serious[]@15/4/4/2` — 「피부 괴사(드묾)」 (「피부 괴사」가 든 이름·표현)
- `taxonomy.json:modality[].subcategories[].items[].extracted.safety.serious[]@15/4/5/2` — 「피부 괴사(드묾)」 (「피부 괴사」가 든 이름·표현)
- `taxonomy.json:modality[].subcategories[].items[].extracted.safety.serious[]@15/4/6/2` — 「피부 괴사(드묾)」 (「피부 괴사」가 든 이름·표현)
- … 외 5 곳(batch3.json evidence 전부)

| 옵션 | 뜻 | 적용되면 | 결정 | 지금 빌더 |
|---|---|---|---|---|
| record | 기록만 확인 | 기록만 — 빌드 값은 바뀌지 않는다(결정 저장소에 approved 로 남고 적용 로그는 recorded) | scope_review `DEC-2026-11-05-B3B-NEC-01` | 적용 |
| keep | 지금대로(제안으로 둔다) | 결정 없음 | 결정 없음 | — |

추천: **—** — 기록만 kind — 값 판단이 아니라 ERD 개정 기록이라 사람이 확인한다(추천 없음).
