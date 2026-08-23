"""발행 계획 조립과 검증 (KDEV-WORK-015 P4 / KDEV-SPEC-010).

**하나라도 위반이면 발행 전체를 거부한다.** 부분 적용을 허용하면 reference 만 나가고
concept 는 빠진 상태가 되어, 링크가 깨진 채로 origin 에 올라간다. 그건 사람이 나중에
손으로 고쳐야 하는 상태다.

검증은 **파일을 쓰기 전에** 전부 끝난다. 커밋 후 부팅 검증으로 잡으면 이미 origin 에
나간 뒤라 늦다.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import frontmatter

# 섹션 이름은 **양식이 갖는다.** 게이트가 갱신안을 만들 때 보는 것과 같은 문자열이라야
# 하고, 두 곳에 적으면 한쪽만 고쳐지는 날 갱신안이 매번 발행 직전에 거부된다.
from service.content_format import CURRENT_MANAGED_SECTION

logger = logging.getLogger("kknaks-back.apply.plan")

#: 발행이 쓸 수 있는 디렉토리. **이 밖은 전부 거부한다** —
#: 경로 조립에 버그가 있어도 `app/` 이나 `.github/` 를 건드리지 못하게 한다.
#:
#: KDEV-WORK-019 이관으로 지식층이 `resources/` 한 접두로 모였다. 종전에는
#: `permanent/` 가 `permanent/concept/` 를 **삼키는** 구조라 "종합 노트가 concept
#: 디렉토리에 있다" 를 잡는 별도 분기가 필요했는데, 셋이 형제가 되면서 `LAYER_PREFIX`
#: 의 정확 일치만으로 충분해졌다 — 그 분기는 제거됐다.
ALLOWED_PREFIXES = (
    "resources/",
    "inbox/",
    "archive/",
    "persona/contents/",
    # 잔디 산출물 (KDEV-WORK-017 P3). 지식층이 아니라 그래프 밖이다.
    "persona/daily/",
    "persona/career/",
    "persona/posts/",
    # 영역 현황 (KDEV-DEC-022). **`## 진행 중` 섹션만** 갈아 끼운다 — 나머지는
    # 사람 소유다. `context/` 는 여전히 계보 밖이고 그래프 노드가 아니다(DEC-020 D4).
    "context/",
)

#: 층과 경로의 정합. 개념이 `reference/` 에 들어가면 로더가 다른 타입으로 읽는다.
LAYER_PREFIX = {
    # **폴더 이름은 층 이름이다** (KDEV-DEC-018 D1). `type` 이름과 다른 것은 의도로,
    # 폴더는 층을 가리키고 `type` 은 frontmatter 계약이라 축이 다르다.
    "reference": "resources/source/",
    "concept": "resources/concept/",
    "idea": "inbox/",
    "content": "persona/contents/",
    "daily": "persona/daily/",
    "career": "persona/career/",
    # 공개 글 — 자료 하나를 1:1 로 받아 압축한 것. 양식은 `templates/persona/post-*.md`.
    "post_article": "persona/posts/",
    "post_note": "persona/posts/",
    # `current` 는 영역마다 경로가 달라(`company`/`studio`) 접두만 고정한다.
    "current": "context/",
}

#: 그래프 노드가 아닌 층. 상류 참조가 없어 `up:` 검사와 그래프 검증에서 빠진다
#: (KDEV-SPEC-013 「그래프 검증 제외」).
OUTSIDE_GRAPH = ("daily", "career", "current", "post_article", "post_note")

#: career frontmatter 중 **사람만 정하는** 필드 (KDEV-SPEC-012).
#: 갱신안에 담기면 발행을 거부한다 — 무시하는 것이 아니라 애초에 담기지 않아야 한다.
PROTECTED_CAREER_FIELDS = (
    "bullets",
    "period",
    "is_current",
    "display_order",
    "title",
    "org",
    "summary",
    "location",
)

_TRAVERSAL = re.compile(r"(^/)|(\.\.)")


@dataclass
class FileAction:
    #: `create` 신규 · `replace` 기존 교체 · `upsert` **둘 다 정상** · `remove` 삭제
    #:
    #: `upsert` 가 필요한 이유는 daily·career 가 첫 회 생성과 이후 덮어쓰기가 둘 다
    #: 정상이기 때문이다(SPEC-013). `create`/`replace` 만으로는 매일 액션 종류가
    #: 갈리고, 그러면 "오늘은 create 인가 replace 인가" 를 발행부가 알아야 한다.
    #:
    #: `remove` 는 **입구를 비우는 데만** 쓴다(KDEV-DEC-021 D1). 발행이 파일을 지우는
    #: 유일한 경우이고, 지우는 것은 공부 노트가 큐로 옮겨 간 뒤 남은 `inbox/` 원본이다.
    #: `content` 는 비어 있다 — 지울 때 쓸 내용이 없다.
    action: str  # create | replace | upsert | remove
    path: str
    content: str
    note_type: str
    stem: str
    source_gate: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "path": self.path,
            "content": self.content,
            "note_type": self.note_type,
            "stem": self.stem,
            "source_gate": self.source_gate,
        }


@dataclass
class Violation:
    rule: str
    path: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return {"rule": self.rule, "path": self.path, "detail": self.detail}


@dataclass
class Plan:
    actions: list[FileAction] = field(default_factory=list)
    violations: list[Violation] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.violations

    def as_json(self) -> list[dict[str, Any]]:
        return [a.as_dict() for a in self.actions]


def _note_type(content: str) -> str:
    try:
        return str(frontmatter.loads(content).metadata.get("type") or "")
    except Exception:  # noqa: BLE001
        return ""


def render_daily(payload: dict[str, Any]) -> str:
    """daily 파일 전문 — **frontmatter 는 시스템이 조립한다.**

    다른 노트 스테이지는 AI 가 md 전문을 낸다(형식 SoT 를 둘로 만들지 않으려고). daily
    는 그럴 수 없다 — `type`·`date`·`auto` 는 시스템 것이고 `counts` 는 코드가 센 값이라
    AI 출력에 섞이면 안 된다(SPEC-012 §5). AI 가 내는 것은 `summary` 와 본문뿐이고,
    그 둘은 여기서 조립되는 값이 아니라 그대로 실린다 — 형식 SoT 가 둘이 되지 않는다.

    `date` 를 **점 표기**로 쓴다. 로더가 파일명(하이픈)과 대조하며, 어긋나면 파일 하나가
    거부되는 게 아니라 persona 로드 전체가 실패한다.
    """
    date = str(payload.get("date") or "")
    post = frontmatter.Post(
        str(payload.get("body") or ""),
        **{
            "type": "daily",
            "date": date.replace("-", "."),
            "auto": True,
            "counts": payload.get("counts") or {},
            "summary": payload.get("summary") or {"ko": [], "en": []},
        },
    )
    return frontmatter.dumps(post)


def _split_frontmatter(existing: str) -> tuple[str, bool]:
    """원문에서 frontmatter 블록을 **문자 그대로** 떼어 낸다. `(블록, 찾았나)`.

    블록은 여는 `---` 부터 닫는 `---` 까지를 포함한다. 파싱하지 않으므로 주석·키
    순서·따옴표·들여쓰기가 원문 그대로 남는다.
    """
    if not existing.startswith("---"):
        return "", False
    lines = existing.splitlines(keepends=True)
    if lines[0].strip() != "---":
        return "", False
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "".join(lines[: i + 1]), True
    # 닫는 구분자가 없다 — frontmatter 가 아니다.
    return "", False


def render_career(payload: dict[str, Any], existing: str) -> str:
    """career 파일 전문 — **기존 frontmatter 를 그대로 이고 본문만 바꾼다.**

    갱신안이 본문만 내는 이유가 여기 있다. career frontmatter 는 `bullets`·`period`
    처럼 사람이 정하는 값이 대부분이라, AI 가 전문을 내면 그것들을 다시 쓰게 된다.
    본문만 받아 얹으면 사람 전용 필드는 **건드릴 방법 자체가 없다.**

    **frontmatter 를 파싱하지 않는다** (KDEV-WORK-017 결함 ⑩). 종전에는
    `frontmatter.loads()` → `dumps()` 로 왕복했는데, 값은 보존되지만 **주석이
    사라지고 키가 알파벳순으로 재정렬된다.** 본문만 바뀌어야 할 발행이 42 insertions
    / 38 deletions 를 냈고 `# 이력서 PDF — 비면 PDF 미표시` 주석이 없어졌다.
    dry-run 이라 되돌렸지만 운영에서는 그것이 그대로 `origin/main` 에 커밋된다.

    "사람 전용 필드를 건드리지 않는다" 는 규율은 **값이 같으면 되는 것이 아니다** —
    사람이 적어 둔 주석과 순서도 그 사람의 것이다. 그래서 텍스트를 그대로 이어 붙인다.
    """
    body = str(payload.get("content") or "")
    block, found = _split_frontmatter(existing)
    if not found:
        # frontmatter 가 없는 career 는 정상이 아니다. 여기서 지어내지 않는다 —
        # `_career_violations` 가 필수 필드 부재로 잡아 발행을 막는다.
        return body if body.endswith("\n") else body + "\n"
    if not block.endswith("\n"):
        block += "\n"
    if not body.endswith("\n"):
        # 종전 구현은 파일을 개행 없이 끝냈다(`\ No newline at end of file`).
        body += "\n"
    return f"{block}\n{body}"


def replace_section(existing: str, header: str, body: str) -> str:
    """`header` 로 시작하는 섹션의 **본문만** 갈아 끼운다. 나머지는 문자 그대로 남는다.

    `render_career` 가 겪은 것을 반복하지 않는다 (KDEV-DEC-022 D3) — 종전에
    frontmatter 를 파싱해 왕복했더니 **값은 보존되지만 주석이 사라지고 키가
    재정렬**돼, 본문만 바뀌어야 할 발행이 42 insertions / 38 deletions 를 냈다.
    사람이 적어 둔 주석·빈 칸·순서도 그 사람의 것이다.

    헤더가 없으면 `ValueError` 다 — **조용히 멈추지 않는다.** 사람이 헤더 이름을
    바꾸면 갱신이 안 되는데, 그것을 모른 채 지나가면 문서가 다시 죽는다.
    """
    lines = existing.splitlines(keepends=True)
    start = None
    for i, line in enumerate(lines):
        if line.strip() == header:
            start = i
            break
    if start is None:
        raise ValueError(f"섹션 없음: {header}")

    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break

    body = body.strip("\n")
    block = [lines[start], "\n", body + "\n"]
    if end < len(lines):
        block.append("\n")
    return "".join(lines[:start] + block + lines[end:])


def render_current(payload: dict[str, Any], existing: str) -> str:
    """`context/{영역}/current.md` — **`## 진행 중` 섹션만** 갈아 끼운다.

    갱신안이 담는 것은 그 표 하나다. 우선순위·이번 주 목표·Blockers 는 판단이라
    사람 소유이고, 담기면 `_current_violations` 가 발행을 막는다.
    """
    return replace_section(existing, CURRENT_MANAGED_SECTION, str(payload.get("content") or ""))


def build_actions(
    approved: dict[str, dict[str, Any]],
    *,
    repo_root: Path | None = None,
    source_key: str | None = None,
) -> list[FileAction]:
    """승인된 게이트 산출물 → 파일 액션 목록.

    `approved` 는 `{stage_name: payload}`. **경로는 payload 의 `target_path` 를 쓰되**,
    그것도 시스템이 조립한 값이지 AI 가 낸 값이 아니다(스테이지에서 stem 만 받는다).

    `source_key` 는 항목의 `normalized_url` 이다. 공부 노트면 `study:{slug}` 라
    **어느 입구 파일에서 왔는지**를 그 값 하나가 안다 — 그래서 발행이 그 파일을
    회수할 수 있다(아래 `remove`).
    """
    actions: list[FileAction] = []

    for stage in ("source_note", "derived", "post"):
        payload = approved.get(stage)
        if not payload:
            continue
        content = str(payload.get("content") or "")
        actions.append(
            FileAction(
                action="create",
                path=str(payload.get("target_path") or ""),
                content=content,
                note_type=_note_type(content),
                stem=str(payload.get("filename_stem") or ""),
                source_gate=stage,
            )
        )

    # --- 잔디 (KDEV-WORK-017 P3) -------------------------------------------
    # 게이트 하나가 목적지 셋을 낸다. 유튜브는 스테이지마다 하나씩이라 모양이 다르다.
    grass = approved.get("daily") or {}
    daily = grass.get("daily") or {}
    if daily.get("target_path"):
        content = render_daily(daily)
        actions.append(
            FileAction(
                # 첫 회 생성과 덮어쓰기가 **둘 다 정상**이다.
                action="upsert",
                path=str(daily.get("target_path") or ""),
                content=content,
                note_type=_note_type(content),
                stem=str(daily.get("date") or ""),
                source_gate="daily",
            )
        )

    career = grass.get("career") or {}
    if career.get("changed") and career.get("target_path"):
        path = str(career.get("target_path") or "")
        existing = ""
        if repo_root is not None:
            target = repo_root / path
            if target.exists():
                existing = target.read_text(encoding="utf-8")
        content = render_career(career, existing)
        actions.append(
            FileAction(
                # career 는 이미 있는 문서를 고치는 것이라 `replace` 다 — 대상이
                # 사라졌으면 `TARGET_MISSING` 으로 막혀야 한다.
                action="replace",
                path=path,
                content=content,
                note_type=_note_type(content),
                stem=str(career.get("stem") or ""),
                source_gate="daily",
            )
        )

    # **목록이다.** 회사·개인사업자 커밋이 하루에 둘 다 있는 것이 보통이라, 하나만
    # 담을 수 있으면 그런 날 한쪽 `current.md` 가 조용히 갱신되지 않는다.
    for current in (grass.get("currents") or []):
        if not (current.get("changed") and current.get("target_path")):
            continue
        path = str(current.get("target_path") or "")
        existing = ""
        if repo_root is not None:
            target = repo_root / path
            if target.exists():
                existing = target.read_text(encoding="utf-8")
        try:
            content = render_current(current, existing)
        except ValueError:
            # 섹션이 없다 — 그대로 넘겨 `_current_violations` 가 잡게 한다.
            content = existing
        actions.append(
            FileAction(
                action="replace",
                path=path,
                content=content,
                note_type="current",
                stem=str(current.get("stem") or ""),
                source_gate="daily",
            )
        )

    for concept in (grass.get("concepts") or []):
        if concept.get("excluded"):
            continue
        content = str(concept.get("content") or "")
        actions.append(
            FileAction(
                action="replace" if concept.get("mode") == "supplement" else "create",
                path=str(concept.get("target_path") or ""),
                content=content,
                note_type=_note_type(content),
                stem=str(concept.get("stem") or ""),
                source_gate="daily",
            )
        )

    for concept in (approved.get("concept") or {}).get("concepts") or []:
        if concept.get("excluded"):
            # 제외한 개념은 계획에 들어가지 않는다 — 승인 화면에서 뺀 것이 그대로 반영된다.
            continue
        content = str(concept.get("content") or "")
        actions.append(
            FileAction(
                action="replace" if concept.get("mode") == "supplement" else "create",
                path=str(concept.get("target_path") or ""),
                content=content,
                note_type=_note_type(content),
                stem=str(concept.get("stem") or ""),
                source_gate="concept",
            )
        )

    # --- 입구 회수 (KDEV-DEC-021 D1) ---------------------------------------
    # 공부 노트는 `inbox/{slug}.md` 에서 왔다. 접수 때 작업트리에서는 이미 지웠지만
    # **그 삭제가 커밋되지 않으면** `reset --hard` 한 번에 파일이 되살아나고, 입구가
    # 비어 있다는 약속이 깨진다. 산출물과 **같은 커밋**으로 묶는 이유이기도 하다 —
    # 나눠 커밋하면 「노트는 발행됐는데 입구에 원본이 남은」 중간 상태가 생긴다.
    #
    # 산출이 하나도 없으면 붙이지 않는다. 지우기만 하는 커밋은 발행이 아니다.
    #
    # 접두는 접수부에서 가져온다 — 여기 `"study:"` 를 다시 적으면 SoT 가 둘이 되고,
    # 한쪽만 고쳐지는 날 입구 파일이 조용히 회수되지 않는다.
    from service.pipeline.study_intake import KEY_PREFIX as STUDY_KEY_PREFIX

    if actions and (source_key or "").startswith(STUDY_KEY_PREFIX):
        slug = source_key[len(STUDY_KEY_PREFIX) :]
        if slug:
            actions.append(
                FileAction(
                    action="remove",
                    path=f"inbox/{slug}.md",
                    content="",
                    note_type="idea",
                    stem=slug,
                    source_gate="intake",
                )
            )
    return actions


def _content_filename_violations(action: FileAction, path: str) -> list[Violation]:
    """교안 파일명이 로더 규약(`{id}-...`)을 지키는지."""
    try:
        meta = frontmatter.loads(action.content).metadata
    except Exception:  # noqa: BLE001
        meta = {}
    content_id = str(meta.get("id") or "").strip()
    if not content_id:
        return [Violation("MISSING_CONTENT_ID", path, "교안에 id 가 없다")]
    stem = path.rsplit("/", 1)[-1][: -len(".md")]
    if not stem.startswith(f"{content_id}-"):
        return [
            Violation(
                "CONTENT_FILENAME",
                path,
                f"파일명이 '{content_id}-' 로 시작해야 한다 — 로더가 거부하면 persona 로드 전체가 실패한다",
            )
        ]
    return []


def _daily_violations(action: FileAction, path: str, repo_root: Path) -> list[Violation]:
    """대상 daily 가 **본인 작성**이면 덮어쓰지 않는다 (SPEC-012 S-5 / SPEC-013 S-6).

    보호는 이중이다 — 접수 단계가 한 번 막고(`intake_daily`) 여기가 한 번 더 막는다.
    접수 뒤에 사람이 직접 쓴 경합을 잡는 자리가 이쪽이다. 그 사이가 몇 시간이라
    실제로 일어날 수 있다.

    `auto: true` 가 아니면 사람 것으로 본다 — 자동 생성분만 명시적으로 표시되므로
    이쪽이 안전한 기본값이다.
    """
    target = repo_root / path
    if not target.exists():
        return []
    try:
        meta = frontmatter.loads(target.read_text(encoding="utf-8")).metadata
    except Exception:  # noqa: BLE001 — 읽을 수 없으면 건드리지 않는 편이 안전하다
        return [
            Violation("USER_AUTHORED_DAILY", path, "대상 daily 를 읽을 수 없다")
        ]
    if meta.get("auto") is not True:
        return [
            Violation(
                "USER_AUTHORED_DAILY",
                path,
                "그날 daily 는 본인 작성이다 — 덮어쓰지 않는다",
            )
        ]
    return []


def _current_violations(action: FileAction, path: str, repo_root: Path) -> list[Violation]:
    """`current.md` 는 **`## 진행 중` 만** 바뀌어야 한다 (KDEV-DEC-022 D2).

    사람 소유 섹션(우선순위·이번 주 목표·Blockers·운영 원칙)이 갱신안에 담기면
    **무시하는 것이 아니라 거부한다** — `PROTECTED_CAREER_FIELDS` 와 같은 규율이다.
    무시하면 다음 사람이 「담아도 되는구나」로 읽는다.
    """
    violations: list[Violation] = []
    target = repo_root / path
    if not target.exists():
        # `replace` 인데 대상이 없다 — 상위 검증이 TARGET_MISSING 으로 잡는다.
        return violations

    existing = target.read_text(encoding="utf-8")
    if CURRENT_MANAGED_SECTION not in existing:
        violations.append(
            Violation(
                "CURRENT_SECTION_MISSING",
                path,
                f"{CURRENT_MANAGED_SECTION} 섹션이 없다 — 헤더 이름이 바뀌었나",
            )
        )
        return violations

    def _sections(text: str) -> dict[str, str]:
        out: dict[str, str] = {}
        cur = None
        buf: list[str] = []
        for line in text.splitlines(keepends=True):
            if line.startswith("## "):
                if cur is not None:
                    out[cur] = "".join(buf)
                cur = line.strip()
                buf = []
            elif cur is not None:
                buf.append(line)
        if cur is not None:
            out[cur] = "".join(buf)
        return out

    before, after = _sections(existing), _sections(action.content)
    if set(before) != set(after):
        violations.append(
            Violation("CURRENT_SECTIONS_CHANGED", path, "섹션 구성이 바뀌었다 — 사람 소유다")
        )
        return violations

    for name in before:
        if name == CURRENT_MANAGED_SECTION:
            continue
        if before[name] != after[name]:
            violations.append(
                Violation(
                    "CURRENT_PROTECTED_SECTION",
                    path,
                    f"{name} 은 사람 소유다 — 갱신안이 건드렸다",
                )
            )
    return violations


def _career_violations(action: FileAction, path: str) -> list[Violation]:
    """사람 전용 필드가 **바뀌었으면** 거부한다 (SPEC-012 / SPEC-013 `PROTECTED_FIELD`).

    계획의 career 내용은 기존 frontmatter 를 그대로 이고 본문만 바꾼 것이라, 정상
    경로에서는 이 검사가 걸릴 일이 없다. 그래도 두는 이유는 **계획이 조립되는 경로가
    하나뿐이라고 가정하지 않기 위해서다** — 저장된 계획으로 재시도하는 경로가 있고,
    그 계획이 다른 코드로 만들어졌을 수 있다. 파일을 쓰기 전이 마지막 기회다.
    """
    try:
        meta = frontmatter.loads(action.content).metadata
    except Exception:  # noqa: BLE001
        return [Violation("PROTECTED_FIELD", path, "career frontmatter 를 읽을 수 없다")]
    missing = [f for f in ("type", "period", "title", "org") if f not in meta]
    if missing:
        # 로더 필수 필드다. 빠지면 파일 하나가 아니라 persona 로드 전체가 실패한다.
        return [
            Violation(
                "PROTECTED_FIELD",
                path,
                f"career 필수 필드가 사라졌다: {', '.join(missing)}",
            )
        ]
    return []


def validate_plan(
    actions: list[FileAction],
    *,
    repo_root: Path,
    known_stems: set[str] | None = None,
) -> list[Violation]:
    """검증 6종 중 파일 단위 5종. 그래프 검증(L1~L6)은 `validate_virtual_graph` 가 맡는다.

    1. 경로 allowlist  2. 층-경로 정합  3. `up:` 필수  4. 신규 중복  5. stale 대상
    """
    violations: list[Violation] = []
    seen: set[str] = set()

    for action in actions:
        path = action.path

        # 1. 경로 allowlist
        if not path or _TRAVERSAL.search(path) or not path.endswith(".md"):
            violations.append(Violation("PATH_SHAPE", path, "경로 형태가 올바르지 않다"))
            continue
        if not any(path.startswith(prefix) for prefix in ALLOWED_PREFIXES):
            violations.append(
                Violation("PATH_NOT_ALLOWED", path, "발행이 쓸 수 없는 디렉토리다")
            )
            continue
        if path in seen:
            violations.append(Violation("DUPLICATE_PATH", path, "한 발행에 같은 경로가 두 번"))
            continue
        seen.add(path)

        # 2. 층-경로 정합
        expected = LAYER_PREFIX.get(action.note_type)
        if expected is None:
            violations.append(
                Violation("UNKNOWN_TYPE", path, f"알 수 없는 type: {action.note_type or '(없음)'}")
            )
        elif not path.startswith(expected):
            violations.append(
                Violation(
                    "LAYER_PATH_MISMATCH",
                    path,
                    f"type={action.note_type} 는 {expected} 아래여야 한다",
                )
            )
        elif action.note_type == "content":
            # 교안은 `{id}-{slug}.md` 여야 한다 (spec-01 §6.1). 규약을 어기면 파일
            # 하나가 거부되는 데서 끝나지 않고 **persona 로드 전체가 실패해** 사이트가
            # 옛 데이터를 계속 서빙한다 — 콘텐츠 갱신이 통째로 멈춘다.
            # 발행 뒤에야 알게 되므로 나가기 전에 잡는다.
            violations.extend(_content_filename_violations(action, path))

        # 2-b. 잔디 전용 검증 (KDEV-WORK-017 P3 / SPEC-013)
        if action.note_type == "daily":
            violations.extend(_daily_violations(action, path, repo_root))
        elif action.note_type == "career":
            violations.extend(_career_violations(action, path))
        elif action.note_type == "current":
            violations.extend(_current_violations(action, path, repo_root))

        # 3. `up:` 필수 (concept) — KDEV-DEC-019 로 permanent 는 폐기됐다
        if action.note_type == "concept":
            try:
                meta = frontmatter.loads(action.content).metadata
            except Exception:  # noqa: BLE001
                meta = {}
            if not meta.get("up"):
                violations.append(Violation("MISSING_UP", path, "up: 이 비어 있다"))

        target = repo_root / path
        exists = target.exists()

        # 4. 신규 중복 — 새로 만든다면서 이미 있으면 덮어쓰는 것이다
        #
        # `upsert` 는 이 검사도 아래 stale 검사도 받지 않는다. 첫 회 생성과 덮어쓰기가
        # 둘 다 정상이라 존재 여부가 판단 근거가 못 된다(SPEC-013). 경로 허용과 층 매핑은
        # 위에서 이미 봤다.
        if action.action == "create":
            if exists:
                violations.append(
                    Violation("ALREADY_EXISTS", path, "신규인데 파일이 이미 있다")
                )
            if known_stems and action.stem in known_stems:
                violations.append(
                    Violation("STEM_TAKEN", path, f"stem '{action.stem}' 이 이미 그래프에 있다")
                )
        # 5. stale 대상 — 고친다면서 대상이 없으면 초안 이후 사라진 것이다
        elif action.action == "replace" and not exists:
            violations.append(
                Violation("TARGET_MISSING", path, "수정 대상 파일이 사라졌다")
            )

    if not actions:
        violations.append(Violation("EMPTY_PLAN", "", "발행할 것이 없다"))
    return violations
