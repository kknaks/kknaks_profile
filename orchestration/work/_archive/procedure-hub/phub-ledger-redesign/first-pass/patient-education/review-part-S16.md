# S16 — /categories/15 M16 수액치료

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/15/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S16.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/15` | [15] | object | (object, 자식 9) | 11173–12026 |  |  |
| `/categories/15/id` | id | string | "M16" | 11180–11183 | 제외(category_code) |  |
| `/categories/15/name` | name | string | "수액치료" | 11193–11197 | 2토큰 | E0707 |
| `/categories/15/patient_name` | patient_name | string | "영양 수액 (비타민 주사)" | 11215–11229 | 6토큰 | E0708 |
| `/categories/15/simple_explanation` | simple_explanation | string | "비타민, 항산화 성분 등을 혈관에 직접 넣어주는 주사입니다." | 11253–11286 | 17토큰 | E0709, E0710, E0711 |
| `/categories/15/how_it_works` | how_it_works | string | "팔 혈관에 수액 줄을 꽂고 글루타치온(항산화), 비타민C, 비타민B 등의 영양 성분을 직접 혈관으로 투여합니다. 정맥 투여는 혈중 농도를 빠르게 높이지만 수용성 비타민은 신장으로 배설되며, 결핍이 없는 경우 경구 섭취보다 추가적인 임상 이득이 있다는 근거는 제한적입니다." | 11304–11455 | 74토큰 | E0712, E0713, E0714, E0715, E0716, E0717, E0718, E0719, E0720, E0721, E0722 |
| `/categories/15/duration_simple` | duration_simple | string | "1-2주 지속, 정기적으로 맞으면 효과가 유지됩니다." | 11476–11505 | 15토큰 | E0723, E0724 |
| `/categories/15/pain_level` | pain_level | string | "일반 주사와 비슷한 찔림, 수액 투여 중 통증 없음" | 11521–11549 | 14토큰 | E0725, E0726 |
| `/categories/15/downtime` | downtime | string | "없음 - 바로 일상 복귀 가능" | 11563–11579 | 7토큰 | E0727 |
| `/categories/15/common_concerns` | common_concerns | array | (array, 자식 3) | 11599–12025 |  |  |
| `/categories/15/common_concerns/0` | [0] | object | (object, 자식 2) | 11600–11770 |  |  |
| `/categories/15/common_concerns/0/q` | q | string | "수액치료로 피부가 하얘지나요?" | 11606–11622 | 10토큰 | E0728 |
| `/categories/15/common_concerns/0/a` | a | string | "정맥 글루타치온의 미백 효과는 아직 임상적으로 충분히 입증되지 않았고 미용 목적 사용은 허가 외입니다. 알레르기·아나필락시스, 드물게 중증 피부반응(SJS/TEN), 고용량 시 간·신장 부담이 발생할 수 있어 의료진과 위험을 충분히 상의해야 합니다." | 11629–11768 | 66토큰 | E0729, E0730, E0731, E0732, E0733, E0734, E0735, E0736, E0737 |
| `/categories/15/common_concerns/1` | [1] | object | (object, 자식 2) | 11771–11871 |  |  |
| `/categories/15/common_concerns/1/q` | q | string | "얼마나 자주 맞아야 하나요?" | 11777–11792 | 7토큰 | E0738 |
| `/categories/15/common_concerns/1/a` | a | string | "목적에 따라 다르지만, 보통 주 1-2회 또는 격주 1회로 시작합니다. 의사와 상담하여 본인에게 맞는 주기를 정하시면 됩니다." | 11799–11869 | 38토큰 | E0739, E0740, E0741, E0742, E0743 |
| `/categories/15/common_concerns/2` | [2] | object | (object, 자식 2) | 11872–12024 |  |  |
| `/categories/15/common_concerns/2/q` | q | string | "영양제를 먹는 것과 뭐가 다른가요?" | 11878–11897 | 12토큰 | E0744 |
| `/categories/15/common_concerns/2/a` | a | string | "정맥 투여는 혈중으로 직접 들어가지만, 결핍이 없는 경우 경구 섭취보다 임상적 이득이 더 크다는 근거는 제한적입니다. 정맥염·감염·수액 과부하·전해질 이상과 성분 알레르기 위험도 있어 의료진의 평가가 필요합니다." | 11904–12022 | 57토큰 | E0745, E0746, E0747, E0748, E0749, E0750, E0751 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S16-O1 | P | `/categories/15/common_concerns/0/a` | 질문(미백)에 근거 부족·허가 외·위험 목록으로 답한다. 「드물게」는 중증 피부반응에, 「고용량 시」는 간·신장 부담에 붙은 것으로 읽힘(잠정) — 알레르기·아나필락시스에는 빈도 수식 없음. 임상적으로 승인하지 않는다 |
| S16-O2 | B | `/categories/15/common_concerns/0/a` | 「고용량」 기준 · 각 위험 빈도 수치 · 아나필락시스 응급 징후·대처 미기재 |
| S16-O3 | P | `/categories/15/how_it_works` | how_it_works 와 cc2 a 가 같은 근거 제한 문장(결핍이 없는 경우 경구 섭취보다 … 근거는 제한적)을 반복 |
| S16-O4 | B | `/categories/15/duration_simple` | 무엇이 1-2주 지속되는지(효과) 생략 · 「정기적」 간격은 cc1 a 에 「주 1-2회 또는 격주 1회」 |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0707 | `/categories/15/name` | 수액치료 | 0–4 | name |  |
| E0708 | `/categories/15/patient_name` | 영양 수액 (비타민 주사) | 0–14 | name,substance,paraphrase |  |
| E0709 | `/categories/15/simple_explanation` | 비타민, 항산화 성분 등을 혈관에 직접 넣어주는 주사입니다. | 0–33 | sentence,substance,site,route,manner |  |
| E0710 | `/categories/15/simple_explanation` | 비타민, 항산화 성분 등 | 0–13 | substance | 「등」 |
| E0711 | `/categories/15/simple_explanation` | 혈관에 직접 | 15–21 | site,route,manner |  |
| E0712 | `/categories/15/how_it_works` | 팔 혈관에 수액 줄을 꽂고 글루타치온(항산화), 비타민C, 비타민B 등의 영양 성분을 직접 혈관으로 투여합니다. | 0–62 | sentence,site,device,substance,paraphrase,route |  |
| E0713 | `/categories/15/how_it_works` | 팔 혈관 | 0–4 | site |  |
| E0714 | `/categories/15/how_it_works` | 글루타치온(항산화) | 15–25 | substance,paraphrase |  |
| E0715 | `/categories/15/how_it_works` | 비타민C | 27–31 | substance |  |
| E0716 | `/categories/15/how_it_works` | 비타민B | 33–37 | substance |  |
| E0717 | `/categories/15/how_it_works` | 정맥 투여는 혈중 농도를 빠르게 높이지만 수용성 비타민은 신장으로 배설되며, 결핍이 없는 경우 경구 섭취보다 추가적인 임상 이득이 있다는 근거는 제한적입니다. | 63–151 | sentence,route,manner,mechanism,condition,comparison,evidence |  |
| E0718 | `/categories/15/how_it_works` | 혈중 농도를 빠르게 높이지만 | 70–85 | manner,mechanism | 속도 수식 |
| E0719 | `/categories/15/how_it_works` | 수용성 비타민은 신장으로 배설되며 | 86–104 | substance,site,mechanism |  |
| E0720 | `/categories/15/how_it_works` | 결핍이 없는 경우 | 106–115 | condition,target,negation |  |
| E0721 | `/categories/15/how_it_works` | 경구 섭취보다 추가적인 임상 이득이 있다는 근거는 제한적입니다 | 116–150 | comparison,evidence,degree | 근거 강도 제한 |
| E0722 | `/categories/15/how_it_works` | 직접 혈관으로 투여합니다 | 48–61 | manner,route,site | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0723 | `/categories/15/duration_simple` | 1-2주 지속, 정기적으로 맞으면 효과가 유지됩니다. | 0–29 | time,range,quantity,frequency,condition,course | 지속 대상 생략 |
| E0724 | `/categories/15/duration_simple` | 정기적으로 맞으면 | 9–18 | frequency,condition |  |
| E0725 | `/categories/15/pain_level` | 일반 주사와 비슷한 찔림, 수액 투여 중 통증 없음 | 0–28 | comparison,sensory,time,negation |  |
| E0726 | `/categories/15/pain_level` | 수액 투여 중 통증 없음 | 15–28 | time,sensory,negation |  |
| E0727 | `/categories/15/downtime` | 없음 - 바로 일상 복귀 가능 | 0–16 | negation,time,possibility |  |
| E0728 | `/categories/15/common_concerns/0/q` | 수액치료로 피부가 하얘지나요? | 0–16 | sentence,effect |  |
| E0729 | `/categories/15/common_concerns/0/a` | 정맥 글루타치온의 미백 효과는 아직 임상적으로 충분히 입증되지 않았고 미용 목적 사용은 허가 외입니다. | 0–57 | sentence,evidence,negation,degree,regulatory |  |
| E0730 | `/categories/15/common_concerns/0/a` | 아직 임상적으로 충분히 입증되지 않았고 | 17–38 | evidence,negation,degree,time |  |
| E0731 | `/categories/15/common_concerns/0/a` | 미용 목적 사용은 허가 외입니다 | 39–56 | regulatory,scope |  |
| E0732 | `/categories/15/common_concerns/0/a` | 알레르기·아나필락시스, 드물게 중증 피부반응(SJS/TEN), 고용량 시 간·신장 부담이 발생할 수 있어 의료진과 위험을 충분히 상의해야 합니다. | 58–139 | sentence,adverse,frequency,condition,site,possibility,instruction,actor |  |
| E0733 | `/categories/15/common_concerns/0/a` | 알레르기·아나필락시스 | 58–69 | adverse,emergency | 아나필락시스 — 응급 사건(징후 기술 없음) |
| E0734 | `/categories/15/common_concerns/0/a` | 드물게 중증 피부반응(SJS/TEN) | 71–91 | frequency,degree,adverse,paraphrase | 「드물게」가 수식하는 범위=중증 피부반응(잠정) |
| E0735 | `/categories/15/common_concerns/0/a` | 고용량 시 간·신장 부담 | 93–106 | condition,degree,site,adverse | 용량 기준 미기재 |
| E0736 | `/categories/15/common_concerns/0/a` | 의료진과 위험을 충분히 상의해야 합니다 | 117–138 | instruction,actor,degree |  |
| E0737 | `/categories/15/common_concerns/0/a` | 발생할 수 있어 | 108–116 | possibility | regex 대조 후 보충(구절 누락 수정) |
| E0738 | `/categories/15/common_concerns/1/q` | 얼마나 자주 맞아야 하나요? | 0–15 | sentence,frequency |  |
| E0739 | `/categories/15/common_concerns/1/a` | 목적에 따라 다르지만, 보통 주 1-2회 또는 격주 1회로 시작합니다. | 0–39 | sentence,condition,frequency,time,range,quantity,alternative |  |
| E0740 | `/categories/15/common_concerns/1/a` | 보통 주 1-2회 또는 격주 1회로 시작합니다 | 13–38 | frequency,time,range,quantity,alternative | 「또는」 두 주기 · 「시작」 — 초기 주기 |
| E0741 | `/categories/15/common_concerns/1/a` | 의사와 상담하여 본인에게 맞는 주기를 정하시면 됩니다. | 40–70 | sentence,actor,instruction,frequency |  |
| E0742 | `/categories/15/common_concerns/1/a` | 목적에 따라 다르지만 | 0–11 | condition | regex 대조 후 보충(구절 누락 수정) |
| E0743 | `/categories/15/common_concerns/1/a` | 의사와 상담하여 본인에게 맞는 주기를 정하시면 됩니다 | 40–69 | actor,instruction,frequency | regex 대조 후 보충(구절 누락 수정) |
| E0744 | `/categories/15/common_concerns/2/q` | 영양제를 먹는 것과 뭐가 다른가요? | 0–19 | sentence,comparison,route |  |
| E0745 | `/categories/15/common_concerns/2/a` | 정맥 투여는 혈중으로 직접 들어가지만, 결핍이 없는 경우 경구 섭취보다 임상적 이득이 더 크다는 근거는 제한적입니다. | 0–65 | sentence,route,condition,comparison,evidence,degree |  |
| E0746 | `/categories/15/common_concerns/2/a` | 결핍이 없는 경우 | 22–31 | condition,target,negation |  |
| E0747 | `/categories/15/common_concerns/2/a` | 정맥염·감염·수액 과부하·전해질 이상과 성분 알레르기 위험도 있어 의료진의 평가가 필요합니다. | 66–118 | sentence,adverse,instruction,actor |  |
| E0748 | `/categories/15/common_concerns/2/a` | 정맥염·감염·수액 과부하·전해질 이상과 성분 알레르기 위험 | 66–98 | adverse | 5개 나열 |
| E0749 | `/categories/15/common_concerns/2/a` | 경구 섭취보다 임상적 이득이 더 크다는 근거는 제한적입니다 | 32–64 | comparison,evidence,degree | regex 대조 후 보충(구절 누락 수정) |
| E0750 | `/categories/15/common_concerns/2/a` | 의료진의 평가가 필요합니다 | 103–117 | actor,instruction | regex 대조 후 보충(구절 누락 수정) |
| E0751 | `/categories/15/common_concerns/2/a` | 혈중으로 직접 들어가지만 | 7–20 | manner,route,contrast | 별도 읽기 검토(형태소 수식어 대조)로 보충 |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/15/name`: 수액/NNG 치료/NNG
- `/categories/15/patient_name`: 영양/NNG 수액/NNG (/SSO 비타민/NNG 주사/NNG )/SSC
- `/categories/15/simple_explanation`: 비타민/NNG ,/SP 항산화/NNG 성분/NNG 등/NNB 을/JKO 혈관/NNG 에/JKB 직접/MAG 넣/VV 어/EC 주/VX 는/ETM 주사/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/15/how_it_works`: 팔/NNG 혈관/NNG 에/JKB 수액/NNG 줄/NNG 을/JKO 꽂/VV 고/EC 글루타치온/NNG (/SSO 항산화/NNG )/SSC ,/SP 비타민/NNG C/SL ,/SP 비타민/NNG B/SL 등/NNB 의/JKG 영양/NNG 성분/NNG 을/JKO 직접/MAG 혈관/NNG 으로/JKB 투여/NNG 하/XSV ᆸ니다/EF ./SF 정맥/NNG 투여/NNG 는/JX 혈/NNG 중/NNB 농도/NNG 를/JKO 빠르/VA 게/EC 높이/VV 지만/EC 수용성/NNG 비타민/NNG 은/JX 신장/NNG 으로/JKB 배설/NNG 되/XSV 며/EC ,/SP 결핍/NNG 이/JKS 없/VA 는/ETM 경우/NNG 경구/NNG 섭취/NNG 보다/JKB 추가/NNG 적/XSN 이/VCP ᆫ/ETM 임상/NNG 이득/NNG 이/JKS 있/VV 다는/ETM 근거/NNG 는/JX 제한/NNG 적/XSN 이/VCP ᆸ니다/EF ./SF
- `/categories/15/duration_simple`: 1-2/W_SERIAL 주/NNB 지속/NNG ,/SP 정기/NNG 적/XSN 으로/JKB 맞/VV 으면/EC 효과/NNG 가/JKS 유지/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/15/pain_level`: 일반/NNG 주사/NNG 와/JKB 비슷하/VA ᆫ/ETM 찔리/VV ᆷ/ETN ,/SP 수액/NNG 투여/NNG 중/NNB 통증/NNG 없/VA 음/EF
- `/categories/15/downtime`: 없/VA 음/EF -/SO 바로/MAG 일상/NNG 복귀/NNG 가능/NNG
- `/categories/15/common_concerns/0/q`: 수액/NNG 치료/NNG 로/JKB 피부/NNG 가/JKS 하얗/VA-I 어/EC 지/VX 나요/EF ?/SF
- `/categories/15/common_concerns/0/a`: 정맥/NNG 글루타치온/NNG 의/JKG 미백/NNG 효과/NNG 는/JX 아직/MAG 임상/NNG 적/XSN 으로/JKB 충분히/MAG 입증/NNG 되/XSV 지/EC 않/VX 었/EP 고/EC 미용/NNG 목적/NNG 사용/NNG 은/JX 허가/NNG 외/NNB 이/VCP ᆸ니다/EF ./SF 알레르기/NNG ·/SP 아나필락시스/NNG ,/SP 드물/VA 게/EC 중증/NNG 피부/NNG 반응/NNG (/SSO SJS/SL //SP TEN/SL )/SSC ,/SP 고/XPN 용량/NNG 시/NNB 간/NNG ·/SP 신장/NNG 부담/NNG 이/JKS 발생/NNG 하/XSV ᆯ/ETM 수/NNB 있/VA 어/EC 의료진/NNG 과/JC 위험/NNG 을/JKO 충분히/MAG 상의/NNG 하/XSV 어야/EC 하/VX ᆸ니다/EF ./SF
- `/categories/15/common_concerns/1/q`: 얼마나/MAG 자주/MAG 맞/VV 어야/EC 하/VX 나요/EF ?/SF
- `/categories/15/common_concerns/1/a`: 목적/NNG 에/JKB 따르/VV 어/EC 다르/VA 지만/EC ,/SP 보통/NNG 주/NNG 1-2/W_SERIAL 회/NNB 또는/MAG 격/NNG 주/NNG 1/SN 회/NNB 로/JKB 시작/NNG 하/XSV ᆸ니다/EF ./SF 의사/NNG 와/JKB 상담/NNG 하/XSV 어/EC 본인/NNG 에게/JKB 맞/VV 는/ETM 주기/NNG 를/JKO 정하/VV 시/EP 면/EC 되/VV ᆸ니다/EF ./SF
- `/categories/15/common_concerns/2/q`: 영양제/NNG 를/JKO 먹/VV 는/ETM 것/NNB 과/JKB 뭐/NP 가/JKS 다르/VA ᆫ가/EF 요/JX ?/SF
- `/categories/15/common_concerns/2/a`: 정맥/NNG 투여/NNG 는/JX 혈중/NNG 으로/JKB 직접/MAG 들어가/VV 지만/EC ,/SP 결핍/NNG 이/JKS 없/VA 는/ETM 경우/NNG 경구/NNG 섭취/NNG 보다/JKB 임상/NNG 적/XSN 이득/NNG 이/JKS 더/MAG 크/VA 다는/ETM 근거/NNG 는/JX 제한/NNG 적/XSN 이/VCP ᆸ니다/EF ./SF 정맥/NNG 염/NNG ·/SP 감염/NNG ·/SP 수액/NNG 과/XPN 부하/NNG ·/SP 전해질/NNG 이상/NNG 과/JKB 성분/NNG 알레르기/NNG 위험/NNG 도/JX 있/VA 어/EC 의료진/NNG 의/JKG 평가/NNG 가/JKS 필요/NNG 하/XSA ᆸ니다/EF ./SF

알려진 오분절(출현별, 교정 안 함):

- `/categories/15/how_it_works` 「혈중」 [70,72) → 혈/NNG 중/NNB — 「혈중」이 「혈」+의존명사 「중」으로 분해 — 「중」이 시간(~하는 중) 표현으로 오탐될 위험. 같은 카테고리 cc2 a 의 「혈중으로」는 정상
- `/categories/15/common_concerns/1/a` 「격주」 [26,28) → 격/NNG 주/NNG — 빈도 표현 「격주」가 「격」+「주」로 분해 — 주기 해석 시 「주」(week) 단독으로 오탐 위험
- `/categories/15/common_concerns/2/a` 「정맥염」 [66,69) → 정맥/NNG 염/NNG — 부작용명 「정맥염」이 「정맥」+「염」으로 분해 — 사건명 토큰 누락·부위 「정맥」 오탐 위험
