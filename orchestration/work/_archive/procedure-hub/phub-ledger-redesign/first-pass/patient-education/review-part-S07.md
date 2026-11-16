# S07 — /categories/6 M7 실리프팅

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/6/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S07.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/6` | [6] | object | (object, 자식 9) | 4420–5076 |  |  |
| `/categories/6/id` | id | string | "M7" | 4427–4429 | 제외(category_code) |  |
| `/categories/6/name` | name | string | "실리프팅" | 4439–4443 | 2토큰 | E0307 |
| `/categories/6/patient_name` | patient_name | string | "실 리프팅 (얼굴 당김 시술)" | 4461–4477 | 8토큰 | E0308 |
| `/categories/6/simple_explanation` | simple_explanation | string | "녹는 실을 피부 아래에 넣어 처진 살을 당겨 올리는 시술입니다." | 4501–4536 | 21토큰 | E0309, E0310, E0311, E0312 |
| `/categories/6/how_it_works` | how_it_works | string | "가는 바늘로 특수한 녹는 실을 피부 아래에 삽입합니다. 실이 처진 조직을 물리적으로 잡아 올려주고, 시간이 지나며 실 주변에 콜라겐이 만들어져 탄력도 개선됩니다." | 4554–4644 | 53토큰 | E0313, E0314, E0315, E0316, E0317, E0318, E0319, E0320 |
| `/categories/6/duration_simple` | duration_simple | string | "실 종류에 따라 6개월-3년 지속됩니다." | 4665–4687 | 14토큰 | E0321, E0322, E0323 |
| `/categories/6/pain_level` | pain_level | string | "국소 마취 후 시술, 삽입 시 당김감" | 4703–4723 | 10토큰 | E0324, E0325, E0326 |
| `/categories/6/downtime` | downtime | string | "붓기 3-5일, 일상생활 2-3일 후 복귀 가능" | 4737–4763 | 11토큰 | E0327, E0328, E0329 |
| `/categories/6/common_concerns` | common_concerns | array | (array, 자식 3) | 4783–5075 |  |  |
| `/categories/6/common_concerns/0` | [0] | object | (object, 자식 2) | 4784–4881 |  |  |
| `/categories/6/common_concerns/0/q` | q | string | "실이 만져지거나 튀어나오나요?" | 4790–4806 | 9토큰 | E0330 |
| `/categories/6/common_concerns/0/a` | a | string | "제대로 시술하면 만져지지 않아요. 극히 드물게 실 끝이 느껴질 수 있는데, 이때는 병원에서 간단히 조치할 수 있습니다." | 4813–4879 | 38토큰 | E0331, E0332, E0333, E0334, E0335, E0336, E0337 |
| `/categories/6/common_concerns/1` | [1] | object | (object, 자식 2) | 4882–4982 |  |  |
| `/categories/6/common_concerns/1/q` | q | string | "실이 녹으면 다시 처지나요?" | 4888–4903 | 8토큰 | E0338 |
| `/categories/6/common_concerns/1/a` | a | string | "실이 녹는 동안 주변에 콜라겐이 만들어지므로 즉시 원래로 돌아가지는 않아요. 다만 시간이 지나면 자연스러운 노화는 진행됩니다." | 4910–4980 | 36토큰 | E0339, E0340, E0341, E0342, E0343, E0344 |
| `/categories/6/common_concerns/2` | [2] | object | (object, 자식 2) | 4983–5074 |  |  |
| `/categories/6/common_concerns/2/q` | q | string | "실리프팅 후 표정이 어색하지 않나요?" | 4989–5009 | 11토큰 | E0345 |
| `/categories/6/common_concerns/2/a` | a | string | "시술 직후에는 약간 당기는 느낌이 있지만, 1-2주면 자연스러워집니다. 일상 표정에는 영향이 없어요." | 5016–5072 | 31토큰 | E0346, E0347, E0348, E0349, E0350 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S07-O1 | B | `/categories/6/simple_explanation` | 「녹는 실」의 재질·종류 미기재(duration_simple 은 「실 종류에 따라」만) |
| S07-O2 | B | `/categories/6/duration_simple` | 실 종류별 지속 값 미기재 |
| S07-O3 | B | `/categories/6/common_concerns/0/a` | 「제대로」의 기준, 「간단히 조치」의 내용 미기재 |
| S07-O4 | P | `/categories/6/common_concerns/2/a` | 시간 역할: 당김감 소실(1-2주). downtime 의 붓기 3-5일·복귀 2-3일 후와 다른 역할 |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0307 | `/categories/6/name` | 실리프팅 | 0–4 | name |  |
| E0308 | `/categories/6/patient_name` | 실 리프팅 (얼굴 당김 시술) | 0–16 | name,paraphrase,site | name 과 띄어쓰기 다름 |
| E0309 | `/categories/6/simple_explanation` | 녹는 실을 피부 아래에 넣어 처진 살을 당겨 올리는 시술입니다. | 0–35 | sentence |  |
| E0310 | `/categories/6/simple_explanation` | 녹는 실 | 0–4 | device,course | 재질 이름 미기재 |
| E0311 | `/categories/6/simple_explanation` | 피부 아래에 | 6–12 | site,depth |  |
| E0312 | `/categories/6/simple_explanation` | 처진 살을 당겨 올리는 | 16–28 | concern,effect |  |
| E0313 | `/categories/6/how_it_works` | 가는 바늘로 특수한 녹는 실을 피부 아래에 삽입합니다. | 0–30 | sentence,device,degree,site |  |
| E0314 | `/categories/6/how_it_works` | 가는 바늘 | 0–5 | device,degree |  |
| E0315 | `/categories/6/how_it_works` | 특수한 녹는 실 | 7–15 | device | 재질 미기재 |
| E0316 | `/categories/6/how_it_works` | 실이 처진 조직을 물리적으로 잡아 올려주고, 시간이 지나며 실 주변에 콜라겐이 만들어져 탄력도 개선됩니다. | 31–90 | sentence,mechanism,time,effect |  |
| E0317 | `/categories/6/how_it_works` | 물리적으로 잡아 올려주고 | 41–54 | manner,mechanism |  |
| E0318 | `/categories/6/how_it_works` | 시간이 지나며 | 56–63 | time | 수치 없음 |
| E0319 | `/categories/6/how_it_works` | 실 주변에 콜라겐이 만들어져 | 64–79 | site,mechanism,substance |  |
| E0320 | `/categories/6/how_it_works` | 탄력도 개선됩니다 | 80–89 | effect |  |
| E0321 | `/categories/6/duration_simple` | 실 종류에 따라 6개월-3년 지속됩니다. | 0–22 | sentence,condition,time,range,quantity | 단위가 다른 범위(개월-년) |
| E0322 | `/categories/6/duration_simple` | 실 종류에 따라 | 0–8 | condition | 종류별 값 미기재 |
| E0323 | `/categories/6/duration_simple` | 6개월-3년 | 9–15 | range,quantity |  |
| E0324 | `/categories/6/pain_level` | 국소 마취 후 시술, 삽입 시 당김감 | 0–20 | time,condition,sensory |  |
| E0325 | `/categories/6/pain_level` | 국소 마취 후 | 0–7 | time,condition |  |
| E0326 | `/categories/6/pain_level` | 삽입 시 당김감 | 12–20 | time,sensory |  |
| E0327 | `/categories/6/downtime` | 붓기 3-5일, 일상생활 2-3일 후 복귀 가능 | 0–26 | adverse,time,range,quantity,possibility | 시간 역할 두 개 |
| E0328 | `/categories/6/downtime` | 붓기 3-5일 | 0–7 | adverse,time,range,quantity |  |
| E0329 | `/categories/6/downtime` | 일상생활 2-3일 후 복귀 가능 | 9–26 | time,range,quantity,possibility |  |
| E0330 | `/categories/6/common_concerns/0/q` | 실이 만져지거나 튀어나오나요? | 0–16 | sentence,adverse |  |
| E0331 | `/categories/6/common_concerns/0/a` | 제대로 시술하면 만져지지 않아요. | 0–18 | sentence,condition,negation |  |
| E0332 | `/categories/6/common_concerns/0/a` | 제대로 시술하면 | 0–8 | condition,actor | 기준 미기재 |
| E0333 | `/categories/6/common_concerns/0/a` | 극히 드물게 실 끝이 느껴질 수 있는데, 이때는 병원에서 간단히 조치할 수 있습니다. | 19–66 | sentence,frequency,adverse,possibility,management |  |
| E0334 | `/categories/6/common_concerns/0/a` | 극히 드물게 | 19–25 | frequency,degree | 수치 없음 |
| E0335 | `/categories/6/common_concerns/0/a` | 실 끝이 느껴질 수 있는데 | 26–40 | adverse,possibility |  |
| E0336 | `/categories/6/common_concerns/0/a` | 병원에서 간단히 조치할 수 있습니다 | 46–65 | actor,degree,management,possibility | 조치 내용 미기재 |
| E0337 | `/categories/6/common_concerns/0/a` | 이때는 | 42–45 | reference,condition | 앞 절(실 끝이 느껴질 때) 참조 · 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0338 | `/categories/6/common_concerns/1/q` | 실이 녹으면 다시 처지나요? | 0–15 | sentence,condition,course |  |
| E0339 | `/categories/6/common_concerns/1/a` | 실이 녹는 동안 주변에 콜라겐이 만들어지므로 즉시 원래로 돌아가지는 않아요. | 0–42 | sentence,time,rationale,negation |  |
| E0340 | `/categories/6/common_concerns/1/a` | 실이 녹는 동안 | 0–8 | time |  |
| E0341 | `/categories/6/common_concerns/1/a` | 즉시 원래로 돌아가지는 않아요 | 25–41 | time,negation,course |  |
| E0342 | `/categories/6/common_concerns/1/a` | 다만 시간이 지나면 자연스러운 노화는 진행됩니다. | 43–70 | sentence,time,condition,course |  |
| E0343 | `/categories/6/common_concerns/1/a` | 시간이 지나면 자연스러운 노화는 진행됩니다 | 46–69 | time,condition,course | regex 대조 후 보충(구절 누락 수정) |
| E0344 | `/categories/6/common_concerns/1/a` | 다만 | 43–45 | contrast | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0345 | `/categories/6/common_concerns/2/q` | 실리프팅 후 표정이 어색하지 않나요? | 0–20 | sentence,time,adverse,negation |  |
| E0346 | `/categories/6/common_concerns/2/a` | 시술 직후에는 약간 당기는 느낌이 있지만, 1-2주면 자연스러워집니다. | 0–39 | sentence,time,degree,sensory,range,quantity,course |  |
| E0347 | `/categories/6/common_concerns/2/a` | 시술 직후에는 | 0–7 | time |  |
| E0348 | `/categories/6/common_concerns/2/a` | 약간 당기는 느낌 | 8–17 | degree,sensory |  |
| E0349 | `/categories/6/common_concerns/2/a` | 1-2주면 자연스러워집니다 | 24–38 | time,range,quantity,course | 소실 시점 |
| E0350 | `/categories/6/common_concerns/2/a` | 일상 표정에는 영향이 없어요. | 40–56 | sentence,negation,scope |  |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/6/name`: 실/NNG 리프팅/NNG
- `/categories/6/patient_name`: 실/NNG 리프팅/NNG (/SSO 얼굴/NNG 당기/VV ᆷ/ETN 시술/NNG )/SSC
- `/categories/6/simple_explanation`: 녹/VV 는/ETM 실/NNG 을/JKO 피부/NNG 아래/NNG 에/JKB 넣/VV 어/EC 처지/VV ᆫ/ETM 살/NNG 을/JKO 당기/VV 어/EC 올리/VV 는/ETM 시술/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/6/how_it_works`: 가늘/VA ᆫ/ETM 바늘/NNG 로/JKB 특수/NNG 하/XSA ᆫ/ETM 녹/VV 는/ETM 실/NNG 을/JKO 피부/NNG 아래/NNG 에/JKB 삽입/NNG 하/XSV ᆸ니다/EF ./SF 실/NNG 이/JKS 처지/VV ᆫ/ETM 조직/NNG 을/JKO 물리/NNG 적/XSN 으로/JKB 잡/VV-R 어/EC 올리/VV 어/EC 주/VX 고/EC ,/SP 시간/NNG 이/JKS 지나/VV 며/EC 실/NNG 주변/NNG 에/JKB 콜라겐/NNP 이/JKS 만들/VV 어/EC 지/VX 어/EC 탄력/NNG 도/JX 개선/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/6/duration_simple`: 실/NNG 종류/NNG 에/JKB 따르/VV 어/EC 6/SN 개월/NNB -/SO 3/SN 년/NNB 지속/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/6/pain_level`: 국소/NNG 마취/NNG 후/NNG 시술/NNG ,/SP 삽입/NNG 시/NNB 당기/VV ᆷ/ETN 감/NNG
- `/categories/6/downtime`: 붓/VV-I 기/ETN 3-5/W_SERIAL 일/NNG ,/SP 일상생활/NNG 2-3/W_SERIAL 일/NNB 후/NNG 복귀/NNG 가능/NNG
- `/categories/6/common_concerns/0/q`: 실/NNG 이/JKS 만지/VV 어/EC 지/VX 거나/EC 튀어나오/VV 나요/EF ?/SF
- `/categories/6/common_concerns/0/a`: 제대로/MAG 시술/NNG 하/XSV 면/EC 만지/VV 어/EC 지/VX 지/EC 않/VX 어요/EF ./SF 극히/MAG 드물/VA 게/EC 실/NNG 끝/NNG 이/JKS 느끼/VV 어/EC 지/VX ᆯ/ETM 수/NNB 있/VV 는데/EC ,/SP 이/MM 때/NNG 는/JX 병원/NNG 에서/JKB 간단히/MAG 조치/NNG 하/XSV ᆯ/ETM 수/NNB 있/VA 습니다/EF ./SF
- `/categories/6/common_concerns/1/q`: 실/NNG 이/JKS 녹/VV 으면/EC 다시/MAG 처지/VV 나요/EF ?/SF
- `/categories/6/common_concerns/1/a`: 실/NNG 이/JKS 녹/VV 는/ETM 동안/NNG 주변/NNG 에/JKB 콜라겐/NNP 이/JKS 만들/VV 어/EC 지/VX 므로/EC 즉시/MAG 원래/NNG 로/JKB 돌아가/VV 지/EC 는/JX 않/VX 어요/EF ./SF 다만/MAG 시간/NNG 이/JKS 지나/VV 면/EC 자연/NNG 스럽/XSA-I 은/ETM 노화/NNG 는/JX 진행/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/6/common_concerns/2/q`: 실/NNG 리프팅/NNG 후/NNG 표정/NNG 이/JKS 어색/XR 하/XSA 지/EC 않/VX 나요/EF ?/SF
- `/categories/6/common_concerns/2/a`: 시술/NNG 직후/NNG 에/JKB 는/JX 약간/MAG 당기/VV 는/ETM 느낌/NNG 이/JKS 있/VA 지만/EC ,/SP 1-2/W_SERIAL 주/NNB 이/VCP 면/EC 자연/NNG 스럽/XSA-I 어/EC 지/VX ᆸ니다/EF ./SF 일상/NNG 표정/NNG 에/JKB 는/JX 영향/NNG 이/JKS 없/VA 어요/EF ./SF
