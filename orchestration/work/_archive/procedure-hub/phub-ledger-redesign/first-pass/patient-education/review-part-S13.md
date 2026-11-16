# S13 — /categories/12 M13 플라즈마

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/12/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S13.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/12` | [12] | object | (object, 자식 9) | 8792–9550 |  |  |
| `/categories/12/id` | id | string | "M13" | 8799–8802 | 제외(category_code) |  |
| `/categories/12/name` | name | string | "플라즈마" | 8812–8816 | 1토큰 | E0569 |
| `/categories/12/patient_name` | patient_name | string | "플라즈마 피부 시술" | 8834–8844 | 3토큰 | E0570 |
| `/categories/12/simple_explanation` | simple_explanation | string | "플라즈마(이온화된 기체) 에너지로 피부 표면을 재생시키고 탄력을 높이는 시술입니다." | 8868–8914 | 24토큰 | E0571, E0572, E0573 |
| `/categories/12/how_it_works` | how_it_works | string | "기기에서 발생하는 플라즈마 에너지가 피부에 닿으면, 피부 표면의 묵은 각질을 제거하고 피부 깊은 층의 콜라겐 재생을 자극합니다. 즉각적인 타이트닝 효과와 함께 피부결이 개선됩니다." | 8932–9032 | 50토큰 | E0574, E0575, E0576, E0577, E0578 |
| `/categories/12/duration_simple` | duration_simple | string | "즉시 효과가 나타나며, 약 3-6개월 지속됩니다." | 9053–9080 | 13토큰 | E0579, E0580, E0581 |
| `/categories/12/pain_level` | pain_level | string | "가벼운 열감과 따끔함, 부위에 따라 마취 크림 사용" | 9096–9124 | 16토큰 | E0582, E0583 |
| `/categories/12/downtime` | downtime | string | "가벼운 붉은기 수시간~1일, 미세한 가피(딱지) 형성 시 자연 탈락 대기" | 9138–9178 | 23토큰 | E0584, E0585, E0586 |
| `/categories/12/common_concerns` | common_concerns | array | (array, 자식 3) | 9198–9549 |  |  |
| `/categories/12/common_concerns/0` | [0] | object | (object, 자식 2) | 9199–9350 |  |  |
| `/categories/12/common_concerns/0/q` | q | string | "플라즈마가 뭔가요? 위험하지 않나요?" | 9205–9225 | 13토큰 | E0587 |
| `/categories/12/common_concerns/0/a` | a | string | "플라즈마는 피부 표면에 의도적인 열손상과 가피를 만드는 시술입니다. 시술 후 색소침착(PIH)·흉터·저색소증 위험이 있으며, 특히 피부색이 진한 편이면 색소침착 위험이 높아 의료진의 적절한 평가가 필요합니다." | 9232–9348 | 62토큰 | E0588, E0589, E0590, E0591, E0592, E0593, E0594, E0595 |
| `/categories/12/common_concerns/1` | [1] | object | (object, 자식 2) | 9351–9446 |  |  |
| `/categories/12/common_concerns/1/q` | q | string | "눈꺼풀 처짐에도 효과가 있나요?" | 9357–9374 | 10토큰 | E0596, E0597 |
| `/categories/12/common_concerns/1/a` | a | string | "일부 클리닉에서 비수술적 눈꺼풀 시술에 사용되나, 눈 주변은 색소침착·흉터 위험이 있어 의료진 상담이 필요합니다." | 9381–9444 | 31토큰 | E0598, E0599, E0600, E0601, E0602 |
| `/categories/12/common_concerns/2` | [2] | object | (object, 자식 2) | 9447–9548 |  |  |
| `/categories/12/common_concerns/2/q` | q | string | "시술 후 딱지가 생기나요?" | 9453–9467 | 7토큰 | E0603 |
| `/categories/12/common_concerns/2/a` | a | string | "미세한 점 형태의 가피가 생길 수 있어요. 절대 억지로 떼지 말고 자연스럽게 떨어지길 기다려주세요. 보통 5-7일이면 사라집니다." | 9474–9546 | 39토큰 | E0604, E0605, E0606, E0607, E0608, E0609, E0610 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S13-O1 | P | `/categories/12/common_concerns/0/a` | 「피부색이 진한 편이면」 대상 조건 + 위험 증가 · 「적절한 평가」 내용 미기재(B). 임상적으로 승인하지 않는다 |
| S13-O2 | P | `/categories/12/common_concerns/1/a` | 질문(효과 있나)에 효과 단정 없이 「일부 클리닉에서 사용」과 위험만 답한다 — 효과 정보 부재(B) |
| S13-O3 | F | `/categories/12/common_concerns/1/q` | 「눈꺼풀 처짐」이 S01 a 에서는 부작용, 여기서는 고민으로 쓰인다 — 같은 문자열의 역할이 다르다. 병합하지 않는다 |
| S13-O4 | P | `/categories/12/downtime` | 가피(딱지) 소실 시간: downtime 은 「자연 탈락 대기」만, cc2 a 는 「보통 5-7일」 — 같은 카테고리 내 값 분산 |
| S13-O5 | B | `/categories/12/pain_level` | 마취 크림 사용 부위 미기재 |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0569 | `/categories/12/name` | 플라즈마 | 0–4 | name |  |
| E0570 | `/categories/12/patient_name` | 플라즈마 피부 시술 | 0–10 | name,site |  |
| E0571 | `/categories/12/simple_explanation` | 플라즈마(이온화된 기체) 에너지로 피부 표면을 재생시키고 탄력을 높이는 시술입니다. | 0–46 | sentence,device_param,paraphrase,site,effect |  |
| E0572 | `/categories/12/simple_explanation` | 플라즈마(이온화된 기체) | 0–13 | device_param,paraphrase |  |
| E0573 | `/categories/12/simple_explanation` | 피부 표면 | 19–24 | site,depth |  |
| E0574 | `/categories/12/how_it_works` | 기기에서 발생하는 플라즈마 에너지가 피부에 닿으면, 피부 표면의 묵은 각질을 제거하고 피부 깊은 층의 콜라겐 재생을 자극합니다. | 0–71 | sentence,condition,device_param,site,depth,mechanism |  |
| E0575 | `/categories/12/how_it_works` | 피부 표면의 묵은 각질을 제거하고 | 29–47 | site,mechanism |  |
| E0576 | `/categories/12/how_it_works` | 피부 깊은 층의 콜라겐 재생 | 48–63 | site,depth,mechanism |  |
| E0577 | `/categories/12/how_it_works` | 즉각적인 타이트닝 효과와 함께 피부결이 개선됩니다. | 72–100 | sentence,time,effect |  |
| E0578 | `/categories/12/how_it_works` | 즉각적인 타이트닝 효과 | 72–84 | time,effect |  |
| E0579 | `/categories/12/duration_simple` | 즉시 효과가 나타나며, 약 3-6개월 지속됩니다. | 0–27 | sentence,time,approx,range,quantity | 발현(즉시)·지속 |
| E0580 | `/categories/12/duration_simple` | 즉시 효과가 나타나며 | 0–11 | time,effect | 발현 · regex 대조 후 보충(구절 누락 수정) |
| E0581 | `/categories/12/duration_simple` | 약 3-6개월 지속됩니다 | 13–26 | time,approx,range,quantity | 지속 · regex 대조 후 보충(구절 누락 수정) |
| E0582 | `/categories/12/pain_level` | 가벼운 열감과 따끔함, 부위에 따라 마취 크림 사용 | 0–28 | degree,sensory,condition,site,substance |  |
| E0583 | `/categories/12/pain_level` | 부위에 따라 마취 크림 사용 | 13–28 | condition,site,substance | 부위 미기재 |
| E0584 | `/categories/12/downtime` | 가벼운 붉은기 수시간~1일, 미세한 가피(딱지) 형성 시 자연 탈락 대기 | 0–40 | degree,adverse,time,range,approx,condition,paraphrase,instruction |  |
| E0585 | `/categories/12/downtime` | 가벼운 붉은기 수시간~1일 | 0–14 | degree,adverse,time,range,approx |  |
| E0586 | `/categories/12/downtime` | 미세한 가피(딱지) 형성 시 자연 탈락 대기 | 16–40 | degree,adverse,paraphrase,condition,instruction | 조건부 행동 지시 |
| E0587 | `/categories/12/common_concerns/0/q` | 플라즈마가 뭔가요? 위험하지 않나요? | 0–20 | sentence,adverse,negation | 두 질문 한 값 |
| E0588 | `/categories/12/common_concerns/0/a` | 플라즈마는 피부 표면에 의도적인 열손상과 가피를 만드는 시술입니다. | 0–37 | sentence,site,mechanism,adverse |  |
| E0589 | `/categories/12/common_concerns/0/a` | 의도적인 열손상과 가피 | 13–25 | mechanism,adverse | 의도된 손상 — 부작용과 기전 경계 |
| E0590 | `/categories/12/common_concerns/0/a` | 시술 후 색소침착(PIH)·흉터·저색소증 위험이 있으며, 특히 피부색이 진한 편이면 색소침착 위험이 높아 의료진의 적절한 평가가 필요합니다. | 38–116 | sentence,time,adverse,target,condition,degree,instruction,actor |  |
| E0591 | `/categories/12/common_concerns/0/a` | 색소침착(PIH)·흉터·저색소증 위험 | 43–63 | adverse,paraphrase | 약어 괄호 · 3개 나열 |
| E0592 | `/categories/12/common_concerns/0/a` | 특히 피부색이 진한 편이면 | 70–84 | target,condition,degree | 위험 증가 조건 |
| E0593 | `/categories/12/common_concerns/0/a` | 색소침착 위험이 높아 | 85–96 | adverse,degree |  |
| E0594 | `/categories/12/common_concerns/0/a` | 의료진의 적절한 평가가 필요합니다 | 97–115 | actor,instruction |  |
| E0595 | `/categories/12/common_concerns/0/a` | 시술 후 색소침착(PIH)·흉터·저색소증 위험이 있으며 | 38–68 | time,adverse,paraphrase | regex 대조 후 보충(구절 누락 수정) |
| E0596 | `/categories/12/common_concerns/1/q` | 눈꺼풀 처짐에도 효과가 있나요? | 0–17 | sentence,concern,site |  |
| E0597 | `/categories/12/common_concerns/1/q` | 눈꺼풀 처짐 | 0–6 | concern,site | S01 에서는 부작용(안검하수)으로 쓰인 같은 표현이 여기서는 고민 |
| E0598 | `/categories/12/common_concerns/1/a` | 일부 클리닉에서 비수술적 눈꺼풀 시술에 사용되나, 눈 주변은 색소침착·흉터 위험이 있어 의료진 상담이 필요합니다. | 0–63 | sentence,scope,place,site,adverse,instruction,actor |  |
| E0599 | `/categories/12/common_concerns/1/a` | 일부 클리닉에서 | 0–8 | scope,place | 효과 여부 답 대신 사용 현황 |
| E0600 | `/categories/12/common_concerns/1/a` | 비수술적 눈꺼풀 시술 | 9–20 | negation,site,name |  |
| E0601 | `/categories/12/common_concerns/1/a` | 눈 주변은 색소침착·흉터 위험이 있어 | 28–48 | site,adverse | 부위 조건부 위험 |
| E0602 | `/categories/12/common_concerns/1/a` | 의료진 상담이 필요합니다 | 49–62 | instruction,actor |  |
| E0603 | `/categories/12/common_concerns/2/q` | 시술 후 딱지가 생기나요? | 0–14 | sentence,time,adverse |  |
| E0604 | `/categories/12/common_concerns/2/a` | 미세한 점 형태의 가피가 생길 수 있어요. | 0–23 | sentence,degree,adverse,possibility |  |
| E0605 | `/categories/12/common_concerns/2/a` | 절대 억지로 떼지 말고 자연스럽게 떨어지길 기다려주세요. | 24–55 | sentence,avoid,negation,instruction,degree,manner | 「절대」 강한 금지 |
| E0606 | `/categories/12/common_concerns/2/a` | 절대 억지로 떼지 말고 | 24–36 | avoid,negation,degree |  |
| E0607 | `/categories/12/common_concerns/2/a` | 보통 5-7일이면 사라집니다. | 56–72 | sentence,frequency,time,range,quantity,course | 소실 |
| E0608 | `/categories/12/common_concerns/2/a` | 미세한 점 형태의 가피 | 0–12 | degree,adverse | regex 대조 후 보충(구절 누락 수정) |
| E0609 | `/categories/12/common_concerns/2/a` | 자연스럽게 떨어지길 기다려주세요 | 37–54 | manner,instruction | regex 대조 후 보충(구절 누락 수정) |
| E0610 | `/categories/12/common_concerns/2/a` | 보통 5-7일이면 사라집니다 | 56–71 | frequency,time,range,quantity,course | regex 대조 후 보충(구절 누락 수정) |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/12/name`: 플라즈마/NNG
- `/categories/12/patient_name`: 플라즈마/NNG 피부/NNG 시술/NNG
- `/categories/12/simple_explanation`: 플라즈마/NNG (/SSO 이온/NNG 화/XSN 되/XSV ᆫ/ETM 기체/NNG )/SSC 에너지/NNG 로/JKB 피부/NNG 표면/NNG 을/JKO 재생/NNG 시키/XSV 고/EC 탄력/NNG 을/JKO 높이/VV 는/ETM 시술/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/12/how_it_works`: 기기/NNG 에서/JKB 발생/NNG 하/XSV 는/ETM 플라즈마/NNG 에너지/NNG 가/JKS 피부/NNG 에/JKB 닿/VV 으면/EC ,/SP 피부/NNG 표면/NNG 의/JKG 묵/VV 은/ETM 각질/NNG 을/JKO 제거/NNG 하/XSV 고/EC 피부/NNG 깊/VA 은/ETM 층/NNG 의/JKG 콜라겐/NNP 재생/NNG 을/JKO 자극/NNG 하/XSV ᆸ니다/EF ./SF 즉각/NNG 적/XSN 이/VCP ᆫ/ETM 타이트닝/NNG 효과/NNG 와/JKB 함께/MAG 피부/NNG 결/NNG 이/JKS 개선/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/12/duration_simple`: 즉시/MAG 효과/NNG 가/JKS 나타나/VV 며/EC ,/SP 약/MM 3-6/W_SERIAL 개월/NNB 지속/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/12/pain_level`: 가볍/VA-I 은/ETM 열/NNG 감/XSN 과/JC 따끔/MAG 하/XSA ᆷ/ETN ,/SP 부위/NNG 에/JKB 따르/VV 어/EC 마취/NNG 크림/NNG 사용/NNG
- `/categories/12/downtime`: 가볍/VA-I 은/ETM 붉/VA 은/ETM 기/NNG 수/MM 시간/NNB ~/SO 1/SN 일/NNB ,/SP 미세/NNG 하/XSA ᆫ/ETM 가피/NNG (/SSO 딱지/NNG )/SSC 형성/NNG 시/NNB 자연/MAG 탈락/NNG 대기/NNG
- `/categories/12/common_concerns/0/q`: 플라즈마/NNG 가/JKS 뭐/NP 이/VCP ᆫ가/EF 요/JX ?/SF 위험/NNG 하/XSA 지/EC 않/VX 나요/EF ?/SF
- `/categories/12/common_concerns/0/a`: 플라즈마/NNG 는/JX 피부/NNG 표면/NNG 에/JKB 의도/NNG 적/XSN 이/VCP ᆫ/ETM 열/NNG 손상/NNG 과/JC 가피/NNG 를/JKO 만들/VX 는/ETM 시술/NNG 이/VCP ᆸ니다/EF ./SF 시술/NNG 후/NNG 색소/NNG 침착/NNG (/SSO PIH/SL )/SSC ·/SP 흉터/NNG ·/SP 저색소증/NNP 위험/NNG 이/JKS 있/VV 으며/EC ,/SP 특히/MAG 피부/NNG 색/NNG 이/JKS 진하/VA ᆫ/ETM 편/NNB 이/VCP 면/EC 색소/NNG 침착/NNG 위험/NNG 이/JKS 높/VA 어/EC 의료진/NNG 의/JKG 적절/XR 하/XSA ᆫ/ETM 평가/NNG 가/JKS 필요/NNG 하/XSA ᆸ니다/EF ./SF
- `/categories/12/common_concerns/1/q`: 눈꺼풀/NNG 처지/VV ᆷ/ETN 에/JKB 도/JX 효과/NNG 가/JKS 있/VA 나요/EF ?/SF
- `/categories/12/common_concerns/1/a`: 일부/NNG 클리닉/NNG 에서/JKB 비/XPN 수술/NNG 적/XSN 눈꺼풀/NNG 시술/NNG 에/JKB 사용/NNG 되/XSV 나/EC ,/SP 눈/NNG 주변/NNG 은/JX 색소/NNG 침착/NNG ·/SP 흉터/NNG 위험/NNG 이/JKS 있/VA 어/EC 의료진/NNG 상담/NNG 이/JKS 필요/NNG 하/XSA ᆸ니다/EF ./SF
- `/categories/12/common_concerns/2/q`: 시술/NNG 후/NNG 딱지/NNG 가/JKS 생기/VV 나요/EF ?/SF
- `/categories/12/common_concerns/2/a`: 미세/NNG 하/XSA ᆫ/ETM 점/NNG 형태/NNG 의/JKG 가피/NNG 가/JKS 생기/VV ᆯ/ETM 수/NNB 있/VA 어요/EF ./SF 절대/MAG 억지로/MAG 떼/VV 지/EC 말/VX 고/EC 자연/NNG 스럽/XSA-I 게/EC 떨어지/VV 기/ETN ᆯ/JKO 기다리/VV 어/EC 주/VX 세요/EF ./SF 보통/MAG 5-7/W_SERIAL 일/NNB 이/VCP 면/EC 사라지/VV ᆸ니다/EF ./SF
