# Runbook Index

규칙: `rules/product-doc-pipeline.md`

> mac-remote의 반복 실행 절차. 배포 *구조/환경*은 `40-architecture/deploy/`, *실행 절차*는 여기.
> 원본: `mac-remote/doc/runbook/`.

## Runbook 목록

| ID | Title | Area | Status | File |
|---|---|---|---|---|
| MRT-RB-001 | Mac 헬퍼 DMG 배포 | deploy | active | [runbook-001-mac-dmg-release.md](v1_0_1-runbook-001-mac-dmg-release.md) |
| MRT-RB-002 | iOS TestFlight / App Store 심사 | deploy | active | [runbook-002-ios-testflight-appstore.md](v1_0_1-runbook-002-ios-testflight-appstore.md) |

## 자산 (assets)

스토어 제출용 바이너리(스크린샷·아이콘·영상)는 [assets/](assets/v1_0_1-README.md)에 모은다. `products/`에서 바이너리를 두는 유일한 자리.

## 원칙

- 절차(명령·단계·검증·트러블슈팅)는 여기 한 곳에만 둔다.
- 배포 환경/타겟은 `40-architecture/deploy/`에 두고 여기서는 링크만 한다.
- 바이너리 자산은 `assets/`에, 그 상태는 `assets/README.md` manifest로 추적한다.
- 일회성 실행 로그는 두지 않는다.
