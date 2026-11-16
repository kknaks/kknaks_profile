# WP-10 TypeSafe Noul 계약 검수

- 읽기 전용으로 `SPEC-006.md` 0.3.13 §3-4-1-7 마지막 primitive 정정과 `WORK-012.md` 0.3.13 WP-10 마지막 문단, `para/resources/note/ai/llms.txt`를 대조한다. TypeSafe 공식 `https://docs.typesafe.ai/llms.txt`에서 `primitives`, `primitives/noul`, `patterns/fan-out`, `cookbooks/classifying_rag_passages`, `sdk/python`을 확인한다.
- WP-10 미커밋 코드의 복수 Choice/첫 stop 결함과 30개 실패는 `reference/2026-10-30-hub-evals/build-out/wp10-node-choice-implementation-report.md`가 근거다. 후보별 Noul+답준비 Noul을 한 요청에 넣는 방식이 공식 API/독립 질문 의미와 맞는지, 낮은 관련성·높은 답준비 확률이 필수 target/의료 안전·부재 증명을 우회할 수 없는지, 후보 미선택/불확실/오류 상태와 시험 게이트가 충분한지 판정한다.
- PASS/WARN/FAIL과 **구현 차단 결함만** `reference/2026-10-30-hub-evals/build-out/wp10-typesafe-noul-review.md`에 기록한다. 코드·DB·서비스·원본 문서는 수정하지 않는다. Orca `worker_done` 보고.
