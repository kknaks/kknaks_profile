"""기존 concept 조회 — 이름과 alias 로 찾는다 (KDEV-WORK-015 P2).

**매칭을 AI 에 맡기지 않는다.** 개념이 이미 있는지는 파일 목록을 보면 알 수 있는
사실이고, 사실 판단을 확률적 경로에 태울 이유가 없다. AI 는 *무엇을 뽑을지*를 정하고,
*그게 이미 있는 것인지*는 여기서 결정적으로 판정한다.

틀렸을 때의 비용이 비대칭이다.
- **놓치면**(있는데 신규로 만듦) 같은 개념이 두 파일로 갈라져 SoT 가 둘이 된다.
- **오매칭이면**(다른 개념을 같은 것으로 봄) 남의 노트를 덮어쓴다.

둘 다 나쁘지만 오매칭이 더 나쁘다 — 갈라진 건 나중에 합칠 수 있지만 덮어쓴 건
git 이력을 뒤져야 한다. 그래서 정규화는 **보수적으로** 한다(공백·하이픈만 무시).
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

import frontmatter

logger = logging.getLogger("kknaks-back.pipeline.concept-index")

CONCEPT_DIR = "resources/concept"

#: 공백·하이픈·밑줄만 무시한다. 어간 추출이나 부분 일치는 하지 않는다 —
#: "스트리밍 ASR" 과 "ASR" 은 다른 개념일 수 있다.
_NORM_RE = re.compile(r"[\s_-]+")


def normalize(value: str) -> str:
    return _NORM_RE.sub("", (value or "").strip().casefold())


@dataclass(frozen=True)
class ConceptEntry:
    stem: str
    title: str
    aliases: tuple[str, ...]
    path: str

    @property
    def keys(self) -> tuple[str, ...]:
        """이 개념을 찾을 수 있는 이름 전부 — stem·title·aliases."""
        return (self.stem, self.title, *self.aliases)


@dataclass(frozen=True)
class ConceptIndex:
    entries: dict[str, ConceptEntry] = field(default_factory=dict)
    #: 정규화된 이름 → stem. 충돌하면 먼저 등록된 쪽을 유지하고 경고를 남긴다.
    by_name: dict[str, str] = field(default_factory=dict)

    def get(self, stem: str) -> ConceptEntry | None:
        return self.entries.get(stem)

    def match(self, name: str) -> tuple[ConceptEntry | None, str | None]:
        """이름 하나로 기존 개념을 찾는다. `(항목, 매칭된 이름)`.

        못 찾으면 `(None, None)` — 신규 생성 후보다.
        """
        key = normalize(name)
        if not key:
            return None, None
        stem = self.by_name.get(key)
        if stem is None:
            return None, None
        entry = self.entries.get(stem)
        if entry is None:
            return None, None
        # 어떤 이름으로 걸렸는지 돌려준다 — 화면이 "무엇 때문에 같다고 봤는지" 를 보여준다.
        for candidate in entry.keys:
            if normalize(candidate) == key:
                return entry, candidate
        return entry, None

    def match_any(self, names: list[str]) -> tuple[ConceptEntry | None, str | None]:
        for name in names:
            entry, matched = self.match(name)
            if entry is not None:
                return entry, matched
        return None, None

    def as_prompt_payload(self) -> list[dict[str, object]]:
        """AI 에 넘길 목록 — 본문은 넣지 않는다.

        전문을 다 넣으면 프롬프트가 터진다. 보충이 필요하면 에이전트가 해당 파일을
        직접 읽는다(레포가 마운트돼 있다).
        """
        return [
            {"stem": e.stem, "title": e.title, "aliases": list(e.aliases), "path": e.path}
            for e in sorted(self.entries.values(), key=lambda e: e.stem)
        ]


def _aliases_of(meta: dict) -> tuple[str, ...]:
    raw = meta.get("aliases") or []
    if isinstance(raw, str):
        raw = [raw]
    return tuple(str(v).strip() for v in raw if str(v).strip())


def build_index(repo_root: Path) -> ConceptIndex:
    """`resources/concept/` 를 훑어 인덱스를 만든다. flat 이라 재귀하지 않는다."""
    index = ConceptIndex()
    directory = repo_root / CONCEPT_DIR
    if not directory.is_dir():
        return index

    for path in sorted(directory.glob("*.md")):
        if path.name == "README.md":
            continue
        try:
            post = frontmatter.load(path)
        except Exception as exc:  # noqa: BLE001
            logger.warning("concept frontmatter 파싱 실패 %s — %s", path, exc)
            continue

        stem = path.stem
        entry = ConceptEntry(
            stem=stem,
            title=str(post.metadata.get("title") or stem),
            aliases=_aliases_of(post.metadata),
            path=f"{CONCEPT_DIR}/{path.name}",
        )
        index.entries[stem] = entry
        for name in entry.keys:
            key = normalize(name)
            if not key:
                continue
            owner = index.by_name.get(key)
            if owner is not None and owner != stem:
                # 같은 이름을 두 개념이 주장하면 자동으로 고르지 않는다.
                # 먼저 등록된 쪽을 유지하고 사람이 볼 수 있게 남긴다.
                logger.warning(
                    "alias 충돌: '%s' 를 %s 와 %s 가 함께 주장한다", name, owner, stem
                )
                continue
            index.by_name[key] = stem
    return index


def read_concept(repo_root: Path, stem: str) -> str | None:
    path = repo_root / CONCEPT_DIR / f"{stem}.md"
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None
