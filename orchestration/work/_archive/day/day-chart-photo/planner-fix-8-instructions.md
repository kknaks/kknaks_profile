# [planner] fix-8 — 사진 파일 형식 (C24-기본값)

**읽을 것**
- 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md` 의 **C24-기본값**
  - JPEG · PNG 둘 다 받는다
  - 확장자는 실제 형식대로 쓴다
- `review-doc-5-report.md` 의 「사용자 확인」 항목

**고칠 곳**: 사진 형식 · 확장자 문장 전부
- SPEC-002 규칙 39 · 매트릭스 · OQ
- SPEC-000 `visit_photo` 키
- 올리기와 KOS 가져오기 둘 다 적용된다
- 형식 밖 파일 = 지금 문장대로 거절 / 건너뜀

**작업 자리**
- 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec`
- 커밋하지 마라

**검증**: lint `--strict` 로 `products/day` ERROR 0

**보고**: `planner-fix-8-report.md` + preamble worker_done 두 채널
