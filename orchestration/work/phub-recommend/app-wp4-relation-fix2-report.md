# 앱 WP-4 관계 어댑터 재검수 수정 2 보고

2026-11-02 · 앱 기준 HEAD `078ac99`, 기존 미커밋 WP-4 변경에 이어 수정. 실물 서버·DB·provider 및 50/239×3 평가는 실행하지 않았다.

## 수정

- **F-1**: 자기 쌍은 확정 단위 시술의 질문 span에 재시술 표현이 연결되거나 명시적인 `같은 시술` 반복일 때만 조회한다. `다시 받` 단독과 `다른/타/별도 시술` 상대는 자기 쌍을 만들지 않고 `unresolved_pair`로 남긴다. 음성 변형의 walk 재생을 추가했다.
- **F-3**: 질문의 `같은 날`·`같은 부위`를 집합으로 보존하고 전역 row의 조건을 각 원소와 대조한다. Q139 형태의 두 조건 fixture에서 `같은 날` row가 선택·전달된다. `unresolved_condition` row는 인용하지 않고, 완료 scope라도 선별에 실패한 row만 있으면 relation facet을 `blocked/incomplete`로 유지한다.
- **F-5**: 완료된 selected pair 응답의 `prior.ok/basis`를 수집하고 페이지 간 일치를 확인한다. resolved 원천 fact ID 전부가 선택된 경우에만 요청 pair, 이전 시술 ID, 경과일, 정/역방향, source ID·원문과 묶어 `relation_prior` 및 facet 원장에 전달한다. 분할 입력에도 같은 source ID가 있는 조각에서만 보낸다. 원천이 불충분하면 prior facet을 `blocked/incomplete`로 둔다. 이전 시술이 두 번째 target인 역방향 요청→Claude 전달→출처 인용 답 fixture를 추가했다. Hub가 계산한 판정만 전달하며 앱에서 정책값을 만들지 않는다.

기존 F-2 pair/global scope 분리와 F-4 resolved/source 결속, 페이지·출처·부분 답·안전·분할 ID 경로는 회귀 시험으로 유지했다.

## 검증

- `uv run pytest -q tests/phase8/test_relation_adapter.py`: 31 passed
- `uv run pytest -q`: 287 passed
- `uv run ruff check .`: PASS
- `git diff --check 078ac99`: PASS

남은 활성화 관문은 WORK-011 인계의 실물 selected/global endpoint와 앱 build hash 일치, 실제 QID 수집→선별→전달→답 재생, WORK-012의 고정 50문항 평가다. 이 보고는 격리 fixture 기반 코드 수정 결과이며 실물 서버 성공을 주장하지 않는다.
