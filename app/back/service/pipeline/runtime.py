"""실행 중인 AI 경로를 프로세스 안에서 공유한다 (KDEV-WORK-014).

요약·게이트 제안은 open-kknaks broker 연결이 필요한데, 그 연결은 캡처 런타임이
lifespan 에서 한 번 연다. 큐 API 가 자기 연결을 또 여는 대신 **그것을 빌려 쓴다** —
연결을 두 벌 들고 있으면 어느 쪽이 살아 있는지 알기 어렵고, 종료 순서도 꼬인다.

`--workers 1` 하드락이 이 단순한 모듈 전역을 성립시킨다. 워커가 여럿이면
프로세스마다 다른 값을 보게 되므로 이 방식은 쓸 수 없다.
"""

from __future__ import annotations

from typing import Any

_registry: dict[str, Any] = {}


def register(
    *,
    summarizer: Any = None,
    route_proposer: Any = None,
    stages: dict[str, Any] | None = None,
) -> None:
    if summarizer is not None:
        _registry["summarizer"] = summarizer
    if route_proposer is not None:
        _registry["route_proposer"] = route_proposer
    if stages:
        _registry.setdefault("stages", {}).update(stages)


def current_summarizer() -> Any:
    """없으면 `None` — 호출자가 "지금은 불가능"을 사용자에게 알려야 한다.

    조용히 대체 경로를 만들지 않는다. 캡처가 꺼져 있으면 재시도도 안 되는 것이
    사실이고, 사실대로 알리는 편이 낫다.
    """
    return _registry.get("summarizer")


def current_route_proposer() -> Any:
    return _registry.get("route_proposer")


def current_generators() -> dict[str, Any]:
    """스테이지명 → generator. route 를 포함해 체인 전체가 여기서 나온다.

    없는 스테이지는 키가 없다 — 호출자가 "아직 못 만든다"를 알아야 한다.
    """
    generators = dict(_registry.get("stages") or {})
    proposer = _registry.get("route_proposer")
    if proposer is not None:
        generators["route"] = proposer
    return generators


def clear() -> None:
    _registry.clear()


# 이전 이름 — 호출부가 하나뿐이라 별칭만 남긴다.
def set_summarizer(summarizer: Any) -> None:
    register(summarizer=summarizer)
