# WORK-001 fix 재검수 보고

- 검수자: `@kknaks-reviewer` (read-only) — 직전 판정 **FAIL**(`review-work-001-report.md`, 차단 3 · 경고 9)의 재검수
- 대상: `app/ontology-agent/` 만. `app/front/` 미추적 34파일은 FE 워커 몫이라 **범위 제외**(내용 미열람, 스코프 침범 여부만 확인 — 이 워커의 변경이 아니다)
- 테스트는 돌리지 않았다(브리프 지시). 코디 재검증치(실데이터 97 passed · `gold.py` bronze 참조 0)를 전제로 **구조·계약**만 본다.
- 참고: SPEC-001 이 그새 **v0.0.7** 로 올라갔다(직전 검수 시 v0.0.5). Case Matrix 에 신설 코드 5종이 등재됐고
  `is_partial_month`·`days_observed` 도 §4 에 들어갔다 — 직전 리포트 §4 의 요청 2건이 반영된 상태다.

## 판정: **PASS** — 차단 3건 전부 닫힘 · 경고 9건 전부 처리 · 새 위반 0건

남은 것은 문서 표기 stale 4건과 관찰 2건뿐이고, 전부 계약 위반이 아니다(§4).

---

## 1. 차단 3건 — 닫힘 확인

### F1. 골드의 브론즈 직독 제거 — **닫힘**

- `build/gold.py:262-268` — `build_promo` 가 브론즈 조회를 버리고 `promos`(= `silver_promotions`)만 읽는다.
  구성 사슬의 출발점은 `p2g.get(r["source_id"])` 로, 실버가 보존한 원천 내부 id 다.
- `db/schema.py:193-207` — `silver_promotions` 에 `source_id TEXT` 추가. 주석이 「식별자 보존이지
  값 변경이 아니다」를 명시해 이식 원칙과의 관계를 남겼다(`silver.py:317-319` 도 동일).
- `build/silver.py:326,333` — v1·v2 모두 `r["id"]` 를 그대로 적재. 필터 조건이
  원본(`build_gold.py:201` 의 `language=='ko' and not deleted_at`)과 동치다 —
  실버 v2 행은 이미 ko 슬라이스이고 `is_deleted` 가 `deleted_at` 의 bool 이다.
  `comp` 키도 `(promotion_code, promotion_started_at)` → `(code, benefit_start)` 로 **같은 값**을 가리킨다.
- **회귀 고정**: `tests/test_fix_gate_enforcement.py:27-34` 가 `gold.py` 소스에서 주석 아닌 `bronze_`
  라인 0건을 단정한다 — 사람 눈이 아니라 테스트가 지킨다. `:38-50` 이 `source_id` 73건 채움과
  `gold_promo_calendar` 57행·구성 특성 채움을, `:54-56` 이 `csv_parity diffs == 0` 으로
  **값이 안 바뀌었음**을 셀 단위로 고정한다. 등가 증명까지 붙은 점이 좋다.
- 독립 확인: `grep -n "bronze_" build/gold.py` → **0건**.

### F2. 게이트 실패 시 이전 DB 유지 — **닫힘**

- `db/connection.py:41-57` `atomic()` — SAVEPOINT/RELEASE 기반 **중첩 가능** 구간. 예외 시
  `ROLLBACK TO` + `RELEASE`. 가장 바깥 savepoint 의 RELEASE 가 곧 커밋이라 단독 실행과
  전체 실행이 같은 코드를 쓴다.
- `db/connection.py:35` `isolation_level=None` — 파이썬 암묵 트랜잭션을 꺼서 `atomic()` 이
  트랜잭션을 단독으로 쥔다. 이게 없으면 중간에 암묵 COMMIT 이 끼어 savepoint 가 풀린다.
- `build/__main__.py:106-121` `_all` — `_bronze … _gate3` 8단계를 `atomic(conn,"adopt")` 하나로 감쌌다.
  게이트 2·3 이 실패하면 실버·뷰·골드·온톨로지가 **통째로 되감긴다**.
- **bootstrap 커밋 버그 제거 확인**: `db/schema.py:270-277` `bootstrap()` 에 `conn.commit()` 이 없고,
  「호출자의 트랜잭션에 참여한다 / 여기서 커밋하면 바깥 savepoint 가 통째로 풀린다」를 독스트링에 남겼다.
  전 소스에 **`conn.commit()` 호출 0건**(`build/`·`db/` 기준, grep 확인) — 각 모듈이 전부 `atomic()` 로 갈렸다:
  `load_bronze.py:68` · `silver.py:373` · `masking.py:147` · `gold.py:378` · `ontology.py:57`.
- **회귀가 실제로 막는가 — 그렇다.** `test_fix_gate_enforcement.py:70-89` 의 `prior_db` 픽스처가
  정상 빌드 뒤 `gold_kpi_daily` 를 **100행으로 깎아 표지를 남긴다.** 롤백이면 100, 채택이면 235 라
  「유지됐는지 채택됐는지」가 값으로 갈린다 — 재빌드 결과가 같아 구분이 안 되는 함정을 정확히 피했다.
  그 위에 4방향을 다 고정한다: 게이트 2 실패(`:93-100`) · 게이트 3 실패(`:104-121`) ·
  실버 fail-fast(`:132-145`) · **전건 통과 시 채택**(`:125-128`). 마지막 것이 특히 중요하다 —
  롤백만 하고 채택을 못 하는 반대 방향 고장까지 막는다.
- 게이트 2 실패 주입이 `monkeypatch.setattr(gates, "REBUILD_TOTALS", …)` 로 모듈 전역을 갈아끼우는데,
  `gates.gate2` 가 호출 시점에 전역을 읽으므로(`gates.py:35,38,41,44,53`) 주입이 실제로 먹는다.

### F3. 정합률 게이트 예외 복원 — **닫힘**

- `build/silver.py:228-234` — `agreement < GU_AGREEMENT_THRESHOLD` 면 `AgreementBelowThreshold`
  (`AGREEMENT_BELOW_THRESHOLD`)를 던진다. 이식 원본 `reviews_finalize.py:117` 의 `sys.exit(2)` 동등물이고,
  주석이 그 대응 관계를 남겼다. 반환 dict 의 `gu_agreement_pass` 는 이제 도달 불가 상수 True 이며
  「미달이면 위에서 이미 중단됐다」로 표기됐다(`:245`).
- `build/__main__.py:54-57` — 출력이 무조건 「통과」로 바뀌었고 근거 주석이 붙었다. 출력만 하는
  게이트가 아니게 됐다.
- **회귀**: `test_fix_gate_enforcement.py:151-169` 의 `low_agreement_scoring` 이 `predicted_score` 만
  0.5 로 덮어 **정합률만** 무너뜨린다 — 근거 실존·폐쇄 목록 등 다른 검증은 통과시키므로 이 게이트를
  단독으로 겨눈다. 설계가 정확하다. `:173-179` 가 예외·코드를, `:183-204` 가 CLI exit 1 과
  **`gold_kpi_daily` 테이블이 아예 생기지 않음**을 단정한다(F2 와 맞물린 이중 확인).
  `:208-213` 이 정상 표본 427/511 = 83.6% 로 하한을 같이 못박았다.

---

## 2. 경고 9건 — 처리 타당성

| # | 처리 | 판정 |
|---|---|---|
| W1 | `gates.py:232-237` 실버 뷰 2종을 **스키마 검사**로 실제 대상에 넣고, 반환에 `value_scanned_views:2`·`schema_checked_views:2` 를 분리 표기(`:243-245`) | **타당**. 「원값 컬럼이 없어야 한다」는 실버 계약을 검사로 옮긴 것이라 수치를 2 로 낮추는 것보다 낫다. `test:220-222` 가 합계 일치를 고정 |
| **W2** | `gates.py:156-165` — 불일치 메시지를 `f"{table}[행 {i}].{c}"` **위치만**으로 바꾸고, 왜 그런지(`silver_reservations.staff` 가 직원 실명)를 주석에 남겼다 | **타당**. `test:225-244` 가 CSV·DB 양쪽 원값 문자열이 `render()` 에 없고 위치 문자열은 있음을 단정한다 — 값이 아니라 **부정 명제**로 고정한 점이 옳다. 같은 규율이 `silver.py:199-200`(마스킹 잔존은 pk 만)·`gates.py:229-230`(실명 토큰은 건수만)에도 일관되게 적용됐다 |
| W3 | `gold.py:319-322` — `END` 를 `max(resv_date)` 로 유도. 「값은 같고 규칙 재해석이 아니다」를 명시 | **타당**. `test:288-301` 이 창을 줄이면 판정이 따라 움직임을 확인해 **상수였다면 고정됐을 것**을 구분한다. 이식 등가는 `csv_parity` 가 지킨다 |
| W4 | `errors.py:64-95` — `REVIEW_SCORE_VIOLATION`·`MASKING_RESIDUE`·`AGREEMENT_BELOW_THRESHOLD`·`UNKNOWN_BRANCH`·`SILVER_ROWCOUNT_MISMATCH` 신설. `silver.py:165-166,218-223` 이 원인별로 갈라 담는다 | **타당**. 게다가 SPEC-001 v0.0.7 Case Matrix 에 5종이 **등재까지 됐다** — 「`ENUM_VIOLATION` 은 `visit_status` 전용」이 spec 문장으로 굳었다 |
| W5 | `silver.py:293-295` — `r.get("language", "ko")` 로 원본과 동일 의미 복원. `or "ko"` 가 왜 갈리는지 주석 | **타당** |
| **W6** | `silver.py:290,301-307` — 항상 참인 식을 버리고 **실제 append 수**(`len(out) - before`)와 실측 제외 수로 대사. `:311-314` 에 「적재본 = 산출 행수」 대사를 추가하고, `:360-367` 이 하나라도 어긋나면 `SILVER_ROWCOUNT_MISMATCH` 로 **중단**한다 | **타당하고 요구 이상**. 지적은 「죽은 식을 살려라」였는데 (a) 실대사로 바꾸고 (b) append 누락까지 잡는 적재 대사를 더하고 (c) 대사 실패를 예외로 승격했다. `build()` 도 예약 대사 불일치를 예외로 올린다(`:374-380`) — 「대사했다」가 아니라 「맞았다」가 됐다 |
| W7 | `masking.py:62-75` — `WHEN length(col)=1 THEN '○'` 분기 추가 | **타당**. `test:247-255` 가 `["○","김○",""]` 로 고정 |
| W8 | `silver.py:110-116` — `UnknownBranch` 로 코드를 남기고 중단 | **타당**. `test:259-273` 가 확인 |
| W9 | `config.py:17-61` — `SourcePaths` 프로즌 데이터클래스 + `sources_for()` 하나로 통합. `load_bronze.py:64,117` · `silver.py:150` · `ontology.py:53` 이 전부 이걸 지난다 | **타당**. 경로 재조립이 소스에서 사라졌다. `test:276-284` 가 `data_dir` 오버라이드 일관성을 고정 |

---

## 3. 새 위반 여부

- **계층 경계** — `gold.py` bronze 참조 0. `silver` 는 브론즈만, `gold` 는 실버만 읽는다.
  `gates.py:186-201` 의 브론즈 조회는 **게이트 3(AC-7) 의 원값 대조**라 계층 빌드가 아니다 —
  뷰 산출을 원값 집합과 맞대는 검사 자체가 원 테이블 접근을 요구한다. 위반 아님.
- **PII** — 새 코드에 원값 로그 경로가 생기지 않았고 오히려 두 곳이 닫혔다(W2, `silver.py:199`).
  신규 테스트 픽스처도 전부 합성값(`'합성표본'`·`'비밀표기'`·`'다른표기'`)이다.
  `low_agreement_scoring`(`test:151-169`)은 채점 산출물(리뷰 pk·점수·마스킹 본문 발췌)만
  `tmp_path` 에 파생 복제하고 원천을 건드리지 않는다 — 원천은 심볼릭 링크로만 참조한다(`:190-194`).
- **이식 원칙** — 변환 규칙은 그대로다. 바뀐 것은 (a) 식별자 보존(`source_id`), (b) 상수 → 데이터 유도
  (`END`), (c) 게이트 **복원**(정합률), (d) 에러 코드 세분화. 셋 다 값을 바꾸지 않고,
  `csv_parity` 10테이블 셀 대조 0 diff 가 그것을 증명한다(`test:54-56`).
- **allowed_paths** — 변경은 전부 `app/ontology-agent/` 안. `app/front/` 34파일은 FE 워커 산출물로
  이 검수 범위 밖이며, 이 워커가 그쪽을 건드린 흔적은 없다.
- **하드코딩** — 절대경로 0. 남은 상수는 `NAVER_START="2026-03-21"`(gold.py:19)뿐이고 spec §4 가
  관측 개시일로 명시한 값이다. `2026-08-30` 은 W3 으로 사라졌다.

---

## 4. 잔여 nit (비차단) · 관찰

**nit — 전부 문서 표기 stale, 동작 영향 0**

1. `build/errors.py:60-62` — 「Case Matrix 미등재 (코디에게 등재 요청)」. SPEC-001 v0.0.7 에서
   **5종 전부 등재됐다.** 주석을 「v0.0.7 등재」로 갱신할 것.
2. `build/errors.py:61` — 「아래 3종」이라 적었는데 실제 신설은 5종이다.
3. `build/spec_contract.py:11,40,80` — SPEC-001 을 v0.0.6 으로 참조. 실제 v0.0.7.
4. `README.md:32-35` — 게이트 실패 코드를 8종만 나열한다. 신설 5종을 추가할 것.
5. `config.py:83-86` `Settings.sources` 프로퍼티가 어디서도 안 쓰인다(전부 `sources_for()` 경유).
   지우거나 `sources_for()` 를 그쪽에 위임시켜 진입점을 하나로 두는 편이 W9 의 취지에 맞다.
6. `build/masking.py:139` 만 `atomic` 을 함수 안에서 import 한다(다른 모듈은 상단). 순환 참조가
   없으므로 상단으로 올려도 된다 — 일관성 문제.

**관찰 — 판단 근거로 남긴다, 조치는 코디 판단**

- **단계 단독 실행은 게이트 밖에서 커밋된다.** `build gold --db X` 는 `atomic(conn,"gold")` 로
  자기 산출물만 커밋하고 게이트 2·3 을 돌지 않는다. 단계별 실행은 WORK-005 가 요구하는 인터페이스라
  설계상 맞고 운영 채택 경로는 `all` 이다(README 도 그렇게 안내한다). 다만 단계 단독 실행 시
  「게이트 미실행 — 채택 아님」한 줄을 찍어 두면 오해가 원천 봉쇄된다. 한 줄짜리 제안이다.
- **빌드가 실패해도 DB 파일과 빈 스키마는 남는다.** `_all` 이 `_bootstrap` 을 atomic 밖에서 돌리기
  때문이다(`__main__.py:116`). 산출물은 하나도 채택되지 않으므로 F2 위반이 아니고, `test:199-204` 가
  `gold_kpi_daily` 미생성으로 그것을 확인한다. 다만 소비자의 `connect_ro()` 는 파일 존재만 보므로
  (`db/connection.py:63`) 「한 번도 안 만든 DB」와 「빌드가 실패한 DB」를 구분하지 못한다.
  WORK-002 가 빈 골드를 「데이터 없음」으로 오독할 여지가 있다 — 빌드 성공 표지(예: `build_meta` 1행)를
  두는 안을 WORK-002 착수 시점에 검토할 것을 권한다.
- AC-8 관련: `db/connection.py:6-9` 에 「`connect_ro()` 는 쓰기만 막는다 · 도구 계층이 화이트리스트를
  따로 세워야 한다」는 경고가 모듈 독스트링으로 박혔다. 직전 리포트 §4(1) 의 권고가 코드에 남아
  WORK-002 브리프로 이어질 준비가 됐다. **이 자리에서 더 요구할 것은 없다.**

---

## 5. 결론

차단 3건은 「고쳤다」가 아니라 **「다시 풀리면 테스트가 잡는다」** 수준까지 닫혔다. 특히 F2 는
표지를 남긴 `prior_db` 로 롤백과 채택을 양방향 고정했고, F3 는 정합률만 겨냥한 오염 표본을 만들어
다른 검증에 가려지지 않게 했다. 경고 9건은 전건 처리됐고 W6 는 지적 범위를 넘어 대사 자체를
예외로 승격시켰다. 새 위반은 없다. **PASS.** §4 의 nit 6건은 다음 커밋에 얹으면 되고 재검수는 필요 없다.
