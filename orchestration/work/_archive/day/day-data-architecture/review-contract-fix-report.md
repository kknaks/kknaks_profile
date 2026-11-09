# 리뷰 리포트 — 가벼운 3건 재확인 · SPEC-002 ⑧ · #231 v4 · #230 v7 (2026-11-06)

대상: mediness `spec-002-procedure-board.md` · `log.md` diff(미커밋) · Issue #231(`contract_version=4`) · #230(`=7`) · `delivery/v2-board-screen.json` · `v2-board-backend.json` · 작성 리포트 `planner-contract-fix-report.md`. 앞 리포트 `review-contract-230v6-231v3-report.md` N1 ~ N3.

lint `--strict` → 0 error. 라벨은 둘 다 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending`이다 — **승인 없음**.

## 판정: PASS

| 건 | 지금 | 판정 |
|---|---|---|
| N1 #231 옛 HAR 줄 | 두 줄을 걷었다. Review Surface 에는 「HAR 요청 = OQ-03 · 12 · 13 만 — 화면 영향은 「시술 완료」 탭 방별 묶음 없음 · OQ-08 · 09 · 10 은 닫힘(#230)」만 남았다 | 닫힘 |
| N2 #230 W8 줄 | 「수락할 의사가 DAY 에 로그인해 있어야」를 지우고 「누르는 쪽 = `DAY_ADMIN_EMAILS` 계정(또는 간호사) 대리 수락 · `doctorIds` 의 데모 원장은 KOS 직원 목록에 있기만 하면 됨」으로 바꿨다. 「원장 본인 DAY 로그인 계정이 따로 필요한지(W8)는 코디가 사용자에게 확인」은 Review Surface · open_question 에 남겼다. 누른 사람 토큰 줄(F10 · cc D-27 실호출)도 함께 들어갔다 | 닫힘 — 규칙 24 와 맞다 |
| N3 F1 팝오버 ↔ SPEC | SPEC-002 개정 ⑧ 이 들어갔다. U-4 의사 호출 창 위치를 「누른 버튼 바로 아래 팝오버(아래 없으면 위 · 오른쪽 넘치면 왼쪽 · 덮개 없음 · 바깥 클릭 · Esc · X · 폭 약 640) · 내용 · 두 칸 그대로」로 바꿨다. U-5 재호출 · U-6 수락 창도 같은 팝오버다. 화면 구성 표 E51 줄에 「셋 다 팝오버」를 적었고, 차트(E55)는 모달 그대로 뒀다. board-feedback F1 내용과 같다. #231 A5 · Review Surface 도 「SPEC ⑧ 에 반영됨」으로 맞췄다 | 닫힘 |

## 남은 것 (코디 몫 · 지적 아님)

- 원천 `screen/procedure-board-decisions.md` L78 「화면 참고 — 의사 호출 창」은 아직 「**모달** · 왼쪽 = 고르기 …」다. SPEC ⑧ 머리말은 「원천의 「모달」을 바꿈」으로 이력을 남겼다. 원천 문구를 팝오버로 맞추는 일은 코디 몫이다.
- W8(원장 본인 DAY 로그인 계정이 필요한지)은 사용자 확인 대기다(지시대로 열린 채).
- 거절된 `delivery/v2-board-screen.v2.apply.json` 과 이름에 공백이 든 빈 파일 4개를 정리해야 한다.
