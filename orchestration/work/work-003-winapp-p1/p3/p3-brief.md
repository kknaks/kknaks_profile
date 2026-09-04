# [winapp] Windows V2 P3 — 트레이 앱 + 로그인 상태 상시화 (+ 닉네임 조인)

너는 **mykakao `winapp` 워커**다. **P1·P2 를 네가 완성했다** — 같은 워크트리·크레이트를 이어서 마무리한다. 안전·자원 규칙 그대로.

작업 워크트리: `C:/Users/sc971/orca/workspaces/mykakao/work-003-winapp-p1` (P1·P2 와 같은 워크트리)
브랜치: `work-003-winapp-p1` (P2 커밋 `e008fb6` 위에 이어서). PR 은 코디.

> 목표: 지금은 콘솔로 서버가 뜬다. P3 는 이걸 **트레이 상주 앱**으로 만든다 — 작업표시줄(트레이) 아이콘 클릭 → 기본 브라우저로 localhost 설정 페이지 열림. + 로그인 상태 상시 감지. 마지막 마감 단계다.

## 1. SSOT (read-only 절대경로)

- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/20-spec/spec-003-windows-v2.md` §UX Contract + 「P3」 + §Work Handoff(WORK-005 = 트레이 tray-icon + 로그인 상태 상시화).
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/00-baseline/baseline-003-windows-tray-realtime-accumulation.md` §UX 구조(트레이→설정 3섹션).
- **P1·P2 코드**(이 워크트리): `main.rs`(현재 콘솔 기동)·`server.rs`(AppState·/api/state·enrich_titles)·`ui/index.html`(3섹션).

## 2. 무엇을 만드나

1. **트레이 아이콘**(`tray-icon` crate): 상주 앱. 좌클릭(또는 메뉴 "설정 열기") → 기본 브라우저로 `http://127.0.0.1:<port>` 오픈(`open`/`ShellExecute`/`webbrowser`). 우클릭 메뉴 = 「설정 열기」·「종료」.
2. **이벤트 루프 ↔ tokio 공존**: 트레이 이벤트 루프(메인 스레드)와 axum(tokio) 서버가 한 프로세스에서 함께 돌게. 서버는 백그라운드 스레드/런타임, 트레이는 메인. busy-loop 금지.
3. **로그인 상태 상시화**: 설정 페이지 ① 섹션이 `/api/state` 를 **적정 주기**(예 3~5s, 타이트 루프 금지)로 폴링해 카톡 실행/로그인/회수가능 방 수를 갱신. 미실행이면 안내 배너.
4. **콘솔 창**: 트레이 앱이므로 콘솔 숨김 고려(`#![windows_subsystem = "windows"]`). 숨기면 로그는 **파일로**(예 `%LOCALAPPDATA%\mykakao\win_app.log`) — 단 키/본문 절대 로깅 금지. (디버그 편의로 콘솔 유지도 허용 — 판단해 보고.)
5. **닉네임 조인(마감 폴리시)**: 지금 `author_name` 이 null 이다. `TalkUserDB.edb`(`talkUser`: userId·nickName)를 복호해 author_id→nickName 매핑을 `author` 테이블/조인에 채워 채팅 내역에 이름이 뜨게. (본문 아님·닉네임은 표시 목적. 로그 노출 금지.)

## 3. 계약

- 기존 6개 API(state/rooms/rooms.select/import/messages/stream) **불변**. 트레이는 API 를 추가하지 않아도 된다(브라우저 오픈만). 필요 시 `/api/quit` 같은 건 만들지 말고 트레이 메뉴로.
- `/api/messages` 응답의 `author_name` 이 이제 채워짐(계약 shape 동일, null→값).

## 4. allowed_paths

- `win_app/`. 밖 금지.

## 5. 자원·안전 (상주 앱 — P3 핵심)

- **이벤트 루프 busy-loop 금지** — 트레이/이벤트 대기는 블로킹 수신. 폴링 주기 타이트 금지.
- **트레이·아이콘 리소스 정리** — 종료 시 clean. 스레드/런타임 누수 금지.
- 로그인 폴링은 서버 부하 낮게(주기 여유). `/api/state` 는 메모리 스캔을 하므로 P1 의 last_refresh 스로틀 유지·활용.
- 닉네임 조인 시에도 **원본 읽기만·복호 임시본 RAII·키 비상주** 유지. TalkUserDB 도 사본/읽기전용.
- **키·본문·닉네임 원값·계정 식별자 로그·커밋 비노출.** 콘솔 숨기고 파일 로그 쓰면 거기에도 금지.
- 카톡 크래시·변조·종료 금지. SAC 미변경. Windows 시작프로그램 자동등록은 **하지 마라**(시스템 변경 — 원하면 후속/옵션).

## 6. 하지 말 것

- 시작프로그램 레지스트리 자동 등록 금지. 새 무거운 크레이트 남발 금지(tray-icon + 필요한 이벤트루프 정도).
- 기존 API 계약·복호 코어 변경 금지(어긋나면 보고). `win_app/` 밖·문서 SoT 수정 금지. commit·push·PR 금지.

## 7. 검증

```
cd win_app && cargo build(에러0) + cargo test. cargo=~/.cargo/bin.
- 트레이는 GUI라 자동 테스트 어렵다 — 빌드 성공 + 수동 기동으로 트레이 아이콘·브라우저 오픈 동작을 육안 확인(코디가 최종 실기동). 못 한 건 못 했다고.
- 닉네임 조인은 단위 테스트(합성) + 실기동 행수/이름 유무만(본문·닉네임 원값 미출력).
- 검증 1회.
```

## 8. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령 모두** 실행.

```bash
orca orchestration send   --to term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --from <네 워커handle>   --type worker_done   --task-id <preamble taskId> --dispatch-id <preamble dispatchId>   --subject "winapp P3 완료: <한 줄>"   --body "구현/파일 / 트레이·이벤트루프 방식 / 닉네임 조인 / cargo 수치 / 자원처리 / 미결"

orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3   --text "[worker_done] winapp P3 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --text "[질문] winapp: <질문>" --enter`
