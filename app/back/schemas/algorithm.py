"""algorithm — front ↔ back 계약. 어드민 알고리즘 화면이 읽고 쓴다.

메타만 다룬다 — 본문 단계(Problem→…→Solution)는 detail_path 의 md 몫이다.
profile_id 는 계약에 없다 — 1인 사이트라 서버가 첫 profile 로 채운다.
visible 은 어드민이라 거르지 않고 그대로 내려준다.
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from dto.algorithm import (
    AlgorithmDTO,
    AlgorithmNeighbor,
    PublicAlgorithmDetail,
    PublicAlgorithmList,
)


class AdminAlgorithmItem(BaseModel):
    id: int
    slug: str
    title: str
    difficulty: str
    summary: str | None = None
    source_platform: str = Field(serialization_alias="sourcePlatform")
    source_number: int | None = Field(default=None, serialization_alias="sourceNumber")
    source_url: str | None = Field(default=None, serialization_alias="sourceUrl")
    curated_in: list[str] = Field(default=[], serialization_alias="curatedIn")
    tags: list[str] = []
    today: bool
    detail_path: str = Field(serialization_alias="detailPath")
    published_on: date | None = Field(default=None, serialization_alias="publishedOn")
    visible: bool

    @classmethod
    def from_dto(cls, dto: AlgorithmDTO) -> AdminAlgorithmItem:
        return cls(
            id=dto.id,
            slug=dto.slug,
            title=dto.title,
            difficulty=dto.difficulty,
            summary=dto.summary,
            source_platform=dto.source_platform,
            source_number=dto.source_number,
            source_url=dto.source_url,
            curated_in=dto.curated_in or [],
            tags=dto.tags or [],
            today=dto.today,
            detail_path=dto.detail_path,
            published_on=dto.published_on,
            visible=dto.visible,
        )


class AdminAlgorithmsResponse(BaseModel):
    items: list[AdminAlgorithmItem]


# ── 공개 /api/algorithms — lib/types.ts 의 AlgorithmsResponse 와 1:1 ─────────
#
# visible=false 는 service 가 걸렀다 — 응답에 visible 필드는 없다(erd §미결 3).
# subtitle·intro 는 내리지 않는다 — erd 에 대응 컬럼이 없고 프론트 기본 문구를 쓴다.
# source 는 컬럼 4개(source_platform·source_number·source_url·curated_in)를
# 객체 하나로 접은 것이다 — 계약(types.ts AlgorithmSource)이 그 모양이라서다.
# 컬럼이 jsonb 가 아닌 이유는 erd.md — 플랫폼·번호로 거르고 싶어진다.


class PublicAlgorithmSource(BaseModel):
    platform: str
    number: int | None = None
    url: str | None = None
    curated_in: list[str] = Field(default=[], serialization_alias="curatedIn")


class PublicAlgorithmItem(BaseModel):
    id: int
    slug: str                                                   # a-001-two-sum
    title: str
    difficulty: str
    source: PublicAlgorithmSource                               # 컬럼 4개를 접은 객체
    tags: list[str] = []
    today: bool
    published_on: date | None = Field(default=None, serialization_alias="publishedOn")
    summary: str | None = None                                  # 컬럼 — 현재 대부분 null

    @classmethod
    def from_dto(cls, dto: AlgorithmDTO) -> PublicAlgorithmItem:
        return cls(
            id=dto.id,
            slug=dto.slug,
            title=dto.title,
            difficulty=dto.difficulty,
            source=PublicAlgorithmSource(
                platform=dto.source_platform,
                number=dto.source_number,
                url=dto.source_url,
                curated_in=dto.curated_in or [],
            ),
            tags=dto.tags or [],
            today=dto.today,
            published_on=dto.published_on,
            summary=dto.summary,
        )


class PublicAlgorithmsMeta(BaseModel):
    total_count: int = Field(serialization_alias="totalCount")
    # today=true 인 한 건 — 목록 상단 큰 카드. 없으면 null.
    today: PublicAlgorithmItem | None = None


class PublicAlgorithmsResponse(BaseModel):
    items: list[PublicAlgorithmItem] = Field(serialization_alias="algorithms[]")
    algorithms: PublicAlgorithmsMeta

    @classmethod
    def from_bundle(cls, bundle: PublicAlgorithmList) -> PublicAlgorithmsResponse:
        return cls(
            items=[PublicAlgorithmItem.from_dto(d) for d in bundle.items],
            algorithms=PublicAlgorithmsMeta(
                total_count=bundle.total_count,
                today=PublicAlgorithmItem.from_dto(bundle.today)
                if bundle.today
                else None,
            ),
        )


# ── 공개 상세 — 단계 구조. md `## Data` yaml 의 정규화 결과를 담는다 ──────────
#
# 필드명이 types.ts 와 1:1 이다 — worked_example 처럼 snake 인 것도 계약이 snake 다.
# 빈 구조가 안전 기본값이다: items·slots·code 가 빈 배열이면 컴포넌트가
# 빈 상태 문구를 그리고, worked_example 이 null 이면 펼침 버튼을 그리지 않는다.


class PublicAlgoProblemIO(BaseModel):
    input: str
    output: str


class PublicAlgoProblem(BaseModel):
    title: str | None = None
    statement: str = ""
    constraints: list[str] = []
    io: list[PublicAlgoProblemIO] = []


class PublicAlgoQuizItem(BaseModel):
    q: str | None = None                                        # clarifying 항목만
    name: str | None = None                                     # approach 항목만
    complexity: str | None = None                               # approach 항목만
    type: str                                                   # good / distractor
    why: str


class PublicAlgoQuizGroup(BaseModel):
    items: list[PublicAlgoQuizItem] = []


class PublicAlgoLogicOption(BaseModel):
    code: str
    type: str                                                   # good / distractor
    why: str


class PublicAlgoLogicSlot(BaseModel):
    label: str
    indent: int = 0
    options: list[PublicAlgoLogicOption] = []


class PublicAlgoLogic(BaseModel):
    format: str = "slot"                                        # 화면은 slot 만 지원(ADR-08)
    slots: list[PublicAlgoLogicSlot] = []


class PublicAlgoTraceCase(BaseModel):
    input: str
    expected: str


class PublicAlgoWorkedExample(BaseModel):
    input: str = ""
    steps: list[str] = []
    answer: str = ""


class PublicAlgoTrace(BaseModel):
    code: list[str] = []
    cases: list[PublicAlgoTraceCase] = []
    worked_example: PublicAlgoWorkedExample | None = None


class PublicAlgoComplexity(BaseModel):
    time: str = ""
    space: str = ""


class PublicAlgoSolution(BaseModel):
    code: str = ""
    complexity: PublicAlgoComplexity = PublicAlgoComplexity()
    followup: list[str] = []


class PublicAlgorithmNeighbor(BaseModel):
    """이전/다음 회차 — 컬럼이 아니라 published_on 정렬의 이웃이다(erd.md)."""

    slug: str
    title: str

    @classmethod
    def from_dto(cls, dto: AlgorithmNeighbor | None) -> PublicAlgorithmNeighbor | None:
        return cls(slug=dto.slug, title=dto.title) if dto else None


class PublicAlgorithmDetailItem(PublicAlgorithmItem):
    problem: PublicAlgoProblem
    clarifying: PublicAlgoQuizGroup
    approach: PublicAlgoQuizGroup
    logic: PublicAlgoLogic
    trace: PublicAlgoTrace
    solution: PublicAlgoSolution
    newer: PublicAlgorithmNeighbor | None = None
    older: PublicAlgorithmNeighbor | None = None

    @classmethod
    def from_public(cls, detail: PublicAlgorithmDetail) -> PublicAlgorithmDetailItem:
        base = PublicAlgorithmItem.from_dto(detail.dto)
        return cls(
            **base.model_dump(),
            problem=PublicAlgoProblem.model_validate(detail.problem),
            clarifying=PublicAlgoQuizGroup.model_validate(detail.clarifying),
            approach=PublicAlgoQuizGroup.model_validate(detail.approach),
            logic=PublicAlgoLogic.model_validate(detail.logic),
            trace=PublicAlgoTrace.model_validate(detail.trace),
            solution=PublicAlgoSolution.model_validate(detail.solution),
            newer=PublicAlgorithmNeighbor.from_dto(detail.newer),
            older=PublicAlgorithmNeighbor.from_dto(detail.older),
        )


class PublicAlgorithmDetailResponse(BaseModel):
    detail: PublicAlgorithmDetailItem = Field(serialization_alias="algorithms.detail")


class AlgorithmCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    slug: str = Field(min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=128)
    # easy/medium/hard 검사는 service 가 한다 — 422 문구를 한 곳에서 내려고.
    difficulty: str = Field(min_length=1, max_length=8)
    summary: str | None = None
    source_platform: str = Field(
        min_length=1, max_length=32, validation_alias="sourcePlatform"
    )
    source_number: int | None = Field(default=None, validation_alias="sourceNumber")
    source_url: str | None = Field(
        default=None, max_length=255, validation_alias="sourceUrl"
    )
    curated_in: list[str] | None = Field(default=None, validation_alias="curatedIn")
    tags: list[str] | None = None
    today: bool = False
    detail_path: str = Field(min_length=1, max_length=255, validation_alias="detailPath")
    published_on: date | None = Field(default=None, validation_alias="publishedOn")
    visible: bool = True


class AlgorithmUpdate(BaseModel):
    """PATCH body — 보낸 필드만 반영 (exclude_unset). NOT NULL 에 null 은 service 가 422."""

    model_config = ConfigDict(populate_by_name=True)

    slug: str | None = Field(default=None, min_length=1, max_length=64)
    title: str | None = Field(default=None, min_length=1, max_length=128)
    difficulty: str | None = Field(default=None, max_length=8)
    summary: str | None = None
    source_platform: str | None = Field(
        default=None, max_length=32, validation_alias="sourcePlatform"
    )
    source_number: int | None = Field(default=None, validation_alias="sourceNumber")
    source_url: str | None = Field(
        default=None, max_length=255, validation_alias="sourceUrl"
    )
    curated_in: list[str] | None = Field(default=None, validation_alias="curatedIn")
    tags: list[str] | None = None
    today: bool | None = None
    detail_path: str | None = Field(
        default=None, max_length=255, validation_alias="detailPath"
    )
    published_on: date | None = Field(default=None, validation_alias="publishedOn")
    visible: bool | None = None
