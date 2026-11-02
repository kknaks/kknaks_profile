# 코드 검수 WARN 수정 결과 — W-1 · W-2 · W-4

## 상태: done

코드 검수 WARN 셋(W-1·W-2·W-4)만 고쳤다. W-3 은 W-2 덕에 확인 범위가 넓어졌다 — 아래 §W-3.
커밋·push·PR 없음. 변경은 `reference/2026-09-09-sc-prototype/desktop/` 안뿐(`git status` 확인). GUI 자동화 없음.

## W-1 — 루프 안 프레임 실패는 폴백 문구로

- `src-tauri/src/place.rs`: 루프에서 쓰는 `frame()` 이 프레임을 못 찾으면 `ScrapeError::other("Cannot read properties of undefined (reading 'evaluate'): searchIframe frame missing")` 을 낸다 → 플레이스 폴백 「플레이스 조회에 실패했습니다…」. PoC 에서 `frame()` 이 `undefined` 일 때 나는 TypeError 에 대응한다.
- 도메인 문구 「플레이스 검색 프레임을 읽지 못했습니다.」는 목록 준비 직후(`place.mjs:68` 대응) **한 곳에서만** 낸다. `grep` 결과 코드 전체에서 1곳(`place.rs:394`).

## W-2 — rustls 암호 제공자를 ring 으로

- `src-tauri/Cargo.toml`:
  - `reqwest` 기능 `rustls` → `rustls-no-provider`.
  - 직접 의존 `rustls = { version = "0.23", default-features = false, features = ["ring", "std", "tls12", "logging"] }` 추가.
- `src-tauri/src/blog.rs`: `HTTP` 클라이언트를 만들기 전에 `rustls::crypto::ring::default_provider().install_default()`. 이미 설치돼 있으면 무시한다. `rustls-platform-verifier` 도 이 기본 제공자를 쓴다.
- 결과:
  ```
  $ cargo tree -i aws-lc-sys
  error: package ID specification `aws-lc-sys` did not match any packages
  $ cargo tree -i aws-lc-rs
  error: package ID specification `aws-lc-rs` did not match any packages
  $ grep -c 'aws-lc' Cargo.lock
  0
  ```
- ring 0.17.14 는 NASM 이 필요한 어셈블리를 미리 빌드된 객체로 싣고 있다(`pregenerated/*-nasm.o` 24개, `build.rs:435-442` 「Nasm was already used to generate the object files」). 그래서 Windows 에는 MSVC(Build Tools)만 있으면 된다.
- `README.md` §2:
  - NASM·`AWS_LC_SYS_PREBUILT_NASM` 절과 PowerShell 환경변수 줄을 지웠다. 「`ring` 이 MSVC 로 C 를 컴파일 · NASM·CMake 불필요」로 고쳤다.
  - 「Windows 실기 빌드로 아직 확인하지 않았다」 한 줄은 남겼다(A-9 전까지 사실).
  - 편집 중 사전 요건 표의 Edge 행이 잘리는 실수가 있었다. 복원하고 README 전체를 다시 읽어 확인했다.
- **썸네일 HTTPS 재확인(smoke 1회)**: 오류 아님, 썸네일 160개 전부 비교(다운로드 실패가 있었다면 「일부 썸네일을 읽지 못해…」 오류가 났을 것이다).
  ```
[browser] {"stage":"launched","executable":"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"}
[blog] {"keyword":"구월동피부과","stage":"batch","scrolls":0,"total":30}
[blog] {"keyword":"구월동피부과","stage":"images-start","images":70,"concurrency":8}
[blog] {"keyword":"구월동피부과","stage":"batch","scrolls":1,"total":60}
[blog] {"keyword":"구월동피부과","stage":"images-start","images":30,"concurrency":8}
[blog] {"keyword":"구월동피부과","stage":"batch","scrolls":2,"total":90}
[blog] {"keyword":"구월동피부과","stage":"images-start","images":30,"concurrency":8}
[blog] {"keyword":"구월동피부과","stage":"batch","scrolls":3,"total":120}
[blog] {"keyword":"구월동피부과","stage":"images-start","images":30,"concurrency":8}
[blog] {"keyword":"구월동피부과","stage":"complete","elapsedMs":9510,"rank":null,"total":120,"scrolls":3}
[browser] {"stage":"closed","profileRemoved":true}
{
  "keyword": "구월동피부과",
  "target": "1.png",
  "targetType": "image",
  "searchUrl": "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_hty.top&query=%EA%B5%AC%EC%9B%94%EB%8F%99%ED%94%BC%EB%B6%80%EA%B3%BC",
  "scope": "PC 네이버 블로그 탭 · 초기 목록 + 최대 3회 스크롤 · 검색 썸네일 pHash(거리 6 이하)",
  "status": "not_found",
  "rank": null,
  "matches": [],
  "total": 120,
  "comparedImages": 160,
  "scrolls": 3,
  "checkedAt": "2026-09-30T23:40:04.883Z",
  "message": "이번 블로그 탭 초기 목록 + 최대 3회 스크롤에서 찾지 못했습니다."
}
exit=0
  ```
  smoke 뒤 `pgrep -f sc-rank-cdp-` 없음 · `$TMPDIR/sc-rank-cdp-*` 없음.

## W-4 — 잔여 프로필은 죽은 pid 만 지운다

- `src-tauri/src/browser.rs`:
  - `remove_stale_profiles()` → `remove_stale_profiles_in(dir)`. 이름 `sc-rank-cdp-<pid>-<nanos>` 에서 pid 를 읽어 **살아 있으면 건너뛴다**. pid 를 못 읽으면 지운다.
  - `pid_alive` (unix): `libc::kill(pid, 0)`, EPERM 도 살아 있음으로 본다. pid 0·음수·i32 초과는 살아 있지 않음으로 본다 — `kill` 의 프로세스 그룹 의미를 피하려는 것.
  - `pid_alive` (windows): `OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION)` + `GetExitCodeProcess == STILL_ACTIVE`.
- `Cargo.toml`: `[target.'cfg(unix)'] libc 0.2` · `[target.'cfg(windows)'] windows-sys 0.61`. 둘 다 이미 의존 트리에 있던 판이다.
- 테스트 `tests/browser.rs::잔여_프로필은_죽은_pid_만_지운다`: 현재 프로세스 pid 폴더는 남고, 끝난 자식 프로세스 pid 폴더는 지워지고, 접두가 다른 폴더는 건드리지 않는다. 통과.
- `README.md` §4 에 「이름의 pid 가 아직 살아 있는 것은 남긴다」 한 줄을 더했다.

## W-3 — `cargo check --target x86_64-pc-windows-msvc`

1. **그대로는 macOS 에서 통과하지 않는다.** 멈춘 크레이트는 `ring v0.17.14`. 빌드 스크립트가 C 파일을 MSVC 대상으로 컴파일하는데 `fatal error: 'assert.h' file not found` 가 난다. MSVC C 런타임 헤더가 필요해서다. aws-lc-sys 때와 같은 종류의 벽이다(NASM 조건은 사라졌지만 C 헤더는 여전히 Windows SDK/MSVC 몫).
2. **Rust 코드 타입 검사는 통과시켰다.** `cargo check` 는 링크하지 않으므로, 네이티브 도구 셋(C 컴파일러·아카이버·리소스 컴파일러 `llvm-rc`)을 빈 파일만 만드는 스크립트로 대신하고 스크래치 폴더·별도 target 디렉터리에서 돌렸다. 산출물·저장소에는 아무것도 남기지 않았다.
   ```
   $ CC_x86_64_pc_windows_msvc=<fake-cc> AR_x86_64_pc_windows_msvc=<fake-ar> PATH=<fake llvm-rc>:$PATH \
     CARGO_TARGET_DIR=<scratch> cargo check --target x86_64-pc-windows-msvc --all-targets
       Finished `dev` profile [unoptimized + debuginfo] target(s)
   $ (같은 환경) cargo clippy --target x86_64-pc-windows-msvc --all-targets -- -D warnings
       Finished `dev` profile — 경고 0
   ```
   → lib·main·tests·examples 전부, `cfg(windows)` 경로(`browser::default_candidates`, 새 `pid_alive` 의 windows-sys 호출)까지 **Windows 타깃으로 타입 검사·clippy 가 통과했다.** 링크·실행·C 코드 컴파일은 여전히 A-9(Windows 실기) 몫이다.
   - 대체 컴파일러 스크립트(참고):
   ```sh
#!/bin/sh
# 타입 검사 전용: C 컴파일 대신 -o / -Fo 대상에 빈 파일만 만든다.
out=""; prev=""
for a in "$@"; do
  case "$prev" in -o) out="$a";; esac
  case "$a" in -Fo*) out="${a#-Fo}";; esac
  prev="$a"
done
[ -n "$out" ] && : > "$out"
exit 0
   ```

## 검증 (macOS, 1회)

| 명령 | 결과 |
|---|---|
| `cargo fmt --check` | 통과 |
| `cargo test` | **39 passed / 0 failed** (이전 38 + W-4 테스트 1) |
| `cargo clippy --all-targets -- -D warnings` | exit 0, 경고 0. 처음 실행 때는 기능 변경으로 의존성이 다시 빌드되면서 `warning` 으로 시작하는 줄 5개가 섞여 나왔는데, 그 줄은 보존하지 못했다. 다시 돌린 결과는 exit 0 에 우리 크레이트 경고 0 이다 |
| `npm run build` | 성공 |
| Windows 타깃 check·clippy (대체 도구) | 통과 — 위 §W-3 |
| 네이버 요청 | smoke 이미지 모드 1회 |

## 코디가 확인할 것

1. W-3: `cargo check --target x86_64-pc-windows-msvc` 가 **그대로는** 통과하지 않는다(ring C 헤더). Rust 타입 검사는 대체 도구로 통과시켰다. 이 방식을 인정할지 판단해 달라. 진짜 확인은 A-9.
2. W-2 로 Windows 사전 요건이 줄었다(NASM 없음). VS Build Tools 「C++ 데스크톱 개발」만 필요하다.
