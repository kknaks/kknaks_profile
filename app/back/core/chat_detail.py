"""공개 문서 루트 밖은 읽지 않는다 (SPEC-017 §4 공개 문서 루트 · §5 · DEC-027 D3).

`core/detail.read_detail` 은 「DB 가 가리키는 md 를 읽는다」이고 신뢰 경계가 없다 —
어드민이 넣은 값을 그대로 믿는 것이 그 자리에선 맞다. 그런데 chat-tool 은 **AI 가
slug 로 고른 행**의 `detail_path` 를 읽으므로, 어드민 실수나 과거 데이터가
`para/resources/persona/…` 같은 개인 지식을 가리키면 그게 그대로 AI 에게 간다.

그래서 유형별로 **허용 루트**를 못 박고 그 밖이면 읽지 않는다. AI 가 경로를 넘기는
경로는 애초에 없지만(인자는 slug 뿐), 경계를 지시가 아니라 구조로 두는 것이 DEC-027 의
태도다 — 여기서 한 겹 더 막는다.

## 허용 단위가 둘이다 — 디렉토리와 **파일 하나**

`summer-star` 는 디렉토리를 통째로 연다(개인 프로젝트라 그 아래가 전부 공개다).
`company` 는 다르다 — 같은 제품 디렉토리 안에 **공개 자료(showcase.md)와 회사 내부
기록(`log/` 작업 회고 · README)이 섞여 있다.** 그래서 디렉토리가 아니라 **파일 하나**를
연다(2026-08-28 owner 피드백 · spec v0.0.7 §4).

showcase.md 를 여는 근거: 그것은 사이트가 이미 공개로 그리는 상세다(공개 `GET /api/career`
번들이 `product_bodies` 로 같은 파일을 내려준다). 사이트가 주는 것을 chat 만 못 주면
「회사 프로젝트는 안 했니?」에 과하게 사리게 된다 — 실제로 그랬다.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from config import get_settings
from core.detail import read_detail


@dataclass(frozen=True)
class _Root:
    """허용 자리 하나.

    `filename` 이 None 이면 `prefix` 아래 **전부**, 아니면 `prefix/<한 단계>/<filename>`
    **정확히 그 모양만** 허용한다. 후자가 회사 제품용이다 — 깊이를 한 단계로 묶어야
    `company/<제품>/log/showcase.md` 같은 하위 디렉토리의 동명 파일이 새지 않는다.
    """

    prefix: str
    filename: str | None = None


#: 유형 → 이 유형의 md 가 살아도 되는 자리.
#: `para/projects/` 를 통째로 열지 않는 이유 = 그 아래 `company/` 는 회사 기록이고,
#: 거기서 공개인 것은 제품마다 `showcase.md` 한 파일뿐이다.
PUBLIC_ROOTS: dict[str, tuple[_Root, ...]] = {
    "project": (_Root("para/projects/summer-star/"),),
    # 회사 제품 — **showcase.md 한 파일만**. `log/`·README 는 그대로 404 다.
    # 두 자리인 이유: 현직 제품은 `projects/company/`, 전 회사 제품은 `archive/company/`
    # 에 산다(charty·linky·quantus — 채용담당자 질문의 핵심이라 spec v0.0.8 이 둘 다 열었다).
    "company_product": (
        _Root("para/projects/company/", filename="showcase.md"),
        _Root("para/archive/company/", filename="showcase.md"),
    ),
    "note": (_Root("para/resources/note/"),),
    "content": (_Root("para/resources/youtube/"),),
    "algorithm": (_Root("para/resources/algorithms/"),),
}


def is_public_path(doc_type: str, detail_path: str | None) -> bool:
    """이 유형이 읽어도 되는 자리인가. 심링크·`..` 이탈까지 실경로로 본다."""
    roots = PUBLIC_ROOTS.get(doc_type)
    if not roots or not detail_path:
        return False
    repo_root = Path(get_settings().repo_root).resolve()
    # resolve() 로 `..` 과 심링크를 편 뒤 비교한다 — 문자열 prefix 검사만으로는
    # `para/resources/note/../persona/x.md` 가 통과한다.
    try:
        target = (repo_root / detail_path).resolve()
    except (OSError, RuntimeError):
        return False
    for root in roots:
        allowed = (repo_root / root.prefix).resolve()
        # 루트 **아래**여야 한다. 루트 자신은 디렉토리라 문서가 아니다.
        if allowed not in target.parents:
            continue
        if root.filename is None:
            return True
        # `<제품>/showcase.md` — 단계 수까지 본다(위 `_Root` 주석).
        relative = target.relative_to(allowed).parts
        if len(relative) == 2 and relative[-1] == root.filename:
            return True
    return False


def read_public_detail(doc_type: str, detail_path: str | None) -> str | None:
    """공개 루트 안이면 md 본문, 아니면 None. **거부와 「파일 없음」을 구분하지 않는다.**

    구분하면 AI 에게 「있는데 못 준다」가 보인다 — 그 자체가 원장 구조에 대한 정보다.
    """
    if not is_public_path(doc_type, detail_path):
        return None
    return read_detail(detail_path)
