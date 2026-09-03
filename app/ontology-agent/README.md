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

게이트 실패는 **exit code ≠ 0** 이고 SPEC-001 §4 Case Matrix 의 코드 **13종**과
기대·실측값을 로그로 남긴다. 로그에 PII 원값은 남지 않는다.

`BRONZE_ROWCOUNT_MISMATCH` · `ENUM_VIOLATION` · `NEGATIVE_AMOUNT` ·
`CLOSED_LIST_VIOLATION` · `REBUILD_MISMATCH` · `ORPHAN_EDGE` · `PII_LEAK` ·
`NODE_ID_MISMATCH` · `REVIEW_SCORE_VIOLATION` · `MASKING_RESIDUE` ·
`AGREEMENT_BELOW_THRESHOLD` · `UNKNOWN_BRANCH` · `SILVER_ROWCOUNT_MISMATCH`

전 게이트를 통과하면 **빌드 표식**(`build_meta` 1행)이 채택 트랜잭션 안에서 찍힌다.
표식이 없는 DB 는 `connect_ro()` 가 열지 않는다 — 「한 번도 안 만든 DB」와 「빌드가 실패한
DB」를 파일 존재만으로는 구분할 수 없기 때문이다.
**단계 단독 실행(`build gold` 등)은 표식을 지운다** — 게이트를 거치지 않은 산출물이
「1,2,3 통과」로 서빙되면 표식이 거짓을 말하게 된다. 다시 서빙하려면 `build all` 을 돌린다.
게이트 단독 재실행(`gate1`~`gate3`)은 읽기만 하므로 표식을 건드리지 않는다.

**소비자(WORK-002~004)는 `db.connect_ro()` + 마스킹 뷰로만 닿는다** — 원 테이블을 직접
읽는 조회 경로를 만들지 않는다(DEC-002). 브론즈는 적재 이후 불변이고, 상위 계층은 바로
아래 계층만 읽는다.
`connect_ro()` 는 **쓰기만** 막으므로 뷰 경유 강제는 커넥션이 아니라 코드로 보장한다 —
`tests/test_w002_ac8_view_only.py` 의 정적 검사가 그 게이트다.

테스트는 원천이 있을 때만 돈다 — `ONTOLOGY_DATA_DIR` 이 없으면 전부 skip 된다.

```bash
ONTOLOGY_DATA_DIR=<원천 경로> uv run pytest -q tests/
```

## 배포 전제 (WORK-005 로 넘기는 것)

- **MCP 도구 서버는 자기 인증을 갖지 않는다.** SPEC-002 가 도구 서버 인증을 Out of scope 로
  두고 배포에 넘겼기 때문이다. 포트(기본 28081)가 노출되면 **비밀번호 없이** `query_layer` 로
  마스킹 브론즈 행을 읽을 수 있다 — 접속 게이트는 HTTP API 앞에만 선다.
  → 포트를 외부에 열지 말고, `ONTOLOGY_MCP_ALLOWED_HOSTS` 를 **명시 주입**한다.
- `mcp_allowed_hosts` 기본값 `["*"]` 는 SDK 의 DNS rebinding 보호를 무력화하는 값이면서
  실제로는 `Invalid Host header` 로 동작하지도 않는다. 배포·로컬 모두 명시가 필요하다.
  예: `ONTOLOGY_MCP_ALLOWED_HOSTS='["ontology-mcp:28081"]'`
- `ONTOLOGY_DEMO_PASSWORD` 미주입이면 인증 발급·검증이 **양쪽 다** 닫힌다(전 API 401).
  기본값이 없다는 것이 「아무나 들어온다」가 되지 않게 한 것이다.
