# [clinic_chat backend] case3 반복 탐색 코드 재검수 FAIL 수정 2

너는 현재 앱 worktree의 미커밋 diff를 이어 수정하는 코드 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다.

## 필수 읽기

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-app-walk-phase-a-code-v2.md` 전체와 같은 디렉터리 SPEC-006 0.3.10 §3-4-1-5, WORK-012 WP-1~3/5
- 현재 `clinic_chat/cases/case3.py` coverage 경로, `hub_rest.py`, `config.py`, 관련 시험. HEAD `078ac99`, 기본 feature gate False 유지.

## 수정

1. 질문의 **명시된 복합 항목을 span별 target/facet으로 추출**한다. intent section 목록만으로 모든 질문을 대표하지 않는다. 수집한 관련 fact가 다른 section에 있더라도 원문 조회·scope 확인 전 `not_required`로 버리지 않는다. 제외 이유는 해당 target/facet과 무관하다는 구체 근거로 남긴다. 두 항목이 서로 다른 section에 있는 질문 fixture와 이웃 section fixture를 추가한다.
2. 다중 대상 A/B에서 fact의 `owner`와 `applies_to`가 **그 facet의 같은 target**에 일치해야 지원·전달한다. `applies_to`가 B인 fact를 A 지원으로 쓰지 않는다. 서로 바뀐 적용 범위 fixture를 추가한다.
3. 근거 0개면 Claude 자유 생성 답을 호출하지 않고, 실제 완료 조회로 증명된 범위에 한정한 부재와 미완료 보류를 결정론적으로 구분한다. 근거가 있으면 답 문장별 인용 ID와 해당 target/section/scope, 필수 안전 flags/guidance를 검사한다. 검증 못 하면 보류로 바꾼다. 근거 없는 임의 답과 과도한 `정보 없음` 시험.
4. 실제 provider별 입력 한도를 확인한다. 큰 입력은 facet별 묶음의 ID/출처를 보존해 내부 처리하고, 묶음 결과를 검증·병합한 뒤 **사용자에게 단일 최종 답 한 번만** 낸다. 일부 묶음 실패는 해당 facet `blocked/incomplete`. CLI 한도 fixture와 복합 facet/분할 누락 시험. 구현할 수 없는 제한은 이유를 보고하되 조용히 fact를 버리거나 여러 독립 답을 출력하지 않는다.
5. 필수 checks 이웃 종류가 peek에서 누락됐을 때 완료 빈 목록인지 불명확하면 미완료로 두고, `more`/page 연속성·remaining 모순을 검증한다. 전체 deadline 시계를 vocab/resolve/Jev 이전부터 시작해 남은 시간을 각 단계에 적용한다. 미지원 필수 frontier는 `blocked/incomplete`로 남긴다.

관계 WP-4는 Hub 계약 인계 전 구현 금지. `walk_coverage_mode=False` 기본 유지. 사용자 서버·포트·컨테이너·개발/운영 DB 조작 금지, 50/239×3 평가 금지.

## 범위·검증

- 앞 앱 코드 허용 경로와 관련 시험만 수정. 다른 레포/문서 수정 금지. 허용 밖 필요 시 코디에게 질문.
- 관련 단위 재생, 전체 `uv run pytest -q`, 만진 파일 ruff, `git diff --check`. 실제 QID 파일은 프로필 레포 `reference/2026-10-30-hub-evals/question-set.json`과 `build-out/sample50-questions.txt`를 읽기만 할 수 있다.
- 검수 지적마다 해결 코드/시험 줄과 미실행 사유를 완료 메시지에 남긴다. 커밋·push·PR 금지. 완료 시 dispatch preamble대로 `worker_done` 한 번.
