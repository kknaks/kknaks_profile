# [frontend] FE 수정 판 1 — FE 검수 FAIL 1 · WARN 7 (2026-10-06)

근거 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/review-fe.md` 전부. `frontend/src/` 만(셸 `src-tauri` 는 이번에 손대지 않는다).
- **F-1(보안)**: 링크 여는 모든 자리(`openLink` · 슬랙 mrkdwn/rich_text 링크 · 언퍼일 `title_link` · 그 밖 href)를 **http · https · mailto 만** 허용, 그 밖(javascript:, data: 등)은 링크로 만들지 않고 글자로 · 새 창은 `noopener,noreferrer` · 시험
- W-1 OAuth 콜백 `connect=error` 처리(설정 화면 오류 배너) · W-2 첨부 state 이름을 be3 실제(`reference`)에 맞춤 · W-3 새 기기 토큰 발급 후 키체인 저장 실패 시 안내 · W-4 동의 URL host 허용 목록(accounts.google.com · slack.com) · W-5 경고 로그에 링크 전체 남기지 않기 · W-6 auxclick(가운데 클릭) 처리 · W-7 시험 빈칸
검증: 브리프와 같은 타겟(tsc · vitest 관련 · 기존 무관 실패 5건은 분리). 커밋 금지. 끝나면 §9(subject "frontend 완료: FE 수정 판 1").
