# [backend + frontend] 폰 피드백 1 — D-27 로그인 확대 · D-28 중국어 번체 선택지

워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc` (main 046eabe 로 맞춰 둠 · 배포된 코드 = 이 상태). 커밋 · push 금지. `.env` 열지 마라.
결정: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` **D-27 · D-28**

## backend (`back/**` 만)
- D-28: 앱 lang 에 `zh-Hant` 추가(`langs.py` 한 곳) — Soniox `zh` · `TRADITIONAL_LANGS` 에 포함(자막 s2tw · TTS 간체) · 용어집 target = `zh` 열 그대로(정방향 · 역방향) · `/api/glossary?lang=zh-Hant` 는 표시용으로 target 을 s2tw 로. `parse_start` · 시험 갱신. 실물 1회: `zh-Hant` 로 한국어 발화 → 자막 번체 · TTS 입력 간체(live_check 에 한 줄 추가 가능)
- 검증: `cd back && uv run ruff check . && uv run pytest -q`

## frontend (`front/**` 만)
- D-27: 로그인 아이디 · 비밀번호 입력(그리고 다른 입력 · ComboBox 입력이 있으면 전부) 글자 크기 16px 이상 — iOS 포커스 확대 방지. viewport `maximumScale` · `userScalable:false` 는 쓰지 않는다
- D-28: 언어 드롭다운 표기 「中文(简体)」(zh) · 「中文(繁體)」(zh-Hant) · 「廣東話」(yue) — `lib/langs.ts` 에 zh-Hant 추가(외국어 안내 문구는 번체로 · 출력 언어 이름 「中文」) · 용어집 패널 zh-Hant
- 검증: `cd front && npx tsc --noEmit && npm run lint && npm run build && npx vitest run`

## 보고
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/fix-phone1-<be|fe>-report.md`. 완료 두 채널(코디 handle 은 `orca terminal list --json` 에서 제목 'Interpretation PWA with terminology integration'):
`orca orchestration send --to <코디> --from <너> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "<backend|frontend> 완료: 폰 피드백 1" --body "..."` + `orca terminal send --terminal <코디> --text "[worker_done] <backend|frontend> 폰 피드백 1 완료 — <한 줄>" --enter`
