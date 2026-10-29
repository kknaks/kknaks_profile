# 리뷰 리포트 — agency-settlement / code r2 — back/ · front/ 2판 ↔ SPEC-001 0.3.1 (2026-10-29)

대상: 워크트리 `agency-settlement`(커밋 전 · `back/**` · `front/**` · `README.md` · `.gitignore`) · 기준 SPEC-001 **0.3.1** · DEC-001 D-01 ~ D-17 · WORK-001 2판 WP-REVIEW2 행
앞 판: `review-code-r1-report.md` · `review-doc-r4-report.md` · 워커 보고 `wp-fe2-report.md` · backend 판단 ① ~ ⑤(dispatch)
read-only. 이 파일 하나만 썼다. 8800 · 3800 서버 · `back/.env` · `back/data/` 내용은 건드리지 않았다(권한만 `ls`). 운영 KOS 호출 0.

## 판정: FAIL

FAIL 1 · WARN 3 · NOTE 9. FAIL 은 **front 한 곳**(확정 달을 확인 없이 다시 받는 길)이다. back 의 돈 경로(증분 새 행 = 수 · 같은 수단 · 같은 금액 · 전체 받기 갈아 끼우기 범위 · 두 달 동시 · `itemsNowhere` · 증분 itemsHere 바뀜 · 줄 선 요청 · 실패 시 DB 안 바뀜)는 SPEC 대로 짜여 있고 시험으로 받쳐져 있다. WARN 3 은 backend 가 SPEC 글자에서 벗어난 판단 둘(r4 W-2 「바뀜」 · 증분 ② 범위 좁힘)과, 시험은 초록인데 운영에서 에이전시 이름이 로그에 찍히는 자리 하나다.

### 돌린 것

| 무엇 | 결과 |
|---|---|
| `cd back && uv run --frozen --no-sync pytest -q -p no:cacheprovider` | **119 passed**(1.79s · 가짜 transport · 임시 DB) |
| `uv run ruff check --no-cache .` | All checks passed |
| `cd front && npx tsc --noEmit --incremental false` | 0 오류 |
| `npx eslint .` | 0 problems |
| `npm run build` | **안 돌림** — 3800 `next dev` 가 같은 `.next/` 를 쓴다(덮으면 코디 서버가 깨짐). FE 보고의 build 통과를 믿음 |
| grep `refresh=1` · `localStorage` · `sessionStorage` · cc-prototype import(front) | 0 |
| grep 실제 꼴 에이전시명 · 전화 · 키(back/app · tests · front) | 0 — 에이전시A/B/C · `옛에이전시` · `없는에이전시` · `010-0000-1111` 같은 가짜만 |
| `git status --ignored` | `back/.env` · `back/data/` · `front/.env.local` ignored · `front/*.tsbuildinfo` front `.gitignore` 로 빠짐 |
| `back/data/` 권한 | 폴더 `drwx------`(700) · `sales.sqlite3` `-rw-------`(600) |

---

## FAIL

### F-1 [전체 다시 받기] 뒤 달을 옮기면 그 달을 **확인 없이 `refresh=full`** 로 다시 받는다 — 확정 달도

- `front/components/monthly/SalesScreen.tsx:30` `const [req, setReq] = useState<{ n; refresh? }>` · `:35` `key = \`${month}#${req.n}\`` · `:56` effect 의존 `[month, key, refresh]` · `:74-77` `goMonth` = `router.push(…?month=)` 만 · `:84` `fetchAgain` 만 `refresh` 를 바꾼다 · `:215` 확인 뒤 `fetchAgain('full')`
- `front/app/page.tsx:10` · `app/agency/page.tsx:11` — `<SalesScreen … month={month} />` 에 `key` 없음. 같은 page 에서 `?month=` 만 바뀌면 React 는 같은 `SalesScreen` 인스턴스를 둔다 → `req.refresh` 가 **남는다**
- 길: 10월에서 [전체 다시 받기] → 확인 → `refresh=full`(정상) → `‹` 로 9월 → effect 가 `month=2026-09&refresh=full` 를 보낸다(월이 바뀌어 `key` 가 바뀜) → back J1 → **확정된 9월을 KOS 에서 처음부터 다시 받는다**(수백 회 호출 · 품목 상태 배지 · 이름 · 유입이 지금 값으로 바뀜). 확인 창 없음 · 화면은 「불러오는 중」만. 브라우저 뒤로 가기 · 앞으로 가기도 같다. 메뉴(`/` ↔ `/agency`)를 바꾸면 page 가 바뀌어 상태가 풀리므로 그 길은 없다
- 같은 원인으로 [새 결제 받기] 뒤 달을 옮기면 `refresh=new` 가 붙는다 — 확정 달은 J3(KOS 0)이라 해가 없고, 이번 달은 J6 대신 J5(① 1회 더) · 저장 안 된 달은 어차피 J2. 해는 작지만 같은 고침으로 닫힌다
- 어기는 것: **D-12**(「지난 달 = 한 번 받으면 다시 안 부른다 · 전체 다시 받기는 사람이 누를 때만」) · SPEC §3.1 저장 상태 줄(「`[전체 다시 받기]` 는 누르면 확인 한 번 뒤 부른다」) · §4.5 J3 · §9.3 「`[전체 다시 받기]` 는 확인 뒤에만 요청」 · 체크리스트 「확정 달 KOS 0」
- 시험이 못 잡은 이유: FE 스크린샷 흐름(`fe2-shoot.mjs` · 보고 「가짜 back 요청 기록 `refresh=full` 1(확인 뒤에만)」)은 전체 다시 받기 뒤 **달을 옮기지 않았다**. back 시험은 front 를 안 본다
- 고칠 것(frontend · 하나): (a) `refresh` 를 그 요청의 달에 묶는다 — `req` 에 `month` 를 같이 넣고 effect 에서 `req.month === month ? req.refresh : undefined` · 또는 (b) `goMonth` 에서 `setReq({ n: n+1 })`(refresh 없이) · 또는 (c) page 두 곳에서 `<SalesScreen key={month} … />`. (c)가 가장 짧지만 `lastOk`(「HH:MM 이후」 글)도 같이 풀린다 — 그 글은 같은 달에서만 쓰므로 해 없음
- 확인(frontend): 가짜 back 으로 「10월 [전체 다시 받기] → 확인 → ‹ → › · 브라우저 뒤로」의 요청 주소에 `refresh` 0 · 「[새 결제 받기] → ‹」도 0

---

## WARN

### W-1 r4 W-2 「바뀜」 = 그 수납의 이 달 ① 행을 KOS 대로 갈아 끼움 — 돈은 맞지만 SPEC 0.3.1 글자와 다르고, 셈 뜻이 바뀐다 (backend 판단 ②-2)

- `back/app/service/sales.py:249-267` `diff_rows` — 한 수납에 남는 묶음(`b > a`)과 모자란 묶음(`a > b`)이 같이 나오면 `changed` · `:456-458` 그 수납은 `replace_rows[pid] = got`(받은 행 전부) · `back/app/repository/store.py:342-344` 그 수납의 이 달 `transactions` 를 지우고 다시 씀 · `:446` 로그 `changedPurchases=N` 만 · 시험 `tests/test_store.py:128` #27g
- 판정: **돈 경로로는 맞다** — r4 W-2 의 「500,000 → 300,000 이 두 번(800,000) 들어감」을 막고 KOS 와 같아진다. `REQUESTED → APPROVED` 처럼 상태만 바뀐 행도 깔끔히 정리된다
- 걸리는 것:
  1. SPEC §4.5 증분 2 `:398` 은 여전히 「`n_new < n_stored` 면 **저장 행을 지우지 않고** `missingTransactions`」다. 0.3.1 에 「바뀜」 줄이 없다(r4 W-2 는 planner 몫이었고 SPEC 이 안 고쳐졌다). SSOT 로는 코드가 계약 밖이다
  2. 한 수납 안에서 **KOS 가 행 하나를 빠뜨리고(§4.6 ⑦) 같은 받기에 다른 새 행이 들어오면** 그 수납은 「바뀜」으로 잡혀 빠진 행이 **지워진다**(§4.6 ⑦ 「저장 행 그대로」와 반대 · D-13 받은 시점 기준). 다른 수납에서만 빠지면 그대로 남는다 — 같은 일이 수납마다 다르게 처리된다. 스펙에 없는 일이라 드물다
  3. 셈: `fetch.newTransactions` 에 갈아 끼운 행의 「남는 쪽」이, `missingTransactions` 에 「모자란 쪽」이 들어간다(`:444`). 그래서 L14 통과 기준 「`missingTransactions 0`」과 L19 ⑥ 이 「바뀜」 한 건으로도 깨지고, 응답에는 바뀜 수가 없어 원인(⑦ 인지 바뀜인지)을 응답만으로 못 가른다(로그 `changedPurchases` 를 봐야 함 — r4 W-3 과 같은 자리)
- 고칠 것: planner — SPEC §4.5 증분 2 에 「한 수납에 모자람 · 남음이 같이 나오면 그 수납의 이 달 ① 행을 KOS 대로 갈아 끼운다(바뀜 · r4 W-2 (b)) · new · missing 셈은 그대로 · 로그 `changedPurchases`」 한 줄 + §4.6 ⑦ 에 「같은 수납에 새 행이 같이 오면 바뀜으로 지워짐」 + L14 · L19 ⑥ 기준에 바뀜 수. 응답 필드(`fetch.changedPurchases`)를 둘지는 코디 판단 — 두면 LIVE2 판독이 쉬워진다

### W-2 증분 ② 를 「이번 증분에서 다시 판정한 수납」으로 좁힘 — 옛 `itemsMissing` 은 사람이 [전체 다시 받기] 를 눌러야만 낫는다 (backend 판단 ②-1)

- `back/app/service/sales.py:468-469` `with_items = store.known(diff.new_pids)` · `_items(m, {새로 판정해 items_here} − with_items)` — ② 후보가 `diff.new_pids` 뿐
- SPEC §4.5 증분 5 `:401`: 「② 는 **`items_here = true` 인데 `items` 가 저장돼 있지 않은 수납이 하나라도 있으면** 한 번」 — 범위는 그 달 수납 전부다. 「처음 보는 수납 · `false → true` 가 된 저장 수납 둘 다 여기 든다」는 예시이지 범위를 좁히는 말이 아니다
- backend 근거 「#26 과 충돌 회피」: #26 `:720` 은 「새 행 없음 → ② · ③ · ⑤ 0」인데, 그 시험의 가짜 달에는 `itemsMissing` 수납이 없어 SPEC 글자대로 해도 #26 은 초록이다. 충돌은 「`itemsMissing` 이 있는 달에서는 증분마다 ② 1회」뿐이고, 그것이 SPEC 이 정한 값이다(② 는 한 달 한 페이지 · 1회)
- 실물: 첫 받기 때 ② 통계에 늦게 들어온 품목(L4 가 0 이 아닌 경우)은 지금 코드로는 **증분이 몇 번 돌아도 「품목을 찾지 못했어요」가 남는다**. 스스로 낫는 길이 SPEC 에는 있는데 코드에는 없다
- 고칠 것(하나 고름 · 코디): (a) backend — SPEC 대로 그 달 `items_here = true` · 품목 없음 수납 전부를 ② 후보에 넣음(+ #26 은 그대로 · 「itemsMissing 수납이 있으면 증분에 ② 1회 · 그 수납 품목 저장 · `itemsMissing 0`」 시험 하나) · 또는 (b) planner — SPEC 증분 5 를 「이번 증분에서 다시 판정한 수납만 · 옛 itemsMissing 은 [전체 다시 받기]」로 고치고 §4.6 에 줄 하나. 돈과는 상관없고 화면 「품목을 찾지 못했어요」가 오래 남느냐의 문제라 (a)를 권함

### W-3 운영에서 uvicorn access log 에 엑셀 주소의 **에이전시 이름**이 찍힌다 — 시험(#40)은 ASGITransport 라 못 본다

- `README.md:38` 실행 명령 `uv run uvicorn app.main:create_app --factory --host 127.0.0.1 --port …` — `--no-access-log` 없음 · `back/app/main.py:25-27` 은 `httpx` · `httpcore` 만 WARNING 으로 내림(`uvicorn.access` 손대지 않음)
- uvicorn 기본 access log = `INFO … "GET /api/sales.xlsx?month=2026-10&view=agency&agency=%EC%97%90…%28%EC%97%90%EC%9D%B4%EC%A0%84%EC%8B%9C%29 HTTP/1.1" 200` — 퍼센트 인코딩일 뿐 그대로 에이전시 이름이다
- 어기는 것: SPEC §4.7 로그 줄(「**에이전시 이름** · 손님 이름 · 금액 · 수납 id · 파일 이름을 남기지 않는다」) · §7.3(로그에 남기는 것 목록 밖) · L9(back 로그 grep)
- 시험: `back/tests/test_export.py:160` #40 은 `httpx.ASGITransport` 로 앱을 직접 불러 uvicorn 로거가 없다 → 초록. 「시험은 초록인데 운영에서 터질 자리」
- 같은 꼴(front 쪽 · 참고): `next dev` 터미널 요청 로그에도 `/agency?month=…&agency=…` 가 찍힌다. 화면 주소에 에이전시 이름을 두는 것은 SPEC §3.5 가 정한 것이라 front 는 고칠 몫이 아니다 — 코디가 LIVE2 때 back 로그만 grep 하면 된다는 것만 알면 됨
- 고칠 것(backend): README · SPEC §10.2 실행 명령에 `--no-access-log` 를 더하거나, `main.py` 에서 `logging.getLogger("uvicorn.access")` 에 쿼리를 지우는 필터를 건다(경로 · 상태는 남김). 시험은 필터를 단위로(레코드 args 에 쿼리 없음)

---

## 1. 돈 경로 — 저장 · 증분 · 확정 · 전체 · 동시

| 자리 | 코드 | 판정 |
|---|---|---|
| 증분 ① = 달 전체 1회 · `fromUtc` = 달 시작 | `sales.py:383-390` · `:442` · `:575` | 맞음(#26) |
| 새 행 = 묶음 키 G(수납 · 상태 · 수단 · 금액 · 통화) 수 · `last_updated` 빼고 | `records.py:25-27` · `sales.py:249-267` | 맞음(#27 a ~ f) |
| 같은 수단 · 같은 금액 새 승인 · 같은 금액 부분 취소 두 번 | `pick_new_rows` `sales.py:270-285`(저장 tx_id 와 다른 거래 → 못 이음 → 나머지) | 맞음 · 수 · 금액은 늘 `n_new − n_stored`(#27 b · c) |
| 행이 그 자리에서 바뀜(r4 W-2) | `sales.py:456-458` · `store.py:342-344` | 돈 맞음 · **W-1** |
| 줄어든 행 | 지우지 않음 · `missing` | 맞음(바뀜 수납 빼고 — W-1-2) |
| 새 행 있는 수납만 ⑤ · 다시 판정 · 처음 보는 수납만 ③ · ④ | `sales.py:448` · `:452-464` · `:470-471` | 맞음(#28) |
| 증분 ② 범위 | `sales.py:468-469` | **W-2** |
| 증분 itemsHere `false → true`(r3 W-3) | 다시 판정 → `with_items` 에 없으면 ② · 쓰기 때 고정 뒤 `here and not has` 만 저장 `store.py:355-360` | 맞음(#43) |
| 전체 = 그 달 `transactions` · `month_purchases` 지우고 다시 · `items` 는 이 달 고정 뒤 `items_here` 수납만 · `purchase_txs` · `visitors` 는 이 달 수납 전부 | `store.py:323-337` | 맞음(#31 · F-3) |
| 지우기 · 쓰기 한 트랜잭션 · KOS 다 끝난 뒤 | `sales.py:415-434`(KOS 전부 → `write_full`) · `store.py:167-188` `BEGIN IMMEDIATE` · 오류면 ROLLBACK | 맞음(#32 · #44) |
| 품목 달 고정 = 확인 · 쓰기 같은 트랜잭션 | `store.py:264-270` `_pin` 을 `write_full` · `write_incremental` 트랜잭션 안에서 · 쓰기 잠금 하나 `sales.py:430` · `:473` | 맞음(#41 · r3 W-1) |
| `itemsNowhere` · `itemsPinnedElsewhere` 에서 뺌 | `store.py:233-236` · `sales.py:556` · `:648-649` | 맞음(#42) |
| 줄 선 요청 = 기다리는 동안 **성공한** 받기가 끝났으면 저장본만 | `sales.py:317-325`(`_done` 은 성공 뒤에만 +1) | 맞음(#12 a ~ c · r4 NOTE-1 「성공한 받기만」도 지켜짐) |
| 응답 = 쓰기 뒤 저장본을 읽기 트랜잭션 하나로 | `sales.py:326` · `store.py:209-238` | 맞음 |
| 확정 = 받기 시작 ≥ 다음 달 1일 + `SALES_OVERLAP_SEC` · 되돌리기 없음 | `sales.py:356-358` · `store.py:318`(옛 `closed_at` 유지) | 맞음(#30) |
| 판단표 J1 ~ J6 | `sales.py:344-354` | 맞음 — 위에서 처음 맞는 줄 차례 그대로 |

**동시 요청**: 같은 달 = 달 잠금 + `_done` · 다른 달 = 쓰기 잠금 + `BEGIN IMMEDIATE` 안 고정 · 엑셀 = 달 잠금(`sales.py:338`). SQLite 호출이 동기라 이벤트 루프 안에서 쓰기 둘이 섞일 수 없다. 두 프로세스는 SPEC 밖(README `:48` 워커 하나). 빠지거나 두 번 들어가는 길은 F-1(front) · W-1-2(바뀜 수납의 빠진 행) 밖에 못 찾았다.

## 2. 확정 달 KOS 0 — 조용히 다시 부르는 길

| 길 | 판정 |
|---|---|
| J3 `closed` → `none` | `sales.py:349-350` 맞음(#25 · 새 인스턴스 · 같은 파일) |
| 줄 선 `full` | 저장본만 맞음 |
| 엑셀 | `stored()` 판단표 안 탐 · 저장 없으면 409 `sales.py:335-342` 맞음(#37) |
| `schema_version` 다름 | 뜨지 않음 · 파일 그대로 `store.py:138-142` 맞음(#36) |
| 경로 규칙 밖 | 뜨지 않음 · 파일 안 만듦 `store.py:117-125` 맞음 |
| 저장 파일 열기 · 읽기 실패 | `store_failed` 500(J2 로 떨어지지 않음) `store.py:175-179` 맞음 |
| **front 가 남긴 `refresh=full`** | **F-1** |

## 3. SQLite 개인정보

- 표 6개 · 칸 = SPEC §4.4 표 그대로(`store.py:36-106`) · `json` · `raw` · `body` 칸 0 · ③ 은 `visitor.name` · `reservation.startDateTime` 만 `sales.py:519-522` · ④ `name` 만 `:533-534` · ⑤ 는 `tx_of` 의 칸만 `:104-111` · ② 는 `item_of` 칸만 — 원본 JSON 저장 0(#20 · #36 덤프 시험 초록)
- 폴더 700(없을 때 만듦) · umask 077 · 셋 600 · 쓰기마다 · 뜰 때 넓으면 고침 `store.py:131-165` · 실물 `back/data` 700 · 본 파일 600 확인
- gitignore `back/data/` · `*.sqlite3*` 레포 `.gitignore` 에 더해짐 · `git status --ignored` ignored
- 로그: 서비스 = 달 · mode · 숫자 · `counts` 숫자 · 걸린 시간 · KOS 오류 이름 `sales.py:330-332` · `:376` · `:381` · `:389` · 저장 = 예외 이름만 `store.py:178` · 엑셀 = 달 · view · 행 수 `api/sales.py:31` — 맞음. 빠진 곳은 uvicorn access log(**W-3**)

## 4. 엑셀

| 항목 | 코드 | 판정 |
|---|---|---|
| 칸 차례 D-14 11칸 | `export.py:22-23` | 같음 |
| 수식 셀 0 · 글자 칸 `data_type = "s"` | `export.py:73-78` | 맞음(#38 `=1+1` · `+A1` · `@SUM(1)` · `-1` 다시 읽음) |
| 금액 숫자 셀 · 음수 그대로 · KRW 밖 통화 형식 | `export.py:81-84` · `:120-121` | 맞음 |
| 결제일 날짜 · 시각 셀(KST · tz 없음) · 방문일 날짜 셀 · 수납 id 글자 전체 | `export.py:100-111` | 맞음 |
| 이름 그대로 D-17 | `export.py:106` | 맞음 |
| 화면 범위와 같음 — 거르기 · 묶음 차례 · 줄 차례 | `filter_purchases` `export.py:39-47`(front `SalesScreen.tsx` `shown` 과 같은 규칙) · 응답 `purchases` 차례 = back `sales.py:562-568` 정렬 = front `format.ts` `sortPurchases` 와 같은 키 · 줄 = 품목 → 시각 차례 | 같음 |
| 합계 행 0 · 머리 행 0 · 시트 「정보」 | `export.py:87-142` | 맞음 |
| 파일 이름 3꼴 · 못 쓰는 글자 `_` · `filename*=UTF-8''` · no-store · Expose-Headers | `export.py:57-66` · `:29-36` · `main.py:57-65` | 맞음(#39) |
| KOS 0 · 디스크 0 | `sales.py:335-342` · `BytesIO` | 맞음(#37 · #40) |

## 5. 손님 셈 · 에이전시 · 탭

- 판정 `agency_of` = 공백 뗀 값이 반각 `(에이전시)` 로 끝남 · 값 그대로 `sales.py:127-132` · 유입 = ① `visitorFunnelName` 첫 값 `:651` · 자유 텍스트 0 — 맞음(#34)
- 손님 D-15 = `visitorId` · 없으면 `purchase:<id>` `sales.py:581-582` · `agencyTotal` 은 에이전시 수납 전부로 다시 셈 `:591-594` — 맞음
- 결제 손님 D-16 = 그달 ① `APPROVED` 행이 하나라도 있는 수납의 손님 — 금액 · 순액 안 봄 `sales.py:588` — 맞음(0 원 · 순액 0 이하 포함 · #35)
- `agencies[]` = 그달 저장본만 · 이름 차례 `sales.py:592` — 맞음
- front 탭 = 「에이전시 전체(agencyTotal.purchases)」 + `agencies[]` · 글자 뗌 · `title` 원래 값 · 없는 `agency=` → 전체 + `router.replace` `AgencyTabs.tsx:17-20` · `SalesScreen.tsx:66-72` — 맞음. 손님 · 결제 손님은 back 값 그대로(front 가 다시 세지 않음 · `SummaryLine.tsx`) — 맞음

## 6. back `schemas` ↔ front `lib/types.ts` · 시안 v2 와 다른 곳

- 필드 하나하나 대조: `SalesResponse` 10 · `RangeUtc`(`from` alias) · `StoreInfo` 4 · `FetchInfo` 7 · `Counts` 15 · `AgencyTotal` 3 · `AgencySummary`(`name` 먼저) · `Purchase` 17 · `Line` 10(`paymentType` 은 item 줄에서 키 빠짐 ↔ types `paymentType?`) — **전부 같음**. types 의 `itemType` 은 4값 리터럴, back 은 `str`(모르는 값이 와도 화면은 `?? t` 로 그대로 — 해 없음)
- labels 두 표: 품목 종류 3 · 품목 상태 5 · 줄 상태 3 · 결제 수단 7 같음(#39 시험이 `labels.ts` 를 읽어 비교 · `test_export.py:127`). front `LINE_TEXT`(`이 달 결제`)는 화면 상품 자리 글이고 엑셀 품목 종류 칸은 back `LINE_KIND_TEXT`(`결제`) — SPEC §4.7 값은 back 쪽이 맞다. `labels.ts:32` 주석 「엑셀 품목 종류 칸(§4.7)」만 틀림(NOTE-8)
- FE 보고 「시안 v2 와 다른 곳」 12: 1 · 2 · 3 · 4 · 6 · 8 = SPEC §3.5 · §6.8 · §3.6 · §3.1 · §3.2 가 정한 값(SPEC 이 이김 — 맞음) · 5 · 9 · 11 = 모양 · 문구(시안 · medikit — 맞음) · 7 = r4 NOTE-1 대응(맞음) · 10 = 1판 그대로 · 12 = 불러오는 중 탭이 「꺼짐」이 아니라 「안 보임」(받은 데이터가 없으므로 — SPEC §3.4 뜻과 어긋나지 않음). **SPEC 과 어긋난 것 없음**

## 7. backend 판단 ① ~ ⑤ — 판정

| # | 판단 | 판정 |
|---|---|---|
| ① | 증분(① 달 전체 · 묶음 키 수 · 새 것만 비싼 조회) | **맞음** — SPEC §4.5 증분 1 ~ 6 그대로 |
| ②-1 | ② 범위를 이번 증분에서 다시 판정한 수납으로 좁힘 | **W-2** — #26 과 실제 충돌은 없다 · SPEC 글자대로 권함 |
| ②-2 | 「바뀜」 = 그 수납 이 달 ① 행 갈아 끼움 · new 1 · missing 1 · 로그만 | **W-1** — 돈은 맞음 · SPEC 줄 · L14/L19 기준 고칠 것 |
| ③ | KOS 설정 없어도 저장본 요청은 200 | **받아들임** — D-12 · §4.7(저장본 = KOS 0)과 맞음. 다만 이번 달은 600초 지나면 J6 증분으로 503 이 된다(NOTE-1) |
| ④ | `closedAt` = 확정한 받기의 시작 | **받아들임** — `fetched_at` 과 같은 시계 · SPEC 「closed 가 된 시각」에 한 단어(NOTE-2) |
| ⑤ | `newPurchases` = 이 요청으로 이 달에 처음 저장된 수납 | **받아들임 · SPEC 글 고칠 것** — 앞 달 수납의 이 달 취소도 1 로 센다(③ 은 안 부름) → SPEC 괄호 「(③ · ② 를 부른 수)」와 다르다(NOTE-3) |

---

## 사용자가 실물에서 만날 자리

1. **10월 [전체 다시 받기] 뒤 ‹ 로 9월을 보면 9월이 다시 「불러오는 중」(수십 초)** — 확정된 달이 확인 없이 다시 받아지고 배지 · 이름이 지금 값으로 바뀐다(F-1)
2. 첫 받기 때 「품목을 찾지 못했어요」였던 수납이 [새 결제 받기] 를 몇 번 눌러도 그대로 — [전체 다시 받기] 를 눌러야 낫는다(W-2)
3. LIVE2 L14 에서 `missingTransactions` 가 0 이 아닌데 응답만으로는 「행이 바뀜」인지 「행이 사라짐」인지 모름 — back 로그 `changedPurchases` 를 같이 봐야 함(W-1)
4. back 터미널 로그에 엑셀 내려받은 에이전시 이름이 퍼센트 인코딩으로 찍힘(W-3) — 로그를 리포트에 붙이면 public 레포로 샐 수 있다
5. `back/.env` 키를 비운 채 띄우면 확정 달은 보이는데 이번 달은 10분 뒤부터 503 「KOS 연결 설정이 비어 있어요」(NOTE-1)
6. 자동 증분(J6)이 받는 중에 누른 [전체 다시 받기] 는 「방금 받은 결과예요 — 한 번 더 눌러 주세요」 — 처리됨(r4 NOTE-1)

## 참고 (NOTE)

- **NOTE-1** `sales.py:362-363` — `kos_not_configured` 는 KOS 를 불러야 할 때만. SPEC §4.3 `kos_not_configured` 줄에 「저장본만 읽는 요청은 200」 한마디 더하면 판단 ③ 이 계약이 된다
- **NOTE-2** `store.py:318` — `closed_at` = 확정한 받기의 시작 시각(옛 값이 있으면 유지). SPEC §4.2 `closedAt` 주석 「closed 가 된 받기의 시작 시각」으로
- **NOTE-3** `sales.py:477` · `:434` — `newPurchases` = 이 달 `month_purchases` 에 처음 생긴 수납. SPEC §4.2 `newPurchases` 괄호를 「(이 달에 처음 저장된 수납 · 앞 달 수납의 이 달 취소 포함)」로
- **NOTE-4** `sales.py:283` — `pick_new_rows` 의 마지막 고르기(`rest`)는 저장 행이 이미 가진 `tx_id` 에 이어진 행을 새 행으로 고를 수 있다 → 두 행이 같은 `tx_id` · 같은 `at`. 수 · 금액은 맞고 시각만 겹친다(§4.6 ⑥ 에 적힌 범위 · r4 NOTE-2) — 고칠 것 없음
- **NOTE-5** `sales.py:469` — ② 후보를 품목 달 고정 **앞** 판정으로 고른다. 다른 달에 고정될 수납 때문에 ② 를 1회 더 부를 수 있다(저장은 `store.py:359` 가 막음). 돈 · 화면 해 없음 · 호출 수만
- **NOTE-6** `store.py:248` — `known()` 의 「품목 있음」은 달을 가리지 않는다. 앞 달 [전체 다시 받기] 로 품목을 놓은 수납이 뒤 달 증분에서 `items_here` 가 되면 앞 달 때 받은 품목(그때 상태)을 그대로 쓴다 — D-13 받은 시점 기준 안
- **NOTE-7** J4 `sales.py:351` — 달이 끝난 뒤 겹침 여유(00:00 ~ 00:10) 안에서는 여는 때마다 증분(① 1회). SPEC J4 글자 그대로 · 10분 동안만
- **NOTE-8** `front/lib/labels.ts:32` 주석 「엑셀 품목 종류 칸(§4.7)」 — 엑셀은 back `labels.py` `LINE_KIND_TEXT`(`결제` · `결제 취소` · `반환`)를 쓴다. 주석만 틀림
- **NOTE-9** `npm run build` 는 3800 dev 서버와 `.next/` 를 같이 써서 이번에 안 돌렸다. 붙이기(진짜 back) 뒤 코디가 dev 서버를 내리고 한 번 돌릴 것

## 고칠 것 — 모아서

| # | 누가 | 무엇 |
|---|---|---|
| F-1 | frontend | 달을 옮기면 `refresh` 를 버림(`req` 에 달을 묶거나 `goMonth` 에서 초기화 · 또는 page 에 `key={month}`) + 「전체 다시 받기 → ‹ · 뒤로」 요청 주소 확인 |
| W-1 | planner | SPEC §4.5 증분 2 · §4.6 ⑦ · L14 · L19 ⑥ 에 「바뀜」 · (선택) `fetch.changedPurchases` |
| W-2 | 코디 → backend 또는 planner | 증분 ② 를 SPEC 글자대로(권함) 또는 SPEC 을 좁힘 |
| W-3 | backend | `--no-access-log` 또는 `uvicorn.access` 쿼리 지우는 필터 · README · SPEC §10.2 |
| NOTE-1 ~ 3 | planner | SPEC 글 세 군데(§4.3 · §4.2 `closedAt` · `newPurchases`) |
