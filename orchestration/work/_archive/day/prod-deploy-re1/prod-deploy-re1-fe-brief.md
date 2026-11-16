
# [frontend] 차트 모달(E55) · 담당자 셀렉터를 medikit 에 맞추기 (웹 W1 · W2)

너는 **day `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/roles/day/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ 이 워크트리에는 **커밋된 PR #244 브랜치**가 있다. 지금 다른 워커는 일하지 않는다. `deploy/` · `backend/day/register_connection.py` · `services/` 는 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- 사용자 피드백(정본): `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/e2e-feedback.md` **W1 · W2** + 그림 `e2e-shots/w01-web-chart-modal.png` · `w01c-web-chart-modal.png`(같은 폴더 — 실명 · 이메일 보임, 리포트에 옮기지 마라)
- 스펙(동작 정본 — 바꾸지 않는다): `/Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec/products/day/20-spec/spec-002-procedure-board.md` :164(E55 · 탭 · 표 「시술명 · 담당자 · 차트 내용」 · 자동 저장 · 「최근 저장 : HH:MM」) · :320 근처(담당자 드롭다운 규칙) · 규칙 31 · 32
- 레포 규칙: `AGENTS.md` :94 ~ :99 — 「스타일은 medikit 토큰 · `ui.html` 매크로의 클래스만」 · 빌드된 CSS 는 손으로 고치지 않는다(빌드로) · JS 는 `static/day.js` 하나 · 인라인 스크립트 금지
- medikit: `backend/day/static/medikit.css` · `medikit.js` · `backend/day/styles/`(medikit-preset · tailwind 설정 · build) · 컴포넌트 견본 `backend/day/templates/partials/kit_page.html` · `ui.html` 매크로. (AGENTS.md 가 가리키는 `docs/development/medikit-htmx-design-guide.md` 는 레포에 없다 — 견본 · 매크로 · CSS 가 기준)

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

사용자(2026-11-11): 차트 모달 「디자인이 너무 이상해」 · 「셀렉터는 우리 메디킷 셀렉터도 아니고」 · **「우리 디자인 메디킷에 맞게 하라고」 · 「프론트만 수정하면 된다」**. E55 는 시안이 없다(21-html · 21-screen 에 그림 없음) — 처음 구현이 medikit 컴포넌트를 쓰지 않고 손으로 짠 모양이다.

지금 보이는 어긋남(코디 관찰 — 그림 기준):
1. 담당자 = **브라우저 기본 `<select>`**(`partials/board_chart_parts.html:40`) — 열면 OS 목록. medikit 셀렉터가 아니다.
2. 한 행의 세 칸(시술명 글자 · 드롭다운 안 이름 · 차트 글 첫 줄)의 글자 줄이 안 맞는다 — 차트 칸 안쪽 여백이 커서 글이 아래에서 시작.
3. 일부 행만 드롭다운 아래 계정 이메일 회색 줄 → 행 높이 들쭉날쭉.
4. 드롭다운(낮음)과 차트 글 칸(한 줄 글에 큰 박스) 크기 · 테두리가 서로 다름.
5. 열 너비 — 시술명 열이 좁아 줄바꿈 · 담당자 열 넓음.
6. 표 머리 줄이 약해 표라기보다 폼처럼 보임.

## 3. 계약

해당 없음 — 서버 라우트 · 폼 필드 이름(`staffId` · 글 칸 이름) · HTMX 속성(자동 저장 · 409 `chart_conflict` 처리 · flash) · 권한(읽기 전용 `disabled`)은 **그대로**. 바뀌는 것은 마크업 · 클래스 · 셀렉터 컴포넌트뿐.

## 4. 먼저 읽을 핵심 파일

- `backend/day/templates/partials/board_chart.html` · `partials/board_chart_parts.html`(:30 · :40)
- `backend/day/templates/ui.html` :338 ~(`chart_modal` 매크로 · 다른 모달 · `popover` :108 · `menu_row` :111 · `tabs` :167)
- `backend/day/templates/partials/kit_page.html` · `kit_modal.html`(견본)
- `backend/day/static/day.js` — 차트 자동 저장 · 셀렉트 변경 처리
- 같은 화면의 다른 medikit 드롭다운이 이미 있으면(원장 고르기 · 방 옮기기 팝오버 등) 그 컴포넌트를 따른다
- 차트 관련 web 시험: `git grep -n -i chart backend/tests` 

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/day/templates/` (차트 모달 · 필요한 매크로 · 견본)
- `backend/day/static/day.js` · `backend/day/styles/`(소스) + 빌드 결과 CSS(빌드 명령으로만)
- `backend/tests/` 아래 차트 화면 시험

## 6. 구현 단계

1. 담당자 셀렉터를 **medikit 셀렉터 컴포넌트**로 바꾼다(키보드 · 접근성 · 읽기 전용 · 자동 저장 트리거 그대로). medikit 에 셀렉터가 없으면 같은 화면에서 쓰는 medikit 팝오버/메뉴 패턴으로 — 무엇을 썼는지 리포트에.
2. 표를 medikit 표/필드 토큰으로 정리: 세 칸 글자 줄 맞춤(위 정렬 기준 한 줄) · 입력 칸 높이 · 테두리 · 여백을 medikit 필드 크기로 통일 · 열 너비(시술명이 줄바꿈 덜 되게) · 머리 줄을 medikit 표 머리 모양으로.
3. 담당자 아래 이메일 줄: **왜 나오는지 코드에서 찾아 리포트**(이름 없는 계정 보조 표시인지 등). 글자 · 정보를 새로 지어 넣거나 지우는 판단은 하지 말고, medikit 필드의 보조 글 자리(행 높이를 흔들지 않는 방식)로 옮기는 것까지만. 판단이 필요하면 리포트 「정할 것」에.
4. 탭 · 「최근 저장 : HH:MM」 · 닫기 · flash 깜빡임 · 409 충돌 화면은 동작 그대로 · 모양만 medikit.
5. **화면 문구를 지어 넣지 마라** — 지금 글자 그대로.

## 7. 범위 제약 — 하지 말 것

- 서버 라우트 · 서비스 · 모델 · 스키마 변경 금지. 스펙 변경 금지.
- 사용자 포트 · 프로세스(로컬 11040 · `day-local`) 건드리지 마라. 화면 확인은 격리 스택이나 견본 페이지 렌더로.
- 실제 직원 이름 · 이메일을 시험 · 리포트 · 캡처 파일명에 넣지 마라.

## 8. 검증

```
uv run pytest -q <네가 만든 화면 테스트만>(TestClient 로 전체 페이지 · HX 조각 렌더 확인) — 1회. CSS 를 다시 빌드했다면 빌드 명령 1회. 인라인 스크립트 0 · 손 CSS 0(grep). 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

- 화면 확인: 바뀐 뒤 차트 모달 캡처 2장(간호관리 · 의사 탭 · 가짜 값) → `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/fe-captures/`
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/fe-1-report.md` (변경 파일:줄 · 쓴 medikit 컴포넌트 · 어긋남 1~6 각각 어떻게 · 이메일 줄 원인 · 시험 수치 · 정할 것)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_e62e850f-aae8-4092-a945-6f9406c2af07 --from term_79355e15-a622-4c93-8d81-eb35e37177fb \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
