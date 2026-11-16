# [planner] SPEC-002 손보기 — 고객 검색 바로잡기 · 실물 확인 반영 · OQ 닫기 (스펙만)

너는 day planner 워커다. 역할 문서 먼저: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/planner/role.md`(+ 같은 폴더). 앞 작업 기록: 같은 폴더의 `planner-plan-align1-brief.md` · `planner-align1-finish-brief.md` · 리뷰 `review-doc-align1b-report.md`.

작업 워크트리 = 스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec`(브랜치 `kknaksss/day-procedure-board-2-spec` · PR #920 · 마지막 커밋 24949777). 커밋 · push 금지(코디가 한다). **Delivery #236 · #234 손대지 마라.**

정본 = `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md` §2 결정 표 — 2026-11-09 ~ 11-10 행. 이번에 반영할 것:

1. **고객 검색(U-13) 바로잡기**(11-10 · 코디가 잘못 넣었던 것): 대상 = **「시술 완료」 탭 고객만**(오늘 귀가 대기 · 귀가 — 지금대로). 「카드가 생겼던 고객 전부 · 지난 방문 · 최근 방문일」 문장 · 결과 줄 · 정렬 · 매트릭스 · API · 스냅샷 · OQ-25(최근 방문일 날짜 모양) 등 관련 자리 전부 바로잡기(grep 전수). 찾는 말 = 이름(발음 · 영문) + **담당 원장 이름 · 관리실 이름**. 누르면 차트(시술 이름과 같은 차트). 상단 검색 칸(E06) 뺌은 그대로
2. **데모 실물 확인 반영**(11-09 사용자): 완료 취소(change-tasks-complete complete=false → KOS 진행 중으로 되돌려짐) · 귀가 대기 1(cancel-flow-tasks reason=CANCEL → KOS 방 배정 작업 없어짐) · 귀가 대기 2(change-flow-step PROCEDURE_DONE → KOS 「귀가 대기」) · 재호출(call-tasks-doctors 다시 → KOS 다시 호출 상태 · 호출 시각 새로) — §3 KOS 쓰기 표 확인 상태 「확인 안 됨」 → 「데모 실물 확인됨(사용자 2026-11-09)」 · OQ-23 정리
3. **OQ-22 닫기**: PROCEDURE_DONE = KOS 「귀가 대기」 단계(KOS 웹 고객 창 머리 「귀가 대기」) · KOS 웹 「귀가」 COMPLETED 는 그다음 단계(실제 귀가)
4. **OQ-31 닫기**: `집도의변경.har` = KOS 웹 집도의 변경이 `change-tasks-doctors {scheduleId, sequences, doctorIds:[1명]}` 1건 · `삭제후의사호출.har` = doctorIds 없이 → 집도의 비움 + call-tasks-doctors ⇒ **목록 덮어쓰기(교체)** · 바뀐 뒤 집도의 = 고른 1명(사용자 확인). 원장 바꾸기 행 확인 상태 「확인됨(HAR · 사용자)」
5. **재호출 설명 한 줄**: KOS 에는 「재호출」 기능이 없고 다시 의사 호출뿐 — DAY [재호출]은 같은 call-tasks-doctors(호출 중 줄은 집도의가 비어 있어 KOS 웹 「다시 의사 호출」과 결과가 같다)
6. **디자인**: 확인 필요 카드 [재호출] 버튼 글자 = 검정(꺼진 것처럼 보이지 않게)

화면 문구는 결정 · 기획 「」만. lint --strict products/day ERROR 0. log.md 같은 날(11-10) spec-change 행.

## 완료 보고
바뀐 절 · 닫은 OQ · lint. 코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd`(원 브리프 §9 두 명령).
