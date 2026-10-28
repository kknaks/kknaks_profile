# 리뷰 리포트 — overall-board 시술 현황 / code r3 · WORK-008 (2026-10-27)

대상: `kknaksss/overall-board-2` · `901267f` 이후 커밋 안 된 변경 5파일(+111 −65) · 기준 SPEC-003 0.6.0(r7 · r8) §5.12 · §5.14 · §6.3 · §9 #27~#32 · 부록 K

## 판정: PASS (FAIL 0 · WARN 2)

## 직접 돌린 수치 (임시 포트 없이 · 파일 수정 없음)
- `cd procedure/back && uv run pytest -q` → **361 passed**, 1 warning (18.7s)
- `cd procedure/front && npx tsc --noEmit` → 0 오류 · `npm run lint` → 0 오류 · 0 경고

## 항목별
| # | 볼 것 | 결과 |
|---|---|---|
| 1 | §5.14 ● #1 카드 머리 Badge | PASS — `OrderCard.tsx:53-78` `stateBadge` (sm · 점 없음 · `phaseStyle` chip className = ResvAside 꼴) · 덮어쓰기(확인 필요 danger · 마취 중 purple)는 sm dot 그대로(○ #2) |
| | ● #3 범례 | PASS — `view.ts` `LEGEND` 차례 시술·대기 → 마취 중 → 시술·진행 → 확인 필요 → 귀가·대기 · 상태 3 점 없음 · 알림 2 dot · `live/page.tsx:244` |
| | ● #4 현황 탭 대기 점 | PASS — `phaseStyle('procedure','waiting').dot`(= `bg-ms-white border-primary`) + `Aside.tsx:188-191` 테두리 2px · 이름 · 수 · 나머지 점 그대로 |
| | ● #5 · #6 고객 탭 Badge · 검색 결과 글자 | PASS — `Aside.tsx:484-486` · `:118` `stateText` 「<방> · 시술 · 대기」 |
| | ● #7 시술 줄 칩 | PASS — `SubChip`(11/16/600/0 5px/4 · nowrap) · 차례 호출함 → 칩 → 아이콘 → 버튼 · 완료 = 아이콘 → 회색 칩 · 진행 줄 바탕 무변경 |
| | ● #14 번호 원 줄 글자 | PASS — `procSubName` 「진행 중」→「진행」 · 번호 원(`now`/`past`) 무변경 |
| | ○ #8~#13 | PASS — `needView` · 원장 상태 · 되돌리기 문구 · 빈 상태 · 흐림 diff 없음. grep `STATE_BADGE\|STATE_NAME\|bg-yellow\|'warning'\|진행 중`(procedures 코드) = 0 (「수납 필요」 JSX `variant="warning"` 만) |
| | 색 = 예약 현황 재사용 · 예약 현황 무변경 | PASS — `view.ts:5` `MAIN_NAME · SUB_NAME · phaseStyle` import(값 복사 없음) · `git diff -- front/components/reservations` = 0줄. 값 대조: home·대기 chip = `bg-ms-gray-200 text-ms-gray-700` · 완료 = `bg-ms-gray-100 text-ms-gray-500` = §5.14 표와 같음 |
| 2 | W2 판 어디든 놓기 | PASS — `live/page.tsx:186-201` 흰 판(스크롤 컨테이너 · padding 12 포함)에 `onDragEnter/Over/Drop` · `drag` 있을 때만 preventDefault(파일 끌기 무시) · 카드 drop 은 버블로 판 한 곳에서 1번 저장 · `over==null` 또는 시작 순서와 같으면 저장 없음 |
| | 판 밖 · Esc | PASS — drop 안 옴 → `onEnd` `setDrag(null)` = 원래 순서 · 저장 0 |
| | 귀가 대기 카드 | PASS — handler 없음 → 미리보기 안 바뀜 · 그 위 drop 은 판으로 올라가 마지막 미리보기 저장(§5.12 ②) |
| | 필터 중 · 경합 SSE | PASS(회귀 없음) — `start = liveIds(ordered)` 전체 순서 · `saveOrder` · `withLocalOrder` 무변경 |
| 3 | 발음 | PASS — `OrderCard.tsx:93-102` 빈 값/공백 = 요소 없음 · 한 줄 `…` · `title` 전체 · 이름 `0 1 auto` / 발음 `0 3 auto`(발음 먼저) · 칩 `flexShrink 0` · 글자 `caption-md-400 gray-500`. W5 오른쪽 칸 `nowrap` (`:255`) |
| 4 | `fake_board.py` | PASS — 1줄(카드 103 고객 이름 · 발음 · 국적 `TW` 예시 값 · 지어낸 이름) · 카드 수 5 그대로 · back 다른 파일 diff 0 |
| 5 | 시술 현황 회귀 · DS · 누출 | PASS — 되돌리기(`canUndo*`) · 호출함 · 체크 · 시작/종료 조건 무변경(자리만 칩 추가) · medikit `Badge`/`Button` 만 · 새 env · 주소 · public 파일 0 |

## FAIL
없음.

## WARN
- **W1 「제자리로 돌아옴」** — `live/page.tsx:178` `onOver` 가 끄는 카드 자신을 무시해, 한 번 다른 카드 위로 간 뒤 자기 자리로 돌아와도 미리보기가 마지막 대상 그대로 → 놓으면 그 순서로 저장된다. §5.12 ① 「제자리로 돌아옴 = 저장 없음」을 「미리보기가 시작 순서와 같을 때」로만 읽으면 맞고, 「자기 카드 위로 돌아오면 원래 자리」로 읽으면 다르다(워커 보고 이슈 1과 같음). 사용자가 E2E #27~#29 에서 원하는 쪽을 정하면 됨 — E2E 막지 않음. 고칠 사람(정하면): FE
- **W2 주석 어긋남** — `live/page.tsx:173` 「귀가 대기 = 끌기 · 놓기 모두 없음」: 이제 귀가 대기 카드 위 drop 도 판이 받아 저장한다. 동작은 SPEC 대로 · 주석만 낡음. FE

## 고객이 실물에서 만날 자리
- 드래그 중 판 밖으로 나가 있는 동안 미리보기가 그대로 보이다가 놓는 순간 원래 순서로 돌아감(SPEC 이 끄는 중 표시를 정하지 않음 · 워커 이슈 2)
- 실제 데모 카드 2장이라 §9 #29 「3장 이상 · 다른 브라우저 · 새로고침」은 사용자 E2E 몫
- 진행 줄: primary-100 바탕 위 진한 「진행」 칩 + [종료] 버튼 — 오른쪽 칸 nowrap 이라 좁은 카드(300)에서 호출함 · 아이콘까지 겹치면 이름 칸이 더 좁아짐(워커 측정 최대 26px 한 줄)

## 참고(기존 부채)
- procedures → `components/reservations/view` import 로 두 화면 값이 묶임 — §5.14 「같은 값」 결정이라 의도대로. 예약 현황 값을 바꾸면 시술 현황도 같이 바뀐다
- front 자동 시험 없음(review-code-r1 W3) — 드래그 · 2계층 · 발음은 E2E + 스크린샷으로만 확인
