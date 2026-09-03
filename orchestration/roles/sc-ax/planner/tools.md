# @sc-ax-planner — 도구 및 제한

## 사용 가능한 도구
- Read, Edit, Write, Glob, Grep, Bash

## 작업 디렉토리
- 실제 작업 위치와 base 는 dispatch brief 의 `작업 워크트리`·`base 브랜치`가 SSOT 다
- **첫 액션**: brief 의 작업 워크트리에서
  - `README.md`, `AGENTS.md`
  - `rules/document-pipeline.md`
  - `products/sc-ax/` 상위 인덱스와 `products/sc-ax/00-baseline/00-overview.md`

## 오케스트레이션 계약
- 태스크·allowed_paths·검증·완료 보고는 dispatch brief 와 preamble 만 따른다

## 금지 사항
- canonical(`/Users/kknaks/git/harness_works/mediness-mediness`) 수정 금지 — 워크트리에서만 작업
- `products/sc-ax/` 밖 파일 수정 금지
- git commit·push·PR 금지
