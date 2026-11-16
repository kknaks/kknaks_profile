# WORK-005 WP-FE1 · WP-FE2 결과 보고 (frontend r1)

## 상태: done

- 워크트리 `cc-prototype/overall-board`(branch `kknaksss/overall-board`) · 커밋 · push 없음. 변경은 `procedure/front/` 만(같은 워크트리의 `procedure/back/` 변경은 backend 워커 몫 · 건드리지 않음)
- 계약 = SPEC-003 0.4.2 · WORK-005 「계약 고정점」 그대로(모양 바꾼 곳 없음)

## 수행 — 파일 · 화면

| 파일 | WP | 바뀐 것 |
|---|---|---|
| `components/common/AppHeader.tsx` | FE1 | 상단 메뉴 「현황」 하나 + 호버 드롭다운(최소 폭 180 · 반경 10 · 그림자 `0 8px 28px rgba(0,0,0,.12)` · 항목 높이 40 · 지금 항목 `body-600 text-primary bg-primary-100`) → 항목 「시술 현황」 하나 `/procedures/live`. 「현황」 글자 클릭 = 첫 항목. 오른쪽 시계 · 지점 · 계정(`name`) · 로그아웃 그대로 |
| `app/(main)/procedures/live/page.tsx` | FE1 · FE2 | medikit 사이드바 제거 · 제목 줄 「명동점 · 」 앞머리 제거 · [입실순 \| 배치순] 과 구분선 제거 · `sort` 상태 제거. 카드 순서 = 스냅샷 `cards[]` + 놓은 뒤 로컬 순서 · 드래그 상태 · `PUT` 경합 규칙(아래) · Aside 에 `ordered`(로컬 순서 반영 목록) 전달 |
| `components/procedures/Aside.tsx` | FE1 | 현황 탭 6칸 = 3 × 2 · 점 6px · 칸 바탕/테두리 없음 · 2 · 3번째 칸 왼쪽 1px `gray-300` · 고른 칸 `body-600 gray-800` / 나머지 `body-400 gray-500`(시안 M:945-955 · padding `14px 12px 10px` · row-gap 8). 고객 탭 줄 순서 = 카드 순서(`orderedCards(board.cards, sort)` 제거) |
| `components/procedures/view.ts` | FE1 · FE2 | `FILTERS` = 점 색(`dot`) · `SortKey` · `orderedCards` 제거 · 새 순수 함수 `withLocalOrder` · `liveIds` · `moveCard`(방향 따라) · `sameOrder`(§5.12 ② 비교) · `orderedProcs` = etc → 진행 → 대기 → 완료 · `cardLook` 에 끄는 중(0.35 · primary 2px 그림자) · `NeedView.label`(경과 글자) 제거 |
| `components/procedures/OrderCard.tsx` | FE2 | 머리 한 줄(방 + Badge / 입실) · 경과 글자 줄 · KOS 반영 줄 제거 · 완료 묶음 앞 점선 · 방 없는 `etc` 줄 맨 위 읽기 전용 그대로 · 드래그 props(`CardDrag`) — 귀가 대기 아닌 카드만 `draggable` · `cursor: grab` |
| `lib/api.ts` | FE2 | `request` 에 `PUT` · `putBoardOrder(visitIds)` |
| `lib/types.ts` | FE2 | `BoardOrderResult {ok, visitIds}` 만 더함(스냅샷 타입 그대로) |

`app/(main)/layout.tsx` 는 바꿀 것이 없었다(헤더 공유 그대로).

### 드래그 · 경합 구현 (SPEC-003 §5.12 · §6.3)

- 시작 때 `start` = 그때 화면의 귀가 대기 아닌 전체 순서(경합 중이면 로컬 순서 · 필터로 숨긴 카드 포함). 앞/뒤 판정은 늘 `start` 기준 — 미리보기로 바뀐 순서로 다시 판정하지 않음
- 미리보기 = `moveCard(start, from, over)` 를 **격자 `order` 로만** 그림(DOM 순서는 그대로)
- 놓기 → `reqNo` 증가 · 로컬 순서 → `PUT /api/board/order {visitIds: 전체}`. 마지막 요청만 봄(앞선 응답 · 실패 무시)
  - ① 응답 전: 스냅샷이 와도 순서는 로컬(`withLocalOrder` — 새 카드는 뒤 · 그사이 귀가 대기 카드는 귀가 대기 묶음 · 사라진 카드 빠짐)
  - ② 성공 뒤: `sameOrder(snapshot, visitIds)` 가 성립하는 첫 스냅샷에서 로컬 해제(응답 전에 이미 온 스냅샷도 바로 판정)
  - ③ 성공 뒤 3초 안에 없으면 해제 · ④ 실패(403 `fake_board` 포함)면 바로 해제 + 오류 토스트(back `message`) · 401 은 세션 지움
- 귀가 대기 카드: `draggable=false` · dragenter/dragover/drop 처리 없음 → 그 위에 놓으면 drop 이 안 오고 dragend 로 원래 순서
- 같은 순서(제자리 놓기)는 PUT 안 보냄

## 검증 — 명령과 결과

| 명령 | 결과 |
|---|---|
| `cd procedure/front && npx tsc --noEmit` | 통과(0) |
| `npm run lint` | 통과(0 경고) |
| `npm run build` | 통과 — 라우트 5(`/` · `/_not-found` · `/login` · `/procedures` · `/procedures/live`). ※ 아래 이슈 1 |
| FE1 grep `SortKey\|배치순\|입실순` (`.ts` · `.tsx` · app · components · lib) | **0** |
| FE1 grep `\bMenu\b` (app · components) | **0** |
| FE2 grep `KOS 반영` (components) | **0** |
| 기능 폴더 밖 import(`cc/` 등) | **0** |

### 완료 조건별

**WP-FE1**
- ① 헤더(드롭다운 펼침) 스크린샷 — `fe-shots/fe1-header-dropdown.png` · 드롭다운 항목 = 「시술 현황 → /procedures/live」 1개(자동 확인)
- ② `board` — `fe-shots/fe1-board.png` · 사이드바 0 · 정렬 버튼 0 · 「명동점 · 」 0(제목 줄) · 다른 상단 메뉴 0 · 예약/원내 현황 항목 0
- ③ `panel-customers` — `fe-shots/fe1-panel-customers.png`(고객 줄 5 = 카드 순서)
- ④ `narrow`(700px) — `fe-shots/fe1-narrow.png` · `aside` 0개
- ⑤ 현황 탭 3 × 2 — `fe-shots/fe1-status-3x2.png`
- reviewer 시안 대조(헤더 M:63-92 · 제목 줄 M:781-800 · 현황 탭 M:944-990) — **pending(reviewer 몫)**

**WP-FE2**
- ① 카드 `board` · `all-done` — `fe-shots/fe1-board.png` · `fe-shots/fe2-card-all-done.png`(A-룸4) · 점선/줄 순서 `fe-shots/fe2-card-doing-cut.png`(진행 → 대기 → 점선 → 완료) · 방 없는 `etc`(시트팩) 줄 `fe-shots/fe2-card-etc.png`
- ② 드래그 중 미리보기 — `fe-shots/fe2-drag-preview.png`(끄는 카드 0.35 + primary 2px · 101 을 아래 103 위로 → 103 **뒤**)
- ③ 놓은 직후 로컬 순서 — `fe-shots/fe2-dropped-local.png`(PUT 응답을 1.5초 늦춰 찍음: `102,103,101,104,105`)
- ④ 가짜 보드 403 → 토스트 「가짜 스냅샷(PROC_FAKE_BOARD) 중에는 조작할 수 없어요」 + 원래 순서 `101,102,103,104,105` — `fe-shots/fe2-after-403-toast.png`
- ⑤ 방향 따라(Playwright 로 PUT 본문 확인): 101→103 `[102,103,101,104]` · 101→102(바로 옆 · 아래) `[102,101,103,104]` · 102→103 `[101,103,102,104]` · 103→101(위) `[103,101,102,104]` · 102→101 `[102,101,103,104]` · 104→101 `[104,101,102,103]` · 귀가 대기 105 위에 놓기 = PUT 없음
- ⑥ 귀가 대기 카드 끌기 안 됨 — `draggable="false"`(105) · 「KOS 반영」 · 경과 글자 · 「방 배정」 줄 0 · 방 없는 `etc` 줄 남음 · `cc/` import 0
- reviewer 시안 대조(카드 M:808-905 · 드래그 표시 M:1464-1475) — **pending(reviewer 몫)**
- 놓은 뒤 유지 · 다른 화면 공유 — **pending(WP-E2E · 가짜 보드는 403 이 맞는 동작)**

스크린샷 환경: back = 지금 워크트리 `procedure/back`(`.venv/bin/uvicorn` · `PROC_FAKE_BOARD=1` · 임시 DB · 임시 계정 · **127.0.0.1:18711**) · front = `next start -p 13711`(빌드 인자 `NEXT_PUBLIC_API_BASE_URL=http://localhost:18711`) · Playwright(chromium, 스크래치 폴더에 설치 — 레포 의존성 아님). 끝난 뒤 두 프로세스 모두 내림(18711 · 13711 LISTEN 0 확인) · 임시 DB 삭제. 사용자 포트(3600 · 8600 · 3700 · 8700) 안 건드림.

## 계약 대조 — SPEC 항목별

| 항목 | 같음/다름 |
|---|---|
| §6.2 헤더(「현황」 하나 · 드롭다운 「시술 현황」 하나 · 치수 · 계정 `name`) | 같음 |
| §6.2 사이드바 없음 · 제목 줄(앞머리 없음 · 조회 시간 밖 · 동기화 실패 · 범례 5 · 정렬 버튼 없음) | 같음 |
| §6.3 정렬 = 스냅샷 `cards[]` 그대로(front 재정렬 없음) | 같음 |
| §6.3 머리 한 줄 · 경과 글자 · KOS 반영 줄 없음 · 고객 줄 | 같음 |
| §5.9 줄 순서 진행 → 대기 → 완료 + 점선 · `etc` 맨 위 | 같음 |
| §5.12 방향 따라(시작 순서 기준) · 귀가 대기 제외 · 전체 순서 PUT · 경합 ①~④ | 같음 |
| §6.3 불투명도 우선순위(0.35 → 0.55 → 0.45) · primary 2px 그림자 | 같음 |
| §6.4 현황 탭 3 × 2 · 고객 탭 순서 = 카드 순서(경합 중 로컬) | 같음 |
| §6.8 760 미만 = 카드만 | 같음(그대로) |
| §7.3 `PUT /api/board/order` 요청 · 응답 모양 | 같음 |

## 이슈 · 코디가 확인할 것

1. **Next.js 보안 알림** — `npm run build`(·`lint` 처음 한 번)가 「Your version of Next.js is affected by a known security vulnerability」 를 띄우고 **가끔 첫 빌드를 `SecurityFatalError` 로 멈춘다**(같은 명령을 다시 돌리면 통과). 출력에 `next upgrade --agent=security …` 실행 권유가 있었으나 범위 밖(의존성 변경)이라 **실행하지 않았다**. 배포 · compose 빌드에서도 같은 멈춤이 날 수 있으니 업그레이드 여부는 코디/사용자 결정
2. 드래그 구현 메모 — 미리보기로 옮겨 온 카드 위에서 `drop` 이 오려면 `dragenter` 도 `preventDefault` 해야 했다(처음엔 빠져 첫 카드를 아래로 끌면 drop 이 안 왔다 → 고쳐서 위 ⑤ 전부 통과). 미리보기는 DOM 이동 없이 격자 `order` 로만 그린다
3. `app/layout.tsx` 의 브라우저 탭 제목 「Céramique 명동점 · 시술 현황」은 제목 줄이 아니라 그대로 둠 — reviewer grep 이 이것을 「명동점 · 」 로 잡으면 범위 밖으로 처리 바람
4. 가짜 보드 스냅샷의 「방 배정」 → 「시트팩」 교체는 backend 워커 변경이 이미 반영된 상태로 찍혔다(스크린샷의 시트팩 줄)

---

# 추가 수정 — 작업 type 구분 없애기 (2026-10-25 · `no-kind-instructions.md` 「frontend」 절)

## 상태: done

## 수행
| 파일 | 바뀐 것 |
|---|---|
| `components/procedures/view.ts` | `isEtc` · `KOS_STATUS` · `etcStatus` 삭제. `orderedProcs` = 모든 작업을 진행 → 대기(sequence) → 완료(완료 시각) 한 줄로(etc 를 맨 위에 따로 빼던 것 제거) |
| `components/procedures/OrderCard.tsx` | 「읽기 전용 줄」(`data-etc` · 제목 + KOS 상태 글자) 분기 삭제 → ETCETERA 도 같은 시술 줄(체크 · [시작]/[종료] · 「호출함」 · 담당 글자). 선택 대상 `pickable` 에서 `!isEtc` 제거 · 점선 판정에서 etc 조건 제거 |
| `components/procedures/Aside.tsx` | 확인 필요 목록의 진행/담당 찾기 · 고객 탭 번호 원 시술 줄에서 `kind !== 'etc'` 거르기 제거 |
| `lib/types.ts` | `kind` · `kosStatus` 필드는 스냅샷 모양 유지로 남김(주석만 — 화면에서 쓰지 않음) |

- 버튼 · 체크 · 호출 가능 여부는 전처럼 back 값(`pickable` · `canStart` · `canFinish` · `canCall`)만 쓴다 → type 무관 여부는 back 규칙이 정한다
- 호출 팝오버 · 호출 탭은 원래 type 으로 거르지 않았다(back 의 `procedureIds` · `calls[].procedures` 그대로)

## 검증
- grep `isEtc|'etc'|etcStatus|KOS_STATUS|data-etc` (app · components · lib) = **0**(남은 것: `lib/types.ts` 의 `ProcKind` 타입 정의 1줄)
- `npx tsc --noEmit` 통과 · `npm run lint` 통과 · `npm run build` 통과(첫 실행 Next `SecurityFatalError` 로 멈춤 → 재실행 통과 — 앞 이슈 1 과 같음)
- 화면 스크린샷은 이번에 안 찍음(지시서에 없음 · 실제 확인은 코디 로컬 E2E)

---

# 재수정 — 규칙 하나로(2026-10-25 · `one-rule-instructions.md` 「frontend」 절 · `no-kind` 대체)

## 상태: done

- 지난 수정(기타 작업 = 일반 시술 줄)은 그대로 둠
- `lib/types.ts` — `Procedure.isRoomTask: boolean` 추가(back `schemas/board.py` 의 같은 이름 확인)
- `components/procedures/view.ts` — `procsOf(c)` = `c.procedures` 에서 `isRoomTask` 만 뺀 목록. **카드 작업 목록을 읽는 곳 전부를 이것으로 바꿈**(grep `\.procedures\b`):
  - `view.ts` `orderedProcs`(카드 시술 줄)
  - `OrderCard.tsx` 선택 대상 · 「N개 선택됨」 · [의사 호출 · N건] 개수
  - `live/page.tsx` 호출 열기 때 고른 id 거르기
  - `CallPopover.tsx` 「호출할 시술 · N개」 목록
  - `Aside.tsx` 확인 필요 목록(진행 · 담당 찾기) · 고객 탭 번호 원 시술 줄
- 남은 직접 사용 = `Aside.tsx` 호출 탭 `calls[].procedures`(back 이 호출된 시술만 실음 — 방 배정은 호출 대상이 아니라 들어오지 않음 · 필드에 `isRoomTask` 없음)
- 검증: `npx tsc --noEmit` 통과 · `npm run lint` 통과 · `npm run build` 통과(첫 실행 Next `SecurityFatalError` → 재실행 통과 — 기존 이슈) · 스크린샷 없음(지시서 범위 밖)

---

# 되돌리기 — WORK-006 WP-FE (2026-10-26 · `overall-board-fe-undo-brief.md` · SPEC-003 0.5.1)

## 상태: done

## 수행 — 파일
| 파일 | 바뀐 것 |
|---|---|
| `front/lib/types.ts` | `Procedure.canUndoStart?` · `canUndoFinish?: boolean`(없으면 false — back 반영 전 스냅샷 호환) |
| `front/lib/api.ts` | `undoStart(id)` → `POST /api/procedures/{id}/undo-start` `{ok, flowStepChanged}` · `undoFinish(id)` → `/undo-finish` `{ok}` · 본문 없음 |
| `front/components/procedures/UndoConfirm.tsx`(새) | medikit `ConfirmModal` — `title` 「시술 대기로 되돌리겠습니까?」/「시술 중으로 되돌리겠습니까?」 · `description` 「<방> · <시술 이름>」 · `variant="caution"` · `leftButton` 「취소」 · `rightButton` 「되돌리기」 · `onBackdropClick` = 닫기. 열 때 잡은 대상을 들고 있어 SSE 로 아이콘 조건이 꺼져도 모달 그대로(누르면 back 409) |
| `front/components/procedures/OrderCard.tsx` | 진행 줄 [종료] 왼쪽(`canUndoStart`) · 완료 줄 「완료」 왼쪽(`canUndoFinish`)에 아이콘 버튼 26 × 26 · 테두리 없음 · `text-ms-gray-500` → `hover:text-primary` · `aria-label="되돌리기"` · medikit `Tooltip`/`TooltipTrigger asChild`/`TooltipContent` 「되돌리기」. 조건은 스냅샷 `canUndo*` 만(front 계산 0) · 대기 줄은 그리는 분기 없음. `CardActions.onUndo` 추가 |
| `front/app/(main)/procedures/live/page.tsx` | `TooltipProvider` 하나(카드 목록을 감쌈) · [시작] · [종료] **성공 토스트 신설** 「<방> · <시술> 시작/종료」 + [되돌리기] · 되돌리기 토스트만 **5초**(`UNDO_TOAST_MS`) · 나머지 2.6초 그대로(`TOAST_MS`) · 새 토스트가 앞 토스트(와 [되돌리기])를 바꿈(기존 `n` 구조) · 토스트 [되돌리기] = 토스트 닫고 바로 API(모달 없음) · 모달 [되돌리기] = 모달 닫고 API · 성공 「… 시술 대기로 되돌림」/「… 시술 중으로 되돌림」(2.6초 · [되돌리기] 없음) · 실패 = back `message` 오류 토스트(기존 `run`) · 주석 「되돌리기 없음(D-28)」 고침 |
| `back/app/service/fake_board.py`(예시 값만 · r6 W2) | `proc()` 에 `canUndoStart = doing · 귀가 대기 아님` · `canUndoFinish = done · started 있음 · 귀가 대기 아님`(지어낸 값). 결과 true 줄: 1021(완료) · 1022(진행) · 1031 · 1032(완료) / 귀가 대기 카드 1041 = false |

## 검증
| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과 |
| `npm run lint` | 통과 |
| `npm run build` | 통과(라우트 5). 첫 실행이 Next 의 보안 업그레이드 권고 출력(`next upgrade --agent=security …`)으로 멈춤 → 재실행 통과 — 앞 판의 `SecurityFatalError` 와 같은 기존 이슈 · 업그레이드는 하지 않음(범위 밖 · 코디 판단) |
| `grep -rn "canUndoStart\|canUndoFinish" front/components front/app` | **2**(≥ 2) |
| `cc/` import | 0 |
| (back 파일 하나 건드려서) `uv run ruff check app/service/fake_board.py` · `uv run pytest -q -k fake` | 통과 · 4 passed |

### 가짜 보드 스크린샷 — `fe-shots/undo-*.png`
환경: back = 워크트리 `procedure/back` `.venv/bin/uvicorn app.main:create_app --factory` · `PROC_FAKE_BOARD=1` · 임시 DB · 임시 계정 · **127.0.0.1:18712** / front = `next start -p 13712`(빌드 인자 `NEXT_PUBLIC_API_BASE_URL=http://localhost:18712`) / Playwright 1.56(스크래치 폴더 · 레포 의존성 아님). 끝난 뒤 두 포트 LISTEN 0 · 임시 DB 삭제 · `.next` 는 기본 env 로 다시 빌드. 사용자 3700 · 8700(docker) 안 건드림. ※ back 설정이 `procedure/.env` 를 읽어 띄운 동안 데모 KOS 를 **읽기만** 함(임시 DB 라 보낼 op 0).

| 파일 | 확인 |
|---|---|
| `undo-board.png` | 전체 판 — 아이콘 수: 카드 101 · 102(대기만) **0** · 103 **2** · 104 **2** · 105(귀가 대기) **0** |
| `undo-card-doing-done.png` | 진행 줄 [종료] 왼쪽 아이콘 · 완료 줄 「완료」 왼쪽 아이콘 · 대기 줄(LDM) 아이콘 없음 |
| `undo-card-all-done.png` · `undo-card-home-none.png` | 완료 두 줄 아이콘 / 귀가 대기 카드 아이콘 없음 |
| `undo-tooltip.png` | 호버 툴팁 「되돌리기」(`role=tooltip` 글자 확인) · 호버 색 primary |
| `undo-modal-start.png` · `undo-modal-finish.png` | 「시술 대기로 되돌리겠습니까? · A-룸3 · 필러 코」 / 「시술 중으로 되돌리겠습니까? · A-룸3 · 보톡스 사각턱」 · caution(앰버 !) · 취소 · 되돌리기. 바깥 클릭 · [취소] = 닫힘 · POST 0 |
| `undo-after-403-toast.png` | 모달 [되돌리기] → 모달 닫힘 · `POST /api/procedures/1021/undo-finish` → 403 → 토스트 「가짜 스냅샷(PROC_FAKE_BOARD) 중에는 조작할 수 없어요」 |
| `undo-finish-403-toast.png` | [종료] 실패 토스트 — 오류 문구만 · [되돌리기] 없음 |
| `undo-toast-mocked-success.png` | **(가로챔 — 참고용)** Playwright 가 `/finish` 응답만 200 으로 바꿔 성공 토스트 모양 확인: 「A-룸3 · 필러 코 종료  되돌리기」 · 살아 있는 시간 ≈ 5.0초(측정 4986ms) |
| `undo-toast-undo-403.png` | (가로챔 상태) 토스트 [되돌리기] → 모달 없이 바로 `POST …/1022/undo-finish` → 403 오류 토스트 |

실제 성공 토스트 · 실제 되돌림은 WP-E2E(데모 지점)에서.

## 계약 대조
| SPEC | 같음/다름 |
|---|---|
| §5.13 들어가는 곳 ① 토스트(모달 없음) · ② 아이콘 → 툴팁 → 확인 모달 | 같음 |
| §5.13 토스트 5초 · 다른 토스트 2.6초 · 새 토스트가 앞 토스트 대체 | 같음 |
| §5.9 · §6.3 아이콘 위치(진행 [종료] 왼쪽 · 완료 「완료」 왼쪽 · 대기 없음) · 26 × 26 · 테두리 없음 · `gray-500` → 호버 primary · `aria-label` | 같음 |
| §7.2 아이콘 = `canUndo*` 만(front 재계산 0) | 같음 |
| §7.3 경로 둘 · 본문 없음 · 실패 = back `message` 토스트 | 같음 |
| §6.3 모달 `caution` · 제목 두 문구 · 설명 「<방> · <시술>」 · 취소/되돌리기 · 바깥 = 닫힘 · API 실패면 모달 닫고 오류 토스트 | 같음(모달은 API 전에 닫는다) |
| §6.3 성공 토스트 문구 「<방> · <시술> 시작/종료」 · 되돌림 문구 | 같음 |
| §6.3 `ResetIcon` `size="sm"` | **다름(작게)** — 아래 1 |
| §6.3 토스트 [되돌리기] 색 토큰 | FE 선택 — 아래 2 |

## 이슈 · 코디가 확인할 것
1. **`ResetIcon` 모양** — medikit 1.4.0 `ResetIcon` 은 원 호 + 오른쪽 위 화살촉의 **시계 방향 새로고침** 화살표다(되돌리기 = 반시계와 반대). 인라인 SVG 로 바꾸지 않고 **medikit `ResetIcon` sm 을 좌우로 뒤집어(`scaleX(-1)`) 반시계 되돌리기 화살표**로 그렸다(`undo-tooltip.png`). 뒤집지 않은 원래 방향을 원하면 `OrderCard.tsx` `UndoIcon` 의 `transform` 한 줄만 빼면 된다.
2. **토스트 [되돌리기] 색** = `text-primary-300`(`--ms-primary-300`) + `text-typo-body-600` · 글자와 간격 16(기존 토스트 `gap`). 진한 토스트(`bg-ms-gray-800`) 위에서 측정 색 `rgb(211, 244, 254)` — 밝은 primary 계열.
3. medikit `ConfirmModal` 의 오른쪽 버튼 색은 `variant` 로 정해진다(`warning` 만 red · 그 밖 blue) — `caution` 이라 blue(이 테마에서 연한 파랑 채움). medikit 기본 그대로 둠(`undo-modal-*.png`).
4. 아이콘 색 측정: 평소 `rgb(207, 207, 207)`(이 테마의 `ms-gray-500`) · 호버 `rgb(36, 152, 189)`(primary).
5. back 은 같은 워크트리에서 backend 워커가 동시에 고치는 중 — 내가 건드린 back 파일은 `service/fake_board.py` 하나. 스키마 두 필드(`schemas/board.py`)는 backend 쪽 변경이 이미 있어 그 위에서 찍었다.

## 되돌리기 — 수정 r2 (review-code-r2 F1 · 2026-10-26)

### 상태: done
- 원인(리뷰 그대로): `medikit-patches.css` [Button-1] `flex-shrink:0` + `ConfirmModal` 두 버튼 `w-full` → 444 + 16 + 444 px 로 넘침. 처음 보고 때 `undo-modal-*.png` 에 넘친 모습이 찍혀 있었는데 「같음」으로 적었다 — 놓친 것
- 수정(국소 · 권장안): `components/procedures/UndoConfirm.tsx` — `leftButton` · `rightButton` 에 `style: SHRINK`(`{ flexShrink: 1, minWidth: 0 }` · 인라인이라 전역 보정을 이김). 전역 css(`app/styles/medikit-patches.css`) 변경 0
- 다시 찍음: `fe-shots/undo-modal-start.png` · `undo-modal-finish.png` — 모달 상자 x 552 ~ 1048 · [취소] x 578 ~ 793(215px) · [되돌리기] x 809 ~ 1022(213px) → 두 버튼 모두 모달 안(목표 각 ~214px). 문구 그대로(「시술 대기로/시술 중으로 되돌리겠습니까?」 · 「A-룸3 · 필러 코」/「A-룸3 · 보톡스 사각턱」)
- 환경: 앞과 같음(가짜 보드 임시 포트 18712 · 13712 → 내림 · LISTEN 0 · 임시 DB 삭제 · `.next` 기본 env 로 다시 빌드 · 사용자 3700 · 8700 안 건드림)
- 검증: `npx tsc --noEmit` 통과 · `npm run lint` 통과 · `npm run build` 통과
