# ax-knowledge-graph

AX 관련 기사, 영상, 링크를 수집하고 개념·사례·도구 사이의 관계를 지식그래프로 전환하는 제품의 SSOT다.

규칙: `para/projects/project.md`

## 코드 레포

| 항목 | 경로 |
|---|---|
| Remote | `https://github.com/kknaks/ax-graph` |
| Local clone | `/Users/kknaks/git/toy_pr2/ax-graph` |
| 문서 SoT | `/Users/kknaks/git/toy_pr2/kknaks_profile/products/ax-knowledge-graph` |

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | AXKG-BL-001 accepted | 핵심 가정 검증 |
| Decision | AXKG-DEC-001~005 accepted | 배포 단계에서 bind mount host path 확정 |
| Spec | AXKG-SPEC-001~012 stable | WP 분해 후 MVP 구현 착수 |
| Work | **WP0 done** + WP1~5 todo | WP1(intake)·WP2(그래프 코어) 병렬 착수 |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | `00-baseline/README.md` |
| 10-decision | `10-decision/README.md` |
| 20-spec | `20-spec/README.md` |
| 30-work | `30-work/README.md` |
| 40-architecture | `40-architecture/README.md` |
| 60-release | `60-release/README.md` |
| 70-runbook | `70-runbook/README.md` |

## 최근 로그

- 2026-07-07 gap 리뷰 major 정리: 게이트 공통 모델·API 단일화, 파이프라인 파생 상태 매핑표, 재분류 재오픈 규칙, document_type 어휘 통일, Slack intake·Graph Rebuild 아키텍처 반영, VoltAgent 불채택 확정.
- 2026-07-07 gap 리뷰 blocker 5건 해소: AXKG-DEC-005(연결 후보 컨텍스트·3자 조립·JSON Schema·project MVP 포함) + AXKG-SPEC-011(AI 실행 파이프라인) 신설, SPEC-004/005/009/010·40-architecture 반영.
- 2026-07-07 Markdown document SoT + PostgreSQL 운영 저장소 decision과 database architecture 초안 작성.
- 2026-07-07 MVP 기본값 확정: AI Transformation, Slack/manual URL, Graph RAG, Claude default, localStorage token, 기존 `/graph` 구현 참고.
- 2026-07-07 seed user와 브라우저 저장 token 기반 간단 로그인 spec 추가.
- 2026-07-07 코드 레포 local clone 경로를 `/Users/kknaks/git/toy_pr2/ax-graph`로 확정.
- 2026-07-07 open-kknaks 기반 내부 AI 실행과 Claude/Codex provider 설정 페이지 spec 추가.
- 2026-07-07 Graph Chat 페이지 spec 추가. `[graph] | [채팅]` 레이아웃과 그래프 기반 응답 계약 정의.
- 2026-07-07 Obsidian/제품 페이지 공용 wikilink + frontmatter `up` 기반 문서 그래프 계약 추가.
- 2026-07-07 resource -> reference 전환 승인 게이트와 대화형 사이드바 spec 추가.
- 2026-07-07 Slack/수동 URL 1차 수신 위치를 Source Inbox spec으로 분리.
- 2026-07-07 PARA 기반 수집-분류-연결-문서화 파이프라인과 승인 게이트 재생성 흐름을 decision/spec으로 정리.
- 2026-07-07 inbox 아이디어를 제품 디렉터리로 승격하고 작업 레포를 생성.
