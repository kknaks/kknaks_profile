# [planner] Delivery #262 · #263 v2 재결속 — 스펙 PR 커밋 기준(머지 전)

같은 워크트리. 스펙은 커밋됨: 브랜치 `kknaksss/day-mobile-v2-spec` `7d198317` · PR MediSolveAIDev/mediness#955(**머지는 나중** — 사용자: 다른 스펙 작업이 같이 돌고 있어서). 

## 할 것
1. CENTURION_DAY#262 · #263 을 같은 key 로 contract_version 2 재결속 — baseline = 지금 워크트리 HEAD `7d198317`(머지 전 PR 커밋). harness 가 main 머지를 요구해 막히면 **억지로 우회하지 말고** 막힌 이유 · 명령 출력을 그대로 보고하라.
2. 재결속 내용에 반드시 반영(목록 = `spec-2-report.md` · `spec-3-report.md` 의 「v2 재결속 때」 · 검수 W-15 · W-16):
   - A2 `can*` 판정 = 서비스 거절 규칙 정본 · A3 호출 취소 확인 창 없음 · M-6 본문 「{방} · 호출 취소」 · 호출이 완전히 닫힐 때만
   - 단계 시작 조건 = 의존 표대로(통역 P1 → P5 를 따로 앞당김 · designer P4 는 스펙만 기다림) — 전부 직렬 금지
   - 출시 순서 prod 서버 먼저 → 정식 앱 · 되돌리기에 통역 되울림
   - #263 FCM: Firebase 준비됨(값은 레포 밖) — 「사용자 대기」 조건 걷기
3. 승인 receipt 는 적용하지 마라(사용자 몫).

## 보고
`spec-5-report.md`(같은 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/`) — 두 Issue 의 새 digest · baseline · 반영 항목 체크 · 막힌 것. 문서 수정 · 커밋 금지(재결속에 스펙 수정이 필요하면 멈추고 보고). 완료 보고는 dispatch preamble 의 worker_done 그대로.
