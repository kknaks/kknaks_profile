# ontology-agent — 온톨로지 데모 앱

기록 01~08 이 밟은 구축 순서를 그대로 재현하는 데모. 계획·게이트의 SoT 는
`para/resources/note/ontology/2026-09-01-ontology-09-agent-app-plan.md` (기록 09).

```
build/    브론즈 적재 + 실버·골드 빌드 DB 이식 (규칙 SoT: 기록 04·05)
tools/    MCP 조회 도구 4종 — query_kpi · query_layer · trace_ontology · get_definition
api/      화면·채팅 API
static/   단일 페이지 (계층 탐색 + KPI + 그래프 + 예보 + 채팅)
tests/    게이트·회귀 테스트
```

- 원천 데이터·DB 는 레포 밖 (`reference/ontology_demo/` — PII, gitignore). 경로는 `config.py` (`ONTOLOGY_DATA_DIR`).
- LLM 은 open-kknaks 경유 (ADR-04). 관계 지식은 프롬프트가 아니라 `ontology_edges` 에 있다 (S-001).
