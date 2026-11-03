# @day-planner — 규칙

## 문서 컨벤션
- mediness 리포 공통 파이프라인을 따른다: 문서 생성/수정 전 `AGENTS.md` · `rules/` 확인
- frontmatter 최소셋을 모든 신규 문서에 채운다. 관계(`sources:`)가 있으면 lineage 명시
- 제품 폴더 구조는 다른 제품(예 `products/selly/`)의 번호 구조(00-baseline · 10-decision · 20-spec · 30-work)를 따른다.
  새 최상위 디렉토리가 필요하면 만들지 말고 코디네이터에게 묻는다

## 스코프 규칙
- `products/day/` 만 수정한다. 타 제품 · 리포 루트 · `rules/` · `context/` · `templates/` 는 읽기 전용
- 한 태스크 = 하나의 관심사

## 사실과 추측
- 도메인 사실은 `00-baseline/` 과 브리프가 준 SSOT 에서만 가져온다. 없으면 미결로 표시하고 코디네이터에게 올린다
- 초안은 draft 로 둔다. 리뷰 전에 accepted 로 단정하지 않는다

## 리포트 형식

```markdown
# <slug> 결과 보고

## 상태: done / in-progress / blocked

## 수행 내용
- {작성/수정한 문서 목록과 위치}

## 검증
- 브리프 §8 검증 결과 (lint-pipeline --strict, products/day/ 범위)

## 미결·주의점
- {모호한 요구·미확정 사항 — 옵션 + 권장으로 정리}
```
