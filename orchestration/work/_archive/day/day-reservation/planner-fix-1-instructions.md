# [planner] SPEC-006 고침 1 — 1차 검수 FAIL 1 · WARN 9 반영

너는 앞 판(SPEC-006 draft)을 쓴 planner 다. 맥락이 없으면 먼저 읽어라:
- 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/day-reservation-spec-brief.md` (§5 allowed_paths · §7 금지 · §8 검증 · §9 완료 보고 그대로)
- **결정 파일(갱신됨 — R17 ~ R20 새로 추가 · R1 한 줄 보충)** `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md`
- 검수 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-1-report.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec` (네 미커밋 변경 위에서 고친다)

## 코디 정정 — 브리프 바뀐 곳

- 원 브리프 §1 「기대는 개념 read-side-effect — 조회 경로가 KOS 를 부르거나 DB 를 쓰는 부작용이 없어야 한다」 와 §7 「KOS 새 API 호출 · 새 동기화 회차를 계약에 넣지 않는다」 는 **코디 잘못이었다 — 취소한다.** 사용자 결정 R17: 날짜를 보면 그 날짜를 KOS 에서 가져와 DB 를 최신화한 뒤 DB 를 읽는다. 「조회 부작용 없음 · cc ensure_day 와 다름」으로 쓴 SPEC 문장은 R17 로 뒤집는다(이력 남김 — 취소선 또는 개정 표기)
- 새 테이블 · 칸 · migration 설계 금지 · 화면 문구 짓기 금지는 그대로

## 고칠 것

1. **F-1 → R17 · R18 로 닫는다.** OQ-R02 를 결정으로 닫고 본문(RV-07 · RV-08 동작 · `?date=` · 날짜 조각 · 필터 유지 · 공지 날짜 · 지난날 / 다음 날 회색 케이스)을 R17 기준으로 일관되게. 조회 흐름: 날짜 d 요청 → 그 날 창(병원 현지 d 00:00 ~ d+1 00:00)으로 기존 일정 동기화 경로(`services/emr_sync.py` `run_schedules` 의 `adapter.fetch_schedules(start, end)` → `apply_schedules`) → DB 읽어 렌더. 코드 근거(파일:줄)를 실물로 확인해 적는다. 오늘은 10초 회차가 이미 돈다 — 오늘도 요청 때 다시 가져올지, KOS 실패 · 느림(시간 초과 · 잠금 · `emr/pacing.py` 호출 한도)일 때 화면이 무엇을 보이는지, 같은 날짜 동시 요청 · 회차 잠금과의 관계는 **사실을 적고 OQ** 로(결정 아님 · 기본안은 표시)
2. **W-3 → R19**: 동기화 멈춤 표시 「두지 않는다」를 OQ 로(이번 판 표시 없음 · `record_sync` 근거 사실로)
3. **W-2 → R20**: OQ-R11 닫음 — 그룹 없는 방문은 없다(사용자). 별도 처리 없음. 「그리지 않음 / 맨 끝 열」 선택지 · 케이스 줄 정리
4. W-1 · W-4 · W-5 · W-6 · W-7 · W-8 · W-9 · OQ-R16 한 줄(리포트 「OQ 기본안이 본문에 섞였나」 끝) — 리포트의 「고칠 것」 그대로
5. `20-spec.md` · `10-decision.md` · `log.md` 에 이번 고침 반영(개정 표기)
6. §8 검증(lint --strict · products/day ERROR 0) → §9 완료 보고(preamble 의 taskId · dispatchId)
