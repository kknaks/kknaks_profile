from __future__ import annotations

import asyncio
import json
import logging

import httpx
import pytest
from conftest import FAKE_KEY, NOT_REGISTERED, dump_dir, ok

from mfds_mcp.client import MfdsError, unwrap_items
from mfds_mcp.config import Config, read_env_file


def _err(excinfo) -> str:
    return excinfo.value.code


# ---- 응답 모양 ----------------------------------------------------------
def test_unwrap_items_shapes():
    assert unwrap_items({"items": [{"item": {"A": 1}}]}) == [{"A": 1}]
    assert unwrap_items({"items": [{"A": 1}]}) == [{"A": 1}]
    assert unwrap_items({}) == []
    assert unwrap_items({"items": {"item": {"A": 1}}}) == [{"A": 1}]
    assert unwrap_items({"items": {"item": [{"A": 1}, {"A": 2}]}}) == [{"A": 1}, {"A": 2}]


# ---- S-1 ----------------------------------------------------------------
def test_device_search_filters_cancelled_and_caches(make_tools):
    tools, rec, config = make_tools()
    r = tools.device_search(type_name="Thermage")
    assert (r["total_count"], r["returned"], r["filtered_out_cancelled"]) == (3, 1, 2)
    assert r["from_cache"] is False
    item = r["items"][0]
    assert "item" not in item and item["TYPE_NAME"].startswith("Thermage Deep")
    assert item["is_cancelled"] is False
    assert item["source"]["operation"] == "getMdlpPrdlstPrmisnItem05"
    assert "serviceKey" not in item["source"]["query"]
    assert tools.client.calls.total() == 1

    r2 = tools.device_search(type_name="Thermage")
    assert r2["from_cache"] is True
    assert len(rec.requests) == 1 and tools.client.calls.total() == 1

    # 캐시는 원본 그대로({"item": …}) · include_cancelled 는 캐시 키에 안 들어간다
    r3 = tools.device_search(type_name="Thermage", include_cancelled=True)
    assert r3["from_cache"] is True and r3["returned"] == 3 and r3["filtered_out_cancelled"] == 0
    cached = [p for p in (config.cache_dir).glob("*_p1.json")]
    assert len(cached) == 1
    raw = json.loads(cached[0].read_text(encoding="utf-8"))
    assert "item" in raw["response"]["body"]["items"][0]


def test_device_search_case_sensitive_empty_not_error(make_tools):
    tools, rec, _ = make_tools()
    r = tools.device_search(type_name="thermage")
    assert r["total_count"] == 0 and r["items"] == [] and r["returned"] == 0
    assert rec.requests[0].url.params["TYPE_NAME"] == "thermage"  # 그대로 보낸다


def test_device_search_uppercase_params_and_one_request(make_tools):
    tools, rec, _ = make_tools()
    tools.device_search(type_name="Thermage", entrps=" 가나 ", prduct="조직")
    assert len(rec.requests) == 1
    req = rec.requests[0]
    assert req.url.path.endswith("/MdlpPrdlstPrmisnInfoService06/getMdlpPrdlstPrmisnItem05")
    params = dict(req.url.params)
    assert params["TYPE_NAME"] == "Thermage" and params["ENTRPS"] == "가나" and params["PRDUCT"] == "조직"
    assert "entrps" not in params and params["type"] == "json"


def test_device_search_requires_filter(make_tools):
    tools, _, _ = make_tools()
    with pytest.raises(MfdsError) as e:
        tools.device_search(type_name="  ")
    assert _err(e) == "invalid_input"
    with pytest.raises(MfdsError) as e:
        tools.device_search(type_name="x", rows=101)
    assert _err(e) == "invalid_input"
    with pytest.raises(MfdsError) as e:
        tools.device_search(type_name="x", page=0)
    assert _err(e) == "invalid_input"


def test_all_pages_truncates(make_tools):
    def handler(request):
        page = int(request.url.params["pageNo"])
        return httpx.Response(200, json=ok([{"TYPE_NAME": f"M{page}"}], total=5, wrap=True))

    tools, rec, _ = make_tools(handler, max_pages=3)
    r = tools.device_search(type_name="M", rows=1, all_pages=True)
    assert r["truncated"] is True and r["returned"] == 3 and len(rec.requests) == 3


# ---- T-2 ----------------------------------------------------------------
def test_device_detail_single_and_filter_ignored(make_tools):
    tools, rec, _ = make_tools()
    r = tools.device_detail("제허 00-001 호")
    assert r["returned"] == 1 and rec.requests[0].url.params["PRDUCT_PRMISN_NO"] == "제허 00-001 호"

    def ignored(request):
        return httpx.Response(200, json=ok([THERMAGE_ROW], total=214377, wrap=True))

    tools2, _, _ = make_tools(ignored)
    with pytest.raises(MfdsError) as e:
        tools2.device_detail("x")
    assert _err(e) == "filter_ignored" and e.value.detail["total_count"] == 214377


THERMAGE_ROW = {"TYPE_NAME": "x"}


# ---- T-3 ----------------------------------------------------------------
def test_company_excludes_address(make_tools):
    tools, rec, _ = make_tools()
    r = tools.device_company("가나다")
    item = r["items"][0]
    assert item["COB_FLAG_CODE_NAME"] == "수입업"
    assert not any(k.startswith(("ENTP_ADDR", "SRVC_TRGT_")) for k in item)
    assert "is_cancelled" not in item
    assert rec.requests[0].url.params["BSSH_NM"] == "가나다"


# ---- 의약품 ------------------------------------------------------------
def test_drug_search_lowercase_and_cancel(make_tools):
    tools, rec, _ = make_tools()
    r = tools.drug_search(item_name="가나", entp_name="가나제약")
    params = dict(rec.requests[0].url.params)
    assert params["item_name"] == "가나" and params["entp_name"] == "가나제약"
    assert rec.requests[0].url.path.endswith("/DrugPrdtPrmsnInfoService08/getDrugPrdtPrmsnInq08")
    assert (r["returned"], r["filtered_out_cancelled"]) == (1, 1)
    assert r["items"][0]["ENTP_ENG_NAME"] == "Gana Pharm" and r["items"][0]["ITEM_ENG_NAME"] == "Gana Inj"
    r2 = tools.drug_search(item_name="가나", entp_name="가나제약", include_cancelled=True)
    assert [i["is_cancelled"] for i in r2["items"]] == [False, True]


def test_drug_detail_with_ingredients(make_tools):
    tools, rec, _ = make_tools()
    r = tools.drug_detail("200000001", include_ingredients=True)
    item = r["items"][0]
    assert item["MATERIAL_NAME"].startswith("총량") and item["PACK_UNIT"] == "1바이알/상자"
    assert rec.requests[0].url.params["item_seq"] == "200000001"
    assert rec.requests[1].url.params["Prduct"] == "가나주(성분A)"
    assert [i["MTRAL_NM"] for i in r["ingredients"]["items"]] == ["성분A"]  # ITEM_SEQ 로 골라낸다


# ---- DUR ----------------------------------------------------------------
def test_dur_check(make_tools):
    tools, rec, _ = make_tools()
    r = tools.dur_check("pregnancy", item_name="다라")
    assert r["kind_name"] == "임부금기" and r["returned"] == 1
    assert rec.requests[0].url.path.endswith("/DURPrdlstInfoService03/getPwnmTabooInfoList03")
    assert rec.requests[0].url.params["itemName"] == "다라"
    with pytest.raises(MfdsError) as e:
        tools.dur_check("nope", item_name="x")
    assert _err(e) == "invalid_input"
    with pytest.raises(MfdsError) as e:
        tools.dur_check("usjnt")
    assert _err(e) == "invalid_input"


def test_dur_not_registered(make_tools):
    tools, _, _ = make_tools(lambda r: httpx.Response(403, json=NOT_REGISTERED))
    with pytest.raises(MfdsError) as e:
        tools.dur_check("usjnt", item_name="x")
    assert _err(e) == "key_not_registered"
    assert e.value.detail["errMsg"] == "SERVICE_KEY_IS_NOT_REGISTERED_ERROR"
    st = tools.status()
    dur = [s for s in st["services"] if s["service"] == "DURPrdlstInfoService03"][0]
    assert dur["state"] == "not_registered"


# ---- 에러 구분 ----------------------------------------------------------
@pytest.mark.parametrize(
    ("response", "code"),
    [
        (httpx.Response(403, json=NOT_REGISTERED), "key_not_registered"),
        (
            httpx.Response(
                200,
                text="<OpenAPI_ServiceResponse><cmmMsgHeader><errMsg>SERVICE ERROR</errMsg>"
                "<returnAuthMsg>SERVICE_KEY_IS_NOT_REGISTERED_ERROR</returnAuthMsg>"
                "<returnReasonCode>30</returnReasonCode></cmmMsgHeader></OpenAPI_ServiceResponse>",
            ),
            "key_not_registered",
        ),
        (httpx.Response(200, json={"header": {"resultCode": "03", "resultMsg": "NODATA"}}), "api_error"),
        (httpx.Response(404, text="API not found"), "service_not_found"),
        (httpx.Response(500, text="Unexpected errors"), "api_error"),
        (httpx.Response(401, text="Unauthorized"), "api_error"),
    ],
)
def test_error_mapping(make_tools, response, code):
    tools, _, config = make_tools(lambda r: response)
    with pytest.raises(MfdsError) as e:
        tools.device_search(type_name="x")
    assert _err(e) == code
    assert not list(config.cache_dir.glob("*_p*.json"))  # 에러는 캐시하지 않는다


def test_missing_key(make_tools):
    tools, rec, _ = make_tools(key=None)
    for call in (
        lambda: tools.device_search(type_name="x"),
        lambda: tools.drug_search(item_name="x"),
        lambda: tools.dur_check("usjnt", item_name="x"),
    ):
        with pytest.raises(MfdsError) as e:
            call()
        assert _err(e) == "missing_key"
    assert rec.requests == []
    st = tools.status(refresh=True)
    assert st["key_present"] is False and all(s["state"] == "unknown" for s in st["services"])


def test_daily_limit(make_tools):
    tools, rec, _ = make_tools(daily_limit=1)
    tools.device_search(type_name="Thermage")
    assert tools.device_search(type_name="Thermage")["from_cache"] is True  # 캐시는 계속 답한다
    with pytest.raises(MfdsError) as e:
        tools.device_search(type_name="Other")
    assert _err(e) == "daily_limit_reached"
    assert len(rec.requests) == 1


def test_status_counts(make_tools):
    tools, _, _ = make_tools()
    tools.device_search(type_name="Thermage")
    st = tools.status()
    assert st["key_present"] is True and st["calls_today"] == 1 and st["cache"]["entries"] == 1
    item = [s for s in st["services"] if s["service"] == "MdlpPrdlstPrmisnInfoService06"][0]
    assert item["state"] == "usable"


# ---- 키 누출 (W-13) -----------------------------------------------------
def test_key_never_leaks(make_tools, caplog, capsys):
    caplog.set_level(logging.DEBUG)

    def echo_key(request):  # 서버가 질의를 그대로 되돌려주는 최악의 경우
        return httpx.Response(500, text=f"bad request: {request.url}")

    def boom(request):
        raise httpx.ConnectError(f"cannot connect {request.url}", request=request)

    collected = []
    for handler in (echo_key, boom, lambda r: httpx.Response(403, json=NOT_REGISTERED)):
        tools, rec, config = make_tools(handler)
        with pytest.raises(MfdsError) as e:
            tools.device_search(type_name="Thermage")
        collected.append(json.dumps(e.value.to_dict(), ensure_ascii=False))
        collected.append(str(e.value) + repr(e.value))
        collected.append(repr(config))
        if config.cache_dir.exists():
            collected.append(dump_dir(config.cache_dir))
        assert FAKE_KEY in str(rec.requests[0].url.params.get("serviceKey"))  # 실제로는 보냈다
    out = capsys.readouterr()
    blob = "\n".join([*collected, caplog.text, out.out, out.err])
    from urllib.parse import quote, quote_plus

    for form in (FAKE_KEY, quote(FAKE_KEY, safe=""), quote_plus(FAKE_KEY)):
        assert form not in blob
    assert "upstream_unreachable" in blob


def test_mcp_tool_error_has_code_and_no_key(make_tools, tmp_path):
    from mfds_mcp.server import build_server

    tools, _, _ = make_tools(lambda r: httpx.Response(403, json=NOT_REGISTERED))
    server = build_server(client=tools.client)
    names = [t.name for t in asyncio.run(server.list_tools())]
    assert names == [
        "mfds_device_search",
        "mfds_device_detail",
        "mfds_device_company",
        "mfds_drug_search",
        "mfds_drug_detail",
        "mfds_dur_check",
        "mfds_status",
    ]


# ---- 설정 ---------------------------------------------------------------
def test_env_file_and_process_env_priority(tmp_path):
    f = tmp_path / ".env"
    f.write_text('# c\nMFDS_API_KEY="from-file"\nMFDS_DAILY_LIMIT=\nexport MFDS_MAX_PAGES=4\n', encoding="utf-8")
    assert read_env_file(f)["MFDS_API_KEY"] == "from-file"
    c = Config.load(env={}, env_file=f)
    assert c.api_key == "from-file" and c.daily_limit == 1000 and c.max_pages == 4
    assert "from-file" not in repr(c)
    c2 = Config.load(env={"MFDS_API_KEY": "from-env"}, env_file=f)
    assert c2.api_key == "from-env"
    c3 = Config.load(env={}, env_file=tmp_path / "none")
    assert c3.api_key is None


def test_mcp_call_tool_error_is_coded(make_tools):
    from mcp.server.mcpserver.exceptions import ToolError

    from mfds_mcp.server import build_server

    tools, _, _ = make_tools(lambda r: httpx.Response(403, json=NOT_REGISTERED))
    server = build_server(client=tools.client)
    with pytest.raises(ToolError) as e:
        asyncio.run(server.call_tool("mfds_dur_check", {"kind": "usjnt", "item_name": "x"}))
    assert '"error": "key_not_registered"' in str(e.value) and FAKE_KEY not in str(e.value)
