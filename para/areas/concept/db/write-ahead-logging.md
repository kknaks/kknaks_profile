---
type: concept
id: write-ahead-logging
title: WAL (Write-Ahead Logging)
aliases:
  - WAL
  - write-ahead log
  - 선행 기입 로그
  - SQLite WAL
  - "-wal 파일"
up:
  - 2026-09-04-kakao-task
tags:
  - db
  - sqlite
  - 저장엔진
  - 동시성
---

# WAL (Write-Ahead Logging)

**바뀐 내용을 원본 파일에 바로 쓰지 않고 별도의 로그 파일에 먼저 append 해 두고, 나중에 원본으로 합치는 저장 방식.** 그래서 「지금 이 순간의 최신 데이터」가 원본 파일이 아니라 로그 파일에 있을 수 있다.

## 정의

SQLite 를 예로 들면 WAL 모드에서 파일이 셋으로 늘어난다.

| 파일 | 담는 것 |
|---|---|
| `db` (main) | 마지막 **checkpoint** 까지 합쳐진 본체 |
| `db-wal` | checkpoint 이후 아직 안 합쳐진 **변경분** (append-only) |
| `db-shm` | 어느 프레임이 유효한지 가리키는 공유 인덱스 |

읽기 트랜잭션은 main 을 보다가 **wal 에 더 최신 프레임이 있으면 그쪽을 읽는다.** checkpoint 가 돌아야 wal 내용이 main 으로 접히고 wal 이 비워진다.

- **쓰기가 읽기를 막지 않는다** — 쓰기는 wal 에 append 하고, 읽기는 그 시점의 스냅샷을 본다. 롤백 저널 방식(원본을 잠그고 덮어씀)과 갈리는 지점이다.
- **checkpoint 전까지 최신은 wal 에 있다** — 활발히 쓰이는 대상일수록 main 만 읽으면 낡은 값(또는 0행)이 나온다.

## 왜 중요한가

**원본 파일만 열어 읽으면 최근 변경을 통째로 놓친다.** kakao-task 에서 활발한 카톡 방의 대화가 `chatLogs` 의 `-wal` 에 쌓여 있어, main 만 복호하면 그 방은 0행으로 나왔다 → main + WAL 을 병합해 복호해야 실제 대화가 나왔다.

파일 감시([[filesystem-change-notification]])와도 얽힌다 — wal 은 크기를 늘리지 않고 **같은 자리에 덮어쓰는(in-place)** 경우가 많아 OS 변경 알림이 이벤트를 놓친다. 그래서 감시만으로는 부족하고 [[polling]] 델타 조회를 병행해야 새 프레임을 잡는다.

## 경계와 오해

- **WAL ≠ 백업 로그** — 복구용 아카이브가 아니라 원본에 합쳐지기 전의 임시 변경분이다. checkpoint 되면 사라진다.
- **최신 = main 이 아니다** — checkpoint 주기 때문에 「파일을 그냥 읽으면 최신」이라는 가정이 깨진다. 외부에서 SQLite 파일을 직접 읽는 도구는 wal 을 함께 처리해야 한다.
- MySQL 의 redo log·PostgreSQL 의 WAL 도 같은 원리다 — 크래시 복구와 복제(binlog/스트리밍)의 뿌리가 이 로그다.

## 함께 보는 개념

- [[filesystem-change-notification]] — wal in-place 쓰기가 파일 감시의 사각지대인 이유
- [[polling]] — 감시가 놓친 wal 변경을 델타 조회로 메우는 보완책
- [[transaction]] — wal 이 커밋·롤백 경계를 구현하는 방식

## 출처

- [[2026-09-04-kakao-task]] — 활발한 카톡 방 대화가 `-wal` 에 있어 main 단독 복호 시 0행 → main+WAL 병합 복호로 해결
