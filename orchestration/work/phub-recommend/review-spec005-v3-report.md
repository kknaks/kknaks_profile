# 검수 보고서 — SPEC-005 v3(0.3.0) · WORK-005

작성 2026-10-31 · 검수자 reviewer 워커(읽기 전용 · 스펙 · 코드 수정 없음) · 발주서 `phub-recommend-review-spec005-v3-brief.md`
대상 `SPEC-005.md`(0.3.0 · updated 10-31) · `WORK-005.md`(todo) · 대조 정본 `fail-triage.md` · `.json`(B 239 · build e9d30ace) · 허브 코드 `phub-recommend/backend`(HEAD 64fe929) · `gold-export.json`(e9d30ace) · `runs/runs.jsonl`(239) · 실버 `step5 · step7 · step8` · `_RESUME.md` §2

## 판정 — **FAIL** (FAIL 8 · WARN 8)

한 줄: v3 가 적은 조항은 실물 이름과 대체로 맞고 결정표와 충돌하지 않지만, **B 239 행을 조항으로 전수 대조하면 분모 222 행 중 72 행(32%)이 어느 조항에도 닿지 않아** 끝 조건 「재인용률 ≥ 90%」를 스펙 자신이 만족시킬 수 없다. §5-13 · §5-14 표의 근거 열과 묶음 열이 어긋난 것이 주 원인이고, §6-5 의 분모 · 판정 규칙 · 현 중앙값 표도 숫자가 실물과 다르거나 셈 규칙이 안 적혀 재현되지 않는다.

| 기준 | 판정 | 요지 |
|---|---|---|
| 1 전수 대조(묶음 → 조항 · 대응 없음 0) | **FAIL** | 분모 222 중 대응 없음 72(resolve 만 호출 17 + 조항 없음 55). §5-14 근거 열 ↔ 묶음 열 불일치 20행 · §5-13 의도 행에 근거로 센 묶음이 빠진 25행 · 조항 자체 없음 3행(F-1) |
| 2 실물 대조(도구 · section · 노드 · fact 이름) | **FAIL(경미)** | section 17 · 노드 13 · 도구 9 · 오류 문구 · self_pair 4 · attrs_text 키 · SC spec 키 · F-E fact id 11 개 전부 실물과 같음. 틀린 곳 2: F-D `pih[].prevention`(없는 칸) · F-C treats `claims[].reason`(실물은 `row.evidence.role`)(F-8) · 엣지 종류 이름 2곳 WARN(W-1) |
| 3 결정표 충돌 | PASS | LLM 없음 · 결정론 · slim D-14(동봉은 요약 + id · 크기 상한) · G13 · 충돌 = resolved 하나(T5 펼침 「가장 엄격 하나 + by_unit」) · 실버 수정 없음(F-A~F-E 는 빌드 규칙 · `family:None` 은 읽는 칸 수정) 전부 어긋남 없음. 10-31 V-1~V-5 위임 행과도 일치 |
| 4 끝 조건(§6-5) 검증 가능성 | **FAIL** | 분모 223 ≠ 실물 222(F-2) · 판정 규칙이 옛 gold_hits fact id 에 묶여 새 fact 66행을 못 셈(F-3) · 조항만으로 닫히는 상한 150/222 = 67.6% < 90%(F-4) · 현 중앙값 표 셈 규칙 미기재 · case3 224 ≠ 201(F-5) |
| 5 WORK-005 | **FAIL** | WP 의존 순서 · WP 마다 시험 · Done Criteria ↔ §6-5 1:1 은 맞음. WP-0 「triage.py import」 는 모듈 수준 실행 때문에 불가(F-6) · 코드 표면 누락 7곳(F-7) |
| 6 V-1~V-5 외 추측 자리 | WARN | F-A ⑤ 연결 키(W-2) · §5-15 「5건 문턱」(W-3) · §6-5 표 필터(F-5 에 포함) |

## FAIL 목록

### F-1 · §5-13 · §5-14 · §6-5 — B 행 72 가 어느 조항에도 닿지 않음(기준 1)

근거: `fail-triage.json` rows(cls B 239)를 행마다 (빠진 칸 · jev_intent · tools_called · owner 종류 · section) 으로 읽고 §5-13 의도 × 동봉 표 · §5-14 의도 → section 표 · §4-3 F-A~F-E · §5-5 · §5-7 로 대응시켰다(부록 A 묶음 표 · 부록 B 행 전부). 허브 안 부른 17행(X0)을 빼면 분모 222. 그중:

| 갈래 | 행 | 무엇 |
|---|---|---|
| (a) §5-14 근거 열 ↔ 기본 section 열 불일치 | 20 | 같은 표에서 근거로 센 section 이 그 의도 묶음에 없다 — I-03 overview 1 · **I-04 overview 5 · timeline 1** · I-05 overview 1 · disclosure 1 · ops 1 · I-06 disclosure 1 · I-08 safety.side_effects 1 · **I-09 aftercare 2 · overview 2** · **I-10 overview 2 · disclosure 2**. 이 때문에 §5-14 본문 「case3 Jev 18건은 기본 묶음이 덮는다」 도 틀림 — 18 중 7(Q020 · Q040 · Q042 · Q058 · Q098 · Q104 · Q170)이 안 덮임 → WORK-005 WP-3 완료 조건(「18건 … 묶음에 들어 있음을 표로」) 달성 불가 |
| (b) §5-13 의도 행에 근거로 센 묶음이 빠짐 | 25 | **I-06 에 C7 없음**(⑤ combo 안 닿음 4 + ⑥ combo full 4 = 8 — 표의 I-06 근거 「⑤ 12 · ⑥ 10」 안에 든 건들) · I-04 · I-09 에 C7 없음(2) · **I-07 · I-09 에 C12 없음**(Q201 · Q150 — C12 근거 「⑥ unit 9 중 7」 에 든 건) · I-06 에 C14 없음(⑧ Q198 2) · I-06 에 C11 없음(Q106 2) · I-11 에 C2 없음(Q025) · 1-hop 기타(Q082 package evidence · Q084 product products · Q068 unit market · Q070 unit side_effects) 4 · C10 비 I-06 10(§5-15 「compare 에서만」 결정 — 결정은 있으나 §6-5 에 미닫힘 행으로 안 적힘) |
| (c) 조항 자체 없음 | 3 | Q123 concern 이름 · Q228 product `1_identity.basis` · Q118 treats `row.evidence.role`(F-8 과 겹침) |
| (d) resolve · vocab 만 호출 | 17 | 재실행이 resolve 응답만 돌려주므로 동봉 · 섹션이 붙을 시술 노드가 없다(T1 은 「G13 요약만」). §6-5 는 「허브 호출이 있던 B」 로 분모에 넣는다 — 닫힐 수 없는 행을 분모에 둔 셈 |
| 합 | **72** | 분모 222 의 32% |

방향: ① §5-14 표를 근거 열에 맞춰 묶음에 넣거나(I-04 overview · timeline / I-09 aftercare · overview / I-10 overview · disclosure / I-05 overview · disclosure · ops / I-03 overview / I-06 disclosure / I-08 side_effects), 넣지 않을 것은 근거 열에서 빼고 §6-5 에 「닫지 않는 행」 표로 옮긴다. ② §5-13 의도 × 동봉에 I-06 C7 · C14 · C11 / I-07 · I-09 C12 / I-11 C2 를 더하거나 같은 식으로 미닫힘 명시. ③ (c) 3행은 미닫힘 명시. ④ (d) 는 §6-5 분모를 「카드 도구(T2~T8) 호출이 있던 B」 로 정의해 빼든지, 미닫힘으로 센다고 적는다. 어느 쪽이든 §6-5 목표 숫자는 F-4 대로 재계산.

### F-2 · §6-5 · §7 V-1 — 재인용률 분모 223 이 실물과 다름(기준 4)

근거: B 239 중 `tools_called == []` 는 **17행 · 문항 14**(case3 16 = 문항 13 + **case2 Q205 1**). 스펙은 case3 16 만 빼 223 으로 썼다. Q205(I-11 · pair_check 안 부름)는 WORK-005 WP-5 가 이미 「호출 없던 Q130 · Q205 제외」 로 알고 있다. 90% 기준선 201 → 200.
방향: 분모 = 「tools_called 가 빈 B 행 전부 제외 = 222」 · 문항 14 로 고치고 V-1 · WORK-005 Goal · Done Criteria 숫자 동기.

### F-3 · §6-5 판정 규칙 — 옛 gold_hits fact id 로는 새 fact 를 못 셈(기준 4)

근거: §6-5 「B 행이 닫힘 = … 그 행 `gold_hits` 의 fact id 하나 또는 정규화 인용」. `gold_hits` 는 e9d30ace export 대조 결과다. B 66행(⑤ combo 속성 27 · ⑦ 엣지 속성 18 · ⑥ unit 9 + combo 7 · concern 3 · unit 1 · product 1)은 gold_hits 에 fact id 가 **없고**(node_attr · edge_attr 만) v3 가 F-C · F-D 로 만드는 fact id(`combo:…#evidence#caveats[1]` 등)는 옛 gold_hits 에 없다. v3 동봉은 요약 + fact id 가 기본(C7 원문은 price · expectedResult ≤ 2 조합 · C12 fitzpatrick_note 1 · C1 2 만)이라 정규화 인용 경로로도 대부분 못 닫는다 → 이 66행은 규칙상 닫힐 수 없다.
방향: recheck 가 **새 gold-export(v3 빌드)** 로 `gold_match` 를 다시 돌려 행마다 gold_hits 를 갱신한 뒤 fact id 일치를 센다고 명시(두 export 해시를 리포트 머리에 · WP-0 기준선만 옛 export). 또는 「원장 경로 → 새 fact id」 대응표를 recheck 가 만든다.

### F-4 · §6-5 끝 조건 — 스펙 조항만으로 닫을 수 있는 상한이 90% 아래(기준 4)

근거: F-1 72행은 조항이 닿지 않으므로 설계상 미닫힘. 222 − 72 = 150 → **최대 67.6%**(F-3 를 고치지 않으면 더 낮음). 목표 「≥ 90%(201+)」 는 스펙 자신과 모순. 브리프 기준(「≥ 90%」)은 유지하되 조항이 따라와야 한다.
방향: F-1 ① ② 보강 후 재계산해 §6-5 표에 「조항이 닿는 행 수 / 분모」 를 적고 목표 숫자를 그 안에서 정한다(사용자 결정 자리 → §7 V 로 올림).

### F-5 · §6-5 현 중앙값 표 — 셈 규칙 미기재 · case3 셈 틀림(기준 4)

근거: `runs/runs.jsonl` 로 재계산 — case2 tool_calls 전부는 **749**, `is_error` 를 빼야 **662**(표와 일치 · recommend 58/7,262 · card 154/17,180 · pair 22/7,200 · checks 28/24,206 · vocab 9/6,314 전부 재현). 표는 「오류 호출 제외」 를 적지 않았다(check_conditions 는 오류 58건 — 빼지 않으면 86/115). case3 「허브 경로 224」 는 실물 **201**(trace.hub.tool 있는 run · 15건 400 포함) — 224 는 239 − 15 로 보이나 허브 경로 없는 run 38 이 섞인 수. `fail-triage.md` 도 201.
방향: 「case2 = trace.tool_calls 중 is_error 아닌 것 662 · case3 = trace.hub.tool 있는 run 201」 으로 적고 224 → 201.

### F-6 · WORK-005 WP-0 — triage.py 를 import 해 쓰는 설계가 성립하지 않음(기준 5)

근거: WP-0 2 「판정 = triage.py 의 norm · 포함 규칙 · fact id 일치 그대로(함수 import — 복사하지 않음)」 · 시험 「같은 모듈 객체인지(import 검사)」. `triage.py` 는 `if __name__` 없이 **모듈 수준에서** replay.json · gold-export · 원장 21 을 읽어 색인을 만들고(24~66행) 320행 분류를 돌려 `triage-rows.json` 을 쓴다(141~301행). import 하면 ① `$E` 기존 파일 변경(Done Criteria 「$E 변경 0」 위반) ② replay.json 이 없거나 옛 export 와 맞지 않으면 실패. Meta 는 triage.py 「읽기만」.
방향: recheck.py 에 `norm` · 포함 규칙(골드 쪽 8자 이상 · 양방향) · fact id 일치를 **같은 식으로 적고** 고정 입력 동일성 시험(triage 결과 320행 재분류 = 같음)으로 동일성을 증명하거나, triage.py 를 함수화(`main()` 가드)하는 수정을 범위에 넣고 Meta 「읽기만」 예외를 적는다.

### F-7 · WORK-005 Scope · Code Surface — 쓰는 곳 전부가 아님(기준 5)

근거(grep `sections` · `PAIR_MIN` · facts cols): 표에 없는 것 —
- `app/modules/gold/service.py` — `GoldToolService.resolve · procedure_card · check_conditions · compare · vocab` 는 인자를 명시 선언(`intent` 추가 필요) · `GoldState.load` 의 facts cols 7개에 `attached_to` 없음(메모리 색인 `facts_by_attach` 를 못 만듦)
- `app/modules/gold/application.py:149` — export cols 7개(attached_to 없으면 `gold-export.json` 에 안 나가 recheck · gold_match 가 못 읽음) · `scripts/gold_export.py`
- `tests/test_gold_api.py:58` — `procedures 1개 → 400 "procedures 는 2~6개"` 기대 → PAIR_MIN 1 로 바뀌면 깨짐 · `tests/test_gold_pairs.py`
- `scripts/gold_e2e.py`(sections 호출 · `intent_used` · `sections_used` 검증 추가 자리) · `tests/test_public_api_contract.py`(section 응답 계약 시험 — 영향 확인 필요)
방향: 위 7곳을 표에 더하고 「grep sections · PAIR_MIN · cols(… "source") 0 누락」 을 WP-7 검증에 넣는다.

### F-8 · §4-3 F-C · F-D — 실물에 없는 칸 이름 2곳(기준 2)

근거: (a) F-D 「단위 시술 `silver.pih[]{fitzpatrick_note, source, condition, pih_rate, pih_risk, prevention}`」 — 실물 unit `silver.pih[]` 키 = attach · condition · fitzpatrick_note · pih_rate · pih_risk · source · target(32행 · `prevention` 0). `prevention` 은 step8 `safety.pih[]` 행(meta)에 있고 이미 `pih[k]` fact 본문. (b) F-C 「treats 엣지 근거 `claims[R8-…].reason`(1건)」 — treats 엣지에 `row.claims` 는 0건. 해당 B 1건(Q118)은 treats `attrs.row.evidence.role`(「색소 제거」) · `R8-0321#reason` 은 이미 procedure_relation evidence fact.
방향: (a) `prevention` 을 빼고 `target` 을 더함(또는 「잎 전부」 로만 쓰기) (b) 「treats `row.evidence.role` → section evidence」 로 고침.

## WARN

| id | 조항 | 내용 · 방향 |
|---|---|---|
| W-1 | §5-13 C2 · C3 · §5-5 | 단위 수준 엣지 종류는 실물 `requires_check_unit`(1,600) · `procedure_pair`(`pair:a:b` 4,687) — 스펙은 `requires_check` · `procedure_relation`(저장 230) 으로만 씀. 「펼친 종류 포함 · 단위 시술은 pair/UnitSets 로 닿는 것」 한 줄 |
| W-2 | §4-3 F-A ⑤ | 규칙 8 ↔ concern_avoid 연결 키 미명시. 실물: `step8_notes[45].text == avoid_edges[AV8-001].text`(source `combination_rules`) 1건만 연결 · 나머지 7은 scope:all. 「text 동일 + source 동일」 로 적기(추측 자리) |
| W-3 | §5-15 | 「5건 이상이면 slim 승격」 문턱은 결정표 · 브리프에 없는 작성자 기준 — §7 V 로 올리거나 근거 적기(추측 자리) |
| W-4 | §5-15 · §6-5 | C10 「비교 맥락 밖은 안 올림」 결정으로 ⑦ combo_component 11건 중 비 I-06 10건은 못 닫힘 — §6-5 「닫지 않는 행」 표에 명시(F-1 (b) 와 함께) |
| W-5 | WORK-005 Meta · WP-0 3 | 「18005 는 띄우지도 끄지도 않는다」 와 「지금 허브 18005 로 기준선」 — 읽기 호출(GET · POST 조회)은 허용임을 Meta 에 적기 |
| W-6 | §6-5 | 「실패 174문항의 호출 묶음 755」 — 755 는 239문항 전체 replay 유일 호출 수(meta.replay_unique_calls). 「전체 replay 755 중 실패 174문항분」 으로 정정 |
| W-7 | §5-7 · §4-3 F-D | attrs_text 키에 `asian_skin_note`(2) · 목적 레시피 `effect.expectedResults · repeatCycle`(7) 열거 누락 — 「잎 전부」 규칙이면 영향 없음 · 열거만 보완 |
| W-8 | §2-2(v2 영역) | `safety.family_text` 칸 「상담 · 준비 · 고지 · 조건 아닌 문장」 「critical_safety_facts」 「안전 원문」 은 일부 계열만(union 13 · 공통 9) — 「17계열 공통」 문구 정정 |

## 기준 2 실물 대조표(맞은 것)

| 스펙 | 실물(gold-export e9d30ace · tools.py · 실버) | 결과 |
|---|---|---|
| section 17(§4-3) | `facts.SECTIONS` 17 같음 · export section 17 종 | ○ |
| 노드 13 · 도구 9 · REST 경로 · MCP 이름 | `NODE_KINDS` 13 · router · mcp_server 9 | ○ |
| T5 400 문구 「id: family:M8 는 family — 받는 종류 …」 | `_need` f"{what}: {nid} 는 {kind} — 받는 종류 …" · `("unit_procedure","product","package")` | ○ |
| T4 1~6(지금 2~6) · T6 2~4 · pair 30 · compare 8 | `PAIR_MIN,PAIR_MAX = 2,6` · `COMPARE 2,4` · 30 · 8 | ○ |
| self_pair 4(E8-0059 · 0214 · 0225 · 0228) | step8 `self_pair` 4 같음 | ○ |
| SC 22 · spec 키 key_warning · risk · safe_zone · dose_range · target_muscle · `vessels[].danger` · `clinical_pearls` · `safe_injection_depth` · `units_affected` | step8 site_caution 22 · 키 전부 있음(spec 에 risk_level · primary_risk · safe_technique 등 더 있음 — 잎 전부 규칙으로 덮임) | ○ |
| 비교 조합 9 · members attrs_text 9키 · anchor.subtitle | 9 · 키 9 + asian_skin_note 2(W-7) | ○ |
| 조합 79 · effect{expectedResult, clinicalRationale, riskBenefit} · price · evidence_notes · caveats · rationale · sessions · maintenance · follow_up · avoid_text · annual_focus · subtitle | step7 combos 79 · 전부 존재(effect 31 · price 70 · caveats 24 …) | ○ |
| step8_notes 245 · ① 13 ② 152 ③ 44 ④ 28 ⑤ 8 · ② CC ⊂ edges.ccs | 재계산 245 = 13 + 152 + 44 + 28 + 8 · ② 152/152 | ○ |
| attrs 56 · 비노드 owner 21 + 28 + 4 + 2 | step8 attrs 56 · export 비노드 owner 55 (+ family:M3 1) | ○ |
| `family:None` owner 40 | export 40 | ○ |
| F-E fact id 11(`U5-091#ops#ops.needsAnesthesia` · `pih[1]` · `fractional-co2#phases[4].normal[3]` · `SC-cheek-M1` · `botox#phases[3].emergency[1]` · `K8-0303` · `family:M9#checks#family_text[…][1]` …) | 전부 export 에 있음 | ○ |
| 계열 카드 `definition` 이미 있음(§5-15) | `tools.py:582,588` | ○ |
| 오류 15 = `GET /procedures/family:M*/checks` | case3_errors 15 · 문항 15 일치 | ○ |
| 755 호출 · 174문항 · 320행 | meta 755 · 174 · 320 | ○ |

## 기준 3 결정표 대조

| 결정(_RESUME §2) | v3 조항 | 결과 |
|---|---|---|
| 허브 LLM 없음(10-26 · 10-30) | §5-13 「LLM 이 고르지 않아도 붙는다 · dict 조회」 · §5-0 | ○ |
| 결정론 | §5-13 S4 · §6-5 두 번 같음 · §3-5 | ○ |
| slim D-14(10-30 「기본 짧은 카드 + sections」) | §5-13 요약 + id · 원문 상한 · §5-14 fact 수 상한 · 크기 상한 ≤ ×2(V-2 · V-3 위임 10-31) | ○(동봉 기본 추가는 V-2 위임 범위) |
| G13 안전 동봉 | §5-0 · C2 전 등급 · §6-4 안전 동봉 시험 | ○ |
| 충돌 = resolved 하나(D-13b 10-30) | §3-0 · T5 펼침 「가장 엄격 하나 + by_unit(접지 않음)」 · claims 는 근거 | ○ |
| 실버 · 시맨틱 수정 없음 | F-A~F-E 빌드 규칙 · `family:None` 은 읽는 칸 · A 61 은 9단계 | ○ |
| 10-31 V-1~V-5 추천값 위임 | §7 표와 같음(V-1 숫자는 F-2) | ○ |

## 기준 5 WORK-005

| 항목 | 결과 |
|---|---|
| WP 의존 순서 | WP-0 측정 도구 → WP-1 facts(attached_to) → WP-2 매핑(facts_by_attach 사용) → WP-3 intent(INTENTS) → WP-4 동봉(INTENTS · 재료 dict) → WP-5 쌍 → WP-6 checks → WP-7 — 순서 맞음 |
| WP 마다 시험 · 검증 명령 | 전 WP 있음 · 「WP 마다 그 WP 시험만」 규칙 명시 |
| Done Criteria ↔ §6-5 | 재인용률 · 오류 15 · 크기 · 품질 · 결정론 · 시험 1:1 — 단 숫자(223 · 201) 는 F-2 · F-4 로 바뀜 |
| 코드 표면 | 누락 7곳(F-7) |
| WP-0 설계 | triage.py import 불가(F-6) · 18005 읽기 호출 문구(W-5) |
| WP-3 완료 조건 | 「case3 18건 묶음 포함 표」 — 7건 불가(F-1 (a)) |

## 부록 A — 빠진 칸 20종 → v3 조항 대응표(B 239)

열: 조항(건) · X0 = 허브 안 부름(분모 밖) · X1 = resolve · vocab 만 호출 · NONE = 조항 없음

| 빠진 칸 | 건 | 대응 조항(건) | X0 | X1 | NONE |
|---|---|---|---|---|---|
| 이웃 노드(1-hop) — 도구가 안 펼침 | 42 | §5-13 C2(19) · §5-13 C4 + §5-14 I-04 safety.side_effects(C4 제품에 섹션 적용 여부 모호)(4) · §5-13 C4 + §5-14 I-03 aftercare(C4 제품에 섹션 적용 여부 모호)(3) · §5-13 C6(2) · §5-13 C1(1) · §5-13 C5 + §5-14 I-04 disclosure(1) · §5-13 C5 + §5-14 I-06 recovery(1) · §5-13 C5 + §5-14 I-02 overview(1) | 0 | 3 | 7 |
| slim 카드 밖 섹션(section 안 요청) | 35 | §5-14 I-04 기본 묶음에 disclosure(4) · §5-14 I-02 기본 묶음에 overview(2) · §5-14 I-03 기본 묶음에 disclosure(2) · §5-14 I-03 기본 묶음에 aftercare(1) · §5-13 C2(1) · §5-14 I-06 기본 묶음에 method(1) · §5-14 I-02 기본 묶음에 ops(1) · §5-14 I-05 기본 묶음에 recovery(1) · §5-14 I-05 기본 묶음에 timeline(1) · §5-14 I-05 기본 묶음에 aftercare(1) · §5-13 C1(1) · §5-14 I-07 기본 묶음에 checks(1) | 0 | 5 | 13 |
| 노드 속성(combo) · 노드에 안 닿음 | 27 | §4-3 F-D + §5-13 C7 + §5-15(16) | 2 | 3 | 6 |
| 엣지 속성 — 양끝 도달 | 20 | §4-3 F-C + §5-13 C1(4) · §4-3 F-A ⑤(1) · §4-3 F-C + §5-13 C10(compare 만)(1) · §4-3 F-C basis→overview(1) | 0 | 1 | 12 |
| 섹션 요청했는데도 응답에 없음(section 매핑 밖) | 16 | §4-3 F-E · §5-0 공통 매핑(16) | 0 | 0 | 0 |
| 경로가 그 노드에 안 닿음 | 16 | §5-13 C11(1) · §5-13 C5 + §5-14 I-04 safety.side_effects(1) · §5-13 C5 + §5-14 I-04 disclosure(1) · §5-13 C6(1) | 12 | 0 | 0 |
| 쌍 관계 fact — 쌍 도구 불렀으나 다른 쌍 | 14 | §5-5 relations[]/claims 원문 · §5-7 relations[] · C9/C3(14) | 0 | 0 | 0 |
| step8 메모(step8_notes) fact — 어느 노드에도 안 붙음(도구로 못 꺼냄) | 14 | §4-3 F-A/F-B + §5-13 C14(12) | 0 | 1 | 1 |
| slim 카드 밖 섹션(section 안 요청) · Jev noul<0.5(안 고름) | 10 | §5-14 I-05 기본 묶음에 aftercare(2) · §5-14 I-04 기본 묶음에 disclosure(1) · §5-14 I-10 기본 묶음에 market(1) · §5-14 I-02 기본 묶음에 overview(1) · §5-14 I-06 기본 묶음에 recovery(1) · §5-14 I-04 기본 묶음에 emergency(1) · §5-14 I-04 기본 묶음에 safety.side_effects(1) | 0 | 0 | 2 |
| 노드 속성(unit_procedure · full 카드 전용) | 9 | §4-3 F-D + §5-13 C12 + §5-15(4) | 0 | 3 | 2 |
| 쌍 관계 fact — 쌍 맞음 · evidence 섹션 안 요청(claims id 만) | 8 | §5-5 relations[]/claims 원문 · §5-7 relations[] · C9/C3(8) | 0 | 0 | 0 |
| slim 카드 밖 섹션(section 안 요청) · Jev 상위4 밖 | 8 | §5-14 I-05 기본 묶음에 recovery(1) · §5-14 I-06 기본 묶음에 safety.pih(1) · §5-14 I-04 기본 묶음에 emergency(1) | 0 | 0 | 5 |
| 노드 속성(combo · full 카드 전용) | 8 | §4-3 F-D + §5-13 C7 + §5-15(4) | 0 | 0 | 4 |
| 쌍 관계 fact — pair_check/compare 안 부름 | 4 | §5-13 C3(금기류 관계만)(2) | 2 | 0 | 0 |
| 노드 속성(concern) · 노드에 안 닿음 | 3 | — | 1 | 1 | 1 |
| 노드 속성(unit_procedure) · 노드에 안 닿음 | 1 | §4-3 F-D + §5-13 C12 + §5-15(1) | 0 | 0 | 0 |
| 노드 속성(family · full 카드 전용) | 1 | §5-13 C5 definition(1) | 0 | 0 | 0 |
| 쌍 관계 fact — 쌍 맞음 · evidence 요청했는데도 안 실림 | 1 | §5-5 relations[]/claims 원문 · §5-7 relations[] · C9/C3(1) | 0 | 0 | 0 |
| 조합(CC · 레시피) fact — combos 안 부름 | 1 | — | 0 | 0 | 1 |
| 노드 속성(product) · 노드에 안 닿음 | 1 | — | 0 | 0 | 1 |
합: 239 = 대응 있음 150 + X0 17 + X1 17 + NONE 55. 큰 묶음별 대응 없음(X1 + NONE): ① 25 / ② 0 / ④ 0 / ⑤ 22 / ⑥ 9 / ⑦ 13 / ⑧ 3 = 72.

## 부록 B — 대응 없는 행 전부(72)

| 문항 | 케이스 | 의도(Jev) | 빠진 칸 | 호출 | owner | section | 사유 |
|---|---|---|---|---|---|---|---|
| Q015 | case2 | I-06 | slim 카드 밖 섹션(section 안 요청) | resolve | family:M9 | overview | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q020 | case3 | I-08 | slim 카드 밖 섹션(section 안 요청) | pair_check | product:auto-40-1774737181584 | safety.side_effects | NONE ① I-08 기본 묶음에 safety.side_effects 없음 |
| Q025 | case2 | I-11 | 이웃 노드(1-hop) — 도구가 안 펼침 | resolve,combos | check_condition:C-NMJ | checks | NONE ⑤ I-11 owner=check_condition sec=checks 닿는 동봉 없음 |
| Q028 | case2 | I-09 | 노드 속성(combo) · 노드에 안 닿음 | resolve | combo:RC-PC-P2-1 | — | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q039 | case3 | I-06 | 노드 속성(combo) · 노드에 안 닿음 | compare | combo:RC-PC-P7-1 | — | NONE ⑤/⑥ combo 속성 — I-06 에 C7 없음 |
| Q040 | case3 | I-09 | slim 카드 밖 섹션(section 안 요청) | procedure_card | unit_procedure:U5-010 | aftercare | NONE ① I-09 기본 묶음에 aftercare 없음 |
| Q042 | case3 | I-06 | slim 카드 밖 섹션(section 안 요청) | compare | family:M2 | disclosure | NONE ① I-06 기본 묶음에 disclosure 없음 |
| Q050 | case3 | I-04 | 노드 속성(combo) · 노드에 안 닿음 | procedure_card | combo:RC-CP-volume | — | NONE ⑤/⑥ combo 속성 — I-04 에 C7 없음 |
| Q054 | case2 | I-05 | slim 카드 밖 섹션(section 안 요청) | resolve,resolve,resolve,resolve,compare | family:M3 | overview | NONE ① I-05 기본 묶음에 overview 없음 |
| Q058 | case2 | I-04 | slim 카드 밖 섹션(section 안 요청) | resolve,procedure_card | family:M4 | overview | NONE ① I-04 기본 묶음에 overview 없음 |
| Q058 | case3 | I-04 | slim 카드 밖 섹션(section 안 요청) | procedure_card | family:M4 | overview | NONE ① I-04 기본 묶음에 overview 없음 |
| Q066 | case2 | I-09 | slim 카드 밖 섹션(section 안 요청) | resolve,resolve,resolve,resolve,resolve,check_conditions,check_conditions | family:M4 | overview | NONE ① I-09 기본 묶음에 overview 없음 |
| Q068 | case2 | I-04 | 이웃 노드(1-hop) — 도구가 안 펼침 | resolve,resolve,procedure_card | unit_procedure:U5-090 | market | NONE ⑤ I-04 owner=unit_procedure sec=market 닿는 동봉 없음 |
| Q070 | case2 | I-09 | 이웃 노드(1-hop) — 도구가 안 펼침 | resolve,resolve,check_conditions,procedure_card,procedure_card | unit_procedure:U5-034 | safety.side_effects | NONE ⑤ I-09 owner=unit_procedure sec=safety.side_effects 닿는 동봉 없음 |
| Q072 | case2 | I-06 | 노드 속성(combo) · 노드에 안 닿음 | resolve,compare | combo:RC-PC-P3-1 | — | NONE ⑤/⑥ combo 속성 — I-06 에 C7 없음 |
| Q074 | case2 | I-09 | slim 카드 밖 섹션(section 안 요청) | resolve,resolve,check_conditions,procedure_card | family:M9 | overview | NONE ① I-09 기본 묶음에 overview 없음 |
| Q082 | case2 | I-07 | 이웃 노드(1-hop) — 도구가 안 펼침 | resolve,resolve | package:P6-09 | evidence | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q082 | case3 | I-07 | 이웃 노드(1-hop) — 도구가 안 펼침 | pair_check | package:P6-09 | evidence | NONE ⑤ I-07 owner=package sec=evidence 닿는 동봉 없음 |
| Q084 | case3 | I-07 | 이웃 노드(1-hop) — 도구가 안 펼침 | pair_check | product:M9-2-2 | products | NONE ⑤ I-07 owner=product sec=products 닿는 동봉 없음 |
| Q098 | case2 | I-10 | slim 카드 밖 섹션(section 안 요청) | resolve,procedure_card | family:M11 | overview | NONE ① I-10 기본 묶음에 overview 없음 |
| Q098 | case3 | I-10 | slim 카드 밖 섹션(section 안 요청) | procedure_card | family:M11 | disclosure | NONE ① I-10 기본 묶음에 disclosure 없음 |
| Q102 | case2 | I-06 | 노드 속성(combo) · 노드에 안 닿음 | resolve,resolve,recommend,resolve | combo:RC-CP-pigment | — | NONE ⑤/⑥ combo 속성 — I-06 에 C7 없음 |
| Q102 | case3 | I-06 | 노드 속성(combo · full 카드 전용) | compare | combo:RC-CP-pigment | — | NONE ⑤/⑥ combo 속성 — I-06 에 C7 없음 |
| Q102 | case3 | I-06 | 노드 속성(combo · full 카드 전용) | compare | combo:RC-CP-pigment | — | NONE ⑤/⑥ combo 속성 — I-06 에 C7 없음 |
| Q104 | case3 | I-10 | slim 카드 밖 섹션(section 안 요청) | procedure_card | family:M8 | overview | NONE ① I-10 기본 묶음에 overview 없음 |
| Q105 | case2 | I-04 | 노드 속성(combo) · 노드에 안 닿음 | resolve,resolve,resolve,resolve | combo:RC-CP-pigment | — | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q106 | case2 | I-06 | 이웃 노드(1-hop) — 도구가 안 펼침 | resolve,resolve,procedure_card | unit_procedure:U5-028 | timeline | NONE ⑤ I-06 owner=unit_procedure sec=timeline 닿는 동봉 없음 |
| Q106 | case3 | I-06 | 이웃 노드(1-hop) — 도구가 안 펼침 | compare | unit_procedure:U5-028 | timeline | NONE ⑤ I-06 owner=unit_procedure sec=timeline 닿는 동봉 없음 |
| Q113 | case2 | I-06 | 노드 속성(unit_procedure · ful | resolve,resolve,resolve,resolve | unit_procedure:U5-023 | — | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q113 | case2 | I-06 | 노드 속성(unit_procedure · ful | resolve,resolve,resolve,resolve | unit_procedure:U5-023 | — | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q115 | case2 | I-04 | step8 메모(step8_notes) fact | resolve,resolve | scope:all | evidence | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q117 | case2 | I-11 | 엣지 속성 — 양끝 도달 | resolve,recommend | combo_component:002206 | — | NONE ⑦ 비교 조합 members — I-11/recommend 에 C10 없음 |
| Q118 | case2 | I-06 | 엣지 속성 — 양끝 도달 | resolve,resolve,vocab,recommend | treats:0206 | — | NONE ⑦ treats reason — I-06 |
| Q119 | case2 | I-07 | 엣지 속성 — 양끝 도달 | resolve,resolve,pair_check | combo_component:002208 | — | NONE ⑦ 비교 조합 members — I-07/pair_check 에 C10 없음 |
| Q121 | case2 | I-01 | 엣지 속성 — 양끝 도달 | resolve,resolve,vocab,recommend,procedure_card,procedure_card,neighbors | combo_component:002210 | — | NONE ⑦ 비교 조합 members — I-01/recommend 에 C10 없음 |
| Q122 | case2 | I-06 | 노드 속성(concern) · 노드에 안 닿음 | resolve,resolve | concern:P6-3 | — | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q123 | case3 | I-07 | 노드 속성(concern) · 노드에 안 닿음 | pair_check | concern:P8-2 | — | NONE ⑤ concern 이름 · 속성 — 조항 없음 |
| Q129 | case2 | I-03 | slim 카드 밖 섹션(section 안 요청) | resolve | family:M8 | aftercare | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q129 | case2 | I-03 | slim 카드 밖 섹션(section 안 요청) | resolve | family:M8 | aftercare | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q135 | case2 | I-05 | slim 카드 밖 섹션(section 안 요청) | resolve | family:M8 | recovery | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q136 | case2 | I-03 | 이웃 노드(1-hop) — 도구가 안 펼침 | resolve | unit_procedure:U5-028 | timeline | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q137 | case2 | I-10 | slim 카드 밖 섹션(section 안 요청) | resolve,recommend,procedure_card,procedure_card | family:M8 | disclosure | NONE ① I-10 기본 묶음에 disclosure 없음 |
| Q138 | case2 | I-09 | 노드 속성(combo) · 노드에 안 닿음 | resolve,recommend,recommend,recommend | combo:RC-CP-skin_texture | — | NONE ⑤/⑥ combo 속성 — I-09 에 C7 없음 |
| Q140 | case2 | I-05 | slim 카드 밖 섹션(section 안 요청) | resolve,check_conditions,procedure_card,procedure_card | family:M8 | disclosure | NONE ① I-05 기본 묶음에 disclosure 없음 |
| Q146 | case2 | I-04 | slim 카드 밖 섹션(section 안 요청) | resolve,check_conditions,procedure_card,procedure_card | unit_procedure:U5-028 | timeline | NONE ① I-04 기본 묶음에 timeline 없음 |
| Q149 | case3 | I-09 | 엣지 속성 — 양끝 도달 | procedure_card | combo_component:002187 | — | NONE ⑦ 비교 조합 members — I-09/procedure_card 에 C10 없음 |
| Q149 | case3 | I-09 | 엣지 속성 — 양끝 도달 | procedure_card | combo_component:002177 | — | NONE ⑦ 비교 조합 members — I-09/procedure_card 에 C10 없음 |
| Q150 | case2 | I-09 | 노드 속성(unit_procedure · ful | resolve,resolve,check_conditions,procedure_card | unit_procedure:U5-023 | — | NONE ⑥ pih — I-09 에 C12 없음 |
| Q156 | case2 | I-07 | 엣지 속성 — 양끝 도달 | resolve,recommend,check_conditions | combo_component:002177 | — | NONE ⑦ 비교 조합 members — I-07/recommend 에 C10 없음 |
| Q156 | case3 | I-07 | 엣지 속성 — 양끝 도달 | pair_check | combo_component:002177 | — | NONE ⑦ 비교 조합 members — I-07/pair_check 에 C10 없음 |
| Q156 | case3 | I-07 | 엣지 속성 — 양끝 도달 | pair_check | combo_component:002167 | — | NONE ⑦ 비교 조합 members — I-07/pair_check 에 C10 없음 |
| Q162 | case2 | I-06 | 엣지 속성 — 양끝 도달 | resolve,resolve | product_family:000262 | — | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q162 | case2 | I-06 | slim 카드 밖 섹션(section 안 요청) | resolve,resolve | family:M8 | recovery | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q163 | case2 | I-04 | slim 카드 밖 섹션(section 안 요청) | resolve,procedure_card | family:M15 | overview | NONE ① I-04 기본 묶음에 overview 없음 |
| Q167 | case2 | I-03 | slim 카드 밖 섹션(section 안 요청) | resolve,procedure_card | family:M15 | overview | NONE ① I-03 기본 묶음에 overview 없음 |
| Q169 | case2 | I-09 | 엣지 속성 — 양끝 도달 | resolve,resolve,check_conditions,procedure_card | product_family:000253 | — | NONE ⑦ product_family basis — I-09 기본 묶음에 overview 없음 |
| Q170 | case2 | I-04 | slim 카드 밖 섹션(section 안 요청) | resolve,procedure_card | family:M15 | overview | NONE ① I-04 기본 묶음에 overview 없음 |
| Q170 | case3 | I-04 | slim 카드 밖 섹션(section 안 요청) | procedure_card | family:M15 | overview | NONE ① I-04 기본 묶음에 overview 없음 |
| Q191 | case2 | I-06 | 노드 속성(combo · full 카드 전용) | resolve,resolve,compare | combo:RC-CP-lifting | — | NONE ⑤/⑥ combo 속성 — I-06 에 C7 없음 |
| Q191 | case3 | I-06 | 노드 속성(combo · full 카드 전용) | compare | combo:RC-CP-lifting | — | NONE ⑤/⑥ combo 속성 — I-06 에 C7 없음 |
| Q192 | case2 | I-02 | 노드 속성(combo) · 노드에 안 닿음 | resolve,resolve | combo:RC-CP-body_contouring | — | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q192 | case3 | I-02 | 엣지 속성 — 양끝 도달 | procedure_card | combo_component:002204 | — | NONE ⑦ 비교 조합 members — I-02/procedure_card 에 C10 없음 |
| Q198 | case2 | I-06 | step8 메모(step8_notes) fact | resolve,resolve,recommend,compare | scope:all | evidence | NONE ⑧ I-06 에 C14 없음 · 기본 묶음 evidence 없음 |
| Q198 | case3 | I-06 | 조합(CC · 레시피) fact — combos | compare | CC P14:미라드라이 속성(원소 1개 — 쌍 아님) | evidence | NONE ⑧ I-06 에 C14 없음 · 기본 묶음 evidence 없음 |
| Q201 | case3 | I-07 | 노드 속성(unit_procedure · ful | pair_check | unit_procedure:U5-028 | — | NONE ⑥ pih — I-07 에 C12 없음 |
| Q202 | case2 | I-09 | slim 카드 밖 섹션(section 안 요청) | resolve,check_conditions,neighbors,resolve,check_conditions,check_conditions | unit_procedure:U5-026 | aftercare | NONE ① I-09 기본 묶음에 aftercare 없음 |
| Q211 | case2 | I-08 | 이웃 노드(1-hop) — 도구가 안 펼침 | resolve,resolve,resolve | product:auto-29-1774737181584 | aftercare | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q212 | case3 | I-06 | 노드 속성(combo) · 노드에 안 닿음 | compare | combo:RC-PC-P3-1 | — | NONE ⑤/⑥ combo 속성 — I-06 에 C7 없음 |
| Q219 | case2 | I-05 | slim 카드 밖 섹션(section 안 요청) | resolve,procedure_card,procedure_card | unit_procedure:U5-090 | ops | NONE ① I-05 기본 묶음에 ops 없음 |
| Q228 | case2 | I-04 | 노드 속성(product) · 노드에 안 닿음 | resolve,recommend | product:auto-M15-1775401780659 | — | NONE ⑤ product 1_identity.basis — 조항 없음(C4 는 id · 이름 · 허가만) |
| Q231 | case2 | I-05 | 노드 속성(unit_procedure · ful | resolve,resolve | unit_procedure:U5-010 | — | X1 resolve/vocab 만 호출 — 카드 도구 없음(동봉 · 섹션 적용 자리 없음) |
| Q234 | case3 | I-05 | 엣지 속성 — 양끝 도달 | procedure_card | combo_component:002167 | — | NONE ⑦ 비교 조합 members — I-05/procedure_card 에 C10 없음 |
## 부록 C — §6-5 현 중앙값 표 재계산(`runs/runs.jsonl` 239)

| 도구 | case2 전부 n / 중앙 | case2 오류 제외 n / 중앙(= 스펙 표) | case3 n / 중앙 | case2 sections 없는 호출 n / 중앙 |
|---|---|---|---|---|
| recommend | 65 / 6,713 | 58 / 7,262 | 18 / 8,171 | 47 / 6,567 |
| procedure_card | 169 / 16,537 | 154 / 17,180 | 125 / 26,325 | 16 / 1,447 |
| pair_check | 24 / 6,968 | 22 / 7,200 | 29 / 6,882 | 23 / 7,151 |
| check_conditions | 86 / 115 | 28 / 24,206 | 5 / 21,977 | 10 / 115 |
| compare | 14 / 7,997 | 14 / 7,997 | 21 / 6,146 | 6 / 7,268 |
| combos | 4 / 9,537 | 4 / 9,537 | 3 / 7,288 | 4 / 9,537 |
| neighbors | 9 / 6,544 | 9 / 6,544 | — | 7 / 5,633 |
| resolve | 364 / 1,059 | 364 / 1,059 | — | 364 / 1,059 |
| vocab | 14 / 5,501 | 9 / 6,314 | — | 14 / 5,501 |
| 합 | 749 | **662** | **201**(스펙 224) | — |

case2 오류(is_error) 87 = check_conditions 58 · procedure_card 15 · recommend 7 · vocab 5 · pair_check 2. case3 허브 경로 없는 run 38(되묻기 · 필수 슬롯 없음 · I-12).

## 부록 D — 검수에 쓴 대조 방법

- B 행 대응: `fail-triage.json` rows(cls B) → (sub · jev_intent · tools_called · gold_owner 종류 · gold_section · gold_hits 종류) → §5-13 의도 × 동봉 표 · §5-14 표 · F-A~F-E · §5-5 · §5-7 로 결정론 매핑(스크립트는 보고서에 안 넣음 · 규칙은 부록 A 열과 같음). jev_intent 가 없거나 표 밖이면 도구 기본 의도(§5-0).
- 실물: `gold-export.json`(e9d30ace) 노드 · 엣지 · fact 종류 · 키 union · step5/7/8 json 키 union · `tools.py` · `router/gold.py` · `schema/gold.py` · `mcp_server.py` · `service.py` · `application.py` · `facts.py` · `pairs.py` · `config.py` · `tests/`.
- 셈: `runs/runs.jsonl` case2 `trace.tool_calls[].output_bytes` · case3 `trace.hub.result_bytes` 중앙값(statistics.median).
