# mykakao win_app — 재개 노트 (kakao-task 정본)

> **정리(2026-09-04):** `work/` 아래 흩어져 있던 폴더(work-003 + 서브 + poc 3종)를 이 `kakao-task/` 하나로 합쳤다.
> - `SUMMARY.md` — 무엇이 완료됐나 (P1~P3 + WORK-006/007/008 + 배포)
> - `briefs.md` — 발주 브리프 19건 시간순 통합
> - `mykakao-dist.zip` — 배포본 (mykakao.exe + ui/ + 사용법.txt)
> - 코드는 별도 워크트리 `workspaces/mykakao/work-003-winapp-p1/win_app/`, 브랜치 `feat/win-app`.
>
> **현재 상태:** P1~P3·로그인상태·설정리디자인·사진수집 전부 done. 프로필 레포는 푸쉬됨.
> 남은 것 — mykakao 코드 레포(`kknaksss/mykakao`) `feat/win-app` 푸쉬+PR(계정 토큰 필요), 이후 대화 패턴 추출.
>
> 아래는 P1 착수 시점의 원본 재개 노트(P1~P3만). 이후 이력은 SUMMARY·briefs 참조.

---

## 발주 (2026-09-02)
- 성격: **실제 코드** (spike 아님) — 커밋/PR 대상. Windows V2 P1.
- 범위: win_app/ Rust 스캐폴드 + 메모리 키회수 + 페이지 복호(순수 Rust) + SQLite 저장 + axum API 5개 + 설정 HTML(3섹션+2pane). 실시간(P2)·트레이(P3) 제외.
- Run: run_562b2ec38263 (공유) · Task: task_4aac0b4b5892 · Dispatch: ctx_a94446a3d800
- 워커handle(winapp): term_d636cc9c-c322-4a95-8261-f9ab50143832
- 워크트리: C:/Users/sc971/orca/workspaces/mykakao/work-003-winapp-p1 (base origin/main, win_app 없음 — 새로 생성)
- 코디handle: term_eda12742-b6d9-434d-8eb8-f534be92dcc3
- 참조: SPEC-003(계약) + spike3 key_recover.py/KEY_REPORT.md(포팅 원천, poc-windows-key-derivation 워크트리)
- 복호전략: 순수 Rust 크립토→평문 SQLite→rusqlite bundled (OpenSSL 회피)
- 검증(코디): cargo build/test + 카톡 대상 실기동(행수만, 본문 미열람). PR 은 코디.
- 완료 캐치: 2채널. 폴링 금지.

## 워크트리 정책 (사용자 결정 2026-09-02)
- **win_app 개발은 이 워크트리 하나에서 쭈욱.** P2(실시간)·P3(트레이)도 새 워크트리 만들지 말고 같은 워크트리 + 같은 winapp 워커(context 보존)로 이어서 발주한다.
- 브랜치명 work-003-winapp-p1 은 라벨 — PR 시 필요하면 win-app 등으로 rename(워커가 브랜치 물고 있을 땐 변경 금지).

## §P1 완료 (2026-09-02)
- 판정: done. cargo test 11 passed(코디 직접) + 실기동 /api/state=카톡감지·7방 recoverable + import 1450행(본문 미열람).
- 안전 검증(코디): 원본 read-only(fs::read 바이트만) / 복호 임시본 RAII Drop 삭제 / 키 비상주(요청마다 회수·폐기, AppState에 키 없음) / unsafe는 memkey.rs만 / 로그에 키·본문 없음 / 계정은 지문 마스킹 / SSE 없음(P1 정합) / allowed_paths win_app/ 준수.
- 자원누수 관점(리뷰어 대체): 전역 무한캐시 없음, 요청 로컬 Vec만. exe 3.67MB.
- 커밋: 1fa8a18 (브랜치 work-003-winapp-p1). PR 은 아직(사용자와 타이밍 상의).
- 워커 유지(release 안 함) — P2 를 같은 워커/워크트리로 이어 발주.
- 미결(후속): author_name(TalkUserDB 닉네임 조인), -wal 델타, import 속도.

## §P2 완료 (2026-09-02)
- 판정: done. cargo test 13 passed(코디). watch.rs(notify→700ms 디바운스→import_room 델타 재사용→bounded broadcast) + /api/stream SSE + ui EventSource.
- 자원검증(코디): SSE bounded(256)+Lagged drop / 워처 핸들1개+Drop clean stop+NonRecursive / 델타만(import_room 재사용) / 원본 read-only(fs::read) / 임시본 RAII 삭제 / 키 비상주 / 로그 노출0.
- 실기동: 카톡감지+파일감시 시작+SSE 연결 OK.
- 커밋: e008fb6.
- 미결: author_name(닉네임 조인) 여전히 null — P3 또는 후속.

## §P3 완료 (2026-09-02)
- 판정: done. SAC 블로커(tray-icon→thiserror v2/mime_guess build-script 차단) 해소 = tray-icon 제거, windows crate 로 트레이 직접(Shell_NotifyIconW+WndProc+TrackPopupMenu+ShellExecuteW+GetMessageW). 신규 crate 0.
- 추가: 닉네임 조인(TalkUserDB→author_name), applog 파일로거(마스킹 규율), state 10s 캐시, UI 4s 폴링.
- 검증(코디): cargo build --release SAC 통과(차단0, exe 3.93MB, 코디 직접) / cargo test 14 passed / headless /api/state 정상 / 로그 파일 시크릿 없음 / 트레이 NIM_DELETE 정리 / busy-loop 없음.
- 커밋: 3583361. 브랜치 work-003-winapp-p1 = 1fa8a18(P1)→e008fb6(P2)→3583361(P3).
- 워커 유지(release 안 함) — 사용자 검수 후 수정 대비.
- 사용자 담당: 트레이 GUI·이름표시 실기동(exe 실행 시 SmartScreen 승인 필요할 수 있음).
- SAC 주의: mime_guess(tower-http fs 경유) build-script 가 SAC 에서 간헐 차단 이력 — 이번 clean 빌드는 통과. 재발 시 tower-http fs feature 대체 검토(백로그).
