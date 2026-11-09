# S02 — /categories/1 M2 필러

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/1/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S02.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/1` | [1] | object | (object, 자식 9) | 754–1444 |  |  |
| `/categories/1/id` | id | string | "M2" | 761–763 | 제외(category_code) |  |
| `/categories/1/name` | name | string | "필러" | 773–775 | 1토큰 | E0056 |
| `/categories/1/patient_name` | patient_name | string | "볼륨 필러" | 793–798 | 2토큰 | E0057 |
| `/categories/1/simple_explanation` | simple_explanation | string | "피부 아래에 젤 형태의 물질을 넣어서 꺼진 부위를 채우거나 윤곽을 잡아주는 주사입니다." | 822–870 | 26토큰 | E0058, E0059, E0060, E0061, E0062, E0063 |
| `/categories/1/how_it_works` | how_it_works | string | "우리 피부에 원래 있는 히알루론산(수분을 잡아주는 성분)과 비슷한 젤을 주사로 넣어서 볼륨을 만들어줍니다. 팔자주름, 입술, 광대 등에 사용합니다." | 888–970 | 44토큰 | E0064, E0065, E0066, E0067, E0068, E0069, E0070, E0071, E0072 |
| `/categories/1/duration_simple` | duration_simple | string | "약 6-18개월 지속됩니다 (제품과 부위에 따라 다름)." | 991–1022 | 17토큰 | E0073, E0074, E0075 |
| `/categories/1/pain_level` | pain_level | string | "마취 크림을 바르고 시술하여 약간의 압박감 정도" | 1038–1064 | 12토큰 | E0076, E0077, E0078 |
| `/categories/1/downtime` | downtime | string | "가벼운 붓기가 2-3일, 멍이 들 수 있으나 일상생활 가능" | 1078–1110 | 17토큰 | E0079, E0080, E0081, E0082 |
| `/categories/1/common_concerns` | common_concerns | array | (array, 자식 3) | 1130–1443 |  |  |
| `/categories/1/common_concerns/0` | [0] | object | (object, 자식 2) | 1131–1243 |  |  |
| `/categories/1/common_concerns/0/q` | q | string | "필러가 뭉치거나 울퉁불퉁해질 수 있나요?" | 1137–1159 | 13토큰 | E0083 |
| `/categories/1/common_concerns/0/a` | a | string | "숙련된 의사가 시술하면 매우 드뭅니다. 혹시 발생하더라도 가볍게 마사지하거나, 히알루론산 필러는 녹이는 약이 있어서 교정할 수 있어요." | 1166–1241 | 39토큰 | E0084, E0085, E0086, E0087, E0088, E0089, E0090, E0091, E0092 |
| `/categories/1/common_concerns/1` | [1] | object | (object, 자식 2) | 1244–1326 |  |  |
| `/categories/1/common_concerns/1/q` | q | string | "필러가 얼굴에서 이동하나요?" | 1250–1265 | 8토큰 | E0093 |
| `/categories/1/common_concerns/1/a` | a | string | "최신 필러는 점성이 높아서 주입한 자리에 잘 머뭅니다. 시술 직후 세게 누르지 않으면 됩니다." | 1272–1324 | 27토큰 | E0094, E0095, E0096, E0097, E0098, E0099, E0100 |
| `/categories/1/common_concerns/2` | [2] | object | (object, 자식 2) | 1327–1442 |  |  |
| `/categories/1/common_concerns/2/q` | q | string | "필러 맞다가 혈관에 문제가 생길 수 있나요?" | 1333–1357 | 13토큰 | E0101, E0102 |
| `/categories/1/common_concerns/2/a` | a | string | "매우 드물지만 가능한 위험이므로, 반드시 해부학에 능숙한 전문의에게 시술받으세요. 응급 대처가 가능한 병원에서 시술받는 것이 중요합니다." | 1364–1440 | 39토큰 | E0103, E0104, E0105, E0106, E0107 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S02-O1 | P | `/categories/1/how_it_works` | 히알루론산은 「과 비슷한 젤」로 비교 대상이며, 필러 성분이 히알루론산이라고 단정하지 않는다. 같은 카테고리 a(/common_concerns/0/a)는 「히알루론산 필러는」으로 하위 종류를 한정해 필러에 다른 종류가 있음을 시사 |
| S02-O2 | P | `/categories/1/how_it_works` | 「팔자주름」은 고민 명칭이 부위 나열(입술·광대)에 함께 쓰였다. 부위/고민 구분은 후속 |
| S02-O3 | B | `/categories/1/duration_simple` | 제품별·부위별 지속 기간 값은 원문에 없다(「따라 다름」만) |
| S02-O4 | B | `/categories/1/common_concerns/0/a` | 「녹이는 약」 이름 미기재. 「매우 드뭅니다」 수치 없음 — 백분율로 바꾸지 않는다 |
| S02-O5 | B | `/categories/1/common_concerns/2/a` | 혈관 문제의 구체 사건·응급 징후·대처 방법이 기재되지 않음(「응급 대처가 가능한 병원」만) |
| S02-O6 | F | `/categories/1/common_concerns/2/q` | 「혈관에 문제」가 어떤 사건을 가리키는지는 다른 원장(합병증 등)과 연결해 판단할 후속 과제 |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0056 | `/categories/1/name` | 필러 | 0–2 | name |  |
| E0057 | `/categories/1/patient_name` | 볼륨 필러 | 0–5 | name,effect | 효과(볼륨)+시술명 |
| E0058 | `/categories/1/simple_explanation` | 피부 아래에 젤 형태의 물질을 넣어서 꺼진 부위를 채우거나 윤곽을 잡아주는 주사입니다. | 0–48 | sentence |  |
| E0059 | `/categories/1/simple_explanation` | 피부 아래에 | 0–6 | site,depth | 층 표현 — 깊이 수치 없음 |
| E0060 | `/categories/1/simple_explanation` | 젤 형태의 물질 | 7–15 | substance | 물질명 미기재 |
| E0061 | `/categories/1/simple_explanation` | 꺼진 부위를 채우거나 | 21–32 | concern,effect,site | 「거나」 대안 나열 |
| E0062 | `/categories/1/simple_explanation` | 윤곽을 잡아주는 | 33–41 | effect |  |
| E0063 | `/categories/1/simple_explanation` | 주사 | 42–44 | route |  |
| E0064 | `/categories/1/how_it_works` | 우리 피부에 원래 있는 히알루론산(수분을 잡아주는 성분)과 비슷한 젤을 주사로 넣어서 볼륨을 만들어줍니다. | 0–59 | sentence |  |
| E0065 | `/categories/1/how_it_works` | 히알루론산(수분을 잡아주는 성분) | 13–31 | substance,paraphrase |  |
| E0066 | `/categories/1/how_it_works` | 히알루론산(수분을 잡아주는 성분)과 비슷한 젤 | 13–38 | substance,comparison | 「비슷한」 — 같은 물질인지 미단정 |
| E0067 | `/categories/1/how_it_works` | 볼륨을 만들어줍니다 | 48–58 | effect |  |
| E0068 | `/categories/1/how_it_works` | 팔자주름, 입술, 광대 등에 사용합니다. | 60–82 | sentence,site | 「등」 열린 목록 |
| E0069 | `/categories/1/how_it_works` | 팔자주름 | 60–64 | site,concern | 고민 명칭이 적용 부위 자리에 쓰임 |
| E0070 | `/categories/1/how_it_works` | 입술 | 66–68 | site |  |
| E0071 | `/categories/1/how_it_works` | 광대 | 70–72 | site |  |
| E0072 | `/categories/1/how_it_works` | 우리 피부에 원래 있는 | 0–12 | site,course | 내인성 성분이라는 서술 · 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0073 | `/categories/1/duration_simple` | 약 6-18개월 지속됩니다 (제품과 부위에 따라 다름). | 0–31 | sentence,time,approx,range,quantity,condition |  |
| E0074 | `/categories/1/duration_simple` | 약 6-18개월 | 0–8 | approx,range,quantity |  |
| E0075 | `/categories/1/duration_simple` | (제품과 부위에 따라 다름) | 15–30 | condition | 변동 조건 — 제품별·부위별 값 미기재 |
| E0076 | `/categories/1/pain_level` | 마취 크림을 바르고 시술하여 약간의 압박감 정도 | 0–26 | sensory,degree,approx,condition |  |
| E0077 | `/categories/1/pain_level` | 마취 크림 | 0–5 | substance |  |
| E0078 | `/categories/1/pain_level` | 약간의 압박감 정도 | 16–26 | degree,sensory,approx |  |
| E0079 | `/categories/1/downtime` | 가벼운 붓기가 2-3일, 멍이 들 수 있으나 일상생활 가능 | 0–32 | adverse,time,range,possibility |  |
| E0080 | `/categories/1/downtime` | 가벼운 붓기가 2-3일 | 0–12 | degree,adverse,time,range,quantity | 지속 기간 |
| E0081 | `/categories/1/downtime` | 멍이 들 수 있으나 | 14–24 | adverse,possibility |  |
| E0082 | `/categories/1/downtime` | 일상생활 가능 | 25–32 | possibility |  |
| E0083 | `/categories/1/common_concerns/0/q` | 필러가 뭉치거나 울퉁불퉁해질 수 있나요? | 0–22 | sentence,adverse,possibility |  |
| E0084 | `/categories/1/common_concerns/0/a` | 숙련된 의사가 시술하면 매우 드뭅니다. | 0–21 | sentence,condition,actor,frequency | 빈도의 대상(뭉침·울퉁불퉁) 생략 |
| E0085 | `/categories/1/common_concerns/0/a` | 숙련된 의사가 시술하면 | 0–12 | condition,actor |  |
| E0086 | `/categories/1/common_concerns/0/a` | 매우 드뭅니다 | 13–20 | frequency,degree | 수치 없음 |
| E0087 | `/categories/1/common_concerns/0/a` | 혹시 발생하더라도 가볍게 마사지하거나, 히알루론산 필러는 녹이는 약이 있어서 교정할 수 있어요. | 22–75 | sentence,condition,management,possibility |  |
| E0088 | `/categories/1/common_concerns/0/a` | 혹시 발생하더라도 | 22–31 | condition,possibility |  |
| E0089 | `/categories/1/common_concerns/0/a` | 가볍게 마사지하거나 | 32–42 | degree,management | 「거나」 대안 |
| E0090 | `/categories/1/common_concerns/0/a` | 히알루론산 필러는 | 44–53 | scope,name | 교정 수단을 히알루론산 필러로 한정 |
| E0091 | `/categories/1/common_concerns/0/a` | 녹이는 약 | 54–59 | substance | 약 이름 미기재 |
| E0092 | `/categories/1/common_concerns/0/a` | 교정할 수 있어요 | 65–74 | possibility,management |  |
| E0093 | `/categories/1/common_concerns/1/q` | 필러가 얼굴에서 이동하나요? | 0–15 | sentence,adverse,site |  |
| E0094 | `/categories/1/common_concerns/1/a` | 최신 필러는 점성이 높아서 주입한 자리에 잘 머뭅니다. | 0–30 | sentence,scope,rationale |  |
| E0095 | `/categories/1/common_concerns/1/a` | 최신 필러는 | 0–6 | scope | 「최신」 기준 미기재 |
| E0096 | `/categories/1/common_concerns/1/a` | 점성이 높아서 | 7–14 | degree,rationale |  |
| E0097 | `/categories/1/common_concerns/1/a` | 주입한 자리에 잘 머뭅니다 | 15–29 | site,effect |  |
| E0098 | `/categories/1/common_concerns/1/a` | 시술 직후 세게 누르지 않으면 됩니다. | 31–52 | sentence,time,degree,negation,instruction,condition |  |
| E0099 | `/categories/1/common_concerns/1/a` | 시술 직후 | 31–36 | time |  |
| E0100 | `/categories/1/common_concerns/1/a` | 세게 누르지 않으면 | 37–47 | degree,negation,condition,avoid |  |
| E0101 | `/categories/1/common_concerns/2/q` | 필러 맞다가 혈관에 문제가 생길 수 있나요? | 0–24 | sentence,time,site,adverse,possibility |  |
| E0102 | `/categories/1/common_concerns/2/q` | 혈관에 문제 | 7–13 | adverse,site | 문제의 내용 미특정 |
| E0103 | `/categories/1/common_concerns/2/a` | 매우 드물지만 가능한 위험이므로, 반드시 해부학에 능숙한 전문의에게 시술받으세요. | 0–45 | sentence,frequency,possibility,instruction,actor |  |
| E0104 | `/categories/1/common_concerns/2/a` | 매우 드물지만 가능한 위험 | 0–14 | frequency,degree,possibility,adverse |  |
| E0105 | `/categories/1/common_concerns/2/a` | 반드시 해부학에 능숙한 전문의에게 시술받으세요 | 19–44 | instruction,actor | 「반드시」 강한 권고 |
| E0106 | `/categories/1/common_concerns/2/a` | 응급 대처가 가능한 병원에서 시술받는 것이 중요합니다. | 46–76 | sentence,emergency,instruction,actor |  |
| E0107 | `/categories/1/common_concerns/2/a` | 응급 대처가 가능한 병원 | 46–59 | emergency,actor |  |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/1/name`: 필러/NNP
- `/categories/1/patient_name`: 볼륨/NNG 필러/NNP
- `/categories/1/simple_explanation`: 피부/NNG 아래/NNG 에/JKB 젤/NNG 형태/NNG 의/JKG 물질/NNG 을/JKO 넣/VV 어서/EC 꺼지/VV ᆫ/ETM 부위/NNG 를/JKO 채우/VV 거나/EC 윤곽/NNG 을/JKO 잡/VV-R 어/EC 주/VX 는/ETM 주사/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/1/how_it_works`: 우리/NP 피부/NNG 에/JKB 원래/MAG 있/VA 는/ETM 히알루론산/NNP (/SSO 수분/NNG 을/JKO 잡/VV-R 어/EC 주/VX 는/ETM 성분/NNG )/SSC 과/JKB 비슷하/VA ᆫ/ETM 젤/NNG 을/JKO 주사/NNG 로/JKB 넣/VV 어서/EC 볼륨/NNG 을/JKO 만들/VV 어/EC 주/VX ᆸ니다/EF ./SF 팔자/NNG 주름/NNG ,/SP 입술/NNG ,/SP 광대/NNG 등/NNB 에/JKB 사용/NNG 하/XSV ᆸ니다/EF ./SF
- `/categories/1/duration_simple`: 약/MM 6-18/W_SERIAL 개월/NNB 지속/NNG 되/XSV ᆸ니다/EF (/SSO 제품/NNG 과/JKB 부위/NNG 에/JKB 따르/VV 어/EC 다르/VA ᆷ/ETN )/SSC ./SF
- `/categories/1/pain_level`: 마취/NNG 크림/NNG 을/JKO 바르/VV 고/EC 시술/NNG 하/XSV 어/EC 약간/NNG 의/JKG 압박감/NNG 정도/NNG
- `/categories/1/downtime`: 가볍/VA-I 은/ETM 붓/NNG 기/XSN 가/JKS 2-3/W_SERIAL 일/NNB ,/SP 멍/NNG 이/JKS 들/VV ᆯ/ETM 수/NNB 있/VA 으나/EC 일상생활/NNG 가능/NNG
- `/categories/1/common_concerns/0/q`: 필러/NNP 가/JKS 뭉치/VV 거나/EC 울퉁불퉁/MAG 하/XSA 어/EC 지/VX ᆯ/ETM 수/NNB 있/VA 나요/EF ?/SF
- `/categories/1/common_concerns/0/a`: 숙련/NNG 되/XSV ᆫ/ETM 의사/NNG 가/JKS 시술/NNG 하/XSV 면/EC 매우/MAG 드물/VA ᆸ니다/EF ./SF 혹시/MAG 발생/NNG 하/XSV 더라도/EC 가볍/VA-I 게/EC 마사지/NNG 하/XSV 거나/EC ,/SP 히알루론산/NNP 필/NNG 러/EC 는/JX 녹이/VV 는/ETM 약/NNG 이/JKS 있/VA 어서/EC 교정/NNG 하/XSV ᆯ/ETM 수/NNB 있/VA 어요/EF ./SF
- `/categories/1/common_concerns/1/q`: 필러/NNP 가/JKS 얼굴/NNG 에서/JKB 이동/NNG 하/XSV 나요/EF ?/SF
- `/categories/1/common_concerns/1/a`: 최신/NNG 필러/NNP 는/JX 점성/NNG 이/JKS 높/VA 어서/EC 주입/NNG 하/XSV ᆫ/ETM 자리/NNG 에/JKB 잘/MAG 머물/VV ᆸ니다/EF ./SF 시술/NNG 직후/NNG 세/VA 게/EC 누르/VV 지/EC 않/VX 으면/EC 되/VV ᆸ니다/EF ./SF
- `/categories/1/common_concerns/2/q`: 필러/NNP 맞/VV 다가/EC 혈관/NNG 에/JKB 문제/NNG 가/JKS 생기/VV ᆯ/ETM 수/NNB 있/VA 나요/EF ?/SF
- `/categories/1/common_concerns/2/a`: 매우/MAG 드물/VA 지만/EC 가능/NNG 하/XSA ᆫ/ETM 위험/NNG 이/VCP 므로/EC ,/SP 반드시/MAG 해부학/NNG 에/JKB 능숙/XR 하/XSA ᆫ/ETM 전문의/NNG 에게/JKB 시술/NNG 받/VV-R 으세요/EF ./SF 응급/NNG 대처/NNG 가/JKS 가능/NNG 하/XSA ᆫ/ETM 병원/NNG 에서/JKB 시술/NNG 받/XSV 는/ETM 것/NNB 이/JKS 중요/NNG 하/XSA ᆸ니다/EF ./SF
