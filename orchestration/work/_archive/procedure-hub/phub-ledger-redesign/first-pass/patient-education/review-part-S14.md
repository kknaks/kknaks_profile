# S14 — /categories/13 M14 크라이오리포라이시스

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/13/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S14.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/13` | [13] | object | (object, 자식 9) | 9551–10389 |  |  |
| `/categories/13/id` | id | string | "M14" | 9558–9561 | 제외(category_code) |  |
| `/categories/13/name` | name | string | "크라이오리포라이시스" | 9571–9581 | 1토큰 | E0611 |
| `/categories/13/patient_name` | patient_name | string | "냉각 지방분해 (쿨스컬프팅 등)" | 9599–9616 | 7토큰 | E0612, E0613 |
| `/categories/13/simple_explanation` | simple_explanation | string | "차가운 온도로 지방세포를 선택적으로 없애는 비수술 지방 감소 시술입니다." | 9640–9680 | 20토큰 | E0614, E0615, E0616, E0617 |
| `/categories/13/how_it_works` | how_it_works | string | "시술 부위에 냉각 장치를 대면, 지방세포가 다른 세포보다 낮은 온도에 취약한 성질을 이용해 지방세포만 선택적으로 파괴합니다. 파괴된 지방세포는 수 주에 걸쳐 몸 밖으로 자연 배출됩니다." | 9698–9801 | 56토큰 | E0618, E0619, E0620, E0621, E0622 |
| `/categories/13/duration_simple` | duration_simple | string | "3개월 후 최대 효과, 파괴된 지방세포는 재생되지 않아 반영구적입니다." | 9822–9861 | 22토큰 | E0623, E0624, E0625 |
| `/categories/13/pain_level` | pain_level | string | "냉각 시작 시 차가움과 당김감, 수 분 후 감각이 둔해져 편안해짐" | 9877–9913 | 24토큰 | E0626, E0627, E0628 |
| `/categories/13/downtime` | downtime | string | "시술 부위 일시적 붉은기, 저림감, 가벼운 멍 가능. 일상생활 바로 가능" | 9927–9967 | 20토큰 | E0629, E0630, E0631, E0632, E0633 |
| `/categories/13/common_concerns` | common_concerns | array | (array, 자식 3) | 9987–10388 |  |  |
| `/categories/13/common_concerns/0` | [0] | object | (object, 자식 2) | 9988–10117 |  |  |
| `/categories/13/common_concerns/0/q` | q | string | "다이어트와 뭐가 다른가요?" | 9994–10008 | 8토큰 | E0634 |
| `/categories/13/common_concerns/0/a` | a | string | "다이어트는 지방세포 크기를 줄이는 것이고, 이 시술은 지방세포 수 자체를 줄입니다. 따라서 요요 가능성이 낮아요. 다만 전체 체중 감량 목적이 아니라 국소 지방 감소에 적합합니다." | 10015–10115 | 48토큰 | E0635, E0636, E0637, E0638, E0639, E0640, E0641 |
| `/categories/13/common_concerns/1` | [1] | object | (object, 자식 2) | 10118–10206 |  |  |
| `/categories/13/common_concerns/1/q` | q | string | "한 번에 얼마나 빠지나요?" | 10124–10138 | 7토큰 | E0642 |
| `/categories/13/common_concerns/1/a` | a | string | "1회 시술로 해당 부위 지방의 약 20-25%가 감소합니다. 눈에 띄는 변화는 보통 3개월 후에 나타나요." | 10145–10204 | 30토큰 | E0643, E0644, E0645, E0646, E0647 |
| `/categories/13/common_concerns/2` | [2] | object | (object, 자식 2) | 10207–10387 |  |  |
| `/categories/13/common_concerns/2/q` | q | string | "PAH(역설적 지방 비대)가 뭔가요?" | 10213–10233 | 12토큰 | E0648, E0649 |
| `/categories/13/common_concerns/2/a` | a | string | "드물지만 시술 부위 지방이 오히려 딱딱하게 커지는 현상입니다(보고 발생률 약 0.2~0.5%). 실제로는 과소보고 가능성이 있어 이보다 높을 수 있고 남성에서 더 흔합니다. 한번 발생하면 자연 소실되지 않고 지방흡입·절제 등 수술적 제거가 필요할 수 있습니다." | 10240–10385 | 76토큰 | E0650, E0651, E0652, E0653, E0654, E0655, E0656, E0657, E0658, E0659, E0660, E0661 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S14-O1 | P | `/categories/13/common_concerns/2/a` | 빈도 표현 3층: 「드물지만」(어휘)·「보고 발생률 약 0.2~0.5%」(보고 수치)·「과소보고 가능성 … 이보다 높을 수 있고」(수치 한정). 보고 수치를 환자 실제 발생률로 바꾸지 않는다 |
| S14-O2 | B | `/categories/13/common_concerns/2/a` | 보고 발생률의 분모·출처·기간 미기재 · 「남성에서 더 흔합니다」 비교 수치 없음 |
| S14-O3 | B | `/categories/13/common_concerns/1/a` | 「약 20-25%」 측정 방법·출처 미기재 |
| S14-O4 | P | `/categories/13/duration_simple` | 이 키는 지속 기간이 아니라 최대 효과 시점(3개월 후)과 「반영구적」 성질을 담는다 |
| S14-O5 | P | `/categories/13/downtime` | 값 안에 마침표로 두 문장 — 이 키에서 문장 종결형이 있는 값 |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0611 | `/categories/13/name` | 크라이오리포라이시스 | 0–10 | name | 음역 전문어 |
| E0612 | `/categories/13/patient_name` | 냉각 지방분해 (쿨스컬프팅 등) | 0–17 | name,mechanism,paraphrase | 괄호 제품명 · 「등」 |
| E0613 | `/categories/13/patient_name` | 쿨스컬프팅 | 9–14 | name |  |
| E0614 | `/categories/13/simple_explanation` | 차가운 온도로 지방세포를 선택적으로 없애는 비수술 지방 감소 시술입니다. | 0–40 | sentence,device_param,manner,mechanism,negation,effect |  |
| E0615 | `/categories/13/simple_explanation` | 차가운 온도 | 0–6 | device_param,degree | 온도 수치 미기재 |
| E0616 | `/categories/13/simple_explanation` | 선택적으로 | 14–19 | manner,scope |  |
| E0617 | `/categories/13/simple_explanation` | 비수술 지방 감소 시술 | 24–36 | negation,effect,name |  |
| E0618 | `/categories/13/how_it_works` | 시술 부위에 냉각 장치를 대면, 지방세포가 다른 세포보다 낮은 온도에 취약한 성질을 이용해 지방세포만 선택적으로 파괴합니다. | 0–69 | sentence,site,device,condition,comparison,mechanism,scope |  |
| E0619 | `/categories/13/how_it_works` | 지방세포가 다른 세포보다 낮은 온도에 취약한 성질 | 18–45 | comparison,degree,mechanism |  |
| E0620 | `/categories/13/how_it_works` | 지방세포만 선택적으로 파괴합니다 | 51–68 | scope,manner,mechanism |  |
| E0621 | `/categories/13/how_it_works` | 파괴된 지방세포는 수 주에 걸쳐 몸 밖으로 자연 배출됩니다. | 70–103 | sentence,time,approx,course,mechanism |  |
| E0622 | `/categories/13/how_it_works` | 수 주에 걸쳐 | 80–87 | time,approx | 수치 불명확 |
| E0623 | `/categories/13/duration_simple` | 3개월 후 최대 효과, 파괴된 지방세포는 재생되지 않아 반영구적입니다. | 0–39 | time,quantity,degree,negation,course,rationale |  |
| E0624 | `/categories/13/duration_simple` | 3개월 후 최대 효과 | 0–11 | time,quantity,degree,effect | 시간 역할=최대 효과 시점 |
| E0625 | `/categories/13/duration_simple` | 재생되지 않아 반영구적 | 23–35 | negation,course | 「반영구적」 — 지속 기간 수치 아님 |
| E0626 | `/categories/13/pain_level` | 냉각 시작 시 차가움과 당김감, 수 분 후 감각이 둔해져 편안해짐 | 0–36 | time,sensory,approx,course |  |
| E0627 | `/categories/13/pain_level` | 냉각 시작 시 | 0–7 | time |  |
| E0628 | `/categories/13/pain_level` | 수 분 후 감각이 둔해져 편안해짐 | 18–36 | time,approx,sensory,course |  |
| E0629 | `/categories/13/downtime` | 시술 부위 일시적 붉은기, 저림감, 가벼운 멍 가능. | 0–29 | site,course,adverse,sensory,degree,possibility |  |
| E0630 | `/categories/13/downtime` | 일시적 붉은기 | 6–13 | course,adverse |  |
| E0631 | `/categories/13/downtime` | 저림감 | 15–18 | adverse,sensory |  |
| E0632 | `/categories/13/downtime` | 가벼운 멍 가능 | 20–28 | degree,adverse,possibility |  |
| E0633 | `/categories/13/downtime` | 일상생활 바로 가능 | 30–40 | time,possibility |  |
| E0634 | `/categories/13/common_concerns/0/q` | 다이어트와 뭐가 다른가요? | 0–14 | sentence,comparison |  |
| E0635 | `/categories/13/common_concerns/0/a` | 다이어트는 지방세포 크기를 줄이는 것이고, 이 시술은 지방세포 수 자체를 줄입니다. | 0–46 | sentence,comparison,mechanism |  |
| E0636 | `/categories/13/common_concerns/0/a` | 따라서 요요 가능성이 낮아요. | 47–63 | sentence,rationale,possibility,degree |  |
| E0637 | `/categories/13/common_concerns/0/a` | 다만 전체 체중 감량 목적이 아니라 국소 지방 감소에 적합합니다. | 64–100 | sentence,negation,scope,effect |  |
| E0638 | `/categories/13/common_concerns/0/a` | 전체 체중 감량 목적이 아니라 | 67–83 | negation,scope |  |
| E0639 | `/categories/13/common_concerns/0/a` | 국소 지방 감소에 적합합니다 | 84–99 | scope,effect |  |
| E0640 | `/categories/13/common_concerns/0/a` | 요요 가능성이 낮아요 | 51–62 | possibility,degree,course | regex 대조 후 보충(구절 누락 수정) |
| E0641 | `/categories/13/common_concerns/0/a` | 다만 | 64–66 | contrast | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0642 | `/categories/13/common_concerns/1/q` | 한 번에 얼마나 빠지나요? | 0–14 | sentence,quantity,frequency |  |
| E0643 | `/categories/13/common_concerns/1/a` | 1회 시술로 해당 부위 지방의 약 20-25%가 감소합니다. | 0–33 | sentence,quantity,frequency,site,approx,range,effect |  |
| E0644 | `/categories/13/common_concerns/1/a` | 1회 시술로 | 0–6 | quantity,frequency |  |
| E0645 | `/categories/13/common_concerns/1/a` | 해당 부위 지방의 약 20-25% | 7–25 | site,approx,range,quantity | 분모=해당 부위 지방 · 측정 방법·출처 미기재 |
| E0646 | `/categories/13/common_concerns/1/a` | 눈에 띄는 변화는 보통 3개월 후에 나타나요. | 34–59 | sentence,degree,frequency,time,quantity,effect |  |
| E0647 | `/categories/13/common_concerns/1/a` | 보통 3개월 후에 나타나요 | 44–58 | frequency,time,quantity,effect | 기준 시점 생략 · regex 대조 후 보충(구절 누락 수정) |
| E0648 | `/categories/13/common_concerns/2/q` | PAH(역설적 지방 비대)가 뭔가요? | 0–20 | sentence,adverse,paraphrase |  |
| E0649 | `/categories/13/common_concerns/2/q` | PAH(역설적 지방 비대) | 0–14 | adverse,paraphrase | 약어 괄호 풀이 |
| E0650 | `/categories/13/common_concerns/2/a` | 드물지만 시술 부위 지방이 오히려 딱딱하게 커지는 현상입니다(보고 발생률 약 0.2~0.5%). | 0–53 | sentence,frequency,site,comparison,degree,adverse,quantity,approx,range,evidence |  |
| E0651 | `/categories/13/common_concerns/2/a` | 드물지만 | 0–4 | frequency |  |
| E0652 | `/categories/13/common_concerns/2/a` | 오히려 딱딱하게 커지는 | 15–27 | comparison,degree,adverse |  |
| E0653 | `/categories/13/common_concerns/2/a` | (보고 발생률 약 0.2~0.5%) | 33–52 | evidence,quantity,approx,range,frequency | 「보고」 발생률 — 분모·출처 미기재 |
| E0654 | `/categories/13/common_concerns/2/a` | 실제로는 과소보고 가능성이 있어 이보다 높을 수 있고 남성에서 더 흔합니다. | 54–96 | sentence,evidence,possibility,comparison,target,frequency |  |
| E0655 | `/categories/13/common_concerns/2/a` | 과소보고 가능성이 있어 이보다 높을 수 있고 | 59–83 | evidence,possibility,comparison |  |
| E0656 | `/categories/13/common_concerns/2/a` | 남성에서 더 흔합니다 | 84–95 | target,comparison,frequency | 대상 집단 비교 — 수치 없음 |
| E0657 | `/categories/13/common_concerns/2/a` | 한번 발생하면 자연 소실되지 않고 지방흡입·절제 등 수술적 제거가 필요할 수 있습니다. | 97–145 | sentence,condition,negation,course,management,possibility |  |
| E0658 | `/categories/13/common_concerns/2/a` | 자연 소실되지 않고 | 105–115 | negation,course |  |
| E0659 | `/categories/13/common_concerns/2/a` | 지방흡입·절제 등 수술적 제거가 필요할 수 있습니다 | 116–144 | management,name,possibility | 「등」 열린 목록 |
| E0660 | `/categories/13/common_concerns/2/a` | 한번 발생하면 | 97–104 | condition,frequency | regex 대조 후 보충(구절 누락 수정) |
| E0661 | `/categories/13/common_concerns/2/a` | 실제로는 | 54–58 | evidence,contrast | 보고 수치와 실제의 대비 · 별도 읽기 검토(형태소 수식어 대조)로 보충 |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/13/name`: 크라이오리포라이시스/NNG
- `/categories/13/patient_name`: 냉각/NNG 지방/NNG 분해/NNG (/SSO 쿨스컬프팅/NNG 등/NNB )/SSC
- `/categories/13/simple_explanation`: 차갑/VA-I 은/ETM 온도/NNG 로/JKB 지방/NNG 세포/NNG 를/JKO 선택/NNG 적/XSN 으로/JKB 없애/VV 는/ETM 비/XPN 수술/NNG 지방/NNG 감소/NNG 시술/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/13/how_it_works`: 시술/NNG 부위/NNG 에/JKB 냉각/NNG 장치/NNG 를/JKO 대/VV 면/EC ,/SP 지방/NNG 세포/NNG 가/JKS 다른/MM 세포/NNG 보다/JKB 낮/VA 은/ETM 온도/NNG 에/JKB 취약/NNG 하/XSA ᆫ/ETM 성질/NNG 을/JKO 이용/NNG 하/XSV 어/EC 지방/NNG 세포/NNG 만/JX 선택/NNG 적/XSN 으로/JKB 파괴/NNG 하/XSV ᆸ니다/EF ./SF 파괴/NNG 되/XSV ᆫ/ETM 지방/NNG 세포/NNG 는/JX 수/MM 주/NNB 에/JKB 걸치/VV 어/EC 몸/NNG 밖/NNG 으로/JKB 자연/NNG 배출/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/13/duration_simple`: 3/SN 개월/NNB 후/NNG 최대/NNG 효과/NNG ,/SP 파괴/NNG 되/XSV ᆫ/ETM 지방/NNG 세포/NNG 는/JX 재생/NNG 되/XSV 지/EC 않/VX 어/EC 반영구/NNG 적/XSN 이/VCP ᆸ니다/EF ./SF
- `/categories/13/pain_level`: 냉각/NNG 시작/NNG 시/NNB 차갑/VA-I 음/ETN 과/JC 당기/VV ᆷ/ETN 감/NNG ,/SP 수/MM 분/NNB 후/NNG 감각/NNG 이/JKS 둔하/VA 어/EC 지/VX 어/EC 편안/NNG 하/XSA 어/EC 지/VX ᆷ/EF
- `/categories/13/downtime`: 시술/NNG 부위/NNG 일시/NNG 적/XSN 붉/VA 은/ETM 기/NNG ,/SP 저리/VA ᆷ/ETN 감/XSN ,/SP 가볍/VA-I 은/ETM 멍/NNG 가능/NNG ./SF 일상생활/NNG 바로/MAG 가능/NNG
- `/categories/13/common_concerns/0/q`: 다이어트/NNG 와/JKB 뭐/NP 가/JKS 다르/VA ᆫ가/EF 요/JX ?/SF
- `/categories/13/common_concerns/0/a`: 다이어트/NNG 는/JX 지방/NNG 세포/NNG 크기/NNG 를/JKO 줄이/VV 는/ETM 것/NNB 이/VCP 고/EC ,/SP 이/MM 시술/NNG 은/JX 지방/NNG 세포/NNG 수/NNG 자체/NNG 를/JKO 줄이/VV ᆸ니다/EF ./SF 따라서/MAJ 요/MM 요/MM 가능/NNG 성/XSN 이/JKS 낮/VA 어요/EF ./SF 다만/MAG 전체/NNG 체중/NNG 감량/NNG 목적/NNG 이/JKC 아니/VCN 라/EC 국소/NNG 지방/NNG 감소/NNG 에/JKB 적합/NNG 하/XSA ᆸ니다/EF ./SF
- `/categories/13/common_concerns/1/q`: 한/MM 번/NNB 에/JKB 얼마나/MAG 빠지/VV 나요/EF ?/SF
- `/categories/13/common_concerns/1/a`: 1/SN 회/NNB 시술/NNG 로/JKB 해당/NNG 부위/NNG 지방/NNG 의/JKG 약/MM 20-25/W_SERIAL %/SW 가/JKS 감소/NNG 하/XSV ᆸ니다/EF ./SF 눈/NNG 에/JKB 띄/VV 는/ETM 변화/NNG 는/JX 보통/MAG 3/SN 개월/NNB 후/NNG 에/JKB 나타나/VV 어요/EF ./SF
- `/categories/13/common_concerns/2/q`: PAH/SL (/SSO 역설/NNG 적/XSN 지방/NNG 비대/NNG )/SSC 가/JKS 뭐/NP 이/VCP ᆫ가요/EF ?/SF
- `/categories/13/common_concerns/2/a`: 드물/VA 지만/EC 시술/NNG 부위/NNG 지방/NNG 이/JKS 오히려/MAG 딱딱/XR 하/XSA 게/EC 커지/VV 는/ETM 현상/NNG 이/VCP ᆸ니다/EF (/SSO 보/VV 고/EC 발생/NNG 률/XSN 약/MM 0.2/SN ~/SO 0.5/SN %/SW )/SSC ./SF 실제로/MAG 는/JX 과소/NNG 보고/NNG 가능/NNG 성/XSN 이/JKS 있/VA 어/EC 이/NP 보다/JKB 높/VA 을/ETM 수/NNB 있/VA 고/EC 남성/NNG 에서/JKB 더/MAG 흔하/VA ᆸ니다/EF ./SF 한/MM 번/NNB 발생/NNG 하/XSV 면/EC 자연/MAG 소실/NNG 되/XSV 지/EC 않/VX 고/EC 지방/NNG 흡입/NNG ·/SP 절제/NNG 등/NNB 수술/NNG 적/XSN 제거/NNG 가/JKS 필요/NNG 하/XSA ᆯ/ETM 수/NNB 있/VA 습니다/EF ./SF

알려진 오분절(출현별, 교정 안 함):

- `/categories/13/common_concerns/0/a` 「요요」 [51,53) → 요/MM 요/MM — 「요요」(체중 재증가)가 관형사 두 개로 분석 — 명사 소실
