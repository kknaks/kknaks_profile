# [frontend] WP4 검수 손질 — WARN 셋 (코디 택일)

정본: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-wp4-report.md` §WARN.

- **W-1 창이 없을 때 배너 클릭** — 코디 택일 **①**: medi-ax(트레이 상주)는 창이 없으면 **트레이 「열기」 와 같은 길로 창을 만들고** 웹이 준비되면 클릭 사건을 보낸다(AC-T33 「동시에 둘이 아님」 유지). strong-hajin(프로세스가 새로 뜬 경우)도 **웹이 준비될 때까지 클릭을 보관했다가** 한 번 보낸다(웹 쪽 「준비됨」 신호 · 보관은 하나만 · 시간 상한). 시험
- **W-3 Windows 컴파일** — `rustup target add x86_64-pc-windows-msvc` 가 되면 `cargo check --target x86_64-pc-windows-msvc`(두 판) 를 한 번 시도해 결과를 리포트에. 툴체인·링커 때문에 안 되면 **안 됨 · 이유**만 적는다(Windows 배포는 그 확인 전까지 막는다 — 코디 기록)
- **W-4 `target: null` OS 클릭** — 셸 검증이 `target: null` 을 허용해 목록 클릭과 **같은 일**(읽음 + 「열 수 없는 항목입니다」)이 되게. 묶음(「새 알림 N건」 `notification_id:null`)은 지금대로 알림 목록. 시험
- W-2 · W-5 · W-6 은 코디가 기록만(손대지 마라)
- 검증 관련만(`SHELL_FLAVOR=medi-ax cargo test --features kakao-collector` · `cargo test` · clippy 두 판 · 고른 vitest · tsc) · 금지는 앞 브리프 그대로
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-wp4fix-report.md` · 완료 보고 앞 브리프 §7 두 명령 — subject 「frontend 완료: WP4 손질」 · text 「[worker_done] frontend WP4 손질 완료 — <한 줄>. 리포트 fe-wp4fix-report.md」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
