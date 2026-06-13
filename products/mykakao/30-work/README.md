# Work Index

규칙: `rules/product-doc-pipeline.md`

> spec을 실제 구현 작업으로 내린 work 목록과 spec coverage를 관리한다.

## Work 목록

work 문서를 만들거나 상태, branch, 다음 작업이 바뀌면 이 표를 갱신한다.

| ID | Title | Type | Owner | Status | Progress | Covers Spec | PR/Branch | Next |
|---|---|---|---|---|---|---|---|---|
| WORK-001 | 메시지 추출 확인용 웹 데모 | new-feature | kknaks | done | 100% | SPEC-001 | mykakao (미커밋) | 커밋 / 일정 파싱 단계 |

## Spec Coverage

각 spec이 어떤 work로 구현되는지 확인한다.

| Spec | Work | Status |
|---|---|---|
| SPEC-001 | WORK-001 | done (demo) |
