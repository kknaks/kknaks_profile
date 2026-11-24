# [reviewer_doc] 재검수 2 — planner fix-1 반영 확인

맥락이 없으면 읽어라: 원 브리프 `day-chart-photo-review-doc-brief.md` · 네 1차 리포트 `review-doc-1-report.md` · planner 지시 `planner-fix-1-instructions.md` · 보고 `planner-fix-1-report.md` (모두 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/`) · 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md` — **C17 · C17-기본값이 새로 들어왔다(사용자 결정 · 다시 열지 않음)**.
워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec` read-only · `git diff origin/main`.

## 볼 것
1. W1 ~ W9 가 지시서의 기본값대로 닫혔는지(절:줄)
2. C17 반영 — 저장 전 KOS 확인 · 하나라도 다르면 탭 전체 저장 0(이력 · outbox · event 0) · 걸린 줄 = KOS 글 + 줄바꿈 + 요청 글 · 담당자 KOS 값 · 안 걸린 줄 그대로 · 토스트 · 다시 저장 = 같은 확인 · KOS 읽기 실패 = DAY 사본만. 「걸린 줄만 빼고 저장」 문장이 살아 있지 않은지 전수 grep
3. 코드 워커가 되묻지 않을 만큼 닫혔는지 — 「연 때 값」 비교 기준 · KOS 읽기 경로 · 응답 모양(200/409 · 무엇을 싣나) · 새 OQ-90 ~ 92 중 착수를 막는 것에 기본값이 있는지
4. 새로 생긴 어긋남 · 발명 · 금지 위반(원 브리프 §7) · lint

리포트 `review-doc-2-report.md`(같은 폴더) — 판정 · 지적 파일:줄 · 근거. 레포 수정 · 커밋 금지. 완료 = preamble 의 worker_done 두 채널.
