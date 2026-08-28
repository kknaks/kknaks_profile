"""slug 규약 — AI 가 문서를 가리키는 유일한 손잡이 (DEC-027 D3).

## 왜 합성 slug 가 있나

`project` · `note` · `content` · `algorithm` 은 `slug` 컬럼을 갖는다. 그런데 `career` 와
`problem` 은 **없다** — career 는 (회사, 직함)이 신원이고 problem 은 career 에 매달린
행이라, 원장 파일이 없어 slug 를 둘 이유가 없었다.

tool 인자를 id 로 열지 않는 이유는 하나다: 인자를 slug 로 **한정**하는 것이 D3 의
계약이고(경로 인자 없음), 유형마다 인자 이름이 갈리면 모델이 헷갈린다. 그래서 두
유형에는 **결정적 합성 slug** 를 준다.

    career   `<company.slug>-<career.id>`   예: `medisolve-ai-3`
    problem  `problem-<problem.id>`

회사 slug 를 앞에 두는 이유는 모델이 목록에서 본 것을 상세에 다시 넣을 때 「어느
회사의 역할인가」가 눈에 보이기 때문이다.

## 파싱 실패는 404 다 — 존재 여부가 새지 않게

합성 slug 를 복원하지 못했거나, 복원한 id 가 없거나, 그 행이 미노출이거나 — **셋 다
같은 404** 다. 다르게 답하면 AI(그리고 인젝션)가 id 를 훑어 「있는데 안 보여주는 것」과
「없는 것」을 가를 수 있다.
"""

from __future__ import annotations

TYPE_CAREER = "career"
TYPE_PROJECT = "project"
#: 회사에서 만든 제품. 개인 프로젝트(`project`)와 **다른 표·다른 tool** 이다 —
#: 「회사 일」과 「혼자 만든 것」이 섞이면 이력이 흐려진다(spec v0.0.8).
#:
#: ⚠ **값이 표 이름(`product`)이 아니라 `company_product` 다.** 축이 둘이기 때문이다:
#: 어드민 토글의 `{kind}` 는 **표**를 가리켜 `product` 이고(career·project·problem 과 같은
#: 규칙), 이 상수는 **문서·근거 카드의 유형**을 가리킨다(spec v0.0.9 §4 — FE 의
#: `ChatSourceType` 도 `company_product` 다). 두 집합은 원래 다르다 — `note` 는 토글
#: 대상이 아니고, 회사 제품은 카드에서 개인 프로젝트와 구분돼야 한다.
TYPE_COMPANY_PRODUCT = "company_product"
TYPE_PROBLEM = "problem"
TYPE_NOTE = "note"
TYPE_CONTENT = "content"
TYPE_ALGORITHM = "algorithm"

_PROBLEM_PREFIX = "problem-"

#: 근거 카드의 `url` — 그 유형의 **공개 페이지** 경로(SPEC-017 §4 Data Contract).
#: career · problem 은 아이템 전용 페이지가 없다 — 둘 다 `/career` 타임라인 안에서
#: 그려지므로(공개 `GET /api/career` 한 벌에 problem 이 실린다) 그 표면을 가리킨다.
_URL_BUILDERS = {
    TYPE_CAREER: lambda slug: "/career",
    TYPE_PROBLEM: lambda slug: "/career",
    # 회사 제품 — **`/career`**. 제품 하나를 가리키는 전용 페이지는 없지만, 그 제품이
    # 속한 회사 경력이 그려지는 표면은 있다(공개 `GET /api/career` 번들의
    # products_by_career).
    #
    # 한때 여기를 None 으로 뒀다(정확히는 「제품 하나를 가리키는 자리가 아니다」였다).
    # owner 판정으로 뒤집혔다 — **화살표가 있는 카드가 안 눌리는 것이 더 나쁘다.**
    # 정확도보다 눌리는 것이 우선이고, 보낸 자리에 그 제품의 회사 이력이 실제로 있다
    # (2026-08-28 · spec v0.0.9 §4). url null 자체는 여전히 허용값이다 — 링크 없는
    # 카드를 그릴 유형이 나중에 생기면 그때는 None 을 준다.
    TYPE_COMPANY_PRODUCT: lambda slug: "/career",
    TYPE_PROJECT: lambda slug: f"/projects/{slug}",
    TYPE_NOTE: lambda slug: f"/notes/{slug}",
    TYPE_CONTENT: lambda slug: f"/contents/{slug}",
    TYPE_ALGORITHM: lambda slug: f"/algorithms/{slug}",
}


def career_slug(company_slug: str, career_id: int) -> str:
    return f"{company_slug}-{career_id}"


def parse_career_slug(slug: str) -> int | None:
    """`<company>-<id>` → id. 못 읽으면 None (호출부가 404 로 접는다)."""
    _, _, tail = (slug or "").rpartition("-")
    return int(tail) if tail.isdigit() else None


def problem_slug(problem_id: int) -> str:
    return f"{_PROBLEM_PREFIX}{problem_id}"


def parse_problem_slug(slug: str) -> int | None:
    if not (slug or "").startswith(_PROBLEM_PREFIX):
        return None
    tail = slug[len(_PROBLEM_PREFIX) :]
    return int(tail) if tail.isdigit() else None


def public_url(doc_type: str, slug: str) -> str | None:
    """근거 카드가 걸 링크. 모르는 유형이면 None — 억지로 만들지 않는다."""
    builder = _URL_BUILDERS.get(doc_type)
    return builder(slug) if builder else None
