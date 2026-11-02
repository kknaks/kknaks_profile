# @mykakao-winapp — 기술 스택

- Rust 2021 (rustc/cargo 1.98, MSVC host). cargo 는 `~/.cargo/bin`.
- axum + tokio (localhost HTTP + SSE) · serde/serde_json
- rusqlite (feature `bundled` — 평문 SQLite 저장 + 복호 후 열람)
- 순수 Rust 크립토: `aes`·`cbc`·`hmac`·`sha2`·`pbkdf2` (SQLCipher v4 페이지 복호)
- `windows` crate (OpenProcess/ReadProcessMemory/VirtualQueryEx — passive 메모리 키 회수)
- `notify` crate (ReadDirectoryChangesW — chat_data -wal 파일 감시)
- (P3) `tray-icon` crate

## 핵심 원칙
- 최소 크레이트 · OpenSSL 빌드 회피 · 원본 읽기만 · 키/본문 비노출 · 카톡 무변조
