# 재검수 v2 — SPEC-005 · WORK-003 (v1 지적 수정분)

**PASS** · FAIL 0 · WARN 0 · **open = 4**(SPEC §7 O-1 · O-2 · O-3 · O-4 — 넷 다 「안 막음」)

- 대상: `SPEC-005.md` · `WORK-003.md`(13:40 수정본 · 머리에 「검수 반영 2026-10-30(F-1 ~ F-5 · W-1 ~ W-9)」 한 줄 있음)
- 기준: v1 `review-spec005-report.md` · 코디 수정 지시 `phub-recommend-spec005-fix-brief.md`(F-5 = 판단 ①) · `_RESUME.md` §2 · 실물 json
- 실물 칸 · 셈 · 가드 식은 스크립트로 다시 돌렸다. 쌍 셈은 `step8-apply.py` `UnitSets` 를 import 해서 셈(파일 쓰기 없음). 입력 해시 11/11 은 v1 때와 같고, 노드 1,071 · 저장 엣지 3,179 도 그대로다

## 1. v1 지적 — 고쳐졌나

| id | 고친 곳 | 실물 대조 | 판정 |
|---|---|---|---|
| F-1 | §2-2 step5 행 · §5-4 overview · method · recovery · aftercare · §3-6 | `source_text` 칸 = aftercare · safety.common · serious · note · contraindications · long_term(셈 521 · 521 · 189 · 4 · 4 · 1 / 59 · 59 · 31 · 1 · 1)로 적음. overview · method 는 `family_text` 「환자 설명 가이드」 `simple_explanation` · `how_it_works` · `pain_level` · `common_concerns` + 근거 문장 moa · effects. recovery 는 `downtime` · `duration_simple` — 칸 전부 실물에 있음. 단위 시술 · 제품 개요 없음은 §3-6 보강 후보로 | 고쳐짐 |
| F-2 | G9 가드 | 「`override_of` 가 계열 노드(27)에 없으면 실패」. 실물 override 624 의 override_of 계열은 전부 계열 노드 안에 있다. gap 계열 72(N1 63 · N4 4 · N5 2 · N2 · N6 · N7 각 1)는 「정보 없음(gap)」으로 다룸 — 셈이 실물과 같다 | 고쳐짐 |
| F-3 | G15b 가드 | 「`None` 을 뺀 방향별 값이 둘 이상이면 실패」 = `step8-apply.py:2008` 과 같은 식. 실물 걸림 0 · 한쪽 None 11건 통과 | 고쳐짐 |
| F-4 | §5-10 T9 | 「G18 라벨 8 — 고민 패키지의 `anchor.source_label`」 | 고쳐짐 |
| F-5 | G18 · §5-2 T1 · §6-1 · WORK Phase 2 · 3 · 4 | 기존 고민 대상 mode 그대로 · `menu_candidates[]` 라는 별도 칸 · I-01 은 `candidates` 의 concern · site 만 · I-11 은 라벨이면 menu 후보로 T7. 예시도 실물과 같음(처짐/탄력 P3 · P4-1 「전부」 · 색소/미백 P5 「하나」 · 쁘띠시술 `none:` + menu) — 코디 판단 ① 그대로 | 고쳐짐 |
| W-1 | §3-3 가드 문단 | 전역 제외 229엣지 → 4,674 · 2,048 · 100 / 포함 230 → 4,791 · 2,075 · 105 · 차이 5 = 전역 때문에 생긴 쌍 — 다시 셈해 같음 | 고쳐짐 |
| W-2 | §3-3 확인 조건 | 대상 키 셈 family 195 · units 20 · all 16 · product 7 · ledger 3. product · ledger 는 단위 시술을 덮지 않음. product 행은 제품에만 붙고, ledger 행은 「대상 없음」으로 보관(O-4) — 실물과 같음 | 고쳐짐 |
| W-3 | §3-2 9단계 「사전 적재 + G18」 · WORK Phase 2 같은 자리 | 둘이 맞음 | 고쳐짐 |
| W-4 | §6-1 · WORK Phase 4 | Q101 → T3 `sections=overview,ops`. 원문 `family_text.M9` 환자 설명 가이드 `pain_level` 은 F-1 에서 overview 칸에 들어감 | 고쳐짐 |
| W-5 | §3-3 자기 쌍 행 · §5-5 입력 · §6-1 · WORK | self_pair 엣지 4(E8-0059 · 0214 · 0225 · 0228 — 실물 a == b 인 엣지도 이 4개뿐) · `step8-apply.py:2028` u ≠ v 건너뜀 확인 | 고쳐짐 |
| W-6 | G6 · T2 ③ | `site_rules.site_free` = 「해당 없음」 · 「병변 단위」 통과 | 고쳐짐 |
| W-7 | G9 | priority 작을수록 먼저 · 0 = 111 · 1 = 207 + 58 · 2 = 159 · 3 = 89 · 그다음 계열 — 실물 셈과 같음 | 고쳐짐 |
| W-8 | §3-0 「골드 판단 ⑤」 행 | 실물 4행 `also_sub_families` KTP · G5 가 읽음 | 고쳐짐 |
| W-9 | §2-1 · §3-3 | semantic.md 문장은 「읽지 않는다」만 남음. `covers` 는 `:1976` 로 고쳐짐. `semantic-build.py:661` 은 그대로 두었는데 **v1 지적이 틀렸다** — `inputs = {…hashlib.sha256…}` 는 실제 661행에 있다(v1 의 「662」 철회) | 고쳐짐(v1 일부 철회) |

## 2. 고치면서 새로 생긴 어긋남 · 새 결정

- 새 어긋남: 없음. WORK Phase 0 입력 대조 셈(override 624 · 72 · by_direction 118 · 자기 쌍 4 · product 7 · ledger 3 등)을 실물과 대조해 모두 같았다
- 결정표에 없는 새 결정이 「정해진 것」으로 들어간 곳: 없음
  - 자기 쌍 규칙(self_pair 엣지의 resolved · 가장 구체적인 것)은 8단계 데이터를 읽는 방법일 뿐이고 값을 새로 정하지 않는다
  - Q101 · Q091 의 도구 대응은 측정 경로다. 문항 · 정답 · 채점 식은 바꾸지 않는다
- O-4 가 정말 결정표 밖인가: **맞다**
  - `_RESUME.md` 에 ledger 대상 처리 결정이 없다(grep 0)
  - `semantic ids.string_forms` 의 ledger 규칙은 「→ product:{원장 id} · 행선지 없는 원장 항목이면 대상 없음 표시」까지다
  - 실물에서 `ledger:auto-6-1774737181584` 는 step1 제품에 없고 ids.map 에도 없다. 대신 `step6 packages[] P6-03 「넥큐레이션」 ledger_id` 로 있다
  - 그래서 패키지에 붙일지는 정해진 적이 없고, 「대상 없음」 보관은 semantic 규칙을 그대로 따른 것이다

## 3. v1 PASS 항목 회귀

- 입력 해시 11/11 · §2-2 다른 칸 · 셈 · D-01 ~ D-14 · 판단 ① ~ ④ · U-1 ~ U-3 · KOS · hub-evals · §6 완료 조건 · WORK Phase 순서 · 완료 조건 · 로컬 전용 · push 금지 · 뼈대 재사용: v1 판정과 같음. 회귀 0
- SPEC `version` 은 0.1.0 그대로이고 WORK 의 「SPEC-005 0.1.0」 표기와 맞는다
