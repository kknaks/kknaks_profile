# [researcher] 추가 지시 — 처방전 상세 화면 주소(딥링크) — **실제 지점 HAR · 모양만**

앞 판 `reservation-prescription-report.md` 에 이어진다. 보고 · 질문은 예약 코디 **`term_fa2737b7-e69a-40e1-9fac-019199b9dad3`**. **앞 판 §0 규칙 그대로**: 실제 지점 테넌트 호출 금지(조회 포함) · 값(환자 · 처방 · 의사 · id)을 메모 · 덤프 · 리포트에 옮기지 않음 · 쓰기 0.

## 무엇을 하나

사용자가 실제 지점 KOS 에서 **고객 일정 상세의 처방전을 조회해 연** 장면을 떴다: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/처방전상세.har`(gitignore).

1. 그 화면의 **페이지 주소 꼴** — 문서 · Referer · Origin 에서. 앞 판 일정 상세 딥링크(`/{tenantId}/reservation/schedule/?visitorId=&scheduleId=&tab=`)에 처방 탭 값(`tab=…`)이 붙나 · 다른 쿼리(`prescriptionId` 등)가 있나 — **값은 `{…}` 꼴로만**
2. 처방전을 불러오는 호출(`get-prescriptions-by-ids` 등)의 요청 키 · 응답 키(값 없이)
3. 결론 한 줄: ccc [처방전 출력] 이 일정 상세 딥링크 하나로 그 처방전 화면까지 열 수 있나 · 필요한 값이 ccc 사본(일정 `visitorId` · `scheduleId` · `prescriptionIds`)에 다 있나
4. 「정할 것」은 Q-135 부터

## allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-prescription-detail-report.md`
