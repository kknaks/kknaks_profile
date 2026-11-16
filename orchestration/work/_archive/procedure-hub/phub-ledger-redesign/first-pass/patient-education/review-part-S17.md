# S17 — /categories/16 M17 줄기세포치료

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/16/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S17.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/16` | [16] | object | (object, 자식 9) | 12027–13041 |  |  |
| `/categories/16/id` | id | string | "M17" | 12034–12037 | 제외(category_code) |  |
| `/categories/16/name` | name | string | "줄기세포치료" | 12047–12053 | 2토큰 | E0752 |
| `/categories/16/patient_name` | patient_name | string | "줄기세포 피부 재생" | 12071–12081 | 3토큰 | E0753 |
| `/categories/16/simple_explanation` | simple_explanation | string | "줄기세포에서 추출한 재생 성분을 이용하여 피부를 재생하는 시술입니다." | 12105–12143 | 21토큰 | E0754, E0755 |
| `/categories/16/how_it_works` | how_it_works | string | "줄기세포의 배양액(세포가 만들어낸 재생 성분)을 피부에 도포하거나 주사합니다. 이 성분 속의 성장인자들이 피부 세포 재생을 촉진하고, 콜라겐 합성을 도와 피부를 젊고 건강하게 만듭니다." | 12161–12264 | 55토큰 | E0756, E0757, E0758, E0759, E0760, E0761 |
| `/categories/16/duration_simple` | duration_simple | string | "효과 발현 2-4주, 약 3-6개월 지속됩니다." | 12285–12311 | 12토큰 | E0762, E0763, E0764 |
| `/categories/16/pain_level` | pain_level | string | "도포 시 통증 없음, 주사 시 마취 크림 사용 후 가벼운 따끔함" | 12327–12362 | 17토큰 | E0765, E0766, E0767 |
| `/categories/16/downtime` | downtime | string | "가벼운 붉은기 1-2일, 일상생활 가능" | 12376–12397 | 10토큰 | E0768 |
| `/categories/16/common_concerns` | common_concerns | array | (array, 자식 3) | 12417–13040 |  |  |
| `/categories/16/common_concerns/0` | [0] | object | (object, 자식 2) | 12418–12525 |  |  |
| `/categories/16/common_concerns/0/q` | q | string | "줄기세포를 직접 넣는 건가요?" | 12424–12440 | 10토큰 | E0769 |
| `/categories/16/common_concerns/0/a` | a | string | "아닙니다. 줄기세포 자체가 아니라 줄기세포가 만들어낸 성장인자와 재생 성분(배양액)을 사용합니다. 세포 자체를 주입하는 것과는 다릅니다." | 12447–12523 | 39토큰 | E0770, E0771, E0772, E0773 |
| `/categories/16/common_concerns/1` | [1] | object | (object, 자식 2) | 12526–12685 |  |  |
| `/categories/16/common_concerns/1/q` | q | string | "안전한 시술인가요?" | 12532–12542 | 7토큰 | E0774 |
| `/categories/16/common_concerns/1/a` | a | string | "국내에 주사용으로 허가된 줄기세포 배양액/엑소좀 의약품은 없으며, 배양액은 화장품(도포)용 원료로만 허용됩니다. 주사 사용은 허가된 적응증이 아니며, 미허가 주사는 알레르기·감염 등 예측하기 어려운 위험이 있어 안전성을 단정할 수 없습니다." | 12549–12683 | 69토큰 | E0775, E0776, E0777, E0778, E0779, E0780, E0781, E0782, E0783, E0784, E0785 |
| `/categories/16/common_concerns/2` | [2] | object | (object, 자식 2) | 12686–13039 |  |  |
| `/categories/16/common_concerns/2/q` | q | string | "다른 시술과 함께 받을 수 있나요?" | 12692–12711 | 10토큰 | E0786, E0787 |
| `/categories/16/common_concerns/2/a` | a | string | "MTS(미세침)나 레이저 시술 후 미세 통로를 통한 흡수를 높이려는 목적으로 함께 사용하는 경우가 있습니다. 다만 이렇게 피부 장벽이 열린 상태에서 배양액·엑소좀을 도포하면 사실상 진피 안으로 전달되므로, 앞서 안내드린 미허가 주사와 비슷한 감염·염증(육아종·결절) 위험이 생길 수 있습니다. 실제로 미허가·오염된 제품을 시술 통로로 넣은 뒤 결절·육아종 등이 보고된 사례가 있어, 반드시 무균적으로 관리되고 검증된 제품을 사용해야 합니다. 병용의 미용 효과에 대한 임상 근거는 아직 제한적이므로, 병용 여부는 위험과 이득을 의사와 충분히 상담한 뒤 결정하시기 바랍니다." | 12718–13037 | 164토큰 | E0788, E0789, E0790, E0791, E0792, E0793, E0794, E0795, E0796, E0797, E0798, E0799, E0800, E0801, E0802, E0803, E0804, E0805, E0806 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S17-O1 | P | `/categories/16/common_concerns/1/a` | 규제 서술(국내·허가·적응증)이 들어 있다. 시점·출처 미기재 — 현재 유효성은 외부 확인 대상이며 여기서 승인·보충하지 않는다(B) |
| S17-O2 | P | `/categories/16/common_concerns/2/a` | 조합 질문에 「함께 사용하는 경우가 있습니다」(현황) + 위험 + 「의사와 상담」으로 답한다. 동시 가능·보완 효과·순서를 단정하지 않는다. 선후 표현 「MTS(미세침)나 레이저 시술 후」는 조합의 시점 |
| S17-O3 | F | `/categories/16/common_concerns/2/a` | 「MTS(미세침)」「레이저」는 S12(M12)·S08(M8) 참조로 보이며 「앞서 안내드린 미허가 주사」는 같은 카테고리 cc1 a 참조. 연결은 후속 |
| S17-O4 | B | `/categories/16/common_concerns/2/a` | 「보고된 사례」 출처·빈도 미기재 · 「검증된 제품」 기준 미기재 |
| S17-O5 | P | `/categories/16/how_it_works` | how_it_works 는 「도포하거나 주사합니다」로 주사를 일반 방법으로 기술하나, cc1 a 는 주사 사용이 허가 적응증이 아니라고 기술 — 같은 카테고리 안 서술 긴장(I 후보). 임상·규제 판단은 하지 않는다 |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0752 | `/categories/16/name` | 줄기세포치료 | 0–6 | name |  |
| E0753 | `/categories/16/patient_name` | 줄기세포 피부 재생 | 0–10 | name,site,effect |  |
| E0754 | `/categories/16/simple_explanation` | 줄기세포에서 추출한 재생 성분을 이용하여 피부를 재생하는 시술입니다. | 0–38 | sentence,substance,effect |  |
| E0755 | `/categories/16/simple_explanation` | 줄기세포에서 추출한 재생 성분 | 0–16 | substance |  |
| E0756 | `/categories/16/how_it_works` | 줄기세포의 배양액(세포가 만들어낸 재생 성분)을 피부에 도포하거나 주사합니다. | 0–43 | sentence,substance,paraphrase,route,alternative |  |
| E0757 | `/categories/16/how_it_works` | 줄기세포의 배양액(세포가 만들어낸 재생 성분) | 0–25 | substance,paraphrase |  |
| E0758 | `/categories/16/how_it_works` | 도포하거나 주사합니다 | 31–42 | route,alternative | 두 투여 경로 |
| E0759 | `/categories/16/how_it_works` | 이 성분 속의 성장인자들이 피부 세포 재생을 촉진하고, 콜라겐 합성을 도와 피부를 젊고 건강하게 만듭니다. | 44–103 | sentence,substance,mechanism,effect |  |
| E0760 | `/categories/16/how_it_works` | 성장인자들 | 52–57 | substance |  |
| E0761 | `/categories/16/how_it_works` | 피부를 젊고 건강하게 만듭니다 | 86–102 | effect |  |
| E0762 | `/categories/16/duration_simple` | 효과 발현 2-4주, 약 3-6개월 지속됩니다. | 0–26 | sentence,time,range,quantity,approx | 발현·지속 |
| E0763 | `/categories/16/duration_simple` | 효과 발현 2-4주 | 0–10 | time,range,quantity | 발현 · regex 대조 후 보충(구절 누락 수정) |
| E0764 | `/categories/16/duration_simple` | 약 3-6개월 지속됩니다 | 12–25 | time,approx,range,quantity | 지속 · regex 대조 후 보충(구절 누락 수정) |
| E0765 | `/categories/16/pain_level` | 도포 시 통증 없음, 주사 시 마취 크림 사용 후 가벼운 따끔함 | 0–35 | time,route,condition,sensory,negation,substance,degree | 경로별 통증 |
| E0766 | `/categories/16/pain_level` | 도포 시 통증 없음 | 0–10 | time,route,sensory,negation |  |
| E0767 | `/categories/16/pain_level` | 주사 시 마취 크림 사용 후 가벼운 따끔함 | 12–35 | time,route,substance,degree,sensory |  |
| E0768 | `/categories/16/downtime` | 가벼운 붉은기 1-2일, 일상생활 가능 | 0–21 | degree,adverse,time,range,quantity,possibility |  |
| E0769 | `/categories/16/common_concerns/0/q` | 줄기세포를 직접 넣는 건가요? | 0–16 | sentence,substance,route |  |
| E0770 | `/categories/16/common_concerns/0/a` | 아닙니다. | 0–5 | negation |  |
| E0771 | `/categories/16/common_concerns/0/a` | 줄기세포 자체가 아니라 줄기세포가 만들어낸 성장인자와 재생 성분(배양액)을 사용합니다. | 6–54 | sentence,negation,substance,paraphrase |  |
| E0772 | `/categories/16/common_concerns/0/a` | 세포 자체를 주입하는 것과는 다릅니다. | 55–76 | sentence,comparison,negation |  |
| E0773 | `/categories/16/common_concerns/0/a` | 줄기세포 자체가 아니라 | 6–18 | negation,scope | regex 대조 후 보충(구절 누락 수정) |
| E0774 | `/categories/16/common_concerns/1/q` | 안전한 시술인가요? | 0–10 | sentence,adverse |  |
| E0775 | `/categories/16/common_concerns/1/a` | 국내에 주사용으로 허가된 줄기세포 배양액/엑소좀 의약품은 없으며, 배양액은 화장품(도포)용 원료로만 허용됩니다. | 0–62 | sentence,regulatory,place,route,negation,scope,substance |  |
| E0776 | `/categories/16/common_concerns/1/a` | 국내에 | 0–3 | place,scope | 관할 범위 |
| E0777 | `/categories/16/common_concerns/1/a` | 줄기세포 배양액/엑소좀 의약품 | 14–30 | substance,alternative | 「/」 나열 |
| E0778 | `/categories/16/common_concerns/1/a` | 엑소좀 | 23–26 | substance |  |
| E0779 | `/categories/16/common_concerns/1/a` | 화장품(도포)용 원료로만 허용됩니다 | 42–61 | regulatory,scope,route,paraphrase |  |
| E0780 | `/categories/16/common_concerns/1/a` | 주사 사용은 허가된 적응증이 아니며, 미허가 주사는 알레르기·감염 등 예측하기 어려운 위험이 있어 안전성을 단정할 수 없습니다. | 63–134 | sentence,regulatory,negation,adverse,possibility |  |
| E0781 | `/categories/16/common_concerns/1/a` | 주사 사용은 허가된 적응증이 아니며 | 63–82 | regulatory,negation,route |  |
| E0782 | `/categories/16/common_concerns/1/a` | 알레르기·감염 등 예측하기 어려운 위험 | 92–113 | adverse,possibility | 「등」 |
| E0783 | `/categories/16/common_concerns/1/a` | 안전성을 단정할 수 없습니다 | 118–133 | negation,evidence |  |
| E0784 | `/categories/16/common_concerns/1/a` | 의약품은 없으며 | 27–35 | negation,regulatory | regex 대조 후 보충(구절 누락 수정) |
| E0785 | `/categories/16/common_concerns/1/a` | 미허가 주사는 | 84–91 | regulatory,negation,route | regex 대조 후 보충(구절 누락 수정) |
| E0786 | `/categories/16/common_concerns/2/q` | 다른 시술과 함께 받을 수 있나요? | 0–19 | sentence,combination,possibility |  |
| E0787 | `/categories/16/common_concerns/2/q` | 함께 받을 수 있나요 | 7–18 | combination,possibility | regex 대조 후 보충(구절 누락 수정) |
| E0788 | `/categories/16/common_concerns/2/a` | MTS(미세침)나 레이저 시술 후 미세 통로를 통한 흡수를 높이려는 목적으로 함께 사용하는 경우가 있습니다. | 0–60 | sentence,reference,name,paraphrase,time,sequence,combination,mechanism,scope |  |
| E0789 | `/categories/16/common_concerns/2/a` | MTS(미세침)나 레이저 시술 후 | 0–18 | reference,name,paraphrase,time,sequence | 다른 카테고리(M12·M8) 참조로 보임 · 선후(시술 후) |
| E0790 | `/categories/16/common_concerns/2/a` | 함께 사용하는 경우가 있습니다 | 43–59 | combination,scope,frequency | 사용 현황 서술 — 권고 아님 |
| E0791 | `/categories/16/common_concerns/2/a` | 다만 이렇게 피부 장벽이 열린 상태에서 배양액·엑소좀을 도포하면 사실상 진피 안으로 전달되므로, 앞서 안내드린 미허가 주사와 비슷한 감염·염증(육아종·결절) 위험이 생길 수 있습니다. | 61–163 | sentence,condition,site,depth,route,reference,comparison,adverse,possibility |  |
| E0792 | `/categories/16/common_concerns/2/a` | 피부 장벽이 열린 상태에서 | 68–82 | condition,site |  |
| E0793 | `/categories/16/common_concerns/2/a` | 사실상 진피 안으로 전달되므로 | 97–113 | depth,site,rationale,hedge |  |
| E0794 | `/categories/16/common_concerns/2/a` | 앞서 안내드린 미허가 주사 | 115–129 | reference | 같은 카테고리 /common_concerns/1/a 참조 |
| E0795 | `/categories/16/common_concerns/2/a` | 감염·염증(육아종·결절) 위험이 생길 수 있습니다 | 135–162 | adverse,paraphrase,possibility |  |
| E0796 | `/categories/16/common_concerns/2/a` | 실제로 미허가·오염된 제품을 시술 통로로 넣은 뒤 결절·육아종 등이 보고된 사례가 있어, 반드시 무균적으로 관리되고 검증된 제품을 사용해야 합니다. | 164–246 | sentence,evidence,condition,time,adverse,instruction |  |
| E0797 | `/categories/16/common_concerns/2/a` | 보고된 사례가 있어 | 202–212 | evidence | 출처 미기재 |
| E0798 | `/categories/16/common_concerns/2/a` | 반드시 무균적으로 관리되고 검증된 제품을 사용해야 합니다 | 214–245 | instruction,condition | 「검증」 기준 미기재 |
| E0799 | `/categories/16/common_concerns/2/a` | 병용의 미용 효과에 대한 임상 근거는 아직 제한적이므로, 병용 여부는 위험과 이득을 의사와 충분히 상담한 뒤 결정하시기 바랍니다. | 247–319 | sentence,combination,evidence,degree,instruction,actor,sequence |  |
| E0800 | `/categories/16/common_concerns/2/a` | 임상 근거는 아직 제한적이므로 | 261–277 | evidence,degree,time |  |
| E0801 | `/categories/16/common_concerns/2/a` | 의사와 충분히 상담한 뒤 결정하시기 바랍니다 | 294–318 | instruction,actor,sequence |  |
| E0802 | `/categories/16/common_concerns/2/a` | 배양액·엑소좀을 도포하면 | 83–96 | substance,route,condition | regex 대조 후 보충(구절 누락 수정) |
| E0803 | `/categories/16/common_concerns/2/a` | 미허가 주사와 비슷한 | 123–134 | regulatory,comparison,reference | regex 대조 후 보충(구절 누락 수정) |
| E0804 | `/categories/16/common_concerns/2/a` | 미허가·오염된 제품을 시술 통로로 넣은 뒤 | 168–191 | regulatory,condition,time,sequence | regex 대조 후 보충(구절 누락 수정) |
| E0805 | `/categories/16/common_concerns/2/a` | 다만 | 61–63 | contrast | 별도 읽기 검토(형태소 수식어 대조)로 보충 |
| E0806 | `/categories/16/common_concerns/2/a` | 실제로 | 164–167 | evidence | 별도 읽기 검토(형태소 수식어 대조)로 보충 |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/16/name`: 줄기세포/NNG 치료/NNG
- `/categories/16/patient_name`: 줄기세포/NNG 피부/NNG 재생/NNG
- `/categories/16/simple_explanation`: 줄기/NNG 세포/NNG 에서/JKB 추출/NNG 하/XSV ᆫ/ETM 재생/NNG 성분/NNG 을/JKO 이용/NNG 하/XSV 어/EC 피부/NNG 를/JKO 재생/NNG 하/XSV 는/ETM 시술/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/16/how_it_works`: 줄기/NNG 세포/NNG 의/JKG 배양액/NNG (/SSO 세포/NNG 가/JKS 만들/VV 어/EC 내/VX ᆫ/ETM 재생/NNG 성분/NNG )/SSC 을/JKO 피부/NNG 에/JKB 도포/NNG 하/XSV 거나/EC 주사/NNG 하/XSV ᆸ니다/EF ./SF 이/MM 성분/NNG 속/NNG 의/JKG 성장/NNG 인자/NNG 들/XSN 이/JKS 피부/NNG 세포/NNG 재생/NNG 을/JKO 촉진/NNG 하/XSV 고/EC ,/SP 콜라겐/NNP 합성/NNG 을/JKO 돕/VV-I 어/EC 피부/NNG 를/JKO 젊/VA 고/EC 건강/NNG 하/XSA 게/EC 만들/VV ᆸ니다/EF ./SF
- `/categories/16/duration_simple`: 효과/NNG 발현/NNG 2-4/W_SERIAL 주/NNB ,/SP 약/MM 3-6/W_SERIAL 개월/NNB 지속/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/16/pain_level`: 도포/NNG 시/NNB 통증/NNG 없/VA 음/ETN ,/SP 주사/NNG 시/NNB 마취/NNG 크림/NNG 사용/NNG 후/NNG 가볍/VA-I 은/ETM 따끔/XR 하/XSA ᆷ/EF
- `/categories/16/downtime`: 가볍/VA-I 은/ETM 붉/VA 은/ETM 기/NNG 1-2/W_SERIAL 일/NNG ,/SP 일상생활/NNG 가능/NNG
- `/categories/16/common_concerns/0/q`: 줄기/NNG 세포/NNG 를/JKO 직접/MAG 넣/VV 는/ETM 거/NNB 이/VCP ᆫ가요/EF ?/SF
- `/categories/16/common_concerns/0/a`: 아니/VCN ᆸ니다/EF ./SF 줄기세포/NNG 자체/NNG 가/JKC 아니/VCN 라/EC 줄기세포/NNP 가/JKS 만들/VV 어/EC 내/VX ᆫ/ETM 성장/NNG 인자/NNG 와/JC 재생/NNG 성분/NNG (/SSO 배양액/NNG )/SSC 을/JKO 사용/NNG 하/XSV ᆸ니다/EF ./SF 세포/NNG 자체/NNG 를/JKO 주입/NNG 하/XSV 는/ETM 것/NNB 과/JKB 는/JX 다르/VA ᆸ니다/EF ./SF
- `/categories/16/common_concerns/1/q`: 안전/NNG 하/XSA ᆫ/ETM 시술/NNG 이/VCP ᆫ가요/EF ?/SF
- `/categories/16/common_concerns/1/a`: 국내/NNG 에/JKB 주사/NNG 용/XSN 으로/JKB 허가/NNG 되/XSV ᆫ/ETM 줄기세포/NNG 배양액/NNG //SP 엑소좀/NNG 의약품/NNG 은/JX 없/VA 으며/EC ,/SP 배양액/NNG 은/JX 화장품/NNG (/SSO 도포/NNG )/SSC 용/XSN 원료/NNG 로/JKB 만/JX 허용/NNG 되/XSV ᆸ니다/EF ./SF 주사/NNG 사용/NNG 은/JX 허가/NNG 되/XSV ᆫ/ETM 적응증/NNG 이/JKC 아니/VCN 며/EC ,/SP 미/XPN 허가/NNG 주사/NNG 는/JX 알레르기/NNG ·/SP 감염/NNG 등/NNB 예측/NNG 하/XSV 기/ETN 어렵/VA-I 은/ETM 위험/NNG 이/JKS 있/VA 어/EC 안전/NNG 성/XSN 을/JKO 단정/NNG 하/XSV ᆯ/ETM 수/NNB 없/VA 습니다/EF ./SF
- `/categories/16/common_concerns/2/q`: 다른/MM 시술/NNG 과/JKB 함께/MAG 받/VV-R 을/ETM 수/NNB 있/VA 나요/EF ?/SF
- `/categories/16/common_concerns/2/a`: MTS/SL (/SSO 미세침/NNP )/SSC 나/JC 레이저/NNG 시술/NNG 후/NNG 미세/NNG 통로/NNG 를/JKO 통하/VV ᆫ/ETM 흡수/NNG 를/JKO 높이/VV 려는/ETM 목적/NNG 으로/JKB 함께/MAG 사용/NNG 하/XSV 는/ETM 경우/NNG 가/JKS 있/VV 습니다/EF ./SF 다만/MAG 이렇/VA-I 게/EC 피부/NNG 장벽/NNG 이/JKS 열리/VV ᆫ/ETM 상태/NNG 에서/JKB 배양액/NNG ·/SP 엑소좀/NNP 을/JKO 도포/NNG 하/XSV 면/EC 사실/NNG 상/XSN 진피/NNG 안/NNG 으로/JKB 전달/NNG 되/XSV 므로/EC ,/SP 앞서/MAG 안내/NNG 드리/VV ᆫ/ETM 미/XPN 허가/NNG 주사/NNG 와/JKB 비슷하/VA ᆫ/ETM 감염/NNG ·/SP 염증/NNG (/SSO 육아종/NNG ·/SP 결절/NNG )/SSC 위험/NNG 이/JKS 생기/VV ᆯ/ETM 수/NNB 있/VA 습니다/EF ./SF 실제로/MAG 미/XPN 허가/NNG ·/SP 오염/NNG 되/XSV ᆫ/ETM 제품/NNG 을/JKO 시술/NNG 통로/NNG 로/JKB 넣/VV 은/ETM 뒤/NNG 결절/NNG ·/SP 육아종/NNP 등/NNB 이/JKS 보고/NNG 되/XSV ᆫ/ETM 사례/NNG 가/JKS 있/VV 어/EC ,/SP 반드시/MAG 무/XPN 균/NNG 적/XSN 으로/JKB 관리/NNG 되/XSV 고/EC 검증/NNG 되/XSV ᆫ/ETM 제품/NNG 을/JKO 사용/NNG 하/XSV 어야/EC 하/VX ᆸ니다/EF ./SF 병용/NNG 의/JKG 미용/NNG 효과/NNG 에/JKB 대하/VV ᆫ/ETM 임상/NNG 근거/NNG 는/JX 아직/MAG 제한/NNG 적/XSN 이/VCP 므로/EC ,/SP 병용/NNG 여부/NNG 는/JX 위험/NNG 과/JC 이득/NNG 을/JKO 의사/NNG 와/JKB 충분히/MAG 상담/NNG 하/XSV ᆫ/ETM 뒤/NNG 결정/NNG 하/XSV 시/EP 기/ETN 바라/VV ᆸ니다/EF ./SF
