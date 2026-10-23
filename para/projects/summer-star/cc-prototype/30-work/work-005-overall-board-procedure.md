---
type: work
id: WORK-005
title: "전체현황판 — 「현황 › 시술 현황」 시안 반영 · 카드 드래그 순서 저장 · 「방 배정」 줄 빼기"
status: draft
product: cc-prototype
feature: procedure
work_type: new-feature
owner: kknaks
progress: 0
created_at: 2026-10-23
updated_at: 2026-10-23
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/work
  - status/draft
links:
  baselines:
    - "[[baseline-008-procedure-board|BASE-008]]"
  decisions:
    - "[[decision-005-procedure-board|DEC-005]]"
  specs:
    - "[[spec-003-procedure-board|SPEC-003]]"
  works:
    - "[[work-003-procedure-board|WORK-003]]"
  releases: []
  related: []
sources:
  - "orchestration/work/overall-board/_RESUME.md §2 (2026-10-23 결정 줄)"
  - "reference/2026-10-23-cc-overall-board/design/Ceramique 전체현황판.dc.html"
  - "orchestration/work/overall-board/design-analysis-report.md"
  - "orchestration/work/overall-board/current-board-report.md"
---

# 전체현황판 — 시술 현황 시안 반영

배포된 시술 현황판(`procedure/` · `ccc.medisolveai.xyz`)을 「Ceramique 전체현황판」 시안의 **「현황 › 시술 현황」 하위 화면**으로 바꾼다. 계약은 **SPEC-003 0.4.0**(부록 E 가 `_RESUME 10-23` 결정 줄 → 절 대응표) — 이 문서는 빌드 계획만 적고 계약을 다시 쓰지 않는다.

> 1 파일 = 1 work = **빌드 계획**. 결정 원천 = `orchestration/work/overall-board/_RESUME.md` §2 2026-10-23 줄 · 화면 정본 = 전체현황판 시안(`M:63-92` · `M:777-1153`).

## Meta

- Covers spec: SPEC-003 0.4.2(r3 · §1 · §3.2 · §5.1 · §5.9 · §5.12 · §6.2 ~ §6.4 · §6.7 · §7.2 ~ §7.5 · §9 #10 · #12 ~ #17 · §10)
- 코드 레포: `kknaksss/cc-prototype` — 범위 `procedure/back/**` · `procedure/front/**`. **`procedure/app/`(시술실 앱) · KOS 쓰기(§8) · infra 는 건드리지 않는다**
- slug: `overall-board` · 코드 워크트리 `cc-prototype/overall-board`(브랜치 `kknaksss/overall-board` · base `origin/main`) · 워커: backend · frontend · reviewer
- 순서 원칙: **계약 고정점(아래)은 SPEC-003 0.4.2 로 이미 고정**(역할 표 = SPEC-004 0.3.1 §3.4) → back(WP-BE1 · WP-BE2)과 front(WP-FE1 · WP-FE2)가 병렬 → 리뷰 + 코디 E2E(WP-E2E)
- 검증은 WP 마다 그 범위만. 전체 검증(`make` 급 · compose · 데모 지점)은 WP-E2E 에서 한 번
- 배포: 이번 문서 범위 밖 — 사용자 E2E 통과 뒤 코디가 따로 정한다(WORK-004 WP10 과 같은 길)

## 계약 고정점 — BE ↔ FE 병렬의 기준

| 고정점 | 값 | SPEC-003 |
|---|---|---|
| 순서 저장 API | `PUT /api/board/order` · 본문 `{visitIds:[StrictInt,…]}`(문자열 · 실수 · 불리언 400 — r2)(귀가 대기 아닌 카드 전체 새 순서 · 빈 배열 허용) · 응답 `{ok:true, visitIds:[…]}` · 400 `invalid_request`(형식 · 같은 id 두 번) · 401 · 403 `fake_board` · 없는 id 는 오류 없이 거름 | §7.3 · §5.12 |
| 스냅샷 순서 | **`cards[]` 배열 순서 = 화면 순서**(새 필드 없음) — 목록 순 → 목록 밖 입실순 → 귀가 대기 맨 뒤 귀가 대기 시각 순 | §7.2 · §5.12 |
| 「방 배정」 | `procedures[]` 에 방 있는 `etc` 가 **없다**(남는 `etc` = 방 없는 기타 작업) · 필드 모양 그대로 | §5.1 · §7.2 |
| `cards[].kos` | 그대로 실림(웹은 안 그림) | §7.2 · §6.3 |
| SSE | 순서 저장 직후 `board` 1개(§7.5 ①) | §7.5 |

스키마(`schemas/board.py` · `front/lib/types.ts`)의 **필드 이름 · 모양은 바뀌지 않는다** → front 는 back 을 기다리지 않고 WP1 의 가짜 보드(`PROC_FAKE_BOARD`)로 그린다. 순서 API 만 front 가 새로 부른다. **가짜 보드에서는 `PUT` 이 403 `fake_board` → 일반 오류와 같이 토스트 + 스냅샷 순서로 돌아간다(예외 없음 · SPEC-003 §6.3).** 그래서 FE 는 가짜 보드에서 **미리보기 · 놓은 직후 로컬 순서**까지만 확인하고, 「놓은 뒤 순서 유지 · 다른 화면 공유」는 WP-E2E(데모 지점)에서 본다 (r2 — review r1 F2 (c))

## Work Packages

| WP | 내용 | 계약 | 워커 | 대상 파일(범위) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| WP-BE1 | **「방 배정」 거르기** — `Rules.items`(「카드에 보이는 작업」)에서 `kind = etc` 이고 `room_kos_id` 있는 작업을 뺀다(방 있는 ETCETERA 전부 · OQ-511 여럿 포함). 판정은 `kos/sync.py` `_room_task` 와 같은 뜻(ETCETERA + room) — 한 곳에 이름 붙인 함수로. [귀가 대기] 취소 대상(`open_task_seqs` 기반) · 호출 전 방 넣기(`visit.room_id`)는 **바꾸지 않는다**. 가짜 보드(`service/fake_board.py`)의 「방 배정」 예시를 방 없는 기타 작업 예시(예: 「시트팩」)로 바꾼다 | §5.1 · §7.2 | backend | `procedure/back/app/domain/rules.py` · `service/board_service.py`(필요하면) · `service/fake_board.py` · `tests/test_rules.py` · `tests/test_e2e3_home.py` | ① 방 있는 `etc` 가 스냅샷 `procedures[]` 에 없음 ② 방 없는 `etc` 는 있음(읽기 전용 · `pickable/canStart/canFinish` false) ③ [귀가 대기] `cancel-flow-tasks` 의 `sequences` 에 「방 배정」 sequence 가 그대로 들어감 ④ `canCall` · `all_done` · `paymentRequired` 결과 변화 없음 — 각각 pytest | `cd procedure/back && uv run ruff check . && uv run pytest -q tests/test_rules.py tests/test_e2e3_home.py tests/test_contract.py` | 대기 |
| WP-BE2 | **드래그 순서 저장** — 표 `board_order`(§3.2 · `repository/db.py` `SCHEMA` 에 `CREATE TABLE IF NOT EXISTS` — 기존 DB 파일에 ALTER 없음) · repository 읽기/쓰기 · service 순서 저장(거르기: 지금 카드 · 귀가 대기 아님 · 오늘 KST · 중복은 400) → `event_log(board_order)` 1줄 · `kos_op` 0줄 · 트랜잭션 하나 · router `PUT /api/board/order`(Bearer · `fake_board` 403 · 역할 = 세 역할 모두 — SPEC-004 §3.4 표 줄(r2) · `visitIds` = StrictInt) · 저장 뒤 SSE 발행 · 스냅샷 정렬을 §5.12 로 바꿈(`board_service.snapshot` 의 `cards.sort`) · 날짜 바뀌면 순서 없음 | §3.2 · §5.12 · §7.2 · §7.3 · §7.5 | backend | `procedure/back/app/repository/{db,repo}.py` · `service/{actions,board_service}.py`(또는 새 `service/order.py`) · `api/board.py`(또는 `api/actions.py`) · `schemas/actions.py` · `domain/errors.py`(필요하면) · `tests/test_order.py`(새) · `tests/test_stream.py` · `tests/test_auth_roles.py` | SPEC-003 §9 끝 「0.4.0 더함」 시험 전부 통과: 저장 · 거르기(없는 id · 귀가 대기 · 사라진 카드) · 400 형식 · 같은 id 두 번 · 마지막 쓰기 · `event_log` 1줄 · `kos_op` 0줄 · 저장 뒤 SSE 1개 · 401 · 403 `fake_board` · StrictInt(`"3"` · `3.0` · `true` → 400) · 정렬(목록 → 목록 밖 입실순 → 귀가 대기 시각 순 · 다음 날 순서 없음). **옛 스키마 DB 시험** `tests/test_order.py::test_old_schema_db_keeps_rows` — 0.3.0 `SCHEMA`(board_order 없음)로 만든 SQLite 파일에 visit 행 하나를 넣고 지금 초기화를 돌리면 `board_order` 가 생기고 그 visit 행이 남는다 (r2). 경로 수 17(§7.4) | `uv run ruff check . && uv run pytest -q tests/test_order.py tests/test_stream.py tests/test_auth_roles.py tests/test_contract.py` | 대기 |
| WP-FE1 | **헤더 · 틀 · 제목 줄 · 패널** — `AppHeader`: 상단 메뉴 「현황」 하나 + 호버 드롭다운(「시술 현황」 한 항목 → `/procedures/live` · 시안 `M:70-78` 치수) · 오른쪽 시계 · 지점 · 계정(`name` 그대로) · 로그아웃. 현황판 페이지: **medikit `Menu` 사이드바 제거** · 제목 줄 = 「시술 현황」 · 「마지막 KOS 동기화 HH:MM:SS」(「명동점 · 」 앞머리 제거) · 조회 시간 밖 · 동기화 실패 · 범례 5 · **[입실순 \| 배치순] 제거**. Aside 고객 탭 줄 순서 = 카드 순서(스냅샷 `cards[]` · 경합 중 로컬 — `orderedCards(board.cards, sort)` 제거 · SPEC-003 §6.4 · 시안 `M:1591`) (r3) · Aside 현황 탭 6칸 = 3 × 2 · 점 · 칸 바탕 없음 · 왼쪽 구분선(§6.4 · `M:945-955`). 좁은 화면(760 미만) 규칙 그대로 | §6.1 · §6.2 · §6.4 · §6.7 #5 · #14 · #16 · #17 · #18 | frontend | `procedure/front/components/common/AppHeader.tsx` · `app/(main)/layout.tsx` · `app/(main)/procedures/live/page.tsx` · `components/procedures/Aside.tsx` · `components/procedures/view.ts`(필터 칸 정의) | **frontend 가 가짜 보드(`PROC_FAKE_BOARD`) 화면 스크린샷을 보고서에 붙인다** — 장면: 헤더(드롭다운 펼침) · `board` · `panel-customers` · `narrow`. **reviewer 가 시안 같은 장면**(헤더 `M:63-92` · 제목 줄 `M:781-800` · 현황 탭 `M:944-990`)과 대조해 같음 (r2) · 사이드바 · 정렬 버튼 · 「명동점 · 」 0 · 다른 상단 메뉴 5개 · 예약 · 원내 현황 항목 0 | `cd procedure/front && npx tsc --noEmit && npm run lint && npm run build` · `grep -rnE --include='*.ts' --include='*.tsx' "SortKey\|배치순\|입실순" procedure/front/{app,components,lib} \| wc -l`(표 안이라 파이프를 `\|` 로 적음 — 실행 때는 역슬래시 없이) = **0** · `grep -rnE --include='*.ts' --include='*.tsx' "\bMenu\b" procedure/front/{app,components}` = **0**(medikit `Menu` import · 사용 없음 — 복사 테마 CSS `medikit-patches.css` 의 `[Menu-n]` 주석은 SPEC-003 §2.4 「그대로 복사」라 대상 밖) (r3) | 대기 |
| WP-FE2 | **카드 · 드래그** — `OrderCard`: 머리 한 줄(방 · Badge / 입실) · **경과 글자 줄 · 「KOS 반영 중/실패」 줄 제거** · 고객 줄 시안 글자 · 시술 줄 순서 진행 → 대기 → 완료 + 완료 앞 점선(`view.ts` `orderedProcs`) · 방 없는 `etc` 줄은 맨 위 읽기 전용 그대로(스냅샷에 「방 배정」이 안 오므로 front 는 거르지 않는다). 카드 순서 = 스냅샷 `cards[]` 그대로(`orderedCards` 정렬 제거). **드래그**: 놓기 = **방향 따라**(**드래그 시작 때의 전체 순서**에서 대상보다 앞이던 카드 → 대상 뒤 · 뒤이던 카드 → 대상 앞 · 미리보기도 같은 기준 — 미리보기로 바뀐 순서로 다시 판정하지 않음 — SPEC-003 §5.12 (r2 · r3)) · 경합 규칙 = SPEC-003 §5.12 「놓은 뒤 화면」(마지막 요청만 · 응답까지 로컬 · 응답 `visitIds` 에 든 카드끼리의 차례가 스냅샷과 같은 첫 스냅샷부터 서버(새 카드 · 그사이 귀가 대기 · 사라진 카드는 비교에서 뺌) · 그사이 귀가 대기가 된 카드는 로컬 순서에서 빼고 귀가 대기 묶음으로 · 3초 · 실패면 바로 스냅샷 (r2 · r3)) · 귀가 대기 아닌 카드만 `draggable` · 끄는 카드 0.35 + primary 2px 그림자 · 다른 카드 위 = 미리 옮겨 그림 · 놓으면 로컬 순서 → `PUT /api/board/order`(전체 순서 · 필터로 숨긴 카드 포함) → 다음 스냅샷으로 교체 · 실패면 오류 토스트 + 스냅샷 순서 · 귀가 대기 카드 위에 놓기 무시 · 불투명도 우선순위(끄는 중 0.35 → 귀가 0.55 → 강조 밖 0.45). `lib/api.ts` 에 `putBoardOrder` | §5.9 · §5.12 · §6.3 · §6.4(고객 탭 순서) · §6.7 #8 · #11 · #13 · #15 · #19 ~ #22 (r3) · §7.3 | frontend | `procedure/front/components/procedures/OrderCard.tsx` · `components/procedures/view.ts` · `app/(main)/procedures/live/page.tsx` · `lib/api.ts` · `lib/types.ts`(요청 · 응답 타입만) | frontend 스크린샷(가짜 보드 — 카드 `board` · `all-done` · 드래그 중 미리보기 · 놓은 직후 로컬 순서)을 보고서에 붙이고 reviewer 가 시안 카드(`M:808-905`) · 드래그 표시(`M:1464-1475`)와 대조해 같음. 놓기 위치는 방향 따라(§6.7 #21 — 시안과 다른 점) · 가짜 보드에선 놓은 뒤 403 토스트 + 원래 순서로 돌아가는 것이 맞는 동작(유지 · 공유 확인은 WP-E2E) (r2) · 귀가 대기 카드 끌기 안 됨 · 「KOS 반영」 · 경과 글자 · 「방 배정」 줄 0 · 방 없는 `etc` 줄 남음 · `cc/` import 0 | `npx tsc --noEmit && npm run lint && npm run build` · `grep -rn "KOS 반영" procedure/front/components` 0 | 대기 |
| WP-E2E | **리뷰 + 코디 E2E(데모 지점)** — reviewer: SPEC-003 0.4.2 ↔ 코드 대조(부록 E 의 절 전부 · §6.7 #11 ~ #22(#21 방향 따라 · #22 [의사 호출]) (r3) · OQ 기본값이 코드에 그대로인지). FAIL 은 모아서 한 번에 수정 발주. 코디: 백엔드 커밋 뒤 **compose 다시 올리고** 데모 지점 연결 → SPEC-003 §9 0 ~ 17 단계(브라우저 2개 · 새로고침 없이 같은 순서). **0 단계 준비에 방 없는 ETCETERA(마취 · 시트팩 등) 1개 이상 필수** — 데모 환자에 없으면 KOS 화면에서 붙이고, 못 만들면 기록하고 사용자에게 알린다(§9 #13 필수 확인) · 드래그 놓은 뒤 유지 · 공유 · 방향 따라(§9 #14) (r2) → 사용자 E2E(사용자 표면 · 피드백은 모아서 한 batch) | §9 | reviewer · 코디(진행) · backend · frontend(수정) | `procedure/back/**` · `procedure/front/**` | 리뷰 PASS · 코디 §9 #0 ~ #17 통과 · 사용자 E2E 통과 | `cd procedure/back && uv run ruff check . && uv run pytest -q` · `cd procedure/front && npx tsc --noEmit && npm run lint && npm run build` · `cd procedure && docker compose up --build` | 대기 |

## 병렬

```text
(SPEC-003 0.4.2 = 계약 고정)
 ├─ WP-BE1 ── WP-BE2 ─────────┐
 └─ WP-FE1 ── WP-FE2 ─────────┴─ WP-E2E
```

- **BE ↔ FE 병렬 가능** — 스냅샷 필드 모양이 그대로이고(배열 순서 · 「방 배정」 빠짐은 값 차이뿐) 새 API 하나의 모양이 위 고정점에 박혀 있다
- WP-BE1 · WP-BE2 는 같은 back(`rules.py` · `board_service.py` 를 둘 다 만진다) → 한 워커가 차례로. WP-FE1 · WP-FE2 도 같은 `live/page.tsx` 를 만진다 → 한 워커가 차례로
- 모양을 바꿔야 하면 SPEC-003 §7 을 먼저 고친다(코디 → planner) → 양쪽 다시 맞춤

## 하지 않는 것

- 예약 현황 · 원내 현황 화면 · 다른 상단 메뉴 5개 · 경로 바꾸기(`/live/*`) — SPEC-003 §1.2 · OQ-520 · OQ-524
- 시술실 앱(`procedure/app/`) — 앱은 자기 입실순 정렬 그대로(OQ-523) · 스냅샷 모양이 안 바뀌어 앱 빌드도 필요 없다
- KOS 쓰기(§8) · 조회 루프 · `kos_op` 대기열 — 순서는 KOS 에 보내지 않는다
- 비동기 KOS 반영 실패 알림(OQ-522) · 경과 글자 되살리기(OQ-521) · 계정 표시 역할 글자(OQ-514) — 열린 것
- 터치 드래그(태블릿) — 시안에 없음

## 주의

- public 레포(코드 · 문서 모두) — KOS 키 · 토큰 · 비밀번호 · 계정 이메일 · 실명 · KOS id 값을 코드 · 시험 데이터 · 커밋에 넣지 않는다. **전체현황판 시안의 공지 예시 · 직원 이름(실명)을 코드 · 가짜 보드 · 시험에 옮기지 않는다** — 가짜 값은 지어낸 것으로
- 실 데모 지점에서 쓰기는 기존 조작만(순서 저장은 KOS 에 안 간다). 운영 명동점 키 금지(D-06)
- 워커는 사용자 포트(3600 · 8600 · 3700 · 8700)에 떠 있는 사용자 프로세스를 죽이지 않는다
- 백엔드 커밋 뒤 compose 를 다시 올리고 E2E(옛 코드가 떠 있는 채로 확인 금지)
- 배포 DB 는 PVC 의 기존 SQLite 파일 — 새 표는 `CREATE TABLE IF NOT EXISTS` 로만 더한다(기존 표 · 열을 바꾸지 않는다)

## 열린 것 (2026-10-23)

| 무엇 | 지금(기본값) | 근거 |
|---|---|---|
| 드롭다운에 예약 · 원내 현황 항목 | 그리지 않음 | SPEC-003 OQ-520 |
| 카드 경과 글자 되살리기 | 안 그림(시안대로) | SPEC-003 OQ-521 |
| 비동기 KOS 반영 실패의 웹 알림 | 없음 | SPEC-003 OQ-522 |
| 앱도 공유 순서를 따르나 | 앱 그대로(입실순) | SPEC-003 OQ-523 |
| 경로 `/live/*` | `/procedures/live` 그대로 | SPEC-003 OQ-524 |
| 전날 순서 행 정리 | 지우지 않음 | SPEC-003 OQ-525 |
| 헤더 계정 표시 「역할 · 이름」 | `name` 그대로 | SPEC-003 OQ-514 |

## r1 처분 (r2 · 2026-10-23)

review-doc r1 FAIL 2 · WARN 12 처분은 SPEC-003 부록 F 가 정본. 이 문서에서 바뀐 곳: 고정점 표(StrictInt) · 고정점 아래 문단(F2 (c) — 가짜 보드 403 = 일반 오류) · WP-BE2(SPEC-004 §3.4 줄 · StrictInt · 옛 스키마 DB 시험 이름 — W3 · W7 · W11) · WP-FE1(스크린샷 → reviewer 대조 · grep 기대 수 0 — W11) · WP-FE2(방향 따라 · 경합 규칙 · 가짜 보드 확인 범위 — F2 · W5 · W6 · W11) · WP-E2E(방 없는 ETCETERA 준비 필수 — W10).

## r2 처분 (r3 · 2026-10-23)

review-doc r2 FAIL 1 · WARN 6 처분은 SPEC-003 부록 G 가 정본. 이 문서에서 바뀐 곳: Meta · 순서 원칙 · 병렬 그림(SPEC-003 0.4.2 · SPEC-004 0.3.1 — R5) · WP-FE1(grep 을 `.ts` · `.tsx` 로 — R1 · 고객 탭 순서 — R4) · WP-FE2(방향 판정 = 드래그 시작 순서 — R3 · 경합 ② 비교 · 그사이 귀가 대기 — R2 · 계약 칸 §6.7 #19 ~ #22 — R5) · WP-E2E(대조 범위 §6.7 #11 ~ #22 — R5).
