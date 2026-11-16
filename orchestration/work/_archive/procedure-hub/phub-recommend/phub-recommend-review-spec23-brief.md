# [reviewer_doc] SPEC-002 · SPEC-003 검수 — 구현 발주 전 문서 게이트

너는 **procedure-hub `reviewer_doc` 워커**다(read-only). 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/reviewer/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` (리뷰 리포트 1개 외 수정 금지)

## 1. 기준 · 대상 (`orchestration/work/phub-recommend/`)

- 기준: `DEC-003.md` · `DEC-001.md` D-12(Hub 에 LLM 없음) · `_RESUME.md` §2 10-27 행(특히 「외국어 이름 → 정확히 일치하지 않으면 승인 게이트」 · 「DEC-003 OQ 처리」 · MCP 는 프로필 reference · public)
- 대상: `SPEC-002-mfds-mcp.md` · `SPEC-003-mfds-ingest.md`
- 사실 확인: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp/NOTES.md` · 필요하면 같은 폴더 `.env` 키로 식약처 API 를 엔드포인트당 몇 번만(키 값을 쓰지 않는다) · `SPEC-001.md` · 코드 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend/app/modules/graph/`(read-only)

## 2. 볼 것

1. DEC 이탈 — Hub 쪽 모델 호출 · 자동 매칭이 완전 일치 밖으로 새는 곳 · 레거시/canonical 접촉 · 미허가/취소 제품이 추천 쪽으로 새는 길
2. 실물 대조 — 오퍼레이션 이름 · 대문자 파라미터 · 응답 필드 · 페이지 처리가 실제 API 와 맞나(의약품은 「응답 미확인」 표시가 정직한가)
3. 구현 가능성 — 워커가 문서만 보고 만들 수 있나. MCP tool 입출력 · 적재 질의 목록 규칙 · 매칭 → 게이트 → Hub 반영 흐름이 닫혀 있나
4. 보안 — public reference 에 키 · 캐시 · 실명이 새는 길
5. 사용자가 실물에서 만날 자리

## 3. 산출물 · 판정

- 생성: `orchestration/work/phub-recommend/review-spec-002-003-report.md` 1개
- 맨 위 종합 PASS/WARN/FAIL · 지적마다 파일:줄 + 근거. FAIL 은 「문서대로 만들면 틀린 결과 · 실패」만

## 4. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <판정>" \
  --body "FAIL / WARN 목록 / 실물 대조 결과"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] reviewer_doc 완료 — <판정>. 상세는 인박스." --enter
```
