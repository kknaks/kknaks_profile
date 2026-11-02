# [backend] WORK-012 Phase WP3-BE

기존 구현 브리프(`strong-hajin-enhance-be-impl-brief.md`)의 규칙 그대로(allowed_paths · 하지 말 것 · 커밋 금지 · 포트 금지). **WP1 `e51fe3b` · WP2 `e58fb25` 커밋됨** — 그 위에서.

- 할 일: `P/30-work/work-012-enhance.md` **「Phase WP3-BE」 절의 계약 체크박스 전부** + Code Surface WP3 표의 자리 전부(표 밖 같은 심볼도)
- 계약: SPEC-010(AX 회의 생성 · 회의실 셀렉트 · AX 수정 카드 편집 계약 · 옛 meeting.update 합침 · 업무 생성 맥락 목록) · DEC-009
- **먼저** WP2 재검수 WARN 셋(`W/review-wp2-r2-report.md`): **W-r2-2** heartbeat 예외를 잡아 로그만(연장 실패·예외 시험 두 갈래) · **W-r2-3** stdin 없는 옛 호출로 되돌아가는 `TypeError` 낱말 맞추기 제거(시그니처로 좁히거나 되돌이 금지 — 프로세스 이중 실행 방지) · **W-r2-4** `Popen` 에 `encoding="utf-8"`
- WP1 검수 **W-2**(`W/review-wp1-code-report.md`): AX 회의 생성에서 `carried_from_meeting_id` 를 줄 때 그 회의의 미결 안건은 `source:"carried"` — 정책 문장 + 도구 설명 + 시험
- AI 맥락 목록은 WP2 의 `WorkflowApplication.ai_context_catalog` 를 그대로 쓴다(새로 만들지 마라)
- Connect 는 외부 서비스 — 단위·계약 시험은 가짜로, 실물 방 변경 1회는 코디 E2E
- **검증 = 바꾼 부분 관련 시험만**(전체 make test · make verify · 프론트 전체 vitest 금지 — 마지막에 코디가 한다). 돌린 시험 파일 목록과 수치를 리포트에
- 리포트: `W/be-wp3-report.md` · 완료 보고: 기존 브리프 §7 두 명령(subject 「backend 완료: WP3-BE」). **코디handle = term_367ca23a-f846-44c0-afc7-07b6655df214**
