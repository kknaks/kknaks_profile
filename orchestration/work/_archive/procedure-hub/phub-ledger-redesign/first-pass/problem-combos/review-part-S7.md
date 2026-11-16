# review-part-S7 — /combos/6 (P9 흉터) 전체

원본: `orchestration/work/phub-recommend/bronze/phub-ledger/problem-combos.json` sha256 `74453c724800975ef7f3fa8b81546fe69fa014bfbc7a8f7e60c75774c2cf2262`

## 원문 값

원본 컬럼명은 축약하지 않는다. 배열은 원본 순서. 원문 칸에는 원문만 둔다.

### `/combos/6` 묶음

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | object | 키 ['problem_id', 'problem', 'packages'] | `/combos/6` |
| `problem_id` | string | P9 | `/combos/6/problem_id` |
| `problem` | string | 흉터 | `/combos/6/problem` |
| `packages` | array | (길이 2) | `/combos/6/packages` |

### `/combos/6/packages/0` — P9-1 프락셔널 레이저

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/6/packages/0` |
| `id` | string | P9-1 | `/combos/6/packages/0/id` |
| `tier` | string | entry | `/combos/6/packages/0/tier` |
| `tierLabel` | string | 기본 | `/combos/6/packages/0/tierLabel` |
| `name` | string | 프락셔널 레이저 | `/combos/6/packages/0/name` |
| `procedures` | array | (길이 1) | `/combos/6/packages/0/procedures` |
| `procedures[0]` | string | M8 | `/combos/6/packages/0/procedures/0` |
| `productTier` | string | 국산/수입 | `/combos/6/packages/0/productTier` |
| `products` | array | (길이 1) | `/combos/6/packages/0/products` |
| `products[0]` | string | 프락셀 or CO2 프락셔널 | `/combos/6/packages/0/products/0` |
| `priceRange` | string | 15~30만/회 | `/combos/6/packages/0/priceRange` |
| `expectedResult` | string | 여드름 흉터·수술 흉터 점진적 개선. 5~10회 반복 필요 | `/combos/6/packages/0/expectedResult` |
| `salesPitch` | string | 흉터 치료의 기본은 프락셔널 레이저예요. 피부에 미세한 구멍을 뚫어서 새 피부가 올라오게 만드는 원리예요. | `/combos/6/packages/0/salesPitch` |
| `upsellHook` | string | 프락셔널만 하시면 재생이 느려요. PRP를 같이 하시면 새 피부가 훨씬 빨리 올라와요! | `/combos/6/packages/0/upsellHook` |
| `clinicalRationale` | string | 프락셔널 레이저의 미세열손상 → 상처 치유 반응 → 콜라겐 리모델링 → 흉터 조직 대체. 여러 회 반복으로 점진적 개선 | `/combos/6/packages/0/clinicalRationale` |
| `riskBenefit` | string | 다운타임 3~7일. PIH 주의. 에너지·밀도 조절로 안전성 확보. 흉터 치료의 표준 치료법 | `/combos/6/packages/0/riskBenefit` |

### `/combos/6/packages/1` — P9-2 프락셔널 + 니들RF + PRP

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/6/packages/1` |
| `id` | string | P9-2 | `/combos/6/packages/1/id` |
| `tier` | string | recommended | `/combos/6/packages/1/tier` |
| `tierLabel` | string | 표준 | `/combos/6/packages/1/tierLabel` |
| `name` | string | 프락셔널 + 니들RF + PRP | `/combos/6/packages/1/name` |
| `procedures` | array | (길이 3) | `/combos/6/packages/1/procedures` |
| `procedures[0]` | string | M8 | `/combos/6/packages/1/procedures/0` |
| `procedures[1]` | string | M11 | `/combos/6/packages/1/procedures/1` |
| `procedures[2]` | string | M5 | `/combos/6/packages/1/procedures/2` |
| `productTier` | string | 혼합 | `/combos/6/packages/1/productTier` |
| `products` | array | (길이 1) | `/combos/6/packages/1/products` |
| `products[0]` | string | 프락셀 + 포텐자/인트라셀 + PRP | `/combos/6/packages/1/products/0` |
| `priceRange` | string | 50~80만/회 | `/combos/6/packages/1/priceRange` |
| `expectedResult` | string | 흉터 확실한 개선 + 재생 가속. 표면(레이저) + 심부(니들RF) 이중 리모델링 | `/combos/6/packages/1/expectedResult` |
| `salesPitch` | string | 흉터 치료 최강 조합이에요! 레이저가 표면, 니들RF가 깊은 곳을 동시에 리모델링하고, PRP가 재생을 가속시켜요. 3회면 눈에 보이는 차이! | `/combos/6/packages/1/salesPitch` |
| `upsellHook` | string | 여기에 스킨부스터 추가하시면 회복이 더 빨라지고 PIH도 줄어들어요. | `/combos/6/packages/1/upsellHook` |
| `clinicalRationale` | string | 프락셔널(표피~얕은 진피 리모델링) + 니들RF(깊은 진피 열응고 → 흉터 기저부 콜라겐 재배열) + PRP(성장인자가 양쪽 시술의 재생 가속). 표면·심부를 함께 자극해 단일 시술보다 추가적 개선을 기대 | `/combos/6/packages/1/clinicalRationale` |
| `riskBenefit` | string | 열 시술 2개로 다운타임 5~7일. 그러나 각 시술의 에너지를 개별 시술 시보다 낮춰도 시너지로 동등 이상의 효과. PRP가 회복 기간 단축 | `/combos/6/packages/1/riskBenefit` |

## 잠정 관찰 (원문과 분리)

| Pointer | 상태 | 관찰 |
|---|---|---|
| `/combos/6` | P | P9 묶음은 packages 2개(entry·recommended)뿐 — premium 없음. |
| `/combos/6/packages/0/products/0` | P | "프락셀 or CO2 프락셔널" — 하나는 제품명(프락셀), 하나는 방식명(CO2 프락셔널)이 대안으로 나란히. |
| `/combos/6/packages/1/riskBenefit` | P | "그러나 ... 낮춰도 시너지로 동등 이상의 효과" — P3-4·P2-4와 유사한 '강도 낮춰도 시너지' 서술 반복. |
| `/combos/6/packages/1/clinicalRationale` | P | "단일 시술보다 추가적 개선을 기대" — 유보 어조(기대). salesPitch "흉터 치료 최강 조합"과 어조 대비. |

## 수동 수집 표현 (원문 구간)

| Pointer | 구간 | 원문 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|
| `/combos/6/packages/0/productTier` | [0,5) | 국산/수입 | 제품 등급 대안 |  |
| `/combos/6/packages/0/products/0` | [0,15) | 프락셀 or CO2 프락셔널 | 제품/방식 대안 | CO2 영숫자 |
| `/combos/6/packages/0/priceRange` | [0,8) | 15~30만/회 | 수량·범위·회당 |  |
| `/combos/6/packages/0/expectedResult` | [0,19) | 여드름 흉터·수술 흉터 점진적 개선 | 대상·정도 |  |
| `/combos/6/packages/0/expectedResult` | [21,32) | 5~10회 반복 필요 | 회차·범위 |  |
| `/combos/6/packages/0/salesPitch` | [23,56) | 피부에 미세한 구멍을 뚫어서 새 피부가 올라오게 만드는 원리 | 기전 | '미세한' 수치화 금지 |
| `/combos/6/packages/0/upsellHook` | [0,17) | 프락셔널만 하시면 재생이 느려요 | 조건 |  |
| `/combos/6/packages/0/upsellHook` | [19,47) | PRP를 같이 하시면 새 피부가 훨씬 빨리 올라와요 | 조건·비교 |  |
| `/combos/6/packages/0/clinicalRationale` | [0,48) | 프락셔널 레이저의 미세열손상 → 상처 치유 반응 → 콜라겐 리모델링 → 흉터 조직 대체 | 기전 인과 연쇄 |  |
| `/combos/6/packages/0/clinicalRationale` | [50,66) | 여러 회 반복으로 점진적 개선 | 회차 | 회수 불특정 |
| `/combos/6/packages/0/riskBenefit` | [0,9) | 다운타임 3~7일 | 시간·범위 |  |
| `/combos/6/packages/0/riskBenefit` | [11,17) | PIH 주의 | 부작용 |  |
| `/combos/6/packages/0/riskBenefit` | [19,36) | 에너지·밀도 조절로 안전성 확보 | 조건 |  |
| `/combos/6/packages/0/riskBenefit` | [38,51) | 흉터 치료의 표준 치료법 | 평가 |  |
| `/combos/6/packages/1/productTier` | [0,2) | 혼합 | 제품 등급 |  |
| `/combos/6/packages/1/products/0` | [0,20) | 프락셀 + 포텐자/인트라셀 + PRP | 제품 결합+대안 |  |
| `/combos/6/packages/1/priceRange` | [0,8) | 50~80만/회 | 수량·범위·회당 |  |
| `/combos/6/packages/1/expectedResult` | [19,45) | 표면(레이저) + 심부(니들RF) 이중 리모델링 | 층-시술 대응 |  |
| `/combos/6/packages/1/salesPitch` | [0,11) | 흉터 치료 최강 조합 | 최상급 |  |
| `/combos/6/packages/1/salesPitch` | [16,47) | 레이저가 표면, 니들RF가 깊은 곳을 동시에 리모델링하고 | 층·동시성 |  |
| `/combos/6/packages/1/salesPitch` | [65,78) | 3회면 눈에 보이는 차이 | 회차·조건 |  |
| `/combos/6/packages/1/upsellHook` | [4,37) | 스킨부스터 추가하시면 회복이 더 빨라지고 PIH도 줄어들어요 | 조건·인과 |  |
| `/combos/6/packages/1/clinicalRationale` | [0,19) | 프락셔널(표피~얕은 진피 리모델링) | 층 범위 | '~' 층 범위 |
| `/combos/6/packages/1/clinicalRationale` | [22,54) | 니들RF(깊은 진피 열응고 → 흉터 기저부 콜라겐 재배열) | 층·기전 |  |
| `/combos/6/packages/1/clinicalRationale` | [57,80) | PRP(성장인자가 양쪽 시술의 재생 가속) | 기전·지시 |  |
| `/combos/6/packages/1/clinicalRationale` | [96,114) | 단일 시술보다 추가적 개선을 기대 | 비교·가능성 |  |
| `/combos/6/packages/1/riskBenefit` | [0,18) | 열 시술 2개로 다운타임 5~7일 | 수량·시간 |  |
| `/combos/6/packages/1/riskBenefit` | [24,63) | 각 시술의 에너지를 개별 시술 시보다 낮춰도 시너지로 동등 이상의 효과 | 양보·비교 |  |
| `/combos/6/packages/1/riskBenefit` | [65,78) | PRP가 회복 기간 단축 | 인과 |  |

## 이 구획의 미결

이 구획에서 새로 연 미결 없음(공통 미결은 issues.md).

## 알려진 형태소 오분절 (K) — 10건

상세·원시 토큰은 `morphology.json#/known_missegmentations`.

| Pointer | 구간 | 표현 | 원시 토큰 |
|---|---|---|---|
| `/combos/6/packages/0/products/0` | [7,10) | CO2 | CO/SL[7,9) 2/SN[9,10) |
| `/combos/6/packages/0/clinicalRationale` | [10,15) | 미세열손상 | 미세/NNG[10,12) 열/NNG[12,13) 손상/NNG[13,15) |
| `/combos/6/packages/0/clinicalRationale` | [12,15) | 열손상 | 열/NNG[12,13) 손상/NNG[13,15) |
| `/combos/6/packages/1/name` | [7,11) | 니들RF | 니들/NNP[7,9) RF/SL[9,11) |
| `/combos/6/packages/1/expectedResult` | [32,36) | 니들RF | 니들/NNP[32,34) RF/SL[34,36) |
| `/combos/6/packages/1/expectedResult` | [29,31) | 심부 | 심/XR[29,30) 부/NNG[30,31) |
| `/combos/6/packages/1/expectedResult` | [38,40) | 이중 | 이/MM[38,39) 중/NNB[39,40) |
| `/combos/6/packages/1/salesPitch` | [25,29) | 니들RF | 니들/NNP[25,27) RF/SL[27,29) |
| `/combos/6/packages/1/clinicalRationale` | [22,26) | 니들RF | 니들/NNP[22,24) RF/SL[24,26) |
| `/combos/6/packages/1/clinicalRationale` | [33,36) | 열응고 | 열/NNG[33,34) 응고/NNG[34,36) |
