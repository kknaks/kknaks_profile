# [reviewer] 코드 검수 — WP1-FE (앱 전역 SSE 연결)

읽기 전용 · 판정(PASS/WARN/FAIL)과 근거만.

- 대상: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify` 의 **`frontend/` 변경 전부**(git diff · 새 파일). ⚠ backend 워커가 `backend/` 에서 WP2-BE 를 쓰는 중 — 이번 대상 아님
- 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/30-work/work-013-notifications.md` 「Phase WP1-FE」 체크박스 · Code Surface WP1 표의 화면 줄 · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-011-notifications.md` §4.1(연결 수명 전부) · `spec-008` §4.4
- 워커 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-wp1-report.md` · 기준선 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-baseline.md` · 서버 실물 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/be-wp1-report.md`

## 볼 것
1. 체크박스 7개가 **코드로** — 특히: 로그인 동안 연결 **하나**(화면 오가도) · CLOSED → `/api/auth/me` 401 이면 세션 상실, 아니면 백오프 새 `EventSource` + `?last_event_id=` · 한 연결 다시 읽기 **한 번**(resync 가 오면 둘째 ready 로 다시 읽지 않음) · 10회 멈춤은 auth 200 + 스트림 실패만 셈 · 5분 느린 재시도 + visibility/focus · (id, 순번) 거름
2. **서버와 맞나** — 사건 이름·필드·`retry`·`ready`·`resync` 사유가 `backend/` 의 실제 구현(WP1-BE)과 같나
3. **조용히 통과하는 자리** — EventSource 대역이 실물과 다르게 굴어 시험만 초록인 곳(닫힘 상태 · 자동 재연결 · 헤더) · 타이머 누수 · 로그아웃 때 연결이 남는가
4. Code Surface 화면 줄을 **네가 grep 해** 다 닿았나 · 회의 WS(`features/meetings/stream.ts`) 무변경 · `src-tauri` 무변경
5. 시험은 관련 파일만(`npx vitest run <파일> --no-file-parallelism` · `npx tsc --noEmit`) — 전체 금지 · 사용자 포트 금지

## 산출물
- `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-wp1-fe-report.md` — §0 판정 · 항목별 · FAIL/WARN(파일:줄 · 고칠 것) · 「사람 눈에 이상해 보일 자리」
- 완료 보고는 앞 브리프 §6 두 명령. subject 「reviewer 완료: WP1-FE 코드 검수 <판정>」 · text 「[worker_done] reviewer WP1-FE 코드 검수 <판정> — FAIL n · WARN n. 리포트 review-wp1-fe-report.md」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
