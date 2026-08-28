# @kknaks-fe — 도구 및 구조

## 작업 디렉토리
- brief 의 워크트리·base 가 SSOT. **첫 액션**: `git branch --show-current` →
  `app/front/package.json` → `app/front/app/`·`components/` 구조 Glob 파악

## 탐색 경로
```
app/front/app/            # App Router 라우트 (page.tsx, globals.css)
app/front/components/     # home/ shell/ 등 도메인별 컴포넌트
app/front/lib/            # api 클라이언트 · 타입
```

## 자주 쓰는 명령
- `cd app/front && npx tsc --noEmit`

## 금지 사항
- `app/back/`·`para/`·`orchestration/` 수정 금지
- git commit·push·PR 금지 · `npm run build` 금지 (사용자 방침)
