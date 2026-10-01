# [writer 3차] 워드마크 SCAX → MEDISOLVE · 로그아웃 가운데 정렬 (사용자 지시, 데모 빌드)

코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-deploy` 의 `frontend/` 만. 커밋·push 금지.
앞서 남긴 미커밋 2건(App.tsx 관계 탐색 disabled · screens-a.css)은 그대로 둔다.

## 1. 화면에 보이는 「SCAX」 → 「MEDISOLVE」
- 사용자가 보는 글자만 바꾼다. 알려진 곳: `index.html:11` <title> · `src/App.tsx:415` logo · `src/features/auth/LoginPage.tsx:66`
- **위 목록으로 끝내지 말고** `git grep -n "SCAX" -- src index.html src-tauri` 로 사용자 노출 문자열(JSX 텍스트·labels·title·aria·Tauri 창 제목)을 전부 세라
- 바꾸지 않는 것: 주석 · CSS 변수/클래스(`--scax-*`, `.scax-*`) · 전역명 `SCAX` · 코드 식별자 · 백엔드
- 테스트가 「SCAX」 문구를 단언하면 같이 고친다

## 2. 사이드 기둥 바닥의 로그아웃 → 가운데 정렬
- `src/shell/SideNav.tsx:61` 계정 행동 · `src/styles/shell.css:98` 근처 규칙. 버튼 안 글자를 가운데로(워드마크와 같은 축). 접힌 상태 동작은 그대로

## 3. 검증
- `cd frontend && npx tsc --noEmit` · 바꾼 파일 관련 vitest(전량 아님)
- 떠 있는 local-stack(5176, COMPOSE_PROJECT_NAME=strong-hajin-work)에서 화면으로 확인. Vite HMR 이면 재기동 불필요
- dmg 재빌드는 **하지 않는다**(origin 결정 대기)

## 보고
바꾼 파일:줄 목록 · grep 전수 결과(바꾼 것/안 바꾼 것 이유) · 검증 수치. 두 채널(task `task_b12450b8e256` · dispatch `ctx_9d693170f05a` · 코디 `term_8d586fcb-a104-4f31-9f5f-fd3b659a1d24`).
