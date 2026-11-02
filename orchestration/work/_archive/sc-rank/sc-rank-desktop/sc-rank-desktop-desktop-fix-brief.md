
# [desktop] 코드 검수 WARN 수정 — W-1 · W-2 · W-4

너는 **sc-rank `desktop` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/roles/sc-rank/desktop/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 앞 맥락이 없다 — 아래 파일이 전부다. 이 워크트리는 너 혼자 쓴다. **이번 판은 검수 수정 셋뿐**이다. P1~P5 는 끝나 있다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/review-code-report.md` — **W-1 · W-2 · W-4** 절 (근거·파일:줄·방법이 거기 있다)
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/20-spec/spec-001-desktop-app.md` §3·§4

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

코드 검수 FAIL 0 · WARN 6. 코디 판정: W-1·W-2·W-4 는 PR 전에 고친다. W-3 은 W-2 를 고치면 macOS 에서 확인 가능해진다. W-5·W-6 은 기록만(코디).

## 3. 계약

- **W-1**: 페이지 루프 안 `frame()` 실패는 PoC 처럼 `ScrapeError` Other → 플레이스 폴백 문구. 「플레이스 검색 프레임을 읽지 못했습니다.」 Domain 은 목록 준비 직후 한 곳(`place.mjs:68` 대응)만.
- **W-2**: rustls 암호 제공자를 `ring` 으로. `aws-lc-rs`·`aws-lc-sys` 가 `Cargo.lock` 에서 사라져야 한다(`cargo tree -i aws-lc-sys` 빈 결과). README 의 NASM·`AWS_LC_SYS_PREBUILT_NASM` 절을 지우고 Windows 사전 요건을 맞춘다.
- **W-4**: 기동 시 잔여 정리는 이름의 pid 가 **살아 있지 않은** `sc-rank-cdp-*` 만 지운다. 단위 테스트 1개(살아 있는 pid 는 남고 죽은 pid 는 지워짐).

## 4. 먼저 읽을 핵심 파일

- `desktop/src-tauri/src/place.rs:378-471` · `desktop/src-tauri/Cargo.toml:37` · `desktop/src-tauri/src/blog.rs:643` 근처 · `desktop/src-tauri/src/browser.rs:93-149` · `desktop/README.md`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `reference/2026-09-09-sc-prototype/desktop/`
- 리포트 파일 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/report-desktop-fix-review.md`

## 6. 구현 단계

1. W-1 · W-2 · W-4.
2. `rustup target add x86_64-pc-windows-msvc` 후 `cargo check --target x86_64-pc-windows-msvc` — **이번엔 통과해야 한다**(W-3). 안 되면 멈춘 크레이트·사유 보고.
3. verify(test·clippy·build) 1회.
4. 썸네일 HTTPS 재확인: `cargo run --example smoke -- blog 구월동피부과 image tests/fixtures/1.png` **1회** — 오류 아님.
5. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/report-desktop-fix-review.md` 에 — 항목별 변경·명령 출력.

## 7. 범위 제약 — 하지 말 것

- 위 셋 밖의 변경 금지. GUI 자동화(osascript·System Events·screencapture) 금지. 커밋·push·PR 금지.

## 8. 검증

```
desktop/src-tauri 에서 cargo test · cargo clippy --all-targets -- -D warnings, desktop 에서 npm run build. Phase 범위에 맞게 1회씩 — 통과하면 반복하지 마라. 실수집(네이버 요청)은 Phase 끝에 1회만, 요청 간격 규칙을 지킨다. 사용자 포트·프로세스·브라우저 프로필을 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_4d2a12b8-e3cf-45de-a097-daa193cfd908 --from term_5065cf30-3784-4dae-bfa5-2e4934c0468e \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "desktop 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4d2a12b8-e3cf-45de-a097-daa193cfd908 \
  --text "[worker_done] desktop 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4d2a12b8-e3cf-45de-a097-daa193cfd908 --text "[질문] desktop: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
