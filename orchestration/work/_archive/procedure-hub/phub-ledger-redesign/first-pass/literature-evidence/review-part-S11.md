# S11 — /categories/M11

[← review.md 목차](./review.md)

- 읽기 상태: read_direct · 마지막 읽은 Pointer `/categories/M11/effects`
- 공동 참조 문맥(소유 아님): `/source_method`, `/accuracy_summary`, `/categories/M11/name`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 JSON 리터럴 그대로다(이스케이프 포함). 관찰은 이 표에 섞지 않고 §2 에 둔다. 표현 ID 는 expressions.json.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/M11` | M11 | object | (object, 자식 4) | 70558–70670 |  |  |
| `/categories/M11/name` | name | string | "Fractional radiofrequency microneedling (RF microneedling)" | 70566–70626 | excluded | E0542, E0543 |
| `/categories/M11/moa` | moa | array | (array, 자식 0) | 70633–70635 |  |  |
| `/categories/M11/adverse_effects` | adverse_effects | array | (array, 자식 0) | 70654–70656 |  |  |
| `/categories/M11/effects` | effects | array | (array, 자식 0) | 70667–70669 |  |  |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

- **S11-O1** [P] `/categories/M11/moa`, `/categories/M11/adverse_effects`, `/categories/M11/effects` — 세 배열 모두 빈 배열.
- **S11-O2** [P] `/categories/M11/name` — name 'Fractional radiofrequency microneedling (RF microneedling)' — 괄호는 약칭. M12 'Microneedling … (non-RF)' 와 RF 유무로 구분되는 이름(연결은 후속).

## 3. 수동 표현 (직접 읽기에서 수집)

| 표현 ID | Pointer | 구간 | 원문 구절 | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0542 | `/categories/M11/name` | 0–39 | Fractional radiofrequency microneedling | name_candidate, device | P |  |
| E0543 | `/categories/M11/name` | 40–58 | (RF microneedling) | name_candidate, abbreviation | P |  |

## 4. 미결

- **S11-B1** [B] `/categories/M11/moa`, `/categories/M11/adverse_effects`, `/categories/M11/effects` — 진술 0개.
