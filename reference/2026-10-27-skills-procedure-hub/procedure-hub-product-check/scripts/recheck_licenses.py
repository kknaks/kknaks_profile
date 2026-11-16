"""정기 점검 — 원장에 연결된 허가 전부의 지금 상태를 다시 조회해 변경분만 낸다.

읽기만 한다. 원장(step1-products.json)은 고치지 않는다 — 결과는 결정 목록의 재료다.

    # MFDS MCP 의 가상환경 python 으로 돌린다(httpx · mfds_mcp 를 그대로 쓴다)
    MFDS=reference/2026-10-27-mfds-mcp
    $MFDS/.venv/bin/python <이 파일> \
        --ledger orchestration/work/phub-recommend/step1-products.json \
        --mfds-dir $MFDS --out <scratchpad>/recheck.json [--limit 10] [--ids M9-1-3,M1-2-3] [--no-emedi]

조회:
- 의료기기 — 식약처 품목허가 상세(getMdlpPrdlstPrmisnItem05, PRDUCT_PRMISN_NO) → 취소 · 취하(RTRCN_DSCTN_*) ·
  품목일련번호 MDEQ_PRDLST_SN → emedi 품목 상세 POST(meddevItemSeq) → xprtppYn(수출용에 한함) · 취소취하 · 유효기간
- 의약품 — 식약처 의약품 허가 상세(getDrugPrdtPrmsnDtlInq08, item_seq) → CANCEL_NAME/DATE · 품목명 「(수출용)」

키는 MFDS MCP 의 .env 에서 mfds_mcp.Config 가 읽는다. 이 스크립트는 키 값을 출력하지 않는다.
"""

from __future__ import annotations

import argparse
import http.cookiejar
import json
import re
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

EMEDI_PAGE = "https://emedi.mfds.go.kr/search/data/MNU20237"
EMEDI_ITEM = "https://emedi.mfds.go.kr/search/data/item"
UA = "Mozilla/5.0"


# ---- 허가번호 ------------------------------------------------------------
def api_license_no(no: str) -> str:
    """원장 표기(「제허20-527호」 · 「제허 20-527 호」) → 식약처 API 표기 「제허 20-527 호」."""
    m = re.match(r"^\s*(\D+?)\s*(\d+\s*-\s*\d+)\s*호?\s*$", no)
    if not m:
        return no.strip()
    return f"{m.group(1)} {m.group(2).replace(' ', '')} 호"


def license_kind(lic: dict) -> str:
    key = lic.get("key") or ""
    if key.startswith("drug:") or lic.get("kind") == "의약품":
        return "drug"
    return "device"


# ---- emedi ---------------------------------------------------------------
class Emedi:
    def __init__(self) -> None:
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
        self.calls = 0
        self._primed = False

    def _prime(self) -> None:
        if not self._primed:
            self.opener.open(urllib.request.Request(EMEDI_PAGE, headers={"User-Agent": UA}), timeout=30).read()
            self._primed = True

    def item(self, seq: str) -> dict:
        self._prime()
        body = {
            "chkGroup1": "", "meddevItemSeq": seq, "typeName": "", "isUdiCodeSearch": "N", "udidiCode": "",
            "udiIsFirst": "Y", "searchUdiCode": "", "seq": "", "seqGroup": "",
        }
        req = urllib.request.Request(
            EMEDI_ITEM,
            data=json.dumps(body).encode(),
            headers={
                "User-Agent": UA, "Referer": EMEDI_PAGE, "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/json;charset=utf-8",
            },
            method="POST",
        )
        self.calls += 1
        raw = self.opener.open(req, timeout=40).read()
        time.sleep(0.3)  # 공공 사이트 — 천천히
        return (json.loads(raw) or {}).get("mebItemInfo") or {}


# ---- 판정 ----------------------------------------------------------------
def valid_end(valid: str | None) -> str | None:
    """「2021-08-19 ~ 2031-08-18」 → 「2031-08-18」."""
    if not valid or "~" not in valid:
        return None
    end = valid.split("~", 1)[1].strip()
    return end or None


def check_device(tools, emedi: Emedi | None, lic: dict, today: str) -> dict:
    sent = api_license_no(lic["license_no"])
    res = tools.device_detail(sent, no_cache=True)
    it = res["items"][0]
    now = {
        "api_license_no": it.get("PRDUCT_PRMISN_NO"),
        "cancelled": bool(it.get("is_cancelled")),
        "cancel_code": it.get("RTRCN_DSCTN_DIVS_CD"),
        "cancel_date": it.get("RTRCN_DSCTN_DT"),
        "holder": it.get("ENTRPS"),
        "serial": it.get("MDEQ_PRDLST_SN"),
    }
    src = [f"식약처 의료기기 품목허가 상세 getMdlpPrdlstPrmisnItem05 PRDUCT_PRMISN_NO={sent}"]
    flags = []
    if now["cancelled"]:
        flags.append("취소·취하")
    if emedi and now["serial"]:
        m = emedi.item(str(now["serial"]))
        now.update({
            "xprtppYn": m.get("xprtppYn"),
            "remark": m.get("remark"),
            "emedi_cancel": m.get("cancelwithdwCode"),
            "emedi_cancel_date": m.get("cancelwithdwDate"),
            "valid": m.get("validDate"),
            "model": m.get("mebTypeName"),
        })
        src.append(f"emedi 품목 상세 POST {EMEDI_ITEM} meddevItemSeq={now['serial']}")
        if m.get("xprtppYn") == "예":
            flags.append("수출용")
        # cancelwithdwCode 는 「아니오」 / 「취소」 / 「취하」 로 온다(10-28 실호출 — 제허 23-60 「취하」)
        if (m.get("cancelwithdwCode") or "아니오") != "아니오" and "취소·취하" not in flags:
            flags.append("취소·취하")
        end = valid_end(m.get("validDate"))
        if end and end < today:
            flags.append("유효기간 만료")
    return {"now": now, "flags": flags, "source": src}


def check_drug(tools, lic: dict) -> dict:
    seq = (lic.get("key") or "").removeprefix("drug:") or lic["license_no"]
    res = tools.drug_detail(seq, no_cache=True)
    it = res["items"][0]
    name = it.get("ITEM_NAME") or ""
    eng = it.get("ITEM_ENG_NAME") or ""
    now = {
        "item_name": name,
        "cancelled": bool(it.get("is_cancelled")),
        "cancel_name": it.get("CANCEL_NAME"),
        "cancel_date": it.get("CANCEL_DATE"),
        "holder": it.get("ENTP_NAME"),
    }
    flags = []
    if now["cancelled"]:
        flags.append("취소·취하")
    if "(수출용)" in name or "for export" in eng.lower():
        flags.append("수출용")
    return {"now": now, "flags": flags, "source": [f"식약처 의약품 허가 상세 getDrugPrdtPrmsnDtlInq08 item_seq={seq}"]}


# ---- main ----------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", required=True, help="step1-products.json")
    ap.add_argument("--mfds-dir", required=True, help="reference/2026-10-27-mfds-mcp (src · .env 를 여기서 읽는다)")
    ap.add_argument("--out", required=True, help="변경분 JSON 을 쓸 곳(원장 폴더가 아닌 곳)")
    ap.add_argument("--limit", type=int, default=0, help="앞에서 N 행만(시험용). 0 = 전부")
    ap.add_argument("--ids", default="", help="ledger_id 쉼표 목록 — 이 행만")
    ap.add_argument("--no-emedi", action="store_true", help="emedi 상세(xprtppYn) 조회를 건너뛴다")
    args = ap.parse_args()

    mfds_dir = Path(args.mfds_dir).resolve()
    sys.path.insert(0, str(mfds_dir / "src"))
    from mfds_mcp.client import MfdsClient, MfdsError  # noqa: E402
    from mfds_mcp.config import Config  # noqa: E402
    from mfds_mcp.tools import Tools  # noqa: E402

    config = Config.load(env_file=mfds_dir / ".env")
    if not config.api_key:
        print("MFDS_API_KEY 가 없다 — <mfds-dir>/.env 를 채운다(값은 출력하지 않는다).", file=sys.stderr)
        return 2
    client = MfdsClient(config)
    tools = Tools(client)
    emedi = None if args.no_emedi else Emedi()

    ledger = json.loads(Path(args.ledger).read_text(encoding="utf-8"))
    rows = [r for r in ledger["items"] if r.get("active")]
    if args.ids:
        want = {x.strip() for x in args.ids.split(",") if x.strip()}
        rows = [r for r in rows if r["ledger_id"] in want]
    rows = [r for r in rows if r["4_license"].get("licenses")]
    if args.limit:
        rows = rows[: args.limit]

    today = date.today().isoformat()
    changes, unchanged, errors = [], [], []
    n_lic = 0
    for r in rows:
        name = r["2_names"]["display_name"]
        for lic in r["4_license"]["licenses"]:
            n_lic += 1
            base = {
                "ledger_id": r["ledger_id"], "display_name": name, "license_no": lic["license_no"],
                "kind": license_kind(lic), "ledger_state": lic.get("state"),
                "ledger_status": r["4_license"]["status"], "recommendable": r["4_license"]["recommendable"],
            }
            try:
                got = check_drug(tools, lic) if base["kind"] == "drug" else check_device(tools, emedi, lic, today)
            except MfdsError as e:  # filter_ignored(0건 · 여러 건) · 한도 · 키 오류
                errors.append({**base, "error": e.to_dict()})
                continue
            except Exception as e:  # emedi 네트워크 등
                errors.append({**base, "error": {"code": type(e).__name__, "message": str(e)[:200]}})
                continue
            row = {**base, **got}
            (changes if got["flags"] else unchanged).append(row)

    out = {
        "generated_at": today,
        "ledger": str(args.ledger),
        "scope": {"rows": len(rows), "licenses": n_lic, "filter": {"limit": args.limit, "ids": args.ids, "emedi": emedi is not None}},
        "calls": {"emedi": emedi.calls if emedi else 0},
        "summary": {"changed": len(changes), "unchanged": len(unchanged), "errors": len(errors)},
        "rule": "flags 가 있는 허가 = 결정 목록 후보. 취소·취하 · 유효기간 만료 → history · 수출용 → reference. "
                "행에 정상 허가가 남지 않으면 상태 「허가 취소(이력)」 · 추천 제외 — 반영은 승인 뒤(SKILL.md 4)",
        "changes": changes,
        "unchanged": [{k: v for k, v in u.items() if k in ("ledger_id", "display_name", "license_no", "kind")} for u in unchanged],
        "errors": errors,
    }
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    client.close()
    print(f"rows {len(rows)} · licenses {n_lic} · changed {len(changes)} · unchanged {len(unchanged)} · errors {len(errors)} → {args.out}")
    for c in changes:
        print(f"  {c['ledger_id']} {c['display_name']} {c['license_no']} — {' · '.join(c['flags'])}")
    for e in errors:
        print(f"  ERROR {e['ledger_id']} {e['display_name']} {e['license_no']} — {e['error'].get('code')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
