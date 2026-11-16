# 실버 빌드 리포트 — ERD v3.3(동결)

입력: 브론즈 22(원장 21 + step1-products.json) 원장은 phub-ledger 판 3 · HASHES.txt 일치 · step1 sha256 ERD 일치 · ERD `erd-v3.3.json` · 사전 `erd-v3.3-dictionaries.json` · 잎 키 행선지 `erd-v3.3-column-map.md`. 결정은 status=approved 만 읽었다. §1~§9 는 이번 빌드 수치, §10~ 은 빌드 차수별 대조.

## 1. 개체별 레코드 수

| 개체 | 레코드 |
|---|---|
| source_file | 22 |
| modality | 17 |
| modality_subcategory | 73 |
| catalog_item | 523 |
| procedure | 669 |
| product | 423 |
| technique | 12 |
| site | 44 |
| anatomical_structure | 36 |
| problem | 14 |
| problem_subcategory | 53 |
| complaint | 121 |
| package | 230 |
| adverse_effect | 269 |
| person_condition | 310 |
| citation | 313 |
| evidence_statement | 119 |
| clinical_rule | 139 |
| conflict | 1119 |
| decision | 505 |
| post_procedure_timeline | 10 |
| emergency_sign | 52 |

## 2. 관계별 엣지 수

| 관계 | 엣지 | 비고 |
|---|---|---|
| R1 | 74 |  |
| R2 | 523 |  |
| R3 | 245 |  |
| R4 | 556 |  |
| R5 | 25 |  |
| R6 | 53 |  |
| R7 | 232 |  |
| R8 | 105 |  |
| R9 | 594 |  |
| R10 | 21 |  |
| R11 | 12 |  |
| R12 | 488 |  |
| R13 | 32 |  |
| R14 | 146 |  |
| R15 | 2479 |  |
| R16 | 514 |  |
| R17 | 20 |  |
| R18 | 146 |  |
| R19 | 378 |  |
| R20 | 119 |  |
| R21 | 45 |  |
| R22 | 22 |  |
| R23 | 53 | conflict → target(target_id 있는 것만) |
| R24 | 273 | 결정(approved) → 대상 |
| R25 | 4387 | 레코드 × 원장 파일(값 단위 provenance 는 레코드의 provenance[]) |
| R26 | 523 |  |
| R27 | 663 | 튜플 → what |
| R28 | 64 | 튜플 → site(none 제외) |
| R30 | 3 | 결정 edge_create 로만 — 1차 0 |
| R31 | 54 | 부작용 → site · 상대 부위(사전 값) |
| R32 | 112 |  |
| R33 | 10 |  |
| R34 | 366 |  |
| R35 | 69 |  |
| R36 | 0 |  |

## 3. 충돌 — kind · 규칙 · 상태

| kind | rule | status | 건 |
|---|---|---|---|
| duplicate_candidate | ⑦ | open | 326 |
| duplicate_candidate | ⑦ | resolved | 23 |
| unregistered_value | ⑧ | open | 480 |
| unresolved_reference | ⑨ | open | 240 |
| value_conflict | ④ | auto_resolved_by_trust | 1 |
| value_conflict | ⑥ | open | 49 |

합계 1119 · ⑦⑧⑨ 1069

## 4. gate 목록

| 목록 | 건 |
|---|---|
| unresolved_references (⑨) | 240 |
| unregistered_fragments (⑧ · 조각+사전 밖 값) | 480 |
| unlinked_phrases (문구 사전 unlinked 항목 · 자리) | 0 · 자리 0 |
| catalog_partial (항목 자신 시술) | 251 |
| conflicts.md ⑦ duplicate_candidate | 349 |
| conflicts.md ⑥ open | 49 |
| conflicts.md ④ auto | 1 |

## 5. ERD 실측(erd-v3.3-tuples.json) 대조 — 결정 ⓪~⑦ 적용 전 분해(ERD 사전 · 시술 · 부작용 단위·문구 사전 · 조건 단위)

키 171 · 차이 **0**. 대표 수치:

| 축 | 키 | 빌드 | ERD 실측 | 대조 |
|---|---|---|---|---|
| procedure | catalog_items | 523 | 523 | 같음 |
| procedure | catalog_distinct_tuples | 523 | 523 | 같음 |
| procedure | reference_total | {"n": 367, "tuple": 169, "multi_tuple": 4, "combo_ref": 0, "node": 9, "unresolved": 185, "none": 0, "complete": 173, "pa | {"n": 367, "tuple": 169, "multi_tuple": 4, "combo_ref": 0, "node": 9, "unresolved": 185, "none": 0, "complete": 173, "pa | 같음 |
| procedure | market_pricing | {"n": 122, "tuple": 16, "multi_tuple": 0, "combo_ref": 0, "node": 0, "unresolved": 106, "none": 0, "complete": 16, "part | {"n": 122, "tuple": 16, "multi_tuple": 0, "combo_ref": 0, "node": 0, "unresolved": 106, "none": 0, "complete": 16, "part | 같음 |
| procedure | tuples_total | 610 | 610 | 같음 |
| procedure | tuples_status | {"partial": 322, "complete": 288} | {"partial": 322, "complete": 288} | 같음 |
| procedure | edge_ends_total | {"procedure": 2058, "modality": 953, "subcategory": 62, "product": 318, "unresolved": 185} | {"procedure": 2058, "modality": 953, "subcategory": 62, "product": 318, "unresolved": 185} | 같음 |
| procedure | edge_ends_total_n | 3576 | 3576 | 같음 |
| procedure | unregistered_distinct | 558 | 558 | 같음 |
| procedure | unregistered_total | 818 | 818 | 같음 |
| adverse | complications_names | 65 | 65 | 같음 |
| adverse | units_total | 333 | 333 | 같음 |
| adverse | units_created_by_phrases | 289 | 289 | 같음 |
| adverse | edges_total | 2480 | 2480 | 같음 |
| condition | units_total | 310 | 310 | 같음 |
| condition | units_dict | 100 | 100 | 같음 |
| condition | units_raw | 210 | 210 | 같음 |
| condition | unregistered_distinct | 497 | 497 | 같음 |
| condition | unregistered_total | 1485 | 1485 | 같음 |
| procedure | tuple_ids(순서 포함) | 610 | 610 | 같음 |
| adverse | tuple_ids(순서 포함) | 333 | 333 | 같음 |
| adverse | complications(locator·단위) | 65 | 65 | 같음 |
| adverse | phrase_dictionary(PHR·status·단위) | 530 | 530 | 같음 |
| adverse | R15 edges(출발·단위·경과·문구) | 2480 | 2480 | 같음 |
| condition | unit_ids(순서 포함) | 310 | 310 | 같음 |
| procedure | catalog(항목→튜플·상태) | 523 | 523 | 같음 |

전부 같다 — 분해 모듈(lib/decompose.py · lib/adverse31.py)이 참조 구현 erd-v3.1-tuples.py 와 같은 튜플·단위·문구 사전 항목·조건 단위·같은 id·같은 등록 순서를 낸다(행 단위 대조 포함).

결정 적용 뒤(실버 산출물) 수치는 적용된 결정만큼 다를 수 있다 — 이번 빌드에서 값을 바꾼(applied) 결정 318 건: DEC-2026-11-05-B3-EXO-02A(product_reclassify ⓪), DEC-2026-11-05-B3-EXO-02B(product_reclassify ⓪), DEC-2026-11-04-B1-PRD-001(dictionary_add ①), DEC-2026-11-04-B1-PRD-002(dictionary_add ①), DEC-2026-11-04-B1-PRD-003(dictionary_add ①), DEC-2026-11-04-B1-PRD-004(dictionary_add ①), DEC-2026-11-04-B1-PRD-005(dictionary_add ①), DEC-2026-11-04-B1-PRD-006(dictionary_add ①), DEC-2026-11-04-B1-PRD-007(dictionary_add ①), DEC-2026-11-04-B1-PRD-008(dictionary_add ①), DEC-2026-11-04-B1-PRD-009(dictionary_add ①), DEC-2026-11-04-B1-PRD-010(dictionary_add ①), DEC-2026-11-04-B1-PRD-011(dictionary_add ①), DEC-2026-11-04-B1-PRD-012(dictionary_add ①), DEC-2026-11-04-B1-PRD-013(dictionary_add ①), DEC-2026-11-04-B1-PRD-014(dictionary_add ①), DEC-2026-11-04-B1-PRD-015(dictionary_add ①), DEC-2026-11-04-B1-PRD-016(dictionary_add ①), DEC-2026-11-04-B1-PRD-017(dictionary_add ①), DEC-2026-11-04-B1-PRD-018(dictionary_add ①), DEC-2026-11-04-B1-PRD-019(dictionary_add ①), DEC-2026-11-04-B1-PRD-020(dictionary_add ①), DEC-2026-11-04-B1-PRD-021(dictionary_add ①), DEC-2026-11-04-B1-PRD-022(dictionary_add ①), DEC-2026-11-04-B1-PRD-023(dictionary_add ①), DEC-2026-11-04-B1-PRD-024(dictionary_add ①), DEC-2026-11-04-B1-PRD-025(dictionary_add ①), DEC-2026-11-04-B1-PRD-026(dictionary_add ①), DEC-2026-11-04-B1-PRD-027(dictionary_add ①), DEC-2026-11-04-B1-PRD-028(dictionary_add ①), DEC-2026-11-04-B1-PRD-029(dictionary_add ①), DEC-2026-11-04-B1-PRD-030(dictionary_add ①), DEC-2026-11-04-B1-PRD-031(dictionary_add ①), DEC-2026-11-04-B1-PRD-032(dictionary_add ①), DEC-2026-11-04-B1-PRD-033(dictionary_add ①), DEC-2026-11-04-B1-PRD-034(dictionary_add ①), DEC-2026-11-04-B1-PRD-035(dictionary_add ①), DEC-2026-11-04-B1-PRD-036(dictionary_add ①), DEC-2026-11-04-B1-PRD-037(dictionary_add ①), DEC-2026-11-04-B1-PRD-038(dictionary_add ①), DEC-2026-11-04-B1-PRD-039(dictionary_add ①), DEC-2026-11-04-B1-PRD-040(dictionary_add ①), DEC-2026-11-04-B1-PRD-041(dictionary_add ①), DEC-2026-11-04-B1-PRD-042(dictionary_add ①), DEC-2026-11-04-B1-PRD-043(dictionary_add ①), DEC-2026-11-04-B1-PRD-044(dictionary_add ①), DEC-2026-11-04-B1-PRD-045(dictionary_add ①), DEC-2026-11-04-B1-PRD-046(dictionary_add ①), DEC-2026-11-04-B1-PRD-047(dictionary_add ①), DEC-2026-11-04-B1-PRD-048(dictionary_add ①), DEC-2026-11-04-B1-PRD-049(dictionary_add ①), DEC-2026-11-04-B1-PRD-050(dictionary_add ①), DEC-2026-11-04-B1-PRD-051(dictionary_add ①), DEC-2026-11-04-B1-PRD-052(dictionary_add ①), DEC-2026-11-04-B1-PRD-053(dictionary_add ①), DEC-2026-11-04-B1-PRD-054(dictionary_add ①), DEC-2026-11-04-B1-PRD-055(dictionary_add ①), DEC-2026-11-04-B1-PRD-056(dictionary_add ①), DEC-2026-11-04-B1-PRD-057(dictionary_add ①), DEC-2026-11-04-B1-PRD-058(dictionary_add ①), DEC-2026-11-04-B1-PRD-059(dictionary_add ①), DEC-2026-11-04-B1-PRD-060(dictionary_add ①), DEC-2026-11-04-B1-PRD-061(dictionary_add ①), DEC-2026-11-04-B1-PRD-062(dictionary_add ①), DEC-2026-11-04-B1-PRD-063(dictionary_add ①), DEC-2026-11-04-B1-PRD-064(dictionary_add ①), DEC-2026-11-04-B1-PRD-065(dictionary_add ①), DEC-2026-11-04-B1-PRD-066(dictionary_add ①), DEC-2026-11-04-B1-PRD-067(dictionary_add ①), DEC-2026-11-04-B1-PRD-068(dictionary_add ①), DEC-2026-11-04-B1-PRD-069(dictionary_add ①), DEC-2026-11-04-B1-PRD-070(dictionary_add ①), DEC-2026-11-04-B1-PRD-071(dictionary_add ①), DEC-2026-11-04-B1-PRD-072(dictionary_add ①), DEC-2026-11-04-B1-PRD-073(dictionary_add ①), DEC-2026-11-04-B1-PRD-074(dictionary_add ①), DEC-2026-11-04-B1-PRD-075(dictionary_add ①), DEC-2026-11-04-B1-PRD-076(dictionary_add ①), DEC-2026-11-04-B1-PRD-077(dictionary_add ①), DEC-2026-11-04-B1-PRD-078(dictionary_add ①), DEC-2026-11-04-B1-PRD-079(dictionary_add ①), DEC-2026-11-04-B1-PRD-080(dictionary_add ①), DEC-2026-11-04-B1-PRD-081(dictionary_add ①), DEC-2026-11-04-B1-PRD-082(dictionary_add ①), DEC-2026-11-04-B1-PRD-083(dictionary_add ①), DEC-2026-11-04-B1-PRD-084(dictionary_add ①), DEC-2026-11-04-B1-PRD-085(dictionary_add ①), DEC-2026-11-04-B1-PRD-086(dictionary_add ①), DEC-2026-11-04-B1-PRD-087(dictionary_add ①), DEC-2026-11-04-B1-PRD-088(dictionary_add ①), DEC-2026-11-04-B1-PRD-089(dictionary_add ①), DEC-2026-11-04-B1-PRD-090(dictionary_add ①), DEC-2026-11-04-B1-PRD-091(dictionary_add ①), DEC-2026-11-04-B1-PRD-092(dictionary_add ①), DEC-2026-11-04-B1-PRD-093(dictionary_add ①), DEC-2026-11-04-B1-PRD-094(dictionary_add ①), DEC-2026-11-04-B1-PRD-095(dictionary_add ①), DEC-2026-11-04-B1-PRD-096(dictionary_add ①), DEC-2026-11-04-B1-PRD-097(dictionary_add ①), DEC-2026-11-04-B1-PRD-098(dictionary_add ①), DEC-2026-11-04-B1-PRD-099(dictionary_add ①), DEC-2026-11-04-B1-PRD-100(dictionary_add ①), DEC-2026-11-04-B1-PRD-101(dictionary_add ①), DEC-2026-11-04-B1-PRD-102(dictionary_add ①), DEC-2026-11-04-B1-PRD-103(dictionary_add ①), DEC-2026-11-04-B1-PRD-104(dictionary_add ①), DEC-2026-11-04-B1-PRD-105(dictionary_add ①), DEC-2026-11-04-B1-PRD-106(dictionary_add ①), DEC-2026-11-04-B1-PRD-107(dictionary_add ①), DEC-2026-11-04-B1-PRD-108(dictionary_add ①), DEC-2026-11-04-B1-PRD-109(dictionary_add ①), DEC-2026-11-04-B1-PRD-110(dictionary_add ①), DEC-2026-11-04-B1-PRD-111(dictionary_add ①), DEC-2026-11-04-B1-PRD-112(dictionary_add ①), DEC-2026-11-04-B1-PRD-113(dictionary_add ①), DEC-2026-11-04-B1-PRD-114(dictionary_add ①), DEC-2026-11-04-B1-PRD-115(dictionary_add ①), DEC-2026-11-04-B1-PRD-116(dictionary_add ①), DEC-2026-11-04-B1-PRD-117(dictionary_add ①), DEC-2026-11-04-B1-PRD-118(dictionary_add ①), DEC-2026-11-04-B1-PRD-119(dictionary_add ①), DEC-2026-11-04-B1-PRD-120(dictionary_add ①), DEC-2026-11-04-B1-PRD-121(dictionary_add ①), DEC-2026-11-04-B1-PRD-122(dictionary_add ①), DEC-2026-11-04-B1-PRD-123(dictionary_add ①), DEC-2026-11-04-B1-PRD-124(dictionary_add ①), DEC-2026-11-04-B1-PRD-125(dictionary_add ①), DEC-2026-11-04-B1-PRD-126(dictionary_add ①), DEC-2026-11-04-B1-PRD-127(dictionary_add ①), DEC-2026-11-04-B1-PRD-128(dictionary_add ①), DEC-2026-11-04-B1-PRD-129(dictionary_add ①), DEC-2026-11-04-B1-PRD-130(dictionary_add ①), DEC-2026-11-04-B1-PRD-131(dictionary_add ①), DEC-2026-11-04-B1-PRD-132(dictionary_add ①), DEC-2026-11-04-B1-PRD-133(dictionary_add ①), DEC-2026-11-04-B1-PRD-134(dictionary_add ①), DEC-2026-11-04-B1-PRD-135(dictionary_add ①), DEC-2026-11-04-B1-PRD-136(dictionary_add ①), DEC-2026-11-04-B1-PRD-137(dictionary_add ①), DEC-2026-11-04-B1-PRD-138(dictionary_add ①), DEC-2026-11-04-B1-PRD-139(dictionary_add ①), DEC-2026-11-04-B1-PRD-140(dictionary_add ①), DEC-2026-11-04-B1-PRD-141(dictionary_add ①), DEC-2026-11-04-B1-PRD-142(dictionary_add ①), DEC-2026-11-04-B1-PRD-143(dictionary_add ①), DEC-2026-11-04-B1-PRD-144(dictionary_add ①), DEC-2026-11-04-B1-PRD-145(dictionary_add ①), DEC-2026-11-04-B1-PRD-146(dictionary_add ①), DEC-2026-11-04-B1-PRD-147(dictionary_add ①), DEC-2026-11-04-B1-PRD-148(dictionary_add ①), DEC-2026-11-04-B1-PRD-149(dictionary_add ①), DEC-2026-11-04-B1-PRD-150(dictionary_add ①), DEC-2026-11-04-B1-PRD-151(dictionary_add ①), DEC-2026-11-04-B1-PRD-152(dictionary_add ①), DEC-2026-11-04-B1-PRD-153(dictionary_add ①), DEC-2026-11-04-B1-PRD-154(dictionary_add ①), DEC-2026-11-04-B1-PRD-155(dictionary_add ①), DEC-2026-11-04-B1-PRD-156(dictionary_add ①), DEC-2026-11-04-B1-PRD-157(dictionary_add ①), DEC-2026-11-04-B1-PRD-158(dictionary_add ①), DEC-2026-11-04-B1-PRD-159(dictionary_add ①), DEC-2026-11-04-B1-PRD-160(dictionary_add ①), DEC-2026-11-04-B1-PRD-161(dictionary_add ①), DEC-2026-11-04-B1-PRD-162(dictionary_add ①), DEC-2026-11-04-B1-PRD-163(dictionary_add ①), DEC-2026-11-04-B1-PRD-164(dictionary_add ①), DEC-2026-11-04-B1-PRD-165(dictionary_add ①), DEC-2026-11-04-B1-PRD-166(dictionary_add ①), DEC-2026-11-04-B1-PRD-167(dictionary_add ①), DEC-2026-11-04-B1-PRD-168(dictionary_add ①), DEC-2026-11-04-B1-SYN-001(dictionary_add ①), DEC-2026-11-04-B1-SYN-002(dictionary_add ①), DEC-2026-11-04-B1-SYN-003(dictionary_add ①), DEC-2026-11-04-B1-SYN-004(dictionary_add ①), DEC-2026-11-04-B1-SYN-005(dictionary_add ①), DEC-2026-11-04-B1-SYN-006(dictionary_add ①), DEC-2026-11-04-B1-SYN-007(dictionary_add ①), DEC-2026-11-04-B1-SYN-008(dictionary_add ①), DEC-2026-11-04-B2A-SYN-001(dictionary_add ①), DEC-2026-11-04-B2A-SYN-002(dictionary_add ①), DEC-2026-11-04-B2A-SYN-003(dictionary_add ①), DEC-2026-11-04-B2A-SYN-004(dictionary_add ①), DEC-2026-11-04-B2A-SYN-005(dictionary_add ①), DEC-2026-11-04-B2A-SYN-006(dictionary_add ①), DEC-2026-11-04-B2A-SYN-007(dictionary_add ①), DEC-2026-11-05-B3-CAT-01(dictionary_add ①), DEC-2026-11-05-B3-DICT-COURSE-01(dictionary_add ①), DEC-2026-11-05-B3-MFR-01(dictionary_add ①), DEC-2026-11-05-B3-PRD-01(dictionary_add ①), DEC-2026-11-05-B3-PRD-02(dictionary_add ①), DEC-2026-11-05-B3-PRD-03(dictionary_add ①), DEC-2026-11-05-B3-PRD-04(dictionary_add ①), DEC-2026-11-05-B3-SIT-01(dictionary_add ①), DEC-2026-11-05-B3-SIT-02(dictionary_add ①), DEC-2026-11-05-B3-SIT-03(dictionary_add ①), DEC-2026-11-06-B6A-ABB-01(dictionary_add ①), DEC-2026-11-06-B6A-ABB-02(dictionary_add ①), DEC-2026-11-06-B6A-ABB-03(dictionary_add ①), DEC-2026-11-06-B6A-ABB-04(dictionary_add ①), DEC-2026-11-06-B6A-ABB-05(dictionary_add ①), DEC-2026-11-06-B6A-ABB-06(dictionary_add ①), DEC-2026-11-06-B6A-ABB-07(dictionary_add ①), DEC-2026-11-06-B6A-ING-01(dictionary_add ①), DEC-2026-11-06-B6A-ING-02(dictionary_add ①), DEC-2026-11-06-B6A-ING-03(dictionary_add ①), DEC-2026-11-06-B6A-ING-04(dictionary_add ①), DEC-2026-11-06-B6A-ING-05(dictionary_add ①), DEC-2026-11-06-B6A-ING-06(dictionary_add ①), DEC-2026-11-06-B6A-SITE-01(dictionary_add ①), DEC-2026-11-06-B6A-SITE-02(dictionary_add ①), DEC-2026-11-06-B6A-SITE-03(dictionary_add ①), DEC-2026-11-06-B6A-SITE-04(dictionary_add ①), DEC-2026-11-06-B6A-SITE-05(dictionary_add ①), DEC-2026-11-06-B6A-SITE-06(dictionary_add ①), DEC-2026-11-06-B6A-SITE-07(dictionary_add ①), DEC-2026-11-06-B6A-SITE-08(dictionary_add ①), DEC-2026-11-06-B6A-SITE-09(dictionary_add ①), DEC-2026-11-06-B6A-SITE-10(dictionary_add ①), DEC-2026-11-06-B6A-SITE-11(dictionary_add ①), DEC-2026-11-06-B6A-SITE-12(dictionary_add ①), DEC-2026-11-06-B6A-SITE-13(dictionary_add ①), DEC-2026-11-06-B6A-SITE-14(dictionary_add ①), DEC-2026-11-06-B6A-SITE-15(dictionary_add ①), DEC-2026-11-05-B3-REN-01(canonical_rename ①), DEC-2026-11-05-B3-REN-02(canonical_rename ①), DEC-2026-11-06-B6A-SFX-06(canonical_rename ①), DEC-2026-11-05-B3-EXO-06(dictionary_remove ①), DEC-2026-11-04-B2B-EVS-01(event_split ④), DEC-2026-11-04-B2B-EVS-02(event_split ④), DEC-2026-11-04-B2B-EVS-04(event_split ④), DEC-2026-11-06-B6A-SFX-01(fold_approve ④), DEC-2026-11-06-B6A-SFX-02(fold_approve ④), DEC-2026-11-06-B6A-SFX-03(fold_approve ④), DEC-2026-11-06-B6A-SFX-04(fold_approve ④), DEC-2026-11-06-B6A-SFX-05(fold_approve ④), DEC-2026-11-06-B6A-SFX-07(fold_approve ④), DEC-2026-11-06-B6A-SFX-08(fold_approve ④), DEC-2026-11-06-B6A-SFX-09(fold_approve ④), DEC-2026-11-06-B6A-SFX-10(fold_approve ④), DEC-2026-11-06-B6A-SFX-11(fold_approve ④), DEC-2026-11-06-B6A-SFX-12(fold_approve ④), DEC-2026-11-06-B6A-SFX-13(fold_approve ④), DEC-2026-11-06-B6A-SFX-14(fold_approve ④), DEC-2026-11-06-B6A-SFX-15(fold_approve ④), DEC-2026-11-06-B6A-SFX-16(fold_approve ④), DEC-2026-11-06-B6A-SFX-17(fold_approve ④), DEC-2026-11-06-B6A-SFX-18(fold_approve ④), DEC-2026-11-06-B6A-SFX-19(fold_approve ④), DEC-2026-11-06-B6A-SFX-20(fold_approve ④), DEC-2026-10-26-08(reclassification ⓪), DEC-2026-11-04-B2A-MAP-001(canonical_mapping ②), DEC-2026-11-04-B2B-BTX-01(canonical_mapping ②), DEC-2026-11-04-B2B-TEC-01(canonical_mapping ②), DEC-2026-11-04-B2B-TEC-02(canonical_mapping ②), DEC-2026-11-04-B2B-TEC-03(canonical_mapping ②), DEC-2026-11-04-B2B-TEC-04(canonical_mapping ②), DEC-2026-11-04-B2B-TEC-05(canonical_mapping ②), DEC-2026-11-04-B2B-TEC-07(canonical_mapping ②), DEC-2026-11-04-B2B-TEC-08(canonical_mapping ②), DEC-2026-11-04-B2B-TEC-09(canonical_mapping ②), DEC-2026-11-05-B3-MAP-01(canonical_mapping ②), DEC-2026-11-04-B2B-ISE-01(adverse_tuple_assign ③), DEC-2026-11-04-B2B-PAR-01(adverse_tuple_assign ③), DEC-2026-11-04-B2B-PAR-02(adverse_tuple_assign ③), DEC-2026-11-04-B2B-PAR-03(adverse_tuple_assign ③), DEC-2026-11-04-B2B-PAR-04(adverse_tuple_assign ③), DEC-2026-11-04-B2B-SLS-02(tuple_assign ③), DEC-2026-11-04-B2B-SLS-09(tuple_assign ③), DEC-2026-11-04-B2B-TEV-01(adverse_tuple_assign ③), DEC-2026-11-04-B2B-TEV-02(adverse_tuple_assign ③), DEC-2026-11-04-B2B-TEV-03(adverse_tuple_assign ③), DEC-2026-11-04-B2B-TEV-04(adverse_tuple_assign ③), DEC-2026-11-04-B2B-TEV-05(adverse_tuple_assign ③), DEC-2026-11-04-B2B-TEV-06(adverse_tuple_assign ③), DEC-2026-11-04-B2B-TEV-07(adverse_tuple_assign ③), DEC-2026-11-04-B2B-TEV-08(adverse_tuple_assign ③), DEC-2026-11-04-B2B-TEV-09(adverse_tuple_assign ③), DEC-2026-11-04-B2B-TEV-10(adverse_tuple_assign ③), DEC-2026-11-05-B3-ADV-01(adverse_tuple_assign ③), DEC-2026-11-05-B3-ADV-02(adverse_tuple_assign ③), DEC-2026-11-05-B3-ADV-03(adverse_tuple_assign ③), DEC-2026-11-05-B3-ADV-04(adverse_tuple_assign ③), DEC-2026-11-05-B3-ADV-05(adverse_tuple_assign ③), DEC-2026-11-05-B3-ADV-COURSE-01(adverse_tuple_assign ③), DEC-2026-11-05-B3-ADV-COURSE-02(adverse_tuple_assign ③), DEC-2026-11-05-B3-ADV-COURSE-03(adverse_tuple_assign ③), DEC-2026-11-05-B3-TUP-01(tuple_assign ③), DEC-2026-11-05-B3-TUP-02(tuple_assign ③), DEC-2026-11-05-B3-TUP-03(tuple_assign ③), DEC-2026-11-05-B3-TUP-04(tuple_assign ③), DEC-2026-11-04-B2B-MFC-01(fold_approve ④), DEC-2026-11-04-B2B-MFC-02(fold_approve ④), DEC-2026-11-04-B2B-S3C-01(fold_approve ④), DEC-2026-11-04-B2B-S3C-02(fold_approve ④), DEC-2026-11-04-B2B-S3C-03(fold_approve ④), DEC-2026-11-04-B2B-S3C-04(fold_approve ④), DEC-2026-11-04-B2B-S3C-05(fold_approve ④), DEC-2026-11-04-B2B-S3C-06(fold_approve ④), DEC-2026-11-04-B2B-S3C-07(fold_approve ④), DEC-2026-11-04-B2B-S3C-09(fold_approve ④), DEC-2026-11-04-B2B-S3C-10(fold_approve ④), DEC-2026-11-04-B2B-S3C-11(fold_approve ④), DEC-2026-11-04-B2B-S3C-12(fold_approve ④), DEC-2026-11-04-B2B-S3C-13(fold_approve ④), DEC-2026-11-04-B2B-S3C-14(fold_approve ④), DEC-2026-11-04-B2B-S3C-15(fold_approve ④), DEC-2026-11-04-B2B-S3C-17(fold_approve ④), DEC-2026-11-04-B2B-S3C-18(fold_approve ④), DEC-2026-11-04-B2B-S3C-19(fold_approve ④), DEC-2026-11-04-B2B-S3C-21(fold_approve ④), DEC-2026-11-05-B3-EXO-05A(edge_create ⑤), DEC-2026-11-05-B3-EXO-05B(edge_create ⑤), DEC-2026-11-05-B3-EXO-05C(edge_create ⑤), DEC-2026-11-05-B3-R16-01(edge_create ⑤), DEC-2026-11-05-B3-R16-02(edge_create ⑤), DEC-2026-11-05-B3-R30-01(edge_create ⑤), DEC-2026-11-05-B3-R30-02(edge_create ⑤), DEC-2026-11-05-B3-R30-03(edge_create ⑤). 나머지는 기록만(recorded):

| 결정 | kind | 단계 | 결과 |
|---|---|---|---|
| DEC-2026-11-05-B3-EXO-02A | product_reclassify | ⓪ | applied ·  |
| DEC-2026-11-05-B3-EXO-02B | product_reclassify | ⓪ | applied ·  |
| DEC-2026-11-04-B1-PRD-001 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-002 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-003 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-004 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-005 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-006 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-007 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-008 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-009 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-010 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-011 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-012 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-013 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-014 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-015 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-016 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-017 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-018 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-019 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-020 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-021 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-022 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-023 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-024 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-025 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-026 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-027 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-028 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-029 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-030 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-031 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-032 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-033 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-034 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-035 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-036 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-037 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-038 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-039 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-040 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-041 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-042 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-043 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-044 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-045 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-046 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-047 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-048 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-049 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-050 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-051 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-052 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-053 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-054 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-055 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-056 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-057 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-058 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-059 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-060 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-061 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-062 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-063 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-064 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-065 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-066 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-067 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-068 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-069 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-070 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-071 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-072 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-073 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-074 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-075 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-076 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-077 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-078 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-079 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-080 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-081 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-082 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-083 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-084 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-085 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-086 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-087 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-088 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-089 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-090 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-091 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-092 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-093 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-094 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-095 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-096 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-097 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-098 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-099 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-100 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-101 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-102 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-103 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-104 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-105 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-106 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-107 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-108 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-109 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-110 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-111 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-112 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-113 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-114 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-115 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-116 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-117 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-118 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-119 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-120 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-121 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-122 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-123 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-124 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-125 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-126 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-127 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-128 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-129 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-130 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-131 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-132 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-133 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-134 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-135 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-136 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-137 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-138 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-139 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-140 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-141 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-142 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-143 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-144 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-145 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-146 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-147 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-148 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-149 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-150 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-151 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-152 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-153 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-154 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-155 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-156 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-157 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-158 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-159 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-160 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-161 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-162 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-163 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-164 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-165 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-166 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-167 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-PRD-168 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-SYN-001 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-SYN-002 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-SYN-003 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-SYN-004 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-SYN-005 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-SYN-006 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-SYN-007 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B1-SYN-008 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B2A-SYN-001 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B2A-SYN-002 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B2A-SYN-003 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B2A-SYN-004 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B2A-SYN-005 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B2A-SYN-006 | dictionary_add | ① | applied ·  |
| DEC-2026-11-04-B2A-SYN-007 | dictionary_add | ① | applied ·  |
| DEC-2026-11-05-B3-CAT-01 | dictionary_add | ① | applied ·  |
| DEC-2026-11-05-B3-DICT-COURSE-01 | dictionary_add | ① | applied ·  |
| DEC-2026-11-05-B3-MFR-01 | dictionary_add | ① | applied ·  |
| DEC-2026-11-05-B3-PRD-01 | dictionary_add | ① | applied ·  |
| DEC-2026-11-05-B3-PRD-02 | dictionary_add | ① | applied ·  |
| DEC-2026-11-05-B3-PRD-03 | dictionary_add | ① | applied ·  |
| DEC-2026-11-05-B3-PRD-04 | dictionary_add | ① | applied ·  |
| DEC-2026-11-05-B3-SIT-01 | dictionary_add | ① | applied ·  |
| DEC-2026-11-05-B3-SIT-02 | dictionary_add | ① | applied ·  |
| DEC-2026-11-05-B3-SIT-03 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-ABB-01 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-ABB-02 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-ABB-03 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-ABB-04 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-ABB-05 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-ABB-06 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-ABB-07 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-ING-01 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-ING-02 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-ING-03 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-ING-04 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-ING-05 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-ING-06 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-SITE-01 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-SITE-02 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-SITE-03 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-SITE-04 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-SITE-05 | dictionary_add | ① | applied · 값은 이미 있었다(앞선 결정) — kind·parent 만 채움 |
| DEC-2026-11-06-B6A-SITE-06 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-SITE-07 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-SITE-08 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-SITE-09 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-SITE-10 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-SITE-11 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-SITE-12 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-SITE-13 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-SITE-14 | dictionary_add | ① | applied ·  |
| DEC-2026-11-06-B6A-SITE-15 | dictionary_add | ① | applied ·  |
| DEC-2026-11-05-B3-REN-01 | canonical_rename | ① | applied ·  |
| DEC-2026-11-05-B3-REN-02 | canonical_rename | ① | applied ·  |
| DEC-2026-11-06-B6A-SFX-06 | canonical_rename | ① | applied ·  |
| DEC-2026-11-05-B3-EXO-06 | dictionary_remove | ① | applied ·  |
| DEC-2026-11-04-B2B-EVS-01 | event_split | ④ | applied · 사건 사전을 나누고 부작용 분해를 다시 돌렸다(③ 지정은 다시 적용) |
| DEC-2026-11-04-B2B-EVS-02 | event_split | ④ | applied · 사건 사전을 나누고 부작용 분해를 다시 돌렸다(③ 지정은 다시 적용) |
| DEC-2026-11-04-B2B-EVS-04 | event_split | ④ | applied · 사건 사전을 나누고 부작용 분해를 다시 돌렸다(③ 지정은 다시 적용) |
| DEC-2026-11-06-B6A-SFX-01 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-02 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-03 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-04 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-05 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-07 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-08 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-09 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-10 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-11 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-12 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-13 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-14 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-15 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-16 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-17 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-18 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-19 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-11-06-B6A-SFX-20 | fold_approve | ④ | applied · v3.2(V3.2-0): 원장 사건 노드를 접힐 곳의 동의어로 — 분해가 그 핵심어를 접힐 곳 사건으로 읽는다(단위 id 는 접힐 곳 기준 · ⑦ 닫음) |
| DEC-2026-10-26-08 | reclassification | ⓪ | applied · R2 재배치만 — CAT- id 불변(3-B′) |
| DEC-2026-11-04-B2A-MAP-001 | canonical_mapping | ② | applied · ['REF-ebd2e2d352', 'REF-1882bc8e24', 'REF-16da584a56', 'REF-47bcf3ffcf', 'REF-07845a4790', 'REF-6189269ba0', 'REF-0efc3dbf09', 'REF-3cf0e9f3bb', 'REF-acd058fcc5'] |
| DEC-2026-11-04-B2B-BTX-01 | canonical_mapping | ② | applied · ['REF-9a0f3675e7', 'REF-23605eeac1', 'REF-dec6de5280', 'REF-bed029264d'] |
| DEC-2026-11-04-B2B-TEC-01 | canonical_mapping | ② | applied · ['CAT-6965975e4c', 'CAT-ebf6e7d503', 'CAT-6ffc78adb2', 'CAT-3ecdef5045', 'CAT-aeeecf36e0', 'CAT-e91c5c5f50', 'CAT-fee4877abb', 'CAT-55e95a471c', 'CAT-26d6ad6ad6', 'CAT-d463a63896', 'CAT-151442cf59', 'CAT-5ed7f7728a', 'CAT-7d9aefd9df', 'CAT-33d31ebbc2', 'CAT-dc0e0160e9', 'CAT-ed330d370c', 'CAT-660560ac3d', 'CAT-c5c7ecdaae', 'CAT-0f8dad7ca6', 'CAT-84b578630a', 'CAT-58d2f4a7a9', 'CAT-c665d4c0c7', 'CAT-85fde7a930', 'CAT-b836ff318b', 'CAT-06bb376060', 'CAT-35b8d5974c', 'CAT-0d2eb26819', 'CAT-9aebb2f7df', 'CAT-c62f009141', 'CAT-0400fda6ae'] |
| DEC-2026-11-04-B2B-TEC-02 | canonical_mapping | ② | applied · ['CAT-05d25fb165', 'CAT-96a86bdbe8', 'CAT-43aff21b1f', 'CAT-1a034e89e1', 'CAT-b011d47f18', 'CAT-df4f8b2c22', 'CAT-9aa95e316f', 'CAT-b1afa4c303', 'CAT-630c54a531', 'CAT-1259e70d7b'] |
| DEC-2026-11-04-B2B-TEC-03 | canonical_mapping | ② | applied · ['CAT-7001760b31', 'CAT-d68756b1c5', 'CAT-1daa9211bc', 'CAT-2151698137', 'CAT-f3110392e3', 'CAT-fda48682a7', 'CAT-1ed7eb9a4f'] |
| DEC-2026-11-04-B2B-TEC-04 | canonical_mapping | ② | applied · ['CAT-60470c8529', 'CAT-29f4655d73', 'CAT-de97bf1304', 'CAT-c90daa0e22'] |
| DEC-2026-11-04-B2B-TEC-05 | canonical_mapping | ② | applied · ['CAT-0d46a67493', 'CAT-3c6f31b90c', 'CAT-5065190d26', 'CAT-593a0c1a05', 'CAT-b1078ae328'] |
| DEC-2026-11-04-B2B-TEC-07 | canonical_mapping | ② | applied · ['CAT-eb9d3ba8f5', 'CAT-4a98a1a31a', 'CAT-b6953edd44', 'CAT-874c93774c', 'CAT-816a6ed4c6', 'CAT-1070cb2dca', 'CAT-fb53d4c993', 'CAT-3f7dda4c32', 'CAT-9fb11a8d62', 'CAT-299f742e3b', 'CAT-bad8b16922', 'CAT-d56ec3e196', 'CAT-8439905379', 'CAT-7eba19df59', 'CAT-cac4804755', 'CAT-1796e9553c', 'CAT-c61c69e5cc', 'CAT-d3ef509f6b', 'CAT-51aae881a2', 'CAT-1cb24ec92b', 'CAT-e71e638382', 'CAT-5af92bc234', 'CAT-c5f129c970', 'CAT-1e5867c836', 'CAT-aeabf21b28', 'CAT-959458af36', 'CAT-6891420a64', 'CAT-7b2daa58b9', 'CAT-5d0bf36287'] |
| DEC-2026-11-04-B2B-TEC-08 | canonical_mapping | ② | applied · ['CAT-4839fe2677', 'CAT-593fe618bc', 'CAT-bcd3331375', 'CAT-72d70487d9', 'CAT-16aabd1b2f', 'CAT-a099d43b25', 'CAT-be114529cb', 'CAT-e10b36ed0c', 'CAT-78b1fd3370', 'CAT-8620066867', 'CAT-34310fa1fe', 'CAT-c385fb0dfe', 'CAT-8651227607', 'CAT-9acf01f98a', 'CAT-b8d6d063bb', 'CAT-b86fc1b238', 'CAT-c72c19fc93', 'CAT-c4aab9b063', 'CAT-d2388afd01', 'CAT-3ffbc8e401', 'CAT-3abea35209', 'CAT-577dcf45d7', 'CAT-f7d490261c', 'CAT-7e7346faf1', 'CAT-a9f8c1845c', 'CAT-7fd25fbe8e', 'CAT-d912513a6a', 'CAT-d24d47ec89', 'CAT-e78cb80e2e', 'CAT-4ad500b52d', 'CAT-1b975c02d8', 'CAT-0e8e82baf9', 'CAT-4305fe0023'] |
| DEC-2026-11-04-B2B-TEC-09 | canonical_mapping | ② | applied · ['CAT-83a25f8d92', 'CAT-6930ad2e52', 'CAT-b0449b9a25', 'CAT-01c7237669', 'CAT-a2a8b54851', 'CAT-3c3169984e', 'CAT-000766a064', 'CAT-0158317211', 'CAT-5feac9b5bc', 'CAT-214efe4d6d', 'CAT-ec637df0c8', 'CAT-61e0e476a6', 'CAT-9e4c8fd946', 'CAT-633bdd3dbf', 'CAT-31ac07fe45', 'CAT-428eebe812', 'CAT-deeee2f86b', 'CAT-00864ad58d', 'CAT-034f572396', 'CAT-bd1d93db49', 'CAT-9860292243', 'CAT-663bc994c8', 'CAT-d02cb5f6d2', 'CAT-c94e99a8ed', 'CAT-3555509429', 'CAT-b1d734a953', 'CAT-1bc36de49a', 'CAT-ec97abb2f0', 'CAT-ca288b80ed', 'CAT-f8703c0e47', 'CAT-631aaead00', 'CAT-e323c4b83b', 'CAT-d418c24050', 'CAT-cebb75b22e', 'CAT-4c18f58a27', 'CAT-7e7ea7efb3', 'CAT-524bb22e97', 'CAT-ce22aa045c', 'CAT-5999336fbb', 'CAT-270ae30310', 'CAT-7cdbea8668', 'CAT-8bff5e0102', 'CAT-49044f56a3'] |
| DEC-2026-11-05-B3-MAP-01 | canonical_mapping | ② | applied · ['CAT-6db65700a1'] |
| DEC-2026-11-04-B2B-ISE-01 | adverse_tuple_assign | ③ | applied · v3.2: 이름 단위(raw_name)는 없다 — 이 이름의 단위(홍반, 부종)를 지정 단위로 대체(V3.2-0 · 같은 locator) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-04-B2B-PAR-01 | adverse_tuple_assign | ③ | applied · v3.2: 이름 단위(raw_name)는 없다 — 이 이름의 단위(감각 이상)를 지정 단위로 대체(V3.2-0 · 같은 locator) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-04-B2B-PAR-02 | adverse_tuple_assign | ③ | applied · v3.2: 이름 단위(raw_name)는 없다 — 이 이름의 단위(감각 이상)를 지정 단위로 대체(V3.2-0 · 같은 locator) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-04-B2B-PAR-03 | adverse_tuple_assign | ③ | applied · v3.2: 이름 단위(raw_name)는 없다 — 이 이름의 단위(홍반, 부종)를 지정 단위로 대체(V3.2-0 · 같은 locator) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-04-B2B-PAR-04 | adverse_tuple_assign | ③ | applied · v3.2: 이름 단위(raw_name)는 없다 — 이 이름의 단위(경결, 섬유화)를 지정 단위로 대체(V3.2-0 · 같은 locator) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-04-B2B-SLS-02 | tuple_assign | ③ | applied ·  |
| DEC-2026-11-04-B2B-SLS-09 | tuple_assign | ③ | applied ·  |
| DEC-2026-11-04-B2B-TEV-01 | adverse_tuple_assign | ③ | applied · v3.2: 옛 표현 지정 → 그 자리의 부작용 문구 사전 항목 지도(phrase_map 과 같은 효과 · 같은 정규화형 자리 전부 · 항목 status exact → approved) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-04-B2B-TEV-02 | adverse_tuple_assign | ③ | applied · v3.2: 옛 표현 지정 → 그 자리의 부작용 문구 사전 항목 지도(phrase_map 과 같은 효과 · 같은 정규화형 자리 전부 · 항목 status exact → approved) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-04-B2B-TEV-03 | adverse_tuple_assign | ③ | applied · v3.2: 옛 표현 지정 → 그 자리의 부작용 문구 사전 항목 지도(phrase_map 과 같은 효과 · 같은 정규화형 자리 전부 · 항목 status approved → approved) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-04-B2B-TEV-04 | adverse_tuple_assign | ③ | applied · v3.2: 옛 표현 지정 → 그 자리의 부작용 문구 사전 항목 지도(phrase_map 과 같은 효과 · 같은 정규화형 자리 전부 · 항목 status approved → approved) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-04-B2B-TEV-05 | adverse_tuple_assign | ③ | applied · v3.2: 옛 표현 지정 → 그 자리의 부작용 문구 사전 항목 지도(phrase_map 과 같은 효과 · 같은 정규화형 자리 전부 · 항목 status exact → approved) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-04-B2B-TEV-06 | adverse_tuple_assign | ③ | applied · v3.2: 옛 표현 지정 → 그 자리의 부작용 문구 사전 항목 지도(phrase_map 과 같은 효과 · 같은 정규화형 자리 전부 · 항목 status approved → approved) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-04-B2B-TEV-07 | adverse_tuple_assign | ③ | applied · v3.2: 옛 표현 지정 → 그 자리의 부작용 문구 사전 항목 지도(phrase_map 과 같은 효과 · 같은 정규화형 자리 전부 · 항목 status approved → approved) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-04-B2B-TEV-08 | adverse_tuple_assign | ③ | applied · v3.2: 옛 표현 지정 → 그 자리의 부작용 문구 사전 항목 지도(phrase_map 과 같은 효과 · 같은 정규화형 자리 전부 · 항목 status approved → approved) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-04-B2B-TEV-09 | adverse_tuple_assign | ③ | applied · v3.2: 옛 표현 지정 → 그 자리의 부작용 문구 사전 항목 지도(phrase_map 과 같은 효과 · 같은 정규화형 자리 전부 · 항목 status approved → approved) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-04-B2B-TEV-10 | adverse_tuple_assign | ③ | applied · v3.2: 옛 표현 지정 → 그 자리의 부작용 문구 사전 항목 지도(phrase_map 과 같은 효과 · 같은 정규화형 자리 전부 · 항목 status approved → approved) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-05-B3-ADV-01 | adverse_tuple_assign | ③ | applied · v3.2: 이름 단위(raw_name)는 없다 — 이 이름의 단위(감각 이상)를 지정 단위로 대체(V3.2-0 · 같은 locator) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-05-B3-ADV-02 | adverse_tuple_assign | ③ | applied · v3.2: 이름 단위(raw_name)는 없다 — 이 이름의 단위(감각 이상)를 지정 단위로 대체(V3.2-0 · 같은 locator) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-05-B3-ADV-03 | adverse_tuple_assign | ③ | applied · v3.2: 이름 단위(raw_name)는 없다 — 이 이름의 단위(홍반, 부종)를 지정 단위로 대체(V3.2-0 · 같은 locator) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-05-B3-ADV-04 | adverse_tuple_assign | ③ | applied · v3.2: 이름 단위(raw_name)는 없다 — 이 이름의 단위(괴사, 동상)를 지정 단위로 대체(V3.2-0 · 같은 locator) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-05-B3-ADV-05 | adverse_tuple_assign | ③ | applied · v3.2: 이름 단위(raw_name)는 없다 — 이 이름의 단위(경결)를 지정 단위로 대체(V3.2-0 · 같은 locator) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-05-B3-ADV-COURSE-01 | adverse_tuple_assign | ③ | applied · v3.2: 타임라인 줄은 문구 사전이 아니라 자기 테이블(post_procedure_timeline · V3.2-9) — 옛 표현 지정을 그 줄의 참조(adverse_ref · R34)로 옮기고 경과는 계열 R15 엣지 경과로(지정 단위가 없으면 결정이 세운다) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-05-B3-ADV-COURSE-02 | adverse_tuple_assign | ③ | applied · v3.2: 타임라인 줄은 문구 사전이 아니라 자기 테이블(post_procedure_timeline · V3.2-9) — 옛 표현 지정을 그 줄의 참조(adverse_ref · R34)로 옮기고 경과는 계열 R15 엣지 경과로(지정 단위가 없으면 결정이 세운다) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-05-B3-ADV-COURSE-03 | adverse_tuple_assign | ③ | applied · v3.2: 타임라인 줄은 문구 사전이 아니라 자기 테이블(post_procedure_timeline · V3.2-9) — 옛 표현 지정을 그 줄의 참조(adverse_ref · R34)로 옮기고 경과는 계열 R15 엣지 경과로(지정 단위가 없으면 결정이 세운다) · 옛 네 칸(course_id) → 세 칸 단위 + R15 경과(v3.1 V3.1-9) |
| DEC-2026-11-05-B3-TUP-01 | tuple_assign | ③ | applied ·  |
| DEC-2026-11-05-B3-TUP-02 | tuple_assign | ③ | applied ·  |
| DEC-2026-11-05-B3-TUP-03 | tuple_assign | ③ | applied ·  |
| DEC-2026-11-05-B3-TUP-04 | tuple_assign | ③ | applied ·  |
| DEC-2026-11-04-B2B-MFC-01 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-MFC-02 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-01 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-02 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-03 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-04 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-05 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-06 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-07 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-09 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-10 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-11 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-12 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-13 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-14 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-15 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-16 | fold_approve | ④ | rejected ·  |
| DEC-2026-11-04-B2B-S3C-17 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-18 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-19 | fold_approve | ④ | applied ·  |
| DEC-2026-11-04-B2B-S3C-21 | fold_approve | ④ | applied ·  |
| DEC-2026-11-05-B3-EXO-05A | edge_create | ⑤ | applied ·  |
| DEC-2026-11-05-B3-EXO-05B | edge_create | ⑤ | applied ·  |
| DEC-2026-11-05-B3-EXO-05C | edge_create | ⑤ | applied ·  |
| DEC-2026-11-05-B3-R16-01 | edge_create | ⑤ | applied ·  |
| DEC-2026-11-05-B3-R16-02 | edge_create | ⑤ | applied ·  |
| DEC-2026-11-05-B3-R30-01 | edge_create | ⑤ | applied · 옛 네 칸 adverse_tuple — 경과 미상, 미상 — 이 관계에 경과 자리 없음(단위 세 칸만 · v3.1) |
| DEC-2026-11-05-B3-R30-02 | edge_create | ⑤ | applied · 옛 네 칸 adverse_tuple — 경과 미상, 미상 — 이 관계에 경과 자리 없음(단위 세 칸만 · v3.1) |
| DEC-2026-11-05-B3-R30-03 | edge_create | ⑤ | applied · 옛 네 칸 adverse_tuple — 경과 미상, 미상 — 이 관계에 경과 자리 없음(단위 세 칸만 · v3.1) |
| DEC-2026-10-26-01 | verification_hold | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-10-26-02 | ledger_correction_note | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-10-26-06 | ledger_correction_note | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-10-26-07 | ledger_correction_note | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-01 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-02 | scope_review | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-03 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-04 | scope_review | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-05 | scope_review | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-06 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-07 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-08 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-09 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-10 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-11 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-12 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-13 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-14 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-15 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-16 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-17 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-18 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-19 | conflict_resolution | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-B2B-SLS-01 | scope_review | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-B2B-SLS-04 | scope_review | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-B2B-SLS-05 | scope_review | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-B2B-SLS-06 | scope_review | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-B2B-SLS-07 | scope_review | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-B2B-SLS-10 | scope_review | — | recorded · build_reads=false — 값을 바꾸지 않음 |
| DEC-2026-11-04-B2B-SLS-11 | scope_review | — | recorded · build_reads=false — 값을 바꾸지 않음 |

## 6. 결정 묶음 1 제안 (decisions/proposed/ · status=proposed · 빌드가 읽지 않음)

| 묶음 | 건 |
|---|---|
| 1. 제품 사전 확장 dictionary_add(product_name) | 0 |
|    제외 목록(확인 불가·병원 메뉴명·업체명·kind 밖·근거 없음·이미 원장 등) | 395 |
| 2. 동의어 dictionary_add | 0 |
|    제안하지 않은 조각(근거 없음·둘 이상 후보·이미 사전 값) | 21 |
| 4. 빈 템플릿 | 11 |

제안하지 않은 동의어 조각:
- 「전체얼굴」 — 원장에 그 라벨(「얼굴 전체」류) 문자열이 없다
- 「풀페이스」 — 원장에 그 라벨(「얼굴 전체」류) 문자열이 없다
- 「HIFU」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「RF」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「MTS」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「필링」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「LED」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「토닝」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「크라이오」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「HIFES」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「수액」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「줄기세포」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「CO2」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「Nd:YAG」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「혈관레이저」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「다이오드」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「HA」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「CaHA」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「PLLA」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「PCL」 — 1차 빌드 시술 축 미등록 조각에 없다
- 「PDO」 — 1차 빌드 시술 축 미등록 조각에 없다

제품 제외 목록 사유별: 대표 이름이 이미 사전 product_name 값과 같다(정규화 일치)=174, 허가 건(licenses[])·웹 근거(web URL) locator 없음=71, 이미 원장 제품(product_name 사전)에 닿음=60, 1_identity.kind 「확인 불가」=57, active=false(조사 산출물에서 비활성 항목)=14, 1_identity.kind 「제품(인체조직=6, 1_identity.kind 「병원 메뉴명」=4, 1_identity.kind 「진단 장비」=4, 1_identity.kind 「화장품」=2, 1_identity.kind 「제품(라인)」=1, 1_identity.kind 「업체명」=1, 1_identity.kind 「화장품(원료 성분명)」=1

## 7. ERD 개정 후보 (결정 파일로 만들지 않음)

- **resolve_rules.stopwords**(발주서 결정 묶음 1-3) — 수식어 제외 목록. 1차 빌드 시술 축 미등록 횟수: `회`×0, `차`×0, `터치업`×0, `유지`×0, `집중`×0, `연말`×0, `하반기`×0, `가을`×0, `관리`×0, `케어`×0, `과도한`×0, `빈도`×0. 규칙 데이터 변경이라 ERD 개정(v3) 사안이다.
- **분해 사전 순서에 성분 사전(ingredient_material) 없음** — CaHA·PLLA·PCL·PDO 는 이미 성분 사전 정준값인데 §1.3 사전 순서(product → modality_subcategory → procedure → site → spec → product_tier)에 성분 사전이 없어 미등록 조각이 된다. 동의어 추가로는 안 풀린다.

## 8. 잎 키 행선지 대조 (erd-v3.3-column-map.md 1,072 · 브론즈만/버림 제외)

행선지(개체·엣지·사전) 잎 키 706 중 실버 값·엣지·충돌·사전 출처에 locator 로 닿은 것 703 · 안 닿은 것 3:

| 파일 | 잎 키 | 표적 | 까닭 |
|---|---|---|---|
| extracted.json | {code}.safety.serious | R15(serious) | 값이 null 2(M10·M13) = 미입력(질문 17) — 엣지 없음 |
| procedure-comparison.json | comparisons[].procedures[].asian_skin_note | R12.asian_skin_note | 그 비교 행의 시술 이름이 미해결(⑨) — 끝이 없어 R12 엣지가 없다(⑨ 레코드에 이름 locator) |
| step1-products.json | items[].6_companies.conflicts | conflict | 명시적 빈 목록 384 = 충돌 없음 — 레코드가 생기지 않는다 |

## 9. 해석 보류

- modality_subcategory 식별자: 하위분류 ['M15-7', 'M15-8'] 는 같은 계열·같은 라벨이라 식별자 규칙(계열 코드 + 정규화 label)상 한 레코드 SUB-f7a7d76234 — id 는 alias 로 둘 다 보존(74 → 73)
- ⓪ reclassification: reclassified_to 는 계열(M 코드)만 준다 — 재배치될 하위분류가 결정에 없어 R2 엣지는 원 하위분류에서 두고 reclassified_modality_id·decision_id 속성으로 표시했다(하위분류 지정은 사람 결정 몫)
- R24 erd 끝: scope_review 7 건(DEC-2026-11-04-B2B-SLS-01, DEC-2026-11-04-B2B-SLS-04, DEC-2026-11-04-B2B-SLS-05, DEC-2026-11-04-B2B-SLS-06, DEC-2026-11-04-B2B-SLS-07, DEC-2026-11-04-B2B-SLS-10, DEC-2026-11-04-B2B-SLS-11)의 target.erd_ref 가 ERD 결정 레코드의 erd_ref 가 아니다(§12 `/` 같은 ERD 본문 자리) — erd 노드가 없어 R24 엣지를 만들지 않았다(기록만 kind · 결정 레코드는 decision.jsonl 에 있음)
- 참조 구현 `erd-v3.1-tuples.py` 는 `erd-v3-tuples.py`(→ v2.4 → … · `erd-v1.1-resolve.py`)를 import 한다 — 분해를 옮기려고 그 사슬을 읽었다(이전 실버 설계·값은 읽지 않았다). summary 의 v3 대조 키(adverse.v3_comparison · 수식어 표 v3_unregistered)는 `erd-v3-tuples.json` 을 함께 읽어 같은 값을 만든다(--tuples-prev) · v24_reference_changes 는 참조 구현과 같이 빈 목록.
- same_session_order(treatment-sequence) — ERD 는 modality·modality_subcategory 속성으로만 적었는데 라벨 참조가 시술 튜플로 풀린 3 건(IPL·프락셔널·혈관 @M8)은 그 procedure 레코드의 같은 이름 속성으로 두었다.
- R19 출처 — extracted.json {code}.source(교과서) 는 modality → citation, step1 근거 URL 은 product → citation 으로 이었다(ERD R19 from 은 evidence_statement·clinical_rule 만 적음 · 컬럼 표 비고 「→ R19」를 따름). 문헌 adverse_effects 의 인용은 문구 사전 항목 citations[](v3.1).
- R15 엣지 레코드 — complications 이름 유래는 이름마다(엣지 속성 severity·incidence… 가 이름의 것이라) · 문구 유래는 (출발, 단위) 마다 하나(source_phrases 부록 · course = 그 단위 후보의 경과 합). 참조 구현의 (출발, 단위) distinct 수는 §14 에 함께 적는다.
- clinical_rule 식별자 — ERD §2.18 「kind + 정규화 문장」대로 정규화(norm_v1) 문장으로 계산한다(5차까지는 원문 그대로 해시 — RUL- 값이 바뀐다 · 결정이 RUL- 를 가리키지 않아 영향 없음).
- dictionary_add 의 new_value 모양(canonical, synonyms, category)에 product_name 의 계열 code 자리가 없다 — 제안 파일은 new_value.code 를 더했다(승인 때 확인).
- ⑦ 「procedure-profiles mechanism · 제조사 · purpose_label 유사값 4쌍 = 6」 중 purpose_label 4쌍은 ERD 가 쌍을 적지 않아 만들지 않았다(유사도 판정 금지). regenerative/regeneration(질문 21)과 클래시스/클래시스(Classys)(§3.10 규칙에 걸림)만 레코드.
- conflict.stable_key — ⑧ unregistered_value 는 같은 원장 위치(locator)에 미등록 조각이 여럿이라 {kind, locators} 만으로는 겹친다 → ⑧ 에 한해 stable_key.value(조각)를 더했다. 같은 kind·같은 출처 쌍이 두 규칙에 걸리면(pih 괄호 보충 ⑦ = §3.10 표면형 ⑦) 레코드 하나로 합치고 also 에 둘째 규칙을 남겼다.
- ④ 자동 해결은 같은 사실에 순위가 다른 출처가 있을 때만 생긴다 — 순위가 갈리는 자리는 products.json mfds(2) vs taxonomy mfds(3)와 step1 허가 값(licenses[].source 가 식약처 API 면 2) vs 다른 출처(3)뿐이고, 1차에서 값이 다른 것은 step1 1 건이다(mfds 는 두 출처 값이 다른 제품 0).

해석 보류 12 건.

## 10. 2차 빌드 · 결정 묶음 1 적용

1차 = 결정 묶음 1 적용 전(`baseline/manifest-1차.json` · 같은 빌더로 `decisions/batch1/` 없이 빌드) · 2차 = `decisions/batch1/` approved 176 건 적용(① dictionary_add — 제품 168 · 동의어 8). ③ ERD 실측 대조는 결정 전 분해 기준이라 그대로 차이 0.

### 개체

|  | 1차 | 2차 | 변화 |
|---|---|---|---|
| adverse_effect | 57 | 57 | 0 |
| adverse_expression | 2935 | 2935 | 0 |
| anatomical_structure | 36 | 36 | 0 |
| catalog_item | 521 | 521 | 0 |
| citation | 313 | 313 | 0 |
| clinical_rule | 29 | 29 | 0 |
| complaint | 121 | 121 | 0 |
| conflict | 2852 | 2667 | -185 |
| decision | 35 | 211 | +176 |
| evidence_statement | 87 | 87 | 0 |
| modality | 17 | 17 | 0 |
| modality_subcategory | 73 | 73 | 0 |
| package | 223 | 228 | +5 |
| person_condition | 298 | 298 | 0 |
| problem | 14 | 14 | 0 |
| problem_subcategory | 53 | 53 | 0 |
| procedure | 585 | 631 | +46 |
| product | 385 | 378 | -7 |
| site | 21 | 22 | +1 |
| source_file | 22 | 22 | 0 |
| technique | 12 | 12 | 0 |

### 관계

|  | 1차 | 2차 | 변화 |
|---|---|---|---|
| R1 | 74 | 74 | 0 |
| R2 | 521 | 521 | 0 |
| R3 | 33 | 159 | +126 |
| R4 | 476 | 476 | 0 |
| R5 | 25 | 25 | 0 |
| R6 | 53 | 53 | 0 |
| R7 | 232 | 232 | 0 |
| R8 | 105 | 105 | 0 |
| R9 | 577 | 579 | +2 |
| R10 | 21 | 21 | 0 |
| R11 | 12 | 12 | 0 |
| R12 | 366 | 431 | +65 |
| R13 | 32 | 32 | 0 |
| R14 | 146 | 146 | 0 |
| R15 | 793 | 793 | 0 |
| R16 | 455 | 455 | 0 |
| R17 | 15 | 21 | +6 |
| R18 | 94 | 109 | +15 |
| R19 | 378 | 378 | 0 |
| R20 | 119 | 119 | 0 |
| R21 | 45 | 45 | 0 |
| R22 | 22 | 22 | 0 |
| R23 | 53 | 53 | 0 |
| R24 | 24 | 200 | +176 |
| R25 | 9515 | 9302 | -213 |
| R26 | 521 | 521 | 0 |
| R27 | 585 | 631 | +46 |
| R28 | 10 | 31 | +21 |
| R29 | 685 | 685 | 0 |
| R30 | 0 | 0 | 0 |
| R31 | 2 | 2 | 0 |

### 게이트 4종

|  | 1차 | 2차 | 변화 |
|---|---|---|---|
| unresolved_references | 348 | 302 | -46 |
| unregistered_fragments | 2298 | 2159 | -139 |
| unlinked_expressions | 2156 | 2156 | +0 |
| catalog_partial | 472 | 345 | -127 |

### 충돌 kind 별

|  | 1차 | 2차 | 변화 |
|---|---|---|---|
| ④ value_conflict auto_resolved_by_trust | 1 | 1 | 0 |
| ⑥ value_conflict open | 49 | 49 | 0 |
| ⑦ duplicate_candidate open | 156 | 156 | 0 |
| ⑧ unregistered_value open | 2298 | 2159 | -139 |
| ⑨ unresolved_reference open | 348 | 302 | -46 |

- **제품 385→378**: 제품 사전에 들어간 step1 이름으로 B 규칙 대응이 바뀌어, 따로 있던 survey 레코드 7 개가 사전 제품 레코드로 합쳐졌다(새 id 0 · origin {'ledger': 61, 'survey': 324} → {'ledger': 61, 'survey': 317}).
- **시술 585→631**: 1차 미해결이던 참조·시장가 이름이 새 사전 값(제품·HIFU/RF 등 동의어)으로 풀려 튜플이 됐다 — 참조 자리 튜플 +24 · 시장가 튜플 +22. 분류 항목 튜플은 521→521(항목 자신이 what 인 튜플 478→355, 나머지는 what 이 제품 등 사전 값으로 바뀌었지만 anchor 가 남아 항목마다 하나 — 수는 그대로).

## 11. 3차 빌드 · 결정 묶음 2A

2차 = `baseline/manifest-2차.json`(결정 묶음 1 까지) · 3차 = `decisions/batch2a/` approved 8 건(사용자 2026-11-04 「진행」 — 코디 추천 매핑). ① dictionary_add 7(조각 → 계열·하위분류 동의어) · ② canonical_mapping 1(「HA」 — 계열 힌트 M2 참조 자리에서만). ③ ERD 실측 대조는 결정 전 분해 기준이라 그대로 차이 0.

### 결정별 적용

| 결정 | kind | 단계 | 결과 | 내용 |
|---|---|---|---|---|
| DEC-2026-11-04-B2A-SYN-001 | dictionary_add | ① | applied | modality += 크라이오 |
| DEC-2026-11-04-B2A-SYN-002 | dictionary_add | ① | applied | modality += 수액 |
| DEC-2026-11-04-B2A-SYN-003 | dictionary_add | ① | applied | modality += 줄기세포 |
| DEC-2026-11-04-B2A-SYN-004 | dictionary_add | ① | applied | modality_subcategory_label += 혈관레이저 |
| DEC-2026-11-04-B2A-SYN-005 | dictionary_add | ① | applied | modality_subcategory_label += 다이오드 |
| DEC-2026-11-04-B2A-SYN-006 | dictionary_add | ① | applied | modality += CO2 |
| DEC-2026-11-04-B2A-SYN-007 | dictionary_add | ① | applied | modality += Nd:YAG |
| DEC-2026-11-04-B2A-MAP-001 | canonical_mapping | ② | applied | scope anchor 9 중 튜플로 풀림 4 |

### 게이트 4종

|  | 2차 | 3차 | 변화 |
|---|---|---|---|
| unresolved_references | 302 | 282 | -20 |
| unregistered_fragments | 2159 | 2152 | -7 |
| unlinked_expressions | 2156 | 2156 | +0 |
| catalog_partial | 345 | 345 | +0 |

### 충돌 kind 별

|  | 2차 | 3차 | 변화 |
|---|---|---|---|
| ④ value_conflict auto_resolved_by_trust | 1 | 1 | 0 |
| ⑥ value_conflict open | 49 | 49 | 0 |
| ⑦ duplicate_candidate open | 156 | 156 | 0 |
| ⑧ unregistered_value open | 2159 | 2152 | -7 |
| ⑨ unresolved_reference open | 302 | 282 | -20 |

### 개체

|  | 2차 | 3차 | 변화 |
|---|---|---|---|
| adverse_effect | 57 | 57 | 0 |
| adverse_expression | 2935 | 2935 | 0 |
| anatomical_structure | 36 | 36 | 0 |
| catalog_item | 521 | 521 | 0 |
| citation | 313 | 313 | 0 |
| clinical_rule | 29 | 29 | 0 |
| complaint | 121 | 121 | 0 |
| conflict | 2667 | 2640 | -27 |
| decision | 211 | 219 | +8 |
| evidence_statement | 87 | 87 | 0 |
| modality | 17 | 17 | 0 |
| modality_subcategory | 73 | 73 | 0 |
| package | 228 | 228 | 0 |
| person_condition | 298 | 298 | 0 |
| problem | 14 | 14 | 0 |
| problem_subcategory | 53 | 53 | 0 |
| procedure | 631 | 647 | +16 |
| product | 378 | 378 | 0 |
| site | 22 | 22 | 0 |
| source_file | 22 | 22 | 0 |
| technique | 12 | 12 | 0 |

### 관계

|  | 2차 | 3차 | 변화 |
|---|---|---|---|
| R1 | 74 | 74 | 0 |
| R2 | 521 | 521 | 0 |
| R3 | 159 | 159 | 0 |
| R4 | 476 | 476 | 0 |
| R5 | 25 | 25 | 0 |
| R6 | 53 | 53 | 0 |
| R7 | 232 | 232 | 0 |
| R8 | 105 | 105 | 0 |
| R9 | 579 | 594 | +15 |
| R10 | 21 | 21 | 0 |
| R11 | 12 | 12 | 0 |
| R12 | 431 | 448 | +17 |
| R13 | 32 | 32 | 0 |
| R14 | 146 | 146 | 0 |
| R15 | 793 | 793 | 0 |
| R16 | 455 | 455 | 0 |
| R17 | 21 | 21 | 0 |
| R18 | 109 | 118 | +9 |
| R19 | 378 | 378 | 0 |
| R20 | 119 | 119 | 0 |
| R21 | 45 | 45 | 0 |
| R22 | 22 | 22 | 0 |
| R23 | 53 | 53 | 0 |
| R24 | 200 | 207 | +7 |
| R25 | 9302 | 9261 | -41 |
| R26 | 521 | 521 | 0 |
| R27 | 631 | 647 | +16 |
| R28 | 31 | 36 | +5 |
| R29 | 685 | 685 | 0 |
| R30 | 0 | 0 | 0 |
| R31 | 2 | 2 | 0 |

- **시술 631→647**: 2차 미해결이던 참조·시장가 이름이 새 동의어(크라이오·수액·줄기세포 → 계열 · 혈관레이저·다이오드 → M8 하위분류 · CO2·Nd:YAG → M8 계열)와 「HA」(힌트 M2 자리)로 풀려 튜플이 됐다 — 참조 자리 튜플 +11 · 시장가 튜플 +5. 분류 항목 튜플은 그대로.
- **「HA」 → M2 계열(하위분류 미지정)**: 원장 M2 하위분류에 「HA 필러」 라벨이 없다 — 「국산 HA」(M2-1)·「수입 HA」(M2-2) 둘이라 「HA」 하나로는 가를 근거가 없어 계열 M2 로 읽었다. 계열 힌트 M4 인 참조 자리는 0 이라 M4 「HA (물광)」 결정은 만들지 않았다. 힌트 없는 참조 5 개(원장 자리 8)는 결정 없음(미해결 유지).
- 조각이 풀렸어도 같은 이름에 다른 미등록 조각(「810nm」「볼륨」「프랙셔널」 등)이 남은 참조는 그대로 미해결이다 — 조각 수 감소와 미해결 참조 수 감소가 같지 않다.

## 12. 4차 빌드 · 브론즈 2판 + 결정 묶음 2B

3차 = `baseline/manifest-3차.json`(브론즈 1판 · 결정 묶음 2A 까지) · 4차 = 원장 phub-ledger 판 2(HASHES.txt 검증 · manifest `bronze_version`) + `decisions/batch2b/` approved 57 건(사용자 게이트 답 2026-11-05).

### 결정 묶음 2B 적용

| 결과 | 건 |
|---|---|
| applied | 48 |
| recorded | 7 |
| rejected | 2 |

| kind | applied | recorded | rejected | no_target |
|---|---|---|---|---|
| adverse_tuple_assign | 15 | 0 | 0 | 0 |
| canonical_mapping | 9 | 0 | 0 | 0 |
| event_split | 3 | 0 | 0 | 0 |
| fold_approve | 21 | 0 | 0 | 0 |
| scope_review | 0 | 7 | 0 | 0 |
| tuple_assign | 0 | 0 | 2 | 0 |

거부·대상 없음:

- `DEC-2026-11-04-B2B-SLS-02` tuple_assign — rejected: anchor 또는 지정 값이 실버에 없다
- `DEC-2026-11-04-B2B-SLS-09` tuple_assign — rejected: anchor 또는 지정 값이 실버에 없다

결정을 만들지 않은 답(원장 2판으로 해소):

- `slash-together-or/03` = per_site — 원장 2판에서 이름의 `/` 가 `+` 로 바뀌어 참조 anchor(REF-)가 사라졌다 — 결정을 만들지 않음(원장 2판으로 해소)
- `slash-together-or/08` = per_site — 원장 2판에서 이름의 `/` 가 `+` 로 바뀌어 참조 anchor(REF-)가 사라졌다 — 결정을 만들지 않음(원장 2판으로 해소)
- `slash-together-or/12` = per_site — 원장 2판에서 이름의 `/` 가 `+` 로 바뀌어 참조 anchor(REF-)가 사라졌다 — 결정을 만들지 않음(원장 2판으로 해소)

### 브론즈 2판으로 바뀐 참조

3차 미해결 참조 중 2판에서 원장 이름이 바뀐 것 4 — 그중 해결 0 · 새 이름으로도 미해결 4.

| 3차 anchor | 1판 이름 | 2판 이름 | 4차 |
|---|---|---|---|
| REF-393ecee04b | 보톡스(턱선/광대) | 보톡스(턱선+광대) | 미해결(⑨) REF-6c649b6a74 |
| REF-55c667d515 | 보톡스 이마/미간 | 보톡스 이마+미간 | 미해결(⑨) REF-14e31cbffb |
| REF-9cc2bf84b1 | 필러 팔자/볼 | 필러 팔자+볼 | 미해결(⑨) REF-073838857f |
| REF-e8ed11044f | 필러 볼/턱 | 필러 볼+턱 | 미해결(⑨) REF-11c54d1449 |

- `+` 로 바뀐 이름은 §1.4 조합 규칙상 primary 를 가진 멤버가 하나뿐이라(「보톡스 이마」+「미간」) 조합이 아니라 부위 둘(multi_site) → 여전히 ⑨. 1판 anchor 를 가리키던 per_site 답 3(slash 03·08·12)은 anchor 가 없어 결정을 만들지 않았다 — 새 anchor 에 다시 정하려면 tuple_assign_multi 를 미해결 참조에 적용하는 빌더 보강이 먼저다.

### 게이트 4종

|  | 3차 | 4차 | 변화 |
|---|---|---|---|
| unresolved_references | 282 | 282 | +0 |
| unregistered_fragments | 2152 | 2152 | +0 |
| unlinked_expressions | 2156 | 2158 | +2 |
| catalog_partial | 345 | 344 | -1 |

### 충돌 kind 별

|  | 3차 | 4차 | 변화 |
|---|---|---|---|
| ④ value_conflict auto_resolved_by_trust | 1 | 1 | 0 |
| ⑥ value_conflict open | 49 | 49 | 0 |
| ⑦ duplicate_candidate open | 156 | 156 | 0 |
| ⑧ unregistered_value open | 2152 | 2152 | 0 |
| ⑨ unresolved_reference open | 282 | 282 | 0 |

### 개체

|  | 3차 | 4차 | 변화 |
|---|---|---|---|
| adverse_effect | 57 | 59 | +2 |
| adverse_expression | 2935 | 2935 | 0 |
| anatomical_structure | 36 | 36 | 0 |
| catalog_item | 521 | 521 | 0 |
| citation | 313 | 313 | 0 |
| clinical_rule | 29 | 29 | 0 |
| complaint | 121 | 121 | 0 |
| conflict | 2640 | 2640 | 0 |
| decision | 219 | 276 | +57 |
| evidence_statement | 87 | 87 | 0 |
| modality | 17 | 17 | 0 |
| modality_subcategory | 73 | 73 | 0 |
| package | 228 | 228 | 0 |
| person_condition | 298 | 298 | 0 |
| problem | 14 | 14 | 0 |
| problem_subcategory | 53 | 53 | 0 |
| procedure | 647 | 613 | -34 |
| product | 378 | 378 | 0 |
| site | 22 | 22 | 0 |
| source_file | 22 | 22 | 0 |
| technique | 12 | 12 | 0 |

### 관계

|  | 3차 | 4차 | 변화 |
|---|---|---|---|
| R1 | 74 | 74 | 0 |
| R2 | 521 | 521 | 0 |
| R3 | 159 | 159 | 0 |
| R4 | 476 | 476 | 0 |
| R5 | 25 | 25 | 0 |
| R6 | 53 | 53 | 0 |
| R7 | 232 | 232 | 0 |
| R8 | 105 | 105 | 0 |
| R9 | 594 | 594 | 0 |
| R10 | 21 | 21 | 0 |
| R11 | 12 | 12 | 0 |
| R12 | 448 | 448 | 0 |
| R13 | 32 | 32 | 0 |
| R14 | 146 | 146 | 0 |
| R15 | 793 | 778 | -15 |
| R16 | 455 | 455 | 0 |
| R17 | 21 | 21 | 0 |
| R18 | 118 | 118 | 0 |
| R19 | 378 | 378 | 0 |
| R20 | 119 | 119 | 0 |
| R21 | 45 | 45 | 0 |
| R22 | 22 | 22 | 0 |
| R23 | 53 | 53 | 0 |
| R24 | 207 | 207 | 0 |
| R25 | 9261 | 9261 | 0 |
| R26 | 521 | 521 | 0 |
| R27 | 647 | 613 | -34 |
| R28 | 36 | 36 | 0 |
| R29 | 685 | 673 | -12 |
| R30 | 0 | 0 | 0 |
| R31 | 2 | 3 | +1 |

## 13. 5차 빌드 · ERD v3 + 묶음 3

4차 = `baseline/manifest-4차.json`(ERD v2.4 · 브론즈 2판 · 결정 묶음 2B 까지) · 5차 = ERD **v3**(`erd-v3.json` · `erd-v3-dictionaries.json` · 빌더 V3-1~V3-10) + `decisions/batch3/` approved 30 건(사용자 2026-11-05 · 발주서 `silver-build-5-brief.md`). 제안 `decisions/batch3-proposed/` 은 빌드가 읽지 않는다(목록 `_INDEX.md`). ③ 결정 적용 전 분해 = `erd-v3-tuples.json` 요약 차이 0/166(§5).

### 결정 적용

| 묶음 | applied | recorded | rejected | no_target |
|---|---|---|---|---|
| batch1 | 176 | 0 | 0 | 0 |
| batch2a | 8 | 0 | 0 | 0 |
| batch3 | 30 | 0 | 0 | 0 |
| batch2b | 50 | 7 | 0 | 0 |
| 원장 메모 | 1 | 4 | 0 | 0 |
| _bootstrap | 0 | 19 | 0 | 0 |

| kind(묶음 3) | applied | rejected | no_target |
|---|---|---|---|
| adverse_tuple_assign | 8 | 0 | 0 |
| canonical_mapping | 1 | 0 | 0 |
| canonical_rename | 2 | 0 | 0 |
| dictionary_add | 10 | 0 | 0 |
| edge_create | 5 | 0 | 0 |
| tuple_assign | 4 | 0 | 0 |

거부·대상 없음: 없음.

제안(batch3-proposed · status=proposed · 읽지 않음) 18 건 — `decisions/batch3-proposed/_INDEX.md`.

### 4차에서 거부·미적용이던 것

| 결정·답 | 고른 것 | 4차 | 5차 | 참조 지금 | 어떻게 |
|---|---|---|---|---|---|
| DEC-2026-11-04-B2B-SLS-02 | tuple_assign outer_only | rejected | applied | 「HIFU(슈링크/울쎄라)」 → tuple · alternatives ['슈링크', '울쎄라'] | 자동 해소 — v3 규칙(V3-4 괄호 안 대안)으로 참조가 튜플이 됐고 결정은 그 anchor 에 같은 값을 적용 |
| DEC-2026-11-04-B2B-SLS-09 | tuple_assign outer_only | rejected | applied | 「HIFU(울쎄라/슈링크)」 → tuple · alternatives ['울쎄라', '슈링크'] | 자동 해소 — v3 규칙(V3-4 괄호 안 대안)으로 참조가 튜플이 됐고 결정은 그 anchor 에 같은 값을 적용 |
| slash-together-or/03 | per_site | 결정 안 만듦 | 결정 없음(규칙) | 「보톡스(턱선+광대)」 → multi_tuple · 부위 ['턱선', '광대'] · 튜플 2 | 자동 해소 — V3-4 「무엇을 하나 × 부위 여럿」(같은 what 의 튜플 여럿 · R12 member_mode and · anchor #s<i>) |
| slash-together-or/08 | per_site | 결정 안 만듦 | 결정 없음(규칙) | 「보톡스 이마+미간」 → multi_tuple · 부위 ['이마', '미간'] · 튜플 2 | 자동 해소 — V3-4 「무엇을 하나 × 부위 여럿」(같은 what 의 튜플 여럿 · R12 member_mode and · anchor #s<i>) |
| slash-together-or/12 | per_site | 결정 안 만듦 | 결정 없음(규칙) | 「필러 볼+턱」 → multi_tuple · 부위 ['볼', '턱'] · 튜플 2 | 자동 해소 — V3-4 「무엇을 하나 × 부위 여럿」(같은 what 의 튜플 여럿 · R12 member_mode and · anchor #s<i>) |

### 게이트 4종

|  | 4차 | 5차 | 변화 |
|---|---|---|---|
| unresolved_references | 282 | 260 | -22 |
| unregistered_fragments | 2152 | 2112 | -40 |
| unlinked_expressions | 2158 | 2155 | -3 |
| catalog_partial | 344 | 336 | -8 |

### 충돌 kind 별

|  | 4차 | 5차 | 변화 |
|---|---|---|---|
| ④ value_conflict auto_resolved_by_trust | 1 | 1 | 0 |
| ⑥ value_conflict open | 49 | 49 | 0 |
| ⑦ duplicate_candidate open | 156 | 152 | -4 |
| ⑦ duplicate_candidate resolved | 0 | 4 | +4 |
| ⑧ unregistered_value open | 2152 | 2112 | -40 |
| ⑨ unresolved_reference open | 282 | 260 | -22 |

- **⑦ 닫힘(V3-10)**: duplicate_candidate 156 중 fold_approve 가 닫은 것 **4**(status=resolved · decision_id · 결정별 DEC-2026-11-04-B2B-MFC-01×1, DEC-2026-11-04-B2B-MFC-02×1, DEC-2026-11-04-B2B-S3C-06×1, DEC-2026-11-04-B2B-S3C-07×1) · 4차는 0(규칙 없음). 「쌍의 ⑦」= ⑦ 레코드의 원장 위치가 전부 그 결정의 anchors 위치이고 anchor 둘 이상에 걸친 것 — fold anchor 위치에 하나라도 닿는 open ⑦ 은 13(한쪽이 접는 anchor 밖 표면형이라 결정이 판정한 쌍이 아님 · conflict_close 몫).

### 개체

|  | 4차 | 5차 | 변화 |
|---|---|---|---|
| adverse_effect | 59 | 66 | +7 |
| adverse_expression | 2935 | 2935 | 0 |
| anatomical_structure | 36 | 36 | 0 |
| catalog_item | 521 | 521 | 0 |
| citation | 313 | 313 | 0 |
| clinical_rule | 29 | 29 | 0 |
| complaint | 121 | 121 | 0 |
| conflict | 2640 | 2578 | -62 |
| decision | 276 | 324 | +48 |
| evidence_statement | 87 | 87 | 0 |
| modality | 17 | 17 | 0 |
| modality_subcategory | 73 | 73 | 0 |
| package | 228 | 229 | +1 |
| person_condition | 298 | 298 | 0 |
| problem | 14 | 14 | 0 |
| problem_subcategory | 53 | 53 | 0 |
| procedure | 613 | 645 | +32 |
| product | 378 | 378 | 0 |
| site | 22 | 28 | +6 |
| source_file | 22 | 22 | 0 |
| technique | 12 | 12 | 0 |

### 관계

|  | 4차 | 5차 | 변화 |
|---|---|---|---|
| R1 | 74 | 74 | 0 |
| R2 | 521 | 521 | 0 |
| R3 | 159 | 162 | +3 |
| R4 | 476 | 476 | 0 |
| R5 | 25 | 25 | 0 |
| R6 | 53 | 53 | 0 |
| R7 | 232 | 232 | 0 |
| R8 | 105 | 105 | 0 |
| R9 | 594 | 594 | 0 |
| R10 | 21 | 21 | 0 |
| R11 | 12 | 12 | 0 |
| R12 | 448 | 478 | +30 |
| R13 | 32 | 32 | 0 |
| R14 | 146 | 146 | 0 |
| R15 | 778 | 783 | +5 |
| R16 | 455 | 457 | +2 |
| R17 | 21 | 20 | -1 |
| R18 | 118 | 119 | +1 |
| R19 | 378 | 378 | 0 |
| R20 | 119 | 119 | 0 |
| R21 | 45 | 45 | 0 |
| R22 | 22 | 22 | 0 |
| R23 | 53 | 53 | 0 |
| R24 | 207 | 222 | +15 |
| R25 | 9261 | 9178 | -83 |
| R26 | 521 | 521 | 0 |
| R27 | 613 | 645 | +32 |
| R28 | 36 | 55 | +19 |
| R29 | 673 | 676 | +3 |
| R30 | 0 | 3 | +3 |
| R31 | 3 | 8 | +5 |

### v3 규칙으로 자동 해소된 참조

4차 미해결 참조(⑨ · REF- anchor) 241 중 **v3 규칙만으로** 튜플이 된 것 **14**(묶음 3 없이 · 4차 결정 사전 + ERD v3 규칙으로 다시 분해) · 묶음 3 사전·지정으로 풀린 것 **7** · 남은 것 220.

| 원인(v3 규칙) | 참조 |
|---|---|
| V3-3 stopwords | 8 |
| V3-4 부위 여럿(+ · /) | 3 |
| V3-4 괄호 안 대안 | 2 |
| V3-4 `/` 대안(combo or) | 1 |

| anchor | 라벨 | 4차 사유[조각] | 5차 | 원인 |
|---|---|---|---|---|
| REF-34a10b058f | PRP + MTS 콤보 | unregistered[콤보] | combo_ref «콤보» | V3-3 stopwords |
| REF-919f782e1e | HIFU(울쎄라/슈링크) | combo_outside_fragment[] | tuple {울쎄라,슈링크} | V3-4 괄호 안 대안 |
| REF-db89800cfc | HIFU/RF(하반기) | unregistered[하반기] | combo_ref «하반기» | V3-4 `/` 대안(combo or) |
| REF-84e619bad0 | LED 집중(여름철) | unregistered[집중,여름철] | tuple «집중,여름철» | V3-3 stopwords |
| REF-a5aea36d26 | 바이오스티뮬레이터(유지 1차) | unregistered[유지] | tuple «유지» | V3-3 stopwords |
| REF-14e31cbffb | 보톡스 이마+미간 | multi_site[] | multi_tuple 부위 ['이마', '미간'] | V3-4 부위 여럿(+ · /) |
| REF-b24d3790d9 | 보톡스 터치업 | unregistered[터치업] | tuple «터치업» | V3-3 stopwords |
| REF-a0f2dc8268 | 연말 집중 케어(필링+LED) | unregistered[연말,집중,케어] | combo_ref «연말,집중,케어» | V3-3 stopwords |
| REF-6c5d5b2089 | 연말 특별 관리(필링+LED) | unregistered[연말,특별,관리] | combo_ref «연말,특별,관리» | V3-3 stopwords |
| REF-3204815658 | 필러 터치업 | unregistered[터치업] | tuple «터치업» | V3-3 stopwords |
| REF-554e7d5964 | HIFU(슈링크/울쎄라) | combo_outside_fragment[] | tuple {슈링크,울쎄라} | V3-4 괄호 안 대안 |
| REF-673e1858f4 | IPL(유지) | unregistered[유지] | tuple «유지» | V3-3 stopwords |
| REF-6c649b6a74 | 보톡스(턱선+광대) | multi_site[] | multi_tuple 부위 ['턱선', '광대'] | V3-4 부위 여럿(+ · /) |
| REF-11c54d1449 | 필러 볼+턱 | multi_site[] | multi_tuple 부위 ['볼', '턱'] | V3-4 부위 여럿(+ · /) |

ERD 실측(결정 전 · ERD 사전 · `erd-v3-tuples.json`)의 같은 규칙 효과: `+` 4곳 중 multi_tuple 4(필러 팔자+볼 은 「팔자」 미등록 → 묶음 3 SIT-02 로 해소) · 괄호 안 대안 3 · stopwords 로 새로 튜플이 된 참조 4(결과가 바뀐 참조 21) · 괄호 안 회사·제품 2. 실버(결정 뒤 사전)에서는 묶음 1·2A 의 동의어(HIFU·RF·얼굴 전체 …)가 더해져 괄호 안 대안 5 · multi_tuple 5 · 회사·제품 괄호 라벨 4.

묶음 3 으로 풀린 참조:

| anchor | 라벨 | 4차 사유[조각] | 5차 |
|---|---|---|---|
| REF-83b20e5b6e | PRP (두피) | unregistered[두피] | tuple |
| REF-065677ad2d | 엑소좀 (두피) | unregistered[두피] | tuple |
| REF-aa77bf5d91 | 보톡스 (보툴리눔톡신) | unregistered[보툴리눔톡신] | tuple |
| REF-970cb51b1c | MTS(두피) | unregistered[두피] | tuple |
| REF-0e51b270df | 필러(팔자/볼) | unregistered[팔자] | multi_tuple 부위 ['팔자주름', '볼'] |
| REF-660cd35c4a | 필러 팔자 | unregistered[팔자] | tuple |
| REF-073838857f | 필러 팔자+볼 | unregistered[팔자] | multi_tuple 부위 ['팔자주름', '볼'] |

### 미해결(⑨ open) 사유 · 상위 조각

⑨ open 260(참조 자리 225) · 사유: unregistered=205, 고민 사전 일치 없음(질문 12)=29, multi_primary=18, canonical_category 가 하위분류 사전에 없다(질문 23)=6, combo_outside_fragment=2.

미해결 참조의 미등록 조각 상위 30(참조 수): `바디`×7 · `HA`×7 · `리쥬란`×5 · `지방분해`×4 · `비타민C`×4 · `시술`×4 · `리프팅`×4 · `심부`×4 · `볼륨`×4 · `이모드`×4 · `리프팅기기`×3 · `프랙셔널`×3 · `저출력`×3 · `810nm`×3 · `고주파`×3 · `주사`×3 · `색소`×3 · `복부`×3 · `여드름`×3 · `써마지`×2 · `CO2레이저`×2 · `반영구화장`×2 · `미백주사`×2 · `병변내`×2 · `스테로이드주사`×2 · `제모레이저`×2 · `약물치료`×2 · `모발이식`×2 · `피코레이저`×2 · `미라드라이`×2

### 빌더 v3(V3-1~V3-10) — 이번 빌드 실측

| # | 무엇 | 실측(5차) |
|---|---|---|
| V3-1 | 부작용 수식 칸 qualifier · 네 칸 식별자 · 접두 가름 | 수식 사전 5 · qualifier≠none 단위 0 · 접두 가름 2(공기색전→공기+색전, 혈전정맥염→혈전+정맥염) |
| V3-2 | 괄호 안 회사·제품 | 적용 라벨 4: 「보톡스(엘러간)」→보톡스(회사 앨러간/애브비) · 「엠페이스(EMFACE)」→엠페이스(괄호 안 제품) · 「바이오스티뮬레이터 (쥬베룩볼륨)」→쥬베룩볼륨(괄호 안 제품) · 「바이오스티뮬레이터(쥬베룩)」→쥬베룩(괄호 안 제품) |
| V3-3 | stopwords → qualifier_text · session_index | qualifier_text 참조 21 · session_index 8 · 엣지 속성 R9/R12/R17/R18 qualifier_text 12 |
| V3-4 | `+`/`/` · multi_tuple(#s<i>) · member_mode · alternatives | multi_tuple 5 · 괄호 안 대안 5 · combo_ref member_mode {'or': 5, 'and': 4} |
| V3-5 | site.kind · layer 는 시술 site 금지 | 부위 kind {'anatomical': 21, 'region': 2, 'layer': 5} · 시술 layer site 0 · 부작용 layer 단위 2 |
| V3-6 | canonical_rename | 보톡스→보툴리눔 톡신(DIC-d73ced8043→DIC-70be6aa6e9) · 바이오스티뮬레이터/콜라겐부스터→바이오스티뮬레이터(DIC-18b7f09eb1→DIC-b185cb5a49) |
| V3-7 | description·media_refs | 새 브론즈 원천 0 → 값 0(빌더는 출처 있는 값만 싣는다) |
| V3-8 | R5 하위분류 기법(canonical_mapping R5:<하위분류>) | 적용 0 · 제안 batch3-proposed P-TEC-* |
| V3-9 | 미해결·조합·#s anchor 에도 ③ | 결정이 세운 자리 0 · anchor 부재 거부 0 |
| V3-10 | fold_approve 가 ⑦ 을 닫음 | 4 |

## 14. 6차 빌드 · ERD v3.1 + 엑소좀 approved

5차 = `baseline/manifest-5차.json`(ERD v3 · 결정 묶음 3 approved 24 까지) · 6차 = ERD **v3.1**(`erd-v3.1.json` · `erd-v3.1-dictionaries.json` · 빌더 V3.1-1~10 · 발주서 `silver-build-6-brief.md`) + 엑소좀 EXO-02·05·06 을 v3.1 kind 로 올린 결정 6 건(`decisions/batch3/DEC-2026-11-05-B3-EXO-*` · 사용자 확정 방향). ③ 결정 적용 전 분해 = `erd-v3.1-tuples.json` 요약 차이 0/233(§5 · 시술 · 부작용 · 조건 + 행 대조).

### 결정 적용(6차)

| kind | applied | recorded | rejected | no_target |
|---|---|---|---|---|
| adverse_tuple_assign | 23 | 0 | 0 | 0 |
| canonical_mapping | 11 | 0 | 0 | 0 |
| canonical_rename | 2 | 0 | 0 | 0 |
| conflict_resolution | 0 | 16 | 0 | 0 |
| dictionary_add | 193 | 0 | 0 | 0 |
| dictionary_remove | 1 | 0 | 0 | 0 |
| edge_create | 8 | 0 | 0 | 0 |
| event_split | 3 | 0 | 0 | 0 |
| fold_approve | 21 | 0 | 0 | 0 |
| ledger_correction_note | 0 | 3 | 0 | 0 |
| product_reclassify | 2 | 0 | 0 | 0 |
| reclassification | 1 | 0 | 0 | 0 |
| scope_review | 0 | 10 | 0 | 0 |
| tuple_assign | 6 | 0 | 0 | 0 |
| verification_hold | 0 | 1 | 0 | 0 |

거부·대상 없음: 없음 — 기존 결정(_bootstrap · batch1 · 2a · 2b · 3) 전부 v3.1 빌더가 받았다.

v3.1 로 옮겨 적용한 옛 결정(거부 아님 · 적용 로그 note):

- 옛 네 칸 adverse_tuple_assign(raw_name) 10 — course_id 를 단위에서 빼 그 이름 → 단위 R15 엣지의 course 로(미상은 null) · 상대 부위 site_id 는 none(relative_site_text): `B2B-ISE-01`, `B2B-PAR-01`, `B2B-PAR-02`, `B2B-PAR-03`, `B2B-PAR-04`, `B3-ADV-01`, `B3-ADV-02`, `B3-ADV-03`, `B3-ADV-04`, `B3-ADV-05`
- 옛 adverse_tuple_assign(kind=expression) 13 — 표현은 개체가 아니므로(V3.1-10) 그 자리의 문구 사전 항목 지도로 적용(phrase_map 과 같은 효과 · status=approved · 같은 정규화형 자리 전부): `B2B-TEV-01`→PHR-0d10bd307d, `B2B-TEV-02`→PHR-4db30daf7b, `B2B-TEV-03`→PHR-4db30daf7b, `B2B-TEV-04`→PHR-0d10bd307d, `B2B-TEV-05`→PHR-559472746f, `B2B-TEV-06`→PHR-4db30daf7b, `B2B-TEV-07`→PHR-4db30daf7b, `B2B-TEV-08`→PHR-0d10bd307d, `B2B-TEV-09`→PHR-559472746f, `B2B-TEV-10`→PHR-0d10bd307d, `B3-ADV-COURSE-01`→PHR-f02aa749d6, `B3-ADV-COURSE-02`→PHR-1fd0edfbe0, `B3-ADV-COURSE-03`→PHR-d7c258f5f6
- 옛 네 칸 edge_create(adverse_tuple) 3 — R30 이라 경과 자리 없음(세 칸 끝 · 경과 「미상」 버림 아님 = 원래 null): `B3-R30-01`, `B3-R30-02`, `B3-R30-03`

#### 엑소좀(EXO-02·05·06 · v3.1 kind)

| 결정 | kind | 단계 | 결과 | 내용 |
|---|---|---|---|---|
| EXO-02A | product_reclassify | ⓪ | applied | ASCEplus: M5→M4 · PRD-be57673deb → PRD-e45033395c(옛 id alias) |
| EXO-02B | product_reclassify | ⓪ | applied | EXOSOME SKIN: M5→M4 · PRD-8a1d788eec → PRD-f4264ddf37(옛 id alias) |
| EXO-06 | dictionary_remove | ① | applied | modality 「PRP/자가혈」 동의어 「PRP/엑소좀」 제거 |
| EXO-05A | edge_create | ⑤ | applied | clinical_rule:RUL-dacbdc189b→product:PRD-e45033395c |
| EXO-05B | edge_create | ⑤ | applied | clinical_rule:RUL-dacbdc189b→product:PRD-f4264ddf37 |
| EXO-05C | edge_create | ⑤ | applied | clinical_rule:RUL-dacbdc189b→product:PRD-209656bf00 |

- ② 재분류: R4 5 엣지가 M5 → M4 로 옮겨졌다(reclassified_from_modality · decision_id · section_key 보존). 제품 레코드 id 는 새 PRD-, 옛 id 는 alias.
- ⑤ 임상 규칙: clinical_rule(product_note) 「화장품 허가 (주사 사용 불법)」(`taxonomy.json:modality[].products[].note@4/3`) → R32 3(scope=product · severity=prohibited · basis=edge_create) — ASCEplus · EXOSOME SKIN · 셀엑소좀. 기법=주사 끝은 만들지 않았다(R32 scope=all 은 주사 전체에 걸린다 · 발주서는 제품만).
- ⑥ 「PRP/엑소좀」 M5 동의어 제거 — 효과: treatment-optimization optimal_combo 「PRP/엑소좀」 이 계열 통째 일치가 아니라 `/` 대안(PRP · 엑소좀)으로 분해돼 combo_ref 패키지 +1 · R12 +3, 그리고 그 이름을 그대로 쓰는 원장 계열 레코드 이름 2 곳(market-pricing categories[4].name · procedure-profiles profiles[4].name)이 사전 modality 밖 값 ⑧ 2 로 드러났다(원장 불변 · 판정은 conflict_close 또는 이름 결정).

### 개체

|  | 5차 | 6차 | 변화 | 비고 |
|---|---|---|---|---|
| adverse_effect | 66 | 71 | +5 | 세 칸 단위(V3.1-9) · 문구가 세운 조합 포함 |
| adverse_expression | 2935 | 0 | -2935 | v3.1 삭제(V3.1-10 · 문구 사전) |
| anatomical_structure | 36 | 36 | 0 |  |
| catalog_item | 521 | 521 | 0 |  |
| citation | 313 | 313 | 0 |  |
| clinical_rule | 29 | 139 | +110 | + disclosure(V3.1-7) · product_note(EXO-05) · 식별자 정규화 문장 |
| complaint | 121 | 121 | 0 |  |
| conflict | 2578 | 2818 | +240 | 아래 충돌 표 |
| decision | 324 | 457 | +133 |  |
| evidence_statement | 87 | 87 | 0 |  |
| modality | 17 | 17 | 0 |  |
| modality_subcategory | 73 | 73 | 0 |  |
| package | 229 | 230 | +1 |  |
| person_condition | 298 | 312 | +14 | 조건 단위(V3.1-4 · 사전 + raw_name) |
| problem | 14 | 14 | 0 |  |
| problem_subcategory | 53 | 53 | 0 |  |
| procedure | 645 | 645 | 0 |  |
| product | 378 | 378 | 0 | 엑소좀 2 재분류(id 재계산 · 수 그대로) |
| site | 28 | 28 | 0 |  |
| source_file | 22 | 22 | 0 |  |
| technique | 12 | 12 | 0 |  |

### 관계

|  | 5차 | 6차 | 변화 | 비고 |
|---|---|---|---|---|
| R1 | 74 | 74 | 0 |  |
| R2 | 521 | 521 | 0 |  |
| R3 | 162 | 163 | +1 |  |
| R4 | 476 | 476 | 0 |  |
| R5 | 25 | 25 | 0 |  |
| R6 | 53 | 53 | 0 |  |
| R7 | 232 | 232 | 0 |  |
| R8 | 105 | 105 | 0 |  |
| R9 | 594 | 594 | 0 |  |
| R10 | 21 | 21 | 0 |  |
| R11 | 12 | 12 | 0 |  |
| R12 | 478 | 481 | +3 | session_count(V3.1-5) · EXO-06 combo |
| R13 | 32 | 32 | 0 |  |
| R14 | 146 | 146 | 0 |  |
| R15 | 783 | 1429 | +646 | 이름(이름마다) + 문구((출발, 단위) 마다 · source_phrases) |
| R16 | 457 | 514 | +57 | 끝 = 조건 단위(원칙 B 로 문장 하나가 단위 둘이면 엣지 둘) |
| R17 | 20 | 20 | 0 |  |
| R18 | 119 | 119 | 0 |  |
| R19 | 378 | 346 | -32 | 문헌 adverse_effects 인용은 문구 사전 citations[] |
| R20 | 119 | 87 | -32 | 끝 evidence_statement 만 |
| R21 | 45 | 45 | 0 |  |
| R22 | 22 | 22 | 0 |  |
| R23 | 53 | 53 | 0 |  |
| R24 | 222 | 225 | +3 |  |
| R25 | 9178 | 6419 | -2759 |  |
| R26 | 521 | 521 | 0 |  |
| R27 | 645 | 645 | 0 |  |
| R28 | 55 | 55 | 0 |  |
| R29 | 676 | 0 | -676 | v3.1 삭제 |
| R30 | 3 | 3 | 0 |  |
| R31 | 8 | 14 | +6 | 상대 부위 끝 없음(none) |
| R32 | 0 | 112 | +112 | v3.1 신설 — 고지 ledger + edge_create |

### 게이트

|  | 5차 | 6차 | 비고 |
|---|---|---|---|
| unresolved_references | 260 | 260 |  |
| unregistered_fragments | 2112 | 2352 | ⑧ 부작용 조각은 수식어 목록(V3.1-8)으로 줄고 고지 109 문장의 새 토큰으로 는다 · 조각 행 = (축, 조각) |
| unlinked_expressions→unlinked_phrases | 2155 | 1032 | 표현 레코드(자리) → 문구 사전 unlinked 항목 · 자리 1641 |
| catalog_partial | 336 | 336 |  |

### 충돌 kind 별

|  | 5차 | 6차 | 변화 | 비고 |
|---|---|---|---|---|
| ④ value_conflict auto_resolved_by_trust | 1 | 1 | 0 |  |
| ⑥ value_conflict open | 49 | 49 | 0 |  |
| ⑦ duplicate_candidate open | 152 | 152 | 0 |  |
| ⑦ duplicate_candidate resolved | 4 | 4 | 0 |  |
| ⑧ unregistered_value open | 2112 | 2352 | +240 |  |
| ⑨ unresolved_reference open | 260 | 260 | 0 |  |

### 문구 사전(V3.1-10)

|  | 결정 전(ERD 실측) | 6차(결정 뒤) |
|---|---|---|
| 항목 | 1218 | 1235 |
| status(항목) | unlinked 1033 · auto 185 | unlinked 1032 · auto 197 · approved 6 |
| 문구 자리(고지 포함 · 번역 제외) | 2948 | 2948 |
| 자리 status | unlinked 1637 · auto 1298 · (고지) 109 | unlinked 1641 · auto 1294 · approved 13 |
| 문구가 세운 단위(조합) | 12 | 18 |
| 부록: R15 source_phrases 에 오른 항목 | — | 203 |
| 부록: 게이트 unlinked_phrases | 1033 | 1032 |

결정 뒤 auto 가 는 것은 ① 사전 결정(DICT-COURSE-01 「지속」 · 동의어·부위 추가 등)으로 조각이 사전 값이 된 문구, approved 는 옛 표현 지정(TEV · ADV-COURSE)이 문구 사전 지도로 옮겨진 항목이다. 항목 id(PHR-)는 정규화형 유도라 경과·사전 값이 바뀌면 정규화형이 갈린다(ERD §1.1 S-5 — 지금 approved 항목은 결정 locator 로 다시 찾으므로 끊기지 않는다).

### 단위(V3.1-9 · 사건, 부위, 물질)

단위 71(사전 57 + raw_name 14) — 결정 전(ERD) 61(사전 47 + raw 14). 사건 41 중 조합이 둘 이상인 사건 10 · 하나뿐 31. 문구가 세운 조합 18 · 결정이 세운 단위 2.

| 사건 | 조합 | 단위 (부위 · 물질 · 출처) |
|---|---|---|
| 당김감 | 4 | (none, none) · (눈가:anatomical, none ← 문구) · (이마:anatomical, none ← 문구) · (피부:layer, none ← 문구) |
| 괴사 | 3 | (none, none) · (피부:layer, none) · (피하 지방층:layer, none) |
| 부종 | 3 | (none, none) · (눈가:anatomical, none ← 문구) · (두피:region, none ← 문구) |
| 자극감 | 3 | (none, none) · (두피:region, none ← 문구) · (피부:layer, none ← 문구) |
| 홍반 | 3 | (none, none) · (두피:region, none ← 문구) · (피부:layer, none ← 문구) |
| 비대칭 | 2 | (none, none) · (얼굴:region, none ← 문구) |
| 색전 | 2 | (none, none) · (none, 역행성 ← 문구) |
| 섬유화 | 2 | (none, none) · (사각턱:anatomical, none ← 문구) |
| 정맥염 | 2 | (none, none) · (none, 혈전 ← 문구) |
| 통증 | 2 | (none, none) · (두피:region, none ← 문구) |
| PAH | 1 | (none, none) |
| 감각 이상 | 1 | (none, none) |
| 감염 | 1 | (none, none) |
| 건조 | 1 | (none, none) |
| 결절 | 1 | (none, none) |
| 경결 | 1 | (none, none) |
| 과민반응 | 1 | (none, none ← 문구) |
| 낙설 | 1 | (none, none) |
| 독감 유사 증상 | 1 | (none, none) |
| 동상 | 1 | (none, none) |
| 두통 | 1 | (none, none) |
| 딤플링 | 1 | (none, none ← 문구) |
| 멍 | 1 | (none, none) |
| 바이오필름 | 1 | (none, none) |
| 반흔 | 1 | (none, none) |
| 색소침착 | 1 | (none, none) |
| 소양감 | 1 | (none, none) |
| 수포 | 1 | (none, none ← 문구) |
| 실 노출 | 1 | (none, none) |
| 실 이동 | 1 | (none, none) |
| 실신 | 1 | (none, none) |
| 아나필락시스 | 1 | (none, none ← 문구) |
| 열감 | 1 | (none, none) |
| 육아종 | 1 | (none, none) |
| 이물반응 | 1 | (none, none) |
| 작열감 | 1 | (none, none) |
| 항체 내성 | 1 | (none, none) |
| 혈관 폐색 | 1 | (none, none) |
| 혈관외유출 | 1 | (none, none) |
| 혈종 | 1 | (none, none) |
| 화상 | 1 | (none, none) |

### R15 may_cause(경과 = 엣지 속성 · 원칙 C)

|  | 결정 전(ERD · (출발, 단위) distinct) | 6차 |
|---|---|---|
| 엣지 | 1342 | 레코드 1429 · (출발, 단위) distinct 1372 |
| 이름 유래 / 문구 유래 | 79 / 1306 | 82 / 1321 (+ pih-risk 26) |
| 경과 있는 엣지 | 247 | 262 |
| 경과 값별 | 지연 12 · 재발 2 · 일시 234 · 영구 1 | 일시 237 · 지속 12 · 재발 2 · 지연 12 · 영구 1 |
| 고지 유래(disclosure) | 0 | 0 |

이름 유래 엣지는 이름마다 하나(severity·incidence 같은 속성이 이름의 것)라 레코드 수가 (출발, 단위) distinct 보다 많다. 경과는 그 단위 후보의 경과만 — 검산 V3.1-9 가 문구 엣지마다 확인한다(S-1).

### 조건 단위(V3.1-4)

이름 자리 471 · distinct 298(kind 포함 299) → 단위 **312**(사전 96 + raw_name 216) · kind condition 172 · check 136 · age_group 4 · 문장 부록 529(원칙 B 로 문장 하나가 단위 둘이면 둘에 붙는다) · R16 514 · R17 20. 5차의 person_condition 298(문자열 식별)은 v3.1 에서 쓰지 않는다 — 결정 B3-R16-01·02 의 끝(locator)은 그 문장의 조건 단위로 닿았다.

### 결정 묶음 4 제안(동의어 · proposed — 빌드가 읽지 않음)

`decisions/batch4-proposed/` 130 · 게이트 `out/gate/batch4.json`(2B 스키마) 고를 자리 187 · 추천 있음 13 · 추천 없음 174. ① 부작용 문구 조각 80 · ② 부위·물질 조각 47 · ③ 시술 조각 60. 승인하면 닫히는 문구 자리 합 90 · 참조 합 0(추천대로 고를 때 · 항목 effect).

## 15. 7차 빌드 · ERD v3.2

6차 = `baseline/manifest-6차.json`(ERD v3.1 · 결정 457) · 7차 = ERD **v3.2**(`erd-v3.2.json` · `erd-v3.2-dictionaries.json` 의 파생 항목(원장 사건 노드 · 장비 제품)은 빼고 분해가 다시 세운다 · 빌더 `lib/v32.py` · 발주서 `silver-build-7-brief.md`). ③ 결정 적용 전 분해 = `erd-v3.2-tuples.json` 요약 차이 0/171(§5 · 행 대조는 check ③). 결정은 6차와 같은 저장소(새 결정 0) — 옛 결정을 v3.2 구조로 옮겨 적용했다.

### 결정 적용(7차)

| kind | applied | recorded | rejected | no_target |
|---|---|---|---|---|
| adverse_tuple_assign | 23 | 0 | 0 | 0 |
| canonical_mapping | 11 | 0 | 0 | 0 |
| canonical_rename | 2 | 0 | 0 | 0 |
| conflict_resolution | 0 | 16 | 0 | 0 |
| dictionary_add | 193 | 0 | 0 | 0 |
| dictionary_remove | 1 | 0 | 0 | 0 |
| edge_create | 8 | 0 | 0 | 0 |
| event_split | 3 | 0 | 0 | 0 |
| fold_approve | 21 | 0 | 0 | 0 |
| ledger_correction_note | 0 | 3 | 0 | 0 |
| product_reclassify | 2 | 0 | 0 | 0 |
| reclassification | 1 | 0 | 0 | 0 |
| scope_review | 0 | 10 | 0 | 0 |
| tuple_assign | 6 | 0 | 0 | 0 |
| verification_hold | 0 | 1 | 0 | 0 |

거부·대상 없음: **0** — 기존 결정(_bootstrap · batch1 · 2a · 2b · 3) 전부 v3.2 빌더가 받았다.

v3.2 새 구조로 옮겨 적용한 옛 결정(거부 아님 · 사유는 적용 로그 note):

- 옛 이름 단위(raw_name) 대상 adverse_tuple_assign **10** — v3.2 에는 이름 단위가 없다(V3.2-0 노드 원칙). 같은 locator 의 이름 단위(원장 사건 노드 · 사전 사건)를 지정 단위로 대체:

| 결정 | 이름 locator | v3.2 분해 단위(대체 전) | 지정 단위 |
|---|---|---|---|
| B2B-ISE-01 | M1/2 | 홍반, 부종 | (홍반, none, none), (부종, none, none) |
| B2B-PAR-01 | M9/4 | 감각 이상 | (감각 이상, none, none) |
| B2B-PAR-02 | M14/2 | 감각 이상 | (감각 이상, none, none) |
| B2B-PAR-03 | M14/3 | 홍반, 부종 | (홍반, none, none), (부종, none, none) |
| B2B-PAR-04 | M16/4 | 경결, 섬유화 | (경결, none, none) |
| B3-ADV-01 | M9/4 | 감각 이상 | (감각 이상, none, none) |
| B3-ADV-02 | M14/2 | 감각 이상 | (감각 이상, none, none) |
| B3-ADV-03 | M14/3 | 홍반, 부종 | (홍반, none, none), (부종, none, none) |
| B3-ADV-04 | M14/1 | 괴사, 동상 | (괴사, 피부, none), (괴사, 피하 지방층, none), (동상, none, none) |
| B3-ADV-05 | M16/4 | 경결 | (경결, none, none), (섬유화, none, none) |

- 옛 표현 지정(kind=expression · 부작용 문구 자리) **10** — 그 자리의 부작용 문구 사전 항목 지도(phrase_map 과 같은 효과 · status approved): `B2B-TEV-01`→PHR-0d10bd307d, `B2B-TEV-02`→PHR-4db30daf7b, `B2B-TEV-03`→PHR-4db30daf7b, `B2B-TEV-04`→PHR-0d10bd307d, `B2B-TEV-05`→PHR-559472746f, `B2B-TEV-06`→PHR-4db30daf7b, `B2B-TEV-07`→PHR-4db30daf7b, `B2B-TEV-08`→PHR-0d10bd307d, `B2B-TEV-09`→PHR-559472746f, `B2B-TEV-10`→PHR-0d10bd307d
- 옛 표현 지정(타임라인 줄) **3** — v3.2 타임라인 줄은 문구 사전이 아니라 자기 테이블(post_procedure_timeline · V3.2-9) — 그 줄의 참조(adverse_ref · R34)를 지정 단위로 · 경과는 계열 R15 경과: `B3-ADV-COURSE-01`(M16/6 → 줄 5/3/0 · 경과 지속), `B3-ADV-COURSE-02`(M16/9 → 줄 5/4/1 · 경과 지속), `B3-ADV-COURSE-03`(M16/9 → 줄 5/2/1 · 경과 지속)

### 개체

|  | 6차 | 7차 | 변화 | 비고 |
|---|---|---|---|---|
| adverse_effect | 71 | 338 | +267 | 원장 사건 노드 단위(V3.2-0) · 이름 단위(raw_name) 없음 |
| anatomical_structure | 36 | 36 | 0 |  |
| catalog_item | 521 | 521 | 0 |  |
| citation | 313 | 313 | 0 |  |
| clinical_rule | 139 | 139 | 0 |  |
| complaint | 121 | 121 | 0 |  |
| conflict | 2818 | 1290 | -1528 | 아래 충돌 표 |
| decision | 457 | 457 | 0 |  |
| evidence_statement | 87 | 119 | +32 | + 문헌 adverse_effects 32(kind=adverse_effects · V3.2-0) |
| modality | 17 | 17 | 0 |  |
| modality_subcategory | 73 | 73 | 0 |  |
| package | 230 | 230 | 0 |  |
| person_condition | 312 | 310 | -2 | 토큰화(V3.2-1)로 raw_name 일부가 사전 단위로 |
| problem | 14 | 14 | 0 |  |
| problem_subcategory | 53 | 53 | 0 |  |
| procedure | 645 | 646 | +1 | 토큰화·성분 what·장비 승격 |
| product | 378 | 421 | +43 | 장비 제품 자동 등록 78(origin=taxonomy · V3.2-5) — 그중 step1 제품과 이름이 닿아 합친 것 포함 |
| site | 28 | 28 | 0 |  |
| source_file | 22 | 22 | 0 |  |
| technique | 12 | 12 | 0 |  |
| post_procedure_timeline | 0 | 10 | +10 | v3.2 신설(V3.2-9) |
| emergency_sign | 0 | 52 | +52 | v3.2 신설(V3.2-0) |

### 관계

|  | 6차 | 7차 | 변화 | 비고 |
|---|---|---|---|---|
| R1 | 74 | 74 | 0 |  |
| R2 | 521 | 521 | 0 |  |
| R3 | 163 | 241 | +78 | 장비 승격(항목 이름 = 제품) |
| R4 | 476 | 554 | +78 | + 장비 제품(계열 → 제품) |
| R5 | 25 | 25 | 0 |  |
| R6 | 53 | 53 | 0 |  |
| R7 | 232 | 232 | 0 |  |
| R8 | 105 | 105 | 0 |  |
| R9 | 594 | 594 | 0 |  |
| R10 | 21 | 21 | 0 |  |
| R11 | 12 | 12 | 0 |  |
| R12 | 481 | 482 | +1 |  |
| R13 | 32 | 32 | 0 |  |
| R14 | 146 | 146 | 0 |  |
| R15 | 1429 | 2511 | +1082 | (출발, 단위) 마다 하나 · 이름+문구+타임라인+응급 참조 · inheritance · layer |
| R16 | 514 | 514 | 0 |  |
| R17 | 20 | 20 | 0 |  |
| R18 | 119 | 119 | 0 |  |
| R19 | 346 | 378 | +32 | + 문헌 adverse_effects 인용 |
| R20 | 87 | 119 | +32 | + 계열 → adverse_effects 근거 |
| R21 | 45 | 45 | 0 |  |
| R22 | 22 | 22 | 0 |  |
| R23 | 53 | 53 | 0 |  |
| R24 | 225 | 225 | 0 |  |
| R25 | 6419 | 4602 | -1817 |  |
| R26 | 521 | 521 | 0 |  |
| R27 | 645 | 643 | -2 | 성분 what 튜플은 R27 끝 없음(해석 보류) |
| R28 | 55 | 55 | 0 |  |
| R30 | 3 | 3 | 0 |  |
| R31 | 14 | 51 | +37 | 단위가 는 만큼 |
| R32 | 112 | 112 | 0 |  |
| R33 | 0 | 10 | +10 | v3.2 신설 |
| R34 | 0 | 366 | +366 | v3.2 신설(줄 → 단위 참조) |
| R35 | 0 | 70 | +70 | v3.2 신설 |

### 충돌 kind 별

|  | 6차 | 7차 | 변화 | 비고 |
|---|---|---|---|---|
| ④ value_conflict auto_resolved_by_trust | 1 | 1 | 0 |  |
| ⑥ value_conflict open | 49 | 49 | 0 |  |
| ⑦ duplicate_candidate open | 152 | 471 | +319 |  |
| ⑦ duplicate_candidate resolved | 4 | 4 | 0 |  |
| ⑧ unregistered_value open | 2352 | 506 | -1846 |  |
| ⑨ unresolved_reference open | 260 | 259 | -1 |  |

### 게이트

|  | 6차 | 7차 | 비고 |
|---|---|---|---|
| unresolved_references | 260 | 259 |  |
| unregistered_fragments | 2352 | 506 | 부작용 문구 미등록 조각은 핵심어 노드 · side · 설명으로(⑧ 은 시술·조건 축 위주) |
| unlinked_phrases | 1032 | 0 | v3.2 부작용 축에 미연결 상태 없음(새 노드 · 메모 · 설명문) |
| unlinked_phrase_locators | 1641 | 0 |  |
| catalog_partial | 336 | 259 |  |
| conflicts_md_duplicate | 156 | 475 | + ⑦ 원장 사건 노드 쌍(strong · weak) · 장비 제품 ↔ 기존 제품 |

### 부작용 문구 분포(V3.2-0 · V3.2-7)

|  | 결정 전(ERD 실측) | 7차(결정 뒤) |
|---|---|---|
| 부작용 문구 자리 | 2285 | 2285 |
| 자리 status | new 835 · exact 1407 · sentence 13 · note 30 | new 835 · exact 1399 · approved 10 · sentence 11 · note 30 |
| 문구 사전 항목(부작용) · 메모 항목 | 530 · 28 | 536 · 27 |
| 항목 status | new 341 · exact 189 + 메모 sentence 7 · note 21 | new 342 · exact 191 · approved 3 · sentence 6 · note 21 |
| 어느 단위에도 안 붙은 부작용 문구(unlinked) | 0 | 0 |
| complications 이름 65 | exact 62 · new 3 | exact 62 · new 3 |

exact = 사전 사건에 닿음 · new = 핵심어 새 노드에 닿음 · note = 메모(사건 0 + 메모 어휘) · sentence = 설명문(문턱) · approved = 옛 표현 지정이 문구 사전 지도로. 미연결 상태는 없다(ERD §0.2).

### 원장 사건 노드 · ⑦ duplicate_candidate

|  | 결정 전(ERD 실측) | 7차(결정 뒤) |
|---|---|---|
| 원장 사건 노드(origin=ledger · unreviewed) | 262 | 260 |
| 부작용 단위 · event_kind | 328 | 338 · dict 66 · ledger 272 |
| ⑦ 노드 쌍 strong / weak | 98 / 207 | 96 / 207 (충돌 레코드 strong·open 96 · weak·open 207) |
| ⑦ 장비 제품 ↔ 기존 제품(접두) | 13(씨앗 ⑦) | 18 |

결정 전 → 7차 노드 차이: 빠짐 두피 민감성, 두피 온감 · 새로 없음 — 이미 approved 인 ① 사전 결정(부위·동의어 추가)이 그 토막의 조각을 사전 값으로 만들어 핵심어가 남지 않았다.

### 타임라인 줄 · 응급 징후 · 고지 · 문헌(자기 테이블 · 참조만)

|  | 결정 전(ERD 실측) | 7차(결정 뒤) |
|---|---|---|
| 타임라인 · 단계 · 줄 | 10 · 43 · 435 | 10 · 43 · 435 |
| 줄 상태 | ref_partial 109 · normal_memo 78 · ref 192 · none 56 | ref_partial 107 · normal_memo 78 · ref 194 · none 56 |
| R34 timeline_refers | 368 | 366 |
| 응급 징후(SGN) · 상태 | 52 · ref 26 · none 7 · ref_partial 19 | 52 · ref 27 · none 7 · ref_partial 18 |
| R35 sign_refers | 69 | 70 |
| 필수 고지 자리 · 상태 | 109 · none 58 · ref 10 · ref_partial 41 | 109 · none 58 · ref 10 · ref_partial 41 |
| 문헌 adverse_effects · 상태 | 32 · none 20 · ref_partial 12 | 32 · none 20 · ref_partial 12 |

| 반응 등급 | ref | ref_partial | none | normal_memo |
|---|---|---|---|---|
| normal | 52 | 32 | 0 | 78 |
| abnormal | 43 | 19 | 24 | 0 |
| caution | 45 | 26 | 22 | 0 |
| emergency | 54 | 30 | 10 | 0 |

- R33 has_timeline 10: 끝 procedure 6 · modality 4 — 타임라인 이름이 튜플로 풀리면 그 튜플, 아니면 category 계열(V3.2-9).
- 결정이 바꾼 줄: 5/2/1(DEC-2026-11-05-B3-ADV-COURSE-03), 5/3/0(DEC-2026-11-05-B3-ADV-COURSE-01), 5/4/1(DEC-2026-11-05-B3-ADV-COURSE-02) · 참조 끝이 사라져 뺀 참조: 0

### 항목 자신 · 제품 승격 · 성분 what(V3.2-5 · V3.2-6)

|  | 6차 | 결정 전(ERD v3.2 실측) | 7차 |
|---|---|---|---|
| 분류 항목 → what_kind(항목 521) | — | catalog_item 324 · product 187 · modality_subcategory 7 · ingredient 3 | product 245 · catalog_item 266 · modality_subcategory 7 · ingredient 3 |
| 항목 자신이 시술(분류 항목 원천 튜플 what=catalog_item) | 342 | 324 | 263 |
| 튜플 what_kind(전체) | catalog_item 348 · product 190 · modality_subcategory 46 · modality 61 | catalog_item 326 · product 216 · modality_subcategory 14 · ingredient 3 · modality 41 | catalog_item 267 · product 269 · modality_subcategory 46 · ingredient 3 · modality 61 |
| 장비 제품 자동 등록(origin=taxonomy) | 0 | 151 | 78 |

- 장비 자동 등록: 장비 항목 176 · 결정 전 등록 151 → 7차 78 — 결정 전에 등록되던 것 중 7차에 등록하지 않은 73(사유 already 73): approved 결정(dictionary_add · 묶음 1 등)이 이미 그 이름을 사전 값(product_name:BBL, product_name:BBL 히어로, product_name:노블린, product_name:더마샤인, product_name:더블로골드S, product_name:듀오타이트, product_name:디스커버리 피코, product_name:라라젯, product_name:라이트쉬어 듀엣, product_name:리니어펌, product_name:리팟, product_name:리프테라 …)으로 두어 「이미 사전 값」이다 — 그 항목도 product 로 승격되는 것은 같다.
- 성분 what(분류 항목): PDO[M7], PCL[M7], PLLA[M7] · R27 끝 없는 성분 what 튜플 3(성분은 사전 값 · 개체 아님 — 해석 보류)

### ⑨ 미해결 참조

6차 260 → 7차 **259** — 풀림 1 · 새로 0. 사유별(7차) unregistered 204 · 고민 사전 일치 없음(질문 12) 29 · multi_primary 18 · canonical_category 가 하위분류 사전에 없다(질문 23) 6 · combo_outside_fragment 2

풀린 참조: 「서브시전(subcision)」@—

### R15 may_cause · 속성 상속(V3.2-8 · 참조만)

R15 2511(결정 전 ERD (출발, 단위) 2476) · layer family 301 · item 2184 · 타임라인 참조가 있는 엣지 155 · 응급 참조 73 · 경과 있는 엣지 438 · basis 없는 상속 0 · 값 복사 0.

항목·제품 출발(layer=item) — 속성마다 basis:

| 속성 | item | family | unit | none |
|---|---|---|---|---|
| severity | 0 | 966 | 0 | 1218 |
| incidence | 0 | 966 | 0 | 1218 |
| onset | 0 | 966 | 0 | 1218 |
| duration | 0 | 135 | 0 | 2049 |
| mechanism | 0 | 966 | 0 | 1218 |
| management | 0 | 966 | 416 | 802 |
| prevention | 0 | 966 | 0 | 1218 |
| risk_factors | 0 | 966 | 0 | 1218 |

계열 출발(layer=family) — 속성마다 basis:

| 속성 | family | unit | none |
|---|---|---|---|
| severity | 91 | 0 | 210 |
| incidence | 91 | 0 | 210 |
| onset | 91 | 0 | 210 |
| duration | 23 | 0 | 278 |
| mechanism | 91 | 0 | 210 |
| management | 91 | 87 | 123 |
| prevention | 91 | 0 | 210 |
| risk_factors | 91 | 0 | 210 |

### 결정 묶음 5 게이트(노드 단위 · `out/gate/batch5.json`·`.md`)

| 묶음 | 자리 | 추천 |
|---|---|---|
| ledger-nodes | 260 | 0 |
| dup-strong | 96 | 1 |
| seed-site | 15 | 0 |
| seed-ingredient_material | 17 | 0 |
| seed-product_abbrev | 29 | 0 |
| m5-rename | 1 | 0 |
| m16-technique | 6 | 4 |
| site-synonyms | 6 | 1 |
| air-embolism-qualifier | 1 | 0 |
| records | 1 | 0 |

고를 자리 432 · 옵션 3060 · 추천 6 · 원문 935(읽기 실패 0) · ⑦ weak 207 은 `batch5-weak.json`(게이트에 올리지 않음). 고른 답 → `python3 apply_gate.py --gate out/gate/batch5.json --answers answers.json`(→ decisions/batch5/).

## 16. 8차 빌드 · ERD v3.3 · 원장 3판 · 결정 묶음 6-A

7차 = `baseline/manifest-7차.json`(ERD v3.2 · 원장 2판 · 결정 457) · 8차 = ERD **v3.3**(`erd-v3.3.json` · `erd-v3.3-dictionaries.json` · 원장 **3판** `bronze/phub-ledger/` · 빌더 `lib/adverse33.py`(분석기) · `lib/analyzer.py`(kiwipiepy 캐시) · 발주서 `silver-build-8-brief.md`). ③ 결정 적용 전 분해(분석기 없는 목록 규칙 — ERD 실측 `erd-v3.3-tuples.py` 의 조건) = `erd-v3.3-tuples.json` 요약 차이 0/171(§5). 실버 산출(결정 전·뒤 둘 다)은 **분석기(V3.3-B)** 로 분해한 값이다 — ERD 실측(목록 규칙)과 노드 수가 다르며 그 차이는 아래 표가 센다.

### 결정 묶음 6-A 적용 로그(decisions/batch6a/)

| kind | 건 | applied | rejected | no_target |
|---|---|---|---|---|
| canonical_rename | 1 | 1 | 0 | 0 |
| dictionary_add | 28 | 28 | 0 | 0 |
| fold_approve | 19 | 19 | 0 | 0 |

6-A 결정 48(site 15 · ingredient_material 6 · 접미사 쌍 20 = fold_approve 19 + canonical_rename 1 · product_name 동의어 7) · 적용 48 · 거부 0 · 대상 없음 0.

전체 결정 적용 결과(8차 · 기존 결정 포함):

| kind | applied | recorded | rejected | no_target |
|---|---|---|---|---|
| adverse_tuple_assign | 23 | 0 | 0 | 0 |
| canonical_mapping | 11 | 0 | 0 | 0 |
| canonical_rename | 3 | 0 | 0 | 0 |
| conflict_resolution | 0 | 16 | 0 | 0 |
| dictionary_add | 221 | 0 | 0 | 0 |
| dictionary_remove | 1 | 0 | 0 | 0 |
| edge_create | 8 | 0 | 0 | 0 |
| event_split | 3 | 0 | 0 | 0 |
| fold_approve | 39 | 0 | 1 | 0 |
| ledger_correction_note | 0 | 3 | 0 | 0 |
| product_reclassify | 2 | 0 | 0 | 0 |
| reclassification | 1 | 0 | 0 | 0 |
| scope_review | 0 | 10 | 0 | 0 |
| tuple_assign | 6 | 0 | 0 | 0 |
| verification_hold | 0 | 1 | 0 | 0 |

거부·대상 없음 1(기존 결정 — 7차와 같은 것인지는 아래):
- `DEC-2026-11-04-B2B-S3C-16` fold_approve — rejected: anchors/keep_anchor 가 실버에 없다

접미사 쌍 fold_approve 가 닿은 자리(locators) · 닫은 ⑦:

| 결정 | 노드 | → | 닿은 자리 | 닫은 ⑦ |
|---|---|---|---|---|
| 01 | 건조감 | 건조 | 43 | 1 |
| 02 | 흉터형성 | 흉터 | 1 | 1 |
| 03 | 경결감 | 경결 | 26 | 1 |
| 04 | 따가움감 | 따가움 | 1 | 1 |
| 05 | 가피형성 | 가피 | 1 | 1 |
| 07 | 경화감 | 경화 | 3 | 1 |
| 08 | 건조증 | 건조 | 4 | 1 |
| 09 | 표정 경직감 | 표정 경직 | 1 | 1 |
| 10 | 결절감 | 결절 | 2 | 1 |
| 11 | 경직감 | 경직 | 1 | 1 |
| 12 | 마비감 | 마비 | 1 | 1 |
| 13 | 박탈감 | 박탈 | 1 | 1 |
| 14 | 색전증 | 색전 | 2 | 1 |
| 15 | 수포형성 | 수포 | 2 | 1 |
| 16 | 자반증 | 자반 | 1 | 1 |
| 17 | 통증감 | 통증 | 2 | 1 |
| 18 | 화상감 | 화상 | 2 | 1 |
| 19 | 결절형성 | 결절 | 1 | 1 |
| 20 | 반흔형성 | 반흔 | 1 | 1 |

### 개체

|  | 7차(v3.2 · 2판) | 8차(v3.3 · 3판) | 변화 | 비고 |
|---|---|---|---|---|
| adverse_effect | 338 | 269 | -69 | 분석기 핵심어 노드 · R2 사전 값(혈관 폐색 → 폐색+혈관) · 부위 15 · 접미사 접기 |
| anatomical_structure | 36 | 36 | 0 |  |
| catalog_item | 521 | 523 | +2 | 원장 3판 +2(M8-6 저출력레이저(LLLT) · 다이오드 레이저) |
| citation | 313 | 313 | 0 |  |
| clinical_rule | 139 | 139 | 0 |  |
| complaint | 121 | 121 | 0 |  |
| conflict | 1290 | 1119 | -171 | 아래 충돌 표 |
| decision | 457 | 505 | +48 | +48(6-A) |
| emergency_sign | 52 | 52 | 0 |  |
| evidence_statement | 119 | 119 | 0 |  |
| modality | 17 | 17 | 0 |  |
| modality_subcategory | 73 | 73 | 0 |  |
| package | 230 | 230 | 0 |  |
| person_condition | 310 | 310 | 0 |  |
| post_procedure_timeline | 10 | 10 | 0 |  |
| problem | 14 | 14 | 0 |  |
| problem_subcategory | 53 | 53 | 0 |  |
| procedure | 646 | 669 | +23 | 3판 synergy 정식 이름 · 부위 15 · 성분 6 · 동의어 7 |
| product | 421 | 423 | +2 | product.kind=product 전부(구성품 0 · R36 0) |
| site | 28 | 44 | +16 | +15(6-A) +3(v3.3 동맥·정맥·안동맥) |
| source_file | 22 | 22 | 0 |  |
| technique | 12 | 12 | 0 |  |

### 관계

|  | 7차(v3.2 · 2판) | 8차(v3.3 · 3판) | 변화 | 비고 |
|---|---|---|---|---|
| R1 | 74 | 74 | 0 |  |
| R2 | 521 | 523 | +2 |  |
| R3 | 241 | 245 | +4 |  |
| R4 | 554 | 556 | +2 |  |
| R5 | 25 | 25 | 0 |  |
| R6 | 53 | 53 | 0 |  |
| R7 | 232 | 232 | 0 |  |
| R8 | 105 | 105 | 0 |  |
| R9 | 594 | 594 | 0 |  |
| R10 | 21 | 21 | 0 |  |
| R11 | 12 | 12 | 0 |  |
| R12 | 482 | 488 | +6 |  |
| R13 | 32 | 32 | 0 |  |
| R14 | 146 | 146 | 0 |  |
| R15 | 2511 | 2479 | -32 | (출발, 단위) 마다 하나 |
| R16 | 514 | 514 | 0 |  |
| R17 | 20 | 20 | 0 |  |
| R18 | 119 | 146 | +27 |  |
| R19 | 378 | 378 | 0 |  |
| R20 | 119 | 119 | 0 |  |
| R21 | 45 | 45 | 0 |  |
| R22 | 22 | 22 | 0 |  |
| R23 | 53 | 53 | 0 |  |
| R24 | 225 | 273 | +48 |  |
| R25 | 4602 | 4387 | -215 |  |
| R26 | 521 | 523 | +2 |  |
| R27 | 643 | 663 | +20 | what_kind=component 0 |
| R28 | 55 | 64 | +9 |  |
| R30 | 3 | 3 | 0 |  |
| R31 | 51 | 54 | +3 | 단위가 는 만큼 · (폐색, 혈관) 등 |
| R32 | 112 | 112 | 0 |  |
| R33 | 10 | 10 | 0 |  |
| R34 | 366 | 366 | 0 |  |
| R35 | 70 | 69 | -1 |  |
| R36 | 0 | 0 | 0 | v3.3 신설 component_of — 원장 칸 없음 · 엣지 0 |

### 충돌 kind 별

|  | 7차(v3.2 · 2판) | 8차(v3.3 · 3판) | 변화 | 비고 |
|---|---|---|---|---|
| ④ value_conflict auto_resolved_by_trust | 1 | 1 | 0 |  |
| ⑥ value_conflict open | 49 | 49 | 0 |  |
| ⑦ duplicate_candidate open | 471 | 326 | -145 |  |
| ⑦ duplicate_candidate resolved | 4 | 23 | +19 |  |
| ⑧ unregistered_value open | 506 | 480 | -26 |  |
| ⑨ unresolved_reference open | 259 | 240 | -19 |  |

### 게이트 목록

|  | 7차 | 8차 |
|---|---|---|
| unresolved_references | 259 | 240 |
| unregistered_fragments | 506 | 480 |
| unlinked_phrases | 0 | 0 |
| unlinked_phrase_locators | 0 | 0 |
| catalog_partial | 259 | 251 |
| conflicts_md_duplicate | 475 | 349 |

### 부작용 — 사건 노드 · 단위 · 문구 분포(8차)

|  | ERD 실측(목록 규칙 · 3판) | 결정 전(분석기) | 8차(결정 뒤) |
|---|---|---|---|
| 사건 사전 값(adverse_event_type · 사전) | — | 40 | 43 |
| 새 사건 노드(origin=ledger · 정식) | 262 | 203 | 182(out/dictionaries.json origin=ledger 182) |
| 사건 노드 합(사전 + 새) | — | — | 225 |
| 부작용 단위 | — | 278 | 269 · dict 75 · ledger 194 |
| 부작용 문구 자리 2,285 · status | — | new 796 · exact 1425 · sentence 34 · note 30 | new 711 · exact 1500 · approved 12 · sentence 32 · note 30 |
|   sentence 의 까닭(자리) | — | — | judge_phrase 11 · sentence_b 20 · ambiguous 1 |
| 문구 사전 항목 status | — | new 299 · exact 196 + 메모 sentence 19 · note 21 | new 279 · exact 222 · approved 3 · sentence 18 · note 21 |
| 사건 칸이 비는 exact·new 문구 자리 | — | 0 | 0 |
| complications 이름 65 | — | exact 62 · new 3 | exact 62 · new 3 |
| ⑦ strong / weak(결정 전) · open(8차) | — | 60 / 124 | 38 / 119 · open strong 38 |

exact = 사전 사건 · new = 새 노드 · sentence = 설명문/문장꼴(b)/애매(분석기 · 노드 없음 · 사람 판정) · note = 메모 · approved = 결정 지도. 미연결 상태는 없다(§0.2).

분석기(V3.3-B) 토막 결과(결정 뒤 · 사전 사건 0 인 토막):

| 결과 | 토막 |
|---|---|
| node | 831 |
| T2b | 28 |
| T4 | 10 |
| T2a-capture | 2 |
| T3 | 2 |
| T1-none | 1 |
| T1-partial | 1 |

규칙 적용 T1 760 · R2 79 · T2b 28 · T4 10 · N1 73 · T2a 2 · R1 19 · T3 2 · N1 명사형 노드 21 · 단독 출현 0 노드(R3 신호 · 버리지 않음) 21 · 괄호 안 판정 noun 99 · S 26 · sentence 10 · tie 5 · 사전 밖 구조 말(R2 · side 보존) 안면신경 7 · 감각신경 2 · 눈 4 · 신경 44 · 전신 4 · 표정근 3 · 결막 1 · 표면 3 · 진피 1 · 하악변연신경 13 · R1 후보(N2 수식어 · 노드 토막) 씹는 1 · 제한된 2 · 따가운 1 · 따뜻한 2 · 불규칙한 1.

### (폐색, 부위) 단위 — V3.3-C R2 를 사전 값에도 · 폐색 ≠ 색전

| 단위 | 사건 | 부위 | 물질 | 자리(occ) | 원천 |
|---|---|---|---|---|---|
| ADV-53f3c30947 | 폐색 | none | none | 1 | complications |
| ADV-c14c2a44a5 | 폐색 | 동맥 | none | 1 | safety_phrase |
| ADV-54aa74391e | 폐색 | 미간 | none | 1 | safety_phrase |
| ADV-df2c6ea24f | 폐색 | 안동맥 | none | 2 | safety_phrase |
| ADV-e4cef191c9 | 폐색 | 혈관 | none | 16 | complications, safety_phrase |

폐색 단위 5((폐색, 혈관) 있음 True) · (혈관 폐색, none) 단위 0 · 색전 단위 5((색전, none, none), (색전, none, 공기), (색전, none, 역행성), (색전, none, 지방), (색전, 안동맥, 역행성)) · 폐색↔색전 공유 동의어 0 · 둘을 잇는 ⑦ 쌍 0 · 옛 표면형 「혈관 폐색」이 사전 값에 남음 0.

### category 참조 · unreviewed

- out/ 의 사건 분류 속성 참조(adverse_effect 의 분류 속성 · adverse_event_type 의 category/category_review): **0** (V3.3-E · check V3.3-E 가 out/ 텍스트 전수로 다시 센다).
- 사건 노드(adverse_event_type origin=ledger)의 status 필드: 0(정식 노드 · 필드 없음) · 장비 제품(product_name origin=taxonomy)의 status=unreviewed: 80(ERD §1.4 V3.2-5 문장 그대로 — ERD 질문 #8).

### 제품 구성품(V3.3-A)

product.kind product 423 · component_of 값 있음 0 · R36 엣지 0 · what_kind=component 튜플 0 — 원장 칸 없음 · 값 0.

### 분석기 캐시(V3.3-B · kiwipiepy)

kiwipiepy **0.24.1**(고정 0.24) · 정본 캐시 `cache/kiwi-cache.json`(항목 8241) · 이번 빌드가 읽은 항목 2764(사전 등록 묶음 2 · 7a128f9e880f8f1e678e1e6a65c4c2c2d907629743e02f791b5f1842e7fda782 1107 · dd1c210003d7dbc0a1ca6a932cbb1fbd803379006b4bbc67efec475a035bc378 1657) → `out/kiwi-cache.json`(1,058,672 bytes) · 워커 호출 0(미리 채움 문구 0 · 지연 미스 0) · 캐시 키 = 판 + 등록 사전 해시 + 문구(NFC). 캐시가 차면 venv 없이 재현(check ④).

### 결정 묶음 6 게이트(`out/gate/batch6.json`·`.md`) — 묶음별 자리

| 묶음 | 자리 | 물을 자리 | 옵션 | 추천 |
|---|---|---|---|---|
| ledger-nodes | 182 | 0 | 0 | 0 |
| dup-strong | 38 | 38 | 152 | 0 |
| sentence-b | 11 | 11 | 33 | 0 |
| ambiguous | 13 | 13 | 33 | 0 |
| occlusion-embolism | 3 | 3 | 6 | 0 |
| r30-candidates | 2 | 2 | 4 | 0 |
| batch3 | 15 | 15 | 52 | 5 |
| r1-candidates | 20 | 20 | 40 | 0 |
| mxx-prefix | 34 | 34 | 68 | 0 |

자리 318 · 물을 자리 136 · 추천 5(원장 병기 쌍만) · ⑦ weak 119 은 `batch6-weak.json`. 새 사건 노드는 목록만(옵션 없음 · 사용자 「종류 질문 없음」).

### 7차 재현(8차 lib · ERD v3.2 · 원장 2판)

`baseline/manifest-7차-repro.json` determinism_key `970159a280b6cba27aad6c6f5eda87a2b235d7e7a676bbdc88d54123a60961b2` vs `baseline/manifest-7차.json` `970159a280b6cba27aad6c6f5eda87a2b235d7e7a676bbdc88d54123a60961b2` → **같음**. 명령: `python3 build.py --erd ../erd-v3.2.json --dict ../erd-v3.2-dictionaries.json --colmap ../erd-v3.2-column-map.md --tuples ../erd-v3.2-tuples.json --tuples-prev ../erd-v3.1-tuples.json --bronze ../bronze/phub-ledger-v2 --decisions <batch6a 를 뺀 저장소> --out <임시>` (6-A 결정은 v3.3 몫이라 v3.2 재현 저장소에서 뺐다 — 결정 저장소에 ERD 판 필드가 없다 · ERD 질문 #14).

### ERD 질문 — v3.3 문장으로 구현이 갈리지 않는 자리(코디가 ERD 로 돌려보낼 것 · 임시 처리는 전부 보존·기록)

| # | 자리 | ERD 문장 | 갈리는 점 | 임시 처리(8차) |
|---|---|---|---|---|
| 1 | §1.3 R1·R2 목록 | 「수식어(R1)」「부위·구조 말(R2)」 | R1 낱말(장기간·임시·과도 …)·R2 구조 말(신경·안면신경·전신 …)이 ERD 규칙 데이터에 없다(1차 발주서 목록) | lib/adverse33.py ASSIST_R1/ASSIST_R2 상수(analyzer_assist) · 뗀 말은 parsed.misc(by=analyzer_r1)·side 로 보존 |
| 2 | §1.3 관형어 하나 = 수식어 | 「R1 · R15 qualifier_text · 보존」 | 뗀 관형어가 어느 칸에 보존되나(R15 qualifier_text 자리가 부작용 엣지에 없음) | 문구 parsed.misc(class misc · by=analyzer_n2) · R1 후보 게이트 |
| 3 | §1.3 R2 사전 밖 구조 말 | 「부위 칸으로 뗀다」 | 신경·안면신경·전신은 부위 사전 값이 아니라 부위 칸에 못 간다 | side(보존 · 칸 아님) · 수는 §16 분석기 표 |
| 4 | §1.3 문장꼴(b)·애매 | 「노드를 세우지 않고 사람 판정으로」 | phrase_dictionary.status 열거형에 「애매」 값이 없다 | status=sentence + why.analyzer(sentence_b\|ambiguous\|predicate) |
| 5 | §9.22 #6 자극감↔자극 | 「fold_approve + canonical_rename」 | rename 뒤 핵심어 「자극」은 사전 값이라 결정 전 분해에 노드가 없다 → fold_approve 는 대상 없음 | canonical_rename 하나로 닫음(fold 19 + rename 1 = 20) |
| 6 | §9.22 #9 표정 경직감↔표정 경직 | 대표 이름 「경직」 | 쌍의 b 는 「표정 경직」(수식어 표정 + 경직) — 「표정 경직」→「경직」 접기는 결정에 없다 | into=표정 경직 · 「표정 경직」 노드 그대로 |
| 7 | §10 ③ 대조 | 「ERD 실측은 분석기 없이 돈다」 | ③ 「결정 전 수치 = 실측」은 분석기 없는 분해로만 성립 | check ③ 은 analyzer=None 분해로 대조 · 분석기 수치는 §16 |
| 8 | §1.4 V3.2-5 장비 제품 status=unreviewed | 「status=unreviewed · license_status=미확인」 | 발주서 「unreviewed 등급 0」과 충돌(사건 노드만?) | 사건 노드 status 삭제 · 장비 제품은 ERD 문장 그대로(수 §16) |
| 9 | §1.5 원칙 C R2 부위 칸 | 「같은 멤버 안에서 바로 붙은 사건에만」 | R2 로 뗀 부위는 토막이 아니라 멤버 단위로 붙는다(한 멤버 두 토막이면 둘 다) | 멤버 단위(원칙 C 글자대로) · 자리 수는 (폐색, 부위) 표 |
| 10 | 발주서 캐시 키 「문구 정규화형」 | — | 분석기 결과가 글자 위치를 가지므로 정규화형(공백 제거)으로는 못 키운다 | 키 = 판 + 등록 사전 해시 + 원문(NFC) |
| 11 | §9.23 lib 참조 10 | 「실버 빌더 8차 개정 몫」 | v3.2 경로(7차 재현 · 바이트 동일)에는 사건 분류 속성이 남아야 한다 | v3.3 경로만 0 · lib 의 v≤3.2 분기 자리 수는 종료 보고 |
| 12 | §9.21 HA·히알루론산 | 따로 선 값 둘 | 한 값 + 동의어인지 | 값 둘(동의어 결정 없음) |
| 13 | §9.21 동의어 자리 | 전체얼굴·풀페이스·러브핸들·팔·눈 밑·코 끝 | 승인 범위(값 15)에 동의어가 드나 | 넣지 않음(결정 reason 에 후보 기록) |
| 14 | §5 결정 레코드 | 「빌드는 approved 만」 | v3.3 결정(6-A)을 v3.2 재현 빌드가 읽지 않게 할 필드가 없다 | 재현은 batch6a 를 뺀 저장소 사본으로 |
| 15 | §1.3 T2a 사전 사건 포착 | 「사전 통째 일치가 먼저」 | 문장꼴 토막 안 사전 사건 NNG(조사 붙음)를 분석기가 잡아 exact 로 붙임 — 통째 일치 밖 | T2a-capture 로 붙이고 수를 §16 표에 |
| 16 | §1.9 원장 3판 · 결정 anchor | 「synergy 라벨이 Mxx- 접두 없이 정식 이름에 닿는다」 | 2판 synergy 라벨로 세운 REF- anchor(DEC-2026-11-04-B2B-S3C-16 fold_approve 의 anchor 7 중 synergy @45·@55)가 3판에서 바뀌어 결정이 실버에 닿지 않는다(rejected 1) | 그대로 거부 기록 · 재지정은 사용자(새 anchor 로 결정 갱신) |

