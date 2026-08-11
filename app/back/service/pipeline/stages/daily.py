"""`daily` 게이트 스테이지 — 잔디 산출물 작성 (KDEV-WORK-017 P2 / KDEV-SPEC-012·013).

`investigate` 가 만든 레포별 재료를 daily·career·concept 초안으로 바꾼다. 여기서 처음
**형식**이 등장하고, 그 형식은 프롬프트에 적혀 있지 않고 `templates/persona/` 에서
실려 온다(SPEC-012 「형식 SoT」).

**작성 주체가 게이트인 이유.** 처음에는 `compose` 라는 auto 스테이지가 초안을 만들고
게이트는 그것을 보여 주기만 하는 모양이었다. 그런데 재생성(SPEC-013 S-3)은 "조사는
다시 돌지 않고 서술만 다시 만든다" 이므로 **게이트가 작성 능력을 갖고 있어야 한다.**
그러면 auto 쪽 작성은 첫 회에만 쓰이고 재생성마다 게이트가 다시 만드는 중복이 된다.
그래서 작성을 게이트 한 곳으로 모았다. 유튜브도 같은 모양이다 — `summarize`(auto)는
route 판단 재료를 만들 뿐이고 노트 **작성**은 게이트 스테이지가 한다.

세 산출물의 성격이 다르다.

    daily     매일 만든다. 본문은 사이트에 노출되지 않고 다음 단계의 입력이다
    career    **조건부다.** company 귀속 커밋이 0이면 대상에서 아예 빠진다
    concept   후보가 있을 때만. 억지로 만들지 않는다

`counts` 는 코드가 채운다. AI 출력의 숫자를 믿지 않는다(SPEC-012 §5).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import frontmatter

from service.content_format import (
    CURRENT_MANAGED_SECTION,
    career_format,
    current_format,
    daily_format,
)

from ..collect_common import CONTEXT_AREAS
from ..concept_index import build_index
from ..executor import AgentStage
from ..gates import GateError, GenerationInput
from .common import (
    CONCEPT_STEM_RE,
    READ_THE_RULES,
    check_note,
    extract_json_object,
)

logger = logging.getLogger("kknaks-back.pipeline.daily")

#: 본문 하드 상한 (SPEC-012). 1200자가 목표이고 이 값을 넘으면 자른다.
BODY_HARD_LIMIT = 1500

PROMPT = """하루치 커밋 조사와 레포별 정리를 읽고 문서 초안을 만든다.

아래 **형식 명세를 그대로 따른다.** 명세에 없는 필드를 만들지 않는다.

=== daily 형식 ===
{daily_format}

=== career 형식 ===
{career_format}

=== current 형식 ===
{current_format}

## 만들 것

JSON 하나로 답한다. 코드펜스로 감싸지 않고, **앞뒤에 설명 문장을 붙이지 않는다** —
첫 글자가 `{{` 여야 한다. 무엇을 왜 그렇게 판단했는지는 JSON 안의 자리에 적는다.

{{
  "daily": {{
    "summary": {{"ko": ["[owner/repo] ...", "[notes] ..."], "en": [...]}},
    "body": "마크다운 본문"
  }},
  "career": {career_shape},
  "currents": {current_shape},
  "concepts": [
    {{"stem": "kebab-case", "title": "제목", "content": "노트 전문", "mode": "create"}}
  ]
}}

- `counts` 를 만들지 마라. 코드가 채운다
- `summary` 는 활동 단위마다 한 줄이고, **활동이 0인 카테고리는 줄을 만들지 않는다**
- `feedback` 이 있으면 그 지적을 반영해 다시 쓴다. 조사 결과는 바뀌지 않았다

## current 는 「지금 무엇을 하고 있나」다 — 그날 일지가 아니다

`currents` 의 `content` 는 **`## 진행 중` 표 본문만**이다. 헤더(`## 진행 중`)를 담지
않는다 — 시스템이 붙인다.

- **아래 `current_targets` 의 `current_section` 이 지금 적혀 있는 표다.** 그것을
  **고쳐 쓴다.** 처음부터 다시 쓰면 어제 남긴 `todo` 행이 조용히 사라진다
- 그날 커밋이 있는 제품은 행을 **갱신**하고, 커밋이 없던 제품 행은 **그대로 둔다** —
  오늘 안 건드렸다는 것이 그 일이 끝났다는 뜻은 아니다
- `Blocker` 는 **커밋에서 드러난 것만** 쓴다. 없으면 비운다. 지어내지 않는다
- 우선순위·이번 주 목표·Blockers 절을 담지 마라. **사람 소유라 담기면 발행이 거부된다**

## concept 는 지식그래프에 들어간다 — 규율이 다르다

daily·career 와 달리 concept 는 **그래프 노드**다. 유튜브가 만드는 개념과 같은 규칙을
받는다.

{concept_rules}

- **억지로 만들지 않는다.** 뽑을 것이 없으면 빈 배열이다. 그날 작업에만 붙어 있는
  설명은 개념이 아니다
- **이미 있는 개념인지 먼저 확인하라.** 아래 `existing_concepts` 에 stem·title·aliases 가
  있다. 이름이 달라도 같은 개념이면 새로 만들지 말고 `mode: "supplement"` 로 그 파일을
  직접 읽고 다시 쓴다. 기존 `aliases` 와 `up:` 은 하나도 빠뜨리지 않는다
- `stem` 에 **날짜를 붙이지 않는다.** 개념은 특정 시점에 묶이지 않는다
- `aliases` 는 **필수**다. 비면 다음에 같은 개념이 두 파일로 갈라진다
- `up:` 은 **필수**이고 `existing_concepts` 나 기존 지식노트 중 **실재하는 stem** 을
  가리켜야 한다. **daily 나 career 를 걸지 마라 — 그 둘은 그래프 노드가 아니라서
  고아가 되고 발행이 거부된다.** 개념이 개념에서 자라는 것이 정상이다
- `up:` 에 쓴 stem 은 **본문에도 `[[stem]]` 으로 있어야 한다.** `up:` 은 본문 링크의
  부분집합이다 — 어긋나면 발행 직전 검증(L3)에 걸린다
"""

CAREER_SHAPE_ACTIVE = """{
    "changed": true,
    "stem": "<대상 stem>",
    "content": "본문 전문 (frontmatter 없이 ## 섹션들만)"
  }"""

CAREER_SHAPE_NONE = """null   (이번엔 career 대상이 없다. null 로 둔다)"""

CURRENT_SHAPE_ACTIVE = """[
    {"area": "<대상 area>", "changed": true, "content": "| Project | Work | Status | Blocker | Next |\\n|---|---|---|---|---|\\n| ... |"}
  ]"""

CURRENT_SHAPE_NONE = """[]   (이번엔 current 대상이 없다. 빈 배열로 둔다)"""


def career_targets(collect: dict[str, Any], repo_root: Path) -> list[dict[str, Any]]:
    """갱신 대상 career. **결정적으로 고른다 — 모델에게 묻지 않는다.**

    빠지는 조건이 셋이다(SPEC-012 S-2).

        귀속 커밋 0       `type=studio` 만 커밋한 날. career 를 만들지 않는다
        `is_current` 아님  끝난 재직 기간을 오늘 커밋으로 고치지 않는다
        파일 없음          `detail` 이 가리키는 문서가 사라졌다

    제출과 수확 양쪽에서 같은 값이 나와야 하므로 **저장하지 않고 다시 계산한다** —
    입력이 같으면 결과가 같다. 제출 시점의 지역 변수를 붙잡아 두면 back 재시작 뒤에
    수확이 다른 판단을 하게 된다.
    """
    targets: list[dict[str, Any]] = []
    for stem, repos in (collect.get("career_map") or {}).items():
        if not repos:
            continue
        path = repo_root / "persona" / "career" / f"{stem}.md"
        if not path.exists():
            logger.info("career 대상 없음 — %s (DETAIL_NOT_FOUND)", stem)
            continue
        # 로그만으로는 아무도 모른다 — 이 결과는 `missing_career()` 가 화면까지 들고 간다.
        try:
            post = frontmatter.load(path)
        except Exception:  # noqa: BLE001
            logger.warning("career 문서를 읽지 못했다 — %s", stem)
            continue
        if not post.metadata.get("is_current"):
            continue
        targets.append({"stem": stem, "repos": repos, "body": post.content})
    return targets


def missing_career(collect: dict[str, Any], repo_root: Path) -> list[str]:
    """`detail` 이 가리키는 career 문서가 없는 stem (KDEV-SPEC-011 `DETAIL_NOT_FOUND`).

    **레지스트리의 CHECK 는 `detail` 이 비었는지만 막는다.** 오타난 stem
    (`medisolve-ai` → `medisolveai`)은 그대로 등록되고, 그때 `career_targets` 가 조용히
    건너뛴다 — 그 레포의 그날 작업이 **어느 career 에도 안 실린다**는 뜻인데 아무도
    모른다. 로그는 사람이 안 본다.

    **검증을 여기 두는 이유**는 등록 시점이 아니라 귀속 시점이 맞기 때문이다. 등록
    시점에 보면 DB 계층이 레포 파일시스템을 알게 되고, 나중에 career 파일 이름이
    바뀌면 그 검증이 무용해진다. 여기는 이미 파일을 읽는 층이고 매번 다시 본다.

    `career_targets` 와 **같은 판정을 두 번 하지 않는다** — 저 함수가 거르는 셋 중
    "파일 없음" 만 여기서 센다. `is_current` 아님이나 귀속 커밋 0은 정상이라 알릴 것이 없다.
    """
    missing: list[str] = []
    for stem, repos in (collect.get("career_map") or {}).items():
        if not repos:
            continue
        if not (repo_root / "persona" / "career" / f"{stem}.md").exists():
            missing.append(stem)
    return sorted(missing)


def current_targets(collect: dict[str, Any], repo_root: Path) -> list[dict[str, Any]]:
    """갱신 대상 `context/{영역}/current.md` (KDEV-DEC-022 D1).

    `career_targets` 와 같은 규율이다 — **결정적으로 고른다.** 모델은 표를 어떻게
    쓸지만 정하고, 어느 문서를 건드릴지는 코드가 정한다.

        커밋 0        그 영역에 커밋이 없으면 대상이 아니다
        파일 없음      만들지 않는다. `current.md` 는 사람이 세운 문서다
        섹션 없음      헤더를 바꿨다는 뜻이다. **조용히 지나가지 않고 대상에서 뺀다**

    셋째가 중요하다. 섹션이 없는 채로 갱신안을 만들면 발행 직전 `CURRENT_SECTION_MISSING`
    으로 **잔디 전체가 거부된다** — daily 까지 같이 막힌다. 사람이 헤더를 바꾼 것은
    그 사람의 자유이고, 그 대가가 그날 잔디 실패여서는 안 된다.
    """
    targets: list[dict[str, Any]] = []
    for area in CONTEXT_AREAS:
        projects = (collect.get("context_map") or {}).get(area) or {}
        if not projects:
            continue
        path = repo_root / "context" / area / "current.md"
        if not path.exists():
            logger.info("current 대상 없음 — context/%s/current.md 가 없다", area)
            continue
        try:
            existing = path.read_text(encoding="utf-8")
        except OSError:
            logger.warning("context/%s/current.md 를 읽지 못했다", area)
            continue
        if CURRENT_MANAGED_SECTION not in existing:
            logger.warning(
                "context/%s/current.md 에 %s 섹션이 없다 — 갱신 대상에서 뺀다",
                area,
                CURRENT_MANAGED_SECTION,
            )
            continue
        targets.append(
            {
                "area": area,
                "projects": projects,
                "current_section": _section_body(existing, CURRENT_MANAGED_SECTION),
            }
        )
    return targets


def _section_body(text: str, header: str) -> str:
    """`header` 섹션의 본문. 없으면 빈 문자열.

    갱신안을 만들려면 **지금 뭐라고 적혀 있는지**를 모델이 봐야 한다. 안 주면 매일
    표를 처음부터 다시 써서 어제 남긴 `todo` 행이 조용히 사라진다.
    """
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.strip() != header:
            continue
        end = len(lines)
        for j in range(i + 1, len(lines)):
            if lines[j].startswith("## "):
                end = j
                break
        return "".join(lines[i + 1 : end]).strip()
    return ""


def _currents(value: Any, targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """대상 밖 영역은 무엇이 오든 버린다 — `_career` 와 같은 규율이다.

    **목록인 이유**는 하루에 회사·개인사업자 커밋이 둘 다 있는 것이 보통이기
    때문이다. 하나만 담을 수 있으면 그런 날 한쪽이 조용히 갱신되지 않는다.
    """
    by_area = {t["area"]: t for t in targets}
    if not by_area or not isinstance(value, list):
        return []
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for entry in value:
        if not isinstance(entry, dict):
            continue
        area = str(entry.get("area") or "")
        content = str(entry.get("content") or "").strip()
        if area not in by_area or area in seen or not content:
            continue
        if not entry.get("changed", True):
            continue
        if content.lstrip().startswith("## "):
            # 헤더까지 담아 오면 `replace_section` 이 헤더를 한 번 더 넣는다.
            raise GateError(
                "INVALID_CURRENT_OUTPUT",
                f"{area} 갱신안이 헤더를 담았다 — 표 본문만이다",
            )
        seen.add(area)
        out.append(
            {
                "changed": True,
                "area": area,
                "stem": area,
                "content": content,
                "previous_content": by_area[area]["current_section"],
                "target_path": f"context/{area}/current.md",
            }
        )
    return out


def _prep(request: GenerationInput) -> dict[str, Any]:
    return (request.preparation.payload or {}) if request.preparation else {}


def _collection(prep: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    """조사가 얼마나 온전했는지 — 승인 화면이 그린다 (KDEV-SPEC-011 S-3 4항).

    **전부 코드가 센 값이다.** AI 가 세면 "조사가 잘 됐다" 는 서술과 실제 상태가
    어긋날 수 있고, 사람이 그 둘을 구분할 방법이 없다.

    `total` 은 조사를 **시도한** 레포 수다 — 성공한 것과 결과가 돌아오지 않은 것의
    합이다. `failed` 는 그보다 앞 단계(클론·fetch)에서 빠진 것이라 `total` 에 들지
    않는다. 두 실패가 다른 자리에서 나므로 한 숫자로 뭉개지 않는다.
    """
    investigate = prep.get("investigate") or {}
    collect = prep.get("collect") or {}
    reports = investigate.get("repos") or {}
    missing = sorted(investigate.get("missing") or [])
    return {
        "done": len(reports),
        "total": len(reports) + len(missing),
        "missing": missing,
        "failed": list(collect.get("failures") or []),
        "truncated": dict(collect.get("truncated") or {}),
        # `detail` 오타로 갈 곳이 없어진 career. 승인하는 사람이 **바로 지금** 알아야
        # 한다 — 그 레포의 그날 작업이 어느 career 에도 안 실린 채 발행되기 때문이다.
        "career_missing": missing_career(collect, repo_root),
    }




def _summary(value: Any) -> dict[str, list[str]]:
    """`{ko: [], en: []}` 로 정규화. **로더가 이 모양을 하드 검증한다.**

    여기서 막지 않으면 발행 뒤 persona 로드 전체가 실패해 사이트가 옛 데이터를
    계속 서빙한다.
    """
    if not isinstance(value, dict):
        raise GateError("INVALID_DAILY_OUTPUT", "summary 가 {ko, en} 이 아니다")
    out: dict[str, list[str]] = {}
    for key in ("ko", "en"):
        items = value.get(key)
        if not isinstance(items, list) or not all(isinstance(i, str) for i in items):
            raise GateError("INVALID_DAILY_OUTPUT", f"summary.{key} 가 list[str] 이 아니다")
        # 활동이 0인 카테고리는 줄이 없어야 한다. 빈 줄이 오면 잔디 셀 카드에 그대로 뜬다.
        out[key] = [i.strip() for i in items if i.strip()]
    return out


def _career(value: Any, targets: list[dict[str, Any]]) -> dict[str, Any]:
    """대상이 아니면 무엇이 오든 `changed: false` 다.

    모델이 대상 밖 career 를 지어내는 경우를 여기서 버린다 — 대상 판정은 코드가
    결정적으로 했고, 그 판단이 모델 출력보다 우선한다.

    **기존 본문을 함께 담는다.** career 는 고쳐 쓰는 문서라 승인 화면이 "무엇이
    바뀌었는지" 를 보여줘야 하는데, 화면이 그것을 알려면 비교 대상이 있어야 한다.
    파일을 화면이 직접 읽을 수는 없으므로 여기서 실어 보낸다.
    """
    by_stem = {t["stem"]: t for t in targets}
    if not by_stem or not isinstance(value, dict):
        return {"changed": False}
    stem = str(value.get("stem") or "")
    content = str(value.get("content") or "").strip()
    if stem not in by_stem or not content or not value.get("changed"):
        return {"changed": False}
    return {
        "changed": True,
        "stem": stem,
        "content": content,
        "previous_content": by_stem[stem]["body"],
        "target_path": f"persona/career/{stem}.md",
    }


def _concepts(value: Any) -> list[dict[str, Any]]:
    """concept 는 **그래프 노드라 검사를 받는다.**

    daily·career 는 그래프 밖이라 모양만 맞으면 되지만, concept 는 유튜브가 만든 것과
    같은 계보 규율을 지켜야 한다(SPEC-012 §5). 여기서 막지 않으면 발행 직전 그래프
    검증에 걸려 **발행 전체가 거부된다** — daily 까지 같이 막힌다. 사람이 화면에서
    고칠 수 있는 시점에 걸러 주는 편이 낫다.

    유튜브 concept 게이트와 **같은 검사기**(`check_note`)를 쓴다. 규율이 둘이 되면
    한쪽만 고쳐지는 날 산출물이 갈라진다.
    """
    if not isinstance(value, list):
        return []
    out: list[dict[str, Any]] = []
    for entry in value:
        if not isinstance(entry, dict):
            continue
        stem = str(entry.get("stem") or "").strip()
        content = str(entry.get("content") or "").strip()
        if not stem or not content:
            continue
        check_note(
            stem,
            content,
            expected_type="concept",
            stem_pattern=CONCEPT_STEM_RE,
            # `up:` 이 없으면 고아가 되고, `aliases` 가 없으면 다음에 같은 개념이
            # 두 파일로 갈라진다.
            required=("title", "aliases", "up"),
        )
        out.append(
            {
                "stem": stem,
                "title": str(entry.get("title") or stem),
                "content": content,
                # **`create`** 다 — `new` 가 아니다. 유튜브 concept 게이트가 쓰는 값과
                # 같아야 승인 화면의 `ConceptList` 를 그대로 재사용할 수 있고,
                # 발행부의 create/replace 분기도 한 규약으로 돈다.
                "mode": "supplement" if entry.get("mode") == "supplement" else "create",
                "target_path": f"resources/concept/{stem}.md",
            }
        )
    return out


class DailyStage(AgentStage):
    """잔디 게이트 — daily·career·concept 초안을 만들고 사람에게 넘긴다."""

    source = "pipeline-daily"

    def prompt(self, request: GenerationInput) -> str:
        collect = _prep(request).get("collect") or {}
        targets = career_targets(collect, self.repo_root)
        currents = current_targets(collect, self.repo_root)
        return PROMPT.format(
            daily_format=daily_format(self.repo_root),
            career_format=career_format(self.repo_root),
            current_format=current_format(self.repo_root),
            career_shape=CAREER_SHAPE_ACTIVE if targets else CAREER_SHAPE_NONE,
            current_shape=CURRENT_SHAPE_ACTIVE if currents else CURRENT_SHAPE_NONE,
            # 형식을 복사하지 않고 **레포를 읽게** 한다 — 유튜브 concept 게이트와 같다.
            concept_rules=READ_THE_RULES.format(template="concept.md"),
        )

    def payload(self, request: GenerationInput) -> dict[str, Any]:
        prep = _prep(request)
        collect = prep.get("collect") or {}
        investigate = prep.get("investigate") or {}
        targets = career_targets(collect, self.repo_root)
        payload: dict[str, Any] = {
            "date": collect.get("date"),
            "counts": collect.get("counts"),
            "areas": collect.get("areas"),
            "repo_reports": investigate.get("repos") or {},
            # 조사가 빠진 레포와 상한 적중을 알려 준다 — 서술이 얕은 이유가 자료 부족
            # 때문인지 그날 일이 적어서인지 구분되어야 한다.
            "missing_repos": investigate.get("missing") or [],
            "truncated": collect.get("truncated") or {},
            "failed_repos": collect.get("failures") or [],
            # career 는 **전문 교체**라 기존 본문을 함께 준다. 안 주면 모델이 append 할
            # 수밖에 없고, 그러면 career 가 daily 의 복사본이 된다.
            # 매칭을 AI 에 맡기지 않는다 — 있는지 없는지는 파일 목록을 보면 아는
            # 사실이다. AI 는 무엇을 뽑을지만 정한다.
            "existing_concepts": build_index(self.repo_root).as_prompt_payload(),
            "career_targets": [
                {"stem": t["stem"], "repos": t["repos"], "current_body": t["body"]}
                for t in targets
            ],
            # **지금 표에 뭐라고 적혀 있는지**를 함께 준다. 안 주면 매일 표를 처음부터
            # 다시 써서 어제 남긴 `todo` 행이 조용히 사라진다 — career 에 기존 본문을
            # 주는 것과 같은 이유다.
            "current_targets": current_targets(collect, self.repo_root),
        }
        if request.previous_payload is not None:
            payload["previous_draft"] = request.previous_payload
        if request.feedback:
            payload["feedback"] = request.feedback
        return payload

    def parse(self, raw: str, request: GenerationInput) -> dict[str, Any]:
        try:
            data = json.loads(extract_json_object(raw))
        except ValueError as exc:
            raise GateError("INVALID_DAILY_OUTPUT", f"JSON 파싱 실패: {exc}") from exc
        if not isinstance(data, dict):
            raise GateError("INVALID_DAILY_OUTPUT", "출력이 객체가 아니다")

        prep = _prep(request)
        collect = prep.get("collect") or {}
        daily = data.get("daily") or {}
        body = str(daily.get("body") or "")
        if len(body) > BODY_HARD_LIMIT:
            logger.info("daily 본문 %d자 — %d자로 자른다", len(body), BODY_HARD_LIMIT)
            body = body[:BODY_HARD_LIMIT]

        targets = career_targets(collect, self.repo_root)
        return {
            "daily": {
                "date": collect.get("date"),
                # **코드가 넣는다.** AI 가 센 숫자를 쓰지 않는다.
                "counts": collect.get("counts") or {},
                "summary": _summary(daily.get("summary")),
                "body": body,
                "target_path": f"persona/daily/{collect.get('date')}.md",
            },
            "career": _career(data.get("career"), targets),
            "currents": _currents(data.get("currents"), current_targets(collect, self.repo_root)),
            "concepts": _concepts(data.get("concepts")),
            # **조사가 얼마나 온전했는지**를 화면까지 들고 간다. AI 프롬프트에는
            # 이미 실려 있었지만(payload) 승인 화면이 보는 것은 이쪽이라, 여기 없으면
            # 사람은 서술이 얕은 이유가 **자료 부족인지 그날 일이 적어서인지** 구분할
            # 수 없다. `counts` 와 같은 규율이다 — 코드가 세고 AI 는 관여하지 않는다.
            "collection": _collection(prep, self.repo_root),
        }
