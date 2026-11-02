
# [frontend · 시안 조회] 시술 현황판 시안 찾아 받기 (read-only)

너는 **cc-prototype `frontend` 워커**(시안 조회 담당). claude design 작업(DesignSync). **코드 금지 · 시안 수정 금지 · 업로드 금지.**
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더 문서)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2` — 코디네이터가 같은 워크트리에서 문서를 쓰고 있다. **아래 산출물 경로 말고는 아무것도 만들거나 고치지 마라.**

## 1. 배경

명동 PoC v2 = **시술 현황판**. 사용자가 claude design 프로젝트에 새 시안을 **이미 만들었다**. 파일 이름은 모른다. 시안을 받아야 코디가 결정(DEC-005) · 스펙(SPEC-003)을 시안 기준으로 쓴다.

- claude design 프로젝트: `https://claude.ai/design/p/dda9a931-097f-4780-9301-972d5ac1fc23` (1 · 2차 시안이 전부 여기 있다)
- 기존 파일(1 · 2차, 참고): 현황판 v3~v5 · 직원 화면(의사 · 코디 · 모바일) · `Ceramique 예약관리 v1.dc.html` · `Ceramique 현황판 폰 v1.dc.html` 등. 2차 업로드 직후 목록은 23개였다(`orchestration/work/_archive/cc-prototype/cc-nav-resv/design-report.md`)
- 업무 흐름(무엇을 그린 시안인지 알아보는 기준): `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/reference/2026-10-12-cc-prototype/workflow-v2.md`

## 2. 할 일

1. DesignSync 로 프로젝트 **파일 목록 전체**를 받는다(이름 · 수정 시각 · 크기, 도구가 주는 만큼)
2. **새 시안 찾기** — 2차 목록(23개)에 없던 파일, 또는 수정 시각이 2026-10-20 인 파일. 이름에 「시술」 · 「현황」 · 「오더」 · 「태블릿」 · 「v2」 등이 있으면 우선. 후보를 전부 적는다(하나로 좁히지 마라)
3. 후보 파일을 **전부 내려받아** `orchestration/work/myeongdong-poc-v2/design-download/` 에 원래 이름 그대로 저장한다. `truncated` 여부를 확인하고 잘렸으면 그렇게 적는다
4. 각 후보 시안을 읽고 정리한다:
   - 화면 · 장면 목록(캔버스 props · scene 값이 있으면 그 값) · 폭(데스크톱 · 태블릿 · 폰)
   - 화면마다 보이는 요소 — 카드 구성 · 버튼 · 상태 이름 · 필터 · 모달
   - `workflow-v2.md` 와 **다른 점** · workflow 에 없는데 시안에 있는 것 — 판단하지 말고 사실만 한 줄씩
   - 쓰인 디자인 시스템(medikit · Ceramique 테마인지)
5. 리포트 작성

## 3. 산출물 — 이 둘만

- `orchestration/work/myeongdong-poc-v2/design-download/` — 받은 시안 파일
- `orchestration/work/myeongdong-poc-v2/design-fetch-report.md` — 맨 위에 **파일 목록 전체 표**(새 파일 표시) → 후보별 정리 → 「정할 것」

## 4. 하지 말 것

- 시안 수정 · 업로드 · 삭제(DesignSync 쓰기 0)
- 코드 레포 · 다른 리포 파일 수정, 커밋 · push · PR
- **실제 고객 · 직원 이름이 시안에 있으면 리포트에 옮기지 마라** — 「이름 칸」으로만(이 레포는 public)
- 결정하지 마라 — 시안과 workflow 가 다르면 「정할 것」으로

## 5. 검증

- 목록 표의 파일 수 = DesignSync 가 준 수
- 받은 파일 수 = 후보 수, 각 파일 `truncated` 확인
- 리포트에 사람 이름 · 연락처 0(grep)

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다. preamble 의 코디네이터 핸들과 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: 시안 조회 <한 줄>" \
  --body "찾은 파일 / 받은 경로 / 화면 요약 / workflow 와 다른 점 수 / 정할 것"

# (2) 직접 주입
orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] frontend 시안 조회 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] frontend: <질문>" --enter`
