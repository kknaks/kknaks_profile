---
type: baseline
id: OKK-BL-002
title: "Slack inbox·reference 생성과 지식그래프 연결"
status: accepted
product: open-kknaks
created_at: 2026-07-02
updated_at: 2026-07-02
tags:
  - product/open-kknaks
  - doc/baseline
  - status/accepted
links:
  baselines: []
  decisions: []
  specs:
    - "[[spec-011-slack-knowledge-capture|OKK-SPEC-011]]"
  works: []
  related:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
---

# OKK-BL-002 Slack inbox·reference 생성과 지식그래프 연결

## Raw

Slack으로 생각이나 외부 자료를 입력하고, `open_kknaks`가 메시지를 구조화한다.
처리 결과는 내용의 성격에 따라 `kknaks_profile`의 `inbox/` 또는
`reference/`에 Markdown으로 저장한다.

### 1단계 MVP — inbox/reference 생성기

| Slack 입력 | 처리 | 저장 위치 |
|---|---|---|
| 일반 텍스트 아이디어 | 제목·본문·태그 후보 구조화 | `inbox/` (`type: idea`) |
| 유튜브·블로그·논문 등 URL | 원문 수집·요약·출처와 핵심 주장 구조화 | `reference/` (`type: reference`) |

처리 흐름:

1. Slack에서 봇을 mention해 텍스트/URL을 전달한다.
2. `kknaks_profile`의 Socket Mode bridge가 요청을 검증하고 root thread를 연다.
3. 서버가 `open_kknaks` task를 제출한다.
4. `open_kknaks`가 입력을 구조화하고 저장 대상과 노트 데이터를 반환한다.
5. `kknaks_profile`이 `inbox/` 또는 `reference/`에 Markdown SoT를 생성한다.
6. 생성 결과를 Slack에 반환한다.
7. `reference`는 기존 graph builder가 `_graph.json`에 반영한다. `inbox`는
   현재 그래프 스캔 대상이 아니며 정제 전 임시 저장소로 유지한다.
8. 같은 thread의 후속 메시지는 같은 `open_kknaks` session과 같은 노트를 이어 갱신한다.

### 후속 단계 — 지식 고도화

`reference`와 `inbox`가 쌓이면 기존 지식과의 연결 후보를 제안한다. 작성자가
검토하고 자신의 언어로 재작성한 지식만 `permanent/`에 새 노트로 만든다.
원본 `reference`는 근거 자료로 남기며, `inbox` 원본은 분류 후 폐기한다.

## Context

`kknaks_profile`에는 이미 inbox, Markdown frontmatter, wikilink, graph builder,
검증과 시각화 흐름이 있다. 빠진 부분은 일상적으로 사용하는 Slack에서 생각을
입력하고, 이를 기존 파일 기반 지식 구조에 맞게 변환하는 실행 계층이다.

역할 경계:

| 구성요소 | 책임 |
|---|---|
| `kknaks_profile` Slack adapter | 메시지 수신, 인증, 중복 이벤트 방지, 수신·결과 응답 |
| `open_kknaks` | 구조화 prompt 실행, 결과 streaming, 실패·재시도 관리 |
| `kknaks_profile` knowledge pipeline | 저장 대상 결정 결과 검증, Markdown SoT 저장, 그래프 생성·검증·시각화 |
| 작성자 | 연결 후보 승인, 영구노트 정제와 최종 분류 |

## Why It Matters

- 아이디어가 떠오른 시점과 기록하는 시점 사이의 마찰을 줄인다.
- Slack의 비정형 메시지를 기존 Markdown SoT 계약으로 편입한다.
- `open_kknaks`의 queue, provider, streaming, retry 기능을 실제 지식 관리
  워크플로에 적용한다.
- 자동화가 사람의 정제 행위를 대체하지 않고 제목·태그·연결 후보 제안에 집중한다.

## Possible Direction

1. MVP는 Slack의 단일 지정 채널과 단일 사용자만 지원한다.
2. Slack 원문과 event identifier를 보존해 재처리와 중복 방지를 가능하게 한다.
3. 구조화 결과는 자유 형식 Markdown이 아니라 버전이 있는 출력 schema로 받는다.
4. 저장 전에 파일명 충돌, 필수 필드, 링크 대상을 검증한다.
5. 자동 생성 idea는 사람이 분류할 때까지 `inbox/`에 두고 자동 승격하지 않는다.
6. 자동 생성 reference는 원문 URL과 수집 시각을 반드시 보존한다.
7. `permanent/` 자동 생성은 1단계 범위에서 제외한다.

## Open Questions

- 없음. 입력 분류, structured output, Slack thread/session, 연결 후보 정책은
  [[spec-011-slack-knowledge-capture|OKK-SPEC-011]]에서 확정한다.
