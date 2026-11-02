# @sc-rank-desktop — 도구 및 구조

## 작업 위치
- 워크트리·base 는 브리프가 SSOT. 첫 액션: `git branch --show-current` → SPEC-001·WORK-001(브리프 §1 절대경로) 통독 → PoC `server/`·`src/`·`tests/` 정독.

## 레이아웃 (초안 — SPEC 우선)
```
./package.json          vite + tauri cli
./index.html
./src/                  PoC src/ 사본 (main.jsx 의 호출부 두 곳만 변경)
./src-tauri/Cargo.toml
./src-tauri/tauri.conf.json
./src-tauri/src/main.rs     명령 등록 · 종료 정리
./src-tauri/src/commands.rs check_blog · check_place · export_xlsx · 가드
./src-tauri/src/browser.rs  Edge→Chrome 탐색 · CDP 기동·재사용·정리
./src-tauri/src/place.rs    수집 + 판정
./src-tauri/src/blog.rs     수집 + 파싱 + 이미지 해시
./src-tauri/src/workbook.rs
./src-tauri/js/place-dom.js PoC place-dom.mjs 사본(주입용)
./README.md             macOS 개발 · Windows 빌드 절차
```

## 명령
- `npm install && npm run tauri dev` (화면 확인) · `npm run build`
- `cd src-tauri && cargo test && cargo clippy --all-targets -- -D warnings`
- cargo 가 안 잡히면 `export PATH="$HOME/.cargo/bin:$PATH"`.

## 금지
- 레포 밖 수정 · 커밋·push·PR · 사용자 포트/프로세스 종료.
