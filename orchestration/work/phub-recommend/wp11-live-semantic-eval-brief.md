# WP-11 고정 한국어 17사례 실제 Jev 평가

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현재 코드와 `reference/2026-10-30-hub-evals/build-out/wp11-eval-prep-fix-report.md`/artifacts를 사용한다. 17개 라벨/질문/정책은 모델 결과 보기 전에 동결됐고 코디가 수정 보고와 신규11tests PASS를 확인했다. 기존 사용자 작업은 전체 실물 검증까지 승인돼 있으며 **이번에는 실제 Jev API의 17사례 평가만** 수행한다.
- blind-requests.json만 모델 실행 입력으로 읽는다. expected-labels/fixture expected는 모델 state/questions에 보내지 않는다. candidate-policy의 model/prompt/threshold를 변경하지 말고 모델 실제 버전을 기록한다. API는 앱 기존 client/env를 사용하되 키/인증값 출력·저장 금지. 입력 hash·모델·질문 일치 확인, 17논리 사례 각각1회(기존 SDK 물리 retry는 별도 기록), 실패/누락은 분모에 남긴다. 무제한 재시도/결과 보고 threshold 튜닝 금지. 새 eval 실행기가 필요하면 build-out 한 파일로 만들고 평가 코드는 수정하지 않는다.
- 실제 원응답/choices/nouls/probabilities/confidence/model/usage·latency/input/prompt hash를 별도 immutable artifact로 보존한다. 그 뒤 동결 scorer로 최종 false accept/reject·severe 오승인, relation 혼동표·scope/requirement coverage 오류·보류/누락을 모두 집계한다. fake oracle artifact와 실제 응답을 혼동하지 않는다.
- 17개(양성4·음성13)는 작은 탐색 평가이며 broad 의료정확성 증명이 아니다. 특히 위험/조건/확실성/반대 출처 음성 오승인 하나라도 있으면 활성화 차단으로 보고한다. 전부 통과해도 자동 정책 등록/기능활성화/Q002 batch는 하지 않는다. 검토 가능한 결과만 만든다.
- Hub/DB/사용자 포트·컨테이너·앱 소스·policy registry·라벨/threshold·커밋/푸시/PR 변경 금지. `reference/2026-10-30-hub-evals/build-out/wp11-live-semantic-eval-report.md`와 raw/score artifact에 기록하고 Orca worker_done 보고.
