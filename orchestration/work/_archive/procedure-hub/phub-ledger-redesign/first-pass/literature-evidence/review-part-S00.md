# S00 — 상위 메타데이터 · /version · /updated · /source_method · /accuracy_summary · /categories 컨테이너

[← review.md 목차](./review.md)

- 읽기 상태: read_direct · 마지막 읽은 Pointer `/accuracy_summary/patient_translations_coverage/ja`
- 공동 참조 문맥(소유 아님): `/source_method`, `/accuracy_summary`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 JSON 리터럴 그대로다(이스케이프 포함). 관찰은 이 표에 섞지 않고 §2 에 둔다. 표현 ID 는 expressions.json.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `(root)` | (root) | object | (object, 자식 5) | 0–94601 |  |  |
| `/version` | version | string | "2.0" | 11–16 | excluded |  |
| `/updated` | updated | string | "2026-09-03" | 27–39 | excluded |  |
| `/source_method` | source_method | string | "Curated successor of v1.0. Citation identity and metadata normalized from NCBI ESummary; unverified citations and claims without verified citations excluded. Clinical claim support requires separate dermatologist review." | 56–278 | excluded | E0001, E0002, E0003, E0004, E0005, E0006, E0007 |
| `/accuracy_summary` | accuracy_summary | object | (object, 자식 8) | 298–823 |  |  |
| `/accuracy_summary/scored_by` | scored_by | string | "Legacy content-quality scores retained for surviving statements; not a clinical claim approval." | 311–408 | excluded | E0008, E0009, E0010 |
| `/accuracy_summary/rubric` | rubric | string | "95-100=교과서 consensus, 85-94=주류 표준, 70-84=뉘앙스 보정, 50-69=근거 약함, 0-49=부정확" | 418–490 | applied | E0011, E0012, E0013, E0014, E0015, E0016, E0017, E0018, E0019, E0020, E0021, E0022, E0023, E0024, E0025 |
| `/accuracy_summary/overall_average` | overall_average | number_float | 95.0 | 509–513 | excluded |  |
| `/accuracy_summary/n_scored` | n_scored | number_int | 17 | 525–527 | excluded |  |
| `/accuracy_summary/by_field_average` | by_field_average | object | (object, 자식 3) | 547–597 |  |  |
| `/accuracy_summary/by_field_average/moa` | moa | number_float | 97.5 | 554–558 | excluded |  |
| `/accuracy_summary/by_field_average/adverse_effects` | adverse_effects | number_float | 95.0 | 577–581 | excluded |  |
| `/accuracy_summary/by_field_average/effects` | effects | number_float | 90.0 | 592–596 | excluded |  |
| `/accuracy_summary/by_category_average` | by_category_average | object | (object, 자식 7) | 620–696 |  |  |
| `/accuracy_summary/by_category_average/M1` | M1 | number_float | 97.5 | 626–630 | excluded |  |
| `/accuracy_summary/by_category_average/M2` | M2 | number_float | 100.0 | 636–641 | excluded |  |
| `/accuracy_summary/by_category_average/M5` | M5 | number_float | 98.0 | 647–651 | excluded |  |
| `/accuracy_summary/by_category_average/M12` | M12 | number_float | 95.0 | 658–662 | excluded |  |
| `/accuracy_summary/by_category_average/M15` | M15 | number_float | 97.5 | 669–673 | excluded |  |
| `/accuracy_summary/by_category_average/M16` | M16 | number_float | 87.5 | 680–684 | excluded |  |
| `/accuracy_summary/by_category_average/M17` | M17 | number_float | 95.0 | 691–695 | excluded |  |
| `/accuracy_summary/patient_ko_coverage` | patient_ko_coverage | string | "119/119" | 719–728 | excluded | E0026 |
| `/accuracy_summary/patient_translations_coverage` | patient_translations_coverage | object | (object, 자식 4) | 761–822 |  |  |
| `/accuracy_summary/patient_translations_coverage/ko` | ko | string | "119/119" | 767–776 | excluded |  |
| `/accuracy_summary/patient_translations_coverage/en` | en | string | "119/119" | 782–791 | excluded |  |
| `/accuracy_summary/patient_translations_coverage/zh` | zh | string | "119/119" | 797–806 | excluded |  |
| `/accuracy_summary/patient_translations_coverage/ja` | ja | string | "119/119" | 812–821 | excluded |  |
| `/categories` | categories | object | (object, 자식 17) | 837–94600 |  |  |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

- **S00-O1** [P] `/source_method` — 원장 스스로 v1.0 의 후속 큐레이션이며 인용 신원·메타데이터는 NCBI ESummary 로 정규화, 검증 안 된 인용·인용 없는 주장은 제외했다고 적는다. 동시에 'Clinical claim support requires separate dermatologist review' — 진술의 임상적 지지는 승인되지 않은 상태라는 원문 자기 한정.
- **S00-O2** [P] `/accuracy_summary/scored_by` — 점수는 'Legacy content-quality scores retained for surviving statements; not a clinical claim approval' — 남은 진술의 옛 품질 점수일 뿐 임상 승인 아님(원문 부정 표현).
- **S00-O3** [P] `/accuracy_summary/rubric` — rubric 은 점수 구간 5개를 '구간=설명' 쉼표 나열로 담은 한 문자열(영어 consensus 혼용). 구간 경계(95-100, 85-94 …)는 범위 표현.
- **S00-O4** [P] `/accuracy_summary/overall_average`, `/accuracy_summary/n_scored`, `/accuracy_summary/by_field_average`, `/accuracy_summary/by_category_average` — accuracy_score 를 가진 진술은 17개(S01~S17 집계)이며 overall 95.0·by_field·by_category 평균이 모두 그 17개로 재현된다(validation.md 재계산). by_category_average 에는 점수 진술이 있는 M1·M2·M5·M12·M15·M16·M17 만 있다.
- **S00-O5** [P] `/accuracy_summary/patient_ko_coverage`, `/accuracy_summary/patient_translations_coverage` — '119/119' 는 진술 수 119 와 일치하며 각 진술에 patient_ko/en/zh/ja 가 모두 있다. 단 coverage 는 값 존재만 뜻하고 번역 충실도는 아니다 — 언어 간 수식·가능성 차이가 다수 관찰됨(각 구획 I 항목).
- **S00-O6** [P] `/categories` — categories 는 M1~M17 17개 키(객체). 각 카테고리는 name·moa·adverse_effects·effects 4키. M6·M10·M11·M13·M14 는 세 배열이 모두 빈 배열.

## 3. 수동 표현 (직접 읽기에서 수집)

| 표현 ID | Pointer | 구간 | 원문 구절 | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0001 | `/source_method` | 0–25 | Curated successor of v1.0 | provenance, version_ref | P |  |
| E0003 | `/source_method` | 27–87 | Citation identity and metadata normalized from NCBI ESummary | provenance | P |  |
| E0004 | `/source_method` | 89–156 | unverified citations and claims without verified citations excluded | negation, condition, provenance | P |  |
| E0007 | `/source_method` | 158–220 | Clinical claim support requires separate dermatologist review. | evidence_status, condition | P |  |
| E0008 | `/accuracy_summary/scored_by` | 0–63 | Legacy content-quality scores retained for surviving statements | provenance | P |  |
| E0009 | `/accuracy_summary/scored_by` | 65–94 | not a clinical claim approval | negation, evidence_status | P |  |
| E0011 | `/accuracy_summary/rubric` | 0–20 | 95-100=교과서 consensus | range, score_band | P |  |
| E0014 | `/accuracy_summary/rubric` | 22–33 | 85-94=주류 표준 | range, score_band | P |  |
| E0017 | `/accuracy_summary/rubric` | 35–47 | 70-84=뉘앙스 보정 | range, score_band | P |  |
| E0020 | `/accuracy_summary/rubric` | 49–60 | 50-69=근거 약함 | range, score_band, degree | P |  |
| E0023 | `/accuracy_summary/rubric` | 62–70 | 0-49=부정확 | range, score_band, negation | P |  |
| E0026 | `/accuracy_summary/patient_ko_coverage` | 0–7 | 119/119 | ratio | P |  |

## 4. 미결

- **S00-K1** [K] `/source_method`, `/accuracy_summary/scored_by` — 영어 텍스트는 Kiwi 적용 제외(K-ENG). 직접 읽기·수동 표현으로만 수식·부정을 수집했다.
- **S00-F1** [F] `/accuracy_summary/rubric` — 점수 구간 설명('뉘앙스 보정' 등)이 진술의 어떤 성질을 평가하는지, 점수가 없는 102개 진술의 상태가 무엇인지는 원문만으로 정해지지 않는다 — 후속 의미 조사.
