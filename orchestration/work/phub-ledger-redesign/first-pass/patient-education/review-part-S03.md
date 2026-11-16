# S03 — /categories/2 M3 바이오스티뮬레이터/콜라겐부스터

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/2/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S03.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/2` | [2] | object | (object, 자식 9) | 1445–2219 |  |  |
| `/categories/2/id` | id | string | "M3" | 1452–1454 | 제외(category_code) |  |
| `/categories/2/name` | name | string | "바이오스티뮬레이터/콜라겐부스터" | 1464–1480 | 3토큰 | E0108, E0109, E0110 |
| `/categories/2/patient_name` | patient_name | string | "콜라겐 재생 주사" | 1498–1507 | 3토큰 | E0111 |
| `/categories/2/simple_explanation` | simple_explanation | string | "피부 속에서 콜라겐(피부 탄력 성분)이 스스로 만들어지도록 돕는 주사입니다." | 1531–1573 | 21토큰 | E0112, E0113, E0114, E0115 |
| `/categories/2/how_it_works` | how_it_works | string | "특수 성분을 피부 아래에 주사하면, 우리 몸이 그 주변에 새로운 콜라겐을 만들어냅니다. 당장 볼륨이 채워지는 게 아니라, 몇 주에 걸쳐 서서히 피부가 탱탱해집니다." | 1591–1682 | 51토큰 | E0116, E0117, E0118, E0119, E0120, E0121, E0122, E0123, E0124, E0125 |
| `/categories/2/duration_simple` | duration_simple | string | "효과 발현까지 4-6주, 지속 기간은 1-3년입니다." | 1703–1732 | 14토큰 | E0126, E0127, E0128 |
| `/categories/2/pain_level` | pain_level | string | "주사 시 약간의 통증, 마취 크림 사용 가능" | 1748–1772 | 10토큰 | E0129, E0130, E0131, E0132 |
| `/categories/2/downtime` | downtime | string | "가벼운 붓기 2-3일, 일상생활 가능" | 1786–1806 | 9토큰 | E0133, E0134 |
| `/categories/2/common_concerns` | common_concerns | array | (array, 자식 3) | 1826–2218 |  |  |
| `/categories/2/common_concerns/0` | [0] | object | (object, 자식 2) | 1827–1927 |  |  |
| `/categories/2/common_concerns/0/q` | q | string | "효과가 바로 보이나요?" | 1833–1845 | 6토큰 | E0135 |
| `/categories/2/common_concerns/0/a` | a | string | "아닙니다. 콜라겐이 새로 만들어지는 데 시간이 필요해서, 4-6주 후부터 서서히 효과가 나타나요. 보통 3회 정도 반복 시술합니다." | 1852–1925 | 36토큰 | E0136, E0137, E0138, E0139, E0140, E0141, E0142 |
| `/categories/2/common_concerns/1` | [1] | object | (object, 자식 2) | 1928–2110 |  |  |
| `/categories/2/common_concerns/1/q` | q | string | "결절(딱딱한 덩어리)이 생길 수 있나요?" | 1934–1956 | 14토큰 | E0143, E0144 |
| `/categories/2/common_concerns/1/a` | a | string | "결절 예방은 마사지보다 시술자의 희석량·주입 깊이가 핵심입니다. 시술 직후 의사가 부드럽게 펴 발라주면 충분하고, 집에서 강박적으로 문지를 필요는 없어요(마사지의 결절 예방 효과는 임상연구에서 입증되지 않았습니다). 하시더라도 세게 하지 말고 부드럽게 하세요." | 1963–2108 | 76토큰 | E0145, E0146, E0147, E0148, E0149, E0150, E0151, E0152, E0153, E0154 |
| `/categories/2/common_concerns/2` | [2] | object | (object, 자식 2) | 2111–2217 |  |  |
| `/categories/2/common_concerns/2/q` | q | string | "필러와 뭐가 다른가요?" | 2117–2129 | 8토큰 | E0155 |
| `/categories/2/common_concerns/2/a` | a | string | "필러는 볼륨을 바로 채워주지만, 콜라겐 부스터는 내 피부가 스스로 콜라겐을 만들게 해서 자연스럽게 탄력이 개선됩니다. 지속 기간도 더 길어요." | 2136–2215 | 40토큰 | E0156, E0157, E0158, E0159, E0160, E0161, E0162 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S03-O1 | F | `/categories/2/name` | 「/」 로 묶인 두 호칭의 관계(동의어/대안/상하) 미확정 — README 기호 규칙만으로 확정하지 않는다 |
| S03-O2 | B | `/categories/2/how_it_works` | 「특수 성분」 이름 미기재 |
| S03-O3 | P | `/categories/2/duration_simple` | 시간 역할이 발현(4-6주)과 지속(1-3년)으로 분리 기재된 사례 |
| S03-O4 | P | `/categories/2/common_concerns/0/a` | 「4-6주 후부터」 기준 시점 생략. duration_simple 「효과 발현까지 4-6주」와 같은 수치. 「보통 3회」 간격 미기재(B) |
| S03-O5 | P | `/categories/2/common_concerns/1/a` | 마사지 권고에 대한 부정(입증되지 않음)·조건부 허용(하시더라도…부드럽게)이 겹친 구조 |
| S03-O6 | F | `/categories/2/common_concerns/2/a` | 「필러」 참조는 S02(/categories/1)로 보이나 연결은 후속. 「지속 기간도 더 길어요」 비교는 원문 수치(1-3년 vs 6-18개월)로 정합 확인 가능 — 의미 단계에서 확인 |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0108 | `/categories/2/name` | 바이오스티뮬레이터/콜라겐부스터 | 0–16 | name,alternative | 「/」 — README 규칙상 대안 기호이나 여기서는 두 호칭일 가능성. 관계 미확정 |
| E0109 | `/categories/2/name` | 바이오스티뮬레이터 | 0–9 | name |  |
| E0110 | `/categories/2/name` | 콜라겐부스터 | 10–16 | name |  |
| E0111 | `/categories/2/patient_name` | 콜라겐 재생 주사 | 0–9 | name,effect,route |  |
| E0112 | `/categories/2/simple_explanation` | 피부 속에서 콜라겐(피부 탄력 성분)이 스스로 만들어지도록 돕는 주사입니다. | 0–42 | sentence |  |
| E0113 | `/categories/2/simple_explanation` | 피부 속에서 | 0–6 | site,depth |  |
| E0114 | `/categories/2/simple_explanation` | 콜라겐(피부 탄력 성분) | 7–20 | substance,paraphrase |  |
| E0115 | `/categories/2/simple_explanation` | 스스로 만들어지도록 | 22–32 | manner,mechanism |  |
| E0116 | `/categories/2/how_it_works` | 특수 성분을 피부 아래에 주사하면, 우리 몸이 그 주변에 새로운 콜라겐을 만들어냅니다. | 0–48 | sentence,condition,mechanism |  |
| E0117 | `/categories/2/how_it_works` | 특수 성분 | 0–5 | substance | 성분명 미기재 |
| E0118 | `/categories/2/how_it_works` | 피부 아래에 | 7–13 | site,depth |  |
| E0119 | `/categories/2/how_it_works` | 그 주변에 | 26–31 | site | 지시어 — 주사 부위 주변 |
| E0120 | `/categories/2/how_it_works` | 당장 볼륨이 채워지는 게 아니라, 몇 주에 걸쳐 서서히 피부가 탱탱해집니다. | 49–91 | sentence,negation,time,manner,effect |  |
| E0121 | `/categories/2/how_it_works` | 당장 볼륨이 채워지는 게 아니라 | 49–66 | negation,time,comparison |  |
| E0122 | `/categories/2/how_it_works` | 몇 주에 걸쳐 | 68–75 | time,approx | 수치 불명확 |
| E0123 | `/categories/2/how_it_works` | 서서히 | 76–79 | manner | 변화 속도 — 효과 발현 |
| E0124 | `/categories/2/how_it_works` | 피부가 탱탱해집니다 | 80–90 | effect |  |
| E0125 | `/categories/2/how_it_works` | 새로운 콜라겐을 만들어냅니다 | 32–47 | mechanism,effect | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0126 | `/categories/2/duration_simple` | 효과 발현까지 4-6주, 지속 기간은 1-3년입니다. | 0–29 | sentence,time,range,quantity | 시간 역할 두 개(발현·지속) 명시 |
| E0127 | `/categories/2/duration_simple` | 효과 발현까지 4-6주 | 0–12 | time,range,quantity | 역할=효과 발현 |
| E0128 | `/categories/2/duration_simple` | 지속 기간은 1-3년 | 14–25 | time,range,quantity | 역할=지속 |
| E0129 | `/categories/2/pain_level` | 주사 시 약간의 통증, 마취 크림 사용 가능 | 0–24 | sensory,degree,time,possibility |  |
| E0130 | `/categories/2/pain_level` | 주사 시 | 0–4 | time,condition |  |
| E0131 | `/categories/2/pain_level` | 약간의 통증 | 5–11 | degree,sensory |  |
| E0132 | `/categories/2/pain_level` | 마취 크림 사용 가능 | 13–24 | substance,possibility |  |
| E0133 | `/categories/2/downtime` | 가벼운 붓기 2-3일, 일상생활 가능 | 0–20 | adverse,degree,time,range,quantity,possibility |  |
| E0134 | `/categories/2/downtime` | 가벼운 붓기 2-3일 | 0–11 | degree,adverse,time,range,quantity |  |
| E0135 | `/categories/2/common_concerns/0/q` | 효과가 바로 보이나요? | 0–12 | sentence,time,effect |  |
| E0136 | `/categories/2/common_concerns/0/a` | 아닙니다. | 0–5 | negation |  |
| E0137 | `/categories/2/common_concerns/0/a` | 콜라겐이 새로 만들어지는 데 시간이 필요해서, 4-6주 후부터 서서히 효과가 나타나요. | 6–54 | sentence,rationale,time,range,manner |  |
| E0138 | `/categories/2/common_concerns/0/a` | 4-6주 후부터 | 32–40 | time,range,quantity | 기준 시점 생략(시술 후로 보임 — 잠정) |
| E0139 | `/categories/2/common_concerns/0/a` | 서서히 효과가 나타나요 | 41–53 | manner,effect |  |
| E0140 | `/categories/2/common_concerns/0/a` | 보통 3회 정도 반복 시술합니다. | 55–73 | sentence,frequency,quantity,approx | 간격 미기재 |
| E0141 | `/categories/2/common_concerns/0/a` | 보통 3회 정도 | 55–63 | frequency,quantity,approx | README: 회차는 일정 수식어 |
| E0142 | `/categories/2/common_concerns/0/a` | 시간이 필요해서 | 22–30 | time,rationale | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0143 | `/categories/2/common_concerns/1/q` | 결절(딱딱한 덩어리)이 생길 수 있나요? | 0–22 | sentence,adverse,paraphrase,possibility |  |
| E0144 | `/categories/2/common_concerns/1/q` | 결절(딱딱한 덩어리) | 0–11 | adverse,paraphrase |  |
| E0145 | `/categories/2/common_concerns/1/a` | 결절 예방은 마사지보다 시술자의 희석량·주입 깊이가 핵심입니다. | 0–35 | sentence,comparison,actor,depth,rationale |  |
| E0146 | `/categories/2/common_concerns/1/a` | 마사지보다 | 7–12 | comparison |  |
| E0147 | `/categories/2/common_concerns/1/a` | 시술자의 희석량·주입 깊이 | 13–27 | actor,depth,quantity | 수치 미기재 |
| E0148 | `/categories/2/common_concerns/1/a` | 시술 직후 의사가 부드럽게 펴 발라주면 충분하고, 집에서 강박적으로 문지를 필요는 없어요(마사지의 결절 예방 효과는 임상연구에서 입증되지 않았습니다). | 36–120 | sentence |  |
| E0149 | `/categories/2/common_concerns/1/a` | 시술 직후 의사가 부드럽게 펴 발라주면 충분하고 | 36–62 | time,actor,manner,condition |  |
| E0150 | `/categories/2/common_concerns/1/a` | 부드럽게 | 46–50 | manner,degree |  |
| E0151 | `/categories/2/common_concerns/1/a` | 집에서 강박적으로 문지를 필요는 없어요 | 64–85 | place,degree,negation,instruction |  |
| E0152 | `/categories/2/common_concerns/1/a` | (마사지의 결절 예방 효과는 임상연구에서 입증되지 않았습니다) | 85–119 | evidence,negation | 연구 출처 미기재 |
| E0153 | `/categories/2/common_concerns/1/a` | 하시더라도 세게 하지 말고 부드럽게 하세요. | 121–145 | sentence,condition,degree,avoid,instruction |  |
| E0154 | `/categories/2/common_concerns/1/a` | 세게 하지 말고 | 127–135 | degree,avoid,negation |  |
| E0155 | `/categories/2/common_concerns/2/q` | 필러와 뭐가 다른가요? | 0–12 | sentence,comparison,reference | 다른 카테고리(필러) 참조 |
| E0156 | `/categories/2/common_concerns/2/a` | 필러는 볼륨을 바로 채워주지만, 콜라겐 부스터는 내 피부가 스스로 콜라겐을 만들게 해서 자연스럽게 탄력이 개선됩니다. | 0–65 | sentence,comparison,reference |  |
| E0157 | `/categories/2/common_concerns/2/a` | 필러는 볼륨을 바로 채워주지만 | 0–16 | reference,time,effect |  |
| E0158 | `/categories/2/common_concerns/2/a` | 콜라겐 부스터 | 18–25 | name | name 「콜라겐부스터」와 띄어쓰기 다름 |
| E0159 | `/categories/2/common_concerns/2/a` | 자연스럽게 탄력이 개선됩니다 | 49–64 | manner,effect |  |
| E0160 | `/categories/2/common_concerns/2/a` | 지속 기간도 더 길어요. | 66–79 | sentence,comparison,time | 비교 기준 수치 미기재 |
| E0161 | `/categories/2/common_concerns/2/a` | 지속 기간도 더 길어요 | 66–78 | comparison,time | regex 대조 후 보충(구절 누락 수정) |
| E0162 | `/categories/2/common_concerns/2/a` | 스스로 콜라겐을 만들게 해서 | 33–48 | manner,mechanism | 별도 읽기 검토(형태소 수식어 대조)로 보충 |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/2/name`: 바이오스티뮬레이터/NNP //SP 콜라겐부스터/NNP
- `/categories/2/patient_name`: 콜라겐/NNP 재생/NNG 주사/NNG
- `/categories/2/simple_explanation`: 피부/NNG 속/NNG 에서/JKB 콜라겐/NNP (/SSO 피부/NNG 탄력/NNG 성분/NNG )/SSC 이/JKS 스스로/MAG 만들/VV 어/EC 지/VX 도록/EC 돕/VV-I 는/ETM 주사/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/2/how_it_works`: 특수/NNG 성분/NNG 을/JKO 피부/NNG 아래/NNG 에/JKB 주사/NNG 하/XSV 면/EC ,/SP 우리/NP 몸/NNG 이/JKS 그/MM 주변/NNG 에/JKB 새롭/VA-I 은/ETM 콜라겐/NNP 을/JKO 만들/VV 어/EC 내/VX ᆸ니다/EF ./SF 당장/NNG 볼륨/NNG 이/JKS 채우/VV 어/EC 지/VX 는/ETM 것/NNB 이/JKC 아니/VCN 라/EC ,/SP 몇/MM 주/NNB 에/JKB 걸치/VV 어/EC 서서히/MAG 피부/NNG 가/JKS 탱탱/MAG 하/XSA 어/EC 지/VX ᆸ니다/EF ./SF
- `/categories/2/duration_simple`: 효과/NNG 발현/NNG 까지/JX 4-6/W_SERIAL 주/NNG ,/SP 지속/NNG 기간/NNG 은/JX 1-3/W_SERIAL 년/NNB 이/VCP ᆸ니다/EF ./SF
- `/categories/2/pain_level`: 주사/NNG 시/NNB 약간/NNG 의/JKG 통증/NNG ,/SP 마취/NNG 크림/NNG 사용/NNG 가능/NNG
- `/categories/2/downtime`: 가볍/VA-I 은/ETM 붓/NNG 기/XSN 2-3/W_SERIAL 일/NNG ,/SP 일상생활/NNG 가능/NNG
- `/categories/2/common_concerns/0/q`: 효과/NNG 가/JKS 바로/MAG 보이/VV 나요/EF ?/SF
- `/categories/2/common_concerns/0/a`: 아니/VCN ᆸ니다/EF ./SF 콜라겐/NNP 이/JKS 새로/MAG 만들/VV 어/EC 지/VX 는/ETM 데/NNB 시간/NNG 이/JKS 필요/NNG 하/XSA 어서/EC ,/SP 4-6/W_SERIAL 주/NNB 후/NNG 부터/JX 서서히/MAG 효과/NNG 가/JKS 나타나/VV 어요/EF ./SF 보통/MAG 3/SN 회/NNB 정도/NNG 반복/NNG 시술/NNG 하/XSV ᆸ니다/EF ./SF
- `/categories/2/common_concerns/1/q`: 결절/NNG (/SSO 딱딱/XR 하/XSA ᆫ/ETM 덩어리/NNG )/SSC 이/JKS 생기/VV ᆯ/ETM 수/NNB 있/VA 나요/EF ?/SF
- `/categories/2/common_concerns/1/a`: 결절/NNG 예방/NNG 은/JX 마사지/NNG 보다/JKB 시술자/NNG 의/JKG 희석/NNG 량/NNG ·/SP 주입/NNG 깊이/NNG 가/JKS 핵심/NNG 이/VCP ᆸ니다/EF ./SF 시술/NNG 직후/NNG 의사/NNG 가/JKS 부드럽/VA-I 게/EC 펴/VV 어/EC 바르/VV 어/EC 주/VX 면/EC 충분/XR 하/XSA 고/EC ,/SP 집/NNG 에서/JKB 강박/NNG 적/XSN 으로/JKB 문지르/VV ᆯ/ETM 필요/NNG 는/JX 없/VA 어요/EF (/SSO 마사지/NNG 의/JKG 결절/NNG 예방/NNG 효과/NNG 는/JX 임상/NNG 연구/NNG 에서/JKB 입증/NNG 되/XSV 지/EC 않/VX 었/EP 습니다/EF )/SSC ./SF 하/VV 시/EP 더라도/EC 세/VA 게/EC 하/VV 지/EC 말/VX 고/EC 부드럽/VA-I 게/EC 하/VV 세요/EF ./SF
- `/categories/2/common_concerns/2/q`: 필러/NNP 와/JC 뭐/NP 가/JKS 다르/VA ᆫ가/EF 요/JX ?/SF
- `/categories/2/common_concerns/2/a`: 필러/NNP 는/JX 볼륨/NNG 을/JKO 바로/MAG 채우/VV 어/EC 주/VX 지만/EC ,/SP 콜라겐/NNP 부스터/NNP 는/JX 나/NP 의/JKG 피부/NNG 가/JKS 스스로/MAG 콜라겐/NNP 을/JKO 만들/VV 게/EC 하/VX 어서/EC 자연/NNG 스럽/XSA-I 게/EC 탄력/NNG 이/JKS 개선/NNG 되/XSV ᆸ니다/EF ./SF 지속/NNG 기간/NNG 도/JX 더/MAG 길/VA 어요/EF ./SF
