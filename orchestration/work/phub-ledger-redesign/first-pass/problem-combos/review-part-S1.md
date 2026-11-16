# review-part-S1 — /combos/0 (P1 쁘띠시술) 전체

원본: `orchestration/work/phub-recommend/bronze/phub-ledger/problem-combos.json` sha256 `74453c724800975ef7f3fa8b81546fe69fa014bfbc7a8f7e60c75774c2cf2262`

## 원문 값

원본 컬럼명은 축약하지 않는다. 배열은 원본 순서. 원문 칸에는 원문만 둔다.

### `/combos/0` 묶음

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | object | 키 ['problem_id', 'problem', 'packages'] | `/combos/0` |
| `problem_id` | string | P1 | `/combos/0/problem_id` |
| `problem` | string | 쁘띠시술 | `/combos/0/problem` |
| `packages` | array | (길이 3) | `/combos/0/packages` |

### `/combos/0/packages/0` — P1-1 보톡스 단독

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/0/packages/0` |
| `id` | string | P1-1 | `/combos/0/packages/0/id` |
| `tier` | string | entry | `/combos/0/packages/0/tier` |
| `tierLabel` | string | 기본 | `/combos/0/packages/0/tierLabel` |
| `name` | string | 보톡스 단독 | `/combos/0/packages/0/name` |
| `procedures` | array | (길이 1) | `/combos/0/packages/0/procedures` |
| `procedures[0]` | string | M1 | `/combos/0/packages/0/procedures/0` |
| `productTier` | string | 국산 | `/combos/0/packages/0/productTier` |
| `products` | array | (길이 1) | `/combos/0/packages/0/products` |
| `products[0]` | string | 나보타 or 보툴렉스 | `/combos/0/packages/0/products/0` |
| `priceRange` | string | 5~8만 | `/combos/0/packages/0/priceRange` |
| `expectedResult` | string | 이마·미간·눈가 주름 개선. 시술 10분, 바로 일상 복귀 | `/combos/0/packages/0/expectedResult` |
| `salesPitch` | string | 처음이시면 가볍게 보톡스부터 시작해보세요. 10분이면 끝나고 점심시간에도 가능해요. | `/combos/0/packages/0/salesPitch` |
| `upsellHook` | string | 보톡스로 주름 펴시고, 필러로 꺼진 부분 채우시면 확 달라지세요! | `/combos/0/packages/0/upsellHook` |
| `clinicalRationale` | string | 보톡스 단독으로도 동적 주름에 충분한 효과. 첫 방문 환자 신뢰 구축 후 추가 시술 연계 | `/combos/0/packages/0/clinicalRationale` |
| `riskBenefit` | string | 위험 최소, 효과 확실. 첫 시술로 최적 | `/combos/0/packages/0/riskBenefit` |

### `/combos/0/packages/1` — P1-2 보톡스 + 필러

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/0/packages/1` |
| `id` | string | P1-2 | `/combos/0/packages/1/id` |
| `tier` | string | recommended | `/combos/0/packages/1/tier` |
| `tierLabel` | string | 표준 | `/combos/0/packages/1/tierLabel` |
| `name` | string | 보톡스 + 필러 | `/combos/0/packages/1/name` |
| `procedures` | array | (길이 2) | `/combos/0/packages/1/procedures` |
| `procedures[0]` | string | M1 | `/combos/0/packages/1/procedures/0` |
| `procedures[1]` | string | M2 | `/combos/0/packages/1/procedures/1` |
| `productTier` | string | 국산+수입 혼합 | `/combos/0/packages/1/productTier` |
| `products` | array | (길이 1) | `/combos/0/packages/1/products` |
| `products[0]` | string | 나보타 + 쥬비덤 or 이브아르 | `/combos/0/packages/1/products/0` |
| `priceRange` | string | 25~45만 | `/combos/0/packages/1/priceRange` |
| `expectedResult` | string | 주름 개선 + 볼륨 복원. 동적주름(보톡스) + 정적주름·볼륨(필러) 동시 해결 | `/combos/0/packages/1/expectedResult` |
| `salesPitch` | string | 보톡스+필러가 가장 인기 있는 동안 조합이에요. 30분이면 끝나고 '좀 쉬었나?' 소리 들으실 거예요. | `/combos/0/packages/1/salesPitch` |
| `upsellHook` | string | 여기에 스킨부스터 한 번 추가하시면 피부결까지 달라져요. 패키지로 묶으면 할인도 돼요! | `/combos/0/packages/1/upsellHook` |
| `clinicalRationale` | string | 보톡스(근이완) + 필러(볼륨)는 가장 검증된 쁘띠 조합. 보톡스가 근육 움직임을 줄여 필러 유지력도 향상시킴 | `/combos/0/packages/1/clinicalRationale` |
| `riskBenefit` | string | 위험 낮음. 필러 혈관 폐색 주의 → 히알루로니다아제 비상 준비. 효과 대비 위험 비율 매우 우수 | `/combos/0/packages/1/riskBenefit` |

### `/combos/0/packages/2` — P1-3 수입 보톡스 + 수입 필러 + 스킨부스터

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/0/packages/2` |
| `id` | string | P1-3 | `/combos/0/packages/2/id` |
| `tier` | string | premium | `/combos/0/packages/2/tier` |
| `tierLabel` | string | 확장 | `/combos/0/packages/2/tierLabel` |
| `name` | string | 수입 보톡스 + 수입 필러 + 스킨부스터 | `/combos/0/packages/2/name` |
| `procedures` | array | (길이 3) | `/combos/0/packages/2/procedures` |
| `procedures[0]` | string | M1 | `/combos/0/packages/2/procedures/0` |
| `procedures[1]` | string | M2 | `/combos/0/packages/2/procedures/1` |
| `procedures[2]` | string | M4 | `/combos/0/packages/2/procedures/2` |
| `productTier` | string | 수입 | `/combos/0/packages/2/productTier` |
| `products` | array | (길이 1) | `/combos/0/packages/2/products` |
| `products[0]` | string | 보톡스(엘러간) + 쥬비덤 + 리쥬란 | `/combos/0/packages/2/products/0` |
| `priceRange` | string | 60~100만 | `/combos/0/packages/2/priceRange` |
| `expectedResult` | string | 주름 + 볼륨 + 피부결·광채까지. 1회로 동안 얼굴 완성 | `/combos/0/packages/2/expectedResult` |
| `salesPitch` | string | 수입 정품으로 주름·볼륨·피부결을 한 번에! 프리미엄 라인이라 결과가 더 자연스럽고 오래가요. | `/combos/0/packages/2/salesPitch` |
| `upsellHook` | string | 피부 탄력까지 원하시면 HIFU 추가하시는 분들이 많으세요. 풀 패키지로 가시면 원장님이 직접 해드려요. | `/combos/0/packages/2/upsellHook` |
| `clinicalRationale` | string | 수입 보톡스(엘러간)는 임상 데이터 가장 풍부. 쥬비덤 Vycross 기술로 자연스러운 결과. 리쥬란 PN(폴리뉴클레오타이드)이 시술 후 재생 촉진 | `/combos/0/packages/2/clinicalRationale` |
| `riskBenefit` | string | 위험 낮음. 수입 제품의 예측 가능한 결과 + 스킨부스터 재생으로 부작용 최소화 | `/combos/0/packages/2/riskBenefit` |

## 잠정 관찰 (원문과 분리)

| Pointer | 상태 | 관찰 |
|---|---|---|
| `/combos/0/problem` | P | problem 값 "쁘띠시술"은 다른 problem(주름·모공 등)과 달리 고민이 아니라 시술군 이름처럼 읽힌다. 고민/시술군 구분은 후속 의미 조사(F). |
| `/combos/0/packages/0/products/0` | P | 제품 대안을 영문 "or"로 표기. README 규칙의 "/"(대안)와 다른 기호. 같은 의미인지 확정하지 않음(F). |
| `/combos/0/packages/1/products/0` | P | products 배열 원소가 1개뿐이고 그 안에 "+"와 "or"가 섞인 결합 문자열. 결합 우선순위(나보타 + (쥬비덤 or 이브아르))는 원문에 괄호가 없어 확정 불가(B). |
| `/combos/0/packages/0/priceRange` | B | "5~8만" — 통화·단위(원)·1회당/패키지당 여부가 원문에 없음. 채우지 않음. |
| `/combos/0/packages/0/procedures` | P | procedures는 M코드 배열(M1). 코드가 가리키는 시술 이름은 이 원장 안에 정의가 없음 — 다른 원장 참조로 보이며 후속 연결 과제(F). name의 시술명 순서와 procedures 순서 대응도 미확정. |
| `/combos/0/packages/1/clinicalRationale` | P | "보톡스가 근육 움직임을 줄여 필러 유지력도 향상시킴" — 시술 간 인과 주장. 임상적 사실 여부 판단하지 않음. |
| `/combos/0/packages/1/riskBenefit` | P | "→" 기호가 위험(혈관 폐색)과 대비 조치(히알루로니다아제 비상 준비)를 잇는다. 기호 의미 확정 안 함. |
| `/combos/0/packages/2/name` | P | name은 "수입 보톡스 + 수입 필러 + 스킨부스터"로 '수입' 수식어가 이름에 들어감. productTier="수입"과 중복 표현. |
| `/combos/0/packages/2/products/0` | P | "보톡스(엘러간)" — 괄호가 제조사/브랜드를 표기. README의 '괄호 안 대안은 예시' 규칙과 다른 쓰임일 수 있음(F). |
| `/combos/0/packages/2/upsellHook` | P | HIFU가 업셀 대상으로 등장하지만 이 패키지 procedures에는 없음. 업셀 문구 속 시술은 패키지 구성원이 아님. |
| `/combos/0/packages/0/expectedResult` | P | "이마·미간·눈가" 부위 나열에 가운뎃점(·) 사용. README의 부위 나열 '+' 규칙과 다른 기호. |

## 수동 수집 표현 (원문 구간)

| Pointer | 구간 | 원문 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|
| `/combos/0/packages/0/products/0` | [0,11) | 나보타 or 보툴렉스 | 제품 대안 | or 연결 |
| `/combos/0/packages/0/priceRange` | [0,4) | 5~8만 | 수량·범위 | 단위 미기재 |
| `/combos/0/packages/0/expectedResult` | [0,14) | 이마·미간·눈가 주름 개선 | 부위+효과 |  |
| `/combos/0/packages/0/expectedResult` | [16,22) | 시술 10분 | 시간 |  |
| `/combos/0/packages/0/expectedResult` | [24,32) | 바로 일상 복귀 | 시간·회복 |  |
| `/combos/0/packages/0/salesPitch` | [0,22) | 처음이시면 가볍게 보톡스부터 시작해보세요 | 조건 | 조건 -시면 |
| `/combos/0/packages/0/salesPitch` | [34,45) | 점심시간에도 가능해요 | 가능성 |  |
| `/combos/0/packages/0/upsellHook` | [13,27) | 필러로 꺼진 부분 채우시면 | 조건·부위 | 부위 불특정 '꺼진 부분' |
| `/combos/0/packages/0/clinicalRationale` | [0,23) | 보톡스 단독으로도 동적 주름에 충분한 효과 | 수식·범위 | '단독으로도'의 보조사 '도' |
| `/combos/0/packages/0/clinicalRationale` | [25,49) | 첫 방문 환자 신뢰 구축 후 추가 시술 연계 | 시간·순서 |  |
| `/combos/0/packages/0/riskBenefit` | [0,12) | 위험 최소, 효과 확실 | 평가 |  |
| `/combos/0/packages/1/products/0` | [0,17) | 나보타 + 쥬비덤 or 이브아르 | 제품 결합+대안 | 괄호 없음, 결합 범위 모호 |
| `/combos/0/packages/1/productTier` | [0,8) | 국산+수입 혼합 | 제품 등급 |  |
| `/combos/0/packages/1/priceRange` | [0,6) | 25~45만 | 수량·범위 | 단위 미기재 |
| `/combos/0/packages/1/expectedResult` | [15,44) | 동적주름(보톡스) + 정적주름·볼륨(필러) 동시 해결 | 문제-시술 대응 | 괄호가 담당 시술을 표기 |
| `/combos/0/packages/1/salesPitch` | [27,36) | 30분이면 끝나고 | 시간·조건 |  |
| `/combos/0/packages/1/salesPitch` | [37,56) | '좀 쉬었나?' 소리 들으실 거예요 | 인용·추측 | 작은따옴표 인용 |
| `/combos/0/packages/1/upsellHook` | [4,19) | 스킨부스터 한 번 추가하시면 | 회차·조건 |  |
| `/combos/0/packages/1/upsellHook` | [32,47) | 패키지로 묶으면 할인도 돼요 | 조건·가격 |  |
| `/combos/0/packages/1/clinicalRationale` | [0,17) | 보톡스(근이완) + 필러(볼륨) | 시술-기전 | 괄호가 기전 표기 |
| `/combos/0/packages/1/clinicalRationale` | [33,61) | 보톡스가 근육 움직임을 줄여 필러 유지력도 향상시킴 | 인과 |  |
| `/combos/0/packages/1/riskBenefit` | [7,35) | 필러 혈관 폐색 주의 → 히알루로니다아제 비상 준비 | 위험+대비 | → 기호 |
| `/combos/0/packages/1/riskBenefit` | [37,54) | 효과 대비 위험 비율 매우 우수 | 정도 부사+평가 |  |
| `/combos/0/packages/2/products/0` | [0,20) | 보톡스(엘러간) + 쥬비덤 + 리쥬란 | 제품 결합 | 괄호=브랜드/제조사 |
| `/combos/0/packages/2/priceRange` | [0,7) | 60~100만 | 수량·범위 | 단위 미기재 |
| `/combos/0/packages/2/expectedResult` | [20,32) | 1회로 동안 얼굴 완성 | 회차+효과 |  |
| `/combos/0/packages/2/salesPitch` | [35,51) | 결과가 더 자연스럽고 오래가요 | 비교 수식 | 비교 대상 미기재 |
| `/combos/0/packages/2/upsellHook` | [0,32) | 피부 탄력까지 원하시면 HIFU 추가하시는 분들이 많으세요 | 조건·업셀 |  |
| `/combos/0/packages/2/upsellHook` | [34,57) | 풀 패키지로 가시면 원장님이 직접 해드려요 | 조건·시술자 |  |
| `/combos/0/packages/2/clinicalRationale` | [13,25) | 임상 데이터 가장 풍부 | 최상급 평가 |  |
| `/combos/0/packages/2/clinicalRationale` | [27,41) | 쥬비덤 Vycross 기술 | 제품+기술명 | 영문 기술명 |
| `/combos/0/packages/2/clinicalRationale` | [53,70) | 리쥬란 PN(폴리뉴클레오타이드) | 제품+성분 | 약어+괄호 풀이 |
| `/combos/0/packages/2/clinicalRationale` | [72,82) | 시술 후 재생 촉진 | 시간+효과 |  |
| `/combos/0/packages/2/riskBenefit` | [7,23) | 수입 제품의 예측 가능한 결과 | 가능성 |  |
| `/combos/0/packages/2/riskBenefit` | [26,44) | 스킨부스터 재생으로 부작용 최소화 | 인과 |  |
| `/combos/0/packages/1/salesPitch` | [8,22) | 가장 인기 있는 동안 조합 | 최상급 | '동안'(외모) — 정규식 부정 '안' 오탐 위치 |
| `/combos/0/packages/1/clinicalRationale` | [19,31) | 가장 검증된 쁘띠 조합 | 최상급 |  |
| `/combos/0/packages/0/salesPitch` | [24,33) | 10분이면 끝나고 | 시간·조건 |  |
| `/combos/0/packages/2/clinicalRationale` | [0,11) | 수입 보톡스(엘러간) | 제품+브랜드 |  |

## 이 구획의 미결

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| I-PC-01 | B | `/combos/*/packages/*/priceRange` | 가격 범위 단위·기준(원, 회당/패키지) 원문 미기재 — 전 구획 공통 확인 예정 |
| I-PC-02 | F | `/combos/*/packages/*/procedures/*` | M코드 정의가 이 원장에 없음 — 다른 원장 참조 후속 연결 |
| I-PC-03 | F | `/combos/*/packages/*/products/*` | products 원소 안 '+'·'or'·'/'·괄호 혼용, 결합 우선순위 원문에 없음 |

## 알려진 형태소 오분절 (K) — 3건

상세·원시 토큰은 `morphology.json#/known_missegmentations`.

| Pointer | 구간 | 표현 | 원시 토큰 |
|---|---|---|---|
| `/combos/0/packages/1/expectedResult` | [27,31) | 정적주름 | 정적/NNG[27,29) 주름/NNG[29,31) |
| `/combos/0/packages/2/products/0` | [17,20) | 리쥬란 | 리쥬/NNP[17,19) 이/VCP[19,19) 란/ETM[19,20) |
| `/combos/0/packages/2/clinicalRationale` | [53,56) | 리쥬란 | 리쥬/NNP[53,55) 이/VCP[55,55) 란/ETM[55,56) |
