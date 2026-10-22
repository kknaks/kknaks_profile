# 시술현황판 시안 r2 결과 보고 — 배포 코드 기준으로 다시 그림 (2026-10-20)

## 상태: done

claude design `dda9a931` 에 새 파일 **`Ceramique 시술현황판 v2.dc.html`** 을 올렸다. v1 파일은 지우지도 고치지도 않았다.

- 기준 = 코드 레포 `cc-prototype` **`origin/main` `339293e`**. `git show origin/main:<경로>` 로만 읽었다(checkout · pull 안 함)
- 로컬 사본: `orchestration/work/myeongdong-poc-v2/design-upload/Ceramique 시술현황판 v2.dc.html`(52,632 bytes)
- ⚠ 렌더링은 눈으로 못 봤다. medikit 번들이 로컬에 없고, 배포 화면(`ccc.medisolveai.xyz`)도 열지 않았다(브라우저 도구 없음 · 로그인 금지). 값은 전부 코드를 읽어서 옮겼고, 장면은 node 로 확인했다

## 1. 코드 대조표

경로 앞부분 `cc/front/` 는 뺐다.

| 시안 값 | 코드 파일:줄 | 시안 |
|---|---|---|
| 헤더 높이 | `components/common/AppHeader.tsx:13` `HEADER_H = 57` | 57px · 아래 화면 `calc(100vh - 57px)` |
| 헤더 틀 | `AppHeader.tsx:60-76` | `bg-ms-white border-ms-gray-200` · 좌우 28 · 아래 테두리 1 · sticky z30 |
| 로고 · 메뉴 간격 | `AppHeader.tsx:77,80,83` | 로고 22px · 로고↔메뉴 48 · 메뉴 사이 40 |
| 메뉴 글자 | `AppHeader.tsx:89` | 현재 `text-typo-heading-md-500 text-primary` · 나머지 `heading-md-400 text-ms-gray-800` |
| 메뉴 배열 | `AppHeader.tsx:16-20,36` `NAVS` · 데스크는 내 스케쥴 뺌 | `현황판 \| 시술 현황 \| 예약관리`(데스크 계정 기준 · 「시술 현황」 한 칸 추가 · 현재 = 시술 현황) |
| 헤더 오른쪽 | `AppHeader.tsx:100-108,48,54` | 시각 `heading-sm-400 text-ms-black` · 지점 `heading-sm-400 text-ms-gray-700` · 「데스크」 `heading-sm-400 text-primary` · 로그아웃 `heading-sm-400 text-ms-gray-700` · 간격 16 |
| 왼쪽 사이드바 | `app/(main)/desk/page.tsx:23-29,131` medikit `Menu` | `MedisolveAiMedikit.Menu` · `menus` 꼴 같음(묶음 1 · 항목 1 · 아이콘 같은 path) · 이름만 「시술 현황」 · 폭은 medikit 기본(1·2차 시안 `hint-size` 274px) |
| 바탕 · main 여백 | `desk/page.tsx:128,133-142` | `var(--ms-gray-100)` · main 패딩 20/28 · 간격 12 · overflow hidden |
| 제목 줄 | `desk/page.tsx:144-151` | `h1 text-typo-title-md-600 text-ms-gray-800` 「시술 현황」 + `body-400 text-ms-gray-600` 「명동점 · 마지막 KOS 동기화 14:45:08」 |
| 범례 | `desk/page.tsx:165-176` | 14×10 · 반경 3 · 테두리 1 · `BOX` 색 + `caption-md-400 text-ms-gray-700` · 구분선 `bg-ms-gray-300` 1×14 |
| [입실순 \| 배치순] | 코드에 없음 — 가장 가까운 `desk/page.tsx:178` `Button size=sm` 사용 | Button sm 둘 · 고른 쪽 `solid blue` · 나머지 `outlined gray` |
| 가운데 판 | `desk/page.tsx:198-209` | `bg-ms-white` · 반경 12 · 패딩 12 · 그림자 `0 2px 10px rgba(0,0,0,.04)` · overflow auto |
| 카드 격자 | `components/desk/FloorGrid.tsx:127-141` | `bg-ms-gray-100` · 반경 8 · 패딩 6 · 간격 6. 열은 도면 8칸 대신 `auto-fill minmax(220px,1fr)` — 도면이 아니라서(코드에 없음) |
| **카드 = 방 칸** | `FloorGrid.tsx:218-230` | 테두리 1 solid · **반경 6** · **패딩 6/8** · 간격 4 · `cc-room` hover 그림자(`app/globals.css:37`). **색 띠 없음** |
| 카드 색 | `lib/board.ts:37-42` `BOX` · `:50` | 시술 대기 = `BOX.wait`(노랑) · 마취 중 = `BOX.consult`(보라) · 시술 진행 = `BOX.treat`(파랑) · 확인 필요 = `BOX.need`(빨강) · 귀가 대기 = `bg-ms-gray-100 border-ms-gray-300 text-ms-gray-600`(`Aside.tsx:535` 「귀가」 칸) |
| 카드 머리 | `FloorGrid.tsx:239-249,170-172,191-193` | 방 이름 `caption-md-600` · 상태 `caption-md-500 text-ms-gray-700`(확인 필요면 `caption-md-600 text-red`) · 둘째 줄 `caption-md-400 text-ms-gray-700` |
| 고객 줄 | `FloorGrid.tsx:30-37,273` | 점 7px `#3e3e3e`(`ROLE_COLOR.고객`) + `caption-md-600 text-ms-gray-800` · 줄임표 |
| 국적 칩 | `Aside.tsx:584-585` | `bg-ms-gray-200 caption-md-500 text-ms-gray-700` · 패딩 1/6 · 반경 4 |
| 첫내원 · 재내원 칩 | `Aside.tsx:627-637` `VisitChip` | 첫내원 `bg-primary-100 text-primary caption-md-600` · 재내원 `bg-ms-gray-200 text-ms-gray-700 caption-md-600` |
| 오더 메모 | `lib/memo.tsx:124-160` `MemoCard` | `bg-ms-white border-ms-gray-200` · 반경 8 · 패딩 8/10 · 제목 `caption-md-600 text-ms-gray-700` · 본문 `body-400 text-ms-gray-800` · **3줄 · 120자 넘으면 3줄로 접고 [펼치기 · 접기]**(`caption-md-500 text-primary`) |
| 마취 중 | `lib/board.ts:26` Badge variant `purple` | `Badge purple sm dot` 「마취 중 05분 경과」 |
| 시술 줄 | `Aside.tsx:254` 단계 줄 · `lib/board.ts:94-108` `stepNum` | 격자 `18px 1fr auto` · 간격 8 · 이름 = 완료 `caption-md-400 text-ms-gray-500` / 진행 `caption-md-600 text-primary` / 대기 `caption-md-400 text-ms-gray-800` · 오른쪽 `caption-md-400 text-ms-gray-500`(진행 · 호출은 `caption-md-500 text-primary`) |
| 체크칸 | `components/desk/CheckInModal.tsx:150-163` · `lib/board.ts:90-91` `checkBox` | 18×18 · 반경 4 · 테두리 1 · ✓ 12px 700 |
| 카드 버튼 | `desk/page.tsx:178` | `Button size=sm` — [마취 시작] outlined gray · [마취 종료] solid blue · [의사 호출] outlined gray · [귀가 대기] solid blue(전부 끝났을 때만 · 아니면 disabled) |
| 카드 강조 | `FloorGrid.tsx:231-234` 동선 표시 | 지금 = `2px solid var(--ms-primary)` · 대기 = `2px dashed` · offset 2 · 나머지 흐림 0.45 |
| 귀가 대기 흐림 | `Aside.tsx:560` 노쇼 0.55 | 0.55 · 맨 뒤 |
| 오른쪽 패널 | `components/desk/Aside.tsx:115-136` | `bg-ms-white` · **폭 340** · 반경 12 · 그림자 `0 0 10px rgba(0,0,0,.09)` |
| 고객 검색 | `Aside.tsx:147-154` · `globals.css:21-36` `.cc-input` | 패딩 12/16/0 · 높이 40 · 14px |
| 탭 | `Aside.tsx:171-172` medikit `Tabs` | 패딩 8/16/0 · 탭 = **현황 · 원장 · 고객** |
| 상태 수 카드 | `Aside.tsx:21-69` `SummaryCards` | 3열 · 간격 8 · 바깥 16/16/12 · 칸 반경 8 · 테두리 1 · 패딩 8/10 · 이름 `caption-md-500` · 수 `title-sm-600` |
| 구분선 | `Aside.tsx:311` | `border-ms-gray-200` 위 1 |
| 손이 필요한 고객 카드 | `Aside.tsx:312-360` StatusTab 카드 | 목록 간격 8 · 패딩 12/16 · 카드 `bg-ms-white border-ms-gray-200` 반경 10 · 패딩 10/12 · 간격 6 · `Badge danger sm dot` 「확인 필요」 + 방 `body-600` · 담당 `caption-md-500 text-ms-gray-700` · 이름 `body-500` · 두 줄 `body-500` / `elapsedCls`(`caption-md-600 text-red`) |
| 원장 탭 줄 | `Aside.tsx:181-216` 직원 탭 | 패딩 12/16 · 아래 테두리 · 점 8px `#ac47ff`(`ROLE_COLOR.의사`) · 이름 `body-600` · 직군 `caption-md-400` · 「지금 / 대기」 격자 `28px 1fr` · 고른 줄 `bg-primary-100` |
| 고객 탭 줄 | `Aside.tsx:226-287` 고객 탭 | 같은 줄 틀 · `Badge sm dot` + 이름 + 방 · 번호 원 18px(`stepNum`) |
| 검색 결과 줄 | `Aside.tsx:441-466` | 최소 높이 52 · 패딩 8/16 · 이름 `body-600` + VisitChip · 오른쪽 `caption-md-500 text-ms-gray-600` |
| 의사 호출 모달 | `CheckInModal.tsx:77-86,93,126-138,253-262` | medikit `Modal` · 폭 `min(560px, 100vw-64)` · 간격 16 · 제목 `title-sm-600` · 소제목 `caption-md-600 text-ms-gray-700` · 고르기 줄 `pickCls`(`lib/board.ts:88`) 반경 8 · 패딩 10/12 · 버튼 [취소] outlined gray · [호출] solid blue(기본 크기) |
| 토스트 | `desk/page.tsx:283-302` | `bg-ms-gray-800 text-ms-white` · 반경 10 · 아래 28 · `body-500` |

코드에 없어서 가장 가까운 것을 쓴 값:

- 정렬 토글 → Button sm 두 개
- 카드 격자 열 → `minmax(220px,1fr)` 자동 채움(도면 8칸이 아니라서)
- 원장 · 호출 모드 고르기 → `pickCls` 고르기 줄(라디오가 코드에 없음)
- 「마취 중」 색 → `BOX.consult` · Badge `purple`(현황판에서는 「상담」 색)
- 「호출함」 칸 → `Aside.tsx:532` 「전체」 칸 흰색
- 원장 직군 글자 → 직원 탭과 같이 「의사」

## 2. 피드백 #1~#4 반영

| # | 피드백 | 반영 |
|---|---|---|
| 1 | 현황판과 같은 3단 · 테마 | AppHeader 그대로(HTML 로 옮김 — medikit `Header` 를 쓰지 않는다. 코드도 안 쓴다) · 왼쪽 medikit `Menu` · 가운데 흰 판 + 회색 격자 · 오른쪽 `Aside` 340. v1 의 자체 클래스(`pb-*`)와 자체 색은 전부 뺐다 |
| 2 | 글자 크기 · 컴포넌트 코드와 같게 | 위 대조표의 클래스만 쓴다. 컴포넌트는 medikit `Menu · Tabs · Badge · Button · Modal` 다섯 개 + 코드의 `MemoCard · VisitChip · SummaryCards · pickCls · checkBox · stepNum` 모양 |
| 3 | 카드 = 기존 카드 · 컴팩트 · 색 띠 없음 | 카드 = FloorGrid 방 칸(반경 6 · 패딩 6/8 · 간격 4 · 상태 바탕색). 윗선 색 띠 없음. 시술 줄 한 줄(체크 · 이름 · 「원장 · 시각/상태」). 메모는 3줄로 접힘. 버튼 sm |
| 4 | 오른쪽 패널 = Aside · 탭 현황 · 원장 · 고객 | 검색 → 검색 결과(누르면 고객 탭 · 그 고객 선택). **현황**: 상태 수 5칸(시술 대기 · 마취 중 · 호출함 · 시술 진행 · 귀가 대기) + 「손이 필요한 고객」(호출 미수락 · 마취 길어짐 · 시술 다 끝나 귀가 대기 전). 누르면 가운데 그 카드에 실선 강조. **원장**: 원장마다 시술 중/대기 · 지금(방 · 시술 · 고객) · 대기(호출 받음 포함). 누르면 그 원장 카드 실선/점선 · 나머지 흐림. **고객**: 오늘 시술 고객 전체(가운데와 같은 순서) · 시술 번호 원 줄. 누르면 그 카드만 남기고 흐림 |

## 3. 장면

| scene | 값(node 출력) |
|---|---|
| `board` | 입실순 A-룸2(파랑) → 5(파랑) → 4(빨강 · 「호출함 · 전체 · 수락 전」 「호출 5분 경과」) → 1(노랑) → 3(빨강 · 「마취 중」 「마취 23분 경과」) → 6(회색 0.55). 수 3 · 1 · 2 · 2 · 1. 손이 필요 = A-룸3 · A-룸4 |
| `board-placement` | A-룸1 → 6 · [배치순] solid |
| `memo-expanded` | A-룸2 메모 3줄 접힘 풀림 · 「접기」 |
| `call-modal` | A-룸1 · 시술 3개 선택 · [전체 호출] 고름 · 버튼 「전체 호출」 |
| `call-modal-specific` | 리쥬란 힐러 2cc 만(「1개 선택」) · [특정 의사 선택] · 원장 4명(박 · 이 「시술 중」, 최 · 정 「대기」) 중 최 원장 · 버튼 「최 원장 호출」 |
| `all-done` | A-룸2 4/4 완료 → 빨강 「시술 모두 완료 · 귀가 대기 전」 · [귀가 대기] solid · 손이 필요에 추가 |
| `panel-doctors` | 원장 탭 · 박 원장 선택 → A-룸2 실선 · 나머지 0.45. 박 「시술 중」 / 이 「시술 중」 / 최 「대기 1건(A-룸5 바디보톡스 호출 받음)」 / 정 「대기」 |
| `panel-customers` | 고객 탭 · A-룸5 선택 → 그 카드 실선 · 나머지 0.45 · 6줄(귀가 대기 0.55) |

## 4. v1 대비 크기 (추정 — 렌더 못 봄 · 클래스 줄 높이로 셈)

| | v1 | v2 |
|---|---|---|
| 카드 폭 | 최소 300 · 본문 전체 폭 | 최소 220 · 가운데 판 안 |
| 카드 높이(A-룸2 · 시술 4 · 긴 메모) | 약 500px | 약 340px(메모 3줄로 접힘 · 시술 줄 22px) |
| 시술 3개 · 짧은 메모 | 약 430px | 약 280px |
| 1440×900 한 화면 | 4열 × 약 1.4줄 → 온전히 보이는 카드 4장 안팎 | 가운데 약 720px → 3열 × 2줄 → **6장 안팎** |
| 1280×800 | 3열 × 1줄 → 3장 | 가운데 약 560px → 2열 × 2줄 → 4장 |

사이드바 274 + 패널 340 이 폭을 먹기 때문에 열 수는 v1 보다 적다. 대신 카드가 짧아져서 한 화면에 들어가는 카드 수는 v1 보다 많다.

## 5. v1 과 달라진 것 · workflow 와 다른 점 (사실만)

1. 신규/재방문 → 코드 문구 **첫내원/재내원**(`VisitChip`)
2. 오더 메모 접힘 규칙: v1 「4줄 · 140자 · 높이 92px 스크롤」 → 코드 `MemoCard` 「3줄 · 120자 · 3줄 자르기」. 스크롤이 아니라 줄 자르기다
3. 카드 색이 고객 상태를 따른다. 손이 필요하면 빨강(확인 필요)이 먼저다(FloorGrid `boxKey` 와 같은 순서). 그래서 board 에서 마취 23분 카드(A-룸3)는 보라가 아니라 빨강이다. 보라는 [마취 시작]을 누른 직후처럼 20분 전인 경우에만 보인다
4. 헤더 사용자 칸 = 「데스크」(코드는 데스크 계정 · 직원 계정 둘뿐). v1 의 「간호 스테이션」은 뺐다
5. 상태 수 5칸이 서로 겹친다 — 시술 대기 고객이 「마취 중」이나 「호출함」에도 함께 세진다
6. 「손이 필요」 기준 수치(호출 5분 · 마취 20분)는 코드 · workflow 어디에도 없다. 마취 20분은 workflow 의 「기본 20분」에서 가져왔다
7. 손이 필요한 카드의 담당 칸은 원장이 없으면 「미배정」이다(`Aside.tsx:371` `ownerOf` 와 같은 말)
8. 검색은 시술 고객 이름(영문)만 찾는다. 한글 읽기 · 전화번호는 데이터에 없다
9. v1 에서 넘어온 것(그대로): 시술 진행 카드는 마취 버튼 없음 · 진행 중에도 [의사 호출] 가능 · 방 · 입실 시각은 카드에 하나

## 6. 정할 것

| 항목 | 시안에 둔 것 |
|---|---|
| 「시술 현황」 헤더 메뉴 자리 · 경로 · 어느 계정에 보이나 | 현황판 다음 · `/procedures` · 데스크 계정 |
| 사이드바 묶음 · 항목 이름 | 「시술 현황」 > 「시술 현황」(현황판의 「현황판 > 실시간 현황판」 꼴) |
| 간호 스테이션 로그인 계정 | 데스크 계정 |
| 「마취 중」 색 = 현황판 「상담」 보라를 빌림 | 보라 |
| 손이 필요 기준 — 호출 미수락 몇 분 · 마취 몇 분 | 5분 · 20분 |
| 정렬 토글 모양(코드에 없음) | Button sm 두 개 |
| 오더 메모 접힘 — MemoCard 3줄 자르기 vs v1 일정 높이 + 스크롤 | MemoCard |
| 상태 수 5칸이 겹쳐 세지는 것 | 겹침 허용 |
| 고객 탭 범위 — 오늘 시술 고객 전체 = 귀가 대기 포함? 귀가(COMPLETED) 포함? | 귀가 대기까지 · 귀가는 없음 |
| v1 정할 것 12건 | 그대로 이어 간다(`design-report.md` §정할 것) |

## 7. 검증

1. **목록** — `list_files` 45 → **46**. 늘어난 것은 `Ceramique 시술현황판 v2.dc.html` 하나다. v1 포함 기존 파일은 그대로다
2. **다시 받기** — `get_file` `truncated:false`. 받은 내용이 로컬 사본과 **바이트 단위로 같다**(52,632 bytes · sha256 `4e8606d9bcb3…` 같음)
3. **node** — 스크립트를 DCLogic 대역으로 돌렸다. 8개 장면의 값은 §3 표와 같다. 조작:
   - A-룸1 [마취 시작] → 보라 · [마취 종료] · 수 3/2/2/2/1
   - 손이 필요 카드 클릭 → 가운데 그 카드 실선
   - 원장 탭에서 최 원장 → A-룸5 점선 · 나머지 0.45
   - 검색 「tanaka」 → 1건 → 누르면 고객 탭 · 그 고객 선택 · 검색어 비움. 「zzz」 → 「검색 결과 없음」
   - 모달: 특정 의사 · 원장 안 고르면 막힘 → 박 원장 → 보내기 → 세 줄 「호출함 · 지정 박 원장」 · 토스트
   - 미완료 [귀가 대기] 막힘 · 메모 [펼치기]
   - `all-done` 에서 [귀가 대기] → A-룸2 회색 0.55 맨 뒤 · 수 3/1/2/1/2
4. **사람 이름 0** — 고객은 v1 의 영문 가짜 이름, 원장은 성만(박 · 이 · 최 · 정)이다. grep 결과는 아래와 같다
   - `grep -nE "010-|\+82"` → 0건
   - `grep -nE "[가-힣]{3} ?(원장|코디|간호사)"` → 시안 0건
