
# [frontend] WP-129 P4 — 상세 메타 요청자 행 (요청 표시)

너는 **mediness `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-improve`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

**BE 워커가 같은 워크트리의 `back/`·`mcp/` 에서 병렬 작업 중이다 — 거기를 건드리지 마라.**

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec/products/mediness/30-work/work-129-task-request-axis.md` — **네 몫 = P4(FE 요청 표시) + P6 중 FE 항목만.** P4 의 작업·검증 체크리스트가 정본이다
- `../20-spec/spec-154-decision-workflow.md` §4.19 — 상세 셸·메타 존 계약 (같은 spec 워크트리)

기대는 개념 — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

업무 요청(만든 사람 ≠ 담당자인 비워크플로 태스크)이 도입된다. 「누가 시켰는가」가 상세에서 읽혀야 하므로 **상세 메타 존에 요청자 행**을 넣는다. 목록/칸반 화면은 사용자 시안 대기라 **이 작업이 건드리지 않는다.**

## 3. 계약

- 요청자 행은 **요청일 때만** 렌더 — 빈 행 두지 않는다 (요청 판정은 서버 응답 필드를 따른다. BE 가 P2 에서 내려주는 파생 필드 — shape 는 WP-129 P2·P4 참조. 응답에 아직 없으면 BE 워커와 코디를 통해 계약 확인)
- **요청자 계정에는 상태 칩 드롭다운 미노출** — 요청자는 취소만 가능(상태 전이는 담당자 몫)
- ⛔ `/ax/tasks` 목록·칸반 구조 금지 (WP-130 P7 시안 대기)
- ⛔ 상세 **본문 존** 금지 — 6블록 재구성은 WP-130 몫. 네 diff 는 **메타 존에 한정**된다

## 4. 먼저 읽을 핵심 파일

- `front/components/tasks/detail/*` — 상세 메타 존 (WP-129 §Code Surface)
- WP-129 P4 검증 체크리스트 3항목

## 5. allowed_paths — 이 밖은 건드리지 마라

- `front/`

## 6. 구현 단계

1. WP-129 P4 정독 → 메타 존 컴포넌트·응답 필드 확인
2. 요청자 행 + 상태 칩 미노출 구현
3. P4 검증 체크리스트 3항목 확인 (본문 존 diff 0 포함)

## 7. 범위 제약 — 하지 말 것

- 목록/칸반·본문 존·WP-130 범위 금지
- 전체 빌드·전체 포맷 검사 금지 (사용자 방침)
- 커밋·push·PR 금지 (§9)

## 8. 검증

```
cd /Users/kknaks/orca/workspaces/mediness-app/task-improve/front && npx tsc --noEmit && npx prettier --check <네가 만진 파일만>
```

- 네가 만진 파일 0 에러. 전체 빌드·전체 포맷 검사 금지 — 사용자 방침. **검증은 1회만.**
- node_modules 없으면 `npm ci` 선행 (끝나면 워크트리에 남겨 둬도 된다 — 코디 검증이 재사용).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 브리프 작성 시점 값이라 오래됐을 수 있다 — preamble 값과 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(tsc·prettier) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[질문] frontend: <질문>" --enter`
