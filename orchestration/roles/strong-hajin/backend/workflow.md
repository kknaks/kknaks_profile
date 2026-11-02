# @sc-ax-be — Workflow

## 태스크 수행 절차

1. **시작**: dispatch brief 에 적힌 작업 워크트리와 base 를 확인한다. canonical checkout 이나 다른 브랜치로 이동하지 않는다.
2. **태스크 입력**: brief 의 SSOT(SPEC·ERD 절)·계약·핵심 파일을 읽는다. **brief 가 이번 태스크의 유일한 입력**이다.
3. **영향 분석**: entrypoints(HTTP·MCP·워커) → application → platform → tests → `docs/domain-model.md` 순으로 닿는 곳을 전수 나열한다.
4. **기존 코드 탐색**: 같은 모듈의 domain/application 패턴·예외 매핑·envelope 조립 방식을 확인한다. 있는 operation 을 놔두고 재구현하지 않는다.
5. **테스트 먼저**: `tests/unit` 또는 `tests/contract` 에 RED 테스트를 쓰고 실패를 확인한다.
6. **구현**: brief 의 allowed_paths 와 계층 규칙(`rules.md`)을 지키며 최소 변경한다. 표가 바뀌면 `docs/domain-model.md` 한 줄.
7. **검증**: brief §8 의 명령을 우선한다 — 고친 테스트 파일 + `tests/architecture`, `-m 'not integration'`. 전체 스위트를 돌리지 않는다. 검증은 1회만.
8. **보고**: 변경 파일, 구현 요약, 검증 수치, FE 영향(envelope·응답), SPEC 불일치, 미결 사항을 정리한다 (`rules.md` 리포트 형식).
9. **완료**: 커밋·push·PR 을 하지 않는다. brief §9 와 dispatch preamble 의 `taskId`·`dispatchId` 로 2채널 완료 보고를 보낸 뒤 멈춘다.

## 모호할 때
- SPEC·ERD·FE 계약 판단이 필요하면 임의 결정하지 말고 dispatch preamble 의 질문 채널로 코디네이터에게 확인한다.
