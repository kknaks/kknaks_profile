# Decision Index

규칙: `rules/product-doc-pipeline.md`

## 결정 로그

| ID | Title | Status | Baseline | Result | Spec |
|---|---|---|---|---|---|
| KDEV-DEC-001 | products 단일 루트 통합 | accepted | KDEV-BL-001 | accepted | 디렉토리 구조 |
| KDEV-DEC-002 | 지식 파이프라인 층 (루트 레벨) | accepted | KDEV-BL-001 | accepted | 디렉토리 구조 |
| KDEV-DEC-003 | 노드 타입 + 식별자(파일명 stem) | accepted | KDEV-BL-001 | accepted | 스키마 |
| KDEV-DEC-004 | 엣지 모델 + 스키마 SSOT | accepted | KDEV-BL-001 | accepted | 스키마 |
| KDEV-DEC-005 | 분류 워크플로 (독립 SSOT) | accepted | KDEV-BL-001 | accepted | 워크플로 |
| KDEV-DEC-006 | 검증 게이트 L1~L6 | accepted | KDEV-BL-001 | accepted | 검증 |
| KDEV-DEC-007 | 블로그 그래프 시각화 | accepted | KDEV-BL-001 | accepted | 시각화 |
| KDEV-DEC-008 | contents 잔류 (YouTube 요약, 그래프 무관) | accepted | KDEV-BL-001 | accepted | 디렉토리 구조 |

## 미결 사항

| ID | Question | Owner | Next |
|---|---|---|---|
| ~~OQ-1~~ | (해결) medi_docs 전체 폐기 완료 2026-06-29, spec-02/04는 KDEV-SPEC-002 계승 | kknaks | done |
| OQ-2 | force graph 라이브러리 선택 (구현 OQ) | kknaks | 시각화 work |
