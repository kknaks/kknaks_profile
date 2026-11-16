# WORK-008 WP-FE1 · FE2 · FE3 결과 보고 (+ 추가 지시 1 · review-doc r5)

## 상태: done (커밋 · push 없음 — 워크트리 변경만)

branch `kknaksss/overall-board-2` (base `901267f`)

## 수행 — 바뀐 파일

| 파일 | 내용 |
|---|---|
| `procedure/front/components/procedures/view.ts` | `STATE_NAME` · `STATE_BADGE` 삭제 → `stateText` · `stateBadge` · `procChip` · `procSubName`(2계층). 이름 · 색 = `components/reservations/view.tsx` 의 `MAIN_NAME` · `SUB_NAME` · `phaseStyle` 를 **import 해서 그대로 씀**(복사 없음 · 예약 현황 파일 무변경). `LEGEND` 5개 새 꼴 · `FILTERS` 대기 점 = `phaseStyle('procedure','waiting').dot` + `ring` |
| `procedure/front/components/procedures/OrderCard.tsx` | 머리 Badge 2계층(덮어쓰기 확인 필요 · 마취 중은 sm dot 그대로) · 시술 줄 부상태 칩 `SubChip`(ScheduleTable 칩 꼴 11/16/600/0 5px/4) · 오른쪽 칸 한 줄(`nowrap`) · 카드 `onDrop` 제거(판이 받음) · 한글 발음 span |
| `procedure/front/components/procedures/Aside.tsx` | 고객 탭 Badge · 검색 결과 글자 · 번호 원 줄 글자(「진행 중」→「진행」) · 현황 탭 대기 점 ○ |
| `procedure/front/app/(main)/procedures/live/page.tsx` | 범례 Badge(`dot` · `className`) · 흰 판(스크롤 컨테이너)에 `onDragEnter` · `onDragOver` · `onDrop` — 저장 함수 한 곳 |
| `procedure/back/app/service/fake_board.py` | (추가 지시 1 W2 · 예시 값만) 카드 103 고객 = `(TW) CHEN WANLING ALEXANDRA` / 발음 `첸 완링 알렉산드라 테스트 발음`(지어낸 값). 카드 수 5 그대로 |

예약 현황(`components/reservations/**`) diff = 0줄.

## §5.14 대조표 ● 줄 처리

| # | 자리 | 처리 |
|---|---|---|
| 1 | 카드 머리 Badge | `stateBadge` — 「시술 · 대기」 primary-100/primary · 「시술 · 진행」 primary/white · 「귀가 · 대기」 gray-200/gray-700 · 점 없음 · Badge sm + `phaseStyle` chip className(ResvAside 꼴). 덮어쓰기는 sm dot 그대로(○ #2) |
| 3 | 범례 | 시술 · 대기 → 마취 중(purple dot) → 시술 · 진행 → 확인 필요(danger dot) → 귀가 · 대기 |
| 4 | 현황 탭 대기 점 | 흰 속 + `border-primary` 2px(○) · 나머지 그대로 · 칸 이름 · 수 · 정의 그대로 |
| 5 | 고객 탭 줄 Badge | #1 과 같은 꼴(덮어쓰기 없음) |
| 6 | 검색 결과 둘째 줄 | 「<방> · 시술 · 대기」 |
| 7 | 시술 줄 오른쪽 | 대기 · 진행 · 완료 칩. 차례 = 호출함 → 칩 → 되돌리기 아이콘 → 버튼 · 완료 줄은 아이콘 → 칩(맨 오른쪽). 귀가 대기 카드의 대기 · 진행 줄도 칩 보임. 진행 줄 바탕 그대로 |
| 14 | 고객 탭 번호 원 줄 글자 | 「진행 중」 → 「진행」(`procSubName`) · 번호 원 그대로 |

○ 줄(#2 · #8 ~ #13) 손대지 않음. grep `STATE_BADGE|STATE_NAME|'warning'|bg-yellow` (procedures 범위) = **0**(「수납 필요」는 JSX `variant="warning"` 로 남음). 목록 밖 사용처 없음.

## FE2 드래그 놓기 (W2 · 추가 지시 W1)

- 받는 곳 = 가운데 **흰 판(스크롤 컨테이너) 전체**(가장자리 12px 포함). 우리 카드를 끄는 중일 때만 `preventDefault`(파일 끌기 등 무시)
- 카드 위 drop 은 판으로 올라와 **한 곳에서 한 번** 저장. 카드는 `dragover` 로 미리보기 대상만 알림(귀가 대기 카드는 handler 없음 → 미리보기 유지)
- 저장 = `moveCard(start, from, over)` · `over` 없음 또는 시작 순서와 같으면 저장 없음. 판 밖 · Esc = drop 없음 → `onEnd` 원래 순서. 경합 로직(`saveOrder` · `withLocalOrder` · `sameOrder`)은 무변경

PUT 수(Playwright 마우스 드래그 · 네트워크 이벤트로 셈):

| 장면 | 가짜 보드(403 기대) | 실제 back(데모 · 임시 포트 8791 · 임시 DB) |
|---|---|---|
| 첫 카드 → 둘째 위(미리보기) → 틈에 놓기 | 1 (403 → 원래 순서 · 토스트) | 1 (200 · SSE 뒤에도 새 순서 유지) |
| 판 아래 빈 공간 | 1 | 1 (200) |
| 흰 판 가장자리(12px 안) | 1 | 1 (200) |
| 귀가 대기 카드 위에 놓기 | 1 (미리보기 그대로 확정) | — (데모에 귀가 대기 카드 없음) |
| 오른쪽 패널 | 0 · 원래 순서 | 0 · 원래 순서 |
| 헤더 | 0 · 원래 순서 | 0 · 원래 순서 |
| Esc | 0 · 원래 순서 | 0 · 원래 순서 |
| 미리보기 없이 틈에 놓기 | 0 | 0 |

실제 데모 카드는 2장뿐이라 §9 #29 의 「3장 이상」 · 「다른 브라우저」 · 「새로고침」은 E2E 몫으로 남김. KOS 쓰기 0(순서 = 임시 ccc DB 만 · 끝나고 삭제).

## FE3 한글 발음

이름 바로 오른쪽 · `text-typo-caption-md-400 text-ms-gray-500` · `flex: 0 3 auto` (이름 `0 1 auto`) · 둘 다 `minWidth 0` · 한 줄 `…` · `title` 전체 · 값이 null/공백이면 요소 없음. 카드 폭 300 측정: 긴 이름 span 144px · 발음 33px(둘 다 잘림 · 발음이 먼저 줄어듦) · 국적 · 첫내원 칩 안 줄어듦. 오른쪽 칸 높이 최대 26px(한 줄 · W5).

## 검증

- `cd procedure/front && npx tsc --noEmit && npm run lint` — 통과(0 오류 · 0 경고)
- `cd procedure/back && uv run pytest -q` — **361 passed**, 1 warning(fake_board.py 고친 뒤)
- build 는 코디 몫(돌리지 않음)
- 예약 현황 무변경: `git diff -- components/reservations` 0줄 + 스크린샷 `v2-resv-unchanged.png`
- 임시 포트 3791 · 8791만 사용 · 끝나고 내림. 사용자 3700 · 8700(docker) 그대로

## 스크린샷 (`fe-shots/`)

가짜 보드: `v2-fe1-board.png` · `v2-fe1-legend.png` · `v2-fe1-card-101~105.png`(대기 · 마취 덮어쓰기 · 진행 · 확인 필요 덮어쓰기 · 귀가 대기) · `v2-fe1-proc-rows-300.png` · `v2-fe1-aside-status.png`(대기 ○) · `v2-fe1-aside-customers.png` · `v2-fe1-search.png` · `v2-fe2-gap-before.png` / `-after.png`(403 → 원래 순서) · `v2-fe3-phonetic-yes-300.png` · `v2-fe3-phonetic-none-300.png` · `v2-fe3-long-300.png` · `v2-resv-unchanged.png`
실제 back: `v2-fe2-real-gap-before-2.png` / `-after-2.png` — 고객 이름 · 패널 글자는 blur(실명 노출 없음)

## 이슈 · 코디가 확인할 것

1. ~~「제자리로 돌아옴」 미리보기 유지~~ → 리뷰 W1 로 고침(아래 절)
2. 판 밖으로 끄는 동안(놓기 전) 미리보기는 유지되고, 놓을 때 원래 순서로 돌아감 — SPEC 이 끄는 중 표시는 정하지 않음
3. `next dev` 로그에 Next 보안 업그레이드 권고 문구가 찍힘(도구 출력 — 이 판에서 실행하지 않음 · 참고만)

## 리뷰 W1 · W2 (review-code-r3 · 코디 지시)

- **W1 — 원래 자리로 돌아오면 미리보기 지움**: 「자기 카드 위」를 **끄는 카드의 원래 칸**(드래그 시작 때 카드 사각형 · 판 내용 좌표라 스크롤과 무관)으로 판정. 판 `dragover`(`allowDrop`)에서 포인터가 그 칸 안이면 `over = null` → 원래 순서 · 그 자리에서 놓으면 저장 없음
  - 왜 「자기 카드 위 dragover」가 아닌가: 미리보기가 생기면 끄는 카드가 대상 칸으로 옮겨 그려져 포인터 바로 밑에 온다 → 자기 카드 위에서 지우면 대상 ↔ 자기 카드가 번갈아 깜빡인다. 또 옆 카드와 바꾼 경우 원래 칸에는 대상 카드가 와 있어 「자기 카드」로 돌아갈 수가 없다. 원래 칸 좌표 판정은 둘 다 없다(지운 뒤엔 끄는 카드가 그 칸에 돌아와 안정)
  - 확인(가짜 보드 · 임시 포트 · Playwright): 101 → 102 위(미리보기 102,101,…) → 원래 칸으로 → 101,102,… · 더 움직여도 그대로 · 놓기 PUT **0** / 101 → 103 위(102,103,101,…) → 원래 칸 → 원래 순서 · PUT **0** / 회귀: 틈에 놓기 PUT **1**
- **W2 — 낡은 주석**: `live/page.tsx` 귀가 대기 줄 주석 → 「끌 수 없고 미리보기 대상도 아님. 그 위 drop 은 판이 받는다(마지막 미리보기 자리)」
- 바뀐 파일: `procedure/front/app/(main)/procedures/live/page.tsx` 만(`boardRef` · `Drag.home` · `inBoard` · `allowDrop`)
- 검증: `npx tsc --noEmit` · `npm run lint` 통과
- 작업 중 실수 한 번: `OrderCard.tsx` 를 `git checkout` 으로 잘못 되돌렸다가 앞 판 편집(FE1 · FE2 · FE3 · W5)을 같은 내용으로 다시 적용 — diff 가 앞 보고와 같음(79줄 · +44/−35) · tsc · lint 통과로 확인
