# S01 — /categories/0 M1 보톡스

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/0/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S01.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/0` | [0] | object | (object, 자식 9) | 54–753 |  |  |
| `/categories/0/id` | id | string | "M1" | 61–63 | 제외(category_code) |  |
| `/categories/0/name` | name | string | "보톡스" | 73–76 | 1토큰 | E0001 |
| `/categories/0/patient_name` | patient_name | string | "주름 보톡스" | 94–100 | 2토큰 | E0002, E0003 |
| `/categories/0/simple_explanation` | simple_explanation | string | "근육을 일시적으로 쉬게 해서 주름을 펴는 주사입니다." | 124–153 | 17토큰 | E0004, E0005, E0006, E0007, E0008 |
| `/categories/0/how_it_works` | how_it_works | string | "주름을 만드는 근육에 약을 주사하면 근육이 쉬면서 주름이 펴집니다. 칼로 자르거나 꿰매지 않아요." | 171–225 | 29토큰 | E0009, E0010, E0011, E0012, E0013 |
| `/categories/0/duration_simple` | duration_simple | string | "약 3-6개월 지속됩니다." | 246–260 | 7토큰 | E0014, E0015 |
| `/categories/0/pain_level` | pain_level | string | "모기 물린 정도의 따끔함" | 276–289 | 8토큰 | E0016, E0017 |
| `/categories/0/downtime` | downtime | string | "바로 일상 복귀 가능" | 303–314 | 4토큰 | E0018, E0019 |
| `/categories/0/common_concerns` | common_concerns | array | (array, 자식 3) | 334–752 |  |  |
| `/categories/0/common_concerns/0` | [0] | object | (object, 자식 2) | 335–426 |  |  |
| `/categories/0/common_concerns/0/q` | q | string | "보톡스 맞으면 표정이 굳나요?" | 341–357 | 8토큰 | E0020, E0021 |
| `/categories/0/common_concerns/0/a` | a | string | "적절한 양을 맞으면 자연스러운 표정을 유지할 수 있어요. 과도하게 맞는 경우에만 표정이 어색할 수 있습니다." | 364–424 | 36토큰 | E0022, E0023, E0024, E0025, E0026 |
| `/categories/0/common_concerns/1` | [1] | object | (object, 자식 2) | 427–490 |  |  |
| `/categories/0/common_concerns/1/q` | q | string | "보톡스에 중독되나요?" | 433–444 | 6토큰 | E0027 |
| `/categories/0/common_concerns/1/a` | a | string | "의학적으로 중독성은 없어요. 효과가 빠지면 원래 상태로 돌아갑니다." | 451–488 | 19토큰 | E0028, E0029, E0030, E0031 |
| `/categories/0/common_concerns/2` | [2] | object | (object, 자식 2) | 491–751 |  |  |
| `/categories/0/common_concerns/2/q` | q | string | "보톡스 맞고 바로 운동해도 되나요?" | 497–516 | 10토큰 | E0032, E0033 |
| `/categories/0/common_concerns/2/a` | a | string | "가벼운 활동은 바로 가능하고, 격한 운동·사우나·음주는 시술 당일(대략 24시간) 삼가는 것이 안전합니다. 시술 후 약 4시간은 눕지 말고 주사 부위를 문지르지 마세요. 최근 연구는 톡신이 수 시간 내 결합해 운동에 의한 이동 위험이 크지 않을 수 있다고 보지만, 이 주의사항은 멍·홍조, 톡신 확산으로 인한 눈꺼풀 처짐(안검하수), 운동·사우나로 인한 땀·오염에 따른 감염 위험을 줄이기 위한 것입니다." | 523–749 | 121토큰 | E0034, E0035, E0036, E0037, E0038, E0039, E0040, E0041, E0042, E0043, E0044, E0045, E0046, E0047, E0048, E0049, E0050, E0051, E0052, E0053, E0054, E0055 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S01-O1 | B | `/categories/0/duration_simple` | 무엇이 3-6개월 지속되는지(효과) 문장에 주어가 생략됨 |
| S01-O2 | B | `/categories/0/how_it_works` | 주사하는 「약」의 이름·성분이 이 항목에 없다 |
| S01-O3 | B | `/categories/0/common_concerns/0/a` | 「적절한 양」「과도하게」의 기준값 미기재 |
| S01-O4 | B | `/categories/0/common_concerns/1/a` | 「의학적으로」의 근거 출처 미기재 |
| S01-O5 | P | `/categories/0/common_concerns/2/a` | 행동 지시(삼가·눕지 말고·문지르지 마세요)와 근거 설명(최근 연구…·이 주의사항은…)이 한 값에 섞여 있다. 시간 기준이 「당일(대략 24시간)」「시술 후 약 4시간」 두 개 |
| S01-O6 | F | `/categories/0/common_concerns/2/a` | 「톡신」과 name 「보톡스」의 관계(호칭 차이)는 의미 단계 과제. 「최근 연구」의 주장과 주의사항이 서로 다른 강도라 구조화 시 근거·지시 분리 필요 |
| S01-O7 | B | `/categories/0/common_concerns/2/a` | 「최근 연구」의 출처 미기재 |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0001 | `/categories/0/name` | 보톡스 | 0–3 | name | 카테고리명 |
| E0002 | `/categories/0/patient_name` | 주름 보톡스 | 0–6 | name,concern | 환자용 명칭 — 고민(주름)+시술명 결합 |
| E0003 | `/categories/0/patient_name` | 주름 | 0–2 | concern |  |
| E0004 | `/categories/0/simple_explanation` | 근육을 일시적으로 쉬게 해서 주름을 펴는 주사입니다. | 0–29 | sentence | 전체 문장 |
| E0005 | `/categories/0/simple_explanation` | 근육을 일시적으로 쉬게 해서 | 0–15 | mechanism,course | 작용 설명 |
| E0006 | `/categories/0/simple_explanation` | 일시적으로 | 4–9 | course | 지속 특성 수식 — 시간 기준 없음 |
| E0007 | `/categories/0/simple_explanation` | 주름을 펴는 | 16–22 | effect,concern |  |
| E0008 | `/categories/0/simple_explanation` | 주사 | 23–25 | route | 투여 형태 |
| E0009 | `/categories/0/how_it_works` | 주름을 만드는 근육에 약을 주사하면 근육이 쉬면서 주름이 펴집니다. | 0–37 | sentence,condition,mechanism |  |
| E0010 | `/categories/0/how_it_works` | 주름을 만드는 근육 | 0–10 | site | 시술 대상 부위를 기능으로 표현 |
| E0011 | `/categories/0/how_it_works` | 약을 주사하면 | 12–19 | condition,route | 약 이름 미기재 |
| E0012 | `/categories/0/how_it_works` | 주름이 펴집니다 | 28–36 | effect |  |
| E0013 | `/categories/0/how_it_works` | 칼로 자르거나 꿰매지 않아요. | 38–54 | sentence,negation | 비수술임을 부정형으로 설명 |
| E0014 | `/categories/0/duration_simple` | 약 3-6개월 지속됩니다. | 0–14 | sentence,time,approx,range,quantity | 지속 대상(효과) 생략 |
| E0015 | `/categories/0/duration_simple` | 약 3-6개월 | 0–7 | approx,range,quantity |  |
| E0016 | `/categories/0/pain_level` | 모기 물린 정도의 따끔함 | 0–13 | sensory,degree,approx | 통증을 비유로 표현 |
| E0017 | `/categories/0/pain_level` | 정도의 | 6–9 | approx |  |
| E0018 | `/categories/0/downtime` | 바로 일상 복귀 가능 | 0–11 | time,possibility |  |
| E0019 | `/categories/0/downtime` | 바로 | 0–2 | time | 시점 — 수치 없음 |
| E0020 | `/categories/0/common_concerns/0/q` | 보톡스 맞으면 표정이 굳나요? | 0–16 | sentence,condition,adverse | 환자 질문 |
| E0021 | `/categories/0/common_concerns/0/q` | 표정이 굳나요 | 8–15 | adverse |  |
| E0022 | `/categories/0/common_concerns/0/a` | 적절한 양을 맞으면 자연스러운 표정을 유지할 수 있어요. | 0–31 | sentence,condition,possibility |  |
| E0023 | `/categories/0/common_concerns/0/a` | 적절한 양을 맞으면 | 0–10 | condition,degree | 양의 기준 미기재 |
| E0024 | `/categories/0/common_concerns/0/a` | 과도하게 맞는 경우에만 표정이 어색할 수 있습니다. | 32–60 | sentence,condition,scope,possibility,adverse |  |
| E0025 | `/categories/0/common_concerns/0/a` | 과도하게 맞는 경우에만 | 32–44 | condition,scope,degree | 「~에만」 한정 |
| E0026 | `/categories/0/common_concerns/0/a` | 표정이 어색할 수 있습니다 | 45–59 | adverse,possibility |  |
| E0027 | `/categories/0/common_concerns/1/q` | 보톡스에 중독되나요? | 0–11 | sentence,adverse |  |
| E0028 | `/categories/0/common_concerns/1/a` | 의학적으로 중독성은 없어요. | 0–15 | sentence,negation,evidence | 근거 출처 미기재 |
| E0029 | `/categories/0/common_concerns/1/a` | 중독성은 없어요 | 6–14 | negation |  |
| E0030 | `/categories/0/common_concerns/1/a` | 효과가 빠지면 원래 상태로 돌아갑니다. | 16–37 | sentence,condition,course |  |
| E0031 | `/categories/0/common_concerns/1/a` | 효과가 빠지면 | 16–23 | condition,course |  |
| E0032 | `/categories/0/common_concerns/2/q` | 보톡스 맞고 바로 운동해도 되나요? | 0–19 | sentence,time,instruction |  |
| E0033 | `/categories/0/common_concerns/2/q` | 바로 | 7–9 | time |  |
| E0034 | `/categories/0/common_concerns/2/a` | 가벼운 활동은 바로 가능하고, 격한 운동·사우나·음주는 시술 당일(대략 24시간) 삼가는 것이 안전합니다. | 0–59 | sentence,possibility,avoid,time | 문장 전체 — 허용(가벼운 활동 바로)과 회피(격한 운동 등 당일)가 한 문장 · verify 문장 탈락 검사로 보충 |
| E0035 | `/categories/0/common_concerns/2/a` | 가벼운 활동은 바로 가능하고 | 0–15 | degree,time,possibility |  |
| E0036 | `/categories/0/common_concerns/2/a` | 가벼운 활동 | 0–6 | degree |  |
| E0037 | `/categories/0/common_concerns/2/a` | 격한 운동·사우나·음주는 시술 당일(대략 24시간) 삼가는 것이 안전합니다. | 17–59 | sentence,avoid,time,approx,quantity |  |
| E0038 | `/categories/0/common_concerns/2/a` | 격한 운동·사우나·음주 | 17–29 | degree,avoid | 회피 대상 3개 나열(·) |
| E0039 | `/categories/0/common_concerns/2/a` | 시술 당일(대략 24시간) | 31–45 | time,approx,quantity | 「당일」과 「대략 24시간」 두 기준 병기 |
| E0040 | `/categories/0/common_concerns/2/a` | 삼가는 것이 안전합니다 | 46–58 | avoid,instruction |  |
| E0041 | `/categories/0/common_concerns/2/a` | 시술 후 약 4시간은 눕지 말고 주사 부위를 문지르지 마세요. | 60–94 | sentence,time,approx,quantity,avoid,negation,site |  |
| E0042 | `/categories/0/common_concerns/2/a` | 시술 후 약 4시간 | 60–70 | time,approx,quantity | 기준 시점=시술 후 |
| E0043 | `/categories/0/common_concerns/2/a` | 눕지 말고 | 72–77 | avoid,negation |  |
| E0044 | `/categories/0/common_concerns/2/a` | 주사 부위를 문지르지 마세요 | 78–93 | avoid,negation,site |  |
| E0045 | `/categories/0/common_concerns/2/a` | 최근 연구는 톡신이 수 시간 내 결합해 운동에 의한 이동 위험이 크지 않을 수 있다고 보지만 | 95–146 | evidence,time,negation,possibility,degree | 연구 출처 미기재 · 단정 회피 |
| E0046 | `/categories/0/common_concerns/2/a` | 톡신 | 102–104 | name | 카테고리명 「보톡스」와 다른 호칭 |
| E0047 | `/categories/0/common_concerns/2/a` | 수 시간 내 | 106–112 | time,approx | 수치 불명확 |
| E0048 | `/categories/0/common_concerns/2/a` | 크지 않을 수 있다 | 131–141 | negation,possibility,degree |  |
| E0049 | `/categories/0/common_concerns/2/a` | 이 주의사항은 멍·홍조, 톡신 확산으로 인한 눈꺼풀 처짐(안검하수), 운동·사우나로 인한 땀·오염에 따른 감염 위험을 줄이기 위한 것입니다. | 148–226 | sentence,rationale,adverse |  |
| E0050 | `/categories/0/common_concerns/2/a` | 멍·홍조 | 156–160 | adverse |  |
| E0051 | `/categories/0/common_concerns/2/a` | 톡신 확산으로 인한 눈꺼풀 처짐(안검하수) | 162–185 | adverse,cause,site,paraphrase | 원인→사건, 괄호는 전문어 |
| E0052 | `/categories/0/common_concerns/2/a` | 눈꺼풀 | 173–176 | site | 부작용 발생 부위 |
| E0053 | `/categories/0/common_concerns/2/a` | 운동·사우나로 인한 땀·오염에 따른 감염 위험 | 187–212 | adverse,cause | 원인 연쇄 2단 |
| E0054 | `/categories/0/common_concerns/2/a` | 최근 연구는 톡신이 수 시간 내 결합해 운동에 의한 이동 위험이 크지 않을 수 있다고 보지만, 이 주의사항은 멍·홍조, 톡신 확산으로 인한 눈꺼풀 처짐(안검하수), 운동·사우나로 인한 땀·오염에 따른 감염 위험을 줄이기 위한 것입니다. | 95–226 | sentence,evidence,rationale,adverse | 문장 전체 — 연구 서술(…보지만)과 주의사항 근거가 한 문장 · verify 문장 탈락 검사로 보충 |
| E0055 | `/categories/0/common_concerns/2/a` | 이 주의사항은 | 148–155 | reference | 앞 문장 지시사항 참조 · 별도 읽기 검토(형태소 수식어 대조)로 보충 |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/0/name`: 보톡스/NNG
- `/categories/0/patient_name`: 주름/NNG 보톡스/NNG
- `/categories/0/simple_explanation`: 근육/NNG 을/JKO 일시/NNG 적/XSN 으로/JKB 쉬/VV 게/EC 하/VX 어서/EC 주름/NNG 을/JKO 펴/VV 는/ETM 주사/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/0/how_it_works`: 주름/NNG 을/JKO 만들/VX 는/ETM 근육/NNG 에/JKB 약/NNG 을/JKO 주사/NNG 하/XSV 면/EC 근육/NNG 이/JKS 쉬/VV 면서/EC 주름/NNG 이/JKS 펴지/VV ᆸ니다/EF ./SF 칼/NNG 로/JKB 자르/VV 거나/EC 꿰매/VV 지/EC 않/VX 어요/EF ./SF
- `/categories/0/duration_simple`: 약/MM 3-6/W_SERIAL 개월/NNB 지속/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/0/pain_level`: 모기/NNG 물리/VV ᆫ/ETM 정도/NNG 의/JKG 따끔/MAG 하/XSA ᆷ/EF
- `/categories/0/downtime`: 바로/MAG 일상/NNG 복귀/NNG 가능/NNG
- `/categories/0/common_concerns/0/q`: 보톡스/NNG 맞/VV 으면/EC 표정/NNG 이/JKS 굳/VV-R 나요/EF ?/SF
- `/categories/0/common_concerns/0/a`: 적절/XR 하/XSA ᆫ/ETM 양/NNG 을/JKO 맞/VV 으면/EC 자연/NNG 스럽/XSA-I 은/ETM 표정/NNG 을/JKO 유지/NNG 하/XSV ᆯ/ETM 수/NNB 있/VA 어요/EF ./SF 과도/NNG 하/XSA 게/EC 맞/VV 는/ETM 경우/NNG 에/JKB 만/JX 표정/NNG 이/JKS 어색/XR 하/XSA ᆯ/ETM 수/NNB 있/VA 습니다/EF ./SF
- `/categories/0/common_concerns/1/q`: 보톡스/NNG 에/JKB 중독/NNG 되/XSV 나요/EF ?/SF
- `/categories/0/common_concerns/1/a`: 의학/NNG 적/XSN 으로/JKB 중독/NNG 성/XSN 은/JX 없/VA 어요/EF ./SF 효과/NNG 가/JKS 빠지/VV 면/EC 원래/NNG 상태/NNG 로/JKB 돌아가/VV ᆸ니다/EF ./SF
- `/categories/0/common_concerns/2/q`: 보톡스/NNG 맞/VV 고/EC 바로/MAG 운동/NNG 하/XSV 어도/EC 되/VV 나요/EF ?/SF
- `/categories/0/common_concerns/2/a`: 가볍/VA-I 은/ETM 활동/NNG 은/JX 바로/MAG 가능/NNG 하/XSA 고/EC ,/SP 격하/VA ᆫ/ETM 운동/NNG ·/SP 사우나/NNG ·/SP 음주/NNG 는/JX 시술/NNG 당일/NNG (/SSO 대략/MAG 24/SN 시간/NNB )/SSC 삼가/VV 는/ETM 것/NNB 이/JKS 안전/NNG 하/XSA ᆸ니다/EF ./SF 시술/NNG 후/NNG 약/MM 4/SN 시간/NNG 은/JX 눕/VV-I 지/EC 말/VX 고/EC 주사/NNG 부위/NNG 를/JKO 문지르/VV 지/EC 말/VX 세요/EF ./SF 최근/NNG 연구/NNG 는/JX 톡신/NNP 이/JKS 수/MM 시간/NNB 내/NNB 결합/NNG 하/XSV 어/EC 운동/NNG 에/JKB 의하/VV ᆫ/ETM 이동/NNG 위험/NNG 이/JKS 크/VA 지/EC 않/VX 을/ETM 수/NNB 있/VA 다고/EC 보/VV 지만/EC ,/SP 이/MM 주의/NNG 사항/NNG 은/JX 멍/NNG ·/SP 홍조/NNG ,/SP 톡신/NNG 확산/NNG 으로/JKB 인하/VV ᆫ/ETM 눈꺼풀/NNG 처지/VV ᆷ/ETN (/SSO 안검하수/NNP )/SSC ,/SP 운동/NNG ·/SP 사우나/NNG 로/JKB 인하/VV ᆫ/ETM 땀/NNG ·/SP 오염/NNG 에/JKB 따르/VV ᆫ/ETM 감염/NNG 위험/NNG 을/JKO 줄이/VV 기/ETN 위하/VV ᆫ/ETM 것/NNB 이/VCP ᆸ니다/EF ./SF
