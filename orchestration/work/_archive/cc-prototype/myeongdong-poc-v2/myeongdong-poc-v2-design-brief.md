
# [frontend · 시안] 디자인 1단계 — 시술 현황판(간호 스테이션) 새 시안

너는 **cc-prototype `frontend` 워커**(시안 담당). claude design 작업(DesignSync). **코드 금지.**
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더 문서)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2` — 코디가 같은 워크트리에서 문서를 쓴다. **산출물 경로 말고 리포 파일을 건드리지 마라.**

## 1. SSOT

- **업무 흐름 정본**: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/reference/2026-10-12-cc-prototype/workflow-v2.md` — 특히 「원칙」 · 「화면」 · 2~6절 · 「KOS 반영 표」
- **오늘 정한 것(결정 표)**: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/_RESUME.md` §2 — 취소선 줄은 뒤집힌 것이다. 아래 §3 이 그 요약이다
- KOS 실데이터 모양(필드 · 상태 enum): `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/reference/2026-10-12-cc-prototype/kos-demo-api.md` §3.3
- **디자인 언어**: claude design `https://claude.ai/design/p/dda9a931-097f-4780-9301-972d5ac1fc23` 의 기존 Ceramique 시안(현황판 v5 · 직원 화면 · 예약관리 v1) — 같은 medikit · Ceramique 테마 · 1차 컴포넌트. **기존 파일은 하나도 고치지 않는다**(DEC-004 D-21)
- 방금 네가 만든 `orchestration/work/myeongdong-poc-v2/design-fetch-report.md`(있으면) — 기존 파일 목록

## 2. 만들 것 — 새 파일 1개

**`Ceramique 시술현황판 v1.dc.html`** — 간호 스테이션 PC(데스크톱 가로, 본문 1280px 이상에서 카드가 가로로 흐른다)

같은 프로젝트에 **추가**만 한다. 업로드 전에 로컬 사본을 `orchestration/work/myeongdong-poc-v2/design-upload/` 에 둔다.

## 3. 화면 내용

### 머리

- 제목 「시술 현황」 · 정렬 토글 **[입실순 | 배치순]**(입실순 = 방에 들어온 시각, 배치순 = 방 순서)
- 상태별 수: 시술 대기 n · 시술 진행 n · 귀가 대기 n
- 마지막 KOS 동기화 시각(작게)

### 본문 = 오더지 카드 나열(도면 아님)

간호사들이 오더지를 출력해 방 번호와 꽂아 두고 보는 방식을 그대로 화면으로. **고객이 있는 방만** 카드. 귀가 대기 카드는 **흐리게 맨 뒤**.

카드 하나(위 → 아래):

1. **머리** — 방(`A-룸2`) · 고객 이름 · 신규/재방문 · 국적 · 입실 시각 · 고객 상태(시술 대기 / 시술 진행 / 귀가 대기)
2. **오더 메모** — 원문 그대로(잘라 읽지 않는다). **일정 높이 + 넘치면 스크롤 + [접기 · 펴기]**. 길이는 사람마다 다르다
3. **마취** — 한 줄. 진행 중이면 「마취 중 05분 경과 [마취 종료]」, 아니면 [마취 시작]. 끝난 회차는 「마취 1회 23분」 요약. **여러 회차** 가능. 알람 · 목표 시간 표시 없음(경과 시간만)
4. **시술 진행** — 체크박스 목록. 완료된 시술이 완료 시각 순으로 위 `[✓] 울쎄라 300shot 14:20~14:38 ○○ 원장`, 그 아래 진행 중 `[ ] 써마지 FLX 진행 중 07분`, 맨 아래 대기. 줄마다 집도의 또는 호출 상태(「호출함 · 전체」 · 「호출함 · 지정 ○○ 원장」)
5. **버튼** — [의사 호출] · [귀가 대기](시술이 전부 끝났을 때만 활성). 시술 진행 중 카드는 **조회 위주**(시술 [시작] · [종료]는 시술실 태블릿 · 폰 몫이라 현황판에 없다)

### [의사 호출] 모달

- 시술 체크(기본 = 남은 시술 전부 선택) → **[전체 호출] | [특정 의사 선택]**(원장 목록에서 하나)
- 보통은 한 방 = 원장 한 명이 전부. 예외: 「이 시술만 특정 원장」 → 그 시술만 체크하고 특정 의사

### 장면(캔버스 props `scene`)

하나의 화면에 상태가 섞인 카드 5~6장이 기본 장면이다. 최소:

- `board` — 섞인 상태: 시술 대기(마취 전) · 마취 중 · 호출함(전체) · 시술 진행(완료 1 · 진행 1 · 대기 2) · 지정 호출이 섞인 카드 · 귀가 대기(흐림)
- `board-placement` — 같은 데이터 배치순
- `memo-expanded` — 긴 오더 메모 펼친 카드
- `call-modal` · `call-modal-specific` — 의사 호출 모달(전체 / 특정 의사 + 시술 하나만 체크)
- `all-done` — 모든 시술 완료 → [귀가 대기] 활성

### 데이터

- KOS 데모 지점 **모양**: 방 `A-룸1 ~ A-룸n`, 시술 3~5개(예: 바디보톡스 100unit · 울쎄라피 프라임 300shot · 써마지 FLX 300shot · 쥬베룩 · 포텐자 · 리쥬란 힐러 2cc), 오더 메모는 번호 줄이 있는 자유 글
- **이름은 전부 가짜**(고객 · 원장 · 직원). 실제 사람 이름 금지(public 레포)

## 4. 하지 말 것

- 기존 시안 파일 수정 · 삭제(쓰기 = 새 파일 1개 업로드뿐)
- 코드 · 다른 리포 파일 수정, 커밋 · push · PR
- 태블릿 · 폰 화면(디자인 2단계 — 사용자 고민 중), 시술실 고객 모니터(다음 버전), 시술 차트(보류)
- 흐름을 새로 정하지 마라 — workflow 에 없는 게 필요하면 시안엔 가장 단순하게 두고 리포트 「정할 것」에

## 5. 검증 · 리포트

- 업로드 뒤 `list_files` 로 기존 파일 수 그대로 + 새 파일 1개 확인, 다시 받아 로컬 사본과 같은지
- 장면마다 값이 바뀌는지(렌더를 못 보면 스크립트를 node 로 돌려 장면별 값 확인 — 2차 방식)
- 리포트 `orchestration/work/myeongdong-poc-v2/design-report.md` — 파일 · 장면 표 · §3 항목별 반영 · workflow 와 다른 점 · 정할 것 · 사람 이름 0 grep 결과

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "frontend 완료: 시술현황판 시안 v1" \
  --body "업로드 파일 / 장면 / 반영 요약 / workflow 와 다른 점 / 정할 것 / 검증"

orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] frontend 시술현황판 시안 v1 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] frontend: <질문>" --enter`
