# planner-spec002-fix2 결과 보고 — N1 · N2 + 사용자 결정

## 상태: done (미커밋)

## 수행

| 파일 | 변경 |
|---|---|
| `products/day/20-spec/spec-002-procedure-board.md` | 머리말 개정 ② · N1 · N2 · OQ-01 · OQ-04 · OQ-07 · OQ-11 반영 · §5 재구성 |
| `products/day/log.md` | 2026-11-06 `spec-change` 한 줄(DAY-SPEC-002) |
| `products/day/20-spec/spec-000-data-model.md` | **이번엔 바꾸지 않음** — 공용 계정 설정 키를 넣었다가 코디 정정 2 로 되돌렸다(diff 는 앞 판의 `closed_at` · OQ-04-2 · sources · last_updated 만) |

lint `--strict` → 0 error · products/day 경고 0.

## 고친 것

- **N1** — 규칙 9 끝 · 닫은 OQ-05 「결과」에 「그 의사가 DAY 에 로그인할 때까지 같은 방문의 뒤 KOS 쓰기(첫 시작 · 종료 · 귀가 대기)도 함께 멈춘다 — KOS 화면에서는 그 고객이 시술 대기 · 미완료로 남는다」. 규칙 24 는 그대로.
- **N2** — 규칙 25: `assigneeIds` = 그 병원 연결의 시스템 계정(`crm_connection.config` `system_email` 로 worker 가 sign-in 하는 계정 = `is_system_account = true` 인 직원 · #226 은 그 하나에만 켬)의 KOS id 하나. 새 칸 없음. OQ-06 닫은 줄도 같게.
- **OQ-01**(사용자) — §3 API 계약을 다시 짰다: 웹 = 화면 라우트 `/board/...` 가 HTML 조각(조작 10 + `GET /board` · `GET /board/stream`), JSON `/api/...` = 앱 전용 짝 · 업무 규칙은 service 한 곳. 실시간 갱신: 웹 `GET /board/stream`(신호 → `GET /board` 조각) · 앱 `/api/board/stream`(스냅샷). 스냅샷 제목을 「앱 · 서버가 조각 그릴 때 쓰는 값」으로.
- **OQ-04**(사용자 · 코디 정정 1) — 재호출 = 고르는 창 「모든 의사」 \| 원장 한 명 · **기본 선택 = 처음 호출 대상**(시안 M L1634 · L1064). U-5 · S-3 · API · 규칙 6 · cc 표에서 「OQ-04 대기」를 걷었다.
- **OQ-07**(사용자) — S-7 · 규칙 22 · KOS 쓰기 재전송 줄: 끝내 실패하면 실패 토스트만 · 다시 보내기 · 관리 화면 없음 · KOS 에서 고치면 폴링이 맞춤.
- **OQ-11**(사용자 · 코디 정정 2) — 규칙 19: 1차는 마취용 · 공용 계정을 빼지 않고 다 넣는다 · 빠지는 것은 sign-in 시스템 계정 하나뿐. 뺄 목록 · 설정 키 · SPEC-000 변경 없음.
- 수락 창 기본 선택(앞 판에서 「OQ-04 와 같이 열림」)은 OQ-04 결정이 재호출만 말해서 **시안대로**(지정 호출 → 지정 원장 · 아니면 보는 원장 본인 · 그 밖 없음, M L1630)를 기본값으로 적고 「그 밖(기본값 확인만)」 OQ-19 로 뒀다.

## OQ 상태

- **사용자 결정 OQ 0.** 닫은 것: OQ-01 · 02 · 03 · 04 · 05 · 06 · 07 · 11.
- HAR 요청: OQ-03 · 08 · 09 · 10 · 12 · 13.
- 기본값 확인만: OQ-14 ~ OQ-19.

## 주의

- DAY-SPEC-000 `staff.is_system_account`(L608) 설명이 아직 「사람이 아닌 계정(시스템 · 공용) — 원장 목록 등에서 뺀다 (cc KOS_EXCLUDE_ACCOUNT_IDS)」다. 실제(#226)와 이번 결정은 「sign-in 시스템 계정 하나」 — SPEC-000 을 고치지 말라는 지시라 두었다. 다음 SPEC-000 동기화 때 설명을 맞출 것.
