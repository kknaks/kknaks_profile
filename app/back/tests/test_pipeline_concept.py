"""concept 게이트 — 매칭과 재검증 (KDEV-WORK-015 P2).

이 파이프라인의 실질 품질은 추출이 아니라 **매칭**이 결정한다.

- 놓치면(있는데 신규로 만듦) 같은 개념이 두 파일로 갈라져 SoT 가 둘이 된다.
- 오매칭이면(다른 개념을 같은 것으로 봄) 남의 노트를 덮어쓴다.

둘 다 나쁘지만 오매칭이 더 나쁘다 — 갈라진 건 합칠 수 있지만 덮어쓴 건 git 이력을
뒤져야 한다. 그래서 **의심스러우면 실패시킨다.**
"""

from __future__ import annotations

from pathlib import Path

import pytest

from service.pipeline.concept_index import build_index, normalize
from service.pipeline.gates import GateError
from service.pipeline.stages.concept import verify_concepts

REFERENCE_STEM = "2026-07-28-sample-source"


def _concept_md(
    *,
    stem: str,
    title: str = "샘플 개념",
    aliases: tuple[str, ...] = ("샘플", "sample"),
    ups: tuple[str, ...] = (REFERENCE_STEM,),
    body_extra: str = "",
) -> str:
    """concept 노트 한 장.

    `textwrap.dedent` 를 쓰지 않는다 — 여러 줄 값을 끼우면 둘째 줄부터 들여쓰기가
    달라져 공통 접두가 무너지고 frontmatter 가 깨진다.
    """
    lines = ["---", "type: concept", f"id: {stem}", f"title: {title}", "aliases:"]
    lines += [f"  - {a}" for a in aliases]
    lines += ["up:"]
    lines += [f"  - {u}" for u in ups]
    lines += ["---", "", f"# {title}", "", "정의.", body_extra, "", "## 출처", ""]
    lines += [f"- [[{u}]] — 출처" for u in ups]
    return "\n".join(lines) + "\n"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "resources/concept").mkdir(parents=True)
    return tmp_path


def _write_existing(repo: Path, stem: str, **kw) -> None:
    (repo / "resources/concept" / f"{stem}.md").write_text(
        _concept_md(stem=stem, **kw), encoding="utf-8"
    )


def _verify(repo: Path, concepts, *, reference_stem: str | None = REFERENCE_STEM):
    return verify_concepts(
        concepts, index=build_index(repo), repo_root=repo, reference_stem=reference_stem
    )


class TestNormalize:
    @pytest.mark.parametrize(
        "a, b",
        [
            ("음성 인식", "음성인식"),
            ("STT", "stt"),
            ("gpt-4", "GPT 4"),
            ("structure_content", "structure-content"),
        ],
    )
    def test_equivalent_names(self, a, b):
        assert normalize(a) == normalize(b)

    def test_different_concepts_stay_different(self):
        """부분 일치나 어간 추출은 하지 않는다 — 'ASR' 과 '스트리밍 ASR' 은 다를 수 있다."""
        assert normalize("ASR") != normalize("스트리밍 ASR")


class TestIndex:
    def test_matches_by_alias(self, repo):
        _write_existing(repo, "stt", title="음성 인식", aliases=("STT", "speech to text"))
        index = build_index(repo)
        entry, matched = index.match("speech-to-text")
        assert entry is not None and entry.stem == "stt"
        assert matched == "speech to text"

    def test_readme_is_not_a_concept(self, repo):
        (repo / "resources/concept/README.md").write_text("# 안내", encoding="utf-8")
        assert build_index(repo).entries == {}

    def test_alias_conflict_keeps_first_and_does_not_crash(self, repo):
        """같은 이름을 두 개념이 주장하면 자동으로 고르지 않는다."""
        _write_existing(repo, "aaa", aliases=("겹치는이름",))
        _write_existing(repo, "bbb", aliases=("겹치는이름",))
        index = build_index(repo)
        entry, _ = index.match("겹치는이름")
        assert entry is not None and entry.stem == "aaa"

    def test_prompt_payload_omits_body(self, repo):
        """전문을 다 넣으면 프롬프트가 터진다 — 필요하면 에이전트가 직접 읽는다."""
        _write_existing(repo, "abc")
        payload = build_index(repo).as_prompt_payload()
        # `path` 는 빠졌다 — `stem` 에서 나오는 값이라 363건이면 12,000자가
        # 중복이었다 (KDEV-DEC-023 D5). 엔트리에는 남아 보충 흐름이 쓴다.
        assert set(payload[0]) == {"stem", "title", "aliases"}


class TestCreate:
    def test_new_concept_passes(self, repo):
        results = _verify(repo, [{"filename_stem": "new-idea", "mode": "create",
                                  "names": ["새 개념"], "content": _concept_md(stem="new-idea")}])
        assert results[0]["mode"] == "create"
        assert results[0]["target_path"] == "resources/concept/new-idea.md"
        assert results[0]["excluded"] is False

    def test_create_over_existing_is_rejected(self, repo):
        """이 스테이지에서 가장 비싼 실수 — 조용히 통과시키지 않는다."""
        _write_existing(repo, "stt", title="음성 인식", aliases=("STT",))
        with pytest.raises(GateError) as exc:
            _verify(repo, [{"filename_stem": "speech-to-text", "mode": "create",
                            "names": ["STT"], "content": _concept_md(stem="speech-to-text")}])
        assert exc.value.code == "CONCEPT_ALREADY_EXISTS"
        assert "stt" in exc.value.message

    def test_alias_only_match_blocks_creation(self, repo):
        """stem 이 전혀 달라도 **alias 로만 걸리는 경우**를 잡아야 한다.

        여기가 alias 의 존재 이유다 — 이걸 놓치면 같은 개념이 두 파일로 갈라진다.
        """
        # title 을 일부러 다르게 둬서 **alias 로만** 걸리는 경로를 확인한다.
        _write_existing(repo, "stt", title="자동 음성 전사", aliases=("음성인식", "speech to text"))
        with pytest.raises(GateError) as exc:
            _verify(repo, [{"filename_stem": "voice-recognition", "mode": "create",
                            "names": ["음성 인식"],
                            "content": _concept_md(stem="voice-recognition")}])
        assert exc.value.code == "CONCEPT_ALREADY_EXISTS"
        # 무엇 때문에 같다고 봤는지가 메시지에 있어야 사람이 판단할 수 있다.
        assert "음성인식" in exc.value.message and "stt" in exc.value.message

    def test_empty_list_is_allowed(self, repo):
        """뽑을 개념이 없으면 억지로 만들지 않는다."""
        assert _verify(repo, []) == []

    def test_duplicate_stem_in_one_batch_rejected(self, repo):
        payload = {"filename_stem": "dup", "mode": "create", "names": [],
                   "content": _concept_md(stem="dup")}
        with pytest.raises(GateError) as exc:
            _verify(repo, [payload, dict(payload)])
        assert exc.value.code == "DUPLICATE_CONCEPT"


class TestSupplement:
    def test_second_source_supplements(self, repo):
        """같은 개념의 두 번째 자료는 새 파일이 아니라 보충이다."""
        _write_existing(repo, "stt", title="음성 인식", aliases=("STT",), ups=("2026-01-01-first",))
        content = _concept_md(
            stem="stt", title="음성 인식", aliases=("STT", "speech to text"),
            ups=("2026-01-01-first", REFERENCE_STEM),
        )
        results = _verify(repo, [{"filename_stem": "stt", "mode": "supplement",
                                  "names": ["STT"], "content": content}])
        assert results[0]["mode"] == "supplement"
        assert results[0]["stem"] == "stt"

    def test_diff_shows_removed_lines(self, repo):
        """보충은 덧붙이기가 아니라 다시 쓰기 — 무엇이 사라지는지가 승인 판단의 핵심이다."""
        _write_existing(repo, "stt", aliases=("STT",), body_extra="\n지워질 문장.\n")
        content = _concept_md(stem="stt", aliases=("STT",))
        results = _verify(repo, [{"filename_stem": "stt", "mode": "supplement",
                                  "names": [], "content": content}])
        assert "-지워질 문장." in results[0]["diff"]

    def test_matched_by_is_reported(self, repo):
        """화면이 '무엇 때문에 같다고 봤는지' 를 보여줄 수 있어야 한다.

        stem 이 맞으면 stem 으로 걸린다 — alias 가 값을 하는 곳은 stem 이 다른
        경우이고, 그건 신규 거부 경로에서 확인한다.
        """
        _write_existing(repo, "stt", aliases=("음성인식",))
        results = _verify(repo, [{"filename_stem": "stt", "mode": "supplement",
                                  "names": ["음성 인식"], "content": _concept_md(
                                      stem="stt", aliases=("음성인식",))}])
        assert results[0]["matched_by"] == "stt"

    def test_losing_existing_alias_is_rejected(self, repo):
        """alias 를 잃으면 다음 자료에서 같은 개념이 또 갈라진다."""
        _write_existing(repo, "stt", aliases=("STT", "speech to text"))
        content = _concept_md(stem="stt", aliases=("STT",))  # speech to text 유실
        with pytest.raises(GateError) as exc:
            _verify(repo, [{"filename_stem": "stt", "mode": "supplement",
                            "names": [], "content": content}])
        assert exc.value.code == "ALIASES_LOST"

    def test_losing_existing_source_is_rejected(self, repo):
        """기존 `up:` 을 지우면 그 자료가 이 개념에 기여한 사실이 사라진다."""
        _write_existing(repo, "stt", aliases=("STT",), ups=("2026-01-01-first",))
        content = _concept_md(stem="stt", aliases=("STT",), ups=(REFERENCE_STEM,))
        with pytest.raises(GateError) as exc:
            _verify(repo, [{"filename_stem": "stt", "mode": "supplement",
                            "names": [], "content": content}])
        assert exc.value.code == "SOURCES_LOST"

    def test_supplement_of_missing_concept_rejected(self, repo):
        with pytest.raises(GateError) as exc:
            _verify(repo, [{"filename_stem": "ghost", "mode": "supplement",
                            "names": [], "content": _concept_md(stem="ghost")}])
        assert exc.value.code == "CONCEPT_NOT_FOUND"


class TestNoteRules:
    def test_missing_aliases_rejected(self, repo):
        """`aliases` 가 비면 다음 자료에서 개념이 갈라진다 — L2 필수 필드."""
        content = _concept_md(stem="x-y").replace("aliases:\n  - 샘플\n  - sample\n", "")
        with pytest.raises(GateError) as exc:
            _verify(repo, [{"filename_stem": "x-y", "mode": "create", "names": [],
                            "content": content}])
        assert exc.value.code == "MISSING_NOTE_FIELD"

    def test_lineage_to_this_source_is_required(self, repo):
        """계보는 같은 발행 묶음 안에서 만들어진다 (DEC-010 D4)."""
        content = _concept_md(stem="x-y", ups=("2026-01-01-other",))
        with pytest.raises(GateError) as exc:
            _verify(repo, [{"filename_stem": "x-y", "mode": "create", "names": [],
                            "content": content}])
        assert exc.value.code == "MISSING_LINEAGE"

    def test_lineage_not_required_when_no_reference(self, repo):
        """reference 를 끈 경우에는 걸 상류가 없다."""
        content = _concept_md(stem="x-y", ups=("2026-01-01-other",))
        results = _verify(
            repo,
            [{"filename_stem": "x-y", "mode": "create", "names": [], "content": content}],
            reference_stem=None,
        )
        assert results[0]["stem"] == "x-y"

    def test_up_must_be_in_body(self, repo):
        content = _concept_md(stem="x-y").replace(f"- [[{REFERENCE_STEM}]] — 출처", "")
        with pytest.raises(GateError) as exc:
            _verify(repo, [{"filename_stem": "x-y", "mode": "create", "names": [],
                            "content": content}])
        assert exc.value.code == "UP_NOT_IN_BODY"

    def test_dated_stem_rejected(self, repo):
        with pytest.raises(GateError) as exc:
            _verify(repo, [{"filename_stem": "2026-07-28-x", "mode": "create", "names": [],
                            "content": _concept_md(stem="2026-07-28-x")}])
        assert exc.value.code == "INVALID_NOTE_STEM"

    @pytest.mark.parametrize(
        "bad",
        [
            {"filename_stem": "a/b", "mode": "create", "content": "x"},
            {"filename_stem": "ab", "mode": "bogus", "content": "x"},
            {"filename_stem": "ab", "mode": "create", "content": ""},
            "not a dict",
        ],
    )
    def test_malformed_entry_rejected(self, repo, bad):
        with pytest.raises(GateError):
            _verify(repo, [bad])


class TestApprovalGuard:
    """승인 시점에 사람이 바꿀 수 있는 것은 **제외 토글뿐**이다."""

    @staticmethod
    def _proposed():
        return {
            "concepts": [
                {"stem": "a-b", "mode": "create", "content": "AAA", "excluded": False},
                {"stem": "c-d", "mode": "supplement", "content": "BBB", "excluded": False},
            ]
        }

    def test_exclusion_is_applied(self):
        from service.pipeline.stages.concept import apply_exclusions

        approved = {
            "concepts": [
                {"stem": "a-b", "mode": "create", "content": "AAA", "excluded": True},
                {"stem": "c-d", "mode": "supplement", "content": "BBB", "excluded": False},
            ]
        }
        merged = apply_exclusions(approved, self._proposed())
        assert [c["excluded"] for c in merged["concepts"]] == [True, False]

    def test_content_swap_is_rejected(self):
        """검증을 통과한 내용과 발행되는 내용이 달라지면 게이트가 무의미해진다."""
        from service.pipeline.stages.concept import apply_exclusions

        approved = {
            "concepts": [
                {"stem": "a-b", "mode": "create", "content": "바꿔치기", "excluded": False},
                {"stem": "c-d", "mode": "supplement", "content": "BBB", "excluded": False},
            ]
        }
        with pytest.raises(GateError) as exc:
            apply_exclusions(approved, self._proposed())
        assert exc.value.code == "INVALID_CONCEPT_APPROVAL"

    def test_unknown_stem_is_rejected(self):
        from service.pipeline.stages.concept import apply_exclusions

        approved = {
            "concepts": [
                {"stem": "몰래끼움", "mode": "create", "content": "AAA", "excluded": False},
                {"stem": "c-d", "mode": "supplement", "content": "BBB", "excluded": False},
            ]
        }
        with pytest.raises(GateError):
            apply_exclusions(approved, self._proposed())

    def test_excluding_everything_is_rejected(self):
        """전부 제외는 목적지에서 개념을 끄는 것과 같은 결정이다 — 조용히 통과시키지 않는다."""
        from service.pipeline.stages.concept import apply_exclusions

        approved = {
            "concepts": [
                {"stem": "a-b", "mode": "create", "content": "AAA", "excluded": True},
                {"stem": "c-d", "mode": "supplement", "content": "BBB", "excluded": True},
            ]
        }
        with pytest.raises(GateError) as exc:
            apply_exclusions(approved, self._proposed())
        assert exc.value.code == "ALL_CONCEPTS_EXCLUDED"


class TestNeighbors:
    """이웃은 **양방향**이다 (KDEV-WORK-020 P1).

    나가는 링크만 보면 「A 가 B 를 딛는다」에서 B 로부터 A 를 못 찾는다. 개념은
    나중에 만들어진 쪽이 먼저 것을 가리키므로, 상류만 따라가면 최근에 자란 가지가
    통째로 안 보인다.
    """

    def test_outgoing_and_incoming(self, repo):
        _write_existing(repo, "inheritance", aliases=("상속",))
        _write_existing(
            repo, "polymorphism", aliases=("다형성",),
            body_extra="[[inheritance]] 위에서 자란다.",
        )
        index = build_index(repo)

        assert "polymorphism" in index.neighbors("inheritance")  # 들어오는 링크
        assert "inheritance" in index.neighbors("polymorphism")  # 나가는 링크

    def test_alias_link_resolves_to_stem(self, repo):
        _write_existing(repo, "stt", aliases=("STT",))
        _write_existing(repo, "asr", aliases=("ASR",), body_extra="[[STT]] 와 같다.")
        assert index_neighbors(repo, "asr") == {"stt"}

    def test_dead_link_is_not_a_neighbor(self, repo):
        """프롬프트에 없는 개념을 실을 수 없다."""
        _write_existing(repo, "asr", body_extra="[[없는-개념]] 을 가리킨다.")
        assert index_neighbors(repo, "asr") == set()


def index_neighbors(repo: Path, stem: str) -> set:
    return build_index(repo).neighbors(stem)


class TestSeeds:
    """seed 는 사전이 찾는다 — 사실 판단이라 AI 에 맡기지 않는다."""

    def test_alias_in_text_becomes_a_seed(self, repo):
        _write_existing(repo, "servlet", title="서블릿", aliases=("서블릿",))
        assert build_index(repo).seeds("오늘 서블릿 필터를 봤다") == {"servlet"}

    def test_spacing_does_not_matter(self, repo):
        """「추상 클래스」와 「추상클래스」는 같은 것을 가리킨다."""
        _write_existing(repo, "abstract-class", aliases=("추상 클래스",))
        assert build_index(repo).seeds("추상클래스를 배웠다") == {"abstract-class"}

    def test_one_character_alias_is_skipped(self, repo):
        """`락`·`빈`·`큐` 는 아무 글에나 걸리고, 그 seed 가 이웃 20건을 끌고 온다."""
        _write_existing(repo, "queue", aliases=("큐",))
        assert build_index(repo).seeds("큐레이션 도구를 만들었다") == set()

    def test_unrelated_text_has_no_seed(self, repo):
        _write_existing(repo, "servlet", aliases=("서블릿",))
        assert build_index(repo).seeds("점심으로 국수를 먹었다") == set()


class TestNarrowing:
    """의심스러우면 **안 자른다** (KDEV-DEC-023 D3·D4)."""

    def _many(self, repo, n: int) -> None:
        for i in range(n):
            _write_existing(repo, f"c{i:03d}", title=f"개념{i:03d}", aliases=(f"별칭{i:03d}",))

    def test_seed_itself_is_always_included(self, repo):
        _write_existing(repo, "servlet", aliases=("서블릿",))
        self._many(repo, 20)
        payload, meta = build_index(repo).narrowed_payload("서블릿을 봤다")
        assert meta["mode"] == "narrowed"
        assert "servlet" in {e["stem"] for e in payload}

    def test_no_seed_falls_back_to_everything(self, repo):
        """새 영역인지 사전이 놓친 것인지 **구분할 수 없다.**"""
        self._many(repo, 20)
        payload, meta = build_index(repo).narrowed_payload("아무 관련 없는 문장")
        assert meta["mode"] == "all" and meta["reason"] == "no_seed"
        assert len(payload) == 20

    def test_over_ceiling_falls_back_to_everything(self, repo):
        """seed 가 많은 날은 자르는 값이 없다 — 목록을 두 벌 만드는 비용만 남는다."""
        self._many(repo, 10)
        text = " ".join(f"별칭{i:03d}" for i in range(9))  # 90% 가 seed
        payload, meta = build_index(repo).narrowed_payload(text)
        assert meta["mode"] == "all" and meta["reason"] == "over_ceiling"
        assert len(payload) == 10

    def test_reason_is_reported(self, repo):
        """좁히기는 조용히 실패한다 — 판단 근거가 없으면 알 방법이 없다."""
        self._many(repo, 20)
        _, meta = build_index(repo).narrowed_payload("아무 관련 없는 문장")
        assert set(meta) == {"mode", "reason", "seeds", "picked", "total"}
        assert meta["total"] == 20
