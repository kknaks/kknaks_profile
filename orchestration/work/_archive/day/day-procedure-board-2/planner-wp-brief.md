# [planner] WP 정리 — Delivery #236 다시 쓰기 · #234 A6 정리

같은 스펙 워크트리(PR #920 · 마지막 커밋 e421b77b · 미머지). 레포 Skill `start-delivery`(`.claude/skills/start-delivery/SKILL.md` · `tools/harness/references/requests.md`). 파일 수정 · 커밋 금지 — Issue 만.

## 1. CENTURION_DAY#236 — 같은 key `day/board-plan-align-1` · contract_version +1 · scope_delta
SPEC-002 개정 ⑬ · ⑭(현재 브랜치)를 결과 계약으로. **Target Delta = 아래 16개 전부**(사용자에게 보인 구현 리스트 — 정본 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md` §2):
- A 고객 카드: ① 체크박스 대기 줄만(전체/부분) ② 고객 이름 누르기 없음 ③ 시술 이름 → 차트 모달(전체 차트는 ④ 차트 작업) ④ 「⋯」 늘 보임 ⑤ 카드 스크롤 먼저 → 끝/없으면 판
- B 고객 검색: ⑥ 「시술 완료」 탭 검색 — 이름(발음 · 영문) + 담당 원장 + 관리실 · 누르면 같은 차트 ⑦ 상단 검색 칸(E06) 뺌
- C 확인 필요(사이드 · 팝업 없음 · 빨강): ⑧ 5상황(마취 전 대기 5 · 마취 초과 20 · 받지 않은 호출 5 · 수락 뒤 미시작 5 · 귀가 대기 전 즉시) · 풀리는 때 · since ⑨ 귀가 대기 전 카드 [귀가 대기] ⑩ [재호출] 호출 중 줄에 늘 · 글자 검정
- D 마취: ⑪ [마취 시작] → [마취중 mm:ss][마취 종료] → [마취 완료 mm:ss][마취 시작] 반복 ⑫ [귀가 대기]가 열린 마취 닫기
- E 호출 · 수락 · 상태: ⑬ 「{원장} 수락 완료 HH:MM」 · 「{원장} · 진행 mm:ss」 · 「{원장} · n분」 ⑭ 담당 원장 바꾸기(툴팁 「원장 교체」 · 원장 목록 · KOS change-tasks-doctors 1명 덮어쓰기 · 새 원장 표시 · 수락 뒤 미시작 다시 셈 · 취소/변경 알림은 앱 연결 전까지 기록만) ⑮ 동시 수락 「다른 원장이 먼저 받았습니다」 ⑯ 시작 취소 · 완료 취소 확인 모달
- Acceptance 는 항목별로(화면 테스트 · API 테스트 · 데모 실물이 필요한 것 = ⑭ 원장 바꾸기 KOS 반영)
- Non-Goals: SPEC-002 「기획안 중 이번에 안 하는 것」 표 · 관리실 이동 · 관리실 기록 · 전체 차트(④)
- Execution: 코드 레포 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2`(브랜치에 #234 커밋 96fff917 이미 있음 — 그 위에서). backend(검색 라우트 · 확인 필요 계산 · 원장 바꾸기 · 마취 · 동시 수락 · 귀가 대기 마취 닫기) / frontend(카드 · 모달 · 스크롤 · 툴팁 · 「⋯」 · 상단 검색 칸 · 빨강 · 검정) 나눠서 phase
- baseline pending(#920 미머지). L2/L3 면 `delivery-plan:review` 에서 **멈춘다**(승인 대행 금지)

## 2. CENTURION_DAY#234 — 같은 key `day/demo-live-unify` · version +1 · scope_delta
- A6 데모 실물 확인을 사실대로: 시작 취소 ✅(HAR · 데모) · 완료 취소 ✅ · 귀가 대기 1 ✅ · 귀가 대기 2 ✅(PROCEDURE_DONE = KOS 「귀가 대기」) · **① 재호출 = [재호출] 버튼 경로**(체크박스는 대기 줄만이 되어 「이미 수락된 줄 다시 호출」 경로 없음) ✅ — 모두 사용자 2026-11-09 데모 확인. 근거 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md` §2 「#234 A6 데모 실물 정리」 행
- Target Delta (가)의 「재호출의 call-tasks-doctors 재전송」을 「호출 중(WAITING) 작업 재호출」로
- 계약이 바뀌면 `delivery-plan:review` 로 돌아간다 — 멈추고 보고

## 완료 보고
두 Issue 의 version · plan_digest · 라벨 · next_action. 코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd`(원 브리프 §9 두 명령 — orchestration send worker_done + terminal send).
