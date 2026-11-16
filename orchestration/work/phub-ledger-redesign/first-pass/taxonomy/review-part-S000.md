# S000 — 루트 컨테이너

- 읽기 상태: **read** · 마지막 읽은 Pointer `/problem`
- 단위: root
- 상위 문맥(공동 참조·소유 아님): 없음
- 기계 기록: `source-map.json`(section=S000) · `morphology/S000.json` · `expressions.json`(section=S000) · 읽기 렌더 `reading/S000.txt`

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `(루트)` | (루트) | object | {object, 키 2: modality, problem} |
| `/modality` | modality | array | [array, 원소 17] |
| `/problem` | problem | array | [array, 원소 14] |

## 잠정 관찰 (원문 아님 · 직접 읽기 기록)

| 상태 | 근거 Pointer | 관찰 |
|---|---|---|
| P | ``, `/modality`, `/problem` | 루트는 modality(시술 계열 측)와 problem(고민 측) 두 배열로 나뉜다. 두 배열의 원소 키 구성이 다르다(modality: id,category,category_en,group,subcategories,extracted,products,name / problem: id,category,category_en,subcategories). 같은 깊이를 같은 개체 유형으로 보지 않는다. |

## 수동 복합 표현 (원문 구간)

(없음)

## 형태소 분석 확인 (알려진 오분절 K)

(없음)

## 미결

(없음)

