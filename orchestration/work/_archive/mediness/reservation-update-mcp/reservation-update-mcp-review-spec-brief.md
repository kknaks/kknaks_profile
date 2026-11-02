
# [reviewer_spec] 검수 — SPEC-151 §7.10(시각 해석)·§6.2b(update MCP 툴) + SPEC-060 예고

너는 **mediness `reviewer_spec` 워커**다. 먼저 역할 문서를 읽어라: `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 문서들)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/reservation-update-mcp-spec` (planner 미커밋 변경 3파일 +92/−5 위 — **read-only, stash·checkout·복원 금지**)

## 1. 먼저 읽을 것

- `git diff` — 리뷰 대상 (spec-151 · spec-060-mcp-surface · log.md)
- SPEC-151 개정 후 본문 전체 — 특히 §6.2·§6.2b·§7.9(무개정 주장)·신설 §7.10 과 기존 절들의 정합
- 코드 실측 대조용 (mediness-app read-only 절대경로 `/Users/kknaks/orca/workspaces/mediness-app/reservation-update-mcp/`): `mcp/app/tools/reservation_cancel_request.py` · `back/app/routers/action_runtime_v2.py:2027-2070` · `back/app/services/action_runtime/chat/provider.py:26-30`

## 2. 계약 (2026-08-31 사용자 확정 — 검수 기준)

1. `reservation_update_request` 툴 = 기존 update REST thin wrapper, cancel 동형. 새 REST·leaf·카드 유형 0.
2. 시각 해석: 명시 날짜+시간 그대로(침묵 조정 금지) / 완전히 지난 시각은 되묻기 1턴 → 예=그대로 카드·승인 게이트, 아니=미생성 / 모호 시각·날짜 없음 규칙은 유지.
3. §7.9 무개정 (파급은 기존 계약이 커버).

## 3. 검수 관점

1. **코드 실측 주장 검증** — planner 가 단정한 사실들: REST 실경로 `/reservations/{run_id}/update` · date 는 422 `update_date_forbidden` · title 수용 · 접수/후보 계산에 과거 거부 검증 없음 · 감사 규칙의 되묻기 억제 조항. 각각 코드에서 맞나.
2. **§7.10 내부 정합** — 「완전히 지났다 = 종료 시각 경계」가 R-1 과 모순 없이 서나. 되묻기 계약(카드 미생성·예/아니 처분·승인 게이트 불변)이 §5(상태 축)·§7.7(침묵 종결 금지)·감사 규칙 예외 명문화와 충돌 없나.
3. **§6.2b 등재 정합** — cancel 선례와 «동형» 주장이 실제로 동형인가(다른 것 1개=revision 만인가). 「아직 넣지 않은 것」 목록 정리가 정확한가.
4. **SPEC-060 규약 준수** — 실측 일치 표에 행·카운트를 안 늘리고 ⏳ 예고로만 실었는가.
5. **사용자 확정 3건 위반 여부** + 소유 경계(§7.9 diff 0 확인).
6. `python3 scripts/lint-pipeline.py --strict` 1회 — **리포 루트에서 실행** (PostToolUse hook cwd 이슈가 있었다). mediness 범위 ERROR 0.

## 4. 산출물 — 리포트 1개

`/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/reservation-update-mcp/review-spec-report.md`

- 판정(PASS/WARN/FAIL) + 근거(절·파일:줄). 리포 파일 수정·생성 금지. FAIL 기준은 확정 위반·계약 모순·사실 오류 — 취향 첨삭은 WARN 도 아님.

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 preamble 이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_spec 완료: <판정 한 줄>" \
  --body "판정 / 관점별 근거 / 위반 목록"

# (2) 직접 주입
orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a \
  --text "[worker_done] reviewer_spec 완료 — <판정>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --text "[질문] reviewer_spec: <질문>" --enter`
