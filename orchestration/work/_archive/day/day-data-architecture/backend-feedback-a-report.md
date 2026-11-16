# 화면 피드백 1차분 — F8 오더 메모 (백엔드)

## 결론: 매핑은 맞다 — 오늘 일정의 KOS `orderMemo` 가 비어 있다

데모 지점에서 일정 조회 `get-schedules-grouped-by-zone` 만 읽었다. 칸 이름과 「값 있음/없음」 수만 셌고, 값은 남기지 않았다.

| 칸(일정 응답 안) | 오늘(일정 2) 값 있음 | 지난 30일 + 3일(일정 322) 값 있음 | 뜻 |
|---|---|---|---|
| `orderMemo`(일정 단위) | **0 / 2** | 14 / 322 | 오더 메모 — 지금 매핑하는 칸 |
| `consultation.consultationMemo` | 1 / 2 | 15 / 322 | 상담 메모 |
| `reservation.reservationMemo` | 0 / 2 | 240 / 322 | 예약 메모 |
| `visitor.memo` | 0 / 2 | 8 / 322 | 고객 메모 |
| `tasks[].memo` · `assigneeMemo` · `doctorMemo` | 0 / 8 작업 | 5 · 10 · 10 / 244 작업 | 작업(시술) 단위 메모 |
| `etceteraWorks[].memo` · `taskTimers[].memo` | — | 1 / 18 · 8 / 8 | 기타 작업 · 타이머 |

- **오더 메모 = 일정의 `orderMemo`** 다. 근거는 셋이다.
  - 이 칸은 응답에 늘 있고, 다른 날 일정에는 값이 있다(14건).
  - 원천 ERD `03-visit.md` 「`procedure_order_note` ← orderMemo · 오더지에 인쇄되는 메모」와 같다.
  - cc 원천 `workflow-v2.md` 「오더 메모 = 일정의 `orderMemo`(일정에 하나, 작업별 아님)」와 같다.
- 오늘 방문 2건의 DB `procedure_order_note` 가 빈 것은 KOS 값이 비어서다. 로컬 `day_dev` 에서 최근 방문 2 중 값 있는 것 0 — KOS 와 같다.
  - 오늘 일정에 값이 있는 메모는 **상담 메모**(`consultation.consultationMemo`) 1건뿐이다.
  - 화면에 기대한 글이 그 상담 메모였을 수 있다. 그래도 오더 메모 칸으로 옮겨 채우지 않았다(추정 금지 · AGENTS.md 「다른 칸으로 추정해 채우지 않는다」).
  - 상담 메모는 #230 상담(`consultation`) 동기화 범위다. 카드에 보일지는 사용자 · 코디 결정이다.
- HAR(cc-prototype · overall-board)에는 메모 칸을 쓰는 요청이 없다. 오더 메모를 어느 화면에서 쓰는지는 HAR 로 확인할 수 없다(「없음」).

## 고친 것
- **매핑 코드 변경 없음**(`mapper.visit` → `procedure_order_note = text(orderMemo)` 그대로).
- 테스트(DB 없이 · `tests/day/emr/test_kos_mapper.py`): `test_오더_메모는_일정의_orderMemo_만`
  - `orderMemo` 가 들어온다.
  - `orderMemo` 가 빈 글자이거나 null 이면 None 이다.
  - 다른 메모 칸 여섯(작업 셋 · 고객 · 상담 · 예약)에 값이 있어도 오더 메모로 채우지 않는다.

## SPEC 대조
- SPEC-000 · 002 원문은 이 워크트리 · 프로필에서 찾지 못했다(GitHub 이슈 본문에는 「오더 메모」 화면 언급만 있고 KOS 칸 표가 없다).
  - 원천 ERD 와 코드는 `orderMemo` 로 같다.
  - planner 가 SPEC 의 「KOS 칸」 표에서 `procedure_order_note ← orderMemo`(일정 단위)인지 한 번 확인해 주면 된다.

## 검증
| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | 282 passed |
| ruff check · format --check | 통과 |
| compose | down 안 함 · `--profile app up -d --build --wait worker` healthy |
| KOS | 조회만(일정 조회 34회 — 30일 + 3일 · 오늘). 쓰기 0 |

## 남은 것
- 카드에 상담 메모도 보일지(F8 기대가 그 글이었다면) — 사용자 · 코디 결정.
- 실물 확인은 KOS 데모에서 오늘 일정에 오더 메모를 넣으면 10초 안에 카드에 뜬다. 데모 데이터에 쓰는 일이라 하지 않았다.
