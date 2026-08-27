# @mediness-planner — 기술 스택

## 도메인 지식
- mediness — Centurion (의료 SaaS) 의 메인 하네스 + 자체 풀스택 앱 (mediness-app)
- 하위 서비스: charty (음성 차트), linky (시술 카탈로그 hub), pay (수납), procedure-hub (시술 카탈로그), watch (?) — 각자 독립 오케스트레이션이 있음
- mediness 하네스 자체의 책임: 통합 운영·문서 파이프라인·릴리스 룰·신규 서비스 추가 절차
- mediness 문서 도서관의 9 카테고리 모델: planning / plan / spec / policy / adr / runbook / test / release-notes / retrospective
- frontmatter 기반 문서 lineage (R4-R9 최소셋, D4 lineage)

## 사용하는 mediness 스킬
- `medi-new`: 9 카테고리 중 하나에 새 문서 생성 (frontmatter 자동 채움)
- `docs-validate`: frontmatter + 관계 검증
- `api-design`: 신규/수정 API 의 구현 전 5 단계 설계 합의
- `medi-version-cut`: cut 시점 박제 (admin 지시 시에만)

## 문서 작성 원칙
- 통합 정책은 `mediness/rules/`, `mediness/context/`, `mediness/docs/` 의 SSOT 한 곳에만 — 중복 X
- 하위 서비스 별 정책은 해당 서비스 오케스트레이션에 위임, 여기서는 메타 규칙만
- 모호한 요구는 옵션 + 권장으로 정리해서 admin 결정을 받는다
- 신규 서비스 추가 시 `products/{새서비스}/` 스캐폴드는 mediness-planner 가 만들고, 본문 작성은 해당 서비스 오케스트레이션으로 위임
