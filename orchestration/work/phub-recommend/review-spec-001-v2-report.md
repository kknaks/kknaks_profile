# SPEC-001 · WORK-001 재검수 리포트 (reviewer_doc · v2)

> 2026-10-26 · 대상 수정본 `SPEC-001.md`(649줄) · `WORK-001.md`(286줄) · 기준 `DEC-001.md` · 1차 `review-spec-001-report.md`
> 수치: 1차에서 받아 둔 stg 응답 10개(새 GET 0)에 **바뀐 규칙**을 스크래치 스크립트로 다시 구현해 셌다(레포에 남기지 않음)

## 종합 판정: **FAIL**

1차 FAIL 7건은 전부 닫혔다. writer 가 센 값도 하나도 빠짐없이 재현됐다. FAIL 은 수정이 새로 만든 결함 1건뿐이다 — 시술군 단위 safety 묶음(F6 · §7 「응답이 크다」 대응)이
시술 항목에만 붙은 안전 엣지를 이웃 · 부분 그래프 응답에서 빠뜨린다(D-06). 고치는 범위는 한 문단이다.

| # | FAIL | 위치 |
|---|---|---|
| R1 | 이웃 · 부분 그래프의 `safety` 를 시술군 묶음으로만 내면, 시술 항목 끝점의 안전 엣지(stg 1건: CO2 프락셔널 ↔ 필러 같은 날 불가)가 그 항목의 safety 에서 빠진다 | SPEC:302 · 280 · 293 |

---

## 1. F1~F7 판정

| # | 판정 | 근거(수정본 위치 · 다시 센 값) |
|---|---|---|
| F1 | **PASS** | 좁은 규칙 세 개(제품 끝점 → `*_category` · 자기쌍 제외 + `self_relation_skipped` · `sequence_order` 는 양 끝 시술군 노드끼리만)가 SPEC:180-187 에 적혔다. 다시 세면 **106쌍 · 주장 167 · 충돌 7 · 자기쌍 1**이다. 넓게 읽을 때 108 · 12 가 나온다는 점과 OQ-S03 · OQ-S10 도 남겼다 |
| F2 | **PASS** | `coverage_gap` 이 원천별 하위 종류로 쪼개졌다(SPEC:221-229). 다시 센 값: `concern_item_without_taxonomy_ref` 26 · `_without_any_treats` 1 · `procedure_without_concern` 513 · `concern_without_curated_package` 6(P6 · P8 · P10 · P12 · P13 · P14). SPEC:171 「의도적으로 없음」도 ④ 예외를 적어 S-2 4번과 맞는다 |
| F3 | **PASS** | `edge_id` 해시 입력과 타입별 「원천 키」 열이 정해졌다. 원천 행 하나가 주장 하나다(SPEC:151 · 154 · 161-170). `treats` 엣지/주장 수 ① 105/105 · ② 32/63 · ③ 244/254 · ④ 19/26 → **400/448** 로 재현된다 |
| F4 | **PASS** | `category_id` 문자열/배열을 명시했다. ② 노드 키는 분류 키로 바꿨고 `group_ids` 를 펴서 쓴다(SPEC:136 · 140-141 · 168). `has_product` **154**(59 + 95) · 제품 동의어 **57** 이 재현된다. fixture 에 배열 케이스도 넣었다(WORK:190) |
| F5 | **PASS** | 동률 규칙(`cc_group` == 하위 분류 `label`)과 `ambiguous_cc_match` 를 추가했다(SPEC:173-174 · 211). 다시 세면 동률 4건이 모두 하나로 갈려 ambiguous 0 · unresolved 0/115 다. OQ-S09 도 열었다 |
| F6 | **PASS** | subgraph 에 `direction`(기본 `out`) · 무방향 엣지 처리 · 너비 우선 순서 · 상한 규칙이 생겼다. `has_procedure` 를 `has_child` 에서 떼어 냈다(SPEC:343-353). 다시 센 값: S-1 **노드 16 · 엣지 34**(treats: taxonomy 5 · problem-combos 5 · problem-packages 15), S-2 2번 **7 · 12**, 3번 엣지 4, 4번 엣지 3 · 주장 4 |
| F7 | **PASS** | 허용 목록 표가 SoT 가 되었다(SPEC:477-491). `app.repository.base` · `app.schema.base` · `app.core.logging` · `app.core.db` 를 넣었고 `app.core.lifespan` 은 금지로 명시했다. WORK:102 · 107 · 158 이 같은 목록을 옮겼다 |

**다시 센 값(전부 writer 값과 같음)**: 노드 941(타입별 §3.2 표와 같음 · 중복 id 0) · 엣지 **1,504**(`has_child` 170 · `has_procedure` 521 · `treats` 400 · `procedure_relation` 106 · `has_complication` 65 · `has_product` 154 · `site_caution` 22 · `synonym` 66) ·
M1 `procedure_relation` 이웃 **17** · M1 safety 엣지 6 · `orphan_node` 565(시술 항목 500 · 고민 하위 52 · 시너지 목표 10 · 고민 대분류 2 · 고민 항목 1) ·
`unresolved_by_source` 67/230 · 48/74 · 66/254 · 23/35 · optimization 이 제품으로 풀린 것 0.

## 2. WARN 반영

| # | 판정 | 위치 |
|---|---|---|
| W1 (검색 · 목록 safety 제외) | **OQ 로 남음** — OQ-S04(SPEC:643) · SPEC:281 | — |
| W2 이름 원천 필드 | 반영 — 「name ← · names.en ←」 열(SPEC:121-138) | — |
| W3 `?build=latest` | 반영 — 파라미터 · `build_id` · `build_status` · 발행본 없음 처리(SPEC:373 · 377-378) | — |
| W4 `limit=0` | 반영 — 검증 API 만 하한 0(SPEC:375 · 388) | — |
| W5 ruff 범위 | 반영 — WORK 전 Phase `uv run ruff check .` | — |
| W6 인덱스 이름 | 반영 — 이름 명시(WORK:135) | — |
| W7 S-4 「엣지 1개」 | 반영 — 「17개, 그중 M1↔M2 하나」(SPEC:550). 실측 17 | — |
| W8 S-7 재적재 | 반영 — `--save-dir` / `--from-dir` · 스크립트는 S-7 을 부르지 않음(SPEC:105 · 590-595 · WORK:246 · 248) | — |
| 1차 §7 (safety 에 시너지 섞임 · 응답 크기 · 알려진 이상) | 반영 — Safety 포함 조건(SPEC:293) · 시술군 묶음(SPEC:302) · §6.3 표 | R1 · W-n3 참고 |

## 3. 회귀 (수정이 만든 새 결함)

### R1 — 시술군 묶음 safety 가 시술 항목의 안전 엣지를 놓친다 (FAIL)

- SPEC:302 는 이웃 · 부분 그래프의 `safety` 맵 키를 「응답에 나온 `procedure_group` id + `procedure` 노드의 시술군 id」로만 정하고, 시술 항목은 `attributes.group_id` 로 그 묶음을 가리키게 했다. 시술군 묶음의 `procedure_relations` 는 그 **시술군 노드**에 붙은 엣지다(SPEC:293 「이 노드(또는 inherited_from)의」)
- 그런데 `procedure_relation` 끝점은 시술 항목일 수도 있다(SPEC:166). stg 실측으로 안전 주장(contraindications · minimum_intervals · incompatible_same_day)이 있는 시술 항목 끝점 엣지가 **1건** 있다: `procedure:M8-2-1`「CO2 프락셔널」 ↔ `procedure_group:M2` — `incompatible_same_day` 「열린 상처에 필러 주입 감염 위험」
- 부분 그래프나 이웃 응답에 `procedure:M8-2-1` 이 나오면 그 항목은 `procedure_group:M8` 묶음을 가리킨다. 이 엣지는 M8 시술군 노드에 붙어 있지 않아 **M8 묶음에 없다.** M2 가 같은 응답에 없으면 어디에도 실리지 않는다 → D-06 「시술 노드를 내보낼 때 안전 엣지를 **항상** 같이」 위반. 상세(`/nodes/procedure:M8-2-1`)는 SPEC:302 마지막 문장과 SPEC:293 덕분에 실린다. 그래서 같은 노드인데 상세와 부분 그래프의 안전 정보가 서로 다르다
- SPEC:280 「`procedure` 노드마다 `safety`」 · §6.2 두 번째 기준(SPEC:600)과도 문구가 어긋난다. WORK:223 의 「시술군당 한 묶음」 테스트는 이 누락을 그대로 굳힌다
- 고칠 자리: 시술 항목이 자기 이름으로 안전 엣지를 가지면 그 항목에도 묶음(또는 항목 전용 `procedure_relations`)을 싣는다는 한 줄 + WORK:223 · Phase 3 fixture 에 그 케이스 1개

### WARN

- **W-n1 Mount 예시가 옵션을 빠뜨린다**(SPEC:443 · WORK:234 ↔ SPEC:442 · WORK:233): 옵션은 `streamable_http_app(stateless_http=True, json_response=True)` 로 준다고 적고서, 바로 아래 마운트 예시는 `streamable_http_app()`(인자 없음)이다. 예시를 그대로 옮기면 stateful · SSE 응답으로 뜬다. `session_manager` 는 `streamable_http_app()` 을 부를 때 만들어지므로(`/run/asgi/` 「mcp.session_manager only exists after streamable_http_app() has been called」) 두 번 부르지 말고 한 번에 인자를 넣는 형태로 맞춰 두는 게 좋다
- **W-n2 WORK:182 「엣지 8종」**: SPEC:64 · 152 와 WORK:193 은 9종(`has_procedure` 추가)이다. 숫자만 낡았다
- **W-n3 §6.3 「이소트레티노인」 줄이 사실과 다르다**(SPEC:614): 「이소트레티노인 → 프락셔널 간격이 이 노드에 붙는다」고 썼지만, 다시 세면 `procedure:auto-M15-1775361878302` 에 붙는 `procedure_relation` 은 **0**이다. `minimum_intervals` 의 상대편(「프락셔널/얕은 필링」 · 「박리성(ablative) 레이저/심부 필링」)이 풀리지 않아 「양 끝 다 풀린 것만」(SPEC:182) 규칙으로 엣지가 안 생긴다. 사용자가 E2E 에서 그 엣지를 찾다가 헤맬 수 있다. 「노드는 있지만 간격 엣지는 상대편이 안 풀려서 없다」로 고치면 된다
- **W-n4 `synonyms` 가 비었는데 점수표는 `synonyms` 를 본다**(SPEC:123 ↔ 312-318 · 322): SPEC:123 은 「`names.en` 을 synonym 점수로 함께 본다」고 하지만, 점수 문장 · 표 · `match.field="synonym"` 은 `synonyms` 필드 기준이다. 결과는 같다(영문이라 S-1~S-3 후보 수 그대로 — 실측). 다만 점수 문장에 「`synonyms` + `names.en`」을 한 번 적어 두면 워커가 `names.en` 을 빼먹지 않는다

## 4. DEC 이탈 재확인

**PASS.**

- D-12: 빌드 · 해석 · 검색이 전부 규칙 · 정규화 · 사전순이다. 새 규칙(CC 동률 · 제품 동률 · 자기쌍 · 제품 끝점)도 결정론이고 모델이 없다(SPEC:173 · 194-199 · 180-185). 경계 테스트에서 LLM 클라이언트 금지도 그대로다(WORK:197)
- D-13c: 허용 목록에 레거시 · canonical 모델 · repository · service 가 없다(SPEC:488). 새로 허용한 `app.repository.base` · `app.schema.base` 는 세션 틀 · Pydantic base 뿐이라 테이블을 읽지 않는다. `app.core.db` 는 엔진이다
- D-13d: 동의어는 정규화 완전 일치만 쓴다. 제품 동의어에 「`group_ids` 겹침」 조건이 추가됐는데, 이건 매칭을 넓히는 게 아니라 좁히는 조건이다(SPEC:141 · 170)
- D-13e: `treats` 는 원천이 다르면 다른 엣지다(원천 키 = 엔드포인트, SPEC:165). 같은 원천 안에서도 행을 주장으로 보존하고 합치지 않는다. 제품 두 원장도 합치지 않는다

## 무관

없음. 문서만 검수했다.
