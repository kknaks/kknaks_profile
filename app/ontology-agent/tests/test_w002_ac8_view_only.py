"""AC-8 정적 게이트 — 소비자 표면이 원 테이블을 읽지 못함을 **코드로** 고정한다.

`connect_ro()` 는 쓰기만 막는다. 같은 커넥션으로 `SELECT * FROM bronze_vegas_reservations`
가 그대로 되므로, 「뷰 경유 강제」는 커넥션이 아니라 **코드에 무엇이 적혀 있는가**로만
보장된다(WORK-001 리뷰어 조건 · DEC-002 「새 경로가 곧 구멍」).

그래서 이 파일은 실행 경로가 아니라 **소스 텍스트와 AST** 를 검사한다 — 런타임 테스트는
「지금 그 코드가 안 불렸다」만 증명하지만, 정적 검사는 「그런 코드가 없다」를 증명한다.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

APP = Path(__file__).resolve().parents[1]
#: 소비자 표면 — 도구·API 와 그 둘이 공유하는 조회 구현.
#: `main.py` 도 넣는다. 라우트가 DB 를 직접 여는 자리가 생겼기 때문이다(`/api/meta/build`) —
#: 「조회 코드는 저기 없다」는 전제가 이미 깨졌다(검수 §3).
SURFACE_DIRS = ("tools", "api", "service")
SURFACE_FILES = ("main.py",)

#: 브론즈·실버 **원 테이블** 이름. 뷰(`v_bronze_*`·`v_silver_*`)는 앞의 `v_` 로 빠진다.
#:
#: 뒤에 `.` 이 오는 것은 제외한다 — `silver_reservations.sales` 는 **컬럼 출처 표기**이지
#: 조회 대상이 아니다(계보 응답의 `source_columns`·`related_columns` 가 그 형태다).
#: 점 없는 홑이름만 FROM 절에 들어갈 수 있으므로, 이 구분이 게이트를 무디게 하지 않는다.
#: `\b` 가 없으면 `[a-z_]+` 가 되감기며 `silver_reservation` 으로 줄여 매치해 버린다 —
#: 뒤의 `(?!\.)` 가 무력해지는 자리다. 경계를 박아 **식별자 전체**로만 매치시킨다.
#: **대소문자를 가리지 않는다.** SQLite 식별자는 대소문자 무관이라
#: `FROM BRONZE_VEGAS_RESERVATIONS` 가 런타임에 그대로 동작한다 — 게이트만 못 보면 구멍이다.
RAW_TABLE = re.compile(r"(?<![\w.])(?<!v_)(?<!V_)(bronze|silver)_[a-z_]+\b(?!\.)", re.IGNORECASE)

#: f-string 합성 — `f"bronze_{t}"` · `f"SELECT * FROM {prefix}_vegas_reservations"` 처럼
#: 접두어와 치환식을 이어 붙여 관계명을 만드는 자리. 홑이름 검사가 원리적으로 못 본다.
#: allowlist 의 `relation` 을 거치지 않는 관계명 조립은 이 표면에 있으면 안 된다.
COMPOSED_RELATION = re.compile(
    r"(?:"
    r"(?:bronze|silver)_[a-z_]*\{"          # bronze_{t} · silver_{name}
    r"|\}_[a-z_]*(?:reservations|reviews|catalog|promotions|mappings|branch_alias)"
    r")",                                    # {prefix}_vegas_reservations
    re.IGNORECASE,
)

#: 마스킹 뷰만 예외로 허용. `v_` 접두어가 붙은 것과 실버의 PII 없는 테이블 4종이다.
#: (SPEC-002 §4 — catalog·promotions·mappings·branch_alias 는 PII 가 없어 원형을 읽는다)
PII_FREE_SILVER = frozenset({
    "silver_catalog", "silver_promotions", "silver_mappings", "silver_branch_alias",
})
#: nexus 브론즈 14종도 PII 가 없다(SPEC-002 §4 허용 테이블 표).
PII_FREE_BRONZE_PREFIX = "bronze_nexus_"

#: PII 원 컬럼 — 소비자 표면 어디에도 이 이름으로 조회하는 코드가 없어야 한다
PII_COLUMNS = ("patientName", "phone", "birthday")


def _surface_files() -> list[Path]:
    files: list[Path] = []
    for d in SURFACE_DIRS:
        files += sorted(p for p in (APP / d).rglob("*.py") if "__pycache__" not in p.parts)
    files += [APP / f for f in SURFACE_FILES]
    return files


def test_소비자_표면_파일이_실제로_있다():
    """검사 대상이 비면 이 게이트는 조용히 통과한다 — 그 자체가 구멍이다."""
    files = _surface_files()
    assert len(files) >= 8, f"소비자 표면 파일이 너무 적다: {[f.name for f in files]}"


@pytest.mark.parametrize("path", _surface_files(), ids=lambda p: f"{p.parent.name}/{p.name}")
def test_AC8_소비자_표면에_PII_원_테이블_문자열이_없다(path: Path):
    """브론즈·실버 원 테이블 이름이 코드에 나오면 FAIL.

    허용은 마스킹 뷰(`v_*`)와 PII 없는 테이블뿐이다 — allowlist 방식이라
    새 테이블이 생겨도 자동으로 막히는 쪽이다.
    """
    offenders: list[str] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue  # 주석의 설명 문구는 조회 경로가 아니다
        for match in RAW_TABLE.finditer(line):
            name = match.group(0)
            # 값 whitelist 는 소문자 정본으로만 인정한다 — 대문자 변형은 통과시키지 않는다
            if name in PII_FREE_SILVER or name.startswith(PII_FREE_BRONZE_PREFIX):
                continue
            offenders.append(f"{path.name}:{lineno} {name}")
        for match in COMPOSED_RELATION.finditer(line):
            offenders.append(f"{path.name}:{lineno} (합성) {match.group(0)}")
    assert offenders == [], (
        "소비자 표면이 PII 를 담은 원 테이블을 가리킨다 — 마스킹 뷰(v_*)만 읽어야 한다:\n"
        + "\n".join(offenders)
    )


def test_AC8_게이트_정규식이_알려진_우회를_잡는다():
    """게이트 자체의 회귀 — 「무엇을 못 보는가」를 테스트로 고정한다.

    검수 W2 가 실측한 두 갈래(대소문자 · f-string 합성)를 닫았고, 닫지 못한 한 갈래
    (동적 컬럼 조립)는 아래 `test_AC8_게이트의_한계` 가 명시한다.
    """
    caught = [
        "FROM bronze_vegas_reservations",
        "FROM BRONZE_VEGAS_RESERVATIONS",          # SQLite 는 대소문자를 안 가린다
        'f"bronze_{t}"',                            # 접두어 + 치환식 합성
        'f"SELECT * FROM {prefix}_vegas_reservations"',
        "conn.execute('SELECT * FROM silver_reservations')",
    ]
    for line in caught:
        hit = bool(RAW_TABLE.search(line)) or bool(COMPOSED_RELATION.search(line))
        assert hit, f"게이트가 못 잡는다: {line}"

    passed = [
        "SELECT * FROM v_bronze_vegas_reservations",   # 마스킹 뷰
        '"silver_reservations.sales"',                 # 컬럼 출처 표기
        "FROM silver_catalog",                         # PII 없는 실버(SPEC-002 §4)
        "FROM bronze_nexus_branches",                  # PII 없는 nexus
    ]
    for line in passed:
        offenders = [
            m.group(0) for m in RAW_TABLE.finditer(line)
            if m.group(0) not in PII_FREE_SILVER
            and not m.group(0).startswith(PII_FREE_BRONZE_PREFIX)
        ] + [m.group(0) for m in COMPOSED_RELATION.finditer(line)]
        assert offenders == [], f"게이트가 잘못 잡는다: {line} → {offenders}"


def test_AC8_게이트의_한계():
    """**이 게이트가 지키지 못하는 것**을 코드에 남긴다 — 오독을 막는 것도 게이트의 일이다.

    동적 컬럼 조립(`col = f'"{_ident(field)}"'`)은 정적으로 볼 수 없다. 따라서
    **「AC-8 게이트가 있으니 AC-3 도 지켜진다」로 읽으면 안 된다** — 둘은 다른 축이다.
    AC-3(PII 원 컬럼 우회 차단)의 실질 보장은 「값이 마스킹본이라 원값 조회가 0건」이고,
    그것은 정적 검사가 아니라 `test_w002_tools.py` 의 런타임 테스트가 진다.
    """
    dynamic = "col = f'\"{_ident(field)}\"'"
    assert not RAW_TABLE.search(dynamic)
    assert not COMPOSED_RELATION.search(dynamic)


@pytest.mark.parametrize("path", _surface_files(), ids=lambda p: f"{p.parent.name}/{p.name}")
def test_AC8_소비자_표면에_PII_원_컬럼_조회가_없다(path: Path):
    """`patientName` 등이 SQL 문자열 안에 나오면 FAIL.

    마스킹 표기 상수(`masked_fields` 목록·`MASK_NOTATION`)는 조회가 아니라 **응답 메타**라
    허용한다 — 무엇이 가려졌는지 알리려면 이름을 말해야 한다.
    """
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    offenders: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        text = node.value
        if not any(c in text for c in PII_COLUMNS):
            continue
        # SQL 로 보이는 문자열에만 걸린다
        if re.search(r"\b(SELECT|FROM|WHERE|ORDER BY)\b", text, re.IGNORECASE):
            offenders.append(f"{path.name}:{node.lineno} {text[:60]!r}")
    assert offenders == [], (
        "소비자 표면이 PII 원 컬럼을 SQL 로 조회한다:\n" + "\n".join(offenders))


@pytest.mark.parametrize("path", _surface_files(), ids=lambda p: f"{p.parent.name}/{p.name}")
def test_AC8_소비자_표면이_쓰기_구문을_갖지_않는다(path: Path):
    """읽기 전용 표면이다 — INSERT·UPDATE·DELETE·DROP·CREATE 가 나오면 FAIL."""
    source = path.read_text(encoding="utf-8")
    offenders = []
    for lineno, line in enumerate(source.splitlines(), 1):
        if line.strip().startswith("#"):
            continue
        if re.search(r"\b(INSERT\s+INTO|UPDATE\s+\w+\s+SET|DELETE\s+FROM|DROP\s+|CREATE\s+TABLE)\b",
                     line, re.IGNORECASE):
            offenders.append(f"{path.name}:{lineno}")
    assert offenders == [], f"소비자 표면에 쓰기 구문이 있다: {offenders}"


def test_AC8_도구_서버가_자유_SQL_파라미터를_갖지_않는다():
    """`sql`·`query`·`path` 류 파라미터는 **표면 자체로 없어야** 한다(SPEC-002 S-6).

    거부하는 게 아니라 부재다 — 받는 자리가 있으면 언젠가 누가 통과시킨다.
    """
    tree = ast.parse((APP / "tools" / "server.py").read_text(encoding="utf-8"))
    banned = {"sql", "query", "path", "expr", "where", "raw", "cmd", "command", "script"}
    offenders = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not any(_is_tool_decorator(d) for d in node.decorator_list):
            continue
        args = [a.arg for a in node.args.args + node.args.kwonlyargs]
        hits = banned & set(args)
        if hits:
            offenders.append(f"{node.name}: {sorted(hits)}")
    assert offenders == [], f"도구에 자유 입력 파라미터가 있다: {offenders}"


def _is_tool_decorator(node: ast.expr) -> bool:
    target = node.func if isinstance(node, ast.Call) else node
    return isinstance(target, ast.Attribute) and target.attr == "tool"


def test_AC1_도구가_정확히_4종이다():
    """자유 SQL·파일·쉘 도구가 0개임을 도구 목록으로 확인한다(SPEC-002 AC-1)."""
    tree = ast.parse((APP / "tools" / "server.py").read_text(encoding="utf-8"))
    names = [
        node.name for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and any(_is_tool_decorator(d) for d in node.decorator_list)
    ]
    assert sorted(names) == sorted(
        ["query_kpi", "query_layer", "trace_ontology", "get_definition"]), names

    from tools.server import TOOL_NAMES

    assert sorted(TOOL_NAMES) == sorted(names)


def test_비밀번호가_코드에_하드코딩되지_않는다():
    """값은 env 로만 주입한다 — 기본값·문서·응답 어디에도 없다(SPEC-003 AC-2)."""
    from config import Settings

    assert Settings().demo_password == "", "demo_password 에 기본값이 있으면 게이트가 아니다"
    for path in _surface_files() + [APP / "config.py"]:
        source = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(source.splitlines(), 1):
            if "demo_password" in line and "=" in line and "settings." not in line:
                value = line.split("=", 1)[1].strip()
                assert value in ('""', "''", "str = \"\"", 'str = ""'), (
                    f"{path.name}:{lineno} 비밀번호에 값이 박혀 있다: {line.strip()}")
