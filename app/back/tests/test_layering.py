"""계층 규약 회귀 방지 (KDEV-WORK-018 P2).

규약의 SoT 는 `products/kknaks-dev/40-architecture/system/README.md` 「백엔드 계층
규약」이다. 여기서는 **신규 도메인이 그 규약을 어겼는지**만 기계로 잡는다.

레거시(`api/routers/queue.py`·`service/pipeline/**`)는 대상이 아니다. 일괄 리팩터를
하지 않기로 했고(WORK-017 이 구 경로 제거를 P5 한 곳에 가둔 것과 같은 이유), 그 결정을
테스트가 뒤집으면 안 된다. **대상 목록을 명시해 두는 것이 그 경계다** — 새 도메인이
생기면 여기 한 줄을 더한다.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

BACK = Path(__file__).resolve().parents[1]

#: 규약 적용 대상. 레거시는 여기 없다 — 없는 것이 결정이다.
GOVERNED_SERVICE = ("service/products",)
GOVERNED_API = ("api/routers/products.py", "api/schemas/products.py")
REPOSITORY = "repository"


def _sources(*rel: str) -> list[Path]:
    out: list[Path] = []
    for r in rel:
        target = BACK / r
        if target.is_dir():
            out += [p for p in target.rglob("*.py") if p.name != "__init__.py"]
        elif target.exists():
            out.append(target)
    return out


def _calls(path: Path) -> set[str]:
    """호출된 이름들. `select(...)` 같은 직접 호출을 찾는다."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                names.add(func.id)
            elif isinstance(func, ast.Attribute):
                names.add(func.attr)
    return names


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    mods: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module)
            mods |= {f"{node.module}.{a.name}" for a in node.names}
    return mods


class TestRepositoryOwnsDbAccess:
    """`select()` 와 ORM 은 `repository/` 안에서 끝난다."""

    @pytest.mark.parametrize("path", _sources(*GOVERNED_SERVICE, *GOVERNED_API))
    def test_no_direct_select(self, path: Path) -> None:
        assert "select" not in _calls(path), (
            f"{path.relative_to(BACK)} 가 select() 를 직접 부른다. "
            "DB 접근은 repository/ 가 맡는다"
        )

    @pytest.mark.parametrize("path", _sources(*GOVERNED_SERVICE, *GOVERNED_API))
    def test_no_orm_import(self, path: Path) -> None:
        """ORM 이 계층 밖으로 나가면 세션 수명과 lazy load 가 도메인으로 번진다."""
        mods = _imported_modules(path)
        assert "core.models" not in mods and "core.models.TrackedRepo" not in mods, (
            f"{path.relative_to(BACK)} 가 ORM 을 임포트한다. "
            "계층을 넘는 것은 service/products/dto.py 의 DTO 뿐이다"
        )


class TestServiceKnowsNothingAboutHttp:
    @pytest.mark.parametrize("path", _sources(*GOVERNED_SERVICE))
    def test_no_fastapi_import(self, path: Path) -> None:
        """service 가 `HTTPException` 을 던지면 CLI·잡에서 그 코드를 못 쓴다.

        도메인 예외로 올리고 라우터가 매핑한다 — `GateError` → `_gate_error()` 가
        이미 같은 형태다.
        """
        mods = _imported_modules(path)
        offenders = {m for m in mods if m.split(".")[0] == "fastapi"}
        assert not offenders, (
            f"{path.relative_to(BACK)} 가 fastapi 를 임포트한다: {sorted(offenders)}"
        )


class TestRepositoryStaysThin:
    @pytest.mark.parametrize("path", _sources(REPOSITORY))
    def test_no_external_io(self, path: Path) -> None:
        """repository 는 DB 만 만진다. git·HTTP·파일은 service 의 일이다."""
        mods = _imported_modules(path)
        banned = {"subprocess", "httpx", "requests", "urllib.request"}
        offenders = mods & banned
        assert not offenders, (
            f"{path.relative_to(BACK)} 가 외부 I/O 를 한다: {sorted(offenders)}"
        )

    @pytest.mark.parametrize("path", _sources(REPOSITORY))
    def test_returns_dto_not_orm(self, path: Path) -> None:
        """반환 타입 주석에 ORM 이 없어야 한다 — 경계에서 변환이 끝난다."""
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                if node.name.startswith("_"):
                    continue  # `_to_dto` 는 경계 변환 자체다
                annotation = ast.unparse(node.returns) if node.returns else ""
                assert "TrackedRepo" not in annotation.replace("TrackedRepoDTO", ""), (
                    f"{path.relative_to(BACK)}::{node.name} 가 ORM 을 반환한다"
                )
