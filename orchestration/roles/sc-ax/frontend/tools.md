# @sc-ax-fe — 도구 및 제한

## 사용 가능한 도구
- Read, Edit, Write, Glob, Grep, Bash

## 작업 디렉토리
- 실제 작업 위치와 base 는 dispatch brief 의 `작업 워크트리`·`base 브랜치`가 SSOT 다
- 문서 SSOT 는 brief §1 에 적힌 경로(spec 리포 코디 워크트리 절대경로)만 read-only 로 참조한다
- **첫 액션**: brief 의 작업 워크트리에서
  - `git branch --show-current` 와 brief 의 base/branch 관계 확인
  - `frontend/package.json`, `frontend/tsconfig.json`, `frontend/vite.config.*`
  - `frontend/src/` 를 Glob 으로 파악 — `App.tsx`·`api.ts`·`viewModels.ts`·`labels.ts` 먼저
  - `docs/design/README.md` 에서 이번 화면이 쓰는 토큰·컴포넌트 확인

## 탐색 경로 (ax-workspace 루트 기준, 실 파일은 Glob 으로 확인)
```
frontend/src/*Page.tsx      # 화면
frontend/src/api.ts         # 서버 호출 (유일한 fetch 자리)
frontend/src/viewModels.ts  # 응답 → 화면 모델
frontend/src/labels.ts      # 한국어 카피
frontend/src/chat/          # AX 대화
frontend/src/*.test.tsx     # vitest
frontend/scripts/*-e2e.mjs  # Playwright journey
docs/design/                # 디자인 시스템 참조본 (read-only)
```

## 오케스트레이션 계약
- 태스크·allowed_paths·검증·완료 보고는 dispatch brief 와 preamble 만 따른다

## Bash 자주 쓰는 명령
- `cd frontend && npx tsc --noEmit` · `npx vitest run src/X.test.tsx`
- `npm run dev`(5173) — 브라우저 확인이 필요할 때. API 는 `make api`(8000) 가 떠 있어야 한다
- 전체 빌드(`npm run build`)·`make verify`·`acceptance-e2e` 는 코디네이터 몫 — 워커가 돌리지 않는다

## 금지 사항
- canonical(`/Users/kknaks/git/harness_works/ax-workspace`) 수정 금지 — 워크트리에서만 작업
- `backend/`·`docs/`·spec 리포 수정 금지
- git commit·push·PR 금지
