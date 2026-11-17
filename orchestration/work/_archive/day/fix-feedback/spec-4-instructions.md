# [planner] spec-4 — 호출 취소 결정 반영 (작은 판)

너는 앞 맥락이 없다. 먼저 읽어라: 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fix-feedback-spec-brief.md`(역할 · allowed_paths `products/day/` · 제약 · 검증) · 앞 판 `…/fix-feedback/spec-3-instructions.md` · `…/fix-feedback/spec-3-report.md` · 결정 표 `…/fix-feedback/_RESUME.md` §2(2026-11-17 행).

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec`(앞 판 미커밋 위에). 커밋 · push · PR · Delivery 수정 금지.

## 사용자 결정(2026-11-17) — 스펙에 반영

1. **호출 취소 알림은 이번에 안 한다** — 앱 업데이트 뒤로 미룸(심사 중 앱이 모르는 알림 종류 → 배지 어긋남 · migration 피함). 호출 취소 기능(F-5 · 규칙 38 · 엔드포인트)은 **이번에 그대로**. SPEC-005 「알림 행 만들기 — 호출 취소」 · OQ-N14 는 「다음 스펙(앱 업데이트 뒤) — 사용자 2026-11-17」로 옮기고 이번 계약에서 뺀다. 새 알림 종류 · migration 없음. SPEC-002 의 「호출 취소 + 취소 알림」 문장도 맞춘다.
2. **앱 푸시**도 알림과 함께 다음(심사에 영향이 있어서).
3. **KOS 에는 호출 취소 명령이 없다 · 재호출만 있다**(사용자) → 호출 취소는 **DAY 만**(KOS 쓰기 없음). KOS 데스크 화면에 「호출」이 남는 것은 감수(사용자). OQ-68 을 이 결정으로 닫고 KOS 쓰기 표의 「HAR 대기」를 정리.

## 검증 · 보고

- `python3 scripts/lint-pipeline.py --strict` → products/day/ ERROR 0.
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/spec-4-report.md` — 고친 곳 파일:줄. 완료 보고는 preamble 의 worker_done.
