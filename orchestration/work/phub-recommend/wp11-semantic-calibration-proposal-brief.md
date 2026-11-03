# WP-11 실제 all-hold 원인·독립 검증 계획

- 읽기 전용으로 앱 answer_contract.py/17라벨과 `reference/2026-10-30-hub-evals/build-out/wp11-live-semantic-eval-report.md`/실제 raw/state/questions를 분석한다. 실제 jev1.14는 relation15/17, scope11/17, coverage12/17, 최종 양성4/4 거부·전체17/17 hold였다. 동결0.9는 fixture용 초기 문턱이었으며 아직 calibration 성적이 없다.
- 공식 TypeSafe llms.txt→primitives/Noul/confidence/how-to-build/citation-check를 확인하고 한 질문에 복잡한 독립 판단을 과하게 묶었는지, 부정/조건/전체커버 질문이 중복되거나 서로 다른 정의를 강요하는지, state의 불필요 정책 metadata/한국어 표현이 불확실성을 만드는지 원점수로 진단한다. 단순 threshold 인하나 all-green oracle로 해결했다고 하지 않는다.
- 하나의 최소 수정안과 재현 가능한 calibration/holdout 절차를 `orchestration/work/phub-recommend/wp11-semantic-calibration-proposal.md`에 쓴다. 기존17은 이미 관측한 개발 집합이며 새 독립 검증의 성적으로 재사용하지 않는다. 임계값/prompt 조정용과 최종 미관측 검증용 사례를 분리하고 양성/부정·확실성·조건·수치/분모·다른부위·반대문맥·고지삭제·다중claim/다중source를 균형 있게 포함하는 새 라벨 후보를 별도 파일로 작성한다. 라벨은 원문 지지 여부에 한정하고 외부 임상 사실 인증으로 주장하지 않는다. semantic gate가 의무/범위를 줄일 수 없도록 기존 hard gate 유지.
- 현재 raw에서 문턱별 성적 분석은 개발용으로 명시할 수 있으나 그것만으로 정책 등록/활성화하지 않는다. 다음 실제 평가의 질문·정책·모델·선정 기준을 결과 보기 전에 동결하고 추가 API 반복 횟수를 통제할 계획을 제시한다.
- 앱/정본/DB/서비스·policy registry 수정, API/provider/judge/Hub/batch 호출 금지. 제안/새 fixture 후보만 작성하고 Orca worker_done 보고.
