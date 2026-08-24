# Release Index

규칙: `para/projects/project.md`

> 제품의 배포 버전별 release note를 관리한다. 최신 버전이 위.

## Release 목록

| ID | Version | Title | Status | Released At | Summary |
|---|---|---|---|---|---|
| [MRT-REL-003](release-003-deskdeck-appstore.md) | 1.0.1 | DeskDeck App Store 출시 | released | 2026-06-10 | 5.2.5 대응 MacRemote→DeskDeck 개명, App Store 첫 출시(build 5). 기능 변경 없음 |
| [MRT-REL-002](release-002-v1-0-1.md) | 1.0.1 | mac-remote 1.0.1 | released | 2026-05-26 | 단말 격리 Wi-Fi 페어링/재연결/아이콘 + stale IP 수정 |
| [MRT-REL-001](release-001-v1-0-0.md) | 1.0.0 | mac-remote 1.0.0 | released | 2026-05-24 | iPhone 리모컨 + Mac 헬퍼 초기 릴리즈 |

## 배포 상태

| Current Version | Status | Notes |
|---|---|---|
| 1.0.1 (DeskDeck) | released | **App Store 출시** (build 5, https://apps.apple.com/app/id6772868137), Mac DMG `DeskDeckHelper-1.0.1.dmg` (공증) |

## 검증 기준

- release note는 `release-*.md` 파일로 작성한다.
- frontmatter `type`은 `release`, `version`/`released_at`/`summary`/`details` 필수.
- 관련 spec/work/release 링크는 frontmatter `links`에 wikilink로 둔다.
