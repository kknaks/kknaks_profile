
# [planner] 마이크로 정정 — 검수 WARN 3건 (판정은 PASS · 이것만)

너는 **mediness `planner` 워커**다. 네 산출물이 검수 PASS(WARN 3) 를 받았다. 아래 3건만 고친다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/reservation-update-mcp-spec` (네 미커밋 변경 위에서 계속)

기준: `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/reservation-update-mcp/review-spec-report.md` 의 W-1·W-2·W-3

## 고칠 것

1. **W-1 (중)** — §7.10 의 「규칙의 침묵」 진단 정정: 현행 `TIME_RESOLUTION_RULE` 에 'A reservation must start in the future' **무조건 제약이 이미 있다.** 진단을 「빈 자리에 추가」가 아니라 「**기존 문장 삭제·재작성**」으로 바꿔, 구현자가 그 문장을 존치한 채 R-1 을 얹는 충돌 경로를 막아라.
2. **W-2 (저)** — date 거절 서술 정밀화: 무조건이 아니라 **값이 바뀔 때만** 422 (동치 날짜는 통과 — surface.py:570).
3. **W-3 (저)** — 되묻기 «기제» 지목 정정: 워크플로를 고른 턴은 최종 답변 감사에 도달하지 않는다 — 출구(최종 답변)와 결정 자리를 분리해 재서술.

## 하지 말 것

- 위 3건 외 개정 금지. 계약 내용(R-1~R-4·등재) 무변경. 커밋·push 금지.

## 검증

```
python3 scripts/lint-pipeline.py --strict (리포 루트에서) → mediness 범위 ERROR 0. 1회만
```

## 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 다르면 preamble 이 맞다. 한 곳으로만 보내라.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context 에 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context 에 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "3건 처리 / lint 결과"

# (2) 직접 주입
orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --text "[질문] planner: <질문>" --enter`
