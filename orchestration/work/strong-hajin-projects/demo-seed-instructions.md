# 데모 더미 — 「프로젝트」 화면 E2E 용 (사용자가 바로 눈으로 볼 것)

**사용자가 지금 이 데이터로 브라우저 E2E 를 한다.** 화면의 **어려운 자리가 전부 한 번씩 나와야** 한다.

**고칠 파일**: `backend/src/ax_workspace/bootstrap/demo_work.py` (+ 필요하면 그 계약 테스트
`backend/tests/contract/test_demo_work_seed.py`). **그 밖은 건드리지 마라.**
**넣는 법**: `make reset-demo` (DATABASE_URL 기본값 = 로컬 demo DB). **반드시 돌려서 실제로 들어간 것을 확인하라.**

지금 `demo_work.py` 는 mina 의 업무만 넣고 **프로젝트가 하나도 없다.** 그래서 새 화면이 빈 채로 뜬다.

## 반드시 나와야 하는 것 — 화면의 어려운 자리

### A. 프로젝트 둘

1. **「하반기 제품 개편」** — 아래 트리가 사는 곳. **mina·jiho 둘 다 참여**
2. **「브랜드 리뉴얼」** — **업무가 하나도 없는 프로젝트**(빈 본문·빈 간트를 본다). mina 참여

### B. 3층 트리 — **요청을 주고받으면 나오는 기본 모양**

```
보고서 작성            (mina, 최상위)
└ 보고서 디자인        (jiho 에게 요청 → 수락)       ← 1단계
  └ 디자인 시안 조사   (jiho 가 자기 하위로 쪼갬)     ← 2단계 = 손자
```

- **실제 요청 경로로 만들어라** — `WorkRequest` 발송 → 수락. 직접 배정으로 흉내내지 마라
  (그 경로는 프로젝트를 못 싣는다). 지금 파일의 `Ask(...)` 가 그 길이다
- **손자가 프로젝트에 속하는지 확인**하라 — 상속으로 들어가야 한다

### C. 의존선 — **접었을 때가 핵심이다**

- **손자에 선행을 건다** — 같은 프로젝트의 **다른 가지 업무**를 선행으로. 그래야 가지를 접었을 때
  「닻이 접힌 부모 바에 붙는」 화면이 보인다
- **같은 접힌 가지 «안쪽»** 선도 하나 만들어라(형제끼리 선행) — 그때는 선이 아니라 **건수**로 나온다
- **평범한 선** 두엇 — 최상위끼리 선행 → 후행

### D. 진행률 — 네 경우가 다 보이게

- **체크리스트가 있는 업무**(일부 완료 — 막대에 fill 과 % 가 난다)
- **체크리스트가 없는 업무**(**% 도 fill 도 안 난다** — 0% 가 아니다)
- **완료된 업무**
- **하위를 가진 상위 업무**(바가 14px 이고 % 가 없다)

### E. 기간 — 정규화 네 갈래

- 시작·마감 다 있는 업무 / **마감만 있는 업무**(그 날 하루) /
  **기간이 아예 없는 업무**(간트에 안 서고 좌 레일에만) / **기한이 지난 업무**(지연 칸에 잡힌다)

### F. 상태·담당

- `open` · `in_progress` · `blocked`(사유 필수) · `done` · **`cancelled` 하나**(취소선 바 + 요약 모수에서 빠진다)
- **담당이 없는 업무 하나**(`assignee: null` — 화면이 「미정」을 지어내지 않는 걸 본다)

## 지킬 것

- **날짜는 `today` 기준 상대값**으로 둬라(지금 파일이 그렇게 한다). 고정 날짜를 박지 마라
- **기존 시드를 깨지 마라** — 지금 있는 업무·요청은 다른 화면(업무·캘린더·수신함)이 쓴다.
  **더하는 쪽**으로 간다
- 실패하면 조용히 넘기지 말고 **왜 실패했는지 리포트에 적어라**
- **`material_*` 은 건드리지 마라.** 서버·API 를 띄우지 마라(`reset-demo` 는 DB 작업이라 괜찮다)
- **커밋·push 금지**

## 검증

1. `make reset-demo` 가 **exit 0**
2. **실제로 들어갔는지 확인** — `GET /api/projects` 와 `GET /api/projects/{id}` 를 계약 테스트
   하네스 안에서 찍어(서버 기동 없이) **A~F 각각이 실제로 나오는지** 리포트에 붙여라
3. `make test-contract-serial FILES=tests/contract/test_demo_work_seed.py` 통과
4. 리포트: `orchestration/work/strong-hajin-projects/demo-seed-report.md` —
   **A~F 각 항목이 어느 업무로 실현됐는지 표**로. 사용자가 그 표를 보고 화면에서 찾는다

## 역할·맥락

너는 **strong-hajin `backend` 워커**다. 먼저 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `.md`)
- 코드 레포 `AGENTS.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/be-impl-report.md` §6 (실물 응답 모양)
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md` (화면 계약)

워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`
⚠ **다른 워커가 `backend/tests/` 에서 Phase 0 를 곧 시작한다.** 너는 `bootstrap/demo_work.py` 와
그 계약 테스트 **하나**만 건드려라.

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_f21b0b84-376b-4c2d-9856-905d432ce974 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: 데모 더미" \
  --body "A~F 각각 어느 업무로 실현됐나 / reset-demo 결과 / 실물 응답 확인 결과 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] backend 완료 — 데모 더미. 상세는 인박스." --enter
```
