# planner-spec002-feedback-fix 결과 보고 — done (미커밋)

SPEC-002 개정 ⑦ · SPEC-000 한 칸 · `log.md` 한 줄 · lint `--strict` 0 error.

| 항목 | 고친 곳 |
|---|---|
| **W1** | KOS 쓰기 표 시작 취소 · 귀가 대기 2(change-flow-step 내부 경로 + `PROCEDURE_WAITING` · `PROCEDURE_DONE`)에 「데모 지점 실물 확인 전 미확인 — 확인 전엔 운영 병원에 열지 않는다(cc 는 공개 경로)」 · 완료 취소 · 귀가 대기 1 에 「실물 확인 전엔 운영에 안 엶」. SPEC 에 「방배정.har 의 PROCEDURE_WAITING」 근거는 원래 없었다(남은 `방배정.har` 언급은 change-tasks-room 의 맞는 근거) |
| **W2** | 규칙 9 · 닫은 OQ-05 의 「cc 와 같음」 → 「KOS 는 대리 수락을 받는다: cc D-27 실호출 · cc 자체는 시스템 계정 하나로 보냈다」 · 「cc 와 다른 곳」 호출 대상 줄 「cc 와 같음」 → 「cc D-26 · D-27 그대로」 |
| **W3** | 호출 상태도 「끝남」 · 호출 탭 대상 · E23 시술 목록 = **그 호출을 유효 호출로 갖는 시술** 기준(다른 호출로 넘어간 시술은 앞 카드에 안 보임) |
| **W4** | 스냅샷 `cards[].state` 에서 `"home"` 삭제(귀가 대기 · 귀가는 `doneTab[].state`) · 규칙 10 · 13 · 14 · 16 「귀가 대기 카드」 → 「귀가 대기 방문」 |
| **OQ-09 닫음** | KOS 쓰기 표 호출 3단계 — 다시 호출 · 재호출도 WAITING · READY 작업에 `call-tasks-doctors` 를 다시 보냄 · 데모 실물 확인 뒤 운영(원천 「결정 — 다시 호출」) · 「닫은 것」에 줄 |
| **OQ-21 닫음** | 규칙 24 = op 을 만들 때 누른 직원을 `external_outbox.sender_staff_id` 에 적고 그 직원 토큰으로 보냄 · 「닫은 것」에 줄. **SPEC-000 §3 05 `external_outbox` 에 `sender_staff_id` uuid FK → staff**(토큰 고르기 전용 · 업무 기록 아님 · KOS 떼면 테이블째 지움 · 원천 「결정 — 코디」) |
| **F8** | U-1 에 「카드 메모 = 오더 메모만(E39 · `visit.procedure_order_note` ← KOS 일정 `orderMemo` · 일정 단위 · SPEC-000 §3 03 표에 있음 · #226 이 채움) · 상담 메모는 카드에 안 보임」 |

## 남은 것 (이 SPEC 밖 · 검수 「같이 정리할 것」)

- **#230 계약 v6** — W6 「닫음 · 되돌림 감수」 · 수락 토큰 「수락한 의사」 · 「준비중만 호출」 · 「귀가 대기 흐림」 · `sender_staff_id` migration · 실물 확인(A8)에 시작 취소 · 귀가 대기 · 다시 호출 1회를 더하기(W1 · OQ-09).
- **#231 계약** — 「귀가 대기 흐림 맨 뒤」 · E09 · E10 「자리는 그림」 · 바이탈 줄 「입실」.
- `sender_staff_id` 는 #225 모델(PR #228)에 없다 — #230 이 migration 으로 더한다.
