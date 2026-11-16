# review-part-S4 — /combos/3 (P4 피부결/톤/항노화) 전체

원본: `orchestration/work/phub-recommend/bronze/phub-ledger/problem-combos.json` sha256 `74453c724800975ef7f3fa8b81546fe69fa014bfbc7a8f7e60c75774c2cf2262`

## 원문 값

원본 컬럼명은 축약하지 않는다. 배열은 원본 순서. 원문 칸에는 원문만 둔다.

### `/combos/3` 묶음

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | object | 키 ['problem_id', 'problem', 'packages'] | `/combos/3` |
| `problem_id` | string | P4 | `/combos/3/problem_id` |
| `problem` | string | 피부결/톤/항노화 | `/combos/3/problem` |
| `packages` | array | (길이 3) | `/combos/3/packages` |

### `/combos/3/packages/0` — P4-1 스킨부스터 단독

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/3/packages/0` |
| `id` | string | P4-1 | `/combos/3/packages/0/id` |
| `tier` | string | entry | `/combos/3/packages/0/tier` |
| `tierLabel` | string | 기본 | `/combos/3/packages/0/tierLabel` |
| `name` | string | 스킨부스터 단독 | `/combos/3/packages/0/name` |
| `procedures` | array | (길이 1) | `/combos/3/packages/0/procedures` |
| `procedures[0]` | string | M4 | `/combos/3/packages/0/procedures/0` |
| `productTier` | string | 국산 | `/combos/3/packages/0/productTier` |
| `products` | array | (길이 1) | `/combos/3/packages/0/products` |
| `products[0]` | string | 리쥬란 힐러 | `/combos/3/packages/0/products/0` |
| `priceRange` | string | 15~25만 | `/combos/3/packages/0/priceRange` |
| `expectedResult` | string | 피부 수분감·광채 향상. 잔주름 완화. 3~5회 반복 시 확연한 차이 | `/combos/3/packages/0/expectedResult` |
| `salesPitch` | string | 피부결 관리의 기본이에요. 한 번만 해보시면 촉촉함이 다르다는 걸 느끼실 거예요. 월 1회가 이상적이에요. | `/combos/3/packages/0/salesPitch` |
| `upsellHook` | string | 스킨부스터 전에 MTS로 채널 열고 하시면 흡수율이 훨씬 좋아요! MTS+스킨부스터 패키지가 있어요. | `/combos/3/packages/0/upsellHook` |
| `clinicalRationale` | string | PN/PDRN이 진피 섬유아세포를 자극하여 콜라겐·엘라스틴 합성 촉진. 반복 시술로 진피 두께 증가 | `/combos/3/packages/0/clinicalRationale` |
| `riskBenefit` | string | 위험 최소. 자잘한 구진 1~3일 내 소실. 가격 대비 만족도 높음 | `/combos/3/packages/0/riskBenefit` |

### `/combos/3/packages/1` — P4-2 MTS + PRP + 스킨부스터 (골든루틴)

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/3/packages/1` |
| `id` | string | P4-2 | `/combos/3/packages/1/id` |
| `tier` | string | recommended | `/combos/3/packages/1/tier` |
| `tierLabel` | string | 표준 | `/combos/3/packages/1/tierLabel` |
| `name` | string | MTS + PRP + 스킨부스터 (골든루틴) | `/combos/3/packages/1/name` |
| `procedures` | array | (길이 3) | `/combos/3/packages/1/procedures` |
| `procedures[0]` | string | M12 | `/combos/3/packages/1/procedures/0` |
| `procedures[1]` | string | M5 | `/combos/3/packages/1/procedures/1` |
| `procedures[2]` | string | M4 | `/combos/3/packages/1/procedures/2` |
| `productTier` | string | 국산 | `/combos/3/packages/1/productTier` |
| `products` | array | (길이 1) | `/combos/3/packages/1/products` |
| `products[0]` | string | MTS + 자가 PRP + 리쥬란 | `/combos/3/packages/1/products/0` |
| `priceRange` | string | 30~50만 | `/combos/3/packages/1/priceRange` |
| `expectedResult` | string | 피부결·톤·탄력 종합 개선. '아기 피부' 효과. 3~5회 1클 권장 | `/combos/3/packages/1/expectedResult` |
| `salesPitch` | string | 저희 클리닉 시그니처 프로그램이에요! MTS로 구멍 열고 PRP+스킨부스터 넣으면 흡수율이 수십 배예요. 피부 재생의 골든루틴이라 불려요. | `/combos/3/packages/1/salesPitch` |
| `upsellHook` | string | 피부결에 색소·기미도 있으시면 레이저 토닝 추가가 가능해요. 같이 하시면 톤 균일 + 재생 시너지! | `/combos/3/packages/1/upsellHook` |
| `clinicalRationale` | string | MTS(채널 생성) → PRP(성장인자 PDGF·TGF-β 전달) → 스킨부스터(PDRN·HA 전달) = 경피 흡수율 극대화. 세포 재생의 3가지 신호(성장인자+DNA회복+수분)를 동시 공급 | `/combos/3/packages/1/clinicalRationale` |
| `riskBenefit` | string | 위험 낮음. MTS 후 약간의 홍반·출혈은 정상. 24시간 세안 제한. 자가혈(PRP)이라 알레르기 위험 없음 | `/combos/3/packages/1/riskBenefit` |

### `/combos/3/packages/2` — P4-3 레이저 + MTS + PRP + 스킨부스터

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/3/packages/2` |
| `id` | string | P4-3 | `/combos/3/packages/2/id` |
| `tier` | string | premium | `/combos/3/packages/2/tier` |
| `tierLabel` | string | 확장 | `/combos/3/packages/2/tierLabel` |
| `name` | string | 레이저 + MTS + PRP + 스킨부스터 | `/combos/3/packages/2/name` |
| `procedures` | array | (길이 4) | `/combos/3/packages/2/procedures` |
| `procedures[0]` | string | M8 | `/combos/3/packages/2/procedures/0` |
| `procedures[1]` | string | M12 | `/combos/3/packages/2/procedures/1` |
| `procedures[2]` | string | M5 | `/combos/3/packages/2/procedures/2` |
| `procedures[3]` | string | M4 | `/combos/3/packages/2/procedures/3` |
| `productTier` | string | 수입+국산 | `/combos/3/packages/2/productTier` |
| `products` | array | (길이 1) | `/combos/3/packages/2/products` |
| `products[0]` | string | 피코레이저/프락셀 + MTS + PRP + 리쥬란 | `/combos/3/packages/2/products/0` |
| `priceRange` | string | 50~90만 | `/combos/3/packages/2/priceRange` |
| `expectedResult` | string | 색소+피부결+톤+탄력 종합 리뉴얼. 확실한 피부 업그레이드 | `/combos/3/packages/2/expectedResult` |
| `salesPitch` | string | 피부 리뉴얼 풀 프로그램이에요. 레이저로 묵은 각질·색소 정리하고, MTS+PRP+스킨부스터로 새 피부를 만들어요. 프리미엄 피부관리의 정석! | `/combos/3/packages/2/salesPitch` |
| `upsellHook` | string | 탄력까지 원하시면 HIFU를 다음 회차에 추가하시는 분들이 많아요. | `/combos/3/packages/2/upsellHook` |
| `clinicalRationale` | string | 레이저(표피 색소 파괴+진피 미세 열손상) → MTS(채널 추가 확보) → PRP(재생 촉진) → 스킨부스터(수분+DNA 회복). 자극(레이저·MTS) + 재생(PRP·스킨부스터)의 이상적 밸런스 | `/combos/3/packages/2/clinicalRationale` |
| `riskBenefit` | string | 레이저 후 자외선 차단 필수. 시술 순서 반드시 준수(레이저→MTS→PRP→스킨부스터). 열 시술(레이저) + 채널(MTS) + 재생(PRP/SB) 조합은 과학적 근거 충분 | `/combos/3/packages/2/riskBenefit` |

## 잠정 관찰 (원문과 분리)

| Pointer | 상태 | 관찰 |
|---|---|---|
| `/combos/3/problem` | P | "피부결/톤/항노화" 세 항목을 '/'로 나열. 대안인지 묶음인지 정의 없음(F). |
| `/combos/3/packages/1/name` | P | name에 괄호 별칭 "(골든루틴)" — 패키지 별칭. salesPitch '골든루틴이라 불려요'와 대응. |
| `/combos/3/packages/1/expectedResult` | B | "3~5회 1클 권장" — '1클'(1클래스/1코스로 추정되는 약어) 뜻이 원문에 없음. 추정해 채우지 않음. |
| `/combos/3/packages/2/riskBenefit` | P | "PRP/SB" — SB가 스킨부스터 약어로 보이나 원문 정의 없음(P). '/'가 대안이 아니라 둘을 함께 묶는 쓰임으로 읽혀 README 규칙과 다를 수 있음. |
| `/combos/3/packages/2/productTier` | P | "수입+국산" — 다른 항목 "국산+수입 혼합"과 표기 순서·형태가 다름. |
| `/combos/3/packages/2/products/0` | P | "피코레이저/프락셀" — '/' 대안 표기. |
| `/combos/3/packages/1/salesPitch` | P | "흡수율이 수십 배예요" — 수치 주장, 근거 미기재. 임상 판단 안 함. |
| `/combos/3/packages/1/riskBenefit` | P | "24시간 세안 제한" — 시술 후 관리 지시가 riskBenefit 칸에 있음. |
| `/combos/3/packages/0/salesPitch` | P | "월 1회가 이상적이에요" 주기 권장이 salesPitch에 있음. |
| `/combos/3/packages/1/procedures` | P | M12,M5,M4 순서가 name(MTS+PRP+스킨부스터)·rationale 화살표 순서와 일치. |

## 수동 수집 표현 (원문 구간)

| Pointer | 구간 | 원문 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|
| `/combos/3/packages/0/products/0` | [0,6) | 리쥬란 힐러 | 제품명 | 공백 포함 제품명 |
| `/combos/3/packages/0/priceRange` | [0,6) | 15~25만 | 수량·범위 |  |
| `/combos/3/packages/0/expectedResult` | [0,12) | 피부 수분감·광채 향상 | 효과 |  |
| `/combos/3/packages/0/expectedResult` | [14,20) | 잔주름 완화 | 효과 |  |
| `/combos/3/packages/0/expectedResult` | [22,38) | 3~5회 반복 시 확연한 차이 | 회차·조건 |  |
| `/combos/3/packages/0/salesPitch` | [15,44) | 한 번만 해보시면 촉촉함이 다르다는 걸 느끼실 거예요 | 조건·추측 |  |
| `/combos/3/packages/0/salesPitch` | [46,58) | 월 1회가 이상적이에요 | 주기 |  |
| `/combos/3/packages/0/upsellHook` | [0,35) | 스킨부스터 전에 MTS로 채널 열고 하시면 흡수율이 훨씬 좋아요 | 순서·조건·비교 |  |
| `/combos/3/packages/0/upsellHook` | [37,50) | MTS+스킨부스터 패키지 | 시술 결합 |  |
| `/combos/3/packages/0/clinicalRationale` | [0,38) | PN/PDRN이 진피 섬유아세포를 자극하여 콜라겐·엘라스틴 합성 촉진 | 성분·층·기전 | PN/PDRN 영문 약어 |
| `/combos/3/packages/0/clinicalRationale` | [40,55) | 반복 시술로 진피 두께 증가 | 조건·효과 |  |
| `/combos/3/packages/0/riskBenefit` | [7,23) | 자잘한 구진 1~3일 내 소실 | 부작용·시간 |  |
| `/combos/3/packages/0/riskBenefit` | [25,37) | 가격 대비 만족도 높음 | 평가 |  |
| `/combos/3/packages/1/name` | [0,24) | MTS + PRP + 스킨부스터 (골든루틴) | 시술 결합+별칭 |  |
| `/combos/3/packages/1/products/0` | [0,18) | MTS + 자가 PRP + 리쥬란 | 제품 결합 | '자가' 수식 |
| `/combos/3/packages/1/priceRange` | [0,6) | 30~50만 | 수량·범위 |  |
| `/combos/3/packages/1/expectedResult` | [0,14) | 피부결·톤·탄력 종합 개선 | 효과 |  |
| `/combos/3/packages/1/expectedResult` | [16,26) | '아기 피부' 효과 | 인용·비유 |  |
| `/combos/3/packages/1/expectedResult` | [28,38) | 3~5회 1클 권장 | 회차·약어 | '1클' 뜻 원문 없음 |
| `/combos/3/packages/1/salesPitch` | [21,57) | MTS로 구멍 열고 PRP+스킨부스터 넣으면 흡수율이 수십 배예요 | 순서·조건·수치 |  |
| `/combos/3/packages/1/upsellHook` | [0,32) | 피부결에 색소·기미도 있으시면 레이저 토닝 추가가 가능해요 | 조건·가능성 |  |
| `/combos/3/packages/1/upsellHook` | [41,54) | 톤 균일 + 재생 시너지 | 효과 |  |
| `/combos/3/packages/1/clinicalRationale` | [0,56) | MTS(채널 생성) → PRP(성장인자 PDGF·TGF-β 전달) → 스킨부스터(PDRN·HA 전달) | 순서+기전 | TGF-β 그리스 문자 |
| `/combos/3/packages/1/clinicalRationale` | [59,69) | 경피 흡수율 극대화 | 효과 |  |
| `/combos/3/packages/1/clinicalRationale` | [71,106) | 세포 재생의 3가지 신호(성장인자+DNA회복+수분)를 동시 공급 | 수량·나열 |  |
| `/combos/3/packages/1/riskBenefit` | [7,26) | MTS 후 약간의 홍반·출혈은 정상 | 시간·부작용·정도 | '약간의' |
| `/combos/3/packages/1/riskBenefit` | [28,38) | 24시간 세안 제한 | 시간·관리 |  |
| `/combos/3/packages/1/riskBenefit` | [40,61) | 자가혈(PRP)이라 알레르기 위험 없음 | 인과·부정 |  |
| `/combos/3/packages/2/productTier` | [0,5) | 수입+국산 | 제품 등급 |  |
| `/combos/3/packages/2/products/0` | [0,27) | 피코레이저/프락셀 + MTS + PRP + 리쥬란 | 제품 결합+대안 |  |
| `/combos/3/packages/2/priceRange` | [0,6) | 50~90만 | 수량·범위 |  |
| `/combos/3/packages/2/expectedResult` | [0,18) | 색소+피부결+톤+탄력 종합 리뉴얼 | 효과 나열 |  |
| `/combos/3/packages/2/salesPitch` | [18,36) | 레이저로 묵은 각질·색소 정리하고 | 시술-효과 |  |
| `/combos/3/packages/2/upsellHook` | [0,36) | 탄력까지 원하시면 HIFU를 다음 회차에 추가하시는 분들이 많아요 | 조건·회차 |  |
| `/combos/3/packages/2/clinicalRationale` | [0,23) | 레이저(표피 색소 파괴+진피 미세 열손상) | 층·기전 |  |
| `/combos/3/packages/2/clinicalRationale` | [73,109) | 자극(레이저·MTS) + 재생(PRP·스킨부스터)의 이상적 밸런스 | 역할 분류 |  |
| `/combos/3/packages/2/riskBenefit` | [0,15) | 레이저 후 자외선 차단 필수 | 시간·관리 |  |
| `/combos/3/packages/2/riskBenefit` | [17,48) | 시술 순서 반드시 준수(레이저→MTS→PRP→스킨부스터) | 순서 제약 |  |
| `/combos/3/packages/2/riskBenefit` | [72,82) | 재생(PRP/SB) | 약어 | SB 정의 없음 |
| `/combos/3/packages/2/riskBenefit` | [87,96) | 과학적 근거 충분 | 근거 주장 | 출처 미기재 |
| `/combos/3/packages/2/clinicalRationale` | [0,71) | 레이저(표피 색소 파괴+진피 미세 열손상) → MTS(채널 추가 확보) → PRP(재생 촉진) → 스킨부스터(수분+DNA 회복) | 순서+기전 | 읽기 검토에서 전체 연쇄 추가 |
| `/combos/3/packages/1/upsellHook` | [34,54) | 같이 하시면 톤 균일 + 재생 시너지 | 조건·효과 |  |
| `/combos/3/problem` | [0,9) | 피부결/톤/항노화 | problem 값 / 나열 |  |
| `/combos/3/packages/2/riskBenefit` | [50,85) | 열 시술(레이저) + 채널(MTS) + 재생(PRP/SB) 조합 | 역할-시술 |  |

## 이 구획의 미결

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| I-PC-08 | B | `/combos/3/packages/1/expectedResult` | '1클' 약어 뜻 원문 없음 |
| I-PC-09 | B | `/combos/3/packages/2/riskBenefit` | 'SB' 약어 정의 원문 없음(스킨부스터로 보이는 것은 잠정) |

## 알려진 형태소 오분절 (K) — 11건

상세·원시 토큰은 `morphology.json#/known_missegmentations`.

| Pointer | 구간 | 표현 | 원시 토큰 |
|---|---|---|---|
| `/combos/3/packages/0/products/0` | [0,3) | 리쥬란 | 리쥬/NNP[0,2) 이/VCP[2,2) 란/ETM[2,3) |
| `/combos/3/packages/0/clinicalRationale` | [0,7) | PN/PDRN | PN/SL[0,2) //SP[2,3) PDRN/SL[3,7) |
| `/combos/3/packages/0/clinicalRationale` | [3,8) | PDRN이 | PDRN/SL[3,7) 이/MM[7,8) |
| `/combos/3/packages/1/products/0` | [15,18) | 리쥬란 | 리쥬/NNP[15,17) 이/VCP[17,17) 란/ETM[17,18) |
| `/combos/3/packages/1/expectedResult` | [33,35) | 1클 | 1/SN[33,34) 클/NNG[34,35) |
| `/combos/3/packages/1/salesPitch` | [66,70) | 골든루틴 | 골든/NNG[66,68) 루틴/NNG[68,70) |
| `/combos/3/packages/1/clinicalRationale` | [27,32) | TGF-β | TGF/SL[27,30) -/SO[30,31) β/SW[31,32) |
| `/combos/3/packages/1/clinicalRationale` | [90,95) | DNA회복 | DNA/SL[90,93) 회복/NNG[93,95) |
| `/combos/3/packages/2/products/0` | [24,27) | 리쥬란 | 리쥬/NNP[24,26) 이/VCP[26,26) 란/ETM[26,27) |
| `/combos/3/packages/2/clinicalRationale` | [19,22) | 열손상 | 열/NNG[19,20) 손상/NNG[20,22) |
| `/combos/3/packages/2/riskBenefit` | [75,81) | PRP/SB | PRP/SL[75,78) //SP[78,79) SB/SL[79,81) |
