
# [reviewer_code] WP-129 코드 검수 (BE+FE)

너는 **mediness `reviewer_code` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-improve`
base: `origin/dev`. **read-only 검수** — 코드를 고치지 않고 테스트도 돌리지 않는다. `git diff origin/dev...HEAD` + `git status`(untracked 포함)로 범위를 산정한다.

## 1. SSOT — 판정 기준

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec/products/mediness/30-work/work-129-task-request-axis.md` — 빌드 계획 정본 (phase 별 작업·검증·금지선)
- 같은 트리 `20-spec/spec-154-decision-workflow.md` §4.8 · `spec-155` §6.1·§7 · `spec-111`·`spec-156`(입구 차단) · `spec-119`(DM)
- 발주 브리프: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/task-improve-be-brief.md` · `task-improve-fe-brief.md`
- BE↔FE 합의 계약(코디 확정): TaskDetail 응답 `display.requester_name` + 최상위 `is_request`(서버 파생 한 곳) / 요청자(비담당) viewer 에 `canTransitionTask=true + allowed_transitions=['canceled']`
- 워커 리포트(참고): `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-app-task-improve/e3f928fe-ecf4-46f4-a624-ac35a5520f17/scratchpad/wp129-backend-report.md` — 워커 주장은 검증 대상이지 근거가 아니다

## 2. 검수 체크리스트

**계약 준수 (위반 = FAIL):**

1. **게이트 재도입 0** — 수락·검수 어떤 형태로도 없나
2. **판정 술어 한 곳** — request_axis 파생식(비워크플로 ∧ created_by≠assignee ∧ NOT NULL)이 중복 정의돼 있지 않나. FE 어댑터가 판정을 재유도하지 않나(fail-closed 서버 필드 소비만)
3. **migration = 인덱스 1건뿐** — 0137 이 만드는 객체가 정확히 인덱스 1개인지, 다른 스키마 변경 잠입 없나
4. **자동 cc 0** — 요청자 task_ccs 자동 추가 코드 없나
5. **DM graceful** — spec-119 재사용(신설 인프라 0), 실패해도 태스크 생성. fail-loud 혼입 없나
6. **입구 차단 = 주석/상수 수준 비활성** — RETIRED_FLOW_TYPES 축이 내부 로직·원장·leaf 를 삭제하지 않았나, 재활성이 실제로 한 줄인가, 기존 instruction run·결정 승인 발/[후속 실행] 발 부트스트랩이 계속 도나
7. **FE 금지선** — front/ diff 가 상세 메타 존에 한정(목록·칸반·본문 존 diff 0), CTA 코드 diff 0
8. **allowed_paths** — BE=back/(+mcp 진짜 필요분), FE=front/ 만. 그 밖 파일 0

**정합·품질 (WARN 후보):**

9. 채팅 담당자 해소가 spec-155 §6.1 계약(발화 명시 시에만·같은 조직 활성 구성원·모호하면 미해소+사유)과 일치하나
10. scope=requested 가 신규 endpoint·신규 leaf 없이 기존 필터 축 확장인가, read_all 미요구인가
11. 워커가 보고한 **6번째 입구(버전 WBS 태스크 발)** — WP 문서 입구 목록에 없던 것: 차단이 계약 위반이 아닌지(지시 흐름 발이 맞는지) 코드로 판정하고, WP 문서 환류 대상으로 기록
12. 테스트가 계약을 실제로 고정하나(재활성 한 줄 증명·금지선 테스트·요청자 취소 축) — 수치가 아니라 내용으로
13. 기존 실패 2건(worker 주장: 선행 실패) — diff 무관성 판정

## 3. 산출물

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/review-code-report.md` — 판정(PASS/WARN/FAIL) + 항목별 근거(파일:줄) + 위반 목록
- 리포 파일 수정·생성 금지(리포트 1개 예외 — 코디 레포 경로). 테스트 실행 금지.

## 4. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 값과 아래가 다르면 preamble 이 맞다.

```bash
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "reviewer_code 완료: <판정 한 줄>" \
  --body "판정 / 위반 목록(파일:줄) / 리포트 경로"

orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] reviewer_code 완료 — <판정 한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[질문] reviewer_code: <질문>" --enter`
