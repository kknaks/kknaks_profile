# S06 — /categories/5 M6 지방이식

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/5/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S06.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/5` | [5] | object | (object, 자식 9) | 3671–4419 |  |  |
| `/categories/5/id` | id | string | "M6" | 3678–3680 | 제외(category_code) |  |
| `/categories/5/name` | name | string | "지방이식" | 3690–3694 | 2토큰 | E0259 |
| `/categories/5/patient_name` | patient_name | string | "내 지방으로 볼륨 채우기" | 3712–3725 | 7토큰 | E0260 |
| `/categories/5/simple_explanation` | simple_explanation | string | "본인의 지방을 다른 부위에서 채취해서 얼굴에 넣어주는 시술입니다." | 3749–3785 | 20토큰 | E0261, E0262, E0263 |
| `/categories/5/how_it_works` | how_it_works | string | "복부나 허벅지 같은 부위에서 소량의 지방을 뽑아 정제한 뒤, 얼굴의 꺼진 부위(볼, 이마, 관자놀이 등)에 미세하게 주입합니다. 생착된 지방은 오래 유지됩니다." | 3803–3892 | 49토큰 | E0264, E0265, E0266, E0267, E0268, E0269, E0270, E0271, E0272 |
| `/categories/5/duration_simple` | duration_simple | string | "생착률은 개인차·부위차가 커서 평균 약 40~50% 정도가 유지되는 것으로 보고됩니다. 코·이마 등은 상대적으로 낮고 볼·턱은 높은 편이라, 일부 흡수를 고려해 여유 있게 주입합니다. 생착된 조직은 유지되지만 노화에 따른 전반적 볼륨 감소는 계속됩니다." | 3913–4054 | 81토큰 | E0273, E0274, E0275, E0276, E0277, E0278, E0279, E0280, E0281, E0282, E0283 |
| `/categories/5/pain_level` | pain_level | string | "국소 마취 하에 시술, 시술 중 통증 거의 없음" | 4070–4096 | 12토큰 | E0284, E0285, E0286 |
| `/categories/5/downtime` | downtime | string | "붓기와 멍이 1-3주, 사회 활동 복귀까지 약 1주" | 4110–4138 | 15토큰 | E0287, E0288, E0289 |
| `/categories/5/common_concerns` | common_concerns | array | (array, 자식 3) | 4158–4418 |  |  |
| `/categories/5/common_concerns/0` | [0] | object | (object, 자식 2) | 4159–4254 |  |  |
| `/categories/5/common_concerns/0/q` | q | string | "지방이 다 흡수되지는 않나요?" | 4165–4181 | 10토큰 | E0290 |
| `/categories/5/common_concerns/0/a` | a | string | "일부 흡수가 일어나므로 의사가 약간 여유 있게 넣습니다. 보통 3개월 후 안정화되며, 생착된 지방은 오래 유지돼요." | 4188–4252 | 33토큰 | E0291, E0292, E0293, E0294, E0295, E0296 |
| `/categories/5/common_concerns/1` | [1] | object | (object, 자식 2) | 4255–4326 |  |  |
| `/categories/5/common_concerns/1/q` | q | string | "지방 뽑는 부위가 움푹 꺼지지 않나요?" | 4261–4282 | 11토큰 | E0297 |
| `/categories/5/common_concerns/1/a` | a | string | "소량만 채취하고 균일하게 뽑기 때문에 눈에 띄는 변화는 없어요." | 4289–4324 | 21토큰 | E0298, E0299, E0300, E0301 |
| `/categories/5/common_concerns/2` | [2] | object | (object, 자식 2) | 4327–4417 |  |  |
| `/categories/5/common_concerns/2/q` | q | string | "살이 찌면 넣은 지방도 커지나요?" | 4333–4351 | 11토큰 | E0302 |
| `/categories/5/common_concerns/2/a` | a | string | "생착된 지방세포는 정상 지방세포처럼 작동하므로 체중 변화에 따라 약간의 볼륨 변화가 있을 수 있습니다." | 4358–4415 | 29토큰 | E0303, E0304, E0305, E0306 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S06-O1 | P | `/categories/5/duration_simple` | 이 키는 다른 카테고리처럼 「N개월 지속」이 아니라 생착률(%)·부위별 비교·노화 경과를 담는다. 같은 키 이름 아래 정보 종류가 다르다 |
| S06-O2 | B | `/categories/5/duration_simple` | 「평균 약 40~50%」의 분모·대상 집단·측정 시점·보고 출처 미기재. 환자 실제 생착률로 바꾸지 않는다 |
| S06-O3 | P | `/categories/5/duration_simple` | 「~」가 이 값에서는 범위 기호로 쓰였다(다른 값은 「-」). 근사 표현 「약」「정도」가 함께 붙음 |
| S06-O4 | P | `/categories/5/how_it_works` | 부위 역할 두 개: 채취(복부·허벅지)와 주입(볼·이마·관자놀이). duration_simple 의 코·이마·볼·턱은 생착률 비교 대상 부위로 how_it_works 목록과 다르다(코·턱은 how_it_works 에 없음, 「등」으로 열림) |
| S06-O5 | P | `/categories/5/common_concerns/0/a` | 「보통 3개월 후 안정화」 기준 시점 생략(시술 후로 보임) |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0259 | `/categories/5/name` | 지방이식 | 0–4 | name |  |
| E0260 | `/categories/5/patient_name` | 내 지방으로 볼륨 채우기 | 0–13 | name,substance,effect |  |
| E0261 | `/categories/5/simple_explanation` | 본인의 지방을 다른 부위에서 채취해서 얼굴에 넣어주는 시술입니다. | 0–36 | sentence,sequence |  |
| E0262 | `/categories/5/simple_explanation` | 다른 부위에서 채취해서 | 8–20 | site,sequence | 채취 부위(역할 다름) |
| E0263 | `/categories/5/simple_explanation` | 얼굴에 넣어주는 | 21–29 | site | 주입 부위 |
| E0264 | `/categories/5/how_it_works` | 복부나 허벅지 같은 부위에서 소량의 지방을 뽑아 정제한 뒤, 얼굴의 꺼진 부위(볼, 이마, 관자놀이 등)에 미세하게 주입합니다. | 0–71 | sentence,site,degree,sequence,manner |  |
| E0265 | `/categories/5/how_it_works` | 복부나 허벅지 같은 부위 | 0–13 | site | 채취 부위 예시 · 「같은」 열린 목록 |
| E0266 | `/categories/5/how_it_works` | 소량의 지방 | 16–22 | degree,substance | 수치 없음 |
| E0267 | `/categories/5/how_it_works` | 정제한 뒤 | 27–32 | sequence |  |
| E0268 | `/categories/5/how_it_works` | 얼굴의 꺼진 부위(볼, 이마, 관자놀이 등) | 34–58 | site,concern,paraphrase | 주입 부위 · 「등」 열린 목록 |
| E0269 | `/categories/5/how_it_works` | 미세하게 주입합니다 | 60–70 | manner,degree |  |
| E0270 | `/categories/5/how_it_works` | 생착된 지방은 오래 유지됩니다. | 72–89 | sentence,condition,course | 「오래」 수치 없음 |
| E0271 | `/categories/5/how_it_works` | 생착된 지방 | 72–78 | condition,substance |  |
| E0272 | `/categories/5/how_it_works` | 오래 유지됩니다 | 80–88 | course | 수치 없음 · 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0273 | `/categories/5/duration_simple` | 생착률은 개인차·부위차가 커서 평균 약 40~50% 정도가 유지되는 것으로 보고됩니다. | 0–48 | sentence,quantity,approx,range,condition,evidence |  |
| E0274 | `/categories/5/duration_simple` | 개인차·부위차가 커서 | 5–16 | condition,degree |  |
| E0275 | `/categories/5/duration_simple` | 평균 약 40~50% 정도 | 17–31 | quantity,approx,range | 「~」는 범위 · 「약」「정도」 근사 중복 · 분모·대상 집단 미기재 |
| E0276 | `/categories/5/duration_simple` | 유지되는 것으로 보고됩니다 | 33–47 | evidence,hedge | 보고 출처 미기재 |
| E0277 | `/categories/5/duration_simple` | 코·이마 등은 상대적으로 낮고 볼·턱은 높은 편이라, 일부 흡수를 고려해 여유 있게 주입합니다. | 49–102 | sentence,site,comparison,degree,rationale |  |
| E0278 | `/categories/5/duration_simple` | 코·이마 등은 상대적으로 낮고 | 49–65 | site,comparison,degree | 생착률 비교 — 수치 없음 |
| E0279 | `/categories/5/duration_simple` | 볼·턱은 높은 편 | 66–75 | site,comparison,degree |  |
| E0280 | `/categories/5/duration_simple` | 일부 흡수를 고려해 여유 있게 주입합니다 | 79–101 | rationale,degree,manner |  |
| E0281 | `/categories/5/duration_simple` | 생착된 조직은 유지되지만 노화에 따른 전반적 볼륨 감소는 계속됩니다. | 103–141 | sentence,course,condition |  |
| E0282 | `/categories/5/duration_simple` | 노화에 따른 전반적 볼륨 감소는 계속됩니다 | 117–140 | cause,course |  |
| E0283 | `/categories/5/duration_simple` | 생착된 조직은 유지되지만 | 103–116 | condition,course,contrast | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0284 | `/categories/5/pain_level` | 국소 마취 하에 시술, 시술 중 통증 거의 없음 | 0–26 | condition,time,sensory,degree,negation |  |
| E0285 | `/categories/5/pain_level` | 국소 마취 하에 | 0–8 | condition |  |
| E0286 | `/categories/5/pain_level` | 시술 중 통증 거의 없음 | 13–26 | time,sensory,degree,negation | 「거의」 근사 부정 |
| E0287 | `/categories/5/downtime` | 붓기와 멍이 1-3주, 사회 활동 복귀까지 약 1주 | 0–28 | adverse,time,range,quantity,approx | 시간 역할 두 개(증상 지속·복귀) |
| E0288 | `/categories/5/downtime` | 붓기와 멍이 1-3주 | 0–11 | adverse,time,range,quantity |  |
| E0289 | `/categories/5/downtime` | 사회 활동 복귀까지 약 1주 | 13–28 | time,approx,quantity |  |
| E0290 | `/categories/5/common_concerns/0/q` | 지방이 다 흡수되지는 않나요? | 0–16 | sentence,negation,scope |  |
| E0291 | `/categories/5/common_concerns/0/a` | 일부 흡수가 일어나므로 의사가 약간 여유 있게 넣습니다. | 0–31 | sentence,rationale,actor,degree |  |
| E0292 | `/categories/5/common_concerns/0/a` | 약간 여유 있게 | 17–25 | degree |  |
| E0293 | `/categories/5/common_concerns/0/a` | 보통 3개월 후 안정화되며, 생착된 지방은 오래 유지돼요. | 32–64 | sentence,frequency,time,quantity,course |  |
| E0294 | `/categories/5/common_concerns/0/a` | 보통 3개월 후 안정화 | 32–44 | frequency,time,quantity,course | 기준 시점 생략 |
| E0295 | `/categories/5/common_concerns/0/a` | 오래 유지돼요 | 56–63 | course | 수치 없음 |
| E0296 | `/categories/5/common_concerns/0/a` | 일부 흡수가 일어나므로 | 0–12 | scope,course,rationale | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0297 | `/categories/5/common_concerns/1/q` | 지방 뽑는 부위가 움푹 꺼지지 않나요? | 0–21 | sentence,site,adverse,negation |  |
| E0298 | `/categories/5/common_concerns/1/a` | 소량만 채취하고 균일하게 뽑기 때문에 눈에 띄는 변화는 없어요. | 0–35 | sentence,degree,scope,manner,rationale,negation |  |
| E0299 | `/categories/5/common_concerns/1/a` | 소량만 | 0–3 | degree,scope |  |
| E0300 | `/categories/5/common_concerns/1/a` | 균일하게 | 9–13 | manner |  |
| E0301 | `/categories/5/common_concerns/1/a` | 눈에 띄는 변화는 없어요 | 21–34 | negation,degree |  |
| E0302 | `/categories/5/common_concerns/2/q` | 살이 찌면 넣은 지방도 커지나요? | 0–18 | sentence,condition |  |
| E0303 | `/categories/5/common_concerns/2/a` | 생착된 지방세포는 정상 지방세포처럼 작동하므로 체중 변화에 따라 약간의 볼륨 변화가 있을 수 있습니다. | 0–57 | sentence,comparison,rationale,condition,degree,possibility |  |
| E0304 | `/categories/5/common_concerns/2/a` | 정상 지방세포처럼 | 10–19 | comparison |  |
| E0305 | `/categories/5/common_concerns/2/a` | 체중 변화에 따라 | 26–35 | condition |  |
| E0306 | `/categories/5/common_concerns/2/a` | 약간의 볼륨 변화가 있을 수 있습니다 | 36–56 | degree,possibility |  |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/5/name`: 지방/NNG 이식/NNG
- `/categories/5/patient_name`: 나/NP 의/JKG 지방/NNG 으로/JKB 볼륨/NNG 채우/VV 기/ETN
- `/categories/5/simple_explanation`: 본인/NNG 의/JKG 지방/NNG 을/JKO 다른/MM 부위/NNG 에서/JKB 채취/NNG 하/XSV 어서/EC 얼굴/NNG 에/JKB 넣/VV 어/EC 주/VX 는/ETM 시술/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/5/how_it_works`: 복부/NNG 나/JC 허벅지/NNG 같/VA 은/ETM 부위/NNG 에서/JKB 소량/NNG 의/JKG 지방/NNG 을/JKO 뽑/VV-R 어/EC 정제/NNG 하/XSV ᆫ/ETM 뒤/NNG ,/SP 얼굴/NNG 의/JKG 꺼지/VV ᆫ/ETM 부위/NNG (/SSO 볼/NNG ,/SP 이마/NNG ,/SP 관자놀이/NNG 등/NNB )/SSC 에/JKB 미세/NNG 하/XSA 게/EC 주입/NNG 하/XSV ᆸ니다/EF ./SF 생착/NNG 되/XSA ᆫ/ETM 지방/NNG 은/JX 오래/MAG 유지/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/5/duration_simple`: 생착률/NNP 은/JX 개인/NNG 차/NNG ·/SP 부위/NNG 차/NNG 가/JKS 크/VA 어서/EC 평균/NNG 약/MM 40/SN ~/SO 50/SN %/SW 정도/NNG 가/JKS 유지/NNG 되/XSV 는/ETM 것/NNB 으로/JKB 보고/NNG 되/XSV ᆸ니다/EF ./SF 코/NNG ·/SP 이마/NNG 등/NNB 은/JX 상대/NNG 적/XSN 으로/JKB 낮/VA 고/EC 볼/NNG ·/SP 턱/NNG 은/JX 높/VA 은/ETM 편/NNB 이/VCP 라/EC ,/SP 일부/NNG 흡수/NNG 를/JKO 고려/NNG 하/XSV 어/EC 여유/NNG 있/VA 게/EC 주입/NNG 하/XSV ᆸ니다/EF ./SF 생착/NNG 되/XSV ᆫ/ETM 조직/NNG 은/JX 유지/NNG 되/XSV 지만/EC 노화/NNG 에/JKB 따르/VV ᆫ/ETM 전반/NNG 적/XSN 볼륨/NNG 감소/NNG 는/JX 계속/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/5/pain_level`: 국소/NNG 마취/NNG 하/NNG 에/JKB 시술/NNG ,/SP 시술/NNG 중/NNB 통증/NNG 거의/MAG 없/VA 음/EF
- `/categories/5/downtime`: 붓/VV-I 기/ETN 와/JC 멍/NNG 이/JKS 1-3/W_SERIAL 주/NNG ,/SP 사회/NNG 활동/NNG 복귀/NNG 까지/JX 약/MM 1/SN 주/NNB
- `/categories/5/common_concerns/0/q`: 지방/NNG 이/JKS 다/MAG 흡수/NNG 되/XSV 지/EC 는/JX 않/VX 나요/EF ?/SF
- `/categories/5/common_concerns/0/a`: 일부/NNG 흡수/NNG 가/JKS 일어나/VV 므로/EC 의사/NNG 가/JKS 약간/MAG 여유/NNG 있/VV 게/EC 넣/VV 습니다/EF ./SF 보통/MAG 3/SN 개월/NNB 후/NNG 안정/NNG 화/XSN 되/XSV 며/EC ,/SP 생착/NNG 되/XSV ᆫ/ETM 지방/NNG 은/JX 오래/MAG 유지/NNG 되/XSV 어요/EF ./SF
- `/categories/5/common_concerns/1/q`: 지방/NNG 뽑/VV-R 는/ETM 부위/NNG 가/JKS 움푹/MAG 꺼지/VV 지/EC 않/VX 나요/EF ?/SF
- `/categories/5/common_concerns/1/a`: 소량/NNG 만/JX 채취/NNG 하/XSA 고/EC 균일/NNG 하/XSA 게/EC 뽑/VV-R 기/ETN 때문/NNB 에/JKB 눈/NNG 에/JKB 띄/VV 는/ETM 변화/NNG 는/JX 없/VA 어요/EF ./SF
- `/categories/5/common_concerns/2/q`: 살/NNG 이/JKS 찌/VV 면/EC 넣/VV 은/ETM 지방/NNG 도/JX 커지/VV 나요/EF ?/SF
- `/categories/5/common_concerns/2/a`: 생착/NNG 되/XSA ᆫ/ETM 지방/NNG 세포/NNG 는/JX 정상/NNG 지방/NNG 세포/NNG 처럼/JKB 작동/NNG 하/XSV 므로/EC 체중/NNG 변화/NNG 에/JKB 따르/VV 어/EC 약간/NNG 의/JKG 볼륨/NNG 변화/NNG 가/JKS 있/VV 을/ETM 수/NNB 있/VA 습니다/EF ./SF
