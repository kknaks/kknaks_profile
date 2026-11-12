# [reviewer_doc] SPEC-008 0.2.0 · WORK-012 검수 r2

같은 reviewer_doc 워커다. 원 브리프(`api-swagger-docs-review-doc-brief.md`) 제약 그대로(read-only · KOS 호출 0 · public grep · 리포트 1개).

- 대상: SPEC-008 **0.2.0** · WORK-012 · DEC-010(D-16 · D-19 · D-31 고침 · D-35 · D-36 추가 — 사용자 승인으로 Q-A ~ Q-C 답함)
- 지난 리포트: `review-doc-r1.md` — **W1 ~ W13 · 참고 1 ~ 4 · S1 · S5 · 고객 자리(앱 설명 첫 줄)** 가 각각 닫혔는지 하나씩 판정(닫힘 / 덜 닫힘 / 새 문제)
- planner 수정 지시: `spec-fix-r2-instructions.md`
- 새로 생긴 문장(이름 정확 일치 · 1000 상한 · 중복 제거 · IP 제한 · 미들웨어 기록 · 행위자 문자열 겹 · 503 구역 0 · bundlePrice · syncedAt)이 코드 근거 · DEC 와 맞는지
- 코드 기준: `kknaksss/cc-prototype` `c9f30ac`(canonical `git show` 로만)
- 백엔드 구현이 **병렬로** 이미 시작됐다. FAIL 이 있으면 「구현자가 무엇을 다르게 해야 하나」를 한 줄로 같이 적어라(코디가 그대로 전달)

산출물: `review-doc-r2.md` (같은 폴더). 판정 PASS / WARN / FAIL. 완료 보고는 원 브리프 §9 두 채널(이번 dispatch 의 taskId · dispatchId).
