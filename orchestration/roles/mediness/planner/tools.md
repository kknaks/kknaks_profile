# @mediness-planner — 도구 및 제한

## 사용 가능한 도구
- Read, Edit, Write, Glob, Grep, Bash
- mediness 의 SKILLs (`medi-new`, `docs-validate`, `api-design` 등)

## 작업 디렉토리
- 실제 작업 위치와 base는 dispatch brief의 `작업 워크트리`·`base 브랜치`가 SSOT다.
- **첫 액션**: brief의 작업 워크트리에서
  - `README.md`, `AGENTS.md`
  - `rules/document-pipeline.md`, `rules/` 전체
  - `context/manifest.yaml`, `context/index.md`, `context/current-state.md`
  - `templates/` (신규 문서 양식)
  - `products/_map.md` 또는 상위 인덱스가 있다면 그것

## 오케스트레이션 계약
- 태스크·allowed_paths·검증·완료 보고는 dispatch brief와 preamble만 따른다.
- legacy 태스크 큐·리포트 디렉토리·`.processed`를 읽거나 갱신하지 않는다.

## mediness 앱 코드 (읽기 전용, 별도 레포 · dev 브랜치)
- `/Users/kknaks/git/harness_works/mediness-app/back/` — 백엔드 (스펙 작성 시 참고)
- `/Users/kknaks/git/harness_works/mediness-app/front/` — 프론트 (UX 참고)

## 금지 사항
- `/Users/kknaks/git/harness_works/mediness-app/` 코드 수정 금지 (BE/FE 담당)
- **★ `mediness-mediness/mediness-app/` 는 repo split 잔재 — 절대 참조 금지.** 코드는 `harness_works/mediness-app/` 만
- `/Users/kknaks/git/harness_works/mediness-mediness/products/{service}/` 하위 서비스 문서 수정 금지 (해당 서비스 오케스트레이션 담당)
- git push, 직접 배포 금지
