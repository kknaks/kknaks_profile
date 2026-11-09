# planner-contract-fix 결과 보고 — done (미커밋 · 승인 안 함)

1. **SPEC-002 개정 ⑧**(N3 · F1) — U-4 의사 호출 창 위치 = 누른 버튼 바로 아래 팝오버(아래 없으면 위 · 오른쪽 넘치면 왼쪽 · 덮개 없음 · 바깥 클릭 · Esc · X · 폭 약 640 · 내용 · 두 칸 그대로) · U-5 재호출 · U-6 수락 창도 같은 팝오버 · 화면 구성 표 E51 줄 · 차트(E55)는 모달 그대로. `log.md` 한 줄 · lint `--strict` 0 error. (원천 screen 「화면 참고」의 「모달」 문구는 코디 몫.)
2. **#231 contract v4** — [Issue #231](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/231) · **`sha256:7253c3be9562eda2494c1aee2178776f38f115b3f4d1042fe4dd44025c61d0f3`**. Review Surface 의 지난 판 줄 둘(HAR 미확인 KOS 쓰기 · HAR 미확인 버튼 처리) 걷고 「HAR 요청 = OQ-03 · 12 · 13 만 · 화면 영향 = 시술 완료 탭 방 묶음 없음」 · F1 줄 = 「SPEC-002 ⑧ 에 반영됨」(N1 · N3).
3. **#230 contract v7** — [Issue #230](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/230) · **`sha256:f42df733df556f532bf19728993342e9131ec3fe9f7dc79276ce923b300e75af`**. W8 줄의 「수락할 의사가 DAY 에 로그인해 있어야」 삭제 → 「누르는 쪽 = DAY_ADMIN_EMAILS 계정(또는 간호사) 대리 수락 · doctorIds 의 데모 원장은 KOS 직원 목록에 있기만 하면 됨 · 원장 로그인 계정이 따로 필요한지(W8)는 코디가 사용자에게 확인」 · A8 수락 단계 문구 · open_question 같은 뜻으로(N2).

라벨 둘 다 `delivery-plan:review`. 거절된 `delivery/v2-board-screen.v2.apply.json` 은 그대로 둠(지우는 건 코디).
