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
