# review-part-S6 — /combos/5 (P7 모공) 전체

원본: `orchestration/work/phub-recommend/bronze/phub-ledger/problem-combos.json` sha256 `74453c724800975ef7f3fa8b81546fe69fa014bfbc7a8f7e60c75774c2cf2262`

## 원문 값

원본 컬럼명은 축약하지 않는다. 배열은 원본 순서. 원문 칸에는 원문만 둔다.

### `/combos/5` 묶음

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | object | 키 ['problem_id', 'problem', 'packages'] | `/combos/5` |
| `problem_id` | string | P7 | `/combos/5/problem_id` |
| `problem` | string | 모공 | `/combos/5/problem` |
| `packages` | array | (길이 3) | `/combos/5/packages` |

### `/combos/5/packages/0` — P7-1 스킨보톡스 + 레이저

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/5/packages/0` |
| `id` | string | P7-1 | `/combos/5/packages/0/id` |
| `tier` | string | entry | `/combos/5/packages/0/tier` |
| `tierLabel` | string | 기본 | `/combos/5/packages/0/tierLabel` |
| `name` | string | 스킨보톡스 + 레이저 | `/combos/5/packages/0/name` |
| `procedures` | array | (길이 2) | `/combos/5/packages/0/procedures` |
| `procedures[0]` | string | M1 | `/combos/5/packages/0/procedures/0` |
| `procedures[1]` | string | M8 | `/combos/5/packages/0/procedures/1` |
| `productTier` | string | 국산 | `/combos/5/packages/0/productTier` |
| `products` | array | (길이 1) | `/combos/5/packages/0/products` |
| `products[0]` | string | 나보타(희석) + 레이저 토닝 | `/combos/5/packages/0/products/0` |
| `priceRange` | string | 15~30만 | `/combos/5/packages/0/priceRange` |
| `expectedResult` | string | 피지 분비 감소 + 모공 축소. 1~2주 후 모공이 조여지는 느낌 | `/combos/5/packages/0/expectedResult` |
| `salesPitch` | string | 모공에는 스킨보톡스가 기본이에요. 보톡스를 희석해서 피부 전체에 얇게 깔면 모공이 조여지고 피지가 줄어요! | `/combos/5/packages/0/salesPitch` |
| `upsellHook` | string | 모공 확실하게 잡으시려면 니들RF가 있어요. 모공 크기가 확 줄어들어요! | `/combos/5/packages/0/upsellHook` |
| `clinicalRationale` | string | 희석 보톡스의 피내 주사 → 피지선 아세틸콜린 차단 → 피지 분비 감소 → 모공 축소. 레이저가 진피 콜라겐 자극으로 모공벽 탄력 향상 | `/combos/5/packages/0/clinicalRationale` |
| `riskBenefit` | string | 위험 매우 낮음. 스킨보톡스는 일반 보톡스보다 용량이 적어 부작용 최소 | `/combos/5/packages/0/riskBenefit` |

### `/combos/5/packages/1` — P7-2 니들RF + PRP

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/5/packages/1` |
| `id` | string | P7-2 | `/combos/5/packages/1/id` |
| `tier` | string | recommended | `/combos/5/packages/1/tier` |
| `tierLabel` | string | 표준 | `/combos/5/packages/1/tierLabel` |
| `name` | string | 니들RF + PRP | `/combos/5/packages/1/name` |
| `procedures` | array | (길이 2) | `/combos/5/packages/1/procedures` |
| `procedures[0]` | string | M11 | `/combos/5/packages/1/procedures/0` |
| `procedures[1]` | string | M5 | `/combos/5/packages/1/procedures/1` |
| `productTier` | string | 국산 | `/combos/5/packages/1/productTier` |
| `products` | array | (길이 1) | `/combos/5/packages/1/products` |
| `products[0]` | string | 포텐자/인트라셀 + PRP | `/combos/5/packages/1/products/0` |
| `priceRange` | string | 30~50만 | `/combos/5/packages/1/priceRange` |
| `expectedResult` | string | 모공 크기·피부결의 점진적 개선. 3~5회 반복 시 눈에 띄는 변화(개인차 큼) | `/combos/5/packages/1/expectedResult` |
| `salesPitch` | string | 모공 줄이는 데 가장 효과적인 조합이에요. 니들RF가 모공 주변 콜라겐을 조이고, PRP가 새 콜라겐 생성을 도와요. 결과가 정말 좋아요! | `/combos/5/packages/1/salesPitch` |
| `upsellHook` | string | 여기에 스킨부스터 추가하시면 모공+피부결+탄력까지! 완벽한 피부 리뉴얼이에요. | `/combos/5/packages/1/upsellHook` |
| `clinicalRationale` | string | 니들RF(진피 열응고 → 콜라겐 수축 → 모공벽 타이트닝) + PRP(성장인자가 열손상 부위 콜라겐 리모델링 가속) = 모공 축소의 골든 조합 | `/combos/5/packages/1/clinicalRationale` |
| `riskBenefit` | string | 니들RF 후 2~3일 홍반·부종. PRP가 회복을 촉진하여 다운타임 단축. 3~5회 반복 시 모공 크기·피부결의 점진적 개선(문헌상 병용요법 모공 약 20~30% 감소, 개인차 큼) | `/combos/5/packages/1/riskBenefit` |

### `/combos/5/packages/2` — P7-3 니들RF + 레이저 + PRP + 스킨부스터

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/5/packages/2` |
| `id` | string | P7-3 | `/combos/5/packages/2/id` |
| `tier` | string | premium | `/combos/5/packages/2/tier` |
| `tierLabel` | string | 확장 | `/combos/5/packages/2/tierLabel` |
| `name` | string | 니들RF + 레이저 + PRP + 스킨부스터 | `/combos/5/packages/2/name` |
| `procedures` | array | (길이 4) | `/combos/5/packages/2/procedures` |
| `procedures[0]` | string | M11 | `/combos/5/packages/2/procedures/0` |
| `procedures[1]` | string | M8 | `/combos/5/packages/2/procedures/1` |
| `procedures[2]` | string | M5 | `/combos/5/packages/2/procedures/2` |
| `procedures[3]` | string | M4 | `/combos/5/packages/2/procedures/3` |
| `productTier` | string | 수입 | `/combos/5/packages/2/productTier` |
| `products` | array | (길이 1) | `/combos/5/packages/2/products` |
| `products[0]` | string | 포텐자 + 피코레이저 + PRP + 리쥬란 | `/combos/5/packages/2/products/0` |
| `priceRange` | string | 60~90만 | `/combos/5/packages/2/priceRange` |
| `expectedResult` | string | 모공+색소+피부결 종합 개선. 매끈하고 깨끗한 피부 | `/combos/5/packages/2/expectedResult` |
| `salesPitch` | string | 모공만 줄이는 게 아니라 색소·피부결까지 한 번에! 종합 피부 리뉴얼 프리미엄이에요. 이걸 3회만 하시면 '피부 어디서 했어?' 소리 들으실 거예요. | `/combos/5/packages/2/salesPitch` |
| `upsellHook` | string | 5회 패키지 가입하시면 매회 10% 할인 + 유지 스킨부스터 2회 무료! | `/combos/5/packages/2/upsellHook` |
| `clinicalRationale` | string | 니들RF(진피 모공 타이트닝) + 레이저(표피 색소·각질 정리) + PRP(재생 촉진) + 스킨부스터(수분·DNA 회복) = 모공의 원인(피지·콜라겐 이완·각질)과 동반 문제(색소·피부결)를 동시 해결 | `/combos/5/packages/2/clinicalRationale` |
| `riskBenefit` | string | 열 시술 2개(니들RF+레이저)이므로 순서·간격 주의. 니들RF→레이저→PRP→SB 순서. 효과는 최대이나 다운타임도 상대적으로 길 수 있음(3~5일) | `/combos/5/packages/2/riskBenefit` |

## 잠정 관찰 (원문과 분리)

| Pointer | 상태 | 관찰 |
|---|---|---|
| `/combos/5/packages/0/name` | P | "스킨보톡스" — procedures M1(보톡스와 동일 코드). 시술 변형(희석)이 코드가 아니라 이름·products 괄호(나보타(희석))로만 구분됨. |
| `/combos/5/packages/0/products/0` | P | "레이저 토닝"이 products에 시술명 형태로 들어감 — products 원소가 제품명만 담지는 않음. |
| `/combos/5/packages/1/riskBenefit` | P | "문헌상 병용요법 모공 약 20~30% 감소, 개인차 큼" — 원문에 있는 백분율. 출처 미기재(F). expectedResult와 riskBenefit에 '3~5회 반복 시 ... 점진적 개선'이 거의 같은 문장으로 중복 출현. |
| `/combos/5/packages/2/upsellHook` | P | "매회 10% 할인" — 가격 할인 백분율이 원문에 있음. |
| `/combos/5/packages/2/riskBenefit` | P | "다운타임도 상대적으로 길 수 있음(3~5일)" — 가능성+괄호 수치 범위. |
| `/combos/5/packages/0/clinicalRationale` | P | 화살표 연쇄가 시술 순서가 아니라 기전 인과(차단 → 감소 → 축소)를 나타냄. 같은 '→' 기호가 순서(P2-3)와 인과(여기) 두 쓰임. |

## 수동 수집 표현 (원문 구간)

| Pointer | 구간 | 원문 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|
| `/combos/5/packages/0/name` | [0,11) | 스킨보톡스 + 레이저 | 시술 결합 |  |
| `/combos/5/packages/0/products/0` | [0,16) | 나보타(희석) + 레이저 토닝 | 제품 결합·변형 | 괄호=희석 |
| `/combos/5/packages/0/priceRange` | [0,6) | 15~30만 | 수량·범위 |  |
| `/combos/5/packages/0/expectedResult` | [0,16) | 피지 분비 감소 + 모공 축소 | 효과 |  |
| `/combos/5/packages/0/expectedResult` | [18,36) | 1~2주 후 모공이 조여지는 느낌 | 시간·범위 |  |
| `/combos/5/packages/0/salesPitch` | [19,41) | 보톡스를 희석해서 피부 전체에 얇게 깔면 | 조건·부위·정도 | '얇게' 수치화 금지 |
| `/combos/5/packages/0/upsellHook` | [0,23) | 모공 확실하게 잡으시려면 니들RF가 있어요 | 조건·업셀 |  |
| `/combos/5/packages/0/clinicalRationale` | [0,47) | 희석 보톡스의 피내 주사 → 피지선 아세틸콜린 차단 → 피지 분비 감소 → 모공 축소 | 기전 인과 연쇄 | → = 인과 |
| `/combos/5/packages/0/clinicalRationale` | [49,75) | 레이저가 진피 콜라겐 자극으로 모공벽 탄력 향상 | 층·기전 |  |
| `/combos/5/packages/0/riskBenefit` | [10,39) | 스킨보톡스는 일반 보톡스보다 용량이 적어 부작용 최소 | 비교·인과 | 용량 수치 미기재 |
| `/combos/5/packages/1/products/0` | [0,14) | 포텐자/인트라셀 + PRP | 제품 결합+대안 |  |
| `/combos/5/packages/1/priceRange` | [0,6) | 30~50만 | 수량·범위 |  |
| `/combos/5/packages/1/expectedResult` | [19,44) | 3~5회 반복 시 눈에 띄는 변화(개인차 큼) | 회차·조건·유보 |  |
| `/combos/5/packages/1/salesPitch` | [0,19) | 모공 줄이는 데 가장 효과적인 조합 | 최상급 |  |
| `/combos/5/packages/1/salesPitch` | [24,44) | 니들RF가 모공 주변 콜라겐을 조이고 | 부위·기전 |  |
| `/combos/5/packages/1/upsellHook` | [4,27) | 스킨부스터 추가하시면 모공+피부결+탄력까지 | 조건·효과 |  |
| `/combos/5/packages/1/clinicalRationale` | [0,32) | 니들RF(진피 열응고 → 콜라겐 수축 → 모공벽 타이트닝) | 기전 인과 연쇄 |  |
| `/combos/5/packages/1/clinicalRationale` | [35,64) | PRP(성장인자가 열손상 부위 콜라겐 리모델링 가속) | 기전 |  |
| `/combos/5/packages/1/clinicalRationale` | [67,79) | 모공 축소의 골든 조합 | 평가 |  |
| `/combos/5/packages/1/riskBenefit` | [0,17) | 니들RF 후 2~3일 홍반·부종 | 시간·부작용 |  |
| `/combos/5/packages/1/riskBenefit` | [19,40) | PRP가 회복을 촉진하여 다운타임 단축 | 인과 |  |
| `/combos/5/packages/1/riskBenefit` | [70,100) | 문헌상 병용요법 모공 약 20~30% 감소, 개인차 큼 | 근거·수치·유보 | '약' 근사 |
| `/combos/5/packages/2/products/0` | [0,23) | 포텐자 + 피코레이저 + PRP + 리쥬란 | 제품 결합 |  |
| `/combos/5/packages/2/priceRange` | [0,6) | 60~90만 | 수량·범위 |  |
| `/combos/5/packages/2/expectedResult` | [17,28) | 매끈하고 깨끗한 피부 | 형용사 |  |
| `/combos/5/packages/2/salesPitch` | [0,27) | 모공만 줄이는 게 아니라 색소·피부결까지 한 번에 | 부정·범위 | '-이 아니라' |
| `/combos/5/packages/2/salesPitch` | [48,82) | 이걸 3회만 하시면 '피부 어디서 했어?' 소리 들으실 거예요 | 회차·조건·인용 |  |
| `/combos/5/packages/2/upsellHook` | [0,39) | 5회 패키지 가입하시면 매회 10% 할인 + 유지 스킨부스터 2회 무료 | 회차·조건·가격 |  |
| `/combos/5/packages/2/clinicalRationale` | [70,112) | 모공의 원인(피지·콜라겐 이완·각질)과 동반 문제(색소·피부결)를 동시 해결 | 원인 나열 |  |
| `/combos/5/packages/2/riskBenefit` | [0,29) | 열 시술 2개(니들RF+레이저)이므로 순서·간격 주의 | 수량·인과 |  |
| `/combos/5/packages/2/riskBenefit` | [31,49) | 니들RF→레이저→PRP→SB 순서 | 순서 |  |
| `/combos/5/packages/2/riskBenefit` | [51,84) | 효과는 최대이나 다운타임도 상대적으로 길 수 있음(3~5일) | 양보·가능성·시간 |  |
| `/combos/5/packages/1/riskBenefit` | [42,69) | 3~5회 반복 시 모공 크기·피부결의 점진적 개선 | 회차·조건 | expectedResult와 거의 같은 문장 반복 출현 |
| `/combos/5/packages/0/riskBenefit` | [0,8) | 위험 매우 낮음 | 정도 |  |
| `/combos/5/packages/2/clinicalRationale` | [0,67) | 니들RF(진피 모공 타이트닝) + 레이저(표피 색소·각질 정리) + PRP(재생 촉진) + 스킨부스터(수분·DNA 회복) | 시술-층-기전 |  |

## 이 구획의 미결

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| I-PC-13 | F | `/combos/5/packages/1/riskBenefit` | '문헌상 ... 약 20~30% 감소' 출처 미기재 — 외부 보충 금지, 후속 근거 연결 |
| I-PC-14 | P | `/combos/5/packages/0/procedures` | 스킨보톡스(희석)가 M1 코드로만 표현 — 변형 시술의 코드 구분 없음(의미 판단은 후속) |

## 알려진 형태소 오분절 (K) — 17건

상세·원시 토큰은 `morphology.json#/known_missegmentations`.

| Pointer | 구간 | 표현 | 원시 토큰 |
|---|---|---|---|
| `/combos/5/packages/0/name` | [0,5) | 스킨보톡스 | 스킨/NNG[0,2) 보톡스/NNG[2,5) |
| `/combos/5/packages/0/salesPitch` | [5,10) | 스킨보톡스 | 스킨/NNG[5,7) 보톡스/NNG[7,10) |
| `/combos/5/packages/0/upsellHook` | [14,18) | 니들RF | 니들/NNP[14,16) RF/SL[16,18) |
| `/combos/5/packages/0/clinicalRationale` | [66,69) | 모공벽 | 모공/NNG[66,68) 벽/NNG[68,69) |
| `/combos/5/packages/0/riskBenefit` | [10,15) | 스킨보톡스 | 스킨/NNG[10,12) 보톡스/NNG[12,15) |
| `/combos/5/packages/1/name` | [0,4) | 니들RF | 니들/NNP[0,2) RF/SL[2,4) |
| `/combos/5/packages/1/salesPitch` | [24,28) | 니들RF | 니들/NNP[24,26) RF/SL[26,28) |
| `/combos/5/packages/1/clinicalRationale` | [0,4) | 니들RF | 니들/NNP[0,2) RF/SL[2,4) |
| `/combos/5/packages/1/clinicalRationale` | [8,11) | 열응고 | 열/NNG[8,9) 응고/NNG[9,11) |
| `/combos/5/packages/1/clinicalRationale` | [23,26) | 모공벽 | 모공/NNG[23,25) 벽/NNG[25,26) |
| `/combos/5/packages/1/clinicalRationale` | [45,48) | 열손상 | 열/NNG[45,46) 손상/NNG[46,48) |
| `/combos/5/packages/1/riskBenefit` | [0,4) | 니들RF | 니/NP[0,1) 들/XSN[1,2) RF/SL[2,4) |
| `/combos/5/packages/2/name` | [0,4) | 니들RF | 니들/NNP[0,2) RF/SL[2,4) |
| `/combos/5/packages/2/products/0` | [20,23) | 리쥬란 | 리쥬/NNP[20,22) 이/VCP[22,22) 란/ETM[22,23) |
| `/combos/5/packages/2/clinicalRationale` | [0,4) | 니들RF | 니들/NNP[0,2) RF/SL[2,4) |
| `/combos/5/packages/2/riskBenefit` | [8,12) | 니들RF | 니들/NNP[8,10) RF/SL[10,12) |
| `/combos/5/packages/2/riskBenefit` | [31,35) | 니들RF | 니들/NNP[31,33) RF/SL[33,35) |
