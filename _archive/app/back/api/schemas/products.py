"""제품 레지스트리 HTTP 계약 (KDEV-WORK-018 P3 / KDEV-SPEC-014 §4).

**도메인 DTO(`service/products/dto.py`)와 별개 클래스다.** 응답에는 도메인에 없는
파생값 둘이 붙는다 — 제품 디렉토리 실재 여부와 카드 노출 값. 둘 다 DB 에 저장하지 않고
응답 시점에 판정한다(KDEV-DEC-017 D7·D14).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CardInput(BaseModel):
    """공개 카드 입력. `id`·`type`·`org` 는 **받지 않는다** — 시스템이 매긴다."""

    title: dict[str, str]
    summary: dict[str, str]
    category: str
    status: str = "wip"
    stack: list[str] = Field(default_factory=list)
    date: str | None = None
    thumbnail: str | None = None
    links: dict[str, str] | None = None


class RegisterRequest(BaseModel):
    """등록 요청. **구분에 따라 필요한 필드가 다르다.**

    `company` 는 레포와 career stem 만, `studio` 는 제품 slug 와 카드를 함께 받는다.
    어느 조합이 유효한지는 service 가 판정한다 — 스키마에서 갈라 두면 계약이 두 곳에
    살고, 규칙이 바뀔 때 한쪽만 고쳐진다.
    """

    repo: str
    type: str
    detail: str | None = None
    product_slug: str | None = None
    card: CardInput | None = None


class PatchRequest(BaseModel):
    """부분 수정.

    **`model_fields_set` 이 계약의 일부다.** `detail` 을 안 보낸 것과 `null` 로 보낸
    것이 다르다 — 전자는 손대지 않는다는 뜻이고 후자는 지운다는 뜻이다.
    """

    detail: str | None = None
    product_slug: str | None = None
    enabled: bool | None = None


class VisibleRequest(BaseModel):
    """카드 노출 변경. **DB 가 아니라 `showcase.md` 를 고친다**(KDEV-DEC-017 D18)."""

    value: bool


class RegistryRow(BaseModel):
    """레지스트리 표 한 줄."""

    id: int
    slug: str
    type: str
    detail: str | None
    product_slug: str | None
    account: str
    enabled: bool
    last_fetched_at: datetime | None
    last_error: str | None
    #: `product_slug` 가 가리키는 디렉토리가 실재하는가. **경고이지 차단이 아니다.**
    product_exists: bool
    #: 공개 카드의 노출 값. 파일이 SoT 라 **읽기 전용**이고, 카드가 없으면 `null` 이다.
    card_visible: bool | None


class RegistryList(BaseModel):
    items: list[RegistryRow]


class OptionsResponse(BaseModel):
    """폼 선택지. **코드가 아니라 레포 상태에서 나온다.**

    `categories` 는 `persona/_meta.yaml` 소유다 — 목록 밖의 값 하나가 persona 로드
    전체를 실패시키므로 화면이 자유입력을 주면 안 된다.
    """

    products: list[str]
    categories: list[str]
    statuses: list[str]
    careers: list[str]


class DiscoveredRow(BaseModel):
    slug: str
    account: str
    pushed_at: str | None = None
    private: bool = False


class DiscoveredResponse(BaseModel):
    """미등록 목록. **실패해도 표는 정상이어야 한다**(SPEC-014 U-1).

    그래서 오류를 예외로 올리지 않고 `error` 로 싣는다 — 배너만 실패한다.
    """

    items: list[DiscoveredRow] = Field(default_factory=list)
    #: 최근성 창 밖이라 감춘 수. **조용히 자르지 않는다** — 0건과 구분돼야 한다.
    hidden_old: int = 0
    window_days: int = 0
    error: str | None = None


class ErrorBody(BaseModel):
    """거부 사유. `field` 로 화면이 어느 입력 아래에 붙일지 정한다."""

    code: str
    message: str
    field: str | None = None


class SyncResponse(BaseModel):
    row: RegistryRow
    ok: bool
    code: str | None = None
    message: str | None = None
