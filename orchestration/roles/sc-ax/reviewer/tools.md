# @sc-ax-reviewer — 도구 및 제한

## 사용 가능한 도구
- Read, Glob, Grep, Bash(읽기 성격 명령 + 린트 실행), Write(**리뷰 리포트 파일 1개만**)

## 작업 디렉토리
- 실제 작업 위치와 base 는 dispatch brief 가 SSOT 다. 검수는 브리프가 지정한 워크트리에서 한다

## 오케스트레이션 계약
- 태스크·리포트 경로·완료 보고는 dispatch brief 와 preamble 만 따른다

## 금지 사항
- 대상 리포 파일 수정·생성·삭제 금지 — 산출물은 리뷰 리포트 1개뿐
- git commit·push·PR 금지
- canonical(`/Users/kknaks/git/harness_works/mediness-mediness`) 접근은 읽기도 하지 않는다 — 워크트리만 본다
