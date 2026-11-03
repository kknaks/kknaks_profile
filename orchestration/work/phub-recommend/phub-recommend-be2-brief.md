# [backend] WORK-002 — 그래프 v2 구현 · 빌드 · 로컬 E2E (오늘 안에)

역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/backend/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend` (브랜치 `kknaksss/phub-recommend` · **로컬 전용 — 커밋 · push 금지**). v1 그래프 코드(미커밋)가 이미 있다 — 그 위에 쌓는다.

## 1. SSOT
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-004.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/WORK-002.md` ← 계약. §3 이 SPEC 보다 우선
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-spec-004-report.md` ← 검수(코디가 반영 지시를 §3 에 적는다)
- 입력(큐레이션 원천 — 브론즈로 적재):
  - `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/procedure-master-v3.json` (계열 23 · 단위 시술 236 · 큰 기법 65 · 원장 521 행선지) — 재빌드 스크립트 `procedure-master-build.py`
  - `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/product-master-draft.json` (v4 — 제조사 · 제품 · 규격 · 매칭)
  - `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/gate-answers/product-match.json` (게이트 유효 상태 — 코디가 빌드 직전 재생성) · `classify-v1.json` · `classify-v2.json` · `source-fix.json`
- 기존: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-001.md` · 코드 `backend/app/modules/graph/` · `backend/docs/graph-local.md`

## 2. 배경
사용자 지시: **오늘 골드까지.** Hub 에 LLM 없음(DEC-001 D-12). 사용자가 오늘 로컬에서 「처짐이 고민이에요」 · 「턱쪽에 필러」 · 「포텐자 하고 싶어요」 · 「보톡스랑 필러 같이」 를 REST · MCP 로 확인한다.

## 3. 검수 반영 지시
- SPEC-004 는 검수 FAIL 3(입력 계약이 실물과 다름)을 writer 가 실물 기준으로 고친 판이 최종이다(\`review-spec-004-report.md\` 는 배경). **재검수는 하지 않았다 — Phase 0 의 입력 대조가 그 역할이다.** 대조에서 SPEC 과 실물이 하나라도 다르면 멈추고 질문하라
- 범위는 SPEC §8 「오늘」 · WORK-002 Phase 0~5. 「2차」 항목은 손대지 않는다
- 골드 기본 응답 = 승인 · 자동만, \`include_unconfirmed=true\` 로 나머지(코디 기본값 · 사용자 확인 대기 — 바뀌면 파라미터 기본값 하나만 바뀌게 짜라)
- 빌드 직전 코디가 \`gate-answers/product-match.json\` 을 다시 만든다 — 적재는 파일을 그때 읽는다(하드코딩 금지)

## 5. allowed_paths
- `backend/` (SPEC-004 위치 절이 정한 새 파일 + 그 절이 허용한 기존 graph 파일). 레거시 · canonical 코드 수정 금지

## 6. 구현 단계
WORK-002 Phase 0 → 6. Phase 마다 그 Phase 테스트만. **Phase 0 의 입력 대조에서 SPEC 과 입력 모양이 다르면 혼자 고치지 말고 질문**(§9 방식).
마지막: phub-graph-postgres(55434)에 v2 적재 · 빌드 · 발행 → API 18005 기동 → E2E 스크립트 REST + MCP 1회 → **결과 수치 보고 후 API 내림**(DB 유지)

## 7. 범위 제약
- 커밋 · push · 브랜치 전환 금지 · 사용자 포트/컨테이너 금지(3700 · 3800 · 8700 · 8800 · 54329) · stg · 식약처 호출 금지(입력 JSON 만) · LLM 호출 금지

## 8. 검증
```
cd backend && uv run ruff check . && DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest --ignore=tests/integration (Phase 마다 관련 테스트만, 전체는 마지막 1회) · alembic 단일 head · E2E 스크립트 전부 PASS 또는 실패 사유
```

## 9. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: 그래프 v2" \
  --body "노드 · 엣지 수 / 검증 / E2E 결과 / 미결"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] backend 완료 — 그래프 v2. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b --text "[질문] backend: <질문>" --enter`
