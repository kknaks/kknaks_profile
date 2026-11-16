# problem-combos 1차 조사 — review

## 상태

- **1차 범위 종료: 예** (아래 조건 충족 — 상세 validation.md)
- **원장 전체 완료 아님** — 의미 관계·공통 개념·원문 부족(B)·후속(F) 미결이 남음(issues.md)
- 전수 읽기: 구획 9/9 직접 읽음 (coverage.json, manual/S*.json)
- 구조·값 수집: 노드 460개(말단 370개) 전부 source-map.json
- 형태소·표현 수집: 값 370건 중 적용 249·제외 121(사유 기록), 필드명 출현 340건; 표현 666건(수동 323)
- 알려진 분석 오류(K): 81건 출현별 기록

## 원본

- 경로: `orchestration/work/phub-recommend/bronze/phub-ledger/problem-combos.json`
- sha256: `74453c724800975ef7f3fa8b81546fe69fa014bfbc7a8f7e60c75774c2cf2262` · 25026 bytes · 14325 코드포인트 · 1줄(개행 없음)
- 중복 키 0건 · 백슬래시 이스케이프 없음 · BOM 없음 · BMP 밖 문자 0개
- 묶음(combos) 8개 · 패키지 24개

## 컬럼 구성 표

모든 경로 패턴. 선택적 필드·빈 값 확인 결과: 모든 패키지가 같은 12키를 같은 순서로 가짐(선택적 필드 0). 빈 문자열·빈 배열·빈 객체·null 0건(verify.py가 재확인).

| 원본 컬럼명/경로 패턴 | 자료형 | 중첩 구조·길이 | 출현 수 | 원문 예시 | 예시 Pointer |
|---|---|---|---|---|---|
| `(root)` | object | 길이 4 | 1 | 키 ['version', 'updated', 'description', 'combos'] | `(root)` |
| `/version` | string | 말단 | 1 | 1.2 | `/version` |
| `/updated` | string | 말단 | 1 | 2026-07-26 | `/updated` |
| `/description` | string | 말단 | 1 | Problem별 추천 조합 — 상담 안내와 의료진 참고 정보 통합 | `/description` |
| `/combos` | array | 길이 8 | 1 | 길이 8 | `/combos` |
| `/combos/*` | object | 길이 3 | 8 | 키 ['problem_id', 'problem', 'packages'] | `/combos/0` |
| `/combos/*/problem_id` | string | 말단 | 8 | P1 | `/combos/0/problem_id` |
| `/combos/*/problem` | string | 말단 | 8 | 쁘띠시술 | `/combos/0/problem` |
| `/combos/*/packages` | array | 길이 2,3,4 | 8 | 길이 3 | `/combos/0/packages` |
| `/combos/*/packages/*` | object | 길이 13 | 24 | 키 ['id', 'tier', 'tierLabel', 'name', 'procedures', 'productTier', 'products', 'priceRange', 'expectedResult', 'salesPit | `/combos/0/packages/0` |
| `/combos/*/packages/*/id` | string | 말단 | 24 | P1-1 | `/combos/0/packages/0/id` |
| `/combos/*/packages/*/tier` | string | 말단 | 24 | entry | `/combos/0/packages/0/tier` |
| `/combos/*/packages/*/tierLabel` | string | 말단 | 24 | 기본 | `/combos/0/packages/0/tierLabel` |
| `/combos/*/packages/*/name` | string | 말단 | 24 | 보톡스 단독 | `/combos/0/packages/0/name` |
| `/combos/*/packages/*/procedures` | array | 길이 1,2,3,4,5 | 24 | 길이 1 | `/combos/0/packages/0/procedures` |
| `/combos/*/packages/*/procedures/*` | string | 말단 | 63 | M1 | `/combos/0/packages/0/procedures/0` |
| `/combos/*/packages/*/productTier` | string | 말단 | 24 | 국산 | `/combos/0/packages/0/productTier` |
| `/combos/*/packages/*/products` | array | 길이 1 | 24 | 길이 1 | `/combos/0/packages/0/products` |
| `/combos/*/packages/*/products/*` | string | 말단 | 24 | 나보타 or 보툴렉스 | `/combos/0/packages/0/products/0` |
| `/combos/*/packages/*/priceRange` | string | 말단 | 24 | 5~8만 | `/combos/0/packages/0/priceRange` |
| `/combos/*/packages/*/expectedResult` | string | 말단 | 24 | 이마·미간·눈가 주름 개선. 시술 10분, 바로 일상 복귀 | `/combos/0/packages/0/expectedResult` |
| `/combos/*/packages/*/salesPitch` | string | 말단 | 24 | 처음이시면 가볍게 보톡스부터 시작해보세요. 10분이면 끝나고 점심시간에도 가능해요. | `/combos/0/packages/0/salesPitch` |
| `/combos/*/packages/*/upsellHook` | string | 말단 | 24 | 보톡스로 주름 펴시고, 필러로 꺼진 부분 채우시면 확 달라지세요! | `/combos/0/packages/0/upsellHook` |
| `/combos/*/packages/*/clinicalRationale` | string | 말단 | 24 | 보톡스 단독으로도 동적 주름에 충분한 효과. 첫 방문 환자 신뢰 구축 후 추가 시술 연계 | `/combos/0/packages/0/clinicalRationale` |
| `/combos/*/packages/*/riskBenefit` | string | 말단 | 24 | 위험 최소, 효과 확실. 첫 시술로 최적 | `/combos/0/packages/0/riskBenefit` |

## 구획 목차

| 구획 | 범위 | 소유 노드 | 말단 | 직접 읽기 | 관찰 | 수동 표현 | 파일 |
|---|---|---|---|---|---|---|---|
| S0 | 루트 객체·메타데이터(version/updated/description)와 /combos 배열 컨테이너 | 5 | 3 | read | 3 | 2 | [review-part-S0.md](review-part-S0.md) |
| S1 | /combos/0 (P1 쁘띠시술) 전체 | 55 | 44 | read | 11 | 39 | [review-part-S1.md](review-part-S1.md) |
| S2 | /combos/1 (P2 주름) 전체 | 77 | 63 | read | 9 | 48 | [review-part-S2.md](review-part-S2.md) |
| S3 | /combos/2 (P3 처짐/탄력) 전체 | 75 | 61 | read | 9 | 51 | [review-part-S3.md](review-part-S3.md) |
| S4 | /combos/3 (P4 피부결/톤/항노화) 전체 | 57 | 46 | read | 10 | 44 | [review-part-S4.md](review-part-S4.md) |
| S5 | /combos/4 (P5 색소/미백) 전체 | 57 | 46 | read | 8 | 43 | [review-part-S5.md](review-part-S5.md) |
| S6 | /combos/5 (P7 모공) 전체 | 57 | 46 | read | 6 | 35 | [review-part-S6.md](review-part-S6.md) |
| S7 | /combos/6 (P9 흉터) 전체 | 38 | 30 | read | 4 | 29 | [review-part-S7.md](review-part-S7.md) |
| S8 | /combos/7 (P11 얼굴윤곽) 전체 | 39 | 31 | read | 7 | 32 | [review-part-S8.md](review-part-S8.md) |

## 전체에 걸친 잠정 관찰 (원문과 분리)

- 패키지 tier 구성이 묶음마다 다름: P2·P3은 entry/recommended/premium/vip 4개, P9·P11은 entry/recommended 2개, 나머지 3개. (P)
- 대안 기호 `or`·`/`·`또는`, 결합 기호 `+`, 순서/인과 기호 `→`, 부위 나열 `·`가 혼용됨. README 작성 규칙과 일치 여부는 기호만으로 확정하지 않음. (P/I)
- 괄호의 쓰임: 브랜드(보톡스(엘러간)), 변형(나보타(희석)), 부위(나보타(교근)), 별칭((골든루틴)), 기전(보톡스(근이완)), 약어 풀이(PIH(시술 후 색소침착)), 코드(동적주름(M1)), 고지((개인차 있음)). (P)
- products 배열은 24개 패키지 모두 원소 1개이며 그 안에 결합·대안이 문자열로 들어 있음. (P)
- 같은 원장 안 어조 차이: 일부 항목(P3-4·P5-2·P11-2·P9-2 일부)은 유보·근거 수준 고지, 다수는 단정적 상담 문구. (P/I)
- M코드·TXA 등은 이 원장 안에 정의가 없음 — 다른 원장과의 연결은 후속(F).

## 다른 산출물

- `source-map.json` 전체 노드·구간·바이트 · `morphology.json` 형태소·제외·K · `expressions.json` 표현·문장 · `coverage.json` 구획 소유 · `issues.md` 미결 · `validation.md` 검증 · `progress.md` 진행 · `manual/S*.json` 구획별 직접 읽기 기록
