---
type: decision
id: CFO-DEC-022
title: "stale 후보 자동 재분석"
status: accepted
product: cloud-file-organizer
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/decision
  - status/accepted
  - approval
  - sync
  - ai-analysis
links:
  baselines:
    - "[[baseline-001-cloud-file-metadata-structuring]]"
  decisions:
    - "[[decision-011-drive-sync-state-and-pending-approval-conflict]]"
  specs: []
  works: []
  releases: []
  related: []
up:
  - queue
  - optimistic-lock
---

# stale 후보 자동 재분석

승인 대기 중 Drive 파일이 변경되어 후보가 `stale`이 되면, 시스템은 최신 Drive mirror 기준 AI 재분석 job을 자동 enqueue한다. 관리자 화면은 stale/reanalyzing/new candidate ready 상태를 보여주고, 자동 재분석 실패 시 수동 재분석 버튼을 제공한다.

## Context

- 관련 baseline: [[baseline-001-cloud-file-metadata-structuring]]
- 관련 decision: [[decision-011-drive-sync-state-and-pending-approval-conflict]]
- Drive가 파일 SoT다.
- 승인 후보는 생성 당시 Drive mirror fingerprint와 현재 fingerprint가 다르면 stale이다.
- stale 후보는 승인할 수 없다.
- 관리자가 승인 화면에 들어가기 전에 최신 후보가 준비되어 있어야 승인 흐름이 끊기지 않는다.

## Decision

- 채택:
  - Drive 변경 이벤트로 pending 후보가 stale되면 기존 후보를 `stale` 상태로 전환한다.
  - stale 전환 후 최신 Drive mirror 기준 AI 재분석 job을 자동 enqueue한다.
  - 재분석 중인 문서는 관리자 화면에 `reanalyzing` 상태로 표시한다.
  - 재분석이 성공하면 새 `pending` 후보를 생성하고 `new candidate ready`로 표시한다.
  - 자동 재분석 실패 시 관리자에게 수동 재분석 버튼을 제공한다.
  - 삭제/휴지통/범위 제외 상태는 재분석하지 않고 `blocked` 또는 문서 상태를 표시한다.
- 기각:
  - stale 후보를 관리자가 버튼을 누르기 전까지 항상 방치하는 방식.
  - stale 후보를 그대로 승인 가능하게 두는 방식.
  - Drive 삭제/휴지통 상태에서도 자동 재분석을 시도하는 방식.

## State Flow

```text
pending candidate
  -> Drive mirror changed
  -> stale
  -> enqueue reanalysis
  -> reanalyzing
  -> new pending candidate
```

예외:

```text
pending candidate
  -> Drive removed/trashed/out_of_scope
  -> blocked / document unavailable
```

## Admin UI States

| State | 표시 |
|---|---|
| `stale` | Drive 변경으로 기존 후보 승인 불가 |
| `reanalyzing` | 최신 파일 기준 재분석 중 |
| `new_candidate_ready` | 새 후보 검토 가능 |
| `reanalysis_failed` | 실패 사유와 수동 재분석 버튼 |

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[queue]] — stale 이 되면 재분석 **job 을 enqueue** 한다 — 요청 경로에서 바로 처리하지 않고 쌓아 두고 처리하는 구조다
- [[optimistic-lock]] — stale 검출 뒤의 처리를 정한 것이라 DEC-011 과 한 쌍이다 — 충돌을 막지 않고 **검출한 뒤 다시 만든다**

## Resulting Spec Direction

| Spec 후보 | 목적 |
|---|---|
| Candidate stale transition contract | pending -> stale 조건 |
| AI reanalysis job contract | 자동 enqueue와 중복 방지 |
| Approval gate state contract | 관리자 화면 상태와 수동 재시도 |

## Closed Questions

| ID | Resolution |
|---|---|
| OQ-1101 | stale 후보가 발생하면 자동 재분석한다. 실패 시 관리자 수동 재분석 버튼을 제공한다. |
