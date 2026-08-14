"""노트를 만드는 게이트 스테이지의 공통부 (KDEV-WORK-015 / KDEV-SPEC-010).

**AI 가 md 전문을 낸다.** 종전 캡처 경로는 `AI → JSON → render.py → md` 였는데,
그러면 `render.py` 의 하드코딩된 섹션 구성이 `templates/knowledge/` 와 나란히
**형식의 SoT 두 번째**가 된다. 규칙을 고쳐도 렌더러가 안 따라오면 조용히 어긋난다.

그래서 여기서는 에이전트가 레포의 템플릿을 읽고 **완성된 markdown 을 직접** 낸다.
`render.py` 는 롤백 경로(`KnowledgeCaptureRunner`)에만 남는다.

AI 가 내는 것은 `filename_stem` 과 본문뿐이다. **디렉토리는 시스템이 층·목적지에서
조립한다**(SPEC-010) — 경로 결정을 AI 에 맡기면 allowlist 밖으로 쓰는 계획이 나온다.

**출력은 JSON 이 아니다** (KDEV-WORK-021 / SPEC-008 §4). 종전 계약은 markdown 전문을
JSON 문자열 값에 넣게 돼 있었는데, 그러면 본문의 따옴표·줄바꿈·백슬래시를 수천 자에
걸쳐 하나도 안 틀리고 이스케이프해야 통과한다. **확률이 본문 길이에 비례**한다.

실제로 막혔다 — 항목 #3880 의 `source_note` 1차가
`INVALID_NOTE_OUTPUT: JSON 파싱 실패: Expecting ',' delimiter: line 3 column 840`
으로 죽었고(95초), 재시도(309초)와 사람의 개입이 한 번씩 더 들었다. 컬럼 840 은
본문 한가운데다 — 모델이 못 쓴 것이 아니라 **이스케이프가 어긋났을 뿐**이다.

그래서 이스케이프가 필요한 자리를 없앤다. **짧은 단일행 헤더 + 손대지 않은 본문**이다.

    filename_stem: 2026-08-13-mcp-spec
    ---8<---
    <markdown 전문 그대로>
    ---8<--- end
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import frontmatter

from ..gates import GateError, GenerationInput

#: `rules/knowledge-note-pipeline.md` 의 파일명 규약.
REFERENCE_STEM_RE = re.compile(r"\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*")
#: concept 는 **날짜를 붙이지 않는다** — 개념은 특정 시점에 묶이지 않는다.
#: 숫자 자체는 허용한다(`gpt-4`, `http2`). 앞머리의 날짜 형태만 막는다.
CONCEPT_STEM_RE = re.compile(r"(?!\d{4}-\d{2}-\d{2})[a-z0-9]+(?:-[a-z0-9]+)*")

READ_THE_RULES = """작성 전에 레포의 규칙과 양식을 **반드시 읽어라.** 이 프롬프트에 복사돼 있지 않다.

1. `rules/knowledge-note-pipeline.md` — 4층 모델, SoT 위임, 개념 성장, `up:` 방향, 층별 필수 필드
2. `templates/knowledge/{template}` — 만들 노트의 양식 (섹션 구성과 각 섹션에 넣을 것)

읽지 않고 쓰면 형식이 어긋나 발행 전 검증에서 거부된다."""

#: 구분자. 뒤에 역할(`note`·`content`·`end`·`none`)이 붙을 수 있고, 없으면 `content` 다.
MARKER = "---8<---"

MARKER_RE = re.compile(rf"^\s*{re.escape(MARKER)}(?:\s+(note|content|end|none))?\s*$")
#: 헤더 한 줄. 값은 **전부 짧은 단일행**이라 이스케이프가 필요한 자리가 없다.
HEADER_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s?(.*)$")

_CONTRACT_HEAD = """아래 형식 그대로 출력한다. **JSON 이 아니다** — 본문을 따옴표로 감싸거나
이스케이프하지 않는다. 코드펜스나 설명 문장을 붙이지 않는다."""

_CONTRACT_TAIL = """`---8<---` 아랫줄부터는 **손대지 않은 markdown** 이다. 따옴표·줄바꿈·백슬래시를
있는 그대로 쓴다. 본문은 완성된 노트 그대로이고 요약이나 발췌가 아니다.
헤더 값은 전부 **한 줄**이다 — 여러 줄이 필요한 것은 본문뿐이다.
경로는 시스템이 조립하므로 디렉토리를 지어내지 않는다."""

NOTE_SHAPE = """filename_stem: <파일명 stem. 확장자·디렉토리 없이>
---8<---
<frontmatter 를 포함한 markdown 전문>"""

#: 노트 하나를 내는 스테이지 (`source_note`·`post`).
OUTPUT_CONTRACT = f"""{_CONTRACT_HEAD}

{NOTE_SHAPE}
{MARKER} end

{_CONTRACT_TAIL}"""

#: 노트 하나를 내되 헤더 키가 여럿인 스테이지 (`derived`).
OUTPUT_CONTRACT_ONE = f"""{_CONTRACT_HEAD}

{{shape}}
{MARKER} end

{_CONTRACT_TAIL}"""

#: 노트를 0..N 건 내는 스테이지 (`concept`).
OUTPUT_CONTRACT_LIST = f"""{_CONTRACT_HEAD}

{{shape}}
{MARKER} end

레코드는 `{MARKER} note` 로 시작하고 **필요한 만큼 반복한다.** 마지막에 `{MARKER} end` 를 둔다.
낼 것이 하나도 없으면 레코드 없이 `{MARKER} none` 한 줄만 낸다.

{_CONTRACT_TAIL}"""


@dataclass(frozen=True)
class Record:
    """구분자 레코드 하나 — 짧은 헤더 값들과 손대지 않은 본문."""

    header: dict[str, list[str]]
    body: str

    def one(self, key: str) -> str:
        """헤더 값 하나. 없으면 빈 문자열 — 판정은 호출부가 한다."""
        values = self.header.get(key) or []
        return values[0].strip() if values else ""

    def many(self, key: str, *, split: str | None = None) -> list[str]:
        """반복해서 쓴 헤더 줄들.

        `split` 을 주면 한 줄 안에서 또 나눈다 — `names`·`tags` 처럼 쉼표로 늘어놓는
        값이다. **문장 목록(`concept`)에는 쓰지 않는다** — 문장 안에 쉼표가 들어간다.
        """
        out: list[str] = []
        for raw in self.header.get(key) or []:
            parts = raw.split(split) if split else [raw]
            out.extend(part.strip() for part in parts)
        return [value for value in out if value]


def _strip_fence(raw: str) -> str:
    """출력 전체를 감싼 코드펜스를 벗긴다.

    프롬프트가 "코드펜스를 붙이지 않는다" 고 적어 둬도 모델이 붙이는 일이 실제로
    있었다(종전 `extract_json_object` 가 같은 것을 벗겼다). 형식이 바뀌었다고 이
    관용이 필요 없어지지는 않는다.
    """
    text = (raw or "").strip()
    if not text.startswith("```"):
        return text
    text = text.split("\n", 1)[1] if "\n" in text else ""
    stripped = text.rstrip()
    if stripped.endswith("```"):
        text = stripped[:-3]
    return text.strip()


def parse_records(raw: str, *, keys: frozenset[str]) -> list[Record]:
    """모델 출력에서 구분자 레코드를 꺼낸다 (SPEC-008 §4).

    **`keys` 를 받는 이유**는 머리말을 어디서 자를지 판단하기 위해서다. 「이 줄이
    헤더인가 산문인가」는 아는 키가 나왔는지로만 갈린다 — 없으면 `참고:` 로 시작하는
    설명 문장이 헤더로 읽힌다.

    관용은 종전 JSON 파서가 갖고 있던 것과 **같은 급**이다.

        ① 출력 전체를 감싼 코드펜스를 벗긴다
        ② 첫 마커나 아는 헤더 키 앞의 산문을 버린다
        ③ `---8<--- end` 뒤의 산문을 버린다
        ④ 본문의 앞뒤 빈 줄을 다듬는다 — frontmatter 는 첫 줄에서 시작해야 한다

    **관용은 여기까지다.** 마커가 없거나 본문이 비면 통과시키지 않는다 — 조용히
    넘기면 형식이 깨진 노트가 사람의 승인 화면까지 올라간다.

    본문 안의 `---8<---` (역할 없는 마커)는 **본문 글자로 읽는다.** 경계를 여는 일은
    이미 끝났고, 구조로 읽으면 노트가 조용히 잘린다 — 잘리는 쪽이 더 나쁘다.
    """
    text = _strip_fence(raw)
    records: list[Record] = []
    header: dict[str, list[str]] = {}
    body: list[str] | None = None
    declared_none = False

    def flush() -> None:
        nonlocal header, body
        if body is None and not header:
            return
        records.append(
            Record(header=header, body="\n".join(body or []).strip())
        )
        header, body = {}, None

    for line in text.splitlines():
        marker = MARKER_RE.match(line)
        if marker:
            role = marker.group(1) or "content"
            if role == "end":
                break
            if role == "none":
                flush()
                declared_none = True
                continue
            if role == "note":
                flush()
                continue
            if body is None:  # content — 경계를 연다
                body = []
                continue
            # 이미 본문 안이다. 구조가 아니라 글자다.
        if body is not None:
            body.append(line)
            continue
        field = HEADER_RE.match(line)
        if field and field.group(1) in keys:
            header.setdefault(field.group(1), []).append(field.group(2))
        # 그 밖의 줄은 버린다 — 머리말·설명 문장·모르는 키.

    flush()

    if not records:
        if declared_none:
            return []
        raise GateError(
            "INVALID_NOTE_OUTPUT",
            f"구분자({MARKER})를 찾지 못했다 — 받은 앞부분: {text[:200]!r}",
        )
    for record in records:
        if not record.body:
            raise GateError(
                "INVALID_NOTE_OUTPUT",
                f"본문이 비었다 — 헤더만 왔다: {sorted(record.header)}",
            )
    return records


def extract_json_object(raw: str) -> str:
    """모델 출력에서 JSON 본문만 꺼낸다 (KDEV-WORK-017 결함 ⑥).

    **노트 스테이지는 더는 이것을 쓰지 않는다** (KDEV-WORK-021). 남은 소비자는
    본문이 없는 `route` 와, 산출물이 넷으로 중첩돼 레코드 하나로 안 떨어지는
    잔디(`daily`)다. 잔디도 같은 이스케이프 위험을 갖고 있다 — SPEC-008 §7 OPEN.

    두 가지를 벗긴다.

        ① 코드펜스 — ```` ```json ... ``` ````
        ② **머리말** — JSON 앞에 붙는 산문 문단

    ②가 이번에 실제로 게이트를 막았다. 프롬프트가 "JSON 하나로 답한다" 고 적어
    두었는데도 모델이 앞에 설명 두 줄을 붙였고, `json.loads` 가 char 0 에서 죽어
    **재시도 3회를 태우고 게이트가 열리지 않았다.** 프롬프트를 조여도 이 관용성은
    있어야 한다 — 모델이 매번 지킨다는 보장에 기대면 같은 자리에서 또 멎는다.

    **첫 `{` 부터 괄호 균형이 맞는 곳까지**를 잘라낸다. 단순히 마지막 `}` 를 찾으면
    본문 뒤에 붙은 꼬리말 안의 `}` 에 걸리고, 첫 `}` 를 찾으면 중첩 객체에서 끊긴다.
    문자열 리터럴 안의 괄호와 이스케이프는 세지 않는다 — daily 본문에 `{` 가 들어
    있으면 그것을 구조로 오인한다.

    꺼낼 것이 없으면 원문을 그대로 돌려준다. 판단은 호출부의 `json.loads` 가 하고,
    그 에러 메시지가 스테이지별 코드로 올라간다.
    """
    cleaned = (raw or "").strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
    # `{` 로 시작해도 지름길로 빠지지 않는다 — 꼬리말이 붙어 있으면 그것도 잘라야
    # 하고, `json.loads` 는 뒤에 남은 산문을 `Extra data` 로 거부한다.
    start = cleaned.find("{")
    if start < 0:
        return cleaned

    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(cleaned)):
        ch = cleaned[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return cleaned[start : i + 1]
    return cleaned


#: 노트 하나짜리 스테이지의 헤더 키.
NOTE_KEYS = frozenset({"filename_stem"})


def check_stem(stem: str) -> str:
    """경로·확장자가 섞이지 않았는지. 섞이면 allowlist 밖으로 쓰는 계획이 만들어진다."""
    if not stem:
        raise GateError("INVALID_NOTE_OUTPUT", "filename_stem 이 없다")
    if "/" in stem or stem.endswith(".md"):
        raise GateError("INVALID_NOTE_OUTPUT", f"stem 에 경로나 확장자가 들어갔다: {stem}")
    return stem


def parse_note_output(raw: str) -> tuple[str, str]:
    """레코드 하나에서 `(stem, 본문)` 을 꺼낸다. 어긋나면 `GateError`.

    **레코드가 둘 이상이면 실패다.** 노트 하나를 만드는 스테이지이므로, 여럿이 왔다는
    것은 모델이 형식을 다르게 이해했다는 뜻이다 — 첫 건만 조용히 쓰면 나머지가 소리
    없이 버려진다.
    """
    records = parse_records(raw, keys=NOTE_KEYS)
    if len(records) != 1:
        raise GateError(
            "INVALID_NOTE_OUTPUT", f"노트 하나여야 하는데 {len(records)}건이 왔다"
        )
    record = records[0]
    return check_stem(record.one("filename_stem")), record.body


def check_note(
    stem: str,
    content: str,
    *,
    expected_type: str,
    stem_pattern: re.Pattern[str],
    required: tuple[str, ...],
) -> dict[str, Any]:
    """게이트 시점의 가벼운 검사 — 사람이 보기 전에 명백히 틀린 것을 거른다.

    전체 그래프 검증(L1~L6)은 발행 직전에 가상 그래프로 돈다(SPEC-010 S-3).
    여기서 그걸 다 하지 않는 이유는, 이 시점에는 형제 노트들이 아직 안 만들어져
    링크가 깨져 보이기 때문이다.
    """
    if not stem_pattern.fullmatch(stem):
        raise GateError("INVALID_NOTE_STEM", f"'{stem}' 은 파일명 규약에 맞지 않는다")
    try:
        post = frontmatter.loads(content)
    except Exception as exc:  # noqa: BLE001
        raise GateError("INVALID_NOTE_OUTPUT", f"frontmatter 파싱 실패: {exc}") from exc

    meta = post.metadata
    declared = meta.get("type")
    if declared is None:
        # **없는 것도 막는다.** 종전에는 *틀린* type 만 막았는데, 그래프 빌더는 노드
        # 종류를 이 필드에서 읽으므로 없으면 발행 직전에 `UNKNOWN_TYPE` 으로 거부된다.
        # 즉 게이트를 넷 다 승인한 **뒤에야** 막힌다 — item #3881 이 그랬다.
        # 여기서 막으면 그 게이트 하나가 실패하고 재시도가 그 자리에서 고친다.
        raise GateError("MISSING_NOTE_FIELD", f"필수 필드 누락: type ({expected_type})")
    if declared != expected_type:
        raise GateError(
            "INVALID_NOTE_OUTPUT", f"type 이 {declared} 다 — {expected_type} 이어야 한다"
        )
    missing = [f for f in required if not meta.get(f)]
    if missing:
        raise GateError("MISSING_NOTE_FIELD", f"필수 필드 누락: {', '.join(missing)}")

    declared_id = str(meta.get("id") or "").strip()
    if declared_id and declared_id != stem:
        # stem 과 id 가 다르면 로더가 실패한다(지식 노트는 id = 파일명 stem).
        raise GateError("INVALID_NOTE_OUTPUT", f"id({declared_id}) 와 stem({stem}) 이 다르다")
    return meta


def up_targets(meta: dict[str, Any]) -> list[str]:
    raw = meta.get("up") or []
    if isinstance(raw, str):
        return [raw]
    return [str(v) for v in raw if str(v).strip()]


def body_links(content: str) -> set[str]:
    """본문 `[[...]]` 대상. `|` 별칭 표기를 걷어낸다."""
    return {
        match.split("|")[0].strip()
        for match in re.findall(r"\[\[([^\]]+)\]\]", content)
    }


def require_up_in_body(meta: dict[str, Any], content: str) -> None:
    """`up:` 은 본문 링크의 부분집합이어야 한다 (L3 · KDEV-DEC-004).

    본문이 엣지의 단일 소스이고 `up:` 은 그중 계보인 것을 마킹하는 오버레이다.
    여기서 잡지 않으면 발행 직전 검증에서 통째로 거부돼 다시 만들어야 한다.
    """
    links = body_links(content)
    missing = [stem for stem in up_targets(meta) if stem not in links]
    if missing:
        raise GateError(
            "UP_NOT_IN_BODY",
            f"up: 에 있는 {', '.join(missing)} 이 본문 [[]] 에 없다",
        )


def context_payload(request: GenerationInput) -> dict[str, Any]:
    """모든 노트 스테이지가 공통으로 넘기는 입력.

    **세션을 이어받으면 원문을 다시 보내지 않는다** (KDEV-DEC-024 D5). SPEC-009 S-1
    5항이 「이어받으면 원문·지침을 다시 보내지 않아도 된다」고 적어 뒀는데, 실행기가
    프롬프트 뒤에 payload 전문을 붙이기 때문에 **코드는 매번 4만 자를 다시 보내고
    있었다.** 문서와 코드가 갈려 있던 자리다.

    **요약은 항상 보낸다.** 짧고, 뒤 스테이지의 판단 축이며, 세션이 압축돼 앞부분을
    잃었을 때의 마지막 방어선이다.
    """
    preparation = (request.preparation.payload or {}) if request.preparation else {}
    payload: dict[str, Any] = {
        "source_url": request.item.source_url,
        "source_kind": request.item.source_kind,
        "note": request.item.note,
        "summary": preparation.get("summary"),
        "material_source": preparation.get("material_source"),
        "collected_at": preparation.get("source", {}).get("accessed_at")
        if isinstance(preparation.get("source"), dict)
        else None,
    }
    source = preparation.get("source")
    if isinstance(source, dict):
        payload["source_title"] = source.get("title")
        if request.session_ref:
            # 원문은 이 대화 위쪽에 이미 있다. 안 알려 주면 「자료를 안 줬다」고 읽는다.
            payload["resumed_session"] = True
        else:
            payload["source_excerpt"] = (source.get("content") or "")[:40_000] or None
    if request.previous_payload is not None:
        payload["previous_draft"] = request.previous_payload
    if request.feedback:
        payload["feedback"] = request.feedback
    if request.retry_error:
        # 사람 피드백과 **다른 키**다. 섞으면 사람이 하지 않은 말이 지적으로 남는다.
        payload["previous_error"] = request.retry_error
    return payload
