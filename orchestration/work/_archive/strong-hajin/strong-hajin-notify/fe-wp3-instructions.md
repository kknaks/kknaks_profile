# [frontend] WORK-013 Phase WP3-FE — 화면 (WP1-FE 검수 PASS)

WP1-FE 는 검수 PASS 다(`/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-wp1-fe-report.md`). 이어서 **WP3-FE** 다. 앞 브리프(`strong-hajin-notify-fe-impl-brief.md`)의 allowed_paths · 금지 · 보고 방식 그대로.

- **할 일**: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/30-work/work-013-notifications.md` **「Phase WP3-FE」 절** 체크박스 전부 + Code Surface **WP3 표** 전부 · 원칙 P-1~P-10(특히 P-9 시안·DS 안에서)
- **계약**: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/20-spec/spec-011-notifications.md` §2.1~§2.3 · §4.5(알림 API · `/api/me/badges` · 설정 API) · §4.4(설정 16항목 id)
- **확정 시안 — 화면 정본**: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/reference/2026-09-10-sc-meeting/package 2/Alerts.html` · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/reference/2026-09-10-sc-meeting/package 2/handoff/alerts/` · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/reference/2026-09-10-sc-meeting/package 2/handoff/settings/js/{data.js,settings.v1.jsx}` · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/reference/2026-09-10-sc-meeting/package 2/handoff/settings/css/settings.css` · `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/reference/2026-09-10-sc-meeting/package 2/handoff/shell/js/nav.js` · 변경 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/design-change-1~4.md`

## ⚠ 시작 조건 예외 (코디 판단)
WORK 의 시작 조건은 「WP2-BE 계약 고정」 인데, **backend 가 WP2-BE 를 지금 쓰는 중**이다. 알림 API 모양은 SPEC-011 §4.5 로 고정돼 있으니 **SPEC 대로 짓는다.** `backend/` 의 WP2-BE 변경이 보이면 읽어서 맞추되 **고치지 마라.** 서버와 다른 자리를 찾으면 리포트 「서버와 맞춰 볼 자리」 에 적어라 — 코디가 WP2-BE 완료 뒤 맞춘다. 서버가 없어도 도는 시험(대역)으로 검증한다

## 검증 — 관련 시험만
WP3-FE 「시험」 줄의 **고른 vitest 파일만** `npx vitest run <파일들> --no-file-parallelism` + `npx tsc --noEmit`. 전체 금지

## 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-wp3-report.md`
체크박스별 파일:줄 · Code Surface 대비 · 시안 대조(항목 16 · 꼬리표 16 · 상태 넷) · DS-gaps(스위치 등) · 시험 수치 · **서버와 맞춰 볼 자리** · 미결

## 완료 보고 — 앞 브리프 §7 두 명령 그대로
subject 「frontend 완료: WP3-FE」 · text 「[worker_done] frontend WP3-FE 완료 — <한 줄>. 리포트 fe-wp3-report.md」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
