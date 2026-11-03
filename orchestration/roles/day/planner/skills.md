# @day-planner — 기술 스택

## 도메인 지식
- DAY — 센추리온 제품군의 CRM(환자 · 상담 · 접수 · 예약 · 수납 맥락). **도메인 사실의 SSOT 는 `products/day/00-baseline/`** —
  이 파일에 도메인 요약을 복사해 두지 않는다. 매 태스크 baseline 에서 읽는다

## 리포 공통 도구
- 문서 파이프라인 · frontmatter 규칙: 리포의 `rules/` 가 소유. 워커는 따르기만 한다
- 린트: `python3 scripts/lint-pipeline.py --strict` (products/day/ 범위 ERROR 0 이 기준)
