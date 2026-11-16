# 리뷰 리포트 — interpreter-idea WP19 / code (2026-11-14)

대상: `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea` 미커밋 변경 6파일(`git diff` · untracked 0)
SSOT: SPEC-001 0.7.0 §2.4 · §5.9 「보관 기간 — env」 · 「삭제 규칙」 · 기동 ② ④ · §9.1 「기록」 ⑦ ⑨ · WORK WP19 · DEC D-42

## 판정: WARN

FAIL 은 없다. SPEC §5.9 표의 네 갈래가 코드와 시험에 모두 맞고, 기본값(off)에서는 기동 삭제와 24시간 태스크가 둘 다 없다. 아주 큰 N 에서 기동이 죽는 자리 1건을 WARN 으로 남긴다(운영 기본은 값을 넣지 않아서 지금은 닿지 않는다).

### 관문(리뷰어가 직접 1회 실행)
- `uv run ruff check .` → All checks passed!
- `uv run pytest -q tests/test_records.py tests/test_api_surface.py tests/test_interpret.py` → **172 passed**, 1 warning (backend 보고의 172 와 같다)

## FAIL
없음.

## WARN

### W-1 아주 큰 N 이면 기동이 죽는다 — 「기동은 멈추지 않는다」에 어긋남
- 위치: `back/app/service/records.py:154`(`date − timedelta(days=N)`) · `back/app/service/records.py:122`(`int(value)`) · 호출 경로 `records.py:261` → `main.py:72`(lifespan · try 없음)
- 재현(리뷰어 실행):
  - `INTERPRET_RECORD_KEEP_DAYS=1000000`(오늘 서수 ≈ 739,5xx 보다 큰 N 모두) → 로그 `keep_days=1000000` 뒤 `OverflowError: date value out of range` → **앱 기동 실패**(TestClient lifespan 으로 확인)
  - 4300 자리 넘는 숫자 → `parse_keep_days` 안 `int()` 가 `ValueError(Exceeds the limit (4300 digits))` — docstring 「예외를 올리지 않는다」(`records.py:116~118`)와 어긋남 → 같은 길로 기동 실패
- 근거: SPEC §5.9 「보관 기간」 표 아래 「잘못된 값 때문에 기동이 멈추면 안 된다」 · 기동 ③ 「기록 때문에 기동을 멈추지 않는다」 · D-42. 표대로면 이 값은 「양의 정수 N」이라 삭제를 켜는 쪽이지만, 어느 갈래로 봐도 기동이 죽는 것은 계약 밖이다.
- 영향: 운영은 ConfigMap 에 키를 넣지 않는다(§9.6 · OQ-020)라서 WP20 에서는 닿지 않는다. 베타가 끝나 값을 넣을 때 오타(`7000000` 같은 것)가 나면 back 이 CrashLoop 에 빠진다.
- 제안(backend 몫): `sweep()` 에서 cutoff 계산의 `OverflowError` 를 잡아 「지울 것 없음」으로 두거나, `parse_keep_days` 에서 자릿수나 상한(예: `date.today().toordinal()` 미만)을 보고 넘으면 경고 1줄 뒤 off 로 둔다. 어느 쪽이든 시험 1건(`"1000000"` → 기동 성공)을 더한다. SPEC 에 상한 문구가 없으니 off 와 「삭제 0 인 N」 중 어느 쪽으로 할지는 코디가 정한다.

## 항목별 대조 (브리프 §2)

| # | 항목 | 결과 | 근거 |
|---|---|---|---|
| 1 | §5.9 표 — 비었음 · 없음 · 공백만 → 경고 0 · off | 같음 | `records.py:116~125` · `config.py` `env_ignore_empty=True` 로 빈 env → `""` · 시험 `test_keep_days_empty_never_deletes[None/""/"   "]`(`test_records.py:466`) |
| 1 | 십진 숫자 1 이상(`7` · ` 7 ` · `07`) → N | 같음 | `_DIGITS=[0-9]+` fullmatch + `>=1` · 시험 `test_records.py:484`(3건 · 기동 삭제 3 · 남김 3 · `slept==[86400.0]`) |
| 1 | 그 밖(`0` · `-1` · `abc` · `+7` · `7.0` · `7d`) → 경고 1줄 · off · 기동 성공 · 기록 켜짐 | 같음 | 시험 `test_records.py:502`(경고 1줄 · 파일 그대로 · 세션 줄 4개 써짐) · `test_parse_keep_days`(`:523`, `7d` 포함) |
| 1 | 기록 끔 + 값(`7` · `abc`) → `interpret records: off` 만 · 경고 0 | 같음 | `records.py:246~248`(판정 전에 return) · 시험 `test_off_when_empty[7]` · `test_open_records_off_without_folder[""/7/abc]` (§9.1 ⑦) |
| 2 | off 일 때 기동 sweep 0 | 같음 | `records.py:260~261` + `sweep()` 자체도 `keep_days is None` 이면 0(`:152`) — 이중 방어 |
| 2 | off 일 때 24시간 태스크 0 | 같음 | `main.py:75` `keep_days is not None` 일 때만 `create_task` |
| 2 | 로그 `keep_days=off` · `sweep: deleted=` 줄 0 | 같음 | `records.py:258` · 시험이 `"sweep" not in caplog.text` 로 확인 |
| 3 | 태스크 생성 여부를 실제로 보나(조용히 통과) | 본다 | off 시험의 `slept == []`(`:474` · `:512`)는 양성 대조 (b) `slept == [86400.0]` 와 짝이라 빈 단언이 아니다 — 태스크가 생기면 잠이 1번 기록되는 것이 같은 장치로 확인된다 |
| 3 | 설정 클래스에서 기동이 죽는 길 | 없음 | `interpret_record_keep_days: str`(정수 변환 안 함) · 시험 `test_settings_reads_keep_days_as_text`(`:528`, `"   "`·`abc`·`-1`·`7.0`) |
| 3 | 유니코드 숫자 | off(경고) | `[0-9]` 는 ASCII 범위 — `٧` 은 시험에 있고, 리뷰어가 전각 `７` 도 off+경고 1줄인 것을 확인. `str.strip()` 은 유니코드 공백(`　` · 탭 · 개행)도 지워 `"\t7　"` → 7 (§5.9 「앞뒤 공백을 지운 뒤」와 맞다) |
| 3 | 아주 큰 N | **WARN W-1** | 위 |
| 4 | D-41 그대로 — 줄 모양 · term 판정 · 넣지 않는 것 · 쓰기 실패 | 무변경 | `records.py` diff 는 보관 기간 관련 줄뿐(`KEEP_DAYS` 삭제 · `parse_keep_days` · `Recorder.keep_days` · `sweep` 머리 · `open_records`). 기존 ①~⑥ · ⑧ 시험 본문 무변경 |
| 4 | `test_api_surface.py` | 무변경 · 통과 | `git diff --stat` 0 |
| 5 | allowed_paths(`back/` · `.env.example`) 밖 변경 | 0 | 변경 6파일 모두 범위 안 · untracked 0 |
| 5 | 키 · 기록 문장 | 0 | `.env.example` 은 이름만(`:21` 값 없음). 경고 로그는 env 값만 찍는다(비밀 아님) |
| — | 0.6.0 삭제 규칙(대상 · 실패 계속 · 로그) N 으로 그대로 | 같음 | 기존 `test_sweep_*` 을 `keep_days=7` 로 옮김 — 24시간 뒤 다시 · 실패 하나 뒤 계속 · 폴더 · 다른 이름 남김 |

## 고객이 실물에서 만날 자리 (WP20)
- 운영 기동 로그 `interpret records: on dir=/data/records keep_days=off` 1줄과 `sweep: deleted=` 줄 0 을 확인한다. 배포 전후 `ls -l /data/records` 에서 가장 오래된 파일(11-11)과 파일 수가 그대로인지 본다. **11-18 전에** 반영해야 한다(0.6.x 가 떠 있으면 그날 11-11 파일이 지워진다 · §9.6).
- 나중에 베타가 끝나 ConfigMap 에 값을 넣을 때(OQ-020): 첫 기동에서 N 일보다 오래된 파일이 **한꺼번에** 지워지고, 값에 오타가 있으면 경고 1줄 뒤 off 다(삭제가 조용히 안 켜진다 — 로그에서 `keep_days=N` 을 확인할 것). 아주 큰 값은 W-1 이 고쳐지기 전까지 기동 실패로 이어진다.

## 참고(기존 부채)
- `sweep_forever` 안에서 `sweep()` 이 예상 밖 예외를 올리면 태스크가 조용히 끝나고 이후 24시간 삭제가 멈춘다. 0.6.0 부터 있던 구조이고 W-1 말고는 닿는 길이 없다(OSError · ValueError 는 안에서 잡는다).
