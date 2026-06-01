# Agent Entry

이 파일은 에이전트가 `kknaks_profile` 레포에 들어왔을 때 가장 먼저 읽는 진입점이다.

## 시작 흐름

에이전트는 작업을 시작할 때 아래 순서로 진입한다.

```text
CLAUDE.md
→ agent.md
→ context/index.md
→ context/kknaks.md
→ company 또는 studio context
```

`context/index.md`는 사용자 요청을 회사 업무와 개인사업자/개인 프로젝트 업무로 분기하는 최상위 라우터다.

`context/kknaks.md`는 회사 업무와 개인사업자 영역을 구분하는 기준 문서다.

## 목적

이 레포는 단순 포트폴리오가 아니라 이건학의 페르소나, 프로젝트, 학습 기록, 콘텐츠, 개발 현황을 하나의 source of truth로 관리하기 위한 작업 공간이다.

최종 목표는 하나의 진입점에서 다음을 모두 파악하고 개발할 수 있게 만드는 것이다.

- 나는 누구인지
- 어떤 프로젝트를 하고 있는지
- 각 프로젝트가 지금 어떤 상태인지
- 무엇을 다음에 개발해야 하는지
- 공개 포트폴리오에는 무엇을 보여줄지

## 응답 종료 전 Hook

에이전트가 아래 경로를 생성하거나 수정했다면, 최종 응답 전에 반드시 product doc pipeline hook을 수행한다.

```text
products/**
templates/product/**
rules/product-doc-pipeline.md
.agent/hooks/product-doc-pipeline.md
.agent/scripts/product_doc_pipeline.py
```

수행 순서:

```text
.agent/hooks/product-doc-pipeline.md 체크리스트 확인
→ python3 .agent/scripts/product_doc_pipeline.py 실행
→ warnings/errors/needs_user_decision 확인
→ 최종 응답에 검증 결과 포함
```

hook이 실패하면 성공처럼 보고하지 않는다. 자동으로 판단할 수 없는 제품 결정은 사용자에게 결정이 필요하다고 보고한다.
