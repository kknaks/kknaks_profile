# [reviewer] 코드 검수 — WP2-BE(+ WP1 손질) · WP3-FE · **서버↔화면 맞춤**

읽기 전용 · 판정(PASS/WARN/FAIL)과 근거만.

- 대상: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify` 작업 트리 — `backend/` 전부 · `Makefile` · `docs/unified-operations-inventory.json` · `frontend/src/`(WP3 화면). ⚠ frontend 워커가 **WP4-SHELL**(`frontend/src-tauri/` · `frontend/src/lib/shell.ts` · OS 알림 생략/묶음)을 지금 쓰고 있다 — **그 자리는 이번 대상 아님**
- 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/30-work/work-013-notifications.md` 「Phase WP2-BE」 · 「Phase WP3-FE」 체크박스 · Code Surface WP2·WP3 표 · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-011-notifications.md`(v0.2.3) §2 · §4.2~§4.5 · §4.7(백필) · `spec-008`(v0.7.0)
- 확정 시안: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/reference/2026-09-10-sc-meeting/package 2/Alerts.html` · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/reference/2026-09-10-sc-meeting/package 2/handoff/alerts/` · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/reference/2026-09-10-sc-meeting/package 2/handoff/settings/js/`
- 워커 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/be-wp1fix-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/be-wp2-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-wp3-report.md`(**§6 서버와 맞춰 볼 자리 8**)
- 앞 검수: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-wp1-be-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-wp1-fe-report.md`

## 볼 것
1. **서버↔화면 맞춤 — 최우선**: `fe-wp3-report.md` §6 의 8 자리를 실제 `backend/` 와 `frontend/src/` 로 대조 — 항목 모양(§4.5-2) · 경로 · 응답(`{items, next_cursor}`) · `data` 칸 이름(화면이 가정한 것 전부) · `read-all` 빈 본문 · 설정 PUT/409 · `target` · `notification.read` 사건 모양 · SSE `notification` 사건 모양 · 숫자 아닌 `Last-Event-ID` = 첫 연결(backend 정정 — 화면이 아는가). **다른 곳마다 SPEC 이 맞는 쪽을 가리켜라**(고칠 쪽 · 파일:줄)
2. WP2-BE 체크박스 16 · WP3-FE 6 이 **코드로** — 사건 × 관계 68행이 생성기에 다 있나(표본 아니라 전수 — 행 id 로) · 원칙 ①②③ + 예외 · 관계 우선 · 슬랙 합침 · 설정 거름 · 옛 생성 흡수(`.emit(` 0) · `from_me` 셋 · 슬랙 안 읽음 버그 · 메시지함 읽음 → 알림 읽음 · meeting_worker 게시
3. **코디가 정한 것 확인**: W17·W24·W30 은 지금 권한상 늘 0줄 — 코드 자리는 남기고 권한은 안 넓힌다(코디 결정). 그 근거가 맞나(정말 0 줄인가 · 시험이 고정하나)
4. **조용히 통과하는 자리**: 빈 단언 · 대역이 실물과 다른 곳 · 폴백 · 시험만 초록
5. **운영 안전**: `2026-10-08-notifications-v2.sql`(WP1+WP2) · 인덱스 CONCURRENTLY · 옛 종류 바꾸기 · 카톡/메일/슬랙 백필 SQL 두 걸음(`apply=0` → 판단 → `apply=1`) · **실명이 SQL·시험·코드에 없나**(grep) · `actor_member_id` NOT NULL 채우기 · `/api/me/badges` 의 메시지함 셈 무게
6. 시안 일치(화면) — 항목 16 · 꼬리표 16 · 상태 넷 · 사이드바 점 둘
7. 시험은 **관련 파일만**(Makefile 타겟 · 고른 vitest) · 전체 금지 · 사용자 포트 금지

## 산출물
- `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-wp2-wp3-report.md` — §0 판정 · §1 서버↔화면 맞춤 표(자리 · 서버 · 화면 · SPEC · 고칠 쪽) · 항목별 · FAIL/WARN(파일:줄 · 고칠 것 · **backend/frontend 어느 워커 몫인지**) · 사람 눈에 이상해 보일 자리
- 완료 보고는 앞 브리프 §6 두 명령. subject 「reviewer 완료: WP2·WP3 코드 검수 <판정>」 · text 「[worker_done] reviewer WP2·WP3 코드 검수 <판정> — FAIL n · WARN n. 리포트 review-wp2-wp3-report.md」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
