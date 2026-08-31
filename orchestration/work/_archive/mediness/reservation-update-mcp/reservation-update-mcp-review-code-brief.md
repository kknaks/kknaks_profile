
# [reviewer_code] 검수 — WP-128 착지 (update MCP 툴 + 시각 해석 재작성)

너는 **mediness `reviewer_code` 워커**다. 먼저 역할 문서를 읽어라: `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 문서들)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/reservation-update-mcp` (**read-only — backend 미커밋 변경 11파일 +169/−23 위. 수정·테스트 실행 금지** — 코디가 52+46 passed 독립 확인)

## 1. SSOT — 판정 기준

- `/Users/kknaks/orca/workspaces/mediness-mediness/reservation-update-mcp-spec/products/mediness/30-work/work-128-reservation-update-mcp-time-resolution.md` — 작업서
- 같은 경로 `.../20-spec/spec-151-ax-assistant-reservation.md` §6.2·§6.2b·§7.10 — 계약
- 워커 리포트: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-app-reservation-update-mcp/38056ae4-770a-4253-88ad-c4397a576f55/scratchpad/wp-128-backend-report.md`

## 2. 검수 관점

1. **① 툴이 정말 thin wrapper 인가** — cancel 동형(구조·409/404·requires_tools·오염 등급·감사 문구), 새 REST·leaf·카드 유형 0. date 를 툴이 자체 판정하지 않고 back 에 넘기는가(계약: 판정은 back 소유).
2. **② 규칙 재작성** — 'must start in the future'·무한정 'from now' 부재. R-1~R-4 가 규칙 문면에 서고, now-상대가 «날짜 없는 요청» 한정인가. 기존 예시 2개 보존/정합.
3. **되묻기 배선** — `CatalogTurn.clarification` 축이 «접수 해석»에서 워크플로 선택 **전에** 갈리는가. 되묻는 턴 카드 0. 감사 규칙 6 무개정 주장 diff 로 확인. 「감사 스코프 밖(정형 응답 축)으로 내보냄」이 §7.10 의 출구/결정 분리와 맞는가 — service.py 변경분 정독.
4. **인벤토리 실측 +1** — 62 = 40+22 가 test_tool_inventory 규율(그 시점 실측)대로인가. 부수 수정 4파일(test_read_file_offset 등)이 수치 동기 외 변경이 없는가.
5. **테스트가 계약을 무는가** — R-1 고정·되묻기 3분기·질문 2사실·감사 포함 회귀·21:57 「오늘 3시」 합성·금지 구절 부재 단언. 빠진 분기.
6. **allowed_paths·무관 실패 분리** — diff 가 back/·mcp/ 만인가. pre-existing 14건 주장(HEAD 동일)의 근거가 리포트에 있는가.

## 3. 산출물 — 리포트 1개

`/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/reservation-update-mcp/review-code-report.md`

- 판정(PASS/WARN/FAIL) + 위반 목록(파일:줄 + 근거 계약 절). 리포 파일 수정·생성 금지.

## 4. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 다르면 preamble 이 맞다. 한 곳으로만 보내라.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "reviewer_code 완료: <판정 한 줄>" \
  --body "판정 / 관점별 근거 / 위반 목록"

# (2) 직접 주입
orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a \
  --text "[worker_done] reviewer_code 완료 — <판정>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --text "[질문] reviewer_code: <질문>" --enter`
