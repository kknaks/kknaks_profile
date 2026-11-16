# S12 — /categories/11 M12 마이크로니들링(MTS)

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/11/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S12.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/11` | [11] | object | (object, 자식 9) | 8073–8791 |  |  |
| `/categories/11/id` | id | string | "M12" | 8080–8083 | 제외(category_code) |  |
| `/categories/11/name` | name | string | "마이크로니들링(MTS)" | 8093–8105 | 4토큰 | E0528 |
| `/categories/11/patient_name` | patient_name | string | "미세 바늘 피부 관리 (MTS)" | 8123–8140 | 7토큰 | E0529 |
| `/categories/11/simple_explanation` | simple_explanation | string | "아주 가는 바늘로 피부에 미세한 자극을 주어 피부가 스스로 재생하도록 유도하는 시술입니다." | 8164–8214 | 27토큰 | E0530, E0531, E0532 |
| `/categories/11/how_it_works` | how_it_works | string | "미세한 바늘(0.2~2.0mm)이 피부 표면에 작은 구멍을 만들면, 우리 몸이 이를 치유하는 과정에서 콜라겐이 새로 만들어집니다. 동시에 바른 약물의 피부 흡수도 높아집니다." | 8232–8329 | 51토큰 | E0533, E0534, E0535, E0536, E0537, E0538 |
| `/categories/11/duration_simple` | duration_simple | string | "효과가 2-4주 후 나타나며, 3-6개월 지속됩니다. 정기적 시술로 효과가 쌓입니다." | 8350–8397 | 23토큰 | E0539, E0540, E0541, E0542, E0543 |
| `/categories/11/pain_level` | pain_level | string | "마취 크림 도포 후 시술, 약간의 따끔함" | 8413–8435 | 11토큰 | E0544 |
| `/categories/11/downtime` | downtime | string | "붉은기 1-3일, 24시간 후 세안 및 화장 가능" | 8449–8476 | 13토큰 | E0545, E0546, E0547 |
| `/categories/11/common_concerns` | common_concerns | array | (array, 자식 3) | 8496–8790 |  |  |
| `/categories/11/common_concerns/0` | [0] | object | (object, 자식 2) | 8497–8608 |  |  |
| `/categories/11/common_concerns/0/q` | q | string | "홈케어 더마롤러와 병원 시술은 같은 건가요?" | 8503–8527 | 15토큰 | E0548, E0549 |
| `/categories/11/common_concerns/0/a` | a | string | "병원에서는 멸균 환경에서 더 깊은 깊이로 시술하므로 효과가 다릅니다. 홈케어 제품은 0.25mm 이하로 피부 흡수 보조 용도예요." | 8534–8606 | 33토큰 | E0550, E0551, E0552, E0553, E0554 |
| `/categories/11/common_concerns/1` | [1] | object | (object, 자식 2) | 8609–8686 |  |  |
| `/categories/11/common_concerns/1/q` | q | string | "시술 후 피가 나나요?" | 8615–8627 | 7토큰 | E0555 |
| `/categories/11/common_concerns/1/a` | a | string | "깊이에 따라 미세한 출혈이 있을 수 있지만 금방 멈추고, 다음 날이면 거의 보이지 않아요." | 8634–8684 | 28토큰 | E0556, E0557, E0558, E0559, E0560 |
| `/categories/11/common_concerns/2` | [2] | object | (object, 자식 2) | 8687–8789 |  |  |
| `/categories/11/common_concerns/2/q` | q | string | "감염 위험은 없나요?" | 8693–8704 | 6토큰 | E0561 |
| `/categories/11/common_concerns/2/a` | a | string | "병원에서 멸균 장비로 시술하므로 감염 위험은 매우 낮습니다. 시술 후 안내사항(세안 시기, 자극 제품 자제 등)을 잘 지켜주시면 됩니다." | 8711–8787 | 38토큰 | E0562, E0563, E0564, E0565, E0566, E0567, E0568 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S12-O1 | P | `/categories/11/how_it_works` | 「0.2~2.0mm」가 바늘 길이인지 침투 깊이인지 원문은 괄호 수치로만 제시. 단위 대상 확정하지 않음 |
| S12-O2 | P | `/categories/11/common_concerns/0/a` | 홈케어 「0.25mm 이하」와 병원 「더 깊은 깊이」 비교. how_it_works 범위 하한 0.2mm 는 0.25mm 이하와 겹친다 — 원문 내 범위 겹침은 의미 단계 확인(I 로 확정하지 않음, P) |
| S12-O3 | P | `/categories/11/downtime` | 「24시간 후 세안 및 화장 가능」 기준 시점 생략. cc2 a 「세안 시기」 안내와 연결될 수 있음 |
| S12-O4 | B | `/categories/11/how_it_works` | 「바른 약물」 종류 미기재 |
| S12-O5 | B | `/categories/11/common_concerns/2/a` | 「자극 제품」 범위·자제 기간 미기재 |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0528 | `/categories/11/name` | 마이크로니들링(MTS) | 0–12 | name,paraphrase | 약어 괄호 |
| E0529 | `/categories/11/patient_name` | 미세 바늘 피부 관리 (MTS) | 0–17 | name,device,paraphrase |  |
| E0530 | `/categories/11/simple_explanation` | 아주 가는 바늘로 피부에 미세한 자극을 주어 피부가 스스로 재생하도록 유도하는 시술입니다. | 0–50 | sentence,device,degree,mechanism,manner |  |
| E0531 | `/categories/11/simple_explanation` | 아주 가는 바늘 | 0–8 | device,degree |  |
| E0532 | `/categories/11/simple_explanation` | 미세한 자극 | 14–20 | degree |  |
| E0533 | `/categories/11/how_it_works` | 미세한 바늘(0.2~2.0mm)이 피부 표면에 작은 구멍을 만들면, 우리 몸이 이를 치유하는 과정에서 콜라겐이 새로 만들어집니다. | 0–72 | sentence,device,quantity,range,site,condition,mechanism |  |
| E0534 | `/categories/11/how_it_works` | 미세한 바늘(0.2~2.0mm) | 0–17 | device,quantity,range,paraphrase | 괄호 수치 — 바늘 길이로 보이나 원문은 길이/깊이 명시 없음 · 「~」 범위 |
| E0535 | `/categories/11/how_it_works` | 0.2~2.0mm | 7–16 | quantity,range |  |
| E0536 | `/categories/11/how_it_works` | 피부 표면에 작은 구멍 | 19–31 | site,degree |  |
| E0537 | `/categories/11/how_it_works` | 동시에 바른 약물의 피부 흡수도 높아집니다. | 73–97 | sentence,time,substance,effect,degree | 「바른 약물」 이름 미기재 |
| E0538 | `/categories/11/how_it_works` | 바른 약물 | 77–82 | substance,route | 「바른」=바르다(도포) — Kiwi 는 VA(옳다)로 태깅(K) · 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0539 | `/categories/11/duration_simple` | 효과가 2-4주 후 나타나며, 3-6개월 지속됩니다. | 0–29 | sentence,time,range,quantity | 발현·지속 |
| E0540 | `/categories/11/duration_simple` | 정기적 시술로 효과가 쌓입니다. | 30–47 | sentence,frequency,effect | 간격 미기재 |
| E0541 | `/categories/11/duration_simple` | 효과가 2-4주 후 나타나며 | 0–15 | time,range,quantity,effect | 발현 · regex 대조 후 보충(구절 누락 수정) |
| E0542 | `/categories/11/duration_simple` | 3-6개월 지속됩니다 | 17–28 | time,range,quantity | 지속 · regex 대조 후 보충(구절 누락 수정) |
| E0543 | `/categories/11/duration_simple` | 정기적 시술로 효과가 쌓입니다 | 30–46 | frequency,effect,course | 간격 미기재 · regex 대조 후 보충(구절 누락 수정) |
| E0544 | `/categories/11/pain_level` | 마취 크림 도포 후 시술, 약간의 따끔함 | 0–22 | time,substance,degree,sensory |  |
| E0545 | `/categories/11/downtime` | 붉은기 1-3일, 24시간 후 세안 및 화장 가능 | 0–27 | adverse,time,range,quantity,possibility |  |
| E0546 | `/categories/11/downtime` | 붉은기 1-3일 | 0–8 | adverse,time,range,quantity |  |
| E0547 | `/categories/11/downtime` | 24시간 후 세안 및 화장 가능 | 10–27 | time,quantity,possibility,instruction | 기준 시점 생략(시술 후로 보임) · 그 전에는 불가로 읽힘(잠정) |
| E0548 | `/categories/11/common_concerns/0/q` | 홈케어 더마롤러와 병원 시술은 같은 건가요? | 0–24 | sentence,comparison,device,place |  |
| E0549 | `/categories/11/common_concerns/0/q` | 홈케어 더마롤러 | 0–8 | device,place |  |
| E0550 | `/categories/11/common_concerns/0/a` | 병원에서는 멸균 환경에서 더 깊은 깊이로 시술하므로 효과가 다릅니다. | 0–38 | sentence,place,condition,comparison,depth,rationale |  |
| E0551 | `/categories/11/common_concerns/0/a` | 멸균 환경에서 | 6–13 | condition,place |  |
| E0552 | `/categories/11/common_concerns/0/a` | 더 깊은 깊이로 | 14–22 | comparison,depth | 수치 미기재 |
| E0553 | `/categories/11/common_concerns/0/a` | 홈케어 제품은 0.25mm 이하로 피부 흡수 보조 용도예요. | 39–72 | sentence,device,quantity,comparison,effect |  |
| E0554 | `/categories/11/common_concerns/0/a` | 0.25mm 이하 | 47–56 | quantity,comparison | 상한 — how_it_works 범위(0.2~2.0mm)와 겹침 |
| E0555 | `/categories/11/common_concerns/1/q` | 시술 후 피가 나나요? | 0–12 | sentence,time,adverse |  |
| E0556 | `/categories/11/common_concerns/1/a` | 깊이에 따라 미세한 출혈이 있을 수 있지만 금방 멈추고, 다음 날이면 거의 보이지 않아요. | 0–50 | sentence,condition,depth,degree,adverse,possibility,time,course,negation |  |
| E0557 | `/categories/11/common_concerns/1/a` | 깊이에 따라 | 0–6 | condition,depth |  |
| E0558 | `/categories/11/common_concerns/1/a` | 미세한 출혈이 있을 수 있지만 | 7–23 | degree,adverse,possibility |  |
| E0559 | `/categories/11/common_concerns/1/a` | 금방 멈추고 | 24–30 | time,course | 수치 없음 |
| E0560 | `/categories/11/common_concerns/1/a` | 다음 날이면 거의 보이지 않아요 | 32–49 | time,degree,negation,course |  |
| E0561 | `/categories/11/common_concerns/2/q` | 감염 위험은 없나요? | 0–11 | sentence,adverse,negation |  |
| E0562 | `/categories/11/common_concerns/2/a` | 병원에서 멸균 장비로 시술하므로 감염 위험은 매우 낮습니다. | 0–33 | sentence,place,device,rationale,adverse,degree,frequency |  |
| E0563 | `/categories/11/common_concerns/2/a` | 감염 위험은 매우 낮습니다 | 18–32 | adverse,degree,frequency | 수치 없음 |
| E0564 | `/categories/11/common_concerns/2/a` | 시술 후 안내사항(세안 시기, 자극 제품 자제 등)을 잘 지켜주시면 됩니다. | 34–76 | sentence,time,instruction,avoid,paraphrase |  |
| E0565 | `/categories/11/common_concerns/2/a` | 안내사항(세안 시기, 자극 제품 자제 등) | 39–62 | instruction,avoid,time,paraphrase | 「등」 열린 목록 · 세안 시기 수치는 downtime 에 「24시간 후」 |
| E0566 | `/categories/11/common_concerns/2/a` | 자극 제품 자제 | 51–59 | avoid,substance | 제품 범위 미기재 |
| E0567 | `/categories/11/common_concerns/2/a` | 시술 후 안내사항 | 34–43 | time,instruction | regex 대조 후 보충(구절 누락 수정) |
| E0568 | `/categories/11/common_concerns/2/a` | 잘 지켜주시면 됩니다 | 64–75 | instruction | 별도 읽기 검토(형태소 수식어 대조)로 보충 |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/11/name`: 마이크로니들링/NNP (/SSO MTS/SL )/SSC
- `/categories/11/patient_name`: 미세/NNG 바늘/NNG 피부/NNG 관리/NNG (/SSO MTS/SL )/SSC
- `/categories/11/simple_explanation`: 아주/MAG 가늘/VA ᆫ/ETM 바늘/NNG 로/JKB 피부/NNG 에/JKB 미세/NNG 하/XSA ᆫ/ETM 자극/NNG 을/JKO 주/VV 어/EC 피부/NNG 가/JKS 스스로/MAG 재생/NNG 하/XSV 도록/EC 유도/NNG 하/XSV 는/ETM 시술/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/11/how_it_works`: 미세/NNG 하/XSA ᆫ/ETM 바늘/NNG (/SSO 0.2/SN ~/SO 2.0/SN mm/SL )/SSC 이/JKS 피부/NNG 표면/NNG 에/JKB 작/VA 은/ETM 구멍/NNG 을/JKO 만들/VV 면/EC ,/SP 우리/NP 몸/NNG 이/JKS 이/NP 를/JKO 치유/NNG 하/XSV 는/ETM 과정/NNG 에서/JKB 콜라겐/NNP 이/JKS 새로/MAG 만들/VV 어/EC 지/VX ᆸ니다/EF ./SF 동시/NNG 에/JKB 바르/VA ᆫ/ETM 약물/NNG 의/JKG 피부/NNG 흡수/NNG 도/JX 높아지/VV ᆸ니다/EF ./SF
- `/categories/11/duration_simple`: 효과/NNG 가/JKS 2-4/W_SERIAL 주/NNB 후/NNG 나타나/VV 며/EC ,/SP 3-6/W_SERIAL 개월/NNB 지속/NNG 되/XSV ᆸ니다/EF ./SF 정기/NNG 적/XSN 시술/NNG 로/JKB 효과/NNG 가/JKS 쌓이/VV ᆸ니다/EF ./SF
- `/categories/11/pain_level`: 마취/NNG 크림/NNG 도포/NNG 후/NNG 시술/NNG ,/SP 약간/NNG 의/JKG 따끔/MAG 하/XSA ᆷ/EF
- `/categories/11/downtime`: 붉/VA 은/ETM 기/NNG 1-3/W_SERIAL 일/NNB ,/SP 24/SN 시간/NNG 후/NNG 세안/NNG 및/MAG 화장/NNG 가능/NNG
- `/categories/11/common_concerns/0/q`: 홈케어/NNG 더/MAG 마/MAG 롤러/NNG 와/JC 병원/NNG 시술/NNG 은/JX 같/VA 은/ETM 거/NNB 이/VCP ᆫ가/EF 요/JX ?/SF
- `/categories/11/common_concerns/0/a`: 병원/NNG 에서/JKB 는/JX 멸균/NNG 환경/NNG 에서/JKB 더/MAG 깊/VA 은/ETM 깊이/NNG 로/JKB 시술/NNG 하/XSV 므로/EC 효과/NNG 가/JKS 다르/VA ᆸ니다/EF ./SF 홈케어/NNG 제품/NNG 은/JX 0.25/SN mm/SL 이하/NNG 로/JKB 피부/NNG 흡수/NNG 보조/NNG 용도/NNG 이/VCP 예요/EF ./SF
- `/categories/11/common_concerns/1/q`: 시술/NNG 후/NNG 피/NNG 가/JKS 나/VV 나요/EF ?/SF
- `/categories/11/common_concerns/1/a`: 깊이/NNG 에/JKB 따르/VV 어/EC 미세/NNG 하/XSA ᆫ/ETM 출혈/NNG 이/JKS 있/VV 을/ETM 수/NNB 있/VA 지만/EC 금방/MAG 멈추/VV 고/EC ,/SP 다음/NNG 날/NNG 이/VCP 면/EC 거의/MAG 보이/VV 지/EC 않/VX 어요/EF ./SF
- `/categories/11/common_concerns/2/q`: 감염/NNG 위험/NNG 은/JX 없/VA 나요/EF ?/SF
- `/categories/11/common_concerns/2/a`: 병원/NNG 에서/JKB 멸균/NNG 장비/NNG 로/JKB 시술/NNG 하/XSV 므로/EC 감염/NNG 위험/NNG 은/JX 매우/MAG 낮/VA 습니다/EF ./SF 시술/NNG 후/NNG 안내/NNG 사항/NNG (/SSO 세안/NNG 시기/NNG ,/SP 자극/NNG 제품/NNG 자제/NNG 등/NNB )/SSC 을/JKO 잘/MAG 지키/VV 어/EC 주/VX 시/EP 면/EC 되/VV ᆸ니다/EF ./SF

알려진 오분절(출현별, 교정 안 함):

- `/categories/11/common_concerns/0/q` 「더마롤러」 [4,8) → 더/MAG 마/MAG 롤러/NNG — 기구명 「더마롤러」에서 「더」가 비교 부사로 분석 — 비교 표현 오탐·기구명 누락
- `/categories/11/how_it_works` 「바른」 [77,79) → 바르/VA ᆫ/ETM — 「바른 약물」의 바르다(도포·VV)가 형용사 VA(옳다)로 태깅 — lemma 「바르다」는 같으나 품사로 의미가 바뀜. 도포 행위 탐색 누락·「옳은 약물」 오해 위험
