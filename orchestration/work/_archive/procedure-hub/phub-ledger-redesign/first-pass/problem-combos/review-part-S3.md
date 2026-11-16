# review-part-S3 — /combos/2 (P3 처짐/탄력) 전체

원본: `orchestration/work/phub-recommend/bronze/phub-ledger/problem-combos.json` sha256 `74453c724800975ef7f3fa8b81546fe69fa014bfbc7a8f7e60c75774c2cf2262`

## 원문 값

원본 컬럼명은 축약하지 않는다. 배열은 원본 순서. 원문 칸에는 원문만 둔다.

### `/combos/2` 묶음

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | object | 키 ['problem_id', 'problem', 'packages'] | `/combos/2` |
| `problem_id` | string | P3 | `/combos/2/problem_id` |
| `problem` | string | 처짐/탄력 | `/combos/2/problem` |
| `packages` | array | (길이 4) | `/combos/2/packages` |

### `/combos/2/packages/0` — P3-1 국산 HIFU 리프팅

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/2/packages/0` |
| `id` | string | P3-1 | `/combos/2/packages/0/id` |
| `tier` | string | entry | `/combos/2/packages/0/tier` |
| `tierLabel` | string | 기본 | `/combos/2/packages/0/tierLabel` |
| `name` | string | 국산 HIFU 리프팅 | `/combos/2/packages/0/name` |
| `procedures` | array | (길이 1) | `/combos/2/packages/0/procedures` |
| `procedures[0]` | string | M9 | `/combos/2/packages/0/procedures/0` |
| `productTier` | string | 국산 | `/combos/2/packages/0/productTier` |
| `products` | array | (길이 1) | `/combos/2/packages/0/products` |
| `products[0]` | string | 슈링크유니버스 or 더블로골드 | `/combos/2/packages/0/products/0` |
| `priceRange` | string | 15~30만 | `/combos/2/packages/0/priceRange` |
| `expectedResult` | string | 턱선 정리, 가벼운 리프팅. 시술 다음날부터 일상 가능 | `/combos/2/packages/0/expectedResult` |
| `salesPitch` | string | 리프팅 입문으로 슈링크가 딱이에요. 가격도 합리적이고 다운타임이 거의 없어서 부담 없이 시작하실 수 있어요. | `/combos/2/packages/0/salesPitch` |
| `upsellHook` | string | 슈링크도 좋지만, 울쎄라가 깊은 층까지 닿아서 효과가 더 확실해요. 보톡스도 같이 하시면 유지력이 2배! | `/combos/2/packages/0/upsellHook` |
| `clinicalRationale` | string | 국산 HIFU(슈링크/더블로)는 울쎄라 대비 에너지가 낮지만 가격 대비 효과 우수. 리프팅 입문 환자에게 적합 | `/combos/2/packages/0/clinicalRationale` |
| `riskBenefit` | string | 위험 매우 낮음. 효과는 울쎄라 대비 약하지만 반복 시술로 보완 가능 | `/combos/2/packages/0/riskBenefit` |

### `/combos/2/packages/1` — P3-2 울쎄라 + 보톡스

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/2/packages/1` |
| `id` | string | P3-2 | `/combos/2/packages/1/id` |
| `tier` | string | recommended | `/combos/2/packages/1/tier` |
| `tierLabel` | string | 표준 | `/combos/2/packages/1/tierLabel` |
| `name` | string | 울쎄라 + 보톡스 | `/combos/2/packages/1/name` |
| `procedures` | array | (길이 2) | `/combos/2/packages/1/procedures` |
| `procedures[0]` | string | M9 | `/combos/2/packages/1/procedures/0` |
| `procedures[1]` | string | M1 | `/combos/2/packages/1/procedures/1` |
| `productTier` | string | 수입 | `/combos/2/packages/1/productTier` |
| `products` | array | (길이 1) | `/combos/2/packages/1/products` |
| `products[0]` | string | 울쎄라 + 보톡스(엘러간) or 나보타 | `/combos/2/packages/1/products/0` |
| `priceRange` | string | 60~120만 | `/combos/2/packages/1/priceRange` |
| `expectedResult` | string | 확실한 리프팅 + 장기 유지. SMAS층 콜라겐 수축으로 자연스러운 턱선 | `/combos/2/packages/1/expectedResult` |
| `salesPitch` | string | 리프팅하면 울쎄라+보톡스죠! 울쎄라로 당기고 보톡스로 잡아두니까 효과가 6개월 이상 가요. 가장 인기 있는 리프팅 조합이에요. | `/combos/2/packages/1/salesPitch` |
| `upsellHook` | string | 볼이 꺼져 보이시면 필러 1cc만 추가해도 확 달라져요. 탄력 후 볼륨까지! | `/combos/2/packages/1/upsellHook` |
| `clinicalRationale` | string | HIFU(SMAS 열응고) + 보톡스(광경근 이완) = 올리는 힘 + 당기는 힘 제거. 가장 검증된 비수술 리프팅 조합 | `/combos/2/packages/1/clinicalRationale` |
| `riskBenefit` | string | 울쎄라 열응고 후 보톡스 주입 순서 준수. 위험 낮고 효과 확실 | `/combos/2/packages/1/riskBenefit` |

### `/combos/2/packages/2` — P3-3 울쎄라 + 보톡스 + 필러 + 스킨부스터

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/2/packages/2` |
| `id` | string | P3-3 | `/combos/2/packages/2/id` |
| `tier` | string | premium | `/combos/2/packages/2/tier` |
| `tierLabel` | string | 확장 | `/combos/2/packages/2/tierLabel` |
| `name` | string | 울쎄라 + 보톡스 + 필러 + 스킨부스터 | `/combos/2/packages/2/name` |
| `procedures` | array | (길이 4) | `/combos/2/packages/2/procedures` |
| `procedures[0]` | string | M9 | `/combos/2/packages/2/procedures/0` |
| `procedures[1]` | string | M1 | `/combos/2/packages/2/procedures/1` |
| `procedures[2]` | string | M2 | `/combos/2/packages/2/procedures/2` |
| `procedures[3]` | string | M4 | `/combos/2/packages/2/procedures/3` |
| `productTier` | string | 수입 | `/combos/2/packages/2/productTier` |
| `products` | array | (길이 1) | `/combos/2/packages/2/products` |
| `products[0]` | string | 울쎄라 + 보톡스(엘러간) + 쥬비덤 + 리쥬란 | `/combos/2/packages/2/products/0` |
| `priceRange` | string | 120~200만 | `/combos/2/packages/2/priceRange` |
| `expectedResult` | string | 리프팅 + 볼륨 복원 + 피부 재생. 탄력·볼륨·피부결 트리플 개선 | `/combos/2/packages/2/expectedResult` |
| `salesPitch` | string | 처짐은 당기는 것만으로 안 돼요. 꺼진 볼륨도 채우고 피부결까지 관리해야 자연스러워요. 이 조합이 가장 완성도가 높아요. | `/combos/2/packages/2/salesPitch` |
| `upsellHook` | string | 확실한 구조 변화를 원하시면 실리프팅을 추가하세요. 물리적으로 올려주니까 차원이 달라요. | `/combos/2/packages/2/upsellHook` |
| `clinicalRationale` | string | HIFU(타이트닝) + 보톡스(근이완) + 필러(볼륨손실 보충) + 스킨부스터(재생) = 처짐의 4대 원인(이완·근긴장·볼륨감소·피부노화) 동시 해결 | `/combos/2/packages/2/clinicalRationale` |
| `riskBenefit` | string | 시술 순서 준수. HIFU→보톡스→필러→스킨부스터. 각 시술이 서로 다른 층·메커니즘이라 부작용 중복 없음 | `/combos/2/packages/2/riskBenefit` |

### `/combos/2/packages/3` — P3-4 실리프팅 + 울쎄라 + 필러 + 보톡스

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/2/packages/3` |
| `id` | string | P3-4 | `/combos/2/packages/3/id` |
| `tier` | string | vip | `/combos/2/packages/3/tier` |
| `tierLabel` | string | 종합 | `/combos/2/packages/3/tierLabel` |
| `name` | string | 실리프팅 + 울쎄라 + 필러 + 보톡스 | `/combos/2/packages/3/name` |
| `procedures` | array | (길이 4) | `/combos/2/packages/3/procedures` |
| `procedures[0]` | string | M7 | `/combos/2/packages/3/procedures/0` |
| `procedures[1]` | string | M9 | `/combos/2/packages/3/procedures/1` |
| `procedures[2]` | string | M2 | `/combos/2/packages/3/procedures/2` |
| `procedures[3]` | string | M1 | `/combos/2/packages/3/procedures/3` |
| `productTier` | string | 수입 프리미엄 | `/combos/2/packages/3/productTier` |
| `products` | array | (길이 1) | `/combos/2/packages/3/products` |
| `products[0]` | string | 실루엣소프트 + 울쎄라 + 쥬비덤 + 보톡스(엘러간) | `/combos/2/packages/3/products/0` |
| `priceRange` | string | 250~400만 | `/combos/2/packages/3/priceRange` |
| `expectedResult` | string | 실 구조 확립 + HIFU 열 타이트닝 + 필러 볼륨 보충으로 하안면 라인 및 처짐의 현저한 개선 기대(개인차 있음). | `/combos/2/packages/3/expectedResult` |
| `salesPitch` | string | 비수술 리프팅 조합으로, 수술 전 단계에서 고려해볼 수 있는 통합 관리 프로그램입니다. 수술과 동일한 결과를 보장하지는 않습니다. | `/combos/2/packages/3/salesPitch` |
| `upsellHook` | string | 이 패키지를 6개월 간격으로 유지하시면 연간 프로그램 할인이 적용돼요. | `/combos/2/packages/3/upsellHook` |
| `clinicalRationale` | string | 실(물리적 거상·뼈대) + HIFU(열 타이트닝·고정) + 필러(볼륨 보충) + 보톡스(근이완·유지) = 4가지 메커니즘의 상보적 조합. 실이 구조를 잡으면 HIFU·필러의 효과가 배가됨 | `/combos/2/packages/3/clinicalRationale` |
| `riskBenefit` | string | 실리프팅 후 HIFU는 2~3개월 간격 필요 (같은 날이면 다른 부위). 실 부위와 HIFU 부위 겹침 주의. 그러나 각각의 시술 강도를 낮춰도 시너지로 우수한 결과 | `/combos/2/packages/3/riskBenefit` |

## 잠정 관찰 (원문과 분리)

| Pointer | 상태 | 관찰 |
|---|---|---|
| `/combos/2/problem` | P | "처짐/탄력" — problem 값에 "/"가 쓰임. README의 '/ = 둘 중 하나' 규칙이 problem 이름에도 적용되는지 원문에 정의 없음(F). |
| `/combos/2/packages/0/clinicalRationale` | P | "국산 HIFU(슈링크/더블로)" — 괄호 안 '/' 대안 예시로 README 규칙 형태와 일치. products는 "슈링크유니버스 or 더블로골드"로 다른 표면형(더블로 vs 더블로골드). |
| `/combos/2/packages/1/products/0` | P | "울쎄라 + 보톡스(엘러간) or 나보타" — or가 '보톡스(엘러간)'과 '나보타' 사이 대안인지 결합 전체 대안인지 괄호가 없어 원문상 모호(B). |
| `/combos/2/packages/1/clinicalRationale` | P | "올리는 힘 + 당기는 힘 제거" — '제거'가 '당기는 힘'에만 걸리는지 전체에 걸리는지 모호. HIFU=올리는 힘, 보톡스=당기는 힘 제거로 읽히나 잠정. |
| `/combos/2/packages/3/expectedResult` | P | P3-4의 expectedResult·salesPitch는 다른 항목과 달리 '(개인차 있음)', '기대', '보장하지는 않습니다' 같은 유보·고지 문체. 문체 차이 관찰만. |
| `/combos/2/packages/3/procedures` | P | procedures 순서 M7,M9,M2,M1 이 name 순서(실리프팅+울쎄라+필러+보톡스)와 일치. P2-3과 달리 name 순서=배열 순서. |
| `/combos/2/packages/3/riskBenefit` | P | "2~3개월 간격 필요 (같은 날이면 다른 부위)" — 간격 규칙과 같은 날 예외 조건이 한 칸 안에 있음. |
| `/combos/2/packages/0/upsellHook` | P | "유지력이 2배!" — 수치 주장, 근거 미기재. 임상 사실 판단 안 함. |
| `/combos/2/packages/0/name` | P | name "국산 HIFU 리프팅" — 제품 등급(국산)이 name에 들어감. |

## 수동 수집 표현 (원문 구간)

| Pointer | 구간 | 원문 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|
| `/combos/2/packages/0/products/0` | [0,16) | 슈링크유니버스 or 더블로골드 | 제품 대안 |  |
| `/combos/2/packages/0/priceRange` | [0,6) | 15~30만 | 수량·범위 |  |
| `/combos/2/packages/0/expectedResult` | [0,14) | 턱선 정리, 가벼운 리프팅 | 부위+정도 |  |
| `/combos/2/packages/0/expectedResult` | [16,30) | 시술 다음날부터 일상 가능 | 시간·가능성 |  |
| `/combos/2/packages/0/salesPitch` | [30,42) | 다운타임이 거의 없어서 | 부정·정도 | '거의 없어서' |
| `/combos/2/packages/0/salesPitch` | [43,59) | 부담 없이 시작하실 수 있어요 | 부정·가능성 |  |
| `/combos/2/packages/0/upsellHook` | [10,36) | 울쎄라가 깊은 층까지 닿아서 효과가 더 확실해요 | 비교·깊이 | '깊은 층' 수치화 금지 |
| `/combos/2/packages/0/upsellHook` | [38,57) | 보톡스도 같이 하시면 유지력이 2배 | 조건·수치 |  |
| `/combos/2/packages/0/clinicalRationale` | [0,16) | 국산 HIFU(슈링크/더블로) | 계열+장비 대안 |  |
| `/combos/2/packages/0/clinicalRationale` | [18,45) | 울쎄라 대비 에너지가 낮지만 가격 대비 효과 우수 | 비교·양보 | '-지만' |
| `/combos/2/packages/0/clinicalRationale` | [47,61) | 리프팅 입문 환자에게 적합 | 대상 |  |
| `/combos/2/packages/0/riskBenefit` | [0,8) | 위험 매우 낮음 | 정도 |  |
| `/combos/2/packages/0/riskBenefit` | [10,38) | 효과는 울쎄라 대비 약하지만 반복 시술로 보완 가능 | 비교·양보·가능성 |  |
| `/combos/2/packages/1/products/0` | [0,21) | 울쎄라 + 보톡스(엘러간) or 나보타 | 제품 결합+대안 | 범위 모호 |
| `/combos/2/packages/1/priceRange` | [0,7) | 60~120만 | 수량·범위 |  |
| `/combos/2/packages/1/expectedResult` | [0,15) | 확실한 리프팅 + 장기 유지 | 정도·시간 |  |
| `/combos/2/packages/1/expectedResult` | [17,40) | SMAS층 콜라겐 수축으로 자연스러운 턱선 | 층+부위 | SMAS층 혼합어 |
| `/combos/2/packages/1/salesPitch` | [36,49) | 효과가 6개월 이상 가요 | 시간·범위 | '이상' |
| `/combos/2/packages/1/salesPitch` | [51,66) | 가장 인기 있는 리프팅 조합 | 최상급 |  |
| `/combos/2/packages/1/upsellHook` | [0,23) | 볼이 꺼져 보이시면 필러 1cc만 추가해도 | 조건·부위·수량 | 1cc |
| `/combos/2/packages/1/upsellHook` | [32,41) | 탄력 후 볼륨까지 | 순서 |  |
| `/combos/2/packages/1/clinicalRationale` | [17,28) | 보톡스(광경근 이완) | 시술-부위-기전 | 광경근 해부 용어 |
| `/combos/2/packages/1/clinicalRationale` | [31,47) | 올리는 힘 + 당기는 힘 제거 | 기전 | 수식 범위 모호 |
| `/combos/2/packages/1/clinicalRationale` | [49,66) | 가장 검증된 비수술 리프팅 조합 | 최상급 |  |
| `/combos/2/packages/1/riskBenefit` | [0,22) | 울쎄라 열응고 후 보톡스 주입 순서 준수 | 순서 제약 |  |
| `/combos/2/packages/2/products/0` | [0,26) | 울쎄라 + 보톡스(엘러간) + 쥬비덤 + 리쥬란 | 제품 결합 |  |
| `/combos/2/packages/2/priceRange` | [0,8) | 120~200만 | 수량·범위 |  |
| `/combos/2/packages/2/expectedResult` | [21,37) | 탄력·볼륨·피부결 트리플 개선 | 수량 |  |
| `/combos/2/packages/2/salesPitch` | [0,17) | 처짐은 당기는 것만으로 안 돼요 | 부정 | '안 돼요' |
| `/combos/2/packages/2/salesPitch` | [30,47) | 피부결까지 관리해야 자연스러워요 | 조건(필요) |  |
| `/combos/2/packages/2/upsellHook` | [0,27) | 확실한 구조 변화를 원하시면 실리프팅을 추가하세요 | 조건·업셀 |  |
| `/combos/2/packages/2/clinicalRationale` | [50,83) | 처짐의 4대 원인(이완·근긴장·볼륨감소·피부노화) 동시 해결 | 원인 나열 |  |
| `/combos/2/packages/2/riskBenefit` | [10,27) | HIFU→보톡스→필러→스킨부스터 | 순서 | 공백 없는 → |
| `/combos/2/packages/2/riskBenefit` | [29,59) | 각 시술이 서로 다른 층·메커니즘이라 부작용 중복 없음 | 부정·인과 |  |
| `/combos/2/packages/3/products/0` | [0,29) | 실루엣소프트 + 울쎄라 + 쥬비덤 + 보톡스(엘러간) | 제품 결합 |  |
| `/combos/2/packages/3/priceRange` | [0,8) | 250~400만 | 수량·범위 |  |
| `/combos/2/packages/3/expectedResult` | [35,65) | 하안면 라인 및 처짐의 현저한 개선 기대(개인차 있음) | 부위·가능성·유보 |  |
| `/combos/2/packages/3/salesPitch` | [14,44) | 수술 전 단계에서 고려해볼 수 있는 통합 관리 프로그램 | 가능성·순서 |  |
| `/combos/2/packages/3/salesPitch` | [49,71) | 수술과 동일한 결과를 보장하지는 않습니다 | 부정·고지 |  |
| `/combos/2/packages/3/upsellHook` | [7,38) | 6개월 간격으로 유지하시면 연간 프로그램 할인이 적용돼요 | 주기·조건·가격 |  |
| `/combos/2/packages/3/clinicalRationale` | [0,56) | 실(물리적 거상·뼈대) + HIFU(열 타이트닝·고정) + 필러(볼륨 보충) + 보톡스(근이완·유지) | 시술-기전 |  |
| `/combos/2/packages/3/clinicalRationale` | [77,104) | 실이 구조를 잡으면 HIFU·필러의 효과가 배가됨 | 조건·인과 |  |
| `/combos/2/packages/3/riskBenefit` | [0,39) | 실리프팅 후 HIFU는 2~3개월 간격 필요 (같은 날이면 다른 부위) | 순서·간격·조건 |  |
| `/combos/2/packages/3/riskBenefit` | [41,60) | 실 부위와 HIFU 부위 겹침 주의 | 부위·주의 |  |
| `/combos/2/packages/3/riskBenefit` | [66,92) | 각각의 시술 강도를 낮춰도 시너지로 우수한 결과 | 양보·조건 | '-도' |
| `/combos/2/packages/1/salesPitch` | [0,14) | 리프팅하면 울쎄라+보톡스죠 | 조건·결합 |  |
| `/combos/2/packages/2/salesPitch` | [49,66) | 이 조합이 가장 완성도가 높아요 | 최상급 |  |
| `/combos/2/packages/3/clinicalRationale` | [59,75) | 4가지 메커니즘의 상보적 조합 | 수량 |  |
| `/combos/2/problem` | [0,5) | 처짐/탄력 | problem 값 / 나열 |  |
| `/combos/2/packages/1/clinicalRationale` | [0,28) | HIFU(SMAS 열응고) + 보톡스(광경근 이완) | 시술-기전 |  |
| `/combos/2/packages/2/clinicalRationale` | [0,47) | HIFU(타이트닝) + 보톡스(근이완) + 필러(볼륨손실 보충) + 스킨부스터(재생) | 시술-기전 |  |

## 이 구획의 미결

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| I-PC-06 | B | `/combos/2/packages/1/products/0` | '울쎄라 + 보톡스(엘러간) or 나보타' or 적용 범위 원문 괄호 없음 |
| I-PC-07 | I | `/combos/2/packages/0` | 같은 항목 안 제품 표면형 차이: products '더블로골드' vs clinicalRationale '더블로' (원문 내 표기 차이, 동일 대상 여부 미확정) |

## 알려진 형태소 오분절 (K) — 8건

상세·원시 토큰은 `morphology.json#/known_missegmentations`.

| Pointer | 구간 | 표현 | 원시 토큰 |
|---|---|---|---|
| `/combos/2/packages/1/expectedResult` | [17,22) | SMAS층 | SMAS/SL[17,21) 층/NNG[21,22) |
| `/combos/2/packages/1/clinicalRationale` | [21,24) | 광경근 | 광/NNG[21,22) 경/NNG[22,23) 근/NNG[23,24) |
| `/combos/2/packages/1/riskBenefit` | [4,7) | 열응고 | 열/NNG[4,5) 응고/NNG[5,7) |
| `/combos/2/packages/2/products/0` | [23,26) | 리쥬란 | 리쥬/NNP[23,25) 이/VCP[25,25) 란/ETM[25,26) |
| `/combos/2/packages/2/upsellHook` | [16,20) | 실리프팅 | 실/NNG[16,17) 리프팅/NNG[17,20) |
| `/combos/2/packages/2/clinicalRationale` | [27,31) | 볼륨손실 | 볼륨/NNG[27,29) 손실/NNG[29,31) |
| `/combos/2/packages/3/expectedResult` | [35,38) | 하안면 | 하/VV[35,36) 안면/NNG[36,38) |
| `/combos/2/packages/3/riskBenefit` | [0,4) | 실리프팅 | 실/NNG[0,1) 리프팅/NNG[1,4) |
