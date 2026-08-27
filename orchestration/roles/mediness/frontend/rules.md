# @mediness-fe — 규칙

## 코딩 컨벤션
- mediness 레포 `CLAUDE.md`, `AGENTS.md`, `rules/` 우선
- TS strict 모드. `any` 지양
- 컴포넌트는 가능한 한 작게, 단일 책임
- shadcn/Radix 기존 컴포넌트를 우선 사용, 직접 만들기 전에 확인
- `cva` + `clsx` + `tailwind-merge` 로 variant 일관 처리
- 서버 컴포넌트 vs 클라이언트 컴포넌트 경계 명확화 ('use client' 최소화)

## TDD
- 신규 훅/유틸은 단위 테스트 동반
- 컴포넌트는 critical path 만 testing-library 로 검증 (설정 도입 시)
- 테스트 통과 없이 "완료" 표현 금지

## UI/UX
- 와이어프레임/디자인 100% 매핑. 임의 카드 추가/삭제 X
- 모호한 부분은 yes/no 로 admin 에게 확인
- 버튼/배지 chrome 에 이모지 X — lucide-react 아이콘

## 스코프 규칙
- 작업 전 영향 받는 파일 목록을 전수 나열
- 누락·불일치 사항은 리포트 "다른 팀 영향" 에 명시
- `mediness/products/{service}/` 하위 서비스 코드/문서에는 손대지 않는다

## 리포트 형식

```markdown
# {PLAN-NNN-T-NNN} 결과 보고

## 상태: done / in-progress / blocked

## 수행 내용
- {추가/수정한 페이지·컴포넌트·훅 목록}
- {API 연동 변경}

## 테스트 결과
- 테스트 실행 결과 (몇 개 통과/실패)
- 빌드/타입체크 결과

## 다른 팀 영향
- BE 가 알아야 할 신규 엔드포인트 요청
- 디자인/플로우 변경
- planning 이 알아야 할 정책 불일치 사항

## 이슈/블로커
- {막힌 부분, UX 결정 필요 항목}
```
