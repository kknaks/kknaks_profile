# WORK-001 P6 결과 보고 — 레포 분리 정리

## 상태: done (fresh clone 검증만 pending — 아래)

## 수행 — 파일·모듈 목록

워크트리 `/Users/kknaks/orca/workspaces/sc-rank/sc-rank-desktop` (브랜치 `kknaksss/sc-rank-desktop`, 커밋 안 함).

| 파일 | 변경 |
|---|---|
| `poc/place-dom.mjs` · `poc/place.mjs` · `poc/blog-browser.mjs` (신규) | kknaks_profile `d6954f0:reference/2026-09-09-sc-prototype/server/<f>` 를 `git show` 로 바이트 그대로 추출. 작업 트리 원본과 `cmp` 일치, 원본은 `d6954f0` 이후 변경 없음(`git diff --quiet d6954f0`) |
| `poc/README.md` (신규) | 출처(kknaks_profile 경로·커밋 `d6954f0`) · 「수정 금지 — 동일성 검사용」 · 읽는 테스트 이름 |
| `src-tauri/tests/collect_offline.rs` | `../../server/{place-dom,place,blog-browser}.mjs` → `../poc/…` (3곳). 단언 변경 없음 |
| `README.md` | ① 4행 `../server/`·`../src/` → 「kknaks_profile 레포 `reference/…/server/`·`src/`」, SPEC-001 경로도 「kknaks_profile 레포」 명시, `poc/` 안내 1줄 ② macOS `cd reference/…/desktop` → `git clone https://github.com/kknaksss/sc-rank.git` + `cd sc-rank` ③ Windows 동일(`git clone` 부터 시작) ④ 산출물 `desktop\src-tauri\…` → `src-tauri\…` ⑤ 폴더 트리 `desktop/` → `sc-rank/`, `poc/` 행 추가 ⑥ Windows 사전 요건 표에 Git 행(비공개 레포라 clone 시 GitHub 로그인 필요) |

sha256: place-dom.mjs `d6d52750…e450` · place.mjs `0495508b…4ae6` · blog-browser.mjs `69c94abf…1824`

### 레포 밖을 가리키던 곳 — grep 전수
`grep -rn -E '\.\./\.\./|\.\./server|\.\./src|reference/2026|desktop/|kknaks_profile|sc-prototype|/Users/' --exclude-dir={node_modules,target,.git,dist}`

| 위치 | 처리 |
|---|---|
| `collect_offline.rs:17,18,30` | `poc/` 로 |
| `README.md:4,5,27,75,79,121` | 위 표대로 |
| 남은 히트: `README.md:4`·`poc/README.md:10-12` | 의도된 출처 표기(레포 이름 명시) — 경로 의존 아님 |
| `capabilities/default.json` `../gen/schemas` · `tauri.conf.json` `../dist` · `src/*.rs` `include_str!("../js/…")` | 레포 안 상대경로 — 문제 없음 |
| Rust 주석의 PoC 인용(`place.mjs:4`, `index.mjs:35`, `server/workbook.mjs` 등) | 경로가 아닌 출처 인용이라 손대지 않음(문구 변경 0). `index.mjs`·`workbook.mjs`·`blog.mjs` 는 `poc/` 에 없음 — 브리프대로 테스트가 읽는 파일만 복사 |

## 검증 — 명령과 수치 (각 1회)

- `npm ci` — exit 0, found 0 vulnerabilities
- `cd src-tauri && cargo test` — exit 0, **39 passed / 0 failed** (lib 4 · blog 3 · blog_rules 8 · browser 3 · collect_offline 3 · place 9 · place_rules 2 · workbook 7; main·doctest 0)
- `cargo clippy --all-targets -- -D warnings` — exit 0, 경고 0
- 루트 `npm run build` — exit 0 (vite, `dist/assets/index-*.js` 206.46 kB)
- `git check-ignore poc/*` — 무시되지 않음(exit 1) → 커밋하면 clone 에 포함됨
- 실수집·앱 실행: 이번 판 범위 밖(동작 변경 0) — 하지 않음

**pending**: WORK-001 P6 완료 기준 「새 레포 clone 에서 통과」는 커밋·push 가 금지라 fresh clone 으로는 돌리지 못했다. 이 워크트리에서 레포 밖 경로 의존이 0 임을 grep 으로 확인했으니, 코디가 커밋 후 clone 에서 `cargo test` 1회 확인 바람.

## PoC 대조 — SPEC-001 §4

동작·판정·문구 변경 없음(코드 변경은 테스트의 읽기 경로 3곳뿐). 주입 JS 동일성 테스트는 `poc/` 사본 대상으로 통과 — 같음.

## 이슈 · 코디가 확인할 것

- README 의 Windows 사전 요건에 **Git 행을 추가**했다(clone 부터 시작하라는 계약을 따르려면 필요). 원치 않으면 그 한 줄만 빼면 된다.
- PoC 원본이 이후 바뀌면 `poc/` 를 다시 복사해야 한다(`poc/README.md` 에 적음).
