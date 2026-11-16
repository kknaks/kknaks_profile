# 앱 WP-4 관계 어댑터 구현 보고

2026-11-02 · 앱 기준 HEAD `078ac99` · WORK-011 공개 계약(`567677edfe7123e9` 격리 Hub build) 기준

## 구현

- `hub_rest.route`에 선택 쌍과 전역 scope POST 경로를 추가했다. 기존 기본 `walk_coverage_mode=False`와 이전 WP 수집 경로는 유지했다.
- coverage walk는 질문에서 확정된 단위 시술만 질문 순서의 pair로 만들고 중복 없이 `selected_pair`를 조회한다. 명시된 같은 날·같은 부위·심부 페놀 조건과 이전 시술 경과 기간을 요청에 넣는다. U5-045/U5-110/U5-020 관련 I-07 범위는 Q139 전역 scope를 별도 조회한다.
- 선택 쌍과 전역 scope의 `more/next_cursor/complete/status`를 마지막 페이지까지 확인한다. 커서 반복, 행 반복, 잔여 수 불일치, 오류/잘림, 요청·build 불일치, REST 실패는 해당 범위를 미완료로 둔다. 호출당 응답 상한을 전체 탐색 중단 조건으로 사용하지 않는다.
- resolved source, claim, 대안, 전역 메모의 ID·원문·source file/path·`applies_to`·`quotable`을 `walk.relations`와 `walk.selection`에 남긴다. 전달에는 완성된 범위에서 pair·방향·조건·출처·인용 자격이 맞는 fact만 넣는다. 공유 claim의 미확정 owner 범위와 `quotable=false`는 제외한다. 같은 fact ID의 대안과 claim이 함께 나오면 대안 적용 범위를 우선하여 한 번만 전달한다. Q139 전역 메모는 R8 edge claim과 별도 원장 항목이다.
- vocab·resolve와 이후 Hub 응답의 build hash를 대조한다. 불일치가 있으면 지원·부재 완료와 모델 전달을 막고 `incomplete`로 남긴다.

## 검증

- 모의 Hub 응답으로 Q018.1/R8-0163, Q064.1/R8-0075, Q139.1/2/R8-0218/0219, Q173.1/R8-0111 ID·원문·출처 보존과 Q139 전역 scope, 선택 쌍 다중 페이지, 조건·방향·공유 claim, 잘못된 출처, 빈/오류/커서/빌드 불일치를 시험했다. coverage walk 통합 시험에서 선택 관계 fact가 facet과 전달 근거로 연결되는 것도 확인했다.
- `uv run pytest -q`: **274 passed**. `uv run ruff check .`: **PASS**. `git diff --check`: **PASS**.
- 사용자 실물 서버/모델/DB/50문항/239×3 평가는 실행하지 않았다. 이 보고의 대표 QID 시험은 모의 응답의 ID·scope 계약 검사이며, 실물 질문 재생의 회복 판정은 아니다. 기능 활성화 전 실제 앱·Hub build hash 일치와 별도 고정 질문 재생이 남아 있다.

## 변경 범위

이번 작업은 `clinic_chat/cases/relation_adapter.py`, `clinic_chat/cases/case3.py`, `clinic_chat/clients/hub_rest.py`, `tests/phase8/test_relation_adapter.py`와 이 보고 파일을 수정/추가했다. 시작 시 이미 존재하던 `case3.py`, `hub_rest.py`, `config.py`, `tests/conftest.py`, `tests/phase4/test_timing_runs.py`, `tests/phase8/test_case3_walk.py`의 미커밋 WP-1~3/5 작업은 유지했다. 커밋·push·PR은 하지 않았다.
