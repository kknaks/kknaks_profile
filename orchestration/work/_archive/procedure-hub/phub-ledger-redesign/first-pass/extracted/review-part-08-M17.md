# S08 — `M17` (줄기세포치료) · extracted.json 1차 조사

> 구획 S08 · 소유 Pointer `/M17` 와 그 아래 47개 노드(말단 33). 문맥 참조: 루트 `""`, `/M17/name`, `/M17/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 3 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M17)` | `/M17` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M17/name` | string | 줄기세포치료 | 분석 |
| 3 | `safety` | `/M17/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M17/safety/common` | array | (array · 2) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M17/safety/common/0` | string | 지방흡입 부위의 일시적 통증과 멍 | 분석 |
| 6 | `safety.common[1]` | `/M17/safety/common/1` | string | 이식 부위의 약간의 부종 | 분석 |
| 7 | `safety.serious` | `/M17/safety/serious` | array | (array · 1) | —(컨테이너) |
| 8 | `safety.serious[0]` | `/M17/safety/serious/0` | string | 줄기세포 치료의 단기 효과는 비교적 만족스럽지만, 장기적 안전성에 대한 연구가 아직 충분하지 않음 | 분석 |
| 9 | `safety.uncommon` | `/M17/safety/uncommon` | array | (array · 1) | —(컨테이너) |
| 10 | `safety.uncommon[0]` | `/M17/safety/uncommon/0` | string | 이식된 세포가 시간이 지나면서 일부 흡수되어 효과가 줄어들 수 있음 | 분석 |
| 11 | `source` | `/M17/source` | string | 임상적 피부관리 34장 | 분석 |
| 12 | `name_en` | `/M17/name_en` | string | Stem Cell Therapy | 분석 |
| 13 | `overview` | `/M17/overview` | string | 줄기세포치료는 우리 몸의 줄기세포(여러 종류의 세포로 변할 수 있는 '만능 세포')를 이용해 피부를 재생하는 시술이다. 주로 자신의 지방에서 추출한 지방유래줄기세포(ADSCs)를 활용하며, 피부 노화 개선, 함몰흉터(꺼진 흉터) 치료, 피부 탄력 회복 등에 사용된다. 줄기세포 배양액(AAPE 등) 성분을 이용한 화장품도 개발되고 있다. | 분석 |
| 14 | `aftercare` | `/M17/aftercare` | array | (array · 3) | —(컨테이너) |
| 15 | `aftercare[0]` | `/M17/aftercare/0` | string | 이식 부위를 강하게 누르거나 마사지하지 않기 | 분석 |
| 16 | `aftercare[1]` | `/M17/aftercare/1` | string | 의사의 지시에 따라 경과 관찰하기 | 분석 |
| 17 | `aftercare[2]` | `/M17/aftercare/2` | string | 지방흡입 부위는 압박 붕대 착용이 필요할 수 있음 | 분석 |
| 18 | `mechanism` | `/M17/mechanism` | string | 지방조직에서 줄기세포를 분리하면 지방유래줄기세포(ADSCs)를 얻을 수 있다. 이 줄기세포는 EGF(표피성장인자), FGF(섬유모세포성장인자), HGF, TGF-β 등 다양한 성장인자와 콜라겐, 히알루론산 같은 세포외기질 단백질을 풍부하게 분비한다. 이들이 주변 세포의 성장과 새로운 조직 형성을 도와 피부를 재생시킨다. 아디포셀(Adipocell)의 경우, 자기 지방에서 분리한 줄기세포를 지방세포로 완전히 분화시킨 '어린 지방세포'를 피부 아래에 이식해, 함몰된 부위의 부피를 자연스럽게 채우고 시간이 지나면서 성숙해져 부피가 더 늘어난다. SVF(기질혈관분획) 치료법은 지방조직에서 추출한 줄기세포, 섬유모세포, 면역세포 등이 섞인 혼합물을 이식해 피부 재생을 유도한다. | 분석 |
| 19 | `indications` | `/M17/indications` | object | (object · 2) | —(컨테이너) |
| 20 | `indications.primary` | `/M17/indications/primary` | array | (array · 2) | —(컨테이너) |
| 21 | `indications.primary[0]` | `/M17/indications/primary/0` | string | 함몰흉터 (여드름, 수술, 창상, 선천적 기형 등으로 꺼진 피부) | 분석 |
| 22 | `indications.primary[1]` | `/M17/indications/primary/1` | string | 노화로 인한 피부주름 및 볼륨 감소 | 분석 |
| 23 | `indications.extended` | `/M17/indications/extended` | array | (array · 4) | —(컨테이너) |
| 24 | `indications.extended[0]` | `/M17/indications/extended/0` | string | 피부 탄력 개선 | 분석 |
| 25 | `indications.extended[1]` | `/M17/indications/extended/1` | string | 피부 미백 효과 (ADSCs의 TGF-β가 멜라닌 생성을 줄일 가능성) | 분석 |
| 26 | `indications.extended[2]` | `/M17/indications/extended/2` | string | 상처 치유 촉진 | 분석 |
| 27 | `indications.extended[3]` | `/M17/indications/extended/3` | string | 지방이식 시 생착률 향상 (ADSCs 병행) | 분석 |
| 28 | `source_type` | `/M17/source_type` | string | kr | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 29 | `extracted_at` | `/M17/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 30 | `procedure_id` | `/M17/procedure_id` | string | M17-STEMCELL | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 31 | `onset_duration` | `/M17/onset_duration` | object | (object · 3) | —(컨테이너) |
| 32 | `onset_duration.peak` | `/M17/onset_duration/peak` | string | 아디포셀의 경우 12개월에 걸쳐 성숙하며 부피 증가 | 분석 |
| 33 | `onset_duration.onset` | `/M17/onset_duration/onset` | string | 이식 후 서서히 효과 발현 (세포가 자리잡는 데 수주 소요) | 분석 |
| 34 | `onset_duration.duration` | `/M17/onset_duration/duration` | string | 살아있는 세포를 이식하므로 효과가 오래 지속될 수 있지만, 재흡수율에 따라 차이 있음 | 분석 |
| 35 | `contraindications` | `/M17/contraindications` | object | (object · 2) | —(컨테이너) |
| 36 | `contraindications.absolute` | `/M17/contraindications/absolute` | array | (array · 2) | —(컨테이너) |
| 37 | `contraindications.absolute[0]` | `/M17/contraindications/absolute/0` | string | 악성 종양(암)이 있는 경우 | 분석 |
| 38 | `contraindications.absolute[1]` | `/M17/contraindications/absolute/1` | string | 전신 감염이 있는 경우 | 분석 |
| 39 | `contraindications.relative` | `/M17/contraindications/relative` | array | (array · 3) | —(컨테이너) |
| 40 | `contraindications.relative[0]` | `/M17/contraindications/relative/0` | string | 지방 채취가 불가능할 정도로 체지방이 적은 경우 | 분석 |
| 41 | `contraindications.relative[1]` | `/M17/contraindications/relative/1` | string | 자가면역질환이 있는 경우 의사와 상의 필요 | 분석 |
| 42 | `contraindications.relative[2]` | `/M17/contraindications/relative/2` | string | 장기적인 부작용에 대한 평가가 아직 미흡한 상태이므로 신중한 결정 필요 | 분석 |
| 43 | `guardrail_version` | `/M17/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 44 | `related_techniques` | `/M17/related_techniques` | array | (array · 3) | —(컨테이너) |
| 45 | `related_techniques[0]` | `/M17/related_techniques/0` | string | 자가지방이식 — 줄기세포 없이 지방만 이식하는 기존 방법 | 분석 |
| 46 | `related_techniques[1]` | `/M17/related_techniques/1` | string | SVF(기질혈관분획) 치료법 — 지방에서 추출한 줄기세포 혼합물 이식 | 분석 |
| 47 | `related_techniques[2]` | `/M17/related_techniques/2` | string | 줄기세포 배양액(AAPE) — 줄기세포가 분비한 성장인자 단백질을 이용한 치료 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S08-01** (I) safety/serious 값이 사건이 아니라 근거 상태 진술이고, uncommon 값은 효과 감소 가능성이다. contraindications/relative 셋째 값도 환자 조건이 아니라 평가 미흡에 따른 권고다. → I6, I8  
  근거: `/M17/safety/serious/0` 「장기적 안전성에 대한 연구가 아직 충분하지 않음」; `/M17/safety/uncommon/0` 「효과가 줄어들 수 있음」; `/M17/contraindications/relative/2` 「평가가 아직 미흡한 상태이므로 신중한 결정 필요」
- **OB-S08-02** (B) 하위 방법(ADSCs·아디포셀·SVF·배양액)이 overview·mechanism·related 에 나오는데 peak 은 아디포셀만 적었고 나머지 방법의 정점 시기는 없다. duration 에도 기간 값이 없다. → B3, B5  
  근거: `/M17/onset_duration/peak` 「아디포셀의 경우 12개월에 걸쳐」; `/M17/onset_duration/duration` 「재흡수율에 따라 차이 있음」
- **OB-S08-03** (F) 부위 역할이 둘이다 — 지방흡입(채취) 부위의 통증·멍·압박 붕대, 이식 부위의 부종·누르지 않기. → F1  
  근거: `/M17/safety/common/0` 「지방흡입 부위」; `/M17/safety/common/1` 「이식 부위」; `/M17/aftercare/2` 「지방흡입 부위는 압박 붕대」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX085 | site_role | `/M17/safety/common/0` | 지방흡입 부위의 일시적 통증과 멍 | 채취(지방흡입) 부위 |
| MX086 | site_role | `/M17/safety/common/1` | 이식 부위의 약간의 부종 | 이식 부위 |
| MX087 | evidence_gap_statement | `/M17/safety/serious/0` | 장기적 안전성에 대한 연구가 아직 충분하지 않음 | safety/serious 칸이 사건이 아닌 근거 진술(I6) |
| MX088 | possibility_statement | `/M17/safety/uncommon/0` | 일부 흡수되어 효과가 줄어들 수 있음 |  |
| MX089 | possibility_obligation | `/M17/aftercare/2` | 압박 붕대 착용이 필요할 수 있음 |  |
| MX090 | subtype_condition | `/M17/mechanism` | 아디포셀(Adipocell)의 경우 |  |
| MX091 | possibility_statement | `/M17/indications/extended/1` | 멜라닌 생성을 줄일 가능성 |  |
| MX092 | subtype_time | `/M17/onset_duration/peak` | 아디포셀의 경우 12개월에 걸쳐 |  |
| MX093 | speed_modifier_scoped | `/M17/onset_duration/onset` | 이식 후 서서히 효과 발현 |  |
| MX094 | possibility_condition | `/M17/onset_duration/duration` | 오래 지속될 수 있지만, 재흡수율에 따라 차이 있음 |  |
| MX095 | negated_threshold_condition | `/M17/contraindications/relative/0` | 지방 채취가 불가능할 정도로 체지방이 적은 경우 |  |
| MX096 | evidence_gap_statement | `/M17/contraindications/relative/2` | 장기적인 부작용에 대한 평가가 아직 미흡한 상태이므로 신중한 결정 필요 | 금기 칸이 환자 조건이 아님(I8) |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|

규칙 기반 표현 후보 202건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S08"` 에 있다. 후보이며 전수 의미 해석이 아니다.
