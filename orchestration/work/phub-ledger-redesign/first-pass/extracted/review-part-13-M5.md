# S13 — `M5` (PRP 피부재생술) · extracted.json 1차 조사

> 구획 S13 · 소유 Pointer `/M5` 와 그 아래 50개 노드(말단 36). 문맥 참조: 루트 `""`, `/M5/name`, `/M5/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 5 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M5)` | `/M5` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M5/name` | string | PRP 피부재생술 | 분석 |
| 3 | `safety` | `/M5/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M5/safety/common` | array | (array · 3) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M5/safety/common/0` | string | 주사 부위 통증 | 분석 |
| 6 | `safety.common[1]` | `/M5/safety/common/1` | string | 1~2일 정도 붓기 | 분석 |
| 7 | `safety.common[2]` | `/M5/safety/common/2` | string | 3~7일 정도 멍이 들 수 있음 | 분석 |
| 8 | `safety.serious` | `/M5/safety/serious` | array | (array · 1) | —(컨테이너) |
| 9 | `safety.serious[0]` | `/M5/safety/serious/0` | string | 본인 혈액을 사용하므로 알레르기·거부반응이 거의 없음 (매우 안전한 시술) | 분석 |
| 10 | `safety.uncommon` | `/M5/safety/uncommon` | array | (array · 1) | —(컨테이너) |
| 11 | `safety.uncommon[0]` | `/M5/safety/uncommon/0` | string | 피부 재생 정도가 사람마다 달라 시술 결과에 차이가 있을 수 있음 | 분석 |
| 12 | `source` | `/M5/source` | string | 임상적 피부관리 33장 | 분석 |
| 13 | `name_en` | `/M5/name_en` | string | Platelet-Rich Plasma Therapy | 분석 |
| 14 | `overview` | `/M5/overview` | string | PRP는 자기 혈액에서 혈소판이 풍부한 혈장(피를 뽑아서 성장인자가 많은 부분만 모은 것)을 추출해 피부에 주사하거나 바르는 재생 시술이다. 1987년 심장수술에서 처음 사용된 후, 피부 노화 개선 효과가 알려지면서 미용 분야에서 단독 또는 다른 시술과 병행해 널리 쓰이고 있다. | 분석 |
| 15 | `aftercare` | `/M5/aftercare` | array | (array · 3) | —(컨테이너) |
| 16 | `aftercare[0]` | `/M5/aftercare/0` | string | 시술 후 세안이나 화장 등 일상생활에 지장 없음 | 분석 |
| 17 | `aftercare[1]` | `/M5/aftercare/1` | string | 시술 부위 청결 유지 | 분석 |
| 18 | `aftercare[2]` | `/M5/aftercare/2` | string | 깊은 주름이나 심한 노화에는 PRP 단독보다 고주파, IPL, 필러, 보톡스, 지방이식 등과 병행하는 것이 좋음 | 분석 |
| 19 | `mechanism` | `/M5/mechanism` | string | 환자 본인의 혈액을 채취해 원심분리기(빠르게 회전시키는 기계)로 돌려 혈소판이 농축된 혈장을 추출한다. 이 PRP에는 PDGF, TGF-β, VEGF, EGF, IGF 등 다양한 성장인자(세포 성장을 촉진하는 단백질)가 풍부하게 들어있다. 이 성장인자들이 피부의 섬유모세포(콜라겐을 만드는 세포)를 자극해서 새로운 콜라겐과 엘라스틴(피부 탄력 성분)을 만들어내고, 히알루론산 생성도 촉진한다. 활성화된 PRP는 피브린 네트워크(그물 구조)를 형성해 피부에 볼륨감도 준다. | 분석 |
| 20 | `indications` | `/M5/indications` | object | (object · 2) | —(컨테이너) |
| 21 | `indications.primary` | `/M5/indications/primary` | array | (array · 3) | —(컨테이너) |
| 22 | `indications.primary[0]` | `/M5/indications/primary/0` | string | 피부 노화 개선 (전반적인 피부결, 탄력, 피부톤 개선) | 분석 |
| 23 | `indications.primary[1]` | `/M5/indications/primary/1` | string | 잔주름 감소 | 분석 |
| 24 | `indications.primary[2]` | `/M5/indications/primary/2` | string | 꺼진 부위 볼륨 회복 (꺼진 볼, 꺼진 눈밑, 팔자주름 등) | 분석 |
| 25 | `indications.extended` | `/M5/indications/extended` | array | (array · 4) | —(컨테이너) |
| 26 | `indications.extended[0]` | `/M5/indications/extended/0` | string | 여드름흉터 (진피절제주입법과 병행) | 분석 |
| 27 | `indications.extended[1]` | `/M5/indications/extended/1` | string | 탈모치료 (두피에 주입) | 분석 |
| 28 | `indications.extended[2]` | `/M5/indications/extended/2` | string | 처진 피부 탄력 개선 | 분석 |
| 29 | `indications.extended[3]` | `/M5/indications/extended/3` | string | 다른 시술과 병행 — MTS, 프랙셔널 레이저, 메조테라피 후 도포 | 분석 |
| 30 | `source_type` | `/M5/source_type` | string | kr | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 31 | `extracted_at` | `/M5/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 32 | `procedure_id` | `/M5/procedure_id` | string | M5-PRP | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 33 | `onset_duration` | `/M5/onset_duration` | object | (object · 3) | —(컨테이너) |
| 34 | `onset_duration.peak` | `/M5/onset_duration/peak` | string | 2~3개월에 걸쳐 서서히 좋아짐 | 분석 |
| 35 | `onset_duration.onset` | `/M5/onset_duration/onset` | string | 시술 후 3~6주경부터 효과가 나타나기 시작 | 분석 |
| 36 | `onset_duration.duration` | `/M5/onset_duration/duration` | string | 1회 시술로 6~12개월 유지 (반복시술은 4~6주 간격 가능) | 분석 |
| 37 | `contraindications` | `/M5/contraindications` | object | (object · 2) | —(컨테이너) |
| 38 | `contraindications.absolute` | `/M5/contraindications/absolute` | array | (array · 3) | —(컨테이너) |
| 39 | `contraindications.absolute[0]` | `/M5/contraindications/absolute/0` | string | 혈소판 기능 장애가 있는 경우 | 분석 |
| 40 | `contraindications.absolute[1]` | `/M5/contraindications/absolute/1` | string | 패혈증이나 전신 감염이 있는 경우 | 분석 |
| 41 | `contraindications.absolute[2]` | `/M5/contraindications/absolute/2` | string | 주사 부위에 활동성 감염이나 염증이 있는 경우 | 분석 |
| 42 | `contraindications.relative` | `/M5/contraindications/relative` | array | (array · 3) | —(컨테이너) |
| 43 | `contraindications.relative[0]` | `/M5/contraindications/relative/0` | string | 혈액 응고에 영향을 주는 약물(아스피린 등) 복용 중이면 출혈 위험이 높아질 수 있음 | 분석 |
| 44 | `contraindications.relative[1]` | `/M5/contraindications/relative/1` | string | 혈액으로 인한 감염성 질환이 있는 경우 주의 | 분석 |
| 45 | `contraindications.relative[2]` | `/M5/contraindications/relative/2` | string | 색소성 질환에 대한 치료 효과는 적은 편 | 분석 |
| 46 | `guardrail_version` | `/M5/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 47 | `related_techniques` | `/M5/related_techniques` | array | (array · 3) | —(컨테이너) |
| 48 | `related_techniques[0]` | `/M5/related_techniques/0` | string | MTS + PRP — MTS로 미세 구멍을 낸 후 PRP를 도포해 흡수 촉진 | 분석 |
| 49 | `related_techniques[1]` | `/M5/related_techniques/1` | string | 프랙셔널 레이저 + PRP — 레이저 시술 후 PRP를 도포해 재생 효과 증대 | 분석 |
| 50 | `related_techniques[2]` | `/M5/related_techniques/2` | string | 진피절제주입법 + PRP — 여드름흉터에 서브시전 후 PRP 주입 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S13-01** (I) safety/serious 값은 사건이 아니라 사건 부재 주장(알레르기·거부반응이 거의 없음, 매우 안전)이다. uncommon 값은 결과 차이다. aftercare 셋째 값은 병합 권고, contraindications/relative 셋째 값은 효과 진술이다. → I6, I8, I13  
  근거: `/M5/safety/serious/0` 「거의 없음 (매우 안전한 시술)」; `/M5/safety/uncommon/0` 「시술 결과에 차이가 있을 수 있음」; `/M5/aftercare/2` 「병행하는 것이 좋음」; `/M5/contraindications/relative/2` 「치료 효과는 적은 편」
- **OB-S13-02** (F) duration 괄호의 「반복시술은 4~6주 간격 가능」은 재시술 간격이다. 지속 기간(6~12개월)과 같은 값에 있다. → F5  
  근거: `/M5/onset_duration/duration` 「반복시술은 4~6주 간격 가능」
- **OB-S13-03** (F) related 세 값은 「A + PRP — 순서 설명」 꼴이며 설명에 「후」로 선후가 있다(MTS 후 도포, 레이저 시술 후 도포, 서브시전 후 주입). → F6, F5  
  근거: `/M5/related_techniques/0` 「MTS로 미세 구멍을 낸 후」; `/M5/related_techniques/1` 「레이저 시술 후」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX133 | possibility_with_time | `/M5/safety/common/2` | 3~7일 정도 멍이 들 수 있음 |  |
| MX134 | negated_safety_claim | `/M5/safety/serious/0` | 알레르기·거부반응이 거의 없음 (매우 안전한 시술) | serious 칸이 사건 부재 진술(I6) |
| MX135 | possibility_variability | `/M5/safety/uncommon/0` | 시술 결과에 차이가 있을 수 있음 |  |
| MX136 | condition_combination_recommendation | `/M5/aftercare/2` | 깊은 주름이나 심한 노화에는 PRP 단독보다 고주파, IPL, 필러, 보톡스, 지방이식 등과 병행하는 것이 좋음 | aftercare 칸이 병합 권고(I13) |
| MX137 | interval | `/M5/onset_duration/duration` | (반복시술은 4~6주 간격 가능) |  |
| MX138 | time_window_with_anchor | `/M5/onset_duration/onset` | 시술 후 3~6주경부터 |  |
| MX139 | efficacy_in_contraindication | `/M5/contraindications/relative/2` | 색소성 질환에 대한 치료 효과는 적은 편 | 금기 칸이 효과 진술(I8) |
| MX140 | sequence_after | `/M5/related_techniques/0` | MTS로 미세 구멍을 낸 후 PRP를 도포해 |  |
| MX141 | sequence_after | `/M5/related_techniques/2` | 여드름흉터에 서브시전 후 PRP 주입 |  |
| MX184 | historical_claim | `/M5/overview` | 1987년 심장수술에서 처음 사용된 후 |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|
| R07-2 | `/M5/aftercare/2` | [35,37) | 필러 | 필/NNP + 러/EC | 「필러」가 필 + 러/EC(연결어미)로 분절 | 시술명 「필러」 식별 실패(같은 원장 다른 출현은 NNP 로 정상). 시술명 교차 참조 탐색 누락 |

규칙 기반 표현 후보 230건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S13"` 에 있다. 후보이며 전수 의미 해석이 아니다.
