# cleanup-1 결과 보고 — KOS 데모 지점 시험 예약 정리(11-26 ~ 11-27)

## 상태: done (시험 고객은 안 지움 · 스택 안 건드림 · 값 · 개인정보 출력 없음)

- 스크립트 `/private/tmp/day-e2e-r3/cleanup.py` · 결과 `cleanup.json`(id 앞 8자 · 상태만).
- **데모 지점 확인 통과 뒤에만** 썼다(`check_open_key_is_demo`). 취소 = 공개 `schedule/open/v1/commands/cancel-reservation` `{reason: CANCELED}` · 그 뒤 KOS 상세 다시 읽기.
- 안전 장치: KOS 상세의 고객이 시험 고객(이름 「(시험)」 또는 `@example.com`)일 때만 취소 — 아니면 건너뜀(이번엔 건너뛴 것 없음).

## 찾은 곳 (후보 15건 · 중복 합침)

| 출처 | 무엇 |
|---|---|
| probe-1 `state.json` `res.*.sid` | 3건 |
| probe-r3 `state.json` `sids` · `state2/3.json` `sid_full_for_cleanup` | 3건 |
| e2e `state.json` `visit_*`(6개) → `external_ref` 일정 id | 6건 |
| 로컬 DB `visit` — 11-26 00:00 KST 뒤 생김 ∧ 시험 고객(이름 「(시험)」 · `@example.com`) → `external_ref` 일정 id | 위와 겹침 + 2건 더(`744d7fac` · `d22f4e1f` 포함) |

예약 요청 표는 0030 ↔ 0031 다시 올림으로 비어 있어 거기서는 못 찾았다(대신 DB `visit` 조건이 덮음).

## 결과

| KOS 일정 id | DAY 방문 id | 일시(KST) | 전 | 처리 | KOS 다시 읽기 |
|---|---|---|---|---|---|
| `744d7fac` | **`ce7ca6c1`** | 11-28 16:00 | RESERVED | 취소 200 | **CANCELED** |
| `d22f4e1f` | `3b19636d` | 11-27 15:00 | RESERVED | 취소 200 | **CANCELED** |
| 나머지 13건(`1070f82f` · `1f60960b` · `41d5a357` · `52120b35` · `7ba87e01` · `7e2dbde9` · `abec7310` · `b7cf07f9` · `d828b97b` · `e5e6ec70` · `e756ecb6` · `fa27500d` · `fcdd84d6`) | — | — | 이미 CANCELED | 안 함 | CANCELED |

→ **KOS 에 안 취소된 이번 작업 시험 예약 = 0건.**

## 남은 것

- DAY 사본: `3b19636d` = `canceled`(동기화 반영됨). **`ce7ca6c1`(11-28 16:00) = 아직 `reserved`** — 4분 기다려도 안 바뀜. 로컬 동기화가 내일 날짜를 아직 안 읽는 것으로 보인다(스택 · 동기화는 안 건드림). 그 날짜가 동기화되면(예약 현황에서 11-28 을 열거나 다음 회차) `canceled` 로 바뀔 것 — KOS 가 정본.
- `ce7ca6c1` 은 오늘 09:37 KST 에 만들어진 예약(시연 첫 판 재진 요청 16:00 에서 생성된 것으로 보임 · 내가 누른 것 아님).
- 시험 고객(KOS · DAY)은 지시대로 남김.
- 지금 시연 요청 두 건(`bfd5fa31` · `c3c4113b`)은 예약이 아니라 요청 — 그대로 둠.
