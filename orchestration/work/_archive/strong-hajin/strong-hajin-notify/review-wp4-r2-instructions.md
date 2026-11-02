# [reviewer] WP4 재검수 r2 — 좁게

앞 판 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-wp4-report.md` WARN 중 코디가 고치기로 한 셋(W-1 · W-3 · W-4)을 frontend 가 고쳤다 — `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-wp4fix-report.md`.
1. **W-1 클릭 중계** — 하나만 보관 · 60초 상한 · 웹 「준비됨」(`shell_info`) 뒤 한 번 · 문서 교체/창 파괴 때 다시 대기 · medi-ax 창 없으면 `REOPEN_MAIN`(트레이 「열기」 와 같은 길) — **경합**(두 클릭 · 준비 전 창 파괴 · 동시에 둘 생성 금지 AC-T33) · 스레드 안전 · 누수
2. **W-4** `target:null` — 셸 검증 허용이 다른 커맨드 검증을 느슨하게 하지 않았나 · 묶음 알림은 그대로 목록
3. **W-3** Windows check 불가(llvm-rc · openssl-sys) — 기록만 확인
4. 회귀 — 고친 파일 주변 · 시험은 관련만
산출물 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-wp4-r2-report.md` · 완료 보고 앞 브리프 §6 두 명령 — subject 「reviewer 완료: WP4 재검수 <판정>」 · text 「[worker_done] reviewer WP4 재검수 <판정> — FAIL n · WARN n. 리포트 review-wp4-r2-report.md」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
