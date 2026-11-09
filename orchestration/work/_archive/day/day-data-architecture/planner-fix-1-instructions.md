# [planner] 수정 1판 — 검수 FAIL(F1 · F2) · WARN 반영

너는 **day planner 워커**다. 앞 판 맥락이 없을 수 있다 — 아래를 순서대로 읽어라.

1. 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/planner/` (role · rules · tools)
2. 1판 발주서: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/day-data-architecture-spec-brief.md` — 계약(설계를 바꾸지 마라 · products/day 밖 금지 · 커밋 금지)은 그대로다
3. 네 1판 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-report.md`
4. **검수 리포트(이번 판의 이유)**: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-doc-report.md` — FAIL F1 · F2, WARN W1 ~ W4

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec` (1판 산출물이 미커밋으로 있다 — 그 위에서 고친다)

## 원천이 바뀌었다 (코디 · 사용자, 2026-11-03) — 원천 경로: `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/`

- **묶은 행 분리(F1 원인 제거)**: `created_at · updated_at · deleted_at | ✓` 42행을 `created_at · updated_at | ✓` + `deleted_at | (필수 아님) | 소프트 딜리트 — null = 살아 있음` 두 행으로 나눴다(01 ~ 07 · 04-1 전부). README 공통 규칙 「삭제」에 **NULL 허용** 명시.
- **칸 표 추가(F2)**: `03-visit.md` 에 `consultation_procedure`(상담 시술 · 상담 1 : N) 표, `06-room.md` 에 `visit_occupied_resource_doctor`(N:M) 표. 각 `—` 행이 이 테이블을 가리키게 바꿨다. README 관계도에 두 관계 추가.
- `03-visit.md` 머리말 「정하는 중」 → 「정함」(W4).

## 할 일

1. **SPEC-000 을 바뀐 원천으로 다시 맞춘다** — 표는 원천을 그대로 옮긴다(1판처럼). 01 ~ 07 · 04-1 의 deleted_at 분리 행 · 두 새 테이블 · 03 머리말 · README 공통 규칙 · 관계도.
2. **F1**: `spec-000-data-model.md` 의 「묶은 행 = 같은 타입 · 필수」 규칙(:77)을 지운다. 「필수 ✓ = NOT NULL」(:74)을 남기면 「§2 공통 규칙이 우선」을 붙인다.
3. **F2**: 「타입 `—` = 만들지 않는다」(:76 · :1196)를 지운다. 타입 `—` 는 원천 표기 그대로(보류 / 다른 곳으로 / 연결 테이블로). OQ-03-2 · OQ-06-1 은 이제 원천에 칸 표가 있으므로 **지운다**.
4. **W1**: SPEC 「주제와 상태」 표의 깨진 링크 8개(:61-68) → 절 앵커 또는 링크 없는 이름.
5. **erd.md** 에 두 테이블 · 관계 · 핵심 키 추가(1차 테이블 49 → 51). 인벤토리 · 개수 갱신.
6. W2(ESC-001 값)는 **사용자가 그대로 두기로 했다** — 손대지 마라. W3(log PR 칸)은 코디가 PR 때 채운다 — 손대지 마라.
7. lint `--strict` 1회 · 원천 대비 개수 대조표 갱신.

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-fix-1-report.md` — 고친 곳 `파일:줄` · 개수 대조표(원천 / SPEC) · lint 결과.
완료는 dispatch preamble 의 `worker_done` 절차대로(태스크 · 디스패치 id 는 preamble 값).
