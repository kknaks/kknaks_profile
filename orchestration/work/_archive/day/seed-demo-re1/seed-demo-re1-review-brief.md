# [reviewer] 데모 시드 스크립트 리뷰 — 「방 배정」 기본 · 한국어 이름 · 상담 양식 메모 · 시술 4 ~ 6개

너는 **day `reviewer` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 rules · skills · tools · workflow).

작업 워크트리(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/seed-demo-re1` — 미커밋 `scripts/seed_demo_board.py` · `backend/tests/scripts/test_seed_demo_board.py`

## 기준
- 브리프(정본): `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/seed-demo-re1/seed-demo-re1-be-brief.md` 2절 1 ~ 5 · 7절
- 워커 보고: `orca orchestration inbox --json` 의 backend worker_done(seed-demo-re1)

## 볼 것
1. 모든 방문에 「방 배정」 기타 작업(설정 id → 없으면 제목 → 없으면 멈춤) · 방 붙임
2. 이름 한국어 가짜(실제 인물 · 유명인 이름 없음 · `[TEST]` 없음) · 국적 KR 기본
3. 오더 메모가 브리프 양식 줄 순서 그대로 · 시술 줄 = KOS 에 실제로 들어간 시술 제목(반영 지연 대기)
4. 시술 4 ~ 6 무작위 · 수납 흐름 그대로 반복 · 금액 · 트랜잭션 맞음
5. 데모 테넌트 가드 · dry-run KOS 쓰기 0 · 출력에 이름 · 전화 · 생년월일 없음 유지
6. 제품 코드 · migration 변경 없음 · 시험이 위를 판정

## 하지 말 것
- 코드 수정 · KOS · 서버 쓰기 금지. 시험은 관련 파일만 1회(`cd backend && uv run pytest -q tests/scripts/test_seed_demo_board.py` · ruff). 사용자 포트 · 프로세스 금지.

## 완료 보고 — 문구 변경 금지
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/seed-demo-re1/review-1-report.md` (PASS / WARN / FAIL · 파일:줄)
```bash
orca orchestration send --to term_e62e850f-aae8-4092-a945-6f9406c2af07 --from term_6e4dab46-3a94-4e3b-95c4-5a3aef91cf78 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "reviewer 완료: <한 줄>" --body "<판정 · 지적>"
orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 --text "[worker_done] reviewer 시드 리뷰 — <판정>. 상세는 인박스." --enter
```
