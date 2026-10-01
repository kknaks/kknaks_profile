# WORK-001 P4·P5 결과 보고

## 상태: done — 저장 대화상자·링크 열기의 **눈 확인은 사용자 몫(pending)**, Windows 실기 빌드는 A-9(사용자)

커밋·push·PR 없음. 변경은 `reference/2026-09-09-sc-prototype/desktop/` 안뿐이다(`git status` 로 확인).

## 수행 — 파일

| 파일 | 내용 |
|---|---|
| `src/bridge.js` (새 파일) | SPEC §5 의 세 곳. ① `checkRank` — `invoke` 의 reject 문자열을 `Error` 로 감싼다(빈 문자열이면 PoC `'조회에 실패했습니다.'`). 180초 `Promise.race` 로 상한을 두고, 넘기면 `name = 'TimeoutError'` 인 Error 를 던진다 → `main.jsx:66` 의 기존 catch 가 「조회 시간이 초과되었습니다.」를 낸다. `check_place` Err 도 같은 catch 로 가서 오류 행이 된다. ② `saveWorkbook` — `export_xlsx` 를 부른다. 취소는 조용히 끝나고, 모든 실패는 「엑셀을 저장하지 못했습니다. 다시 시도해 주세요.」. ③ 모듈 로드 때 document 캡처 단계에서 `a[target="_blank"]` 클릭을 가로채 `openUrl`(tauri-plugin-opener)로 연다 |
| `src/main.jsx` | 바뀐 줄 **셋뿐**: bridge `import` 1줄 추가 · 조회 호출부(`fetch`+`res.json`+`!res.ok`+`result=data` 4줄 → `checkRank` 1줄) · 저장부(`fetch`~`a.click()` 4줄 → `saveWorkbook` 1줄). catch 줄·문구·스타일·기본 키워드·`<a>` 는 diff 0. `style.css`·`vendor/`·`index.html` 은 PoC 와 동일 |
| `package.json`·`package-lock.json` | + `@tauri-apps/plugin-opener` ^2 |
| `src-tauri/src/commands.rs` | `export_xlsx` 구현: 검증(Err `index.mjs:45`) → 워크북(실패 Err `index.mjs:51`) → 저장 대화상자(`.xlsx` 필터, 기본 파일명) → 취소면 `{saved:false}` → 쓰기(실패 Err `index.mjs:51`) → `{saved:true, path}` + `[export]` 로그. 대화상자는 콜백 + oneshot 이라 비동기 런타임을 막지 않는다. `NOT_IMPLEMENTED` 삭제 — 「아직 구현되지 않은」 문구가 코드 어디에도 없다(grep 0건) |
| `src-tauri/src/workbook.rs` | + `default_file_name(now)` — `네이버_키워드순위_YYYY-MM-DD.xlsx`, 한국 날짜 |
| `src-tauri/tests/workbook.rs` | + 기본 파일명 테스트: UTC 15:30 → 다음 날 KST, 14:59:59 → 같은 날 |
| `README.md` (새 파일) | P5 — 아래 |

**`import` 줄에 대해.** 계약은 「바뀌는 줄은 fetch 호출부·다운로드부뿐」이다. 그런데 `index.html` 은 무변경이고 진입 모듈이 `main.jsx` 하나라서, 링크 가로채기를 진입부에 넣고 bridge 를 불러오려면 import 1줄이 꼭 필요하다. 이것만 더했다.

## 앱 확인 (사용자 실행, 워커는 로그·파일·pgrep 만)

이 세션에는 macOS 손쉬운 사용 권한이 없어 웹뷰 요소를 조작할 수 없었다(요소 0개). 코디 결정으로 사용자가 직접 확인했고, 그 뒤 GUI 자동화·창 조회는 금지됐다.

- **조회:** 앱 로그 기준으로 플레이스 3개(09:02:15~09:02:38 UTC) · 블로그 19개(09:03:46~09:04:49 UTC). 오류 행 없음(`stage:"error"` 0건). 첫 조회 때 Edge 를 한 번 띄웠고 이후 재사용했다(`launched` 1줄).
- **저장:** 로그 `[export] {"saved":true,"path":"/Users/kknaks/Documents/네이버_키워드순위_2026-09-30.xlsx"}`(09:02:56 UTC). 저장은 플레이스 조회 뒤 한 번뿐이다. 블로그 조회 뒤에는 `[export]` 줄이 없다.
- **저장 파일 머리행과 행** (zip XML 을 직접 읽음):
  ```
  1 키워드 | 상태 | 전체 순위 | 광고 제외 순위 | 페이지 | 확인 업체 수 | 광고 수 | 타겟 병원명 | 매칭 상호 | 조회 시각 (한국) | 조회 기준 | 검색 URL | 안내
  2 강남역성형외과   | 노출 | 69  | 53  | 1 | 88  | 18 | 무이성형외과 | 무이성형외과의원 | 2026-09-30 18:02:19 | …
  3 강남성형외과     | 노출 | 163 | 145 | 3 | 228 | 18 | 무이성형외과 | 무이성형외과의원 | 2026-09-30 18:02:29 | …
  4 신논현역성형외과 | 노출 | 226 | 208 | 3 | 228 | 18 | 무이성형외과 | 무이성형외과의원 | 2026-09-30 18:02:38 | …
  autoFilter A1:M4 · 틀 고정 · creator SCAX
  ```
  기본 파일명(한국 날짜)이 그대로 쓰였다. 순위는 숫자, 시각은 KST 다. 강남역성형외과는 코디 대조값(69 · 53 · 88 · 18)과 같다.
- **pending — 사용자 눈 확인:** 저장 대화상자의 모양(`.xlsx` 필터 표시), 취소했을 때 메시지가 없는지, 「네이버」·「매칭 글」 링크가 OS 기본 브라우저로 열리는지. 링크 열기는 로그를 남기지 않아 워커가 확인할 수단이 없다.

### A-8 (앱 쪽)
사용자가 창을 닫은 뒤:
- `pgrep -f sc-rank-cdp-` → **없음**
- `$TMPDIR/sc-rank-cdp-*` → **없음**
- 로그 마지막 줄: `[browser] {"stage":"closed","profileRemoved":true}` (23:22:16 UTC)
- `tauri dev`·vite 프로세스도 창과 함께 끝났다. 워커가 따로 끈 프로세스는 없다.

### 로그 09:14 「CDP connection ended」 원인
```
[2026-09-30][09:14:28][sc_rank_lib::browser][WARN] [browser] CDP connection ended: WebSocket protocol error: Connection reset without closing handshake
```
- 로그 시각은 UTC 다. 09:14:28 UTC = **18:14:28 KST**. 마지막 조회(09:04:49 UTC)에서 약 9분 반 뒤라 조회 중이 아니었다(유휴).
- `pmset -g log` 의 같은 시각 기록: `18:14:25 Display is turned off` → `18:14:30 Entering Sleep state due to 'Clamshell Sleep'`(덮개 닫힘). 18:18:11 에는 `Delays to Sleep notifications: [Microsoft Edge is slow(3063 ms)]` 도 있다.
- Edge 충돌 보고서(`~/Library/Logs/DiagnosticReports`)는 없고, Edge 업데이트도 없었다(프레임워크 154.0.4258.48 은 9/29 설치 그대로).
- **원인: Mac 이 잠들면서 유휴 헤드리스 Edge 와의 CDP WebSocket 이 끊겼다.** 코드 결함이 아니다. 설계대로 동작했다 — 핸들러가 연결을 죽은 것으로 표시했고, 창을 닫을 때 정리가 정상으로 끝났다(프로필 삭제, 잔여 프로세스 없음). 다음 조회가 있었다면 `open_context` 가 브라우저를 다시 띄운다(SPEC §3 「끊기면 다음 조회에서 다시 띄운다」). 이번에는 그 뒤 조회가 없어 재기동 경로는 실측하지 못했다.

## P5 — `desktop/README.md`

- **macOS 개발:** 사전 요건(Rust 1.97, 최소 1.85 · Node 20 LTS · Xcode CLT · Edge/Chrome) · `npm install` / `npm run tauri dev`(13100) / `npm run build` / `cargo test` / `cargo clippy` · smoke 3종(요청 간격 주의).
- **Windows 빌드:** VS 2022 Build Tools 17.x 「C++를 사용한 데스크톱 개발」(MSVC v143 + Windows SDK) · Rust MSVC 툴체인 · Node 20 LTS · WebView2 Evergreen · Edge. 명령은 `npm install` → `npm run tauri build`. 산출물은 `src-tauri\target\release\bundle\nsis\SC Rank_0.1.0_x64-setup.exe`.
- **NASM:** 조사해 보니 `aws-lc-sys` 0.45 는 x64 Windows 에서 NASM 으로 어셈블리를 빌드한다. 미리 빌드된 객체는 `prebuilt-nasm` 기능이나 `AWS_LC_SYS_PREBUILT_NASM=1` 이 있을 때만 쓰고, 우리 의존 트리는 이 기능을 켜지 않는다(`cargo tree -e features` 로 확인). 그래서 README 는 `$env:AWS_LC_SYS_PREBUILT_NASM = "1"`(또는 NASM 설치)을 명령에 넣었다. **Windows 실기에서는 아직 확인하지 않았다고 README 에 표시했다.**
- **설치·첫 실행:** SmartScreen 「추가 정보 → 실행」(D-10, 서명 없음).
- **조회 실패 안내:** Edge·Chrome 그룹 정책 `RemoteDebuggingAllowed = 0` 이면 조회가 폴백 문구로 실패한다. 확인 방법(`edge://policy`, 레지스트리 경로)과 함께, Edge 가 설치돼 있으면 Chrome 으로 넘어가지 않는다는 점을 적었다.
- **로그 위치:** Windows `%LOCALAPPDATA%\com.summerstar.scrank\logs\sc-rank.log` · macOS `~/Library/Logs/com.summerstar.scrank/sc-rank.log`(실측).

### `cargo check --target x86_64-pc-windows-msvc` — 실패, 사유 있음
- `rustup target add x86_64-pc-windows-msvc` 는 됐다.
- check 는 `aws-lc-sys` 빌드 스크립트에서 멈춘다: `fatal error: 'stdlib.h' file not found` · `'windows.h' file not found`. MSVC·Windows SDK 헤더가 필요한 C 컴파일이라 macOS 에서는 불가능하다.
- 우리 Rust 코드는 그 앞에서 멈춰 타입 검사되지 않았다. `cfg(windows)` 경로(`browser::default_candidates`)는 **Windows 실기 빌드(A-9)에서 처음 컴파일된다.**

## 검증

| 명령 | 결과 |
|---|---|
| `cargo fmt --check` | 통과 (사용자 확인 중에는 fmt 를 보류했다 — `src-tauri/src` 를 고치면 dev 앱이 재시작되기 때문. 창을 닫은 뒤 적용) |
| `cargo test` | **38 passed / 0 failed** (P3 37 + 기본 파일명 1) |
| `cargo clippy --all-targets -- -D warnings` | 0 |
| `npm run build` | 성공 |
| 네이버 요청 | 워커는 0건. 사용자 GUI 확인에서 플레이스 3 · 블로그 19 |

## 이슈 · 코디가 확인할 것

1. **사용자 눈 확인 pending:** 저장 대화상자 · 취소 무메시지 · 링크가 OS 브라우저로 열림 (A-6 나머지).
2. **Windows:** NASM 처리(`AWS_LC_SYS_PREBUILT_NASM=1`)와 `cfg(windows)` 경로 모두 실기 빌드 전에는 확인되지 않는다 — A-9.
3. **덮개를 닫아 잠든 뒤의 재기동 경로는 실측하지 못했다.** 필요하면 사용자가 잠자기 → 깨우기 → 조회 1회로 확인한다. 로그에 `launched` 가 한 줄 더 찍히면 정상이다.
4. **`import` 1줄** — 위 설명. 코드 검수에서 「§5 외 변경」으로 볼지 판단해 달라.
