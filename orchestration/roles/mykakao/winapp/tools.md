# @mykakao-winapp — 도구 및 구조

## 작업 디렉토리
- 실제 위치·base 는 dispatch brief 의 `작업 워크트리`·`base 브랜치`가 SSOT.
- **첫 액션**: 워크트리에서 `git branch --show-current` → SPEC-003(브리프 §1 절대경로) 통독 → spike3 참조 코드 읽기.

## win_app 레이아웃 (초안 — 브리프/spec 우선)
```
win_app/Cargo.toml
win_app/src/main.rs      # 기동: axum 서버 + (P3) 트레이
win_app/src/server.rs    # axum 라우터 · API · SSE · ui/ 정적 서빙
win_app/src/kakao/mod.rs # 카톡 경로 탐색 · 방 목록
win_app/src/kakao/memkey.rs   # ReadProcessMemory 키 회수 + SQLCipher v4 HMAC 검증
win_app/src/kakao/decrypt.rs  # 순수 Rust 페이지 복호 → 평문 SQLite
win_app/src/store.rs     # rusqlite 축적 DB (room/message/author)
win_app/src/watch.rs     # (P2) notify 파일 감시
win_app/ui/index.html    # 설정 3섹션 + 2-pane
```

## 참조 (read-only — 알고리즘 포팅 원천)
- spike3 Python: 브리프 §1 의 절대경로. `key_recover.py`(메모리 회수+HMAC 검증)·`key_analysis.py`(복호·행수)·`KEY_REPORT.md`(파라미터 정본).

## 명령
- `cd win_app && cargo build` · `cargo test <파일>` · `cargo run` (실기동은 코디)
- cargo 가 안 잡히면 `export PATH="$HOME/.cargo/bin:$PATH"`.

## 금지
- `win_app/` 밖·문서 SoT 수정 금지. git commit·push·PR 금지. 카톡 원본 쓰기·프로세스 변조 금지.
