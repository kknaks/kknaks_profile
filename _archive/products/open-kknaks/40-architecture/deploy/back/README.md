# Package / PyPI Deploy

규칙: `rules/product-doc-pipeline.md`

## Runtime

| Item | Value |
|---|---|
| Language | Python `>=3.10` |
| Package type | Python library + CLI scripts |
| Build backend | `hatchling.build` |
| Version source | `hatch-vcs` git tag 기반 dynamic version |
| Deploy environment | GitHub Actions `ubuntu-latest` |
| Workflow | `.github/workflows/release.yml` |
| Trigger | `v*` tag push |
| Python version | `3.12` in workflow |
| Distribution | sdist + wheel |
| Production registry | PyPI |
| Release artifact | GitHub Release assets |

## Package Metadata

| Item | Value |
|---|---|
| Package name | `open-kknaks` |
| Description | `PTY-based task queue library for Claude Code CLI` |
| License | MIT |
| Readme | `README.md` |
| Author | `kknaks` |
| Main package | `open_kknaks` |

## Scripts

| Script | Entry |
|---|---|
| `open-kknaks` | `open_kknaks.cli.main:main` |
| `open-kknaks-mcp` | `open_kknaks.mcp:run` |

## Dependencies

| Type | Values |
|---|---|
| Required | `pydantic>=2.7`, `structlog>=24.1`, `redis>=5.0`, `mcp>=1.6`, `typer>=0.12` |
| Dev extra | `pytest`, `pytest-asyncio`, `fakeredis[lua]`, `ruff`, `mypy`, `coverage` |

## Build Scope

| Target | Include | Exclude |
|---|---|---|
| sdist | package source and package metadata | `examples/`, `tests/`, `docs/` |
| wheel | `open_kknaks` package | `examples/`, `tests/`, `docs/` |

## Environment Variables

| Name | Required | Description |
|---|---|---|
| `PYPI_API_TOKEN` | yes | GitHub Actions가 PyPI에 publish할 때 사용하는 repository secret |
| `GITHUB_TOKEN` | yes | GitHub Release 생성과 artifact upload에 사용하는 Actions 기본 token |

문서에는 token 값을 기록하지 않는다.

## CI Gates

GitHub Actions workflow가 release 전에 아래 gate를 수행한다.

| Gate | Scope |
|---|---|
| Lint | `open_kknaks/`, `tests/` |
| Format check | `open_kknaks/`, `tests/` |
| Type check | `open_kknaks/` |
| Test | `tests/`, e2e 제외 |
| Build package | sdist + wheel |
| Publish | PyPI |
| Release | GitHub Release 생성 및 artifact upload |

## Deploy Steps

1. `CHANGELOG.md`에 release note를 정리한다.
2. `pyproject.toml`의 metadata, scripts, build exclude 설정을 확인한다.
3. release version에 해당하는 git tag를 만든다.
4. `v*` tag를 remote에 push한다.
5. GitHub Actions `PyPI Release` workflow 실행 결과를 확인한다.
6. workflow가 PyPI publish와 GitHub Release 생성을 완료했는지 확인한다.
7. 새 환경에서 PyPI package를 설치하고 import/CLI/MCP schema 생성 경로를 확인한다.

```bash
pip install open-kknaks
python -c "import open_kknaks; print(open_kknaks.__version__)"
open-kknaks --help
python -c "from open_kknaks.mcp.server import create_server; create_server(); print('mcp schema ok')"
```

## Release Gate

- [ ] release tag가 `v*` 형식임
- [ ] GitHub Actions `PyPI Release` workflow 성공
- [ ] workflow에서 lint/type/test/build gate 성공
- [ ] PyPI publish 성공
- [ ] GitHub Release 생성 성공
- [ ] GitHub Release에 sdist + wheel artifact upload 성공
- [ ] PyPI 설치 후 `open-kknaks --help` 성공
- [ ] PyPI 설치 후 MCP schema server 생성 경로 성공

## Rollback

- PyPI에 올라간 release artifact는 같은 version으로 덮어쓰지 않는다.
- 잘못 배포된 version은 yanked release로 처리하고, 수정 version을 새 tag/version으로 재배포한다.
- workflow 실패 시 같은 tag를 재사용하지 않고 원인을 수정한 뒤 새 tag/version으로 재배포한다.

## Open Questions

- `open-kknaks-mcp` entrypoint의 smoke test 방식을 별도 CLI option으로 만들지 결정이 필요하다.
