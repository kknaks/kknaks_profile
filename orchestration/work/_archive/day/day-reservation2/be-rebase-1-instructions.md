# [backend · 마감] dev 최신 위로 rebase + migration 번호 맞춤

같은 터미널 · 같은 맥락. **이번엔 로컬 커밋 허용(push 금지).** 로컬 스택(11140) 손대지 마라.

1. 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation2` 의 지금 변경 전부(미추적 포함 · `deploy/*.env` · `.venv` · `.local` 같은 gitignored 는 빼고 — `git status` 로 확인)를 **한 커밋**으로: `feat: 예약 등록 · 예약 상세(웹) — 접수 · 상담 · 시술 · 귀가 · 예약 현황 SSE (DAY-SPEC-007)` (+ 끝줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`)
2. `git fetch origin dev` → **`origin/dev`(지금 `e76e27be` — #274 고객 목록 · 차트 · #279 시술현황 차트 · migration `0024_customer_memo` · `0025_visit_photo`) 위로 rebase**. 충돌은 양쪽 기능을 다 살리는 쪽으로(dev 쪽 시술현황 차트 · 고객 차트 동작을 깨지 마라)
3. 우리 migration `0024_purchase_base_price` · `0025_detail_permission` · `0026_visit_discharge_reason` → **`0026_…` · `0027_…` · `0028_…`** 로 번호 · `down_revision` 을 dev head(`0025_visit_photo`) 뒤로 이음. 파일 이름 · revision id · 테스트(`test_alembic` HEAD 등) · 칼럼 스냅샷 같이
4. `scripts/check.sh` 1회 — 실패 0(무관 실패는 이유)
5. 리포트 `be-rebase-1-report.md`(같은 폴더) — 커밋 SHA · 충돌 파일과 처리 · migration 새 번호 · 검사 결과. 완료 보고 두 명령(subject 「backend 완료: rebase 1」 · 이번 dispatch 값)
