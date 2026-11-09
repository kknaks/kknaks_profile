# [backend] Delivery #230 — 시술 현황 1차 ① 백엔드 (DAY-SPEC-002)

너는 day backend 워커다(#226 · #227 을 만들었다). 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/backend/`(테스트 규칙 2026-11-06). 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` — #224 ~ #229 커밋 위에 이어서(PR #228 하나).

## SSOT
- **계약 = Issue #230**(contract v4 · 곧 v5 — 아래 「전체 권한 계정」 추가분) `gh issue view 230 -R MediSolveAIDev/CENTURION_DAY` · 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-delivery230-231-report.md` · `review-delivery230-231-v2-report.md` · `review-login-board-v-report.md` · `review-login-board-v-fix-report.md`.
- **정본 = DAY-SPEC-002** `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/20-spec/spec-002-procedure-board.md`(PR #909 `c61885a7`) · SPEC-000 · SPEC-001 · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md`(U1 ~ U12 · OQ · W6 · 의사 호출 창).
- 본: cc-prototype `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:procedure/back/app/<...>`(domain/rules.py · service/board_service.py · api/board.py · kos/ops.py · kos/sync.py) · KOS HAR(main 체크아웃 · gitignore) `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-10-12-cc-prototype/*.har` — 경로 · 칸 이름만.
- #229 웹 기반(매크로 · base.html · web_errors · CSRF) 은 이미 있다. **#231(화면 템플릿)이 기댈 조각 계약 표**(라우트 · 조각 이름 · 넘기는 값 · SSE 이벤트 · 토스트)를 계약 A9 대로 리포트에 남긴다 — 템플릿은 자리만(#231 몫).

## 정해 둔 것
- **전체 권한 계정**(사용자 2026-11-06 · 원천 `erd/04-staff.md`): env `DAY_ADMIN_EMAILS` 의 계정은 `job_role_permission` 과 관계없이 모든 권한 — 권한 검사 한 곳 · 로그 표시. `deploy/local.env.example` 에 **이름만**. **`deploy/local.env` 에 값을 넣지 마라 — 사용자가 직접 넣는다.** 권한 표 시드는 만들지 않는다.
- **KOS 쓰기**: (경로 + 값) 단위 · HAR 확인된 값만 연다 · HAR 미확인 동작(귀가 대기 · 시작 취소 · 완료 취소 · 재호출 재전송)은 KOS 쓰기를 닫고 DAY 만 동작(W6). #226 W7 outbox 구멍 · `(visit_id, seq)` 유일 migration.
- **실제 KOS 쓰기 실물은 하지 마라** — 사용자 허락 뒤 · 데모 지점만(계약). 이번 실물 확인은 **조회 · DAY 쪽 동작 · outbox 적재까지**(가짜 어댑터 또는 쓰기 닫은 상태). 데모 원장 계정(W8)은 없다 — 수락 실물은 미룬다.

## 하지 말 것
#231 화면 템플릿(자리만) · 앱 · 방 옮기기 · 차트 작성 · 명동점 키 · KOS 쓰기 실호출 · 커밋. **compose 는 사용자가 http://127.0.0.1:11040 을 보고 있다 — down 하지 말고, 끝나면 `--profile app up -d --build api worker scheduler` 로 새 코드만 다시 올려라.**

## 검증 · 보고
`uv run pytest -m "not infra"` · `scripts/test.sh -q` · ruff 두 수치 · 실물(데모 지점 조회 · DAY 동작 · SSE 신호 1회) · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-230-report.md` — 계약 Acceptance 증거 · **조각 계약 표** · 열린 쓰기 표(경로 + 값) · 남은 것. 완료는 preamble 의 worker_done 절차대로(둘 다).
