# [planner] SPEC-008 마감 — main 충돌 풀기 + 코드 · e2e 결과 반영 (planner-close-1)

너는 day `planner` 워커다. 맥락이 없으면 먼저 읽어라: `day-reservation3-spec-brief.md`(규칙 · 완료 보고 §9) · `_RESUME.md` §2(11-26 · 11-27 결정 전부).

워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation3-spec` — **지금 git rebase 가 진행 중이다**(코디가 우리 두 커밋을 하나로 합쳐 `origin/main` 위로 올리는 중 · 충돌 7 파일). **git 명령(add · rebase · commit · reset · checkout)은 하지 마라** — 파일 내용만 고친다. 끝나면 코디가 add · continue 한다.

## 1. 충돌 풀기 (먼저)

충돌 파일: `products/day/10-decision.md` · `20-spec.md` · `20-spec/spec-000-data-model.md` · `spec-005-notifications.md` · `spec-006-reservation-board.md` · `30-work.md` · `log.md`.

- main 쪽(`HEAD` — #964 · #969 · #967)과 우리 쪽을 **둘 다 살린다**. 어느 한쪽을 지우지 않는다. 개정 번호 · 목록 순서가 겹치면 main 것을 앞에, 우리 것을 다음 번호로.
- **SPEC-007**: main #964 가 이미 「고침 6」을 썼다 → 우리 것은 **「고침 7」**. spec-007 · spec-008 · 20-spec.md · log · 30-work · Delivery 문구 등 우리가 「007 고침 6」이라 쓴 곳 전부를 grep 해서 「고침 7」로(main 의 고침 6 은 그대로).
- 같은 방식으로 SPEC-000 · 005 · 006 개정 번호(③ · ⑭ 등)가 main 과 겹치는지 확인하고 겹치면 다음 번호로.
- 끝나면 `grep -rn "^<<<<<<<\|^=======\|^>>>>>>>" products/day` = 0.

## 2. 코드 · e2e 결과 반영 (코드가 맞다)

근거: `be-swagger-1-report.md` ④ 표 · `be-swagger-2-report.md` · `fe-nav-1-report.md` ⑤ · `be-probe-1-report.md` · `be-probe-2-report.md` · `e2e-1-report.md` · `e2e-2-report.md` · 코드 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation3`(dev `65506f35` 에 머지됨 · 읽기만).

- SPEC-008:
  - 판정 Rule 1 = 이름(대소문자 · 띄어쓰기 무시) + 식별값(생년월일 · 연락처 · SNS · 이메일) 하나 이상 정확히 같음 · 국적은 둘 다 있을 때만 · 1 = 재진 · 0 = 초진 · 2+ = 「고객 확인 필요」
  - 본문 `birthDate` 선택 · 식별값 하나 이상 필수(400)
  - [예약 생성] = W3 `reserve` 에 `counselor` 바로(W18 없음) · W18 = [예약 수정]에서 바뀌거나 지울 때(`counselor: {}`) · W1 에 이메일
  - 예약이 이미 취소된 스레드에 `cancel` = 202 `canceled` + `reservation_applied` `cancel` · 동기화 때 자동 `canceled`
  - E2 다른 고객 `change` = 400 `customer_changed`(OQ-Q15 닫음)
  - `Idempotency-Key` 재시도 = 처음 응답 그대로(`accepted_status`)
  - 스웨거에 상태값 뜻 · 상태 × 행동 · 오류 코드 · 흐름이 있다는 한 줄 + 오류 코드 목록(be-swagger-1 ③)
  - e2e 결과(실제 KOS 데모 2회 통과 · 날짜 · 확인 항목) · 배포(dev `65506f35` · CENTURION_DAY#299 · ext 키 새 형식 · prod 는 다음)
  - 화면 문구 결정: 「KOS 등록 실패」 · 「답변 대기중」(사용자 11-26)
- SPEC-000: `reservation_request_version.accepted_status` 칸.
- **SPEC-001**: 로그인 뒤 갈 곳 = **예약 현황 `/reservations`**(사용자 2026-11-27 · 11-06 「시술 현황」을 바꿈). 셸 메뉴(아이콘 줄) 「홈」 → **「현황」**(키 `status`) · 예약/원내/시술 현황 탭은 현황 아래 · 화면 있는 메뉴 = 고객 · 현황 · 현황 화면은 모든 직원이 본다. SPEC-002 · SPEC-006 에 「아이콘 줄 시술/예약이 켜진다」 같은 줄이 있으면 「현황」으로. 이 개정은 SPEC-001 개정 머리에 번호를 붙여 적는다.
- 「아직 정하지 않은 것」: 정책 15 와 다름(후보 화면 없음 · 판정 규칙) → 기획 통보 · OQ-Q05 · Q08 열린 채 · 취소 버전 reason 줄 이름 · 2+ 배지 문구 · 외부 에이전시 페이지(시안 v1 · 이 SPEC 범위 밖).
- stable 로 올릴 수 있으면 올리고(구현 · dev 배포 · e2e 끝), 못 올리면 이유.
- `log.md` · `30-work.md` · `20-spec.md` 줄 갱신.

## 검증 · 보고

`lint-pipeline --strict products/day` ERROR 0 · 충돌 표지 0. 리포트 `planner-close-1-report.md`(이 폴더): ① 충돌 푼 방법(파일마다 · 번호 바꾼 곳) ② 반영한 것(파일:줄) ③ stable 여부 ④ 남은 것. 완료 보고는 브리프 §9 두 명령 · subject `planner 완료: SPEC-008 마감`.
