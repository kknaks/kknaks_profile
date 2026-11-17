# 리뷰 리포트 — ext-api-staff-fields / code (2026-11-17)

- 대상: 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/ext-api-staff-fields` 미커밋 diff(base `969f44f` · 5파일 · +54 −8 · untracked 0)
- 기준: SPEC-008 0.4.7 §6.17 · §6.1 「id」 · §8 · §9 T67 · T70 · WORK-015 계약 고정점 · DEC-012 D-48
- 검증 관문(직접 실행 · `procedure/back`): `uv run pytest -q tests/test_ext_clinic.py tests/test_ext_docs.py tests/test_openapi_docs.py` → **24 passed**
- 추가 확인(직접 · repo 파일 무변경): 임시 시험 파일을 넣어 돌리고 바로 지움(`git status` 로 5파일 그대로 확인). 아래 W2 의 동작을 실측함

## 판정: **PASS** (FAIL 0 · WARN 2 — 둘 다 이번 diff 의 계약 위반은 아니다)

## 항목별 대조

| # | 볼 것 | 결과 | 근거 |
|---|---|---|---|
| 1 | §6.17 응답 표 ↔ 코드 | 같음 | `app/service/ext.py:900-901` — `email`/`realName` = `a.get(k) or None`(null · 빈 문자열 · 칸 없음 → null · 그 밖은 그대로) · `kosAccountId = kid`(= `str(a["id"])` · 사본을 잇는 바로 그 값 · 사본 없어도 값 있음). `app/schemas/ext.py:501-506` — 타입 `str \| None` · `str \| None` · `str`(null 없음) · 세 칸 `description` 있음(§8 「모든 칸」). `name` 원천은 그대로 `a["name"]`(D-48 ② — 합치지 않음) |
| 1 | T67 ↔ 시험 | 같음 | `tests/test_ext_clinic.py:123-131` 키 집합 = 여덟 · `name` ≠ `realName` 가짜 값 · 사본 없는 계정 `staffId` null + `kosAccountId` 값 · `userId` · `licenseNumber` · `mfaMethods`(`mfa`) · `roleId` 여전히 없음. `:134-153` null · `""` · 칸 없음 세 갈래 · KOS 호출 1 · `ext_call` + 로그에 세 값 0. `:164-167` `id` 없는 원소 → 502(W4) |
| 1 | T70 ↔ 시험 | 같음 | `tests/test_ext_docs.py:140-143` — 설명에 `` `kosAccountId` `` 있음 · 옛 문장 없음 · `ExtStaff` 세 칸 description 있음. `test_openapi_docs.py` 통과 |
| 2 | 필드 추가만 | 맞음 | diff 는 `out.append` 한 줄 · 스키마 세 칸 · `STAFF_DOC` 문장 · 시험뿐. 행 고르기(`skip`) · 차례 · 오류 code · KOS 호출(1) · 다른 ext 경로 · 직원 API · 사본 표(`tx.staff()` 읽기만) · 동기화 · `fake_kos.py` 변경 0 |
| 3 | 응답 밖에 안 남음 | 맞음 | `ext_call` 은 연동처 · 경로 틀 · 상태 · 결과만(`app/service/ext.py:178-191`). 실패 로그는 `kos_errors.describe(e)` · 500 로그는 예외 **종류만**(`app/api/ext.py:123-124`) — W2 실측에서도 `외부 처리 오류: ValidationError` 뿐, 값 없음. 사본 저장 없음 |
| 4 | Swagger 옛 문장 전수 | 지워짐 | `grep -rn "이메일 · 실명 · KOS id 는 내지 않는다" app/` → 0. `app/api/ext.py:521-530` 첫 줄 칸 나열에 셋 · §6.17 지정 문장 그대로. 남은 「내지 않는다」 는 다른 경로(`:193` `:313` `:325` `:379` `:384` `:410`) 몫 — 무관. 단 공통 설명 id 줄은 W1 |
| 5 | 실제 값 grep | 0 | 더한 줄의 이메일 꼴 = `doc-a@` · `new-1@` · `kos-acct-x4@example.com` 뿐 · 실명 = `<실명…>` · KOS id = `doc-a` · `kos-acct-x*` 등 지어낸 값 |
| 6 | 조용히 통과하는 자리 | 아래 W2 · 참고 | — |

## FAIL

없음.

## WARN

**W1 — Swagger 공통 설명의 「id」 줄에 0.4.7 예외가 없다** — `app/openapi_docs.py:108-109`
- 지금: 「메뉴 · 시술권의 … id = KOS id 문자열 · 고객 · 예약 id = ccc 정수(고객의 KOS id 는 내지 않는다)」. SPEC §6.1 「id」 는 0.4.7 에서 「예외 하나 — 직원 목록 `kosAccountId` 는 직원의 KOS 계정 id 문자열」 을 더했는데(DEC-012 D-48), Swagger 첫 화면의 이 요약은 그대로라 KOS id 가 나오는 곳을 메뉴 · 시술권으로만 읽게 된다. 문장 자체가 틀린 것은 아니다(고객 KOS id 는 여전히 안 냄).
- 범위: SPEC §6.17 · §8 의 「Swagger 설명 고침」 은 `STAFF_DOC` 만 지정했고, WORK-015 BE1 대상 파일에 `app/openapi_docs.py` 가 없다 → **이번 diff 의 위반은 아니다(SPEC 이 정하지 않은 자리)**.
- 고칠 방향: 코디 판단 — 넣는다면 `openapi_docs.py:109` 괄호에 「· 직원 목록 `kosAccountId` 는 직원 KOS 계정 id 문자열(예외)」 한 구절(+ SPEC §8 에 한 줄). 안 넣으면 그대로 둬도 계약은 맞다.

**W2 — `email` · `realName` 이 문자열이 아닌 값으로 오면 `500 internal_error`(502 아님)** — `app/service/ext.py:900-901` · `app/schemas/ext.py:501-503`
- 실측: 가짜 원소 `email = 123` · `realName = {"a": 1}` → 둘 다 `500 internal_error`, `ext_call` = `(500, internal_error)`, 로그 = `외부 처리 오류: ValidationError`(값 없음). `roleName = 5` 도 똑같이 500 — **`roleName` 선례와 같은 동작**이다. 공백뿐 `"  "` 은 200 · 그대로 옮김(SPEC 「다듬지 않는다」 와 맞음).
- SPEC 판정: §6.17 2단계의 502 갈래는 「실패 · `data` 배열 아님 · 원소가 객체 아님 · `id` 없음」 뿐이고 칸 타입 갈래는 **없다**. 그러니 계약 위반이 아니고 새 계약을 만들 일도 아니다. 시험도 이 갈래를 단언하지 않는다(T67 이 요구하지 않음).
- 고칠 방향: 이번엔 고치지 않는다. 바꾸려면(문자열 아닌 값 → 502 또는 null) SPEC §6.17 2단계에 갈래를 먼저 더하고 `roleName` 까지 같이 맞춘다 — 별 판.

## 조용히 통과하는 자리 (참고 · 조치 불필요)

- `test_t67_staff_email_realname_null` 의 「응답 밖 0」 단언(`tests/test_ext_clinic.py:151-153`)은 이 시험 안의 `caplog` 만 본다. 정상 경로(`log.info("외부 호출 …")`)와 실패 경로 로그가 모두 값을 싣지 않는 코드라 지금은 참이다. 앞으로 누가 `staff()` 안에 원소 값을 찍는 `log.debug` 를 넣으면 이 시험이 잡는다(`DEBUG` 로 열어 둠) — 잘 되어 있음.
- `id` 가 빈 문자열(`""`)인 원소 → 502 는 코드(`x.get("id")` 거짓)로 성립하지만 시험은 「칸 없음」 갈래만 단언한다. SPEC T67 이 요구한 것은 「`id` 없는 원소」 이라 충분.
- T70 옛 문장 단언은 정확한 한 문자열만 본다(`"이메일 · 실명 · KOS id 는 내지 않는다" not in`). 지금 소스 전수 grep 0 이라 문제없음.

## 고객(연동처 · Swagger 독자)이 실물에서 만날 자리

1. **새 세 칸은 항상 키가 있다** — `email` · `realName` 은 값이 없으면 `null`(빈 문자열도 `null`), `kosAccountId` 는 언제나 문자열. 기존 다섯 칸 · 차례 · 비활성 포함은 그대로라 기존 파서는 깨지지 않는다(키만 늘어남 — 연동처가 모르는 키를 거부하는 엄격 파서라면 영향).
2. **`kosAccountId` ≠ `staffId`** — 다른 ext 응답(접수 목록 · 예약 상세 `counselor.staffId`)은 ccc 정수다. 둘을 잇는 곳은 이 목록뿐이고, 사본 동기화 전 새 계정은 `staffId = null` 이지만 `kosAccountId` 는 있다. Swagger 직원 설명 · 스키마 설명에 적혀 있음.
3. **`realName` 과 `name` 은 다른 칸** — `name` 은 KOS 표시 이름(예 「가 원장」), `realName` 은 실명. 같을 수도, `realName` 만 null 일 수도 있다.
4. **KOS 값을 다듬지 않는다** — 이메일 대소문자 · 앞뒤 공백도 KOS 그대로(공백뿐인 값도 그대로 나온다).
5. **비활성 직원의 이메일 · 실명도 나온다**(비활성 포함 규칙 + D-48). 연동처 키 하나로 병원 전 직원의 이메일 · 실명을 받는다 — D-48 사용자 결정이므로 계약대로지만, 협업자 안내(WORK-015 DEPLOY 「사용자 몫」) 때 함께 알릴 점.
6. KOS 가 이상한 타입을 주면 `500 internal_error` 로 보인다(W2 · 기존 `roleName` 과 같음).
7. Swagger 첫 화면 공통 「id」 요약에는 직원 KOS id 예외가 안 적혀 있다(W1).

## 참고(기존 부채)

- `roleName` 비문자열 → 500 은 0.4.0 부터 있던 동작(W2 와 같은 뿌리).
- allowed_paths: 리뷰어는 이 리포트 1개만 만들었다. repo 파일 변경 0(임시 시험 파일은 실행 뒤 즉시 지움 · `git status` 5파일 그대로).
