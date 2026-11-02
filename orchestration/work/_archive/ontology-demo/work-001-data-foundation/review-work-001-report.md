# WORK-001 코드 검수 보고 — 데이터 기반 (P1~P5)

- 검수자: `@kknaks-reviewer` (read-only)
- 대상: 워크트리 `work-001-data-foundation` / `app/ontology-agent/` — 수정 4파일 + 신규 19파일
- 기준: `roles/ontology-demo/backend/rules.md` · SPEC-001(파일 실제 버전 **v0.0.5**, 브리프는 v0.0.4로 표기) ·
  이식 원본 `reference/ontology_demo/scripts/`(코디 워크트리에서 read-only 대조)
- 테스트는 돌리지 않았다(브리프 지시). 코디가 확인한 실데이터 81 passed 를 전제로 **구조·계약 위반만** 본다.

## 판정: **FAIL** — 차단 3건 · 경고 9건

세 건 모두 SPEC-001 이 명문으로 적어 둔 줄을 어긴 것이고, 셋 다 국소 수정으로 닫힌다.
그 외의 이식 정확도·PII 경계·스코프 준수는 **전항 통과**다. 아래 F1~F3 만 닫히면 PASS 로 뒤집힌다.

---

## 1. 차단 위반 (FAIL)

### F1. 골드가 브론즈를 직접 읽는다 — 계층 경계 위반

- **위치**: `app/ontology-agent/build/gold.py:262-265`

  ```python
  v2rows = [dict(r) for r in conn.execute(
      "SELECT id, promotion_code, promotion_started_at FROM bronze_nexus_promotion_v2s "
      "WHERE language = 'ko' AND (deleted_at IS NULL OR deleted_at = '')")]
  ```

- **근거 규칙**: SPEC-001 §4 「계층 경계 — 읽기 방향」 — *"상위 계층은 **바로 아래 계층만** 읽는다.
  **골드가 브론즈를 직접 읽지 않는다.**"* / DEC-001.
- **왜 차단인가**: 이 문장은 spec 이 그림(§4 다이어그램)과 산문 두 곳에 못 박아 둔 계약이다.
  주석(`gold.py:260-261`)이 "읽기 전용 참조"라고 자인하지만, 계약은 「쓰지 않는다」가 아니라
  「읽지 않는다」다. 원본 `build_gold.py:196-201` 도 같은 우회를 하고 있으므로 **이식 정확도로는
  무결**하지만, spec 이 그 우회를 계약에서 금지한 쪽으로 앞서 있다.
- **뿌리**: `db/schema.py:193-203` `silver_promotions` 가 v2 내부 id 를 보존하지 않는다.
- **닫는 법**: `silver_promotions` 에 원천 내부 id 컬럼 1개(`source_id`)를 보존하고 `build_promo` 가
  실버만 읽게 한다. **식별자 보존은 변환 규칙 재해석이 아니므로 이식 원칙과 충돌하지 않는다.**
  기존 CSV 에는 없는 컬럼이지만 `gates.csv_parity` 는 `cols = ref ∩ db`(`gates.py:152`)라
  대조가 깨지지 않는다 — 지금 구조에서 안전하게 고칠 수 있다.

### F2. 게이트 2·3 이 실패해도 이전 DB 상태가 남지 않는다

- **위치**: `build/silver.py:317` · `build/gold.py:383` · `build/ontology.py:75` (각 단계가 자기 커밋을
  끝낸다) + `build/__main__.py:114-115` (`all` 순서가 `... gold, ontology, gate1, gate2, gate3`)
- **근거 규칙**: SPEC-001 §4 Case Matrix `REBUILD_MISMATCH` → *"산출물 미채택, **이전 DB 유지**"* ·
  State/Lifecycle *"FAILED → 이전 DB 상태 유지"* · §5 *"게이트는 전부 통과해야 산출물을 채택한다."*
  S-2.5 *"어긋나면 산출물을 채택하지 않는다 — 이전 DB 상태를 유지하고 실패를 기록한다."*
- **실제 동작**: `uv run python -m build all` 에서 실버·골드·온톨로지가 각각 커밋된 **뒤에** 게이트 2·3 이
  돈다. 게이트가 실패하면 exit 1 은 나지만 DB 파일에는 이미 대조 불일치 산출물이 들어앉아 있고,
  `db.connect_ro()` 로 붙는 소비자에게 그대로 보인다. 게이트가 **탐지는 하되 채택을 막지 못한다** —
  브리프 기준 4「게이트가 실제로 막는 구조인가」에 정확히 걸린다.
- **대비**: 게이트 1 은 올바르다 — `load_bronze.load()` 가 적재와 대사를 한 트랜잭션에 넣고
  불일치 시 `ROLLBACK` 한다(`load_bronze.py:71-115`). 게이트 2·3 만 이 규율이 빠졌다.
- **닫는 법**(둘 중 하나):
  1. 단일 커넥션에서 `BEGIN` → 실버·골드·온톨로지·뷰 → 게이트 2·3 → 통과 시에만 `COMMIT`.
     SQLite 는 DDL 도 트랜잭션 안이라 `write_table` 의 DROP/CREATE 가 함께 롤백된다.
  2. 임시 DB 파일에 빌드하고 전 게이트 통과 시에만 원자적 교체(rename). WORK-005 재실행과도 맞는다.

### F3. 강남언니 정합률 게이트가 계산만 하고 막지 않는다 — 게이트 기준 완화

- **위치**: `build/silver.py:203-210` (`gu_agreement_pass` 를 dict 로 **반환만** 한다) ·
  `build/__main__.py:54-56` (`통과/미달` 을 **출력만** 하고 exit code 에 반영하지 않는다)
- **이식 원본**: `reference/ontology_demo/scripts/reviews_finalize.py:117-118`

  ```python
  if agree < THRESH:
      sys.exit(2)
  ```

- **근거 규칙**: rules.md 스코프 규칙 *"게이트 기준(행수 대사·대조값·PII 0건)을 임의로 완화하지
  않는다 — 미달이면 그대로 보고"* · 이식 원칙 *"기존 scripts 의 규칙·fail-fast·대사 로직을 그대로
  옮기고 입출력만 파일→DB 로 바꾼다"*. 기록 04 게이트(정합률 ≥ 80%)가 포팅 과정에서 **차단력을
  잃었다.** 현재 값이 기준을 넘는지와 무관하게, 재빌드에서 미달이 나도 빌드는 exit 0 으로 끝난다.
- **닫는 법**: `silver.build()` 가 `gu_agreement_pass` 가 False 면 `BuildError`(전용 코드 또는
  `REBUILD_MISMATCH`)를 던지게 한다. 채점 누락·점수 단위 위반은 이미 그렇게 막고 있으므로
  (`silver.py:197-198`) 같은 자리에 얹으면 된다.

---

## 2. 경고 (WARN) — 차단은 아니나 남겨 두면 새는 자리

| # | 위치 | 내용 |
|---|---|---|
| W1 | `build/gates.py:232` | 게이트 3 반환이 `views_scanned: 4` 인데 실제 스캔은 `v_bronze_vegas_reservations`·`v_bronze_reviews` 2종뿐이다(`gates.py:178-226`). 실버 뷰는 가릴 원값이 없어 검사 자체는 불필요하지만, **리포트 수치가 실측보다 넓다.** 2 로 고치거나 실버 뷰도 스캔 대상에 넣어라 |
| W2 | `build/gates.py:157` | `csv_parity` 불일치 메시지가 **셀 원값을 그대로 로그에 찍는다**(`CSV {a[c]!r} vs DB {b[c]!r}`). `silver_reservations.staff` 는 직원 실명이고, 같은 값을 리뷰 본문에서는 `[직원]` 으로 가린다. spec PII 목록(환자명·전화·생년월일·작성자명) 밖이라 위반은 아니지만 경계가 어긋난다 — 불일치 위치(테이블·행·컬럼)만 남기는 편이 규율에 맞다 |
| W3 | `build/gold.py:320` | `END = datetime.date(2026, 8, 30)` 하드코딩. 원본(`build_gold.py:252`)과 동일하므로 이식으로는 정확하나, 데이터 창이 늘면 `is_partial_cohort` 가 **조용히** 틀린다. `MAX(resv_date)` 유도로 바꿔도 규칙 재해석이 아니다 |
| W4 | `build/silver.py:198` | 점수 범위·근거 미실존·마스킹 잔존·채점 누락을 전부 `EnumViolation`(`ENUM_VIOLATION`)으로 올린다. Case Matrix 에서 `ENUM_VIOLATION` 은 `visit_status` enum 전용이다 — 코드가 원인을 가리키지 못한다. `procedure_concept` 은 올바르게 `CLOSED_LIST_VIOLATION` 을 쓰고 있으니(`silver.py:171`) 나머지도 전용 코드 또는 신설 코드로 갈라라 |
| W5 | `build/silver.py:256` | `(r.get("language") or "ko") != "ko"` — 원본은 `r.get("language", "ko") != "ko"`(`build_catalog.py:60`). **빈 문자열 처리가 갈린다**(원본: 제외 / 이식: ko 취급하여 포함). 현 데이터에 빈 값이 없어 `csv_parity` 가 통과하지만 잠재 이식 편차다 |
| W6 | `build/silver.py:264` | `"reconciled": len(rows) == kept + (len(rows) - kept)` — 항상 True 인 죽은 대사식. 「대사했다」는 착시만 남는다 |
| W7 | `build/masking.py:62-68` | 1자 이름은 `substr(1,1) || (빈 문자열)` = **원값 그대로**가 된다. 다행히 게이트 3 의 값 집합 대조가 이를 `PII_LEAK` 으로 잡아 빌드를 세우지만(안전한 방향), 실데이터에 1자 이름이 들어오면 마스킹이 아니라 **빌드 실패**로 끝난다. `길이 1 → '○'` 분기를 두는 편이 낫다 |
| W8 | `build/silver.py:104` | `BRANCH_ALIAS[r["branch"]]` — 알 수 없는 지점 표기가 들어오면 `BuildError` 코드 없이 `KeyError` 로 죽는다. 다른 fail-fast 는 전부 코드를 남기는데 여기만 예외다 |
| W9 | `build/load_bronze.py:64-66` | `config.py:48-58` 에 `vegas_dir`·`nexus_dir`·`scoring_dir` 프로퍼티를 두고도 여기서 `dd / "bronze" / "vegas"` 를 다시 조립한다(`gate1` 도 동일, `:131,:137`). 원천 경로 규약의 SoT 가 둘이 된다 — `data_dir` 오버라이드를 받는 헬퍼 하나로 합쳐라 |

문서 정합 하나: `build/spec_contract.py:11,41,80` 이 SPEC-001 을 v0.0.4 / v0.0.3 으로 참조한다.
파일 실제 버전은 **v0.0.5**(OQ-3·OQ-6 닫힘 반영)다. 값은 v0.0.5 와 일치하므로 표기만 갱신하면 된다.

---

## 3. 통과 확인 (근거 있음)

- **S-001 (관계는 데이터에)** — 통과. `ontology.py` 는 정본 CSV 를 그대로 적재할 뿐이고, 코드 상수에
  cause→effect 쌍은 **0건**이다. `spec_contract.py` 가 갖는 것은 노드 id·라벨·유형과 개수(§4 표)이며,
  이는 AC-6 이 명령한 1:1 대조용 계약값이지 관계 지식이 아니다. 프롬프트도 없다.
- **S-002 (read-only 소비)** — 통과. `db/connection.py:34` 가 `file:...?mode=ro` URI 로 열고,
  `tests/test_p1_bootstrap.py:23-32` 가 INSERT·DDL 거부를 실증한다. 자유 SQL 표면은 이 WORK 에 없다.
- **PII** — 통과. 실버에 `patientName`·`phone` 미반입(`db/schema.py:148-167`, 테스트
  `test_p4:183-190`), `birthday` → `age_band`. 로그는 행수·`resvDate`·`chartNo` 만 남고
  (`load_bronze.py:148-155`, `silver.py:80-87` — `chart_no` 는 기록 03 확정으로 PII 아님),
  게이트 3 은 건수만 보고한다(`gates.py:190,206`). 테스트 픽스처의 위조 표본은 전부 합성값
  (`test_p4:136` `'합성표본'`)이고, 리뷰 근거 문장은 **마스킹된 본문 안에 실존할 것**을 강제해
  (`silver.py:175-176`) `score_evidence` 경유 누출 경로도 닫혀 있다.
- **이식 원칙** — F3 을 제외하고 통과. `build_reservations.py` · `build_catalog.py` · `build_gold.py` ·
  `reviews_prepare.py` · `reviews_finalize.py` 5종을 전건 대조했다. 연령대·감성 임계·중복 11필드·
  백분위 경계(하위 25%/10%)·직전 존재 행 기준 파생·네이버 관측 개시 빈 값·프로모션 이벤트 1행 —
  **규칙 재해석 0건**. `gates.csv_parity` 가 10테이블을 셀 단위로 대조해 등가를 증명하는 구조는
  요구 이상이다(원본 게이트였던 「유기 신호 주별 배분 합 60」·「리텐션 코호트 합」은 gate2 목록에
  없지만, 두 테이블 모두 셀 대조 대상이라 실질 커버된다).
- **spec 이름·값 계약** — 통과. 브론즈 16 · 실버 6 · 골드 5 · 온톨로지 2 · 뷰 4 가 §4 표와 정확히
  일치하고(`db/schema.py`, `masking.py:30-35`), enum 8종·마스킹 표기 3종·Case Matrix 코드 8종이
  전부 매핑된다(`errors.py:26-57`). `node_type` 영문 정본·판정 한글 정본·`lag` 원형 보존도 지켜졌다.
- **스코프** — 통과. 변경은 전부 `app/ontology-agent/` 안이고 그 밖은 0건. 산출 DB 는
  `.data/ontology_demo.db` 로컬이며 `.gitignore:2` 로 제외된다. `/Users/...` 같은 절대경로·
  원천 파일명 하드코딩은 grep 상 0건이고 전부 `config.py`(env `ONTOLOGY_*`) 경유다.
- **코드 품질** — `app/back/config.py` 의 pydantic-settings 패턴을 따랐다. `build/` 가 패키지 내부는
  상대 import, `config`·`db` 는 절대 import 로 섞이는데(`load_bronze.py:18-26`), `app/back` 은 전부
  절대 import 다 — 패키지 내부에서는 일관되므로 지적에 그친다.

---

## 4. 워커 보고 미결 3건에 대한 의견

### (1) AC-8(뷰 경유 강제) WORK-002/003 이월 — **이월에 동의. 단 조건을 붙여라**

WORK-001 에는 소비자 표면이 없으니 지금 판정할 대상이 없다. 이월이 맞다.
다만 **`connect_ro()` 는 AC-8 을 강제하지 못한다**는 점을 이월 조건에 명시해야 한다 — 같은 커넥션으로
`SELECT * FROM bronze_vegas_reservations` 가 그대로 되고, 읽기 전용은 **쓰기만** 막는다.
DEC-002 가 경고한 "새 경로가 곧 구멍"은 아직 코드로 막힌 데가 없다. WORK-002 착수 조건으로 둘 중
하나를 요구할 것을 권한다.

1. 도구 계층에 **허용 테이블 화이트리스트**(`v_*` · `gold_*` · `ontology_*`)를 두고 그 밖은 예외로
   떨군다 — 파라미터화 조회만 제공하는 S-002 구조와 자연스럽게 맞는다.
2. 도구·API 소스에 `FROM bronze_` / `FROM silver_`(`v_` 접두 아님) 검색 **0건**을 테스트로 고정한다.

둘 다 값싸고, "조회 경로 목록으로 확인"이라는 AC-8 의 문구를 사람 점검이 아니라 코드로 옮긴다.

### (2) promo v2 id 를 브론즈에서 참조하는 문제 — **미결이 아니라 F1 위반이다**

워커가 미결로 남긴 판단은 옳지 않다. SPEC-001 §4 가 "골드가 브론즈를 직접 읽지 않는다"를 명문으로
적었으므로 이건 열린 질문이 아니라 닫힌 계약이다. 다만 **고치는 비용이 낮고 이식 원칙과도 충돌하지
않는다** — 실버가 원천 내부 id 를 한 컬럼 보존하면 끝난다. 값을 바꾸는 게 아니라 식별자를 버리지 않는
것이므로 "변환 규칙 재해석"이 아니다. F1 항의 닫는 법대로 처리하고, 처리 후 `gold_promo_calendar`
57행과 v2 구성 특성 4컬럼이 `csv_parity` 로 동일한지만 재확인하면 된다.

### (3) 부분 월 플래그 기준 — **현 구현 지지. spec 에 판정식 한 줄을 추가하라**

`build/gold.py:224` 의 `is_partial_month = days_observed < 달력일수` 는 주별
`is_partial_week`(`_days < 7`)와 같은 규율이고, "이 달의 합계가 온전한 한 달을 대표하지 않는다"는
플래그의 목적에 정확히 맞는다. 결측일(2026-02-17) 때문에 2026-02 가 부분 월로 잡히는 것도 옳다 —
그 달의 합계는 실제로 하루 모자란다. 새 정의를 만든 것이 아니라 주별 정의를 그대로 준용했으므로
"일별에서 집계한다는 것 외에 새 정의를 만들지 않는다"(§4)와도 어긋나지 않는다.

문제는 spec 쪽이다. §4 골드 절은 *"기간 경계가 걸린 월에는 부분 월 플래그를 단다"* 라고만 적어
**결측일 사유를 담지 못한다.** 소비자가 이 플래그를 "1월·8월(경계 월)"로만 읽으면 2월을 오독한다.
코디에게: SPEC-001 §4 골드 절에 판정식(`is_partial_month = days_observed < 그 달의 달력일수`)과
동반 컬럼 `days_observed` 를 계약으로 등재해 달라. 코드 수정은 필요 없다.

---

## 5. 재검수 조건

F1·F2·F3 수정 후 (a) `uv run python -m build all` 이 게이트 전항 통과, (b) 게이트 2 를 인위적으로
실패시켰을 때 **DB 가 이전 상태로 남는지**(F2 회귀 테스트), (c) 정합률 미달 표본에서 exit ≠ 0 인지
(F3 회귀 테스트) — 이 세 가지가 테스트로 고정되면 PASS 로 뒤집는다. WARN 9건은 차기 WORK 에 얹어도
무방하나 W1·W2·W6 은 리포트·로그의 사실성 문제라 같이 처리하는 편이 싸다.
