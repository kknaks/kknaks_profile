# reviewer_doc r2 — 재검수 지시

planner 가 r1(`review-doc-r1.md`) FAIL 2 · WARN 12 를 반영했다: SPEC-003 0.4.1(부록 F 처분표) · SPEC-004 §3.4 표 한 줄 · WORK-005(끝 「r1 처분」). `_RESUME.md` §2 에 10-23 줄 2개가 새로 들어갔다(시안대로 · 오류 토스트로만 / DEC-005 개정 안 함 · 방향 따라 놓기) — 다시 읽어라.

1. r1 항목 F1 · F2 · W1 ~ W12 각각: 처분이 실제 문서에 들어갔고 맞는지 `파일:줄`로 판정.
2. r2 에서 새로 생긴 규칙(§5.12 놓은 뒤 화면 3초 경합 · 방향 판정 · StrictInt · §9 #0 준비)이 BE/FE 가 따로 구현 가능할 만큼 닫혔는지.
3. 새로 생긴 모순 · 근거 없는 정책.
4. SPEC-004 version · updated_at 을 그대로 둔 것의 적절성(올려야 하면 WARN 으로).

산출물: `orchestration/work/overall-board/review-doc-r2.md` 1개. 맨 위 종합 판정. 보고는 브리프 §9 두 채널(같은 taskId · dispatchId).
