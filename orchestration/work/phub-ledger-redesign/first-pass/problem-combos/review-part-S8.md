# review-part-S8 — /combos/7 (P11 얼굴윤곽) 전체

원본: `orchestration/work/phub-recommend/bronze/phub-ledger/problem-combos.json` sha256 `74453c724800975ef7f3fa8b81546fe69fa014bfbc7a8f7e60c75774c2cf2262`

## 원문 값

원본 컬럼명은 축약하지 않는다. 배열은 원본 순서. 원문 칸에는 원문만 둔다.

### `/combos/7` 묶음

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | object | 키 ['problem_id', 'problem', 'packages'] | `/combos/7` |
| `problem_id` | string | P11 | `/combos/7/problem_id` |
| `problem` | string | 얼굴윤곽 | `/combos/7/problem` |
| `packages` | array | (길이 2) | `/combos/7/packages` |

### `/combos/7/packages/0` — P11-1 사각턱 보톡스 + 턱필러

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/7/packages/0` |
| `id` | string | P11-1 | `/combos/7/packages/0/id` |
| `tier` | string | entry | `/combos/7/packages/0/tier` |
| `tierLabel` | string | 기본 | `/combos/7/packages/0/tierLabel` |
| `name` | string | 사각턱 보톡스 + 턱필러 | `/combos/7/packages/0/name` |
| `procedures` | array | (길이 2) | `/combos/7/packages/0/procedures` |
| `procedures[0]` | string | M1 | `/combos/7/packages/0/procedures/0` |
| `procedures[1]` | string | M2 | `/combos/7/packages/0/procedures/1` |
| `productTier` | string | 국산 | `/combos/7/packages/0/productTier` |
| `products` | array | (길이 1) | `/combos/7/packages/0/products` |
| `products[0]` | string | 나보타(교근) + 이브아르(턱) | `/combos/7/packages/0/products/0` |
| `priceRange` | string | 20~40만 | `/combos/7/packages/0/priceRange` |
| `expectedResult` | string | 사각턱 축소 + 턱선 정리. V라인 효과. 2~4주 후 확연한 변화 | `/combos/7/packages/0/expectedResult` |
| `salesPitch` | string | V라인의 기본이에요! 사각턱 보톡스로 턱을 좁히고, 턱 필러로 라인을 잡으면 확 달라져요. 20분이면 끝! | `/combos/7/packages/0/salesPitch` |
| `upsellHook` | string | 턱선을 더 확실하게 잡으시려면 실리프팅으로 올려주는 것도 있어요! | `/combos/7/packages/0/upsellHook` |
| `clinicalRationale` | string | 교근 보톡스(근육 위축 → 턱폭 감소) + 턱끝 필러(하안면 길이 증가 → V라인 비율 개선). 비수술 윤곽의 기본 조합 | `/combos/7/packages/0/clinicalRationale` |
| `riskBenefit` | string | 위험 낮음. 교근 보톡스는 씹는 힘 일시 감소 가능 → 단단한 음식 주의 안내. 턱필러는 혈관 폐색 주의 | `/combos/7/packages/0/riskBenefit` |

### `/combos/7/packages/1` — P11-2 보톡스 + 필러 + 리프팅(HIFU 또는 고주파)

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/7/packages/1` |
| `id` | string | P11-2 | `/combos/7/packages/1/id` |
| `tier` | string | recommended | `/combos/7/packages/1/tier` |
| `tierLabel` | string | 표준 | `/combos/7/packages/1/tierLabel` |
| `name` | string | 보톡스 + 필러 + 리프팅(HIFU 또는 고주파) | `/combos/7/packages/1/name` |
| `procedures` | array | (길이 3) | `/combos/7/packages/1/procedures` |
| `procedures[0]` | string | M9 | `/combos/7/packages/1/procedures/0` |
| `procedures[1]` | string | M1 | `/combos/7/packages/1/procedures/1` |
| `procedures[2]` | string | M2 | `/combos/7/packages/1/procedures/2` |
| `productTier` | string | 수입 | `/combos/7/packages/1/productTier` |
| `products` | array | (길이 1) | `/combos/7/packages/1/products` |
| `products[0]` | string | 울쎄라(HIFU) 또는 올리지오(모노폴라 RF) + 보톡스 + 쥬비덤 | `/combos/7/packages/1/products/0` |
| `priceRange` | string | 80~150만 | `/combos/7/packages/1/priceRange` |
| `expectedResult` | string | 윤곽 축소 + 리프팅 + 볼륨 재배치. 얼굴형 자체가 달라지는 수준 | `/combos/7/packages/1/expectedResult` |
| `salesPitch` | string | 울쎄라(HIFU) 또는 올리지오(모노폴라 RF)로 턱선을 타이트닝하고, 보톡스로 교근을 축소하며, 필러로 라인을 보정하는 조합입니다(수술 대체가 아닌 보완적 프로그램). | `/combos/7/packages/1/salesPitch` |
| `upsellHook` | string | 이 위에 바이오스티뮬레이터(스컬트라)를 추가하면 볼륨이 점점 차오르면서 더 자연스러워요! | `/combos/7/packages/1/upsellHook` |
| `clinicalRationale` | string | 울쎄라(HIFU 심부 리프팅) 또는 올리지오(모노폴라 RF 진피 타이트닝) + 보톡스(교근 축소) + 필러(볼륨 재배치·턱 윤곽)로 목표와 작용 깊이에 맞춰 윤곽을 교정 | `/combos/7/packages/1/clinicalRationale` |
| `riskBenefit` | string | 선택한 에너지 시술(HIFU 또는 RF)→보톡스→필러 순서. 열 시술 후 주입으로 안전. 효과 대비 위험 비율 우수. 모노폴라 RF는 드물게 피하지방 위축(볼륨 손실)과 어두운 피부톤에서 PIH가 가능하므로 보수적 에너지·접촉냉각(contact cooling)이 필수이며, 볼륨 목표와 상충 가능성을 상담해야 함 | `/combos/7/packages/1/riskBenefit` |

## 잠정 관찰 (원문과 분리)

| Pointer | 상태 | 관찰 |
|---|---|---|
| `/combos/7/packages/0/products/0` | P | "나보타(교근) + 이브아르(턱)" — 괄호가 시술 부위를 표기. 이 원장 안 괄호는 브랜드(엘러간)·변형(희석)·부위(교근/턱)·별칭(골든루틴) 등 여러 쓰임. |
| `/combos/7/packages/1/name` | P | name "리프팅(HIFU 또는 고주파)" — 한국어 '또는' 대안. 같은 원장에 'or'·'/'·'또는' 세 가지 대안 표기. |
| `/combos/7/packages/1/procedures` | I | procedures는 M9만(M9,M1,M2). name·products·riskBenefit는 HIFU 또는 RF(올리지오) 대안을 말함. RF 대안에 해당하는 코드가 배열에 없음 — 원문 내 대응 불일치 후보(M9 코드 범위가 RF를 포함하는지 이 원장으로 판단 불가). |
| `/combos/7/packages/1/riskBenefit` | P | "드물게 피하지방 위축(볼륨 손실)" — 빈도 부사 '드물게'. 백분율로 바꾸지 않음. "볼륨 목표와 상충 가능성을 상담해야 함" — 상담 지시. |
| `/combos/7/packages/1/salesPitch` | P | salesPitch 문체가 다른 항목의 구어체(-요)와 달리 설명체(-입니다)이고 '(수술 대체가 아닌 보완적 프로그램)' 고지 포함. |
| `/combos/7/packages/0/clinicalRationale` | P | name '턱필러'와 rationale '턱끝 필러', products '(턱)' — 부위 표면형 차이(턱/턱끝). 동일 부위 여부 확정 안 함. |
| `/combos/7` | P | P11 묶음은 packages 2개(entry·recommended). |

## 수동 수집 표현 (원문 구간)

| Pointer | 구간 | 원문 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|
| `/combos/7/packages/0/name` | [0,13) | 사각턱 보톡스 + 턱필러 | 부위+시술 결합 |  |
| `/combos/7/packages/0/products/0` | [0,17) | 나보타(교근) + 이브아르(턱) | 제품+부위 | 괄호=부위 |
| `/combos/7/packages/0/priceRange` | [0,6) | 20~40만 | 수량·범위 |  |
| `/combos/7/packages/0/expectedResult` | [0,14) | 사각턱 축소 + 턱선 정리 | 부위·효과 |  |
| `/combos/7/packages/0/expectedResult` | [16,22) | V라인 효과 | 형태 표현 | 영문+한국어 |
| `/combos/7/packages/0/expectedResult` | [24,37) | 2~4주 후 확연한 변화 | 시간·범위 |  |
| `/combos/7/packages/0/salesPitch` | [12,49) | 사각턱 보톡스로 턱을 좁히고, 턱 필러로 라인을 잡으면 확 달라져요 | 부위·조건 |  |
| `/combos/7/packages/0/salesPitch` | [51,58) | 20분이면 끝 | 시간 |  |
| `/combos/7/packages/0/upsellHook` | [0,35) | 턱선을 더 확실하게 잡으시려면 실리프팅으로 올려주는 것도 있어요 | 조건·업셀 |  |
| `/combos/7/packages/0/clinicalRationale` | [0,21) | 교근 보톡스(근육 위축 → 턱폭 감소) | 부위·기전 인과 |  |
| `/combos/7/packages/0/clinicalRationale` | [24,52) | 턱끝 필러(하안면 길이 증가 → V라인 비율 개선) | 부위·기전 인과 |  |
| `/combos/7/packages/0/clinicalRationale` | [54,67) | 비수술 윤곽의 기본 조합 | 평가 |  |
| `/combos/7/packages/0/riskBenefit` | [7,43) | 교근 보톡스는 씹는 힘 일시 감소 가능 → 단단한 음식 주의 안내 | 부작용·시간·가능성·관리 | '일시' |
| `/combos/7/packages/0/riskBenefit` | [45,58) | 턱필러는 혈관 폐색 주의 | 부작용 |  |
| `/combos/7/packages/1/name` | [0,27) | 보톡스 + 필러 + 리프팅(HIFU 또는 고주파) | 시술 결합+대안 | '또는' |
| `/combos/7/packages/1/products/0` | [0,38) | 울쎄라(HIFU) 또는 올리지오(모노폴라 RF) + 보톡스 + 쥬비덤 | 제품 대안+결합 | 괄호=계열 |
| `/combos/7/packages/1/priceRange` | [0,7) | 80~150만 | 수량·범위 |  |
| `/combos/7/packages/1/expectedResult` | [0,20) | 윤곽 축소 + 리프팅 + 볼륨 재배치 | 효과 나열 |  |
| `/combos/7/packages/1/expectedResult` | [22,37) | 얼굴형 자체가 달라지는 수준 | 정도 |  |
| `/combos/7/packages/1/salesPitch` | [40,53) | 보톡스로 교근을 축소하며 | 부위·기전 |  |
| `/combos/7/packages/1/salesPitch` | [74,92) | 수술 대체가 아닌 보완적 프로그램 | 부정·고지 |  |
| `/combos/7/packages/1/upsellHook` | [5,48) | 바이오스티뮬레이터(스컬트라)를 추가하면 볼륨이 점점 차오르면서 더 자연스러워요 | 조건·시간·비교 | 괄호=제품 예 |
| `/combos/7/packages/1/clinicalRationale` | [0,41) | 울쎄라(HIFU 심부 리프팅) 또는 올리지오(모노폴라 RF 진피 타이트닝) | 대안·층 |  |
| `/combos/7/packages/1/clinicalRationale` | [57,72) | 필러(볼륨 재배치·턱 윤곽) | 시술-부위 |  |
| `/combos/7/packages/1/clinicalRationale` | [74,94) | 목표와 작용 깊이에 맞춰 윤곽을 교정 | 조건 |  |
| `/combos/7/packages/1/riskBenefit` | [0,32) | 선택한 에너지 시술(HIFU 또는 RF)→보톡스→필러 순서 | 순서·대안 |  |
| `/combos/7/packages/1/riskBenefit` | [34,48) | 열 시술 후 주입으로 안전 | 순서·인과 |  |
| `/combos/7/packages/1/riskBenefit` | [66,115) | 모노폴라 RF는 드물게 피하지방 위축(볼륨 손실)과 어두운 피부톤에서 PIH가 가능하므로 | 빈도·부작용·조건·가능성 | '드물게' 백분율 변환 금지 |
| `/combos/7/packages/1/riskBenefit` | [116,149) | 보수적 에너지·접촉냉각(contact cooling)이 필수 | 조건·관리 | 한영 병기 |
| `/combos/7/packages/1/riskBenefit` | [153,174) | 볼륨 목표와 상충 가능성을 상담해야 함 | 가능성·상담 지시 |  |
| `/combos/7/packages/1/salesPitch` | [0,38) | 울쎄라(HIFU) 또는 올리지오(모노폴라 RF)로 턱선을 타이트닝하고 | 제품 대안·부위 |  |
| `/combos/7/packages/1/clinicalRationale` | [44,54) | 보톡스(교근 축소) | 시술-부위-기전 |  |

## 이 구획의 미결

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| I-PC-15 | I | `/combos/7/packages/1/procedures` | RF(올리지오) 대안이 텍스트엔 있으나 procedures엔 M9만 — 코드 범위 미확인, 후속 연결(F) |
| I-PC-16 | I | `/combos/*/packages/*/products/*` | 대안 표기 'or'·'/'·'또는' 세 가지 혼용(원문 내 불일치) |

## 알려진 형태소 오분절 (K) — 12건

상세·원시 토큰은 `morphology.json#/known_missegmentations`.

| Pointer | 구간 | 표현 | 원시 토큰 |
|---|---|---|---|
| `/combos/7/packages/0/name` | [0,3) | 사각턱 | 사각/NNG[0,2) 턱/NNG[2,3) |
| `/combos/7/packages/0/expectedResult` | [0,3) | 사각턱 | 사각/NNG[0,2) 턱/NNG[2,3) |
| `/combos/7/packages/0/expectedResult` | [16,19) | V라인 | V/SL[16,17) 라인/NNG[17,19) |
| `/combos/7/packages/0/salesPitch` | [12,15) | 사각턱 | 사각/NNG[12,14) 턱/NNG[14,15) |
| `/combos/7/packages/0/salesPitch` | [0,3) | V라인 | V/SL[0,1) 라인/NNG[1,3) |
| `/combos/7/packages/0/upsellHook` | [17,21) | 실리프팅 | 실/NNG[17,18) 리프팅/NNG[18,21) |
| `/combos/7/packages/0/clinicalRationale` | [30,33) | 하안면 | 하안/NNP[30,32) 면/NNG[32,33) |
| `/combos/7/packages/0/clinicalRationale` | [15,17) | 턱폭 | 턱/NNG[15,16) 폭/NNG[16,17) |
| `/combos/7/packages/0/clinicalRationale` | [42,45) | V라인 | V/SL[42,43) 라인/NNG[43,45) |
| `/combos/7/packages/0/riskBenefit` | [41,43) | 안내 | 안/MAG[41,42) 내/VV[42,43) 어/EF[42,43) |
| `/combos/7/packages/1/clinicalRationale` | [9,11) | 심부 | 심/XR[9,10) 부/NNG[10,11) |
| `/combos/7/packages/1/riskBenefit` | [124,128) | 접촉냉각 | 접촉/NNG[124,126) 냉각/NNG[126,128) |
