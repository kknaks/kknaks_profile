---
type: decision
id: DEC-001
title: "Tauri + Rust 데스크톱 프로그램, 서버 없음"
status: accepted
product: sc-rank
created_at: 2026-09-30
updated_at: 2026-09-30
tags:
  - product/sc-rank
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-001-desktop-app|BASE-001]]"
  decisions: []
  specs:
    - "[[spec-001-desktop-app|SPEC-001]]"
  works:
    - "[[work-001-desktop-port|WORK-001]]"
  releases: []
  related:
    - "[[decision-005-tauri-wrapper|strong-hajin DEC-005]]"
up: []
---

# Tauri + Rust 데스크톱 프로그램, 서버 없음

> 기능 계약은 `20-spec/`, 작업 순서는 `30-work/` 가 갖는다. 이 문서는 무엇을 정했고
> 무엇이 열려 있는지만 갖는다.

## Context

웹 PoC(BASE-001 입력 2)는 로컬 한 사람이 쓰는데도 백엔드·프론트 두 프로세스와 Node 런타임을
요구한다. 운영 환경은 Windows 다(사용자 원문).

## Options

| Option | Description | 판단 |
|---|---|---|
| A | **Tauri + Rust 로 다시 짠다.** 화면은 React 재사용, 수집·파싱·엑셀은 Rust | **채택** |
| B | Tauri + Node 사이드카로 지금 서버 코드를 동봉 | 기각 — Node·Chromium·OS별 sharp 바이너리 동봉으로 배포가 무겁고 지저분 |
| C | Electron 으로 이식 | 보류 — 이식은 가장 쉽지만 무겁다. A 의 브라우저 자동화 포팅이 막힐 때만 다시 연다 |
| D | 웹 그대로 두고 서버에 배포 | 기각 — 사용자 1명·DB 없음이라 서버가 할 일이 없다 |

## Decision

| ID | 결정 | 근거 |
|---|---|---|
| D-01 | 웹이 아니라 **데스크톱 프로그램**으로 만든다. Tauri + Rust | 사용자 원문 「프로그램 형식」 「타우리 러스트로 할거야」 |
| D-02 | **서버 없음.** 실행 파일 하나 · 프로세스 하나 · HTTP 포트 없음. 화면↔로직은 Tauri `invoke` 로 앱 안에서 직접 호출한다 | 사용자 원문 「서버 필요 없잖아 로컬에서만 구동해서」 |
| D-03 | 결과는 앱 메모리에만 두고 사용자가 **저장 대화상자로 `.xlsx`** 를 쓴다. DB·이력 저장 없음 | 사용자 원문 「엑셀로 저장 되면 되는거」 · PoC 규칙 계승 |
| D-04 | 운영 환경은 **Windows**. macOS 는 개발 환경. Windows 실측은 macOS 통과로 대신하지 않는다 | 사용자 원문 「운영 환경은 윈도우」 |
| D-05 | 브라우저 자동화(플레이스·블로그)는 **PC 에 설치된 Edge 를 CDP 로 조종**한다. Chromium 을 동봉하지 않는다. 페이지 안에서 도는 JS(`place-dom.mjs`)는 재사용한다 | 코디 제안, 사용자 동의(2026-09-30). Windows 10/11 에 Edge 기본 탑재 |
| D-06 | 첫 범위는 **PoC 화면에서 실제로 쓰는 기능 둘(블로그 상위 노출 · 플레이스 순위 조회) + 엑셀 저장**을 그대로 옮긴다. 판정·간격·동시 1건 규칙 포함. 새 기능 없음. 파워링크(`/api/check`)는 PoC 화면이 부르지 않는 API 라 이번 범위에서 뺀다 | 사용자 확인(2026-09-30). 파워링크 제외는 코디 판정 — 화면 없이 옮기면 새 UI 를 만들어야 한다(PoC `src/main.jsx` 는 `/api/blog/check`·`/api/place/check`·`/api/export` 만 호출) |
| D-07 | 코드는 **별도 레포 없이** `reference/2026-09-09-sc-prototype/desktop/` 에 둔다. 웹 PoC(`server/`·`src/`)는 옮기는 원본으로 남기고 수정하지 않는다 | 사용자 원문 「코드는 레퍼런스 프로토타입 아래에 만들자 일단」 |
| D-08 | 제품 문서는 `para/projects/summer-star/sc-rank/` | 사용자 확인(2026-09-30) |

## Scope

- In: 기능 셋 이식, 단일 실행 파일, Windows 설치·실행.
- Out: 서버·DB·계정·이력, 새 조회 기능, 자동 업데이트.

## Closed Questions

2026-09-30 사용자 「쭈욱 진행해」 — 미결 다섯은 코디 기본값으로 닫는다. 사용자가 뒤집으면 해당 D 만 고친다.

| ID | 결정 | 근거 |
|---|---|---|
| D-09 (OQ-101) | 배포는 **NSIS 설치 파일(`*-setup.exe`) 하나**. 전달은 사용자가 파일로 직접. 자동 업데이트 없음 | Tauri 기본 번들 중 WebView2 부트스트랩을 포함하는 형식. 사내 소수 배포 |
| D-10 (OQ-102) | 코드 서명 안 함. 첫 실행 SmartScreen 경고를 감수한다 | 소수 사내 배포. 인증서 비용 대비 이득 없음 |
| D-11 (OQ-103) | Windows 빌드는 **Windows PC 에서 직접**(절차는 `desktop/README.md` 에 고정). CI 는 두지 않는다 — 코드가 프로필 레포 안이다. macOS 에서는 개발·단위 테스트·실수집 확인까지 | D-07 과 정합. macOS→Windows 크로스 빌드는 Tauri 공식 지원이 실험적 |
| D-12 (OQ-104) | 브라우저 탐색 순서: **Edge → Chrome → 없으면 조회 실패 + 설치 안내 문구**. 조회 전체가 아니라 브라우저가 필요한 조회만 실패한다 | D-05 · 사용자 PC 에 Chrome 만 있는 경우 대비 |
| D-13 (OQ-105) | macOS 는 **개발용만**. macOS 설치 파일은 만들지 않는다 | D-04 운영 Windows |
| D-14 (OQ-106) | PoC React 화면을 **그대로 재사용**한다. 바뀌는 곳은 호출부(`fetch` → `invoke`), 저장(브라우저 다운로드 → 저장 대화상자), 결과 링크 열기(OS 브라우저)뿐 — 링크는 웹뷰가 새 창을 OS 로 넘기지 않아 생긴 필연적 변경(문서 검수 F-5) | D-06 새 기능 없음 · 이식 비용 최소 |

## Resulting Spec

SPEC-001(앱 경계 · 명령 계약 · 수집 규칙 이식) · WORK-001(단계).
