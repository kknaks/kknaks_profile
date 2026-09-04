# [winapp] 긴급 — 사진 다운로드가 실시간 SSE 막음 + 터미널 창 스폰

너는 **mykakao `winapp` 워커**다. 같은 워크트리. 커밋 금지(코디).

## 증상 (사용자 실기동)
1. **실시간 전송 안 됨** — 새 메시지/사진이 화면에 바로 안 붙고 새로고침해야 렌더됨.
2. **사진 받을 때마다 터미널(콘솔) 창이 뜸.**

## 근본원인 (코디 진단)
- `src/kakao/photo.rs` `curl_download` 가 `Command::new("curl").output()` — **CREATE_NO_WINDOW 없음** → GUI 앱(콘솔숨김)이 curl 을 띄우면 매번 콘솔 창. (증상2)
- `src/watch.rs` process_delta 가 **collect_room_photos(동기 curl 다운로드)를 SSE tx.send 전에** 호출 → 사진 다운로드가 블로킹/지연되면 그 방의 SSE push 가 늦어짐 → 실시간 안 뜨고 새로고침해야 보임. (증상1)

## 고칠 것
**A. 콘솔 창 제거 + 외부 curl 의존 제거**
- **권장**: curl.exe 대신 **WinHTTP(windows crate — 이미 dep)로 in-process 다운로드**. 창 안 뜨고 curl.exe 존재 의존도 없앤다. (SAC 꺼졌으니 crate/빌드 자유롭지만, WinHTTP 는 crate 추가 없이 windows crate 로 됨.)
- WinHTTP 가 부담이면 최소한 curl Command 에 **CREATE_NO_WINDOW(0x08000000)** `.creation_flags` 적용(std::os::windows::process::CommandExt).

**B. 사진 다운로드가 실시간 SSE 를 막지 않게**
- process_delta 는 **새 메시지 SSE 를 먼저 push**(텍스트·사진 메시지 행 즉시 렌더). 사진 **바이트 다운로드는 그 뒤/백그라운드**로(SSE 를 블로킹하지 마라).
- 사진 행은 SSE 로 보낼 때 media_status(pending/saved) 표식. **다운로드 완료(saved) 시 이미지가 화면에 나타나게**:
  - 방법1: 다운로드 완료 후 그 log_id 에 대해 **SSE 재전송(media 업데이트 이벤트/행)** → UI 가 해당 <img> 갱신.
  - 방법2: UI <img onerror> 로 짧은 재시도(백그라운드 저장 완료되면 /api/media 200) — 간단하지만 방법1 이 확실.
  - 택1 구현(방법1 권장).

## 검증 (라이브 — 사용자 협조 가능)
- 열린 추적 방에 카톡으로 **텍스트 메시지** → **수초 내 화면 append**(새로고침 없이). **사진** → 메시지 즉시 뜨고, 다운로드 완료되면 이미지 나타남. **콘솔 창 안 뜸.**
- cargo build --release + cargo test. 값·URL·토큰 미출력.

## 안전 (불변)
- URL/토큰/이미지 로그·커밋 비노출. 원본 읽기만·카톡 무변조·키 RAM only. `win_app/` 밖·문서 SoT 수정 금지.

## 완료 보고 — 문구 변경 금지
- 커밋 금지. 끝나면 둘 다.
```bash
orca orchestration send --to term_a47812a6-9d90-4086-8f44-a7131976c8ed --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "사진 실시간/콘솔창 수정: <한 줄>" --body "다운로드 방식(WinHTTP/no-window)/SSE 선push/사진 saved 반영/cargo 수치"
orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[worker_done] 사진 실시간/콘솔창 수정 완료 — <한 줄>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_a47812a6-9d90-4086-8f44-a7131976c8ed --text "[질문] winapp: <질문>" --enter`
