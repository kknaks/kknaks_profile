# [reviewer] 코드 검수 — WP1-BE (사건 채널 SSE)

앞 판에서 SPEC·WORK 를 검수한 그 reviewer 다. 이제 **코드 검수**다. 읽기 전용 · 판정(PASS/WARN/FAIL)과 근거만.

- 대상: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify` 의 **작업 트리 변경 전부**(`git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify status` · `git diff` · 새 파일) — backend 만. (frontend 워커가 `frontend/` 에서 WP1-FE 를 병렬로 쓰고 있다 — 이번 검수 대상 아님)
- 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/30-work/work-013-notifications.md` 「Phase WP1-BE」 체크박스 · Code Surface WP1 표 · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-011-notifications.md` §4.1 · `spec-008` §4.4
- 워커 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/be-wp1-report.md` · 기준선 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/be-baseline.md`

## 볼 것
1. 체크박스 8개가 **코드로** 지켜졌나(리포트를 믿지 말고) — 특히 이어 받기(머리 > 쿼리 · 겹침 창 60초 · 기준 줄 대체 · 200 넘침 → resync · **구독 먼저 걸고 DB 읽기** · 같은 순번 한 번) · 큐 넘침 resync · 401/403 · 20초 ping · `X-Accel-Buffering`
2. **조용히 통과하는 자리** — 시험은 초록인데 계약이 깨진 곳(빈 단언 · 폴백 · 개명)
3. Code Surface WP1 표의 자리를 **네가 grep 해** 다 닿았나 · 옛 WS 라우트가 남았나 · 회의 WS 안 건드렸나
4. 마이그레이션 SQL 3파일(운영 적용 순서 · CONCURRENTLY · 되돌리기) · 시퀀스 · schema_sync — 운영 DB 에 안전한가
5. 워커 미결 1 — **운영 인벤토리 drift 시험이 `http_events.py` 를 안 읽는다.** 코디 판단: 시험의 파일 목록에 `http_events.py` 를 더하는 쪽이 맞다고 본다 — 동의/반대 근거
6. 시험은 **관련 파일만** 돌려도 된다(`make test-contract-serial FILES="…"` · 별도 PostgreSQL) — 전체 스위트 금지 · 사용자 포트 금지

## 산출물
- `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-wp1-be-report.md` 하나 — §0 판정 · 항목별 · FAIL/WARN 목록(파일:줄 · 고칠 것)
- 완료 보고는 앞 브리프 §6 두 명령. subject 「reviewer 완료: WP1-BE 코드 검수 <판정>」 · text 「[worker_done] reviewer WP1-BE 코드 검수 <판정> — FAIL n · WARN n. 리포트 review-wp1-be-report.md」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
