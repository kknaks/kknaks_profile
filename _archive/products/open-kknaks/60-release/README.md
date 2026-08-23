# Release Index

규칙: `rules/product-doc-pipeline.md`

> open-kknaks의 배포 버전별 release note를 관리한다.

## Release 목록

| ID | Version | Title | Status | Released At | Summary | Links |
|---|---|---|---|---|---|---|
| [OKK-REL-002](release-002-open-kknaks-2-0-2.md) | 2.0.2 | Claude/Codex provider execution release | released | 2026-06-01 | Claude/Codex provider 기반 headless task queue 배포 | `OKK-WORK-001`~`OKK-WORK-005` |

## 배포 상태

| Current Version | Status | Notes |
|---|---|---|
| 2.0.2 | released | PyPI publish와 GitHub Release 완료. 배포판 examples Docker에서 Claude/Codex E2E 검증 완료. |

## 검증 기준

- release note는 `release-*.md` 파일로 작성한다.
- release note frontmatter의 `type`은 `release`다.
- release note에는 `version`, `released_at`, `summary`, `details`가 있어야 한다.
- 관련 spec/work/release 링크는 frontmatter `links`에 Obsidian wikilink로 둔다.
