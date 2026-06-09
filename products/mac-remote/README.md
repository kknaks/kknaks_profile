# Product Map — mac-remote

규칙: `rules/product-doc-pipeline.md`

iPhone을 리모컨으로 써서 Mac의 창 전환과 단축키 매크로를 전송하는 제품. **1.0.1 배포 완료, 운영 사용 중.** 모든 work 완료. **App Store 심사 1차 거절(5.2.5 IP, 2026-06-08)** → 앱 개명 `MacRemote`→`DeskDeck` + 새 빌드로 재제출 진행 중(절차: `70-runbook/runbook-002` §4).

> 제품 전체 지도. 상세는 각 단계 문서에 두고, 여기에는 현재 상태와 진입점만 둔다.
> 코드는 별도 레포 `mac-remote`(Swift)에 있고, 이 디렉토리는 제품 문서 SoT다.

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | 1건 (accepted) | — |
| Decision | 5건 (ADR-001~005, 모두 accepted) | — |
| Spec | 7건 (모두 implemented) | — |
| Work | 17건 (모두 done) | — |
| Architecture | system / database(DB 없음) / deploy(back·front 구조만) | — |
| Release | 1.0.0, 1.0.1 (released, 운영 중) | App Store 심사 통과·출시 후 REL-003 작성 |
| Runbook | DMG 배포(RB-001), TestFlight/App Store 심사(RB-002) | App Store 심사는 RB-002 따라 진행 |
| Assets | `70-runbook/assets/` — 1024 아이콘 ✅, 스크린샷 수집 중 | iPhone+iPad 스크린샷 세트 캡처 (Universal 타겟) |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | `00-baseline/README.md` |
| 10-decision | `10-decision/README.md` |
| 20-spec | `20-spec/README.md` |
| 30-work | `30-work/README.md` |
| 40-architecture | `40-architecture/README.md` |
| 60-release | `60-release/README.md` |
| 70-runbook | `70-runbook/README.md` |

## 최근 로그

전체 이력은 `log.md`.

- 2026-06-01 — `mac-remote/doc`에서 제품 문서 전체를 이 구조로 마이그레이션 (baseline 1, decision 5, spec 7, work 17, architecture, release 2)
