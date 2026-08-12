"""입구 회수 — 종결된 공부 노트의 `inbox/` 원본을 커밋에서 지운다 (KDEV-DEC-021 D1).

접수는 작업트리에서 파일을 지운다. **그 삭제가 커밋되지 않으면** `reset --hard` 한
번에 되살아나고, 「입구에 파일이 있으면 곧 미처리」라는 약속이 깨진다.

삭제가 커밋되는 시점은 **항목이 종결될 때**다. 종결이 셋이라 회수 자리도 셋이다.

    published   산출물과 **같은 커밋**으로 (`plan.build_actions` 의 `remove` 액션)
    discarded   갈 곳이 없다. 여기서 회수 커밋 하나를 낸다
    deleted     〃

첫째만 발행 계획 안에 있는 이유는 **원자성** 때문이다. 노트가 나가는 커밋과 원본이
사라지는 커밋이 갈리면 「발행됐는데 입구에 원본이 남은」 중간 상태가 생긴다. 폐기와
삭제는 함께 나갈 산출물이 없어 그 문제가 없다.

실패 상태(`prepare_failed`·`publish_failed`)는 여기 없다. **종결이 아니라서** 같은
노트를 다시 push 하면 기존 항목에 합류하고(`ITEM_PENDING_STATUSES`), 그 항목이 나중에
발행되거나 폐기될 때 이 회수가 돈다.
"""

from __future__ import annotations

import logging
from pathlib import Path

from core.models import QueueItem

from .git import PublishOutcome, publish_atomic

logger = logging.getLogger("kknaks-back.apply.reclaim")


def inbox_path(item: QueueItem) -> str | None:
    """이 항목이 어느 입구 파일에서 왔는가. 공부 노트가 아니면 `None`.

    `normalized_url` 이 `study:{slug}` 라 그 값 하나가 출처를 안다 — 컬럼을 늘리지
    않은 이유이자, 잔디가 `daily:{date}` 를 쓰는 것과 같은 자리다.
    """
    from service.pipeline.study_intake import KEY_PREFIX

    key = item.normalized_url or ""
    if not key.startswith(KEY_PREFIX):
        return None
    slug = key[len(KEY_PREFIX) :]
    return f"inbox/{slug}.md" if slug else None


def _tracked(repo_root: Path, path: str) -> bool:
    """이 경로가 git 인덱스에 있는가 — 즉 **지울 커밋 이력이 있는가.**

    파일을 지운 뒤에도 인덱스에는 남아 있으므로 이 판정이 성립한다.
    """
    import subprocess

    return (
        subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", path],
            cwd=repo_root,
            capture_output=True,
        ).returncode
        == 0
    )


def reclaim_inbox(
    item: QueueItem, *, repo_root: Path, dry_run: bool = True
) -> PublishOutcome | None:
    """종결된 항목의 입구 원본을 회수한다. 회수할 것이 없으면 `None`.

    **예외를 올리지 않는다.** 폐기·삭제는 이미 확정된 사람의 결정이고, git 이 실패했다고
    그것을 되돌리면 안 된다 — 파일 하나가 커밋 안 된 채 남는 것이 항목 상태가 어긋나는
    것보다 낫다. 실패는 로그로 남고 다음 회수 기회(재폐기는 없으므로 사람의 손)에 걸린다.

    이미 커밋돼 있지 않은 파일이면 `publish_atomic` 이 「커밋할 것이 없다」로 조용히
    성공한다 — 로컬에서 만들어 push 하지 않은 노트가 그렇다.
    """
    path = inbox_path(item)
    if path is None:
        return None

    # 작업트리에서는 접수가 이미 지웠다. 여기서 하는 일은 **그 삭제를 커밋에 싣는
    # 것**뿐이라, 파일이 아직 남아 있으면(접수가 `delete=False` 였다) 지워 준다.
    target = repo_root / path
    if target.exists():
        try:
            target.unlink()
        except OSError as exc:  # noqa: BLE001
            logger.warning("입구 원본을 지우지 못했다 %s — %s", path, exc)
            return None

    if not _tracked(repo_root, path):
        # **커밋할 것이 없으면 부르지 않는다.** 로컬에서 만들고 push 하지 않은 노트가
        # 그렇다. 그냥 넘기면 `git add` 가 `did not match any files` 로 죽고,
        # `publish_atomic` 이 그것을 발행 실패로 보아 **레포 전체에 `reset --hard` +
        # `clean -fd`** 를 건다 — 남의 미커밋 작업까지 날아간다.
        logger.info("회수할 것이 없다 — %s 는 추적되지 않는다", path)
        return None

    try:
        outcome = publish_atomic(
            [path],
            f"chore(inbox): {path} 회수 — item #{item.id} {item.status}",
            repo_root=repo_root,
            dry_run=dry_run,
        )
    except Exception as exc:  # noqa: BLE001 — 종결을 되돌리지 않는다
        logger.warning("입구 회수 실패 item=%s path=%s — %s", item.id, path, exc)
        return None

    if not outcome.ok:
        logger.warning(
            "입구 회수 실패 item=%s path=%s — %s", item.id, path, outcome.error_code
        )
    return outcome
