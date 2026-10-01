---
type: work
id: WORK-001
title: "웹 PoC → Tauri 데스크톱 앱 이식"
status: in-progress
product: sc-rank
created_at: 2026-09-30
updated_at: 2026-09-30
tags:
  - product/sc-rank
  - doc/work
links:
  decisions:
    - "[[decision-001-desktop-app|DEC-001]]"
  specs:
    - "[[spec-001-desktop-app|SPEC-001]]"
---

# 웹 PoC → Tauri 데스크톱 앱 이식

SPEC-001 을 한 워커(desktop)가 **직렬로** 세운다. P1~P5 는 `reference/2026-09-09-sc-prototype/desktop/` 에서,
P6 부터는 코드 레포 `kknaksss/sc-rank` 에서(DEC-001 D-07 개정).

## Phase

| Phase | 할 것 | 끝 조건 |
|---|---|---|
| P1 뼈대 | Tauri 2 앱 생성(React + Vite, PoC `index.html`(무변경)·`src/` 사본). Rust 크레이트와 §2 명령 셋의 빈 구현. 앱 이름·식별자·창 제목·`bundle.targets=["nsis"]`·dev 포트 13100(SPEC §1). 로그 플러그인 | `npm run tauri dev` 로 PoC 화면이 뜬다(창 제목 `SC Rank`) · `cargo check` · `npm run build` |
| P2 순수 로직 | 플레이스 판정 · 블로그 목록 파싱·키워드 일치 · 이미지 해시(전처리 포함) · 엑셀 · 오류 문구 규칙(SPEC §4) · 브라우저 탐색 함수(후보 목록 인자). PoC 단위 테스트 이식(A-1·A-2·A-7) | `cargo test` 초록 · A-3 |
| P3 브라우저 | CDP 기동·재사용·종료 정리 · 플레이스 수집 · 블로그 스크롤 수집 · 페이지 안 JS 문자열 주입 · UA 규칙 · 동시 1건·간격 가드 · `examples/smoke.rs` | A-4·A-5 smoke 출력 · A-3 |
| P4 화면 연결 | SPEC §5 세 곳(`bridge.js` · 저장 대화상자 · 링크 가로채기) · 명령 Err/반환 모양(SPEC §2) | A-3 · 워커가 앱을 띄워 조회 1건 → 저장한 xlsx 경로와 앱 로그 발췌를 리포트에. A-8 워커 1회 |
| P5 Windows 빌드 절차 | `README.md`(= DEC D-11 의 RUNBOOK): macOS 개발 · Windows 빌드 사전 요건·명령·산출물 위치 · smoke 사용법. `cfg(windows)` 경로 확인 | README · 가능하면 `cargo check --target x86_64-pc-windows-msvc` (못 하면 사유 보고) |
| P6 레포 분리 정리 | 새 레포에서 깨지는 곳 정리 — PoC 원본을 읽던 동일성 테스트(`collect_offline.rs`)는 PoC 원본 사본 `poc/` 를 읽게, README 경로·설치 절차를 레포 루트 기준으로 | `cargo test`·clippy·build 를 새 레포 clone 에서 통과 |

**P3 가 가장 위험하다.** 막히면(CDP 로 `searchIframe` 실행 맥락을 못 잡음, 응답 대기가 안 됨 등)
우회로를 만들지 말고 즉시 코디에게 보고한다. 대안(DEC-001 Option C)을 여는 것은 사용자 결정이다.

## 크레이트 방향 (워커 재량, 바꾸면 보고)

HTTP `reqwest`(rustls) · HTML `scraper` · CDP `chromiumoxide` · 엑셀 `rust_xlsxwriter` ·
이미지 `image` · 저장 대화상자 `tauri-plugin-dialog` · 링크 열기 `tauri-plugin-opener`.
OpenSSL 에 기대는 크레이트는 쓰지 않는다(Windows 빌드 부담).

## 검증 분담

| 누가 | 무엇 |
|---|---|
| 워커 | `cargo test` · `cargo clippy --all-targets -- -D warnings` · `npm run build` · macOS 실수집 1회씩 |
| 리뷰어 | SPEC §4 전수 대조(PoC 와 판정·문구·제한값이 다른 곳) · 범위 이탈 · 「조용히 통과하는 자리」 |
| 코디 | 관문 명령 직접 1회 · A-4·A-8 실측 |
| 사용자 | A-6 화면 E2E · A-9 Windows 설치·실행 |

## Status

| Phase | 상태 |
|---|---|
| P1~P5 | done (2026-10-01) — 검수 WARN 6 중 W-1·2·4 수정 |
| P6 | done — kknaksss/sc-rank#1 (fresh clone test 39) |
| A-6 링크 · A-9 Windows | 사용자 |
