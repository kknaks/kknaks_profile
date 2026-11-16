# 예약 현황 E2E batch 2 — backend 결과 보고
- 2026-10-27 · 기준 커밋 `1d482d8` 위 미커밋(procedure/back 만)
## 상태: done

## 처리 (backend 몫)
| # | 처리 |
|---|---|
| 1 | 해당 없음(front) |
| 2 | ✔ 상세 GET 이 그 일정을 KOS 에서 다시 읽다가 **404** 면 → 404 `reservation_gone` 「KOS 에서 사라진 예약이에요」(`{error:{code,message}}`). 로그는 일정마다 **한 번 · INFO**(같은 일정 폴링 반복에도 한 줄 · 다시 보이면 초기화) — WARNING 폭주 없앰. 사본은 그대로(등록 직후 KOS 가 잠깐 404 를 주므로 지우지 않음 — §3 데모 시험 · 날짜 조회가 목록으로 맞춘다). 등록 직후 다시 읽기는 이 규칙을 안 씀(옛 동작) |
| 3 | 보류(지시) |
| 4 | 해당 없음(front) |
| 5 | ✔ 상담사 목록(form `counselors` · 상세 `counselors` · 등록 `counselorStaffId` 검사 · [실장 호출] 검사) = COUNSELOR 태그 · 활성 · **시스템 계정 · `KOS_EXCLUDE_ACCOUNT_IDS` 뺌** — 시술 현황 원장 목록(`set_doctor_flags`)과 같은 규칙. 그 밖 COUNSELOR 태그 계정(예: 코디3)은 그대로 |
| 6 | 정렬용 값 추가 없음 — 상세 `rooms[]` 에 `busy` · `title`(KOS order 순)이 이미 있음 |
| 7 · 8 · 9 | 해당 없음(front) |

## 파일
- `app/service/reservations.py` — `_counselors(staff, system, exclude)` · `refresh_schedule(..., gone=True)` · 상세가 gone=True
- `app/service/reception.py` — [실장 호출] 상담사 검사에 제외 목록
- `app/domain/errors.py` — `NotFound(message, code="not_found")`(코드를 고를 수 있게)
- tests: `fake_kos.py`(없는 일정 = 실 KOS 처럼 404 NotFoundException) · `test_resv_detail.py` 새 시험 2(`test_detail_kos_gone_404_logged_once` · `test_counselors_exclude_system_and_excluded_accounts`)

## 검증
- `uv run ruff check .` → All checks passed · `uv run pytest -q` → **333 passed**

## 코디가 확인할 것
- 「마취용」 · 「KOS-DEMO」 는 **id 로** 뺀다(로그인 시스템 계정 id · env `KOS_EXCLUDE_ACCOUNT_IDS` — 지금 4개 들어 있음 · 값은 안 봄). 이름 판정은 코드에 없다(시술 현황도 id 목록). 재기동 뒤에도 목록에 남으면 그 계정 id 를 env 에 넣어야 한다
- SPEC 0.3.0: 404 `reservation_gone`(상세) 추가
