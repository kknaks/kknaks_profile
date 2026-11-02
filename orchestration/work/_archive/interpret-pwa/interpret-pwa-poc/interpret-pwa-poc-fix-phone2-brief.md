# [backend · frontend · designer] 폰 피드백 2 — D-28 표시 이름 · D-29 초기화 · D-30 데모 원탭 로그인

워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc` — 폰 피드백 1(D-27 · zh-Hant) 변경이 커밋 없이 그대로 있다. 그 위에 이어서. 커밋 · push 금지 · `.env` 열지 마라.
결정 정본: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` **D-28(개정) · D-29 · D-30** — 먼저 읽어라.

## backend (`back/**` · `.env.example` 만)
- D-30: env `INTERPRET_DEMO_LOGIN`(bool · 기본 false) · `GET /api/auth/config` → `{"demoLogin": bool}`(인증 없음) · `POST /api/auth/demo` → 켜져 있으면 `/api/auth/login` 과 같은 응답 모양(env 계정 토큰 · 잠금 대상 아님), 꺼져 있으면 404 `not_found`. 로그인 env 가 비어 있으면 켜져 있어도 401. `.env.example` 에 이름 · 주석. 시험(켜짐/꺼짐/env 빔)
- D-28: 한국어 이름이 back 에 있으면(오류 문구 등) zh=중국어 · zh-Hant=대만어 확인
- 검증: `cd back && uv run ruff check . && uv run pytest -q`

## frontend (`front/**` 만)
- D-28 개정: 목록 표시 「中国 · 简体中文」(zh) · 「臺灣 · 繁體中文」(zh-Hant) · 「廣東話」(yue) · 한국어 이름 중국어 / 대만어(원 아래 안내 「대만어로 출력 중」 · 용어집 제목) — 대만을 중국어 하위 표기로 쓰지 않는다
- D-29: 멈춤 상태(#5)에서만 원 옆(한국어 영역 쪽 · 회전 영향 없음)에 「초기화」 단추(한국어만 · medikit Button 작은 크기 · 테두리형) → 두 영역 말풍선 비움 · 재생 큐 비우고 남은 조각 버림 · 멈춤 유지 · 언어 유지. 시험 1건
- D-30: 로그인 화면 진입 때 `GET /api/auth/config` → demoLogin 이면 입력 칸 없이 「로그인」 단추 하나(누르면 `POST /api/auth/demo` → 통역 화면) · 아니면 지금 화면. config 실패면 지금 화면
- 검증: `cd front && npx tsc --noEmit && npm run lint && npm run build && npx vitest run` · 클래스 대조

## designer (Claude Design 「Interpret PWA」 · `design/` 만)
- State-5-Paused 에 「초기화」 단추(D-29) · Login 화면 데모 모드 한 장(단추 하나 · D-30) 추가 · 언어 드롭다운이 보이는 화면에 목록 표기 D-28 · 게시 · `design/` 동기

## 보고
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/fix-phone2-<be|fe|design>-report.md`. 완료 두 채널(코디 handle 은 `orca terminal list --json` 에서 제목 'Interpretation PWA with terminology integration'): `orca orchestration send … --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "<역할> 완료: 폰 피드백 2" --body "…"` + `orca terminal send --terminal <코디> --text "[worker_done] <역할> 폰 피드백 2 완료 — <한 줄>" --enter`
