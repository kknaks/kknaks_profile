# 리뷰 리포트 — reservation-update-mcp-spec / planner (문서) 리뷰 (2026-08-31)

## 판정: PASS (WARN 3건)

FAIL 사유 없음 — **사용자 확정 3건 위반 0 · 계약 모순 0 · 하중을 지는 코드 실측 주장 전부 참**.
WARN 3건은 **문면 정밀도·규칙 공백**이며 R-1~R-4·등재 계약의 내용을 바꾸지 않는다.

---

## 검수 범위

- diff: 워킹트리 미커밋 3파일 (+92/−5) — `20-spec/spec-151-ax-assistant-reservation.md` · `20-spec/spec-060-mcp-surface.md` · `log.md`
- 브리프 §allowed_paths 이탈 **없음** (products/mediness 3파일만). 리포 파일 **수정·생성 0** (read-only 준수).
- 실행한 검사:
  - `python3 scripts/lint-pipeline.py --strict` (리포 루트) → **0 error / 255 warning, exit 0**. mediness 범위 warning **0건** (255건은 charty·procedure-hub·selly 의 기존 `doc_no`/`version` 누락).
  - 코드 실측 대조 (read-only, `/Users/kknaks/orca/workspaces/mediness-app/reservation-update-mcp/`) — 아래 §1 표.
  - `git diff -U0` 헝크 범위 ↔ 절 경계 대조 (§7.9 diff 0 확인).

---

## 1. 코드 실측 주장 검증 — 8건 전부 참 (1건 조건부)

| # | planner 가 단정한 사실 | 실측 | 판정 |
|---|---|---|---|
| 1 | REST 실경로 `POST /action-runtime/reservations/{run_id}/update` **선재** | `action_runtime_v2.py:2050` `@router.post("/reservations/{run_id}/update", status_code=201)` + `:136` `APIRouter(prefix="/action-runtime")` (`main.py:345` 이 `/api/v1` 을 더 붙임 — SPEC-060 의 기존 행 표기 관행과 동일하게 `/api/v1` 생략) | ✅ 참 |
| 2 | `date` 는 **422 `update_date_forbidden`** | `workflow.py:124-132` `DomainError(ERR_UPDATE_DATE_FORBIDDEN, 422, …)` · `surface.py:570-571` 에서 raise | ✅ 참 (⚠ 조건부 — **W-2**) |
| 3 | `title` **수용** | `surface.py:573` `for field in ("start", "end", "title")` · 스키마 `UpdateReservationInput.title` (`schemas/action_runtime.py:535`) | ✅ 참 |
| 4 | **409 `amendment_target_invalid`**(완료 상태 아님) | `surface.py:95-96, 420-421` `DomainError("amendment_target_invalid", 409, "완료된 예약에만 취소·변경을 요청할 수 있습니다")` | ✅ 참 |
| 5 | 접수 검증에 「시작이 과거면 거부」 **없음** — 보는 것은 달력 실재·시각 실재·`start < end` 셋뿐 | `ReservationWindow` (`schemas/action_runtime.py:452-483`): `date.fromisoformat` · `time.fromisoformat` · `start >= end` 거부. **과거 판정 없음** | ✅ 참 (문면 그대로) |
| 6 | 회의실 조회·후보 계산에 과거 거부 **없음** | `the_connect.py:384-406` `_candidates` = 중첩·정원·모니터만 · `:252-274` `availability` = 중첩만 | ✅ 참 |
| 7 | 카드 만료가 **오히려 지난 시작을 이미 다룬다**(고정 TTL fallback) | `workflow.py:223-234` `reservation_expiry` — `if start <= now: return now + TTL` | ✅ 참 |
| 8 | 감사 규칙의 되묻기 억제 조항 — 「필수 입력이 정말로 없고 발화·**현재 시각**·대화 맥락에서 안전하게 해소할 수 없을 때만」 | `chat/provider.py:253-254` 원문: *"Use clarification only when required input is genuinely missing and cannot be safely resolved from the utterance, current time, or conversation context."* | ✅ 참 (직역 정확) |

**cancel 선례 «동형» 주장의 실측 (§6.2b·SPEC-060 ②·④)** — `server.py:1707-1725` `reservation_cancel_request_tool` 의 `access(...)`:

- `capability="action.runtime.basic"` → 「요구 leaf = 감싸는 REST 의 leaf」 ✅
- `taint_policy=TAINT_SELF_LEDGER` (`tool_access.py:64` = `"self_ledger"`) → 「오염 등급 = 본인 원장 내 쓰기」 ✅ (SPEC-060 §4 3등급 어휘와 일치)
- `needs=("reservation_list_tool", "reservation_get_tool")` → `requires_tools` ✅
- `structured = {data, action_id, workflow_run_id, plan_version?}` (`tools/reservation_cancel_request.py:95-98`) → §6.2b 의 「cancel 동형」 structured 선언과 **문자 그대로 일치** ✅
- 404 = `reservation_run_not_found` (같은 파일 :36) → 「404(없는 run·다른 조직·`action_id` 오투입)」 ✅

⇒ **「다른 것은 입력 하나(사유 → `revision`)」 주장은 실측상 참**이다. 축(run_id)·leaf·taint·requires_tools·structured·409/404 가 전부 동일하고 갈리는 것은 body 필드 하나다.

**TIME_RESOLUTION_RULE 실물** (`chat/provider.py:26-30`, 계기·원인 주장의 근거):

> `"Korean times without am/pm are ambiguous: resolve to the nearest upcoming time from now (…). A reservation must start in the future - if the spoken time already passed today and no explicit date was given, use tomorrow."`

→ R-3(모호 → 가장 가까운 미래)·R-4(날짜 없는 지난 시각 → 내일)의 「유지」 주장은 **실물과 정확히 대응**한다. 다만 앞 문장 존재가 **W-1**.

---

## 2. §7.10 내부 정합 — 모순 없음

- **「완전히 지났다 = 종료 시각 경계」(:850) ↔ R-1(:843)** — 모순 **없음**. R-2 는 R-1 의 *예외가 아니라 확인 절차*다: 되묻기 이후 「잡아 달라」면 **말한 그대로**(:862) 서므로 두 규칙 모두 "명시 값을 바꾸지 않는다"는 같은 원칙을 지킨다. 경계를 종료 시각에 둔 근거(:850 「시작을 경계로 잡으면 실측 사례가 되묻기로 옮겨갈 뿐」)도 실측 사례(15:08 / 15:00–16:00)와 정합한다.
- **§5 상태 축과 충돌 없음** — 되묻기 턴은 워크플로를 시작하지 않고(:858) 「아니」에 예약 건도 서지 않으므로(:863) **새 상태값·새 조합표 칸이 필요하지 않다.** 변경 노트 ⑨ 의 「§5.3 칸을 늘리지 않는다」와 일치하고, 실제로 §5 diff 0.
- **§7.7 침묵 종결 금지와 충돌 없음** — :866 이 「되묻기는 답변이지 침묵이 아니다」로 명시. 코드 축도 정합(`chat/service.py:1172-1175` — 유일한 응답을 억제하는 suppress 는 `AuditProtocolError` 로 거부).
- **승인 게이트 불변 명문화** — :865 「되묻기가 승인을 대신하지 않는다 … §7.1 의 예외가 `source` 밖으로 새어 나간다」. §7.1 모달 발 자동승인 예외의 경계(입력에 해석이 끼는가)를 정확히 인용했다.
- **감사 규칙 예외 명문화(:867)** — 인용 원문 일치(위 #8), 「해소 vs 확인」 기준(「사용자가 명시한 값을 바꿔야 하는가」)이 R-1·R-2 와 일관.
- **§7.7 ④ 참조 실재** — §7.7:712 에 「감사는 ① 그대로 내보내기 ② … ③ … ④ 사용자에게 되묻기 중 하나를 고른다」가 실재. 참조 번호 정확. (단 그 분기를 *기제* 로 삼는 것은 **W-3**.)

---

## 3. §6.2b 등재 정합 — 정확

- **개수 경위 검산** — §6.2b 표 실제 행 수 **8** (`room_catalog`·`room_status`·`room_plan`·`reservation_request`·`reservation_list`·`reservation_get`·`reservation_approve`·`reservation_reject`, 파일 :456-463) + revise·withdraw 2 + cancel_request 1 + update_request 1 = **12**. 제목 「8종 → 12종」 갱신 **정확**.
- **「아직 넣지 않은 것」 정리 정확** — 구 표기가 담던 `/cancel` 은 2026-08-11(SPEC-060:71 개정 2차에서 실제 등재 확인), `/update` 는 이번 등재로 각각 해소. 남은 항목 **카드 명령** `/actions/{id}/commands/{command_id}` 은 §6.3 명시 transport 목록에 실재하고 [WP-097](products/mediness/30-work/work-097-workflow-mcp-tools.md) 파일 실재 확인.
- **인계 2건 참조 무결** — SPEC-151 §6.2b:501 이 가리키는 [WP-106](products/mediness/30-work/work-106-ax-task-chat-crud.md) `Open Issues` **:67-69** 에 「ⓐ 취소 접수에 소유 판정이 없다 ⓑ 재취소 멱등 가드가 없다 ⇒ SPEC-151 스트림으로 이관」이 실재. SPEC-060 :71 의 인계 문장과도 일치. **참조가 매달리지 않는다.**
- **`revise` 와 갈리는 지점(structured.action_id)** — §6.2b 기존 bullet(:490)이 「`revise` 는 새 카드를 만들지 않는다 ⇒ 규약 대상 아님」이라고 이미 적어 둔 것과 신규 bullet(:498)의 대비가 정합. 코드도 일치(`surface.py:588` `kernel.create_gate(type=C.MEETING_UPDATE, …)` — 새 Action 생성).

---

## 4. SPEC-060 규약 준수 — 준수

- **인벤토리 표 행 diff 0 · 카운트 diff 0 · §5 AC diff 0.** 변경된 것은 ⓐ `last_updated` ⓑ 머리 개정 노트 블록 신설 ⓒ ⏳ 예고 줄의 「3건 → 4건」과 ④ 항목 본문뿐. 2026-08-13 「실측 일치 표」 규약(미구현분을 행으로 세지 않는다) **준수**.
- **증분 합산 회피가 명시적** — ④ 말미 「③ 과 함께 착지하면 증분이 겹치므로 그 시점의 실측으로 다시 센다(여기에 미리 합산해 두지 않는다)」. ③(baseline_publish)이 `write 18→19` / `/health 57→58` 을 이미 예약해 둔 것과 충돌하지 않게 **숫자를 비워 둔 것이 옳다**.
- **소유 경계 준수** — SPEC-060 은 「wrapper 등재만」, 계약 본문은 SPEC-151 §6.2b 가 owns 로 양쪽에서 상호 선언. cancel(2026-08-11) 때와 같은 분할.

---

## 5. 사용자 확정 3건 위반 여부 — 위반 0

| 확정 | 문서 반영 | 판정 |
|---|---|---|
| ① thin wrapper · cancel 동형 · **새 REST·leaf·카드 유형 0** | §6.2b:493 「REST·게이트·카드 문법은 불변이며 등재일 뿐」 · 변경 노트 ②(:39) 「⛔ 새 REST · 새 leaf · 새 카드 유형 · 새 판단 버튼 0」 · SPEC-060 ④ 「대응 REST = **선재** · 요구 leaf = `action.runtime.basic`」 | ✅ 준수 |
| ② 시각 해석 (명시 그대로 / 완전히 지난 것 되묻기 1턴 → 예=카드+승인게이트·아니=미생성 / R-3·R-4 유지) | R-1(:843)·R-2(:844)·처분표(:860-863)·R-3(:845)·R-4(:846). 「승인 게이트는 평소와 같다」(:862·§3 S-2c) | ✅ 준수 (침묵 조정 금지·되묻기≠승인 모두 명문) |
| ③ **§7.9 무개정** | `git diff -U0` 헝크 = `+35..45`, `+148`, `+412`, `+446..448`, `+492..502`, `+831..883`, `+908`. §7.9 는 **726–830** 행 ⇒ **어느 헝크도 §7.9 를 건드리지 않음**. 신설 §7.10 은 §7.9 종료 **뒤**(831)부터 시작 | ✅ diff 0 확인 |

부수 확인:
- **§7.9 파급 참조 방식이 옳다** — §6.2b:502 · 변경 노트 ③(:40) 이 「§7.9.5 파급이 그대로 걸린다 / 게이트를 여는 표면이 하나 늘 뿐」로 **참조만** 하고 §7.9 본문을 복제하지 않는다. 「발동 조건은 게이트의 승인·실행 성공이지 어느 표면에서 접수됐나가 아니다」는 §7.9.5 의 실제 서술과 정합.
- **log.md 규약** — 최신 entry 상단(역시간순) ✅ · `종류` = `spec-change` (enum 내) ✅ · `영향 ID` 콤마+공백 ✅ · 요약이 결정 근거를 담음(대안·제약·판단 정황) ✅.

---

## 위반 (FAIL 사유)

**없음.**

---

## 경미 (WARN)

### W-1 (중) — 「규칙의 침묵」 진단이 실물보다 좁다 → 구현자가 모순 문장을 남겨 둘 수 있다

- `spec-151:837` — 「현행 규칙이 규정한 것은 **「지난 시각 + 명시 날짜가 «없음» → 내일」 하나뿐**이라, 명시 날짜가 있는데 그 시각이 지난 경우에 대해 계약이 **아무 말도 하지 않았다**」
- **실측**: `chat/provider.py:26-30` `TIME_RESOLUTION_RULE` 은 **두 문장**이다. 두 번째가 인용된 「no explicit date → tomorrow」이지만, **첫 문장이 `"A reservation must start in the future"`** — 날짜 명시 여부에 **조건이 붙지 않은 무조건 제약**이다. 즉 그 자리는 «비어 있던» 것이 아니라 **「미래여야 한다」고 말하고 있었고**, 모델은 그 제약을 지키려고 유일하게 가진 처방(내일)을 적용한 것이다.
- **왜 실무에 걸리나**: §7.10:852 는 문면을 코드 SoT 로 넘기고 「본 절이 소유하는 것은 **그 규칙이 무엇을 말해야 하는가**」라고만 둔다. 진단이 「빈칸」이면 구현자는 **문장을 «추가»** 하는 쪽으로 읽고, `"A reservation must start in the future"` 를 **그대로 남겨** R-1 과 직접 충돌하는 프롬프트가 된다. 실제 필요한 조치는 추가가 아니라 **그 문장의 삭제·재작성**이다.
- 근거 출처: 리뷰 브리프 §3-1(코드 실측 주장 검증) · reviewer `rules.md` 공통 3(근거 있는 지적).
- **권장 수정**: :837 을 「현행 규칙은 **무조건 제약(«예약은 미래에 시작해야 한다»)** + 처방 하나(날짜 없음 → 내일)로 되어 있고, 명시 날짜가 있는 충돌 케이스에 **처방이 없어** 모델이 그 제약을 지키려 유일한 처방을 전용했다」로 정정하고, §7.10 이 요구하는 것에 **「그 무조건 제약 문장은 R-1 과 양립하지 않으므로 존치할 수 없다」**를 한 줄 더한다.

### W-2 (저) — `date` 거절이 **무조건이 아니라 «값이 바뀔 때»** 다

- `spec-151:412`(§6.2 표) 「⚠ **`date` 는 받지 않는다 — 422 `update_date_forbidden`**」 · `spec-060:185`(④) 「⚠ **`revision` 에 `date` 는 넣을 수 없다**(REST 가 422 로 거절)」
- **실측**: `surface.py:570` — `if revision.get("date") and revision["date"] != previous.date: raise …`. **현재 예약과 같은 날짜를 실으면 통과**한다(무해한 no-op 이지만 「받지 않는다」와는 다르다).
- 계약 의도(「날짜는 바꿀 수 없다」)는 **정확**하고 툴이 우회로를 만들지 말라는 지시도 옳다. 다만 client·QA 가 표만 읽고 「`date` 를 실으면 항상 422」로 테스트를 고정하면 **동치 날짜 케이스에서 어긋난다.**
- 근거 출처: 브리프 §3-1 · `document-pipeline.md` 「API endpoint 계약 … client 가 봐야 할 계약은 SPEC」.
- **권장 수정**: 「`date` 는 **바꿀 수 없다** — 값이 현재와 다르면 **422 `update_date_forbidden`**(같은 값이면 무시된다)」로 한 구절만 정밀화.

### W-3 (저) — 되묻기의 «기제» 를 최종 답변 감사 분기로 지목한 것이 §7.7 자기 서술과 어긋난다

- `spec-151:856` 「되묻기는 **최종 답변 감사가 이미 가진 분기**(§7.7 「최종 답변 감사」 ④)를 그대로 쓴다」 + `:858` 「되묻는 턴에는 **카드가 서지 않는다** — 워크플로를 시작하지 않고 턴이 답으로 끝난다」
- **같은 문서 §7.7:712**: 최종 답변 감사는 「**도구를 고른 턴·정형 되묻기는 대상이 아니다**」. 코드도 동일 — `chat/service.py:1127-1129` docstring 「tool/**workflow** 를 고른 턴과 템플릿 응답은 **애초에 이 경로에 오지 않는다**」.
- ⇒ **예약 워크플로를 고른 턴은 감사에 도달하지 않으므로, 감사 ④ 분기는 카드 생성을 «막을» 수 있는 자리가 아니다.** R-2 가 카드를 세우지 않으려면 판단이 **그 앞(카탈로그 턴 / `TIME_RESOLUTION_RULE` 축)** 에서 나야 한다. 감사 ④ 는 «되묻기를 내보내는 출구» 로는 맞지만 «되묻기를 결정하는 자리» 로는 성립하지 않는다.
- 이 문장을 문자 그대로 읽은 구현자가 R-2 를 감사 프롬프트 규칙 6 에 얹으면 **구조적으로 동작하지 않는다**(카드는 이미 서 있고 감사는 호출되지 않는다).
- 근거 출처: 같은 SPEC §7.7:712 + `chat/service.py:1127-1129` · reviewer `rules.md` planner 리뷰 「spec 내부 정합」.
- **권장 수정**: :856 을 「**새 표면(고정 문구 채널)을 만들지 않는다** — 되묻기 텍스트는 감사가 이미 가진 되묻기 출구(§7.7 ④)와 같은 자리로 나간다. ⚠ **되묻을지 «결정» 하는 자리는 감사가 아니라 접수 해석 축**이다(감사는 워크플로를 고른 턴에 도달하지 않는다, §7.7)」로 두 축을 분리.

### (참고 · WARN 미만) R-1 ↔ R-3 우선순위가 표에 없다

`spec-151:843·845` — **명시 날짜 + 모호 시각**(예: 15:08 에 「오늘 3시」, 「오후」 없음)이 어느 규칙인지 표가 답하지 않는다. R-3 의 「가장 가까운 미래」를 그대로 적용하면 명시된 「오늘」을 벗어날 수 있어 §7.10 이 없애려는 실패와 같은 모양이 된다. 실측 사고 사례는 「오후」가 붙어 있어 이번 확정 범위 밖이며 사용자 확정 3건에도 없다 — 그래서 위반이 아니라 **다음 라운드 관찰 항목**으로만 남긴다.

---

## 기존 부채 (이번 판정 제외)

- **소유 판정·멱등 가드 2건이 owner 없이 참조만 순환한다** — SPEC-060:71(2026-08-11)은 「⇒ 소유·멱등 축은 **SPEC-151 소관**으로 넘긴다」고 이관했는데, SPEC-151 은 그 축에 대한 **자기 OQ 를 두지 않고** WP-106 Open Issues 로 되가리킨다(:501). WP-106:69 도 「이 WP 가 고칠 자리가 아니다」로 되돌린다. **2026-08-11 부터 있던 상태**이고 이번 diff 는 그 사실을 정확히 재기술하며 「이 등재가 그것을 늘리지도 줄이지도 않는다」고 명시했다 ⇒ **이번 판정 대상 아님.** 다음 라운드에서 SPEC-151 §9 OQ 로 세우거나 담당 WP 를 지정할 것을 권고.
- 타 제품 lint WARN 255건(charty·procedure-hub·selly 의 `doc_no`/`version` 누락) — 이번 작업과 **무관**.
- `log.md` `PR` 칸 `—` 사용 — `document-pipeline.md` 는 「PR 번호 또는 근거가 있는 실제 링크」를 요구하지만, 직전 행(2026-08-31 WP-124)도 동일하게 `—` 다. PR 발행 전 entry 에 대한 **리포 관행**이며 이번 diff 가 만든 이탈이 아니다. PR 머지 시 번호로 채우면 해소.

---

## 확인한 것 (PASS 근거) — 체크리스트 전수

- [x] **린트** — `--strict` 실행, mediness 범위 **ERROR 0 · WARN 0** (전체 0 error / 255 warning, 전부 타 제품 기존분). 리포 루트에서 실행 확인.
- [x] **read-only 준수** — 리포 파일 수정·생성·삭제 **0**. 유일한 산출물이 이 리포트.
- [x] **allowed_paths** — diff 3파일 전부 `products/mediness/` 내부. 이탈 0.
- [x] **코드 실측 주장 8건** — 전부 파일:줄로 대조 (§1 표). 조건부 1건은 W-2.
- [x] **§7.10 내부 정합** — R-1/R-2 경계 · §5 상태 축 · §7.7 침묵 종결 · §7.1 승인 게이트 · 감사 예외 5축 전부 대조.
- [x] **§6.2b 등재 정합** — 표 8행 실카운트 검산(8+2+1+1=12) · cancel 동형 6축 코드 대조 · 「아직 넣지 않은 것」 잔여 항목 실재 확인 · 인계 참조(WP-106:67-69) 무결.
- [x] **SPEC-060 규약** — 인벤토리 행·카운트·§5 AC diff 0 확인, ⏳ 예고 ④ 로만 등재.
- [x] **사용자 확정 3건** — 위반 0 (§5 표).
- [x] **소유 경계 §7.9 diff 0** — 헝크 범위 ↔ 절 경계(726–830) 대조로 확인.
- [x] **log.md 규약** — 위치·`종류` enum·`영향 ID` 형식·결정 근거 깊이 확인.
- [ ] **WP 갱신 / Spec Coverage / Status Board 3자 동기** — **해당 없음.** 이번 라운드는 SPEC 개정만이고(변경 노트 ⑨ 「WP·코드는 이 개정의 범위가 아니다 — 다음 발주」), `30-work*` diff 0. lint 의 3자 일치 검사도 통과. **구현 WP 발주 시 재검수 대상.**
- [ ] **frontmatter doc_no/status 신규 부여** — **해당 없음** (신규 문서 0, 기존 두 SPEC 모두 `doc_no` 보유 · lint WARN 0). `last_updated` 는 SPEC-060 만 갱신됨 — **SPEC-151 의 `last_updated` 는 diff 에 없다**(같은 날 앞 PR #665 에서 이미 `2026-08-31` 로 갱신돼 값이 이미 맞다. 확인함, 위반 아님).
