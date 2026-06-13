---
type: work
id: WORK-001
title: "메시지 추출 확인용 웹 데모"
status: done
product: mykakao
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: ""
progress: 100
created_at: 2026-06-12
updated_at: 2026-06-12
tags:
  - product/mykakao
  - doc/work
  - status/done
links:
  baselines: []
  decisions:
    - "[[decision-001-extraction-approach]]"
  specs:
    - "[[spec-001-message-extraction]]"
  works: []
  releases: []
  related: []
---

# 메시지 추출 확인용 웹 데모

SPEC-001의 추출(자체 키 유도 + sqlcipher 복호화)이 실제로 동작함을 브라우저에서 확인하는 백+프론트 데모.

> spec의 조합을 실제 구현 단위로 내리는 작업 지시서다.

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature (demo) |
| Owner | kknaks |
| Status | done |
| Progress | 100% |
| Branch/PR | `toy_pr2/mykakao` (코드 레포, 미커밋) |
| Blocker | — |
| Next | 커밋 / (다음 단계) 일정 파싱 spec |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| BE | kknaks | 키 유도·복구·ORM·API | done |
| FE | kknaks | 단일 페이지 UI | done |
| QA | kknaks | 4 엔드포인트 라이브 검증 | done |

## Scope

- Covers: [[spec-001-message-extraction]] — 복호화 + 메시지/방/검색 조회 + **실시간 스트림(SSE)**을 UI로 확인.
- Out of scope: 일정 파싱(NLP), 캘린더/ics 출력, 인증/멀티유저, 배포.

## Target Surface

- 코드 레포: `/Users/kknaks/git/toy_pr2/mykakao`
  - `backend/extract.py` 키 유도 + user_id 복구(SHA512 preimage, C 가속)
  - `backend/db.py` sqlcipher3 + SQLAlchemy 엔진(StaticPool, immutable read-only)
  - `backend/models.py` NTChatRoom / NTChatMessage / NTUser ORM
  - `backend/main.py` FastAPI: `/api/stats|chats|messages|search` + **`/api/stream`(SSE)** + 프론트 서빙
  - `frontend/index.html` 바닐라 JS (사이드바·말풍선·검색)
  - `run.sh` venv+빌드+기동

## Data / API Notes

- 키는 256-hex를 **passphrase**로, `PRAGMA cipher_default_compatibility=3`. (SPEC-001 §BE Contract)
- chatId/logId는 18자리(>2^53) → API에서 **문자열로 직렬화**(JS 정밀도 보호).
- 오픈채팅 발신자/방이름은 NTUser에 없어 `(이름 없음)`/`sender:null`로 표시(친구·1:1은 정상 표시). 데모 한계로 수용.
- **읽기 모드 = `mode=ro`** (NOT `immutable`): immutable은 WAL을 무시해 연 시점 스냅샷에 고정 → 새 메시지 안 보임. mode=ro는 WAL 반영. (라이브 검증: 단일 연결 4초 새 count 전진)
- **동시성/freshness**: `NullPool`(요청마다 새 연결) → 동시 요청 충돌 없고 매 요청 최신 커밋. (StaticPool 단일연결은 `ResourceClosedError` 유발)
- **실시간(SSE)**: `/api/stream`이 전용 ro 연결로 1초 폴링, `logId > last` 새 행을 `data:`로 push. keep-alive ping. 진짜 write 후킹은 아니고 DB 폴링 기반(~1초 지연). `after=<logId>`로 백로그 재생 가능.

## Acceptance Criteria

- [x] 내보내기 없이 로컬 DB를 복호화해 메시지를 읽는다 (런타임에 kakaocli 미사용).
- [x] `/api/stats` 총량 반환 (632,989 메시지 / 741 방 / user_id 39411126).
- [x] `/api/chats` 최근 대화방 목록 + 이름/시각.
- [x] `/api/messages` 특정 방 메시지(말풍선, 내 메시지 구분).
- [x] `/api/search` 한국어 키워드 검색("회의" → 실제 결과).
- [x] user_id 자동 복구(plist 활성 해시 → SHA512 preimage) end-to-end 동작.
- [x] `/api/stream` SSE 실시간 push (새 메시지 ~1초 내, 백로그 재생 검증).

## Test Plan

| Case | Owner | Status | Notes |
|---|---|---|---|
| 4 엔드포인트 curl | kknaks | done | stats/chats/messages/search 라이브 응답 확인 |
| 키 자동 복구 | kknaks | done | `python -m backend.extract` → user_id 39411126, config 캐시 |
| read-only 안전성 | kknaks | done | `immutable=1`, DB 미변경 |

## Done Criteria

- [x] role별 완료 상태 갱신.
- [x] SPEC-001 Work Handoff 반영(조회 래퍼 = db.py/main.py).
- [x] 라이브 검증 완료.
- [x] `log.md` / `30-work/README.md` 갱신.

## Open Issues

- 오픈채팅 발신자명/방이름 해석(별도 메타 테이블) — 일정 플로우에서 필요 시.
- 코드 레포 커밋 대기(사용자 승인 후).
