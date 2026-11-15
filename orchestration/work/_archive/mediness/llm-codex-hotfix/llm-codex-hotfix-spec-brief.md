
# [planner] 서버 LLM 경로 claude → codex 핫픽스 — SPEC 반영 + WP 작성

너는 **mediness `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/roles/mediness/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/llm-codex-hotfix-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness` (PR 은 코디네이터가 올린다)

너는 앞 맥락이 없다. 이 브리프와 아래 리포트가 입력의 전부다.

## 1. SSOT — 먼저 읽을 것

- **운영 실측 리포트(사실의 원천)**: `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/work/llm-codex-hotfix/survey-prod-claude-usage.md` — 경로 A~G 정의·운영 env·실패 근거. 여기 경로 기호(A·B·C·D…)를 그대로 쓴다.
- 레포 문서 규칙: `AGENTS.md` · `rules/document-pipeline.md` · `context/manifest.yaml` · `context/current-state.md` (SPEC 수정·WP/Delivery Issue 절차는 여기 따름)
- 관련 SPEC (이 워크트리 `products/mediness/20-spec/`): `spec-070-briefing.md`(C) · `spec-130-weekly-report.md`(D) · `spec-111-decision-intake-slack.md` / `spec-156-decision-chat-intake-workflow.md`(B) · `spec-116-okknaks-v2-migration.md`(provider 파이프) · **선례** `spec-031-meeting-v2-diarization.md`(회의록 codex 전환 2026-08-11 C1) · `spec-230-landing-agent-chat.md` §3(codex 제출 스펙)
- 코드(운영 = mediness-app `origin/main`, **read-only**): `git -C /Users/kknaks/git/harness_works/mediness-app show origin/main:<경로>` 로 읽어라. checkout·pull 금지.

**기대는 개념** — 해당 없음. 원칙: **새로 설계하지 말고 회의록 v2 의 codex 전환 선례를 그대로 따른다.**

## 2. 배경 / 무엇을 바꾸나

2026-11-10 부터 조직이 Claude Code 구독 접근을 막아 서버의 claude 호출이 전부 실패한다(리포트 §0). 데일리 브리프(C)는 11-10~13 매일 FAILED, 주간보고 AI 요약(D)은 11-13 4콜 실패. 회의록 v2(E)·랜딩 채팅(F)은 이미 codex 라 정상이다.

사용자 결정(2026-11-13) — **다시 묻지 마라**:

| # | 결정 |
|---|---|
| D1 | 서버 LLM 경로를 **codex 로 살린다.** 이번 핫픽스 범위 = **B(결정 게이트 `_default_ai_call`, 이를 재사용하는 B′ pipeline_ingest 포함) · C(데일리 브리프) · D(주간보고)**. 셋 다 worker 큐 `mediness-brief` 로 제출되고 worker 에는 codex·인증이 이미 있다 → **코드만** 바꾼다. |
| D2 | **A(AX 비서 back 직접 spawn)는 이번 범위 밖** — back 파드에 codex·인증이 없어 인프라(GitOps 차트) 작업이 필요하다. 별도 후속으로 둔다. `DEPLOY.md §4-4` 드리프트도 그쪽 몫. |
| D3 | 사용자 PC 데몬 `agent/` 는 범위 밖. |
| D4 | 코드는 **main 기준 핫픽스** → 머지 후 main→dev 반영. |

## 3. 계약

해당 없음 (BE 단독). 단 WP 는 아래를 **코드 근거(파일:줄)로** 명시해야 한다 — 코드 워커가 이것만 보고 구현한다:

- B·C·D 각 제출 지점의 현 claude 제출 스펙(provider·model·provider_options 키·options) ↔ codex 제출 스펙(회의록 v2 `meeting_v2_submission.py` / 랜딩 `landing_chat/submission.py` 선례)의 대응표.
- codex 가 거부하는 claude 전용 키(`system_prompt`·`max_turns`·`json_schema`·`allowed_tools`·`mcp_config`·`effort` 등)를 각각 **어떻게 옮기나**: 프롬프트 앞 붙이기 / codex MCP 주입(`-c mcp_servers…`·enabled_tools) / 버림 — 선례가 한 방식 그대로.
- 모델: 선례(`meeting_codex_model` 빈 값 → landing 모델)와 같은 방식. provider 를 설정값으로 둘지 고정할지도 **선례 방식**을 따른다.
- 결과 파싱: claude 출력 형식에 기대던 파싱(JSON 응답 등)이 codex 출력에서 깨지지 않는지.
- 수용 기준: 운영과 같은 조건에서 **실물 codex 호출 1회**씩(C 브리프 합성 1회 · D 주간 version_summary 1회 · B 게이트 1회) 성공 — 단위 테스트만으로 done 아님.

## 4. 먼저 읽을 핵심 파일 (mediness-app `origin/main`)

- `back/app/services/decision_gate.py:651-720` — B `_default_ai_call` (provider 기본 claude, claude options)
- `back/app/services/pipeline_ingest_consumer.py:144-200` — B′ 재사용
- `back/app/services/brief/synthesizer.py:540-580` — C 제출 (`provider="claude"`, mcp_config·allowed_tools)
- `back/app/services/weekly_report_pipeline.py:490-530` — D 제출
- `back/app/services/meeting_v2_submission.py` · `meeting_v2_extractor.py:440-550` — **codex 선례** (provider 분기)
- `back/app/services/meeting_extractor_client.py:240-330` — `provider_options` 통째 전달 seam
- `back/app/services/landing_chat/submission.py` — codex 제출 스펙·resume 제약·MCP 주입
- `back/app/config.py:255-275` — `meeting_llm_provider`·`meeting_codex_model` 선례

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/mediness/`
- `context/`

## 6. 구현 단계

1. 리포트 + SPEC 들 + 선례 코드 읽기.
2. **SPEC 반영** — B·C·D 의 LLM provider 를 규정하는 SPEC 절을 codex 로 고친다(선례 SPEC-031 C1 처럼 결정·날짜·근거를 남김). provider 를 어디서도 규정하지 않으면 그 사실을 보고하고 최소 절만 추가.
3. **WP 작성** — 레포 규칙(번호·frontmatter·Delivery Issue/대시보드 절차)대로 새 WP 1개. §3 의 대응표·옮기는 방식·수용 기준 포함. **구현 대상 브랜치 = mediness-app `main`(핫픽스)** 명시. 범위 밖(A·agent·DEPLOY §4-4)을 「후속」으로 명시.
4. 결정이 선례로 안 닫히는 지점은 **추측으로 메우지 말고** WP 의 Open 항목으로 남기고 보고에 적는다.

## 7. 범위 제약 — 하지 말 것

- mediness-app 코드 수정 금지(읽기만). A 경로 설계 금지.
- 사용자 결정 D1~D4 를 바꾸거나 되묻는 문서 작성 금지.
- 관련 없는 SPEC 정리·리포맷 금지.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict   → 이번에 만진 파일 ERROR 0 (타 제품 기존 WARN/ERROR 는 「무관」으로 분리)
git -C /Users/kknaks/orca/workspaces/mediness-mediness/llm-codex-hotfix-spec status --short  → products/mediness/·context/ 밖 변경 0
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_4d39f44d-7335-41dc-bd4a-b274304b05d9 --from term_7c6d1054-c63d-4781-a69b-faa689f5bcfb \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4d39f44d-7335-41dc-bd4a-b274304b05d9 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4d39f44d-7335-41dc-bd4a-b274304b05d9 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
