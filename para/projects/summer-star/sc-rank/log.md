# Product Log

> 제품 단위 통합 변경 로그. baseline, decision, spec, work 변경 이력을 한 곳에 모은다.

| Date | Entry | Links |
|---|---|---|
| 2026-09-30 | 제품 착수. 웹 PoC 관측을 BASE-001 로, 사용자 대화에서 닫은 방향(Tauri + Rust · 서버 없음 · 운영 Windows · 시스템 Edge 조종 · 기능 3종 그대로 · 코드는 PoC 아래 `desktop/`)을 DEC-001 로 기록. 코드 미착수 | [입력](00-baseline/baseline-001-desktop-app.md) · [결정](10-decision/decision-001-desktop-app.md) |
| 2026-09-30 | 사용자 「쭈욱 진행해」 — DEC-001 미결 다섯을 코디 기본값으로 닫음(D-09~D-14) · accepted. 범위를 **화면이 쓰는 기능 둘(블로그·플레이스)** 로 정정 — 파워링크 API 는 PoC 화면이 부르지 않는다. SPEC-001 v0.1.0(명령 셋 · 브라우저 · 이식 규칙 전수 · 인수조건 9) · WORK-001(P1~P5 직렬) 작성. 코드 미착수 | [결정](10-decision/decision-001-desktop-app.md) · [스펙](20-spec/spec-001-desktop-app.md) · [계획](30-work/work-001-desktop-port.md) |
| 2026-09-30 | 문서 검수 FAIL 6 · WARN 11 반영 → SPEC-001 **v0.2.0**. §4 를 「정본 함수 본문 전체」로 바꾸고 틀리기 쉬운 값을 표로, 오류 문구 한글 규칙·폴백, 명령 Err 표(블로그 입력 검증은 정상 반환), 평평한 invoke 인자·camelCase·null, UA 규칙(실제 UA 에서 Headless 만 제거 — 의도된 변경), 화면 변경 **셋**(연결 모듈·저장·링크 가로채기, DEC D-14 보강), 180초 상한 화면 유지, smoke 예제로 실수집 수단 고정, 이미지 모드 실수집 추가. WORK-001 Phase 끝 조건에 A-3 | [검수](../../../../orchestration/work/sc-rank-desktop/review-doc-report.md) · [스펙](20-spec/spec-001-desktop-app.md) |
| 2026-10-01 | WORK-001 P1~P5 구현 완료(desktop 워커) — cargo test 38 · clippy 0 · 헤드리스 Edge 수집이 같은 시각 PoC 와 완전 일치(69/53/88/광고18) · 사용자 macOS 조회(플레이스 3·블로그 19)·엑셀 저장 확인. 코드 검수 FAIL 0 · WARN 6 — W-1(루프 안 프레임 실패 문구 PoC 로)·W-2(rustls ring 전환, Windows NASM 제거)·W-4(잔여 프로필 정리 범위 축소) 수정 발주, W-5·W-6 은 SPEC-001 **v0.2.1** §7 「이식 중 확정한 차이」로 기록 | [스펙](20-spec/spec-001-desktop-app.md) · [계획](30-work/work-001-desktop-port.md) |
| 2026-10-01 | **코드 레포 분리** — 사용자 「윈도우 빌드 하려면 깃 레포 필요」. `kknaksss/sc-rank`(비공개) 생성, `desktop/` 을 subtree split 으로 이력째 이전(20ef3b7). DEC-001 D-07 개정 · SPEC-001 v0.2.2(위치·구성) · WORK-001 P6(새 레포에서 깨지는 PoC 원본 참조 정리). 코드 PR #65 는 닫음 | [결정](10-decision/decision-001-desktop-app.md) · [스펙](20-spec/spec-001-desktop-app.md) |
| 2026-10-01 | **Windows 설치 파일을 GitHub Actions 에서** — 사용자 「exe 빌드 깃에서 하자고」. DEC-001 D-11 개정(CI 없음 → `windows-build` 워크플로), SPEC-001 v0.2.3(배포물·A-9 문구). PR 마다 Windows 에서 `cargo test` + NSIS 빌드 → 산출물, `v*` 태그 → Release | [결정](10-decision/decision-001-desktop-app.md) · [코드](https://github.com/kknaksss/sc-rank/pull/1) |
