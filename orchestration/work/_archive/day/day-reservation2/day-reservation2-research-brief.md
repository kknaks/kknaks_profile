# [researcher · 읽기 전용] 예약 상세 모달 — 칸 · 버튼마다 원천 전수 표 + 시술현황 차트와 비교

너는 **day `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2` (코디와 같은 워크트리 — 리포트 파일 1개 말고는 아무것도 만들거나 고치지 마라)

**코드 · 문서 · DB 를 고치지 않는다. 결과는 리포트 하나.** 결정하지 말고 「정할 것」으로 모은다.

## 1. SSOT — 먼저 읽을 것

- 시안(생김새 · 문구 정본): `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-23-reservation/20261124_예약현황_시연.html`
  - 4MB 짜리 한 파일(이미지 · 글꼴이 base64). 읽기 쉬운 사본: `sed -E 's#data:[a-z/+.-]+;base64,[A-Za-z0-9+/=]+#DATA#g'` 로 빼서 봐라(사본은 `/private/tmp/` 아래 너만의 폴더에).
  - 모달 = `function detailV6Html(r)`(사본 약 2133줄) · 확인 창 `s5Pop` · 동작 `s5Act` · 우클릭 메뉴 `renderCtx`(약 2891줄) · 예약 등록 창 `openBook`(약 2386줄). 머리 주석 v9(11-24) 가 이번 판 변경.
  - 11-13판(앞 작업 정본)과의 차이를 볼 땐 같은 폴더 `20261113_예약현황_시연 (1).html`.
- 앞 작업 결정(동작 기준): `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-23-reservation/reservation-board-decisions.md` (R1 ~ R75 · 특히 R2 「상세 모달은 뺀다」 → 이번에 넣음 · R42 · R48 ~ R57 · R63 · R65 ~ R69)
- 스펙(mediness `origin/main`, `git -C /Users/kknaks/git/harness_works/mediness-mediness show origin/main:<path>`):
  - `products/day/20-spec/spec-006-reservation-board.md` (예약 현황)
  - `products/day/20-spec/spec-002-procedure-board.md` (시술 현황 · **차트 모달** 개정 ⑯)
  - `products/day/20-spec/spec-000-data-model.md` · `products/day/10-decision.md`
- 코드(CENTURION_DAY `origin/dev` `4bf0b4a1`, `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:<path>` 로만 읽어라 — canonical 체크아웃 · pull · checkout 금지):
  - 레포 루트 `AGENTS.md` 먼저
  - 시술현황 차트: `backend/day/routers/board.py`(GET `/board/visits/{id}/chart`) · `templates/partials/board_chart.html` · `board_chart_parts.html` · `board_chart_saved.html` · `board_action.html` 과 그 서비스 · 차트 JSON 을 만드는 곳
  - 예약 현황: `backend/day/routers/reservations.py` · `templates/partials/reservations_*.html` · 서비스
  - KOS 어댑터 `backend/day/emr/kos/` · 쓰기 큐 · 동기화 `services/emr_*`
- KOS 문서: `/Users/kknaks/git/ax-clinic-project` · 참고 구현 cc-prototype `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:<path>`(예약 상세 · 접수 · 수납 관련)

기대는 개념: 해당 없음.

## 2. 배경

DAY 예약 현황(웹)의 1차는 조회만 했고 카드 클릭 동작이 없다(R2). 이번 작업은 카드를 누르면 뜨는 **예약 상세 모달**(시안 v9 — 머리 = 단계 이름 · 단계 색, 왼쪽 고객 정보 · 예약 정보 · 상담 정보, 오른쪽 시술 목록 · 수납 정보, 재진이면 이전 방문 기록, 아래 단계별 버튼)을 만든다.
시술 현황판에는 이미 **시술현황 차트 모달**이 있다. 사용자는 「시술현황 차트 일부 기능 수정」이라고 했다 — 새 모달이 그 차트를 바탕으로 일부를 바꾸는 것인지, 따로 짓는 것인지를 판단할 재료가 필요하다.
범위(읽기만 / 버튼 쓰기까지)는 아직 안 정했다 — 이 조사 표를 보고 사용자가 정한다. 그래서 쓰기 동작도 다 조사한다.

## 3. 물음 (각 칸 · 버튼마다 「그대로 / 가공 / 없음」 + 근거 file:line 또는 git ref)

1. **칸 전수 표** — 시안 모달에 보이는 칸을 **시안 코드에서 전부 grep 해서** 센 뒤(목록을 내가 주지 않는다 — `kv(` · `fld(` · `<h4>` · `m6-` 클래스 · 단계별 분기 전부) 한 줄씩:
   칸 이름(시안 문구) · 보이는 단계 · DAY DB 원천(테이블.칼럼) · KOS 원천(API · 필드) · 지금 DAY 에 저장되나 · 시술현황 차트에 이미 있나(있으면 file:line) · 「그대로 / 가공 / 없음」
   - 특히: 신분확인 · 초진 문진 · 건강정보 · 특이사항 · 의사 지정 · 유입채널 · 희망 시술/예산 · 예약메모(덧붙이기 · 작성자 · 시각) · 담당자 · 상담사 · 관리실 · 시술권 · 오더 메모 · 시술 목록 「진행 / 미진행」 · 시술메모 · 귀가 사유 · 수납 정보 다섯 숫자(상품 합계 · 할인 · 총 수납 · 수납 완료 · 수납 필요 — R49 ~ R55 금액 기준과 같은지) · 이전 방문 기록 네 줄(예약 담당 · 상담 · 시술 · 받은 시술)
2. **버튼 · 동작 전수 표** — 시안의 `data-s5=` · `data-ctx=` · `data-s6-*` 전부 grep:
   동작 · 보이는 단계 · 바뀌는 것 · KOS 쓰기가 필요한가(어느 API) · DAY 에 이미 있는 경로(시술 현황 · 앱 · 쓰기 큐 · 라우터 file:line) · 없음
   - 시안의 「다른 화면에서 일어나는 일」 흉내 막대(`mimicBtns`)는 DAY 화면 동작이 아니다 — 표에서 따로 표시만.
3. **시술현황 차트와 비교** — 차트 모달의 구성(칸 · 버튼 · 권한 · 여는 경로 · JSON 모양)을 정리하고, 새 모달과 ⓐ 같은 것 ⓑ 차트에만 있는 것 ⓒ 새 모달에만 있는 것으로 나눠라. 차트 JSON · 조각(partial)을 새 모달이 재사용할 수 있는지 근거만(설계 결정은 하지 마라).
4. **단계 경계** — 시안은 단계(예약 · 접수 · 상담 대기 · 상담 진행 · 시술 대기 · 시술 진행 · 귀가 대기 · 귀가 · 예약 취소 · 노쇼)와 「오늘 / 지난 날 / 앞날」로 보이는 칸 · 버튼이 갈린다. 그 갈림을 시안 코드 그대로 표로(지어내지 말고 조건식 인용).
5. **이전 방문 기록** — 같은 고객의 지난 방문을 DAY DB 에서 읽을 수 있나(백필 범위 · 어디까지 과거가 있나 — customer-erd 백필 기준), 네 줄 각각의 원천.
6. **우클릭 메뉴(예약 변경 = 끌어 옮김 · 예약 취소 · 동행 추가)** — 예약 변경 · 취소의 KOS 쓰기 API 와 DAY 에 있는 경로. 동행 추가는 R65 ~ R69 가 이미 있으니 시안의 「동행 고르기」와 지금 구현(끌어 놓기)이 어떻게 다른지만.
7. **로컬 데모 DB 표본**(읽기 전용 SELECT 만 · 접속법은 레포 문서에서 찾고 못 찾으면 「확인 못 함」): 단계별 방문 하나씩 골라 1번 표의 칸이 실제로 채워지는지 — 방문 id 앞 8자 · 칸 채움 여부(값 대신 O / 빈칸)만.
8. **빠진 것** — DAY 에 없어 동기화 · 새 테이블 · 새 KOS 호출이 필요한 것 목록 + 어느 KOS API 로.

## 4. allowed_paths

- 리포트 1개만 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/research-detail-1-report.md`
- 시안 사본은 `/private/tmp/` 아래 너만의 폴더(워크트리 밖).

## 5. 하지 말 것

- 고치기 · 커밋 · push · PR 금지. git checkout · pull · worktree 만들기 금지(`git show origin/...` 로만 읽기).
- 로컬 스택 · docker · 포트 건드리지 마라. INSERT / UPDATE / DELETE 금지.
- 고객 이름 · 전화 · 메모 · 금액 원문을 리포트에 쓰지 마라. `*.env` 읽지도 출력하지도 마라. KOS 를 직접 호출하지 마라.
- 없는 값을 다른 필드로 추정해 채우지 마라. 모르면 「없음 / 확인 못 함」. 결정하지 말고 「정할 것」으로.
- 시안에 없는 화면 문구를 지어 쓰지 마라.

## 6. 리포트 모양

맨 위: 물음 1 ~ 8 답 한 줄씩 표 → 「정할 것」 목록(사용자에게 물을 것 · 각각 선택지와 근거) → 아래 근거 표(1 · 2 · 3 은 전수 표).

## 7. 검증

```
질문마다 답 + 근거(파일:줄 · git ref · 문서 URL). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다
```

- 1 · 2 번 표는 **grep 으로 센 수**를 표 머리에 적어라(시안에서 찾은 칸 n개 · 버튼 n개 = 표 행 수).

## 8. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --from term_ab4b9a17-9d28-489c-a70c-908b47c4cf7b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 예약 상세 모달 원천 조사" \
  --body "리포트 경로 / 칸 n · 버튼 n / 정할 것 n / 미결·주의점"

# (2) 직접 주입
orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 \
  --text "[worker_done] researcher 완료 — 예약 상세 모달 원천 조사. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 물어라:
  `orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --text "[질문] researcher: <질문>" --enter`
