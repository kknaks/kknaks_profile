# [PROCEDURE-HUB backend] 선택 관계 재검수 FAIL 2~4 수정

너는 현재 Hub worktree의 미커밋 diff를 이어 수정하는 코드 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다.

## 필수 읽기

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-hub-selected-code-v2.md` 전체와 같은 디렉터리 SPEC-005 0.3.9 §5-5·§6-9, WORK-011
- 현재 `backend/app/modules/gold/selected.py`, gold schema/route/MCP/시험. HEAD `2edc190`, 실물 build `567677edfe7123e9`.

## 수정

1. Q139 combo anchor의 `sequence_text_8`가 증명하는 **서브시전→프락셔널/니들RF 4주 후**, **니들RF/프락셔널→PRP 동시** 관계만 pair scope로 매핑한다. combo 구성 요소 모든 교차 쌍 23개를 자동으로 인용 가능하게 하지 않는다. `U5-110/U5-045`, `U5-110/U5-020` 양방향은 원천/Gold 관계에 맞춰 검증하고 조합 내부 비지원 쌍(`U5-045/U5-020` 등)과 무관 외부 쌍은 인용 불가 시험. 확정 pair 없이 global 목록 조회할 때는 pair별 인용 가능으로 표시하지 않는다. 원천 순서/동시성 매핑이 증명되지 않는 항목은 `unresolved_scope`로 둔다.
2. R8-0144 조건부 fact는 qualifier의 **조건 차원 key와 값이 모두** 요청 `sub_condition`에 맞을 때만 인용 가능. 다른 key에 같은 값을 넣는 음성 시험. 차원 미확정이면 미지원/인용 불가.
3. edge claim/conditional/resolved/대안 fact의 `owner_id`가 해당 edge인지 검증한다. 다른 **존재하는 edge**로 owner를 바꾼 메모리 fixture는 `error,complete=false` 시험. 원천/source 결속도 유지한다.
4. 186개 첫 페이지 ID 순서의 HEAD 기준 자료가 있으면 비교 증거를 남기고, 없으면 정확히 무엇이 없어 미확인인지 보고한다. 페이지 코어는 이번 diff에서 변경하지 않는다. REST/MCP 공통 코어, cursor 550행/9페이지 회수, 호출별 cap·조건/방향 회귀 유지.

사용자 포트/컨테이너/DB 조작 금지, 새 평가 실행 금지. 공개 원장 본문 복제 금지.

## 범위·검증

- 앞 Hub 허용 경로와 관련 시험만 수정. 다른 레포/문서 수정 금지.
- 관련 `uv run pytest`, DB 비의존 unit suite, 만진 파일 ruff, `git diff --check`. 실물 Gold는 메모리 fixture/inprocess만 사용.
- FAIL별 코드/시험 근거와 아직 미검증인 항목을 완료 메시지에 남긴다. 커밋·push·PR 금지. 완료 시 dispatch preamble대로 `worker_done` 한 번.
