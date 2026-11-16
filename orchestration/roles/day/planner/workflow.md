# @day-planner — Workflow

1. **시작**: brief 의 작업 워크트리와 base 를 확인한다. canonical checkout 이나 다른 브랜치로 이동하지 않는다.
2. **태스크 입력**: brief 의 SSOT · 핵심 파일을 읽는다. **brief 가 이번 태스크의 유일한 입력**이다.
3. **기존 문서 탐색**: `products/day/` 안에서 중복 · 충돌을 확인한다. 이미 있는 문서를 놔두고 새로 만들지 않는다.
4. **작성 · 검증**: frontmatter 와 파이프라인을 지키며 작성하고 brief §8 의 검증을 실행한다.
5. **완료**: 커밋 · push · PR 을 하지 않는다. brief §9 와 preamble 의 `taskId` · `dispatchId` 로 완료 보고 후 멈춘다.

모호하면 자율 결정하지 말고 preamble 의 질문 채널로 코디네이터에게 묻는다.
