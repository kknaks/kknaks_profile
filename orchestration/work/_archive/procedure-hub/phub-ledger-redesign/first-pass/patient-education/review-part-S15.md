# S15 — /categories/14 M15 메디컬스킨케어

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/14/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S15.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/14` | [14] | object | (object, 자식 9) | 10390–11172 |  |  |
| `/categories/14/id` | id | string | "M15" | 10397–10400 | 제외(category_code) |  |
| `/categories/14/name` | name | string | "메디컬스킨케어" | 10410–10417 | 3토큰 | E0662 |
| `/categories/14/patient_name` | patient_name | string | "메디컬 피부 관리 (필링/스케일링 등)" | 10435–10456 | 10토큰 | E0663, E0664, E0665 |
| `/categories/14/simple_explanation` | simple_explanation | string | "의료 전문가가 시행하는 전문 피부 관리로, 필링, 약물 도포, 수분 관리 등을 포함합니다." | 10480–10530 | 25토큰 | E0666, E0667, E0668 |
| `/categories/14/how_it_works` | how_it_works | string | "피부 상태에 맞는 의약 성분(AHA, BHA, TCA 등)을 사용하여 묵은 각질을 제거하거나, 전문 기기로 약물을 피부 깊이 전달합니다. 피부 턴오버를 촉진하고 트러블, 색소, 모공 등을 개선합니다." | 10548–10659 | 56토큰 | E0669, E0670, E0671, E0672, E0673, E0674, E0675, E0676, E0677 |
| `/categories/14/duration_simple` | duration_simple | string | "시술 종류에 따라 다릅니다. 가벼운 필링은 주 1회, 깊은 필링은 수 주 간격으로 반복합니다." | 10680–10732 | 28토큰 | E0678, E0679, E0680, E0681 |
| `/categories/14/pain_level` | pain_level | string | "가벼운 필링은 약간의 따끔함, 깊은 필링은 열감이나 화끈거림" | 10748–10781 | 19토큰 | E0682, E0683, E0684 |
| `/categories/14/downtime` | downtime | string | "가벼운 필링: 거의 없음 / 중간 필링: 각질 벗겨짐 3-7일 / 깊은 필링: 1-2주" | 10795–10843 | 23토큰 | E0685, E0686, E0687, E0688 |
| `/categories/14/common_concerns` | common_concerns | array | (array, 자식 3) | 10863–11171 |  |  |
| `/categories/14/common_concerns/0` | [0] | object | (object, 자식 2) | 10864–10969 |  |  |
| `/categories/14/common_concerns/0/q` | q | string | "필링 후 피부가 벗겨지는 게 정상인가요?" | 10870–10892 | 12토큰 | E0689 |
| `/categories/14/common_concerns/0/a` | a | string | "네, 묵은 각질이 벗겨지고 새로운 피부가 나오는 정상적인 과정이에요. 억지로 벗기지 말고 자연스럽게 떨어지길 기다려주세요." | 10899–10967 | 38토큰 | E0690, E0691, E0692, E0693, E0694 |
| `/categories/14/common_concerns/1` | [1] | object | (object, 자식 2) | 10970–11059 |  |  |
| `/categories/14/common_concerns/1/q` | q | string | "필링이 피부를 얇게 만드나요?" | 10976–10992 | 9토큰 | E0695, E0696 |
| `/categories/14/common_concerns/1/a` | a | string | "적절한 농도와 간격으로 시술하면 오히려 피부 재생을 촉진합니다. 과도하게 자주 받지 않는 것이 중요해요." | 10999–11057 | 32토큰 | E0697, E0698, E0699, E0700, E0701 |
| `/categories/14/common_concerns/2` | [2] | object | (object, 자식 2) | 11060–11170 |  |  |
| `/categories/14/common_concerns/2/q` | q | string | "집에서 하는 필링과 병원 필링은 다른가요?" | 11066–11089 | 14토큰 | E0702 |
| `/categories/14/common_concerns/2/a` | a | string | "병원에서는 더 높은 농도의 전문 약품을 사용하고, 의사가 피부 상태를 보며 농도와 시간을 조절합니다. 효과와 안전성 모두 높아요." | 11096–11168 | 38토큰 | E0703, E0704, E0705, E0706 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S15-O1 | P | `/categories/14/downtime` | 세분 축이 「가벼운/중간/깊은 필링」 — duration_simple·pain_level 은 「가벼운/깊은」 2단, downtime 은 3단(중간 추가). 「깊은 필링: 1-2주」는 무엇의 기간인지 생략(B) |
| S15-O2 | P | `/categories/14/common_concerns/1/a` | S08 cc0 a 와 거의 같은 문형(적절한 …와 간격으로 시술하면 오히려 … 과도하게 자주 받지 않는 것이 중요) — 다른 카테고리 간 반복 문형. 병합하지 않는다 |
| S15-O3 | B | `/categories/14/how_it_works` | AHA·BHA·TCA 풀이·농도 미기재 · 전문 기기 이름 미기재 |
| S15-O4 | B | `/categories/14/common_concerns/2/a` | 「효과와 안전성 모두 높아요」 근거 미기재 |
| S15-O5 | P | `/categories/14/duration_simple` | 「가벼운」은 정도, 「깊은」은 깊이 수식으로 필링 종류를 가른다 — 정도/깊이 축 혼재(잠정) |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0662 | `/categories/14/name` | 메디컬스킨케어 | 0–7 | name |  |
| E0663 | `/categories/14/patient_name` | 메디컬 피부 관리 (필링/스케일링 등) | 0–21 | name,paraphrase | 괄호 「/」 나열 · 「등」 |
| E0664 | `/categories/14/patient_name` | 필링 | 11–13 | name |  |
| E0665 | `/categories/14/patient_name` | 스케일링 | 14–18 | name |  |
| E0666 | `/categories/14/simple_explanation` | 의료 전문가가 시행하는 전문 피부 관리로, 필링, 약물 도포, 수분 관리 등을 포함합니다. | 0–50 | sentence,actor,name,scope |  |
| E0667 | `/categories/14/simple_explanation` | 의료 전문가가 시행하는 | 0–12 | actor |  |
| E0668 | `/categories/14/simple_explanation` | 필링, 약물 도포, 수분 관리 등을 포함합니다 | 24–49 | name,scope | 구성 나열 · 「등」 |
| E0669 | `/categories/14/how_it_works` | 피부 상태에 맞는 의약 성분(AHA, BHA, TCA 등)을 사용하여 묵은 각질을 제거하거나, 전문 기기로 약물을 피부 깊이 전달합니다. | 0–76 | sentence,condition,substance,paraphrase,mechanism,device,depth |  |
| E0670 | `/categories/14/how_it_works` | 피부 상태에 맞는 | 0–9 | condition |  |
| E0671 | `/categories/14/how_it_works` | 의약 성분(AHA, BHA, TCA 등) | 10–32 | substance,paraphrase | 약어 나열 · 풀이 없음 · 「등」 |
| E0672 | `/categories/14/how_it_works` | AHA | 16–19 | substance |  |
| E0673 | `/categories/14/how_it_works` | BHA | 21–24 | substance |  |
| E0674 | `/categories/14/how_it_works` | TCA | 26–29 | substance |  |
| E0675 | `/categories/14/how_it_works` | 전문 기기로 약물을 피부 깊이 전달합니다 | 53–75 | device,substance,depth | 기기·약물 이름 미기재 |
| E0676 | `/categories/14/how_it_works` | 피부 턴오버를 촉진하고 트러블, 색소, 모공 등을 개선합니다. | 77–111 | sentence,mechanism,concern,effect |  |
| E0677 | `/categories/14/how_it_works` | 트러블, 색소, 모공 등 | 90–103 | concern | 「등」 |
| E0678 | `/categories/14/duration_simple` | 시술 종류에 따라 다릅니다. | 0–15 | sentence,condition |  |
| E0679 | `/categories/14/duration_simple` | 가벼운 필링은 주 1회, 깊은 필링은 수 주 간격으로 반복합니다. | 16–52 | sentence,degree,depth,name,frequency,time,quantity,approx |  |
| E0680 | `/categories/14/duration_simple` | 가벼운 필링은 주 1회 | 16–28 | degree,name,frequency,time,quantity |  |
| E0681 | `/categories/14/duration_simple` | 깊은 필링은 수 주 간격으로 | 30–45 | depth,name,time,approx | 「수 주」 불명확 |
| E0682 | `/categories/14/pain_level` | 가벼운 필링은 약간의 따끔함, 깊은 필링은 열감이나 화끈거림 | 0–33 | degree,depth,name,sensory |  |
| E0683 | `/categories/14/pain_level` | 가벼운 필링은 약간의 따끔함 | 0–15 | degree,name,sensory |  |
| E0684 | `/categories/14/pain_level` | 깊은 필링은 열감이나 화끈거림 | 17–33 | depth,name,sensory |  |
| E0685 | `/categories/14/downtime` | 가벼운 필링: 거의 없음 / 중간 필링: 각질 벗겨짐 3-7일 / 깊은 필링: 1-2주 | 0–48 | degree,depth,name,negation,adverse,time,range,quantity | 「 / 」 종류 구분자 |
| E0686 | `/categories/14/downtime` | 가벼운 필링: 거의 없음 | 0–13 | degree,name,negation |  |
| E0687 | `/categories/14/downtime` | 중간 필링: 각질 벗겨짐 3-7일 | 16–34 | degree,name,adverse,time,range,quantity |  |
| E0688 | `/categories/14/downtime` | 깊은 필링: 1-2주 | 37–48 | depth,name,time,range,quantity | 무엇의 기간인지 생략 |
| E0689 | `/categories/14/common_concerns/0/q` | 필링 후 피부가 벗겨지는 게 정상인가요? | 0–22 | sentence,time,adverse |  |
| E0690 | `/categories/14/common_concerns/0/a` | 네, 묵은 각질이 벗겨지고 새로운 피부가 나오는 정상적인 과정이에요. | 0–38 | sentence,course,mechanism |  |
| E0691 | `/categories/14/common_concerns/0/a` | 억지로 벗기지 말고 자연스럽게 떨어지길 기다려주세요. | 39–68 | sentence,avoid,negation,instruction,manner |  |
| E0692 | `/categories/14/common_concerns/0/a` | 억지로 벗기지 말고 | 39–49 | avoid,negation,degree |  |
| E0693 | `/categories/14/common_concerns/0/a` | 자연스럽게 떨어지길 기다려주세요 | 50–67 | manner,instruction | regex 대조 후 보충(구절 누락 수정) |
| E0694 | `/categories/14/common_concerns/0/a` | 정상적인 과정 | 27–34 | course | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0695 | `/categories/14/common_concerns/1/q` | 필링이 피부를 얇게 만드나요? | 0–16 | sentence,thickness,adverse |  |
| E0696 | `/categories/14/common_concerns/1/q` | 피부를 얇게 | 4–10 | thickness,adverse | 피부 두께 |
| E0697 | `/categories/14/common_concerns/1/a` | 적절한 농도와 간격으로 시술하면 오히려 피부 재생을 촉진합니다. | 0–35 | sentence,condition,degree,time,comparison,effect |  |
| E0698 | `/categories/14/common_concerns/1/a` | 적절한 농도와 간격으로 시술하면 | 0–17 | condition,degree,time | 기준 미기재 |
| E0699 | `/categories/14/common_concerns/1/a` | 과도하게 자주 받지 않는 것이 중요해요. | 36–58 | sentence,degree,frequency,negation,instruction |  |
| E0700 | `/categories/14/common_concerns/1/a` | 오히려 피부 재생을 촉진합니다 | 18–34 | comparison,effect | regex 대조 후 보충(구절 누락 수정) |
| E0701 | `/categories/14/common_concerns/1/a` | 과도하게 자주 받지 않는 것이 중요해요 | 36–57 | degree,frequency,negation,instruction | regex 대조 후 보충(구절 누락 수정) |
| E0702 | `/categories/14/common_concerns/2/q` | 집에서 하는 필링과 병원 필링은 다른가요? | 0–23 | sentence,place,comparison |  |
| E0703 | `/categories/14/common_concerns/2/a` | 병원에서는 더 높은 농도의 전문 약품을 사용하고, 의사가 피부 상태를 보며 농도와 시간을 조절합니다. | 0–56 | sentence,place,comparison,degree,substance,actor,condition |  |
| E0704 | `/categories/14/common_concerns/2/a` | 더 높은 농도의 전문 약품 | 6–20 | comparison,degree,substance | 수치 미기재 |
| E0705 | `/categories/14/common_concerns/2/a` | 농도와 시간을 조절합니다 | 42–55 | degree,time,management |  |
| E0706 | `/categories/14/common_concerns/2/a` | 효과와 안전성 모두 높아요. | 57–72 | sentence,comparison,effect | 근거 미기재 |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/14/name`: 메디컬/NNG 스킨/NNG 케어/NNG
- `/categories/14/patient_name`: 메디컬/NNG 피부/NNG 관리/NNG (/SSO 필/NNG 링/NNG //SP 스케일링/NNP 등/NNB )/SSC
- `/categories/14/simple_explanation`: 의료/NNG 전문가/NNG 가/JKS 시행/NNG 하/XSV 는/ETM 전문/NNG 피부/NNG 관리/NNG 로/JKB ,/SP 필/NNP 링/NNG ,/SP 약물/NNG 도포/NNG ,/SP 수분/NNG 관리/NNG 등/NNB 을/JKO 포함/NNG 하/XSV ᆸ니다/EF ./SF
- `/categories/14/how_it_works`: 피부/NNG 상태/NNG 에/JKB 맞/VV 는/ETM 의약/NNG 성분/NNG (/SSO AHA/SL ,/SP BHA/SL ,/SP TCA/SL 등/NNB )/SSC 을/JKO 사용/NNG 하/XSV 어/EC 묵/VV 은/ETM 각질/NNG 을/JKO 제거/NNG 하/XSV 거나/EC ,/SP 전문/NNG 기기/NNG 로/JKB 약물/NNG 을/JKO 피부/NNG 깊이/MAG 전달/NNG 하/XSV ᆸ니다/EF ./SF 피부/NNG 턴/NNG 오버/NNG 를/JKO 촉진/NNG 하/XSV 고/EC 트러블/NNG ,/SP 색소/NNG ,/SP 모공/NNG 등/NNB 을/JKO 개선/NNG 하/XSV ᆸ니다/EF ./SF
- `/categories/14/duration_simple`: 시술/NNG 종류/NNG 에/JKB 따르/VV 어/EC 다르/VA ᆸ니다/EF ./SF 가볍/VA-I 은/ETM 필링/NNG 은/JX 주/NNG 1/SN 회/NNB ,/SP 깊/VA 은/ETM 필링/NNG 은/JX 수/MM 주/NNB 간격/NNG 으로/JKB 반복/NNG 하/XSV ᆸ니다/EF ./SF
- `/categories/14/pain_level`: 가볍/VA-I 은/ETM 필링/NNG 은/JX 약간/NNG 의/JKG 따끔/MAG 하/XSA ᆷ/ETN ,/SP 깊/VA 은/ETM 필링/NNG 은/JX 열/NNG 감/XSN 이나/JC 화끈거리/VV ᆷ/EF
- `/categories/14/downtime`: 가볍/VA-I 은/ETM 필링/NNG :/SP 거의/MAG 없/VA 음/ETN //SP 중간/NNG 필링/NNG :/SP 각질/NNG 벗겨지/VV ᆷ/ETN 3-7/W_SERIAL 일/NNB //SP 깊/VA 은/ETM 필링/NNG :/SP 1-2/W_SERIAL 주/NNB
- `/categories/14/common_concerns/0/q`: 필링/NNG 후/NNG 피부/NNG 가/JKS 벗겨지/VV 는/ETM 것/NNB 이/JKS 정상/NNG 이/VCP ᆫ가요/EF ?/SF
- `/categories/14/common_concerns/0/a`: 네/IC ,/SP 묵/VV 은/ETM 각질/NNG 이/JKS 벗겨지/VV 고/EC 새롭/VA-I 은/ETM 피부/NNG 가/JKS 나오/VV 는/ETM 정상/NNG 적/XSN 이/VCP ᆫ/ETM 과정/NNG 이/VCP 에요/EF ./SF 억지로/MAG 벗기/VV 지/EC 말/VX 고/EC 자연/NNG 스럽/XSA-I 게/EC 떨어지/VV 기/ETN ᆯ/JKO 기다리/VV 어/EC 주/VX 세요/EF ./SF
- `/categories/14/common_concerns/1/q`: 필링/NNG 이/JKS 피부/NNG 를/JKO 얇/VA 게/EC 만들/VV 나요/EF ?/SF
- `/categories/14/common_concerns/1/a`: 적절/XR 하/XSA ᆫ/ETM 농도/NNG 와/JC 간격/NNG 으로/JKB 시술/NNG 하/XSV 면/EC 오히려/MAG 피부/NNG 재생/NNG 을/JKO 촉진/NNG 하/XSV ᆸ니다/EF ./SF 과도/NNG 하/XSA 게/EC 자주/MAG 받/VV-R 지/EC 않/VX 는/ETM 것/NNB 이/JKS 중요/NNG 하/XSA 어요/EF ./SF
- `/categories/14/common_concerns/2/q`: 집/NNG 에서/JKB 하/VV 는/ETM 필/NNP 링/NNG 과/JC 병원/NNG 필링/NNG 은/JX 다르/VA ᆫ가/EF 요/JX ?/SF
- `/categories/14/common_concerns/2/a`: 병원/NNG 에서/JKB 는/JX 더/MAG 높/VA 은/ETM 농도/NNG 의/JKG 전문/NNG 약품/NNG 을/JKO 사용/NNG 하/XSV 고/EC ,/SP 의사/NNG 가/JKS 피부/NNG 상태/NNG 를/JKO 보/VV 며/EC 농도/NNG 와/JC 시간/NNG 을/JKO 조절/NNG 하/XSV ᆸ니다/EF ./SF 효과/NNG 와/JC 안전/NNG 성/XSN 모두/MAG 높/VA 어요/EF ./SF

알려진 오분절(출현별, 교정 안 함):

- `/categories/14/patient_name` 「필링」 [11,13) → 필/NNG 링/NNG — 「필링」이 「필」+「링」으로 분해(같은 카테고리 다른 출현은 「필링/NNG」) — 시술명 토큰 불일치
- `/categories/14/simple_explanation` 「필링」 [24,26) → 필/NNP 링/NNG — 「필링」이 「필」+「링」으로 분해(같은 카테고리 다른 출현은 「필링/NNG」) — 시술명 토큰 불일치
- `/categories/14/common_concerns/2/q` 「필링」 [7,9) → 필/NNP 링/NNG — 「필링」이 「필」+「링」으로 분해(같은 카테고리 다른 출현은 「필링/NNG」) — 시술명 토큰 불일치
