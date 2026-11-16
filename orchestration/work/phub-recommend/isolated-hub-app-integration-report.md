# Hub·앱 격리 연결 관문 보고

2026-11-02 KST. Hub `2edc190e70d4322f69672cc0e9e23417169e63cd` + 미커밋 코드, 앱 `078ac99b2f307de65acdcdecc9beb94bcda1249c` + 미커밋 코드를 읽기 전용으로 관찰했다. 실물 입력을 `backend/tests/gold_support.py`의 inprocess 메모리 graph로 로드한 build hash는 `567677edfe7123e9`이다. `app.graph_main:app`에 ASGI transport를 붙여 공개 REST를 호출했고 앱 `HubRest.call` 및 `relation_adapter.collect/facts`에 같은 응답을 통과시켰다. 사용자 서버 `127.0.0.1:18005`, 컨테이너, 포트, DB, 평가는 건드리지 않았다.

## 대표 원문과 출처

질문 원문은 `reference/2026-10-30-hub-evals/question-set.md`의 QID 행에서 확인했다. 아래 관계 원문은 실제 Gold fact이며 출처는 각각 `step8-relations.json`의 `claims[ID]`다. 지정 pair 조회는 모두 `found`, `pair_scope.complete=true`, `more=0`, cursor 없음, 앱 어댑터의 해당 claim `quotable=true`였다.

| 질문 원문 | ID와 Gold 원문 | owner edge / 확정 unit pair | 전달 판단 |
|---|---|---|---|
| Q018 “이마 보톡스랑 팔자 필러 같이 맞아도 돼요?” | R8-0163 “같은 날 필러+보톡스: 필러 먼저(위치 안정화) → 보톡스 나중에 (필러 위치 보존, 전문가 합의 기반 기본값, 같은 날엔 순서 유연)” | E8-0005 / U5-001, U5-082 | 해당 pair에서 가능. 관련 대안 1행은 적용 범위 미충족으로 제외됨 |
| Q064 “스킨부스터와 필러는 같은 날 맞을 수 있나요?” | R8-0075 “M4-리쥬란 함께 M2-필러 · 같은 날 시술 가능” | E8-0069 / U5-082, U5-018 | 해당 pair에서 가능. 일반 스킨부스터 전체로 확대 불가 |
| Q139 “서브시전과 프락셔널 레이저는 뭘 먼저 하나요?” | R8-0218 “서브시전(깊은 흉터 박리) → 4주 후 프락셔널/니들RF → PRP 동시 도포” | E8-0031 / U5-110, U5-045 | 해당 pair에서 가능 |
| Q139 동일 질문 | R8-0219 동일 원문 | E8-0029 / U5-110, U5-020 | 해당 pair에서 가능. 위 행과 owner edge가 다름 |
| Q173 “필링과 토닝을 같은 날 받을 수 있나요?” | R8-0111 “M8-레이저토닝 함께 M15-필링 · 같은 날 시술 가능” | E8-0185 / U5-023, U5-034 | 해당 pair에서 가능. 안전 조건은 별도 확인 필요 |

Q139 전역 메모 `scope:all#evidence#step8_notes[26]`는 R8 edge와 별도 `global-claims` 경로로 U5-110/U5-020 및 U5-110/U5-045를 조회했다. 실제 원문은 “서브시전(깊은 흉터 박리) → 4주 후 프락셔널/니들RF → PRP 동시 도포”, 출처는 `step7-concerns.json`의 `step8_notes[26]`이다. 두 선택 pair에서 모두 `found`, `scope_complete=true`, `more=0`, cursor 없음, 행 `quotable=true`였고 앱도 전달 가능으로 판정했다.

## 결정론·페이지·크기

동일 build와 동일 요청을 각각 두 번 실행했다. 위 5개 pair와 2개 단일 global scope의 앱 수집 결과 전체가 같아 ID·순서·원문·출처·상태·serialized 크기 선택이 일치했다. pair 응답 바이트는 위 표 순서로 `21701, 8009, 3117, 10715, 5572`로 64 KiB 이하다. Q139 단일 scope는 두 pair 모두 `2175`바이트로 32 KiB 이하다. `family:M1`을 pair로 넣은 REST 400은 앱 `HubRestError`로 올라왔다.

별도 `scope:all` REST cursor를 9쪽 끝까지 따라가 550행을 재조립했다. 행 수는 `85,83,51,52,52,36,48,75,68`, 각 serialized 바이트는 `32579,32432,31659,32582,32698,25037,32548,32621,27061`이다. 앞 8쪽은 `truncated`, `scope_complete=false`, cursor 있음; 마지막은 `found`, `scope_complete=true`, `more=0`, cursor 없음이다. 앱 어댑터 수집은 완료됐고 두 번의 전체 결과가 같았다. 550행 모두가 인용 가능하다는 뜻은 아니다.

## 판단·한계

**격리 Hub/app 연결 관문 PASS.** 실제 Gold build의 공개 REST와 현 앱 client/관계 어댑터가 대표 관계 및 Q139 전역 메모의 완료·cursor·출처·적용 범위를 해석했다. 이는 모델 답변 평가나 일반 명칭에서 특정 unit pair로의 매핑 검증이 아니다. 실제 사용자 서버의 route/build는 확인하지 않았으므로 기능 활성화 전 동일 build 확인이 남는다. 앱 `case3.py`는 다른 워커가 수정 중이어서 질문 전체 탐색·Claude 전달·답변까지의 최종 통합 판정은 보류한다.

앱 최종 관찰 HEAD `078ac99`; 수정 파일 `case3.py`, `hub_rest.py`, `config.py`, `tests/conftest.py`, `tests/phase4/test_timing_runs.py`, `tests/phase8/test_case3_walk.py`; 신규 파일 `relation_adapter.py`, `tests/phase8/test_relation_adapter.py`. 주요 mtime은 `relation_adapter.py` 15:42:32, `hub_rest.py` 15:12:33, `case3.py` 15:49:17, `test_relation_adapter.py` 15:42:35 KST. 저장소 AGENTS.md가 가리키는 `/Users/marin/AGENTS.md`는 이 환경에 없어 읽을 수 없었다.
