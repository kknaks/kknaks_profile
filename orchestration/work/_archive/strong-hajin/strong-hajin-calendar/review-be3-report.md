# 리뷰 리포트 — Phase BE-3 코드 검수 (2026-09-21)

## 판정: **PASS**

**여덟 항목이 전부 통과했다.** 계약과 다른 것이 도는 자리·경계 위반·증명 없음이 없다.

가장 중요한 자리 — **K12 순서** — 가 코드와 **3연타 테스트**로 둘 다 닫혔다.
겹침 검사는 멱등 원장 claim **뒤**에 있고, 테스트가 `201 / 200 / 200` 과
**「두 번째 effect 가 없다」(회차 1 그대로)**까지 단언한다.

**읽는 문이 정말 하나다** — `overlapping_blocks` 를 부르는 자리가 `src/` 에 **하나**뿐이고,
반열림·자정 분할 규칙은 **순수 도메인 한 파일**에 모여 `PURE_DOMAIN_MODULES` 에 등재됐다.

**「DB 제약으로 올리지 않았다」를 적극적으로 증명한다** — postgres 테스트가
`pg_constraint` 에 `contype='x'`(EXCLUDE)가 **0개**임을 두 표에서 단언하고,
테스트 이름이 **`…_and_must_not_become_one`** 이다. 나중에 누가 「고치려」 들면 그 테스트가 깨진다.

**워커가 스스로 신고한 조용한 깨짐도 정당하게 고쳤다** — 약화가 아니라 **단언을 더한** 수정이고,
같은 자리가 더 있는지 세어 보니 **없다.**

WARN 둘은 **BE-4 브리프**로 넘긴다. 하나는 코디 확인이 필요하다.

---

## 검수 범위

`aa8576b`(FE-2) 위의 **uncommitted diff** — 수정 6 · 신규 5, **전부 `backend/`**.
**테스트는 돌리지 않았다**(지시). **코드도 한 줄 고치지 않았다.**
코디가 추인한 셋(**K25·K26·K27**)은 **지적에서 뺐다** — 구현이 그 셋과 맞는 것만 확인했다.

| 신규 | 무엇 |
|---|---|
| `modules/time_blocks.py` | **순수 도메인** — 반열림 · 사무실 시간대 · 자정 분할 |
| `platform/time_blocks.py` | **읽는 문 하나** — 두 표 조회 |
| `tests/unit/test_time_blocks.py` | 13건 |
| `tests/contract/test_task_schedule_overlap.py` | 19건 |
| `tests/integration/postgres/test_task_schedule_overlap_postgres.py` | 7건 |

---

## 1. 읽는 문이 정말 하나인가 — **하나다**

- **공개 메서드가 하나다.** `SqlAlchemyTimeBlockRepository`(`platform/time_blocks.py:63`)에
  `overlapping_blocks` 만 공개이고 `_schedule_blocks`·`_meeting_blocks`·`_members_held_by` 는 사설이다.
  클래스 docstring 이 「**이 클래스에 다른 공개 메서드를 더하지 않는다**」로 못 박았다.
- **부르는 자리가 하나다.** `src/` 전체에서 `overlapping_blocks` 호출은
  `modules/work/application.py:677`(`_require_free_time` 안) **한 곳**뿐이다.
- **판정 함수가 새지 않는다.** `overlaps`·`split_across_office_dates` 를 쓰는 곳은
  `time_blocks.py` 짝 **둘뿐**이고, `application.py` 는 `office_span`(창을 만드는 것)만 쓴다 —
  **판정을 다시 하지 않는다.**
- `platform/the_connect.py:50` 의 `_overlaps` 는 **이번 diff 밖의 기존 코드**이고
  외부 Connect 연동의 문자열 시각 비교라 **다른 도메인**이다. 이 문과 무관하다.
- **규칙이 순수 도메인에 있다** — `test_test_pyramid.py` 의 `PURE_DOMAIN_MODULES` 에
  `"time_blocks.py"` 가 등재됐다. 주석이 이유를 적는다: 「문은 platform 이지만 **그 문이 쓰는 규칙**은
  데이터베이스 없이 서야 한다: 규칙이 두 곳에 있으면 두 규칙이 된다」.

---

## 2. 반열림이 실제로 반열림인가 — **네 방향 다 맞다**

`modules/time_blocks.py:110-121` `overlaps`:

```python
if one_from >= one_to or other_from >= other_to:   # 길이 0 · 뒤집힘 → 겹치지 않는다
    return False
return one_from < other_to and other_from < one_to  # 반열림
```

| 방향 | 예 | 결과 | 맞나 |
|---|---|---|---|
| **뒤로 닿음** | `[10,11)` vs `[11,12)` | `11 < 11` 이 거짓 → **False** | ✓ |
| **앞으로 닿음** | `[11,12)` vs `[10,11)` | `11 < 11` 이 거짓 → **False** | ✓ |
| **포함** | `[9:30,12:30)` vs `[10,11)` | 둘 다 참 → **True** | ✓ |
| **길이 0** | `[10,10)` vs 무엇이든 | 첫 줄에서 **False** | ✓ |

**길이 0 을 따로 막은 이유가 적혀 있고 옳다** — 배정은 `starts_at < ends_at` 을 DB CHECK 까지 걸어
막지만 **이미 저장된 회의 행은 그 보장을 받지 않는다**(검증은 새 쓰기에만 — K22).
그런 행 하나가 **남의 하루를 통째로 막지 않게** 한다.

테스트도 네 방향을 각각 든다 — 계약 `:124`(경계) · `:138`(포함) · `:194`(경계로 이동) ·
`:260`(회의가 끝나는 순간 시작), 단위 13건, postgres `:176`.

---

## 3. 자정 분할 — **맞다. 창으로 먼저 자르는 것도 맞다**

`split_across_office_dates`(`:124-147`):

- **`within` 으로 먼저 clip 한다**(`:133-135`). 이유가 docstring 에 있다 —
  「**오래 걸친 행 하나가 조각 수천 개가 되지 않게**」. 순서가 맞다: 자른 뒤 쪼개야 조각 수가 창에 묶인다.
- **23:00~01:00** → cursor 23:00 → `min(다음 자정, 끝)` = 자정 → 조각①(1일차 23:00–24:00),
  cursor 자정 → 조각②(2일차 00:00–01:00). **두 조각** ✓
- **자정에 정확히 끝나는 회의(23:00~24:00)** → 조각① 뒤 `cursor == local_end` 라 루프 종료.
  **한 조각** ✓ — 반열림이라 다음 날에 조각을 만들지 않는다. docstring 이 그 문장을 갖는다.
- `office_dates_in`(`:98-107`)이 **끝에서 1마이크로초를 뺀 뒤** 날짜를 읽는다 —
  자정에 끝나는 창이 **다음 날 행을 끌어오지 않는다** ✓. 빈 창은 시작 날 하루로 읽고,
  **판정은 `overlaps` 가 한다**고 적어 조회 좁히기와 판정을 갈랐다.
- 시간대는 `OFFICE_TIMEZONE = Asia/Seoul` 고정이고 **서버 TZ 에 기대지 않는다** ✓.
  `aware()` 가 tz 없는 값을 **UTC 로** 읽는다(SQLite) — 기존 `business_date` 와 같은 결이다.

테스트: 계약 `:269`(두 날짜) · postgres `:143`(실물 `timestamptz`) · 단위.

---

## 4. K12 순서 — **닫혔다. 이번 Phase 에서 가장 중요한 자리**

**코드**: 겹침 검사(`_require_free_time`)는 `create_schedule` **안**(`application.py:739`)에 있고,
`create_schedule` 은 `TaskCreationApplication.create_task_schedule` 이
**`_ledger.claim` → (같은 키면 영수증 반환) → 아니면 호출**하는 구조 그대로다
(`creation_commands.py` 는 **이번 diff 에 없다** — BE-1 의 순서가 그대로 산다).
→ **재전송은 겹침 검사에 도달하지 못한다.**

주석도 그 자리에 있다(`:737-738`) — 「**겹침은 마지막 409 다** — 영수증은 이 명령보다 먼저
지났으므로(증보 K12) 재전송이 자기 자신과 겹쳐 거절되는 일이 없다」.

**테스트 `test_task_schedule_overlap.py:222`
`test_the_same_idempotency_key_replays_as_a_receipt_and_never_as_an_overlap`** —
코디가 물은 **3연타**를 그대로 한다:

```
first / again / once_more  →  201 / 200 / 200
again.json() == first.json() and once_more.json() == first.json()
합본 조회의 schedules == [("10:00", version 1)]     ← 두 번째 effect 가 없다
```

**상태 코드뿐 아니라 「행이 하나이고 회차가 1」까지 본다** — 조용히 두 번 쓰이는 경우도 잡힌다.
`errors.py` 의 `TaskScheduleOverlap` docstring 도 같은 순서를 적어 두어 **문서가 코드 옆에 있다.**

`http.py` 매핑도 맞다 — `TaskScheduleOverlap` 이 **409 튜플**에 들어갔고(일반 `TaskError`→422 분기보다 먼저),
주석이 「422 가 아닌 이유 — **다른 시간이면 같은 값이 통과한다**」로 상태 코드 선택을 설명한다.

---

## 5. `ignore_schedule_id` — **옳게 쓰이고, 빼는 범위가 자기 하나다**

- **범위**: `platform/time_blocks.py:117-118` 이 `TaskScheduleRecord.id != ignore_schedule_id` —
  **id 하나**로 뺀다. `task_id` 나 날짜로 빼지 않는다 → **너무 넓게 빼서 겹침을 놓치는 일이 없다** ✓
- **시각 변경**: `application.py:761` 이 `ignoring=schedule.id` 를 넘긴다 ✓
- **생성**: 넘기지 않는다. **그것이 맞다** — 주석이 이유를 적는다: 「뺄 자기 자신도 없다:
  같은 (업무, 날) 은 위 줄이 이미 막았다」. 확인했다 — 창이 하루 안이고 같은 (업무,날) 은
  `DAY_TAKEN` 이 먼저 막으므로 자기와 겹칠 행이 존재할 수 없다 ✓
- 테스트 `:206` `test_a_slot_never_collides_with_itself_when_it_slides` —
  10:00–11:00 → 10:30–11:30 이 `200` 이고 **회차가 2** 가 되는 것까지 단언한다 ✓

---

## 6. 한 트랜잭션인가 — **그렇다**

`bootstrap/application.py:4323` 이 `time_blocks=SqlAlchemyTimeBlockRepository(session)` 을
`_tasks(session)` **안에서** 조립한다 — 멱등 원장·배정 저장소·겹침 조회가 **같은 session** 이다.
`WorkflowApplication.create_task_schedule` 이 그 session 하나를 `with` 로 열고 **한 번 commit** 한다(BE-1).
→ **원장 claim · 겹침 조회 · insert 가 한 트랜잭션** ✓

그리고 **틈을 감추지 않는다** — `_require_free_time` docstring 과 `errors.py`,
`platform/time_blocks.py` 머리 세 곳이 「**동시 요청 둘이 각각 통과해 둘 다 설 수 있다** ·
「하루 한 칸」과 같은 세기의 보장이 아니다」를 적는다. SPEC §2.9 한계 표와 같은 말이다.

---

## 7. DB 제약으로 올리지 않았나 — **안 올렸고, 그것을 적극적으로 단언한다**

`tests/integration/postgres/test_task_schedule_overlap_postgres.py:69`
**`test_overlap_is_not_a_database_constraint_and_must_not_become_one`**:

- `:82-87` — `pg_constraint` 를 `task_schedules` 에 대해 조회해
  **`[name for name, contype in kinds if contype == "x"] == []`** (`x` = EXCLUDE) 단언 ✓
- `:95-98` — `meetings` 에 대해 **같은 단언** ✓
- 파일 머리 `:11` — 「`EXCLUDE USING gist` 로 막고 싶어지는 자리이고,
  **막지 않았다는 것이 계약이다**」

**단언이 실제로 있다.** 그리고 테스트 이름이 **「그리고 그렇게 되어서는 안 된다」**라
나중에 누가 제약으로 「고치려」 들면 **이 테스트가 깨져서 막는다** — WP 가 「이 Phase 의 가장 흔한 오답」
이라고 경고한 자리에 회귀 가드를 세웠다.

---

## 8. 조용히 통과하는 자리 — **워커의 수정이 정당하고, 같은 자리는 더 없다**

### 고친 방식 — **약화가 아니라 강화다**

`tests/contract/test_task_schedules.py:379-385`
`test_a_finished_task_leaves_the_calendar_while_a_submitted_one_stays`:

| | 전 | 후 |
|---|---|---|
| 두 업무의 배정 | **둘 다 10:00–11:00** (같은 날) | **10:00–11:00 / 11:00–12:00** |
| 반환 | **단언 없음** | **`assert … == 201`** |

- **원래 무엇이 깨져 있었나** — K22 가 붙으면 둘째 배정이 `409` 가 되는데 반환을 안 봐서
  **`kept_id` 가 배정 없이 서고**, 그 테스트가 재려던 「`COMPLETION_SUBMITTED` 는 **배정이 살아 있다**」가
  **조용히 공회전**한다.
- **고친 것이 재던 것을 약화시켰나 — 아니다.** ① **없던 단언(`201`)을 더했고**,
  ② 두 업무 모두 **살아 있는 배정을 갖게 되어** 테스트의 주제가 **오히려 복원**됐다.
  ③ 시간을 11:00 로 민 것은 **반열림이라 겹침이 아니다** — 계약을 피해 간 것이 아니라
  계약대로 둔 것이고, 덤으로 경계 규칙을 한 번 더 밟는다.

### 같은 자리가 더 있나 — **없다. 세었다**

배정을 만드는 기존 테스트를 전수로 훑었다(`test_task_schedules.py` · `test_task_schedule_release.py`).
**겹침으로 조용히 깨질 수 있는 모양은 「한 테스트 안에서 두 업무가 같은 날 같은 시간을 잡는 것」뿐**인데,
그 둘을 뺀 모든 테스트가 **업무 하나**(`task_id = _spanned_task(client)` 단수)를 쓰고,
여러 배정을 만드는 자리는 **전부 날짜가 다르다**(`for day in (…)`).
→ **워커가 고친 그 하나가 유일한 자리였다.**

### 그 밖

- 새 소스·새 테스트에 `expect(True)` 류·`skip`·`xfail`·`except Exception`·빈 단언이 **0건**.
- 새 테스트 **39건**(계약 19 · 단위 13 · postgres 7)이 항목마다 붙어 있다 —
  경계 넷 · 자정 둘 · K12 3연타 · 자기 자신 빼기 · **K25 셋**(남의 회의 `:304` / 참석 회의 `:313` /
  남의 배정 `:327`) · **K26** `:288` · **K27** `:336` · **기존 데이터 불간섭** `:357`·postgres `:193`.
- 기존 테스트 중 **약화·삭제·skip 이 0건**이다(수정된 테스트 파일은 위 하나, +4/−2).

---

## WARN — **BE-4 브리프에 실을 것**

### WARN-1 → **BE-4 브리프 + 코디 확인** (증명 쪽)

**`make test-contract` 의 실패 3건이 기준선인지 새것인지가 문서로 남지 않았다.**

- 코디가 실물 확인한 것은 **`make test-unit` 369p/0f** 이고, `test-contract` **1135p/3f** 는
  **워커 보고**다. **`be3-report.md` 파일이 없어** 그 3건의 분리 근거를 읽을 수 없다.
- BE-2 때는 코디가 **2f 를 직렬 재실행으로 「무관」 판정**해 기록했다. 이번은 **3f 이고 그 기록이 없다.**
- 새 계약 테스트 19건이 바로 그 `test-contract` 층에 있으므로, **분리 없이는 이번 계약이
  초록이라는 증명이 닫히지 않는다.** (나는 테스트를 돌리지 말라는 지시라 확인하지 못했다.)

**브리프에 실을 한 줄**: 「BE-4 착수 전에 `test-contract` 3건의 **기준선 분리**를 한 줄로 남긴다 —
BE-2 의 `material_worker_recovery` flaky 와 같은 것인지, 셋째가 새로 생긴 것인지.」

### WARN-2 → **BE-4 브리프** (낮음)

**`_meeting_blocks` 가 회의마다 참석자 조회를 한 번씩 더 한다** — `platform/time_blocks.py:165`
가 루프 안에서 `_members_held_by`(`:182`)를 부른다.

- **BE-3 에서는 문제가 아니다** — `member_ids` 가 **나 하나**라 창 안 회의가 몇 건뿐이다.
- **BE-4 가 그 집합을 「주최자 + 참석자 전원」으로 넓힌다.** 그때는 회의 수 × 1 질의가 되고,
  그 경로가 **회의 생성·시각 변경마다** 돈다.
- **계약이 갈리는 자리가 아니다** — 결과는 같다. 고쳐도 되고 안 고쳐도 된다.

**브리프에 실을 한 줄**: 「참석자를 **한 번에** 읽어 회의별로 나누면 질의가 하나로 준다
(`meeting_id.in_(…)`). BE-4 에서 `member_ids` 가 넓어지니 그때 판단한다.」

---

## 확인한 것 (근거)

- **1** `overlapping_blocks` 호출을 `src/` 전수 grep(하나) · 공개 메서드 하나 ·
  `overlaps`/`split_…` 가 `time_blocks` 짝 밖으로 안 새는 것 · `PURE_DOMAIN_MODULES` 등재를 확인했다.
  `the_connect.py` 의 동명 함수가 **이번 diff 밖의 다른 도메인**임도 확인했다.
- **2** `overlaps` 를 네 방향(뒤·앞·포함·길이0)으로 **손으로 대입**해 확인했고, 길이 0 을 막은 이유가
  「기존 회의 행은 CHECK 보장을 안 받는다」로 옳은 것을 확인했다.
- **3** `split_across_office_dates` 를 23:00~01:00 과 23:00~24:00 두 입력으로 **손으로 돌려** 두 조각/한 조각을
  확인했고, `within` clip 이 쪼개기 **앞**인 것과 `office_dates_in` 의 1마이크로초 보정을 확인했다.
- **4** `creation_commands.py` 가 이번 diff에 **없음**을 확인해 BE-1 의 순서가 사는 것을 확인하고,
  `:739` 의 자리와 테스트 `:222` 의 3연타(`201/200/200` + 회차 1)를 읽었다.
- **5** `ignore_schedule_id` 가 **id 하나**로 좁히는 것과 생성 쪽에 안 넘기는 이유를 확인했다.
- **6** `bootstrap:4323` 의 같은 session 조립과 BE-1 의 단일 commit 구조를 확인했다.
- **7** postgres 테스트의 `contype='x' == []` 단언 **두 표**를 직접 읽었다.
- **8** 고친 테스트의 전후를 비교해 **단언이 늘었음**을 확인하고, 같은 모양(두 업무·같은 날·같은 시간)이
  다른 테스트에 있는지 전수로 훑어 **없음**을 확인했다.
- **read-only 준수** — 코드 한 줄도 고치지 않았고 **테스트를 돌리지 않았다.** 산출물은 이 리포트 하나.

---

## `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar status --short`

```text
 M backend/src/ax_workspace/bootstrap/application.py
 M backend/src/ax_workspace/entrypoints/http.py
 M backend/src/ax_workspace/modules/work/application.py
 M backend/src/ax_workspace/modules/work/errors.py
 M backend/tests/architecture/test_test_pyramid.py
 M backend/tests/contract/test_task_schedules.py
?? backend/src/ax_workspace/modules/time_blocks.py
?? backend/src/ax_workspace/platform/time_blocks.py
?? backend/tests/contract/test_task_schedule_overlap.py
?? backend/tests/integration/postgres/test_task_schedule_overlap_postgres.py
?? backend/tests/unit/test_time_blocks.py
```

(검수 시작 시점과 **같다** — 읽기만 했다. **회의 도메인 파일 0건**이라 경계도 지켰다.)
