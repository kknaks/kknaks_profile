# Release Index

규칙: `rules/product-doc-pipeline.md`

> 제품의 배포 버전별 release note를 관리한다. 최신 버전이 위.

## Release 목록

| ID | Version | Title | Status | Released At | Summary |
|---|---|---|---|---|---|
| [MRT-REL-002](v1_0_1-release-002-v1-0-1.md) | 1.0.1 | mac-remote 1.0.1 | released | 2026-05-26 | 단말 격리 Wi-Fi 페어링/재연결/아이콘 + stale IP 수정 |
| [MRT-REL-001](v1_0_1-release-001-v1-0-0.md) | 1.0.0 | mac-remote 1.0.0 | released | 2026-05-24 | iPhone 리모컨 + Mac 헬퍼 초기 릴리즈 |

## 배포 상태

| Current Version | Status | Notes |
|---|---|---|
| 1.0.1 | released | Mac DMG (Developer ID 사인), iOS TestFlight 빌드 3 |

## 검증 기준

- release note는 `release-*.md` 파일로 작성한다.
- frontmatter `type`은 `release`, `version`/`released_at`/`summary`/`details` 필수.
- 관련 spec/work/release 링크는 frontmatter `links`에 wikilink로 둔다.
