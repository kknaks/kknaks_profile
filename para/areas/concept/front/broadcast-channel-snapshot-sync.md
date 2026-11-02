---
type: concept
id: broadcast-channel-snapshot-sync
title: 탭 간 스냅샷 동기화와 연결 판정
aliases:
  - BroadcastChannel
  - 탭 동기화
  - 듀얼 스크린 목업
  - 스냅샷 동기화
  - presence ping
  - 연결 판정 지연
up:
  - 2026-10-22-charty-consult-mockup
tags:
  - frontend
  - sync
  - browser-api
---

# 탭 간 스냅샷 동기화와 연결 판정

같은 브라우저의 탭 두 개를 서버 없이 묶는 `BroadcastChannel`. 한쪽(조작하는 태블릿)이 **상태 전체를 seq 와 함께** 쏘고 다른 쪽(보여 주는 큰 화면)은 받기만 하면, 새로고침 · 유실이 다음 스냅샷으로 저절로 메워진다.

## 정의

1. **쓰는 쪽은 하나다** — 태블릿 store 가 원본, 바뀔 때마다 전체 스냅샷 + `seq` 송신. 큰 화면 쪽 조작(필터 칩)은 `filter:set` 요청으로 보내 태블릿이 반영 후 다시 스냅샷
2. **늦게 온 쪽은 hello 로 당긴다** — 큰 화면이 열리거나 새로고침되면 `hello` → 태블릿이 즉시 현재 스냅샷 회신
3. **seq 는 세션 안에서만 비교한다** — 태블릿 저장소가 날아가 seq 가 1 부터 다시 시작하면 큰 화면이 「옛것」으로 보고 버린다. `sessionId` 가 바뀌면 seq 비교를 건너뛴다
4. **연결 판정의 최악 지연 = 무응답 문턱 + 판정 tick** — ping 2초 · 문턱 4초 · tick 0.5초면 닫힌 뒤 「없음」까지 최악 4.5초, 최선 2초. 문턱은 ping 주기보다 길어야 연결 중 깜빡이지 않는다

## 경계와 오해

- **판정 tick 을 ping 주기에 묶으면 지연이 숨는다** — 「현재 시각」을 ping 때만 갱신하면 문턱 5초여도 최악 6초가 된다. 테스트 timeout 을 늘려 통과시키면 결함이 테스트에 묻힌다 — tick 을 떼고 최악을 **계산으로** 닫는다
- **같은 브라우저 · 같은 origin 만이다** — 기기 두 대(실제 큰 스크린 + 태블릿)는 중계 서버(WebSocket 등)가 필요하다. 목업 시연 범위의 도구다
- 저장소가 막힌 탭 둘이 동시에 살아 있으면 서로의 스냅샷을 번갈아 받는다 — sessionId 예외의 대가

## 함께 보는 개념

- [[observer-pattern]] — 한쪽 변경을 구독자에게 알리는 구조
- [[idempotency]] — 같은 스냅샷이 두 번 와도 결과가 같다
- [[server-authoritative-transition]] — 원본이 한쪽에만 있는 상태 전이

## 출처

- [[2026-10-22-charty-consult-mockup]] §2 — 피부 상담 목업 화면 ①·② 동기화(`review-report.md` F-1 · `web/src/sync/` · `e2e/sync.spec.ts`)
