"""조회 서비스 — **도구(MCP)와 API 가 공유하는 유일한 구현**.

WORK-002 「Internal Interface Contract」의 귀착점이다. 화면용 집계 로직을 따로 만들지
않으므로 `/api/kpi/series` 와 도구 `query_kpi` 는 같은 함수를 지난다 — 두 수치가
어긋날 수 있는 자리 자체가 없다.

- `allowlist` — 조회 가능한 것의 단일 정의(테이블·필드·지표·상한)
- `queries` — 도구 4종의 조회 구현
- `glossary` — 용어·계산식·enum 사전
- `lineage` — 계층 목록과 컬럼 계보
- `monitoring` — KPI 카드·그래프·예보
- `errors` — Case Matrix 코드
"""

from . import allowlist, errors, glossary, lineage, monitoring, queries
from .db import open_serving_db

__all__ = [
    "allowlist", "errors", "glossary", "lineage", "monitoring", "queries",
    "open_serving_db",
]
