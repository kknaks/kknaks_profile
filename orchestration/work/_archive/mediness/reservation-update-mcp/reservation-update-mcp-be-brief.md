
# [backend] WP-128 착지 — ① reservation_update_request MCP 툴 ② 시각 해석 규칙 재작성

너는 **mediness `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/roles/mediness/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/reservation-update-mcp`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

이 워크트리는 지금 backend 너 혼자다.

## 1. SSOT — 먼저 읽을 것 (spec 워크트리 절대경로 — read-only, 수정 금지)

- `/Users/kknaks/orca/workspaces/mediness-mediness/reservation-update-mcp-spec/products/mediness/30-work/work-128-reservation-update-mcp-time-resolution.md` ← **작업의 SoT. P1~P3 를 이대로 착지한다.**
- `/Users/kknaks/orca/workspaces/mediness-mediness/reservation-update-mcp-spec/products/mediness/20-spec/spec-151-ax-assistant-reservation.md` §6.2·§6.2b·§7.10 — 계약
- 위 문서들은 spec 레포 브랜치(미커밋·미머지)에 있다 — 네 워크트리 base(origin/dev)에는 없으니 **반드시 위 절대경로로 읽어라.**

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- `<…/para/areas/concept/<영역>/<stem>.md>` — <이 작업에서 무엇을 이대로 하라는 건지 한 줄>

## 2. 배경 / 무엇을 바꾸나

① MCP 로 잡은 완료 예약을 «시간 변경해 달라» 하면 에이전트가 「변경이 안 된다」고 답한다 — back REST(`/reservations/{run_id}/update`, off-graph 변경 amendment)는 있는데 MCP 손이 없다. cancel(`reservation_cancel_request`)과 동형의 update 손을 만든다.
② 15:08 「오늘 오후 3시」 예약이 말없이 다음날로 잡혔다 — `TIME_RESOLUTION_RULE` 의 무조건 미래 제약 때문. §7.10 (R-1 명시 날짜·시각 그대로 / R-2 완전히 지난 시각은 되묻기 → 예=카드·아니=미생성 / R-3 시각 축은 날짜를 옮기지 않음) 으로 재작성한다.

## 3. 계약 — WP-128 이 전부다. 특히 어기기 쉬운 것:

- ① 툴은 **thin wrapper** — 새 REST·새 leaf·새 카드 유형 0. server.py 등록 + 오염 등급 선언(미선언 = 기동 실패가 곧 확인). date 는 현재와 다른 값이면 422(동치는 통과) — 우회로 만들지 마라.
- ② 재작성 규칙에서 'must start in the future' **와** 'from now' 상대 구절 둘 다 제거. now-상대 해석은 «날짜 없는 요청» 한정으로 명시. 되묻기는 **접수 해석 축**에서 갈린다 — 감사 프롬프트에 얹으면 구조적으로 동작하지 않는다(§7.10 ⛔). 되묻는 턴엔 카드 0, 고정 문구 템플릿 신설 0(질문은 «지난 시각 사실 + 잡을지 물음» 두 축 포함).
- 테스트: WP-128 P1·P2 열거 케이스 전부 — R-1 고정(15:08 「오늘 15~16시」→오늘) · 되묻기 3분기 · 감사 포함 end-to-end 회귀 · 21:57 「오늘 3시」 합성 · 금지 구절 부재 단언 포함.

## 4. 먼저 읽을 핵심 파일

- `mcp/app/tools/reservation_cancel_request.py` — ① 동형 표본 (구조·409·requires_tools·감사 문구)
- `mcp/app/server.py` — 등록·오염 등급 fail-fast (`assert_write_tools_declare_taint`)
- `mcp/tests/test_tool_inventory.py` — 인벤토리는 «착지 시점 실측 +1» (표 숫자 옮겨 적기 금지 — 머리 주석이 규율)
- `back/app/services/action_runtime/chat/provider.py:26-30` — 재작성 대상 `TIME_RESOLUTION_RULE`
- `back/app/routers/action_runtime_v2.py:2050-2070` — 감쌀 update REST

## 5. allowed_paths — 이 밖은 건드리지 마라

- `back/`
- `mcp/`
- `docker-compose.yml`
- `docker-compose.local.yml`

## 6. 구현 단계

1. WP-128 P1 (MCP 툴 + 툴 테스트 + 인벤토리 실측 +1) — mcp/ 만.
2. WP-128 P2 (규칙 재작성 + 되묻기 접수 해석 축 + 테스트) — back/ 만. P1 과 파일이 안 겹친다.
3. WP-128 P3 (무회귀 — 기존 시각 해석 소비처·cancel 툴 무회귀 확인).

## 7. 범위 제약 — 하지 말 것

- WP-128 비목표 전부. §7.9 체인·모달 경로·회의관리 무개정. spec 워크트리 수정 금지.
- 커밋·push·PR 금지 — 워크트리에 변경만 남긴다.

## 8. 검증

```
cd back && pytest -q <네가 만들거나 고친 테스트 파일만> (전체 스위트 금지 — 사용자 방침. DATABASE_URL 은 back/pyproject.toml 의 테스트 DB = localhost:25434/mediness_test) + cd mcp && pytest -q <네가 만든 툴 테스트만>. 검증은 1회만 — 통과하면 반복하지 마라
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
  --to term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
