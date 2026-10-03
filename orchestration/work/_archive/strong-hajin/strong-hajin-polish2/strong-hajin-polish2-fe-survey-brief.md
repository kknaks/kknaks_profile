# [frontend] 고도화 2차 — 운영 E2E 요청 5건의 화면 쪽 현재 코드 전수조사

너는 **strong-hajin `frontend` 워커**다. **너는 이 작업의 맥락이 없다** — 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2/AGENTS.md`
- 1차(직전 판) 기록: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md`(WORK-008 — 원칙 P-1~P-3, Phase 3b·5 가 이번 요청과 닿는다) · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/_archive/strong-hajin/strong-hajin-polish/fe-survey-report.md`(1차 조사 — 출발점, 줄 번호는 옛 값)
- 회고: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/log/2026-10-02-strong-hajin-polish.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2`
base: `origin/main` (`3d47a32` — 1차가 운영에 반영된 코드)

⚠ **같은 워크트리에 backend 워커가 동시에 탄다.** 둘 다 읽기 전용 조사이고 서로 다른 리포트 파일 하나씩만 쓴다. `backend/` `frontend/` 어느 쪽도 **고치지 마라.** 네 몫은 `frontend/` 이지만, 답에 필요하면 반대쪽도 읽어라.

## 0. 이것은 조사다 — 고치지 마라

**읽기 전용 조사다.** 코드를 한 줄도 바꾸지 않는다. 산출물은 리포트 **한 장**뿐이다.
「이렇게 고치면 된다」는 쓰지 마라 — 사용자가 이 리포트를 보고 계약을 정한다. **지금 무엇이 어떻게 도는지만** 적는다.
테스트·빌드를 돌리지 마라. 읽어서 답할 수 있는 것만 답하고, 못 답한 것은 「조사 한계」에 적는다.

## 1. 왜 조사하나

사용자가 운영(`https://ax.medisolveai.xyz`)을 쓰며 요청 다섯을 냈다(E2E-1~5). 사용자는 **전부 논의하고 정하겠다**고 했다.
그 논의의 근거가 이 리포트다. 각 요청이 닿는 코드가 **어디에 몇 군데** 있는지, 지금 **어떻게** 동작하는지를 확정한다.
빠진 자리가 곧 다음 판의 FAIL 이다 — **시작점에서 멈추지 말고, 같은 심볼·패턴을 쓰는 곳을 grep 으로 전부 세어 숫자로 적어라.**

## 2. 요청별 물음

### E2E-1 AX 업무 초안 카드의 체크리스트 페이지가 「없음」
- 시작점: `features/action/ActionTaskCard.tsx`(초안 카드), 「새 업무 추가」 모달(`WorkModals.tsx` `CreateTab`)
1. 카드 체크리스트 페이지가 어느 필드를 읽어 그리나(파일:줄). 서버가 체크리스트를 주면 그려지는 상태인가 — 즉 빈 것이 화면 탓인지 데이터 탓인지
2. 「수정」 모달이 초안의 체크리스트를 미리 채우나, 모달에서 넣은 체크리스트가 confirm draft 에 실리나

### E2E-2 「수정」으로 연 새 업무 추가 모달의 「등록」 → 「저장」으로 바꿀 예정
- 사실: 운영에서 AX 카드 「수정」 → 「새 업무 추가」 모달이 열리고 아래 단추가 파란 「등록」. 누르면 바로 등록(confirm)된다
1. AX 초안으로 모달을 여는 경로와 모드 구분(prop·상태) — 일반 새 업무 추가와 어디서 갈리나(파일:줄)
2. 모달 「등록」이 부르는 함수·API 와 성공 뒤 카드·채팅·홈·「AX 제안」 칩이 어떻게 갱신되나
3. 카드가 초안 값을 어디서 받나 — 채팅 메시지에 박힌 스냅샷인가, 판단 대기 목록인가, 매번 다시 읽나. 초안이 바뀌면 카드가 새 값을 보일 길이 지금 있나
4. 같은 「새 업무 추가」 모달을 미리 채운 값(`initial`)으로 여는 자리 **전부**(하위 업무·회의 승격·재요청·AX 초안…) — 단추 문구·제출 함수가 각각 무엇인가

### E2E-3 AX 채팅 카드 「등록」을 누르면 「등록 중」 단추가 파란색
- 원칙(1차): 채팅 서랍 안 사람이 누르는 단추 = 검정, 파랑 = AI 진행만. 1차에서 검정 solid 단추 변형을 세웠다(`94cacfd`)
1. 「등록 중」이 파랗게 되는 원인 — 진행 중 상태에서 바뀌는 클래스·variant·disabled 스타일(파일:줄)
2. 채팅 서랍 안의 사람 행동 단추 **전부**(AX 카드 거절·수정·등록, 다른 액션카드 — 회의실 예약 등, 추천 대화, 입력창 전송 등) × 상태(기본·hover·진행 중·disabled·focus) 표 — 상태마다 실제 색(토큰)
3. 검정 단추 변형의 CSS 정의와 DS 의 solid 단추 상태 규칙이 어디 있나

### E2E-4 업무 상세 헤더 — 「담당 …」 줄과 「AX 제안에서 생성됨 [업무 링크]」 줄이 붙어 있다
1. 업무 상세(`TaskDetailDrawer` 등) 헤더 아래 메타 영역의 DOM 구조·클래스·CSS 를 **실제 코드 그대로** 1:1 로 적는다(어떤 줄이 어떤 조건에서 나오나 — 담당·기한·시작·출처 배지·링크)
2. 「AX 제안에서 생성됨」 배지와 그 옆 링크가 무엇을 가리키나(자기 자신 업무로 보인다 — 실제 대상 확인), 어느 데이터로 그리나
3. 같은 출처 배지(「회의에서 생성됨」 등)가 나오는 자리 전부

### E2E-5 업무 날짜 — 시작 예정일 · 실제 시작일 · 실제 종료일 · 마감일 (논의용, 현재 상태만)
- 사실: 업무 상세 헤더가 「담당 · 기한 2026/10/06 · 시작 2026/10/01」 순이고 상세에서 날짜를 고칠 길이 안 보인다(헤더에 「편집」 단추는 있다)
1. 날짜를 **보여 주는** 화면 **전부** — 업무 상세·내 업무 목록/타임라인·캘린더·프로젝트 간트·홈·수신함·보고·AX 카드·업무 카드 등. 화면별 어떤 필드를 어떤 라벨·형식으로 보이나(표, 파일:줄)
2. 날짜를 **고치는** 입구 전부 — 「편집」 단추가 무엇을 고치나, 기한 변경·기간 변경 UI 가 어디 있나, 부르는 API
3. 날짜 표시 형식 함수(포맷터)가 몇 개이고 어디서 쓰나

### 공통 — 화면 계약을 쓸 수 있게
- 위 각 자리에서 실제 컴포넌트 파일:줄 · 클래스 · DS 부품 이름을 적는다. 다음 판 발주서는 이걸 1:1 로 옮긴다

## 3. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/fe-survey-report.md` ← **이 파일 하나만 만든다**

코드 워크트리는 **읽기만** 한다. 커밋·push·PR 금지.

## 4. 하지 말 것

- 코드·테스트·CSS 를 고치지 마라
- **서버·프론트를 띄우지 마라. 사용자 포트와 프로세스를 건드리지 마라** (8001·5176·54329)
- 브라우저를 열지 마라. **운영 서버에 접속하지 마라**
- 「이렇게 바꾸자」를 쓰지 마라
- 리포트에 사람 실명·메일을 쓰지 마라(공개 레포로 아카이브된다) — 「팀원 A」처럼 쓴다

## 5. 리포트 형식

```
# 고도화 2차 화면 전수조사

## 0. 한 줄 요약 — 요청별 한 줄 (원인이 보이면 원인 한 줄)
## 1~. 요청별 절 — §2 물음 번호대로 답
## N. grep 개수표 — 요청별로 센 심볼과 개수
## N+1. 조사 한계
```

**모든 답에 `파일:줄` 근거를 단다.** 근거 없는 문장은 쓰지 않는다.

## 6. 검증

- 리포트가 위 경로에 있다. §2 의 물음이 하나도 빠지지 않았다(못 답한 것은 조사 한계에)
- `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2 status --short` 가 비어 있다

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다. preamble 과 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --from term_82fc2322-7b14-4d60-90ee-efe1c243fd31 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: 2차 조사" \
  --body "리포트 경로 / 요청별 한 줄 요약 / 조사 한계"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba \
  --text "[worker_done] frontend 2차 조사 완료 — <한 줄 요약>. 리포트 fe-survey-report.md" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --text "[질문] frontend: <질문>" --enter`
