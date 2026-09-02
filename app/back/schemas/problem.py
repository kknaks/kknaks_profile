"""problem — front ↔ back 계약. 어드민 해결한 문제 화면이 읽고 쓴다.

careerTitle · companyName 은 2단 조인(problem → career → company)의 읽기 전용
표시값이고 productTitle 은 선택 조인 — product_id 가 NULL 이면 null. 수정은
careerId · productId 로 한다. body 는 Text 컬럼 그대로다 — 이 표는 detail_path
없이 본문을 행에 담는다(erd.md §problem).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from dto.problem import ProblemDTO


class AdminProblemItem(BaseModel):
    id: int
    career_id: int = Field(serialization_alias="careerId")
    career_title: str = Field(serialization_alias="careerTitle")
    company_name: str = Field(serialization_alias="companyName")
    product_id: int | None = Field(default=None, serialization_alias="productId")
    product_title: str | None = Field(default=None, serialization_alias="productTitle")
    title: str
    body: str | None = None
    display_order: int = Field(serialization_alias="displayOrder")
    # 채팅 노출 토글의 현재값(SPEC-017 U-7).
    chat_exposed: bool = Field(default=False, serialization_alias="chatExposed")

    @classmethod
    def from_dto(cls, dto: ProblemDTO) -> AdminProblemItem:
        return cls(
            id=dto.id,
            career_id=dto.career_id,
            career_title=dto.career_title,
            company_name=dto.company_name,
            product_id=dto.product_id,
            product_title=dto.product_title,
            title=dto.title,
            body=dto.body,
            display_order=dto.display_order,
            chat_exposed=dto.chat_exposed,
        )


class AdminProblemsResponse(BaseModel):
    items: list[AdminProblemItem]


class ProblemCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    career_id: int = Field(validation_alias="careerId")
    product_id: int | None = Field(default=None, validation_alias="productId")
    title: str = Field(min_length=1, max_length=128)
    body: str | None = None
    display_order: int = Field(default=0, validation_alias="displayOrder")


class ProblemUpdate(BaseModel):
    """PATCH body — 보낸 필드만 반영 (exclude_unset). NOT NULL 에 null 은 service 가 422.

    productId 는 null 을 **보내는 것**이 연결 해제다 — 안 보낸 것과 다르다.
    """

    model_config = ConfigDict(populate_by_name=True)

    career_id: int | None = Field(default=None, validation_alias="careerId")
    product_id: int | None = Field(default=None, validation_alias="productId")
    title: str | None = Field(default=None, min_length=1, max_length=128)
    body: str | None = None
    display_order: int | None = Field(default=None, validation_alias="displayOrder")
