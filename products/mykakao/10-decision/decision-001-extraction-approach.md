---
type: decision
id: MK-DEC-001
title: "메시지 추출 방식 — 로컬 SQLCipher DB 복호화 (kakaocli)"
status: accepted
product: mykakao
created_at: 2026-06-12
updated_at: 2026-06-12
tags:
  - product/mykakao
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-001-kakao-message-extraction]]"
  decisions: []
  specs:
    - "[[spec-001-message-extraction]]"
  works: []
  releases: []
  related: []
---

# 메시지 추출 방식 — 로컬 SQLCipher DB 복호화 (kakaocli)

카톡 메시지를 내보내기 없이 가져오기 위해, 로컬 암호화 DB를 복호화해 SQL로 직접 조회하는 방식을 채택한다.

> baseline의 날것 입력을 spec으로 내리기 전에 적용 방향을 정하는 문서.

## Context

- 관련 baseline: [[baseline-001-kakao-message-extraction]]
- 문제/기회: 내보내기 없이, 여러 단톡방 전체 히스토리를 자동으로 한 번에 긁어야 한다.
- 결정이 필요한 이유: 메시지 DB가 암호화되어 있어 접근 경로 자체를 먼저 정해야 후속 작업이 가능하다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A. 내보내기(.txt) | 카톡 앱 내장 내보내기 → txt 파싱 | 합법·안정 | **방마다 수동, 반복 불가** | 사용자가 명시적으로 거부 |
| B. 로컬 DB 복호화 | 자체 키 유도 + 표준 sqlcipher 로 SQL 조회 | 전체 방·전체 히스토리 일괄, 자동, 외부 런타임 의존 없음 | 키 유도 의존, 버전 변화에 취약 | **채택** (kakaocli는 참고만) |
| C. AX 스크래핑 / OCR | 화면에 뜬 텍스트를 접근성/OCR로 수집 | 복호화 불필요 | 스크롤로 보이는 것만, 대량에 비효율 | 라이브 보조용 후보 |

- 채택: **B. 로컬 SQLCipher DB 복호화**. **복호화는 mykakao 내부 코드로 직접 수행**한다 — 자체 키 유도(device UUID + user_id, blluv 연구 기반) + 표준 `sqlcipher` 라이브러리(`PRAGMA cipher_default_compatibility=3` + `PRAGMA key`).
- `kakaocli`는 **reference-only**: PRAGMA compat 모드와 키 유도식을 파악하는 지식 출처로만 사용하고, **런타임 의존성으로 두지 않는다**. (이미 자체 유도/복호화로 라이브 검증 완료)
- 기각: A(내보내기) — 자동화 불가.
- 보류: C(AX/OCR) — 향후 실시간 신규 메시지 수집 보조로 재검토 가능.

## Rationale

- 판단 기준: 자동화 가능 여부 + 전체 히스토리 커버리지.
- 대안 대비 이유: 사용자 상황("여러 방 + 일정 많음")은 일괄 SQL 조회가 압도적으로 유리. 631,713 메시지 / 741 방을 한 번에 조회 가능.
- 리스크:
  - 카톡 버전 업데이트 시 키 유도/스키마가 바뀔 수 있음.
  - `kakaocli` 자동 user_id 탐지가 실패할 수 있음 → 복구 절차를 spec에 고정 (SPEC-001 §BE Contract).
  - 본인 기기·개인용 전제. 외부 배포/타인 데이터 대상 아님.

## Scope

- In: 로컬 DB 복호화, 메시지/대화방 데이터 SQL 조회까지.
- Out: 일정 파싱(NLP), 캘린더/ics/md 출력 — **다음 단계에서 별도 decision/spec**.
- 영향을 받는 spec 후보: [[spec-001-message-extraction]]

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | 카톡 버전 업데이트 시 키 유도 깨짐 대응(재추출 자동화 vs 수동) | kknaks | 추출 안정화 후 |
| OQ-2 | 신규 메시지 증분 수집(폴링/`kakaocli sync`) 여부 | kknaks | 출력 플로우 결정 시 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| [[spec-001-message-extraction]] | create | 메시지 추출 기능 계약 + 방법 상세 |
