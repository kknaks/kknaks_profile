# @sc-rank-desktop — 도구 및 구조

## 작업 위치
- 워크트리·base 는 브리프가 SSOT. 첫 액션: `git branch --show-current` → SPEC-001·WORK-001(브리프 §1 절대경로) 통독 → PoC `server/`·`src/`·`tests/` 정독.

## 레이아웃 (초안 — SPEC 우선)
```
desktop/package.json          vite + tauri cli
desktop/index.html
desktop/src/                  PoC src/ 사본 (main.jsx 의 호출부 두 곳만 변경)
desktop/src-tauri/Cargo.toml
desktop/src-tauri/tauri.conf.json
desktop/src-tauri/src/main.rs     명령 등록 · 종료 정리
desktop/src-tauri/src/commands.rs check_blog · check_place · export_xlsx · 가드
desktop/src-tauri/src/browser.rs  Edge→Chrome 탐색 · CDP 기동·재사용·정리
desktop/src-tauri/src/place.rs    수집 + 판정
desktop/src-tauri/src/blog.rs     수집 + 파싱 + 이미지 해시
desktop/src-tauri/src/workbook.rs
desktop/src-tauri/js/place-dom.js PoC place-dom.mjs 사본(주입용)
desktop/README.md             macOS 개발 · Windows 빌드 절차
```

## 명령
- `cd desktop && npm install && npm run tauri dev` (화면 확인) · `npm run build`
- `cd desktop/src-tauri && cargo test && cargo clippy --all-targets -- -D warnings`
- cargo 가 안 잡히면 `export PATH="$HOME/.cargo/bin:$PATH"`.

## 금지
- `desktop/` 밖 수정 · 커밋·push·PR · 사용자 포트/프로세스 종료.
