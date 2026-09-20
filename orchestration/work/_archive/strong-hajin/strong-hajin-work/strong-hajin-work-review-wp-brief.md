
# [reviewer] WORK-001 W1 구현 계획 검수

너는 **strong-hajin `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이번은 planner 리뷰다. 코드 워크트리에서 실행하되 실제 검수 대상은 아래 코디 문서 4건이다. 모두 read-only, 보고서 1개만 작성한다.

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/strong-hajin-work-wp-brief.md` — WP 발주와 수정 범위.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-spec-report.md` — 이전 재검수 및 R-1~6.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md` · `spec-002-action-item-review.md` v0.2.1.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/templates/projects/30-work/work.md`, `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/project.md`.

## 2. 배경

WORK-001 W1 구현 계획 초안 8 phase를 검수한다. 코드 착수 전이며 사용자에게 리뷰할 수 있는 실행 가능한 계획인지 판정한다. R-1~6 수정도 필요한 부분 확인한다.

## 3. 계약

W1 한 slice로 생성/일반 타인 요청/관리자 배정/회의후속승격/수락제거/권한/멱등/영속/REST/MCP/AX/seed/FE를 닫는다. 완료 승인·AX 확인 보존. OQ-A·D2는 임의 확정하지 않는다. 데이터 전환·호환은 D4 제외.

## 4. 대상

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-001-task-creation.md`
- BASE/DEC/SPEC 수정본과 코디 소유 index/log 정합.
- 코드 작업 사본은 read-only. `temp.md`는 다른 사용자 작업이므로 건드리거나 판정에 포함하지 않는다. `reference/2026-09-10-sc-meeting/task.md`도 제외.

## 5. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-wp-report.md` 하나만 작성.

## 6. 검수

1. phase 의존·BE/FE 경계·W1 인수조건/테스트 매핑·실제 파일 후보·내부 계약이 구현 가능한지 검수.
2. 코디 발견 의심점 검증: 내부 계약은 '키 없으면 멱등 보장 없음'인데 Phase 2는 '키 없는 같은 명령 동시 실행 중복0'을 요구한다. 독립적인 같은 내용 생성과 재시도를 구분할 식별 근거 없이 가능한지, SPEC도 같은 모순인지 조사하고 정확한 수정 범위를 제시.
3. migration 신설/rollback 계획이 현행 스키마 소유(reset_demo --sync)·D4 제외와 충돌하는지 확인. 운영 DB 적용·기존 데이터 호환 검증을 불필요한 착수 gate로 다시 넣었는지 본다. 테스트 DB 검증은 필요한데 환경 미확인 이유로 필수 검증 자체를 빼지는 않는지 확인.
4. 승인자 필드를 저장·노출하면서 완료 경로는 현행 그대로 두는 '최소 호환'이 실제 성립하는지: 요청자와 다른 승인자를 지정해도 W1 완료가 올바르게 처리되는지 코드 근거를 확인. 새 요청 생성이 기존 source_work_request_id 기반 완료 승인 의미를 깨뜨리는지도 확인. W1 범위를 임의 확대하지 말고 안전한 단계 경계 제안.
5. self 검사 없음이 인증·조직권한 우회를 뜻하는지, 새 일반 요청의 허용 후보 규칙이 결정을 개발자에게 떠넘기는지 확인. 키 scope·권한 재검증·payload 충돌·동일 회의 후보 동시승격 보장도 본다.
6. 수락/거절 명령의 전체 제거 표현이 기존 AX 확인/완료 승인이나 D4 제외와 충돌하는지. 과거 행 읽기 호환 요구가 제외 범위를 복원하는지.
7. 모든 phase에서 전량 테스트 반복 요구가 과도한지(의미 있는 단계별 focused 검증 + 통합 1회로 충분한지) 확인. 관찰하지 않은 테스트 성공 주장 금지.
8. R-1~6 수정에 새 계약 모순 없는지, W1 외 미결이 gate로 들어오지 않았는지 확인. PASS/WARN/FAIL에 파일:줄+근거, 필수 수정과 구현 중 선택 가능한 항목 분리.

## 7. 제약

리뷰 보고서 외 수정 금지. 코드 테스트/빌드/DB 실행 금지. 새로운 제품 결정 만들지 않는다. 코디의 문서 목록은 생성 완료했다.

## 8. 검증

실제 코드·원문·spec에 근거해 검수한다. 코드 실행은 하지 않는다. WP는 모든 phase TODO이며 완료 근거는 미작성이어야 한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_4086a70a-8678-476c-90bd-f0a2e71c1356 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
