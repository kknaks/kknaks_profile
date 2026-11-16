# [reviewer_doc] add1 검수 — DEC-011 · SPEC-008 0.3.0 · WORK-013

같은 reviewer_doc 워커다. 원 브리프(`api-swagger-docs-review-doc-brief.md`) 제약 그대로(read-only · KOS 호출 0 · public grep · 리포트 1개).

- 대상: `10-decision/decision-011-ext-api-add1.md` · `20-spec/spec-008-product-ext-api.md` 0.3.0 의 새 절(§6.6 ~ §6.9 · T32 ~ T44 · 변경 이력) · `30-work/work-013-ext-api-add1.md` · README 행
- 원천: planner 지시 `add1-spec-instructions.md` · `_RESUME.md` §2 2026-11-12 행 · planner 질문 4개 답(Q1 운영 구간×간격 · 행 없는 구역 제외 / Q2 요청마다 slots 1번 → replace_slots / Q3 get-schedules-by-visitor 1번 · reservationId · state 7값 / Q4 오늘 겹침 그대로)
- 코드 기준: `kknaksss/cc-prototype` main `e0e4a16` (코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs` · 읽기만)
- 특히 볼 것: 「목록에 있는 시각이면 정원으로 거절되지 않는다」가 예약 생성 정원 검사와 실제로 같은 규칙인지 · 고객 찾기가 DEC-010 규칙과 같고 404 가 바이트까지 같은지 · 내보내는 칸에 메모 · 의사 이름 · 담당자가 섞이지 않았는지 · KOS 호출 수 · 시험 T 가 모든 오류 갈래를 덮는지 · 기존 0.2.3 계약을 깨지 않는지
- 백엔드 구현이 **병렬로** 이미 시작됐다. FAIL/WARN 마다 「구현자가 무엇을 다르게 해야 하나」를 한 줄로 같이 적어라

산출물: `review-doc-add1.md` (같은 폴더). 판정 PASS / WARN / FAIL. 완료 보고는 원 브리프 §9 두 채널(이번 dispatch 의 taskId · dispatchId).
