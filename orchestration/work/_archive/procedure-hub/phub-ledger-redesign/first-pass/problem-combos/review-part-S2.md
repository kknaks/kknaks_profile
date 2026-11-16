# review-part-S2 — /combos/1 (P2 주름) 전체

원본: `orchestration/work/phub-recommend/bronze/phub-ledger/problem-combos.json` sha256 `74453c724800975ef7f3fa8b81546fe69fa014bfbc7a8f7e60c75774c2cf2262`

## 원문 값

원본 컬럼명은 축약하지 않는다. 배열은 원본 순서. 원문 칸에는 원문만 둔다.

### `/combos/1` 묶음

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | object | 키 ['problem_id', 'problem', 'packages'] | `/combos/1` |
| `problem_id` | string | P2 | `/combos/1/problem_id` |
| `problem` | string | 주름 | `/combos/1/problem` |
| `packages` | array | (길이 4) | `/combos/1/packages` |

### `/combos/1/packages/0` — P2-1 보톡스 기본

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/1/packages/0` |
| `id` | string | P2-1 | `/combos/1/packages/0/id` |
| `tier` | string | entry | `/combos/1/packages/0/tier` |
| `tierLabel` | string | 기본 | `/combos/1/packages/0/tierLabel` |
| `name` | string | 보톡스 기본 | `/combos/1/packages/0/name` |
| `procedures` | array | (길이 1) | `/combos/1/packages/0/procedures` |
| `procedures[0]` | string | M1 | `/combos/1/packages/0/procedures/0` |
| `productTier` | string | 국산 | `/combos/1/packages/0/productTier` |
| `products` | array | (길이 1) | `/combos/1/packages/0/products` |
| `products[0]` | string | 나보타 or 보툴렉스 | `/combos/1/packages/0/products/0` |
| `priceRange` | string | 5~10만 | `/combos/1/packages/0/priceRange` |
| `expectedResult` | string | 이마·미간·눈가 동적 주름 개선. 3~7일 후 효과 시작 | `/combos/1/packages/0/expectedResult` |
| `salesPitch` | string | 주름은 보톡스로 시작하는 게 정석이에요. 가볍게 한번 해보시면 왜 다들 하는지 아실 거예요. | `/combos/1/packages/0/salesPitch` |
| `upsellHook` | string | 보톡스로 주름 펴시고, 이미 깊게 파인 주름은 필러로 채워야 완벽해요! | `/combos/1/packages/0/upsellHook` |
| `clinicalRationale` | string | 동적 주름(표정 지을 때 생기는 주름)의 1차 치료. 근이완으로 추가 진행 방지 효과 | `/combos/1/packages/0/clinicalRationale` |
| `riskBenefit` | string | 최소 위험. 3~6개월 유지. 반복 시 주름 예방 효과 | `/combos/1/packages/0/riskBenefit` |

### `/combos/1/packages/1` — P2-2 보톡스 + 필러 + 스킨부스터

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/1/packages/1` |
| `id` | string | P2-2 | `/combos/1/packages/1/id` |
| `tier` | string | recommended | `/combos/1/packages/1/tier` |
| `tierLabel` | string | 표준 | `/combos/1/packages/1/tierLabel` |
| `name` | string | 보톡스 + 필러 + 스킨부스터 | `/combos/1/packages/1/name` |
| `procedures` | array | (길이 3) | `/combos/1/packages/1/procedures` |
| `procedures[0]` | string | M1 | `/combos/1/packages/1/procedures/0` |
| `procedures[1]` | string | M2 | `/combos/1/packages/1/procedures/1` |
| `procedures[2]` | string | M4 | `/combos/1/packages/1/procedures/2` |
| `productTier` | string | 국산+수입 혼합 | `/combos/1/packages/1/productTier` |
| `products` | array | (길이 1) | `/combos/1/packages/1/products` |
| `products[0]` | string | 나보타 + 쥬비덤/이브아르 + 리쥬란 | `/combos/1/packages/1/products/0` |
| `priceRange` | string | 40~70만 | `/combos/1/packages/1/priceRange` |
| `expectedResult` | string | 동적주름(보톡스) + 정적주름(필러) + 잔주름·피부결(스킨부스터) 완벽 해결 | `/combos/1/packages/1/expectedResult` |
| `salesPitch` | string | 주름 3총사예요! 보톡스로 펴고, 필러로 채우고, 스킨부스터로 피부결까지. 이 조합이 만족도 1위입니다. | `/combos/1/packages/1/salesPitch` |
| `upsellHook` | string | 탄력까지 신경 쓰시면 HIFU 추가하시는 분들이 많아요. 주름+탄력을 한 번에! | `/combos/1/packages/1/upsellHook` |
| `clinicalRationale` | string | 동적주름(M1)+정적주름(M2)+미세주름·피부결(M4) → 주름의 3가지 유형을 각각 다른 메커니즘으로 타겟. 스킨부스터 PN(폴리뉴클레오타이드)이 보톡스·필러 시술 부위 재생 촉진 | `/combos/1/packages/1/clinicalRationale` |
| `riskBenefit` | string | 위험 낮음. 3가지 메커니즘이 겹치지 않아 부작용 최소. 만족도 매우 높은 조합 | `/combos/1/packages/1/riskBenefit` |

### `/combos/1/packages/2` — P2-3 보톡스 + 필러 + HIFU + 스킨부스터

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/1/packages/2` |
| `id` | string | P2-3 | `/combos/1/packages/2/id` |
| `tier` | string | premium | `/combos/1/packages/2/tier` |
| `tierLabel` | string | 확장 | `/combos/1/packages/2/tierLabel` |
| `name` | string | 보톡스 + 필러 + HIFU + 스킨부스터 | `/combos/1/packages/2/name` |
| `procedures` | array | (길이 4) | `/combos/1/packages/2/procedures` |
| `procedures[0]` | string | M9 | `/combos/1/packages/2/procedures/0` |
| `procedures[1]` | string | M1 | `/combos/1/packages/2/procedures/1` |
| `procedures[2]` | string | M2 | `/combos/1/packages/2/procedures/2` |
| `procedures[3]` | string | M4 | `/combos/1/packages/2/procedures/3` |
| `productTier` | string | 수입 | `/combos/1/packages/2/productTier` |
| `products` | array | (길이 1) | `/combos/1/packages/2/products` |
| `products[0]` | string | 보톡스(엘러간) + 쥬비덤 + 울쎄라 + 리쥬란 | `/combos/1/packages/2/products/0` |
| `priceRange` | string | 100~180만 | `/combos/1/packages/2/priceRange` |
| `expectedResult` | string | 주름 완벽 해결 + 피부 탄력 향상. '5살 어려 보이는' 수준의 변화 | `/combos/1/packages/2/expectedResult` |
| `salesPitch` | string | 원장님이 직접 추천하는 주름 프리미엄이에요. 울쎄라로 탄력까지 잡으면 주름이 다시 생기기 어려워져요. | `/combos/1/packages/2/salesPitch` |
| `upsellHook` | string | 여기서 더 가시면 실리프팅으로 구조적 리프팅까지. VIP 고객분들이 많이 선택하세요. | `/combos/1/packages/2/upsellHook` |
| `clinicalRationale` | string | HIFU(콜라겐 수축·리모델링) → 보톡스(근이완) → 필러(볼륨) → 스킨부스터(재생). 주름의 원인(근육+볼륨손실+콜라겐감소+피부노화)을 전부 타겟 | `/combos/1/packages/2/clinicalRationale` |
| `riskBenefit` | string | 열 시술 후 주입 시술 순서 준수 필수. 울쎄라의 SMAS 열응고가 장기적 콜라겐 리모델링을 유도하여 주름 재발 방지 | `/combos/1/packages/2/riskBenefit` |

### `/combos/1/packages/3` — P2-4 실리프팅 + HIFU + 보톡스 + 필러 + 스킨부스터

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/1/packages/3` |
| `id` | string | P2-4 | `/combos/1/packages/3/id` |
| `tier` | string | vip | `/combos/1/packages/3/tier` |
| `tierLabel` | string | 종합 | `/combos/1/packages/3/tierLabel` |
| `name` | string | 실리프팅 + HIFU + 보톡스 + 필러 + 스킨부스터 | `/combos/1/packages/3/name` |
| `procedures` | array | (길이 5) | `/combos/1/packages/3/procedures` |
| `procedures[0]` | string | M7 | `/combos/1/packages/3/procedures/0` |
| `procedures[1]` | string | M9 | `/combos/1/packages/3/procedures/1` |
| `procedures[2]` | string | M1 | `/combos/1/packages/3/procedures/2` |
| `procedures[3]` | string | M2 | `/combos/1/packages/3/procedures/3` |
| `procedures[4]` | string | M4 | `/combos/1/packages/3/procedures/4` |
| `productTier` | string | 수입 프리미엄 | `/combos/1/packages/3/productTier` |
| `products` | array | (길이 1) | `/combos/1/packages/3/products` |
| `products[0]` | string | 실루엣소프트 + 울쎄라 + 보톡스(엘러간) + 쥬비덤 + 리쥬란 | `/combos/1/packages/3/products/0` |
| `priceRange` | string | 200~350만 | `/combos/1/packages/3/priceRange` |
| `expectedResult` | string | 구조적 리프팅 + 타이트닝 + 주름 제거 + 볼륨 복원 + 피부 재생. 수술 없이 최대 효과 | `/combos/1/packages/3/expectedResult` |
| `salesPitch` | string | 비수술로 가능한 최고의 주름·리프팅 풀패키지예요. VIP 고객분들이 6개월~1년에 한 번 받으시는 프로그램이에요. | `/combos/1/packages/3/salesPitch` |
| `upsellHook` | string | 이 패키지를 연간 프로그램으로 가입하시면 매번 할인 + 스킨부스터 유지 시술 무료예요. | `/combos/1/packages/3/upsellHook` |
| `clinicalRationale` | string | 실(물리적 거상) + HIFU(열 응고·콜라겐 수축) + 보톡스(근이완) + 필러(볼륨) + 스킨부스터(재생) = 5가지 메커니즘으로 노화의 모든 축을 타겟. 비수술 최대 효과 | `/combos/1/packages/3/clinicalRationale` |
| `riskBenefit` | string | 시술 순서·간격 엄격 준수. 실리프팅 부위 열 시술 주의. 그러나 각 시술이 서로 보완하여 개별 시술보다 적은 양·강도로도 더 좋은 결과 | `/combos/1/packages/3/riskBenefit` |

## 잠정 관찰 (원문과 분리)

| Pointer | 상태 | 관찰 |
|---|---|---|
| `/combos/1/packages/3/tier` | P | P2에만 4번째 tier "vip"(tierLabel "종합")가 있음. P1은 entry/recommended/premium 3단. |
| `/combos/1/packages/2/procedures` | P | procedures 순서 M9,M1,M2,M4 가 name 순서(보톡스+필러+HIFU+스킨부스터)와 다르고 clinicalRationale의 화살표 순서(HIFU→보톡스→필러→스킨부스터)와 일치. 배열 순서가 시술 순서를 뜻하는지는 원문에 정의 없음(F). |
| `/combos/1/packages/1/products/0` | P | 이 항목은 대안을 "/"로(쥬비덤/이브아르), P1-2는 "or"로 표기. 같은 원장 안 대안 기호 불일치. |
| `/combos/1/packages/1/clinicalRationale` | P | M코드를 문장 안 괄호로 직접 참조(동적주름(M1)). procedures 값과 텍스트 사이 대응 단서. |
| `/combos/1/packages/2/riskBenefit` | P | riskBenefit 안에 시술 순서 제약("열 시술 후 주입 시술 순서 준수 필수")이 있음 — 다른 필드가 아닌 위험 칸에 순서 규칙이 섞임. |
| `/combos/1/packages/2/expectedResult` | P | "'5살 어려 보이는' 수준" — 따옴표 인용된 비유적 수치. 수치로 해석하지 않음. |
| `/combos/1/packages/3/salesPitch` | P | "6개월~1년에 한 번" 주기 표현이 salesPitch에 있음. |
| `/combos/1/packages/3/riskBenefit` | P | "그러나"로 위험 진술과 이점 진술이 대조됨. 위험/이점 분리 시 접속 문맥 보존 필요. |
| `/combos/1/packages/0/riskBenefit` | P | "3~6개월 유지" 유지 기간이 riskBenefit 칸에 있음. |

## 수동 수집 표현 (원문 구간)

| Pointer | 구간 | 원문 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|
| `/combos/1/packages/0/priceRange` | [0,5) | 5~10만 | 수량·범위 |  |
| `/combos/1/packages/0/expectedResult` | [0,17) | 이마·미간·눈가 동적 주름 개선 | 부위+효과 |  |
| `/combos/1/packages/0/expectedResult` | [19,31) | 3~7일 후 효과 시작 | 시간·범위 |  |
| `/combos/1/packages/0/salesPitch` | [0,21) | 주름은 보톡스로 시작하는 게 정석이에요 | 평가 |  |
| `/combos/1/packages/0/upsellHook` | [13,38) | 이미 깊게 파인 주름은 필러로 채워야 완벽해요 | 조건·정도 | '깊게' 정도 부사, 수치화 금지 |
| `/combos/1/packages/0/clinicalRationale` | [0,28) | 동적 주름(표정 지을 때 생기는 주름)의 1차 치료 | 정의+순서 | 괄호가 용어 풀이 |
| `/combos/1/packages/0/clinicalRationale` | [30,47) | 근이완으로 추가 진행 방지 효과 | 인과 |  |
| `/combos/1/packages/0/riskBenefit` | [7,15) | 3~6개월 유지 | 시간·범위 |  |
| `/combos/1/packages/0/riskBenefit` | [17,30) | 반복 시 주름 예방 효과 | 조건 |  |
| `/combos/1/packages/1/products/0` | [0,20) | 나보타 + 쥬비덤/이브아르 + 리쥬란 | 제품 결합+대안 | / 대안 |
| `/combos/1/packages/1/priceRange` | [0,6) | 40~70만 | 수량·범위 |  |
| `/combos/1/packages/1/expectedResult` | [23,37) | 잔주름·피부결(스킨부스터) | 문제-시술 대응 |  |
| `/combos/1/packages/1/expectedResult` | [38,43) | 완벽 해결 | 정도 |  |
| `/combos/1/packages/1/salesPitch` | [42,57) | 이 조합이 만족도 1위입니다 | 순위 주장 | 근거 미기재 |
| `/combos/1/packages/1/upsellHook` | [0,30) | 탄력까지 신경 쓰시면 HIFU 추가하시는 분들이 많아요 | 조건·업셀 |  |
| `/combos/1/packages/1/clinicalRationale` | [0,30) | 동적주름(M1)+정적주름(M2)+미세주름·피부결(M4) | 문제-코드 대응 | 텍스트 속 M코드 |
| `/combos/1/packages/1/clinicalRationale` | [33,60) | 주름의 3가지 유형을 각각 다른 메커니즘으로 타겟 | 수량 |  |
| `/combos/1/packages/1/clinicalRationale` | [83,101) | 보톡스·필러 시술 부위 재생 촉진 | 부위(지시적) |  |
| `/combos/1/packages/1/riskBenefit` | [7,30) | 3가지 메커니즘이 겹치지 않아 부작용 최소 | 부정·인과 | '않아' 부정 |
| `/combos/1/packages/1/riskBenefit` | [32,44) | 만족도 매우 높은 조합 | 정도 |  |
| `/combos/1/packages/2/products/0` | [0,26) | 보톡스(엘러간) + 쥬비덤 + 울쎄라 + 리쥬란 | 제품 결합 |  |
| `/combos/1/packages/2/priceRange` | [0,8) | 100~180만 | 수량·범위 |  |
| `/combos/1/packages/2/expectedResult` | [21,39) | '5살 어려 보이는' 수준의 변화 | 인용·비유 |  |
| `/combos/1/packages/2/salesPitch` | [25,55) | 울쎄라로 탄력까지 잡으면 주름이 다시 생기기 어려워져요 | 조건·가능성 |  |
| `/combos/1/packages/2/upsellHook` | [10,26) | 실리프팅으로 구조적 리프팅까지 | 업셀 |  |
| `/combos/1/packages/2/clinicalRationale` | [0,49) | HIFU(콜라겐 수축·리모델링) → 보톡스(근이완) → 필러(볼륨) → 스킨부스터(재생) | 순서+기전 | → 순서 |
| `/combos/1/packages/2/clinicalRationale` | [51,84) | 주름의 원인(근육+볼륨손실+콜라겐감소+피부노화)을 전부 타겟 | 원인 나열 | + 가 원인 나열 |
| `/combos/1/packages/2/riskBenefit` | [0,21) | 열 시술 후 주입 시술 순서 준수 필수 | 순서 제약 |  |
| `/combos/1/packages/2/riskBenefit` | [23,65) | 울쎄라의 SMAS 열응고가 장기적 콜라겐 리모델링을 유도하여 주름 재발 방지 | 기전·인과 | SMAS 영문 약어 |
| `/combos/1/packages/3/productTier` | [0,7) | 수입 프리미엄 | 제품 등급 |  |
| `/combos/1/packages/3/products/0` | [0,35) | 실루엣소프트 + 울쎄라 + 보톡스(엘러간) + 쥬비덤 + 리쥬란 | 제품 결합 |  |
| `/combos/1/packages/3/priceRange` | [0,8) | 200~350만 | 수량·범위 |  |
| `/combos/1/packages/3/expectedResult` | [40,51) | 수술 없이 최대 효과 | 부정·최상급 | '없이' |
| `/combos/1/packages/3/salesPitch` | [0,24) | 비수술로 가능한 최고의 주름·리프팅 풀패키지 | 가능성·최상급 |  |
| `/combos/1/packages/3/salesPitch` | [38,49) | 6개월~1년에 한 번 | 주기·범위 |  |
| `/combos/1/packages/3/upsellHook` | [7,45) | 연간 프로그램으로 가입하시면 매번 할인 + 스킨부스터 유지 시술 무료 | 조건·가격 |  |
| `/combos/1/packages/3/clinicalRationale` | [0,29) | 실(물리적 거상) + HIFU(열 응고·콜라겐 수축) | 시술-기전 |  |
| `/combos/1/packages/3/clinicalRationale` | [64,87) | 5가지 메커니즘으로 노화의 모든 축을 타겟 | 수량·범위 |  |
| `/combos/1/packages/3/riskBenefit` | [0,14) | 시술 순서·간격 엄격 준수 | 순서·간격 제약 | 간격 수치 미기재 |
| `/combos/1/packages/3/riskBenefit` | [16,31) | 실리프팅 부위 열 시술 주의 | 부위+주의 |  |
| `/combos/1/packages/3/riskBenefit` | [51,76) | 개별 시술보다 적은 양·강도로도 더 좋은 결과 | 비교 | 양·강도 수치 미기재 |
| `/combos/1/packages/0/salesPitch` | [23,50) | 가볍게 한번 해보시면 왜 다들 하는지 아실 거예요 | 조건·추측 |  |
| `/combos/1/packages/2/upsellHook` | [0,9) | 여기서 더 가시면 | 조건·업셀 |  |
| `/combos/1/packages/1/salesPitch` | [0,6) | 주름 3총사 | 수량 |  |
| `/combos/1/packages/0/products/0` | [0,11) | 나보타 or 보툴렉스 | 제품 대안 |  |
| `/combos/1/packages/1/expectedResult` | [0,37) | 동적주름(보톡스) + 정적주름(필러) + 잔주름·피부결(스킨부스터) | 문제-시술 대응 |  |
| `/combos/1/packages/1/clinicalRationale` | [68,81) | PN(폴리뉴클레오타이드) | 약어 풀이 |  |
| `/combos/1/packages/3/clinicalRationale` | [32,61) | 보톡스(근이완) + 필러(볼륨) + 스킨부스터(재생) | 시술-기전 |  |

## 이 구획의 미결

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| I-PC-04 | F | `/combos/1/packages/2/procedures` | procedures 배열 순서와 name 순서 불일치, rationale 화살표 순서와 일치 — 배열 순서 의미 미정의 |
| I-PC-05 | B | `/combos/1/packages/3/riskBenefit` | '시술 순서·간격' 구체 간격 원문 없음 |

## 알려진 형태소 오분절 (K) — 9건

상세·원시 토큰은 `morphology.json#/known_missegmentations`.

| Pointer | 구간 | 표현 | 원시 토큰 |
|---|---|---|---|
| `/combos/1/packages/1/products/0` | [17,20) | 리쥬란 | 리쥬/NNP[17,19) 이/VCP[19,19) 란/ETM[19,20) |
| `/combos/1/packages/1/clinicalRationale` | [0,4) | 동적주름 | 동적/NNG[0,2) 주름/NNG[2,4) |
| `/combos/1/packages/2/products/0` | [23,26) | 리쥬란 | 리쥬/NNP[23,25) 이/VCP[25,25) 란/ETM[25,26) |
| `/combos/1/packages/2/upsellHook` | [10,14) | 실리프팅 | 실/NNG[10,11) 리프팅/NNG[11,14) |
| `/combos/1/packages/2/clinicalRationale` | [66,71) | 콜라겐감소 | 콜라겐/NNP[66,69) 감소/NNG[69,71) |
| `/combos/1/packages/2/riskBenefit` | [33,36) | 열응고 | 열/NNG[33,34) 응고/NNG[34,36) |
| `/combos/1/packages/3/products/0` | [32,35) | 리쥬란 | 리쥬/NNP[32,34) 이/VCP[34,34) 란/ETM[34,35) |
| `/combos/1/packages/3/salesPitch` | [20,24) | 풀패키지 | 풀/NNG[20,21) 패키지/NNG[21,24) |
| `/combos/1/packages/3/riskBenefit` | [16,20) | 실리프팅 | 실/NNG[16,17) 리프팅/NNG[17,20) |
