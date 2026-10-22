
# [planner] SPEC-003 · WORK-003 — 시술 현황판(procedure) 계약 · 작업 순서

너는 **cc-prototype `planner` 워커**다. 역할 문서(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/roles/cc-prototype/planner/role.md` (+ 같은 폴더)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2`(코디 워크트리 · 문서 레포 `kknaks/kknaks_profile` · **public**). 코디가 같은 워크트리에 있다 — allowed_paths 밖은 건드리지 마라.

## 1. SSOT — 이 순서로 이긴다

1. **결정**: `para/projects/summer-star/cc-prototype/10-decision/decision-005-procedure-board.md`(DEC-005 D-01~D-34 · OQ-501~503) — 계약의 원천. 여기 없는 정책을 만들지 마라
2. **확정 시안**: `orchestration/work/myeongdong-poc-v2/design-user-r4/Ceramique 시술현황판 v2.dc.html` + 읽기 리포트 `design-r3-read-report.md`(§3 바뀐 것 · §4 정책 P1~P19 · §5 코드 어긋남) · `design-r4-read-report.md`(Q1~Q4). **DEC-005 가 시안을 고친다고 적은 곳(D-23 마취 · D-27 수락 범위 · D-28 되돌리기 없음)은 DEC 가 이긴다**
3. **KOS API 사실**: `reference/2026-10-12-cc-prototype/kos-demo-api.md`(공개 API 필드 · 모양) · 결정 표의 HAR 사실(`orchestration/work/myeongdong-poc-v2/_RESUME.md` §2 「(사실)」 줄 — 내부 API 경로 · 본문 · 헤더 · 상태 변화)
4. 배경: `reference/2026-10-12-cc-prototype/workflow-v2.md`(10-20 판 — DEC-005 와 다르면 DEC 가 맞다) · BASE-008
5. 형식 참고: 기존 `20-spec/spec-002-cc-nav-reservation.md` · `30-work/work-002-cc-nav-reservation.md` · 각 폴더 README(인덱스)
6. 디자인 코드 원천(read-only): `/Users/kknaks/git/toy_pr2/cc-prototype` `origin/main` 의 `cc/front`(`git -C … show origin/main:<경로>` 로 읽어라 — checkout · pull 금지). r2 리포트 `design-r2-report.md` §1 코드 대조표

## 2. 만들 것

### A. `20-spec/spec-003-procedure-board.md` (+ `20-spec/README.md` 인덱스 한 줄)

`procedure/back`(FastAPI) · `procedure/front`(Next.js) 가 지킬 계약. 최소 절:

1. 범위 In/Out(DEC-005 D-01~05 · D-34)
2. **폴더 · 실행** — `procedure/` 구조, 로컬 실행(사용자가 로컬 E2E 를 한다): `procedure/docker-compose.yml` 또는 동등한 한 줄 실행, env 목록(`.env.example` — **값 없이 이름만**: KOS 공개 키 · 시스템 계정 이메일/비번 · ccc 관리자 아이디/비번 · 조회 구역 · 조회 시간 · DB 경로 등), 포트. 테마 복사 목록(D-02 — 어느 파일을 `cc/` 에서 가져오나)
3. **데이터 모델**(D-12~15) — 테이블 · 필드(ccc 이름) · `kos_id` · 원천(KOS/ccc) · **KOS 필드 대응표**. ccc 고유: 마취 회차 · 호출(만든 시각 · 대상 시술 · 지정 원장/전체) · 수락 · 시술 시작 · 귀가 대기 · 조작 이벤트 로그 · KOS 반영 상태(대기 · 보냄 · 확인 · 실패)
4. **KOS 연동** — 인증(공개 · 내부, 토큰 보관 · 갱신 D-07), 조회(D-08 — 무엇을 · 주기 · 시간창 · 4층), 덮어쓰기 · 기준 규칙(D-09 — 필드별 표), 「KOS 반영 중 · 실패」 재전송 규칙, 원장 목록 필터(D-11)
5. **상태 · 규칙** — 고객 상태(대기 · 진행 · 귀가 대기 ← KOS `flowStep`), 마취(D-23), 호출 · 유효 호출 · 수락(D-24~28), [시작] · [종료] 조건(D-30~32), 귀가 대기(D-33), 카드 표시 조건(D-21 · 22), 「확인이 필요」 기준(D-20). **상태 전이표**와 **버튼 활성 조건표**
6. **화면** — 시안 기준: 헤더 · 사이드바 · 가운데 카드(D-17~19) · 오른쪽 패널 탭(현황 · 호출 · 고객 · D-20) · 의사 호출 팝오버 · 로그인 화면(관리자 1개 · D-05). 시안 장면 이름으로 가리킨다. 시안과 DEC 가 다른 곳은 따로 표
7. **back ↔ front API** — 경로 · 요청 · 응답 필드 · 오류 코드. 화면 갱신 방식(폴링 주기 등 — 정해지지 않았으면 단순한 것으로 두고 「열린 것」에)
8. **KOS 반영 표** — ccc 조작마다 KOS 호출(공개/내부 · 경로 · 본문)
9. 검증 기준 — 로컬 E2E 시나리오(데모 지점으로): 카드 등장 → 마취 → 호출(전체 · 지정) → 수락 → 시작/종료 → 귀가 대기, 각 단계 KOS 쪽 확인 방법
10. 열린 것(OQ-501~503 + 새로 생긴 것)

### B. `30-work/work-003-procedure-board.md` (+ `30-work/README.md` 인덱스 한 줄)

구현 작업 순서(WP). **이번 목표 = 사용자가 로컬에서 E2E 를 할 수 있는 상태**(배포 · `_archive/cc` 이동 · infra 는 **마지막 WP 로 분리** — 로컬 E2E 통과 뒤). WP 마다 담당(backend · frontend · infra), 범위(파일 경로), 완료 조건, 검증 명령(부분 검증 — 전체는 마지막 한 번). backend 와 frontend 가 병렬로 갈 수 있게 계약(§7)을 먼저 고정하는 순서로.

### C. `reference/2026-10-12-cc-prototype/workflow-v2.md` 갱신

DEC-005 로 바뀐 것 반영(현황판에서 [시작]/[종료] · 의국 화면 수락 · 호출 시각 규칙 · 마취 별개 · 방 빼기 = 귀가 대기 · 4층 · 조회 시간 · 새 기능 폴더 · 데이터 모델 원칙 등). 뒤집힌 것은 지우지 말고 「(2026-10-21 바뀜)」으로 표시.

## 3. allowed_paths

- `para/projects/summer-star/cc-prototype/20-spec/` · `para/projects/summer-star/cc-prototype/30-work/` · `reference/2026-10-12-cc-prototype/workflow-v2.md`
- 그 외 read-only. 커밋 · push · PR 금지

## 4. 하지 말 것

- DEC · 시안에 없는 정책 발명 — 비면 「열린 것」
- 키 · 토큰 · 비밀번호 · 실명 · 연락처(public). env 는 이름만
- 코드 작성

## 5. 검증

- SPEC 각 규칙 줄에 근거(DEC-005 D-번호 · 시안 장면/P-번호 · HAR 사실) — 근거 없는 줄 0
- DEC-005 D-01~D-34 가 SPEC 어디에 반영됐는지 대응표(SPEC 끝 부록)
- 링크 · 인덱스 · frontmatter(`spec-002` 형식) · public grep(`@` 메일 · 긴 토큰 · 한글 실명) 0

## 5-1. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "planner 완료: SPEC-003 · WORK-003" \
  --body "변경 파일 / SPEC 절 요약 / WP 목록 / 열린 것 / DEC 대응표 누락 0 여부 / 검증"

orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] planner SPEC-003 · WORK-003 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] planner: <질문>" --enter`
