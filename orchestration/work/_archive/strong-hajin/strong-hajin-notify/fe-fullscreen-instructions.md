# [frontend] 버그 — 전체화면 나갔다 다시 들어가면 아래가 빈 공간 (사용자 2026-10-10 · medi-ax 서명 dmg `3321504`)

「메시지」 세 곳(`fe-label-fix2-instructions.md`)을 **끝낸 다음에** 이어서 한다. 같은 브랜치 `kknaksss/strong-hajin-notify-label`.

## 증상
macOS 앱(medi-ax)에서 전체화면 → 나가기 → 다시 전체화면. 그러면 화면 아래 약 110px 이 흰 빈 공간이다(사이드바 배경도 그 위에서 끊긴다 — 문서 높이가 창보다 짧다). 홈 화면에서 재현(사용자 캡처).

## 먼저 원인을 가른다 (고치기 전에 리포트에)
1. **셸(웹뷰 크기)인가** — 창 크기 변화 뒤 WKWebView 프레임이 창을 다 덮나. 이번 판에 **tauri 2.11.6 → 2.12.1**(tao · wry 포함 65 크레이트, WP4 검수 W-2 「회귀 실측」)을 올렸다 — **업그레이드 회귀 가능성이 1순위.** wry/tao 의 해당 판 변경 기록·이슈(전체화면 · resize · 웹뷰 bounds)와 우리 `src-tauri` 의 창 설정(`tauri.conf.json` 오버레이 · `lib.rs` 창 만들기 · `shell_ui.rs`)을 본다
2. **화면(CSS)인가** — 앱 셸 높이를 `100vh` 류 · JS 로 잰 고정 높이로 잡는 자리를 grep(`100vh` · `innerHeight` · `--app-height` 류). 전체화면 전환 때 `resize` 가 오는가
3. 이전 판(2.11.6 · `d2a06fa`)에서는 안 났는지 — 코드로 판단할 수 있는 만큼(실행은 코디·사용자)

## 고치기
- 원인 쪽에서 고친다. 셸이면 창 resize/전체화면 사건에 웹뷰 bounds 를 맞추는 최소 수정 또는 판 고정(근거와 함께) · CSS 면 동적 높이(`100dvh`/`height:100%` 사슬)
- 시험: 가능한 단위 시험 + cargo 두 벌(`cargo test` · `SHELL_FLAVOR=medi-ax cargo test --features kakao-collector`) · clippy · 고친 vitest · tsc. 실물(전체화면 왕복)은 코디가 dmg 로
- 사용자 포트·앱 실행 금지 · 커밋 금지
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-fullscreen-report.md` — 원인(근거 링크·파일:줄) · 고친 것 · 시험 · 코디 실측 절차
- 완료 보고 앞 브리프 §7 두 명령 — subject 「frontend 완료: 전체화면 빈 공간」 · text 「[worker_done] frontend 전체화면 빈 공간 완료 — <원인 한 줄>」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
