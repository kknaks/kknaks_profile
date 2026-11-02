# @sc-ax-planner — 기술 스택

## 도메인 지식
- sc-ax — mediness 문서 리포의 제품 하나. **도메인 사실의 SSOT 는 `products/sc-ax/00-baseline/`** —
  개요·문제·사용자·비전·원칙·범위·역량·지표·로드맵·용어가 번호 문서로 정리돼 있다
- 이 문서(skills.md)에 도메인 요약을 복사해 두지 않는다 — 낡는다. 매 태스크 baseline 에서 읽는다

## 리포 공통 도구
- 문서 파이프라인·frontmatter 규칙: 리포의 `rules/` 가 소유. 워커는 따르기만 한다
- 린트: `python3 scripts/lint-pipeline.py --strict` (products/sc-ax/ 범위 ERROR 0 이 기준)

## 문서 작성 원칙
- 같은 사실은 한 곳에만 — 중복 서술 대신 참조
- 모호한 요구는 옵션 + 권장으로 정리해서 코디네이터 결정을 받는다
