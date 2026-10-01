---
sot: here
status: active
---

# SC Rank

네이버 키워드 순위(블로그 · 플레이스)를 조회해 엑셀로 저장하는 **데스크톱 프로그램**.
2026-09-09 웹 PoC(`reference/2026-09-09-sc-prototype`)를 Tauri + Rust 로 옮긴다. 서버는 없다.

## 코드 위치

| 항목 | 경로 |
|---|---|
| 웹 PoC (원본, 읽기 전용) | `reference/2026-09-09-sc-prototype/` (`server/` · `src/`) |
| 데스크톱 앱 | `https://github.com/kknaksss/sc-rank`(공개) · 로컬 `/Users/kknaks/git/toy_pr2/sc-rank` (DEC-001 D-07, 10-01 개정) |

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | raw 1건 | — |
| Decision | accepted 1건 (결정 14) | — |
| Spec | SPEC-001 v0.2.3 draft | — |
| Work | WORK-001 P1~P5 done · P6 레포 분리 정리 | Windows 빌드(A-9) |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | [입력](00-baseline/README.md) |
| 10-decision | [결정](10-decision/README.md) |
| 20-spec | [스펙](20-spec/README.md) |
| 30-work | [구현 계획](30-work/README.md) |

## 최근 로그

- 2026-10-01: 코드를 `kknaksss/sc-rank` 로 분리 — Windows PC 빌드에 clone 할 레포가 필요. 이식 P1~P5 완료(test 39 · 헤드리스 Edge 결과 PoC 와 일치). [전체 이력](log.md)
- 2026-09-30: DEC-001 미결 다섯을 기본값으로 닫고(NSIS·무서명·Windows PC 빌드·Edge→Chrome·화면 재사용) SPEC-001·WORK-001 작성. 파워링크는 화면이 부르지 않아 범위 밖. [전체 이력](log.md)
- 2026-09-30: 제품 착수 — 웹 PoC 를 Tauri + Rust 데스크톱 프로그램으로 옮기기로 결정. 서버 없음 · 운영 Windows. [전체 이력](log.md)
