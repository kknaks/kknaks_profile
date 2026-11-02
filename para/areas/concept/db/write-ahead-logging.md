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
  - WAL 아카이빙
  - pg_receivewal
  - WAL 세그먼트
up:
  - 2026-09-04-kakao-task
  - 2026-09-21-data-backup
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

- **「WAL ≠ 백업 로그」는 SQLite 얘기다** — SQLite 의 wal 은 checkpoint 되면 사라지는 임시 변경분이다. **PostgreSQL 은 반대다** — WAL 세그먼트를 밖으로 빼서 쌓아 두는 것(WAL 아카이빙)이 시점 복구의 기반이다. 같은 이름이지만 수명과 쓰임이 갈린다 → [[point-in-time-recovery]]
- **최신 = main 이 아니다** — checkpoint 주기 때문에 「파일을 그냥 읽으면 최신」이라는 가정이 깨진다. 외부에서 SQLite 파일을 직접 읽는 도구는 wal 을 함께 처리해야 한다.
- MySQL 의 redo log·PostgreSQL 의 WAL 도 같은 원리다 — 크래시 복구와 복제(binlog/스트리밍)의 뿌리가 이 로그다.

## PostgreSQL 의 WAL — 물리 로그라는 것

PG 의 WAL 은 **「몇 번 파일의 몇 번 블록을 이렇게 바꿔라」**의 나열이다. 논리적인 SQL 이 아니라 물리적인 블록 지시다. 여기서 두 가지가 따라온다.

- **논리 덤프 위에 못 얹는다** — `pg_restore` 로 복원한 DB 는 파일 번호·블록 배치가 원본과 달라 지시가 맞지 않는다. 시작할 때 `pg_control` 대조에서 거부된다 (`database system identifier differs...`). 물리 WAL 에는 **물리 베이스**가 짝으로 필요하다
- **버전·플랫폼에 묶인다** — 기동 시 카탈로그 버전·`MAXALIGN`·`BLCKSZ`·포인터 크기·엔디안을 자기 바이너리와 대조한다. 메이저 버전이 다르면 확실히 거부되고, 아키텍처(x86_64 ↔ arm64)는 공식 지원 밖이지만 둘 다 64bit 리틀엔디안·`MAXALIGN 8`·`BLCKSZ 8192` 라 통과할 여지가 있다

**밖으로 빼는 방법이 둘이고 성질이 다르다.**

| | `archive_command` | `pg_receivewal` |
|---|---|---|
| 방향 | 원본이 민다 (push) | 받는 쪽이 붙는다 (pull) |
| 요구 | 원본 호스트에서 **셸 실행** | **네트워크 접속만** |
| 관리형 RDB | 불가 | 가능 |
| 단위 | 세그먼트가 꽉 차야 넘어감 | 도착 즉시 `.partial` 에 기록 |
| 원본 위험 | 없음 | 슬롯이 밀리면 디스크 증가 → [[replication-slot]] |

관리형에서 「WAL 을 못 쓴다」고 말하기 쉬운데, 막히는 것은 **셸을 요구하는 `archive_command`** 지 WAL 자체가 아니다. MySQL 의 binlog 도 `mysqlbinlog --read-from-remote-server` 로 같은 pull 을 한다.

## 함께 보는 개념

- [[filesystem-change-notification]] — wal in-place 쓰기가 파일 감시의 사각지대인 이유
- [[polling]] — 감시가 놓친 wal 변경을 델타 조회로 메우는 보완책
- [[transaction]] — wal 이 커밋·롤백 경계를 구현하는 방식
- [[point-in-time-recovery]] — PG 에서 이 로그를 쌓아 두고 쓰는 자리
- [[replication-slot]] — 받는 쪽이 읽기 전에 로그가 지워지지 않게 하는 장치
- [[change-data-capture]] — 같은 로그를 디코딩해 이벤트로 바꾸는 쪽

## 출처

- [[2026-09-04-kakao-task]] — 활발한 카톡 방 대화가 `-wal` 에 있어 main 단독 복호 시 0행 → main+WAL 병합 복호로 해결
- [[2026-09-21-data-backup]] — 사내 DB 백업 설계에서 PG WAL 이 **블록 단위 물리 로그**라는 성질이 설계를 갈랐다. 논리 덤프를 베이스로 쓸 수 없어 물리 베이스가 짝으로 필요했고, 그 물리 베이스를 뜰 수 없는 관리형 RDB 구간이 별도 경로로 빠질 뻔했다. `archive_command`(셸 필요) 대신 `pg_receivewal`(네트워크만)을 수집 방식으로 잡자 호스팅별 분기가 사라졌다
