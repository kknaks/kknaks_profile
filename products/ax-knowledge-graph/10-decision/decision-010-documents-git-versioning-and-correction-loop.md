---
type: decision
id: AXKG-DEC-010
title: "문서 SoT git 버전관리와 승인 커밋·사람 교정 루프"
status: accepted
product: ax-knowledge-graph
created_at: 2026-07-24
updated_at: 2026-07-24
tags:
  - product/ax-knowledge-graph
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-002-markdown-sot-postgres-storage|AXKG-DEC-002]]"
    - "[[decision-004-mvp-defaults-and-scope|AXKG-DEC-004]]"
  specs:
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-005-document-link-graph-contract|AXKG-SPEC-005]]"
    - "[[spec-015-documents-git-sync|AXKG-SPEC-015]]"
  works: []
  releases: []
  related: []
---

# 문서 SoT git 버전관리와 승인 커밋·사람 교정 루프

Markdown 문서 SoT(DEC-002)를 `ax-graph` 코드 레포 하위 `documents/` 폴더로 git 버전관리한다. 서버 AI는 문서화 승인 시점에 자동 commit+push 하고, 사람은 로컬 clone에서 pull→수정→push 로 교정한다.

> DEC-002는 최종 문서를 Markdown SoT로 정했고 배포 host path(OQ-001)를 유보했다. 운영에서 SoT(`/mnt/data/axkg/documents`)가 버전관리도 백업도 없이 앱(root)이 자동으로 덮어쓰는 상태라, "잘못 생성된 문서를 사람이 되돌려 고치는" 루프가 불가능하다. 이 결정으로 SoT를 git 트리로 만들어 백업·이력·교정 루프를 확보한다.

## Context

- 관련 decision: AXKG-DEC-002(Markdown SoT), AXKG-SPEC-004(문서화 승인=디스크 확정).
- 현행 실측: SoT `/mnt/data/axkg/documents`는 git 아님·백업 0. api가 rw로 쓰고 qmd가 ro로 읽어 인덱싱. 코드는 github/ax-graph → CI(ghcr) → 서버가 이미지 pull 실행(서버엔 코드 레포 체크아웃 없음).
- 문제: ① SoT 유실 시 복구 불가(백업 없음). ② 작성자가 서버 AI + 사람 둘인데 동기화 규칙이 없어 사람 교정이 소실되거나 정합이 깨진다.
- 결정 필요 이유: 승인 파이프라인(SPEC-004)이 이미 확정 문서를 파일로 쓰고 있으므로, 그 write에 버전관리를 붙일 지점과 사람 교정의 반영 규칙을 확정해야 한다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | 서버 SoT를 계속 비-git 폴더로 두고 별도 rsync 백업 | 앱 변경 없음 | 이력·교정 루프 없음, 사람 수정 반영 불가 | 기각 |
| B | 문서를 **전용 repo**(ax-graph-documents)로 분리 git 관리 | 코드/데이터 관심사 분리, 운영 단순 | 레포 2개, 코드-문서 한 곳 이력 아님 | 후보(유지 결정으로 미채택) |
| C | 문서를 **코드 레포 하위 `documents/`** 로 git 관리 | 코드-문서 한 레포 이력, clone 1개 | 서버 SoT가 sparse checkout+push 크리덴셜 필요 | 채택 |
| D | 사람 교정도 앱 UI(재분류/피드백)로만 | 파일 직접수정 불필요 | 관계 문서 대량 교정엔 비효율, 사용자가 raw 편집 원함 | 기각 |

## Decision

- 채택:
  - 문서 SoT를 `ax-graph` 레포 top-level `documents/` 로 git 버전관리한다(Option C).
  - 서버 SoT(`/mnt/data/axkg/…/documents`)는 코드 레포의 **cone sparse-checkout(`documents/`만)** 워킹트리로 만든다.
  - 커밋 시점은 **문서화 승인**이다: `ApplyExecutor.apply()`가 파일을 확정한 뒤 background로 `add documents/ → commit → pull --rebase → push`.
  - 사람 교정은 로컬 clone에서 `documents/` 파일을 직접 pull→수정→push 한다.
  - 정합 불변식: 서버는 승인마다 즉시 commit 하여 uncommitted 상태로 방치하지 않는다. 사람은 서버를 직접 만지지 않는다.
  - 충돌(같은 파일 AI+사람)은 자동 병합하지 않고 알림 후 정지한다.
  - CI(`deploy-prod.yml`) 트리거에 `documents/**` 를 넣지 않아 문서 push가 이미지 재빌드를 유발하지 않는다.
  - push 크리덴셜(GitHub email·PAT)은 `.env`(배포 시크릿)로 주입한다.
- 기각:
  - 비-git 폴더 유지(A), 앱 UI 전용 교정(D).
- 보류:
  - 전용 repo 분리(B) — 운영 부담이 커지면 재검토.
  - origin 바이너리(.docx) git-lfs 여부 — 용량 초과 시 도입.

## Rationale

- 판단 기준: 백업 확보, 이력/되돌리기, 사람 교정 반영, 앱 변경 최소, 코드-문서 이력 통합.
- 대안 대비: (A)는 교정 루프가 없고, (B)는 운영이 단순하나 코드-문서 한 레포 이력을 잃는다. commit-on-approval 구조에서는 (C)의 sparse-checkout·크리덴셜 부담이 유일한 대가이며, CI 경로 필터로 재빌드 위험이 없음을 확인해 수용 가능하다.
- 리스크: ① 서버 SoT가 git 트리가 되어 sparse-checkout·safe.directory·push 크리덴셜이 필요. ② 사람 교정을 서버가 pull 한 뒤 **그래프 인덱스 재빌드**가 없으면 교정이 그래프에 반영되지 않는다(정합) → SPEC-015가 재인덱싱을 계약에 포함. ③ push 실패는 비치명으로 처리해 승인 트랜잭션을 깨지 않는다.

## Scope

- In:
  - `documents/` 를 코드 레포로 git 버전관리
  - 서버 SoT sparse-checkout 전환 + 바인드 마운트 재지정
  - 승인 시 commit+push 훅, pull --rebase 교정 흡수, 충돌 정지
  - pull 후 변경 문서 재인덱싱
  - `.env` push 크리덴셜(email·PAT)
- Out:
  - 전용 repo 분리
  - git-lfs
  - 문서 편집용 신규 UI

## Deployment Deferred

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-002 | origin 바이너리(.docx) 용량 증가 시 git-lfs 도입 | DevOps | 용량 임계 도달 시 |
| OQ-003 | 다중 api 레플리카 시 commit 직렬화(현재 단일 컨테이너 in-process 락 전제) | DevOps | 스케일아웃 시 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| AXKG-SPEC-015 | create | 문서 git 동기화 계약(commit-on-approval·교정 루프·재인덱싱) |
| AXKG-SPEC-004 | update | 승인 apply 후 git-sync 훅 연결 지점 참조 |
| AXKG-DEC-002 | update | OQ-001(배포 host path) 해소 링크 |
