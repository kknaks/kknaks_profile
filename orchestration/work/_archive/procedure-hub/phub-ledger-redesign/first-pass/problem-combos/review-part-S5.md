# review-part-S5 — /combos/4 (P5 색소/미백) 전체

원본: `orchestration/work/phub-recommend/bronze/phub-ledger/problem-combos.json` sha256 `74453c724800975ef7f3fa8b81546fe69fa014bfbc7a8f7e60c75774c2cf2262`

## 원문 값

원본 컬럼명은 축약하지 않는다. 배열은 원본 순서. 원문 칸에는 원문만 둔다.

### `/combos/4` 묶음

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (묶음) | object | 키 ['problem_id', 'problem', 'packages'] | `/combos/4` |
| `problem_id` | string | P5 | `/combos/4/problem_id` |
| `problem` | string | 색소/미백 | `/combos/4/problem` |
| `packages` | array | (길이 3) | `/combos/4/packages` |

### `/combos/4/packages/0` — P5-1 레이저 토닝

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/4/packages/0` |
| `id` | string | P5-1 | `/combos/4/packages/0/id` |
| `tier` | string | entry | `/combos/4/packages/0/tier` |
| `tierLabel` | string | 기본 | `/combos/4/packages/0/tierLabel` |
| `name` | string | 레이저 토닝 | `/combos/4/packages/0/name` |
| `procedures` | array | (길이 1) | `/combos/4/packages/0/procedures` |
| `procedures[0]` | string | M8 | `/combos/4/packages/0/procedures/0` |
| `productTier` | string | 국산/수입 | `/combos/4/packages/0/productTier` |
| `products` | array | (길이 1) | `/combos/4/packages/0/products` |
| `products[0]` | string | 피코슈어 or 레블라이트 or 클라리티 | `/combos/4/packages/0/products/0` |
| `priceRange` | string | 5~15만/회 | `/combos/4/packages/0/priceRange` |
| `expectedResult` | string | 점진적 색소 개선. 5~10회 반복 시 확연한 톤 개선 | `/combos/4/packages/0/expectedResult` |
| `salesPitch` | string | 색소는 레이저 토닝이 기본이에요. 점심시간에 하고 바로 일상 복귀 가능해요. 5회 패키지로 시작하시면 할인돼요! | `/combos/4/packages/0/salesPitch` |
| `upsellHook` | string | 토닝만 하시면 아까워요! PRP를 같이 하시면 재생이 빨라져서 색소침착 재발이 훨씬 줄어요. | `/combos/4/packages/0/upsellHook` |
| `clinicalRationale` | string | Nd:YAG/피코레이저의 선택적 광열분해로 멜라닌 파괴. 낮은 에너지 반복 조사로 PIH(시술 후 색소침착) 최소화 | `/combos/4/packages/0/clinicalRationale` |
| `riskBenefit` | string | 위험 낮음. PIH 가능성 있으나 적절한 에너지·간격으로 관리 가능. 자외선 차단 필수 | `/combos/4/packages/0/riskBenefit` |

### `/combos/4/packages/1` — P5-2 레이저 토닝 + PRP + 스킨부스터

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/4/packages/1` |
| `id` | string | P5-2 | `/combos/4/packages/1/id` |
| `tier` | string | recommended | `/combos/4/packages/1/tier` |
| `tierLabel` | string | 표준 | `/combos/4/packages/1/tierLabel` |
| `name` | string | 레이저 토닝 + PRP + 스킨부스터 | `/combos/4/packages/1/name` |
| `procedures` | array | (길이 3) | `/combos/4/packages/1/procedures` |
| `procedures[0]` | string | M8 | `/combos/4/packages/1/procedures/0` |
| `procedures[1]` | string | M5 | `/combos/4/packages/1/procedures/1` |
| `procedures[2]` | string | M4 | `/combos/4/packages/1/procedures/2` |
| `productTier` | string | 혼합 | `/combos/4/packages/1/productTier` |
| `products` | array | (길이 1) | `/combos/4/packages/1/products` |
| `products[0]` | string | 피코레이저 + PRP + 리쥬란 | `/combos/4/packages/1/products/0` |
| `priceRange` | string | 25~45만/회 | `/combos/4/packages/1/priceRange` |
| `expectedResult` | string | 색소 파괴 + 재생 촉진 + 피부 보호. 토닝 단독보다 효과 빠르고 색소침착 재발 감소 | `/combos/4/packages/1/expectedResult` |
| `salesPitch` | string | 토닝+재생 조합이에요. 레이저로 색소 부수고, PRP+스킨부스터가 새 피부를 빨리 만들어서 하얗고 깨끗한 피부가 더 빨리 나와요! | `/combos/4/packages/1/salesPitch` |
| `upsellHook` | string | 색소 + 모공까지 같이 하시려면 니들RF를 추가하시면 돼요! | `/combos/4/packages/1/upsellHook` |
| `clinicalRationale` | string | 레이저(멜라닌 파괴) + PRP(성장인자로 정상 멜라노사이트 회복 보조) + 스킨부스터(PDRN 기반 회복 보조). PIH 위험 완화에 기여할 수 있으나 근거는 제한적 | `/combos/4/packages/1/clinicalRationale` |
| `riskBenefit` | string | 레이저 토닝 후 PRP 병용이 재생을 도와 PIH를 줄일 수 있다는 소규모 연구·증례 보고는 있으나 근거는 아직 제한적(멜라스마 대상 PRP는 8개 소규모 연구 수준, 레이저 토닝 병용·PIH 감소 데이터는 예비적). 레이저 토닝 자체가 색소 재발·저색소·PIH 위험을 가지므로 저플루언스·적정 간격 준수가 필요. 참고로 2026 기준 레이저 후 PIH 예방 근거가 가장 확립된 것은 트라넥사민산(TXA)이며 PRP는 보조적 위치. | `/combos/4/packages/1/riskBenefit` |

### `/combos/4/packages/2` — P5-3 피코레이저 + 니들RF + PRP + 스킨부스터

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| (패키지) | object | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPitch', 'upsellHook', 'clinicalRationale', 'riskBenefit'] | `/combos/4/packages/2` |
| `id` | string | P5-3 | `/combos/4/packages/2/id` |
| `tier` | string | premium | `/combos/4/packages/2/tier` |
| `tierLabel` | string | 확장 | `/combos/4/packages/2/tierLabel` |
| `name` | string | 피코레이저 + 니들RF + PRP + 스킨부스터 | `/combos/4/packages/2/name` |
| `procedures` | array | (길이 4) | `/combos/4/packages/2/procedures` |
| `procedures[0]` | string | M8 | `/combos/4/packages/2/procedures/0` |
| `procedures[1]` | string | M11 | `/combos/4/packages/2/procedures/1` |
| `procedures[2]` | string | M5 | `/combos/4/packages/2/procedures/2` |
| `procedures[3]` | string | M4 | `/combos/4/packages/2/procedures/3` |
| `productTier` | string | 수입 | `/combos/4/packages/2/productTier` |
| `products` | array | (길이 1) | `/combos/4/packages/2/products` |
| `products[0]` | string | 피코슈어/피코웨이 + 포텐자 + PRP + 리쥬란 | `/combos/4/packages/2/products/0` |
| `priceRange` | string | 60~100만/회 | `/combos/4/packages/2/priceRange` |
| `expectedResult` | string | 난치성 색소 + 모공 + 피부결 종합 개선. 깊은 기미까지 개선 | `/combos/4/packages/2/expectedResult` |
| `salesPitch` | string | 일반 토닝으로 안 되는 깊은 색소까지 잡는 프리미엄이에요. 피코레이저+니들RF의 이중 타겟 + 재생으로 확실한 결과! | `/combos/4/packages/2/salesPitch` |
| `upsellHook` | string | 이 프로그램을 5회 패키지로 하시면 확실한 차이가 나요. 패키지 할인 + 유지 관리 1회 무료! | `/combos/4/packages/2/upsellHook` |
| `clinicalRationale` | string | 피코레이저(표피 색소·진피 색소) + 니들RF(진피 리모델링·모공 수축) + PRP(재생) + 스킨부스터(보호). 다른 메커니즘으로 색소의 다층 구조를 타겟 | `/combos/4/packages/2/clinicalRationale` |
| `riskBenefit` | string | 니들RF 후 PIH 주의. 레이저→니들RF→PRP→SB 순서 엄수. 열 시술 2개이므로 간격 관리 중요 | `/combos/4/packages/2/riskBenefit` |

## 잠정 관찰 (원문과 분리)

| Pointer | 상태 | 관찰 |
|---|---|---|
| `/combos/4/packages/0/priceRange` | P | P5 묶음 priceRange는 모두 "/회" 접미(5~15만/회 등). P1~P4는 접미 없음. 회당 가격 여부가 묶음마다 다르게 표기됨 — 접미 없는 값이 패키지가인지 회당인지는 B. |
| `/combos/4/packages/0/productTier` | P | "국산/수입" — '/' 대안 표기. P5-2는 "혼합", P1-2는 "국산+수입 혼합". productTier 값 표면형이 일정하지 않음. |
| `/combos/4/packages/0/products/0` | P | 3개 대안을 "or"로 나열(피코슈어 or 레블라이트 or 클라리티). |
| `/combos/4/packages/1/clinicalRationale` | P | "기여할 수 있으나 근거는 제한적" — 가능성+유보 문체. P3-4처럼 다른 항목보다 유보적. |
| `/combos/4/packages/1/riskBenefit` | P | 긴 서술(3문장): 연구 수(8개 소규모 연구), 연도 기준(2026 기준), 다른 성분(트라넥사민산(TXA)) 언급. 출처 표기 없음. 이 원장 안에서 TXA는 procedures·products에 없음 — 참조 표현으로만 보존. |
| `/combos/4/packages/1/riskBenefit` | P | riskBenefit에 '증거 수준' 진술이 포함 — upsell 문구("재생이 빨라져서 색소침착 재발이 훨씬 줄어요", P5-1 upsellHook)의 단정과 같은 원장 안에서 어조가 다름. 의학적 판단 안 함(I 후보: 원문 내 어조 불일치). |
| `/combos/4/packages/2/riskBenefit` | P | "레이저→니들RF→PRP→SB" 순서와 procedures M8,M11,M5,M4 순서 일치. SB 약어 재등장. |
| `/combos/4/packages/2/name` | P | name "피코레이저 + 니들RF ..." — name에 장비 계열명(피코레이저)이 들어감. |

## 수동 수집 표현 (원문 구간)

| Pointer | 구간 | 원문 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|
| `/combos/4/packages/0/productTier` | [0,5) | 국산/수입 | 제품 등급 대안 |  |
| `/combos/4/packages/0/products/0` | [0,21) | 피코슈어 or 레블라이트 or 클라리티 | 제품 대안 |  |
| `/combos/4/packages/0/priceRange` | [0,7) | 5~15만/회 | 수량·범위·회당 |  |
| `/combos/4/packages/0/expectedResult` | [0,9) | 점진적 색소 개선 | 정도·시간 |  |
| `/combos/4/packages/0/expectedResult` | [11,30) | 5~10회 반복 시 확연한 톤 개선 | 회차·조건 |  |
| `/combos/4/packages/0/salesPitch` | [19,41) | 점심시간에 하고 바로 일상 복귀 가능해요 | 시간·가능성 |  |
| `/combos/4/packages/0/salesPitch` | [43,61) | 5회 패키지로 시작하시면 할인돼요 | 회차·조건·가격 |  |
| `/combos/4/packages/0/upsellHook` | [0,12) | 토닝만 하시면 아까워요 | 조건 |  |
| `/combos/4/packages/0/upsellHook` | [14,50) | PRP를 같이 하시면 재생이 빨라져서 색소침착 재발이 훨씬 줄어요 | 조건·인과 |  |
| `/combos/4/packages/0/clinicalRationale` | [0,30) | Nd:YAG/피코레이저의 선택적 광열분해로 멜라닌 파괴 | 장비·기전 | Nd:YAG 콜론 포함 |
| `/combos/4/packages/0/clinicalRationale` | [32,64) | 낮은 에너지 반복 조사로 PIH(시술 후 색소침착) 최소화 | 정도·조건·부작용 | '낮은' 수치화 금지 |
| `/combos/4/packages/0/riskBenefit` | [7,37) | PIH 가능성 있으나 적절한 에너지·간격으로 관리 가능 | 가능성·양보·조건 |  |
| `/combos/4/packages/0/riskBenefit` | [39,48) | 자외선 차단 필수 | 관리 |  |
| `/combos/4/packages/1/productTier` | [0,2) | 혼합 | 제품 등급 |  |
| `/combos/4/packages/1/products/0` | [0,17) | 피코레이저 + PRP + 리쥬란 | 제품 결합 |  |
| `/combos/4/packages/1/priceRange` | [0,8) | 25~45만/회 | 수량·범위·회당 |  |
| `/combos/4/packages/1/expectedResult` | [23,48) | 토닝 단독보다 효과 빠르고 색소침착 재발 감소 | 비교 |  |
| `/combos/4/packages/1/salesPitch` | [51,71) | 하얗고 깨끗한 피부가 더 빨리 나와요 | 형용사·비교 |  |
| `/combos/4/packages/1/upsellHook` | [0,32) | 색소 + 모공까지 같이 하시려면 니들RF를 추가하시면 돼요 | 조건·업셀 |  |
| `/combos/4/packages/1/clinicalRationale` | [14,40) | PRP(성장인자로 정상 멜라노사이트 회복 보조) | 시술-기전 |  |
| `/combos/4/packages/1/clinicalRationale` | [43,63) | 스킨부스터(PDRN 기반 회복 보조) | 시술-성분 |  |
| `/combos/4/packages/1/clinicalRationale` | [65,93) | PIH 위험 완화에 기여할 수 있으나 근거는 제한적 | 가능성·유보 |  |
| `/combos/4/packages/1/riskBenefit` | [0,66) | 레이저 토닝 후 PRP 병용이 재생을 도와 PIH를 줄일 수 있다는 소규모 연구·증례 보고는 있으나 근거는 아직 제한적 | 근거 수준·가능성·양보 |  |
| `/combos/4/packages/1/riskBenefit` | [67,92) | 멜라스마 대상 PRP는 8개 소규모 연구 수준 | 근거 수량 | 출처 미기재 |
| `/combos/4/packages/1/riskBenefit` | [94,119) | 레이저 토닝 병용·PIH 감소 데이터는 예비적 | 근거 수준 |  |
| `/combos/4/packages/1/riskBenefit` | [122,174) | 레이저 토닝 자체가 색소 재발·저색소·PIH 위험을 가지므로 저플루언스·적정 간격 준수가 필요 | 위험·인과·조건 | '저플루언스' 전문어 |
| `/combos/4/packages/1/riskBenefit` | [180,240) | 2026 기준 레이저 후 PIH 예방 근거가 가장 확립된 것은 트라넥사민산(TXA)이며 PRP는 보조적 위치 | 시간 기준·근거 비교 | 원장 밖 성분 참조 |
| `/combos/4/packages/2/products/0` | [0,27) | 피코슈어/피코웨이 + 포텐자 + PRP + 리쥬란 | 제품 결합+대안 |  |
| `/combos/4/packages/2/priceRange` | [0,9) | 60~100만/회 | 수량·범위·회당 |  |
| `/combos/4/packages/2/expectedResult` | [0,23) | 난치성 색소 + 모공 + 피부결 종합 개선 | 효과 나열 |  |
| `/combos/4/packages/2/expectedResult` | [25,35) | 깊은 기미까지 개선 | 깊이·범위 | '깊은' 수치화 금지 |
| `/combos/4/packages/2/salesPitch` | [0,23) | 일반 토닝으로 안 되는 깊은 색소까지 잡는 | 부정·깊이 |  |
| `/combos/4/packages/2/upsellHook` | [8,30) | 5회 패키지로 하시면 확실한 차이가 나요 | 회차·조건 |  |
| `/combos/4/packages/2/upsellHook` | [41,52) | 유지 관리 1회 무료 | 회차·가격 |  |
| `/combos/4/packages/2/clinicalRationale` | [0,18) | 피코레이저(표피 색소·진피 색소) | 층 |  |
| `/combos/4/packages/2/clinicalRationale` | [21,40) | 니들RF(진피 리모델링·모공 수축) | 층·기전 |  |
| `/combos/4/packages/2/clinicalRationale` | [74,87) | 색소의 다층 구조를 타겟 | 층 |  |
| `/combos/4/packages/2/riskBenefit` | [0,13) | 니들RF 후 PIH 주의 | 시간·부작용 |  |
| `/combos/4/packages/2/riskBenefit` | [15,36) | 레이저→니들RF→PRP→SB 순서 엄수 | 순서 제약 |  |
| `/combos/4/packages/2/riskBenefit` | [38,57) | 열 시술 2개이므로 간격 관리 중요 | 수량·인과 |  |
| `/combos/4/problem` | [0,5) | 색소/미백 | problem 값 / 나열 |  |
| `/combos/4/packages/1/clinicalRationale` | [0,11) | 레이저(멜라닌 파괴) | 시술-기전 |  |
| `/combos/4/packages/2/clinicalRationale` | [43,62) | PRP(재생) + 스킨부스터(보호) | 시술-기전 |  |

## 이 구획의 미결

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| I-PC-10 | I | `/combos/4/packages/*/priceRange` | priceRange '/회' 접미가 P5·P9 묶음에만 있음 — 원문 내 표기 불일치 |
| I-PC-11 | I | `/combos/*/packages/*/productTier` | productTier 표면형 불일치: '국산+수입 혼합'·'수입+국산'·'국산/수입'·'혼합' |
| I-PC-12 | F | `/combos/4/packages/1/riskBenefit` | 연구 수·2026 기준·TXA 등 근거 진술 출처 미기재 — 외부 보충 금지, 후속 근거 원장(literature-evidence) 연결 과제 |

## 알려진 형태소 오분절 (K) — 11건

상세·원시 토큰은 `morphology.json#/known_missegmentations`.

| Pointer | 구간 | 표현 | 원시 토큰 |
|---|---|---|---|
| `/combos/4/packages/0/clinicalRationale` | [0,6) | Nd:YAG | Nd/SL[0,2) :/SP[2,3) YAG/SL[3,6) |
| `/combos/4/packages/1/products/0` | [14,17) | 리쥬란 | 리쥬/NNP[14,16) 이/VCP[16,16) 란/ETM[16,17) |
| `/combos/4/packages/1/products/0` | [0,5) | 피코레이저 | 피코/NNP[0,2) 레이저/NNG[2,5) |
| `/combos/4/packages/1/upsellHook` | [18,22) | 니들RF | 니들/NNP[18,20) RF/SL[20,22) |
| `/combos/4/packages/2/name` | [8,12) | 니들RF | 니들/NNP[8,10) RF/SL[10,12) |
| `/combos/4/packages/2/products/0` | [24,27) | 리쥬란 | 리쥬/NNP[24,26) 이/VCP[26,26) 란/ETM[26,27) |
| `/combos/4/packages/2/salesPitch` | [39,43) | 니들RF | 니들/NNP[39,41) RF/SL[41,43) |
| `/combos/4/packages/2/clinicalRationale` | [0,5) | 피코레이저 | 피코/NNP[0,2) 레이저/NNG[2,5) |
| `/combos/4/packages/2/clinicalRationale` | [21,25) | 니들RF | 니들/NNP[21,23) RF/SL[23,25) |
| `/combos/4/packages/2/riskBenefit` | [0,4) | 니들RF | 니/NP[0,1) 들/XSN[1,2) RF/SL[2,4) |
| `/combos/4/packages/2/riskBenefit` | [19,23) | 니들RF | 니들/NNP[19,21) RF/SL[21,23) |
