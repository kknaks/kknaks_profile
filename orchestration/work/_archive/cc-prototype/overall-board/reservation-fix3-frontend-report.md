# WORK-007 WP-FIX3 frontend 결과 보고 (b4 #1 카드 드래그 · 공지 [수정하기] · 추가 지시 1)

## 상태: done (front) — 코디 데모 E2E(§9 #11 · #46 실 KOS)는 남음

base = `kknaksss/overall-board-2`(main `64e1989`) · 커밋 · push 안 함 · back 파일은 손대지 않음(backend 워커가 같은 워크트리에서 작업 중)

## 수행 — 바뀐 파일

| 파일 | 내용 |
|---|---|
| `procedure/front/components/reservations/ScheduleTable.tsx` | 드래그 고침 — 끄는 원본 카드는 제자리에 그대로(흐리게 0.4) · 놓을 칸 미리보기는 따로 그리는 복제 카드(`preview` · 누를 수 없음) · dragstart 안의 상태 바꿈을 다음 틱(`setTimeout 0`)으로 · 칸 폭 계산에 미리보기 1장 더함 |
| `procedure/front/components/reservations/ResvAside.tsx` | 공지 = 그 날 첫 공지 **하나** · 머리 오른쪽 [수정하기](`noticeEditable` 일 때만) → 누를 때 `GET board` 1번 다시 읽고 제자리 편집(medikit `Textarea`) · [취소](호출 없음) · 「저장」(medikit `Button`) · 글자 수 `n / 2,000`(**trim 길이** · 넘으면 빨강 + [저장] 끔) · 성공 = 토스트 「공지를 저장했어요」 + 읽기 상태(응답 공지를 다음 표 응답까지 보임) · 실패 = back `message` 토스트 + 편집 그대로 |
| `procedure/front/app/(main)/reservations/live/page.tsx` | 공지 편집 글자를 페이지가 든다(탭을 옮겨도 남음) · **편집 중 날짜 이동**(‹ › · [오늘] · 달력) = 막지 않고 버림 + 토스트 「저장하지 않은 공지 편집을 취소했어요」(추가 지시 1) · ResvAside 에 토스트 · 오류 · `refreshSoon` 연결 |
| `procedure/front/lib/api.ts` | `saveNotice(date, noticeId, content)` → `PUT /api/reservations/notice`(§7.5) |
| `procedure/front/lib/types.ts` | `ResvBoard.noticeEditable: boolean` |

## b4 #1 「카드가 안 잡혀」 — 원인

끌기가 시작되면(dragstart → 첫 dragover) 화면이 **끄는 카드 자체(드래그 원본 DOM)를 원래 칸 목록에서 빼서 놓을 칸으로 옮겨 그렸다**(미리보기 = 원본 카드를 그 칸에 넣는 방식 · `cells` 계산에서 원본을 건너뛰고 `over` 칸에 다시 넣음). React 는 부모가 바뀐 원본을 언마운트 · 새로 만들고, 같은 칸이라도 끝으로 다시 넣으면 DOM 을 옮긴다. Chrome 은 드래그 원본 노드가 문서에서 빠지거나 옮겨지면 그 끌기를 바로 끝내 버려 `drop` 이 오지 않는다 — 사용자 눈에는 「잡혔다가 놓이지 않음 / 안 잡힘」. 특히 한 줄에 카드가 둘 이상인 칸(끝 카드가 아닌 카드)과 다른 칸으로 끌 때 늘 난다. 재현: 고치기 전 코드 · headless Chromium · 카드 둘 있는 칸의 첫 카드 → 이벤트 `dragstart` 만(`drop` 없음) / 고친 뒤 같은 동작 → `dragstart drop` + move 호출. 고침 = 원본은 끄는 동안 제자리에 두고(흐리게) 미리보기는 복제 카드로 그림 + dragstart 안 상태 바꿈을 다음 틱으로. back 원인 아님(`draggable` = `main ∈ {reserved, reception}` 그대로). `app/**` · 공용 컴포넌트에는 원인 없음.

이동 계약(§5.4)은 그대로 — 놓기 금지 칸 빨간 점선(그 칸에 카드 구역이 안 켜짐 · 슬롯 full) · 놓으면 낙관 표시 → 실패면 원위치 + back `message` 토스트 · 길이 유지(page `move` 그대로).

## 검증 — 명령과 결과

- `npx tsc --noEmit` → 오류 0 · `npm run lint` → 문제 0 · `npm run build` → `✓ Compiled successfully` · 정적 8쪽 생성(첫 실행은 Next.js 의 보안 업그레이드 안내가 끼어 종료 코드 1 — 다시 실행 rc=0 · 코드 문제 아님)
- 화면 확인: 임시 포트 back 8791(`PROC_FAKE_BOARD=1` · 임시 DB · KOS 주소는 닿지 않는 값으로 막음) · front dev 3791 · Playwright(Chromium · WebKit). 끝난 뒤 두 프로세스 끔(3791 · 8791 LISTEN 없음). 사용자 3700 · 8700(docker) 손대지 않음
- 가짜 모드는 조작이 403 이라 **이동 · 공지 저장 응답은 Playwright 가로채기로 흉내**(KOS 쓰기 0)

| 확인 | 결과 |
|---|---|
| 드래그 — 다른 칸 · 다른 시각(일본 10:00 → 동남아 11:00) | `dragstart drop` · 본문 `{resourceIndex:0, groupId:5, start:"…T11:00:00+09:00"}` · 카드 새 자리 + 토스트 「고객 A 예약 이동」 |
| 드래그 — KOS 거절(409 흉내) | 원위치 + 토스트 back `message` |
| 드래그 — 구역 안 켜진 칸 | 빨간 점선 · 놓아도 호출 없음 |
| WebKit 드래그 | 고친 뒤 `dragstart drop` |
| 공지 보기 · [수정하기] · 편집 | 첫 공지 하나 · 편집 칸에 다시 읽은 내용 · **11초(폴링 1번 넘김) 뒤에도 편집 글자 그대로** |
| 저장 실패(409 흉내) | 토스트 「지난 날짜 공지는 고칠 수 없어요」 · 편집 유지 |
| 저장 성공 | 본문 `{date:"2026-10-27", noticeId:1, content:…}`(noticeId = 그 공지 id) · 토스트 · 읽기 상태 |
| [취소] | 원래 내용 · 호출 0 |
| 2001자 | [저장] 꺼짐 · 글자 수 빨강 / 2000자 + 공백 4 = 켜짐(trim) |
| 빈 저장 | 본문 content `"   "` 보냄(지우기는 back) → 「이 날짜 공지가 없어요」 |
| 편집 중 › | 편집 닫힘 + 토스트 「저장하지 않은 공지 편집을 취소했어요」 |
| 지난 날짜(10-26) | [수정하기] 없음 |

스크린샷 `orchestration/work/overall-board/fe-shots-reservation/`: `fix3-drag-before` · `-during` · `-after` · `-blocked` · `-rejected` · `-rejected-toast` · `fix3-notice-view` · `-edit` · `-save-fail` · `-saved` · `-over2000` · `-cleared` · `-date-discard` · `-past` (왼쪽 아래 「Insight」 동그라미는 Next dev 오버레이 — 배포에는 없음)

## 계약 대조

| SPEC | 같음/다름 |
|---|---|
| §5.4 카드 잡기 · 미리 막기 · 원위치 · 길이 유지 | 같음 |
| §5.15 첫 공지 하나 · 누를 때 다시 읽기 · 제자리 편집 · [취소] · [삭제] 없음 · 빈 저장 = 지우기 · trim 2000 · 실패 편집 유지 · 성공 토스트 · 폴링이 편집 안 덮음 | 같음 |
| §6.4 [수정하기] 오늘 · 앞날만(`noticeEditable`) · 글자 수 n / 2000 | 같음(숫자는 천 단위 쉼표 「2,000」) |
| §7.5 `PUT /api/reservations/notice {date, noticeId, content}` | 같음 · content 는 trim 하지 않고 보냄(back 이 갈래별로 trim) |
| DS 만 | `Textarea` · `Button`(medikit) — 브라우저 기본 컨트롤 없음 |
| 추가 지시 1 | 4개 모두 반영 |

## 이슈 · 코디가 확인할 것

1. **실 KOS 데모 E2E 미실행** — §9 #11(실제 이동 → KOS) · #46 (a)~(f) 은 front 에서 KOS 쓰기를 하지 않았다(가로채기로만). 데모 공지 실호출은 backend 몫(§2.4) · 코디 데모 확인 필요. 남긴 데모 흔적: front 0
2. 끄는 중 원본 카드가 없어졌다면(폴링으로 그 예약이 사라짐) `dragend` 가 안 와 끄는 상태가 남을 수 있다 — 아무 칸에 놓거나 다음 끌기에서 풀린다(드묾 · 손대지 않음)
3. Next.js 16.4.0 이 dev · build 때 「알려진 보안 취약점 · 업그레이드 권장」 안내를 낸다 — 이번 범위 밖이라 업그레이드는 안 함(코디 판단)

## 리뷰 r3 수정 (W2 · W3)

| # | 고침 | 파일 |
|---|---|---|
| W2 | [오늘] = 보는 날짜가 이미 오늘(KST)이면 공지 편집 그대로 · 날짜가 바뀔 때만 버림 + 토스트(`goToday` 에서 `shownDate !== kstToday(now)` 일 때만 `leaveDate`) | `app/(main)/reservations/live/page.tsx` |
| W3 | [수정하기] 다시 읽기 응답이 왔을 때 **지금 보는 날짜**(페이지 `shownDate` — 클릭 즉시 바뀌는 값 · ref)와 요청 날짜가 다르면 버림(`setDraft` 안 함). 페이지가 `isShownDate(date)` 를 넘김 | `components/reservations/ResvAside.tsx` · `page.tsx` |

검증: `npx tsc --noEmit` 오류 0 · `npm run lint` 문제 0. 화면 재촬영 없음(지시 범위 = tsc · lint). 커밋 안 함.

## batch 5 #2 — 예약 상세 아래 줄 버튼 높이 통일

| 고침 | 파일 |
|---|---|
| [예약 취소] = 브라우저 `<button>`(40px) → DS `Button variant="outlined" color="red"`(기본 lg = 50px) · 펼침 목록 위치 48 → 58 | `components/reservations/DetailModal.tsx` |
| [시술실 선택 ▴] = `<button>`(40px) → DS `Button variant="outlined"`(방 없음 red · 고정 gray · 고름 blue · ▴ = `rightIcon`) · 방 목록 위치 60 → 70 | 같음 |
| 진행 경로 토글(상담 필요 / 바로 시술) = 트랙 높이 40 → 50(안쪽 여백 4) — DS 에 세그먼트 컨트롤이 없어 기존 토글 모양 그대로 높이만 맞춤 | 같음 |

잰 값(Playwright · 가짜 모드): 접수 전 줄 `예약 취소=50 · [경로]=50 · 시술실 선택=50 · 접수 완료=50` / 상담 · 귀가 대기 줄 = `닫기=50`(이 줄에 오는 버튼은 [닫기] 하나 — [귀가 완료] 등 단계 버튼은 오른쪽 진행 영역에 있어 바닥 줄 아님). 스크린샷 `b5-2-reserved.png` · `b5-2-consultation.png` · `b5-2-home-waiting.png`

## batch 5 #3 — [+] · 시간은 빈 공간 호버 때만 · 카드 가리지 않게

| 고침 | 파일 |
|---|---|
| 칸 호버 판정 `onMouseEnter` → `onMouseOver` + 대상이 카드(`[data-resv]`) 안이면 [+] 안 그림 — 카드 위 호버 = [+] 없음 · 같은 칸 빈 공간(카드 아래 · 옆) = [+] | `components/reservations/ScheduleTable.tsx` |
| 떠 있는 검은 툴팁(「{그룹} \| HH:MM ~ HH:MM」 · 카드를 덮던 것) 뺌 → [+] 상자 안에 「+ 10:30 ~ 11:00」 · 그룹 · 시각은 `aria-label` 에 | 같음 |

확인: 카드 위 호버 → [+] 0개 / 카드 있는 칸의 카드 아래 빈 공간 → [+] 1개(카드 아래 줄 · 카드와 겹침 없음: 카드 bottom 575 · [+] top 581) / 빈 칸 → [+] 1개. 드래그 중 미리보기 그대로. 스크린샷 `b5-3-hover-card.png` · `b5-3-hover-space.png` · `b5-3-hover-empty-cell.png`

검증: `npx tsc --noEmit` 오류 0 · `npm run lint` 문제 0. 임시 포트 3791 · 8791 끔 · 3700 · 8700 손대지 않음 · 커밋 안 함
