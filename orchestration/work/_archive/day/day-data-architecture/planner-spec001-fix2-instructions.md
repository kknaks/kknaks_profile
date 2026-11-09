# [planner] SPEC-001 검수 WARN 반영 + SPEC-000 token_hash · OQ-04-1 (사용자 결정 2026-11-05 — 전부 추천대로)

너는 day planner 워커다. 계약은 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/day-data-architecture-spec-brief.md` 그대로. 같은 워크트리(PR #909 · 미커밋 SPEC-001 위).
읽을 것: 검수 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-spec001-report.md`(W1 ~ W4) · **바뀐 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/04-staff.md`** — `login_session.token_hash` 칸 추가 · 「정할 것」1 닫힘 · 새 절 「로그인 · 세션 계약 (2026-11-05 사용자 결정 — DAY-SPEC-001)」.

할 일:
1. **SPEC-001** 을 원천 새 절에 맞춘다:
   - W1 a ~ f 그대로 확정(경로 `/api/auth/hospital` · `/api/auth/logout` POST · `staff_inactive` · `unauthorized` · `forbidden` · KOS 403 → `kos_unavailable`). **W1 g: 로그아웃된 세션 = `unauthorized`**(`session_expired` 는 만료만).
   - W2: 형식 검사는 KOS 에 맡긴다 — 그대로(근거 = 사용자 결정). 2단계 인증 안내 문구는 「예시」로 표시.
   - W4 · 「아직 열린 것」 닫기: 세션 토큰 = 따로 만든 무작위 토큰 · DB 엔 `token_hash` / 처음 만든 `account.is_active` = true / KOS 호출 시간 제한 15초 / 비활성 판정 = 기준 정보 동기화 `get-accounts.activate` → `staff.is_active` / 병원 여럿이면 임시 토큰(5분) → 병원 고르면 진짜 세션, 하나면 바로 세션.
   - 「아직 열린 것」이 비면 절을 「없음」으로.
2. **SPEC-000**: §3 04 `login_session` 표를 원천대로 다시 옮긴다(`token_hash` 행) · OQ-04-1 에 「→ 정함: DAY-SPEC-001 OQ-6(1차는 막기)」. `40-architecture/erd.md` 핵심 키에 `login_session.token_hash` UNIQUE 가 빠지면 더한다.
3. `log.md` 한 줄 · lint `--strict` 1회.

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec001-fix2-report.md`. 완료는 preamble 의 worker_done 절차대로.
