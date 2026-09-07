---
type: concept
id: filesystem-change-notification
title: 파일 변경 알림 (Filesystem Change Notification)
aliases:
  - 파일 감시
  - 파일 변경 감지
  - file watching
  - inotify
  - FSEvents
  - ReadDirectoryChangesW
  - notify
up:
  - 2026-09-04-kakao-task
tags:
  - os
  - 파일시스템
  - 실시간
  - 이벤트
---

# 파일 변경 알림 (Filesystem Change Notification)

**폴링 대신 OS 커널이 파일·디렉토리 변경을 이벤트로 알려 주는 장치.** 리눅스 `inotify`, macOS `FSEvents`, Windows `ReadDirectoryChangesW` 가 각각이고, Rust `notify` 같은 크레이트가 이 셋을 한 API 로 덮는다. 바뀔 때만 깨어나므로 [[polling]] 보다 지연도 부하도 낮다 — **놓치지 않을 때는.**

## 정의

감시자를 경로에 걸어 두면 커널이 생성·수정·삭제·이동 이벤트를 큐로 흘려 준다. 하지만 이벤트는 **파일시스템 메타데이터가 바뀌는 경계**에서 발생하고, 그 경계가 모든 변경과 일치하지는 않는다.

**놓치는 대표 사례 — in-place 덮어쓰기.** 파일 크기·아이노드를 바꾸지 않고 **같은 블록에 덮어쓰는** 쓰기는 알림이 안 오거나 뭉뚱그려진다. [[write-ahead-logging]] 의 `-wal` 이 대표적이다 — 프레임을 같은 자리에 갱신해 감시자가 조용하다.

그 밖에:
- **이벤트 병합·유실** — 짧은 시간에 몰린 변경이 하나로 접히거나 큐 오버플로로 사라진다.
- **네트워크·가상 파일시스템** — NFS·일부 컨테이너 마운트는 알림을 아예 안 준다.
- **원자적 교체** — 에디터가 임시 파일에 쓰고 rename 하면 감시 대상 경로가 바뀌어 핸들이 끊긴다.

**그래서 감시는 폴링과 병행한다.** 감시로 즉시성을 얻되, 주기적인 델타 [[polling]] 으로 놓친 변경을 쓸어 담는다(디바운스로 이벤트 폭주는 눌러서).

## 왜 중요한가

**「감시를 걸었으니 다 잡힌다」는 가정이 조용한 유실을 만든다.** kakao-task 실시간 축적에서 `notify` 가 카톡 `-wal` 의 in-place 쓰기를 놓쳐 새 대화가 안 들어왔다 → 3초 델타 폴링을 병행하고, 이벤트는 700ms 디바운스로 묶어 해결했다.

## 경계와 오해

- **알림 ≠ 완전성 보장** — 커널은 최선 노력(best-effort)이다. 정확성이 필요하면 감시를 트리거로만 쓰고 실제 데이터는 다시 읽어 대조한다.
- **감시 ≠ 폴링의 상위호환** — 지연·부하는 낫지만 유실 사각지대가 있다. 둘은 대체가 아니라 보완이다.
- **재귀 감시 비용** — 디렉토리 트리 전체를 걸면 감시자 수·메모리가 커진다(inotify watch 상한 등).

## 함께 보는 개념

- [[polling]] — 감시가 놓친 변경을 델타 조회로 메우는 병행 수단
- [[write-ahead-logging]] — in-place 쓰기로 감시 사각지대를 만드는 대표 사례
- [[server-sent-events]] — 감시로 잡은 변경을 클라이언트로 밀어 보내는 통로

## 출처

- [[2026-09-04-kakao-task]] — `notify` 가 카톡 `-wal` in-place 쓰기를 놓침 → 3초 델타 폴링 병행 + 700ms 디바운스로 해결
