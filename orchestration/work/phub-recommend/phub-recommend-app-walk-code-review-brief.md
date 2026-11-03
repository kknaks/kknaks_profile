# [reviewer_code] case3 반복 탐색 1단계 코드 검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다.

## 읽을 것

- 앱 레포 `clinic_chat/hub-evals`의 현재 diff와 관련 코드·시험; 루트 AGENTS.md가 없으면 그 사실만 기록
- 정본(읽기 전용): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-006.md` 0.3.10 §3-4-1-5, `WORK-012.md` WP-0~3/5, `review-coverage-walk-spec-work-v2.md`
- 당시 기준 HEAD `078ac99`; 워커 보고: 지정 시험 54·전체 unit 218·ruff 통과, 미실행 QID 실물 재생/제공자 context 측정

## 검수 초점

사용자는 그래프를 여러 번 탐색하고 **최종 답에 필요한 자료만 Claude에 넘기되 근거를 찾기 전에 버리지 말라**고 했다. diff가 실제 실행 경로에 연결되는지, 8/20/15KB·4걸음·80%를 중단 조건에서 없앴는지, 지원 완료/부재 완료/미완료 상태를 정확히 가르는지 본다. 특히 아래 우려를 독립적으로 확인한다.

1. `coverage_run`의 `focus_terms`/`facet_cues` 키워드 휴리스틱이 질문에 필요한 fact를 누락하거나 다른 facet까지 잘못 거르는지. `supported()`가 원문·출처 확인 전 line만으로 탐색을 멈추는지.
2. `groups`별 `_answer` 반복이 여러 답을 사용자에게 따로 출력하고 최종 결과는 마지막 묶음만 남기는지. 분할 결과의 fact ID 대조·병합이 실제로 있는지.
3. 필수 안전 조건 이웃과 명시 대상 모두를 끝까지 추적하는지. 이웃 목록·page·pair의 미완료를 `unresolved_absence`로 오인하는지. 관계 WP-4 미구현이 의료 사실 부재로 이어지는지.
4. `walk_coverage_mode=True` 기본값으로 새 경로가 실사용에 켜지는데, 검증 범위에 비해 위험이 큰지. 120초 deadline과 기존 TTFT 목표의 관계를 정직하게 기록하는지.
5. 응답 payload의 인용 가능성·source·scope, 선택 ID·원문·출처 보존, `retrieval_limits`와 답변 본문의 관계, 기존 case3 회귀.

각 항목은 FAIL/WARN/PASS, 파일:줄·SPEC 근거·최소 수정안을 적는다. 코드 착수 전이 아니라 **코드 수락 전** 판정이다. 테스트를 실행하지 않아도 된다. 실행하면 필요한 소수만 하고 사용자 서버/DB/포트를 건드리지 않는다.

## 허용 범위

- 읽기 전용. 보고 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-app-walk-phase-a-code.md` 하나만 생성 가능.
- 앱 코드·SPEC·WORK·다른 레포·서버·DB 수정 금지. 커밋·push·PR 금지. 완료 시 dispatch preamble대로 `worker_done` 한 번.
