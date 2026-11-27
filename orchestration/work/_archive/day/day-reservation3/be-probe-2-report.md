# be-probe-2 (day-reservation3) 결과 보고 — e2e 1 발견 ② ③ KOS 데모 지점 실물

## 상태: done

- 2026-11-26 · DAY `KosClient` · `deploy/kos-demo.env`(읽기만) · **데모 지점 확인 통과 뒤에만 씀**
- 시험 고객 2명 새로 만듦(`6b083ed9…` · `6b083efe…` · 이름 「(시험)」 · `example.com` · 가짜 번호 · 남김) · 예약 2건(4일 뒤) 만들고 **끝에 취소(`CANCELED`) 확인**
- 레포 고침 없음 · 값 · 토큰 · 개인정보 출력 없음

## ② `visitor/v1/queries/find-duplicated-visitor` — 같은 이름 + 구분 값

시험 고객 = 이름 + 이메일 + 연락처(`886`) + SNS(line) 로 만든 뒤 본문을 바꿔 찾기:

| 본문 | 응답 | 찾음 | 그 고객 |
|---|---|---|---|
| `{name}` | 200 | **X** | — |
| `{name, email}` | 200 | **O** | O |
| `{name, phone{countryCode, phoneNumber}}`(DAY 지금 키) | 200 | O | O |
| `{name, phoneNumber{…}}` | 200 | X(모르는 키 — 무시) | — |
| `{name, snsInfo{snsType, accountId}}` | 200 | O | O |
| `{name, email: 다른 값}` | 200 | X | — |

→ **`email` 을 실으면 같은 이름 + 같은 이메일을 찾는다.** e2e 1 의 중복 고객은 W1 본문에 이메일이 없어서였다. 연락처 키는 `phone`(지금 그대로) · SNS = `snsInfo`(지금 그대로).

## ③ `schedule/reservation/v2/commands/update-reservation` — 「당일 지정 상담사」 지우기

예약(최상위 `counselor` 로 지정 → 다시 읽어 지정 O 확인) 뒤:

| 본문 | 응답 | 다시 읽기(≤8s) |
|---|---|---|
| `{scheduleId, counselor: null}` | 200 | **안 지워짐**(그대로) |
| `{scheduleId, counselor: {}}` | 200 | **지워짐**(`reservation.counselor` = `{id: "", name: ""}` 꼴) · 담당자 · 상태 그대로 |

→ 지우는 꼴 = **`counselor: {}`**. DAY 매퍼는 빈 id 를 None 으로 읽는다(`mapper_values.external_id`) — 확인 조건 = `requested_counselor_external_id is None`. HAR(`2026-11-20-day-cc-mig/har/`)에는 지우기 요청이 없었다.

## 시험 스크립트

`/private/tmp/day-probe-r3/probe2.py` · `run2.out` · `run3.out` · `state2.json` · `state3.json`(③ 은 첫 판이 지정 반영 전에 읽어 무효 → 기다리기를 고쳐 다시 · state3 이 정본).
