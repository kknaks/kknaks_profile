
# [frontend · 시안 읽기] 사용자가 고친 시술현황판 시안 받아 정리 (read-only)

너는 **cc-prototype `frontend` 워커**. claude design(DesignSync). **시안 수정 · 업로드 금지 · 코드 수정 금지.**
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2` — 산출물 경로 말고 건드리지 마라.

## 1. 배경

사용자가 claude design `dda9a931` 에서 **시술현황판 시안을 직접 고쳤다**(r2 = 네가 올린 `Ceramique 시술현황판 v2.dc.html` 이 출발점). 파일 이름은 받지 못했다 — v2 를 덮어썼을 수도, 새 파일일 수도 있다. 이 시안을 보고 코디와 사용자가 **정책(DEC-005)** 을 정한다.

## 2. 할 일

1. `list_files` — r2 직후 46개와 비교해 **새 파일**을 찾는다. 새 파일이 없으면 `Ceramique 시술현황판 v2.dc.html` 을 받아 로컬 사본 `orchestration/work/myeongdong-poc-v2/design-upload/Ceramique 시술현황판 v2.dc.html` 과 비교해 **바뀌었는지** 확인한다. 시술 관련 후보가 여럿이면 전부
2. 사용자가 고친 파일을 `orchestration/work/myeongdong-poc-v2/design-user-r3/` 에 원래 이름으로 저장(`truncated` 확인)
3. **r2 대비 바뀐 것 전부** — 구조 · 카드 구성 · 버튼 · 상태 이름 · 색 · 패널 탭 · 모달 · 장면 · 문구. diff 로 세고 사람이 읽을 말로
4. **정책 후보 뽑기** — 시안이 정한 것처럼 보이는 규칙을 한 줄씩(예: 「오더 메모 = 일정 높이 + 스크롤」 · 「마취 중 색 = ○」 · 「[귀가 대기] 는 전부 끝나야 활성」 · 「시술 진행 중 카드에도 [의사 호출]」). r2 리포트 §6 · v1 리포트 「정할 것」 각 항목이 **사용자 시안에서 어떻게 됐는지**(정해짐 · 그대로 · 사라짐) 표로
5. **배포 코드와 어긋난 곳** — r2 코드 대조표(`design-r2-report.md` §1) 기준으로 사용자 수정이 코드 값에서 벗어난 곳만(판단하지 말고 사실)
6. `workflow-v2.md` 와 다른 점(사실만)

## 3. 산출물 — 이것만

- `orchestration/work/myeongdong-poc-v2/design-user-r3/` (받은 파일)
- `orchestration/work/myeongdong-poc-v2/design-r3-read-report.md` — 맨 위 「찾은 파일 · 바뀌었나」 → §3 바뀐 것 → §4 정책 후보 표 → §5 코드 어긋남 → §6 workflow 차이

## 4. 하지 말 것

- 시안 수정 · 업로드 · 삭제(DesignSync 쓰기 0), 코드 · 다른 리포 파일 수정, 커밋 · push · PR
- 결정하지 마라 — 후보와 사실만
- 시안에 실제 사람 이름이 있으면 리포트에 옮기지 마라

## 5. 검증

- 받은 파일 `truncated:false` · 비교한 기준 파일 명시 · 리포트 사람 이름 · 연락처 0(grep)

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "frontend 완료: 사용자 시안 r3 읽기" \
  --body "찾은 파일 / 바뀐 것 수 / 정책 후보 수 / 코드 어긋남 수 / 검증"

orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] frontend 사용자 시안 r3 읽기 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] frontend: <질문>" --enter`
