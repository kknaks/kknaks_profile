# Deploy Architecture

규칙: `para/projects/project.md`

> `open-kknaks`의 GitHub Actions 기반 package build, PyPI publish, 설치 검증 절차를 관리한다.

## Environments

| Environment | URL/Target | Purpose | Notes |
|---|---|---|---|
| GitHub Actions | `.github/workflows/release.yml` | release build / publish 실행 환경 | tag push로 실행 |
| PyPI | `pypi.org/project/open-kknaks` | production package registry | `PYPI_API_TOKEN` secret 사용 |
| GitHub Releases | repo release page | 배포 artifact 보관 | tag 기준 release 생성 |

## Deploy Map

| Area | Index |
|---|---|
| Package / PyPI | `back/README.md` |

## Release Flow

1. package metadata와 changelog를 확인한다.
2. release tag `v*`를 push한다.
3. GitHub Actions `PyPI Release` workflow가 lint/type/test/build/publish를 수행한다.
4. workflow가 PyPI publish 후 GitHub Release를 생성하고 artifact를 업로드한다.
5. PyPI 설치 기준으로 CLI/MCP/import 동작을 확인한다.

## Source

| Source | Path |
|---|---|
| GitHub Actions release workflow | `/Users/kknaks/git/library/claude_code_pty/open_kknaks/.github/workflows/release.yml` |
| Sprint 배포 계획 | `/Users/kknaks/git/library/claude_code_pty/open_kknaks/docs/legacy/sprint/S4-D1.md` |
| PRD PyPI 배포 | `/Users/kknaks/git/library/claude_code_pty/open_kknaks/docs/legacy/PRD.md` §12 |
| 개발 명령 | `/Users/kknaks/git/library/claude_code_pty/open_kknaks/CLAUDE.md` |
| Package config | `/Users/kknaks/git/library/claude_code_pty/open_kknaks/pyproject.toml` |
