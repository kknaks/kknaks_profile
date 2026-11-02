# @sc-rank-desktop — 규칙

## 이식 규칙
- 판정·문구·제한값·타임아웃은 PoC 와 **같게**. 「더 낫게」 바꾸지 않는다 — 바꿀 이유가 보이면 보고한다.
- `place-dom.mjs` 의 페이지 안 JS 는 Rust 로 다시 짜지 않고 주입한다(`include_str!`). 원본 파일을 고치지 말고 레포의 `src-tauri/js/` 로 복사해 쓴다.
- PoC 단위 테스트는 **같은 단언**으로 Rust 에 옮긴다. 단언을 약하게 만들지 않는다(빈 단언·`is_ok()` 만 보는 테스트 금지).
- 조회 실패를 「미노출」로 떨어뜨리는 폴백 금지 — PoC 가 error 로 두는 자리는 error.

## Rust
- edition 2021, `cargo fmt`. `unwrap`/`expect` 는 테스트와 불변식에만. 오류는 `thiserror`/`anyhow`.
- 비동기 tokio(Tauri 런타임). OpenSSL 의존 크레이트 금지 — `reqwest` 는 rustls.
- Windows 전용 경로는 `cfg(windows)` 로 분기하고 macOS 에서도 컴파일되게 둔다.

## 안전
- 사용자 브라우저 프로필·실행 중 브라우저를 건드리지 않는다. 헤드리스는 전용 임시 프로필.
- 앱 종료 시 자식 브라우저 프로세스를 정리한다.
- 실수집은 Phase 끝에 1회. 반복 호출로 네이버 차단을 부르지 않는다.

## 스코프
- 레포 밖 수정 금지. 커밋·push·PR 금지.

## 리포트 형식 (브리프가 지정한 경로)
```markdown
# WORK-001 <Phase> 결과 보고
## 상태: done / in-progress / blocked
## 수행 — 파일·모듈 목록
## 검증 — 명령과 수치 (cargo test N passed 등) · 실수집 결과 로그
## PoC 대조 — SPEC-001 §4 항목별 같음/다름
## 이슈 · 코디가 확인할 것
```
