# [writer] SPEC-004 v0.3 — 「2차」 항목을 이번 범위로 + 판매사 역할

역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.
사용자 결정(10-27, `_RESUME.md` §2): **다 만들 때까지 빌드 안 한다** — SPEC-004 §8 「2차」로 미뤘던 것도 이번 구현 범위다. 업체 역할은 **제조사 / 수입사 / 판매사** 3종.

## 읽을 것 (`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`)
- `SPEC-004.md`(현 판 · §8 2차 목록) · `WORK-002.md` · `review-spec-004-report.md`
- 입력 실물: `procedure-master-v3.json` · `product-master-draft.json`(v4 — 품목 사용목적/효능 문장 포함) · `company-relation-check.json`(23 제품 업체 관계 · 근거 URL) · `gate-answers/*.json`
- 원천(브론즈) `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/` (synergy · contraindications · treatment-sequence · complications)

## 할 일
1. §8 「2차」 항목을 전부 본문 계약으로 올린다 — 특히 ① **시술↔시술 관계를 단위 시술 단위로**(원천의 이름 끝점 · 부위 조건 「동일 부위」 등을 단위 시술로 해석하는 결정론 규칙, 못 풀면 계열 단위로 남기고 이슈) ② **품목 → 부위/단위 시술**(품목 사용목적 · 효능 문장에서 부위 사전(부위 트리 + 동의어) 완전 일치로만 — LLM · 유사도 금지) ③ 장비 → 단위 시술 갈래 ④ 규격 정규화 ⑤ 제조사 원장 병합 · 의약품 위탁 제조원 ⑥ 그 밖 §8 항목
2. **업체 역할 3종**: manufactured_by · imported_by · sold_by 엣지. 원천 = 식약처 허가(허가 업체 · 제조원 · 허가번호 접두 제허/수허) + company-relation-check(관계 · URL — 확인된 것만)
3. company-relation-check 를 큐레이션 원천(브론즈)으로 추가하는 계약
4. 원천 수정 목록 반영 방식(원장 업체 오기 → 치환표, 처짐처럼)
5. WORK-002 를 늘어난 범위로 다시(Phase 추가 · 테스트 · 마지막 빌드/E2E 는 「사용자 승인 후 실행」 Phase 로)

## 산출물 · 제약
- `SPEC-004.md` · `WORK-002.md` 수정만 · 변경 이력 · DEC 에 없는 정책은 OQ

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: SPEC-004 v0.3" \
  --body "결과 / 산출물 / 미결"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] writer 완료 — SPEC-004 v0.3. 상세는 인박스." --enter
```
