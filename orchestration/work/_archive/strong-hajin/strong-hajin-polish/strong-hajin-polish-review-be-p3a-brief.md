# [reviewer] WORK-008 Phase 3a 코드 검수 — backend 리뷰 모드

너는 **strong-hajin `reviewer` 워커**다. 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/reviewer/role.md` (+ `rules.md`). **read-only.**

## 1. 대상
코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` 의 **`backend/` 와 `docs/unified-operations-inventory.json` 미커밋 변경만**. `frontend/` 는 다른 리뷰가 본다 — 대상 아님.

## 2. 기준
- WP `…/kknaks_profile/스트롱하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` **Phase 3a** · 원칙 P-1·P-3
- SPEC: `…/strong-hajin/20-spec/` SPEC-001 S-9·§4 Validation·§5 · SPEC-002 §2.4·§2.9·§4·S-7·§6
- 발주서 `…/orchestration/work/strong-hajin-polish/strong-hajin-polish-be-p3a-brief.md` · 조사 `be-survey-report.md` §1
- 워커 보고 요약: 기한 필수 검사 2곳 제거(action_center normalize · actions _edit_contract) · 편집 계약·work_request_create 에 parent_task_id 더함 · 봉투에 created_at · 도구 설명 갱신 · inventory drift 6항목 · supersedes_request_id 는 편집 계약·MCP 인자에서 제외(만들기 창 칸 아님) · test-unit 389 · test-contract 1128+128 통과

## 3. 볼 것
1. **P-1 대조** — 두 kind 의 정규화·스냅샷·편집 계약·MCP 인자가 생성 명령(`TaskCreateInput`·`WorkRequestCreateInput`) 필드와 같은지 직접 대조. 필수·검증이 새 업무 추가와 다르게 남은 자리(AX 전용 검사)를 grep 으로 다시 전부
2. confirm + draft 경로·회차·diff 가 그대로인가
3. 봉투 `created_at` — 모든 ax.* 봉투에 실리나, 형식(ISO), 다른 핸들러 봉투에 영향
4. 계층 경계(modules/platform/entrypoints) · envelope 를 서버가 만드나 · 있는 operation 재사용 · inventory diff 가 그 항목만인가
5. **조용히 통과하는 자리** — 뒤집은 옛 테스트가 이제 아무것도 안 재는지, 대조 테스트가 같은 원천을 양쪽에 써서 항상 참인지
6. `supersedes_request_id` 제외 판단이 SPEC 과 맞나(의견)
7. 3b FE 가 쓸 계약(필드 이름·모양) 요약 — 리포트 끝에 한 표

## 4. 판정
FAIL · WARN · PASS. 파일:줄 + 근거. 테스트는 Makefile 타깃만, 서버·DB 기동 금지(코디 로컬 스택이 떠 있다).

## 5. allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-be-p3a-report.md` 하나만

## 6. 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-008 Phase 3a 코드 검수 <PASS|WARN|FAIL>" \
  --body "판정 / FAIL·WARN(파일:줄) / FE 계약 표 / 리포트 경로"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] reviewer 완료 — Phase 3a 코드 검수 <판정>. 리포트 review-be-p3a-report.md" --enter
```
