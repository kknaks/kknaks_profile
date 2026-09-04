# [winapp] Windows V2 P2 — 실시간 파일감시 → 델타 복호 → SSE 축적

너는 **mykakao `winapp` 워커**다. **P1 을 네가 방금 완성했다** — 같은 워크트리·같은 크레이트를 이어서 확장한다. 역할 문서 규칙(특히 안전·자원 규칙) 그대로.

작업 워크트리: `C:/Users/sc971/orca/workspaces/mykakao/work-003-winapp-p1` (P1 과 **같은 워크트리**, `win_app/` 이미 있음)
base/브랜치: `work-003-winapp-p1` (P1 커밋 `1fa8a18` 위에 이어서). PR 은 코디.

> 목표: P1 의 과거 import 위에 **실시간 축적**을 얹는다. 카톡이 그 방에 새 메시지를 쓰면 파일 변경을 감지해 **새 행만** 복호·저장하고 화면에 스트리밍한다. **함수 주입 후킹 아님**(SAC) — OS 파일 감시다.

## 1. SSOT — 먼저 읽을 것 (read-only 절대경로)

- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/20-spec/spec-003-windows-v2.md` §BE Contract 「실시간 축적 (P2)」 + §FE Contract `/api/stream` ← **계약 SoT**.
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/10-decision/decision-003-windows-v2-approach.md` 결정3(실시간=파일감시→델타복호→append→SSE) + 결정4.
- **P1 코드**(이 워크트리 `win_app/`): `import.rs`(델타 로직 재사용)·`store.rs`(커서·upsert)·`server.rs`(라우터·AppState).

## 2. 무엇을 만드나

P1 은 수동 import(과거)였다. P2 는 **자동 실시간**:
- 선택된 방들의 `chat_data` 를 감시하다 `chatLogs_<chatId>.edb-wal` 변경 시 → 그 방 델타(logId>커서) 복호 → SQLite append → SSE 로 push.
- 델타 복호는 P1 의 import 로직을 재사용(전체 재복호 금지 — 커서 이후만).

## 3. 계약 (SPEC-003 §FE Contract)

- `GET /api/stream?chat_id=` → SSE, `event: message`, payload = P1 `/api/messages` 행 shape(`{log_id,author_id,author_name?,type,sent_at,text}`). 이벤트명·키 그대로.
- 기존 5개 API 는 불변.

## 4. 구현 (win_app/ 확장)

1. `src/watch.rs` 신규: `notify` crate 로 선택 방들의 `chat_data` dir 감시(내부 ReadDirectoryChangesW). `-wal` 변경 이벤트 → 해당 chat_id 델타 동기 트리거.
2. 델타 파이프: import.rs 의 「키회수 → 복호 → 커서 이후 행 → upsert」를 재사용. **전체 재복호 금지.**
3. SSE: `GET /api/stream`. tokio **broadcast 채널(바운드 용량)** 로 새 행 fan-out. **lagging 수신자는 drop**(무한 버퍼 금지). 연결 종료 시 정리.
4. `ui/index.html`: 채팅 내역 2-pane 에서 선택 방의 `EventSource('/api/stream?chat_id=')` 구독 → 새 말풍선 append. 재연결 처리.
5. 감시 누락 폴백(선택): 저빈도 주기 재동기(옵션, 무한 폴링 아님).

## 5. allowed_paths

- `win_app/` (P1 확장). 밖은 금지.

## 6. 자원·안전 (상주 앱 — 이게 P2 의 핵심 리스크)

- **SSE 무한 버퍼 금지** — bounded broadcast, lagged 수신자 drop. 연결 끊기면 태스크·수신자 정리(누수 금지).
- **파일 워처 수명 관리** — 선택 방만 감시. 선택 변경 시 watcher 재구성(핸들 누적 금지). 종료 시 clean stop.
- **델타만 복호** — 이벤트마다 전체 DB 재복호하지 마라(CPU·임시본 폭증). 커서 이후만.
- **복호 임시본 RAII 삭제**(P1 방식 유지). **키 비상주**(요청/이벤트마다 회수·폐기).
- 카톡 크래시·변조·종료 금지. 원본 읽기만. SAC 미변경. **키·본문·계정 식별자 로그·커밋 비노출**(마스킹).
- 실 스트림 검증 시 **행수/이벤트 수만**, 본문 미열람.

## 7. 하지 말 것

- P3(트레이) 구현 금지. 기존 5개 API·P1 복호 코어 계약 변경 금지(어긋나면 보고).
- 함수 주입 후킹·Frida 금지(SAC). 전체 재복호·무한 폴링·무한 SSE 버퍼 금지.
- `win_app/` 밖·문서 SoT 수정 금지. git commit·push·PR 금지.

## 8. 검증

```
cd win_app && cargo build(에러0) + cargo test<네 테스트>. cargo=~/.cargo/bin.
- 순수/단위 가능한 것(델타 선별·SSE 페이로드 직렬화)은 테스트.
- 실스트림: 서버 띄우고(코디가 실카톡으로 최종 확인 가능) 이벤트 수/행수만. 못 하면 못 했다고.
- 검증 1회.
```

## 9. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 검증·커밋·PR 은 코디.
- 끝나면 **아래 두 명령 모두** 실행.

```bash
orca orchestration send   --to term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --from <네 워커handle>   --type worker_done   --task-id <preamble taskId> --dispatch-id <preamble dispatchId>   --subject "winapp P2 완료: <한 줄>"   --body "구현/파일 / cargo 수치 / SSE·워처 자원처리 / 계약 준수 / 미결"

orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3   --text "[worker_done] winapp P2 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --text "[질문] winapp: <질문>" --enter`
