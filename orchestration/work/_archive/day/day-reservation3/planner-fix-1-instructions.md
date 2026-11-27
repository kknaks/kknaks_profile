# [planner] SPEC-008 고침 1 — 검수 1차 FAIL 3 · WARN 14 반영

너는 day `planner` 워커다. 맥락이 없으면 먼저 읽어라: 브리프 `day-reservation3-spec-brief.md` · 검수 리포트 `review-doc-1-report.md`(같은 폴더 · 지적마다 파일:줄 · 고칠 방향 있음).

워크트리 그대로(`mediness-mediness/day-reservation3-spec` · 미커밋 · allowed_paths `products/day/`). 아래는 **코디 기본값(11-26)** — SPEC 에 「코디 결정 11-26」으로 적는다.

## FAIL

- **F1** 확정 × 예약 없음 줄을 채운다: `change` → 새 버전을 `new` 로 기록 · [예약 생성] (취소됨 열과 같게) · `cancel` → 409. 취소됨 · 예약 없음 스레드의 `cancel` 409 메시지 뜻 = 「이미 끝난 요청」(철회 안내 아님). E3 철회의 409 기준은 248 「예약 있음」 정의 하나로 통일. OQ-Q10 닫음.
- **F2** `reservation_request.visit_id` 는 **W3(reserve) 확인 때** 연결. 「예약 있음」 = `visit_id` 있음 ∧ 그 예약이 취소 아님. `reservation_applied` · 상태 전이는 지금처럼 묶음 마지막 확인 뒤. spec-000 설명도 맞춤. OQ-Q19 함께 닫음.
- **F3** RQ23 · RQ27 그대로: [예약 수정]은 메모(합친 글) · 유입을 보낸다. 「보내지 않음」 대체 동작 삭제. OQ-Q02 = **구현 착수 전 실물 확인**(안 되면 사용자 질문)으로.

## WARN (전부 고침)

- W1 쓰기 확인 대기(`pending_version_id` 있음) 중: E3 = 409 · 자동 닫힘 건너뜀 · `cancel` = 예약 있음으로 봄.
- W2 create · update · cancel 409 조건에 「`pending_version_id` 있음」 더함(스레드 행 잠금).
- W3 스레드가 닫히거나 철회될 때 `waiting` 인 `change_request` → **대체됨**(`superseded`).
- W4 빨간 점 = **병원 공용**: 스레드 칸 하나(예: `hospital_seen_at` 와 링키 마지막 활동 비교 — 이름 제안) · SPEC-000 에 칸으로. OQ-Q06 닫음.
- W5 리포트 ①~⑤ 그대로: SPEC-005 U-6 에 target 모양(`requestId` · `date`) · 수는 늘 이 종류를 빼고 셈 · 목록만 transport(쿠키 / Bearer)로 거름 · 만든 뒤 `announce_unread` · `day.js` 갈래 · SPEC-006 ⑭ 에 `/reservations?request={id}` 한 줄.
- W6 Rule 2 이유 문장 고침(사본은 선택). 「이메일 없는 고객의 `customerId` 얻는 길」 = 새 OQ(**사용자 질문** · 코디가 지금 묻는 중 — 답 오면 따로 전달).
- W7 OQ-Q01 에 「KOS 새 예약 화면 『당일 지정 상담사』 저장 요청이 `reservation.counselor` 인지 브라우저 요청으로 확인」 더함 · W18 은 「확인 전 제안」.
- W8 시안 리포트 「지은 문구」 전부 「임시(기획 확인)」 — 한 표로 모아도 됨(OQ-Q04 연결).
- W9 ① 새 ext 오류 코드 `message` = 「임시」 표시하고 OQ-Q04 에 ext 글자 포함 ② 길이 상한(코디 기본값): 이름 · 발음 이름 100 · 이메일 254 · SNS 계정 100 · 희망 시술 500 · 예약 메모 1000 · `reason` 500 · 댓글 `body` 1000 · `authorName` 50 — 넘으면 400 ③ `phone` = 숫자만 · 앞 0 없음 · 아니면 E1 에서 400.
- W10 partner 표에 테스트 파일 줄 · 유일키 좁히기 전 중복 행(겹치면 migration 이 멈추고 보고) · 한도 합쳐짐(병원당 분당 60) · `_charty` 403 없어져 링키 키로 차티 경로 열림 → 「taewoo 리뷰 확인」 항목.
- W11 [고객 차트] 경로 `/customers/{customer_id}/chart` · 권한(기존 보기 키) 적고, SPEC-007 D46(이름 누르면 「준비중」)과 다름을 「시안과 다른 곳」에 한 줄.
- W12 「최근 방문」 · 「보유 시술권」 · 「직원 메모」 원천 = 본문에 「제안 · OQ-Q18」 붙임.
- W13 stable SPEC 넷의 개정 머리에 「DAY-SPEC-008 stable 전까지 계획 · 코드 없음」.
- W14 그대로.

## 그 밖 OQ 코디 기본값(검수 분류대로 닫음)

Q07 통역 코드 = DAY 앱 언어 목록(`APP_LANGS`)과 같은 코드 · 한국어 이름표를 SPEC 에 · Q09 「요청됨 그대로」 · Q11 영소문자 · 숫자 · `-` 1 ~ 16 · Q13 (`updated_at`, `id`) 커서 · Q14 줄바꿈 그대로 · Q16 웹 예약 등록 `start_at` 과 같게 · Q17 제안 그대로 · Q18 위 W12.
남는 사용자 질문 = Q04(문구 · 기획) · Q05 · Q08 · Q12 · Q15 · W6 새 OQ — 열린 채로 둔다.

## 검증 · 보고

lint `--strict` products/day ERROR 0. 보고에 F · W 번호별 고친 자리(파일:줄). 완료 보고는 1판 브리프 §9 두 명령 그대로 · subject `planner 완료: SPEC-008 고침 1`.
