# WP-11 실제 보정·H 결과 독립 검토

- 읽기 전용으로 `reference/2026-10-30-hub-evals/build-out/wp11-calibration-execution-report.md`/execution artifacts와 앱 claim_v1 정책 경로를 검토한다. C48의 사전6grid 선택 t=.60→H24 원래tuple 고정→양성12/12 음성12/12, retry0/72 actual이라는 보고를 raw/selection/H-score/ledger로 대조한다. H후 재선정/expected누출/분모누락이 없는지 확인한다. 신규 API 호출 금지.
- 잔여 H오류3건(number U→C, site U→S, multi_claim coverage T→F)을 source/claim/최종AND·앱 binding과 대조한다. source-only 의미 평가이며 임상 사실 인증 아님. 같은작성자 내부24라 broad성능 승인으로 확대하지 않는다. 완벽한 개별질문 정확도를 새 요구로 만들지 말고 기존 최종 gate와 안전 scope가 실제로 보호하는지 검수한다.
- **사용자 서버 활성화가 아닌 격리 Q002 실험**을 위해 정확한 jev1.14.0/promptko3/t.60/평가fingerprint를 실험정책으로 등록할 근거가 충분한지 PASS/WARN/FAIL한다. 부족하면 구체적 기존 계약 위반만 보고한다. 등록 경로/필요 필드·기본off 유지와 실제 Q002에서 반드시 볼 구조화draft/필수고지/자연어 가독성/최종전달시간을 명시한다. 실제 registry/코드/서버 수정·Q002실행은 하지 않는다.
- 결과 `reference/2026-10-30-hub-evals/build-out/wp11-calibration-result-review.md`, Orca worker_done 보고.
