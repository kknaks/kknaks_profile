# Decision Index

규칙: `rules/product-doc-pipeline.md`

> baseline을 제품에 어떻게 적용할지 판단한 결정 목록과 아직 풀어야 할 질문을 관리한다.

## 결정 로그

decision 문서를 만들거나 상태가 바뀌면 이 표를 갱신한다.

| ID | Title | Status | Baseline | Result | Spec |
|---|---|---|---|---|---|
| DEC-001 | 메시지 추출 방식 — 로컬 SQLCipher DB 복호화 (kakaocli) | accepted | BASE-001 | B 채택 (로컬 복호화) | SPEC-001 |

## 미결 사항

spec으로 내리기 전에 판단해야 하는 질문을 적는다.

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | 카톡 버전 업데이트 시 키 유도 깨짐 대응 | kknaks | 추출 안정화 후 |
| OQ-2 | 신규 메시지 증분 수집(sync) 여부 | kknaks | 출력 플로우 결정 시 |
