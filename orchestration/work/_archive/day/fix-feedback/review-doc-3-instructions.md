# [reviewer_doc] review-doc-3 — 2루프 스펙(spec-3 · spec-4) 검수 (read-only)

너는 앞 맥락이 없다. 먼저 읽어라:
1. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fix-feedback-review-doc-brief.md` — 역할 · read-only · 검증 그대로.
2. **결정 정본**: `…/fix-feedback/e2e-feedback.md`(F-5 행 · E1 ~ E6) · `…/fix-feedback/_RESUME.md` §2(2026-11-17 행 — 특히 호출 취소 알림은 미룸 · 앱 푸시 미룸 · KOS 호출 취소 없음 → DAY 만 · 알림 늘 띄움 · 차트 = 시술 이름만 + 호버 「차트 작성」 · 바로 시작 줄 「간호관리」)
3. 지시 `spec-3-instructions.md` · `spec-4-instructions.md` · 결과 `spec-3-report.md` · `spec-4-report.md` · 앞 검수 `review-doc-2-report.md` · 코드 검수 `review-code-1-report.md`
4. 코드(읽기만 · 1루프 구현 미커밋 포함): `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback`

리뷰 대상: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec` 미커밋 diff(개정 ㉒ · SPEC-005 2차 · SPEC-003 · 20-spec · log).

## 볼 것
1. 결정 정본의 각 항목이 스펙에 빠짐 없이 · 같은 값으로(파일:줄). 호출 취소 **알림 · 새 알림 종류 · migration 이 계약에 남아 있으면 FAIL**(미룸 결정).
2. 넘침 — 사용자 말 아닌 화면 글자(허용 추가분: 「호출 취소」 · 「간호관리」 · 「차트 작성」).
3. 검수 잔여 D1 ~ D4 · W5 · W6 · W8 반영 · 새 모순.
4. 호출 취소(규칙 38 · 엔드포인트 · 저장 방법 `deleted_at`/`closed_at`)가 코드 사실과 맞고 be · fe 가 이 스펙만으로 지을 수 있나 — 착수 막는 것 표.
5. `python3 scripts/lint-pipeline.py --strict` products/day ERROR 0.

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/review-doc-3-report.md` — 판정 PASS/WARN/FAIL · 지적 파일:줄. 완료 보고는 preamble 의 worker_done.
