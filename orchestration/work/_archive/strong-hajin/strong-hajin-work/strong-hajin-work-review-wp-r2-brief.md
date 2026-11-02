
# [reviewer] WORK-001 마지막 최소 diff 검수 — RF-1/RW-1~4

너는 **strong-hajin `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이번은 planner 리뷰다. 코드 워크트리에서 실행하되 실제 검수 대상은 아래 코디 문서 4건이다. 모두 read-only, 보고서 1개만 작성한다.

## 1. SSOT

`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-wp-report.md` 재검수1차의 RF-1 및 RW-1~4.
`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/strong-hajin-work-wp-fix3-brief.md` 최소 정정 발주.

## 2. 목적

마지막 최소 diff 확인만 한다. 전체 재조사 불필요. 이미 해소 확인한 F-1~6/W-1~7은 재개방하지 않는다.

## 3. 대상

코디 문서 레포의 SPEC-001 v0.2.4와 WORK-001. 경로는 이전 브리프와 동일.

## 4. 확인

- RF-1: REST 키가 Idempotency-Key 헤더로만 정의되고 본문표·Validation·sequence·WP Phase1 일치. MCP 명시 인자 계약 유지.
- RW-1: MU-A/B에서 assignee_id REST 거부, MU-C 라우트 소비와 같은 시점에 허용. 입력을 받아 무시하는 창 없음.
- RW-2: assigned 쓰기 work_tasks.py:901과 읽기 action_center.py:302 추가.
- RW-3: MCP key 인자 설명/스키마에 의도/재시도 규칙 추가.
- RW-4: create_current_meeting 및 api.ts 요청 댓글 근거 이름 정정.
- 이 수정으로 새 모순이 생기지 않았는지 좁게 확인한다. 코드/테스트/DB 실행 금지.

## 5. allowed_paths

`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-wp-report.md`에 `재검수 (2차)` 절만 추가. 기존 보고서 보존. 코드·대상 문서 수정 금지.

## 6. 보고

5개 항목별 판정/근거 줄, 최종 PASS/WARN/FAIL. 통과면 사용자 리뷰에 넘길 수 있음을 명시. 짧은 보고면 충분하다.

## 7. 범위 제약

OQ-A/D2 임의 결정 금지. 타 사용자 작업 제외. 새 기술 대안 발명 금지.

## 8. 검증

수정된 표현의 정합과 phase TODO 유지 확인. 실행하지 않은 테스트 성공 주장 금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_c04e3e99-1781-4d5b-97a0-864db71b9293 \
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
