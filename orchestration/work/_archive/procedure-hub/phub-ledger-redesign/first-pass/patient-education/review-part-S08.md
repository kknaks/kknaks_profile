# S08 — /categories/7 M8 레이저

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/7/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S08.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/7` | [7] | object | (object, 자식 9) | 5077–5855 |  |  |
| `/categories/7/id` | id | string | "M8" | 5084–5086 | 제외(category_code) |  |
| `/categories/7/name` | name | string | "레이저" | 5096–5099 | 1토큰 | E0351 |
| `/categories/7/patient_name` | patient_name | string | "레이저 피부 시술" | 5117–5126 | 3토큰 | E0352 |
| `/categories/7/simple_explanation` | simple_explanation | string | "특수한 빛(레이저)으로 기미, 주근깨, 흉터, 모공 등 다양한 피부 문제를 개선하는 시술입니다." | 5150–5203 | 29토큰 | E0353, E0354, E0355, E0356, E0357, E0358, E0359 |
| `/categories/7/how_it_works` | how_it_works | string | "특정 파장의 빛을 피부에 쏘면, 그 빛이 색소나 물 분자에 흡수되면서 문제 부위만 선택적으로 치료합니다. 종류에 따라 색소를 깨뜨리거나, 피부 재생을 유도하거나, 혈관을 치료합니다." | 5221–5322 | 53토큰 | E0360, E0361, E0362, E0363, E0364, E0365, E0366, E0367, E0368 |
| `/categories/7/duration_simple` | duration_simple | string | "시술 종류와 목적에 따라 다릅니다. 토닝은 주 1회씩 여러 차례, 색소 제거는 수회 반복이 필요합니다." | 5343–5400 | 30토큰 | E0369, E0370, E0371, E0372 |
| `/categories/7/pain_level` | pain_level | string | "종류에 따라 다름 - 토닝은 가벼운 따끔함, 프락셔널은 마취 크림 필요" | 5416–5455 | 20토큰 | E0373, E0374, E0375 |
| `/categories/7/downtime` | downtime | string | "토닝: 거의 없음 / 프락셔널: 붉은기 3-7일 / 어블레이티브: 1-2주 회복" | 5469–5513 | 19토큰 | E0376, E0377, E0378, E0379 |
| `/categories/7/common_concerns` | common_concerns | array | (array, 자식 3) | 5533–5854 |  |  |
| `/categories/7/common_concerns/0` | [0] | object | (object, 자식 2) | 5534–5638 |  |  |
| `/categories/7/common_concerns/0/q` | q | string | "레이저 맞으면 피부가 얇아지나요?" | 5540–5558 | 10토큰 | E0380, E0381 |
| `/categories/7/common_concerns/0/a` | a | string | "적절한 세기와 간격으로 시술하면 오히려 콜라겐이 생성되어 피부가 건강해질 수 있어요. 과도하게 자주 받지 않는 것이 중요합니다." | 5565–5636 | 41토큰 | E0382, E0383, E0384, E0385, E0386, E0387, E0388 |
| `/categories/7/common_concerns/1` | [1] | object | (object, 자식 2) | 5639–5751 |  |  |
| `/categories/7/common_concerns/1/q` | q | string | "레이저 후 색소침착이 생길 수 있나요?" | 5645–5666 | 11토큰 | E0389, E0390 |
| `/categories/7/common_concerns/1/a` | a | string | "일시적으로 생길 수 있어요. 시술 후 자외선 차단을 철저히 하면 예방에 도움이 됩니다. 보통 수 주~수 개월 내에 자연스럽게 사라집니다." | 5673–5749 | 38토큰 | E0391, E0392, E0393, E0394, E0395, E0396, E0397 |
| `/categories/7/common_concerns/2` | [2] | object | (object, 자식 2) | 5752–5853 |  |  |
| `/categories/7/common_concerns/2/q` | q | string | "기미가 레이저로 완치되나요?" | 5758–5773 | 8토큰 | E0398 |
| `/categories/7/common_concerns/2/a` | a | string | "기미는 체질적 요인이 크기 때문에 완치라는 표현보다는 관리라고 보시면 됩니다. 레이저로 개선할 수 있지만 재발 관리가 중요해요." | 5780–5851 | 40토큰 | E0399, E0400, E0401, E0402, E0403, E0404 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S08-O1 | P | `/categories/7/downtime` | 「 / 」가 대안이 아니라 종류별 항목 구분자로 쓰였다(README 기호 규칙과 다른 쓰임 — 기호만으로 의미 확정 금지) |
| S08-O2 | P | `/categories/7/downtime` | 토닝·프락셔널·어블레이티브는 카테고리(레이저) 하위 종류명으로 보이나 이 원장 안에 정의 없음. duration_simple 은 토닝·색소 제거, pain_level 은 토닝·프락셔널로 세분 축이 값마다 다르다 |
| S08-O3 | B | `/categories/7/how_it_works` | 파장 수치·레이저 종류명 미기재 |
| S08-O4 | B | `/categories/7/common_concerns/0/a` | 「적절한 세기와 간격」「과도하게 자주」 기준 미기재 |
| S08-O5 | B | `/categories/7/common_concerns/1/a` | 자외선 차단 기간·수단 미기재 · 「수 주~수 개월」 불명확 수치 |
| S08-O6 | P | `/categories/7/common_concerns/0/q` | 두께 표현 「얇아지나요」 — 피부 두께 변화(부작용 우려)로 읽힘. 주입 깊이와 다른 정보 |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0351 | `/categories/7/name` | 레이저 | 0–3 | name |  |
| E0352 | `/categories/7/patient_name` | 레이저 피부 시술 | 0–9 | name,site |  |
| E0353 | `/categories/7/simple_explanation` | 특수한 빛(레이저)으로 기미, 주근깨, 흉터, 모공 등 다양한 피부 문제를 개선하는 시술입니다. | 0–53 | sentence |  |
| E0354 | `/categories/7/simple_explanation` | 특수한 빛(레이저) | 0–10 | device,paraphrase |  |
| E0355 | `/categories/7/simple_explanation` | 기미, 주근깨, 흉터, 모공 등 다양한 피부 문제 | 13–40 | concern | 고민 나열 · 「등」 열린 목록 |
| E0356 | `/categories/7/simple_explanation` | 기미 | 13–15 | concern |  |
| E0357 | `/categories/7/simple_explanation` | 주근깨 | 17–20 | concern |  |
| E0358 | `/categories/7/simple_explanation` | 흉터 | 22–24 | concern |  |
| E0359 | `/categories/7/simple_explanation` | 모공 | 26–28 | concern |  |
| E0360 | `/categories/7/how_it_works` | 특정 파장의 빛을 피부에 쏘면, 그 빛이 색소나 물 분자에 흡수되면서 문제 부위만 선택적으로 치료합니다. | 0–58 | sentence,condition,mechanism,scope |  |
| E0361 | `/categories/7/how_it_works` | 특정 파장의 빛 | 0–8 | device_param | 파장 수치 미기재 |
| E0362 | `/categories/7/how_it_works` | 색소나 물 분자에 흡수되면서 | 23–38 | mechanism | 「나」 대안 |
| E0363 | `/categories/7/how_it_works` | 문제 부위만 선택적으로 치료합니다 | 39–57 | scope,manner,effect |  |
| E0364 | `/categories/7/how_it_works` | 종류에 따라 색소를 깨뜨리거나, 피부 재생을 유도하거나, 혈관을 치료합니다. | 59–101 | sentence,condition,mechanism,effect | 종류별 작용 3갈래 — 종류명 미기재 |
| E0365 | `/categories/7/how_it_works` | 종류에 따라 | 59–65 | condition |  |
| E0366 | `/categories/7/how_it_works` | 색소를 깨뜨리거나 | 66–75 | mechanism |  |
| E0367 | `/categories/7/how_it_works` | 피부 재생을 유도하거나 | 77–89 | mechanism,effect |  |
| E0368 | `/categories/7/how_it_works` | 혈관을 치료합니다 | 91–100 | effect,site |  |
| E0369 | `/categories/7/duration_simple` | 시술 종류와 목적에 따라 다릅니다. | 0–19 | sentence,condition |  |
| E0370 | `/categories/7/duration_simple` | 토닝은 주 1회씩 여러 차례, 색소 제거는 수회 반복이 필요합니다. | 20–57 | sentence,name,frequency,time,quantity,approx |  |
| E0371 | `/categories/7/duration_simple` | 토닝은 주 1회씩 여러 차례 | 20–35 | name,frequency,time,quantity,approx | 간격(주 1회)과 횟수(여러 차례) 동시 |
| E0372 | `/categories/7/duration_simple` | 색소 제거는 수회 반복 | 37–49 | name,frequency,approx | 「수회」 수치 불명확 |
| E0373 | `/categories/7/pain_level` | 종류에 따라 다름 - 토닝은 가벼운 따끔함, 프락셔널은 마취 크림 필요 | 0–39 | condition,name,degree,sensory,substance,instruction | 「 - 」 뒤 종류별 세분 |
| E0374 | `/categories/7/pain_level` | 토닝은 가벼운 따끔함 | 12–23 | name,degree,sensory |  |
| E0375 | `/categories/7/pain_level` | 프락셔널은 마취 크림 필요 | 25–39 | name,substance,instruction |  |
| E0376 | `/categories/7/downtime` | 토닝: 거의 없음 / 프락셔널: 붉은기 3-7일 / 어블레이티브: 1-2주 회복 | 0–44 | name,time,range,quantity,negation,adverse | 「 / 」는 종류 구분자로 쓰임 |
| E0377 | `/categories/7/downtime` | 토닝: 거의 없음 | 0–9 | name,negation,degree |  |
| E0378 | `/categories/7/downtime` | 프락셔널: 붉은기 3-7일 | 12–26 | name,adverse,time,range,quantity |  |
| E0379 | `/categories/7/downtime` | 어블레이티브: 1-2주 회복 | 29–44 | name,time,range,quantity | 시간 역할=회복 |
| E0380 | `/categories/7/common_concerns/0/q` | 레이저 맞으면 피부가 얇아지나요? | 0–18 | sentence,condition,adverse,thickness |  |
| E0381 | `/categories/7/common_concerns/0/q` | 피부가 얇아지나요 | 8–17 | thickness,adverse | 두께 — 피부 두께 |
| E0382 | `/categories/7/common_concerns/0/a` | 적절한 세기와 간격으로 시술하면 오히려 콜라겐이 생성되어 피부가 건강해질 수 있어요. | 0–47 | sentence,condition,degree,time,possibility,effect |  |
| E0383 | `/categories/7/common_concerns/0/a` | 적절한 세기와 간격으로 시술하면 | 0–17 | condition,degree,time | 기준값 미기재 |
| E0384 | `/categories/7/common_concerns/0/a` | 오히려 | 18–21 | comparison | 질문 전제와 반대 |
| E0385 | `/categories/7/common_concerns/0/a` | 피부가 건강해질 수 있어요 | 32–46 | effect,possibility |  |
| E0386 | `/categories/7/common_concerns/0/a` | 과도하게 자주 받지 않는 것이 중요합니다. | 48–71 | sentence,degree,frequency,negation,instruction |  |
| E0387 | `/categories/7/common_concerns/0/a` | 과도하게 자주 | 48–55 | degree,frequency |  |
| E0388 | `/categories/7/common_concerns/0/a` | 과도하게 자주 받지 않는 것이 중요합니다 | 48–70 | degree,frequency,negation,instruction | regex 대조 후 보충(구절 누락 수정) |
| E0389 | `/categories/7/common_concerns/1/q` | 레이저 후 색소침착이 생길 수 있나요? | 0–21 | sentence,time,adverse,possibility |  |
| E0390 | `/categories/7/common_concerns/1/q` | 색소침착 | 6–10 | adverse |  |
| E0391 | `/categories/7/common_concerns/1/a` | 일시적으로 생길 수 있어요. | 0–15 | sentence,course,possibility |  |
| E0392 | `/categories/7/common_concerns/1/a` | 시술 후 자외선 차단을 철저히 하면 예방에 도움이 됩니다. | 16–48 | sentence,time,condition,degree,instruction,management |  |
| E0393 | `/categories/7/common_concerns/1/a` | 시술 후 자외선 차단을 철저히 | 16–32 | time,instruction,degree | 기간 미기재 |
| E0394 | `/categories/7/common_concerns/1/a` | 보통 수 주~수 개월 내에 자연스럽게 사라집니다. | 49–76 | sentence,frequency,time,range,approx,course |  |
| E0395 | `/categories/7/common_concerns/1/a` | 보통 수 주~수 개월 내에 | 49–63 | frequency,time,range,approx | 「~」 범위 · 수치 불명확 |
| E0396 | `/categories/7/common_concerns/1/a` | 자연스럽게 사라집니다 | 64–75 | manner,course | 소실 |
| E0397 | `/categories/7/common_concerns/1/a` | 자외선 차단을 철저히 하면 예방에 도움이 됩니다 | 21–47 | condition,degree,instruction,management | regex 대조 후 보충(구절 누락 수정) |
| E0398 | `/categories/7/common_concerns/2/q` | 기미가 레이저로 완치되나요? | 0–15 | sentence,concern |  |
| E0399 | `/categories/7/common_concerns/2/a` | 기미는 체질적 요인이 크기 때문에 완치라는 표현보다는 관리라고 보시면 됩니다. | 0–43 | sentence,rationale,comparison,degree |  |
| E0400 | `/categories/7/common_concerns/2/a` | 체질적 요인이 크기 때문에 | 4–18 | cause,degree |  |
| E0401 | `/categories/7/common_concerns/2/a` | 완치라는 표현보다는 관리라고 | 19–34 | comparison,negation |  |
| E0402 | `/categories/7/common_concerns/2/a` | 레이저로 개선할 수 있지만 재발 관리가 중요해요. | 44–71 | sentence,possibility,effect,course,instruction |  |
| E0403 | `/categories/7/common_concerns/2/a` | 재발 관리 | 59–64 | course,management |  |
| E0404 | `/categories/7/common_concerns/2/a` | 재발 관리가 중요해요 | 59–70 | course,management,instruction | regex 대조 후 보충(구절 누락 수정) |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/7/name`: 레이저/NNG
- `/categories/7/patient_name`: 레이저/NNG 피부/NNG 시술/NNG
- `/categories/7/simple_explanation`: 특수/NNG 하/XSA ᆫ/ETM 빛/NNG (/SSO 레이저/NNG )/SSC 으로/JKB 기미/NNG ,/SP 주근깨/NNG ,/SP 흉터/NNG ,/SP 모공/NNG 등/NNB 다양/NNG 하/XSA ᆫ/ETM 피부/NNG 문제/NNG 를/JKO 개선/NNG 하/XSV 는/ETM 시술/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/7/how_it_works`: 특정/NNG 파장/NNG 의/JKG 빛/NNG 을/JKO 피부/NNG 에/JKB 쏘/VV 면/EC ,/SP 그/MM 빛/NNG 이/JKS 색소/NNG 나/JC 물/NNG 분자/NNG 에/JKB 흡수/NNG 되/XSV 면서/EC 문제/NNG 부위/NNG 만/JX 선택/NNG 적/XSN 으로/JKB 치료/NNG 하/XSV ᆸ니다/EF ./SF 종류/NNG 에/JKB 따르/VV 어/EC 색소/NNG 를/JKO 깨뜨리/VV 거나/EC ,/SP 피부/NNG 재생/NNG 을/JKO 유도/NNG 하/XSV 거나/EC ,/SP 혈관/NNG 을/JKO 치료/NNG 하/XSV ᆸ니다/EF ./SF
- `/categories/7/duration_simple`: 시술/NNG 종류/NNG 와/JC 목적/NNG 에/JKB 따르/VV 어/EC 다르/VA ᆸ니다/EF ./SF 토닝/NNP 은/JX 주/NNG 1/SN 회/NNB 씩/XSN 여러/MM 차례/NNG ,/SP 색소/NNG 제거/NNG 는/JX 수/MM 회/NNB 반복/NNG 이/JKS 필요/NNG 하/XSA ᆸ니다/EF ./SF
- `/categories/7/pain_level`: 종류/NNG 에/JKB 따르/VV 어/EC 다르/VA ᆷ/EF -/SO 토닝/NNG 은/JX 가볍/VA-I 은/ETM 따끔/MAG 하/XSA ᆷ/ETN ,/SP 프락셔널/NNG 은/JX 마취/NNG 크림/NNG 필요/NNG
- `/categories/7/downtime`: 토닝/NNG :/SP 거의/MAG 없/VA 음/ETN //SP 프락셔널/NNG :/SP 붉/VA 은/ETM 기/NNG 3-7/W_SERIAL 일/NNB //SP 어블레이티브/NNP :/SP 1-2/W_SERIAL 주/NNG 회복/NNG
- `/categories/7/common_concerns/0/q`: 레이저/NNG 맞/VV 으면/EC 피부/NNG 가/JKS 얇/VA 어/EC 지/VX 나요/EF ?/SF
- `/categories/7/common_concerns/0/a`: 적절/XR 하/XSA ᆫ/ETM 세기/NNG 와/JC 간격/NNG 으로/JKB 시술/NNG 하/XSV 면/EC 오히려/MAG 콜라겐/NNP 이/JKS 생성/NNG 되/XSV 어/EC 피부/NNG 가/JKS 건강/NNG 하/XSA 어/EC 지/VX ᆯ/ETM 수/NNB 있/VA 어요/EF ./SF 과도/NNG 하/XSA 게/EC 자주/MAG 받/VV-R 지/EC 않/VX 는/ETM 것/NNB 이/JKS 중요/NNG 하/XSA ᆸ니다/EF ./SF
- `/categories/7/common_concerns/1/q`: 레이저/NNG 후/NNG 색소/NNG 침착/NNG 이/JKS 생기/VV ᆯ/ETM 수/NNB 있/VA 나요/EF ?/SF
- `/categories/7/common_concerns/1/a`: 일시/NNG 적/XSN 으로/JKB 생기/VV ᆯ/ETM 수/NNB 있/VA 어요/EF ./SF 시술/NNG 후/NNG 자외선/NNG 차단/NNG 을/JKO 철저히/MAG 하/VV 면/EC 예방/NNG 에/JKB 도움/NNG 이/JKC 되/VV ᆸ니다/EF ./SF 보통/MAG 수/MM 주/NNG ~/SO 수/MM 개월/NNB 내/NNB 에/JKB 자연/NNG 스럽/XSA-I 게/EC 사라지/VV ᆸ니다/EF ./SF
- `/categories/7/common_concerns/2/q`: 기미/NNG 가/JKS 레이저/NNG 로/JKB 완치/NNG 되/XSV 나요/EF ?/SF
- `/categories/7/common_concerns/2/a`: 기미/NNG 는/JX 체질/NNG 적/XSN 요인/NNG 이/JKS 크/VA 기/ETN 때문/NNB 에/JKB 완치/NNG 이/VCP 라는/ETM 표현/NNG 보다/JKB 는/JX 관리/NNG 이/VCP 라고/EC 보/VV 시/EP 면/EC 되/VV ᆸ니다/EF ./SF 레이저/NNG 로/JKB 개선/NNG 하/XSV ᆯ/ETM 수/NNB 있/VA 지만/EC 재발/NNG 관리/NNG 가/JKS 중요/NNG 하/XSA 어요/EF ./SF
