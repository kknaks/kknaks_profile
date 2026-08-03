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
    auto_stages: dict[str, Any] | None = None,
    driver: Any = None,
) -> None:
    if summarizer is not None:
        _registry["summarizer"] = summarizer
    if route_proposer is not None:
        _registry["route_proposer"] = route_proposer
    if stages:
        _registry.setdefault("stages", {}).update(stages)
    if auto_stages:
        _registry.setdefault("auto_stages", {}).update(auto_stages)
    if driver is not None:
        _registry["driver"] = driver


def current_summarizer() -> Any:
    """없으면 `None` — 호출자가 "지금은 불가능"을 사용자에게 알려야 한다.

    조용히 대체 경로를 만들지 않는다. 캡처가 꺼져 있으면 재시도도 안 되는 것이
    사실이고, 사실대로 알리는 편이 낫다.
    """
    return _registry.get("summarizer")


def current_route_proposer() -> Any:
    return _registry.get("route_proposer")


def current_runners() -> dict[str, Any]:
    """스테이지명 → 실행기(`StageRunner`). route 를 포함해 체인 전체가 여기서 나온다.

    없는 스테이지는 키가 없다 — 호출자가 "아직 못 만든다"를 알아야 한다.
    수확도 같은 객체를 쓴다 — 제출한 쪽과 결과를 읽는 쪽이 달라지면 안 된다.
    """
    runners = dict(_registry.get("stages") or {})
    proposer = _registry.get("route_proposer")
    if proposer is not None:
        runners["route"] = proposer
    return runners


def current_auto_stages() -> dict[str, Any]:
    """스테이지명 → auto 스테이지 실행기(`prepare.AutoStage`) (KDEV-WORK-017 P2).

    게이트 실행기(`current_runners`)와 **레지스트리가 다르다.** 둘은 계약이 다르고
    (auto 는 `GateRevision` 을 만들지 않는다) 이름이 겹칠 수도 있다 — 유튜브의
    `collect` 와 잔디의 `collect` 는 같은 이름이지만 하는 일이 다르다.

    비어 있는 이름은 키가 없다. 그 경우 준비부는 **레거시 수집+요약 경로**로 간다 —
    유튜브가 아직 그쪽이다. 등록된 실행기가 있으면 그쪽이 이긴다.
    """
    return dict(_registry.get("auto_stages") or {})


def current_driver() -> Any:
    """진행 중인 항목을 요청 밖에서 미는 드라이버.

    없으면 `None` — 그래도 조회 시 수확이 남아 있어 화면을 열면 따라잡는다.
    """
    return _registry.get("driver")


async def follow(item_id: int) -> None:
    """이 항목을 드라이버가 이어서 밀게 한다. **커밋 뒤에 부른다.**

    실 드라이버는 백그라운드 태스크를 만들고 곧바로 돌아온다 — 여기서 실행 완료를
    기다리지 않는다. `async` 인 것은 테스트가 같은 자리에서 인라인으로 밀어
    결정적으로 검증할 수 있게 하기 위해서다.

    드라이버가 없으면 아무 일도 하지 않는다 — 조용히 실패하는 것이 아니라,
    조회 시 수확이라는 다른 경로가 남아 있다.
    """
    driver = current_driver()
    if driver is not None:
        await driver.follow(item_id)


def clear() -> None:
    _registry.clear()


# 이전 이름 — 호출부가 하나뿐이라 별칭만 남긴다.
def set_summarizer(summarizer: Any) -> None:
    register(summarizer=summarizer)
