# review-part-S0 — 루트 객체·메타데이터(version/updated/description)와 /combos 배열 컨테이너

원본: `orchestration/work/phub-recommend/bronze/phub-ledger/problem-combos.json` sha256 `74453c724800975ef7f3fa8b81546fe69fa014bfbc7a8f7e60c75774c2cf2262`

## 원문 값

원본 컬럼명은 축약하지 않는다. 배열은 원본 순서. 원문 칸에는 원문만 둔다.

| 원본 컬럼명 | 자료형 | 원문 값 | Pointer |
|---|---|---|---|
| `(root)` | object | (object 길이 4, 키 ['version', 'updated', 'description', 'combos']) | `(root)` |
| `version` | string | 1.2 | `/version` |
| `updated` | string | 2026-07-26 | `/updated` |
| `description` | string | Problem별 추천 조합 — 상담 안내와 의료진 참고 정보 통합 | `/description` |
| `combos` | array | (array 길이 8, 키 ) | `/combos` |

## 잠정 관찰 (원문과 분리)

| Pointer | 상태 | 관찰 |
|---|---|---|
| `/version` | P | 버전 문자열 "1.2". 숫자형이 아니라 문자열로 저장됨. |
| `/updated` | P | 날짜형 문자열 "2026-07-26"(ISO 형태). 원장 폴더 README의 1판 스냅샷 시점(10-26)과 다른 값이지만 의미 해석은 하지 않음. |
| `/description` | P | "상담 안내와 의료진 참고 정보 통합" — 한 항목 안에 상담용 문구(salesPitch·upsellHook)와 의료진 참고(clinicalRationale·riskBenefit)가 함께 있다는 원장 자기서술. 필드 역할 분류는 후속 과제(F). |

## 수동 수집 표현 (원문 구간)

| Pointer | 구간 | 원문 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|
| `/description` | [0,14) | Problem별 추천 조합 | 원문 자기서술 | 영문 Problem + 한국어 조사 혼합 |
| `/description` | [17,36) | 상담 안내와 의료진 참고 정보 통합 | 원문 자기서술 |  |

## 이 구획의 미결

이 구획에서 새로 연 미결 없음(공통 미결은 issues.md).

## 알려진 형태소 오분절 (K) — 0건

상세·원시 토큰은 `morphology.json#/known_missegmentations`.

| Pointer | 구간 | 표현 | 원시 토큰 |
|---|---|---|---|
