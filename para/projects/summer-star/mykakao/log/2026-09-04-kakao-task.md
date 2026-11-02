# 작업 요약 — kakao-task (mykakao)

기간: `2026-09-02` ~ `2026-09-04`
결과: P1~P3·로그인상태·설정리디자인·사진수집 전부 done. 배포본(exe+ui) 산출. mykakao 레포 `feat/win-app` 15커밋 — PR 만 잔여(계정 권한: kknaksss 인증 필요).

## 1. 무엇을 했나

카톡 대화를 내보내기 없이 로컬에서 수집하려면 Windows 에서 돌아야 하는데, 레포 코드는 전부 macOS 전제(ioreg·plist·brew sqlcipher)였다. Windows V2 를 Rust 로 새로 세웠다 — 방 선택·과거 복호·실시간 축적·이름 해석·사진 수집·트레이 앱을 `win_app/` 한 디렉토리에 P1~P3 + 후속 3건으로 쌓았다. 핵심 난관은 **암호화 키를 어떻게 얻느냐**였고, 오프라인 파생을 못 뚫어 실행 중 메모리 회수로 방향을 틀었다. 배포본까지 냈고(서명 없음 → SmartScreen 안내), 원래 목적인 대화 패턴 추출은 미착수로 남겼다.

## 2. 적용한 기술·개념

이 작업의 알맹이다. 새로 쓴 것·판단이 갈린 것·막혔다가 푼 것.

- **실행 중 메모리에서 SQLCipher raw key 회수** — 오프라인 키 파생을 포기하고 라이브 프로세스를 읽어 키를 꺼냄 → [[process-memory-key-recovery]]
  - 왜 이걸 골랐나: 파생식 회수를 4차(spike1~4b)까지 시도했으나 anti-debug 자폭 + DPAPI 벽으로 막혔다. 「어차피 실행 중 카톡은 키를 평문으로 들고 있다」를 이용해 passive VM_READ 로 회수했다. 파생식은 셸빙(BASE-004 백로그).
  - 무엇이 어려웠나: 반복 harvest 가 느려(수십초) 첫 로드 이름 지연이 났다 → 세션 키캐시로 회피. 프로세스 메모리 격리가 같은 사용자 관찰까지는 막지 않는다는 게 성립 근거였다([[process]]).
  - 근거: `win_app/src/memkey.rs` · spike3 KEY_REPORT.md · SUMMARY 핵심기술

- **WAL 병합 복호** — 활발한 방 대화가 `-wal` 에 있어 main 단독 복호 시 0행 → main+WAL 병합 → [[write-ahead-logging]]
  - 무엇이 어려웠나: 처음엔 활발한 방만 조용히 0행으로 나왔다. SQLite WAL 이 checkpoint 전까지 최신을 로그 파일에 두는 성질을 파악하고서야 원인이 잡혔다.
  - 근거: SUMMARY 핵심기술 · WORK-003

- **큰 정수 JSON 직렬화 정밀도** — 카톡 `chatId` 를 JSON number 로 내보내자 프런트에서 방을 못 찾음 → 문자열 직렬화 → [[integer-precision-in-json]]
  - 무엇이 어려웠나: 서버는 정확히 들고 있는데 JS 수신측에서 2^53 위 자리가 뭉개졌다. 에러 없이 다른 ID 가 되어 「방을 못 찾는」증상으로만 드러났다.
  - 근거: SUMMARY 핵심기술 · SPEC-003 API 계약

- **파일 감시 + 델타 폴링 병행** — `notify` 가 WAL in-place 쓰기를 놓쳐 실시간이 안 됨 → 3초 델타 폴링 병행 → [[filesystem-change-notification]] · [[polling]]
  - 왜 이걸 골랐나: 감시만으로는 in-place 쓰기(-wal)를 못 잡는다. 감시로 즉시성을 얻되 폴링으로 사각지대를 메웠다. 이벤트 폭주는 700ms 디바운스로 눌렀다.
  - 근거: `win_app/src/watch.rs` · WORK-002(P2) · 커밋 e008fb6

- **SSE bounded broadcast + push 순서** — 잡은 대화 델타를 `/api/stream` 으로 밀되 느린 구독자에 메모리 안 새게 함 → [[server-sent-events]]
  - 왜 이걸 골랐나: broadcast 채널을 bounded(256)+Lagged drop 으로 둬 느린 구독자가 밀릴 때 이벤트를 버리게 했다. SSE push 를 사진 다운로드보다 먼저 내보내 순서를 잡았다.
  - 근거: `win_app/src/watch.rs`(SSE) · 커밋 e008fb6

- **코드 서명 없는 배포와 SAC 하드 차단** — 미서명 exe 의 SmartScreen 경고 + 빌드 중 SAC 차단 → [[code-signing]]
  - 무엇이 어려웠나: MS 정책 업데이트(9/2~3) 후 Smart App Control 이 서명 없는 rustc/cargo 산출물을 하드 차단해 빌드가 막혔다. 「Rust 라서/트레이 앱이라서」로 오인하기 쉬웠으나 서명 문제였다 → SAC OFF(사용자 승인, 되돌리기=클린 설치). tray-icon crate 의 build-script 도 SAC 에 간헐 차단돼 제거하고 windows crate 로 트레이를 직접 그렸다.
  - 근거: SUMMARY 핵심기술 · WORK-003 P3 · 커밋 3583361

## 3. 막혔던 것 / 사고

- **파생식 RE 4차 실패** → 실행 중 메모리 회수로 우회. 파생식 자체는 못 뚫었고 BASE-004 백로그로 남겼다. 되돌아보면 spike 를 3차에서 끊고 메모리 회수로 갔어도 됐다.
- **오래된 사진 .cng 복호 실패** — talkmedia URL 이 사진 나이에 따라 만료(최근 200 / 오래됨 410)된다는 반전을 발견. 최근 사진은 URL 다운로드로 성립했고, 오래된 .cng 로컬 복호는 키가 힙에 없어(Ghidra RE 필요) BASE-008 백로그.
- **SAC 오진 위험** — 빌드 차단을 언어·라이브러리 탓으로 볼 뻔했다. 서명/실행 방어막을 먼저 의심하는 게 맞았다.

## 4. 결정

정본은 `_RESUME.md` + `10-decision/DEC-003~006`. 핵심만:

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-09-02 | 키 = 실행 중 메모리 회수 (파생식 셸빙) | 오프라인 파생 4차 실패(anti-debug+DPAPI) |
| 2026-09-02 | 구현 = Rust(axum·rusqlite bundled-sqlcipher·notify·windows), 같은 레포 `win_app/` | 순수 Rust 크립토로 OpenSSL 회피, 평문 SQLite 저장 |
| 2026-09-02 | win_app 개발은 워크트리 하나에서 P1~P3 연속 (새 워크트리 안 만듦) | 워커 context 보존 |
| 2026-09-03 | 실시간 = 파일감시 + 3초 델타 폴링 병행 | notify 가 WAL in-place 쓰기를 놓침 |
| 2026-09-04 | 사진 = talkmedia URL 다운로드(.cng 아님), 유실은 정직 표시 | .cng 키가 힙에 없음, URL 은 최근 사진만 생존 |
| 2026-09-03 | SAC OFF (사용자 승인) | 미서명 산출물 하드 차단, 우회 UI 없음 |

## 5. 날짜별 로그

- `2026-09-02` spike3 메모리 키 회수 확증(1455행 실복호) → BASE/DEC/SPEC-003 → P1(키회수·페이지복호·SQLite·axum API·설정 HTML, 커밋 1fa8a18) → P2(watch.rs·SSE·델타폴링, e008fb6)
- `2026-09-03` spike4/4b 파생식 RE 규명하되 막힘(BASE-004) → P3(windows crate 트레이 직접·닉네임 조인·applog, 3583361) → 로그인상태 트래킹(WORK-006, ff79ba2) → 설정 UI 리디자인 착수(SPEC-005)
- `2026-09-04` 사진 획득 조사(URL 생존=사진 나이 반전, .cng 는 백로그) → 사진 수집(WORK-008) → work/ 폴더 통합(work-003+서브+poc 3종 → kakao-task) → 배포본 zip

## 6. 산출물

- code: mykakao 레포 `feat/win-app` (15커밋). PR 대기 — 계정 권한(kknaksss 소유) 인증 필요.
  - `1fa8a18`(P1) → `e008fb6`(P2) → `3583361`(P3) → `ff79ba2`(로그인상태) → … 사진수집
- 문서: BASE/DEC/SPEC-003·005·006·007 + BASE-004·008(백로그) — `para/projects/summer-star/mykakao/`
- 배포본: `mykakao.exe` + `ui/` + 사용법.txt (본인 기기·본인 카톡 전용, 서명 없음)

## 7. 잔여

- **main PR** — mykakao 레포 계정 권한(kknaksss 인증) 해결 후.
- **대화 패턴 추출** — 원래 목적, 미착수. 수집 파이프는 섰으니 그 위에 올린다.
- **첫 로드 이름 지연** — 수십초 harvest, 이름 캐싱 개선 여지.
- **오래된 사진 .cng 복호** (BASE-008) · **파생식 오프라인 회수** (BASE-004) — 둘 다 Ghidra RE 필요, deferred.
- 사진 checkSum 일부 불일치 재시도.
