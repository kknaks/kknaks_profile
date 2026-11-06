# 결정 묶음 3 — 제안 (status=proposed · 빌드가 읽지 않음)

> 6차 빌드(2026-11-05 · ERD v3.1): 엑소좀 B3-P-EXO-02·05·06 은 v3.1 kind(product_reclassify · R32 edge_create · dictionary_remove)로 옮겨 `../batch3/DEC-2026-11-05-B3-EXO-*` 에 approved — 이 폴더에서 뺐다(아래 표에서도 뺐다).

승인: status → approved, decided_by·decided_at 채우기(폴더를 batch3/ 로 옮겨도 된다). 근거 locator 가 없거나 kind·관계가 ERD 에 없거나 사용자 결정이 아닌 것만 여기 둔다.

| id | kind | 대상 → 값 | 왜 제안인가 |
|---|---|---|---|
| B3-P-ADV-01 | adverse_tuple_assign | M16/10 → 2 튜플 | 「공기색전」 수식 튜플 — 「카테터 관련」 처리 미정 |
| B3-P-NEC-01 | scope_review | §4.1 사건 사전 괴사 동의어 「피부 괴사」 · §2.8 site layer | 동의어 제거 kind 없음 · 표현 20 남짓 범위 |
| B3-P-R16-01 | edge_create | R16 {"kind": "dict_value", "dict": {"dictionary": "modality_subcategory", "id": "SUB-6d6c52287f"}} → {"kind": "locator", "locator": "treatment-sequence.json:incompatible_same_day[].pair[]@3/0"} | 끝 person_condition 레코드 없음 — 기존 조건 지정 또는 ERD 출처 추가(사람) |
| B3-P-R16-02 | edge_create | R16 {"kind": "dict_value", "dict": {"dictionary": "modality_subcategory", "id": "SUB-68582f5184"}} → {"kind": "locator", "locator": "treatment-sequence.json:incompatible_same_day[].pair[]@3/0"} | 끝 person_condition 레코드 없음 |
| B3-P-REN-03 | canonical_rename | modality M5: PRP/자가혈 → 자가혈 유래 시술 | 후보 표 「추천 · 미확정」 |
| B3-P-SIT-01 | dictionary_add | site: 턱선 += 턱라인 | 해부 이름 → 부위 동의어 — 코디 추출(사람 확인) |
| B3-P-SIT-02 | dictionary_add | site: 코 += 코끝 | 해부 이름 → 부위 동의어 — 코디 추출 |
| B3-P-SIT-03 | dictionary_add | site: 눈 주변 += 눈밑, 눈꺼풀 | 해부 이름 → 부위 동의어 — 코디 추출 |
| B3-P-SIT-04 | dictionary_add | site: 이중턱/턱밑 += 턱밑, 이중턱 | 해부 이름 → 부위 동의어 — 코디 추출 |
| B3-P-SIT-05 | dictionary_add | site: 목 += 광경근 | 광경근은 원장 미등록 조각이 아님(사전 정합용 제안) |
| B3-P-SIT-06 | dictionary_add | site: 바디 (kind region) | region 「바디」 — ERD §12 후보 · 사용자 결정 없음 |
| B3-P-TEC-1 | canonical_mapping | R5:M16-1 → TEC-428b9bd04a (scope 7) | V3-8 하위분류별 기법 — 하위분류 라벨 근거(임상 확인 필요) |
| B3-P-TEC-2 | canonical_mapping | R5:M16-2 → TEC-428b9bd04a (scope 8) | V3-8 하위분류별 기법 — 하위분류 라벨 근거(임상 확인 필요) |
| B3-P-TEC-3 | canonical_mapping | R5:M16-3 → TEC-428b9bd04a (scope 9) | V3-8 하위분류별 기법 — 하위분류 라벨 근거(임상 확인 필요) |
| B3-P-TEC-4 | canonical_mapping | R5:M16-4 → TEC-428b9bd04a (scope 5) | V3-8 하위분류별 기법 — 하위분류 라벨 근거(임상 확인 필요) |
| B3-P-TEC-DCA | canonical_mapping | R5:M16-DCA → TEC-545a700199 (scope 11) | V3-8 하위분류별 기법 — 하위분류 라벨 근거(임상 확인 필요) |
| B3-P-TEC-LIPO | canonical_mapping | R5:M16-LIPO → TEC-545a700199 (scope 9) | V3-8 하위분류별 기법 — 하위분류 라벨 근거(임상 확인 필요) |

## 확인만 한 것(파일 없음)

- **HIFU·RF·필링·MTS·LED·토닝**(묶음 1 동의어)이 v3 에서 하위분류·계열 라벨에 닿는가 — 닿는다(보강 제안 없음): HIFU → M9 하위분류 「HIFU (초음파)」 · RF → M9 하위분류 「RF (고주파)」 · LED → M15 하위분류 「광치료(LED)」 · 토닝 → M8 하위분류 「색소/토닝」 · MTS → 계열 M12 · 필링 → 계열 M15(묶음 1 이 계열 동의어로 둠 — 하위분류 「케미컬필링」(M15-1)이 아니다; 바꾸려면 새 결정). 5차 실측: 「HIFU(슈링크/울쎄라)」 바깥 HIFU 하나(괄호 안 대안) · 「HIFU/RF(하반기)」 combo(or) · 「연말 집중 케어(필링+LED)」 combo(and).
- **결정 묶음 1 에서 미제안이던 조각 12**(`../proposed/_not_proposed_fragments.json`) 중 v3 규칙으로 근거가 생긴 것 — **0**. 크라이오·수액·줄기세포·CO2·Nd:YAG·혈관레이저·다이오드·HA 는 묶음 2A 에서 이미 결정, CaHA·PLLA·PCL·PDO 는 성분 사전(ingredient_material)이 §1.3 분해 사전 순서에 없어서 생긴 미등록이라 v3(사전 순서 그대로)로도 근거가 생기지 않는다(괄호 안 대안 「실리프팅(PDO/PCL)」은 PDO·PCL 이 분류 항목 이름이라 이미 닿음).
- **더모톡신 ② 안**(기법 사전 「진피내 주사」 추가 후 (M1, 얼굴 전체, 진피내 주사)) — 발주서가 ① 안(스킨보톡스 동의어 · batch3 CAT-01)을 골라 만들지 않았다.
- **엑소좀의 계열 재분류(옛 후보)** — 「엑소좀 통합」으로 대체(후보 표). **원천 수정 요청(`/` → `+`)** · **원장의 집** — 브론즈 2판으로 닫힘(ERD-FROZEN 부록). 2판에 부위 나열 `/` 1곳(「필러(팔자/볼)」)이 남아 있으나 V3-4 가 부위 둘을 함께로 읽는다(5차 multi_tuple) — 브론즈 3판 교정은 원장 작성자 몫.

합계 20 → 6차에서 엑소좀 3 을 approved 로 옮겨 남은 제안 17.
