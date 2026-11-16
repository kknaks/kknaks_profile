# [reviewer_doc] 리뷰 — 스펙 합침(#920 → #921 · merge 67233bf5)

같은 규칙(읽기만 · 수정 · 커밋 · KOS 금지 · 리포트 1개). 대상: 스펙 워크트리 HEAD 67233bf5 — `git diff origin/main...HEAD -- products/day`(지금 PR #921 전체) 중 **merge 로 생긴 것**: 충돌 3(20-spec.md · spec-001 · mobile-deployment) 해소 · spec-000 자동 병합 · 30-work · SPEC-003 개정 ⑥ · SPEC-005 맞춤. 지시: 같은 폴더 `planner-merge-spec-brief.md`.

정본 = `_RESUME.md` §2(⑬ ~ ⑯ · 차트 · 방 이동 · 재호출 결정) — 앱 스펙이 이와 어긋나는 곳.

## 볼 것
1. 충돌 해소가 양쪽 내용을 잃지 않았나(spec-001 is_demo 거르기 없음 + 앱 데모 계정 환경 · spec-000 양쪽 칸 · 목록 · M-18/M-19)
2. 앱 스펙 SPEC-003 · 004 · 005 와 SPEC-002 ⑬ ~ ⑯ 가 서로 반대인 곳(재호출 · 체크박스 · 원장 변경 · 확인 필요 · 마취 · 카드 순서 · 기타 작업 · 차트 JSON 모양 변화 ⑯) — planner 가 남긴 OQ-A32 ~ A36 · N5 근거
3. 스냅샷 · API 계약이 두 스펙에서 한 모양인가(같은 칸 이름 · 뜻)
4. lint --strict products/day ERROR 0

산출물 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-doc-merge921-report.md` · FAIL / WARN / PASS · 「사용자 확인 필요」 표. 완료 보고 두 명령(코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd`).
