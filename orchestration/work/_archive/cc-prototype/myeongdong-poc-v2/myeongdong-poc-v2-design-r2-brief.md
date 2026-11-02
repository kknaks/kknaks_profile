
# [frontend · 시안] 시술현황판 r2 — 배포된 현황판 코드에 맞춰 다시 그리기

너는 **cc-prototype `frontend` 워커**(시안 담당). claude design(DesignSync). **코드 수정 금지.**
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2` — 산출물 경로 말고 건드리지 마라.

## 0. 왜 다시 하나 — 먼저 읽어라

v1 시안을 사용자가 반려했다: **「완전히 다른 프로그램」** — 구조(사이드바 · 오른쪽 패널 없음) · 테마 · 글자 크기 · 카드 모양(색 띠)이 지금 배포된 현황판과 다르다. 원인은 v1 브리프가 기준을 claude design 옛 시안(v5)으로만 줬기 때문이다.

**이번 기준은 옛 시안이 아니라 배포된 코드다.** 시안의 모든 값(레이아웃 · 글자 크기 · 색 · 여백 · 테두리 · 배지 · 탭)은 아래 코드에서 읽은 값을 쓴다. 코드에 없는 값을 새로 만들지 마라.

## 1. SSOT

- **피드백(이번 수정 범위 전부)**: `orchestration/work/myeongdong-poc-v2/design-feedback-batch-1.md` #1 ~ #4
- **배포 코드 = 디자인 기준**: 코드 레포 `/Users/kknaks/git/toy_pr2/cc-prototype`, **`origin/main`(`339293e`)**. canonical 은 사용자 체크아웃이니 checkout · pull 하지 마라 — `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:<경로>` 로 읽는다
  - 레이아웃: `cc/front/app/(main)/layout.tsx`(있으면) · `cc/front/app/(main)/desk/page.tsx`
  - 헤더: `cc/front/components/common/AppHeader.tsx` · 왼쪽 사이드바(현황판 화면의 「현황판 · 실시간 현황판」 메뉴 — desk page 나 공통 컴포넌트에서 찾아라)
  - 가운데 칸 · 카드: `cc/front/components/desk/FloorGrid.tsx` · `RoomPanel.tsx`
  - 오른쪽 패널: `cc/front/components/desk/Aside.tsx`(`Tabs` · `StatusTab` 의 상태 수 카드 · 고객 카드)
  - 디자인 시스템: `@medisolve-ai/medikit` 클래스(`text-typo-*` · `text-ms-gray-*` 등) — 코드에 쓰인 클래스 그대로. 토큰은 `cc/design/_ds/medikit-*/` 참고
- 업무 흐름: `reference/2026-10-12-cc-prototype/workflow-v2.md` · v1 시안 리포트 `orchestration/work/myeongdong-poc-v2/design-report.md`(장면 · 정할 것은 그대로 이어 간다)
- 배포 화면 확인용(눈으로): `https://ccc.medisolveai.xyz` (로그인 화면이 나오면 거기까지만 — 사용자 계정으로 로그인하지 마라)

## 2. 만들 것

claude design `dda9a931` 에 **새 파일 `Ceramique 시술현황판 v2.dc.html`**. v1 파일은 지우지도 고치지도 않는다. 로컬 사본은 `orchestration/work/myeongdong-poc-v2/design-upload/`.

### 구조 — 현황판과 같은 3단(피드백 #1)

- **헤더** = `AppHeader` 그대로. 메뉴에 「시술 현황」 이 들어갈 자리는 코드의 메뉴 배열 방식대로(현재 선택 = 시술 현황)
- **왼쪽 사이드바** = 현황판 사이드바 그대로, 항목만 「시술 현황」
- **가운데** = 오더지 카드 나열(v1 내용 유지: 머리 · 오더 메모 접기/펴기 · 마취 · 시술 체크 목록 · [의사 호출] · [귀가 대기]) + 위에 제목 · [입실순 | 배치순] · 동기화 시각
- **오른쪽 패널** = `Aside` 그대로(고객 검색 · `Tabs` · 상태 수 카드 · 카드 목록). 탭은 **현황 · 원장 · 고객**(피드백 #4):
  - 현황(기본): 상태 수 카드 = 시술 대기 · 마취 중 · 호출함 · 시술 진행 · 귀가 대기(현황판의 대기 · 상담 · 시술 · 확인 필요 카드와 같은 모양) / 목록 = **손이 필요한 고객**(호출 미수락 경과 · 마취 길어짐 경과 · 시술 다 끝나 귀가 대기 필요). 누르면 가운데 그 카드 강조
  - 원장: 원장마다 지금 상태(대기 · 시술 중 · 어느 방)
  - 고객: 오늘 시술 고객 전체(검색)

### 카드(피드백 #2 · #3)

- **색 띠 없음.** 테두리 · 배경 · 여백 · 글자 크기 · 배지 = `FloorGrid` 방 칸 · `Aside` 고객 카드에서 읽은 값
- **컴팩트하게** — v1 보다 줄 간격 · 여백을 줄여 1280~1440px 가운데 영역에 카드가 v1 보다 많이 보이게. 시술 줄은 한 줄(이름 · 시간/상태 · 원장)로
- 상태 색은 현황판 범례 색(대기 · 상담 · 시술 · 확인 필요) 체계를 따른다 — 새 색 만들지 마라

### 장면

v1 과 같은 6개(`board` · `board-placement` · `memo-expanded` · `call-modal` · `call-modal-specific` · `all-done`) + 오른쪽 패널 탭 `panel-doctors` · `panel-customers`. 데이터 · 가짜 이름은 v1 그대로.

## 3. 하지 말 것

- 옛 시안(v5 등)의 값을 기준으로 쓰기 — **코드가 기준**
- 기존 시안 수정 · 삭제, 코드 수정, 커밋 · push · PR
- 태블릿 · 폰 화면 · 고객 모니터 · 시술 차트

## 4. 검증 · 리포트

- 리포트 `orchestration/work/myeongdong-poc-v2/design-r2-report.md`:
  - **코드 대조표** — 시안의 주요 값(헤더 높이 · 사이드바 폭 · 패널 폭 · 카드 테두리 · 반경 · 여백 · 제목/본문/캡션 글자 클래스 · 배지 · 탭)마다 「코드 파일:줄 → 시안 값」. 표에 못 채운 값은 「코드에 없음 — 가장 가까운 ○○ 사용」
  - 피드백 #1~#4 항목별 반영
  - v1 대비 카드 높이(대략) · 한 화면 카드 수
- `list_files` 45 → 46 · 다시 받아 `truncated:false` · node 로 장면 값 확인 · 사람 이름 0 grep

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "frontend 완료: 시술현황판 시안 r2" \
  --body "업로드 파일 / 코드 대조 요약 / 피드백 #1~4 반영 / 장면 / 정할 것 / 검증"

orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] frontend 시술현황판 시안 r2 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] frontend: <질문>" --enter`
