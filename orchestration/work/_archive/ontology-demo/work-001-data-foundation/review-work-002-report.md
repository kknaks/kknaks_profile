# WORK-002 도구·API 검수 보고

- 검수자: `@kknaks-reviewer` (read-only)
- 대상: `app/ontology-agent/` 미커밋 변경분 — 신규 17파일(`service/` 8 · `api/` 4 · `tools/` 1 · `tests/` 3 + `__init__`) + 기존 13파일 수정. `app/front/` 는 커밋됨·범위 제외.
- 기준: `roles/ontology-demo/backend/rules.md` · SPEC-002 v0.0.4 · SPEC-003 v0.0.8 · SPEC-001
- 코디 재검증치(실데이터 222 passed)를 전제로 **계약·규칙 준수와 게이트 실효성**만 본다. 테스트는 돌리지 않았다.

## 판정: **FAIL** — 차단 1건 · 경고 8건 · nit 5건

차단은 한 줄짜리 계약 위반이지만 **화면 렌더 결과를 바꾸고 테스트가 덮지 못한다.**
S-001·S-002·PII·ADR-04 는 전항 통과이고, 구조 결정(§4)과 AC-8 게이트 설계(§3)는 대체로 타당하다.

---

## 1. 차단 (FAIL)

### F1. `source_group` 을 실버 테이블에도 실어 보낸다 — SPEC-003 명문 위반

- **위치**: `service/allowlist.py:90,98,105,109,113,117` (실버 6종 전부에 `source_group=` 지정)
  → `service/lineage.py:46` 이 `spec.source_group or None` 으로 그대로 방출.
- **근거**: SPEC-003 v0.0.8 §4 계층 조회 —
  *"**`source_group`** — 브론즈 테이블의 **원천 축**이다. 허용값 `"vegas"` · `"review"` · `"nexus"`,
  **실버·골드는 `null`**."*
- **결과**: `/api/layers/silver/tables` 가 `reservations→vegas` · `reviews→review` ·
  `catalog·promotions·mappings·branch_alias→nexus` 를 실어 보낸다. FE 는 이 값으로 칩을 묶으므로
  (`app/front/components/ontology/data/data-view.tsx:76` — `table.source_group ?? table.table`)
  **실버 칩이 6개가 아니라 3개**로 접히고 nexus 아래 2단이 열린다. SPEC-004 U-13 은 2단 구조를
  **브론즈에만** 규정했고, 계층 탭 카운트는 6인데 칩은 3이라 화면이 자기 숫자와 어긋난다(AC-17).
- **탐지 실패**: `tests/test_w002_api.py:138-143` 이 **브론즈 3종만** 검사하고 실버·골드가 `null` 인지는
  보지 않는다. 그래서 222 passed 안에서 조용히 지나갔다.
- **닫는 법**: 실버 6행의 `source_group=` 인자를 제거한다(골드는 이미 미지정이라 `None`).
  회귀 테스트는 `assert all(t["source_group"] is None for t in silver_tables)` 한 줄이면 된다.

---

## 2. 경고 (WARN)

### W1. AC-3 이 문언대로는 성립하지 않는다 — 그런데 코드 주석은 성립한다고 단언한다

- **위치**: `service/allowlist.py:227-234`(`fields_of` 가 뷰의 PRAGMA 컬럼을 그대로 허용 목록으로 쓴다)
  · `service/queries.py:278-281` · `service/errors.py:UnknownField` 독스트링
- 마스킹 뷰는 컬럼명을 **그대로 유지**한다 — `build/masking.py:115` 가
  `mask_name_sql(...) AS "patientName"` 으로 별칭을 원본과 같게 준다. 따라서 `patientName`·`phone`·
  `birthday` 는 **허용 필드 목록 안에 있고** `filters`·`order_by` 에 넣으면 통과한다.
  SPEC-002 AC-3(*"어디에 넣어도 `UNKNOWN_FIELD` 로 거부된다"*)과 §4(*"PII 원 컬럼명은 목록에 없다"*)를
  문언 그대로는 못 지킨다.
- **실질 누출은 없다.** 값이 마스킹본이라 원값 조회는 0건이고(`tests/test_w002_tools.py:61-68` 이
  `total == 0` 으로 실증), `contains` 는 이 세 필드에서 차단된다(`queries.py:304-305`).
  워커도 이 편차를 테스트 독스트링에 **명시**했다 — 숨기지 않은 점은 옳다.
- **문제는 주석이다.** `queries.py:279` 「PII 원 컬럼명은 뷰에 없으므로 여기서 막힌다(AC-3)」와
  `errors.py` 「PII 원 컬럼 우회 시도가 여기서 막힌다(AC-3)」는 **사실이 아니다.** 다음 사람이 이
  주석을 믿고 뷰 정의를 바꾸면(별칭을 `patient_masked` 로 준다든지) 아무도 검증하지 않는다.
- **코디 판단 필요**: (a) `fields_of` 에서 `spec.masked_fields` 를 빼 AC-3 을 문언대로 맞추거나,
  (b) SPEC-002 AC-3 을 「마스킹 필드는 필터 가능하되 값이 마스킹본이라 원값 우회가 성립하지 않는다」로
  개정한다. 어느 쪽이든 **주석은 지금 고쳐야 한다.**

### W2. AC-8 정적 게이트에 우회 두 갈래가 남아 있다

게이트 설계 자체는 좋다 — 파일 whitelist 가 **없고**(`tests/test_w002_ac8_view_only.py:44-48` 이
`tools`·`api`·`service` 전 `.py` 를 parametrize), 대상이 비면 그 자체가 구멍임을 알고 하한을 박았다
(`:51-54`). 주석 줄만 건너뛰므로 실행 코드는 못 숨긴다. 워커가 주장한 두 번의 조인(lookahead 되감기 ·
`\b`)도 **실제로 유효하다** — `\b` 가 없으면 `silver_reservations.sales` 에서 엔진이 `silver_reservation`
으로 되감아 `(?!\.)` 를 통과시키는 것을 확인했다. 남은 구멍은 둘이다(`:30` 정규식 실측).

| 입력 | 결과 |
|---|---|
| `FROM bronze_vegas_reservations` | CAUGHT ✓ |
| `FROM BRONZE_VEGAS_RESERVATIONS` | **MISSED** — SQLite 식별자는 대소문자를 안 가리므로 런타임에는 동작한다 |
| `f"bronze_{t}"` | **MISSED** — `bronze_` 뒤가 `{` 라 `[a-z_]+` 가 못 붙는다 |
| `f"SELECT * FROM {prefix}_vegas_reservations"` | **MISSED** |
| `silver_reservations.sales` | MISSED(의도된 제외 — 컬럼 출처 표기) ✓ |

`f"bronze_{t}"` 는 **이미 코드에 있다**(`service/allowlist.py:85`). 오늘은 `_BRONZE_NEXUS`(PII 없음)만
넣으니 안전하지만, 게이트는 그 줄을 보지 못한다. `re.IGNORECASE` 추가와
「f-string 안에서 `bronze_`·`silver_` 접두어 뒤에 치환식이 오면 FAIL」 규칙 한 줄이면 둘 다 닫힌다.

또 하나: PII 원 컬럼 검사(`:81-100`)는 **SQL 처럼 보이는 리터럴 문자열**만 본다. `queries.py` 는 컬럼을
변수로 조립하므로(`col = f'"{_ident(field)}"'`) 이 검사로는 W1 의 경로를 원리적으로 잡을 수 없다 —
정적 게이트의 한계이지 결함은 아니지만, **AC-3 을 이 게이트가 지킨다고 읽으면 안 된다.**

### W3. `/api/meta/build` 가 세션 게이트 밖이다

- **위치**: `main.py:37-50`. 라우터가 아니라 앱 직접 등록이라 `Depends(require_session)` 이 없다.
- `main.py:6` 독스트링은 *"`/health` 와 `/api/auth/session` 만 예외"* 라고 적었는데 **세 번째 예외**가
  생겼고, SPEC-003 §4 엔드포인트 표에도 없는 신설 표면이다. AC-1(*"세션 없이 부른 모든 API 가 401"*)과
  어긋난다.
- 노출값은 `built_at`·`gates_passed`·`daily_rows`·`node_count`·`edge_count` 다. PII 는 아니지만
  **데이터셋 규모가 미인증으로 나간다.** `Depends(require_session)` 을 걸거나(FE 는 게이트 통과 후에만
  부른다) SPEC-003 에 비인증 경로로 등재해야 한다.

### W4. 서명 쿠키 — 비밀번호 미주입 시 **공개 상수 키**로 위조된다

- **위치**: `api/deps.py:22-27`(`_signing_key`) · `:38-48`(`verify_session`) ·
  `api/auth_router.py:31-35`(발급 경로는 503 으로 막음)
- 발급 경로는 `password_configured()` 로 막아 뒀다 — 「기본값이 없다」가 「아무나 들어온다」가 되지 않게
  한 판단은 정확하다. **그런데 검증 경로는 그 확인을 하지 않는다.**
  `demo_password` 가 빈 문자열이면 서명 키는 `sha256(b"ontology-demo-session|")` 라는
  **레포에 적힌 상수**가 되고, 누구나 `<미래 epoch>.<HMAC>` 를 오프라인에서 만들어 전 조회 API 를 연다.
- env 미주입은 데모 배포에서 가장 흔한 사고다. **`verify_session` 첫 줄에
  `if not password_configured(): return False`** 한 줄이면 닫힌다.
- 설계 자체(무상태·비번 파생 키·비번 변경 시 기존 세션 자동 무효)는 work-002 범위 제약
  (테이블 신설 없음) 안에서 합리적이다. 만료가 서명에 포함돼 변조도 막힌다. 개별 폐기 수단이 없는 것은
  DEC-005(공용 비밀번호 하나) 전제상 수용 가능하다.

### W5. `build_meta` 표식이 **단계 단독 실행에 무효화되지 않는다**

- **위치**: `build/__main__.py:126-144`. `build_meta` 를 건드리는 코드가 `_stamp_build` 뿐이고 그것은
  `_all` 에서만 불린다(`:122`). `HANDLERS` 의 `gold`·`silver`·`ontology` 단독 실행은 데이터를 바꾸고
  **표식은 그대로 둔다.**
- 결과: `uv run python -m build gold` 로 게이트 없이 골드를 다시 쓴 뒤에도
  `connect_ro(require_build=True)` 가 정상 서빙하고 `/api/meta/build` 는 「게이트 1,2,3 통과」라고
  보고한다. **표식이 거짓을 말하는 유일한 경로**다.
- 채택 트랜잭션 안에서 찍는 설계(`:127-131`)는 옳고 WORK-001 재검수 관찰을 정확히 닫았다 —
  남은 것은 반대 방향이다. 단계 단독 실행 시작 시 `DELETE FROM build_meta` 한 줄이면 된다.

### W6. `get_definition` 이 ENUMS 13종 중 2종에만 닿는다

- **위치**: `service/glossary.py:219-237`(ENUMS 13종) · `:289`
  (`enum_values = ENUMS.get(t.aliases[0] if t.aliases else t.term)`)
- enum 은 **Term 의 첫 별칭이 ENUMS 키와 같을 때만** 실린다. 실제로 닿는 것은
  `sentiment`(Term 「리뷰 감성」)와 `procedure_concept`(Term 「시술 개념」) 둘뿐이다.
  `visit_status` · `verdict` · `node_type` · `edge_kind` · `confidence` · `kpi_status` ·
  `node_state` · `signal_type` · `line_type` · `promo_version` · `outstanding_direction` 은
  Term 도 별칭도 없어 `UNKNOWN_TERM` 이 된다.
- SPEC-002 §4 *"폐쇄 목록(시술 개념 13종)·enum 도 이 도구로 조회한다"* · OQ-5 확정
  *"글로서리 판정 표 + KPI 컬럼 + enum"* 을 절반만 충족한다. `lookup` 에서 ENUMS 키를 직접 받는
  분기를 하나 두면 닫힌다.

### W7. `note` 와 `reason` 이 같은 컬럼에서 나와 기각·보류 엣지에서 문장이 중복된다

- **위치**: `service/queries.py:350-352` — `reason` 은 기각·보류일 때만 `rationale`,
  `note` 는 **판정과 무관하게 항상** `rationale`.
- SPEC-003 §4 는 *"`note` — 사람이 읽는 설명 … `evidence`·`reason` 과 **별개 필드**"* 라고 못 박았다.
  `ontology_edges` 에 텍스트 컬럼이 `rationale` 하나뿐이라 물리적 제약이 있는 것은 사실이고,
  판정에 따라 `reason` 을 가리는 처리(채택 엣지에 배제 사유가 있는 것처럼 읽히지 않게)는 옳다.
- 그러나 **기각·보류 엣지는 `note == reason`** 이 되고, FE 인스펙터가 두 필드를 각각 렌더하므로
  (`app/front/components/ontology/monitoring/edge-inspector.tsx:107-114`) **같은 문장이 두 번 찍힌다.**
  FE mock 은 배타적으로 채워(`note: negative ? null : ...`) 이 증상이 없었다 — 실 API 전환 시 처음
  드러난다. `note` 도 기각·보류에서는 `None` 으로 두는 편이 mock 과 화면 양쪽에 맞는다.

### W8. MCP 도구 서버가 인증 없이 서고 기본값이 전면 개방이다

- **위치**: `tools/server.py:47-55,207-213`(라우트는 `/health` 와 `Mount("/")` 뿐, 의존성 없음) ·
  `config.py:88-92`(`mcp_host="0.0.0.0"` · `mcp_allowed_hosts=["*"]` · `mcp_allowed_origins=["*"]`)
- `enable_dns_rebinding_protection=True` 를 켰지만 `allowed_hosts=["*"]` 가 그것을 무력화한다.
  포트 28081 이 노출되면 **비밀번호 없이** `query_layer` 로 마스킹 브론즈 행을 읽을 수 있다.
- SPEC-002 는 도구 서버의 인증을 Out of scope 로 두고 SPEC-003·배포에 넘겼으므로 **계약 위반은
  아니다.** 다만 §4 에서 보듯 이 구조 선택의 대가가 여기로 모이므로 배포 브리프에 명시할 것을 권한다.

---

## 3. AC-8 정적 게이트의 실효성 — 종합 평가

**「파일 whitelist 로 덮은 곳」은 없다.** 대상은 `tools`·`api`·`service` 전 `.py` 이고 예외 목록도,
skip 마커도 없다. 값 whitelist(`PII_FREE_SILVER` 4종 · `bronze_nexus_` 접두)는 SPEC-002 §4 허용 테이블
표와 정확히 일치하고 — PII 없는 테이블이라는 근거가 spec 에 있다 — 임의 완화가 아니다.
빈 대상 방어(`:51-54`)와 도구 4종 고정(`:142-155`), 자유 SQL 파라미터 부재 검사(`:117-134`),
비밀번호 하드코딩 검사(`:158-169`)까지 갖춘 것은 요구 이상이다.

한계는 셋이고 두 개는 닫을 수 있다: 대소문자(W2) · f-string 합성(W2) · **동적 컬럼 조립은 원리적으로
불가**(W1). 세 번째 때문에 「AC-8 게이트가 있으니 AC-3 도 지켜진다」로 읽으면 안 된다 —
둘은 다른 축이다. 검사 범위가 `db/`·`build/`·`main.py` 를 포함하지 않는 것은 조회 코드가 그쪽에 없어
현재는 정당하나, `main.py:37-50` 이 이미 DB 를 직접 여는 라우트를 갖게 됐다(W3). **`main.py` 를
SURFACE 에 넣는 편이 안전하다.**

---

## 4. 구조 결정 평가 — 공용 `service/` 계층 vs 연구 권고 B(MCP→내부 API 래퍼)

**타당하다. B 안보다 낫다고 본다.**

- **AC-5 주장은 성립한다.** `/api/kpi/series`(`api/monitoring_router.py:52-56`)와 도구
  `query_kpi`(`tools/server.py:94-97`)가 **같은 `service.queries.query_kpi` 를 무변환으로** 부른다.
  라우터에 후처리가 한 줄도 없고 기본값도 spec 대로 갈렸다(도구 `limit` 20 / API 50 — SPEC-002 §4 ·
  SPEC-003 §4). 구현이 하나뿐이라 「오차 0」이 대조가 아니라 **동일성**으로 성립한다 —
  주장이 과장이 아니다.
- **B 안이었다면** 도구 호출마다 HTTP 홉과 세션 쿠키 취득이 붙고, API 프로세스가 죽으면 도구도 죽으며,
  같은 값을 두 번 직렬화한다. AC-5 는 마찬가지로 성립하지만 실패 지점이 늘 뿐이다.
  **DEC-002 「뷰 경유 강제」도 B 안이 더 잘 지키는 게 아니다** — 어느 쪽이든 최종 SQL 은 한 곳
  (`queries.py`)이고, 실제 강제는 allowlist + 정적 게이트가 한다.
- **대가는 하나**: B 안이었다면 도구가 API 의 세션 게이트를 자동으로 물려받았을 텐데, 지금은 도구
  서버가 자기 인증을 갖지 않는다(W8). 이 대가는 **배포 경계**로 옮겨졌을 뿐 사라지지 않았으므로
  배포 시 포트 비공개·`mcp_allowed_hosts` 지정이 전제다.

---

## 5. 통과 확인 (근거 있음)

- **S-001 (관계는 데이터에)** — 통과. `service/` 어디에도 「A 가 B 의 원인」 지식이 값으로 없다.
  가장 가까운 것이 `monitoring.py:238-256` `FORECAST_RULES` 의 `cause`/`effect` 쌍인데,
  (a) SPEC-003 §4 가 *"예보는 확정 엣지 2건만 **코드화한다**(BASE-001 구현 순서 5)"* 로 명시했고,
  (b) 쌍은 `ontology_edges` **조회 키**로만 쓰이며 없으면 문장을 만들지 않고 건너뛴다(`:267-268`),
  (c) 부호·lag·신뢰도·근거는 전부 엣지 행에서 읽는다(`:269,277-282`). **지식이 아니라 선택이다.**
  글로서리(`glossary.py`)의 「총 내원 = 신환 + 재진」류는 정의(항등식)이지 인과가 아니다.
- **S-002 (파라미터화 조회만)** — 통과. `sql`·`query`·`path` 류 파라미터가 **표면에 없고**
  (AST 검사가 고정), 모든 값은 바인딩 파라미터이며 SQL 에 문자열로 박히는 것은 allowlist 를 통과한
  관계명·컬럼명뿐이고 그것도 `_IDENT` 정규식을 한 번 더 지난다(`queries.py:30-36`).
  상한 초과는 절단이 아니라 거부(`:45-53`, `LIMIT_EXCEEDED`), `total` 항상 동봉(`:257`).
  집계는 전부 골드 View 조회이고 도구가 합산하지 않는다 — grain 마다 View 하나(`allowlist.py:154-159`).
  상태 경계도 상수가 아니라 `_status` 컬럼에서 역산한다(`queries.py:199-210`).
- **PII** — 통과. 응답 행은 뷰 산출이라 마스킹본이고, `masked_fields` 가 항상 동봉된다(`:260`).
  로그는 `tools/server.py:64` 의 `logger.info("도구 거부: %s", exc.code)` **한 줄뿐**이고 코드만 남긴다
  — `service/`·`api/` 에 `print`·로깅 0건. 마스킹 표기 상수는 SPEC-001 §4 값 그대로다
  (`allowlist.py:52-56`).
- **ADR-04** — 통과. `anthropic`·`openai` 등 LLM SDK import **0건**(정규식 확인). 이 WP 에 LLM 경로가
  없다는 것도 확인했다 — 채팅·에이전트 루프는 이 변경분에 없다.
- **SPEC-002 도구 계약** — 4종 정확(`tools/server.py:45,68,102,136,168`), 거부 응답에 허용 목록 동봉
  (`errors.py:24-28`), 기본 `verdicts` 가 채택·자동 확정·선언(`allowlist.py:206`, AC-6),
  기각·보류에 `reason` + `usable_for_causal_claim: false`(`queries.py:350-354`, AC-5),
  `EMPTY_RESULT` 를 예외로 만들지 않은 판단(`errors.py:75-77`)까지 정확하다.
  `edge_id` 는 `<from>__<to>` 로 응답이 실어 준다(`queries.py:325-327`) — 소비자가 조립하지 않는다.
  `lag` 는 원형 유지 + `lag_days` 병기(`:343-344`), `sign` 은 무치환 통과(`:342`)라 U+2212 가 보존된다.
- **SPEC-003 API 계약** — 401 `NO_SESSION`(`deps.py:57-63`) · 401 `INVALID_PASSWORD`
  (`auth_router.py:36-37`) · 쿠키 `ontology_demo_sid`/httpOnly/SameSite=Lax/Secure/30일
  (`auth_router.py:39-47`, `config.py:83-85`) · **`has_prev_period`**(`monitoring.py:76`, WORK-004 검수
  때 이월됐던 항목이 닫혔다) · `columns_note` 대상이 nexus 14 + `gold_promo_calendar` 로 정확
  (`allowlist.py:87,129`) · `SOURCE_UNAVAILABLE` 503(`service/db.py`, `errors.py:70-72`) 전부 준수.
- **스코프** — 변경은 전부 `app/ontology-agent/` 안. 기존 파일 수정 13건은 전부 가산적이고
  (`db/__init__.py` export 추가, `conftest.py` 픽스처 추가, `test_p1` 은 `require_build=False` 로
  의도를 명시하며 표식 테스트를 더했다) 기존 계약을 되돌린 곳이 없다.

---

## 6. nit (비차단)

1. `service/monitoring.py:93-97` — `if grain == "daily"` 와 `else` 분기가 **바이트 동일**하다. 죽은 분기.
2. `service/monitoring.py:285` — `horizon` 이 `edge["lag"]`(= `"2w"`)인데 SPEC-003 §4 예시는 `"14d"` 다.
   FE 가 `horizon` 을 렌더하지 않아 영향은 없다.
3. `service/monitoring.py:355` — `message` 가 `lag=="0d"` 를 「동시점」으로 재서술한다. SPEC-002 §4 가
   *"「동시점」·「2주」 같은 재서술을 만들지 않는다"* 고 적은 것은 `lag` **필드** 얘기라 위반은 아니나,
   SPEC-003 의 예시 문장에는 이 표현이 없다.
4. `tools/server.py:169` — SPEC-002 Validation 의 `term` 1~100자 검증이 없다.
5. `service/queries.py:147` `_COLUMN_CACHE` 가 커넥션과 무관한 전역이라 서로 다른 DB 를 오가면
   오염될 수 있다. `reset_column_cache()` 가 있어 테스트는 넘기지만, 키에 DB 경로를 넣는 편이 안전하다.
6. `sign` 이 U+2212 임을 고정하는 테스트가 없다. spec 이 *"눈으로는 같아 보여서 어긋나도 드러나지
   않는다"* 고 경고한 자리라 한 줄 넣어 둘 값이 있다.

---

## 7. 재검수 조건

**F1(실버 `source_group`)만 고치면 PASS 로 뒤집는다** — 인자 6개 제거 + 「실버·골드는 null」 회귀
테스트 1건. W1 의 **주석 정정**과 W4 의 `verify_session` 한 줄은 값이 싸고 위험이 커서 같이 처리할 것을
권한다. W2·W3·W5·W6·W7 은 코디가 우선순위를 정하면 되고, W8 은 코드가 아니라 배포 브리프에 적을 항목이다.
