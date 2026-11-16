# [clinic_chat backend] case3 반복 그래프 탐색 1단계 구현

너는 `clinic_chat/hub-evals` 코드 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다. 이 브리프 한 장으로 작업한다.

## 읽을 것

- 이 코드 레포의 README/pyproject 및 관련 코드·시험: `clinic_chat/cases/case3.py`, `clinic_chat/clients/hub_rest.py`, `clinic_chat/config.py`, `tests/fake_hub/`, `tests/phase8/test_case3_walk.py` (AGENTS.md가 있으면 읽고, 없으면 없다고 보고)
- 정본(코디 워크트리, 읽기 전용): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-006.md` **0.3.10 §3-4-1-5** 및 `WORK-012.md` WP-0~3, WP-5의 node fact 선별 부분, `review-coverage-walk-spec-work-v2.md`
- Hub page API(읽기 전용): 같은 디렉터리 `SPEC-005.md` 0.3.9 §5-16. 이 문서 §5-16의 15KB 앱 배제는 **0.3.9 당시 기록**이며 현행 앱 정책은 SPEC-006 0.3.10이다.

## 작업

현재 `case3.py`는 4걸음, 8/20/15KB, `enough`/80%, section `taken`, 첫 page만으로 탐색을 멈춘다. 사용자 요구는 **질문에 필요한 근거를 찾기 위해 그래프의 다른 노드·이웃·다음 페이지를 여러 번 탐색하고, 최종 답에 필요한 사실만 Claude에 넘기는 것**이다. Claude 비용 때문에 그래프 탐색을 고정 바이트에서 끊지 않는다.

이번 1단계는 **WORK-012 WP-0~3과 WP-5의 node fact 수집/선별 경로**를 구현한다. question_targets·필수 facet·안전 범위를 추적하고, 초기 4걸음 뒤 미지원 필수 범위의 frontier를 이어 탐색한다. `(node,section,page)`·이웃 목록의 다음 묶음·중복 요청 키/진전 감지로 무한 반복을 막고 Hub `more`를 따라 뒤 page를 받는다. 필요한 fact·출처·안전 고지를 찾으면 그 항목은 지원 완료, 무관한 나머지는 `not_required` 이유를 남긴다. `정보 없음` 판정은 필요한 범위를 실제로 끝까지 조회한 경우에만 가능하다. timeout/도구 오류/미조회는 `blocked/incomplete`다.

모든 응답의 수집 원장과 Claude 전달 선택을 분리하고, Claude에는 질문과 관련된 인용 가능한 원문 fact·출처·필수 안전 fact만 중복 제거해 전달한다. cut 줄은 원문 조회 전 인용하지 않는다. 기존 8/20/15KB·4걸음·80%·Jev enough가 전체 탐색 hard stop이 되지 않아야 한다. 실제 제공자 입력 한계는 최종 전달에서 선별/분할로 처리하고, 조용한 절단은 금지한다. 운영 timeout은 기존 클라이언트 기본값과 격리 측정에 근거해 설정하고 값·근거를 보고한다. Hub page 요청 단위 제한은 지킨다.

**관계 어댑터 WORK-012 WP-4는 이번 발주에서 제외**한다. Hub WORK-011 공개 schema·§6-9 PASS를 코디가 확인해 인계한 뒤 별도 발주한다. 관계 미지원은 원장 사실 부재로 단정하지 않는다. 서버 18005와 사용자 포트·컨테이너는 건드리지 않는다. 새 50/239×3 평가는 돌리지 않는다.

## 범위·검증

- 착수 시 HEAD `078ac99`와 `git status --short`, 연결 Hub build hash를 기록한다. 차이가 있으면 코디에 보고하고 맞춘다.
- 수정 허용: `clinic_chat/cases/case3.py`, `clinic_chat/clients/hub_rest.py`, `clinic_chat/config.py`, `clinic_chat/runner.py`, `prompts/case3.md`, `tests/fake_hub/*`, `tests/fake_jev.py`, `tests/phase8/*`, `tests/phase4/test_timing_runs.py` 중 필요한 파일만. `verify_runs.py`/report CLI는 이번 단계에서 인터페이스가 필요할 때만 수정하고 이유를 보고한다. 허용 밖 파일·다른 레포 수정 금지.
- 의미 있는 단위 재생: 앞 page 지원 후 무관 뒤 page 중단, 뒤 page에서만 지원되면 계속 탐색, 부재는 `more=0` 및 필요한 이웃 범위 완료, 미지원 필수 frontier 잔여는 incomplete, 안전 확인 조건 8KB 초과 뒤에도 수집, 중복 tuple 0, 질문과 무관한 수집 fact는 Claude 입력에서 제외, 필수 안전 fact는 전달. Q015/Q072/Q069/Q173 및 Q085/Q098/Q136/Q160을 가능한 범위에서 개별 재생한다.
- `uv run pytest tests/phase8/test_case3_walk.py tests/phase4/test_timing_runs.py -q`와 만진 파일의 ruff 검사, 가능한 전체 unit suite를 실행한다. DB·서버 접근이 필요한 시험은 격리 환경만 사용한다. 실패/미실행은 이유와 함께 보고한다.
- 코드 diff, 테스트 결과, 운영 시간값·실측, 기존 동작과 남은 WP-4/5/6을 완료 메시지에 요약한다. 커밋·push·PR 금지. 완료 시 dispatch preamble대로 `worker_done` 한 번.
