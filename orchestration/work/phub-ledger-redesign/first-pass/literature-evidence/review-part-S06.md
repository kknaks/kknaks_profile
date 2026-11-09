# S06 — /categories/M6

[← review.md 목차](./review.md)

- 읽기 상태: read_direct · 마지막 읽은 Pointer `/categories/M6/effects`
- 공동 참조 문맥(소유 아님): `/source_method`, `/accuracy_summary`, `/categories/M6/name`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 JSON 리터럴 그대로다(이스케이프 포함). 관찰은 이 표에 섞지 않고 §2 에 둔다. 표현 ID 는 expressions.json.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/M6` | M6 | object | (object, 자식 4) | 35760–35876 |  |  |
| `/categories/M6/name` | name | string | "Autologous fat grafting / lipotransfer for facial rejuvenation" | 35768–35832 | excluded | E0306, E0307 |
| `/categories/M6/moa` | moa | array | (array, 자식 0) | 35839–35841 |  |  |
| `/categories/M6/adverse_effects` | adverse_effects | array | (array, 자식 0) | 35860–35862 |  |  |
| `/categories/M6/effects` | effects | array | (array, 자식 0) | 35873–35875 |  |  |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

- **S06-O1** [P] `/categories/M6/moa`, `/categories/M6/adverse_effects`, `/categories/M6/effects` — moa·adverse_effects·effects 모두 빈 배열. 카테고리 이름만 있다.
- **S06-O2** [P] `/categories/M6/name` — name 'Autologous fat grafting / lipotransfer for facial rejuvenation' — '/' 로 두 명칭 병기, 'for facial rejuvenation' 목적·부위 한정.

## 3. 수동 표현 (직접 읽기에서 수집)

| 표현 ID | Pointer | 구간 | 원문 구절 | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0306 | `/categories/M6/name` | 0–38 | Autologous fat grafting / lipotransfer | name_candidate, alternative_list | P |  |
| E0307 | `/categories/M6/name` | 39–62 | for facial rejuvenation | purpose, anatomy_site | P |  |

## 4. 미결

- **S06-B1** [B] `/categories/M6/moa`, `/categories/M6/adverse_effects`, `/categories/M6/effects` — 진술 0개 — 기전·부작용·효과 근거가 원장에 없다(source_method 상 검증 인용 없는 주장이 제외됐을 가능성은 원문이 개별 확인해 주지 않음).
