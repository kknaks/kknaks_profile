# 실버 8단계 검수 — 관계 · 확인 조건 · 안전 · 근거

**FAIL** · FAIL 2 · WARN 2 · INFO 3 · **open = 0**(산출 `step8-relations.json` open · stale 둘 다 0)

- 기준: `_RESUME.md` §2 2026-10-29 「8단계 조사 반영」 · 「게이트 → 규칙」 · `phub-recommend-step8-apply-brief.md` · `step8-research.md`
- 대상: `step8-decisions.json` · `step8-apply.py` · `step8-relations.json` · `.md` · `step8-origin-questions.md` · `step8-fixture-test.py`
- 지금 데이터에 실제로 있는 것만 봤다(가상 문장 · 미래 원천은 보지 않음). 전수 점검은 모두 스크립트로 395 주장 · 373 조건 · 5 피함 · 19 충돌 전부를 돌렸다

## 결과 표

| # | 볼 것 | 판정 | 근거 |
|---|---|---|---|
| ① | 간격 — 원문 간격 낱말 → 숫자 칸 · 표시 | **FAIL 1**(F2) | 넓은 낱말 목록(숫자+단위 · 같은 날 · 당일 · 동시 · 직후 · 즉시 · 간격 · 전에 · 택 1 · 사이사이 · 순차 · 반복 · 세션 · 먼저 · 이후 · 다음 · 후에 · 뒤에)으로 전수 grep → 걸린 주장 247 중 칸 · 표시가 빈 것은 5뿐이고, 모두 CC 조합 이유 문장의 「동시 개선」이라 간격 낱말이 아님(I3). 숫자 → days 대조 불일치 0(「또는」 · 하위 조건 6건만 겉 칸이 감싼 범위). 같은 날 가능 ↔ 금지 뒤집힘 0. L-SDOK · L-IMM · L-BEFORE 갈래가 걸린 원문을 하나씩 확인했고 맞음. **다만 하위 조건이 갈리는 2건은 겉 칸이 원문과 어긋남 → F2** |
| ② | 끝점 — 7단계 지금 산출 · 5단계 키 | PASS | 조합 조건 74건의 `concern_ids`가 지금 `step7-concerns.json` combos anchor와 74/74 같음. 고민 id는 전부 7단계 노드 · 목적에 있음(J10-피부결 · P2-2/P2-3 중증도 하위 포함 — 경미 → P2-3 · 중등도/중증 → P2-2). 8단계 원천에 잇몸미소 · 코성형 · 다크서클 낱말은 없음(원천 grep 0 — 끝점 해당 없음). 단위 시술 참조 138개는 전부 5단계 키에 있고, 계열 ↔ 단위 시술 계열 어긋남 0. 하위 계열 별칭 일부는 5단계 키에 없음 → I1 |
| ③ | 게이트 잔재(U8-1) | PASS | 주장 395건 모두 `gate_status` 「자동(규칙)」. `unconfirmed` 0. `manual_map`은 decisions의 「두지 않음」 문장에 딱 1번 나옴. 결정 파일에 행 번호 · R8 id로 박은 행별 지정 0 — resolver alias 65는 낱말 → 키 사전이고, 문장 쌍은 `sentence.patterns` 정규식으로 처리 |
| ④ | 피함 엣지(U8-2) | **FAIL 1**(F1) | 고민 노드: 5건 모두 P5-1 기미(7단계 노드 · node true). 원문: 원천 `treatment-optimization`의 combination_rules[4] · contraindicated_combos 4.1.0 · 4.1.1 · 4.2.0 · 4.2.1과 글자 그대로 맞음. **끝점 범위는 문제 → F1** |
| ⑤ | 충돌 — 자동 선택 0 · 보존 | PASS | 고른 값을 담는 칸(chosen · winner · preferred 등) 0. 충돌 19개에 걸린 주장은 전부 review_status=conflict이고 엣지에 주장이 모두 남아 있음. 엣지에 안 들어간 주장 4건은 시술 아닌 끝점(G7). 조건 등급 76 · XW-C-ISO는 원천별 값을 보존. 조사 대비 간격 수치 충돌이 바뀐 것은 W1 |
| ⑥ | 조건 · 합병증 · site_caution · 근거 셈 ↔ 원천 | PASS(+W1 · W2) | pre-procedure 135(12+123) · consent 105 · taxonomy 108(53+55) + 품목 11 = 원천과 같음. 합병증 65 = complications 65(10계열, 원천 없는 계열 17). site_caution 22 = zone 11 × M1/M2. 경과표 10 = timelines 10. 문헌 25 = PMID 고유 25. 웹 29 = 합병증 출처 문자열 고유 29. step8_notes 245 = 7단계 메모 원천 합계 245. coverage 200행 n_map = n_now 전부. 조사 대비 셈 차이의 이유 기록은 W1, 웹 노드 내용은 W2 |
| ⑦ | 원천 질문 16 — 규칙으로 닫히는데 남긴 것 | PASS | Q8-1~7 · 14~16 = 원천끼리 충돌(D-13b, 자동 선택 금지라 의료진에게). Q8-8 TCA Cross(5단계 U5-034에 「TCA 필링」뿐 · CROSS 키 없음) · Q8-10 혈관레이저(엑셀V U5-099 ↔ 브이빔 U5-141 둘 다 후보) · Q8-12 「침습 시술」(묶음 낱말 사전에 없음) · Q8-13 듀얼파장 = 이름이 하나로 안 풀림. Q8-9 · Q8-11 = 원천 수정 요청. 규칙으로 닫을 수 있는데 남긴 질문 없음. Q8-15(보톡스 ↔ HIFU)는 synergy 「보톡스 2주 후 리프팅」 ↔ 13건 「HIFU 먼저」라 실제 충돌이 맞음 |
| ⑧ | open · 결정론 · 고정 시험 · 스킬 · 수정 금지 | PASS(+I2) | open 0 · stale 0. scratch 사본에서 apply 2회 → relations.json · .md · origin-questions.md가 서로 cmp 같고 커밋본과도 같음. 고정 시험 37/37 PASS. 스킬 점검 7종 errors 0 · open 0(family · site · technique · unit · package · concern · relation), relation `--selftest` 9/9 잡힘. 7단계 apply를 scratch에서 다시 돌린 결과가 `step7-concerns.json`과 cmp 같음 → 7단계 산출 손 수정 없음. 1~6단계 산출 · DEC · SPEC-004 · source-map 수정 시각은 전부 8단계 조사(20:35) 이전이고, 원천 폴더는 10-26 그대로 |

## FAIL

### F1 — 피함 엣지 3건이 M8 계열 전체로 열려 있어 7단계 「기미 → 토닝」 추천과 부딪치는데, 충돌 표시도 질문도 없다

- 대상: `AV8-001`(combination_rules[4] 「기미 환자에 **고출력** 레이저 … **저출력 토닝만 권장**」) · `AV8-002`(4.1.0 「기미에 **고에너지** 레이저 금지」) · `AV8-004`(4.2.0 「**고출력** 레이저 금지」)
- 데이터 상태: `to.level` = 「계열」 · `families` = [M8] · `units` = [](G2 · C4에 따라 조회 때 M8 단위 시술 전부가 상속됨). 「고출력 · 고에너지」는 `qualifier` 글자로만 남아 있다. resolver `strip_prefix`가 이 낱말을 떼어 낸 결과다
- 어긋남:
  - U8-2 결정과 `step8-decisions.json` `avoid_edge_type.to`는 「단위 시술(끝점 해석)」인데, 실제 끝점은 계열 전체다
  - 지금 7단계 엣지에는 P5-1 기미 → U5-023 얼굴 전체 토닝 · U5-024/025 토닝 · U5-099 등 M8 단위 시술 7개 추천이 있다(`step7-concerns.json` edges 9건)
  - 같은 원문은 「저출력 토닝만 권장」이라고 하는데, 상속으로 읽으면 기미 → 토닝 = 피함이 된다
  - `conflicts`에도 `origin_questions`에도 이 어긋남이 없다
- 고칠 방향(코디가 선택): ⓐ 5단계 키에 출력 칸이 없어 규칙으로 하나로 안 좁혀지므로, U8-1대로 원천 질문을 더하고 7단계 추천 ↔ 피함을 충돌 표시한다 · 또는 ⓑ qualifier가 있는 피함은 「조건부 — 단위 시술 미특정」으로 표시하고 기본 상속에서 뺀다. 둘 다 결정 파일 한 줄 + 고정 시험 1건이면 된다
- 참고: AV8-003 · 005(IPL 단독)는 U5-030 하나로 좁혀져 있어 문제없다

### F2 — 하위 조건이 갈리는 주장 2건은 겉 숫자 칸이 하위 조건을 섞어, 숫자 칸만 읽으면 원문과 다른 값이 된다

- 읽기 규칙: 추천 · AI는 `interval.days` · `first` · `same_day`만 읽는다(`reading_contract`). `options`는 읽기 규칙에 없다
- `R8-0003`(contraindications.rules[2] 보톡스 ↔ 레이저): 원문은 「비박리: 같은 날 가능(레이저 먼저) / **박리 CO2·Er:YAG: 3일~1주 간격**」이다. 겉 칸은 `same_day` = **True** · `first` = b · `days` = [0,7]이라, 박리 CO2 + 보톡스도 「같은 날 가능 · 레이저 먼저」로 읽힌다 — 안전 쪽 오독
- `R8-0013`(M3 ↔ M8): 원문은 「비침습/논어블레이티브 2~4주 / 어블레이티브 3~4개월」이다. 겉 칸 `days` = [14,120]이라, 어블레이티브의 하한이 2주로 읽힌다
- 원인: `step8-apply.py:46-83` — 하위 조건(`sub_condition`)이 있는 options도 「또는」처럼 겉 칸을 감싼 범위로 만들고 `same_day`는 하나라도 True면 True로 둔다. 「같은 날 또는 2주」처럼 하위 조건 없는 「또는」 5건(R8-0030 · 0049 · 0076 · 0083 · 0115)은 감싼 범위가 원문 뜻과 맞아 문제없다
- 고칠 방향: options에 `sub_condition`이 서로 다르면 겉 `same_day` · `first` · `days`를 비우고 「하위 조건별 값」 표시만 둔다(또는 읽기 규칙에 options를 더한다). 갈래 고정 시험 1건을 더한다

## WARN

### W1 — `research_diff`가 주장 원천별 셈만 담고, 이유는 일반 문장 하나뿐이다

- 조사 → 반영 사이에 셈이 바뀐 곳 가운데 이유가 기록 안 된 것:
  - **간격 수치 충돌** 4 → 2: 조사의 X8-007(M15↔M4 「필링 1주 후」 ↔ 「2주」) · X8-012(M2↔M8 「14일」 ↔ 「최소 4주」) · X8-020/021(M7↔M9 「1개월 후」 ↔ 「2~3개월」 · 「2-4주」)이 빠지고, M4↔M8 · M12↔M8이 새로 생겼다. 원인은 `step8-apply.py:1159-1167`이 「이상 · 후 · 뒤」를 위로 열린 범위로 겹침 비교하기 때문이다. 이것은 간격 사전 `open_high` 결정과는 맞지만, 조사가 쓴 비교 기준(「하한만 비교하지 않고 원문 범위 그대로」)과는 다르다. M2↔M8 · M7↔M9 쌍은 순서 충돌(Q8-3 · Q8-4)로 질문에는 남아 있다
  - 확인 조건 378 → 373: 기미 5건이 피함으로 옮겨감(U8-2)
  - 묶음 낱말 주장 3 → 2, 주장 종류 재분배(같은 날 불가 12 → 7, 원칙 · 조합 규칙(쌍) → 패턴 종류)
- 필요한 것: `research_diff`에 항목별 이유 한 줄씩(값을 고칠 필요는 없음)

### W2 — 웹 근거 노드 29 가운데 19개는 단일 URL이 아니다

- 7개(`EV-WEB-002` · 004 · 009 · 010 · 020 · 023 · 026)는 「;」로 이은 URL 2개가 한 노드에 들어 있다
- 12개(`EV-WEB-005`~008 · 011~018 · 028 · 029)는 URL이 없다. 내용은 「anatomy-danger-zones.json (internal)」 · 「clinical-standard …」 · 「임상 표준 …」 · taxonomy 칸 참조 · PubMed 번호 글자 같은 것이다. 그런데 모두 `kind` 「웹」으로 붙어 있다
- 셈 29는 G14(출처 문자열 중복 제거)와 맞지만, 종류 라벨을 그대로 믿으면 내부 참조 · 통설이 웹 출처로 읽힌다
- 필요한 것: 종류를 「원문 출처 문자열」로 두거나, URL 없는 것에 표시를 단다(쪼개기 · 추출은 G14대로 안 해도 됨)

## INFO

- **I1**: resolver 별칭 5개(PDO실 → M7 PDO · 비가교HA → M4 히알루론산 · HA필러 → M2 히알루론산(HA) · CaHA → M3 CaHA · 턱필러 → site 턱(묶음))의 하위 · 부위 값이 5단계 단위 시술 키에 없다. apply는 이것을 「단위 시술 키에 이 하위 계열 없음 — 계열(+조건) 단위 시술 후보 전부 · 하위 원문 보관」 플래그로 처리한다(R8-0145 · 0181 · 0196 · 0395 등). 숨긴 것은 없고 G2와도 맞다
- **I2**: 브리프는 「스킬 점검 8종」이라 했지만 `*/scripts/check_*.py` 글롭에 걸리는 것은 7개다. product-check는 `recheck_licenses.py`(MFDS 온라인 재조회)뿐이라 read-only 검수 범위 밖이어서 돌리지 않았다. 7종은 모두 errors 0
- **I3**: CC 조합 5건(R8-0262 · 0267 · 0369 · 0373 · 0383)의 이유 문장 「… 동시 개선」은 효과를 말하는 문장이지 간격이 아니다. interval 없음이 맞다

## 돌린 것(재현)

- scratch: `/private/tmp/claude-501/…/scratchpad/s8/w`(작업 폴더 사본)에서 `step8-apply.py --out r1` · `--out r2` → cmp 3파일 같음(커밋본과도 같음) · `step8-fixture-test.py` 37/37 · `step7-apply.py --out r7` → `step7-concerns.json` cmp 같음
- 스킬: `check_families.py --ledger step2-families.json --products step1-products.json` · 나머지 6종 `--work … --source …/phub-stg-2026-10-26` · `check_relations.py --selftest`
- 작업 폴더에는 이 리포트 말고 쓴 파일이 없다
