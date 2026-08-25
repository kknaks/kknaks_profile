"""시드 전체 실행 — 의존 순서대로 돈다. 각 시드는 멱등이라 몇 번을 돌려도
같은 상태가 된다(재실행이 값을 안 되돌린다, _RESUME.md §6).

    uv run python -m seed

개별 실행은 그대로 된다:  uv run python -m seed.seed_profile 등.

## 시드의 경계 — 여기 없는 표는 일부러 없다

| 표 | 왜 시드가 없나 |
|---|---|
| git_token | **비밀** — 토큰 원문(Fernet 암호문)은 시드 대상이 아니다. 어드민에서 입력 |
| repo.git_token_id | 같은 이유 — 토큰 연결도 어드민에서 사람이 다시 한다(seed_repos 머리 주석) |
| queue · gate | 파이프라인 런타임 기록 — 재현할 상태가 아니다 |
| commit | 수집 파생 — 수집기(케이스 6·7)가 다시 채운다 |
| problem | 어드민 입력(게이트 승인 산출) — 시드 원료가 없다 |
"""

from __future__ import annotations

import asyncio

from seed import (
    seed_algorithms,
    seed_companies,
    seed_contents,
    seed_education,
    seed_notes,
    seed_products,
    seed_profile,
    seed_projects,
    seed_repos,
    seed_site_config,
    seed_users,
)

# 의존 순서 — profile → users(FK) → companies(career) → products(career FK)
# → projects → repos(product·project FK). 나머지는 profile 만 본다.
_SEEDS = [
    seed_profile,
    seed_users,
    seed_site_config,
    seed_companies,
    seed_education,
    seed_products,
    seed_projects,
    seed_contents,
    seed_notes,
    seed_algorithms,
    seed_repos,
]


async def main() -> None:
    for module in _SEEDS:
        print(f"\n── {module.__name__} " + "─" * 30)
        await module.seed()


if __name__ == "__main__":
    asyncio.run(main())
