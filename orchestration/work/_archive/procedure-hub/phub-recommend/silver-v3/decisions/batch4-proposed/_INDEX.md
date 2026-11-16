# 결정 묶음 4 — 동의어 제안 (status=proposed · 빌드가 읽지 않음)

게이트 `out/gate/batch4.json`(·`.md`)의 옵션마다 결정 파일 하나. **같은 항목(gate_item)의 옵션은 서로 배타** — 게이트에서 하나만 고른다:
`python3 apply_gate.py --gate out/gate/batch4.json --out decisions/batch4/ --answers answers.json [--recommended]`(answers = {항목 id: 옵션 key}).
추천(★)은 원장 병기·영문 대응이 후보 하나만 가리킬 때뿐 — 부분 일치만이면 추천 없음(추정 금지).

| 항목 | 옵션 | 추천 | kind | 결정 id | 뜻 | effect |
|---|---|---|---|---|---|---|
| b4-adv/001 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-001n | 새 사건 「홍조」(분류 미정) | 닫히는 문구 자리 81/96 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 3 |
| b4-adv/002 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-ADV-002a | adverse_event_type 「아나필락시스」 의 동의어 | 닫히는 문구 자리 3/79(unlinked → auto) · 근거 「즉시형 과민반응」 ⊃ 조각 「반응」 · 원장 문구 병기 「 |
| b4-adv/002 | syn_2 |  | dictionary_add | DEC-2026-11-05-B4-ADV-002b | adverse_event_type 「과민반응」 의 동의어 | 닫히는 문구 자리 3/79(unlinked → auto) · 근거 「과민반응」 ⊃ 조각 「반응」 |
| b4-adv/002 | syn_3 |  | dictionary_add | DEC-2026-11-05-B4-ADV-002c | adverse_event_type 「실신」 의 동의어 | 닫히는 문구 자리 3/79(unlinked → auto) · 근거 「혈관미주신경성 반응」 ⊃ 조각 「반응」 |
| b4-adv/003 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-ADV-003a | adverse_event_type 「화상」 의 동의어 | 닫히는 문구 자리 3/70(unlinked → auto) · 근거 「열손상」 ⊃ 조각 「손상」 |
| b4-adv/004 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-004n | 새 사건 「알레르기」(분류 미정) | 닫히는 문구 자리 1/67 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 1 |
| b4-adv/005 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-ADV-005a | adverse_event_type 「실신」 의 동의어 | 닫히는 문구 자리 0/45(unlinked → auto) · 근거 「혈관미주신경성 반응」 ⊃ 조각 「신경」 |
| b4-adv/006 | syn_1 | ★ | dictionary_add | DEC-2026-11-05-B4-ADV-006a | adverse_event_type 「건조」 의 동의어 | 닫히는 문구 자리 40/43(unlinked → auto) · 근거 조각 「건조감」 ⊃ 「건조」 — 표기 변형(접미 감·함·증 |
| b4-adv/006 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-006n | 새 사건 「건조감」(분류 미정) | 닫히는 문구 자리 40/43 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 27 |
| b4-adv/007 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-ADV-007a | adverse_event_type 「감각 이상」 의 동의어 | 닫히는 문구 자리 7/32(unlinked → auto) · 근거 「감각 이상」 ⊃ 조각 「이상」 |
| b4-adv/008 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-008n | 새 사건 「흉터」(분류 미정) | 닫히는 문구 자리 17/31 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 7 |
| b4-adv/009 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-ADV-009a | adverse_event_type 「낙설」 의 동의어 | 닫히는 문구 자리 16/29(unlinked → auto) · 근거 「각질 박리」 ⊃ 조각 「각질」 |
| b4-adv/009 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-009n | 새 사건 「각질」(분류 미정) | 닫히는 문구 자리 16/29 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 6 |
| b4-adv/011 | syn_1 | ★ | dictionary_add | DEC-2026-11-05-B4-ADV-011a | adverse_event_type 「경결」 의 동의어 | 닫히는 문구 자리 25/26(unlinked → auto) · 근거 조각 「경결감」 ⊃ 「경결」 — 표기 변형(접미 감·함·증 |
| b4-adv/011 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-011n | 새 사건 「경결감」(분류 미정) | 닫히는 문구 자리 25/26 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 1 |
| b4-adv/012 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-012n | 새 사건 「딱지」(분류 미정) | 닫히는 문구 자리 22/26 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 1 |
| b4-adv/013 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-013n | 새 사건 「안검하수」(분류 미정) | 닫히는 문구 자리 15/25 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 5 |
| b4-adv/014 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-ADV-014a | adverse_event_type 「감각 이상」 의 동의어 | 닫히는 문구 자리 10/21(unlinked → auto) · 근거 「감각 이상」 ⊃ 조각 「감각」 · 「감각둔화」 ⊃ 조각  |
| b4-adv/015 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-015n | 새 사건 「가피」(분류 미정) | 닫히는 문구 자리 7/19 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 1 |
| b4-adv/018 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-018n | 새 사건 「농」(분류 미정) | 닫히는 문구 자리 1/16 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 14 |
| b4-adv/019 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-019n | 새 사건 「따가움」(분류 미정) | 닫히는 문구 자리 10/16 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 6 |
| b4-adv/020 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-ADV-020a | adverse_event_type 「색소침착」 의 동의어 | 닫히는 문구 자리 6/16(unlinked → auto) · 근거 「염증후 색소침착」 ⊃ 조각 「염증」 |
| b4-adv/021 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-021n | 새 사건 「색소탈실」(분류 미정) | 닫히는 문구 자리 4/15 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 12 |
| b4-adv/022 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-022n | 새 사건 「실명」(분류 미정) | 닫히는 문구 자리 9/15 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 13 |
| b4-adv/023 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-023n | 새 사건 「정상」(분류 미정) | 닫히는 문구 자리 0/15 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 12 |
| b4-adv/025 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-ADV-025a | adverse_event_type 「감염」 의 동의어 | 닫히는 문구 자리 1/14(unlinked → auto) · 근거 원장 문구 병기 「고열(감염)」 |
| b4-adv/025 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-025n | 새 사건 「고열」(분류 미정) | 닫히는 문구 자리 1/14 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 13 |
| b4-adv/027 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-ADV-027a | adverse_event_type 「멍」 의 동의어 | 닫히는 문구 자리 5/14(unlinked → auto) · 근거 「반상출혈」 ⊃ 조각 「출혈」 |
| b4-adv/027 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-027n | 새 사건 「출혈」(분류 미정) | 닫히는 문구 자리 5/14 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 1 |
| b4-adv/028 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-028n | 새 사건 「필링」(분류 미정) | 닫히는 문구 자리 6/14 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 6 |
| b4-adv/034 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-034n | 새 사건 「발열」(분류 미정) | 닫히는 문구 자리 1/12 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 11 |
| b4-adv/036 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-036n | 새 사건 「비후성」(분류 미정) | 닫히는 문구 자리 3/12 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 2 |
| b4-adv/037 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-037n | 새 사건 「연하곤란」(분류 미정) | 닫히는 문구 자리 10/12 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 12 |
| b4-adv/039 | syn_1 | ★ | dictionary_add | DEC-2026-11-05-B4-ADV-039a | adverse_event_type 「소양감」 의 동의어 | 닫히는 문구 자리 11/11(unlinked → auto) · 근거 조각 「가려움증」 ⊃ 「가려움」 — 표기 변형(접미 감·함 |
| b4-adv/039 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-039n | 새 사건 「가려움증」(분류 미정) | 닫히는 문구 자리 11/11 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 9 |
| b4-adv/041 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-ADV-041a | adverse_event_type 「색소침착」 의 동의어 | 닫히는 문구 자리 7/11(unlinked → auto) · 근거 「색소침착」 ⊃ 조각 「색소」 · 「과색소침착」 ⊃ 조각 「 |
| b4-adv/045 | syn_1 | ★ | dictionary_add | DEC-2026-11-05-B4-ADV-045a | adverse_event_type 「건조」 의 동의어 | 닫히는 문구 자리 9/10(unlinked → auto) · 근거 조각 「건조함」 ⊃ 「건조」 — 표기 변형(접미 감·함·증  |
| b4-adv/045 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-045n | 새 사건 「건조함」(분류 미정) | 닫히는 문구 자리 9/10 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 6 |
| b4-adv/047 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-047n | 새 사건 「마비」(분류 미정) | 닫히는 문구 자리 0/10 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 2 |
| b4-adv/048 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-048n | 새 사건 「물집」(분류 미정) | 닫히는 문구 자리 6/10 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 3 |
| b4-adv/049 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-049n | 새 사건 「민감성」(분류 미정) | 닫히는 문구 자리 5/10 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 1 |
| b4-adv/050 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-ADV-050a | adverse_event_type 「비대칭」 의 동의어 | 닫히는 문구 자리 0/10(unlinked → auto) · 근거 「안면 비대칭」 ⊃ 조각 「안면」 |
| b4-adv/057 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-057n | 새 사건 「피로감」(분류 미정) | 닫히는 문구 자리 7/9 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 3 |
| b4-adv/058 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-058n | 새 사건 「호흡곤란」(분류 미정) | 닫히는 문구 자리 0/9 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 8 |
| b4-adv/061 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-ADV-061a | adverse_event_type 「낙설」 의 동의어 | 닫히는 문구 자리 7/8(unlinked → auto) · 근거 「각질 박리」 ⊃ 조각 「박리」 |
| b4-adv/061 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-061n | 새 사건 「박리」(분류 미정) | 닫히는 문구 자리 7/8 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 6 |
| b4-adv/062 | syn_1 | ★ | dictionary_add | DEC-2026-11-05-B4-ADV-062a | adverse_event_type 「자극감」 의 동의어 | 닫히는 문구 자리 5/8(unlinked → auto) · 근거 「자극감」 ⊃ 조각 「자극」 — 표기 변형(접미 감·함·증 또 |
| b4-adv/068 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-068n | 새 사건 「농양」(분류 미정) | 닫히는 문구 자리 4/7 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 4 |
| b4-adv/071 | new_event |  | dictionary_add | DEC-2026-11-05-B4-ADV-071n | 새 사건 「메스꺼움」(분류 미정) | 닫히는 문구 자리 4/7 · 원장 문구에서 멤버 하나 전체로 쓰인 자리 4 |
| b4-adv/076 | syn_1 | ★ | dictionary_add | DEC-2026-11-05-B4-ADV-076a | adverse_event_type 「부종」 의 동의어 | 닫히는 문구 자리 0/7(unlinked → auto) · 근거 조각 「부종이」 ⊃ 「부종」 — 표기 변형(접미 감·함·증 또 |
| b4-sit/001 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-001a | relative_site 「주사 부위」 의 동의어 | 닫히는 문구 자리 0/16(unlinked → auto) · 근거 「주사 부위」 ⊃ 조각 「부위」 · 「주입 부위」 ⊃ 조각  |
| b4-sit/001 | syn_2 |  | dictionary_add | DEC-2026-11-05-B4-SIT-001b | relative_site 「시술 부위」 의 동의어 | 닫히는 문구 자리 0/16(unlinked → auto) · 근거 「시술 부위」 ⊃ 조각 「부위」 |
| b4-sit/002 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-002a | site 「근육」 의 동의어 | 닫히는 문구 자리 0/14(unlinked → auto) · 근거 조각 「근육통」 ⊃ 「근육」 |
| b4-sit/003 | syn_1 | ★ | dictionary_add | DEC-2026-11-05-B4-SIT-003a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/12(unlinked → auto) · 근거 조각 「피부가」 ⊃ 「피부」 — 표기 변형(접미 감·함·증  |
| b4-sit/004 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-004a | adverse_qualifier 「필러」 의 동의어 | 닫히는 문구 자리 0/8(unlinked → auto) · 근거 조각 「필러가」 ⊃ 「필러」 — 표기 변형(접미 감·함·증 또 |
| b4-sit/005 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-005a | adverse_qualifier 「지방」 의 동의어 | 닫히는 문구 자리 0/6(unlinked → auto) · 근거 조각 「지방이」 ⊃ 「지방」 — 표기 변형(접미 감·함·증 또 |
| b4-sit/006 | syn_1 | ★ | dictionary_add | DEC-2026-11-05-B4-SIT-006a | site 「혈관」 의 동의어 | 닫히는 문구 자리 0/6(unlinked → auto) · 근거 조각 「혈관에」 ⊃ 「혈관」 — 표기 변형(접미 감·함·증 또 |
| b4-sit/007 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-007a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/5(unlinked → auto) · 근거 조각 「피부에서」 ⊃ 「피부」 |
| b4-sit/008 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-008a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/5(unlinked → auto) · 근거 조각 「피부염」 ⊃ 「피부」 |
| b4-sit/009 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-009a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/5(unlinked → auto) · 근거 조각 「피부톤」 ⊃ 「피부」 |
| b4-sit/010 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-010a | ingredient_material 「PDLLA+HA」 의 동의어 | 닫히는 문구 자리 0/4(unlinked → auto) · 근거 영문 낱말 「HA」 ↔ 「PDLLA+HA」 |
| b4-sit/010 | syn_2 |  | dictionary_add | DEC-2026-11-05-B4-SIT-010b | ingredient_material 「PN+HA」 의 동의어 | 닫히는 문구 자리 0/4(unlinked → auto) · 근거 영문 낱말 「HA」 ↔ 「PN+HA」 |
| b4-sit/011 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-011a | adverse_qualifier 「필러」 의 동의어 | 닫히는 문구 자리 0/4(unlinked → auto) · 근거 조각 「필러는」 ⊃ 「필러」 — 표기 변형(접미 감·함·증 또 |
| b4-sit/012 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-012a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/3(unlinked → auto) · 근거 조각 「접촉피부염」 ⊃ 「피부」 |
| b4-sit/013 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-013a | adverse_qualifier 「지방」 의 동의어 | 닫히는 문구 자리 0/3(unlinked → auto) · 근거 조각 「지방위축」 ⊃ 「지방」 |
| b4-sit/014 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-014a | adverse_qualifier 「지방」 의 동의어 | 닫히는 문구 자리 0/3(unlinked → auto) · 근거 조각 「지방의」 ⊃ 「지방」 — 표기 변형(접미 감·함·증 또 |
| b4-sit/015 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-015a | adverse_qualifier 「지방」 의 동의어 | 닫히는 문구 자리 0/3(unlinked → auto) · 근거 조각 「지방이식」 ⊃ 「지방」 |
| b4-sit/016 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-016a | adverse_qualifier 「지방」 의 동의어 | 닫히는 문구 자리 0/3(unlinked → auto) · 근거 조각 「지방흡입」 ⊃ 「지방」 |
| b4-sit/017 | syn_1 | ★ | dictionary_add | DEC-2026-11-05-B4-SIT-017a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/3(unlinked → auto) · 근거 조각 「피부를」 ⊃ 「피부」 — 표기 변형(접미 감·함·증 또 |
| b4-sit/018 | syn_1 | ★ | dictionary_add | DEC-2026-11-05-B4-SIT-018a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/3(unlinked → auto) · 근거 조각 「피부의」 ⊃ 「피부」 — 표기 변형(접미 감·함·증 또 |
| b4-sit/019 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-019a | site 「혈관」 의 동의어 | 닫히는 문구 자리 0/3(unlinked → auto) · 근거 조각 「혈관염」 ⊃ 「혈관」 |
| b4-sit/020 | syn_1 | ★ | dictionary_add | DEC-2026-11-05-B4-SIT-020a | site 「혈관」 의 동의어 | 닫히는 문구 자리 0/3(unlinked → auto) · 근거 조각 「혈관이」 ⊃ 「혈관」 — 표기 변형(접미 감·함·증 또 |
| b4-sit/021 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-021a | ingredient_material 「PDO+PCL」 의 동의어 | 닫히는 문구 자리 0/2(unlinked → auto) · 근거 영문 낱말 「PDO」 ↔ 「PDO+PCL」 |
| b4-sit/022 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-022a | site 「팔자주름」 의 동의어 | 닫히는 문구 자리 0/2(unlinked → auto) · 근거 영문 낱말 「fold」 ↔ 「Nasolabial Fold」 |
| b4-sit/023 | syn_1 | ★ | dictionary_add | DEC-2026-11-05-B4-SIT-023a | site 「얼굴」 의 동의어 | 닫히는 문구 자리 0/2(unlinked → auto) · 근거 조각 「얼굴이」 ⊃ 「얼굴」 — 표기 변형(접미 감·함·증 또 |
| b4-sit/024 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-024a | site 「이마」 의 동의어 | 닫히는 문구 자리 0/2(unlinked → auto) · 근거 조각 「이마나」 ⊃ 「이마」 |
| b4-sit/025 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-025a | adverse_qualifier 「지방」 의 동의어 | 닫히는 문구 자리 0/2(unlinked → auto) · 근거 조각 「지방층」 ⊃ 「지방」 |
| b4-sit/025 | syn_2 |  | dictionary_add | DEC-2026-11-05-B4-SIT-025b | site 「피하 지방층」 의 동의어 | 닫히는 문구 자리 0/2(unlinked → auto) · 근거 「피하 지방층」 ⊃ 조각 「지방층」 |
| b4-sit/026 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-026a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/2(unlinked → auto) · 근거 조각 「피부색」 ⊃ 「피부」 |
| b4-sit/027 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-027a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/2(unlinked → auto) · 근거 조각 「피부색이」 ⊃ 「피부」 |
| b4-sit/028 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-028a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/2(unlinked → auto) · 근거 조각 「피부위축」 ⊃ 「피부」 |
| b4-sit/029 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-029a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/2(unlinked → auto) · 근거 조각 「피부질환이」 ⊃ 「피부」 |
| b4-sit/030 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-030a | adverse_qualifier 「필러」 의 동의어 | 닫히는 문구 자리 0/2(unlinked → auto) · 근거 조각 「필러를」 ⊃ 「필러」 — 표기 변형(접미 감·함·증 또 |
| b4-sit/031 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-031a | ingredient_material 「PDO+PCL」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 영문 낱말 「PCL」 ↔ 「PDO+PCL」 |
| b4-sit/032 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-032a | ingredient_material 「PN/PDRN」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 영문 낱말 「PDRN」 ↔ 「PN/PDRN」 |
| b4-sit/033 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-033a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 조각 「건성피부」 ⊃ 「피부」 |
| b4-sit/034 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-034a | ingredient_material 「PDLLA+HA」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 영문 낱말 「비HA」 ↔ 「PDLLA+HA」 |
| b4-sit/034 | syn_2 |  | dictionary_add | DEC-2026-11-05-B4-SIT-034b | ingredient_material 「PN+HA」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 영문 낱말 「비HA」 ↔ 「PN+HA」 |
| b4-sit/035 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-035a | ingredient_material 「PDLLA+HA」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 영문 낱말 「비가교HA」 ↔ 「PDLLA+HA」 |
| b4-sit/035 | syn_2 |  | dictionary_add | DEC-2026-11-05-B4-SIT-035b | ingredient_material 「PN+HA」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 영문 낱말 「비가교HA」 ↔ 「PN+HA」 |
| b4-sit/036 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-036a | ingredient_material 「PDLLA+HA」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 영문 낱말 「비가교HA와의」 ↔ 「PDLLA+HA」 |
| b4-sit/036 | syn_2 |  | dictionary_add | DEC-2026-11-05-B4-SIT-036b | ingredient_material 「PN+HA」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 영문 낱말 「비가교HA와의」 ↔ 「PN+HA」 |
| b4-sit/037 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-037a | site 「혈관」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 조각 「신경혈관손상」 ⊃ 「혈관」 |
| b4-sit/038 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-038a | site 「얼굴 전체」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 「얼굴 전체」 ⊃ 조각 「전체」 · 「전체얼굴」 ⊃ 조각 「전 |
| b4-sit/039 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-039a | site 「눈 주변」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 「눈 주변」 ⊃ 조각 「주변」 |
| b4-sit/040 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-040a | site 「이중턱/턱밑」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 「이중턱/턱밑」 ⊃ 조각 「턱밑」 |
| b4-sit/041 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-041a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 조각 「피부결」 ⊃ 「피부」 |
| b4-sit/042 | syn_1 | ★ | dictionary_add | DEC-2026-11-05-B4-SIT-042a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 조각 「피부에」 ⊃ 「피부」 — 표기 변형(접미 감·함·증 또 |
| b4-sit/043 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-043a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 조각 「피부톤에서」 ⊃ 「피부」 |
| b4-sit/044 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-044a | site 「피부」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 조각 「피부형에서는」 ⊃ 「피부」 |
| b4-sit/045 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-045a | site 「피하 지방층」 의 동의어 | 닫히는 문구 자리 1/1(unlinked → auto) · 근거 「피하 지방층」 ⊃ 조각 「피하」 · 「피하지방」 ⊃ 조각 「 |
| b4-sit/046 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-046a | adverse_qualifier 「필러」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 조각 「필러의」 ⊃ 「필러」 — 표기 변형(접미 감·함·증 또 |
| b4-sit/047 | syn_1 |  | dictionary_add | DEC-2026-11-05-B4-SIT-047a | site 「혈관」 의 동의어 | 닫히는 문구 자리 0/1(unlinked → auto) · 근거 조각 「혈관계」 ⊃ 「혈관」 |
| b4-prc/001 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-001a | modality_subcategory_label 「HA (물광)」(M4)로 읽기(그 참조  | 풀리는 ⑨ 참조 0/7(원장 자리 0) · 근거 영문 낱말 「HA」 ↔ 「HA (물광)」 |
| b4-prc/001 | syn_2 |  | dictionary_add | DEC-2026-11-05-B4-PRC-001b | ingredient_material 「PDLLA+HA」 의 동의어 | 풀리는 ⑨ 참조 0/7(원장 자리 0) · 성분 사전은 §1.3 분해 사전 순서 밖이라 참조를 풀지 않는다 · 근거 영문 낱말 |
| b4-prc/001 | syn_3 |  | dictionary_add | DEC-2026-11-05-B4-PRC-001c | ingredient_material 「PN+HA」 의 동의어 | 풀리는 ⑨ 참조 0/7(원장 자리 0) · 성분 사전은 §1.3 분해 사전 순서 밖이라 참조를 풀지 않는다 · 근거 영문 낱말 |
| b4-prc/002 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-002a | product_name 「인모드」(M9)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 2/7(원장 자리 2) · 근거 원장 이름 병기 「인모드(바디)」 |
| b4-prc/003 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-003a | product_name 「리쥬란 힐러」(M4)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 4/5(원장 자리 8) · 근거 「리쥬란 힐러」 ⊃ 조각 「리쥬란」 |
| b4-prc/003 | map_2 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-003b | product_name 「리쥬란아이」(M4)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 4/5(원장 자리 8) · 근거 「리쥬란아이」 ⊃ 조각 「리쥬란」 |
| b4-prc/004 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-004a | modality_subcategory_label 「냉각지방분해」(M14)로 읽기(그 참조  | 풀리는 ⑨ 참조 2/4(원장 자리 6) · 근거 「냉각지방분해」 ⊃ 조각 「지방분해」 |
| b4-prc/004 | map_2 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-004b | modality_subcategory_label 「지방분해주사 (마케팅명)」(M16)로 읽 | 풀리는 ⑨ 참조 2/4(원장 자리 6) · 근거 「지방분해주사 (마케팅명)」 ⊃ 조각 「지방분해」 |
| b4-prc/006 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-006a | product_name 「쥬베룩볼륨」(M3)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 0/4(원장 자리 0) · 근거 「쥬베룩볼륨」 ⊃ 조각 「볼륨」 |
| b4-prc/007 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-007a | modality_subcategory_label 「이온토포레시스」(M15)로 읽기(그 참조 | 풀리는 ⑨ 참조 3/4(원장 자리 3) · 근거 원장 이름 병기 「이온토포레시스(비타민C)」 |
| b4-prc/015 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-015a | modality_subcategory_label 「색소/토닝」(M8)로 읽기(그 참조 자리 | 풀리는 ⑨ 참조 0/3(원장 자리 0) · 근거 「색소/토닝」 ⊃ 조각 「색소」 |
| b4-prc/016 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-016a | modality_subcategory_label 「여드름 전용」(M15)로 읽기(그 참조  | 풀리는 ⑨ 참조 0/3(원장 자리 0) · 근거 「여드름 전용」 ⊃ 조각 「여드름」 |
| b4-prc/018 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-018a | modality_subcategory_label 「지방분해주사 (마케팅명)」(M16)로 읽 | 풀리는 ⑨ 참조 0/3(원장 자리 0) · 근거 「지방분해주사 (마케팅명)」 ⊃ 조각 「주사」 |
| b4-prc/020 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-020a | modality_subcategory_label 「제모」(M8)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 2/2(원장 자리 9) · 근거 조각 「제모레이저」 ⊃ 「제모」 |
| b4-prc/030 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-030a | modality_subcategory_label 「CaHA (칼슘하이드록시아파타이트)」(M | 풀리는 ⑨ 참조 0/2(원장 자리 0) · 근거 영문 낱말 「CaHA」 ↔ 「CaHA (칼슘하이드록시아파타이트)」 |
| b4-prc/030 | map_2 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-030b | product_name 「디클래씨」(M3)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 0/2(원장 자리 0) · 근거 영문 낱말 「CaHA」 ↔ 「DCLASSY CaHA」 |
| b4-prc/031 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-031a | modality_subcategory_label 「바디 EMS」(M10)로 읽기(그 참조  | 풀리는 ⑨ 참조 0/2(원장 자리 0) · 근거 영문 낱말 「EMS」 ↔ 「바디 EMS」 |
| b4-prc/031 | map_2 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-031b | modality_subcategory_label 「페이셜 EMS」(M10)로 읽기(그 참조 | 풀리는 ⑨ 참조 0/2(원장 자리 0) · 근거 영문 낱말 「EMS」 ↔ 「페이셜 EMS」 |
| b4-prc/035 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-035a | modality_subcategory_label 「IPL」(M8)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 1/2(원장 자리 1) · 근거 원장 이름 병기 「IPL(광선치료)」 |
| b4-prc/038 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-038a | product_name 「쿨스컬프팅」(M14)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 2/2(원장 자리 2) · 근거 원장 이름 병기 「쿨스컬프팅(냉동지방분해)」 |
| b4-prc/046 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-046a | modality_subcategory_label 「재생/면역」(M16)로 읽기(그 참조 자 | 풀리는 ⑨ 참조 0/2(원장 자리 0) · 근거 「재생/면역」 ⊃ 조각 「재생」 |
| b4-prc/049 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-049a | modality_subcategory_label 「주입장비」(M15)로 읽기(그 참조 자리 | 풀리는 ⑨ 참조 0/2(원장 자리 0) · 근거 「주입장비」 ⊃ 조각 「주입」 |
| b4-prc/050 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-050a | modality_subcategory_label 「탈모(비수술)」(M15)로 읽기(그 참조 | 풀리는 ⑨ 참조 0/2(원장 자리 0) · 근거 「탈모(비수술)」 ⊃ 조각 「탈모」 |
| b4-prc/051 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-051a | product_name 「울쎄라」(M9)로 읽기(그 참조 자리만) | 풀리는 ⑨ 참조 2/2(원장 자리 2) · 근거 원장 이름 병기 「울쎄라(턱라인)」 |
| b4-prc/054 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-054a | modality_subcategory_label 「프락셔널」(M8)로 읽기(그 참조 자리만 | 풀리는 ⑨ 참조 2/2(원장 자리 2) · 근거 원장 이름 병기 「프락셔널(피부결)」 |
| b4-prc/054 | syn_2 |  | dictionary_add | DEC-2026-11-05-B4-PRC-054b | site 「피부」 의 동의어 | 풀리는 ⑨ 참조 2/2(원장 자리 2) · 근거 조각 「피부결」 ⊃ 「피부」 |
| b4-prc/059 | map_1 |  | canonical_mapping | DEC-2026-11-05-B4-PRC-059a | modality_subcategory_label 「흉터 전용」(M15)로 읽기(그 참조 자 | 풀리는 ⑨ 참조 0/2(원장 자리 0) · 근거 「흉터 전용」 ⊃ 조각 「흉터」 |
