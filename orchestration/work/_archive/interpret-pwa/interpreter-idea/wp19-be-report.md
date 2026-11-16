# WP19 backend 결과 보고 — 통역 기록 보관 기간 env (D-42 · SPEC 0.7.0)
## 상태: done (커밋 · push 없음 — 워크트리 변경만)

## 수행 — 파일 · 모듈
- `back/app/config.py` — `interpret_record_keep_days: str = ""` (문자열로 받음 → `abc` 로 기동이 죽지 않음)
- `back/app/service/records.py` — `KEEP_DAYS = 7` 삭제 · `parse_keep_days(raw) -> int | None` 추가(strip → 빈값 = None 경고 0 / `[0-9]+` fullmatch 이고 ≥1 = N / 그 밖 = 경고 1줄 뒤 None, 예외 없음) · `Recorder(keep_days=…)` · `sweep()` 은 keep_days None 이면 0 반환(로그 없음) · `open_records(..., keep_days=<env 원문>)` 기동 로그 `interpret records: on dir=<경로> keep_days=<N|off>` · 기동 삭제는 N 일 때만. 폴더 비었으면 값 판정 자체를 안 함(경고도 0)
- `back/app/container.py` — `open_records` 에 `settings.interpret_record_keep_days` 전달
- `back/app/main.py` — lifespan 24시간 배경 작업은 `recorder.keep_days is not None` 일 때만 생성
- `.env.example` — `INTERPRET_RECORD_KEEP_DAYS=` 이름만 + 한 줄 설명
- `docker-compose.yml` — 변경 없음(`env_file: .env` 로 이미 전달됨)
- `back/tests/test_records.py` — 아래 시험

## 검증
- `uv run ruff check .` → All checks passed!
- `uv run pytest -q` (back 전체) → **328 passed**
- WORK 검증 명령 `pytest -q tests/test_records.py tests/test_api_surface.py tests/test_interpret.py` → **172 passed** (test_records 68)
- Soniox · Procedure Hub 실물 호출: 이 WP 는 해당 경로 변경 없음 — 불필요(pending 아님)

## 계약 대조 (SPEC §5.9 · §9.1 「기록」)
| 항목 | 시험 | 결과 |
|---|---|---|
| ⑦ 폴더 비면 끔 — 값 7 을 줘도 같음 | `test_off_when_empty[None/7]` · `test_open_records_off_without_folder[""/7/abc]` | 같음 |
| ⑨(a) 없음 · `""` · `"   "` → 경고 0 · 삭제 0 · 배경 작업 없음 · `keep_days=off` · sweep 줄 0 | `test_keep_days_empty_never_deletes` ×3 · `test_on_log_line_default_off` | 같음 |
| ⑨(b) `7` · ` 7 ` · `07` → −7 · −8 · 10-01 삭제, −6 · note.txt · .bak 남김 · 기동 1회 · 배경 작업 생성 · `keep_days=7` | `test_keep_days_7_deletes_at_startup` ×3 · 기존 0.6.0 시험(`test_sweep_*` · `test_sweeper_task_lives_with_app` · `test_on_log_line_keep_7`)을 값 7 로 옮김 — 24시간 뒤 다시 · 실패 하나 뒤 계속 포함 | 같음 |
| ⑨(c) `0` · `-1` · `abc` · `+7` · `7.0` → 경고 1줄 · 삭제 0 · 배경 작업 없음 · `keep_days=off` · 기동 성공 · 오늘 파일에 줄 써짐 | `test_keep_days_invalid_warns_and_keeps` ×5 | 같음 |
| 설정 읽기가 잘못된 값으로 죽지 않음 | `test_settings_reads_keep_days_as_text` ×4(env 직접) · `test_parse_keep_days` ×14(`7d` · 유니코드 숫자 `٧` 포함) | 같음 |
| ⑩ `test_api_surface.py` 변경 없이 통과 | 전체 실행 | 같음 |
| 기록 줄 모양 · term 판정 · 넣지 않는 것 · 쓰기 실패 | 코드 무변경 · 기존 시험 그대로 통과 | 같음 |

## 이슈 · 코디가 확인할 것
- 경고 문구: `interpret records: INTERPRET_RECORD_KEEP_DAYS='<값>' 는 양의 정수가 아니다 — 삭제 안 함` (값은 찍음 — 비밀 아님, SPEC 허용 범위)
- 코드 · 시험 · 보고에 키 · 계정값 · 기록 문장 0

## 수정 1 — 리뷰 W-1(아주 큰 N 에서 기동 실패) · SPEC §5.9 상한 36,500
- `back/app/service/records.py` — `KEEP_DAYS_MAX = 36_500` · `parse_keep_days`: 숫자만이면 앞 0 을 떼고 **자릿수(≤5)로 먼저 거른 뒤** `int()` · 1 ~ 36,500 만 N. 36,501 이상 · 4,300 자리 넘는 숫자 · `0…0` 은 경고 1줄 뒤 off — 어떤 문자열에도 예외 없음. 경고에 찍는 값은 앞 20 자까지(5,000 자리 값이 로그를 채우지 않게). 경고 문구 `… 는 1 ~ 36500 정수가 아니다 — 삭제 안 함`
- `back/tests/test_records.py` — `test_keep_days_upper_bound`(`36500` → 기동 성공 · `keep_days=36500` · 배경 작업 생성 · 삭제 0) · `test_keep_days_invalid_warns_and_keeps` 에 `36501` · `1000000` · `"9"*5000` 추가(TestClient lifespan — 경고 1줄 · off · 기동 성공 · 기록 켜짐) · `test_parse_keep_days` 에 `36500` · `0036500` · `36501` · `1000000` · `"9"*5000` · `"0"*5000` 추가
- 검증: `ruff check .` All checks passed · back 전체 `pytest -q` **338 passed** · WORK 명령 **182 passed**
- 그 밖 변경 없음
