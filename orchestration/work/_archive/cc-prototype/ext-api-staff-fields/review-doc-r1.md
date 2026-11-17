# 리뷰 리포트 — ext-api-staff-fields / doc (2026-11-17)

대상: SPEC-008 0.4.7(`git diff` · 작업 트리) · WORK-015(새 파일) · DEC-012 D-48.
코드 대조: `cc-prototype` main `969f44f` `procedure/back`(읽기만 · 시험 실행 안 함).

아래에서 `SPEC` = `para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md`,
`WORK` = `para/projects/summer-star/cc-prototype/30-work/work-015-ext-api-staff-fields.md`,
코드 경로는 `procedure/back/` 기준이다.

## 판정: WARN

FAIL 0 · WARN 5 · 참고 4. D-48 은 빠짐 · 넘침 없이 옮겨졌고 BE1 은 지금 문서로 착수할 수 있다.
WARN 은 전부 문서 한두 줄 고침이다. W1 · W2 는 발주 전에 고치기를 권한다(W2 는 고치지 않으면 옛 Swagger 문장이 남아도 시험이 초록이다).

## FAIL

없음.

## WARN

### W1. §4.4 에 「KOS id 는 메뉴 · 시술권 id 에만 낸다」 가 본문 규칙으로 남아 있다

- `SPEC:379` — 「내지 않는 칸: 카드 KOS id · … (KOS id 는 메뉴 · 시술권 id 에만 낸다 — 코디 Q2 · 부록 B)」
- 근거: DEC-012 D-48 ③ · SPEC §6.1 「id」(`SPEC:417` — 0.4.7 이 예외 줄을 더한 바로 그 규칙). §4.4 는 기록(부록)이 아니라 본문이라, 「에만」 이 0.4.7 뒤로는 틀린 문장이다. 선불카드 규칙 자체(카드 KOS id 안 냄)는 그대로가 맞다
- 고칠 방향: 괄호를 「KOS id 는 메뉴 · 시술권 id 와 직원 목록 `kosAccountId`(§6.17 · 0.4.7)에만 낸다」 로 고치거나 「§6.1 「id」」 를 가리키게 한다
- 같은 문장의 기록 쪽 둘(`SPEC:1154` 부록 B Q2 · `SPEC:1260` 부록 G Q1)은 그때의 답 기록이라 두는 것이 맞다 — planner 판단과 같다

### W2. 옛 Swagger 문장이 지워졌는지 고정하는 시험이 없다 · 검증 명령에 `tests/test_ext_docs.py` 가 빠졌다

- `SPEC:895`(§6.17 Swagger 설명 고침) · `SPEC:991`(§8 엔드포인트(0.4.0)) 가 문장 교체를 계약으로 적었는데, `SPEC:1069` T67 · `SPEC:1072` T70 어느 쪽에도 그 단언이 없다
- `WORK:68` 완료 조건 「Swagger 시험 통과」 의 명령은 `tests/test_openapi_docs.py` 뿐이다 — 그 파일은 칸마다 `description` 이 있는지만 본다(`tests/test_openapi_docs.py:63-68`). 직원 목록 설명 문장을 단언하는 곳은 `tests/test_ext_docs.py:138-140` 이고 명령 · 대상 파일에 없다
- 결과: BE1 이 `app/api/ext.py:527` 의 「이메일 · 실명 · KOS id 는 내지 않는다」 를 그대로 둬도 시험은 전부 통과한다 — 응답은 세 칸을 내는데 문서는 안 낸다고 말하는 상태가 조용히 남는다. 앞 판(0.4.2 · N4)은 같은 종류의 옛 문장을 T70 에 「**없음**」 단언으로 고정했다(`SPEC:1072`)
- 고칠 방향: T70(또는 T67)에 「직원 목록 설명에 `kosAccountId` 있음 · 옛 문장 『이메일 · 실명 · KOS id 는 내지 않는다』 없음」 을 더하고, `WORK:68` 의 대상 파일 · 검증 명령에 `tests/test_ext_docs.py` 를 더한다

### W3. `email` · `realName` 의 null 규칙에 KOS 가 `null` 을 줄 때가 안 적혀 있다

- `SPEC:888` · `SPEC:889` — 「빈 문자열이거나 칸이 없으면 null」 · `SPEC:1069` T67 도 두 갈래(빈 문자열 · 칸 없음)만 든다. `WORK:58` · `WORK:82` 도 같다
- 근거: DEC-012 D-48(「빈 문자열을 주거나 칸을 빼면 `null`」) 을 글자 그대로 옮긴 것이라 어긋남은 아니다. 다만 값이 JSON `null` 일 때를 워커가 정해야 한다. 같은 함수의 선례는 `a.get("roleName") or None`(`app/service/ext.py:899`)이라 자연스러운 답은 null 이다
- 고칠 방향: §6.17 표 두 줄을 「`null` · 빈 문자열 · 칸 없음 → null」 로, T67 가짜 원소에 `null` 갈래 하나를 더한다(결정을 새로 만드는 것이 아니라 빈칸 메우기)

### W4. §6.17 4단계가 가리키는 「2단계의 502」 에 그 조건이 없다 · 시험도 없다

- `SPEC:874` — 「원소에 `id` 가 없으면 지금처럼 2단계의 `502` 다」. 그런데 2단계(`SPEC:872`)는 「실패 · `data` 가 배열 아님 → `502`」 만 적는다. 코드는 원소가 객체가 아니거나 `id` 가 비면(없음 · `""` · `0`) 502 다(`app/service/ext.py:884`)
- `SPEC:890` 의 「`kosAccountId` 에 null 이 없다」 가 이 동작에 기대는데, T67(`SPEC:1069`)의 502 갈래는 「실패 · `data` 배열 아님」 뿐이고 지금 시험(`tests/test_ext_clinic.py:134-138`)에도 `id` 없는 원소 갈래가 없다
- 근거: SPEC §6.17 4 · 응답 표 `kosAccountId` 줄 · DEC-012 D-48 ③. planner 주의 「원소 `id` 없으면 지금도 502」 는 맞다(코드 확인)
- 고칠 방향: 2단계에 「· 원소가 객체가 아님 · `id` 없음(빈 값)」 을 더하고(코드 그대로 · 동작 변화 0), T67 에 「`id` 없는 원소 → 502」 한 갈래를 더한다

### W5. WORK-015 검증 명령의 실행 위치 · 경로 표기가 섞여 있다

- `WORK:68` — 대상 파일은 `procedure/back/app/{…}` 로 레포 루트 기준인데 `tests/test_ext_clinic.py` · `tests/fake_kos.py` 와 명령(`uv run pytest -q tests/…`)은 `procedure/back` 기준이다. 실행 위치가 문서에 없다
- 근거: 체크리스트 「워커가 추측으로 메워야 하는 빈칸」. 실물은 맞다 — `procedure/back/pyproject.toml` · `uv.lock` 이 있고 pytest · ruff 가 거기 선언되어 있다
- 고칠 방향: 「(`procedure/back` 에서)」 한 마디를 명령 앞에 더하고 시험 파일 경로를 같은 기준으로 맞춘다

## 볼 것 다섯 — 대조 결과

### 1. D-48 → SPEC 0.4.7 (빠짐 0 · 넘침 0)

| D-48 항목 | SPEC 자리 | 판정 |
|---|---|---|
| 칸 셋 이름 `email` · `realName` · `kosAccountId` | `SPEC:888-890` | 같음 |
| `email` = 내부 원소 `email` · `realName` = 내부 `realName` · `kosAccountId` = 내부 `id` | `SPEC:874` · `:888-890` | 같음 |
| `name` 은 그대로 · `realName` 과 다른 칸 | `SPEC:889` · T67(`:1069` — 두 값이 다른 가짜 원소) | 같음 |
| `kosAccountId` 는 `staffId` 와 다른 체계 · 잇는 곳은 이 목록뿐 | `SPEC:890` · `:417` | 같음 |
| `email` · `realName` 빈 문자열 · 칸 없음 → null | `SPEC:888-889` | 같음(W3 — `null` 값) |
| 필드 추가만 — 기존 다섯 칸 · 행 고르기(D-21) · KOS 호출 수 1 | `SPEC:104` · `:81` · `:674`(§6.9 그대로 1) · `:873`(3단계 무변경) | 같음 |
| 사본에 이메일 저장 안 함 · 매 호출 KOS 값 | `SPEC:874` · `:893` | 같음 |
| 응답 밖(`ext_call` · 로그 · 리포트 · 시험 데이터)에 안 남김 | `SPEC:893`(ext_call · 로그) · `:1069`(시험 데이터 = 지어낸 값) · `:82`(public 머리말) · `WORK:51` · `:84`(리포트 · 커밋) | 같음 |

- D-48 에 없는데 SPEC 이 더한 것: `kosAccountId` 타입 string · null 없음(`SPEC:890`) — 코드 규약 `app/service/ext.py:884` · `:894` 에서 나온 것이라 넘침이 아니다. Swagger 문장(`SPEC:895`)도 §8 규약의 적용이다
- SPEC 이 인용한 코드 줄은 실물과 맞다 — `app/service/ext.py:884`(모양 검사) · `:894`(`kid = str(a["id"])`) · `app/api/ext.py:520-529`(`STAFF_DOC`) · `app/schemas/ext.py:491-501`(`ExtStaff`)
- 부록 F D-15 줄(`SPEC:1219`) · D-48 줄(`:1252`) · DEC-012 D-15 고침 줄(DEC `:97`) · D-48(DEC `:147`) 서로 맞다. frontmatter(버전 0.4.7 · `links.works` WORK-015 · sources) · `20-spec/README.md:12` · `30-work/README.md:19` · `work-index.md:12` · `orchestration/work/README.md` 진행 수 0 → 1 맞다

### 2. 어긋나는 남은 줄 — 전수

`이메일` · `realName` · `실명` · `KOS id` · `KOS 계정 id` · `계정 id` 로 SPEC 전체를 세고 직원 목록에 대한 줄만 남겼다.

| 줄 | 내용 | 판정 |
|---|---|---|
| `SPEC:379`(§4.4) | 「KOS id 는 메뉴 · 시술권 id 에만 낸다」 | **W1** |
| `SPEC:417`(§6.1) | 예외 줄 더함 | 고쳐짐 |
| `SPEC:892`(§6.17) | 「넣지 않는 칸」 에서 셋 취소선 | 고쳐짐 |
| `SPEC:991`(§8) | 옛 문장 지움 지시 | 고쳐짐(W2 — 시험 없음) |
| `SPEC:1069`(§9 T67) | 「키 0」 취소선 → 키 집합 여덟 | 고쳐짐 |
| `SPEC:1154`(부록 B Q2) · `:1260`(부록 G Q1) | 「KOS id 는 메뉴 · 시술권에만」 | 기록 — 그대로가 맞다 |
| `SPEC:1219`(부록 F D-15) | 「이메일 없음」 취소선 | 고쳐짐 |

- §0(`SPEC:119`) · §1 · §3.4 · §7 · §7.4 에는 직원 이메일 · 실명 · 계정 id 를 「내지 않는다」 는 문장이 없다
- lookup(`SPEC:502`) · 예약 상세(`:776`) · 선불카드(`:379` 앞 절반) · T16(`:1018`) · T69(`:1071`)의 「이메일 · KOS id 없음」 은 고객 · 다른 경로 규칙이라 그대로가 맞다

### 3. T67 (`SPEC:1069`)

- 새 계약 고정: 원소 키 집합 여덟 · `email` · `realName` · `kosAccountId` 값 대조 · 사본에 없는 계정도 `kosAccountId` 값 · 빈 문자열 · 칸 없음 → null · 남은 넷 키 0 · KOS 호출 1 · `ext_call` · 로그에 세 값 0 — D-48 전 항목이 단언으로 내려왔다
- 지금 시험과의 거리(BE1 이 뒤집을 자리 — planner 주의와 같다): `tests/test_ext_clinic.py:121` · `:123` 의 다섯 키 통째 비교 → 여덟 키 · `:124` 의 leak 목록 중 `"@example.com"` · `"<실명"` · `"doc-a"` 는 「있음」 으로, `"u-doc-a"` · `"L-0"` · `"mfa"` · `"roleId"` 는 그대로. `"u-doc-a"` 는 `kosAccountId` 값 `"doc-a"` 를 품지만 반대는 아니라 그대로 둬도 통과한다
- 시험 데이터: 지금 가짜 원소(`tests/test_ext_clinic.py:100-103`)는 `{aid}@example.com` · `<실명{aid}>` · `doc-a` 꼴의 지어낸 값이고, T67 이 「지어낸 값만」 을 못박았다. 실값 0
- 빈 곳: `null` 값 갈래(W3) · `id` 없는 원소 → 502(W4) · Swagger 문장(W2)

### 4. WORK-015

- WP 마다 SPEC 절(§6.17 · §8 · §9 T67)을 가리키고 계약을 다시 쓰지 않는다. 계약 고정점 표(`WORK:55-62`) 여섯 줄 모두 SPEC 과 같다
- BE1 대상 파일 전수(브리프의 grep + `ExtStaff` · `STAFF_DOC` · `/staff` 로 `procedure/back` 재확인):

| 고칠 자리(실물) | WORK 목록 |
|---|---|
| `app/schemas/ext.py:491-500` `ExtStaff` | 있음 |
| `app/service/ext.py:897-899` `staff()` 원소 조립 | 있음 |
| `app/api/ext.py:521`(첫 줄 칸 나열) · `:527`(옛 문장) | 있음 |
| `tests/test_ext_clinic.py:100-103` · `:121-125` | 있음 |
| `tests/test_ext_docs.py:138-140`(직원 설명 단언) | **없음 — W2** |
| `tests/fake_kos.py` | 조건부로 있음 — 실제 가짜 원소는 `test_ext_clinic.py` 의 `internal()` 이라 손댈 일 없다 |

- `app/api/ext.py:540` 의 `summary`(「직원 목록 — 역할 이름 · 태그 · 활성」)와 `app/schemas/ext.py:267` · `:494` 의 기존 칸 설명은 SPEC 이 고치라고 하지 않았고 틀린 문장도 아니다 — 그대로 둔다
- 검증 명령은 실행 가능하다(`uv` · pytest · ruff 선언 확인 · 실행은 하지 않았다). 실행 위치 표기만 W5
- WP-E2E-LOCAL · WP-DEPLOY 완료 기준은 「누가 · 무엇으로」 가 있다(코디 · 데모 KOS 실호출 1 · 운영 실호출 1 · 값 기록 안 함)

### 5. public

- 바뀐 줄(`git diff` 의 `+` 줄)과 WORK-015 전체에서 이메일 꼴 · uuid 꼴 문자열 0. 예시는 `…@example.com` · `<실명…>` 자리표시뿐이다
- `kosAccountId` 의 꼴(uuid)을 적지 않은 것은 맞다 — 꼴은 KOS 것이고 SPEC 은 「문자열」 만 약속한다

## 고객이 실물에서 만날 자리

- **Swagger 직원 목록 설명** — 옛 문장이 남으면 연동처가 「안 낸다」 는 문서와 세 칸이 든 응답을 함께 본다(W2). WP-DEPLOY 의 「`/api/docs` 설명이 새 문장인지」 눈 확인이 지금은 유일한 방어다
- **`email` · `realName` null** — KOS 에 값이 빈 직원은 null 로 나간다. 연동처가 이메일로 자기 계정과 이으려면 null 인 직원 수가 곧 못 잇는 수다. WP-E2E-LOCAL 이 null 수를 적는다(`WORK:70`) — 그 수를 사용자에게 전하는 것이 좋다
- **`kosAccountId` 와 `staffId`** — 다른 ext 응답(`counselor.staffId` 등)은 ccc 정수라 연동처가 둘을 섞을 수 있다. Swagger 문장(`SPEC:895`)이 이를 말한다
- **사본에 없는 새 계정** — `staffId` null 인데 `kosAccountId` · `email` 은 값이 있다(1시간 동기화 전). T67 이 고정한다

## 참고(기존 부채)

- `app/openapi_docs.py:108-109` 앱 설명의 「id」 줄은 §6.1 을 옮긴 문장인데 0.4.7 예외를 싣지 않는다. 「고객의 KOS id 는 내지 않는다」 만 말해 틀린 문장은 아니다 — 고치려면 SPEC §8 「앱 설명」 줄과 WORK 대상 파일에 `app/openapi_docs.py` 를 더해야 한다(이번 범위 밖으로 둬도 된다)
- `SPEC:119` §0 3차 줄의 근거 칸이 「D-01 ~ D-45 · D-48」 이다 — D-46 · D-47 이 빠진 것은 앞 판부터다
- `WORK:70` 「KOS 호출 수 1(로그)」 — 성공 경로에 KOS 호출을 세는 앱 로그가 있는지는 확인하지 않았다. 없으면 T67 의 호출 수 단언(`tests/test_ext_clinic.py:114`)으로 갈음하면 된다
- 원소 `id` 가 숫자 `0` · 빈 문자열이어도 502 다(`app/service/ext.py:884` 의 참 · 거짓 검사) — 지금 동작이고 이번에 바꾸지 않는다
