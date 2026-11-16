# S11 — `M3` (바이오스티뮬레이터) · extracted.json 1차 조사

> 구획 S11 · 소유 Pointer `/M3` 와 그 아래 57개 노드(말단 43). 문맥 참조: 루트 `""`, `/M3/name`, `/M3/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 4 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M3)` | `/M3` | object | (object · 16) | —(컨테이너) |
| 2 | `name` | `/M3/name` | string | 바이오스티뮬레이터 | 분석 |
| 3 | `safety` | `/M3/safety` | object | (object · 3) | —(컨테이너) |
| 4 | `safety.common` | `/M3/safety/common` | array | (array · 4) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M3/safety/common/0` | string | 주사 부위 홍반 (빨개짐) | 분석 |
| 6 | `safety.common[1]` | `/M3/safety/common/1` | string | 붓기 | 분석 |
| 7 | `safety.common[2]` | `/M3/safety/common/2` | string | 멍 | 분석 |
| 8 | `safety.common[3]` | `/M3/safety/common/3` | string | 압통 (누르면 아픈 느낌) | 분석 |
| 9 | `safety.serious` | `/M3/safety/serious` | array | (array · 3) | —(컨테이너) |
| 10 | `safety.serious[0]` | `/M3/safety/serious/0` | string | 이물반응 (몸이 주입 물질을 이물질로 인식해 만성 염증을 일으키는 것) | 분석 |
| 11 | `safety.serious[1]` | `/M3/safety/serious/1` | string | 혈관 막힘 (극히 드물지만 필러가 혈관에 들어갈 위험) | 분석 |
| 12 | `safety.serious[2]` | `/M3/safety/serious/2` | string | 감염 (무균 관리가 안 될 경우) | 분석 |
| 13 | `safety.uncommon` | `/M3/safety/uncommon` | array | (array · 3) | —(컨테이너) |
| 14 | `safety.uncommon[0]` | `/M3/safety/uncommon/0` | string | 피부 아래 결절 (딱딱한 덩어리가 만져지는 것) | 분석 |
| 15 | `safety.uncommon[1]` | `/M3/safety/uncommon/1` | string | 주입 물질이 원래 위치에서 이동하는 현상 | 분석 |
| 16 | `safety.uncommon[2]` | `/M3/safety/uncommon/2` | string | 색소침착 (시술 부위가 어두워지는 현상) | 분석 |
| 17 | `source` | `/M3/source` | string | 임상적 피부관리 35장 (연조직확대술) | 분석 |
| 18 | `name_en` | `/M3/name_en` | string | Biostimulator / Collagen Stimulator | 분석 |
| 19 | `updated` | `/M3/updated` | string | 2026-07-11 | 제외: 날짜값(YYYY-MM-DD) |
| 20 | `overview` | `/M3/overview` | string | 바이오스티뮬레이터는 피부 속에 특수 물질을 주입해서 우리 몸이 스스로 콜라겐(피부 탄력 단백질)을 만들도록 자극하는 시술이다. 일반 필러가 즉각적으로 볼륨을 채워주는 것과 달리, 바이오스티뮬레이터는 시간이 지나면서 자연스러운 콜라겐 재생 효과를 가져온다. 대표적으로 PLLA(스컬트라), CaHA(래디어스), PCL(엘란쎄), PDLLA(쥬베룩) 등이 있다. | 분석 |
| 21 | `aftercare` | `/M3/aftercare` | array | (array · 3) | —(컨테이너) |
| 22 | `aftercare[0]` | `/M3/aftercare/0` | string | PLLA(스컬트라) 시술 후 부드러운 마사지는 선택 (5-5-5 규칙의 결절 예방효과는 RCT 미입증; 핵심은 희석·주입) | 분석 |
| 23 | `aftercare[1]` | `/M3/aftercare/1` | string | 시술 후 과도한 음주, 사우나, 격렬한 운동 피하기 | 분석 |
| 24 | `aftercare[2]` | `/M3/aftercare/2` | string | 시술 부위를 강하게 누르거나 문지르지 않기 | 분석 |
| 25 | `mechanism` | `/M3/mechanism` | string | 바이오스티뮬레이터는 체내에서 분해되는 생체적합성 물질(PLLA, CaHA, PCL 등)을 피부 진피층이나 피하지방층에 주입한다. 주입된 미세 입자들이 주변 조직에 가벼운 이물반응(우리 몸이 이물질에 반응하는 것)을 일으키고, 이 과정에서 섬유모세포(콜라겐을 만드는 세포)가 활성화되어 새로운 콜라겐을 대량으로 생성한다. 주입 물질 자체는 서서히 분해되어 사라지지만, 새로 만들어진 콜라겐은 오랫동안 남아 피부 탄력과 볼륨을 유지해준다. 칼슘 기반 필러(래디어스)의 경우 칼슘을 기반으로 한 마이크로 입자가 주름과 꺼진 부분의 볼륨을 즉시 채워줄 뿐만 아니라, 새로운 콜라겐 생성을 촉진해 효과 지속기간이 평균 18~24개월로 기존 필러보다 길다. | 분석 |
| 26 | `indications` | `/M3/indications` | object | (object · 2) | —(컨테이너) |
| 27 | `indications.primary` | `/M3/indications/primary` | array | (array · 4) | —(컨테이너) |
| 28 | `indications.primary[0]` | `/M3/indications/primary/0` | string | 얼굴 볼륨 감소 (나이가 들면서 볼이 꺼지는 것) | 분석 |
| 29 | `indications.primary[1]` | `/M3/indications/primary/1` | string | 피부 탄력 저하 (늘어진 피부, 처진 피부) | 분석 |
| 30 | `indications.primary[2]` | `/M3/indications/primary/2` | string | 깊은 주름 (팔자주름, 볼 주름 등) | 분석 |
| 31 | `indications.primary[3]` | `/M3/indications/primary/3` | string | 얼굴 윤곽 보정 (관자놀이 꺼짐, 볼 꺼짐) | 분석 |
| 32 | `indications.extended` | `/M3/indications/extended` | array | (array · 4) | —(컨테이너) |
| 33 | `indications.extended[0]` | `/M3/indications/extended/0` | string | 손등 회춘술 (손등 볼륨 채움) | 분석 |
| 34 | `indications.extended[1]` | `/M3/indications/extended/1` | string | 목주름 개선 | 분석 |
| 35 | `indications.extended[2]` | `/M3/indications/extended/2` | string | 턱선 윤곽 보정 | 분석 |
| 36 | `indications.extended[3]` | `/M3/indications/extended/3` | string | 뺨 지방위축증 (뺨 볼륨 감소) | 분석 |
| 37 | `source_type` | `/M3/source_type` | string | kr | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 38 | `extracted_at` | `/M3/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 39 | `procedure_id` | `/M3/procedure_id` | string | M3-BIOSTIMULATOR | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 40 | `onset_duration` | `/M3/onset_duration` | object | (object · 3) | —(컨테이너) |
| 41 | `onset_duration.peak` | `/M3/onset_duration/peak` | string | 시술 후 2~3개월 뒤 콜라겐 재생 효과 최대 | 분석 |
| 42 | `onset_duration.onset` | `/M3/onset_duration/onset` | string | 즉각적 볼륨 효과 + 콜라겐 재생은 4~6주 후부터 시작 | 분석 |
| 43 | `onset_duration.duration` | `/M3/onset_duration/duration` | string | PLLA(스컬트라) 18~24개월, CaHA(래디어스) 18~24개월, PCL(엘란쎄) 12~48개월 (제품에 따라 다름) | 분석 |
| 44 | `contraindications` | `/M3/contraindications` | object | (object · 2) | —(컨테이너) |
| 45 | `contraindications.absolute` | `/M3/contraindications/absolute` | array | (array · 3) | —(컨테이너) |
| 46 | `contraindications.absolute[0]` | `/M3/contraindications/absolute/0` | string | 주입 물질 성분에 알레르기가 있는 경우 | 분석 |
| 47 | `contraindications.absolute[1]` | `/M3/contraindications/absolute/1` | string | 시술 부위에 감염이나 염증이 진행 중인 경우 | 분석 |
| 48 | `contraindications.absolute[2]` | `/M3/contraindications/absolute/2` | string | 켈로이드 체질 (흉터가 비정상적으로 부풀어오르는 체질) | 분석 |
| 49 | `contraindications.relative` | `/M3/contraindications/relative` | array | (array · 3) | —(컨테이너) |
| 50 | `contraindications.relative[0]` | `/M3/contraindications/relative/0` | string | 임신 중이거나 수유 중일 때는 미루는 게 좋음 | 분석 |
| 51 | `contraindications.relative[1]` | `/M3/contraindications/relative/1` | string | 자가면역질환이 있는 경우 의사와 상의 필요 | 분석 |
| 52 | `contraindications.relative[2]` | `/M3/contraindications/relative/2` | string | 혈액 응고에 영향을 주는 약물 복용 중이면 의사에게 알릴 것 | 분석 |
| 53 | `guardrail_version` | `/M3/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 54 | `related_techniques` | `/M3/related_techniques` | array | (array · 3) | —(컨테이너) |
| 55 | `related_techniques[0]` | `/M3/related_techniques/0` | string | 히알루론산 필러 -- 즉각적 볼륨 효과가 필요할 때 병합 | 분석 |
| 56 | `related_techniques[1]` | `/M3/related_techniques/1` | string | 보톡스 -- 주름 예방 목적으로 병합 가능 | 분석 |
| 57 | `related_techniques[2]` | `/M3/related_techniques/2` | string | 고주파(RF) 시술 -- 피부 타이트닝 효과 시너지 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S11-01** (I) 바이오스티뮬레이터 항목의 serious 가 「필러가 혈관에 들어갈 위험」이라고 적었다. 이 항목의 주입 물질을 필러라 부른 것인지 다른 시술의 위험을 옮긴 것인지 원문만으로 불명이다. mechanism 도 래디어스를 「칼슘 기반 필러」라 부른다. → I11  
  근거: `/M3/safety/serious/1` 「필러가 혈관에 들어갈 위험」; `/M3/mechanism` 「칼슘 기반 필러(래디어스)」
- **OB-S11-02** (B) overview 는 제품 넷(PLLA·CaHA·PCL·PDLLA)을 들지만 duration 은 PLLA·CaHA·PCL 셋만 기간을 준다. PDLLA(쥬베룩) 기간은 없다. → B5  
  근거: `/M3/overview` 「PDLLA(쥬베룩)」; `/M3/onset_duration/duration` 「PCL(엘란쎄) 12~48개월」
- **OB-S11-03** (구조) 이 원장에서 updated 키는 M3 에만 있다(2026-07-11). aftercare 첫 값에는 근거 진술(RCT 미입증)과 「;」 구분자가 있다. → B9, F8  
  근거: `/M3/updated` 「2026-07-11」; `/M3/aftercare/0` 「RCT 미입증; 핵심은」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX120 | frequency_degree_scoped | `/M3/safety/serious/1` | 극히 드물지만 필러가 혈관에 들어갈 위험 |  |
| MX121 | optional_instruction | `/M3/aftercare/0` | 부드러운 마사지는 선택 |  |
| MX122 | negated_evidence_statement | `/M3/aftercare/0` | 5-5-5 규칙의 결절 예방효과는 RCT 미입증; 핵심은 희석·주입 |  |
| MX123 | quantity_comparison | `/M3/mechanism` | 효과 지속기간이 평균 18~24개월로 기존 필러보다 길다 |  |
| MX124 | symbol_conjunction_time | `/M3/onset_duration/onset` | 즉각적 볼륨 효과 + 콜라겐 재생은 4~6주 후부터 시작 | 「+」가 효과 두 가지의 병렬 |
| MX125 | subtype_time | `/M3/onset_duration/duration` | PCL(엘란쎄) 12~48개월 (제품에 따라 다름) |  |
| MX126 | condition_combination | `/M3/related_techniques/0` | 즉각적 볼륨 효과가 필요할 때 병합 |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|
| R02-1 | `/M3/mechanism` | [106,109) | 이물질 | 이/MM + 물질/NNG | 관형사 「이」 오분리 — 「이물질」 | 「이물」(foreign body) 개념이 지시어 「이」 + 「물질」로 바뀜. 이물반응 관련 탐색 누락 |
| R08-2 | `/M3/safety/serious/1` | [15,18) | 필러가 | 필러가/NNG | 「필러」+조사가 한 명사(NNG)로 묶임(필러가·필러와) | 조사 정보 소실 및 명사 형태가 「필러가」로 남아 시술명 집계·대조에서 누락 |
| R11-4 | `/M3/safety/common/2` | [0,1) | 멍 | 멍/MAG | 단독 값 「멍」(타박 멍)을 부사(MAG)로 태깅 | 부작용 사건 명사가 부사로 분류 — 품사로 사건 명사를 고르면 누락. 값 자체는 원문 보존 |

규칙 기반 표현 후보 266건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S11"` 에 있다. 후보이며 전수 의미 해석이 아니다.
