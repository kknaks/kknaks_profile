# ontology-agent — 온톨로지 데모 앱

기록 01~08 이 밟은 구축 순서를 그대로 재현하는 데모. 계획·게이트의 SoT 는
`para/resources/note/ontology/2026-09-01-ontology-09-agent-app-plan.md` (기록 09).

```
db/       커넥션 규약(읽기 전용 포함) + 계층 스키마 부트스트랩
build/    브론즈 적재 + 실버·골드 빌드 DB 이식 (규칙 SoT: 기록 04·05)
tools/    MCP 조회 도구 4종 — query_kpi · query_layer · trace_ontology · get_definition
api/      화면·채팅 API
static/   단일 페이지 (계층 탐색 + KPI + 그래프 + 예보 + 채팅)
tests/    게이트·회귀 테스트
```

- 원천 데이터·DB 는 레포 밖 (`reference/ontology_demo/` — PII, gitignore). 경로는 `config.py` (`ONTOLOGY_DATA_DIR`).
- LLM 은 open-kknaks 경유 (ADR-04). 관계 지식은 프롬프트가 아니라 `ontology_edges` 에 있다 (S-001).

## 빌드 (WORK-001)

SQLite 한 파일에 `bronze_*`(16) → `silver_*`(6) → `gold_*`(5) → `ontology_*`(2) 와
마스킹 뷰 `v_*`(4) 가 전부 들어간다. 계약은 SPEC-001 §4 다.

```bash
export ONTOLOGY_DATA_DIR=<원천 경로>          # bronze/·silver/_scoring/·ontology/ 가 있는 곳
export ONTOLOGY_DB_PATH=<산출 DB 경로>        # 미지정 시 $ONTOLOGY_DATA_DIR/db/ontology_demo.db

uv run python -m build all                    # 부트스트랩 → 적재 → 실버 → 뷰 → 골드 → 온톨로지 → 게이트 1·2·3
uv run python -m build bronze                 # 단계별 실행
uv run python -m build gate2                  # 게이트 단독 재실행 (WORK-005 가 쓴다)
```

게이트 실패는 **exit code ≠ 0** 이고 SPEC-001 §4 Case Matrix 의 코드
(`BRONZE_ROWCOUNT_MISMATCH` · `ENUM_VIOLATION` · `NEGATIVE_AMOUNT` ·
`CLOSED_LIST_VIOLATION` · `REBUILD_MISMATCH` · `ORPHAN_EDGE` · `PII_LEAK` ·
`NODE_ID_MISMATCH`)와 기대·실측값을 로그로 남긴다. 로그에 PII 원값은 남지 않는다.

**소비자(WORK-002~004)는 `db.connect_ro()` + 마스킹 뷰로만 닿는다** — 원 테이블을 직접
읽는 조회 경로를 만들지 않는다(DEC-002). 브론즈는 적재 이후 불변이고, 상위 계층은 바로
아래 계층만 읽는다.

테스트는 원천이 있을 때만 돈다 — `ONTOLOGY_DATA_DIR` 이 없으면 전부 skip 된다.

```bash
ONTOLOGY_DATA_DIR=<원천 경로> uv run pytest -q tests/
```
