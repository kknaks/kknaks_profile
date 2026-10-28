# [researcher] 추가 지시 — 상담 구간 KOS 순서 (HAR 해석 · 조회)

앞 판 `reservation-move-cancel-report.md` 에 이어진다. 완료 보고 · 질문은 예약 코디 **`term_fa2737b7-e69a-40e1-9fac-019199b9dad3`**. 데모 테넌트 assert · 운영 키 금지 그대로. **이번 판은 KOS 쓰기 0건**(HAR 해석 + 조회만 — 쓰기 시험은 결과를 보고 따로 지시한다).

## 1. 무엇을 하나

사용자(2026-10-26): 「**상담 완료 상태가 없고 시술 대기로 넘기는 것 같다**」. 사용자가 데모에서 한 고객의 상담 과정을 HAR 로 떴다. KOS 상담 구간이 실제로 어떤 순서 · 호출인지 적고, 시안 상담 카드(design-analysis-report §3.4 「내원 현황」 2 — 상담 대기/진행 중/완료 · [상담사 선택/변경] · [○○ 실장 호출] · [+ 상담 추가])와 비교한다.

정해진 것(`_RESUME` §2): 상담 필요 → [접수 완료] 한 번에 상담 대기까지 · 상담사 목록 = ccc 직원 사본(`getAccounts` COUNSELOR) · 상담 필요 = `consultationRequired` · 상태 2계층(상담 ─ 대기 · 진행).

## 2. 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/상담.har` (gitignore · 58항목). 코디가 본 쓰기:
  - #4 `schedule/v1/commands/recept` → #13 `schedule/v1/commands/change-flow-step` → #27 `schedule/reservation/v2/commands/update-reservation` → #35 **`consultation/v1/commands/create-consultation`** → #53 `schedule/v1/commands/change-flow-step`
  - **이 목록으로 끝내지 말고 KOS 요청을 전부 세어** 인벤토리를 만든다
- 앞 판: `reservation-read-report.md` §3.1 22행 · `reservation-create-report.md`(F10 `counselor` · `consultationRequired`) · `reservation-move-cancel-report.md`(update-reservation 필드)

## 3. 할 일

1. 인벤토리(순서대로 · 본문 키 · 응답 모양 · 화면 동작 추정).
2. 쓰기 5건 해부(값은 모양만): 두 `change-flow-step` 이 각각 어디서 어디로(상담 대기 · 상담 진행 · 시술 대기?) · `update-reservation` 이 무엇을 바꿨나(`counselor`? `consultationRequired`?) · **`create-consultation` 본문 전체**(상담사 · 상담 의사 · 시작 시각 · 상담 내용 · 상담 시술 · 오더 메모?) — 상담사 「배정」이 어디에 남나(`reservation.counselor` / `consultation.counselor` / `consultations[].counselors[]`)
3. **「상담 완료」가 KOS 에 정말 없나**: flowStep enum · 상담 객체에 종료 시각/상태 필드가 있나(스펙 · 응답). 상담이 끝났다는 것을 무엇으로 알 수 있나(시술 대기로 넘어감 · `consultations[]` 생김 · 시각)
4. 전후 상태: HAR 응답 + 지금 데모 같은 일정 **조회**로 flowStep · counselor · consultations[] · tasks[] 변화
5. 공개 짝: `updateScheduleConsultationInfo` 등 공개 상담 작업 — 필드 · HAR 과 차이
6. 시안 비교: 상담 카드 상태 3개(대기/진행 중/완료) ↔ KOS · [상담사 선택] = KOS 의 무엇 · [실장 호출](KOS 에 호출 개념이 있나) · [+ 상담 추가](상담 두 번?). 상담사 「지금 상태」(A-룸2 상담 중)를 KOS 값으로 알 수 있나(Q-14)
7. 「정할 것」 Q-92 부터 — 결정하지 마라

## 4. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-consultation-report.md`

리포트에 id · 토큰 · 이름 · 상담 내용 등 값 금지(모양만).
