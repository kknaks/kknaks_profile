"""tool 본체 — MCP 와 떼어 두어 테스트에서 바로 부른다.

출력 items 는 API 원본 항목을 한 겹 벗긴 것(필드 이름 · 값 그대로)이고,
덧붙이는 파생 표시는 `is_cancelled`(취소 필드가 있는 서비스만) · `source` 둘뿐이다.
"""

from __future__ import annotations

from typing import Any

from .client import MfdsClient, MfdsError

DEVICE_ITEM = ("MdlpPrdlstPrmisnInfoService06", "getMdlpPrdlstPrmisnItem05")
DEVICE_COMPANY = ("MdeqMnftPrmsnDtlService01", "getMdeqMnftPrmsnDtlInq01")
DRUG_SERVICE = "DrugPrdtPrmsnInfoService08"
DRUG_LIST = (DRUG_SERVICE, "getDrugPrdtPrmsnInq08")
DRUG_DETAIL = (DRUG_SERVICE, "getDrugPrdtPrmsnDtlInq08")
DRUG_INGREDIENT = (DRUG_SERVICE, "getDrugPrdtMcpnDtlInq08")
DUR_SERVICE = "DURPrdlstInfoService03"

# kind → (오퍼레이션, 한글 이름)
DUR_KINDS: dict[str, tuple[str, str]] = {
    "usjnt": ("getUsjntTabooInfoList03", "병용금기"),
    "pregnancy": ("getPwnmTabooInfoList03", "임부금기"),
    "age": ("getSpcifyAgrdeTabooInfoList03", "특정연령대금기"),
    "elderly": ("getOdsnAtentInfoList03", "노인주의"),
    "capacity": ("getCpctyAtentInfoList03", "용량주의"),
    "period": ("getMdctnPdAtentInfoList03", "투여기간주의"),
    "efficacy_dup": ("getEfcyDplctInfoList03", "효능군중복"),
    "split": ("getSeobangjeongPartitnAtentInfoList03", "서방정분할주의"),
    "product": ("getDurPrdlstInfoList03", "DUR 품목 목록"),
}

# 상태 화면에 보이는 서비스와, refresh 때 확인용으로 부르는 오퍼레이션
STATUS_SERVICES: list[tuple[str, str]] = [
    DEVICE_ITEM,
    DEVICE_COMPANY,
    DRUG_LIST,
    (DUR_SERVICE, DUR_KINDS["product"][0]),
]

# 업체 상세에서 출력에서 빼는 필드(원장에 쓰지 않음 · 캐시 원본에는 남는다)
COMPANY_EXCLUDED_PREFIXES = ("ENTP_ADDR", "SRVC_TRGT_")


# ---- 입력 검사 -----------------------------------------------------------
def _clean(value: str | None) -> str | None:
    """앞뒤 공백만 자른다. 대소문자 · 가운데 공백은 그대로 둔다(모델명은 대소문자를 가린다)."""
    if value is None:
        return None
    value = value.strip()
    return value or None


def _check_paging(page: int, rows: int) -> None:
    if isinstance(rows, bool) or not isinstance(rows, int) or not 1 <= rows <= 100:
        raise MfdsError("invalid_input", "rows 는 1 이상 100 이하 정수다.", rows=rows)
    if isinstance(page, bool) or not isinstance(page, int) or page < 1:
        raise MfdsError("invalid_input", "page 는 1 이상 정수다.", page=page)


# ---- 취소 판정 -----------------------------------------------------------
def _filled(v: Any) -> bool:
    return v is not None and str(v).strip() != ""


def device_is_cancelled(item: dict[str, Any]) -> bool:
    return _filled(item.get("RTRCN_DSCTN_DIVS_CD")) or _filled(item.get("RTRCN_DSCTN_DT"))


def drug_is_cancelled(item: dict[str, Any]) -> bool:
    name = item.get("CANCEL_NAME")
    return _filled(item.get("CANCEL_DATE")) or (_filled(name) and str(name).strip() != "정상")


# ---- 출력 조립 -----------------------------------------------------------
def _shape(
    result: dict[str, Any],
    items: list[dict[str, Any]],
    cancelled=None,
    include_cancelled: bool = True,
) -> dict[str, Any]:
    source = {"service": result["service"], "operation": result["operation"], "query": result["query"]}
    out_items = []
    filtered = 0
    for it in items:
        row = dict(it)
        if cancelled is not None:
            row["is_cancelled"] = cancelled(it)
            if row["is_cancelled"] and not include_cancelled:
                filtered += 1
                continue
        row["source"] = source
        out_items.append(row)
    return {
        "service": result["service"],
        "operation": result["operation"],
        "query": result["query"],
        "total_count": result["total_count"],
        "page": result["page"],
        "rows": result["rows"],
        "returned": len(out_items),
        "filtered_out_cancelled": filtered,
        "truncated": result["truncated"],
        "from_cache": result["from_cache"],
        "fetched_at": result["fetched_at"],
        "items": out_items,
    }


def _single(result: dict[str, Any], sent: str) -> None:
    if result["total_count"] != 1:
        raise MfdsError(
            "filter_ignored",
            "한 건 조회인데 total_count 가 1 이 아니다(필터가 무시됐거나 값이 틀렸다). 항목을 내지 않는다.",
            total_count=result["total_count"],
            sent_param=sent,
        )


# ---- tools ---------------------------------------------------------------
class Tools:
    def __init__(self, client: MfdsClient) -> None:
        self.client = client

    def device_search(
        self,
        type_name: str | None = None,
        entrps: str | None = None,
        prduct: str | None = None,
        include_cancelled: bool = False,
        page: int = 1,
        rows: int = 100,
        all_pages: bool = False,
        no_cache: bool = False,
    ) -> dict[str, Any]:
        _check_paging(page, rows)
        params = {
            k: v for k, v in (("TYPE_NAME", _clean(type_name)), ("ENTRPS", _clean(entrps)), ("PRDUCT", _clean(prduct))) if v is not None
        }
        if not params:
            raise MfdsError("invalid_input", "type_name · entrps · prduct 중 하나 이상 필요하다.")
        result = self.client.query(*DEVICE_ITEM, params, page, rows, all_pages, no_cache)
        return _shape(result, result["items"], device_is_cancelled, include_cancelled)

    def device_detail(self, prmisn_no: str, no_cache: bool = False) -> dict[str, Any]:
        value = _clean(prmisn_no)
        if value is None:
            raise MfdsError("invalid_input", "prmisn_no(허가번호 PRDUCT_PRMISN_NO)가 필요하다.")
        result = self.client.query(*DEVICE_ITEM, {"PRDUCT_PRMISN_NO": value}, 1, 1, False, no_cache)
        _single(result, "PRDUCT_PRMISN_NO")
        return _shape(result, result["items"], device_is_cancelled, True)

    def device_company(self, name: str, page: int = 1, rows: int = 100, all_pages: bool = False, no_cache: bool = False) -> dict[str, Any]:
        _check_paging(page, rows)
        value = _clean(name)
        if value is None:
            raise MfdsError("invalid_input", "name(업체 이름 일부)이 필요하다.")
        result = self.client.query(*DEVICE_COMPANY, {"BSSH_NM": value}, page, rows, all_pages, no_cache)
        items = [{k: v for k, v in it.items() if not k.startswith(COMPANY_EXCLUDED_PREFIXES)} for it in result["items"]]
        return _shape(result, items)

    def drug_search(
        self,
        item_name: str | None = None,
        entp_name: str | None = None,
        include_cancelled: bool = False,
        page: int = 1,
        rows: int = 100,
        all_pages: bool = False,
        no_cache: bool = False,
    ) -> dict[str, Any]:
        _check_paging(page, rows)
        params = {k: v for k, v in (("item_name", _clean(item_name)), ("entp_name", _clean(entp_name))) if v is not None}
        if not params:
            raise MfdsError("invalid_input", "item_name · entp_name 중 하나 이상 필요하다.")
        result = self.client.query(*DRUG_LIST, params, page, rows, all_pages, no_cache)
        return _shape(result, result["items"], drug_is_cancelled, include_cancelled)

    def drug_detail(self, item_seq: str, include_ingredients: bool = False, no_cache: bool = False) -> dict[str, Any]:
        value = _clean(item_seq)
        if value is None:
            raise MfdsError("invalid_input", "item_seq(품목기준코드 ITEM_SEQ)가 필요하다.")
        result = self.client.query(*DRUG_DETAIL, {"item_seq": value}, 1, 1, False, no_cache)
        _single(result, "item_seq")
        out = _shape(result, result["items"], drug_is_cancelled, True)
        if include_ingredients:
            item_name = result["items"][0].get("ITEM_NAME") or ""
            # 주성분 상세는 item_seq 를 무시하고 Prduct(제품명 · 완전 일치)만 받는다 → 받은 뒤 ITEM_SEQ 로 고른다
            ing = self.client.query(*DRUG_INGREDIENT, {"Prduct": item_name}, 1, 100, True, no_cache)
            rows = [it for it in ing["items"] if str(it.get("ITEM_SEQ")) == value]
            out["ingredients"] = _shape(ing, rows)
        return out

    def dur_check(
        self,
        kind: str,
        item_name: str | None = None,
        item_seq: str | None = None,
        page: int = 1,
        rows: int = 100,
        all_pages: bool = False,
        no_cache: bool = False,
    ) -> dict[str, Any]:
        _check_paging(page, rows)
        if kind not in DUR_KINDS:
            raise MfdsError("invalid_input", "kind 가 목록에 없다.", kind=kind, allowed=sorted(DUR_KINDS))
        params = {k: v for k, v in (("itemName", _clean(item_name)), ("itemSeq", _clean(item_seq))) if v is not None}
        if not params:
            raise MfdsError("invalid_input", "item_name · item_seq 중 하나 이상 필요하다.")
        operation, label = DUR_KINDS[kind]
        result = self.client.query(DUR_SERVICE, operation, params, page, rows, all_pages, no_cache)
        cancelled = drug_is_cancelled if kind == "product" else None
        out = _shape(result, result["items"], cancelled, True)
        out["kind"] = kind
        out["kind_name"] = label
        return out

    def status(self, refresh: bool = False) -> dict[str, Any]:
        c = self.client
        if refresh and c.config.api_key:
            for service, operation in STATUS_SERVICES:
                try:
                    c.fetch_page(service, operation, {}, 1, 1, no_cache=True)
                except MfdsError:
                    pass  # 상태는 client 가 기록했다
        services = []
        for service, operation in STATUS_SERVICES:
            st = c.service_state.get(service)
            services.append(
                {
                    "service": service,
                    "operation": st["operation"] if st else operation,
                    "state": st["state"] if st else "unknown",
                    "last_checked_at": st["last_checked_at"] if st else None,
                    "last_error": st["last_error"] if st else None,
                }
            )
        return {
            "key_present": bool(c.config.api_key),
            "services": services,
            "calls_today": c.calls.total(),
            "daily_limit": c.config.daily_limit,
            "cache": {**c.cache.stats(), "ttl_days": c.config.cache_ttl_days},
        }
