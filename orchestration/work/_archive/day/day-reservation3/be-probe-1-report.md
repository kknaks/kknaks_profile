# be-probe-1 (day-reservation3) 결과 보고 — OQ-Q01 · Q02 · Q03 KOS 데모 지점 실물 확인

## 상태: done

- 실행 2026-11-26(KST) · DAY `KosClient`(이 워크트리 `backend/day/emr/kos/client.py`) 그대로 · 값 원천 = 로컬 `deploy/kos-demo.env`(읽기만 · 출력 안 함)
- **데모 지점 확인(`check_open_key_is_demo`) 통과 뒤에만 썼다**
- 시험 고객 하나 새로 만듦 `6b081f36…`(이름 꼬리표 「(시험)」 · 가짜 번호 · `example.com` 주소) — 지우지 않고 남김
- 예약 하나(모레 · 빈 칸) `e5e6ec70…` 만들고 → 바꾸고 → **끝에 취소 정리(`CANCELED` 확인)**
- 레포 고침 없음 · 값 · 토큰 · 개인정보 출력 없음(O/X · id 앞 8자)

## 결과 표

| OQ | 경로 · 본문 | 응답 | 결과 | 결론 |
|---|---|---|---|---|
| Q01 ① 화면 저장 요청 | HAR `2026-11-20-day-cc-mig/har/예약등록.har`(KOS 새 예약 화면) `reserve` 본문 | 200 | 본문 최상위에 **`counselor{id, name}`** 가 있다(그 밖 `consultationRequired` · `sedationRequired` · `requestedProcedures` · `funnel`) | 화면 「당일 지정 상담사」 = `reserve` 최상위 `counselor` |
| Q01 ② `reserve` 에 바로 | 내부 `schedule/reservation/v2/commands/reserve` + 최상위 `counselor{id,name}`(+ 자원 1 · 담당자 · 메모 · 유입) | 200 `{scheduleId}` | 다시 읽기(≈1.1s) `reservation.counselor.id` = 고른 직원 **O** · 담당자 · 그룹 · 시작 · 지정 의사 · 메모 · 유입 모두 O | **된다 → W3 한 건**(W18 은 생성 묶음에 필요 없음) |
| Q02 W4 한 본문 | 내부 `update-reservation {scheduleId, occupiedResources{items[1]}, reservationMemo, funnel{funnel{…}, funnelDetail:""}}`(시간 한 칸 뒤로 · 유입 다른 값) | 200 | 다시 읽기(≈1.1s) 메모 = 새 글 **O** · 유입 = 새 값 **O** · 시작 = 새 시각 O · 그룹 O · 지정 의사 O · 담당자 그대로 O · **상담사 그대로 O** · 자원 id 그대로 O | **된다** — 메모 · 유입이 W4 한 본문으로 바뀌고 다른 칸은 안 지워짐 |
| Q03 `create-visitor` `email` | 내부 `v1/visitor/commands/create-visitor {name, phoneticName, gender, nationality, dateOfBirth, phoneNumber, email}` | 200 `{data:{id}}` | `get-visitor` 다시 읽기 `email` 키 있음 · 값 = 보낸 값 **O**(이름 · 국적 O) | **된다** — W2 에 `email` 싣는다 |
| 정리 | 공개 `schedule/open/v1/commands/cancel-reservation {reason:"CANCELED"}` | 200 | `reservation.status = CANCELED` O(≈1.1s) | 정리 끝 |

## 구현에 쓰는 것 (DAY `writes.py`)

- **W3 `reserve`**: 상담사가 있으면 최상위 `counselor{id, name}` 을 같이 싣는다 — `write_open` 의 `BANNED_TOP` 에서 `reserve` 만 `counselor` 를 풀고(값 조건 = `{id, name}` · id 글자 있음) · 확인 조건 = `reservation.counselor`(DAY 사본 `visit.requested_counselor_id` — `mapper.py` 가 이미 읽음)
- **W4 `update-reservation`**: `reservationMemo`(합친 글) · `funnel{funnel{…}, funnelDetail:""}` 를 `items` 와 같이 싣는다 · 확인 = 메모 · 유입
- **W18**(`update-reservation {scheduleId, counselor}` 둘만) = [예약 수정]에서 상담사가 바뀔 때만(be-probe-2 #6 실물) — W4 본문에 `counselor` 를 넣는 것은 이번에 시험하지 않았다(그래서 W4 에는 계속 막음)
- **W2 `create-visitor`**: `email` 을 싣는다

## 시험 스크립트

`/private/tmp/day-probe-r3/` — `pcommon.py`(probe-2 본 · env 경로만 `kos-demo.env`) · `harkeys.py`(HAR 본문 키 모양만) · `probe.py` · `run.out` · `log.md` · `state.json`(키 모양 · O/X · id 앞 8자)
