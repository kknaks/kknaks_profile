# [reviewer_doc] 스펙 검수 2차

같은 워크트리 · 같은 범위 · 같은 제약(브리프 `day-mobile-v2-review-doc-brief.md`). 읽기만.

- 1차 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-doc-1-report.md`
- planner 2차 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/spec-2-report.md`
- 사용자 답(2026-11-20): 방 복귀 + 점유 띠 앱에 넣음(OQ-A55) · 웹 = OS 알림만(OQ-N19) · kind `doctor_call_cancel`(OQ-N15) · 알림 본문 「{방} · 호출 취소」 — 시술 수 뺌(OQ-N16)

## 할 것
1. 1차 F-1 ~ F-5 · W-1 ~ W-17 각각 닫혔나(파일:줄 확인). 「반영 안 함」 사유가 타당한가.
2. 2차 수정이 새로 만든 어긋남 · 옛 문장 잔재(취소선 없이 남은 반대 문장)를 다시 grep 으로 전수 — 「알림 없음」 · 「401」 · 「시술 {N}건 · 호출 취소」 · 「확인 창」 · 「반이중」 등.
3. 남은 막는 OQ(K18 · 77 · 78 · N17 · A50 · A51 · A59 · A52 · A54)가 기본값으로 코드 착수 가능한가.
4. lint `--strict` products/day ERROR 0.

## 보고
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-doc-2-report.md` · 판정 PASS/WARN/FAIL
- 파일 수정 · 커밋 · Issue 수정 금지. 완료 보고는 dispatch preamble 의 worker_done 그대로.
