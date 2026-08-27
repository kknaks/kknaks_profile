# @mediness-fe — 기술 스택

## 언어 및 프레임워크
- TypeScript + React + Next.js (App Router)
- Tailwind CSS + `@tailwindcss/typography`
- shadcn/ui + Radix (`@radix-ui/react-*`)
- `class-variance-authority`, `clsx`, `tailwind-merge` — variant 패턴
- `react-markdown` + `remark-gfm` + `rehype-raw` + `rehype-highlight` + `highlight.js`
- `lucide-react` (아이콘)
- npm (`package-lock.json`)

## 디렉토리 구조 (Next.js App Router 기준, 실제는 Glob 으로 확인)
- `app/` — 라우트 (`page.tsx`, `layout.tsx`)
- `components/` — 재사용 컴포넌트 (shadcn 파생 포함)
- `lib/` — 유틸·클라이언트
- `proxy.ts` — 프록시 설정 (있음)
- `public/` — 정적 자산

## 테스트
- 레포 설정 확인 후 적용 (없으면 admin 에 보고 후 도입)

## 핵심 원칙
- TDD: 훅·유틸·critical 컴포넌트는 테스트
- 최소 변경: 정확히 필요한 부분만
- 기존 컴포넌트/훅 재사용 우선 — 중복 X
- 와이어프레임/디자인 명세 100% 매핑, 임의 추측 X (모호하면 admin 확인)
- 버튼/배지 chrome 에 이모지 X — lucide-react 아이콘 사용
