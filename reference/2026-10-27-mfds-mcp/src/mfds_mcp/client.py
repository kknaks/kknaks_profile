"""공공데이터포털 식약처 API 클라이언트 — 키 주입 · 키 마스킹 · 에러 구분 · 캐시 · 하루 상한.

키는 `_send` 한 곳에서만 질의에 넣는다. 로그 · 에러 · 캐시 · 출력의 query 에는 넣지 않는다.
에러 사유에는 예외 클래스 이름과 HTTP 상태 코드만 싣는다(`str(exc)` 에는 요청 URL = 키가 들어간다).
"""

from __future__ import annotations

import json
import logging
import re
from datetime import UTC, datetime
from typing import Any
from urllib.parse import quote, quote_plus

import httpx

from .cache import Cache, CallCounter, cache_key
from .config import Config

# httpx 는 INFO 로 요청 URL 전체(serviceKey 포함)를 남긴다 → WARNING 이상만
for _name in ("httpx", "httpcore", "httpx2", "httpcore2"):
    logging.getLogger(_name).setLevel(logging.WARNING)

log = logging.getLogger("mfds_mcp")

NOT_REGISTERED = "SERVICE_KEY_IS_NOT_REGISTERED_ERROR"


class MfdsError(Exception):
    """tool 에러. `code` 로 구분하고 `detail` 은 키가 없는 값만 담는다."""

    def __init__(self, code: str, message: str, **detail: Any) -> None:
        super().__init__(code)
        self.code = code
        self.message = message
        self.detail = detail

    def to_dict(self) -> dict[str, Any]:
        return {"error": self.code, "message": self.message, **self.detail}


def unwrap_items(body: dict[str, Any]) -> list[dict[str, Any]]:
    """`body.items` 를 항목 목록으로. 서비스마다 모양이 다르다.

    - 의료기기 품목허가: `[{"item": {...}}, ...]` → 한 겹 벗긴다
    - 업체 · 의약품 · DUR: `[{...}, ...]` 평평하다
    - 0건이면 `items` 키가 없다 → `[]`
    - (XML 을 JSON 으로 바꾼 꼴) `{"item": [...]}` · `{"item": {...}}` 도 받는다
    """
    items = body.get("items")
    if items is None or items == "":
        return []
    if isinstance(items, dict):
        items = items.get("item", [])
        if isinstance(items, dict):
            items = [items]
    out: list[dict[str, Any]] = []
    for it in items or []:
        if isinstance(it, dict) and set(it.keys()) == {"item"} and isinstance(it["item"], dict):
            out.append(it["item"])
        elif isinstance(it, dict):
            out.append(it)
    return out


def _xml_tag(text: str, tag: str) -> str | None:
    m = re.search(rf"<{tag}>(.*?)</{tag}>", text, re.S)
    return m.group(1).strip() if m else None


class MfdsClient:
    def __init__(self, config: Config, transport: httpx.BaseTransport | None = None) -> None:
        self.config = config
        self.cache = Cache(config.cache_dir, config.cache_ttl_days)
        self.calls = CallCounter(config.cache_dir)
        self._http = httpx.Client(timeout=config.timeout_seconds, transport=transport)
        # 서비스별 마지막 실제 호출 결과(같은 프로세스 안에서만)
        self.service_state: dict[str, dict[str, Any]] = {}

    # ---- 키 가리기 -------------------------------------------------------
    def scrub(self, text: str | None) -> str | None:
        if text is None or not self.config.api_key:
            return text
        key = self.config.api_key
        for form in sorted({key, quote(key, safe=""), quote_plus(key)}, key=len, reverse=True):
            text = text.replace(form, "<MFDS_API_KEY>")
        return text

    # ---- 상태 ------------------------------------------------------------
    def _mark(self, service: str, operation: str, state: str | None, error: str | None) -> None:
        prev = self.service_state.get(service, {})
        self.service_state[service] = {
            "service": service,
            "operation": operation,
            "state": state or prev.get("state", "unknown"),
            "last_checked_at": datetime.now(UTC).isoformat(),
            "last_error": error,
        }

    # ---- HTTP ------------------------------------------------------------
    def _send(self, service: str, operation: str, query: dict[str, Any]) -> Any:
        if not self.config.api_key:
            raise MfdsError("missing_key", ".env 의 MFDS_API_KEY 를 채운다(공공데이터포털 일반 인증키 · Decoding).")
        if self.calls.total() >= self.config.daily_limit:
            raise MfdsError(
                "daily_limit_reached",
                "오늘 호출 수가 MFDS_DAILY_LIMIT 에 닿았다. 캐시에 있는 질의만 답한다.",
                calls_today=self.calls.total(),
                daily_limit=self.config.daily_limit,
            )
        url = f"{self.config.base_url}/{service}/{operation}"
        params = {"serviceKey": self.config.api_key, **query}
        try:
            resp = self._http.get(url, params=params)
        except httpx.TimeoutException as exc:
            self._mark(service, operation, None, "upstream_unreachable")
            raise MfdsError("upstream_unreachable", "시간 초과. 재시도하지 않았다.", reason=type(exc).__name__, service=service) from None
        except httpx.HTTPError as exc:
            self._mark(service, operation, None, "upstream_unreachable")
            raise MfdsError("upstream_unreachable", "연결 실패. 재시도하지 않았다.", reason=type(exc).__name__, service=service) from None
        self.calls.add(service)
        return self._parse(service, operation, resp)

    def _parse(self, service: str, operation: str, resp: httpx.Response) -> Any:
        text = self.scrub(resp.text) or ""
        data: Any = None
        try:
            data = json.loads(text)
        except ValueError:
            data = None

        # 공통 에러 머리(JSON 또는 XML)
        err_msg = reason_code = auth_msg = None
        if isinstance(data, dict) and "OpenAPI_ServiceResponse" in data:
            hdr = (data["OpenAPI_ServiceResponse"] or {}).get("cmmMsgHeader") or {}
            err_msg, reason_code, auth_msg = hdr.get("errMsg"), hdr.get("returnReasonCode"), hdr.get("returnAuthMsg")
        elif data is None and "<cmmMsgHeader>" in text:
            err_msg = _xml_tag(text, "errMsg")
            reason_code = _xml_tag(text, "returnReasonCode")
            auth_msg = _xml_tag(text, "returnAuthMsg")

        if err_msg is not None or reason_code is not None:
            if err_msg == NOT_REGISTERED or auth_msg == NOT_REGISTERED:
                self._mark(service, operation, "not_registered", "key_not_registered")
                raise MfdsError(
                    "key_not_registered",
                    "이 키로 이 서비스가 활용신청되지 않았거나 승인 반영 전이다(키 값 자체가 틀려도 같은 에러가 온다). "
                    "공공데이터포털에서 활용신청 후 반영(1시간 안팎)을 기다리고, .env 에 Decoding 키를 넣었는지 확인한다.",
                    service=service,
                    errMsg=err_msg,
                    returnReasonCode=reason_code,
                    http_status=resp.status_code,
                )
            self._mark(service, operation, None, "api_error")
            raise MfdsError(
                "api_error",
                "API 가 에러를 돌려줬다.",
                service=service,
                errMsg=err_msg,
                returnAuthMsg=auth_msg,
                returnReasonCode=reason_code,
                http_status=resp.status_code,
            )

        if resp.status_code == 404 or (data is None and "API not found" in text):
            self._mark(service, operation, None, "service_not_found")
            raise MfdsError(
                "service_not_found",
                "서비스 또는 오퍼레이션 이름이 틀린 것으로 보인다.",
                service=service,
                operation=operation,
                http_status=resp.status_code,
            )
        if resp.status_code != 200 or not isinstance(data, dict):
            self._mark(service, operation, None, "api_error")
            raise MfdsError(
                "api_error",
                "예상하지 못한 응답이다(JSON 이 아니거나 HTTP 200 이 아님).",
                service=service,
                http_status=resp.status_code,
                body_head=text[:200],
            )
        header = data.get("header") or {}
        if str(header.get("resultCode")) != "00":
            self._mark(service, operation, None, "api_error")
            raise MfdsError(
                "api_error",
                "API 가 에러를 돌려줬다.",
                service=service,
                resultCode=header.get("resultCode"),
                resultMsg=header.get("resultMsg"),
                http_status=resp.status_code,
            )
        self._mark(service, operation, "usable", None)
        return data

    # ---- 페이지 · 캐시 ---------------------------------------------------
    def fetch_page(
        self, service: str, operation: str, params: dict[str, Any], page: int, rows: int, no_cache: bool = False
    ) -> tuple[dict[str, Any], bool]:
        """(캐시 항목 {fetched_at, query, response}, from_cache)."""
        query = {"type": "json", **params, "numOfRows": rows, "pageNo": page}
        key = cache_key(service, operation, query)
        if not no_cache:
            hit = self.cache.get(key, page)
            if hit is not None:
                return hit, True
        response = self._send(service, operation, query)
        entry = self.cache.put(key, page, query, response, datetime.now(UTC))
        return entry, False

    def query(
        self,
        service: str,
        operation: str,
        params: dict[str, Any],
        page: int = 1,
        rows: int = 100,
        all_pages: bool = False,
        no_cache: bool = False,
    ) -> dict[str, Any]:
        """페이지를 받아 한 겹 벗긴 원본 항목을 모은다. 걸러내기 · 가공은 하지 않는다."""
        if not self.config.api_key:  # 키가 없으면 캐시가 있어도 조회 tool 은 답하지 않는다(S-4)
            raise MfdsError("missing_key", ".env 의 MFDS_API_KEY 를 채운다(공공데이터포털 일반 인증키 · Decoding).")
        entry, from_cache = self.fetch_page(service, operation, params, page, rows, no_cache)
        body = entry["response"].get("body") or {}
        total = int(body.get("totalCount") or 0)
        items = unwrap_items(body)
        fetched_at = entry["fetched_at"]
        truncated = False
        if all_pages:
            last_page = max(page, -(-total // rows)) if total else page
            stop = min(last_page, page + self.config.max_pages - 1)
            for p in range(page + 1, stop + 1):
                e, fc = self.fetch_page(service, operation, params, p, rows, no_cache)
                items.extend(unwrap_items(e["response"].get("body") or {}))
                from_cache = from_cache and fc
                fetched_at = min(fetched_at, e["fetched_at"])
            truncated = stop < last_page
        return {
            "service": service,
            "operation": operation,
            "query": {"type": "json", **params, "numOfRows": rows, "pageNo": page},
            "total_count": total,
            "page": page,
            "rows": rows,
            "truncated": truncated,
            "from_cache": from_cache,
            "fetched_at": fetched_at,
            "items": items,
        }

    def close(self) -> None:
        self._http.close()
