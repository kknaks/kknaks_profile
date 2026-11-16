# S10 — /categories/M10

[← review.md 목차](./review.md)

- 읽기 상태: read_direct · 마지막 읽은 Pointer `/categories/M10/effects`
- 공동 참조 문맥(소유 아님): `/source_method`, `/accuracy_summary`, `/categories/M10/name`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 JSON 리터럴 그대로다(이스케이프 포함). 관찰은 이 표에 섞지 않고 §2 에 둔다. 표현 ID 는 expressions.json.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/M10` | M10 | object | (object, 자식 4) | 70478–70551 |  |  |
| `/categories/M10/name` | name | string | "HIFEM/HIFES and EMS" | 70486–70507 | excluded | E0540, E0541 |
| `/categories/M10/moa` | moa | array | (array, 자식 0) | 70514–70516 |  |  |
| `/categories/M10/adverse_effects` | adverse_effects | array | (array, 자식 0) | 70535–70537 |  |  |
| `/categories/M10/effects` | effects | array | (array, 자식 0) | 70548–70550 |  |  |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

- **S10-O1** [P] `/categories/M10/moa`, `/categories/M10/adverse_effects`, `/categories/M10/effects` — 세 배열 모두 빈 배열.
- **S10-O2** [P] `/categories/M10/name` — name 'HIFEM/HIFES and EMS' — '/' 대안과 'and' 결합이 한 이름에 함께 있음. 약어 풀이 없음.

## 3. 수동 표현 (직접 읽기에서 수집)

| 표현 ID | Pointer | 구간 | 원문 구절 | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0540 | `/categories/M10/name` | 0–11 | HIFEM/HIFES | name_candidate, alternative_list | P |  |
| E0541 | `/categories/M10/name` | 12–19 | and EMS | name_candidate, conjunction | P |  |

## 4. 미결

- **S10-B1** [B] `/categories/M10/moa`, `/categories/M10/adverse_effects`, `/categories/M10/effects` — 진술 0개. 약어(HIFEM·HIFES·EMS) 풀이도 원장에 없다.
