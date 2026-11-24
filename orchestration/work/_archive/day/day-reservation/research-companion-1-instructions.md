# [조사 · 읽기 전용] 예약 표 「동행 그룹」(카드 겹쳐 놓기) — 원천 · 저장 · 화면

너는 맥락이 없다고 생각하고 이 파일만 따른다. 고치지 · 커밋하지 마라. 결과는 리포트 하나.
요청(사용자 2026-11-23 · `e2e-1-feedback.md` E7): 예약 표 카드를 끌어 다른 카드에 겹쳐 놓으면 **같은 동행 그룹**. 조건 = 같은 예약 그룹(열) ∧ 같은 시간대. 같은 그룹 카드는 감싸는 띠로 표시. 시안 없음 · DB 새 테이블 예상. 코디 기본값(사용자 승인): 띠 밖으로 끌어내면 빠짐 · 1명 남으면 그룹 없어짐 · KOS 에서 시간 / 예약 그룹이 바뀌어 조건이 깨지면 자동으로 빠짐 · 10초 폴링으로 다른 화면 반영 · 새 권한 키 기본 모든 직무.

물음(근거 file:line · 그대로 / 가공 / 없음):
1. **KOS 에 동행(일행 · companion · 같이 온 사람 · 그룹 예약) 개념이 있나** — KOS openapi(`/Users/kknaks/git/ax-clinic-project/para/archive/inbox_archive/2026-09-18-kos-openapi.yaml` grep: companion · accompan · group · party · together · 동행 · 일행) · DAY KOS 어댑터 · 매퍼(`backend/day/emr/kos/`) · DAY DB 칸. 있으면 읽기 / 쓰기 명령 · 모양 · DAY 가 이미 받는지.
2. cc-prototype(`git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:<path>` · grep 동행 · companion · group) · centurion(`/Users/kknaks/git/centurion`) · 기획(mediness `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec/products/day/00-baseline/planning/` grep 동행 · 일행) 에 동행 개념 · 화면이 있나.
3. 시안(`/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/20261113_예약현황_시연 (1).html`) 에 동행 · 끌어 놓기(drag · dnd) 흔적이 있나.
4. DAY 지금 표 카드 배치(`policies/reservations.py` stack · 카드 위치) · 프론트 규약(vanilla day.js · HTMX · 인라인 스크립트 금지)에서 끌어 놓기를 넣을 자리 · 기존 끌어 놓기 코드가 DAY 어디에 있나(시술 현황 · 원장 옮기기 등).
5. DB 설계 후보: 새 테이블(예: `companion_group` · `companion_member` 또는 `visit.companion_group_id`) — SPEC-000(mediness `products/day/20-spec/spec-000-data-model.md`) 규칙(외부 id · soft delete · 병원 단위)에 맞는 꼴 2안 · 장단.
6. 조건 「같은 시간대」 판정 후보(같은 시작 시각 · 시간 겹침 · 같은 간격 칸) — 지금 표의 칸(interval) 개념에 맞는 것.
7. 코디가 정할 것(추천 포함).

금지: 고치기 · 커밋 · KOS 호출 · deploy/*.env · 스택. 고객 정보 출력 금지.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/research-companion-1-report.md` · 맨 위 물음 표 · preamble 의 worker_done.
