"""빌드 CLI — 단계별 실행과 게이트 단독 재실행.

WORK-005 의 전건 재실행이 이 인터페이스를 그대로 부른다. 게이트 실패는 exit code ≠ 0 이고
SPEC-001 §4 Case Matrix 의 코드와 기대·실측값을 로그로 남긴다.

    uv run python -m build all
    uv run python -m build bronze --db /path/ontology_demo.db
    uv run python -m build gate1
"""

from __future__ import annotations

import argparse
import datetime
import sys

from config import settings

from . import gates, gold, load_bronze, masking, ontology, silver
from .errors import BuildError
from db.connection import atomic, connect
from db.schema import bootstrap

STAGES = ["bootstrap", "bronze", "views", "silver", "gold", "ontology",
          "all", "gate1", "gate2", "gate3"]


def _bootstrap(conn) -> None:
    bootstrap(conn)
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'bronze_%' ORDER BY name"
    )]
    print(f"부트스트랩 완료 — bronze 테이블 {len(tables)}개")
    for t in tables:
        print(f"  {t}")


def _bronze(conn) -> None:
    load_bronze.report(load_bronze.load(conn))


def _views(conn) -> None:
    print("마스킹 뷰:", ", ".join(masking.build(conn)))


def _silver(conn) -> None:
    result = silver.build(conn)
    r = result["reservations"]
    print(f"silver_reservations: 브론즈 {r['bronze']:,} = 실버 {r['silver']:,} "
          f"+ 제외 {r['filter_excluded']} + 중복 {r['dedup_removed']:,} "
          f"→ {'OK' if r['reconciled'] else 'MISMATCH'}")
    rv = result["reviews"]
    print(f"silver_reviews: {rv['silver']:,}건 (마스킹 적용 {rv['masked_bodies']}건, "
          f"실명 토큰 {rv['name_tokens']}종)")
    # 미달이면 여기 오지 못한다 — `AGREEMENT_BELOW_THRESHOLD` 로 빌드가 이미 멈춘다
    print(f"  강남언니 정합률(±0.5): {rv['gu_match']}/{rv['gu_total']} = "
          f"{rv['gu_agreement']:.1%} (기준 {rv['gu_threshold']:.0%}) → 통과 "
          f"· 예외 큐 {rv['exception_queue']}건")
    for row in result["catalog_recon"]:
        print(f"  {row['table']}: 브론즈 {row['bronze']:,} = 실버 {row['silver']:,} "
              f"+ 제외 {row['filter_excluded']:,} "
              f"→ {'OK' if row['reconciled'] else 'MISMATCH'}")
    for table, n in result["counts"].items():
        print(f"{table}: {n:,} rows")


def _gold(conn) -> None:
    result = gold.build(conn)
    for table, n in result["counts"].items():
        print(f"{table}: {n:,} rows")
    for metric, (direction, warn, alert) in result["status_bounds"].items():
        print(f"  status {metric}: 방향={direction} 주의경계={warn} 경고경계={alert}")


def _ontology(conn) -> None:
    result = ontology.load(conn)
    print(f"ontology_nodes: {result['nodes']} · ontology_edges: {result['edges']} "
          f"· 고아 {result['orphans']}")
    print(f"  node_type: {result['node_type_counts']}")
    print(f"  판정: {result['verdict_counts']}")
    print(f"  lag 표기 → lag_days: {result['lag_forms']}")
    print(f"  SPEC-001 §4 25종 1:1 대조: {result['spec_1to1']}")


def _gate1(conn) -> None:
    load_bronze.report(load_bronze.gate1(conn))


def _gate2(conn) -> None:
    result = gates.gate2(conn)
    print(f"게이트 2 — 빌드 재현 대조 {result['checks']}항 전항 일치")
    for name, got in result["measured"].items():
        print(f"  {name}: {got:,}")
    print(f"  [OQ-3 실측] gold_kpi_monthly {result['gold_kpi_monthly']}행 · "
          f"gold_retention_monthly {result['gold_retention_monthly']}행")
    parity = gates.csv_parity(conn)
    print(f"  기존 CSV 산출물 대조: {parity['tables']}테이블 "
          f"{parity['cells']:,}셀 불일치 {parity['diffs']}건")


def _gate3(conn) -> None:
    result = gates.gate3(conn)
    print(f"게이트 3 — 마스킹 뷰 원값 검출 {result['leaks']}건 "
          f"(vegas {result['vegas_rows']:,}행 · 리뷰 {result['review_rows']:,}행 전수 스캔)")


def _all(conn) -> None:
    """전 계층 빌드 + 게이트 1·2·3 — **전부 통과할 때만 채택한다.**

    SPEC-001 §5 「게이트는 전부 통과해야 산출물을 채택한다」 · Case Matrix
    `REBUILD_MISMATCH` → 「산출물 미채택, **이전 DB 유지**」.

    한 트랜잭션으로 감싸므로 게이트 2·3 이 실패하면 실버·골드·온톨로지 산출물이
    **전부 되감기고 이전 DB 상태가 그대로 남는다.** 게이트가 탐지만 하고 채택을 막지
    못하면 게이트가 아니다 — 실패한 산출물이 `connect_ro()` 소비자에게 보이면 안 된다.
    """
    _bootstrap(conn)
    with atomic(conn, "adopt"):
        for step in (_bronze, _silver, _views, _gold, _ontology, _gate1, _gate2, _gate3):
            print(f"\n--- {step.__name__.lstrip('_')} ---")
            step(conn)
        _stamp_build(conn)
    print("\n전 게이트 통과 — 산출물 채택")


def _stamp_build(conn) -> None:
    """빌드 표식 — 채택 트랜잭션 **안에서** 찍는다.

    게이트가 하나라도 실패하면 이 줄에 닿지 못하고, 닿았더라도 롤백에 함께 되감긴다.
    그래서 표식의 존재가 곧 「전 게이트를 통과한 산출물」이다. 소비자(`connect_ro`)가
    이것으로 미빌드·실패빌드를 정상 서빙과 구분한다.
    """
    daily = conn.execute("SELECT COUNT(*) FROM gold_kpi_daily").fetchone()[0]
    nodes = conn.execute("SELECT COUNT(*) FROM ontology_nodes").fetchone()[0]
    edges = conn.execute("SELECT COUNT(*) FROM ontology_edges").fetchone()[0]
    built_at = datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")
    conn.execute("DELETE FROM build_meta")
    conn.execute(
        "INSERT INTO build_meta (id, built_at, gates_passed, daily_rows, node_count, edge_count) "
        "VALUES (1, ?, ?, ?, ?, ?)",
        (built_at, "1,2,3", daily, nodes, edges),
    )
    print(f"\n빌드 표식: built_at={built_at} · 게이트 1,2,3 통과 "
          f"· 일별 {daily}행 · 노드 {nodes} · 엣지 {edges}")


#: DB 를 바꾸는 단계. 이것들을 **단독으로** 돌리면 전 게이트 통과 보장이 깨지므로
#: 빌드 표식을 무효화한다 — 게이트 없이 골드를 다시 쓴 뒤에도 표식이 「1,2,3 통과」라고
#: 말하면 **표식이 거짓을 말하는 유일한 경로**가 된다(WORK-002 검수 W5).
#: 게이트 단독 재실행(`gate1`~`gate3`)은 읽기만 하므로 표식을 건드리지 않는다.
MUTATING_STAGES = frozenset({"bootstrap", "bronze", "views", "silver", "gold", "ontology"})


def _invalidate_build_stamp(conn, stage: str) -> None:
    """단계 단독 실행 시 표식을 지운다 — 채택 경로는 `all` 하나뿐이다.

    핸들러보다 **먼저** 지운다. 단계가 롤백돼도 표식은 돌아오지 않는데, 그 방향이 안전하다 —
    「서빙하지 않음」으로 틀리는 편이 「게이트 안 거친 산출물을 서빙함」으로 틀리는 것보다 낫다.
    표식을 되살리려면 `all` 로 전 게이트를 다시 통과시켜야 한다.
    """
    has_table = conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='build_meta'"
    ).fetchone()[0]
    if not has_table:
        return
    removed = conn.execute("DELETE FROM build_meta").rowcount
    if removed:
        print(f"\n빌드 표식 무효화 — 단계 단독 실행({stage})은 게이트를 거치지 않는다. "
              "서빙하려면 `build all` 로 전 게이트를 다시 통과시켜야 한다")


HANDLERS = {
    "bootstrap": [_bootstrap],
    "bronze": [_bronze],
    "views": [_views],
    "silver": [_silver],
    "gold": [_gold],
    "ontology": [_ontology],
    "gate1": [_gate1],
    "gate2": [_gate2],
    "gate3": [_gate3],
    "all": [_all],
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m build",
        description="온톨로지 데모 데이터 빌드 — 브론즈 적재부터 온톨로지까지 한 DB",
    )
    parser.add_argument("stage", choices=STAGES, help="실행할 단계 또는 게이트")
    parser.add_argument("--db", default=None, help="산출 DB 경로 (기본: ONTOLOGY_DB_PATH)")
    args = parser.parse_args(argv)

    conn = connect(args.db)
    print(f"DB: {args.db or settings.resolved_db_path}")
    print(f"원천: {settings.data_dir}")
    try:
        if args.stage in MUTATING_STAGES:
            _invalidate_build_stamp(conn, args.stage)
        for handler in HANDLERS[args.stage]:
            print(f"\n--- {handler.__name__.lstrip('_')} ---")
            handler(conn)
    except BuildError as exc:
        print(f"\n{exc.render()}", file=sys.stderr)
        return 1
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
