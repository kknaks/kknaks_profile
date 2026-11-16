# S05 — /categories/4 M5 PRP/자가혈

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/4/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S05.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/4` | [4] | object | (object, 자식 9) | 3015–3670 |  |  |
| `/categories/4/id` | id | string | "M5" | 3022–3024 | 제외(category_code) |  |
| `/categories/4/name` | name | string | "PRP/자가혈" | 3034–3041 | 3토큰 | E0217, E0218, E0219 |
| `/categories/4/patient_name` | patient_name | string | "내 혈액 재생 주사 (PRP)" | 3059–3075 | 8토큰 | E0220 |
| `/categories/4/simple_explanation` | simple_explanation | string | "본인의 피를 뽑아서 재생 성분만 모은 뒤, 피부에 다시 주사하는 시술입니다." | 3099–3141 | 23토큰 | E0221, E0222, E0223, E0224 |
| `/categories/4/how_it_works` | how_it_works | string | "팔에서 소량의 피를 뽑은 후, 원심분리기로 혈소판(상처 치유 성분)을 농축합니다. 이 농축액을 피부에 주사하면 성장인자가 피부 재생과 콜라겐 생성을 촉진합니다." | 3159–3248 | 45토큰 | E0225, E0226, E0227, E0228, E0229, E0230, E0231, E0232 |
| `/categories/4/duration_simple` | duration_simple | string | "효과 발현 2-4주, 약 3-6개월 지속됩니다." | 3269–3295 | 12토큰 | E0233, E0234, E0235 |
| `/categories/4/pain_level` | pain_level | string | "채혈 시 일반 혈액검사 정도, 주사 시 마취 크림 사용" | 3311–3341 | 12토큰 | E0236, E0237, E0238 |
| `/categories/4/downtime` | downtime | string | "붓기와 멍이 며칠 있을 수 있으나 일상생활 가능" | 3355–3381 | 13토큰 | E0239, E0240 |
| `/categories/4/common_concerns` | common_concerns | array | (array, 자식 3) | 3401–3669 |  |  |
| `/categories/4/common_concerns/0` | [0] | object | (object, 자식 2) | 3402–3503 |  |  |
| `/categories/4/common_concerns/0/q` | q | string | "내 피를 쓰니까 부작용이 없나요?" | 3408–3426 | 11토큰 | E0241 |
| `/categories/4/common_concerns/0/a` | a | string | "자신의 혈액을 사용하므로 알레르기나 거부반응 위험이 매우 낮습니다. 다만 주사 부위에 일시적 붓기나 멍은 있을 수 있어요." | 3433–3501 | 34토큰 | E0242, E0243, E0244, E0245, E0246 |
| `/categories/4/common_concerns/1` | [1] | object | (object, 자식 2) | 3504–3580 |  |  |
| `/categories/4/common_concerns/1/q` | q | string | "피를 많이 뽑나요?" | 3510–3520 | 6토큰 | E0247 |
| `/categories/4/common_concerns/1/a` | a | string | "10-20ml 정도로 건강검진 때 뽑는 양과 비슷합니다. 몸에 부담이 가지 않는 소량이에요." | 3527–3578 | 27토큰 | E0248, E0249, E0250, E0251, E0252 |
| `/categories/4/common_concerns/2` | [2] | object | (object, 자식 2) | 3581–3668 |  |  |
| `/categories/4/common_concerns/2/q` | q | string | "효과가 바로 나타나나요?" | 3587–3600 | 6토큰 | E0253 |
| `/categories/4/common_concerns/2/a` | a | string | "2-4주 후부터 서서히 효과가 나타납니다. 보통 2-3회 반복 시술하면 더 좋은 결과를 기대할 수 있어요." | 3607–3666 | 29토큰 | E0254, E0255, E0256, E0257, E0258 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S05-O1 | P | `/categories/4/how_it_works` | 부위 역할이 둘: 채혈 부위(팔)와 주사 부위(피부). 시술 대상 부위 자체는 「피부」로만 기재 |
| S05-O2 | B | `/categories/4/common_concerns/0/a` | 「매우 낮습니다」 수치·근거 미기재 |
| S05-O3 | P | `/categories/4/common_concerns/1/a` | how_it_works 「소량」의 수치가 이 값(10-20ml 정도)에 있다 — 같은 카테고리 안 값 간 대응(잠정) |
| S05-O4 | B | `/categories/4/common_concerns/2/a` | 반복 시술 간격 미기재 |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0217 | `/categories/4/name` | PRP/자가혈 | 0–7 | name,alternative | 「/」 두 호칭 — 관계 미확정 |
| E0218 | `/categories/4/name` | PRP | 0–3 | name |  |
| E0219 | `/categories/4/name` | 자가혈 | 4–7 | name |  |
| E0220 | `/categories/4/patient_name` | 내 혈액 재생 주사 (PRP) | 0–16 | name,substance,effect,route,paraphrase |  |
| E0221 | `/categories/4/simple_explanation` | 본인의 피를 뽑아서 재생 성분만 모은 뒤, 피부에 다시 주사하는 시술입니다. | 0–42 | sentence,sequence |  |
| E0222 | `/categories/4/simple_explanation` | 본인의 피 | 0–5 | substance |  |
| E0223 | `/categories/4/simple_explanation` | 재생 성분만 모은 뒤 | 11–22 | substance,scope,sequence |  |
| E0224 | `/categories/4/simple_explanation` | 피부에 다시 주사하는 | 24–35 | site,route |  |
| E0225 | `/categories/4/how_it_works` | 팔에서 소량의 피를 뽑은 후, 원심분리기로 혈소판(상처 치유 성분)을 농축합니다. | 0–45 | sentence,site,degree,device,substance,sequence |  |
| E0226 | `/categories/4/how_it_works` | 팔에서 | 0–3 | site | 채혈 부위(시술 대상 부위와 다른 역할) |
| E0227 | `/categories/4/how_it_works` | 소량의 피 | 4–9 | degree,quantity | 수치는 cc1 a 에 10-20ml |
| E0228 | `/categories/4/how_it_works` | 원심분리기 | 17–22 | device |  |
| E0229 | `/categories/4/how_it_works` | 혈소판(상처 치유 성분) | 24–37 | substance,paraphrase |  |
| E0230 | `/categories/4/how_it_works` | 이 농축액을 피부에 주사하면 성장인자가 피부 재생과 콜라겐 생성을 촉진합니다. | 46–89 | sentence,condition,mechanism,substance,effect |  |
| E0231 | `/categories/4/how_it_works` | 성장인자 | 62–66 | substance |  |
| E0232 | `/categories/4/how_it_works` | 소량의 피를 뽑은 후 | 4–15 | degree,time,sequence | regex 대조 후 보충(구절 누락 수정) |
| E0233 | `/categories/4/duration_simple` | 효과 발현 2-4주, 약 3-6개월 지속됩니다. | 0–26 | sentence,time,range,quantity,approx | 시간 역할: 발현·지속 |
| E0234 | `/categories/4/duration_simple` | 효과 발현 2-4주 | 0–10 | time,range,quantity |  |
| E0235 | `/categories/4/duration_simple` | 약 3-6개월 지속 | 12–22 | time,approx,range,quantity |  |
| E0236 | `/categories/4/pain_level` | 채혈 시 일반 혈액검사 정도, 주사 시 마취 크림 사용 | 0–30 | sensory,comparison,approx,time,substance | 통증을 단계(채혈/주사)별로 기재 |
| E0237 | `/categories/4/pain_level` | 채혈 시 일반 혈액검사 정도 | 0–15 | time,comparison,approx |  |
| E0238 | `/categories/4/pain_level` | 주사 시 마취 크림 사용 | 17–30 | time,substance |  |
| E0239 | `/categories/4/downtime` | 붓기와 멍이 며칠 있을 수 있으나 일상생활 가능 | 0–26 | adverse,time,approx,possibility |  |
| E0240 | `/categories/4/downtime` | 며칠 | 7–9 | time,approx | 수치 불명확 |
| E0241 | `/categories/4/common_concerns/0/q` | 내 피를 쓰니까 부작용이 없나요? | 0–18 | sentence,negation,adverse,rationale |  |
| E0242 | `/categories/4/common_concerns/0/a` | 자신의 혈액을 사용하므로 알레르기나 거부반응 위험이 매우 낮습니다. | 0–37 | sentence,rationale,adverse,degree |  |
| E0243 | `/categories/4/common_concerns/0/a` | 알레르기나 거부반응 위험이 매우 낮습니다 | 14–36 | adverse,degree,frequency | 수치 없음 |
| E0244 | `/categories/4/common_concerns/0/a` | 다만 주사 부위에 일시적 붓기나 멍은 있을 수 있어요. | 38–68 | sentence,site,course,adverse,possibility |  |
| E0245 | `/categories/4/common_concerns/0/a` | 일시적 붓기나 멍 | 48–57 | course,adverse |  |
| E0246 | `/categories/4/common_concerns/0/a` | 다만 | 38–40 | contrast | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0247 | `/categories/4/common_concerns/1/q` | 피를 많이 뽑나요? | 0–10 | sentence,degree |  |
| E0248 | `/categories/4/common_concerns/1/a` | 10-20ml 정도로 건강검진 때 뽑는 양과 비슷합니다. | 0–31 | sentence,quantity,range,approx,comparison |  |
| E0249 | `/categories/4/common_concerns/1/a` | 10-20ml 정도 | 0–10 | quantity,range,approx | 채혈량 |
| E0250 | `/categories/4/common_concerns/1/a` | 몸에 부담이 가지 않는 소량이에요. | 32–51 | sentence,negation,degree |  |
| E0251 | `/categories/4/common_concerns/1/a` | 몸에 부담이 가지 않는 | 32–44 | negation | regex 대조 후 보충(구절 누락 수정) |
| E0252 | `/categories/4/common_concerns/1/a` | 건강검진 때 뽑는 양과 비슷합니다 | 12–30 | comparison,quantity | regex 대조 후 보충(구절 누락 수정) |
| E0253 | `/categories/4/common_concerns/2/q` | 효과가 바로 나타나나요? | 0–13 | sentence,time,effect |  |
| E0254 | `/categories/4/common_concerns/2/a` | 2-4주 후부터 서서히 효과가 나타납니다. | 0–23 | sentence,time,range,quantity,manner,effect | 기준 시점 생략 |
| E0255 | `/categories/4/common_concerns/2/a` | 보통 2-3회 반복 시술하면 더 좋은 결과를 기대할 수 있어요. | 24–59 | sentence,frequency,range,quantity,condition,comparison,possibility |  |
| E0256 | `/categories/4/common_concerns/2/a` | 보통 2-3회 반복 시술하면 | 24–39 | frequency,range,quantity,condition | 간격 미기재 |
| E0257 | `/categories/4/common_concerns/2/a` | 더 좋은 결과를 기대할 수 있어요 | 40–58 | comparison,possibility,effect |  |
| E0258 | `/categories/4/common_concerns/2/a` | 2-4주 후부터 서서히 | 0–12 | time,range,quantity,manner | regex 대조 후 보충(구절 누락 수정) |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/4/name`: PRP/SL //SP 자가혈/NNP
- `/categories/4/patient_name`: 나/NP 의/JKG 혈액/NNG 재생/NNG 주사/NNG (/SSO PRP/SL )/SSC
- `/categories/4/simple_explanation`: 본인/NNG 의/JKG 피/NNG 를/JKO 뽑/VV-R 어서/EC 재생/NNG 성분/NNG 만/JX 모으/VV ᆫ/ETM 뒤/NNG ,/SP 피부/NNG 에/JKB 다시/MAG 주사/NNG 하/XSV 는/ETM 시술/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/4/how_it_works`: 팔/NNG 에서/JKB 소량/NNG 의/JKG 피/NNG 를/JKO 뽑/VV-R 은/ETM 후/NNG ,/SP 원심/NNG 분리기/NNG 로/JKB 혈소판/NNG (/SSO 상처/NNG 치유/NNG 성분/NNG )/SSC 을/JKO 농축/NNG 하/XSV ᆸ니다/EF ./SF 이/MM 농축액/NNG 을/JKO 피부/NNG 에/JKB 주사/NNG 하/XSV 면/EC 성장/NNG 인자/NNG 가/JKS 피부/NNG 재생/NNG 과/JC 콜라겐/NNP 생성/NNG 을/JKO 촉진/NNG 하/XSV ᆸ니다/EF ./SF
- `/categories/4/duration_simple`: 효과/NNG 발현/NNG 2-4/W_SERIAL 주/NNB ,/SP 약/MM 3-6/W_SERIAL 개월/NNB 지속/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/4/pain_level`: 채혈/NNG 시/NNB 일반/NNG 혈액/NNG 검사/NNG 정도/NNG ,/SP 주사/NNG 시/NNB 마취/NNG 크림/NNG 사용/NNG
- `/categories/4/downtime`: 붓/VV-I 기/ETN 와/JC 멍/NNG 이/JKS 며칠/NNG 있/VV 을/ETM 수/NNB 있/VA 으나/EC 일상생활/NNG 가능/NNG
- `/categories/4/common_concerns/0/q`: 나/NP 의/JKG 피/NNG 를/JKO 쓰/VV 니까/EC 부작용/NNG 이/JKS 없/VA 나요/EF ?/SF
- `/categories/4/common_concerns/0/a`: 자신/NNG 의/JKG 혈액/NNG 을/JKO 사용/NNG 하/XSV 므로/EC 알레르기/NNG 나/JC 거부/NNG 반응/NNG 위험/NNG 이/JKS 매우/MAG 낮/VA 습니다/EF ./SF 다만/MAG 주사/NNG 부위/NNG 에/JKB 일시/NNG 적/XSN 붓/VV-I 기/ETN 나/JC 멍/NNG 은/JX 있/VV 을/ETM 수/NNB 있/VA 어요/EF ./SF
- `/categories/4/common_concerns/1/q`: 피/NNG 를/JKO 많이/MAG 뽑/VV-R 나요/EF ?/SF
- `/categories/4/common_concerns/1/a`: 10-20/W_SERIAL ml/SL 정도/NNG 로/JKB 건강/NNG 검진/NNG 때/NNG 뽑/VV-R 는/ETM 양/NNG 과/JKB 비슷/XR 하/XSA ᆸ니다/EF ./SF 몸/NNG 에/JKB 부담/NNG 이/JKS 가/VV 지/EC 않/VX 는/ETM 소량/NNG 이/VCP 에요/EF ./SF
- `/categories/4/common_concerns/2/q`: 효과/NNG 가/JKS 바로/MAG 나타나/VV 나요/EF ?/SF
- `/categories/4/common_concerns/2/a`: 2-4/W_SERIAL 주/NNB 후/NNG 부터/JX 서서히/MAG 효과/NNG 가/JKS 나타나/VV ᆸ니다/EF ./SF 보통/MAG 2-3/W_SERIAL 회/NNB 반복/NNG 시술/NNG 하/XSV 면/EC 더/MAG 좋/VA 은/ETM 결과/NNG 를/JKO 기대/NNG 하/XSV ᆯ/ETM 수/NNB 있/VA 어요/EF ./SF
