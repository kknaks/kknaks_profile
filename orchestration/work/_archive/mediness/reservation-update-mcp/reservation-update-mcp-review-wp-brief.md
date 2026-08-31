
# [reviewer_spec] 검수 R2 — WP-126 (update MCP 툴 + 시각 해석 착지 작업서) + §7.10 R-1↔R-3 bullet

너는 **mediness `reviewer_spec` 워커**다. R1 에서 네가 PASS(WARN3) 를 준 스펙이 정정·승인됐고, planner 가 WP-126 을 썼다. **WP 와 이번 라운드 추가분만** 검수한다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/reservation-update-mcp-spec` (미커밋 4파일 수정 + WP 1 untracked, +108/−7 — read-only)

## 1. 먼저 읽을 것

- `products/mediness/30-work/work-126-reservation-update-mcp-time-resolution.md` ← 검수 대상
- `git diff` 중 이번 라운드 추가분 — §7.10 R-1↔R-3 bullet · 30-work.md 3자 동기 · log 행 (직전 라운드 정정분은 네가 이미 봤다)
- 네 R1 리포트: `.../work/reservation-update-mcp/review-spec-report.md` — WP 몫으로 넘긴 것들
- 코드 대조 (mediness-app read-only): `mcp/app/tools/reservation_cancel_request.py` · `mcp/app/server.py` · `mcp/tests/test_tool_inventory.py` · `back/app/services/action_runtime/chat/provider.py`

## 2. 판정할 것

1. **계약 확장 0** — WP 작업 항목이 SPEC-151 §6.2b·§7.10 밖의 동작을 만들지 않는가. §7.9·모달 무개정 주장대로인가.
2. **R-1↔R-3 bullet** — 「다른 축이라 함께 걸린다(R-3 는 시각만·날짜는 R-1)」가 기존 R-3 예시와 정합인가. 새 해석 축 발명이 정말 0 인가.
3. **코드 좌표·실측 주장** — cancel 동형 표본 좌표, server.py 등록·오염 등급 fail-fast, 인벤토리 «착지 시점 실측 +1» 방침(표 57 vs 코드 61 드리프트 주장 포함)이 실코드와 맞는가.
4. **테스트 계획 충분성** — P1 6케이스 + P2(R-1 고정·되묻기 3분기·R-3/R-4 무회귀·무조건 제약 문자열 부재 단언)가 §7.10 계약을 실제로 무는가. 빠진 분기 없나.
5. **3자 동기·번호** — Board/WP List/Coverage 등재, doc_no 246·WP-126 유일성 (⚠ 타 세션이 같은 번호로 작업한 이력이 있다 — origin 기준 유일성 확인).
6. lint --strict 1회 (리포 루트) — mediness ERROR 0.

## 3. 산출물 — 리포트 1개

`/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/reservation-update-mcp/review-wp-report.md`

- 판정(PASS/WARN/FAIL) + 항목별 근거. 리포 파일 수정·생성 금지.

## 4. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 다르면 preamble 이 맞다. 한 곳으로만 보내라.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "reviewer_spec 완료: <판정 한 줄>" \
  --body "판정 / 항목별 근거 / 위반 목록"

# (2) 직접 주입
orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a \
  --text "[worker_done] reviewer_spec WP 검수 완료 — <판정>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --text "[질문] reviewer_spec: <질문>" --enter`
