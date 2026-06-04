# Product Log

> 제품 단위 통합 변경 로그. baseline, decision, spec, work, architecture, release 변경 이력을 한 곳에 모은다.

| Date | Type | IDs | Summary | Links |
|---|---|---|---|---|
| 2026-06-01 | baseline-add | MRT-BL-001 | iPhone Mac 리모컨 아이디어 baseline 생성 (Decision.md Project Overview 기반) | [baseline-001](00-baseline/baseline-001-iphone-mac-remote-idea.md) |
| 2026-06-01 | decision-add | MRT-DEC-001~005 | ADR-001~005를 decision으로 이관 (WebSocket, CGWindowList, 앱아이콘, Mac-first, Swifter) | [index](10-decision/README.md) |
| 2026-06-01 | spec-add | MRT-SPEC-001~007 | Spec-01~07을 spec으로 이관, 모두 implemented | [index](20-spec/README.md) |
| 2026-06-01 | work-add | MRT-WORK-001~017 | Work-01~17을 work로 이관 (done 14, todo 3) | [index](30-work/README.md) |
| 2026-06-01 | architecture-add | — | Architecture.md를 system/database/deploy(back·front)로 이관, runbook 2건 포함 | [index](40-architecture/README.md) |
| 2026-06-01 | release-add | MRT-REL-001~002 | Releases.md의 1.0.0/1.0.1을 release note로 이관 | [index](60-release/README.md) |
| 2026-06-01 | status-change | MRT-WORK-014~016 | T1~T3 todo→done (소유자 확인: 실제 배포 1.0.1 및 운영 사용으로 충족) | [index](30-work/README.md) |
| 2026-06-01 | runbook-add | MRT-RB-001~002 | 70-runbook 신설 — DMG 배포 / TestFlight·App Store 심사 절차(원본 doc/runbook/ 분리 복원) | [index](70-runbook/README.md) |
| 2026-06-01 | architecture-change | — | deploy/back·front를 정적 구조만 남기고 절차는 70-runbook으로 이동 (한 곳 원칙) | [deploy](40-architecture/deploy/README.md) |
| 2026-06-01 | runbook-change | — | 70-runbook/assets/ 신설 — App Store 제출 자산 manifest + appstore/{icon,screenshots/{iphone,ipad},preview}. 1024 아이콘 ✅ 복사(알파 없음) | [assets](70-runbook/assets/README.md) |
| 2026-06-01 | runbook-change | — | iPad 스크린샷 N/A→필수 정정 (앱 TARGETED_DEVICE_FAMILY=1,2,7 Universal 확인 — iPhone+iPad 세트) | [assets](70-runbook/assets/README.md) |
| 2026-06-03 | runbook-change | — | iPad를 빌드에서 제거(family=1) → iPad 스크린샷 N/A. iPhone 스크린샷 3장 확보 | [assets](70-runbook/assets/README.md) |
| 2026-06-03 | runbook-change | MRT-RB-001 | 공증(notarization) 절차 추가 — 외부 배포 DMG 더블클릭 실행 (우클릭→열기 제거) | [RB-001](70-runbook/runbook-001-mac-dmg-release.md) |
| 2026-06-04 | runbook-change | MRT-RB-001 | DMG 다운로드 호스팅 — 백엔드 /download 정적 마운트 + repo downloads/에 공증·staple DMG | [RB-001](70-runbook/runbook-001-mac-dmg-release.md) |
| 2026-06-04 | runbook-change | MRT-RB-002 | MacRemote 랜딩(/macremote) app/front 추가 — 지원/마케팅/개인정보 URL 통합, DMG_URL 연결 | [RB-002](70-runbook/runbook-002-ios-testflight-appstore.md) |
