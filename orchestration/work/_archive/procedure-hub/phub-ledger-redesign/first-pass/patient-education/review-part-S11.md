# S11 — /categories/10 M11 니들RF

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/10/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S11.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/10` | [10] | object | (object, 자식 9) | 7348–8072 |  |  |
| `/categories/10/id` | id | string | "M11" | 7355–7358 | 제외(category_code) |  |
| `/categories/10/name` | name | string | "니들RF" | 7368–7372 | 2토큰 | E0487 |
| `/categories/10/patient_name` | patient_name | string | "미세바늘 고주파 (포텐자/인모드 등)" | 7390–7410 | 10토큰 | E0488, E0489, E0490 |
| `/categories/10/simple_explanation` | simple_explanation | string | "아주 가는 바늘을 피부에 찔러 넣고, 바늘 끝에서 고주파 에너지를 쏘아 피부를 재생시키는 시술입니다." | 7434–7490 | 30토큰 | E0491, E0492, E0493 |
| `/categories/10/how_it_works` | how_it_works | string | "미세한 바늘이 피부 속으로 들어가 정확한 깊이에서 고주파(RF) 에너지를 전달합니다. 피부 표면은 크게 손상시키지 않으면서 피부 안쪽에서 콜라겐이 새로 만들어져 모공, 흉터, 주름이 개선됩니다." | 7508–7616 | 56토큰 | E0494, E0495, E0496, E0497, E0498, E0499, E0500 |
| `/categories/10/duration_simple` | duration_simple | string | "효과가 1-2주 후 나타나기 시작하며, 6-12개월 지속됩니다." | 7637–7672 | 17토큰 | E0501, E0502, E0503 |
| `/categories/10/pain_level` | pain_level | string | "마취 크림 도포 후 시술, 따끔한 느낌과 열감" | 7688–7713 | 13토큰 | E0504, E0505 |
| `/categories/10/downtime` | downtime | string | "붉은기와 약간의 붓기 2-3일, 미세한 딱지 3-5일" | 7727–7756 | 17토큰 | E0506, E0507, E0508 |
| `/categories/10/common_concerns` | common_concerns | array | (array, 자식 3) | 7776–8071 |  |  |
| `/categories/10/common_concerns/0` | [0] | object | (object, 자식 2) | 7777–7877 |  |  |
| `/categories/10/common_concerns/0/q` | q | string | "모공이 정말 줄어드나요?" | 7783–7796 | 6토큰 | E0509 |
| `/categories/10/common_concerns/0/a` | a | string | "모공 주변의 콜라겐이 재생되면서 모공이 조여드는 효과가 있습니다. 1회로도 개선을 느끼실 수 있고, 3-4회 반복하면 더 좋아요." | 7803–7875 | 41토큰 | E0510, E0511, E0512, E0513, E0514, E0515 |
| `/categories/10/common_concerns/1` | [1] | object | (object, 자식 2) | 7878–7969 |  |  |
| `/categories/10/common_concerns/1/q` | q | string | "여드름 흉터에도 효과가 있나요?" | 7884–7901 | 9토큰 | E0516 |
| `/categories/10/common_concerns/1/a` | a | string | "네, 여드름으로 파인 흉터 개선에 효과적인 시술 중 하나예요. 흉터 깊이에 따라 필요한 횟수가 달라집니다." | 7908–7967 | 32토큰 | E0517, E0518, E0519, E0520, E0521, E0522 |
| `/categories/10/common_concerns/2` | [2] | object | (object, 자식 2) | 7970–8070 |  |  |
| `/categories/10/common_concerns/2/q` | q | string | "니들RF와 프락셔널 레이저 중 뭐가 좋나요?" | 7976–8000 | 11토큰 | E0523, E0524 |
| `/categories/10/common_concerns/2/a` | a | string | "둘 다 피부 재생 시술이지만 방식이 달라요. 피부 상태와 목표에 따라 의사가 더 적합한 시술을 추천해드립니다." | 8007–8068 | 33토큰 | E0525, E0526, E0527 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S11-O1 | P | `/categories/10/common_concerns/1/a` | 「흉터 깊이」는 고민(흉터)의 깊이로 시술 깊이(how_it_works 「정확한 깊이」)와 대상이 다르다 |
| S11-O2 | B | `/categories/10/how_it_works` | 전달 깊이 수치 미기재 |
| S11-O3 | F | `/categories/10/common_concerns/2/q` | 「프락셔널 레이저」는 S08(M8) downtime·pain_level 의 「프락셔널」과 연결될 수 있으나 후속 |
| S11-O4 | B | `/categories/10/common_concerns/0/a` | 반복 간격 미기재 |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0487 | `/categories/10/name` | 니들RF | 0–4 | name | 혼합 표기(한글+영문) |
| E0488 | `/categories/10/patient_name` | 미세바늘 고주파 (포텐자/인모드 등) | 0–20 | name,device,paraphrase | 괄호 안 「/」 제품 나열 · 「등」 |
| E0489 | `/categories/10/patient_name` | 포텐자 | 10–13 | name |  |
| E0490 | `/categories/10/patient_name` | 인모드 | 14–17 | name |  |
| E0491 | `/categories/10/simple_explanation` | 아주 가는 바늘을 피부에 찔러 넣고, 바늘 끝에서 고주파 에너지를 쏘아 피부를 재생시키는 시술입니다. | 0–56 | sentence,device,degree,device_param,sequence,effect |  |
| E0492 | `/categories/10/simple_explanation` | 아주 가는 바늘 | 0–8 | device,degree | 두께(바늘 굵기) 수식 |
| E0493 | `/categories/10/simple_explanation` | 바늘 끝에서 | 21–27 | site |  |
| E0494 | `/categories/10/how_it_works` | 미세한 바늘이 피부 속으로 들어가 정확한 깊이에서 고주파(RF) 에너지를 전달합니다. | 0–47 | sentence,device,depth,device_param,paraphrase |  |
| E0495 | `/categories/10/how_it_works` | 정확한 깊이에서 | 19–27 | depth,manner | 깊이 수치 미기재 |
| E0496 | `/categories/10/how_it_works` | 고주파(RF) | 28–35 | device_param,paraphrase |  |
| E0497 | `/categories/10/how_it_works` | 피부 표면은 크게 손상시키지 않으면서 피부 안쪽에서 콜라겐이 새로 만들어져 모공, 흉터, 주름이 개선됩니다. | 48–108 | sentence,site,degree,negation,mechanism,effect,concern |  |
| E0498 | `/categories/10/how_it_works` | 피부 표면은 크게 손상시키지 않으면서 | 48–68 | site,degree,negation | 「크게」 — 손상 정도 부분 부정 |
| E0499 | `/categories/10/how_it_works` | 모공, 흉터, 주름이 개선됩니다 | 90–107 | concern,effect |  |
| E0500 | `/categories/10/how_it_works` | 미세한 바늘 | 0–6 | device,degree | regex 대조 후 보충(구절 누락 수정) |
| E0501 | `/categories/10/duration_simple` | 효과가 1-2주 후 나타나기 시작하며, 6-12개월 지속됩니다. | 0–35 | sentence,time,range,quantity | 시간 역할: 시작·지속 |
| E0502 | `/categories/10/duration_simple` | 1-2주 후 나타나기 시작하며 | 4–20 | time,range,quantity |  |
| E0503 | `/categories/10/duration_simple` | 6-12개월 지속됩니다 | 22–34 | time,range,quantity |  |
| E0504 | `/categories/10/pain_level` | 마취 크림 도포 후 시술, 따끔한 느낌과 열감 | 0–25 | time,substance,sensory |  |
| E0505 | `/categories/10/pain_level` | 마취 크림 도포 후 | 0–10 | time,substance,sequence |  |
| E0506 | `/categories/10/downtime` | 붉은기와 약간의 붓기 2-3일, 미세한 딱지 3-5일 | 0–29 | adverse,degree,time,range,quantity |  |
| E0507 | `/categories/10/downtime` | 붉은기와 약간의 붓기 2-3일 | 0–16 | adverse,degree,time,range,quantity |  |
| E0508 | `/categories/10/downtime` | 미세한 딱지 3-5일 | 18–29 | adverse,degree,time,range,quantity |  |
| E0509 | `/categories/10/common_concerns/0/q` | 모공이 정말 줄어드나요? | 0–13 | sentence,concern,effect |  |
| E0510 | `/categories/10/common_concerns/0/a` | 모공 주변의 콜라겐이 재생되면서 모공이 조여드는 효과가 있습니다. | 0–36 | sentence,site,mechanism,effect |  |
| E0511 | `/categories/10/common_concerns/0/a` | 1회로도 개선을 느끼실 수 있고, 3-4회 반복하면 더 좋아요. | 37–72 | sentence,frequency,quantity,range,possibility,condition,comparison |  |
| E0512 | `/categories/10/common_concerns/0/a` | 1회로도 | 37–41 | quantity,scope |  |
| E0513 | `/categories/10/common_concerns/0/a` | 3-4회 반복하면 더 좋아요 | 56–71 | frequency,range,quantity,condition,comparison | 간격 미기재 |
| E0514 | `/categories/10/common_concerns/0/a` | 1회로도 개선을 느끼실 수 있고 | 37–54 | quantity,scope,possibility | regex 대조 후 보충(구절 누락 수정) |
| E0515 | `/categories/10/common_concerns/0/a` | 모공이 조여드는 효과가 있습니다 | 18–35 | effect,concern | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0516 | `/categories/10/common_concerns/1/q` | 여드름 흉터에도 효과가 있나요? | 0–17 | sentence,concern |  |
| E0517 | `/categories/10/common_concerns/1/a` | 네, 여드름으로 파인 흉터 개선에 효과적인 시술 중 하나예요. | 0–34 | sentence,concern,effect,scope |  |
| E0518 | `/categories/10/common_concerns/1/a` | 여드름으로 파인 흉터 | 3–14 | concern,cause |  |
| E0519 | `/categories/10/common_concerns/1/a` | 효과적인 시술 중 하나 | 19–31 | scope,effect |  |
| E0520 | `/categories/10/common_concerns/1/a` | 흉터 깊이에 따라 필요한 횟수가 달라집니다. | 35–59 | sentence,condition,depth,frequency | 흉터 깊이 — 주입 깊이와 다른 대상 · 횟수 수치 없음 |
| E0521 | `/categories/10/common_concerns/1/a` | 흉터 깊이에 따라 | 35–44 | condition,depth |  |
| E0522 | `/categories/10/common_concerns/1/a` | 필요한 횟수가 달라집니다 | 45–58 | frequency,condition | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0523 | `/categories/10/common_concerns/2/q` | 니들RF와 프락셔널 레이저 중 뭐가 좋나요? | 0–24 | sentence,comparison,reference | 다른 카테고리(레이저 하위 프락셔널) 참조 |
| E0524 | `/categories/10/common_concerns/2/q` | 프락셔널 레이저 | 6–14 | name,reference |  |
| E0525 | `/categories/10/common_concerns/2/a` | 둘 다 피부 재생 시술이지만 방식이 달라요. | 0–24 | sentence,comparison |  |
| E0526 | `/categories/10/common_concerns/2/a` | 피부 상태와 목표에 따라 의사가 더 적합한 시술을 추천해드립니다. | 25–61 | sentence,condition,actor,comparison |  |
| E0527 | `/categories/10/common_concerns/2/a` | 의사가 더 적합한 시술을 추천해드립니다 | 39–60 | actor,comparison | regex 대조 후 보충(구절 누락 수정) |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/10/name`: 니들/NNP RF/SL
- `/categories/10/patient_name`: 미세/NNG 바늘/NNG 고/XPN 주파/NNG (/SSO 포텐자/NNG //SP 인모드/NNG 등/NNB )/SSC
- `/categories/10/simple_explanation`: 아주/MAG 가늘/VA ᆫ/ETM 바늘/NNG 을/JKO 피부/NNG 에/JKB 찌르/VV 어/EC 넣/VV 고/EC ,/SP 바늘/NNG 끝/NNG 에서/JKB 고/XPN 주파/NNG 에너지/NNG 를/JKO 쏘/VV 어/EC 피부/NNG 를/JKO 재생/NNG 시키/XSV 는/ETM 시술/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/10/how_it_works`: 미세/NNG 하/XSA ᆫ/ETM 바늘/NNG 이/JKS 피부/NNG 속/NNG 으로/JKB 들어가/VV 어/EC 정확/NNG 하/XSA ᆫ/ETM 깊이/NNG 에서/JKB 고/XPN 주파/NNG (/SSO RF/SL )/SSC 에너지/NNG 를/JKO 전달/NNG 하/XSV ᆸ니다/EF ./SF 피부/NNG 표면/NNG 은/JX 크/VA 게/EC 손상/NNG 시키/XSV 지/EC 않/VX 으면서/EC 피부/NNG 안쪽/NNG 에서/JKB 콜라겐/NNP 이/JKS 새로/MAG 만들/VV 어/EC 지/VX 어/EC 모공/NNG ,/SP 흉터/NNG ,/SP 주름/NNG 이/JKS 개선/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/10/duration_simple`: 효과/NNG 가/JKS 1-2/W_SERIAL 주/NNB 후/NNG 나타나/VV 기/ETN 시작/NNG 하/XSV 며/EC ,/SP 6-12/W_SERIAL 개월/NNB 지속/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/10/pain_level`: 마취/NNG 크림/NNG 도포/NNG 후/NNG 시술/NNG ,/SP 따끔/MAG 하/XSA ᆫ/ETM 느낌/NNG 과/JC 열/NNG 감/XSN
- `/categories/10/downtime`: 붉/VA 은/ETM 기/NNG 와/JC 약간/NNG 의/JKG 붓/VV-I 기/ETN 2-3/W_SERIAL 일/NNB ,/SP 미세/NNG 하/XSA ᆫ/ETM 딱지/NNG 3-5/W_SERIAL 일/NNB
- `/categories/10/common_concerns/0/q`: 모공/NNG 이/JKS 정말/MAG 줄어들/VV 나요/EF ?/SF
- `/categories/10/common_concerns/0/a`: 모공/NNG 주변/NNG 의/JKG 콜라겐/NNP 이/JKS 재생/NNG 되/XSV 면서/EC 모공/NNG 이/JKS 조이/VV 어/EC 들/VX 는/ETM 효과/NNG 가/JKS 있/VA 습니다/EF ./SF 1/SN 회/NNB 로/JKB 도/JX 개선/NNG 을/JKO 느끼/VV 시/EP ᆯ/ETM 수/NNB 있/VA 고/EC ,/SP 3-4/W_SERIAL 회/NNB 반복/NNG 하/XSV 면/EC 더/MAG 좋/VA 어요/EF ./SF
- `/categories/10/common_concerns/1/q`: 여드름/NNG 흉터/NNG 에/JKB 도/JX 효과/NNG 가/JKS 있/VA 나요/EF ?/SF
- `/categories/10/common_concerns/1/a`: 네/IC ,/SP 여드름/NNG 으로/JKB 파이/VV ᆫ/ETM 흉터/NNG 개선/NNG 에/JKB 효과/NNG 적/XSN 이/VCP ᆫ/ETM 시술/NNG 중/NNB 하나/NR 이/VCP 예요/EF ./SF 흉터/NNG 깊이/NNG 에/JKB 따르/VV 어/EC 필요/NNG 하/XSA ᆫ/ETM 횟수/NNG 가/JKS 달라지/VV ᆸ니다/EF ./SF
- `/categories/10/common_concerns/2/q`: 니들/NNP RF/SL 와/JC 프락셔널/NNP 레이저/NNG 중/NNB 뭐/NP 가/JKS 좋/VA 나요/EF ?/SF
- `/categories/10/common_concerns/2/a`: 둘/NR 다/MAG 피부/NNG 재생/NNG 시술/NNG 이/VCP 지만/EC 방식/NNG 이/JKS 다르/VA 어요/EF ./SF 피부/NNG 상태/NNG 와/JC 목표/NNG 에/JKB 따르/VV 어/EC 의사/NNG 가/JKS 더/MAG 적합/XR 하/XSA ᆫ/ETM 시술/NNG 을/JKO 추천/NNG 하/XSV 어/EC 드리/VX ᆸ니다/EF ./SF

알려진 오분절(출현별, 교정 안 함):

- `/categories/10/patient_name` 「고주파」 [5,8) → 고/XPN 주파/NNG — 「고주파」가 접두사+명사로 분해 — 「고」가 정도(높음) 접두로 읽힐 위험·에너지 종류 토큰 누락
- `/categories/10/simple_explanation` 「고주파」 [28,31) → 고/XPN 주파/NNG — 「고주파」가 접두사+명사로 분해 — 「고」가 정도(높음) 접두로 읽힐 위험·에너지 종류 토큰 누락
- `/categories/10/how_it_works` 「고주파」 [28,31) → 고/XPN 주파/NNG — 「고주파」가 접두사+명사로 분해 — 「고」가 정도(높음) 접두로 읽힐 위험·에너지 종류 토큰 누락
