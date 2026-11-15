# planner 수정 1차 — reviewer_spec WARN 6건 반영

리뷰 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/work/llm-codex-hotfix/review-spec-report.md` 의 「경미 (WARN)」 1~6 을 **권장 수정 그대로 전부** 반영한다. 다른 곳은 건드리지 않는다.

1. WP-133 Open ③ + 결과 파싱 표 C 행: 「lint FAILED」 → 「lint 는 통과하고 펜스·머리말 섞인 본문이 조용히 발행될 수 있다」. Phase 3 C 수용에 「`markdown_body` 가 `# 📋 메디솔브 브리핑` 으로 시작하고 펜스·머리말 없음」 추가.
2. `spec-070-briefing.md:414` → 「LLM submit 1회 (codex · 시간 상한 600s · mediness MCP 4 read-only tool 노출)」.
3. WP-133 Phase 2: 깨질 기존 테스트 3파일(리포트 WARN-3 목록)을 명시하고, 「claude 설정을 명시(settings override)해 claude 분기 회귀 테스트로 보존, codex 단정은 신규」 한 줄.
4. WP-133 Phase 3 수용 수단 못박기: B = `recommend_with_ai` 경유(`back/scripts/eval_decision_gate.py` 1건 또는 Slack 멘션 1회) · C = 다음 06:00 정기 run 우선, 수동은 `back/scripts/brief_backfill.py` · D = `weekly_report_pipeline._default_ai_call` 을 W47 실데이터 1버전 프롬프트로 파드 내 1회 호출(admin 재생성 금지 — W47 draft archive 위험). 이에 맞춰 Pre-deploy 의 W47 재생성 확인 문구 정리.
5. WP-133 Phase 1: 「compose 후 최종 프롬프트 바이트 로그(B·C·D 공통)」 추가 — Open ② 는 첫 실호출 로그로 닫는다고 연결.
6. `spec-070-briefing.md:366` 「실패 축이다.」 뒤 문장 분리.

검증: `python3 scripts/lint-pipeline.py --strict` ERROR 0. 완료 보고는 원 브리프 §9 와 같은 두 채널(같은 taskId/dispatchId 로 다시 보내도 됨 — 안 되면 terminal send 만).
