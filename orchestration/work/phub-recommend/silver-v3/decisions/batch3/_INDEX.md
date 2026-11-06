# 결정 묶음 3 — approved (사용자 이건학 · 2026-11-05)

발주서 `silver-build-5-brief.md` B. 근거 = `_batch3-candidates.md`(사용자 대화) · 원장 locator · `sources/`. 빌드가 읽는다(적용 결과는 `out/manifest.json → decisions.apply_log` · report §13).

| id | kind | 대상 → 값 | 근거 locator(원장) | 근거(그 밖) |
|---|---|---|---|---|
| B3-ADV-01 | adverse_tuple_assign | M9/4 → 1 튜플 | 1 | 1 |
| B3-ADV-02 | adverse_tuple_assign | M14/2 → 1 튜플 | 1 | 1 |
| B3-ADV-03 | adverse_tuple_assign | M14/3 → 2 튜플 | 1 | 1 |
| B3-ADV-04 | adverse_tuple_assign | M14/1 → 3 튜플 | 2 | 2 |
| B3-ADV-05 | adverse_tuple_assign | M16/4 → 2 튜플 | 2 | 1 |
| B3-CAT-01 | dictionary_add | catalog_item_name: 스킨보톡스 += 더모톡신, 메조보톡스 | 3 | 1 |
| B3-MAP-01 | canonical_mapping | CAT-6db65700a1 → SUB-9088d13466 (scope 1) | 2 | 1 |
| B3-MFR-01 | dictionary_add | manufacturer: 앨러간/애브비 += 엘러간 | 2 | 2 |
| B3-PRD-01 | dictionary_add | product_name: 시크릿 += 시크릿RF (code M11) | 4 | 1 |
| B3-PRD-02 | dictionary_add | product_name: 라라젯 += LHALA JET (code M15) | 3 | 2 |
| B3-PRD-03 | dictionary_add | product_name: ASCEplus += ASCE+엑소좀 (code M5) | 3 | 1 |
| B3-PRD-04 | dictionary_add | product_name: 셀엑소좀 (code M4) | 2 | 1 |
| B3-R30-01 | edge_create | R30 {"event": "동상", "site": "none", "course": "미상", "qualifier": "none"} → {"event": "괴사", "site": "none", "course": "미상", "qualifier": "none"} | 2 | 1 |
| B3-R30-02 | edge_create | R30 {"event": "혈관 폐색", "site": "none", "course": "미상", "qualifier": "none"} → {"event": "괴사", "site": "none", "course": "미상", "qualifier": "none"} | 3 | 1 |
| B3-R30-03 | edge_create | R30 {"event": "섬유화", "site": "none", "course": "미상", "qualifier": "none"} → {"event": "경결", "site": "none", "course": "영구", "qualifier": "none"} | 2 | 1 |
| B3-REN-01 | canonical_rename | modality M1: 보톡스 → 보툴리눔 톡신 · 동의어 ['BTX'] | 3 | 1 |
| B3-REN-02 | canonical_rename | modality M3: 바이오스티뮬레이터/콜라겐부스터 → 바이오스티뮬레이터 · 동의어 ['콜라겐부스터'] | 2 | 1 |
| B3-SIT-01 | dictionary_add | site: 사각턱 += 교근 | 3 | 1 |
| B3-SIT-02 | dictionary_add | site: 팔자주름 += 팔자 | 3 | 2 |
| B3-SIT-03 | dictionary_add | site: 두피 (kind region) | 3 | 2 |
| B3-TUP-01 | tuple_assign | CAT-b3860c9514 → (SUB-9088d13466, SIT-886ae927b5, TEC-29796b316e) | 1 | 1 |
| B3-TUP-02 | tuple_assign | CAT-b44cb2c2fe → (SUB-9088d13466, SIT-ebd1591544, TEC-545a700199) | 1 | 1 |
| B3-TUP-03 | tuple_assign | REF-4445947203 → (SUB-9088d13466, SIT-446031b79e, none) | 1 | 1 |
| B3-TUP-04 | tuple_assign | REF-065677ad2d → (SUB-9088d13466, SIT-ebd1591544, none) | 1 | 1 |

합계 24. 후보 표에서 approved 로 만들지 않은 것은 `../batch3-proposed/_INDEX.md`.

## 6차 빌드에서 더한 것 — 엑소좀 EXO-02·05·06(ERD v3.1 kind · 2026-11-05 · 발주서 `silver-build-6-brief.md` A)

5차 때 kind·관계가 없어 `batch3-proposed/` 의 scope_review 로 두었던 엑소좀 통합 ②⑤⑥ 을 v3.1 kind 로 옮겨 approved(사용자 확정 방향 · 근거 locator · 결정의 `supersedes_proposal`). 제안 파일 셋은 제안 폴더에서 뺐다. 적용 결과는 report §14.

| id | kind | 대상 → 값 | 바꾼 제안 |
|---|---|---|---|
| B3-EXO-02A | product_reclassify | PRD-be57673deb(ASCEplus · M5) → M4 = PRD-e45033395c | B3-P-EXO-02 |
| B3-EXO-02B | product_reclassify | PRD-8a1d788eec(EXOSOME SKIN · M5) → M4 = PRD-f4264ddf37 | B3-P-EXO-02 |
| B3-EXO-05A | edge_create | R32 clinical_rule(product_note 「화장품 허가 (주사 사용 불법)」 · taxonomy M5 ASCEplus note) → product ASCEplus · scope product · severity prohibited | B3-P-EXO-05 |
| B3-EXO-05B | edge_create | R32 같은 규칙 → product EXOSOME SKIN | B3-P-EXO-05 |
| B3-EXO-05C | edge_create | R32 같은 규칙 → product 셀엑소좀(M4 · B3-PRD-04) | B3-P-EXO-05 |
| B3-EXO-06 | dictionary_remove | modality 「PRP/자가혈」(M5) 동의어 「PRP/엑소좀」 제거 | B3-P-EXO-06 |

기법=주사 끝(⑤ 의 「+ 기법=주사」)은 만들지 않았다 — R32 의 기법 끝은 scope=all(주사 전체)이라 엑소좀 제품에만 걸리는 규칙을 넓힌다(발주서 문장은 「엑소좀 제품 전부에」). 합계 24 + 6 = 30.
