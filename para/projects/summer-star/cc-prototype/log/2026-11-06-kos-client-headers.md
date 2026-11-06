
# 작업 요약 — kos-client-headers (cc-prototype)

기간: `2026-11-04` ~ `2026-11-06`
결과: 운영 핫픽스 머지 · 배포 완료(코드 #20 · infra #47) — 배포 뒤 KOS 403 0

## 1. 무엇을 했나

운영(ccc.medisolveai.xyz) 예약 등록 창 고객 검색이 「요청을 처리하지 못했어요」로 떨어졌다. 로그를 보니 2026-11-03 18:23 KST 부터
KOS 내부 API(`api.kos-solution.com`) 호출이 전부 `403 Unsupported client.` — 일정 폴링 · 하루 예약 · 직원/방 · 고객 검색 · KOS 쓰기가 하루 가까이 멈춰 있었다.
운영 pod 안에서 헤더를 하나씩 붙여 재현해 **브라우저 User-Agent 가 없으면 KOS 가 매 요청을 막는다**는 걸 확인하고,
`procedure/back/app/kos/client.py` 의 내부 요청에 KOS 웹과 같은 User-Agent · Origin · `kos-client-uri` 를 싣는 핫픽스를 backend 워커로 내보냈다.
back 만 재배포했고 새 pod 에서 403 이 사라졌다.

## 2. 적용한 기술·개념

- **헤더 소거법으로 외부 API 차단 원인 좁히기** — 403 의 원인을 「토큰 만료」로 짐작하지 않고 실제 요청으로 가렸다
  - 왜 이걸 골랐나: 첫 403 시각(11-03 09:23 UTC)에 내부 토큰은 13:50 UTC 까지 유효했고, 갓 받은 공개 토큰으로도 같은 시각 내부 호출이 막혔다 → 토큰 문제가 아니다. 응답 본문 `Unsupported client.` 가 「누가 부르는가」를 본다는 신호
  - 무엇이 어려웠나: 무엇을 보는지 문서가 없다 → HAR(KOS 웹이 실제로 보내는 헤더)에서 후보(User-Agent · Origin · Referer · `kos-client-uri`)를 뽑아 하나씩 붙여 봤다. UA 만 200, 나머지 셋만으론 403. 「헤더 없음」 케이스도 실은 `Python-urllib/…` UA 가 붙어 있었다 → 판정 기준은 「UA 유무」가 아니라 「비브라우저 UA」
  - 근거: 운영 pod 실호출(sign-in · get-rooms → 이어서 httpx 로 user-account · rooms · schedules · visitors) · `reference/2026-10-23-cc-overall-board/har/`
- **확인한 것 / 안 한 것을 갈라 말하기** — 「UA 넣으면 된다」를 단정하기 전에 미확인 3가지(httpx 경로 · 나머지 엔드포인트 · 허용 UA 범위)를 밝히고, 머지 전에 back 이 실제 쓰는 httpx 로 다시 실호출해 메웠다
  - 근거: PR #20 본문 「검증」
- **외부 시스템 위장 헤더는 한 곳에서만** — KOS 로 나가는 HTTP 가 `KosClient` 하나뿐인 걸 grep 으로 확인하고 `_internal_headers()` 한 함수로 모았다. 공개 API · presigned PUT 은 건드리지 않았다(공개는 정상, presigned 는 서명이 헤더에 민감)
  - 근거: `procedure/back/app/kos/client.py` `_internal_headers` · `tests/test_kos_headers.py`

## 3. 막혔던 것 / 사고

- KOS 가 사전 공지 없이 내부 API 에 클라이언트 검사를 넣었다 → 운영이 하루 가까이 KOS 없이 돌았는데 **알림이 없었다**. 401 만 재발급 대상이라 back 은 같은 403 을 10초마다 되풀이했고, 화면은 「요청을 처리하지 못했어요」만 보였다 → 사용자 화면 제보로 알았다 → 아직 못 풀었다(§7)
- 우리가 쓰는 건 KOS **내부** API(공개 OpenAPI 에 없는 쓰기 때문에 HAR 로 찾은 것)다. 웹 클라이언트를 흉내 내는 구조라 KOS 가 검사를 더 넣으면 또 막힌다 — Origin · `kos-client-uri` 를 미리 같이 넣은 이유

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-04 | 원인 = KOS 내부 API 의 비브라우저 UA 차단(11-03 18:23 KST~) | 운영 pod 헤더 소거 재현 |
| 2026-11-04 | 내부 요청에 UA + Origin + `kos-client-uri`. 공개 API · presigned PUT 은 그대로 | 사용자 지시 — KOS 가 다음에 볼 수 있는 것까지 미리 |
| 2026-11-04 | SPEC 개정 없이 브리프를 계약으로 핫픽스 | 사용자(「핫픽스로 나가야 하니까」) |

## 5. 날짜별 로그

- `2026-11-04` 고객 검색 실패 제보 → 운영 로그 · pod 재현으로 원인 확인 → backend 워커 발주 · 구현(pytest 536) → httpx 실호출 확인 → 코드 #20 · infra #47 머지 · ArgoCD sync · 403 0
- `2026-11-06` deploy.md 기록 · 마감

## 6. 산출물

- code PR: https://github.com/kknaksss/cc-prototype/pull/20 (스쿼시 `77173cf`)
- infra PR: https://github.com/MediSolveAIDev/k8s_infra_mac/pull/47 (`5ebc4dc`, `back.imageTag`)

- `kknaksss/kos-client-headers` → `main`
  - `4e5f342` fix(procedure): KOS 내부 API 요청에 웹 클라이언트 헤더(UA · Origin · kos-client-uri)
- `kknaksss/cc-kos-client-headers` → `main`
  - `519066e` deploy(cc-prototype): procedure back 이미지 77173cf — KOS 내부 API 클라이언트 헤더 핫픽스
- 문서: `para/projects/summer-star/cc-prototype/deploy.md` 기록 행

## 7. 잔여

- KOS 쓰기(예약 등록 · 방 배정 등)는 같은 헤더 함수를 거치지만 실호출로는 확인 안 함 — 다음 실제 등록 때 운영 로그로 확인
- KOS 403 이 하루 동안 알림 없이 이어졌다 — 연동 끊김을 사람이 알 수단(헬스 · 알림)을 둘지 사용자 판단
- 403 `Unsupported client.` 는 재시도 대상이 아니라 10초마다 같은 실패를 쌓는다 — 그대로 둘지 사용자 판단
