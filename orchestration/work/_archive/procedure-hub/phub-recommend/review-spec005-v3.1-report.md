# 재검수 보고서 — SPEC-005 v3.1(0.3.1) · WORK-005

작성 2026-10-31 · 검수자 reviewer 워커(읽기 전용 · 스펙 · 코드 수정 없음) · 전 판 `review-spec005-v3-report.md`(FAIL 8 · WARN 8)
대상 `SPEC-005.md`(0.3.1 · 14:18) · `WORK-005.md`(0.3.1 반영) · 대조 정본은 전 판과 같음(`fail-triage.json` B 239 · 허브 코드 64fe929 · `gold-export.json` e9d30ace · `runs/runs.jsonl` · 실버 step5/7/8 · `_RESUME.md` §2)

## 판정 — **FAIL(경미 1 · 고치면 PASS)** · FAIL 1 · WARN 3

한 줄: 전 판 FAIL 8 · WARN 8 은 전부 반영됐다. B 239 행을 v3.1 조항으로 다시 전수 매핑하면 **분모 205 · 조항이 닿는 행 186 · 닫지 않는 행 19** 가 스펙 §6-5 표와 **행 단위로 일치**하고, recheck 판정 규칙(새 export 로 gold_match 재실행)과 코드 표면 7곳도 들어갔다. 남은 결함은 WORK-005 본문 두 줄이 v3.1 스펙과 반대로 남아 있는 것(F-1)뿐이다.

| 기준 | 판정 | 요지 |
|---|---|---|
| 1 전수 대조 | PASS | 239 = 닿음 186(+ Q118 c2 1 은 스펙이 보수적으로 미닫힘에 둠) + 닫지 않는 행 19 + 허브 안 부름 17 + resolve · vocab 만 17. 대응 없는데 명시도 안 된 행 **0**(부록 A · B) |
| 2 실물 대조 | PASS | 전 판 F-8 두 칸 고침(pih 키 7 · treats `row.evidence.role`) · W-1 종류 이름(`requires_check_unit` · `procedure_pair` · `g.pair`) · W-7 열거(`asian_skin_note` · `effect{expectedResults, repeatCycle}`) · W-8 family_text 「합집합 13 · 공통 9」 전부 실물과 같음 |
| 3 결정표 충돌 | PASS | 변화 없음 · V-6 · V-7 추가는 10-31 위임 범위 |
| 4 끝 조건(§6-5) | PASS | 분모 205(= 239 − 17 − 17 · 실물 재계산 일치) · 판정 = 새 export 로 gold_match 재실행 뒤 fact id 또는 인용(F-3 해소) · 셈 규칙(case2 오류 제외 662 · case3 201 · sections 없음 열) 재계산 일치 · 목표 = 닿는 행 186 의 ≥ 90%(= 168+ · V-7 사용자 확인) · 닫지 않는 행 19 표 |
| 5 WORK-005 | **FAIL(경미)** | 코드 표면 7곳 추가 · WP-0 판정 규칙 「같은 식으로 적음 · import 안 함」 · 18/18 · 분모 205 · Done Criteria ↔ §6-5 1:1 맞음. 단 「손대지 않는 것」 줄과 WP-1 F-C 한 줄이 v3.1 과 반대(F-1) |
| 6 추측 자리 | PASS | F-A ⑤ 연결 키 명시 · §5-15 문턱 → V-6 · §6-5 필터 명시. 새 추측 자리 없음 |

## FAIL

### F-1 · WORK-005 「손대지 않는 것」(79행) · WP-1 F-C(100행) — v3.1 스펙과 반대 문구 2곳(기준 5)

근거:
- 79행 「`triage.py` · `replay.py`(읽기만 · **recheck 는 import 해 씀**)」 — SPEC §6-4 · §6-5 · WORK WP-0 2 는 「triage.py 는 모듈 수준에서 파일을 읽고 쓰므로 **import · 수정하지 않음**(F-6)」. 구현 워커가 이 줄을 따르면 import 시 `triage-rows.json` 이 덮여 Done Criteria 「`$E` 기존 파일 변경 0」 이 깨진다.
- 100행 「treats **`claims[].reason`** → fact」 — SPEC §4-3 F-C 는 「treats `attrs.row.evidence.role`(treats 에 `row.claims` 는 0건)」 로 고쳐졌다. 「둘이 다르면 SPEC 을 따른다」 규칙으로 해소되지만 발주서 안에서 서로 반대라 그대로 두면 안 된다.
방향: 79행을 「`triage.py` · `replay.py`(읽기만 · import 하지 않음 · 판정 식은 recheck.py 에 같은 식으로)」 로, 100행을 「treats `row.evidence.role` → fact(section evidence · attached to_units)」 로 고친다. 두 줄 수정이면 PASS.

## WARN

| id | 조항 | 내용 · 방향 |
|---|---|---|
| W-1 | WORK-005 WP-0 시험 「320/320 재분류 동일」 | 재분류에는 원 실행의 허브 응답(`replay.json`)이 필요한데 `fail-triage-scripts/` 에 없다(replay.py · report.py · triage.py 만). WP-0 3 의 18005(e9d30ace) 읽기 재호출로 만들 수 있으나 **WP-7 발행 · 재시작 전에 끝내야** 한다 — 순서 의존을 WP-0 에 한 줄 |
| W-2 | SPEC §0 절 표(70행) | 「V-1~V-6」 → 실제 §7 은 V-1~V-7 |
| W-3 | SPEC §6-5 닫지 않는 행 Q118 c2 | 사유 「F-C 로 fact 는 생기나 I-06 compare 동봉 밖」 — §5-14 I-06 에 「조합 `evidence`(C14)」 가 들어 있어 evidence 가 단위 시술 evidence 까지 뜻하는지 모호(검수 매핑에선 닿는 것으로 나옴). 「I-06 evidence 는 조합(C14) 범위만 · 단위 시술 evidence 아님」 한 줄이면 19 가 그대로 선다 |

## 전 판 FAIL · WARN 반영 확인

| 전 판 | 반영 | 확인 |
|---|---|---|
| F-1 72행 미대응 | §5-13 I-06 C7 · C11 · C14 / I-07 · I-08 · I-09 C12 / I-11 C2 · §5-14 I-03 overview · I-04 overview · timeline · I-05 overview · disclosure · ops · I-06 checks · disclosure · I-08 side_effects · I-09 aftercare · overview · I-10 overview · disclosure · §6-5 「닫지 않는 행」 19 · 분모에서 resolve 만 17 제외 | 재매핑 — 미명시 대응 없음 0 · case3 Jev 18건 18/18 묶음 안(Q020 I-08 side_effects · Q040 I-09 aftercare · Q042 I-06 disclosure · Q058 · Q170 I-04 overview · Q098 I-10 disclosure · Q104 I-10 overview 확인) |
| F-2 분모 223 | 205(= 239 − 17 − 17) · 문항 14 · Q205 c2 명시 | 실물 재계산 17 · 17 · 205 일치 · 17행 목록 일치 |
| F-3 옛 gold_hits | 새 export 로 gold_match 재실행 · 두 해시 리포트 머리 · WP-0 기준선만 옛 export | §6-5 · WP-0 2 |
| F-4 67.6% | 목표 = 닿는 행 186 기준 ≥ 90% · 205 · 239 기준 보고 · V-7 | 186 = 205 − 19 실물 일치 |
| F-5 표 셈 규칙 | is_error 제외 662 · hub.tool 있는 run 201 · 「sections 없음」 열 · combos 19,074 | 전 판 부록 C 와 전 열 일치 |
| F-6 triage import | SPEC §6-4 · WP-0 「같은 식으로 적음 · 320/320 동일성 시험 · import 안 함」 | ○(79행 잔존 → F-1) |
| F-7 코드 표면 7 | service.py · application.py · gold_export.py · test_gold_api.py · test_gold_pairs.py · gold_e2e.py · test_public_api_contract.py 추가 · WP-7 4 grep 전수 | ○ |
| F-8 칸 이름 2 | pih 키 7(prevention 제거 · target 추가) · treats `row.evidence.role` | 실물 일치(WP-1 100행 잔존 → F-1) |
| W-1 ~ W-8 | C2 · C3 종류 이름 · F-A ⑤ 키(text == · source ==) · V-6 · 닫지 않는 행 표 · Meta 읽기 호출 허용 · 755 문구 · 열거 보완 · family_text 문구 | ○ 전부 |

## 부록 A — 빠진 칸 20종 → v3.1 조항(B 239)

열: 조항(건) · X0 = 허브 안 부름 · X1 = resolve · vocab 만 · NONE = 조항 없음(= §6-5 닫지 않는 행 표에 전부 명시)

| 빠진 칸 | 건 | 대응 조항(건) | X0 | X1 | NONE |
|---|---|---|---|---|---|
| 이웃 노드(1-hop) — 도구가 안 펼침 | 42 | C2(20) · C4+§5-14 I-04 safety.side_effects(4) · C4+§5-14 I-03 aftercare(3) · C11(2) · C6(2) · C1(1) · C5+§5-14 I-04 disclosure(1) · C5+§5-14 I-06 recovery(1) · C5+§5-14 I-02 overview(1) | 0 | 3 | 4 |
| slim 카드 밖 섹션(section 안 요청) | 35 | §5-14 I-04 disclosure(4) · §5-14 I-04 overview(3) · §5-14 I-02 overview(2) · §5-14 I-09 overview(2) · §5-14 I-03 disclosure(2) · §5-14 I-03 aftercare(1) · §5-14 I-06 checks(1) · §5-14 I-05 overview(1) · §5-14 I-06 method(1) · §5-14 I-02 ops(1) · §5-14 I-05 recovery(1) · §5-14 I-10 overview(1) · §5-14 I-10 disclosure(1) · §5-14 I-05 disclosure(1) · §5-14 I-04 timeline(1) · §5-14 I-05 timeline(1) · §5-14 I-03 overview(1) · §5-14 I-05 aftercare(1) · C1(1) · §5-14 I-09 aftercare(1) · §5-14 I-05 ops(1) · §5-14 I-07 checks(1) | 0 | 5 | 0 |
| 노드 속성(combo) · 노드에 안 닿음 | 27 | F-D+C7(20) | 2 | 3 | 2 |
| 엣지 속성 — 양끝 도달 | 20 | F-C+C1(4) · F-C basis→overview(2) · F-A ⑤(1) · F-C+C10(1) · F-C role→evidence(1) | 0 | 1 | 10 |
| 섹션 요청했는데도 응답에 없음(section 매핑 밖) | 16 | F-E(16) | 0 | 0 | 0 |
| 경로가 그 노드에 안 닿음 | 16 | C11(1) · C5+§5-14 I-04 safety.side_effects(1) · C5+§5-14 I-04 disclosure(1) · C6(1) | 12 | 0 | 0 |
| 쌍 관계 fact — 쌍 도구 불렀으나 다른 쌍 | 14 | §5-5/§5-7(14) | 0 | 0 | 0 |
| step8 메모(step8_notes) fact — 어느 노드에도 안 붙음(도구로 못 꺼냄) | 14 | F-A/F-B+C14(13) | 0 | 1 | 0 |
| slim 카드 밖 섹션(section 안 요청) · Jev noul<0.5(안 고름) | 10 | §5-14 I-05 aftercare(2) · §5-14 I-09 aftercare(1) · §5-14 I-06 disclosure(1) · §5-14 I-04 disclosure(1) · §5-14 I-10 market(1) · §5-14 I-02 overview(1) · §5-14 I-06 recovery(1) · §5-14 I-04 emergency(1) · §5-14 I-04 safety.side_effects(1) | 0 | 0 | 0 |
| 노드 속성(unit_procedure · full 카드 전용) | 9 | F-D+C12(6) | 0 | 3 | 0 |
| 쌍 관계 fact — 쌍 맞음 · evidence 섹션 안 요청(claims id 만) | 8 | §5-5/§5-7(8) | 0 | 0 | 0 |
| slim 카드 밖 섹션(section 안 요청) · Jev 상위4 밖 | 8 | §5-14 I-04 overview(2) · §5-14 I-08 safety.side_effects(1) · §5-14 I-05 recovery(1) · §5-14 I-10 disclosure(1) · §5-14 I-10 overview(1) · §5-14 I-06 safety.pih(1) · §5-14 I-04 emergency(1) | 0 | 0 | 0 |
| 노드 속성(combo · full 카드 전용) | 8 | F-D+C7(8) | 0 | 0 | 0 |
| 쌍 관계 fact — pair_check/compare 안 부름 | 4 | C3(2) | 2 | 0 | 0 |
| 노드 속성(concern) · 노드에 안 닿음 | 3 | — | 1 | 1 | 1 |
| 노드 속성(unit_procedure) · 노드에 안 닿음 | 1 | F-D+C12(1) | 0 | 0 | 0 |
| 노드 속성(family · full 카드 전용) | 1 | C5(1) | 0 | 0 | 0 |
| 쌍 관계 fact — 쌍 맞음 · evidence 요청했는데도 안 실림 | 1 | §5-5/§5-7(1) | 0 | 0 | 0 |
| 조합(CC · 레시피) fact — combos 안 부름 | 1 | F-A/F-B+C14(1) | 0 | 0 | 0 |
| 노드 속성(product) · 노드에 안 닿음 | 1 | — | 0 | 0 | 1 |
합: 239 = 닿음 187(검수 매핑 · 스펙은 Q118 c2 를 미닫힘에 둬 186) + NONE 18(+ Q118 c2 = 19) + X0 17 + X1 17. 큰 묶음별 NONE: ⑤ 7(Q050 · Q068 · Q070 · Q082 · Q084 · Q123 · Q138 · Q228 중 ⑤ 분류) · ⑦ 10 · 합 18.

## 부록 B — 닫지 않는 행 19 행 단위 대조(스펙 §6-5 표 ↔ 검수 매핑)

| 문항 · 케이스 | 스펙 사유 | 검수 매핑 | 일치 |
|---|---|---|---|
| Q117 c2 · Q119 c2 · Q121 c2 · Q149 c3 ×2 · Q156 c2 · Q156 c3 ×2 · Q192 c3 · Q234 c3 | C10 compare 에서만 | combo_component 엣지 속성 · 의도 I-11/I-07/I-01/I-09/I-07/I-02/I-05 에 C10 없음 | ○ 10/10 |
| Q123 c3 | concern 이름 | 조항 없음 | ○ |
| Q228 c2 | product `1_identity.basis` | 조항 없음(C4 는 id · 이름 · 허가) | ○ |
| Q118 c2 | treats `evidence.role` · I-06 동봉 밖 | §5-14 I-06 「조합 evidence」 로 닿는 것으로 나옴 — 스펙이 보수적 · W-3 | △(스펙 쪽이 안전) |
| Q050 c3 · Q138 c2 | I-04 · I-09 에 C7 없음 | 같음 | ○ |
| Q068 c2 · Q070 c2 · Q082 c3 · Q084 c3 | 1-hop 기타(unit market · 다른 unit side_effects · package evidence · product products) | 같음 | ○ |

분모 밖 34 = 허브 안 부름 17(case3 16 · case2 Q205) · resolve · vocab 만 17(스펙 목록과 같음) — 둘 다 실물 재계산 일치.

## 부록 C — 검수 방법

전 판 부록 D 와 같음. v3.1 표(§5-13 의도 × 동봉 · §5-14 의도 → section · §6-5 닫지 않는 행)를 규칙으로 바꿔 B 239 행을 다시 매핑하고, 스펙의 19 · 17 · 17 · 205 · 186 과 행 단위로 비교했다.
