"""실호출 확인 — 키가 있을 때 엔드포인트마다 1~2회만 부른다(캐시를 건너뛰고 새로 받는다).

    uv run python scripts/smoke.py

출력에는 건수와 몇 개 필드만 찍는다. 키는 찍지 않는다.
"""

from __future__ import annotations

import sys

from mfds_mcp.client import MfdsClient, MfdsError
from mfds_mcp.config import Config
from mfds_mcp.tools import Tools

FAILS: list[str] = []


def check(label: str, cond: bool, info: str = "") -> None:
    print(f"[{'OK ' if cond else 'FAIL'}] {label} {info}")
    if not cond:
        FAILS.append(label)


def run(label: str, fn):
    try:
        return fn()
    except MfdsError as exc:
        print(f"[FAIL] {label} → {exc.code} {exc.detail}")
        FAILS.append(label)
        return None


def main() -> int:
    config = Config.load()
    if not config.api_key:
        print("MFDS_API_KEY 가 없다 — .env 를 채운 뒤 다시 실행한다.")
        return 2
    t = Tools(MfdsClient(config))

    # 의료기기 품목허가 (2회: 새로 받기 + 캐시)
    r = run("device_search", lambda: t.device_search(type_name="Thermage", no_cache=True))
    if r:
        check(
            "device_search Thermage",
            r["total_count"] >= 1 and r["returned"] >= 0,
            f"total={r['total_count']} returned={r['returned']} filtered={r['filtered_out_cancelled']}",
        )
        check("unwrapped items", all("item" not in i for i in r["items"]))
        r2 = t.device_search(type_name="Thermage")
        check("second call from cache", r2["from_cache"] is True)
        if r["items"]:
            no = r["items"][0]["PRDUCT_PRMISN_NO"]
            d = run("device_detail", lambda: t.device_detail(no, no_cache=True))
            if d:
                check("device_detail 1건", d["returned"] == 1, d["items"][0].get("TYPE_NAME", ""))

    # 의료기기 업체 (1회)
    c = run("device_company", lambda: t.device_company("솔타", rows=5, no_cache=True))
    if c:
        check(
            "device_company",
            c["total_count"] >= 1,
            f"total={c['total_count']} 첫 행={c['items'][0].get('COB_FLAG_CODE_NAME') if c['items'] else None}",
        )
        check("주소 필드 제외", all("ENTP_ADDR" not in i for i in c["items"]))

    # 의약품 (2~3회)
    s = run("drug_search", lambda: t.drug_search(item_name="나보타", no_cache=True))
    if s:
        first = s["items"][0] if s["items"] else {}
        check(
            "drug_search 나보타",
            s["total_count"] >= 1,
            f"total={s['total_count']} {first.get('ITEM_ENG_NAME')} / {first.get('ENTP_ENG_NAME')} / {first.get('CANCEL_NAME')}",
        )
        if first:
            d = run("drug_detail", lambda: t.drug_detail(first["ITEM_SEQ"], include_ingredients=True, no_cache=True))
            if d:
                it = d["items"][0]
                check("drug_detail 규격", bool(it.get("MATERIAL_NAME")) and bool(it.get("PACK_UNIT")), f"PACK_UNIT={it.get('PACK_UNIT')}")
                check("drug_detail 주성분", d["ingredients"]["returned"] >= 1, f"{[i.get('MTRAL_NM') for i in d['ingredients']['items']]}")

    # DUR (1~2회)
    p = run("dur pregnancy", lambda: t.dur_check("pregnancy", item_name="이소트레티노인", rows=5, no_cache=True))
    if p:
        check(
            "DUR 임부금기 이소트레티노인",
            p["total_count"] >= 1,
            f"total={p['total_count']} {p['items'][0].get('PROHBT_CONTENT', '')[:30] if p['items'] else ''}",
        )
    u = run("dur usjnt", lambda: t.dur_check("usjnt", item_name="이소트레티노인", rows=1, no_cache=True))
    if u:
        check("DUR 병용금기 이소트레티노인", u["total_count"] >= 1, f"total={u['total_count']}")

    st = t.status()
    print("status:", [(s["service"], s["state"]) for s in st["services"]], "calls_today", st["calls_today"])
    print("FAIL:", FAILS if FAILS else "없음")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
