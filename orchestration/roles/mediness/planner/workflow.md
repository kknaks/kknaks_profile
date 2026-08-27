# @mediness-planner — Workflow

## 태스크 수행 절차

1. **시작**: dispatch brief에 적힌 작업 워크트리와 base를 확인한다. canonical checkout이나 다른 브랜치로 이동하지 않는다.
2. **태스크 입력**: brief의 SSOT·계약·핵심 파일을 읽는다. **brief가 이번 태스크의 유일한 입력**이며 legacy 큐를 탐색하지 않는다.
3. **문서 컨텍스트**: 저장소의 `AGENTS.md`, `rules/document-pipeline.md`, `context/manifest.yaml`, `context/index.md`, `context/current-state.md`, 관련 template을 필요한 범위에서 읽는다.
4. **스코프 점검**: `products/{service}/` 하위가 다른 서비스 오케스트레이션 소유라면 수정하지 않고 코디네이터에게 알린다.
5. **기존 문서 탐색**: `rules/`·`context/`·`docs/`에서 중복·충돌을 확인한다.
6. **작성·검증**: 기존 frontmatter와 문서 파이프라인을 지키며 작성하고 brief §8의 검증을 실행한다.
7. **보고**: 변경 파일, 판단 근거, 검증 결과, 다른 서비스 영향, 미결 사항을 정리한다.
8. **완료**: 커밋·push·PR·별도 legacy 리포트·`.processed` 갱신을 하지 않는다. brief §9와 dispatch preamble의 `taskId`·`dispatchId`로 `worker_done`을 보낸 뒤 멈춘다.

## 모호할 때

- 카테고리·정책·메타 규칙 판단이 필요하면 자율 정정하지 말고 dispatch preamble의 질문 채널로 코디네이터에게 확인한다.
