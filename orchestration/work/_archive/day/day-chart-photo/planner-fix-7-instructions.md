# [planner] fix-7 — 문서 검수 review-doc-4 W1 ~ W9

**읽을 것**: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/review-doc-4-report.md` W1 ~ W9

**작업 자리**: 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec` — 네 미커밋 변경 위에서. 커밋하지 마라.

## 어떻게 고치나
- 각 W 는 리포트의 「고칠 방향」대로 고친다.
- 결정이 필요한 것(W2 · W3 · W4 · W5 류)은 다음과 같이 적는다.
  - 결정 파일 C22 · C23 의 취지 안에서 고른다.
  - 「기본값(코디)」 + OQ 로 둔다.
  - 결정 파일에 없는 정책을 확정 문장으로 쓰지 않는다.
- 사진 파일 형식(W4)의 기본값은 채팅 첨부가 받는 이미지 형식 · 확장자 규칙과 같게 한다.
- W8: DAY-SPEC-004 의 `before-after` 언급은 지우지 않는다. 사진 쪽은 `beforeAfter` 라는 한 줄을 덧붙인다(취소선 관례).

## 검증 · 보고
- lint `--strict` → `products/day` ERROR 0
- 보고 `planner-fix-7-report.md` + preamble 의 worker_done 두 채널
