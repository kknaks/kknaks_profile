# WP-FE2 결과 보고 — 시안 v2 적용 · 헤더 메뉴 · 에이전시 탭 · 받기 · 엑셀 버튼 (2026-10-29)

## 상태: done · 커밋 안 함 · `back/` · 루트 README 무변경 · 3800/8800 프로세스 무접촉

## 변경 파일 (`front/` 만)

| 파일 | 무엇 |
|---|---|
| `lib/types.ts` | §4.2 0.3.1 — `store` · `fetch` · `agencyTotal` · `agencies[]` · `purchases[].agency` · `newInLastFetch` · `itemsNowhere` · `counts.itemsPinnedElsewhere` · `itemsNowhere` · `Refresh` · `ExportView` |
| `lib/api.ts` | `getSales(month, refresh?: 'new'\|'full', signal)` · `salesXlsxUrl(month, view, agency?)` · `downloadSalesXlsx(url, fallbackName)`(Blob → 브라우저 내려받기 · `filename*=UTF-8''` 읽음) · 공통 `call()` |
| `lib/labels.ts` | 결제 수단 7개 이름(아래) · `lineText`(이 달 결제 · 결제 취소 · 반환) · `agencyShort`(「(에이전시)」 뗌) |
| `components/common/AppHeader.tsx` | 새로 — cc-prototype AppHeader 복사 · 세션 · 로그아웃 · 시계 · 드롭다운 뺌 · 메뉴 「월별 조회 \| 에이전트별 조회」(`?month=` 이어 감 · 불러오는 중 꺼짐) · 「세라미크 명동점」 + 「운영 · 조회 전용」 칩 |
| `components/monthly/SalesScreen.tsx` | 새로(`MonthlySales.tsx` 대체) — 두 화면 공용. 받기 상태 · 확인 1번 · 받은 시각 · 새 결제 글 · 탭 거르기 · 엑셀 · 상태 화면 |
| `components/monthly/SalesTable.tsx` · `PurchaseGroup.tsx` | `<table>` 10칸 → 시안 v1 **두 층 grid**(머리 6칸 + 들여 쓰고 왼쪽 선 그은 줄 6칸) · 0원 구성품 흐림 · 결제/취소 줄 = 수단 + 설명 글 · 「새로 받음」 · ⚠ 배지 |
| `components/monthly/SummaryLine.tsx` | 새로(`CountsLine.tsx` 대체) — 칩 줄 + 에이전시별 칩 + 「수수료 — 다음 판」 + 「받은 시점 기준」 안내 |
| `components/monthly/StatusView.tsx` | 시안 꼴(원형 아이콘 ! ? ⚙ —) · `BadMonthView` 더함 |
| `components/monthly/MonthPicker.tsx` · `format.ts` | 시안 글꼴 · 칸 너비 상수 · 음수 `−`(U+2212) |
| `components/agency/AgencyTabs.tsx` | 새로 — 「에이전시 전체 N」 + 그달 `agencies[]` 탭(글자 뗌 · title 원래 값 · 숫자 = 수납 건수) |
| `app/page.tsx` · `app/agency/page.tsx`(새로) | `/?month=` · `/agency?month=&agency=` |
| 지움 | `components/monthly/MonthlySales.tsx` · `CountsLine.tsx` |

결제 수단 이름(back `labels.py` 와 맞출 값 — **코디 중계 필요**): `CARD 카드` · `CASH 현금` · `PREPAID_CARD 선불카드` · `EASY_PAY 간편결제` · `TRANSFER 계좌이체` · `PLATFORM 플랫폼` · `MEDICAL_LOAN 메디컬론` · 그 밖(UNSPECIFIED 등) = KOS 값 그대로. 품목 종류 · 상태 이름은 1판 그대로.

## 검증

```
cd front && npx tsc --noEmit && npm run lint && npm run build
```
- tsc 통과 · lint 0 problems(exit 0) · build 통과(Route `/` · `/agency` · 마지막 build 는 기본 env — `.env.local` 의 8800 박힘 · 시험용 8891 빌드 남지 않음)
- `grep -rnE 'refresh=1|refresh: *1' app components lib` = **0** · `localStorage|sessionStorage` = **0** · cc-prototype import = **0**(「원본:」 주석 12)
- 스크린샷 = 시험용 빌드(`NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8891`) + `next start -p 3891` + 가짜 back 8891(scratchpad · 시안 v2 가짜 값) · playwright 1440×900 full page. **8800 으로 가는 요청은 playwright 에서 막음 — 막힌 것 0** · 페이지 오류 = 의도한 502(오류 장면) · 400(잘못된 달) 두 개뿐. 끝나고 3891 · 8891 내림(LISTEN 0). 3800 · 8800 은 그대로 떠 있음
- 가짜 back 요청 기록: `refresh=new` 2 · `refresh=full` 1(확인 뒤에만) · `sales.xlsx?view=monthly` · `view=agency` · `view=agency&agency=에이전시B(에이전시)` 각 1 · 내려받은 이름 `매출_2026-10_월별.xlsx` · `매출_2026-10_에이전시전체.xlsx` · `매출_2026-10_에이전시B.xlsx`

## 스크린샷 — `orchestration/work/agency-settlement/shots-fe2/` (시안 장면 이름 그대로 + 덧붙인 것)

| 파일 | 무엇 | 확인한 값 |
|---|---|---|
| `monthly.png` | 10월 · current | [새 결제 받기] · 마지막으로 받은 시각 10-29 14:03 · 수납 10 · 품목 14 · 결제·취소·환불 5 · 제외 1 |
| `monthly-current-pulling.png` | [새 결제 받기] 누른 직후 | 버튼 「받는 중…」(꺼짐) · 표 그대로 |
| `monthly-current.png` | 받은 뒤 | 15:20 · 「14:03 이후 새 결제 2건을 받았어요」 · 「새로 받음」 2 |
| `monthly-current-none.png` | 한 번 더 | 「새 결제 없음 · 15:31 확인」 · 배지 0 |
| `monthly-closed.png` | 9월 · closed | 「✓ 확정 · 저장됨」 · 새 결제 받기 0 · 13:58 · 작은 [전체 다시 받기] |
| `monthly-closed-confirm.png` · `-full-loading` · `-full-done` | 확인 1번 → 불러오는 중 → 15:22 | |
| `monthly-loading.png` | 불러오는 중 | 스피너 · 월 · 메뉴 · 엑셀 꺼짐 |
| `monthly-empty.png` | 8월 · 빈 달 | 「이 달에는 결제가 없어요」 · 엑셀 켜짐(헤더만 파일 — §3.6) |
| `monthly-error.png` | 502 | 「매출을 불러오지 못했어요 / KOS 에 연결하지 못했어요」 + [다시 시도] · 엑셀 꺼짐 |
| `monthly-bad-month.png` | `2026-13` | back 문구 + ‹ › 안내 |
| `monthly-config.png` | back 주소 빈 빌드 | ⚙ 「back 주소가 비어 있어요」 · back 요청 0 |
| `agency-all.png` | 에이전시 전체 · 10월 | 탭 전체 7 · A 4 · B 2 · C 1 / 에이전시 손님 7 · 결제 손님 6 · 수납 7 · 품목 10 · 줄 4 / A 4·3 · B 2·2 · C 1·1 / 수수료 — 다음 판 |
| `agency-one.png` | 에이전시B | 손님 2 · 결제 손님 2 · 수납 2 · 품목 4 · 줄 1 |
| `agency.png` | 에이전시A | 손님 4 · 결제 손님 3 · 수납 4 · 품목 6 · 줄 3 |
| `agency-empty.png` | 8월 에이전시 전체 0 | 「이 달에는 에이전시 손님의 결제가 없어요 / 에이전시 전체 · 2026년 8월」 |
| `agency-unknown.png` | `agency=에이전시Z(에이전시)` | 주소에서 빠지고 「에이전시 전체」 |
| `agency-closed.png` | 9월 에이전트별 | 탭 = 그달에 나온 A · B 만(C 없음 — §3.5) |

조작: 헤더 「에이전트별 조회」 → `/agency?month=2026-09`(달 이어 감) · 탭 A → `&agency=에이전시A(에이전시)` · ‹ → 8월에 A 없음 → `/agency?month=2026-08`.

가짜 이름 = 홍길동 · 김철수 · 이영희 · 박가명 · 정예시 · 강샘플 · 오가나 · 한다라 · 윤테스트 · 노샘플 · 류가짜 · 최가상 · 문예제 · 서임시 · 백더미 · null / 에이전시 = 에이전시A/B/C(에이전시) 만. 시험 스크립트 사본 `fe2-fake-back.mjs` · `fe2-shoot.mjs`(같은 폴더 위).

## WP-FE2 완료 조건 (WORK-001 2판 행 · SPEC §9.3)

| 조건 | 결과 |
|---|---|
| 헤더 메뉴(AppHeader 복사 · 메뉴 2 · 세션 뺌) | 충족 |
| 넓은 폭(max-width 없음 · 좌우 28) | 충족 |
| 두 층 표 · 결제/취소 줄 수단 · 설명 글 · 0원 구성품 흐림 | 충족 |
| `lib/types.ts` §4.2 0.3.1 | 충족 |
| `lib/api.ts` `getSales(month, refresh?)` · `salesXlsxUrl(month, view, agency?)` | 충족 |
| `lib/labels.ts` 결제 수단 이름 | 충족(7개 · BE2 와 맞추기 = 코디 중계) |
| 받기 버튼 두 상태 · 확인 1번 · 받은 시각 · 「새 결제 N」 · 0건 문구 · 「새로 받음」 · 「받은 시점 기준」 | 충족 |
| `/agency` 탭 · `?agency=` · 없는 값 → 전체 · 걸러진 건수 줄 · 요약 · 「수수료 — 다음 판」 | 충족 |
| `⚠ 통화 섞임` = `approvedTotal === null`(W-5) | 충족 |
| 툴바 오른쪽 [엑셀 내보내기] · 화면별 view/agency · 불러오는 중 · 오류 때 꺼짐 · 실패 토스트 | 충족(토스트 = medikit `notify.error` — 실패 경로는 실제로 띄워 보지 않음) |
| 시안 v2 장면과 나란히 스크린샷 | 충족(장면 12 + 덧붙임 7) |
| `refresh=1` 0 · 저장소 0 · cc-prototype import 0 | 충족 |
| 붙이기(진짜 back) | **안 함** — WP-BE2 뒤(WORK 「붙이기는 WP-BE2 뒤」) |

## 시안 v2 와 다른 곳

1. **탭 목록 = 그달 `agencies[]` 만**(SPEC §3.5 · R§2) — 시안 v2 는 저장된 모든 달. 그래서 `agency-empty` 는 시안의 「9월 · 에이전시C 탭 0」 대신 「8월 · 에이전시 전체 0」
2. **손님 수 = back 값(visitorId · D-15)** — 시안은 이름으로 셈. front 는 다시 세지 않음
3. **에이전트별 요약 줄에 건수 칩(수납 · 품목 · 결제·취소·환불) 더함** — SPEC §3.5 「걸러진 건수 줄」. 시안은 손님 · 결제 손님 · 수납만
4. **툴바 오른쪽 [엑셀 내보내기]**(시안 없음 · SPEC §3.6) — outlined gray 버튼. [전체 다시 받기] 는 그 왼쪽 작은 밑줄 글자
5. **[전체 다시 받기] 확인 모달**(medikit `ConfirmModal` caution · 「이 달을 KOS 에서 처음부터 다시 받아요 / 수십 초 걸려요」 — 확정 달은 「· 확정된 달도 지금 KOS 상태로 다시 저장돼요」 덧붙임). 모달 버튼 넘침은 cc-prototype UndoConfirm 과 같은 `flexShrink` 처리
6. **0건 문구 「새 결제 없음 · HH:MM 확인」** · 「N건을 받았어요」 앞의 「HH:MM 이후」는 같은 화면에 앞 결과가 있을 때만(페이지를 막 연 J6 자동 증분이면 「새 결제 N건을 받았어요」만)
7. **doc r4 NOTE-1 대응**: [전체 다시 받기] 했는데 `fetch.mode none`(줄 선 요청)이면 「방금 받은 결과예요 — 처음부터 다시 받으려면 한 번 더 눌러 주세요」
8. **`itemsNowhere`** = 「품목이 어느 달에도 없어요 — 이 달 [전체 다시 받기]」 빨간 작은 글(시안 없음 · SPEC §3.2)
9. 받은 시각 글 = 시안대로 「마지막으로 받은 시각 MM-DD HH:mm」(SPEC 예 「MM-DD HH:mm 받음」 — 문구는 시안이 이김)
10. 네트워크 오류 화면(「back 에 연결하지 못했어요 / back 이 떠 있나요?」 + 다시 시도) — 시안 없음 · 1판 그대로 · 이번엔 스크린샷 안 찍음(shots-fe 1판에 있음)
11. 스피너 = medikit `Loading`(시안은 CSS 원 대역)
12. 탭 · 메뉴 · 월 이동은 불러오는 중 꺼짐(§3.4). 탭은 불러오는 중엔 아예 안 보임(받은 데이터가 없어서)

## 미결 · 주의

- **labels 결제 수단 7개 이름을 back `labels.py`(WP-BE2)에 같은 값으로** — TRANSFER · PLATFORM · MEDICAL_LOAN 이름은 내가 고른 것(SPEC 에 없음)
- 3800 의 `next dev` 는 같은 워크트리를 보므로 이 변경이 hot reload 로 이미 반영됨 — 8800 back 이 아직 0.3.1 응답(`store` · `agencies` 등)을 안 주면 그 화면은 깨질 수 있음(BE2 전 정상)
- 엑셀 실패 토스트 경로는 실제로 띄워 보지 않음(가짜 back 409 장면 없음)

---

## 수정 1 (2026-10-29 · 지시서 `fe2-fix-1-instructions.md` — code r2 F-1 · 사용자 「좌우 폭이 너무 넓다」)

### 고친 것 (`front/` 만)

| 파일 | 무엇 |
|---|---|
| `app/page.tsx` · `app/agency/page.tsx` | `<SalesScreen key={month} …/>` — 달(주소 `?month=`)이 바뀌면 화면 상태를 새로 시작(‹ › · 브라우저 뒤로 · 앞으로 · 주소 직접) |
| `components/monthly/SalesScreen.tsx` | `req = { n, month, refresh? }` — refresh 를 **누른 달에 묶음**(`req.month === month` 일 때만 보냄) · 새 요청은 `fetchAgain` 하나로만 생기고 그때 refresh 를 다시 정함(다시 시도 = 없음). 본문 `max-w-[1600px] mx-auto` |
| `components/common/AppHeader.tsx` | 헤더 안쪽 `maxWidth: 1600 · margin: 0 auto`(본문과 같은 열) |

탭을 바꿀 때는 back 을 다시 부르지 않으므로(같은 응답 거르기) refresh 가 붙을 자리가 없다. 메뉴(`/` ↔ `/agency`)는 page 가 바뀌어 원래 새로 시작.

### F-1 확인 — 요청 기록(가짜 back 8891 · `fe2-f1-check.mjs`)

| 흐름 | 요청 · refresh |
|---|---|
| A 10월 [전체 다시 받기] → 확인 | 1 · `month=2026-10&refresh=full` 1 |
| → ‹ 9월(확정) · › 10월 · 뒤로 · 앞으로 · 메뉴 에이전트별 | 각 1 · **refresh 0** |
| B 9월(확정) [전체 다시 받기] → 확인 | `month=2026-09&refresh=full` 1 |
| → ‹ 8월 · › 9월 · 뒤로 · 뒤로 | 각 1 · **refresh 0** |
| C `/agency` 10월 [전체 다시 받기] → 확인 → 탭 A · ‹ 9월 · 뒤로 | 탭 = 요청 0 · 나머지 각 1 · **refresh 0** |
| D 10월 [새 결제 받기] → ‹ 9월 · 뒤로 · 새로고침 | `refresh=new` 1(누름) 뒤 **refresh 0** |

**확인 없이 나간 refresh = 0.** `refresh=full` 은 확인 모달의 [다시 받기] 뒤에만 나간다(3/3).

### 폭 1600 — 스크린샷 `shots-fe2/width-{1440,1920}-{monthly,agency-all}.png`

- 1440: 본문 x=28 · 너비 1384(좌우 28 그대로) · 1920: 본문 x=160 · 너비 **1600** · 헤더 로고 · 오른쪽 칩도 같은 열(x 160 ~ 1760)
- 스크린샷의 왼쪽 아래 「N」 동그라미는 Next dev 표시(시험용 dev 서버라서) — 화면 것 아님

### 검증

- `npx tsc --noEmit` 통과 · `npm run lint` exit 0. **`npm run build` 는 안 돌림**(지시 — `.next` 공유)
- 시험 = `front/` 를 scratchpad 로 복사(`.next` · `.env.local` 빼고)해 `next dev -p 3891`(`NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8891`) + 가짜 back 8891 · 8800 요청은 playwright 에서 막음(막힌 것 0). 끝나고 3891 · 8891 내리고 복사본 지움. **3800 · 8800 프로세스 무접촉**(3800 은 hot reload 로 반영)
- 서식: 고친 두 파일에 prettier 를 한 번 돌렸다(`--single-quote --print-width 180` — 레포 꼴에 맞춤 · 줄바꿈 몇 곳 달라짐)
- 워크트리 `git status` 의 `M .gitignore` · `M README.md` 는 backend 작업 것(나는 안 건드림)
