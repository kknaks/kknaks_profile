# S17 — /categories/M17

[← review.md 목차](./review.md)

- 읽기 상태: read_direct · 마지막 읽은 Pointer `/categories/M17/effects`
- 공동 참조 문맥(소유 아님): `/source_method`, `/accuracy_summary`, `/categories/M17/name`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 JSON 리터럴 그대로다(이스케이프 포함). 관찰은 이 표에 섞지 않고 §2 에 둔다. 표현 ID 는 expressions.json.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/M17` | M17 | object | (object, 자식 4) | 93552–94599 |  |  |
| `/categories/M17/name` | name | string | "Stem cells and stem cell-derived products" | 93560–93603 | excluded | E0750 |
| `/categories/M17/moa` | moa | array | (array, 자식 0) | 93610–93612 |  |  |
| `/categories/M17/adverse_effects` | adverse_effects | array | (array, 자식 1) | 93631–94585 |  |  |
| `/categories/M17/adverse_effects/0` | [0] | object | (object, 자식 8) | 93632–94584 |  |  |
| `/categories/M17/adverse_effects/0/statement` | statement | string | "Unregulated stem cell products have caused serious adverse events including blindness after intra-ocular injection and tumor formation at ectopic sites." | 93645–93799 | excluded | E0751, E0752, E0753, E0754, E0755, E0756 |
| `/categories/M17/adverse_effects/0/citations` | citations | array | (array, 자식 1) | 93812–94231 |  |  |
| `/categories/M17/adverse_effects/0/citations/0` | [0] | object | (object, 자식 8) | 93813–94230 |  |  |
| `/categories/M17/adverse_effects/0/citations/0/authors` | authors | string | "Kuriyan AE, Albini TA, Townsend JH, Rodriguez M, Pandya HK, Leonard RE 2nd, Parrott MB, Rosenfeld PJ, Flynn HW Jr, Goldberg JL" | 93824–93952 | excluded |  |
| `/categories/M17/adverse_effects/0/citations/0/title` | title | string | "Vision Loss after Intravitreal Injection of Autologous \"Stem Cells\" for AMD." | 93961–94041 | excluded | E0757 |
| `/categories/M17/adverse_effects/0/citations/0/journal` | journal | string | "The New England journal of medicine" | 94052–94089 | excluded |  |
| `/categories/M17/adverse_effects/0/citations/0/year` | year | number_int | 2017 | 94097–94101 | excluded |  |
| `/categories/M17/adverse_effects/0/citations/0/pmid` | pmid | string | "28296617" | 94109–94119 | excluded |  |
| `/categories/M17/adverse_effects/0/citations/0/doi` | doi | string | "10.1056/NEJMoa1609583" | 94126–94149 | excluded |  |
| `/categories/M17/adverse_effects/0/citations/0/pmc` | pmc | string | "PMC5551890" | 94156–94168 | excluded |  |
| `/categories/M17/adverse_effects/0/citations/0/oa_url` | oa_url | string | "https://pmc.ncbi.nlm.nih.gov/articles/PMC5551890/" | 94178–94229 | excluded |  |
| `/categories/M17/adverse_effects/0/accuracy_score` | accuracy_score | number_int | 95 | 94249–94251 | excluded |  |
| `/categories/M17/adverse_effects/0/accuracy_note` | accuracy_note | string | "검증되지 않은 줄기세포 시술은 종양 형성이나 심각한 손상(실명 등) 위험이 있음." | 94268–94315 | applied | E0758, E0759, E0760 |
| `/categories/M17/adverse_effects/0/patient_ko` | patient_ko | string | "검증되지 않은 성분을 잘못 사용할 경우 드물게 시력 손상이나 이상 조직이 생길 위험이 있습니다." | 94329–94384 | applied | E0761, E0762, E0763, E0764, E0765 |
| `/categories/M17/adverse_effects/0/patient_en` | patient_en | string | "Unregulated treatments can lead to very serious and unexpected health concerns." | 94398–94479 | excluded | E0766, E0767, E0768, E0769, E0770 |
| `/categories/M17/adverse_effects/0/patient_zh` | patient_zh | string | "使用未经监管的护理方案可能会导致非常严重且意想不到的健康问题。" | 94493–94526 | excluded |  |
| `/categories/M17/adverse_effects/0/patient_ja` | patient_ja | string | "承認されていない方法での施術は、まれに深刻なお身体への影響が出る恐れがございます。" | 94540–94583 | excluded | E0771 |
| `/categories/M17/effects` | effects | array | (array, 자식 0) | 94596–94598 |  |  |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

- **S17-O1** [P] `/categories/M17/adverse_effects/0/statement` — 'Unregulated stem cell products have caused serious adverse events including blindness after intra-ocular injection and tumor formation at ectopic sites.' — 조건(Unregulated)·정도(serious)·사건 예시 2개 각각 경로/부위 조건(after intra-ocular injection, at ectopic sites).
- **S17-O2** [P] `/categories/M17/adverse_effects/0/citations/0/title` — 인용 제목 'Vision Loss after Intravitreal Injection of Autologous "Stem Cells" for AMD.' — 원문 리터럴에 이스케이프 따옴표. 제목상 안과(AMD) 맥락.
- **S17-O3** [P] `/categories/M17/adverse_effects/0/patient_ko`, `/categories/M17/adverse_effects/0/patient_en`, `/categories/M17/adverse_effects/0/patient_ja` — patient_ko '검증되지 않은 성분을 잘못 사용할 경우 드물게 시력 손상이나 이상 조직이 생길 위험' — '드물게'·'잘못 사용할 경우' 추가, 'stem cell' 이 '성분'으로. patient_en/zh 는 사건 예시를 모두 뺌, ja 'まれに' 추가.
- **S17-O4** [P] `/categories/M17/moa`, `/categories/M17/effects` — moa·effects 빈 배열.

## 3. 수동 표현 (직접 읽기에서 수집)

| 표현 ID | Pointer | 구간 | 원문 구절 | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0750 | `/categories/M17/name` | 0–41 | Stem cells and stem cell-derived products | name_candidate, conjunction | P |  |
| E0751 | `/categories/M17/adverse_effects/0/statement` | 0–30 | Unregulated stem cell products | condition, negation, regulatory | P |  |
| E0753 | `/categories/M17/adverse_effects/0/statement` | 31–65 | have caused serious adverse events | event, degree, evidence_status | P |  |
| E0754 | `/categories/M17/adverse_effects/0/statement` | 76–114 | blindness after intra-ocular injection | event, time, route, anatomy_site | P |  |
| E0756 | `/categories/M17/adverse_effects/0/statement` | 119–151 | tumor formation at ectopic sites | event, anatomy_site | P |  |
| E0757 | `/categories/M17/adverse_effects/0/citations/0/title` | 18–75 | Intravitreal Injection of Autologous "Stem Cells" for AMD | context_scope, route, escaped_quote | P |  |
| E0758 | `/categories/M17/adverse_effects/0/accuracy_note` | 0–16 | 검증되지 않은 줄기세포 시술은 | condition, negation | P |  |
| E0760 | `/categories/M17/adverse_effects/0/accuracy_note` | 17–44 | 종양 형성이나 심각한 손상(실명 등) 위험이 있음 | event, degree, possibility | P |  |
| E0761 | `/categories/M17/adverse_effects/0/patient_ko` | 0–21 | 검증되지 않은 성분을 잘못 사용할 경우 | condition, negation | I | '잘못 사용' 조건 추가 |
| E0764 | `/categories/M17/adverse_effects/0/patient_ko` | 22–52 | 드물게 시력 손상이나 이상 조직이 생길 위험이 있습니다 | frequency, event, possibility | I | statement 에 빈도 없음 |
| E0766 | `/categories/M17/adverse_effects/0/patient_en` | 0–22 | Unregulated treatments | condition, negation, regulatory | P | 읽기 검토(정규식 미포함 후보 대조)에서 추가 |
| E0768 | `/categories/M17/adverse_effects/0/patient_en` | 23–78 | can lead to very serious and unexpected health concerns | possibility, degree | I | 사건 예시 탈락 |
| E0771 | `/categories/M17/adverse_effects/0/patient_ja` | 16–40 | まれに深刻なお身体への影響が出る恐れがございます | frequency, degree, possibility | P |  |

## 4. 미결

- **S17-I1** [I] `/categories/M17/adverse_effects/0/patient_ko`, `/categories/M17/adverse_effects/0/patient_en`, `/categories/M17/adverse_effects/0/patient_ja` — '드물게'·'まれに'·'잘못 사용할 경우' 추가, 사건 예시 탈락. I-LANG.
- **S17-B1** [B] `/categories/M17/adverse_effects/0/statement`, `/categories/M17/moa`, `/categories/M17/effects` — 빈도 없음. 기전·효과 진술 없음.
