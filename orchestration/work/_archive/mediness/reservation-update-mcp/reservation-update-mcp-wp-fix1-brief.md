
# [planner] 정정 R2 — WP 재번호(126→128) + WARN 3건 (W-2 중요)

너는 **mediness `planner` 워커**다. WP-126 검수가 WARN 4(FAIL 0) 다. 아래만 고친다.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/reservation-update-mcp-spec` (네 미커밋 변경 위에서 계속)

기준: `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/reservation-update-mcp/review-wp-report.md` W-1~W-4

## 고칠 것

1. **W-1 (PR 전 필수)** — **재번호: MEDINESS-WP-126 → WP-128 · DOC-246 → DOC-248**, 파일명 `work-128-reservation-update-mcp-time-resolution.md`. 사유: `origin/task-redesign-spec` 브랜치가 WP-126/DOC-246 을 이미 푸시했고(파일명 달라 git 충돌 안 잡힘 — 머지 후 lint doc_no 유일성 ERROR), origin 전 ref 스캔상 127/247 도 점유라 다음 빈 쌍이 128/248 이다. 30-work.md 3자리·log.md·Coverage·문서 내 자기 참조 전부 함께 갱신.
2. **W-2 (중)** — P2-A 의 삭제 대상에 `'from now'` 상대 구절도 포함시켜라. 'must start in the future' 만 지우고 'from now' 를 남기면 날짜 명시 요청에서 R-1↔R-3 를 규칙이 안에서 되돌린다 — WP 자신이 진단한 실패 모드 그대로다. (규칙 재작성 결과물이 now-상대 해석을 «날짜 없는 요청» 한정으로 명시하게.)
3. **W-3** — 검증 항목 3건 추가: ⓐ 되묻기 질문의 사실 2개 포함 검증 ⓑ 「감사가 되묻기를 억제하지 않는다」 회귀 테스트 ⓒ **명시 날짜+모호 시각이 «둘 다 지난» 조합**(21:57 「오늘 3시」) — 새 결정이 아니라 기존 규칙의 합성으로 닫아라: R-3 가 시각(15:00)·R-1 이 날짜(오늘) → 완전히 지남 → R-2 되묻기. 규칙 표 합성 예시 1줄 + 테스트 1케이스.
4. **W-4 (저)** — 「P1 6케이스」 라벨을 실제 개수로 (또는 개수 표현 제거 — 지난 라운드 교훈대로 **개수 안 세는 표현 권장**).

## 하지 말 것

- 위 외 개정 금지. 계약(R-1~R-4·등재) 무변경. 커밋·push 금지.

## 검증

```
python3 scripts/lint-pipeline.py --strict (리포 루트) → mediness ERROR 0 · doc_no 유일성 통과. 1회만
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
  --body "4건 처리 / lint"

# (2) 직접 주입
orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_ea94ccc7-bf43-455a-bb8a-65b34d92448a --text "[질문] planner: <질문>" --enter`
