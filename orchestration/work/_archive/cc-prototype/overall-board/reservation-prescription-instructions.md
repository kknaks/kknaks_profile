# [researcher] 추가 지시 — 처방전(KOS 에서 출력 · 딥링크) — **실제 지점 HAR · 모양만**

보고 · 질문은 예약 코디 **`term_fa2737b7-e69a-40e1-9fac-019199b9dad3`**.

## 0. ⚠ 이번 HAR 은 데모가 아니다

`처방전.har` 의 테넌트는 **데모 값과 다른 실제 지점**이다(코디 확인 — 모든 KOS 요청이 데모 아닌 테넌트). 그러므로:
- **그 테넌트로는 어떤 호출도 하지 마라**(조회 포함). 운영 명동점 키(`KOS_API_tenent`)도 금지 그대로
- HAR 에서 **경로 · 본문 키 · 응답 키 구조 · 페이지 URL 꼴만** 읽는다. 환자 이름 · 주민번호 · 처방 의약품 · 의사 이름 · 면허번호 · 요양기관 번호 · 전화 등 **값은 메모에도 옮기지 마라.** 스크래치에 응답을 덤프하지 마라(필요하면 키 목록만)
- 확인은 **데모 테넌트로 다시**: 데모에 처방전이 있는 일정(`prescriptionIds` 비지 않은 것)을 공개 · 내부 **조회**로 찾아 같은 조회(`get-prescription`)가 되는지만. **쓰기 0건** — `print-prescription` 은 command 이므로 호출 금지

## 1. 무엇을 하나

사용자 결정(2026-10-26): 예약 상세 「귀가 대기」 정산 상자의 처방전 = **KOS 에서 출력**하게 한다(ccc 는 KOS 처방전 화면을 연다 — 수납처럼 딥링크). 사용자 화면 캡처: KOS 「처방전」 화면(교부번호 · 환자 · 처방의 · 의약품 표 · [처방전 저장] · [처방전 출력]).

## 2. 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/처방전.har` (30항목). 코디가 본 KOS: `v1/visitor/queries/get-visitor` · `drug_manage/v1/hospital/get`(400) · `role/v2/queries/get-roles` 여러 번 · `account/v2/queries/get-accounts` · **`prescription/v1/queries/get-prescription`** · **`prescription/v1/commands/print-prescription`**(2회). 전부 세어라
- 앞 판: `reservation-payment-discharge-report.md`(딥링크 꼴 `…/reservation/schedule/?visitorId=&scheduleId=&tab=` · Q-109) · `reservation-read-report.md` §3.1 25행(`prescriptionIds`)

## 3. 할 일

1. 인벤토리(경로 · 본문 키 · 응답 키 — 값 없이)
2. **처방전 화면 URL 꼴**: Referer · Origin · 문서 항목에서. 일정 · 처방전 id 중 무엇으로 여나(`{prescriptionId}` 꼴). 앞 판 딥링크 탭(`tab=…`)에 처방 탭이 있나
3. `get-prescription` 요청 키 · 응답 구조(키만) · `print-prescription` 이 무엇을 하는지(출력 기록? PDF?) — 키만
4. **데모에서 다시**: 데모 일정 중 `prescriptionIds` 가 있는 것을 조회로 찾는다(있으면 `get-prescription` 조회 1회 · 없으면 「데모에 처방전 없음」). 공개 API 에 처방전 조회 · 출력이 있나(스펙 grep)
5. ccc [처방전 출력] 후보: 딥링크로 KOS 처방전 화면을 연다 — 주소에 필요한 값이 ccc 사본에 있나(일정의 `prescriptionIds`)
6. 「정할 것」 Q-129 부터

## 4. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-prescription-report.md`

리포트에 개인 · 의료 값 금지. id · 토큰 금지.
