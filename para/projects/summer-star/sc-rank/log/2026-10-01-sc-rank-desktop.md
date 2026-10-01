
# 작업 요약 — sc-rank-desktop (sc-rank)

기간: `2026-09-30` ~ `2026-10-01`
결과: 머지 완료 — 코드 kknaksss/sc-rank `main`(20ef3b7 · #1 4c6d570), 문서 kknaks_profile #64(4d72d83). Windows 설치 파일 Actions 빌드 성공. **Windows 실기 설치·실행(A-9)은 미확인.**

## 1. 무엇을 했나

SC 마케팅용 네이버 순위 조회 웹 PoC(Express + React, 포트 둘, Node 필요)를 서버 없는 데스크톱 프로그램으로 옮겼다.
Tauri 2 + Rust 로 다시 짜고, 화면은 PoC React 를 그대로 쓰며, 수집은 PC 에 설치된 Edge 를 헤드리스로 띄워 CDP 로 조종한다.
문서(DEC-001 결정 14건 · SPEC-001 v0.2.3 · WORK-001 P1~P6)를 먼저 닫고 워커 하나가 직렬로 구현했다.
도중에 코드를 프로필 레포 안(`reference/.../desktop/`)에서 별도 레포 `kknaksss/sc-rank` 로 이력째 옮겼고,
Windows 설치 파일은 GitHub Actions 가 만든다.

## 2. 적용한 기술·개념

- **Tauri 2 + Rust 로 웹 PoC 를 「서버 없는」 데스크톱 앱으로** — Express 가 하던 화면↔로직 연결을 Tauri `invoke` 로 바꿨다
  - 왜 이걸 골랐나: 사용자 1명·DB 없음·결과는 파일이라 서버가 할 일이 없었다. Node 사이드카는 Node·Chromium·OS별 sharp 바이너리 동봉으로 배포가 지저분하고, Electron 은 무겁다. 반환 JSON 키를 PoC HTTP 응답과 똑같이(camelCase · `null` 유지) 맞춰 화면 코드는 호출부·저장·링크 세 곳만 바뀌었다
  - 무엇이 어려웠나: `invoke` 는 Err 를 문자열로 reject 해서 PoC 의 `error.message` 가 비고, abort 신호가 없어 180초 상한이 사라진다 — 문서 검수가 잡았다. 연결 모듈 `bridge.js` 가 문자열을 `Error` 로 감싸고 `Promise.race` 로 상한을 유지한다. 웹뷰는 `target="_blank"` 를 OS 브라우저로 넘기지 않아 링크 가로채기가 「필연적인 세 번째 화면 변경」이 됐다
  - 근거: SPEC-001 §2·§5 · `review-doc-report.md` F-3·F-5 · kknaksss/sc-rank `src/bridge.js`

- **Playwright 없이 CDP 로 시스템 Edge 조종** — Chromium 동봉 대신 Windows 기본 탑재 Edge 를 헤드리스로
  - 왜 이걸 골랐나: Rust 에는 Playwright 급 라이브러리가 없다. Edge 는 Chromium 엔진이라 `--headless` + CDP 가 그대로 된다. 설치 파일이 수백 MB → 5.8MB
  - 무엇이 어려웠나: (1) 개발 Mac 에 Edge·Chrome 이 없어 실수집을 못 했다 — Whale·Playwright 캐시 Chromium 우회를 막고 Edge 를 설치했다. (2) 블로그 추가 결과 응답 대기에서 첫 매칭이 CORS 사전 요청(OPTIONS 204, 본문 없음)이었다 — Playwright 의 response 이벤트에는 사전 요청이 없다는 의미를 옮겨 `Preflight` 를 걸렀다. (3) PoC 가 `evaluate` 로 넘기던 페이지 안 JS 는 **문자열 그대로 주입**하고, 그게 PoC 원본과 같은지 테스트로 고정했다(분리 후엔 `poc/` 사본과 비교)
  - 근거: `report-desktop-p3.md` · SPEC-001 §3·§4 · `src-tauri/tests/collect_offline.rs`

- **이식 검증을 「같은 시각 대조」로** — 실수집 결과가 PoC 와 다를 때 원인을 코드가 아니라 실측으로 갈랐다
  - 왜 이걸 골랐나: 워커 smoke 에서 플레이스 광고가 0건(PoC 기록 18건)이었다. 후보는 UA 변경 · 헤드리스 Edge 판별 · 광고 편성 변화. 코드를 의심하기 전에 PoC(Playwright Chromium)와 앱(헤드리스 Edge)을 연달아 1회씩 돌렸다
  - 무엇이 어려웠나: 결과는 69/53/88/광고18 로 **완전히 같았다** — 그 시점 네이버 편성 차이였다. 워커가 본 순위 53 이 광고 제외 순위와 같았던 것도 그 증거. 같은 방식으로 이미지 해시는 sharp 와 비트 단위 동일(거리 0)을 따로 쟀다
  - 근거: `report-desktop-p3.md` 「사용자 확인 사항」 · `report-desktop-p1-p2.md` 해시 표

- **rustls 암호 제공자 선택이 Windows 빌드 조건을 바꾼다** — `aws-lc-rs` → `ring`
  - 왜 이걸 골랐나: reqwest `rustls` 기능의 기본 제공자 `aws-lc-sys` 는 Windows 에서 NASM(또는 셸 한정 환경변수)을 요구하고, macOS 에서 Windows 타깃 `cargo check` 도 막았다. `ring` 은 어셈블리를 미리 빌드된 객체로 실어 MSVC 만 있으면 된다
  - 무엇이 어려웠나: `ring` 도 C 헤더가 필요해 macOS 에서 Windows 타깃 check 는 여전히 막혔다 — C 컴파일러를 빈 파일만 만드는 스크립트로 바꿔 Rust 타입 검사·clippy 만 통과시켰다. 진짜 확인은 Actions 의 `windows-latest` `cargo test` 가 처음 했다
  - 근거: `review-code-report.md` W-2·W-3 · `report-desktop-fix-review.md`

- **subtree split 으로 모노레포 폴더를 이력째 새 레포로** — `git subtree split --prefix=…/desktop`
  - 왜 이걸 골랐나: Windows PC·CI 에서 clone 할 레포가 필요했다. 파일 복사 대신 split 으로 커밋을 옮기면 트리 해시가 그대로라 「옛 커밋 = 새 레포 첫 커밋」을 해시로 증명할 수 있다(`5e74ea9…` 동일) — 옛 워크트리를 지울 근거가 됐다
  - 무엇이 어려웠나: 옛 자리에서 `../server` 로 PoC 를 읽던 테스트가 새 레포에서 깨졌다 → `poc/` 에 바이트 그대로 사본. 「새로 clone 해서 테스트」로 레포 밖 의존이 없음을 확인
  - 근거: kknaksss/sc-rank `20ef3b7` · #1 · DEC-001 D-07 개정

## 3. 막혔던 것 / 사고

- 문서 검수 1회차 FAIL 6 — SPEC §4 를 「옮길 대상의 전수」 표로 썼더니 표가 PoC 의 제한값·문구를 빠뜨렸고, 그 표가 오히려 「목록 밖은 안 옮겨도 된다」는 근거가 될 뻔했다 → 「정본 함수 본문 전체를 옮긴다, 표는 틀리기 쉬운 것」으로 바꿨다. 목록이 아니라 정본을 가리킨다
- 코디 핸들이 두 번 stale — env `ORCA_TERMINAL_HANDLE` 이 시작부터 죽은 값이었고, 10-01 재연결 때 또 바뀌었다. `terminal list` 에서 세션 제목으로 찾아 덮어쓰고 dispatch 에 export 로 넘겼다. 워커가 「preamble 핸들이 stale 이라 이 터미널로 보냄」으로 알려 와서 잡았다
- 새 레포 워크트리에 띄운 워커가 Claude 「폴더 신뢰」 창에서 주입된 발주문을 받아 종료됐다 → 다시 띄워 신뢰를 고르고, 이미 dispatched 인 태스크는 재발주가 안 돼 브리프 경로를 직접 주입했다(고아 task `task_7ecdd98b6d5f`)
- 워커의 GUI 확인 시도(System Events·창 캡처·손쉬운 사용)가 macOS 의 「Orca 가 다른 앱 데이터에 접근」 대화상자를 반복해서 띄웠다 → 이후 GUI 자동화 금지, 화면 확인은 사용자 몫으로
- 사용자가 묻기만 한 질문(권한 창이 왜 뜨나)에 코디가 워커 지시까지 보냈다 — 질문에는 답만

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-09-30 | Tauri + Rust · 서버 없음 · 운영 Windows | 사용자 「프로그램 형식」「서버 필요 없잖아」 |
| 2026-09-30 | 시스템 Edge → Chrome 을 CDP 로, Chromium 동봉 안 함 | Windows 기본 탑재 · 설치 파일 크기 |
| 2026-09-30 | 범위 = 화면이 쓰는 블로그·플레이스 + 엑셀. 파워링크 제외 | PoC 화면이 파워링크 API 를 부르지 않는다 |
| 2026-09-30 | 미결 다섯 기본값: NSIS · 서명 없음 · Windows PC 빌드 · macOS 개발용 · 화면 재사용 | 사용자 「쭈욱 진행해」 |
| 2026-09-30 | UA 는 실제 브라우저 UA 에서 Headless 만 제거(PoC Mac UA 고정과 다름) | Windows 에서 Windows Edge 로 보이게 · 같은 시각 대조로 결과 동일 확인 |
| 2026-10-01 | rustls `ring` 전환 · 잔여 프로필 정리는 죽은 pid 만 · 루프 안 프레임 실패는 PoC 폴백 | 코드 검수 W-1·W-2·W-4 |
| 2026-10-01 | ~~코드는 `reference/…/desktop/` 에~~ → `kknaksss/sc-rank` 별도 레포(공개) | 사용자 「윈도우 빌드 하려면 깃 레포 필요」 |
| 2026-10-01 | ~~Windows PC 에서 직접 빌드, CI 없음~~ → GitHub Actions `windows-build`(PR 산출물 · `v*` 태그 Release) | 사용자 「exe 빌드 깃에서 하자고」 |

## 5. 날짜별 로그

- `2026-09-30` 제품 착수 · DEC-001/SPEC-001/WORK-001 작성 · 문서 검수 2회 · P1+P2(앱 뼈대, 판정·해시·엑셀 테스트 33) · Mac 에 Edge 설치 · P3(CDP 수집, 같은 시각 PoC 대조 일치)
- `2026-10-01` P4·P5(화면 연결, README) · 사용자 macOS 조회·저장 확인 · 코드 검수 WARN 6 → 수정(test 39) · 코드 레포 분리(subtree split) · P6 · GitHub Actions Windows 빌드 성공(35m → 캐시 4m33s) · 레포 공개 · 머지

## 6. 산출물

- spec PR: https://github.com/kknaks/kknaks_profile/pull/64 (스쿼시 4d72d83)
- code PR: ~~kknaks_profile#65~~ 닫음(레포 분리) → https://github.com/kknaksss/sc-rank/pull/1 (스쿼시 4c6d570) · 앱 본체 `20ef3b7`

- `kknaksss/sc-rank-desktop` → `main`
  - `a0c9aa0` chore: 공개 레포 전환 반영 · Actions 를 Node 24 런타임 버전(v5)으로
  - `58822a1` ci: Windows 설치 파일을 GitHub Actions 에서 만든다
  - `f7dac29` chore: kknaks_profile 에서 분리된 레포로 경로를 정리한다
- 리포트: `review-doc-report.md` · `review-code-report.md` · `report-desktop-p1-p2.md` · `report-desktop-p3.md` · `report-desktop-p4-p5.md` · `report-desktop-fix-review.md` · `report-desktop-p6.md`

## 7. 잔여

- **A-9 Windows 실기** — Actions 산출물 설치 → 실행 → 플레이스 조회·엑셀 저장. 회사 관리 PC 의 Edge 원격 디버깅 정책(`RemoteDebuggingAllowed`)으로 막히면 Chromium 동봉(DEC-001 Option 재검토)
- **A-6 링크** — 「네이버」「매칭 글」이 OS 브라우저로 열리는지 사용자 눈 확인 미답
- 덮개 잠자기 뒤 브라우저 재기동 경로 실측 안 함(로그에 `launched` 한 줄 더 찍히면 정상)
- 블로그 이미지 모드 `found` 경로는 실물로 못 봤다(1.png 가 결과에 없었다)
- 엑셀 「광고 수」가 수집 목록 전체 기준이라 「전체 순위 − 광고 수」로 읽힐 수 있다 — 열 이름 변경·「타겟 앞 광고 수」 열은 이번 범위 밖, 개선 후보
- Release 배포(`v0.1.0` 태그) 여부 미정 — 지금은 로그인해야 받는 Actions 산출물뿐
