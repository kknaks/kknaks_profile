"""구분자 레코드 파서 (KDEV-WORK-021 / KDEV-SPEC-008 §4).

여기서 지키는 것은 하나다 — **본문이 한 글자도 안 변한다.** 종전 JSON 계약은 markdown
전문을 문자열 값에 넣게 해서, 본문의 따옴표·줄바꿈·백슬래시를 수천 자에 걸쳐 하나도
안 틀리고 이스케이프해야 통과했다. 그 이스케이프가 실제로 어긋나 게이트가 막혔다.

관용의 **경계**도 여기서 고정한다. 코드펜스·머리말·꼬리말은 받고, 마커 없음·필수 키
없음·본문 빔은 안 받는다. 관용이 한 칸 넘어가면 형식이 깨진 노트가 승인 화면까지 올라간다.
"""

from __future__ import annotations

import pytest

from core.models import ItemPreparation, QueueItem
from service.pipeline.gates import GateError, GenerationInput
from service.pipeline.stages.common import (
    context_payload,
    parse_note_output,
    parse_records,
)
from service.pipeline.stages.concept import CONCEPT_KEYS
from service.pipeline.stages.derived import DERIVED_KEYS, record_fields

NOTE_KEYS = frozenset({"filename_stem"})

#: JSON 계약이었다면 전부 이스케이프해야 했던 것들. 여기서는 그대로 둔다.
NASTY_BODY = '''---
type: reference
title: "따옴표가 든 제목"
---

본문에 "쌍따옴표" 와 \\백슬래시\\ 와 탭\t이 있다.

```python
print("hello\\n")   # 코드펜스 안의 따옴표
```

| 표 | 값 |
|---|---|
| a | b |

줄바꿈이 여러 개 있어도 그대로다.'''


class TestBodyIsUntouched:
    """이 파일의 존재 이유."""

    def test_body_survives_verbatim(self):
        stem, body = parse_note_output(
            f"filename_stem: 2026-08-13-x-y\n---8<---\n{NASTY_BODY}\n---8<--- end"
        )
        assert stem == "2026-08-13-x-y"
        assert body == NASTY_BODY

    def test_frontmatter_starts_at_first_line(self):
        """앞 빈 줄이 남으면 `frontmatter.loads` 가 frontmatter 를 못 본다."""
        _, body = parse_note_output(
            "filename_stem: 2026-08-13-x-y\n---8<---\n\n\n---\ntype: reference\n---\n본문\n"
        )
        assert body.startswith("---\ntype: reference")

    def test_bare_marker_inside_body_is_text(self):
        """본문 안의 역할 없는 마커는 **글자**다.

        구조로 읽으면 노트가 조용히 잘린다 — 잘리는 쪽이 더 나쁘다.
        """
        _, body = parse_note_output(
            "filename_stem: 2026-08-13-x-y\n---8<---\n앞\n---8<---\n뒤"
        )
        assert body == "앞\n---8<---\n뒤"


class TestTolerance:
    """종전 `extract_json_object` 가 갖고 있던 것과 **같은 급**이어야 한다."""

    def test_code_fence_stripped(self):
        raw = "```markdown\nfilename_stem: 2026-08-13-x-y\n---8<---\n본문\n```"
        assert parse_note_output(raw)[1] == "본문"

    def test_preamble_dropped(self):
        raw = (
            "알겠습니다. 아래에 자료 노트를 작성했습니다.\n"
            "참고: 개념은 다음 단계에서 뽑겠습니다.\n\n"
            "filename_stem: 2026-08-13-x-y\n---8<---\n본문"
        )
        assert parse_note_output(raw) == ("2026-08-13-x-y", "본문")

    def test_epilogue_dropped(self):
        raw = (
            "filename_stem: 2026-08-13-x-y\n---8<---\n본문\n"
            "---8<--- end\n\n이상입니다. 검토 부탁드립니다."
        )
        assert parse_note_output(raw)[1] == "본문"

    def test_unknown_header_key_ignored(self):
        raw = "note_type: reference\nfilename_stem: 2026-08-13-x-y\n---8<---\n본문"
        assert parse_note_output(raw)[0] == "2026-08-13-x-y"

    def test_explicit_content_role_accepted(self):
        raw = "filename_stem: 2026-08-13-x-y\n---8<--- content\n본문"
        assert parse_note_output(raw)[1] == "본문"


class TestRefusal:
    """**가드를 깨뜨려 본다** — 위반이 실제로 실패하는지."""

    def test_nothing_structural_rejected(self):
        """옛 JSON 계약이 그대로 오면 여기 걸린다."""
        with pytest.raises(GateError) as exc:
            parse_records('{"filename_stem": "a", "content": "x"}', keys=NOTE_KEYS)
        assert exc.value.code == "INVALID_NOTE_OUTPUT"
        # 사람이 화면에서 원인을 보려면 **무엇이 왔는지**가 메시지에 있어야 한다.
        assert "filename_stem" in exc.value.message

    def test_header_without_marker_rejected(self):
        """헤더만 오고 본문 구분자가 없는 경우 — 어느 쪽이 빠졌는지 메시지가 말한다."""
        with pytest.raises(GateError) as exc:
            parse_records("filename_stem: a\n본문이 그냥 이어진다", keys=NOTE_KEYS)
        assert exc.value.code == "INVALID_NOTE_OUTPUT"
        assert "본문이 비었다" in exc.value.message

    def test_empty_body_rejected(self):
        with pytest.raises(GateError) as exc:
            parse_records("filename_stem: a\n---8<---\n\n  \n", keys=NOTE_KEYS)
        assert exc.value.code == "INVALID_NOTE_OUTPUT"

    def test_two_records_rejected_for_single_note_stage(self):
        raw = (
            "---8<--- note\nfilename_stem: a-b\n---8<---\n하나\n"
            "---8<--- note\nfilename_stem: c-d\n---8<---\n둘"
        )
        with pytest.raises(GateError):
            parse_note_output(raw)

    def test_restored_output_passes(self):
        """깨뜨린 것을 되돌리면 통과한다 — 가드가 늘 실패하는 게 아니라는 확인."""
        assert parse_note_output("filename_stem: a-b\n---8<---\n본문")[1] == "본문"


class TestConceptRecords:
    def test_multiple_records(self):
        raw = (
            "---8<--- note\n"
            "filename_stem: mcp\nmode: create\nnames: MCP, Model Context Protocol\n"
            "---8<---\n첫 노트\n"
            "---8<--- note\n"
            "filename_stem: json-rpc\nmode: supplement\nnames: JSON-RPC\n"
            "---8<---\n둘째 노트\n"
            "---8<--- end"
        )
        records = parse_records(raw, keys=CONCEPT_KEYS)
        assert [r.one("filename_stem") for r in records] == ["mcp", "json-rpc"]
        assert [r.one("mode") for r in records] == ["create", "supplement"]
        assert records[0].many("names", split=",") == ["MCP", "Model Context Protocol"]
        assert records[1].body == "둘째 노트"

    def test_none_marker_is_empty_list(self):
        """개념을 억지로 만들지 않는다 — 0건이 표현될 수 있어야 한다."""
        assert parse_records("---8<--- none", keys=CONCEPT_KEYS) == []

    def test_empty_output_is_not_zero_concepts(self):
        """빈 출력을 0건으로 읽으면 **실패와 「없음」이 구분되지 않는다.**"""
        with pytest.raises(GateError):
            parse_records("", keys=CONCEPT_KEYS)


class TestDerivedRecord:
    RAW = (
        "title_ko: 제목\ntitle_en: Title\n"
        "summary_ko: 요약\nsummary_en: Summary\n"
        "tags: #fastapi, #mcp\n"
        "concept: 첫 문장, 쉼표가 들어 있다\n"
        "concept: 둘째 문장\n"
        "kind: study\n"
        "---8<---\n## 개요\n\n내용\n---8<--- end"
    )

    def test_fields_mapped(self):
        data = record_fields(parse_records(self.RAW, keys=DERIVED_KEYS)[0])
        assert data["title"] == {"ko": "제목", "en": "Title"}
        assert data["summary"] == {"ko": "요약", "en": "Summary"}
        assert data["tags"] == ["#fastapi", "#mcp"]
        assert data["kind"] == "study"
        assert data["body"] == "## 개요\n\n내용"

    def test_concept_sentences_are_not_split_on_comma(self):
        """문장 안에 쉼표가 들어간다 — 나누면 문장이 조각난다."""
        data = record_fields(parse_records(self.RAW, keys=DERIVED_KEYS)[0])
        assert data["concept"] == ["첫 문장, 쉼표가 들어 있다", "둘째 문장"]


class TestResumedPayload:
    """이어받으면 원문을 다시 보내지 않는다 (KDEV-DEC-024 D5).

    SPEC-009 S-1 5항이 「이어받으면 원문·지침을 다시 보내지 않아도 된다」고 적어
    뒀는데, 실행기가 프롬프트 뒤에 payload 전문을 붙이기 때문에 **코드는 매번 4만
    자를 다시 보내고 있었다.** 문서와 코드가 갈려 있던 자리다.
    """

    @staticmethod
    def _request(session_ref: str | None) -> GenerationInput:
        # **실물 타입을 쓴다** — 가짜 dict 를 넘기면 직렬화 결함이 안 잡힌다.
        preparation = ItemPreparation(
            payload={
                "summary": "요약본",
                "source": {"title": "제목", "content": "원" * 50_000},
            }
        )
        return GenerationInput(
            item=QueueItem(source_url="https://x.test/a", source_kind="youtube", note=None),
            gate=None,
            preparation=preparation,
            previous_payload=None,
            feedback=None,
            session_ref=session_ref,
        )

    def test_cold_start_carries_the_source(self):
        payload = context_payload(self._request(None))
        assert len(payload["source_excerpt"]) == 40_000
        assert "resumed_session" not in payload

    def test_resumed_drops_the_source_but_keeps_the_summary(self):
        payload = context_payload(self._request("sess-1"))
        assert "source_excerpt" not in payload
        assert payload["resumed_session"] is True
        # 요약은 짧고, 세션이 압축됐을 때의 마지막 방어선이다.
        assert payload["summary"] == "요약본"
        assert payload["source_title"] == "제목"
