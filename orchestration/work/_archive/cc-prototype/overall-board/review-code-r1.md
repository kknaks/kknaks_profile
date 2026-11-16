# 리뷰 리포트 — overall-board / code r1 (2026-10-23)

## 판정: WARN — FAIL 0 · WARN 3 (사용자 결정 필요 2 포함)

- 대상: 워크트리 `cc-prototype/overall-board` 커밋 안 된 변경 — back 16 파일 + `tests/test_order.py`(새) · front 7 파일 (`git status` 23 M + 1 ??)
- SSOT: SPEC-003 0.4.2(부록 E · F · G · §5.1 · §5.12 · §6.2 ~ §6.4 · §6.7 #11 ~ #22 · §7.2 ~ §7.5 · §9 · §10) · SPEC-004 0.3.1 §3.4 · WORK-005 · `_RESUME` §2 2026-10-23 줄(27 ~ 36행) · 시안 `Ceramique 전체현황판.dc.html`
- FAIL 이 없어 BE / FE 수정 발주는 필요 없다. WARN 3개 중 W1 · W2 는 사용자가 정할 일이고, W3 은 E2E 에서 확인할 일이다

### 직접 돌린 검증

| 명령 | 결과 |
|---|---|
| `cd procedure/back && uv run ruff check .` | All checks passed |
| `uv run pytest -q` | **155 passed**(경고 1 = starlette httpx 폐기 알림 · 기존) |
| `cd procedure/front && npx tsc --noEmit` | 통과 |
| `npm run lint` | 통과(경고 0) |
| `npm run build` | 첫 실행 `SecurityFatalError`(Next 보안 알림으로 멈춤 · exit 1) → 다시 실행하니 **통과**(라우트 5). 이미 알려진 flaky 다(`flaky-baseline-evidence.md`). 출력에 나온 `next upgrade --agent=security` 권유는 실행하지 않았다 |
| WP-FE1 grep `SortKey\|배치순\|입실순`(.ts · .tsx · app · components · lib) | 0 |
| WP-FE1 grep `\bMenu\b`(.ts · .tsx · app · components) | 0 |
| WP-FE2 grep `KOS 반영`(components) | 0 |
| 시안 실명(원장 6명 · 계정 표시 이름 1명) grep — back app · tests · front app · components · lib | 0 |
| `procedure/` 밖 변경 · 밖 import | 0 |

서버는 띄우지 않았고, 사용자 포트도 쓰지 않았다. 빌드 산출물 `.next` 는 ignore 대상이다.

---

## FAIL

없음.

## WARN

### W1 — (사용자 결정 필요) [귀가 대기]가 방 없는 기타 작업(시트팩 · 마취 · 관리 마무리)도 KOS 에서 취소한다. 이 작업들은 「전부 완료」 판정에도 들어가지 않는다
- 위치: `procedure/back/app/service/actions.py:246-247`(`cancel` = `open_task_seqs` 에서 시술 작업만 뺀 나머지 전부) · `procedure/back/app/domain/rules.py:104-106`(`all_done` 은 `kind=procedure` 만 본다). 시험 `procedure/back/tests/test_e2e3_home.py:89` 가 `sequences == [3, 4]` 로 이 동작을 굳힌다. 3 = 「방 배정」, 4 = 시트팩
- 근거: SPEC-003 §5.7(0.3.0)은 「시술 작업을 뺀 것(「방 배정」 등)을 취소」라고 적었고, 코드는 이 SPEC 과 같다 → 계약 위반은 아니다. 하지만 `_RESUME` 10-23(32행)은 「마취 · 시트팩 · 관리 마무리 등 다른 ETCETERA 는 **정당한 시술 — 남긴다**」고 했다. 화면에는 남지만, 그 작업이 「준비중」이어도 카드 아래에 [귀가 대기]가 뜨고, 누르면 KOS 에서 그 작업이 `CANCELED` 가 된다(§5.1 의 「CANCELED 는 목록에서 뺀다」에 따라 카드에서도 사라진다)
- 판정: WARN. 정할 것: ① 지금대로 둔다(SPEC 그대로) ② 취소 대상을 「방 배정」(`is_room_task`)만으로 좁힌다 ③ 방 없는 기타 작업이 끝나지 않았으면 [귀가 대기]를 막는다. ②나 ③을 고르면 SPEC §5.7 · §5.11 부터 고쳐야 한다(코디 → planner)

### W2 — (사용자 결정 필요) 카드 사이 틈이나 판의 빈 곳에 놓으면 미리보기와 달리 원래 순서로 돌아간다
- 위치: `procedure/front/app/(main)/procedures/live/page.tsx:156-166`(drop 처리는 카드에만 있다. 그 밖에서 놓으면 `onEnd` 가 `setDrag(null)` 을 해서 원래 순서로 간다) · `procedure/front/components/procedures/OrderCard.tsx:315-345`
- 근거: SPEC-003 §6.3 드래그 항목은 「다른 카드 위에 놓기」와 「끌기를 그만두기(드래그 끝 · 판 밖에 놓음) = 원래 순서」 두 경우만 정했다. 격자 틈(8px) · 패딩 · 마지막 카드 뒤 빈 칸이 판 안인지 밖인지는 정하지 않았다. 시안 `M:1464-1472` 도 카드에서만 drop 을 받으므로 코드는 시안과 같다. 문제는 미리보기다. `drag.over` 가 마지막으로 지나간 카드에 남아 있어서, 틈 위에서는 카드가 옮겨진 채로 보이다가 손을 놓는 순간 되돌아간다
- 판정: WARN. 계약이 비어 있는 자리다. 정할 것: 지금대로 둘지, 판 안 어디에 놓든 미리보기 자리로 확정할지

### W3 — 놓은 뒤 순서 유지 · 공유(경합 ② · ③)는 E2E 전까지 아무 곳에서도 돌려 보지 않았다. front 순서 함수에는 자동 시험이 없다
- 위치: `procedure/front/components/procedures/view.ts:49`(`withLocalOrder`) · `:62`(`moveCard`) · `:73`(`sameOrder`) · `page.tsx:78`(렌더 중에 「같음」을 확인) · `:88`(3초)
- 근거: WORK-005 「계약 고정점」 아래 문단(r2 F2 (c))에 따라, 가짜 보드에서는 PUT 이 403 이다. 그래서 frontend 보고서도 ①(로컬 유지) · ④(실패 복귀)만 스크린샷으로 확인했다. 방향 따라 놓기 6 경우는 Playwright 로 한 번 확인했지만 레포에 남은 시험은 없다. 코드를 읽어 본 바로는 SPEC §5.12 ① ~ ④ 와 같다(아래 PASS 표)
- 판정: WARN. 조용히 통과하는 자리다. 코디 E2E §9 #14 ~ #16 에서 실물로 꼭 봐야 한다(아래 체크리스트 E3 ~ E6)

---

## PASS — 항목별 대조

### 1. 「방 배정」만 빼고 방 없는 기타 작업은 남긴다 (사용자 핵심 결정 · `_RESUME` 10-23 32행 · SPEC §5.1 · §6.7 #13 · 부록 E #6)

| 확인 | 근거 | 판정 |
|---|---|---|
| back 판정 = `kind=="etc" and room_kos_id` (`rules.py:28`). `kos/sync.py:39-40` `_room_task`(ETCETERA + `room.id`)와 같은 뜻이다 — `room_kos_id` 는 `sync.py` 의 `str(room.id) or None`. 빼는 곳은 `Rules.items` 한 곳(`rules.py:89`). 방 있는 작업이 여럿이어도(OQ-511) 전부 뺀다 | SPEC §5.1 · WORK WP-BE1 | PASS |
| 방 없는 etc 는 남고 읽기 전용(`pickable/canStart/canFinish` false) | `tests/test_rules.py` `test_roomless_etc_stays_read_only` · `test_e2e1_room.py` | PASS |
| DB 에는 「방 배정」을 그대로 저장한다(`kind=etc` · `room_kos_id`) | `tests/test_kos_sync.py`(실제 sync 경로) | PASS |
| `canCall` · `all_done` · `paymentRequired` 는 바뀌지 않는다 | `rules.py` `procedures()` 는 그대로 · `test_room_task_filter_keeps_rules` | PASS |
| [귀가 대기] 취소 대상에 「방 배정」이 그대로 든다(`open_task_seqs` 기반 · `actions.py:246-247` 변경 없음) | `test_e2e3_home.py:77-89` | PASS (방 없는 작업까지 취소되는 점은 → W1) |
| 방 계산(`visit.room_id`) · 호출 전 방 넣기 변경 없음 | `sync.py` · `kos_ops.py` diff 0 | PASS |
| 가짜 보드: 「방 배정」 → 「시트팩」(지어낸 값) | `fake_board.py:79` | PASS |
| front 는 거르지 않고 etc 줄을 맨 위에 읽기 전용으로 그린다(`body-500 gray-600` + `caption-md-400 gray-500`) | `OrderCard.tsx:186-201` · 스크린샷 `fe2-card-etc` · `fe1-board`(A-룸1 「시트팩 · 준비중」) | PASS |
| 앱 부작용 없음: 스냅샷 모양 그대로 · 앱은 etc 를 안 그림(`app/lib/view/view.dart` `procsOnly`) · 앱은 자기 입실순 정렬(`view.dart:57-62`) | SPEC §5.12 「앱」 · OQ-523 | PASS |

### 2. 드래그 순서 — back (SPEC §3.2 · §5.12 · §7.2 · §7.3 · §7.5 · WORK WP-BE2)

| 확인 | 근거 | 판정 |
|---|---|---|
| 표 `board_order`(day PK · visit_ids · updated_at · updated_by · event_id) · `CREATE TABLE IF NOT EXISTS` · ALTER 없음. 옛 스키마 DB 시험 있음 | `db.py:97-101` · `test_old_schema_db_keeps_rows` | PASS |
| `PUT /api/board/order` · `require_real_board`(401 → 403 `fake_board`) · 역할 검사 없음 = 세 역할 모두 | `api/board.py:16` · SPEC-004 §3.4 · `test_auth_roles` 행렬 · `test_fake_board_403` | PASS |
| StrictInt(`"3"` · `3.0` · `true` · `null` → 400) · extra=forbid · 객체 아님 · 배열 아님 → 400 `invalid_request` | `schemas/actions.py` `BoardOrderRequest` · `test_bad_format_400`(8 경우) | PASS |
| 같은 id 두 번 = 거르기 전에 400 | `actions.py:261` · `test_duplicate_*` | PASS |
| 거르기: 지금 카드이고 귀가 대기가 아닌 것만(없는 id · 귀가 대기 · 사라진 카드 · 방 없는 visit). 오류 없이 뺀다 | `actions.py:267-268` · `test_filters_unknown_home_and_gone_cards` | PASS |
| 마지막 쓰기(`INSERT OR REPLACE`) · `event_log(board_order)` 1줄(payload `{day, visitIds}` = 거른 뒤 · `visit_id` NULL) · `kos_op` 0줄 · 트랜잭션 하나 | `repo.py` `put_board_order` · `test_last_write_wins` · `test_event_log_one_row_and_no_kos_op` | PASS |
| 저장 뒤 SSE 1개 · 400 이면 발행 0 | `_done()` → `container.changed` · `test_publishes_one_board_after_save` · `test_stream.py` | PASS |
| KST 날짜 경계(`kst_day`) · 다음 날은 순서 없음 · 전날 행을 지우지 않음(OQ-525) | `clock.py:56` · `test_next_day_has_no_order` · `test_kst_day_boundary` | PASS |
| 스냅샷 정렬 ① 목록 자리 → ② 목록 밖은 `room_assigned_at` 순 · 같으면 visit id → ③ 귀가 대기는 `flow_step_at` 순(목록에 있어도 무시) · 사라진 카드는 건너뜀 | `board_service.py:40-48` · `test_sort_list_then_rest_by_in_at_then_home` | PASS |
| back `procedures[]` 순서(완료 → 진행 → 대기) 그대로 | `ordered_procedures` diff 0 · SPEC §5.9 기본값 | PASS |
| 경로 수 17 | `test_route_count_17` · SPEC §7.4 | PASS |
| CORS — `allow_methods` 에 `PUT` 하나만 더함(origin · 헤더 그대로) | `main.py:79` · `test_cors_allows_put` | PASS (ingress CORS 는 → E8) |

### 3. 드래그 순서 — front (SPEC §5.12 · §6.3 · §6.7 #19 ~ #21 · WORK WP-FE2)

| 확인 | 근거 | 판정 |
|---|---|---|
| 카드 순서 = 스냅샷 `cards[]` 그대로 + 응답이 올 때까지 로컬 순서. front 는 다시 정렬하지 않는다(`orderedCards` 제거) | `page.tsx` `ordered` · `view.ts:49` | PASS |
| 방향 따라 놓기. 앞 · 뒤는 **드래그를 시작할 때의 전체 순서**(`drag.start` = `liveIds(ordered)` — 필터로 숨긴 카드와 경합 중 로컬 순서 포함)로 판정한다. 미리보기도 같은 함수를 쓴다(다시 판정하지 않음) | `page.tsx:152` · `view.ts:62` · SPEC §5.12 「무엇」(r3) | PASS |
| PUT 본문 = 귀가 대기 아닌 카드 전체(숨긴 카드 포함). 순서가 같으면 PUT 을 보내지 않는다 | `page.tsx:156-164` | PASS |
| 경합 ① 응답 전에는 로컬 순서. 새 카드는 뒤에, 그사이 귀가 대기가 된 카드는 귀가 대기 묶음으로, 사라진 카드는 뺀다 | `withLocalOrder` | PASS |
| 경합 ② 「같음」 = 서로 겹치는 카드만 비교한다(새 카드 · 그사이 귀가 대기 · 사라진 카드 제외) | `sameOrder` · SPEC §5.12 (r3) | PASS |
| 경합 ③ 3초 · ④ 실패면 바로 스냅샷 + 토스트(back `message`). 403 `fake_board` 도 예외 없음. 앞선 요청의 응답 · 실패는 무시 | `page.tsx:81-99` · `fe2-after-403-toast` | PASS |
| 귀가 대기 카드 = `draggable=false` · enter · over · drop 처리 없음 → 그 위에 놓아도 안 옮겨진다 | `OrderCard.tsx:315` · `page.tsx` `dragOf` | PASS (§6.7 #20) |
| 끄는 카드 0.35 + `0 0 0 2px var(--ms-primary)`. 불투명도 우선순위 0.35 → 0.55 → 0.45 | `view.ts` `cardLook` · 시안 `M:1475` · `fe2-drag-preview` | PASS |
| 고객 탭 줄 순서 = `ordered`(경합 중이면 로컬) | `Aside.tsx` `CustomersTab` · SPEC §6.4 (r3) · `fe1-panel-customers` | PASS |
| 터치 드래그 없음(범위 밖) | SPEC §6.3 기본값 | PASS |

### 4. 화면 — 시안 대조 (스크린샷 11장 ↔ 시안)

| 장면 · 시안 줄 | 스크린샷 | 결과 |
|---|---|---|
| 헤더 `M:63-92` — 「현황」 하나 · 호버 드롭다운(180 · 반경 10 · 그림자 · 항목 40 · 지금 항목 `body-600 text-primary bg-primary-100` / 나머지 `body-500 gray-800`) · 시계 · 「세라미크 명동점」 · 계정 · 로그아웃 · z 30 | `fe1-header-dropdown` · `AppHeader.tsx:14` 이하 | 같음. 항목은 「시술 현황」 하나(OQ-520 · §6.7 #5). 계정은 `name`(OQ-514 · §6.7 #17) — 표의 차이 |
| 제목 줄 `M:781-800` — 「시술 현황」 · 「마지막 KOS 동기화」(앞머리 없음) · 조회 시간 밖 · 동기화 실패 · 범례 5 · 정렬 버튼 없음 | `fe1-board` | 같음 (§6.7 #14) |
| 카드 `M:808-905` — 머리 한 줄(방 + Badge / 입실) · 고객 줄 · 메모 · 마취 · 선택 줄 · 시술 줄 · 바닥 버튼(`canCall`/`canHome` 만) | `fe1-board` · `fe2-card-all-done` · `fe2-card-doing-cut` | 같음. 시안과 다른 곳은 etc 줄뿐(§6.7 #13). 경과 글자 · KOS 반영 없음 = 시안 template 그대로(§6.7 #11 · #12) |
| 시술 줄 순서 진행 → 대기 → 완료 + 점선(`M:1500-1503` `cut`) | `fe2-card-doing-cut` · `view.ts:106` · `OrderCard.tsx` `cut` | 같음 (§6.7 #15) |
| 현황 탭 `M:944-956` · `M:1536-1541` — 3 × 2 · `row-gap 8` · `padding 14px 12px 10px` · 점 6 · `border-left` 칸 i%3 · 고른 칸 `body-600 gray-800` | `fe1-status-3x2` · `Aside.tsx` | 같음(값 하나하나 일치) (§6.7 #16) |
| 드래그 `M:1464-1475` — 0.35 · primary 2px · 미리보기 | `fe2-drag-preview` · `fe2-dropped-local` | 같음. 놓는 위치만 방향 따라(§6.7 #21), 귀가 대기는 끌기부터 막음(§6.7 #20) — 표의 차이 |
| 좁은 화면(760 미만) = 카드만 | `fe1-narrow` | 같음 (§6.8) |
| [의사 호출] = `canCall` 일 때만 · 둘 다 아니면 버튼 없음(`M:894`) | `OrderCard.tsx` `bottomEl`(코드 변경 없음) | 같음 (§6.7 #22) |

§6.7 #11 ~ #22 열두 줄 모두 코드에 맞게 들어갔다. 시안과 다른 곳은 모두 §6.7 표에 적힌 차이다. 표에 없는 차이는 transition 시간(시안 120ms · 코드 160ms) 하나다. 애니메이션 시간이라 판정에서 뺐다.

### 5. OQ 기본값

| OQ | 기본값 | 코드 | 판정 |
|---|---|---|---|
| OQ-514 | 계정 표시 = `name` | `AppHeader` 오른쪽 변경 없음(스크린샷 「관리자」) | PASS |
| OQ-520 | 드롭다운은 「시술 현황」 하나 | `AppHeader.tsx:14` | PASS |
| OQ-521 | 경과 글자 안 그림 | `NeedView.label` 제거 · 머리 줄 | PASS |
| OQ-522 | 비동기 KOS 실패는 웹에 표시 없음 | `kos` 표시 제거 · 토스트 없음 · 스냅샷 `kos` 필드 그대로 | PASS |
| OQ-523 | 앱 그대로 | `procedure/app/` diff 0 | PASS |
| OQ-524 | 경로 `/procedures/live` 그대로 | `NAVS` href | PASS |
| OQ-525 | 전날 행 지우지 않음 | 지우는 코드 없음 · `test_next_day_has_no_order` | PASS |

### 6. 부록 E 10줄

#1(현황 탭만) · #3(back 소량 · KOS 무변경 — `kos/` · `kos_ops.py` diff 0) · #4(순서 저장 전부) · #5(헤더) · #6(「방 배정」 · 버튼 · KOS 표시) · #7(시안대로 · 토스트만) · #8(방향 따라) · #10(시안 원천) → 모두 PASS. #2 · #9 는 코드에 닿는 정책이 없다.

### 7. 기능 독립 · public

- `procedure/` 밖 변경 · import 0. back 이 새로 import 한 것은 `fastapi` · `pydantic.StrictInt` · `app.*` 뿐이다 → PASS (DEC-001)
- 실명 0. 가짜 값(홍길동 · 김철수 · 이영희 · LI MEI · SMITH JOHN · 가/나/다 원장 · 시트팩)은 모두 지어낸 것이다. 시안 공지의 원장 이름과 계정 표시 이름은 코드 · 시험 · 가짜 보드 어디에도 없다. KOS id · 키 · 토큰 0. 새 env 없음 → PASS (WORK-005 「주의」 · SPEC 머리말)
- CORS 는 메서드에 `PUT` 하나만 더했다 → PASS

---

## 조용히 통과하는 자리 (시험은 초록인데 실물에서 어긋날 수 있는 곳)

1. **W1 을 굳히는 시험** — `test_e2e3_home.py:89` 는 「방 배정」 취소를 확인하면서 시트팩 취소(`[3, 4]`)까지 정답으로 박아 두었다. 사용자가 W1 ② · ③ 을 고르면 이 시험이 먼저 바뀌어야 한다
2. **front 순서 로직에는 레포 시험이 0** — `moveCard` · `sameOrder` · `withLocalOrder` · 렌더 중 `setLocal(null)` 은 tsc · lint · build 로만 확인된다. 방향 따라 놓기 6 경우는 워커가 한 번 손으로 돌린 Playwright 기록뿐이다(W3)
3. **가짜 보드에서는 PUT 이 늘 403** — 그래서 FE 화면에서는 경합 ② · ③(서버 순서로 넘어감 · 3초)과 다른 화면 공유가 한 번도 실행되지 않았다. back 시험은 `TestClient` 안에서 SSE 1개까지만 본다(W3)
4. **「방 배정」 판정은 KOS 가 작업에 방을 붙였는지에만 기대고 있다** — 시험 데이터는 직접 `room_kos_id` 를 넣는다. 실제 데모 KOS 에서 마취 · 시트팩 같은 기타 작업에 방이 붙어 있으면 그 줄은 조용히 사라진다. 게다가 `roomAssignedDateTimeUtc` 가 더 늦으면 카드 방도 그 작업 방으로 바뀐다(`sync.py:39-44` · OQ-511). 결정 줄 자체가 「room 있는 ETCETERA = `sync.py` 판정」이라 계약 위반은 아니다. 다만 §9 #0 에서 **방이 정말 없는** 기타 작업을 준비해야 #13 이 의미가 있다
5. **CORS 시험은 앱 미들웨어만 본다** — `test_cors_allows_put` 는 `localhost:3700` origin 으로 Starlette CORS 를 확인한다. 배포 ingress(`ccc.medisolveai.xyz`)가 따로 CORS 나 메서드를 거르면 실물에서만 막힌다
6. **드래그 중 카드가 사라지거나 귀가 대기가 되는 경우** — 그 카드의 `onEnd` 처리가 없어져 `drag` 상태가 남을 수 있다(`page.tsx` `dragOf` — 귀가 대기 카드는 처리 없음 · 사라진 카드는 dragend 가 오지 않음). 다음 드래그를 시작하면 덮어써지고, 그 사이 놓으면 PUT 에 든 그 id 는 back 이 거른다. 해가 없어 판정에서 뺐다

## 사용자가 실물에서 만날 자리 (코디 E2E 체크리스트)

| # | 보는 것 | SPEC |
|---|---|---|
| E1 | 카드에 「방 배정」 줄이 **없고**, 방 없는 기타 작업(시트팩 등)은 **맨 위 읽기 전용 줄**로 보인다. 준비할 때 그 작업에 KOS 방이 없는지 먼저 확인한다(위 4번) | §9 #0 · #13 |
| E2 | 시술 다 끝나고 시트팩만 「준비중」인 카드에 [귀가 대기]가 뜨는지, 누르면 KOS 시트팩이 `CANCELED` 가 되는지 → 사용자에게 보여 주고 W1 을 정한다 | §5.7 · W1 |
| E3 | 카드 3장 이상: 바로 아래 카드 위에 놓으면 자리 바꿈 · 마지막 카드 위에 놓으면 맨 끝 · 뒤 카드를 앞 카드 위에 놓으면 그 앞. 끄는 동안 같은 자리로 미리 보인다 | §9 #14 |
| E4 | 카드 사이 틈이나 마지막 카드 뒤 빈 칸에 놓기 → 미리보기와 달리 원래 순서로 돌아간다(W2). 사용자가 이걸 버그로 느끼는지 본다 | §6.3 · W2 |
| E5 | 브라우저 두 개: 한쪽에서 놓으면 다른 쪽도 새로고침 없이 같은 순서. 새로고침해도, back 을 재시작해도 그대로. 놓은 쪽 화면이 3초 안에 깜빡이며 옛 순서로 돌아갔다 오지 않는다(경합 ②) | §9 #14 · §5.12 |
| E6 | 두 브라우저에서 거의 같이 다른 순서로 놓기 → 둘 다 나중 것으로 맞춰지고 오류가 없다 | §9 #16 |
| E7 | 순서를 정한 뒤 새 카드는 귀가 대기 아닌 카드들 맨 뒤 · [귀가 대기] 카드는 맨 뒤로 가고 나머지 순서는 그대로 · 귀가 대기 카드는 끌리지 않는다 | §9 #15 |
| E8 | 배포(ingress) 환경에서 PUT 이 CORS 나 메서드 때문에 막히지 않는다(브라우저 콘솔 preflight) | §7.3 · 위 5번 |
| E9 | 필터(예: 「대기」)를 켠 채 끌어 놓은 뒤 필터를 풀면, 숨어 있던 카드 자리가 크게 흐트러지지 않는다. 전체 목록에서 끼우는 방식이라 숨은 카드의 자리 번호는 하나씩 밀릴 수 있다(시안 `M:1471` 과 같음) | §6.3 「필터 중에도」 |
| E10 | 카드 전체가 끌 수 있는 영역이다 → 체크칸 · [시작] 을 누르다 마우스가 조금 밀리면 드래그가 시작된다. 옆 카드에 놓이면 모든 화면 순서가 바뀌고 되돌리기는 없다. 오더 메모 글자를 마우스로 고르기(복사)도 안 된다. 바쁜 간호 스테이션에서 실제로 불편한지 본다 | §6.3 (시안 `M:808` 그대로) |
| E11 | 헤더 「현황」에 마우스를 올리면 「시술 현황」 하나가 펼쳐지고, 「현황」 글자를 누르면 `/procedures/live`. iPad(호버 없음)에서는 누르면 바로 이동한다 | §6.2 · §9 #12 |
| E12 | 카드 머리에 경과 글자 · 「KOS 반영」이 없다. 비동기 KOS 반영 실패는 웹에 전혀 보이지 않는다(OQ-522) — 사용자가 이걸 받아들이는지 본다 | §9 #10 · #17 |
| E13 | compose 빌드에서 Next 보안 알림으로 첫 빌드가 멈출 수 있다 → 다시 돌리면 통과한다(flaky) | `flaky-baseline-evidence.md` |

## 참고 (기존 부채 · 판정 밖)

- 옛 주석이 「방 배정」을 etc 의 예로 든다: `procedure/back/app/schemas/board.py:85` 「etc = KOS ETCETERA(「방 배정」 등)」 · `procedure/front/lib/types.ts:66` 「etc = 「방 배정」 같은 ETCETERA 작업」. 이제 스냅샷의 etc 에는 「방 배정」이 오지 않는다. 다음에 손댈 때 고치면 된다(diff 밖 파일)
- `board_order` 저장도 `container.changed` 를 거쳐 KOS 반영 루프를 `kick()` 한다. 대기 중인 op 가 없어 실해는 없다
- 고객 탭 배지(A-룸4 「시술 진행」)와 카드 배지(「확인 필요」)가 다르게 보인다(`fe1-panel-customers`). 이번 diff 에서 생긴 것이 아니다
- Next.js 보안 업그레이드 권유(`next upgrade --agent=security`)는 의존성을 바꾸는 일이라 범위 밖이다. 코디나 사용자가 정한다
