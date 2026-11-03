# [planner] SPEC-005 · WORK-003 보강 — 평가용 원장 MCP(raw-mcp) + 열린 것 결정 반영

(앞 지시 `phub-recommend-spec005-brief.md` · `-fix-brief.md` · 재검수 `review-spec005-v2-report.md`)

## 사용자 결정(10-30)
- hub-evals 실험(`reference/2026-10-30-hub-evals/README.md`)에서 원장 · 골드를 **같은 환경**으로 잰다 — 실험 레포가 Claude SDK 에 MCP 도구로 쥐어 줌. 원장도 MCP 로
- **원장 MCP 도구 3**(평가용 · 골드 · 시맨틱 사전 · 규칙에 기대지 않는 범용): `raw_list`(파일 21 · 각 파일 키 구조) · `raw_get`(파일 · 경로 하나 — 예 `taxonomy.problem[3]` · 크기 한도 · 잘림 표시) · `raw_search`(원장 전체 낱말 → 파일 · 경로 · 원문 조각 · 정규화는 공백 · 대소문자만 — 시맨틱 정규화 쓰지 말 것)
- 같은 허브 앱에 별도 마운트 `/procedure-hub/raw-mcp/mcp`(골드 MCP 와 같은 전송 · stateless · JSON) · REST 출구는 선택(필요하면 `/procedure-hub/raw`) · 원장 입력 = 로컬 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`(경로는 env · 해시 가드)
- 허브 본 역할(골드)과 섞지 않음 — §1 경계에 「평가용 원장 도구(골드 아님)」 한 줄 · §5 에 도구 절 · WORK-003 에 Phase(도구와 같은 Phase 또는 3b) · 시험(원장 도구가 시맨틱 · 골드를 import 하지 않음 가드)
- **열린 것 O-1 ~ O-4 = 추천대로 결정**(_RESUME §2 10-30 행): §7 에서 결정됨으로 옮기고 본문 반영(O-1 neighbors depth ≤ 2 · limit 50 · truncated · O-2 속도 기준 실측 뒤 · O-3 claude_contract 블록 냄 · O-4 넥큐레이션 3행 → P6-03)
- 머리에 「보강 2026-10-30(raw-mcp · O-1~O-4)」 한 줄

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_d604db9d-e1da-4569-bef7-73441af2e8d8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: SPEC-005 raw-mcp 보강" --body "원장 도구 N · Phase · 열린 것 N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] planner 완료 — SPEC-005 raw-mcp 보강. 상세는 인박스." --enter
```
