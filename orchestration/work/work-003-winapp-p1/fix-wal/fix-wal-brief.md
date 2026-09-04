# [winapp] 긴급 수정 — import 가 WAL 미읽어 활발한 방 0행

너는 **mykakao `winapp` 워커**다. 같은 워크트리. 커밋 금지(코디).

## 증상 (코디 재현 확인)
- 사용자가 **열림·회수가능** 방("딴따라클럽 전체방", chatId 365103356371378)을 과거 가져오기 → **0행**.
- 그 방 파일: `chatLogs_365103356371378.edb` **main 127KB + -wal 482KB**. 데이터는 **대부분 WAL 에 있다.**
- 대조: WAL 작은 방(main 위주)은 정상 import 됨.

## 근본 원인 (코디 확인)
- `src/kakao/import.rs` 의 소스 복호가 `std::fs::read(src)` 로 **main .edb 만 읽는다.** `-wal` 을 안 읽어서, 활발한 방(최근 메시지가 WAL 에 상주, 아직 main 으로 checkpoint 안 됨)은 **0행**.
- 즉 초기 import 이 **WAL-resident 메시지를 누락**한다. (P2 watch 는 WAL 변경을 읽지만, 초기 import 경로는 main 만.)

## 고칠 것
1. **import 이 main + WAL 을 합쳐 현재 상태를 읽게 한다.** SQLCipher v4 는 WAL 프레임 페이지도 같은 방식으로 암호화돼 있다(프레임헤더 24B + 페이지). 접근 예:
   - main 을 평문 SQLite 로 복호 + **-wal 프레임들을 복호해 평문 SQLite -wal 로 재구성**해서 rusqlite(bundled 평문)로 열면 WAL 이 적용된다. 또는 복호한 WAL 페이지를 main 에 반영(apply)해서 읽는다.
   - **P2(watch.rs)의 WAL 프레임 복호 로직을 재사용**하라 — 이미 WAL 을 읽고 있으니 그 코드를 초기 import 에도 쓴다.
   - 원본 -wal 은 **읽기만**(사본). 원본에 쓰지 마라.
2. 검증: 방 365103356371378 을 **커서 0(신규 저장소)**에서 import → **행수 > 0** 이어야 한다(개수만, 본문 미출력).
3. **부가(같이 고쳐라)**: import 완료 후 **③ 채팅 내역이 자동 갱신** 안 된다(`ui/index.html` import 핸들러가 `loadRooms()` 만 하고 현재 방 메시지를 다시 안 읽음). import 끝나면 방금 가져온(또는 현재 선택된 curChat) 방의 메시지를 다시 로드해 ③ 에 바로 보이게 하라.

## 안전 (불변)
- 원본 DB/-wal **읽기만**, 복호 사본 RAII 삭제, 키 비상주, 카톡 무변조, SAC 미변경.
- 키·이름·본문 로그/커밋 비노출. 검증은 개수/유무만.
- 새 crate 금지(SAC). `win_app/` 밖 금지.

## 검증
```
cargo build --release(SAC 통과) + cargo test. 실기동: 저장소 초기화 후 365103356371378 import → 행수>0 확인(본문 미출력). ③ 자동갱신 육안(코디 최종). 검증 1회. SAC 로 test 바이너리 막히면 release+실기동으로 대체하고 보고.
```

## 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 아래 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "winapp WAL import 수정: <한 줄>" --body "원인/수정(main+WAL)/검증 행수/③자동갱신/미결"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] winapp WAL import 수정 완료 — <한 줄>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`
