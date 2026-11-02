# [frontend] WORK-013 Phase WP4-SHELL — 셸 OS 알림 + 카톡 수집기 표지

WP3-FE 는 끝났다(검수는 WP2-BE 와 맞춘 뒤 함께). 이어서 **WP4-SHELL** 이다. 앞 브리프의 금지 · 보고 방식 그대로. **이번엔 `frontend/src-tauri/` 도 allowed_paths 다.**

- **할 일**: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/30-work/work-013-notifications.md` **「Phase WP4-SHELL」 절** 체크박스 + Code Surface **WP4 표** 전부 · 원칙 P-1~P-10
- **계약**: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md`(v0.7.0) · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-011-notifications.md` §2.5 · §4.6 · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-009-mac-kakao-collector.md`(v0.6.0)
- **P0 결과** `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/p0-report.md` — 그리고 **사용자 처분(2026-10-08)이 SPEC 보다 앞선다**(문서는 writer 가 병렬로 고친다):
  1. **OQ-1108 = ④** — **macOS 는 UNUserNotificationCenter 를 objc2(`objc2-user-notifications` 등 — 판 명시)로 셸이 직접 구현**: `requestAuthorization`(진짜 프롬프트) · 권한 상태 읽기(거부면 `notify_show` → `{shown:false}`) · 알림 보내기(`userInfo` 에 `notification_id` · `target`) · **delegate `didReceive` 기본 동작 = 클릭** → 창 보이기·포커스 → 기존 셸→웹 사건 길로 `strong-hajin:notification-click` · 앱이 앞에 있을 때도 배너가 뜨게 `willPresent`(생략 판단은 웹이 한다). **원격 웹에 플러그인 권한을 열지 않는다** — 우리 커맨드 둘만(`notify_permission` · `notify_show`)
  2. **Windows** 는 공식 `tauri-plugin-notification`(클릭 없음 — 앱만 앞으로 · 실기 pending) — `cfg(windows)` 로 가른다
  3. **tauri 를 2.12 로 올린다**(공식 플러그인 요구) — lock 갱신 · 두 판 `cargo test` 로 회귀 확인
  4. **UN 은 번들 id 가 있어야 한다** — dev(`tauri dev`)에서는 번들이 없으니 **panic 없이 조용히 `{shown:false}`** 로 떨어지게 · 실측은 서명 dmg 만(코디)
  5. **OQ-K01 닫힘** — 수집기가 업로드 줄에 `from_me = (authorId == NTChatContext.userId)` 를 싣는다(P0-1 의 그 이름 · 읽기 경로 그대로)
- **dmg 빌드 · 서명 · 공증은 하지 마라** — 코디가 E2E 직전에 한다(사용자 키체인). `make shell-build` 판마다는 된다(서명 없는 빌드)
- **검증 — 관련만**: WP4 「시험」 줄 그대로 — `make shell-verify` · `cargo test` **와** `cargo test --features kakao-collector` · `cargo clippy -- -D warnings`(두 판) · 고른 vitest 파일 · `npx tsc --noEmit`. 전체 금지
- ⚠ backend 워커가 `backend/` 에서 WP2-BE 마무리 중 — 건드리지 마라
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-wp4-report.md` — 체크박스별 파일:줄 · Code Surface 대비 · objc2 구현 요지(스레드·run loop·delegate 수명) · 시험 수치 · **실측 항목(코디 dmg 용 체크리스트)** · 미결

## 완료 보고 — 앞 브리프 §7 두 명령 그대로
subject 「frontend 완료: WP4-SHELL」 · text 「[worker_done] frontend WP4-SHELL 완료 — <한 줄>. 리포트 fe-wp4-report.md」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
