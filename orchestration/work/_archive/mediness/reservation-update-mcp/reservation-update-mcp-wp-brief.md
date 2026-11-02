
# [planner] WP 작성 — update MCP 툴 + 시각 해석 §7.10 착지 작업서

너는 **mediness `planner` 워커**다. 네가 쓴 SPEC-151 §6.2b 등재·§7.10(검수 PASS + 정정 반영)이 사용자 승인을 받았다. 이번 발주는 **구현 WP 작성**이다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/reservation-update-mcp-spec` (네 미커밋 변경 위에서 계속)

## 1. SSOT — 먼저 읽을 것

- `products/mediness/20-spec/spec-151-ax-assistant-reservation.md` §6.2·§6.2b·§7.10 ← 계약. **WP 는 착지 계획이다 — 계약을 다시 정하지 마라.**
- 검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/reservation-update-mcp/review-spec-report.md` — 「WP 몫」·기존 부채 목록
- 코드 표본 (mediness-app read-only): `mcp/app/tools/reservation_cancel_request.py`(동형 표본) · `back/app/services/action_runtime/chat/provider.py:26-30`(삭제·재작성 대상 규칙) · `mcp/tests/`(툴 테스트 관례)
- WP 형식 표본: `products/mediness/30-work/work-125-reservation-meeting-autoregister.md`

## 2. 만들 것 — WP 1건 (`work-NNN`, 다음 빈 번호)

- **P① MCP 툴**: `reservation_update_request` 신설 — cancel 동형 wrapper, server.py 등록, 인벤토리 실측 갱신(SPEC-060 예고 ④ 해소는 착지 시 — WP 에 갱신 자리 명시), 툴 테스트(409·404·성공·date 동치/변경 케이스).
- **P② 시각 해석**: `TIME_RESOLUTION_RULE` 의 무조건 미래 제약 문장 **삭제·재작성**(§7.10 R-1~R-4 그대로), 되묻기는 **접수 해석 축**에서 갈리게(감사 프롬프트 금지 — §7.10 ⛔), 되묻기 턴 테스트(지난 시각 → 질문 / 예 → 카드 / 아니 → 미생성)와 R-1 고정 테스트(15:08 「오늘 15~16시」 → 오늘).
- **THE CONNECT 과거 시작 실처분 dev smoke** 를 Pre-deploy 항목으로 (§7.10 rollout gate).
- **R-1↔R-3 우선순위**(명시 날짜 + 모호 시각, 예: 「9월 3일 3시」): 기존 규칙의 낮 시간대 해석 예시(「3시」=15:00)를 **날짜 무관 동일 적용**으로 §7.10 에 1~2줄 닫아라 — 새 해석 축을 발명하지 말고 기존 예시 축을 일반화하는 것이다. 그 이상이 필요해 보이면 만들지 말고 §5 방식으로 물어라.
- 30-work.md 3자 동기 · log.md wp-add 행(PR 칸 «—»).
- 기존 부채(소유 판정·멱등 가드 owner 부재)는 **범위 밖** — Open Issues 에 기장만.

## 3. 하지 말 것

- 코드 작성 금지. §7.9·모달 경로·회의관리 무개정. 계약 확장 금지. 커밋·push 금지.

## 4. 검증

```
python3 scripts/lint-pipeline.py --strict (리포 루트) → mediness ERROR 0 + WP 3자 일치 통과. 1회만
```

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 다르면 preamble 이 맞다. 한 곳으로만 보내라.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "WP 파일·구성 / R-1↔R-3 닫은 방식 / 3자 동기 / lint"

# (2) 직접 주입
orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --text "[질문] planner: <질문>" --enter`
