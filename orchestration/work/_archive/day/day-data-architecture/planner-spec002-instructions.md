# [planner] DAY-SPEC-002 시술 현황(1차) 작성 — PR #909 같은 워크트리 · 미커밋으로

너는 day planner 워커다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/planner/`. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec`(mediness · PR #909). **커밋 금지.**
SPEC-001(`products/day/20-spec/spec-001-login-session.md`)과 같은 형식 · 같은 생성 방식(lint `--strict`)으로 `products/day/20-spec/spec-002-procedure-board.md` 를 쓴다.

## 정본 (우선순위 순 — 위가 이긴다)

1. **사용자 결정 원천** `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md` — U1 ~ U12 결정 · 「다음 스펙으로」(U5 방 옮기기 · U11 차트 작성 = **범위 밖**) · 추정 금지 7. **여기 있는 것은 다시 열지 마라.**
2. 시안(생김새 정본) `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html` — 화면 요소 · 상태 · 문구. 시안 요소 번호(E01 ~ E56)는 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-ds-research-report.md` 를 따른다.
3. 결정이 없는 동작은 **cc 기존 로직**: `/Users/kknaks/git/toy_pr2/kknaks_profile/para/projects/summer-star/cc-prototype/10-decision/decision-005-procedure-board.md`(D-01 ~ D-34) · `/Users/kknaks/git/toy_pr2/kknaks_profile/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` · `spec-004-procedure-app.md`(시술실 앱 — 이번 웹 SPEC 에는 앱 몫을 넣지 않고 링크만) · `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-10-12-cc-prototype/workflow-v2.md` · cc 코드 `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:procedure/back/app/domain/rules.py` 등.
4. 검수 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-screen-procedure-report.md` — 시안 값 ↔ 데이터 근거 42 · 흐름 30 · 다른 것 15 · KOS 필드 22 · 모델 빈칸. **근거로 쓰되 결정은 1번이 이긴다.**
5. DAY 기존 계약: SPEC-000 `products/day/20-spec/spec-000-data-model.md`(03 · 05 · 06 · §2) · SPEC-001(로그인 · 권한 · 오류 코드 · CSRF) · `products/day/40-architecture/system.md`(api/worker · outbox · SSE) · `code-structure.md`.
6. KOS 쓰기 경로 근거: HAR(main 체크아웃 · gitignore) `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-10-12-cc-prototype/` 의 `의사호출*.har` · `시술완료*.har` · `시술현황_방배정.har` — **경로 · 요청 칸 이름만, 값은 옮기지 마라.**

## 범위 (1차)

- 웹(Jinja2 + HTMX) 시술 현황 한 화면 — 인박스(현황 · 호출 · 시술 완료) · 방 카드 판 · 카드 안 시술 줄 · 의사 호출 · 수락 · [시작] · [종료] · 마취 · 확인 필요 · 수납 필요 · 카드 D&D 순서 · 귀가 대기 · 실시간 갱신(SSE).
- 그 화면이 쓰는 JSON/HTMX 엔드포인트 계약 · 상태 · 오류 매트릭스 · 권한(SPEC-001 permission_key 를 이 화면 몫으로 정할 수 있으면 제안 · OQ-04-2).
- **KOS 동기화 추가분**: 시술 작업(`visit_task` · `visit_task_staff`) · 상담(필요한 만큼) — #226 이 안 한 것. 어느 KOS 응답 필드에서 오는지.
- **KOS 쓰기**: 화면 동작마다 KOS 에 무엇을 쓰나(outbox) · 확인은 무엇으로 하나 · 쓰기가 없는 동작(DAY 에만 남는 것). HAR 로 확인된 것만 「확인됨」, 아닌 것은 OQ.
- **데이터 모델 변경**: U3 「기존 호출 닫기」 칸(`doctor_call`) 등 — SPEC-000 해당 표를 같이 고친다(원천 결정 링크). 그 밖 변경이 필요하면 OQ 로.

범위 밖: Flutter 앱 · 방 옮기기/연결(U5) · 차트 작성(U11 — 1차는 KOS 메모 읽기만) · 알림 · 푸시 · 채팅 · 예약/접수/상담 화면.

## 할 일

1. SPEC-002 본문 — 메타 · BR · 범위 · 용어 · 화면 구성(시안 요소 번호로) · 상태(방문 단계 · 시술 줄 상태 · 호출 상태) · 동작별 Functional Rule · 케이스 매트릭스(오류 · 경계 · 권한 · 빈 상태) · API 계약 · KOS 읽기/쓰기 표 · 실시간 갱신 · Open Questions.
2. SPEC-000 변경분 · `20-spec.md` 인덱스 · In Scope 줄 · `log.md` 한 줄.
3. lint `--strict` 1회.

**발명하지 마라** — 정본에 없는 동작 · 칸 · 값은 OQ. 특히 KOS 쓰기 요청 모양은 HAR 에 있는 것만.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec002-report.md` — 만든 절 목록 · 결정 U1 ~ U12 반영 위치 · cc 에서 가져온 규칙 목록(D 번호) · OQ 목록(사용자 결정 필요한 것만 따로 · 선택지 + 추천) · SPEC-000 변경분. 완료는 preamble 의 worker_done 절차대로(`orca orchestration send` 와 `orca terminal send` 둘 다).
