# [backend] WORK-004 구현 — hub-evals 실험 앱(clinic_chat)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/backend/role.md`(rules · workflow · tools 같이 — 이 레포는 프로시저 허브가 아니라 실험 앱이지만 일하는 규칙은 같다). 코드 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`(브랜치 `kknaksss/hub-evals` · 레포 `kknaks/clinic_chat` **공개** · **push 금지 · 커밋은 로컬만**).
정본: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-006.md` · `WORK-004.md`(검수 v2 PASS). 허브 계약 `SPEC-005.md` §5 · §5-12.

## 하는 일
WORK-004 Phase 1 → 7 순서 · Phase 마다 완료 조건 · 그 Phase 시험만 · 전체는 끝에 한 번.
- **허브(18005)는 다른 워커가 구현 중**(지금 Phase 2) — 허브가 필요한 단계는 SPEC-005 계약대로 모의(mock) 서버 · 픽스처로 먼저 · 허브가 뜨면 실물 대조. 허브 완성 전 Phase 7 실물 E2E 는 대기하고 코디에게 heartbeat
- 키: 사용자가 워크트리 `.env` 에 직접 넣는다(지금 있을 수도 · 없을 수도). **키 값을 읽어 출력 · 기록 · 커밋 금지** · 키 없으면 그 케이스만 「키 없음」
- 실물 외부 호출(Anthropic · TypeSafe)은 Phase 7 실물 E2E 1질문에서만(그 전은 모의) — 비용 · 사용자 키
- 실험 기록 `runs/` = 지금 .gitignore 그대로(커밋 안 함) — 사용자 결정 대기(바뀌면 코디가 알림)

## 지킬 것
- SPEC 과 다르게 해야 하면 고치기 전에 `ask` · Phase 끝마다 `heartbeat`(phase 이름) · 막히면 `escalation`
- 공개 레포: 키 · 원장 · 실버 · 골드 데이터 · 환자 정보 · 사용자 홈 절대경로 커밋 금지(.env.example 은 빈칸 규칙 SPEC §2-4)
- 포트 18210 만 · 사용자 포트 3700 · 3800 · 8700 · 8800 · 54329 · 18005(허브 — 읽기만) 건드리지 말 것 · 끝나면 프로세스 정리

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_56c4278e-4761-44d7-8d67-87ca697be965 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: WORK-004 hub-evals" --body "모의 완료 | 완료 · Phase N · 시험 N passed · 실물 E2E 1질문 결과 · 커밋 N(로컬)"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] backend 완료 — WORK-004 hub-evals. 상세는 인박스." --enter
```
