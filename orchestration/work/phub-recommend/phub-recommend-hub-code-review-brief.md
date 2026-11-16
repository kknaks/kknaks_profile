# [reviewer_code] Hub 선택 관계·전역 메모 코드 검수

너는 read-only 코드 검수 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다.

## 읽을 것

- PROCEDURE-HUB 레포 `AGENTS.md`와 관련 `.agents/skills/`·backend 규칙, 현재 diff와 신규 `selected.py`/시험
- 정본(읽기 전용): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-005.md` 0.3.9 §5-5·§5-16·§6-9, `WORK-011.md`, `SPEC-006.md` 0.3.10 §3-4-1-5
- 당시 HEAD `2edc190`; 워커 보고: 4,687 pair 최대 30,354B, Q139 559B, scope:all 210,511B→truncated, 전체 unit 902 passed/14 xfailed, Ruff 통과

## 검수

REST selected pair/global claims와 MCP selected_pair/global_claims가 같은 코어·schema/상태를 쓰는지 본다. 방향·prior·조건·정규화 쌍, 묶인 pair의 단일 쌍, claim/대안별 fact ID·원문·source·applies_to, Q139 별도 scope, found/empty/truncated/error와 complete 의미, 인용 가능성 판정을 실제 Gold 구조와 시험에 대조한다. 특정 pair/scope가 결과에서 누락됐는데 empty/complete가 될 수 있는지, 64/32KiB 응답 상한 초과를 앱이 여러 호출/페이지로 회복할 방법이 있는지 확인한다. 기존 T4와 page=1 ID 순서/page≥2 `more`/cut/peek bytes 회귀도 본다. 공개 API의 오류 처리/직렬화 차이가 있으면 지적한다.

사용자 요구는 앱의 전체 그래프 탐색을 고정 바이트에서 끊지 않는 것이다. Hub의 **호출별** 상한을 전체 탐색 종료로 오인하는 경로가 있는지 본다. 이 리뷰는 코드 수락 전 판정이다. FAIL/WARN/PASS, 파일:줄·근거·최소 수정안으로 보고하고 앱 관계 어댑터 발주 가능 여부를 분명히 적는다. 필요한 소수 시험은 격리 실행 가능하지만 사용자 서버·포트·DB·컨테이너는 조작하지 않는다.

## 허용 범위

- 읽기 전용. 보고 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-hub-selected-code.md`만 생성.
- 코드·SPEC·WORK·서버·DB 수정 금지. 커밋·push·PR 금지. 완료 시 dispatch preamble대로 `worker_done` 한 번.
