# @mediness-fe — Workflow

## 태스크 수행 절차

1. **시작**: dispatch brief에 적힌 작업 워크트리와 base를 확인한다. canonical checkout이나 다른 브랜치로 이동하지 않는다.
2. **태스크 입력**: brief의 SSOT·계약·핵심 파일을 읽는다. **brief가 이번 태스크의 유일한 입력**이며 legacy 큐를 탐색하지 않는다.
3. **영향 분석**: 라우트/컴포넌트/lib/API 연동 영향을 확인하고 누락을 점검한다.
4. **기존 코드 탐색**: 재사용 가능한 컴포넌트·훅과 서버/클라이언트 경계 패턴을 확인한다.
5. **테스트 먼저**: 적용 가능한 훅·유틸·critical 컴포넌트에 테스트를 작성한다.
6. **구현**: brief의 와이어프레임·API 계약·allowed_paths를 지키며 최소 변경한다.
7. **검증**: brief §8의 명령을 우선한다. 추가 typecheck·lint·브라우저 검증은 범위와 비용이 안전할 때만 수행한다.
8. **보고**: 변경 파일, 구현 요약, 검증 수치, BE 영향, 미결 사항을 정리한다.
9. **완료**: 커밋·push·PR·별도 legacy 리포트·`.processed` 갱신을 하지 않는다. brief §9와 dispatch preamble의 `taskId`·`dispatchId`로 `worker_done`을 보낸 뒤 멈춘다.

## 모호할 때

- UX·디자인·BE API 판단이 필요하면 임의 추측하지 말고 dispatch preamble의 질문 채널로 코디네이터에게 확인한다.
