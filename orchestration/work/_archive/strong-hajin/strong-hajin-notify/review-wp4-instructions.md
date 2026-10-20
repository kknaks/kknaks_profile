# [reviewer] 코드 검수 — WP4-SHELL (셸 OS 알림 · 카톡 수집기 표지)

읽기 전용 · 판정(PASS/WARN/FAIL)과 근거만.

- 대상: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify` — `frontend/src-tauri/` 전부 · `frontend/src/lib/{shell.ts,osNotifier.ts,currentView.ts}` · WP4 가 손댄 화면 자리(`App.tsx` 권한 묻기·클릭 이동 · `MyWorkPage` · `InboxPage` · `MeetingWorkspace` · `SettingsPage` 의 현재 보기 알림) · `package.json`/lock · `Cargo.toml`/lock. ⚠ backend 워커가 `backend/` 손질 중 — 대상 아님
- 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/30-work/work-013-notifications.md` 「Phase WP4-SHELL」 · Code Surface WP4 · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md`(v0.7.1) · `spec-011`(v0.2.4) §2.5 · §4.6 · `spec-009`(v0.6.1) · **사용자 처분** `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/_RESUME.md` §2 「P0 처분」 행(④ macOS UN objc2 직접 · Windows 공식 플러그인 · tauri 2.12 · dev 는 `{shown:false}` · OQ-K01)
- 워커 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-wp4-report.md` · P0 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/p0-report.md` · 코디 관문: cargo medi-ax 98 · strong-hajin 77 통과 · vitest 30 통과

## 볼 것
1. **objc2 UN 구현의 안전** — delegate 수명(해제되면 클릭을 못 받는다) · 메인 스레드/run loop · `requestAuthorization` 콜백 스레드 · 번들 id 없을 때 panic 없음 · `unsafe` 블록의 근거 · 메모리 누수 · 앱이 떠 있는 동안 클릭이 **창 숨김/최소화 상태에서도** 창을 앞으로 가져오나
2. **경계** — 원격 웹이 부를 수 있는 것이 우리 커맨드뿐인가(strong-hajin 4→6 · medi-ax 7→9) · `build.rs` ACL · capability 두 판 · 공식 플러그인 권한이 원격 웹에 열리지 않았나(Windows 포함) · origin 검사
3. **웹 쪽** — OS 발송기: `created:true` · `replayed:false` 만 · 보고 있는 대상이면 생략(`visibilityState` · `hasFocus` · surface · focus) · 10초 창 넷 이상 → 셋 + 「새 알림 N건」(`notification_id:null` · 누르면 목록) · 문장은 WP3 함수 · 클릭 → 이동 함수 · 권한은 로그인 뒤 한 번 · 거부면 다시 묻지 않음 · 타이머 정리
4. **카톡 `from_me`** — `authorId == NTChatContext.userId` · 모르면 키를 싣지 않음(AC-12) · 서버가 받는 필드 이름과 같나(`backend/` 의 카톡 업로드 모델)
5. **tauri 2.12 올림** 회귀 위험 — lock 변화 범위 · 다른 플러그인 판 · 기존 커맨드·사건 이름 시험
6. **조용히 통과하는 자리** — 셸 대역(`__TAURI_INTERNALS__`)이 실물과 다른 곳 · cfg 로 macOS 에서만 컴파일되는 코드가 시험에 안 걸리는 곳
7. 시험은 관련만(`SHELL_FLAVOR=medi-ax cargo test --features kakao-collector` · `cargo test` · clippy · 고른 vitest) — 전체 금지 · 사용자 포트·앱 실행 금지
8. **dmg 실측 체크리스트**(코디가 서명 dmg 로 할 것)가 리포트에 충분한가 — 빠진 것 보태라

## 산출물
- `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-wp4-report.md` — §0 판정 · 항목별 · FAIL/WARN(파일:줄 · 고칠 것) · dmg 실측 체크리스트(보탬) · 사람 눈에 이상해 보일 자리
- 완료 보고 앞 브리프 §6 두 명령 — subject 「reviewer 완료: WP4 코드 검수 <판정>」 · text 「[worker_done] reviewer WP4 코드 검수 <판정> — FAIL n · WARN n. 리포트 review-wp4-report.md」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
