# planner 0.5.1 — doc r7 FAIL 1 · WARN 1~6 (재검수 없음 · 구현 전 마지막)

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-doc-r7-report.md`.
- **F-1** 리포트 「고칠 것」(규칙 두 줄 + 시험 둘) — 확정(잠금)한 달의 수수료가 [전체 다시 받기]로 바뀌지 않게 · D-21 유지. 「잠글 때 얼리기」 대안은 쓰지 않는다
- **W-1** 새 달 스냅샷은 GET 이 만들지 않는다 — 설정 화면을 처음 열거나 [저장]할 때(쓰기 API)만. 매출 GET 은 스냅샷이 없으면 「미설정」으로 읽기만
- **W-2 ~ W-6** 리포트대로. W-3(양수 「앞 달 결제 취소」 수수료)은 기본값 = 「—」 그대로 + OQ(코디) · W-4 같은 이름 상품 둘이면 설정 화면에 「같은 이름 n개 · 한 비율」 표시
- W-7 은 코디가 처리함
- §「구현 때 지킬 것」은 손대지 말 것(구현 브리프에 붙음). 판 0.5.1 · public grep · 원 브리프 §9 두 채널(같은 task/dispatch) · subject 「planner 0.5.1 완료」
