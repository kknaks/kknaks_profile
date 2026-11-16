# S04 — /categories/3 M4 스킨부스터

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/3/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S04.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/3` | [3] | object | (object, 자식 9) | 2220–3014 |  |  |
| `/categories/3/id` | id | string | "M4" | 2227–2229 | 제외(category_code) |  |
| `/categories/3/name` | name | string | "스킨부스터" | 2239–2244 | 1토큰 | E0163 |
| `/categories/3/patient_name` | patient_name | string | "피부 재생 주사 (스킨부스터)" | 2262–2278 | 6토큰 | E0164 |
| `/categories/3/simple_explanation` | simple_explanation | string | "피부 속에 영양 성분을 직접 넣어주어 피부결과 탄력을 개선하는 주사입니다." | 2302–2343 | 23토큰 | E0165, E0166, E0167, E0168, E0169 |
| `/categories/3/how_it_works` | how_it_works | string | "피부 재생을 돕는 성분(히알루론산, PN 등)을 피부 얕은 층에 여러 번 주사합니다. 피부가 안쪽부터 촉촉해지고, 잔주름과 피부결이 개선됩니다." | 2361–2441 | 43토큰 | E0170, E0171, E0172, E0173, E0174, E0175, E0176, E0177, E0178, E0179 |
| `/categories/3/duration_simple` | duration_simple | string | "약 3-6개월 지속됩니다. 보통 2-3회 반복 시술합니다." | 2462–2494 | 15토큰 | E0180, E0181, E0182, E0183 |
| `/categories/3/pain_level` | pain_level | string | "가는 바늘로 여러 번 찔리는 따끔함, 마취 크림 사용" | 2510–2539 | 15토큰 | E0184, E0185, E0186, E0187 |
| `/categories/3/downtime` | downtime | string | "시술 부위에 자잘한 주사 자국이 1-2일, 일상생활 가능" | 2553–2584 | 14토큰 | E0188, E0189 |
| `/categories/3/common_concerns` | common_concerns | array | (array, 자식 3) | 2604–3013 |  |  |
| `/categories/3/common_concerns/0` | [0] | object | (object, 자식 2) | 2605–2719 |  |  |
| `/categories/3/common_concerns/0/q` | q | string | "스킨부스터와 필러는 같은 건가요?" | 2611–2629 | 11토큰 | E0190 |
| `/categories/3/common_concerns/0/a` | a | string | "다릅니다. 필러는 볼륨을 채우는 용도이고, 스킨부스터는 피부 자체의 질감과 탄력을 개선하는 용도예요. 스킨부스터는 더 묽은 제형을 얕게 넣습니다." | 2636–2717 | 41토큰 | E0191, E0192, E0193, E0194, E0195 |
| `/categories/3/common_concerns/1` | [1] | object | (object, 자식 2) | 2720–2911 |  |  |
| `/categories/3/common_concerns/1/q` | q | string | "리쥬란(연어주사)이 생선 알레르기와 관련 있나요?" | 2726–2753 | 13토큰 | E0196, E0197, E0198 |
| `/categories/3/common_concerns/1/a` | a | string | "리쥬란은 연어 DNA에서 추출한 성분(PN)으로, 고도로 정제되어 일반적으로 반응은 드뭅니다. 다만 연어·어류 등 심한 해산물(생선) 알레르기가 있는 분은 금기에 해당할 수 있으므로 시술 전 반드시 알레르기 이력을 의료진에게 알리고, 필요 시 대체 시술을 상의하세요." | 2760–2909 | 72토큰 | E0199, E0200, E0201, E0202, E0203, E0204, E0205, E0206, E0207, E0208 |
| `/categories/3/common_concerns/2` | [2] | object | (object, 자식 2) | 2912–3012 |  |  |
| `/categories/3/common_concerns/2/q` | q | string | "바르는 화장품보다 효과가 좋나요?" | 2918–2936 | 9토큰 | E0209, E0210 |
| `/categories/3/common_concerns/2/a` | a | string | "피부 속에 직접 성분을 넣어주기 때문에 흡수율이 화장품보다 훨씬 높습니다. 다만 화장품과 시술은 서로 보완하는 관계예요." | 2943–3010 | 34토큰 | E0211, E0212, E0213, E0214, E0215, E0216 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S04-O1 | P | `/categories/3/how_it_works` | 「여러 번 주사합니다」(한 회 안 다회 주사로 보임)와 duration_simple 「2-3회 반복 시술」(회차)은 다른 횟수 개념일 수 있다 — 잠정 |
| S04-O2 | P | `/categories/3/common_concerns/1/q` | 제품명 「리쥬란」이 카테고리 설명 안에 처음 등장. 「연어주사」는 통칭 |
| S04-O3 | P | `/categories/3/common_concerns/1/a` | 금기를 「해당할 수 있으므로」 가능성으로 표현 · 대상=「심한 해산물(생선) 알레르기가 있는 분」 · 시점=「시술 전」 행동 지시. 임상적으로 승인하지 않는다 |
| S04-O4 | B | `/categories/3/common_concerns/1/a` | 「반응」의 종류와 「드뭅니다」 빈도 수치 미기재 · 「대체 시술」 이름 미기재 |
| S04-O5 | B | `/categories/3/common_concerns/2/a` | 「흡수율이 … 훨씬 높습니다」 근거·수치 미기재 |
| S04-O6 | F | `/categories/3/common_concerns/1/a` | 리쥬란·PN 과 카테고리 스킨부스터의 관계(제품/성분/카테고리)는 다른 원장과 함께 후속 판단 |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0163 | `/categories/3/name` | 스킨부스터 | 0–5 | name |  |
| E0164 | `/categories/3/patient_name` | 피부 재생 주사 (스킨부스터) | 0–16 | name,effect,route,paraphrase | 괄호 안에 카테고리명 |
| E0165 | `/categories/3/simple_explanation` | 피부 속에 영양 성분을 직접 넣어주어 피부결과 탄력을 개선하는 주사입니다. | 0–41 | sentence |  |
| E0166 | `/categories/3/simple_explanation` | 피부 속에 | 0–5 | site,depth |  |
| E0167 | `/categories/3/simple_explanation` | 영양 성분 | 6–11 | substance | 성분명 미기재(how_it_works 에 예시) |
| E0168 | `/categories/3/simple_explanation` | 직접 넣어주어 | 13–20 | manner,route |  |
| E0169 | `/categories/3/simple_explanation` | 피부결과 탄력을 개선하는 | 21–34 | effect,concern |  |
| E0170 | `/categories/3/how_it_works` | 피부 재생을 돕는 성분(히알루론산, PN 등)을 피부 얕은 층에 여러 번 주사합니다. | 0–47 | sentence |  |
| E0171 | `/categories/3/how_it_works` | 피부 재생을 돕는 성분(히알루론산, PN 등) | 0–25 | substance,paraphrase | 괄호는 예시 목록 · 「등」 열린 목록 |
| E0172 | `/categories/3/how_it_works` | 히알루론산 | 13–18 | substance |  |
| E0173 | `/categories/3/how_it_works` | PN | 20–22 | substance,name | 약어 — 풀이 없음(S04 cc1 a 에 「연어 DNA에서 추출한 성분(PN)」) |
| E0174 | `/categories/3/how_it_works` | 피부 얕은 층에 | 27–35 | site,depth | 깊이 수식 「얕은」 — mm 아님 |
| E0175 | `/categories/3/how_it_works` | 여러 번 주사합니다 | 36–46 | frequency,route | 한 회 시술 안의 주사 횟수(잠정) |
| E0176 | `/categories/3/how_it_works` | 피부가 안쪽부터 촉촉해지고, 잔주름과 피부결이 개선됩니다. | 48–80 | sentence,effect |  |
| E0177 | `/categories/3/how_it_works` | 안쪽부터 | 52–56 | site,manner |  |
| E0178 | `/categories/3/how_it_works` | 잔주름과 피부결이 개선됩니다 | 64–79 | effect,concern |  |
| E0179 | `/categories/3/how_it_works` | 피부가 안쪽부터 촉촉해지고 | 48–62 | site,manner,effect | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0180 | `/categories/3/duration_simple` | 약 3-6개월 지속됩니다. | 0–14 | sentence,time,approx,range,quantity | 지속 대상 생략 |
| E0181 | `/categories/3/duration_simple` | 보통 2-3회 반복 시술합니다. | 15–32 | sentence,frequency,range,quantity | 간격 미기재 |
| E0182 | `/categories/3/duration_simple` | 약 3-6개월 | 0–7 | approx,range,quantity | regex 대조 후 보충(구절 누락 수정) |
| E0183 | `/categories/3/duration_simple` | 보통 2-3회 반복 시술 | 15–28 | frequency,range,quantity | 간격 미기재 · regex 대조 후 보충(구절 누락 수정) |
| E0184 | `/categories/3/pain_level` | 가는 바늘로 여러 번 찔리는 따끔함, 마취 크림 사용 | 0–29 | sensory,degree,frequency |  |
| E0185 | `/categories/3/pain_level` | 가는 바늘 | 0–5 | device,degree | 두께 수식 「가는」 — 바늘 굵기 |
| E0186 | `/categories/3/pain_level` | 여러 번 찔리는 따끔함 | 7–19 | frequency,sensory |  |
| E0187 | `/categories/3/pain_level` | 마취 크림 사용 | 21–29 | substance |  |
| E0188 | `/categories/3/downtime` | 시술 부위에 자잘한 주사 자국이 1-2일, 일상생활 가능 | 0–31 | site,adverse,degree,time,range,quantity,possibility |  |
| E0189 | `/categories/3/downtime` | 자잘한 주사 자국이 1-2일 | 7–22 | degree,adverse,time,range,quantity |  |
| E0190 | `/categories/3/common_concerns/0/q` | 스킨부스터와 필러는 같은 건가요? | 0–18 | sentence,comparison,reference |  |
| E0191 | `/categories/3/common_concerns/0/a` | 다릅니다. | 0–5 | negation,comparison |  |
| E0192 | `/categories/3/common_concerns/0/a` | 필러는 볼륨을 채우는 용도이고, 스킨부스터는 피부 자체의 질감과 탄력을 개선하는 용도예요. | 6–56 | sentence,comparison,reference,effect |  |
| E0193 | `/categories/3/common_concerns/0/a` | 스킨부스터는 더 묽은 제형을 얕게 넣습니다. | 57–81 | sentence,comparison,degree,depth |  |
| E0194 | `/categories/3/common_concerns/0/a` | 더 묽은 제형 | 64–71 | comparison,degree,substance | 비교 대상(필러) 생략 |
| E0195 | `/categories/3/common_concerns/0/a` | 얕게 | 73–75 | depth | 깊이 수식 — 수치 없음 |
| E0196 | `/categories/3/common_concerns/1/q` | 리쥬란(연어주사)이 생선 알레르기와 관련 있나요? | 0–27 | sentence,name,paraphrase,adverse |  |
| E0197 | `/categories/3/common_concerns/1/q` | 리쥬란(연어주사) | 0–9 | name,paraphrase | 제품명+통칭 |
| E0198 | `/categories/3/common_concerns/1/q` | 생선 알레르기 | 11–18 | adverse,condition |  |
| E0199 | `/categories/3/common_concerns/1/a` | 리쥬란은 연어 DNA에서 추출한 성분(PN)으로, 고도로 정제되어 일반적으로 반응은 드뭅니다. | 0–52 | sentence,name,substance,frequency |  |
| E0200 | `/categories/3/common_concerns/1/a` | 연어 DNA에서 추출한 성분(PN) | 5–24 | substance,paraphrase |  |
| E0201 | `/categories/3/common_concerns/1/a` | 고도로 정제되어 | 28–36 | degree,rationale |  |
| E0202 | `/categories/3/common_concerns/1/a` | 일반적으로 반응은 드뭅니다 | 37–51 | frequency,adverse | 「반응」 종류 미특정 · 수치 없음 |
| E0203 | `/categories/3/common_concerns/1/a` | 다만 연어·어류 등 심한 해산물(생선) 알레르기가 있는 분은 금기에 해당할 수 있으므로 시술 전 반드시 알레르기 이력을 의료진에게 알리고, 필요 시 대체 시술을 상의하세요. | 53–149 | sentence,target,condition,contraindication,possibility,instruction,time |  |
| E0204 | `/categories/3/common_concerns/1/a` | 연어·어류 등 심한 해산물(생선) 알레르기가 있는 분 | 56–85 | target,condition,degree | 대상 집단 · 「심한」 정도 조건 |
| E0205 | `/categories/3/common_concerns/1/a` | 금기에 해당할 수 있으므로 | 87–101 | contraindication,possibility | 금기를 가능성으로 표현 |
| E0206 | `/categories/3/common_concerns/1/a` | 시술 전 반드시 알레르기 이력을 의료진에게 알리고 | 102–129 | time,instruction,actor |  |
| E0207 | `/categories/3/common_concerns/1/a` | 필요 시 대체 시술을 상의하세요 | 131–148 | condition,instruction | 대체 시술 이름 미기재 |
| E0208 | `/categories/3/common_concerns/1/a` | 다만 | 53–55 | contrast,condition | 예외·주의 도입 · 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0209 | `/categories/3/common_concerns/2/q` | 바르는 화장품보다 효과가 좋나요? | 0–18 | sentence,comparison |  |
| E0210 | `/categories/3/common_concerns/2/q` | 바르는 화장품보다 | 0–9 | comparison,route | regex 대조 후 보충(구절 누락 수정) |
| E0211 | `/categories/3/common_concerns/2/a` | 피부 속에 직접 성분을 넣어주기 때문에 흡수율이 화장품보다 훨씬 높습니다. | 0–41 | sentence,rationale,comparison,degree |  |
| E0212 | `/categories/3/common_concerns/2/a` | 흡수율이 화장품보다 훨씬 높습니다 | 22–40 | comparison,degree | 수치 없음 |
| E0213 | `/categories/3/common_concerns/2/a` | 다만 화장품과 시술은 서로 보완하는 관계예요. | 42–67 | sentence,relation |  |
| E0214 | `/categories/3/common_concerns/2/a` | 서로 보완하는 관계 | 54–64 | relation |  |
| E0215 | `/categories/3/common_concerns/2/a` | 직접 성분을 넣어주기 때문에 | 6–21 | manner,rationale | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0216 | `/categories/3/common_concerns/2/a` | 다만 | 42–44 | contrast | 별도 읽기 검토(형태소 수식어 대조)로 보충 |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/3/name`: 스킨부스터/NNG
- `/categories/3/patient_name`: 피부/NNG 재생/NNG 주사/NNG (/SSO 스킨부스터/NNP )/SSC
- `/categories/3/simple_explanation`: 피부/NNG 속/NNG 에/JKB 영양/NNG 성분/NNG 을/JKO 직접/MAG 넣/VV 어/EC 주/VX 어/EC 피부/NNG 결/NNG 과/JC 탄력/NNG 을/JKO 개선/NNG 하/XSV 는/ETM 주사/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/3/how_it_works`: 피부/NNG 재생/NNG 을/JKO 돕/VV-I 는/ETM 성분/NNG (/SSO 히알루론산/NNP ,/SP PN/SL 등/NNB )/SSC 을/JKO 피부/NNG 얕/VA 은/ETM 층/NNG 에/JKB 여러/MM 번/NNB 주사/NNG 하/XSV ᆸ니다/EF ./SF 피부/NNG 가/JKS 안쪽/NNG 부터/JX 촉촉/XR 하/XSA 어/EC 지/VX 고/EC ,/SP 잔주름/NNG 과/JC 피부/NNG 결/NNG 이/JKS 개선/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/3/duration_simple`: 약/MM 3-6/W_SERIAL 개월/NNB 지속/NNG 되/XSV ᆸ니다/EF ./SF 보통/MAG 2-3/W_SERIAL 회/NNB 반복/NNG 시술/NNG 하/XSV ᆸ니다/EF ./SF
- `/categories/3/pain_level`: 가늘/VA ᆫ/ETM 바늘/NNG 로/JKB 여러/MM 번/NNB 찔리/VV 는/ETM 따끔/MAG 하/XSA ᆷ/ETN ,/SP 마취/NNG 크림/NNG 사용/NNG
- `/categories/3/downtime`: 시술/NNG 부위/NNG 에/JKB 자잘/XR 하/XSA ᆫ/ETM 주사/NNG 자국/NNG 이/JKS 1-2/W_SERIAL 일/NNG ,/SP 일상생활/NNG 가능/NNG
- `/categories/3/common_concerns/0/q`: 스킨부스터/NNG 와/JC 필러/NNP 는/JX 같/VA 은/ETM 거/NNB 이/VCP ᆫ가/EF 요/JX ?/SF
- `/categories/3/common_concerns/0/a`: 다르/VA ᆸ니다/EF ./SF 필러/NNP 는/JX 볼륨/NNG 을/JKO 채우/VV 는/ETM 용도/NNG 이/VCP 고/EC ,/SP 스킨부스터/NNP 는/JX 피부/NNG 자체/NNG 의/JKG 질감/NNG 과/JC 탄력/NNG 을/JKO 개선/NNG 하/XSV 는/ETM 용도/NNG 이/VCP 예요/EF ./SF 스킨부스터/NNG 는/JX 더/MAG 묽/VA 은/ETM 제형/NNG 을/JKO 얕/VA 게/EC 넣/VV 습니다/EF ./SF
- `/categories/3/common_concerns/1/q`: 리쥬/NNG 란/JX (/SSO 연어주사/NNP )/SSC 이/JKS 생선/NNG 알레르기/NNG 와/JKB 관련/NNG 있/VA 나요/EF ?/SF
- `/categories/3/common_concerns/1/a`: 리쥬란/NNG 은/JX 연어/NNG DNA/SL 에서/JKB 추출/NNG 하/XSV ᆫ/ETM 성분/NNG (/SSO PN/SL )/SSC 으로/JKB ,/SP 고도/NNG 로/JKB 정제/NNG 되/XSV 어/EC 일반/NNG 적/XSN 으로/JKB 반응/NNG 은/JX 드물/VA ᆸ니다/EF ./SF 다만/MAG 연어/NNG ·/SP 어류/NNG 등/NNB 심하/VA ᆫ/ETM 해산물/NNG (/SSO 생선/NNG )/SSC 알레르기/NNG 가/JKS 있/VV 는/ETM 분/NNB 은/JX 금기/NNG 에/JKB 해당/NNG 하/XSV ᆯ/ETM 수/NNB 있/VA 으므로/EC 시술/NNG 전/NNG 반드시/MAG 알레르기/NNG 이력/NNG 을/JKO 의료진/NNG 에게/JKB 알리/VV 고/EC ,/SP 필요/NNG 시/NNB 대체/NNG 시술/NNG 을/JKO 상의/NNG 하/XSV 세요/EF ./SF
- `/categories/3/common_concerns/2/q`: 바르/VV 는/ETM 화장품/NNG 보다/JKB 효과/NNG 가/JKS 좋/VA 나요/EF ?/SF
- `/categories/3/common_concerns/2/a`: 피부/NNG 속/NNG 에/JKB 직접/MAG 성분/NNG 을/JKO 넣/VV 어/EC 주/VX 기/ETN 때문/NNB 에/JKB 흡수/NNG 율/XSN 이/JKS 화장품/NNG 보다/JKB 훨씬/MAG 높/VA 습니다/EF ./SF 다만/MAG 화장품/NNG 과/JC 시술/NNG 은/JX 서로/MAG 보완/NNG 하/XSV 는/ETM 관계/NNG 이/VCP 예요/EF ./SF

알려진 오분절(출현별, 교정 안 함):

- `/categories/3/common_concerns/1/q` 「리쥬란」 [0,3) → 리쥬/NNG 란/JX — 제품명이 「리쥬」+조사 「란」으로 분해 — 토큰 기준 제품명 검색 누락. 같은 카테고리 a 의 「리쥬란은」은 정상(출현별 불일치)
