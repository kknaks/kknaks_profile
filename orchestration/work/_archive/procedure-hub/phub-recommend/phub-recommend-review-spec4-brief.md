# [reviewer_doc] SPEC-004 · WORK-002 검수 — 그래프 v2 구현 전 게이트 (오늘 안에)

역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/reviewer/role.md` (read-only). 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 기준 · 대상 (`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`)
- 대상: `SPEC-004.md` · `WORK-002.md`
- 기준: `DEC-001.md`(D-03 · D-04 · D-05 · D-06 · D-12) · `DEC-002.md` · `DEC-003.md` · `_RESUME.md` §2 10-27 행 전부(이름 정규화 · 계열 공식 일반명 · 라인 제품 · 장비 이름 = 시술 동의어 · 게이트 축소 규칙 · 처짐 원천 수정)
- 사실 확인: 현재 코드 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/app/modules/graph/` · `SPEC-001.md` · 입력 산출물 `product-master-draft*.json` · `taxonomy-classify-v2.json` · `gate-answers/` (procedure-master-v3 는 작성 중 — SPEC 이 요구하는 입력 모양이 합리적인지만)

## 볼 것
1. DEC 이탈(LLM 0 · 자동 확정 범위 · 레거시/canonical 미접촉)
2. 구현 가능성 — 노드 16 · 엣지 16 · 내림 규칙 A~D 가 입력 산출물만으로 결정론으로 계산되나. 입력 모양 가정이 실제 파일과 맞나
3. v1 교체 판단 · 기존 tool · 테스트와의 관계(기존 테스트가 깨지는 범위가 WORK 에 있나)
4. E2E E-1~E-5 가 정직한가(입력 의존 · 성립 조건)
5. 오늘 안에 끝낼 수 있는 Phase 분할인가 — 과한 범위는 WARN 으로 「뒤로 미룰 것」 제안

## 산출물
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-spec-004-report.md` 1개 · 맨 위 PASS/WARN/FAIL. FAIL 은 「문서대로 만들면 틀리거나 실패」만

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: SPEC-004 <판정>" \
  --body "FAIL / WARN / 오늘 범위 제안"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] reviewer_doc 완료 — SPEC-004 <판정>. 상세는 인박스." --enter
```
