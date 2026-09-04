# @mykakao-winapp — 규칙

## Rust 규칙
- Rust 2021 edition. `cargo fmt` 스타일. 경고는 허용하되 `unsafe` 는 **꼭 필요한 곳(메모리 회수)에만** + 안전성 주석.
- 에러는 `anyhow`/`thiserror`. panic 을 정상 경로에 두지 않는다.
- 비동기 = tokio. 웹 = axum. 직렬화 = serde.

## 복호 전략 (중요 — OpenSSL 빌드 지옥 회피)
- **키는 메모리에서 회수한 raw key(32B)** 다 — passphrase KDF 로 main key 를 만들 필요 없다.
- **권장**: SQLCipher v4 페이지를 **순수 Rust 크립토로 복호**(`aes`+`cbc`+`hmac`+`sha2`+`pbkdf2`)해서
  **평문 SQLite 로** 떨군 뒤 `rusqlite`(feature `bundled`, 평문 — cipher/OpenSSL 불필요)로 연다.
  - 이유: `bundled-sqlcipher-vendored-openssl` 은 Windows 에서 OpenSSL(Perl/NASM) 컴파일이 필요해 지옥이다.
  - SQLCipher v4 파라미터(KEY_REPORT.md): compat 4, page 4096, reserve 80(IV16 끝 + HMAC-SHA512 64),
    HMAC key = `PBKDF2-HMAC-SHA512(raw_key, salt⊕0x3a, 2, 32)`, page IV = 각 페이지 reserve 앞 16B(AES-256-CBC).
- 이 전략이 막히면 **구현 전에 코디에 보고**하고 대안(rusqlite bundled-sqlcipher) 상의.

## 안전 규칙 — 이 프로젝트 고유 (불변)
- 카톡 원본 DB·레지스트리 **읽기만**. 복호는 **사본**(임시, 작업 후 삭제).
- **카톡 프로세스를 크래시·변조·종료하지 않는다.** 메모리는 `ReadProcessMemory` **읽기만**(쓰기·주입 금지). SAC 미변경.
- **키·user_id·device UUID·대화 본문·계정 식별자**를 로그·테스트·리포트·커밋에 남기지 않는다. 값은 `<redacted>`/마스킹.
- 우리 SQLite 는 로컬 저장 — 외부 전송 없음. 계정 폴더 해시는 **자동 탐색**(하드코딩 금지).

## 스코프 규칙
- `win_app/` 밖 수정 금지. 문서 SoT(kknaks_profile `para/…`)는 read-only — 코디 소유.
- SPEC-003 의 API 계약(경로·응답 키·SSE 이벤트명)을 임의로 바꾸지 않는다 — 어긋나면 보고.

## 리포트 형식
```markdown
# WORK-003 P1 결과 보고
## 상태: done / in-progress / blocked
## 수행 — win_app 구조·모듈·API 구현 목록
## 검증 — cargo build/test 수치 · 실기동으로 코디가 확인할 것
## 계약 준수 — SPEC-003 API/스키마 일치 여부
## 이슈/블로커
```
