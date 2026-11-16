# @ontology-fe — 기술 스택

- Next.js 15 App Router + TypeScript + React 19 (`app/front/package.json`)
- 스타일: 인라인 style + CSS 변수 토큰 (프레임워크 없음). 데모는 `--ont-*` 스코프 레이어
- 폰트: next/font — 데모 그룹에 Pretendard 추가(next/font 경로, CDN @import 금지)
- 그래프: 고정 좌표 정적 SVG. d3-force@3 가용(필수 아님)
- 마크다운: react-markdown@10 + remark-gfm (채팅 본문)
- 데이터: fetch → SPEC-003 계약. 채팅은 2초 폴링

## 핵심 원칙
- 최소 변경 · 기존 컨벤션 우선 · 디자인 문서(`design/01~08`)와 data/*.json 이 시각의 SoT
- 계약(spec)에 없는 필드를 화면이 요구하게 만들지 않는다 — 비면 보고
