# Studio Current

## 목적

여름별컴퍼니의 개인 프로젝트 운영 상태와 우선순위를 관리한다.

자주 바뀌는 정보만 둔다.

## 현재 상황

여름별컴퍼니로 개인 앱과 서비스를 회사처럼 운영한다.

현재 출시하거나 운영하려는 앱/서비스가 여러 개 있으므로, 동시에 모두 개발하지 않고 우선순위를 나눠 관리한다.

## 현재 우선순위

| Priority | Project | State | Goal | Next |
|---|---|---|---|---|
| P0 | kknaks.dev | building | 페르소나와 프로젝트 운영 SSOT 정리 | context 구조 정리 |
| P1 | Wine Log | live | 운영 중인 앱 개선 | 현재 운영 이슈 정리 |
| P1 | Language Diary | building | 출시 후보 앱 개발 | MVP 범위 정리 |
| P1 | Persona Counselor | building | 출시 후보 앱 개발 | MVP 범위 정리 |
| P1 | Study Timelapse | building | 출시 후보 앱 개발 | 출시 범위 정리 |
| P1 | mykakao | building | 카톡 대화 로컬 추출 → 일정/캘린더 | 일정 파싱 단계 decision/spec |

## 진행 중

| Project | Work | Status | Blocker | Next |
|---|---|---|---|---|
| kknaks.dev | 파이프라인 신뢰성 버그 수정(레이스 컨디션·실행기 소유권)과 세션 상속 설계(KDEV-DEC-024) 도입 | in_progress |  | 세션 상속 적용 범위 확장 점검 |
| Wine Log | 운영 상태 정리 | todo |  | 현재 이슈 확인 |
| Language Diary | MVP 정리 | todo |  | 핵심 사용자 흐름 정의 |
| Persona Counselor | MVP 정리 | todo |  | 상담/코칭/저널링 범위 선택 |
| Study Timelapse | 출시 범위 정리 | todo |  | 앱 출시 체크리스트 작성 |

## 이번 주 목표

- context 라우팅 구조를 정리한다.
- 개인 프로젝트들의 현재 상태와 출시 우선순위를 정리한다.
- 출시 후보 앱 4개의 MVP 범위를 분리한다.

## Blockers

- 출시 우선순위가 아직 확정되지 않았다.

## 운영 원칙

- 개인사업자의 현재 상태는 이 문서에만 둔다.
- 제품 목록의 원장은 `tracked_repos` DB 다(KDEV-DEC-014 D1). 이 문서는 **지금 무엇을 하고 있나**만 둔다.
- 작업 흐름은 `context/studio/workflow.md`를 따른다.
- 앱을 회사처럼 운영하기 위해 current, projects, release 기준을 분리한다.
