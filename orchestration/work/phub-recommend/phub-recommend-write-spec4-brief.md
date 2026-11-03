# [writer] SPEC-004 · WORK-002 — 그래프 v2(새 실버 원장 + 시맨틱 엣지 + 골드 tool)

역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.
사용자 지시(10-27): **오늘 골드까지 간다.** 이 SPEC 을 검수 → 백엔드 구현 → 빌드 → 로컬 E2E 까지 오늘 한다.

## 기준 (`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`)
- `DEC-001.md`(D-03 시술↔시술 엣지 하나 · D-04 엣지 메타 · D-05/06 tool · D-12 LLM 없음) · `DEC-002.md` · `DEC-003.md` · `_RESUME.md` §2 10-27 행 전부
- 현재 구현 `SPEC-001.md` · 코드 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/app/modules/graph/`(v1 그래프 — 브론즈 · 검증 · 발행 · REST/MCP 그대로 재사용)
- `SPEC-003-mfds-ingest.md`(식약처 브론즈 · 매칭) — 이번엔 **작업 산출물 JSON 을 원천으로 적재**하는 쪽으로 단순화해도 된다(아래)
- 입력 산출물(병행 작성 중 — 모양은 브리프로 안다): `procedure-master-v3.json`(계열 · 단위 시술 · 항목 행선지) · `product-master-draft.json`(제조사 · 제품 · 규격 · 매칭) · 게이트 답(아티팩트 db 를 코디가 JSON 으로 내려받아 `gate-answers/` 에 둔다) · `source-fix-list.json`

## SPEC-004 가 정할 것
1. **실버 노드 v2**: 계열(무엇을) · 단위 시술 · 부위(트리) · 기법 · 제품(라인 ⊃ 품목) · 제조사(역할 제조/수입) · 규격 · 고민(taxonomy 고민 트리 — 「쳐짐→처짐」 원천 수정 반영 전까지 이름 치환표로) · 목적. 노드마다 이름(상담 용어) · 공식명 · 동의어 · 원천
2. **원천(브론즈) 추가**: 위 작업 산출물 JSON 과 게이트 답 JSON 을 「큐레이션 원천」으로 브론즈에 적재(해시 · 멱등). 식약처 API 직접 적재는 OQ 로 미뤄도 된다
3. **시맨틱 엣지 v2**: 고민 → 단위 시술(원천: modality_ref · problem-combos · problem-packages · treatment-optimization — 원장 항목이 단위 시술로 풀린 경로로 내린다) · 단위 시술 ↔ 단위 시술(시너지 · 순서 · 간격 · 금기 — 계열 단위 원천을 단위 시술로 내리는 규칙) · 단위 시술 → 부위 · 기법 · 계열 · 쓰는 제품/장비 · 제품 → 제조사 · 규격 · 부작용/금기(계열 단위). 엣지 메타(DEC-001 D-04) · 게이트 상태(자동/승인/미확인)
4. **골드 tool**: v1 REST/MCP 7종을 v2 노드 · 엣지로 — 노드 검색은 동의어 포함 결정론. 「처짐이 고민이에요」 · 「턱쪽에 필러」 · 「포텐자 하고 싶어요」 · 「보톡스랑 필러 같이」 를 E2E 시나리오로(기대값은 입력 산출물 기준으로 「무엇이 나와야 하나」를 적는다)
5. 마이그레이션 · 기존 v1 그래프와의 관계(교체 vs 병행 — 로컬이라 교체 권장 여부를 근거와 함께)

## WORK-002
- 백엔드 워커가 오늘 안에 끝낼 Phase(적재 → 빌드 → 검증 → tool → E2E 스크립트). Phase 마다 테스트 · 검증 명령

## 산출물 · 제약
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-004.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/WORK-002.md` 2개만. DEC 에 없는 정책은 OQ. 코드 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: SPEC-004 · WORK-002" \
  --body "결과 수치 / 산출물 / 미결"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] writer 완료 — SPEC-004 · WORK-002. 상세는 인박스." --enter
```
