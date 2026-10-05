# [frontend] 고도화 3차 — 사용자 요청 6건의 화면 쪽 현재 코드 전수조사

너는 **strong-hajin `frontend` 워커**다. **너는 이 작업의 맥락이 없다** — 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3/AGENTS.md`
- 직전 판 기록: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-009-polish2.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-007-task-detail.md`(업무 상세를 세운 판) · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/20-spec/spec-007-task-detail.md`
- 직전 조사(출발점 — 줄 번호는 옛 값): `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/_archive/strong-hajin/strong-hajin-polish2/be-survey-report.md` · `fe-survey-report.md` (같은 폴더)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3`
base: `origin/main` (`d1b5137` — 운영 반영 코드)

⚠ **같은 워크트리에 다른 워커(backend/frontend)가 동시에 탄다.** 둘 다 읽기 전용 조사이고 서로 다른 리포트 파일 하나씩만 쓴다. `backend/` `frontend/` 어느 쪽도 **고치지 마라.** 네 몫이 아닌 쪽도 답에 필요하면 읽어라.

## 0. 이것은 조사다 — 고치지 마라

**읽기 전용 조사다.** 코드를 한 줄도 바꾸지 않는다. 산출물은 리포트 **한 장**뿐이다.
「이렇게 고치면 된다」는 쓰지 마라 — 사용자가 이 리포트를 보고 계약을 정한다. **지금 무엇이 어떻게 도는지만** 적는다.
테스트·빌드를 돌리지 마라. 읽어서 답할 수 있는 것만 답하고, 못 답한 것은 「조사 한계」에 적는다.

## 1. 왜 조사하나

사용자가 운영(`https://ax.medisolveai.xyz`)을 쓰며 요청 여섯을 냈고, 업무 상세 모달은 **전면 개편**하기로 정했다(아래 R4 「정해진 방향」).
이 리포트가 계약(SPEC·WP)의 근거다. 각 요청이 닿는 코드가 **어디에 몇 군데** 있는지, 지금 **어떻게** 동작하는지를 확정한다.
빠진 자리가 곧 다음 판의 FAIL 이다 — **시작점에서 멈추지 말고, 같은 심볼·패턴·API 를 쓰는 곳을 grep 으로 전부 세어 숫자로 적어라.**

## 요청 6건 (사용자 원문 요지 — 참고용 맥락)

- **R1 로그인** — 브랜드 h1 「기록 → 판단 → 수행 → 보고를 한 흐름으로」→「메디솔브 AX 프로젝트」, 그 아래 설명 문장 삭제
- **R2 회의 상세 「내보내기」** — 옆 「공유」「다음 회의 예약」과 단추 크기가 다르다(내보내기만 `<a>` — `href="/api/meetings/{id}/export?format=html"`). **Tauri 앱에서 다운로드가 안 되는 것 같다**
- **R3 회의 제목** — 「제목 없는 회의」 옆에 「제목 후보 …」가 따로 뜬다. 제목을 클릭해 인라인으로 고치고(blur/Enter 저장), 제목 없을 때 후보를 [적용]으로 반영할 예정
- **R4 업무 상세 모달 개편 — 정해진 방향**: 헤더 = 제목(클릭 인라인 수정) + 닫기(×)만. 「메타 정보」 구역 신설(진행 상태 셀렉트 · 담당 셀렉트 · 시작 예정일/마감일 날짜 선택 즉시 저장 · 실제 시작일/버전 읽기 전용 · 출처 「AX 제안에서 생성됨 · [링크]」). 업무 내용 인라인 수정(blur 저장). **삭제**: 푸터 전체(업무 취소·시작·막힘·완료 처리), 「편집」 단추와 편집 모드, 「진행과 판단」 구역, 헤더의 「AX」 단추·상태 칩·「업무 상세」 머리글. 업무 취소는 진행 상태 셀렉트 맨 아래로. 「자료」「이력」 구역은 그대로
- **R5 선행업무 안내** — 본문 위 빨간 「시작할 수 없습니다 — ○○이 끝나지 않았습니다」 박스와 푸터 문구 「끝나지 않은 선행업무가 있습니다: ○○」 삭제. 막는 규칙은 유지하고, 상태를 바꾸려 할 때 토스트로 알릴 예정
- **R6 업무 상세 헤더 아래 여백** — 칩 줄과 「담당 …」 줄 사이(헤더 아래 패딩 + 본문 위 패딩)가 너무 크다

## 2. 요청별 물음 (네 몫 = 화면)

### R1 로그인 브랜드
1. `.login-shell > .login-brand` 의 h1·설명 `p` 가 있는 컴포넌트 파일:줄. 같은 문구가 다른 곳(문서 title·Tauri 창 제목·메타·테스트 스냅샷)에도 있나 — grep 개수

### R2 「내보내기」 단추 + Tauri 다운로드
1. 회의 상세 머리 단추 묶음(`.scax-detail__head-actions`) 파일:줄 — 「내보내기」 `<a class="scax-button …">` 와 「공유」「다음 회의 예약」 `<button>` 의 크기가 다른 원인(높이 39px — CSS 규칙·line-height·display 차이, 파일:줄)
2. `<a>` 에 `scax-button` 클래스를 쓰는 자리 **전부** — 같은 크기 문제가 있나
3. **Tauri 에서 다운로드가 되나**: `frontend/src-tauri` 설정(capabilities·plugins·window 설정)에 다운로드/파일 저장 처리가 있나, 웹뷰에서 `<a href>` 로 파일 응답을 열면 무엇이 일어나는 구조인가(새 창·내비게이션 차단 등 — 코드로 확인되는 만큼). 앱의 API 요청이 인증을 어떻게 싣나(api.ts — 쿠키/헤더, Tauri flavor 별 origin) — `<a href>` 로 직접 열 때도 실리나
4. 앱에서 파일을 내려받는 자리 **전부**(회의 내보내기·자료 파일·결과 자료 등) — 방식(a href / fetch+blob / Tauri API) 표

### R3 회의 제목
1. 회의 상세 제목 `h2.scax-detail__title` 과 「제목 후보 …」 `span.t-meta` 를 그리는 파일:줄, 각각 어느 데이터 필드인가, 「제목 없는 회의」 대체 문구는 어디서 오나
2. 회의 제목을 바꾸는 화면 입구가 지금 있나(다른 화면 포함)
3. 앱에 **인라인 편집 부품**(클릭 → 입력 → blur 저장)이 이미 있나 — 있으면 쓰는 자리 전부, 없으면 가까운 것

### R4 업무 상세 모달 — 개편 근거 (가장 중요)
1. 업무 상세 모달(`section.scax-modal[aria-label="업무 상세"]` · `.scax-td`)의 구조를 **실제 코드 그대로** 1:1 로 적는다 — 헤더(머리글·제목·상태 칩·버전 배지·편집·AX·닫기), 메타 줄(담당·날짜·출처 배지·링크 — 어떤 줄이 어떤 조건에서), 본문 구역(업무 정보·진행과 판단·연관 업무·자료·이력 — 각 구역의 내용과 조건), 푸터. 컴포넌트·파일:줄·클래스·DS 부품
2. **「편집」 흐름** — 누르면 무엇이 바뀌나(편집 모드 상태·어느 필드가 입력으로 바뀌나·제목 입력이 잘려 보이는 원인·「업무 내용」 라벨이 두 번 나오는 원인), 저장/취소 단추 위치, 저장이 부르는 API·페이로드, 저장 뒤 갱신
3. **「담당자 변경」** — 「진행과 판단」 구역에서 누르면 무엇이 열리나, 부르는 API. 「진행과 판단」 구역에 담당자 변경 말고 **다른 것이 나오는 조건**이 있나(상태별·권한별)
4. **푸터 단추 매트릭스** — 상태 값 전부 × 권한(담당자·요청자·그 외) × 보이는 단추(업무 취소·시작·막힘·재개·완료 처리 등)와 각 핸들러·API·확인창 여부
5. **헤더 「AX」 단추**(「AX에게 이 업무 묻기」) — 핸들러가 무엇을 하나, 같은 기능의 다른 입구(목록 행·카드·AX 패널 등)가 있나 — 전부
6. 출처 배지 「AX 제안에서 생성됨」 과 옆 링크 — 어느 데이터로 그리고 링크가 어디로 가나. 출처 종류별 문구 전부
7. 이 업무 상세 컴포넌트를 **여는 자리 전부**(내 업무·프로젝트·캘린더·수신함·홈·AX 카드·회의 할 일 등) — 개편이 닿는 표면 수
8. 개편에 쓸 기존 부품 — 셀렉트/드롭다운 메뉴, 날짜 선택기(DateField 등), 사람 선택기, **토스트**(있나·어떻게 띄우나), 확인창(ConfirmDialog 등) — 파일:줄과 쓰는 자리 수. DS(`.design-sync/`)에 해당 부품 시안이 있나
9. 상태 칩·상태 표시 문구·색 정의(상태 값별) 파일:줄

### R5 선행업무 안내
1. 본문 위 `section.drawer-section.notice.danger`(「시작할 수 없습니다」)와 푸터 `small.scax-blocked-note` 를 그리는 파일:줄·노출 조건·데이터
2. 막힌 상태에서 「시작」·「완료 처리」를 누르면 지금 무엇이 일어나나(disabled? 서버 거부? 에러 표시 방식)
3. 같은 막힘 안내가 나오는 다른 화면 전부

### R6 업무 상세 헤더 여백
1. `header.scax-modal__head`(padding 20px 24px)와 `.scax-modal__body`·`.scax-td` 첫 요소(메타 줄)의 위쪽 간격을 만드는 CSS 규칙 전부(파일:줄·값) — 칩 줄 아래부터 「담당」 줄까지 px 합
2. `.scax-modal__head`/`.scax-modal__body` 를 쓰는 **다른 모달 전부**(개수·이름) — 공용 규칙을 바꾸면 닿는 범위

## 3. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/fe-survey-report.md` ← **이 파일 하나만 만든다**

코드 워크트리는 **읽기만** 한다. 커밋·push·PR 금지.

## 4. 하지 말 것

- 코드·테스트·CSS 를 고치지 마라. 테스트·빌드를 돌리지 마라
- **서버·프론트·Tauri 를 띄우지 마라. 사용자 포트와 프로세스를 건드리지 마라** (8001·5176·54329)
- 브라우저를 열지 마라. **운영 서버에 접속하지 마라**
- 「이렇게 바꾸자」를 쓰지 마라
- 리포트에 사람 실명·메일을 쓰지 마라(공개 레포로 아카이브된다) — 「팀원 A」처럼 쓴다

## 5. 리포트 형식

```
# 고도화 3차 조사 (frontend)

## 0. 한 줄 요약 — 요청별 한 줄 (원인이 보이면 원인 한 줄)
## 1~. 요청별 절 — §2 물음 번호대로 답
## N. grep 개수표 — 요청별로 센 심볼과 개수
## N+1. 조사 한계
```

**모든 답에 `파일:줄` 근거를 단다.** 근거 없는 문장은 쓰지 않는다.

## 6. 검증

- 리포트가 위 경로에 있다. §2 의 물음이 하나도 빠지지 않았다(못 답한 것은 조사 한계에)
- `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3 status --short` 가 비어 있다

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다. preamble 과 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: 3차 조사" \
  --body "리포트 경로 / 요청별 한 줄 요약 / 조사 한계"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 \
  --text "[worker_done] frontend 3차 조사 완료 — <한 줄 요약>. 리포트 fe-survey-report.md" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[질문] frontend: <질문>" --enter`
