# @mediness-planner — 규칙

## 문서 컨벤션
- mediness 의 frontmatter R4-R9 최소셋을 모든 신규 문서에 채운다
- 관계 (`sources:`) 가 있으면 D4 lineage 를 명시
- 9 카테고리 중 적합한 곳에 박는다 (planning / plan / spec / policy / adr / runbook / test / release-notes / retrospective)
- 문서 생성/수정 전 `rules/document-pipeline.md` 확인

## 스코프 규칙
- mediness 통합 레벨 문서만 수정 — `rules/`, `context/`, `templates/`, `docs/`, 루트 `README.md`/`CLAUDE.md`/`AGENTS.md`
- `products/{service}/` 안은 손대지 않는다. 서비스 워커가 처리
- 신규 서비스 스캐폴드만 필요한 경우 `products/{새서비스}/` 의 빈 `README.md` + `_map.md` 까지만 생성 (본문은 해당 서비스 오케스트레이션이 채움)

## DECISION 작성 규칙
- mediness 레벨 결정은 `mediness/docs/` 또는 `mediness/context/` 의 ADR 형식 (적절한 위치)
- 결정 ID: `MEDINESS-DEC-NNN`
- 표 형식: ID / 결정 / 결론 / Owner / Status (proposed | accepted | superseded)
- Accepted 항목은 본문 섹션으로 별도 기술 (배경 / 옵션 / 근거 / 영향)

## 수정 폭
- 한 태스크 = 하나의 관심사. "이왕 고치는 김에" 다른 문서까지 같이 수정 X
- 의존 변경이 있으면 리포트의 "다른 팀 영향" 에 명시

## 단정 표현 금지
- 정책 초안 단계에서는 "draft" 상태. BE/FE 및 서비스 오케스트레이션 리뷰 전엔 "accepted" 단정 X
- 미해결은 미해결로 그대로 표시 (admin 응답 대기)

## 리포트 형식

```markdown
# {PLAN-NNN-T-NNN} 결과 보고

## 상태: done / in-progress / blocked

## 수행 내용
- {작성/수정한 문서 목록과 위치}
- {핵심 결정 사항 또는 신규 정책 ID}

## 검증
- docs-validate 결과
- frontmatter 충족 여부
- 참고 출처 (rules / context / 코드 경로) 명시

## 다른 팀 영향
- BE/FE 또는 하위 서비스 오케스트레이션이 알아야 할 정책 변경
- 후속 ADR / 미해결 결정

## 이슈/블로커
- {모호한 요구·미확정 사항·admin 결정 필요 항목 — 옵션 + 권장 정리}
```
