# 재검수 보고서 — SPEC-006 v2.1(0.3.1) · WORK-006

작성 2026-11-01 · 검수자 reviewer 워커(읽기 전용 · 수정 없음 · 실물 호출 없음) · 전 판 `review-spec006-v2-report.md`(FAIL 3 · WARN 5)
대상 `SPEC-006.md`(0.3.1 · diff 로 바뀐 줄 전수) · `WORK-006.md`(Scope 표 · WP-0~WP-5) · 대조 = 앱 레포 `clinic_chat/hub-evals`(HEAD 18561a4 · `tests/` 실물 · Meta grep 재실행) · SPEC-005 v3.2 §5-16 · 전 판 근거(fail-triage2 · 바이너리 문자열)는 그대로

## 판정 — **FAIL(경미 1 · 한 줄이면 PASS)** · FAIL 1 · WARN 1

한 줄: 전 판 FAIL 3 · WARN 5 는 전부 반영됐다 — 시험 경로는 실물 폴더로 고쳐졌고(기존 6 전부 존재 · 새 시험은 `tests/phase8/`), Meta 의 grep 을 다시 돌리면 29 파일이 전부 Scope 표에 있으며(deps.py · test_case3.py → fallback · fake_jev 등 추가 · judge 는 「영향 없음」), Codex 마커는 실물 후보 5 를 넣고 WP-0 4 「한도를 일부러 작게 한 호출」 로 `TRUNCATION_MARKERS` 를 고정하는 절차가 들어갔다. 남은 결함은 §3-4-2 의 peek 이웃 꼴이 아직 평면(`neighbors[]{id, kind, edge, label}`)이고 SPEC-005 §5-16(`neighbors_by_kind{…items[:8]}`)을 따른다는 말이 없는 것 하나다.

| 기준 | 판정 | 요지 |
|---|---|---|
| 1 실물 대조 | PASS | §3-5 표 = 전 판 부록 A 와 같음 + 바이너리 확인 항목(`P=25000` · `persistenceThresholdCeiling` · `tool-results/mcp-<name>-blob-…` · Claude 마커 4 + 변형 3 · Codex 키 2 · 실물 후보 5) 그대로 반영 · 「50,000 자」 는 문서 인용임을 명시하고 WP-0 실측 열로 닫음(W-3) |
| 2 fail-triage2 대조 | PASS | 숫자 변화 없음 · §4-4 · §7-6 에 C 비율(fail-triage2 §2 와 같은 셈 — `facts[].text` 정규화 ∋ 인용) 열 추가(W-2) · `intent_passed` 는 값 ∈ I-01~I-12 일 때만 true(`none` 2 → false · W-5) |
| 3 보충 대조 | **FAIL(경미 · F-1)** | 숫자(걸음 4 · 예산 20KB · peek ≤ 2KB · `intent?` 넘김)는 SPEC-005 §5-16 · v3.2 와 맞음(005 쪽이 「받되 무시」 로 고쳐지는 중). **이웃 꼴만** §3-4-2 가 평면 목록으로 남아 있고 「SPEC-005 §5-16 꼴(by_kind · items[:8])을 따름」 이 없음 |
| 4 결정표 충돌 | PASS | 변화 없음 |
| 5 WORK-006 | PASS | 시험 경로: `tests/phase2/test_loop.py` · `tests/cli/test_cli.py` · `tests/cli/test_report.py` · `tests/cli/test_rerun_report.py` · `tests/phase3` · `tests/phase7` 실물 존재 · 새 시험은 `tests/phase8/{test_cli_ingest,test_prompts,test_case3_walk,test_verify_runs}.py` 로 「새」 표시(F-1 해소) / Meta grep 재실행 **29 파일 → Scope 표 밖 0**(F-2 해소 · `deps.py` · `batch.py` · `judge.py`(영향 없음) · `tests/phase3/test_case3.py → test_case3_fallback.py` · `phase2 · 4 · 7` · `cli/test_*` · `fake_jev.py` · `mock_server.py` · `estimate_cost.py` · `web/state.js` 전부 표에) / WP-0 4 마커 확정 절차 · WP-1 `TRUNCATION_MARKERS` · `intent_passed` 값 규칙 · `phase8/test_cli_ingest.py` 시험 항목(F-3 해소) / depends_on 에 v3.2 보충 2 전달 확인(W-1) |
| 6 추측 자리 | PASS | 「50,000 자 · 250,000 자」 인용값임을 적고 실측으로 닫음 · 마커는 WP-0 실물로 고정 — 새 추측 자리 없음 |

## FAIL

### F-1 · SPEC-006 §3-4-2 — peek 이웃 꼴이 SPEC-005 §5-16 과 다르고 「따름」 문구가 없음(기준 3)

근거: §3-4-2 「앱이 읽는 칸(최소)」 = `neighbors[]{id, kind, edge, label}`(평면). SPEC-005 v3.2 §5-16 peek 출력 = `neighbors_by_kind{edge kind: {n, direction, items[:8]{id, kind, name(≤ 20자), label}}}` + `sections[]{name, n_facts, bytes}` + `priority_hint[]`. `sections` 는 같고 `intent?` 는 005 가 「받되 무시」 로 맞추는 중(코디 11-01)이라 문제없지만, 이웃은 키 · 구조가 달라 WORK-006 WP-3 1 「`hub_rest.py` peek · expand(v3.2 계약 · 모의 허브에 같은 꼴)」 과 `tests/fake_hub/gold.py` 모의가 어느 꼴을 만들지 정해지지 않는다(2단 Choice 「kind → id」(W-3)도 by_kind 를 전제로 함).
방향: §3-4-2 peek 행을 「**SPEC-005 §5-16 꼴을 따른다** — `neighbors_by_kind{kind: {n, direction, items[:8]{id, kind, name, label}}}` · `sections[]{name, n_facts, bytes}` · `priority_hint[]` · `intent?` 는 넘기되 허브가 무시(`intent_used: null`)」 한 줄로 바꾸고, `expand` 행도 「`sections{s: {facts[], more_ids[], total}}` · `neighbors[]{…}`(요청한 것만) · `facts[]` · `claude_contract`」 로 §5-16 이름에 맞춘다. 2단 Choice 는 `neighbors_by_kind` 의 kind 키 → items id 로.

## WARN

| id | 조항 | 내용 · 방향 |
|---|---|---|
| W-1 | WORK-006 Meta 「11-01 실행 결과 28 파일」 | 지금 레포에서 같은 grep 을 돌리면 **29** 파일(전부 표에 있음 · 빠짐 0) — 숫자만 29 로 |

## 전 판 FAIL · WARN 반영 확인

| 전 판 | 반영 | 확인 |
|---|---|---|
| F-1 시험 경로 4 | 기존 경로로 고침 · 새 시험 `tests/phase8/` · `test_prompts.py` 「새」 | WP-1 · WP-2 · WP-3 검증 명령의 `tests/…` 9 경로 전부 실물 존재 또는 phase8 새 파일 |
| F-2 표 밖 14 | Scope 표에 deps · batch · judge(영향 없음) · phase3(→ fallback) · phase2 · 4 · 7 · cli 4 · fake_jev · mock_server · estimate_cost · state.js · phase5 · 6(영향 없음) 추가 | grep 재실행 29/29 표 안 |
| F-3 Codex 마커 | §3-5 표 실물 후보 5 + 옛 꼴 「쓰지 않는다」 · 정의 = `TRUNCATION_MARKERS` 상수(WP-0 고정) · WP-0 4 확정 절차(Claude `MAX_MCP_OUTPUT_TOKENS=1000` · Codex `tool_output_token_limit=500`) · `settings.truncation_markers_sha` | ○ |
| W-1 v3.2 보충 2 | depends_on · §7-7 W-1 · W-2 「보충 2 로 전달 · 11-01 확인」 | ○(문서 확인은 코디 기록 기준) |
| W-2 C 비율 | §4-4 행 · §7-6 비교 보고 열 | ○ |
| W-3 50,000 자 | §3-5 「바이너리에서 숫자 특정 못 함 → WP-0 문턱 실측값 열」 · WP-0 5 | ○ |
| W-4 Claude 변형 3 | §3-5 표 · 정의 「Claude 4 + 변형 3」 · `--no-session-persistence` 직결 명시 | ○ |
| W-5 intent `none` | §3-6 기록 규칙 · WP-1 시험 「`intent: "none"` → false」 | ○ |
