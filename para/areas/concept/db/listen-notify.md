---
type: concept
id: listen-notify
title: LISTEN / NOTIFY — 같은 트랜잭션에서 내는 DB 알림
aliases:
  - pg_notify
  - NOTIFY
  - LISTEN
  - 같은 트랜잭션 NOTIFY
  - 짧은 페이로드
up:
  - 2026-10-10-strong-hajin-notify
tags:
  - postgresql
  - 실시간
  - 트랜잭션
---

# LISTEN / NOTIFY — 같은 트랜잭션에서 내는 DB 알림

PostgreSQL 의 프로세스 간 알림. 한 세션이 채널에 `NOTIFY`(`pg_notify(채널, 페이로드)`)를 내면 그 채널을 `LISTEN` 하는 다른 세션들이 받는다. **트랜잭션 안에서 내면 커밋될 때 나가고, 롤백되면 안 나간다** — 「저장된 것만 알린다」 를 DB 가 쥔다.

## 정의

1. **커밋에 묶인다** — 트랜잭션 안의 `NOTIFY` 는 커밋 시점에 배달된다. 저장과 같은 트랜잭션에서 내면 「알림은 갔는데 행은 롤백」 이 생기지 않는다
2. **저장하지 않는다** — 그 순간 `LISTEN` 중인 세션만 받는다. 듣는 쪽이 끊겨 있던 동안의 알림은 사라진다 — 놓친 것은 행(원본)에서 다시 읽어야 한다
3. **페이로드는 짧게** — 크기 상한(기본 8000 바이트 미만)이 있고, 같은 트랜잭션 안의 똑같은 채널·페이로드는 하나로 합쳐질 수 있다. 그래서 **id 만 싣고 받는 쪽이 DB 에서 항목을 읽는다** — 내용의 원천이 행 하나로 남는다
4. **누가 내든 같은 채널** — API · 워커 등 DB 에 쓰는 프로세스 어디서든 낼 수 있고, 듣는 프로세스(예: SSE 를 내는 API)가 모아서 화면으로 민다

## 사용 예시

```sql
-- 저장과 같은 트랜잭션
INSERT INTO notifications (...) VALUES (...) RETURNING id;
SELECT pg_notify('user_events', json_build_object('user_id', $1, 'id', $2)::text);
COMMIT;   -- 여기서 나간다
```

받는 쪽은 `LISTEN user_events` 로 id 를 받고, 그 id 로 행을 읽어 해당 회원의 스트림에 싣는다.

## 왜 중요한가

- 브로커 없이 「커밋된 사건만 다른 프로세스에 알린다」 를 얻는다 — 저장 뒤 별도로 브로커에 보내면 그 사이에 죽었을 때 사건이 빠지거나, 롤백된 사건이 나간다
- 페이로드에 내용을 실으면 알림과 행이 원천 둘이 된다. id 만 실으면 받는 쪽은 늘 지금의 행을 본다

## 경계와 오해

- **NOTIFY ≠ [[message-broker]]** — 보관도 재전송도 없다. 놓친 것을 다시 주는 장치는 위에 따로 있어야 한다(저장된 행 + 사건 id 커서) → [[server-sent-events]]
- **NOTIFY ≠ [[change-data-capture]]** — CDC 는 로그를 읽어 모든 변경을 따라가고, NOTIFY 는 코드가 고른 자리에서만 낸다. **내는 함수를 모든 쓰는 프로세스에 깔아야** 빠짐이 없다 — 게시 프로세스가 일부에만 있으면 나머지 프로세스가 만든 사건은 조용히 안 나간다
- **커밋 순서 ≠ id 순서** — 시퀀스 id 는 발급 순서라, 늦게 커밋된 작은 id 가 있을 수 있다. 「마지막 id 이후」 로 이어받는 쪽은 겹침 창이 필요하다 → [[server-sent-events]]
- 듣는 쪽은 연결을 하나 계속 붙들고 있다 — 커넥션 풀에서 빌린 연결로 들으면 풀이 줄어든다 → [[connection-pool-sizing-formula]]

## 함께 보는 개념

- [[application-event]] — 프로세스 안의 같은 생각(발행하는 쪽은 듣는 쪽을 모른다)
- [[transaction]] — 알림이 커밋에 묶이는 이유
- [[server-sent-events]] — 받은 id 를 화면으로 미는 길
- [[per-user-fanout]] — id 로 읽은 행의 주인에게만 싣는다

## 출처

- [[2026-10-10-strong-hajin-notify]] §2 — Strong Hajin WORK-013 사건 채널. 저장과 같은 트랜잭션에서 `pg_notify` · 페이로드는 id 만 · SSE 를 내는 API 가 DB 에서 항목을 읽는다. 게시 프로세스가 API · external_worker 뿐이라 meeting_worker 에 길을 냈다(`platform/user_events.py` · `W/be-survey-report.md` C-2)
