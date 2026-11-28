# planner-fix-1 결과 보고 — SPEC 개정 검수 1차 WARN · OQ 닫기

## 상태: done (OQ-R41 보류 — 코디 정정)

워크트리 `mediness-mediness/day-reservations-fix-spec` 미커밋 그대로 · 커밋 · push 없음. 변경 파일 = products/day 8개(10-decision · 20-spec.md · spec-000 · 002 · 003 · 006 · 007 · log).

## W 별 고친 곳

| W | 고친 곳 | 내용 |
|---|---|---|
| W1 | spec-002 「원천 고르기」 원칙 줄 바로 뒤 | 「지금 남은 공개(open) 호출 — 목록만 · 이번에 바꾸지 않음」 표 7줄: `identity.py:29-31`(문진 양식 · 약관 · 제출) · `writes.py:91` `cancel-reservation` · `ext_reads.py:22` `get-schedules-by-visitor` · `ext_reads.py:282` `update-schedule-consultation-info`(상담 메모) · 데모 `kos_board.py:45`. 문진 읽기 · 양식 맞춤에는 넣지 않는다고 적음 |
| W2 | spec-007 §3 「KOS 문진 읽기」 「언제」 칸 · 호출량 줄 / spec-002 루프 표 아래 2026-11-27 줄 | **일정 회차가 끝난 뒤 발행하는 별도 태스크**(구매 회차 ② ~ ④ 꼴 · 입력 = 같은 일정 응답의 고객 · 일정 태스크 안에서 안 부름) — 두 문서 같은 말 · 「10초 회차 실행 시간이 늘어남」 문장 지움 |
| W3 | spec-002 「오늘 회차 호출 수」 줄 | 결정 1 의 예외 — 「+ 문진 미확인 고객 수」 · 사용자가 받아들인 호출량이라고 적음 |
| W4 | spec-007 앱 JSON 짝 표 · spec-003 머리 · U-26 글자 | `questionnaire.expired: bool`(이름 제안 · 행 없음 = `questionnaire` null) · 앱 상세가 이 값으로 「6개월 경과」 |
| W5 | spec-000 머리 「2026-11-24 개정 ②」 | `> > ` → `> ` 되돌림 |
| W6 | spec-002 · spec-003 frontmatter | `last_updated: 2026-11-27` |
| W7 | 20-spec.md 예약 현황 줄 | `~~카드 높이 한 줄 고정(R70)~~` + 개정 ⑯ 표시 · R64 줄에 「길이 비례 높이와의 관계 = OQ-R41」 꼬리표(R41 보류라 R64 는 긋지 않음) |
| W8 | log.md | 그대로(코디가 PR 때) |

## 닫은 OQ (본문 규칙으로 옮김)

| OQ | 닫은 값 | 본문 자리 |
|---|---|---|
| OQ-R42 | 짧은 카드 = 높이 길이 그대로 · 넘치는 글자 잘림(시안은 모달 디자인 때) | spec-006 U-5 · 케이스 15분 줄 · OQ 표 |
| OQ-R43 | 같은 시작 = R73 순서 · 동행 = 이어진 빈 자리 첫 묶음 · 띠 = 멤버 다 감싸는 상자 | spec-006 U-5 · U-9 · OQ 표(Rule 15 문장은 R41 보류로 안 건드림 — 그 안의 「OQ-R43」 언급만 남음) |
| OQ-R44 | 앱 예약현황 표도 이번에 같이 — 60분 = 2칸 · 겹치면 옆 자리 · 서버 같은 배치 값 | spec-006 개정 ⑯ 보충 · spec-003 머리(「앱 화면 변경 없음」 메모를 취소선 · 앱 표 규칙으로) · U-25 새 줄 |
| OQ-D44 | 기기 없는 열린 문진 요청이 있으면 링크 복사 · 열기는 그 링크 다시 씀(nonce 로 토큰 다시 만듦 · 시한 그대로) · 기기 줄 = 취소 → 새 요청 | spec-007 규칙 2 · 케이스 3줄 |
| OQ-D45 | 다시 그리기가 팝오버를 닫지 않음 · e2e 확인 항목 | spec-007 규칙 7 |
| OQ-D46 ① ~ ④ | ① `inputType` · `subText` 비움 · `read` 행 INPUT_BOX 판정 = `memo` 유무(내부 양식 경로가 HAR 로 나오면 양식 맞춤으로 · 공개 없음) ② 제출 id = 읽기 id 는 로컬 e2e 1회 제출로 확인 ③ 받은 한 건 = 마지막 ④ 그 고객만 건너뜀 · 행 안 지움 | spec-007 §3 「KOS 문진 읽기」 표 · 답 맞춤 표 · 「제출 id 남기기」 |
| OQ-D47 | 앱 JSON `questionnaire.expired` + 앱 상세도 「6개월 경과」 | spec-007 앱 JSON 짝 · spec-003 머리 · U-26 |
| OQ-D49 | KST 날짜 + n 개월(달력) · 글자 「6개월 경과」 고정 · 건강정보 보임 | spec-007 U-3 |

spec-007 에 「고침 8 보충」 머리 단락 · spec-006 에 「개정 ⑯ 보충」 단락을 더해 위를 한곳에 적음.

## 보류 · 남은 OQ

- **OQ-R41 — 보류**(코디 정정 · 사용자 「5장 규칙은 해야 한다」 · 행 단위 정하는 중): R64 · 열 폭 · `lines` · Rule 15 문장은 손대지 않음(이번 고침에서 바꾼 줄 없음 · 20-spec.md 에 한때 「R41 닫음」을 썼다가 같은 턴에 되돌림 — 최종 diff 에 없음).
- **OQ-D43** 진행 칸 · 복사 알림 글자 — 열린 채 · 그 전까지 지금 글자 · 알림 없음.
- **OQ-D48** 다른 날 낸 문진 글자 — 열린 채 · 그 전까지 지금 글자.

## 참고 반영

- 「중복 가르기 빈틈」(고침 8 전 DAY 제출 행 `external_ref` 없음) → spec-007 §3 「KOS 문진 읽기」 끝 「알고 감」 한 줄(백필 안 함).

## 검증

- `python3 scripts/lint-pipeline.py --strict` → exit 0 · ERROR 0 · products/day 줄 0(ERROR · WARN). 다른 제품 기존 WARN(procedure-hub · selly · charty · mediness)은 무관.
- 새 공개 KOS 호출 0 · 새 화면 문구 0(「6개월 경과」는 결정 글자 재사용).
