
# [reviewer_code] WP-130 코드 검수 (BE+FE — 미커밋 diff)

너는 **mediness `reviewer_code` 워커**다. **read-only** — 코드 수정·테스트 실행 금지.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/reviewer/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-improve`
검수 범위 = **미커밋 diff 만**(`git diff` + untracked). 직전 커밋 5b98247a(WP-129)는 검수 통과분.

## SSOT (판정 기준)

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec/products/mediness/30-work/work-130-task-detail-unification.md` — phase 별 작업·검증·금지선
- 같은 트리 `20-spec/spec-154-decision-workflow.md` §4.8(본문·완료 422)·§4.19(㉘ 상세 2단·완료 모달·보드 v1·AC-33~41) · `spec-155` §6(채팅 채움·첨부 스테이징) · `spec-127`(storage 선례)
- `40-architecture/domains/runtime_task.md` — task_references 스키마·완료 근거 불변식
- 발주 브리프 2장: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/task-improve-be130-brief.md`·`task-improve-fe130-brief.md`
- 코디 확정 계약: 상세 additive(background/goal·references[]·canAdd/DeleteReference=가시성 true)·CRUD /tasks/{id}/references(+download)·완료기록=transition comment·첨부 스테이징 A(POST /action-runtime/task-draft-attachments → draft_id·POST /turns draft_id additive)
- 워커 리포트 2건(참고 — 주장은 검증 대상): `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-app-task-improve/e9d8fd53-e24a-424f-a667-a40408c2c47b/scratchpad/wp130-backend-report.md` · `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-app-task-improve/3cb1f597-ef17-48dc-bba8-45224ede26bc/scratchpad/WP-130-frontend-report.md`

## 체크리스트 (위반 = FAIL)

1. **migration 0138 = 정확히 3객체**(컬럼 2·테이블 1) — 잠입 스키마 변경 0. task_references 스키마가 domains 문서와 일치(role×kind·soft delete·created_by_member_id)
2. **완료 422 술어** — 사람 경로 전부 강제(comment 또는 deliverable≥1)·시스템 경로 면제·파생(체크리스트) 면제·**부분 부수효과 0**(정확한 검사 순서). MCP·채팅 경로 우회 없나
3. **storage** — path-guard 재사용(신규 구현 0)·25MB·denylist·`Content-Disposition: attachment`·DB 상대경로만·출처 행 저장 0
4. **원장 렌더 폐지 대체** — decision·incident 스냅샷 신설이 흐름별로 배경·목표·체크리스트를 채우나. description fallback 한 곳
5. **FE 상세/보드** — 2단 셸·완료 모달 활성 조건(요약 OR 제출자료)·사유 모달 공용·월 필터 completed_at 프론트 파생(API 파라미터 0)·드롭다운 소스 allowed_transitions·마커 5값·D-3 단일 파생·이미지만 인라인·요청 축 화면 0·역할별 게이팅 0(v1)
6. **채팅** — 배경·목표·체크리스트 필수 채움(되묻기)·purpose→goal(구 키 읽기 호환)·첨부 스테이징 계약 일치(draft_id 서버 발급·turns additive·extra=forbid 보존)·승인 시 트랜잭션 귀속
7. **WBS 완료 모달** — canonical 연결 행만 모달 경유·completionNote=comment 동일 축·phase/legacy 행 무영향
8. **allowed_paths·계층** — BE=back/·mcp/, FE=front/. repositories→services 역참조 0(WP-129 W1 재발 방지)
9. 상태 축·TaskEvent 어휘 불변·게이트 재도입 0·자동 cc 0
10. BE 미결 ⓐ(§6.1 «그 턴에 카드를 세우지 않는다» vs 카드 문구 착지)·ⓑ(size_bytes 가 domains 표에 없음) — 코드가 틀린 게 아니라 **스펙 환류 대상**인지 판정. 기존 실패(26건 version_wbs_checkitem·vitest 6건·flake 1건) diff 무관성 코드 근거 판정

## 산출물

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/review-code130-report.md` — 판정(PASS/WARN/FAIL)+근거(파일:줄)+위반 목록

## 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "reviewer_code(130) 완료: <판정>" \
  --body "판정 / 위반(파일:줄) / 리포트 경로"

orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] reviewer_code(130) — <판정 한 줄>. 상세는 인박스." --enter
```
