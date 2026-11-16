# WP-11 평가 준비 P2-01/02 수정

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현 미커밋 WP-11. `reference/2026-10-30-hub-evals/build-out/wp11-code-review.md` P2-01/P2-02와 17라벨 표를 기준으로 수정. claim_v1 기본off/빈 policy registry 유지, 실제 API/provider/Hub/judge/batch 호출 금지.
- scope 질문의 적용/한정조건 보존 정의에 맞게 ko-delayed-time-deleted/ko-individual-deleted expected.scope=false. relation의 부분 명제 지지와 coverage 전체 의무 보존을 명시한다. ko-certainty의 source에 보장 부정을 명확히 하거나 의미 관계 정답을 명확한 한 값으로 확정하고 이유 기록. ko-instruction-data는 감염시 농양 부정을 직접 주장하는 형태로 명료화. 다른 라벨도 동일 정의로 확인하되 모델 응답을 보고 정답을 바꾸는 데이터 누출 금지.
- scorer가 최종 accept만 아니라 relation 혼동표/정확도, scope·requirement key별 coverage 정답/관측/오류, raw probabilities/confidence/Noul·threshold를 남기게 한다. 한 gate가 막았더라도 다른 gate의 오판을 집계한다. 리뷰의 ko-negation relation/scope 오판+coverage거부 재현이 상세 오류로 드러나야 한다. 여러 requirement/candidate claim도 키별 expected 지원. 누락/unknown/duplicate/hash/model 오류와 분모 유지.
- prepare는 정답 없는 model request artifact(state/questions/input/model/prompt hash)와 expected label artifact를 분리한다. 실제 실행기가 expected를 전송할 경로를 없애고 raw response/usage/model과 요청hash를 별도 보존할 수 있게 한다. 작은 API 실행 도구가 필요하면 준비하되 이번에 호출하지 않는다.
- 신규 회귀/기존 suite/Ruff/diff PASS, 17개 수정 라벨/의미정의와 blind artifact/hash를 보고한다. fake oracle은 연결 검증만. `reference/2026-10-30-hub-evals/build-out/wp11-eval-prep-fix-report.md` 작성 후 Orca worker_done. Hub/DB/서비스/정본·커밋/푸시/PR 변경 금지.
