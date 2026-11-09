# @ontology-fe — 도구 및 구조

## 작업 디렉토리
- 실제 작업 위치·base 는 dispatch brief 의 `작업 워크트리`·`base 브랜치`가 SSOT
- **첫 액션**: `git branch --show-current` 확인 → `app/front/app/` 구조 Glob →
  `app/front/app/globals.css`(토큰, 수정 금지) → 브리프의 spec·디자인 절대경로

## 탐색 경로 (레포 루트 기준)
```
app/front/app/(ontology)/        # 담당 — 데모 라우트 그룹 (신설)
app/front/app/globals.css        # 전역 토큰 — 읽기 전용
app/front/lib/                   # API 클라이언트 패턴 참조
app/front/app/chat/              # 기존 포트폴리오 채팅 — ?q= 패턴 참조, 수정 금지
```

## 참조 전용 (수정 금지)
```
<브리프의 spec 절대경로>          # SPEC-001·003·004·005
<브리프의 디자인 절대경로>         # design/01~08 + data/*.json (+ Chat.dc.html 만 최신)
app/ontology-agent/              # 백엔드 — API 확인용
```

## 자주 쓰는 명령
- `cd app/front && npx tsc --noEmit`
- `cd app/front && npm run build`
- `cd app/front && npm run dev` (렌더 확인)

## 금지 사항
- 포트폴리오 기존 파일·globals.css 수정 금지 · para/·orchestration/·reference/ 수정 금지
- git commit·push·PR 금지
