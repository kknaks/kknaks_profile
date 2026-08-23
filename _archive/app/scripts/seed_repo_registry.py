"""배포 1회용 스크립트 — 레포 레지스트리 시드 (KDEV-WORK-017 P5).

`tracked_repos` 는 잔디 조사 대상의 SoT 다. **비어 있으면 파이프라인은 정상 동작하면서
아무것도 내지 않는다** — `collect` 가 훑을 레포가 0건이라 매일 `NO_ACTIVITY` 로 끝난다.
실패로 보이지 않아서 한참 모른다. 배포 직후 한 번 돌려 채운다.

두 단계로 나뉘는 이유는 `company` 의 `detail`(career 귀속) 을 시드가 지어낼 수 없기
때문이다. `showcase.md` 에 그 정보가 없고 어느 career 문서로 갈지는 사람이 정한다.

    1. studio  — `showcase.md` 스캔 + 카드 없는 레포 목록(`CARDLESS_REPOS`)
    2. company — `COMPANY_REPOS` 에 `--company-detail` 로 받은 stem 을 붙여 넣는다
    3. product — 기존 행의 빈 `product_slug` 를 채운다 (KDEV-WORK-018 P2)

**다시 돌려도 안전하다.** 이미 있는 slug 는 건드리지 않는다 — `detail`·`enabled`·
`path_rules` 가 사람이 손본 값이라 덮어쓰면 안 된다. 새 레포만 들어온다.

사용법:

    docker exec -w /repo/app/back kknaks-back \\
        uv run python ../scripts/seed_repo_registry.py --company-detail medisolve-ai

    # 무엇이 들어갈지만 보고 커밋하지 않는다
    ... --company-detail medisolve-ai --dry-run

    # studio 만 넣고 company 는 나중에
    ... (--company-detail 생략)

전제:
- DB 가 떠 있고 마이그레이션이 `0009` 이상 (레지스트리 테이블 + `product_slug`)
- `--company-detail` 은 `persona/career/{stem}.md` 가 실재해야 한다
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from pathlib import Path

BACK_DIR = Path(__file__).resolve().parents[1] / "back"
sys.path.insert(0, str(BACK_DIR))

import config  # noqa: E402
from service.jobs.repo_registry import (  # noqa: E402
    UnknownCareerError,
    backfill_product_slug,
    seed_company_from_showcase,
    seed_from_showcase,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)


def _args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="레포 레지스트리 시드 (1회)")
    parser.add_argument(
        "--company-detail",
        metavar="STEM",
        help="company 레포를 귀속시킬 career stem (예: medisolve-ai). "
        "생략하면 company 는 건너뛴다",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="무엇이 들어갈지 보고 커밋하지 않는다",
    )
    return parser.parse_args()


async def main() -> int:
    args = _args()
    repo_root = config.repo_root()

    from core.db import new_session

    async with new_session() as db:
        studio = await seed_from_showcase(db, repo_root)
        print(
            f"studio  — added={studio['added']} "
            f"needs_detail={studio['needs_detail']} existing={studio['existing']}"
        )

        company = {"added": 0}
        if args.company_detail:
            try:
                company = await seed_company_from_showcase(
                    db, repo_root, detail=args.company_detail
                )
            except UnknownCareerError as exc:
                # 커밋하지 않고 죽는다 — studio 만 반쯤 들어간 상태를 남기지 않는다.
                print(f"\n실패: {exc}", file=sys.stderr)
                return 1
            print(f"company — added={company['added']} detail={company['detail']}")
        elif studio["needs_detail"]:
            print(
                f"\ncompany {studio['needs_detail']}건이 남아 있다 — "
                "`--company-detail <stem>` 으로 다시 돌린다"
            )

        # 컬럼이 `0009` 로 새로 생겨 기존 행은 전부 비어 있다. 새로 넣은 행은 이미
        # 채워져 있으므로 여기서 채워지는 것은 **먼저 시드된 13행**뿐이다.
        product = await backfill_product_slug(db)
        print(
            f"product — filled={product['filled']} kept={product['kept']} "
            f"no_product={product['no_product']}"
        )

        if args.dry_run:
            await db.rollback()
            print("\n[dry-run] 커밋하지 않았다")
            return 0

        await db.commit()

    total = studio["added"] + company["added"]
    print(f"\n=== 시드 완료: {total}건 추가 ===")
    if total == 0:
        print("추가된 것이 없다 — 이미 시드됐거나 showcase 에 대상이 없다")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
