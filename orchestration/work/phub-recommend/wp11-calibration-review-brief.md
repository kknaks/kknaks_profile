# WP-11 보정 실험·48라벨 검수

- 읽기 전용으로 `wp11-semantic-calibration-proposal.md`, `wp11-semantic-calibration-label-candidates.json`, 기존 실제17사례 보고/raw, 앱 의미질문/채점기를 대조한다. 기존17은 관측한 개발집합이고 새48은 source-only 의미 후보이며 calibration24/holdout24다. 외부 임상 사실 인증/배포안전성으로 확대하지 않는다.
- 실제 원문/claim/requirement의 relation/scope/coverage/accept 라벨, source family split 누출, 다중claim/다중source mapping, 반대/조건/시간/개인차 경계를 독립 검토한다. 오라클/fake를 실제 모델 성적으로 보지 않는다. 잘못된 라벨은 구체 ID와 정정안을 보고하되 원본을 수정하지 않는다.
- 최소 prompt/state 투영이 조건/반대문맥을 보존하며 앱 hard gate를 줄이지 않는지, calibration→고정한 단일 후보→미관측 holdout 순서가 유효한지 판정한다. **코디 검토:** 제안의 '문턱은 무조건 .9 이상'과 '라벨러2명+제3검토 의무'는 사용자/정본 요구가 아닌 제안이다. 작은 source-only 개발 실험에서 일률적 .9가 실제 all-hold를 유지한다면 근거없는 제약으로 강제하지 말고 사전 grid를 명시해 calibration에서 정한 뒤 새 holdout으로 검증할 수 있는지 검토한다. 단순 기존17에 맞춘 사후 .43 선택은 금지. 임계값은 의료효능 확률이 아니며 정상/음성 모두에 평가한다.
- PASS/WARN/FAIL·실행 전 고정할 최소사항과 라벨 수정 목록을 `reference/2026-10-30-hub-evals/build-out/wp11-calibration-review.md`에 작성한다. 앱/정본/DB/서비스/라벨 원본 수정·실제 API/batch 호출 금지. Orca worker_done 보고.
