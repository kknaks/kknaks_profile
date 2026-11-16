"""MCP 서버 (stdio). stdout 은 프로토콜 채널이라 로그는 stderr 로만 보낸다."""

from __future__ import annotations

import functools
import json
import logging
import sys
from typing import Annotated, Any, Literal

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field

from .client import MfdsClient, MfdsError
from .config import Config
from .tools import Tools

log = logging.getLogger("mfds_mcp")

INSTRUCTIONS = (
    "식약처(공공데이터포털) 허가 정보 조회 전용 서버다. 의료기기 품목허가 · 의료기기 업체 · 의약품 허가 · DUR 을 "
    "원본 필드 그대로 낸다. 결과는 후보일 뿐 매칭 판정이 아니다. 먼저 mfds_status 로 키와 서비스 상태를 본다. "
    "같은 질의는 캐시로 답한다(from_cache)."
)

Page = Annotated[int, Field(description="페이지 번호(1부터)")]
Rows = Annotated[int, Field(description="한 페이지 행 수(1~100)")]
AllPages = Annotated[bool, Field(description="true 면 totalCount 까지 이어 받는다(최대 MFDS_MAX_PAGES 페이지, 넘으면 truncated)")]
NoCache = Annotated[bool, Field(description="true 면 캐시를 건너뛰고 새로 받아 덮어쓴다")]
IncludeCancelled = Annotated[bool, Field(description="true 면 취소 · 취하된 허가도 낸다(기본은 뺀다)")]

DurKind = Literal["usjnt", "pregnancy", "age", "elderly", "capacity", "period", "efficacy_dup", "split", "product"]


def build_server(config: Config | None = None, client: MfdsClient | None = None) -> MCPServer:
    tools = Tools(client or MfdsClient(config or Config.load()))
    mcp = MCPServer("mfds", instructions=INSTRUCTIONS, version="0.1.0")

    def guarded(fn):
        """MfdsError → 코드가 든 JSON ToolError. 그 밖의 예외는 클래스 이름만(메시지에 URL · 키가 있을 수 있다)."""

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> dict[str, Any]:
            try:
                return fn(*args, **kwargs)
            except MfdsError as exc:
                raise ToolError(json.dumps(exc.to_dict(), ensure_ascii=False)) from None
            except Exception as exc:  # noqa: BLE001
                log.error("internal error in %s: %s", fn.__name__, type(exc).__name__)
                raise ToolError(json.dumps({"error": "internal_error", "reason": type(exc).__name__}, ensure_ascii=False)) from None

        return wrapper

    @mcp.tool(
        description=(
            "식약처 의료기기 품목허가를 모델명(type_name) · 업체(entrps) · 품목명(prduct, 일반명칭)으로 찾는다. "
            "셋 다 부분 일치이고, 여러 개를 주면 모두 만족하는 것만 나온다(AND). 업체 이름 일부가 짧으면 관계없는 "
            "업체도 섞인다. 모델명은 대소문자를 가린다('Thermage' ≠ 'thermage'). 품목명은 '조직수복용생체재료' 같은 "
            "일반명칭이라 브랜드로는 거의 안 걸린다. 브랜드는 모델명에 있을 때만 걸린다. 기본값으로 취소 · 취하된 "
            "허가는 뺀다(total_count 는 API 값 그대로, 뺀 수는 filtered_out_cancelled). 결과는 후보일 뿐 매칭 판정이 아니다."
        )
    )
    @guarded
    def mfds_device_search(
        type_name: Annotated[str | None, Field(description="모델명 TYPE_NAME(부분 일치 · 대소문자 구분)")] = None,
        entrps: Annotated[str | None, Field(description="허가 보유 업체 ENTRPS(부분 일치)")] = None,
        prduct: Annotated[str | None, Field(description="품목명(일반명칭) PRDUCT(부분 일치)")] = None,
        include_cancelled: IncludeCancelled = False,
        page: Page = 1,
        rows: Rows = 100,
        all_pages: AllPages = False,
        no_cache: NoCache = False,
    ) -> dict[str, Any]:
        return tools.device_search(type_name, entrps, prduct, include_cancelled, page, rows, all_pages, no_cache)

    @mcp.tool(
        description=(
            "허가번호(PRDUCT_PRMISN_NO)로 의료기기 허가 한 건을 준다. 품목일련번호(MDEQ_PRDLST_SN)로는 찾을 수 없다. "
            "응답 건수가 1 이 아니면 filter_ignored 에러."
        )
    )
    @guarded
    def mfds_device_detail(
        prmisn_no: Annotated[str, Field(description="허가번호 PRDUCT_PRMISN_NO(예: 수허 00-000 호)")],
        no_cache: NoCache = False,
    ) -> dict[str, Any]:
        return tools.device_detail(prmisn_no, no_cache)

    @mcp.tool(
        description=(
            "식약처 의료기기 제조 · 수입업 허가 업체를 이름 일부로 찾는다(부분 일치 — 관계없는 업체도 섞일 수 있다). "
            "업체가 제조업인지 수입업인지(COB_FLAG_CODE_NAME), 허가일, 휴 · 폐업 여부를 본다. 업체 주소는 출력에서 뺀다."
        )
    )
    @guarded
    def mfds_device_company(
        name: Annotated[str, Field(description="업체 이름 일부 BSSH_NM")],
        page: Page = 1,
        rows: Rows = 100,
        all_pages: AllPages = False,
        no_cache: NoCache = False,
    ) -> dict[str, Any]:
        return tools.device_company(name, page, rows, all_pages, no_cache)

    @mcp.tool(
        description=(
            "식약처 의약품 제품 허가정보(DrugPrdtPrmsnInfoService08)를 제품명(item_name) · 업체명(entp_name)으로 찾는다. "
            "둘 다 부분 일치, 함께 주면 AND. 항목에 제품 원어명 ITEM_ENG_NAME · 업체 원어명 ENTP_ENG_NAME · "
            "품목기준코드 ITEM_SEQ · 취소 상태 CANCEL_NAME/CANCEL_DATE 가 있다. 기본값으로 취소 · 취하는 뺀다. "
            "규격(MATERIAL_NAME · PACK_UNIT)과 효능 · 용법은 mfds_drug_detail 로 본다."
        )
    )
    @guarded
    def mfds_drug_search(
        item_name: Annotated[str | None, Field(description="제품명 일부(예: 나보타)")] = None,
        entp_name: Annotated[str | None, Field(description="업체명 일부")] = None,
        include_cancelled: IncludeCancelled = False,
        page: Page = 1,
        rows: Rows = 100,
        all_pages: AllPages = False,
        no_cache: NoCache = False,
    ) -> dict[str, Any]:
        return tools.drug_search(item_name, entp_name, include_cancelled, page, rows, all_pages, no_cache)

    @mcp.tool(
        description=(
            "품목기준코드(ITEM_SEQ — mfds_drug_search 결과에 있다)로 의약품 허가 상세 한 건을 준다. 규격 "
            "MATERIAL_NAME(총량 · 성분 · 분량 · 단위) · 포장 단위 PACK_UNIT · 전문/일반 ETC_OTC_CODE · 위탁 제조원 "
            "CNSGN_MANUF · 원어명 · 취소 상태 · 효능(EE_DOC_DATA) · 용법(UD_DOC_DATA) · 주의(NB_DOC_DATA, XML 원문). "
            "include_ingredients=true 면 주성분 상세(getDrugPrdtMcpnDtlInq08)를 ingredients 로 덧붙인다(호출 1회 더)."
        )
    )
    @guarded
    def mfds_drug_detail(
        item_seq: Annotated[str, Field(description="품목기준코드 ITEM_SEQ(9자리)")],
        include_ingredients: Annotated[bool, Field(description="주성분 상세도 붙인다")] = False,
        no_cache: NoCache = False,
    ) -> dict[str, Any]:
        return tools.drug_detail(item_seq, include_ingredients, no_cache)

    @mcp.tool(
        description=(
            "식약처 DUR(의약품 안전사용, DURPrdlstInfoService03) 을 제품명(item_name, 부분 일치) 또는 품목기준코드"
            "(item_seq)로 조회한다. kind: usjnt=병용금기 · pregnancy=임부금기 · age=특정연령대금기 · elderly=노인주의 · "
            "capacity=용량주의 · period=투여기간주의 · efficacy_dup=효능군중복 · split=서방정분할주의 · product=DUR 품목 "
            "목록. 금기 내용은 PROHBT_CONTENT, 병용 상대는 MIXTURE_* 필드. 0건은 '그 DUR 대상이 아님'이지 안전 판정이 아니다."
        )
    )
    @guarded
    def mfds_dur_check(
        kind: Annotated[DurKind, Field(description="DUR 종류")],
        item_name: Annotated[str | None, Field(description="제품명 일부")] = None,
        item_seq: Annotated[str | None, Field(description="품목기준코드 ITEM_SEQ")] = None,
        page: Page = 1,
        rows: Rows = 100,
        all_pages: AllPages = False,
        no_cache: NoCache = False,
    ) -> dict[str, Any]:
        return tools.dur_check(kind, item_name, item_seq, page, rows, all_pages, no_cache)

    @mcp.tool(
        description=(
            "키가 있는지, 서비스별로 쓸 수 있는지(usable · not_registered · unknown — 이 프로세스의 마지막 실제 호출 기준), "
            "오늘 호출 수, 캐시 크기를 보여 준다. 다른 tool 을 쓰기 전에 먼저 부른다. refresh=true 면 서비스마다 1회(1행) 확인 호출."
        )
    )
    @guarded
    def mfds_status(
        refresh: Annotated[bool, Field(description="서비스마다 확인용 호출 1회")] = False,
    ) -> dict[str, Any]:
        return tools.status(refresh)

    return mcp


def main() -> None:
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    for name in ("httpx", "httpcore", "httpx2", "httpcore2"):
        logging.getLogger(name).setLevel(logging.WARNING)
    build_server().run("stdio")


if __name__ == "__main__":
    main()
