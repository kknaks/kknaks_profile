# WP-11 검증된 실험정책의 격리 Q002

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현 코드와 `wp11-calibration-result-review.md` PASS/등록필드·fingerprint를 사용한다. 사용자 전체 작업의 Q002 실물 검증 권한에 따라 **이번 격리 Q002 한 문항 실행을 승인**한다. production rollout/사용자 서버 활성화 승인이 아니다.
- 앱소스/공유env/기본registry/Settings는 수정하지 않는다. build-out harness의 **실험 프로세스 메모리**에만 SemanticPolicy version=`wp11-q002-experiment-jev1140-ko3-t060`, modeljev1.14.0/promptclaim-v1-ko-3-candidate/네문턱.60/evaluation_id+실제sealhash를 등록하고 해당 프로세스의 coverage I-01 CLI claim_v1만 opt-in한다. 등록 전에 reviewer의 평가fingerprints·코드입력hash를 확인, 다르면 중단보고. 편의를 위한 검증 우회/테스트 fake policy 주입 금지. 실제 평가 근거로 만든 정책 그대로 실행한다.
- 빈18015 본인 격리 Hub health/db/raw21/21/Gold567677edfe7123e9 확인, 사용자Hub18005/앱18210/DB발행포인터·컨테이너 비조작. Q002 case3 claude-cli 한 문항 새 label, 기존 생성예산/수정최대2회/deadline 유지. 실제 SDK모델/timeout/retry/물리시도 관측 가능 여부를 기록한다. 전송 전 정책/hash 불일치면 호출하지 않는다.
- 실제 draft/manifest/source-context/모든 relation/scope/coverage·번호표/span/환자답을 보존한다. 필러 역할·primary risk·8고지/한정 의미 유지, 여섯갈래 정확보류·자료없음단정부재, 자연스러운 한국어/내부ID·원문덤프·정의없는수치·중복을 각각 판정한다. 독립 judge 안전/정확성/불확실성/관련성과 **별도 가독성 검토**. 실패시 코드/prompt/문턱 변경·추가실행 금지.
- schema_v2 model_first_text/generation_returned/final_validation_completed/on_text시작완료/case_completed/status/hash/단일시도, Jev/Hub호출·bytes·생성/의미검증시간·비용 저장. structured-only에서TTFTnull허용, 최종callback을 화면표시시각으로 확대금지.
- 본인Hub만 종료, registry가 메모리외 변경되지 않았음을 확인. `reference/2026-10-30-hub-evals/build-out/wp11-claim-q002-experiment-report.md`+답/trace artifacts 작성, Orca worker_done. 앱/Hub소스·DB·사용자서비스·커밋/푸시/PR·대표4/50배치 금지.
