# [backend] Phase BE-4 — 회의 쪽 겹침 · `approval` · 운영 대장

너는 **strong-hajin `backend` 워커**다. **BE-3 을 네가 했다** — 맥락이 이어진다.

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`

> ⚠ **BE-3 은 커밋됐다.** 네 새 변경만 uncommitted.
> ⚠ **이 Phase 가 회의 도메인을 연다** — SPEC §1 Scope Out 이 뒤집힌 자리다. 조심해서 가라.
> ⚠ 커밋·push 금지. FE 는 손대지 마라.

## 작업 지시서

`…/30-work/work-004-calendar-scheduling.md` 의 **`Phase BE-4`**.
계약은 SPEC-004 **v0.3.1 §2.9** · 근거는 DEC-003 **증보 8 K22 · 증보 9 K25~K27**.

한 줄로: **회의 생성·시각 변경에 겹침 검증을 걸고, `approval` 을 싣고, 운영 대장을 닫는다.**

## 네가 BE-3 에서 남긴 것을 그대로 쓴다

```
overlapping_blocks(member_ids, window, *, ignore_meeting_id=...)
```

- `member_ids` 를 **주최자 + 활성 참석자 전원**의 `frozenset` 으로 부른다
- **사외 참석자(`external_attendees`)는 `member_ids` 에 안 들어가므로 자동으로 대상 밖**
- 시각 변경은 `ignore_meeting_id=자기 자신` — 안 빼면 시각을 한 칸도 못 옮긴다
- 거절 문구의 「누구」는 반환 블록의 `member_id` 로 조회한다. **제목은 애초에 블록에 없다**

## 검수가 대신 세어 준 것 — **census 는 끝났다**

리뷰어가 회의 도메인을 직접 셌다. **이 숫자로 시작하라. grep 은 그대로 하되 다르면 그게 발견이다.**

| 자리 | 수 | 비고 |
|---|---|---|
| 회의 생성 | **둘** — `application.py:290 create` · `:376 quick_start` | **둘이 `_repository.create` 를 각각 부른다 — 코드를 공유하지 않는다** |
| 시각 변경 | **하나** — `application.py:413 update_info` (쓰기 `:443-444`) | |
| 저장소 쓰기 문 | **하나** — `platform/meetings.py:69` | |

**그래서 `quick_start` 제외에 분기가 필요 없다** — `create` 에만 걸면 `quick_start` 는 자연히 안 탄다.

## 검수가 이 Phase 로 넘긴 것 — 둘

**WARN-1 (증명).** `test-contract` 3f 의 기준선 분리가 문서로 안 남았다. BE-2 때는 2f 를 직렬
재실행으로 무관 판정해 기록했는데 이번 3f 는 그 기록이 없다. **네 계약 테스트 19건이 바로 그
층이라 분리 없이는 이번 계약이 초록이라는 증명이 안 닫힌다.**
→ **코디가 닫았다.** `orchestration/work/strong-hajin-calendar/flaky-baseline-evidence.md` 를 읽어라.
요지: 코디 실측은 **5 failed**(워커는 3)였고 **실패 집합이 회차마다 바뀐다**. 두 파일만 **직렬로
돌리면 20 passed**. 기준선(착수 전)에도 같은 계열이 2건 실패했다 — **기존 flaky, 인과 없음.**
다만 우리가 계약 테스트를 58건 더해 **부하로 악화시켰을 수는 있다**(2f→3f→5f). 그 계열의 병렬
격리는 **이 작업 범위 밖**이다. **너는 이 판정을 그대로 쓰고, 네 새 실패만 따로 가려라.**

**WARN-2 (낮음, 성능).** `_meeting_blocks` 가 루프 안에서 회의마다 `_members_held_by` 를 부른다
(`platform:165→182`). BE-3 은 `member_ids` 가 하나라 무해했지만 **네가 주최자+참석자 전원으로
넓히면 회의 수 × 1 질의**가 되고, 그게 회의 생성·시각 변경마다 돈다.
→ `meeting_id.in_(...)` 로 한 번에 읽어 나누면 질의가 하나로 준다. **계약은 안 갈린다** — 판단은 너.

## 틀리기 쉬운 자리

1. **`quick-start` 는 막지 않는다** — 지금 당장 시작하는 것이라 막으면 못 쓴다.
2. **기존 회의 계약을 깨지 마라** — `my_meetings`·`readable_rows`·회의 목록 응답 모양.
   1루프에서 `meetings_visible_to` 소비처 셋이 걸렸던 자리다. **회귀 테스트를 남겨라.**
3. **`approval` 은 합본 조회 응답 필드다** — 열이 아니다. 스키마를 바꾸지 마라.
   값은 SPEC §4 가 정한 그대로(`null`·`awaiting_review`·`awaiting_revision`·`approved`).
   **`derived` 묶음 전체를 싣지 마라 — 이 한 값만.**
4. **운영 대장** — **새 라우트가 없다.** `http_count` **159 불변**. `approval` 이 합본 조회의
   `http_signature` 에 드는지 **확인하고**, 들면 **그 행만** 패치한다. 전체 재작성 금지.
5. **`MEETING_TIME_OVERLAP` 409** — 문구는 SPEC Case Matrix 그대로. **이름은 말하고 내용은 말하지
   않는다.** 그리고 **K12 사정권 밖이다** — 회의에는 멱등 영수증 규칙을 끌어들이지 마라.

## allowed_paths

`backend/` · `docker-compose.yml` · `Makefile` · **`docs/unified-operations-inventory.json`** ·
**`docs/domain-model.md`**. 그 밖 `docs/` 금지. `frontend/`·`para/`·`orchestration/` 금지.

## 검증

```
make test-unit          ← 운영 대장 통과가 관문
make test-contract
make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_calendar
```

기준선 (BE-3 직후): `test-unit` **369p/0f** · `test-postgres` **96p/0f** · `test-contract` 1135p/3f.

## 완료 보고

끝나면 **이 한 줄**을 실행해 코디를 깨워라:

```bash
orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac \
  --text "[worker_done] backend BE-4 완료 — <한 줄 요약>" --enter
```

본문에 담을 것: 변경 파일 / 구현 요약 / **검증 수치(각 passed/failed)** / 기존 flaky 와 새 실패의 분리 /
계약 준수 / **미결·주의점**. **막히면 30분 넘기지 말고 `[질문]` 으로 물어라 — 조용히 정하지 마라.**
