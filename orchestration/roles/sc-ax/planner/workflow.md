# @sc-ax-planner — Workflow

## 태스크 수행 절차

1. **시작**: dispatch brief 에 적힌 작업 워크트리와 base 를 확인한다. canonical checkout 이나 다른 브랜치로 이동하지 않는다.
2. **태스크 입력**: brief 의 SSOT·핵심 파일을 읽는다. **brief 가 이번 태스크의 유일한 입력**이다.
3. **문서 컨텍스트**: `AGENTS.md`, `rules/document-pipeline.md`, `products/sc-ax/` 인덱스·baseline 을 필요한 범위에서 읽는다.
4. **기존 문서 탐색**: `products/sc-ax/` 안에서 중복·충돌을 확인한다. 이미 있는 문서를 놔두고 새로 만들지 않는다.
5. **작성·검증**: frontmatter 와 문서 파이프라인을 지키며 작성하고 brief §8 의 검증을 실행한다.
6. **보고**: 변경 파일, 판단 근거, 검증 결과, 미결 사항을 정리한다 (`rules.md` 리포트 형식).
7. **완료**: 커밋·push·PR 을 하지 않는다. brief §9 와 dispatch preamble 의 `taskId`·`dispatchId` 로 2채널 완료 보고를 보낸 뒤 멈춘다.

## 모호할 때
- 문서 자리·정책 판단이 필요하면 자율 결정하지 말고 dispatch preamble 의 질문 채널로 코디네이터에게 확인한다.
