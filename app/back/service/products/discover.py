"""미등록 레포 발견 (KDEV-WORK-018 P3 / KDEV-DEC-017 D17).

**D12(레포 4개 편입)만으로는 재발을 못 막는다.** 오늘 발견한 것을 채울 뿐, 다음 달에
레포를 하나 더 파면 같은 일이 반복된다.

근본 원인은 레지스트리가 `showcase.md` 에서 시드돼 **그 사각지대를 그대로 물려받았다**는
것이고, 그 뒤로 발견 장치가 없었다는 것이다. 실패가 침묵한다 — 레포를 파도, 커밋을
쌓아도, 09:05 잔디가 돌아도 알림이 없고 **잡은 성공으로 끝난다.**

**막지 않고 알린다.** 자동 등록하지 않는다 — 무엇을 추적할지는 사람이 정한다.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import httpx

import config
from service.jobs.repo_registry import PERSONAL_OWNERS

logger = logging.getLogger("kknaks-back.products.discover")

_API = "https://api.github.com"
_PER_PAGE = 100
#: 페이지를 무한히 넘기지 않는다. 개인 레포가 300개를 넘으면 그때 페이징을 손본다.
_MAX_PAGES = 3

#: 배너에 올릴 최근성 창(일). **실측으로 정했다** — 미등록 57건 중 29건이 1년 넘게
#: 안 민 것이고, 30일 안쪽은 5건이다. 그 5건이 전부 실제로 손대고 있는 레포였다.
#:
#: 오래된 것을 거르는 근거는 이 배너가 막으려는 실패가 **"팠는데 등록을 잊었다"** 이기
#: 때문이다. 그건 작업을 시작한 직후에 드러나고, 다시 손대면 창 안으로 돌아온다.
#: 57건을 다 띄우면 배너가 소음이 되고, 소음이 되면 아무도 안 본다.
DISCOVERY_WINDOW_DAYS = 30


@dataclass(frozen=True)
class DiscoveredRepo:
    slug: str
    account: str
    pushed_at: str | None = None
    private: bool = False


@dataclass(frozen=True)
class Discovery:
    """발견 결과. **잘린 수를 함께 낸다.**

    조용히 자르면 "미등록이 0건" 과 "오래돼서 감춘 게 29건" 이 화면에서 같아 보인다.
    """

    items: list[DiscoveredRepo]
    hidden_old: int = 0


class DiscoveryError(RuntimeError):
    """목록을 못 받았다. **배너만 실패하고 화면은 정상 표시된다.**"""


def _headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "kknaks-profile-registry",
    }


async def _fetch(client: httpx.AsyncClient, url: str, token: str) -> list[dict]:
    out: list[dict] = []
    for page in range(1, _MAX_PAGES + 1):
        res = await client.get(
            url,
            headers=_headers(token),
            params={"per_page": _PER_PAGE, "page": page, "sort": "pushed"},
        )
        if res.status_code >= 400:
            raise DiscoveryError(f"GitHub {res.status_code} — {url}")
        batch = res.json()
        out += batch
        if len(batch) < _PER_PAGE:
            break
    return out


def _keep(item: dict, *, owners: tuple[str, ...]) -> bool:
    """**거를 것을 거르지 않으면 배너가 소음이 되고, 소음이 되면 아무도 안 본다.**

    - fork — 남의 코드다. 내 커밋이 있어도 그 레포의 작업이 아니다
    - archived — 끝난 것을 다시 추적하자고 권할 이유가 없다
    - 타인 소유 — 조직 레포 중 내가 안 건드린 것까지 뜬다
    """
    if item.get("fork") or item.get("archived"):
        return False
    owner = str((item.get("owner") or {}).get("login") or "")
    return owner in owners


def _within_window(pushed_at: str | None, *, days: int) -> bool:
    if not pushed_at:
        return False
    try:
        when = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
    except ValueError:
        return False
    return (datetime.now(timezone.utc) - when) <= timedelta(days=days)


async def list_undiscovered(
    known: set[str], *, window_days: int = DISCOVERY_WINDOW_DAYS
) -> Discovery:
    """계정·조직 레포에서 레지스트리에 없는 것을 찾는다.

    **화면 진입 시 부른다.** 스케줄 잡으로 만들지 않는 이유는 배너가 볼 사람이 화면에
    있을 때만 의미가 있기 때문이다.
    """
    accounts = config.gh_accounts()
    if not accounts:
        raise DiscoveryError("GitHub 토큰이 없다 — 미등록 확인을 할 수 없다")

    found: dict[str, DiscoveredRepo] = {}
    async with httpx.AsyncClient(timeout=10) as client:
        for acc in accounts:
            token = acc.get("token")
            if not token:
                continue
            kind = "personal" if acc.get("user") in PERSONAL_OWNERS else "company"
            owners = PERSONAL_OWNERS if kind == "personal" else (acc.get("org") or "",)
            try:
                items = await _fetch(client, f"{_API}/user/repos?affiliation=owner", token)
            except DiscoveryError:
                # 계정 하나가 막혀도 나머지는 본다 — 부분 결과가 없는 것보다 낫다.
                logger.warning("레포 목록 조회 실패 — account=%s", acc.get("user"))
                continue
            for item in items:
                if not _keep(item, owners=tuple(o for o in owners if o)):
                    continue
                slug = str(item.get("full_name") or "")
                if not slug or slug in known or slug in found:
                    continue
                found[slug] = DiscoveredRepo(
                    slug=slug,
                    account=kind,
                    pushed_at=item.get("pushed_at"),
                    private=bool(item.get("private")),
                )

    # 최근에 민 것이 위로. 등록할 만한 것이 대개 그쪽이다.
    ordered = sorted(found.values(), key=lambda r: r.pushed_at or "", reverse=True)
    fresh = [r for r in ordered if _within_window(r.pushed_at, days=window_days)]
    return Discovery(items=fresh, hidden_old=len(ordered) - len(fresh))
