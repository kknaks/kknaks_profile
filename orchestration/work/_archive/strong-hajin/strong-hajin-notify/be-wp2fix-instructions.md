# [backend] WP2 검수 손질 — FAIL 1 · WARN 4 · 코드 레포 문서

정본: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-wp2-wp3-report.md` §FAIL · §6 WARN (파일:줄까지 있다).

- **F-1**: `modules/work/assignments.py:253` — W14 `data` 에 `new_assignee_name`(새 담당 `display_name`) · `test_notification_rows.py` W14 단언
- **W-1(서버)**: 합친 슬랙 줄 보낸 사람 수 — `sender_count` 를 따로 올린다(새 이름이 자른 목록에 없으면 +1 · 근사 허용) · 시험
- **W-2**: W29(요청자가 재개) → **담당만** · W30 일 때만 요청자·승격자(`application.py:2241-2245`) · 시험
- **W-3**: `/api/me/badges` 메시지함 점 = 「안 읽은 것이 하나라도 있나」 `EXISTS` 쿼리 하나(같은 `_not_mine` · 읽음 규칙) · 시험
- **W-4**: W11 자료 채택 · 목록 정리도 `_none` 한 번씩
- **코드 레포 문서**(이번 판 allowed_paths 에 더한다): `docs/domain-model.md` 대조표(새 표 `notification_settings` · 알림 칸) · `docs/unified-operations.md:57,85,113` 문구
- 검증 관련만(Makefile 타겟 · 고친 파일) · 금지는 앞 브리프 그대로 · ⚠ frontend 워커가 `frontend/` 손질 중
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/be-wp2fix-report.md` · 완료 보고 앞 브리프 §7 두 명령 — subject 「backend 완료: WP2 손질」 · text 「[worker_done] backend WP2 손질 완료 — <한 줄>. 리포트 be-wp2fix-report.md」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
