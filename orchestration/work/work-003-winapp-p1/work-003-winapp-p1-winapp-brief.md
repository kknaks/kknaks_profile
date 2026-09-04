# [winapp] Windows V2 P1 — 방 선택 + 과거 히스토리 복호·저장 (Rust win_app 스캐폴드)

너는 **mykakao `winapp` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/orchestration/roles/mykakao/winapp/role.md` (+ 같은 폴더 rules·skills·tools·workflow)

작업 워크트리: `C:/Users/sc971/orca/workspaces/mykakao/work-003-winapp-p1`
base: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다). 이건 **실제 코드 작업 = 커밋/PR 대상**(spike 아님).

이 워크트리는 너 혼자 쓴다. `win_app/` 은 아직 없다 — **네가 새로 만든다.** macOS `backend/`(Python)·`frontend/` 는 **건드리지 마라.**

## 1. SSOT — 먼저 읽을 것 (전부 read-only 절대경로)

- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/20-spec/spec-003-windows-v2.md` ← **계약 SoT.** API·UX·BE 메커니즘·SQLite 스키마·win_app 레이아웃. **여기 없는 건 발명하지 마라.**
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/10-decision/decision-003-windows-v2-approach.md` ← 4결정(키=메모리회수/저장=SQLite/실시간=파일감시/Rust·win_app). P1 은 실시간(P2)·트레이(P3) 제외.
- `C:/Users/sc971/orca/workspaces/kknaks_profile/mykakao/para/projects/summer-star/mykakao/00-baseline/baseline-003-windows-tray-realtime-accumulation.md` ← UX 구조·전체 그림.

**참조 코드 (spike 3 — 알고리즘 포팅 원천, read-only):**
- `C:/Users/sc971/orca/workspaces/mykakao/poc-windows-key-derivation/backend/key_recover.py` ← 메모리 키 회수(ReadProcessMemory) + SQLCipher v4 page-1 HMAC-SHA512 검증. **이걸 Rust 로 포팅.**
- `C:/Users/sc971/orca/workspaces/mykakao/poc-windows-key-derivation/backend/key_analysis.py` ← 실복호·행수 확인 로직.
- `C:/Users/sc971/orca/workspaces/mykakao/poc-windows-key-derivation/backend/KEY_REPORT.md` ← **SQLCipher v4 파라미터 정본** (compat4·page4096·reserve80·HMAC key 유도·page IV).

## 2. 배경 / 무엇을 만드나

Windows 카톡 대화 DB(`chatLogs_<chatId>.edb`, SQLCipher v4)를 실행 중 카톡 메모리에서 회수한 raw key 로 복호해, 선택한 방의 과거 히스토리를 우리 로컬 SQLite 에 저장한다. spike 3 에서 1455행 실복호가 이미 증명됐다 — 그 알고리즘을 **Rust 로 제품화**하는 게 P1 이다.

**P1 범위(이번):** `win_app/` Rust 크레이트 스캐폴드 + 메모리 키회수 + 페이지 복호 + SQLite 저장 + axum API 5개 + 설정 HTML(3섹션+2pane).
**P1 아님:** 실시간 파일감시(P2), 트레이 아이콘(P3).

## 3. 계약 (SPEC-003 §FE/BE Contract 그대로 — 요지)

axum API (응답 키·경로 그대로):
- `GET /api/state` → `{kakao_running, logged_in, recoverable_rooms:[chatId], account?}`
- `GET /api/rooms` → `[{chat_id, title, member_count?, selected}]`
- `POST /api/rooms/select` body `{chat_ids:[...]}` → `{ok, selected:[...]}`
- `POST /api/import` body `{chat_id?}` → `{ok, imported:{chat_id:count}}`
- `GET /api/messages?chat_id=&after=&limit=` → `[{log_id, author_id, author_name?, type, sent_at, text}]`

SQLite 스키마: SPEC-003 §Data Contract (room/message/author, message PK=(chat_id,log_id) 멱등 upsert).

## 4. 복호 전략 (rules.md 참고 — OpenSSL 회피)

- 키는 메모리 raw key(32B) — main key KDF 불필요.
- **순수 Rust 크립토**(`aes`+`cbc`+`hmac`+`sha2`+`pbkdf2`)로 SQLCipher v4 페이지 복호 → **평문 SQLite** 로 떨군 뒤 `rusqlite`(feature `bundled`, 평문)로 연다. **bundled-sqlcipher/OpenSSL 쓰지 마라**(Windows 빌드 지옥).
- 파라미터는 KEY_REPORT.md 정본: compat4, page4096, reserve80(IV16+HMAC64), HMAC key=`PBKDF2-HMAC-SHA512(raw_key, salt⊕0x3a, 2, 32)`, page IV=페이지 reserve 앞16B, AES-256-CBC.
- **이 전략이 막히면 구현 전에 코디에 보고**하고 대안 상의.

## 6. 구현 단계

1. cargo 동작 확인(`cargo --version`; 없으면 `export PATH="$HOME/.cargo/bin:$PATH"`). `win_app/` 크레이트 생성.
2. **복호 코어 먼저**: 메모리 키회수(windows crate) + 페이지 복호(순수 Rust) → 평문 SQLite. 순수 함수(HMAC 검증·페이지 복호)는 **합성 픽스처로 cargo test**.
3. 저장: rusqlite 축적 DB(room/message/author).
4. import: 선택 방 키회수 → 복호 → `chatLogs` 행을 우리 SQLite 에 upsert(logId 커서).
5. axum API 5개 + `ui/` 정적 서빙.
6. `ui/index.html`: 설정 3섹션(로그인 상태 감지 / 대화방 설정 / 채팅 내역 2-pane). vanilla HTML/JS, 계약 키 그대로.

## 7. 범위 제약 — 하지 말 것

- **카톡 크래시·변조·종료 금지.** 메모리 ReadProcessMemory **읽기만**(쓰기·주입 금지). SAC 미변경.
- **원본 DB·레지스트리 쓰기 금지.** 복호는 **사본**(임시, 작업 후 삭제).
- **키·user_id·device UUID·대화 본문·계정 식별자를 로그·테스트·리포트·커밋에 남기지 마라.** 마스킹/`<redacted>`. 계정 폴더 해시는 자동 탐색(하드코딩 금지).
- 실복호 검증 시 **행수만 보고**(spike3처럼), 본문 인용 금지.
- `win_app/` 밖·문서 SoT 수정 금지. P2(파일감시)·P3(트레이) 구현하지 마라. git commit·push·PR 금지.
- 크레이트 추가는 최소로. 무거운 결정은 보고.

## 8. 검증

```
cd win_app && cargo build (에러 0, 경고 허용) + cargo test <네가 만든 테스트>. cargo 는 ~/.cargo/bin, MSVC 링킹 자동.
- 순수 함수(HMAC 검증·페이지 복호)는 합성 픽스처 테스트로 확인(실 DB 불필요).
- 실기동(카톡 대상 실복호·행수)은 하되 **본문 미열람·행수만**. 못 하는 환경이면 못 했다고 보고 — 통과했다 쓰지 마라.
- 검증은 1회만.
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "winapp 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3 \
  --text "[worker_done] winapp 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_eda12742-b6d9-434d-8eb8-f534be92dcc3 --text "[질문] winapp: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
