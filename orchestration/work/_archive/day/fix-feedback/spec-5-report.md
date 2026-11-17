# spec-5 report — 마감 전 문서 정리

워크트리 `mediness-mediness/fix-feedback-spec` (미커밋 · products/day/ 만)

- **F1** spec-005 「모델 대조」 호출 취소 migration 문장 → 취소선 + 「→ 이번엔 호출 취소 알림을 쓰지 않음 · migration 없음(사용자 2026-11-17 · 다음 스펙)」
- **W1** spec-005:34 `document.hidden` 일 때만 → 취소선 + 「→ 늘(2차 개정 E5)」
- **W2** spec-003:70 ② OQ-62 구절 → 취소선 + 「→ ⑦」
- **W4** spec-002 규칙 38 끝 — 원래 원장 호출 알림 행 · 앱 푸시 그대로 · 그걸로 수락 시 기존 규칙(남은 줄 없으면 `call_closed` · 있으면 남은 줄만)
- **코드 사실** spec-002 스냅샷 `tasks[].systemDoctor` 주석 — 진행중 · 완료 줄에서만 true(be-3 N1 · `board_rules.py` `system_doctor`)

검증: `python3 scripts/lint-pipeline.py --strict` exit 0 (ERROR 0). log.md 는 손대지 않음(문구 정리만).
