# 실버 빌드 6차 발주서 — 빌더 v3.1 반영 + 결정 묶음 4 제안 (2026-11-05)

## A. 빌더 v3.1 반영 (코드)
ERD 입력을 `erd-v3.1.json`·`erd-v3.1-dictionaries.json` 으로. V3.1-1~10 전부 구현(규칙 정본 `erd-v3.1.md` · 참조 구현 `erd-v3.1-tuples.py` · 대조 기준 `erd-v3.1-tuples.json` — 결정 적용 전 수치 차이 0).
핵심 구조 변경: ① 부작용 단위 세 칸(사건·부위·물질) · 경과는 R15 속성(원칙 C: 사건 멤버에 붙은 경과만) ② adverse_expression 개체·R29 삭제 → **문구 사전**(phrase_dictionary · 정규화형 1줄 · raw_variants · unit 매핑 · parsed · status auto/approved/unlinked · locators) + R15 `source_phrases[]` 부록 + 단위/R20 `explanations[]` ③ 조합 단위를 세 칸 전부 사전 값이면 어느 출처든 생성 ④ person_condition 사전 식별 + phrases 부록 ⑤ clinical_rule(disclosure·product_note) + R32 ⑥ kind product_reclassify · dictionary_remove · phrase_map · canonical_rename 유지 ⑦ 수식어 목록 138·phrase_shape · R12 session_count/index.
- 기존 결정(batch1·2a·2b·3·_bootstrap)은 그대로 적용. 거부되는 것이 있으면 사유를 report 에(특히 옛 네 칸 adverse_tuple_assign — course 가 들어 있으면 R15 속성으로 옮겨 적용).
- 엑소좀 EXO-02·05·06(batch3-proposed)은 이제 kind·관계가 있으니 **approved 로 올려 적용**(사용자 확정 방향 · 근거 locator 있음). R32 로 「화장품 허가 (주사 사용 불법)」 규칙을 엑소좀 제품 전부에.
- `tests/`: 열거기가 v3.1 json 을 읽어 새 경우(2,514)를 요구 → 빠진 테스트를 만들고 구멍은 고친다. `run_tests.py` PASS · `check.py` 전부 PASS(v3.1 항목으로 갱신).

## B. 6차 빌드
`build.py` → `check.py` → `tests/run_tests.py`. report.md 「6차 빌드 · ERD v3.1 + 엑소좀 approved」: 5차 대비 변화표(개체·관계·게이트·충돌) · 문구 사전 항목 수·auto/unlinked · 단위 수(사건별 조합) · R15 수·경과 있는 엣지 수 · 조건 단위 수.

## C. 결정 묶음 4 제안 — 동의어 (proposed · `decisions/batch4-proposed/` · 게이트 자료 `out/gate/batch4.json`(2B 스키마))
기계가 근거를 붙여 제안, 추정 금지(근거 없으면 recommended=null).
1. **부작용 문구 동의어**: 문구 사전 unlinked 항목에서 사건을 못 찾은 조각을 빈도순으로 — 각 조각에 대해 사건 사전 후보(정규화 부분 일치·영문 대응·원장 complications 이름에 함께 쓰인 표기) ≤3 과 그 조각이 나오는 locator 전부. 예: 경결감→경결 · 붓기→부종 · 빨개짐→홍반 · 따가움→통증. 상위 80 조각.
2. **부위·조직 조각**(눈가·얼굴·피부·입술 등 부작용 문구의 부위)과 **물질 조각**.
3. **시술 쪽 남은 조각**: ⑨ open 의 상위 미등록 조각(HA·바디·리쥬란·볼륨·이모드·심부·지방분해·비타민C·810nm…) 각각 — 하위분류/제품/부위/성분 사전 후보 ≤3 + locator. 상위 60.
4. 각 제안은 승인 시 그대로 적용되는 결정 파일(dictionary_add / phrase_map / canonical_mapping) 완성형.
5. `apply_gate.py --gate out/gate/batch4.json --out decisions/batch4/`.
항목마다 「승인하면 닫히는 문구 수/참조 수」를 effect 에 숫자로.

## 규칙·보고
ERD v3.1 정본 · 원장 불변 · provenance 필수 · 재실행 바이트 동일 · Python 표준 라이브러리 · 커밋 금지 · 금지 목록 이전과 같음.
보고: A 반영 위치 · 거부 결정 · tests/check 결과 · B 변화표 · C 항목 수(1~3 각각)·추천 있는 수·닫히는 문구/참조 합. 본문 재붙임 금지.
