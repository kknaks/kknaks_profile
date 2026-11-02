# [frontend] Tauri 셸 — 마이크 권한 (macOS · Windows)

너는 **task-management `frontend` 워커**다. **이번 건은 Tauri 셸 설정과 Rust 쪽이다.**

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`).
회의록 코드가 전부 들어와 있다(HEAD `d44a3e5`).

## 0. 무슨 일이 났나 — 사용자가 앱 창에서 직접 밟았다

`npm run tauri dev` 로 앱을 띄우고 회의를 시작했더니 —

```
마이크 권한을 묻지 않는다
소리가 안 들어간다
화면이 곧바로 「일시정지」로 떨어진다
```

**백엔드 로그로 확인한 것**

```
WebSocket /api/meetings/1/stream  [accepted] ×3 · connection open ×3
Soniox 관련 로그 0줄 · 오디오 프레임 0
POST /api/meetings/1/lines 201 ×5   ← 사람 줄 입력은 정상
```

**백엔드·프론트 로직 문제가 아니다.** 오디오가 한 프레임도 안 오니 업스트림(Soniox)이 아예 안 열렸다.
`getUserMedia` 가 실패해서 트랙이 없고, 그래서 `paused/mic` 로 떨어진 것이다.

**원인** — 셸에 마이크 권한 선언이 없다.

```
src-tauri/Info.plist            없음
src-tauri/*.entitlements        없음
tauri.conf.json  bundle         {active, targets, icon} 뿐 — macOS 키 없음
실행 중                          target/debug/app  (「.app」 번들이 아니다)
```

`audioCapture.ts:11` 에 **「⚠ 실물 확인 필요 — macOS Tauri(WKWebView) 의 `getUserMedia` 권한 프롬프트」**가
주석으로 남아 있었다. 그게 지금 터졌다.

## 1. 할 일 — **맥과 윈도우 둘 다**

`tauri 2.11.3` · `tauri-build 2.6.3`.

### 1-1. macOS

```
NSMicrophoneUsageDescription 를 번들 Info.plist 에 넣는다
문구는 한국어로 — 왜 마이크가 필요한지 사람이 읽고 판단할 수 있게
  (예: 「회의 내용을 받아쓰기 위해 마이크를 사용합니다.」 — 더 나은 문구면 써라)
```

**필요하면 entitlements 도 함께 둬라**(`com.apple.security.device.audio-input`).
서명 없이 로컬에서 도는 경우와 서명본 둘 다 고려해라.

### 1-2. Windows (WebView2)

**WebView2 는 기본적으로 미디어 권한을 거부한다.** `PermissionRequested` 를 처리하지 않으면
`getUserMedia` 가 조용히 실패한다 — 지금 macOS 에서 난 것과 같은 증상이 난다.

`src-tauri/src/lib.rs`(69줄)에서 웹뷰 생성 뒤 그 이벤트를 받아 **마이크 요청을 허용**해라.
**Tauri 2.x 의 실제 API 를 확인하고 써라** — 버전에 따라 접근 경로가 다르다.
방법을 못 찾으면 **만들어내지 말고 보고에 적어라.**

### 1-3. `tauri dev` 에서도 확인되게

`tauri dev` 는 **번들이 아니라 맨 실행파일**로 뜬다. 그래서 `Info.plist` 가 안 붙고 macOS 가 권한을 안 묻는다.

```
① dev 에서도 권한이 붙게 할 방법이 있으면 그렇게 해라
② 없으면 「dev 에서는 안 되고 `tauri build` 로 구운 앱에서 확인해야 한다」를
   README 나 Makefile 도움말에 한 줄로 남겨라 — 다음 사람이 같은 데서 막힌다
```

## 2. 검증

```bash
cd app/front && npx tsc --noEmit          # 0 에러
cd app/front && npx vitest run            # 통과 · Errors 줄 0
cd app/front/src-tauri && cargo check     # Rust 쪽을 고쳤으면
```

**`tauri build` 로 한 번 구워라**(macOS). 구운 `.app` 의 `Info.plist` 에
`NSMicrophoneUsageDescription` 이 실제로 들어갔는지 `PlistBuddy` 로 확인하고 결과를 보고에 붙여라.

```bash
/usr/libexec/PlistBuddy -c "Print :NSMicrophoneUsageDescription" <경로>/Contents/Info.plist
```

**앱 창을 열어 마이크를 실제로 물어보는 것까지는 하지 마라** — 사용자가 확인한다.
**Windows 는 이 기계에서 확인할 수 없다.** 코드와 근거만 남기고 「실물 확인 필요」로 보고해라.

## 3. 지킬 것

1. **이 건만 고쳐라** — 마이크 권한. 회의록 로직·화면을 건드리지 마라
2. **문서를 고치지 마라**(README·Makefile 한 줄 추가는 허용 — §1-3)
3. **커밋·push 하지 마라**
4. **Tauri API 를 지어내지 마라.** 확인하고 쓰고, 못 찾으면 보고해라
5. 막히면 물어라 — `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "..." --enter`

## 4. Done Criteria

- [ ] macOS — 구운 `.app` 의 `Info.plist` 에 `NSMicrophoneUsageDescription` 이 있다(PlistBuddy 출력 첨부)
- [ ] Windows — WebView2 `PermissionRequested` 로 마이크를 허용하는 코드가 있거나, **못 한 이유**가 보고에 있다
- [ ] `tauri dev` 에서 왜 안 되는지가 한 줄로 남았다
- [ ] `tsc` 0 · `vitest` 통과 · `Errors` 0 · `cargo check` 통과
- [ ] 회의록 로직·화면 변경 0 · 커밋 없음

## 5. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_28a436b1-4e1e-402f-8510-12e87d4b8ffb \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "Tauri 마이크 권한 완료" \
  --body "macOS 에 넣은 것(파일·키·문구)과 PlistBuddy 출력 / Windows 에 넣은 것 또는 못 한 이유 / tauri dev 제약 한 줄을 어디에 남겼나 / tsc·vitest·cargo check 결과 / **사용자가 실물로 확인할 절차**(어떤 명령으로 굽고 어디를 눌러야 권한이 뜨는지) / 범위 밖이라 안 한 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] Tauri 마이크 권한 완료. 상세는 인박스." --enter
```
