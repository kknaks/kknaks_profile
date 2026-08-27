# @mediness-fe — 도구 및 제한

## 사용 가능한 도구
- Read, Edit, Write, Glob, Grep, Bash
- mediness 레포의 SKILLs (있다면)

## 작업 디렉토리
- 실제 작업 위치와 base는 dispatch brief의 `작업 워크트리`·`base 브랜치`가 SSOT다.
- 문서 SSOT는 brief §1에 적힌 경로만 read-only로 참조한다.
- **첫 액션**: brief의 작업 워크트리에서
  - `git branch --show-current`와 brief의 base/branch 관계 확인
  - `front/package.json`, `next.config.ts`, `tsconfig.json`, `components.json` (shadcn 설정)
  - `front/app/`, `components/`, `lib/` 디렉토리 Glob 으로 구조 파악
  - 컨벤션·규칙은 brief의 문서 SSOT에 있는 `AGENTS.md`, `rules/`를 read-only로 참조

## 탐색 경로 (mediness-app 레포 루트 기준, 실 디렉토리는 Glob 으로 확인)
```
front/app/        # Next.js 라우트
front/components/ # 공용 컴포넌트
front/lib/        # 유틸
front/public/     # 정적 자산
```

## 오케스트레이션 계약
- 태스크·allowed_paths·검증·완료 보고는 dispatch brief와 preamble만 따른다.
- legacy 태스크 큐·리포트 디렉토리·`.processed`를 읽거나 갱신하지 않는다.

## Bash 자주 쓰는 명령
- `npm install`, `npm run dev`, `npm run build`, `npm run start`
- `npm run lint`
- (설정 있으면) `npx tsc --noEmit`

## 금지 사항
- `back/` 수정 금지 (BE 담당)
- 문서 레포 `mediness-mediness/` 는 read-only — `rules/`, `context/`, `docs/`, `templates/`, `products/` 수정 금지 (planning 담당)
- **★ `mediness-mediness/mediness-app/` 는 repo split 잔재 — 절대 접근 금지.** 코드는 `harness_works/mediness-app/` 만 사용
- git push, 직접 배포 금지
