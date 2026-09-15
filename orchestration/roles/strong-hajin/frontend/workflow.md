# @sc-ax-fe — Workflow

## 태스크 수행 절차

1. **시작**: dispatch brief 에 적힌 작업 워크트리와 base 를 확인한다. canonical checkout 이나 다른 브랜치로 이동하지 않는다.
2. **태스크 입력**: brief 의 SSOT(SPEC·화면 명세·디자인)·API 계약·핵심 파일을 읽는다. **brief 가 이번 태스크의 유일한 입력**이다.
3. **영향 분석**: 페이지 → 컴포넌트 → viewModels → api.ts → 테스트 순으로 닿는 곳을 전수 나열한다.
4. **기존 코드 탐색**: 재사용 가능한 컴포넌트·viewModel·label 을 확인한다. 있는 것을 놔두고 새로 만들지 않는다.
5. **테스트 먼저**: 옆자리 `*.test.tsx` 에 RED 테스트를 쓰고 실패를 확인한다.
6. **구현**: brief 의 화면 명세·API 계약·allowed_paths 를 지키며 최소 변경한다. 권한 판단은 envelope 로만.
7. **검증**: brief §8 의 명령을 우선한다 — `npx tsc --noEmit` + 고친 테스트 파일 vitest. 전체 빌드·e2e 를 돌리지 않는다. 검증은 1회만.
8. **보고**: 변경 파일, 구현 요약, 검증 수치, BE 영향(envelope·응답), SPEC·디자인 불일치, 미결 사항을 정리한다 (`rules.md` 리포트 형식).
9. **완료**: 커밋·push·PR 을 하지 않는다. brief §9 와 dispatch preamble 의 `taskId`·`dispatchId` 로 2채널 완료 보고를 보낸 뒤 멈춘다.

## 모호할 때
- UX·디자인·BE 계약 판단이 필요하면 임의 추측하지 말고 dispatch preamble 의 질문 채널로 코디네이터에게 확인한다.
