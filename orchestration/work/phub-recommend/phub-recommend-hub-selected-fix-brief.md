# [PROCEDURE-HUB backend] 선택 관계 코드 검수 FAIL 수정

너는 앞 판 Hub 코드의 수정 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다. 현재 Hub worktree의 미커밋 변경을 이어서 고친다.

## 읽을 것

- 필수: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-hub-selected-code.md` 전체 FAIL 1~4/WARN과 `SPEC-005.md` 0.3.9 §5-5·§6-9, `WORK-011.md`
- 현재 diff, `backend/app/modules/gold/selected.py`, 관련 schema/route/MCP/service/시험, 실물 Gold fixture 구조

## 수정 요구

1. 64/32 KiB 호출별 상한 초과가 전체 범위 포기가 되지 않게 안정된 cursor/page 또는 ID 목록→묶음 조회 계약을 구현한다. build+scope+정규화 요청과 정렬을 페이지마다 고정하고 `more`/잔여/완료를 정확히 반환한다. `truncated`만 반복되는 경로 금지. 실물 scope:all 210,511B를 여러 호출로 회수해 전체 ID/원문/source의 합이 원 범위와 일치하는 시험.
2. Q139 `scope:all#evidence#step8_notes[26]`의 source `meta.pair`가 없고 `attached_to` combo anchor가 있다는 실물 구조를 조사해, 검증 가능한 pair/condition 적용 범위를 명시한다. `a,b` 있음/없음에 따라 무근거로 `quotable`이 뒤집히지 않게 한다. mapping 미확정이면 `unresolved_scope` 미지원 상태를 정직하게 반환하되, 가능한 원천/Gold 연결을 실제 근거로 확인한다. Q139 두 쌍과 무관 쌍, 양방향 시험.
3. 조건부 R8 claim·대안은 `include_conditional`, `sub_condition`, 원천 조건과 요청 조건의 일치를 판정해 `applies_to`와 인용 자격에 반영한다. 기본 쌍의 무조건 사실로 쓰이지 않게 한다. U5-023/U5-034 `R8-0144` false/true 시험.
4. edge가 참조하는 fact ID 누락·owner/source 결손·잘못된 정본 scope는 `found/empty,complete:true`가 아니라 미완료/오류로 남긴다. 실제 빈 확정 쌍과 손상된 graph를 구분한다.
5. claim/대안의 방향·qualifier·condition provenance를 보존하고 역방향 사례를 시험한다. 축소 후 응답 상한을 재측정하거나 요청 길이를 제한한다. 186 기존 첫 page ID 순서 등 WORK-011 회귀 범위를 가능한 격리 시험으로 확인한다.

REST/MCP 같은 코어·정상 응답 의미 유지. Hub 호출별 제한은 앱 전체 그래프 탐색 제한이 아니다. 사용자 18005 포트·`procedure-*` 컨테이너·개발/운영 DB 조작 금지, 새 평가 실행 금지. 공개 원장 본문 복제 금지.

## 범위·검증

- 앞 발주의 허용 backend/app/modules/gold, router/schema/swagger, gold/public API 시험 파일만 수정. 다른 경로 필요 시 코디에게 보고.
- 관련 `uv run pytest`, 가능한 전체 unit suite, 만진 파일 `ruff`, `git diff --check`. 실물 Gold 메모리 fixture/inprocess만 사용. FAIL별 수정 근거와 공개 JSON 예시·페이지 회수 결과를 완료 메시지에 적는다.
- 커밋·push·PR 금지. 완료 시 dispatch preamble대로 `worker_done` 한 번.
