"""실호출 없는 고정 응답. 응답 모양은 2026-10-27 실호출(NOTES.md)과 같게, 값은 지어낸 것이다."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

import httpx
import pytest

from mfds_mcp.client import MfdsClient
from mfds_mcp.config import Config
from mfds_mcp.tools import Tools

FAKE_KEY = "FAKE+KEY/abc==TEST-ONLY-0123456789"


def ok(items: list | None, total: int | None = None, wrap: bool = False) -> dict:
    body: dict = {"pageNo": 1, "totalCount": len(items or []) if total is None else total, "numOfRows": 100}
    if items:
        body["items"] = [{"item": it} for it in items] if wrap else items
    return {"header": {"resultCode": "00", "resultMsg": "NORMAL SERVICE."}, "body": body}


NOT_REGISTERED = {
    "OpenAPI_ServiceResponse": {
        "cmmMsgHeader": {
            "errMsg": "SERVICE_KEY_IS_NOT_REGISTERED_ERROR",
            "returnAuthMsg": "등록되지 않은 서비스키",
            "returnReasonCode": "30",
        }
    }
}

THERMAGE = [
    {
        "ENTRPS": "가나다(주)",
        "TYPE_NAME": "Thermage Deep Skin외 4건",
        "PRDUCT_PRMISN_NO": "제허 00-001 호",
        "RTRCN_DSCTN_DIVS_CD": None,
        "RTRCN_DSCTN_DT": None,
        "MANUF_NM": None,
    },
    {
        "ENTRPS": "라마바(주)",
        "TYPE_NAME": "Thermage CPT",
        "PRDUCT_PRMISN_NO": "수허 00-002 호",
        "RTRCN_DSCTN_DIVS_CD": "2",
        "RTRCN_DSCTN_DT": "20200101",
        "MANUF_NM": "Example Medical, Inc.",
    },
    {
        "ENTRPS": "라마바(주)",
        "TYPE_NAME": "Thermage NXT",
        "PRDUCT_PRMISN_NO": "수허 00-003 호",
        "RTRCN_DSCTN_DIVS_CD": "5",
        "RTRCN_DSCTN_DT": "",
        "MANUF_NM": "Example Medical Inc.",
    },
]

COMPANY = [
    {
        "BSSH_NM": "가나다코리아(유)",
        "COB_FLAG_CODE_NAME": "수입업",
        "BRNO": "0000000000",
        "ENTP_ADDR": "어딘가 1",
        "SRVC_TRGT_INFO": "x",
        "SRVC_TRGT_ADD_INFO": "y",
    },
]

DRUGS = [
    {
        "ITEM_SEQ": "200000001",
        "ITEM_NAME": "가나주(성분A)",
        "ITEM_ENG_NAME": "Gana Inj",
        "ENTP_NAME": "(주)가나제약",
        "ENTP_ENG_NAME": "Gana Pharm",
        "CANCEL_DATE": None,
        "CANCEL_NAME": "정상",
    },
    {
        "ITEM_SEQ": "200000002",
        "ITEM_NAME": "가나주50단위(성분A)",
        "ITEM_ENG_NAME": None,
        "ENTP_NAME": "(주)가나제약",
        "ENTP_ENG_NAME": "Gana Pharm",
        "CANCEL_DATE": "20241213",
        "CANCEL_NAME": "취하",
    },
]

DRUG_DETAIL = {
    "ITEM_SEQ": "200000001",
    "ITEM_NAME": "가나주(성분A)",
    "MATERIAL_NAME": "총량 : 1바이알|분량 : 100",
    "PACK_UNIT": "1바이알/상자",
    "ITEM_ENG_NAME": "Gana Inj",
    "ENTP_ENG_NAME": "Gana Pharm",
    "CANCEL_DATE": None,
    "CANCEL_NAME": "정상",
}

MCPN = [
    {"PRDUCT": "가나주(성분A)", "MTRAL_NM": "성분A", "ITEM_SEQ": "200000001"},
    {"PRDUCT": "가나주(성분A)", "MTRAL_NM": "성분B", "ITEM_SEQ": "199999999"},
]

PWNM = [{"TYPE_NAME": "임부금기", "ITEM_SEQ": "200000009", "ITEM_NAME": "다라캡슐(성분C)", "PROHBT_CONTENT": "최기형성"}]


class Recorder:
    """보낸 요청을 기록하고 handler 로 응답한다."""

    def __init__(self, handler: Callable[[httpx.Request], httpx.Response]) -> None:
        self.handler = handler
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return self.handler(request)


def default_handler(request: httpx.Request) -> httpx.Response:
    path = request.url.path
    q = request.url.params
    if path.endswith("getMdlpPrdlstPrmisnItem05"):
        if q.get("PRDUCT_PRMISN_NO"):
            return httpx.Response(200, json=ok([THERMAGE[0]], wrap=True))
        if q.get("TYPE_NAME") == "Thermage":
            return httpx.Response(200, json=ok(THERMAGE, wrap=True))
        return httpx.Response(200, json=ok(None, 0))
    if path.endswith("getMdeqMnftPrmsnDtlInq01"):
        return httpx.Response(200, json=ok(COMPANY))
    if path.endswith("getDrugPrdtPrmsnInq08"):
        return httpx.Response(200, json=ok(DRUGS))
    if path.endswith("getDrugPrdtPrmsnDtlInq08"):
        return httpx.Response(200, json=ok([DRUG_DETAIL]))
    if path.endswith("getDrugPrdtMcpnDtlInq08"):
        return httpx.Response(200, json=ok(MCPN))
    if path.endswith("getPwnmTabooInfoList03"):
        return httpx.Response(200, json=ok(PWNM))
    return httpx.Response(404, text="API not found")


@pytest.fixture
def make_tools(tmp_path: Path):
    def _make(handler=default_handler, key: str | None = FAKE_KEY, **cfg):
        rec = Recorder(handler)
        config = Config(api_key=key, cache_dir=tmp_path / "cache", **cfg)
        client = MfdsClient(config, transport=httpx.MockTransport(rec))
        return Tools(client), rec, config

    return _make


def dump_dir(path: Path) -> str:
    """폴더 안 파일 이름 + 내용 전부(키 grep 용)."""
    out = []
    for p in sorted(path.rglob("*")):
        out.append(p.name)
        if p.is_file():
            out.append(p.read_text(encoding="utf-8"))
    return "\n".join(out)


__all__ = ["FAKE_KEY", "NOT_REGISTERED", "dump_dir", "json", "ok"]
