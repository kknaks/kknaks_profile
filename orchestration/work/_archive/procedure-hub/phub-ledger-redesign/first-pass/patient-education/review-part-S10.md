# S10 — /categories/9 M10 HIFES/EMS

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/9/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S10.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/9` | [9] | object | (object, 자식 9) | 6619–7347 |  |  |
| `/categories/9/id` | id | string | "M10" | 6626–6629 | 제외(category_code) |  |
| `/categories/9/name` | name | string | "HIFES/EMS" | 6639–6648 | 3토큰 | E0450 |
| `/categories/9/patient_name` | patient_name | string | "얼굴 근육 운동 기기 (엠페이스 등)" | 6666–6686 | 8토큰 | E0451, E0452 |
| `/categories/9/simple_explanation` | simple_explanation | string | "전기 자극으로 얼굴 근육을 운동시켜 탄력을 높이는 시술입니다." | 6710–6744 | 17토큰 | E0453, E0454 |
| `/categories/9/how_it_works` | how_it_works | string | "기기가 얼굴 근육에 전기 자극을 보내 근육을 수축시킵니다. 동시에 고주파 에너지로 피부 콜라겐 재생도 유도합니다. 얼굴 근육이 탄탄해지면서 자연스러운 리프팅 효과가 나타납니다." | 6762–6860 | 47토큰 | E0455, E0456, E0457, E0458 |
| `/categories/9/duration_simple` | duration_simple | string | "약 3-6개월 지속, 정기적 시술로 유지합니다." | 6881–6907 | 13토큰 | E0459, E0460 |
| `/categories/9/pain_level` | pain_level | string | "전기 자극에 의한 근육 떨림 느낌, 통증은 거의 없음" | 6923–6952 | 15토큰 | E0461, E0462 |
| `/categories/9/downtime` | downtime | string | "없음 - 바로 일상 복귀 가능" | 6966–6982 | 7토큰 | E0463 |
| `/categories/9/common_concerns` | common_concerns | array | (array, 자식 3) | 7002–7346 |  |  |
| `/categories/9/common_concerns/0` | [0] | object | (object, 자식 2) | 7003–7145 |  |  |
| `/categories/9/common_concerns/0/q` | q | string | "전기 자극이 위험하지 않나요?" | 7009–7025 | 9토큰 | E0464 |
| `/categories/9/common_concerns/0/a` | a | string | "심장 박동기·제세동기 등 몸에 이식된 전자기기가 있거나 임신 중이신 분, 치료 부위에 활동성 감염이 있는 분은 시술 대상이 아닙니다. 치료 부위에 금속 임플란트가 있는 분도 반드시 사전에 알려주세요." | 7032–7143 | 58토큰 | E0465, E0466, E0467, E0468, E0469, E0470, E0471, E0472 |
| `/categories/9/common_concerns/1` | [1] | object | (object, 자식 2) | 7146–7239 |  |  |
| `/categories/9/common_concerns/1/q` | q | string | "효과가 바로 느껴지나요?" | 7152–7165 | 8토큰 | E0473 |
| `/categories/9/common_concerns/1/a` | a | string | "1-2주 후부터 서서히 느껴지며, 4주 후에 확실한 변화를 느끼시는 분이 많아요. 보통 4회 정도 코스로 시술합니다." | 7172–7237 | 37토큰 | E0474, E0475, E0476, E0477, E0478, E0479 |
| `/categories/9/common_concerns/2` | [2] | object | (object, 자식 2) | 7240–7345 |  |  |
| `/categories/9/common_concerns/2/q` | q | string | "얼굴 운동을 직접 해도 같은 효과인가요?" | 7246–7268 | 12토큰 | E0480 |
| `/categories/9/common_concerns/2/a` | a | string | "일반적인 얼굴 운동으로는 깊은 표정근까지 자극하기 어렵습니다. 기기는 특정 근육에 정확하게 강한 수축을 유도할 수 있어요." | 7275–7343 | 37토큰 | E0481, E0482, E0483, E0484, E0485, E0486 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S10-O1 | P | `/categories/9/common_concerns/0/a` | 질문(전기 자극 위험)에 금기 대상 목록으로 답한다. 대상 3종은 「시술 대상이 아닙니다」 단정, 금속 임플란트는 「알려주세요」 알림 지시로 강도가 다르다. 임상적으로 승인하지 않는다 |
| S10-O2 | B | `/categories/9/common_concerns/1/a` | 효과 체감 시점의 기준(첫 시술/코스) 미기재 · 「분이 많아요」 비율 없음 · 코스 간격 미기재 |
| S10-O3 | B | `/categories/9/name` | HIFES·EMS 약어 풀이 없음 |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0450 | `/categories/9/name` | HIFES/EMS | 0–9 | name,alternative | 「/」 두 약어 — 관계 미확정 · 풀이 없음 |
| E0451 | `/categories/9/patient_name` | 얼굴 근육 운동 기기 (엠페이스 등) | 0–20 | name,site,device,paraphrase | 괄호 안 제품명 · 「등」 |
| E0452 | `/categories/9/patient_name` | 엠페이스 | 13–17 | name |  |
| E0453 | `/categories/9/simple_explanation` | 전기 자극으로 얼굴 근육을 운동시켜 탄력을 높이는 시술입니다. | 0–34 | sentence,device_param,site,effect |  |
| E0454 | `/categories/9/simple_explanation` | 얼굴 근육 | 8–13 | site |  |
| E0455 | `/categories/9/how_it_works` | 기기가 얼굴 근육에 전기 자극을 보내 근육을 수축시킵니다. | 0–32 | sentence,device_param,site,mechanism |  |
| E0456 | `/categories/9/how_it_works` | 동시에 고주파 에너지로 피부 콜라겐 재생도 유도합니다. | 33–63 | sentence,time,device_param,mechanism | 「동시에」 — 두 에너지 병행 |
| E0457 | `/categories/9/how_it_works` | 얼굴 근육이 탄탄해지면서 자연스러운 리프팅 효과가 나타납니다. | 64–98 | sentence,effect,manner |  |
| E0458 | `/categories/9/how_it_works` | 자연스러운 리프팅 효과 | 78–90 | manner,effect | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0459 | `/categories/9/duration_simple` | 약 3-6개월 지속, 정기적 시술로 유지합니다. | 0–26 | time,approx,range,quantity,frequency |  |
| E0460 | `/categories/9/duration_simple` | 정기적 시술로 유지합니다 | 12–25 | frequency,management | 간격 미기재 |
| E0461 | `/categories/9/pain_level` | 전기 자극에 의한 근육 떨림 느낌, 통증은 거의 없음 | 0–29 | cause,sensory,degree,negation |  |
| E0462 | `/categories/9/pain_level` | 통증은 거의 없음 | 20–29 | sensory,degree,negation |  |
| E0463 | `/categories/9/downtime` | 없음 - 바로 일상 복귀 가능 | 0–16 | negation,time,possibility |  |
| E0464 | `/categories/9/common_concerns/0/q` | 전기 자극이 위험하지 않나요? | 0–16 | sentence,adverse,negation |  |
| E0465 | `/categories/9/common_concerns/0/a` | 심장 박동기·제세동기 등 몸에 이식된 전자기기가 있거나 임신 중이신 분, 치료 부위에 활동성 감염이 있는 분은 시술 대상이 아닙니다. | 0–74 | sentence,target,condition,contraindication,negation |  |
| E0466 | `/categories/9/common_concerns/0/a` | 심장 박동기·제세동기 등 몸에 이식된 전자기기가 있거나 | 0–30 | target,condition,device | 「등」 열린 목록 |
| E0467 | `/categories/9/common_concerns/0/a` | 임신 중이신 분 | 31–39 | target,condition,time |  |
| E0468 | `/categories/9/common_concerns/0/a` | 치료 부위에 활동성 감염이 있는 분 | 41–60 | target,condition,site |  |
| E0469 | `/categories/9/common_concerns/0/a` | 시술 대상이 아닙니다 | 62–73 | contraindication,negation | 단정 표현(가능성 아님) |
| E0470 | `/categories/9/common_concerns/0/a` | 치료 부위에 금속 임플란트가 있는 분도 반드시 사전에 알려주세요. | 75–111 | sentence,target,condition,site,instruction,time |  |
| E0471 | `/categories/9/common_concerns/0/a` | 금속 임플란트가 있는 분도 | 82–96 | target,condition | 「도」 — 대상 아님인지 알림 대상인지 원문은 알림만 지시 |
| E0472 | `/categories/9/common_concerns/0/a` | 반드시 사전에 알려주세요 | 97–110 | instruction,time |  |
| E0473 | `/categories/9/common_concerns/1/q` | 효과가 바로 느껴지나요? | 0–13 | sentence,time,effect |  |
| E0474 | `/categories/9/common_concerns/1/a` | 1-2주 후부터 서서히 느껴지며, 4주 후에 확실한 변화를 느끼시는 분이 많아요. | 0–45 | sentence,time,range,quantity,manner,frequency |  |
| E0475 | `/categories/9/common_concerns/1/a` | 1-2주 후부터 서서히 | 0–12 | time,range,quantity,manner | 기준 시점 생략(첫 시술 후/코스 시작 후 불명) |
| E0476 | `/categories/9/common_concerns/1/a` | 4주 후에 확실한 변화 | 19–31 | time,quantity,degree |  |
| E0477 | `/categories/9/common_concerns/1/a` | 느끼시는 분이 많아요 | 33–44 | frequency,target | 비율 수치 없음 |
| E0478 | `/categories/9/common_concerns/1/a` | 보통 4회 정도 코스로 시술합니다. | 46–65 | sentence,frequency,quantity,approx | 간격 미기재 |
| E0479 | `/categories/9/common_concerns/1/a` | 보통 4회 정도 코스로 | 46–58 | frequency,quantity,approx | 간격 미기재 · regex 대조 후 보충(구절 누락 수정) |
| E0480 | `/categories/9/common_concerns/2/q` | 얼굴 운동을 직접 해도 같은 효과인가요? | 0–22 | sentence,comparison |  |
| E0481 | `/categories/9/common_concerns/2/a` | 일반적인 얼굴 운동으로는 깊은 표정근까지 자극하기 어렵습니다. | 0–34 | sentence,comparison,depth,site,possibility,negation |  |
| E0482 | `/categories/9/common_concerns/2/a` | 깊은 표정근까지 | 14–22 | depth,site |  |
| E0483 | `/categories/9/common_concerns/2/a` | 자극하기 어렵습니다 | 23–33 | possibility,negation |  |
| E0484 | `/categories/9/common_concerns/2/a` | 기기는 특정 근육에 정확하게 강한 수축을 유도할 수 있어요. | 35–68 | sentence,site,manner,degree,possibility |  |
| E0485 | `/categories/9/common_concerns/2/a` | 정확하게 강한 수축 | 46–56 | manner,degree |  |
| E0486 | `/categories/9/common_concerns/2/a` | 유도할 수 있어요 | 58–67 | possibility | regex 대조 후 보충(구절 누락 수정) |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/9/name`: HIFES/SL //SP EMS/SL
- `/categories/9/patient_name`: 얼굴/NNG 근육/NNG 운동/NNG 기기/NNG (/SSO 엠페이스/NNG 등/NNB )/SSC
- `/categories/9/simple_explanation`: 전기/NNG 자극/NNG 으로/JKB 얼굴/NNG 근육/NNG 을/JKO 운동/NNG 시키/XSV 어/EC 탄력/NNG 을/JKO 높이/VV 는/ETM 시술/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/9/how_it_works`: 기기/NNG 가/JKS 얼굴/NNG 근육/NNG 에/JKB 전기/NNG 자극/NNG 을/JKO 보내/VV 어/EC 근육/NNG 을/JKO 수축/NNG 시키/XSV ᆸ니다/EF ./SF 동시/NNG 에/JKB 고/XPN 주파/NNG 에너지/NNG 로/JKB 피부/NNG 콜라겐/NNP 재생/NNG 도/JX 유도/NNG 하/XSV ᆸ니다/EF ./SF 얼굴/NNG 근육/NNG 이/JKS 탄탄/XR 하/XSA 어/EC 지/VX 면서/EC 자연/NNG 스럽/XSA-I 은/ETM 리프팅/NNG 효과/NNG 가/JKS 나타나/VV ᆸ니다/EF ./SF
- `/categories/9/duration_simple`: 약/MM 3-6/W_SERIAL 개월/NNB 지속/NNG ,/SP 정기/NNG 적/XSN 시술/NNG 로/JKB 유지/NNG 하/XSV ᆸ니다/EF ./SF
- `/categories/9/pain_level`: 전기/NNG 자극/NNG 에/JKB 의하/VV ᆫ/ETM 근육/NNG 떨리/VV ᆷ/ETN 느낌/NNG ,/SP 통증/NNG 은/JX 거의/MAG 없/VA 음/EF
- `/categories/9/downtime`: 없/VA 음/EF -/SO 바로/MAG 일상/NNG 복귀/NNG 가능/NNG
- `/categories/9/common_concerns/0/q`: 전기/NNG 자극/NNG 이/JKS 위험/NNG 하/XSA 지/EC 않/VX 나요/EF ?/SF
- `/categories/9/common_concerns/0/a`: 심장/NNG 박동/NNG 기/XSN ·/SP 제세동기/NNG 등/NNB 몸/NNG 에/JKB 이식/NNG 되/XSV ᆫ/ETM 전자/NNG 기기/NNG 가/JKS 있/VV 거나/EC 임신/NNG 중/NNB 이/VCP 시/EP ᆫ/ETM 분/NNB ,/SP 치료/NNG 부위/NNG 에/JKB 활동/NNG 성/XSN 감염/NNG 이/JKS 있/VA 는/ETM 분/NNB 은/JX 시술/NNG 대상/NNG 이/JKC 아니/VCN ᆸ니다/EF ./SF 치료/NNG 부위/NNG 에/JKB 금속/NNG 임플란트/NNG 가/JKS 있/VV 는/ETM 분/NNB 도/JX 반드시/MAG 사전/NNG 에/JKB 알리/VV 어/EC 주/VX 세요/EF ./SF
- `/categories/9/common_concerns/1/q`: 효과/NNG 가/JKS 바로/MAG 느끼/VV 어/EC 지/VX 나요/EF ?/SF
- `/categories/9/common_concerns/1/a`: 1-2/W_SERIAL 주/NNB 후/NNG 부터/JX 서서히/MAG 느끼/VV 어/EC 지/VX 며/EC ,/SP 4/SN 주/NNB 후/NNG 에/JKB 확실/XR 하/XSA ᆫ/ETM 변화/NNG 를/JKO 느끼/VV 시/EP 는/ETM 분/NNB 이/JKS 많/VA 어요/EF ./SF 보통/MAG 4/SN 회/NNB 정도/NNG 코스/NNG 로/JKB 시술/NNG 하/XSV ᆸ니다/EF ./SF
- `/categories/9/common_concerns/2/q`: 얼굴/NNG 운동/NNG 을/JKO 직접/MAG 하/VV 어도/EC 같/VA 은/ETM 효과/NNG 이/VCP ᆫ가요/EF ?/SF
- `/categories/9/common_concerns/2/a`: 일반/NNG 적/XSN 이/VCP ᆫ/ETM 얼굴/NNG 운동/NNG 으로/JKB 는/JX 깊/VA 은/ETM 표정근/NNG 까지/JX 자극/NNG 하/XSV 기/ETN 어렵/VA-I 습니다/EF ./SF 기기/NNG 는/JX 특정/NNG 근육/NNG 에/JKB 정확/NNG 하/XSA 게/EC 강하/VA ᆫ/ETM 수축/NNG 을/JKO 유도/NNG 하/XSV ᆯ/ETM 수/NNB 있/VA 어요/EF ./SF

알려진 오분절(출현별, 교정 안 함):

- `/categories/9/how_it_works` 「고주파」 [37,40) → 고/XPN 주파/NNG — 「고주파」가 접두사+명사로 분해 — 「고」가 정도(높음) 접두로 읽힐 위험·에너지 종류 토큰 누락
- `/categories/9/common_concerns/0/a` 「박동기」 [3,6) → 박동/NNG 기/XSN — 기기명 「심장 박동기」의 「기」가 접미사 처리 — 경미(기기명 토큰 분해)
