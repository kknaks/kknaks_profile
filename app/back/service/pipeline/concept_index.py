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

from core.wikilinks import extract_wikilinks

logger = logging.getLogger("kknaks-back.pipeline.concept-index")

CONCEPT_DIR = "resources/concept"

#: seed 로 인정할 이름의 최소 길이(정규화 후). 아래로 내리면 `락`·`빈`·`큐` 같은
#: 한 글자 별칭이 아무 글에나 걸리고, 그 seed 가 이웃 20건(중앙값)을 끌고 온다.
MIN_SEED_KEY = 2

#: 좁힌 결과가 전량의 이 비율을 넘으면 그냥 전량을 넘긴다 (KDEV-DEC-023 D4).
NARROW_CEILING = 0.6

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
    #: 레포 상대 경로. **payload 에는 안 실린다**(stem 에서 나오는 값이라 중복) —
    #: 보충 흐름이 `target_path` 를 만들 때 쓴다.
    path: str = ""
    #: 이 개념이 딛고 선 상류. frontmatter `up:` 원문이라 별칭일 수 있다.
    up: tuple[str, ...] = ()
    #: 본문 `[[]]` 원문. 〃
    links: tuple[str, ...] = ()

    @property
    def keys(self) -> tuple[str, ...]:
        """이 개념을 찾을 수 있는 이름 전부 — stem·title·aliases."""
        return (self.stem, self.title, *self.aliases)

    @property
    def refs(self) -> tuple[str, ...]:
        """이 개념이 가리키는 것 전부. **계보와 연관을 구분하지 않는다.**

        좁히기는 「관련 있나」만 묻지 「어느 쪽으로 관련 있나」를 묻지 않는다.
        구분이 필요한 것은 그래프 검증(L3~L6)이고 그쪽은 `core/graph.py` 가 한다.
        """
        return (*self.up, *self.links)


@dataclass(frozen=True)
class ConceptIndex:
    entries: dict[str, ConceptEntry] = field(default_factory=dict)
    #: 정규화된 이름 → stem. 충돌하면 먼저 등록된 쪽을 유지하고 경고를 남긴다.
    by_name: dict[str, str] = field(default_factory=dict)
    #: stem → 이 개념을 가리키는 개념들. `neighbors` 의 역방향 절반이다.
    _incoming: dict[str, set[str]] = field(default_factory=dict)

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

    def resolve(self, name: str) -> str | None:
        """이름 하나 → stem. 별칭도 푼다. 없으면 `None`(dead link)."""
        entry, _ = self.match(name)
        return entry.stem if entry else None

    def neighbors(self, stem: str) -> set[str]:
        """이 개념의 이웃 — **양방향**이다.

        나가는 링크만 보면 「A 가 B 를 딛는다」에서 B 로부터 A 를 못 찾는다. 개념은
        나중에 만들어진 쪽이 먼저 것을 가리키므로, 상류만 따라가면 **최근에 자란
        가지가 통째로 안 보인다.**

        실재하지 않는 대상(dead link)은 빠진다 — 프롬프트에 없는 개념을 실을 수 없다.
        """
        out: set[str] = set()
        entry = self.entries.get(stem)
        if entry is not None:
            out |= {r for name in entry.refs if (r := self.resolve(name)) and r != stem}
        out |= self._incoming.get(stem, set())
        return out

    def seeds(self, text: str, *, min_key: int = MIN_SEED_KEY) -> set[str]:
        """텍스트에 이름이 나타나는 개념들 — 좁히기의 **진입점**.

        AI 에 묻지 않는다. 이름이 사전에 있느냐는 사실 판단이고, 사실 판단을 확률
        경로에 태우지 않는다(이 모듈이 세운 원칙 그대로다).

        텍스트를 `normalize` 로 한 번 접고 부분 문자열로 본다. **한국어라 그래야
        한다** — 「추상 클래스」와 「추상클래스」가 같은 것을 가리키고, 조사가 붙어
        「서블릿이」로 나타나기 때문이다.

        `min_key` 보다 짧은 이름은 건너뛴다. `락`·`빈`·`큐` 같은 한 글자 별칭은
        아무 글에나 걸리고, 그렇게 들어온 seed 는 자기 이웃을 통째로 끌고 온다.
        **오탐 하나가 개념 20건이 된다** — 이웃 중앙값이 그 값이다.
        """
        folded = normalize(text)
        if not folded:
            return set()
        return {
            stem
            for key, stem in self.by_name.items()
            if len(key) >= min_key and key in folded
        }

    def narrowed_payload(
        self, text: str, *, min_key: int = MIN_SEED_KEY
    ) -> tuple[list[dict[str, object]], dict[str, object]]:
        """seed + 1홉 이웃만 담은 목록과 **그 판단 근거**.

        근거를 함께 돌려주는 이유는 좁히기가 **조용히 실패하기 때문**이다. seed 가
        0이라 매번 전량이 나가고 있어도 응답 모양은 똑같다 — 로그와 화면이 볼 수
        있어야 한다.

        폴백 둘 다 「의심스러우면 안 자른다」다 (KDEV-DEC-023 D3·D4).
        """
        total = len(self.entries)
        seeds = self.seeds(text, min_key=min_key)

        if not seeds:
            # 새 영역인지 사전이 놓친 것인지 **구분할 방법이 없다.** 놓친 쪽이면
            # 좁히는 순간 있는 개념을 못 보고 새로 만들어 SoT 가 갈라진다.
            return self.as_prompt_payload(), {
                "mode": "all", "reason": "no_seed", "seeds": 0,
                "picked": total, "total": total,
            }

        # **1홉이 상한이다.** 2홉이면 358/363 이라 자르는 의미가 없다 — 파라미터로
        # 열어 두면 언젠가 켜진다(DEC-023 D2).
        picked = set(seeds)
        for s in seeds:
            picked |= self.neighbors(s)

        if total and len(picked) > total * NARROW_CEILING:
            # 여기부터는 목록을 두 벌 만드는 비용만 남는다.
            return self.as_prompt_payload(), {
                "mode": "all", "reason": "over_ceiling", "seeds": len(seeds),
                "picked": total, "total": total,
            }

        return self.as_prompt_payload(picked), {
            "mode": "narrowed", "reason": None, "seeds": len(seeds),
            "picked": len(picked), "total": total,
        }

    def as_prompt_payload(self, stems: set[str] | None = None) -> list[dict[str, object]]:
        """AI 에 넘길 목록 — 본문은 넣지 않는다.

        전문을 다 넣으면 프롬프트가 터진다. 보충이 필요하면 에이전트가 해당 파일을
        직접 읽는다(레포가 마운트돼 있다).

        `path` 를 넣지 않는다(KDEV-DEC-023 D5) — `resources/concept/{stem}.md` 라
        stem 에서 그대로 나오는 값이고, 363건이면 12,000자가 중복이었다.

        `stems` 를 주면 그것만 낸다. 좁히기 판정은 `narrowed_payload` 가 한다.
        """
        picked = (
            sorted(self.entries.values(), key=lambda e: e.stem)
            if stems is None
            else sorted(
                (e for s in stems if (e := self.entries.get(s))), key=lambda e: e.stem
            )
        )
        return [
            {"stem": e.stem, "title": e.title, "aliases": list(e.aliases)} for e in picked
        ]


def _as_names(raw) -> list[str]:
    """`up:` 은 문자열 하나일 수도 목록일 수도 있다. 둘 다 받는다."""
    if raw is None:
        return []
    if isinstance(raw, str):
        raw = [raw]
    return [str(v).strip() for v in raw if str(v).strip()]


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
        # **본문은 이미 손에 있다.** `frontmatter.load` 가 열면서 같이 읽었으니
        # 이웃을 채우는 데 추가 I/O 가 없다 — 지금까지 버리고 있었을 뿐이다.
        entry = ConceptEntry(
            stem=stem,
            title=str(post.metadata.get("title") or stem),
            aliases=_aliases_of(post.metadata),
            path=f"{CONCEPT_DIR}/{path.name}",
            up=tuple(_as_names(post.metadata.get("up"))),
            links=tuple(extract_wikilinks(post.content)),
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

    # 역방향 인덱스는 **전부 등록된 뒤에** 만든다 — 뒤에 나올 개념을 가리키는
    # 링크가 먼저 나오므로, 등록 중에 풀면 그 링크가 dead 로 보인다.
    for stem, entry in index.entries.items():
        for name in entry.refs:
            target = index.resolve(name)
            if target is None or target == stem:
                continue
            index._incoming.setdefault(target, set()).add(stem)
    return index


def read_concept(repo_root: Path, stem: str) -> str | None:
    path = repo_root / CONCEPT_DIR / f"{stem}.md"
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None
