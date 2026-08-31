# 리뷰 리포트 — task-redesign 어댑터 delta / backend (2026-08-31)

## 판정: FAIL — 위반 1건 (IB-6 유실 금지 · IB-7 항상 200 을 깨는 예외 누출 경로)

위반은 **1건뿐이고 수리 폭이 3줄**이다. 계약 매핑(IB-1~IB-9)·감사 7종·설정 게이트·회귀 0 은 전부
확인됐다. FAIL 사유는 「어떤 입력에도 파서가 던지지 않는다」는 이 모듈의 제1 불변식이 실제로는
깨져 있고, 그 예외가 라우터의 `try` **밖**에서 나 200 ack 계약과 유실 금지를 동시에 깬다는 것이다.

## 검수 범위

- delta: 미커밋 7파일 (수정 4 / 신규 3). 직전 커밋 `80f50098` 까지는 검수 완료분이라 보지 않았다.
  - 수정 `back/.env.example` · `back/app/config.py` · `back/app/routers/slack.py`(+166) ·
    `back/app/services/action_runtime/workflow/incident/const.py`
  - 신규 `.../incident/slack_error_adapter.py` · `back/tests/api/test_slack_error_alert_events.py` ·
    `back/tests/services/engine_v2/test_incident_slack_error_adapter.py`
- 기준: SPEC-152 §인바운드 트리거 IB-1~IB-9 / WP-126 §P7 / `task-redesign-adapter-be-brief.md` /
  `roles/mediness/reviewer/rules.md`(backend 모드)
- 실행한 검사: `git diff --stat` · `git status --porcelain` · 호출부 대조(`raise_incident`·`start_run`·
  `_assemble`·`get_catalog`·`product_repo.list_rows`·`AuditLogRepository.create`·`bind_tenant`·
  gatekeeper lead resolver `incident/workflow.py:585-598`) · 기존 테스트 회귀 대조
  (`tests/api/test_slack_events.py:181`) · 파서 예외 경로 재현(격리 스크래치패드에서 순수 함수 재현,
  레포 코드·테스트는 실행하지 않음)

## 위반 (FAIL 사유)

### V-1. `parse_error_alert` 가 예외를 던질 수 있고, 그 호출이 라우터 `try` 밖에 있다

- `back/app/services/action_runtime/workflow/incident/slack_error_adapter.py:496-499` —
  `_parse_datetime` 의 fallback 이 `except ValueError:` **핸들러 안에서** `datetime(...)` 을 조립한다.
  regex(`_RE_DATETIME`)는 `mo`·`d`·`h` 를 `\d{1,2}` 로 받으므로 형식은 맞고 값이 불가능한 문자열이
  그대로 생성자로 들어가고, 거기서 난 `ValueError` 는 **핸들러 안이라 잡히지 않고 그대로 올라간다.**
  재현(동일 로직 재구현): `2026-08-31 24:00` → `hour must be in 0..23`, `2026-02-30 14:22:01` →
  `day 30 must be in range 1..28`, `2026-13-05 10:00` → `month must be in 1..12`.
  이 값은 「시간 (KST)」 라벨 하나로 들어온다 — 리포터가 시각 문자열을 스스로 포맷하는 자리라
  (`%H` 대신 24시 표기, TZ 변환 실수) 도달 불가능한 입력이 아니다.
- 같은 파일 `:508-510` — `_ts_to_iso` 는 `(TypeError, ValueError)` 만 잡는데
  `datetime.fromtimestamp(float(ts))` 는 범위 밖 값에서 `OSError`(`Value too large…`) ·
  `OverflowError`(`timestamp out of range`) 도 던진다. 같은 누출 축이다.
- `back/app/routers/slack.py:349-350` — `parsed = adapter.parse_error_alert(...)` 가 **`try:` 바로 앞**에
  있다. 그래서 위 예외는 `AUDIT_RAISE_FAILED` 로도 착지하지 못하고 500 으로 나간다.
- 결과가 계약 2건을 동시에 깬다:
  - **IB-7** 「슬랙에는 언제나 200 ack(4xx/5xx 는 재전송 폭주를 부른다)」 → 500 응답.
  - **IB-6** 「유실 금지」 → `mark_event_seen` 이 `:337` 에서 **이미 event_id 를 소비한 뒤**라,
    Slack 재전송은 `duplicate_error_alert` 로 조용히 접힌다. 그 알림은 어떤 run 도 되지 못한다 —
    「해석 못 하니 버린다」가 금지된 처분이라고 같은 파일 `:15-17` 이 스스로 선언한 바로 그 상황이다.
- 근거: SPEC-152 §인바운드 트리거 IB-6 표(「형식 미상·라벨 매핑 실패 → raise 진행」) · IB-7 표 서문 ·
  브리프 체크리스트 2「예외 불투과(어떤 입력에도 raise 유실 없음)」 ·
  모듈 자체 docstring `slack_error_adapter.py:13-17`(제1 불변식 — 유실 금지)
- 권장 수정: `_parse_datetime` 의 fallback 조립을 자체 `try/except (ValueError, OverflowError): return None`
  으로 감싸고, `_ts_to_iso` 의 except 절에 `OSError·OverflowError` 를 더한 뒤,
  `slack.py:349` 의 `parse_error_alert` 호출을 아래 `try` 블록 **안**으로 옮긴다(불변식이 나중에 다시
  깨져도 `incident_raise_failed` 로 착지하도록 — 파서를 고치는 것만으로는 구조가 여전히 취약하다).
- 회귀 테스트 자리: `test_incident_slack_error_adapter.py:299 test_parser_never_raises_on_junk` 의
  junk 목록에 「형식은 맞고 값이 불가능한 시각」 1건(`시간 (KST): 2026-08-31 24:00`)을 더하면 잡힌다.

## 경미 (WARN)

- `slack_error_adapter.py:149-180` — `resolve_organization_id` 가 gatekeeper 1단
  (`incident/workflow.py:585-598`)과 **조인 키는 같지만 `User.active.is_(True)` 필터가 없다.**
  퇴사·비활성 대표가 남아 있으면 run 은 그 사람의 조직으로 도장되는데 declare gatekeeper 는 그 대표를
  건너뛰고 admin 폴백으로 간다 — 조직이 medisolve 단일인 동안은 무증상이지만, 조직이 갈리는 순간
  「도장된 조직 ≠ 결재자 조직」이 된다. 근거: SPEC-152 IB-9 ①「gatekeeper resolver 1단과 같은 조인 키」·
  실측 resolver 의 활성 필터. 권장: `User` 조인 + `User.active` 를 같이 걸어 사다리 1단을 완전히 동형화.
- `slack_error_adapter.py:9-11` vs `:149` — 모듈 docstring 이 「여기 있는 것은 **전부 순수 함수**
  (DB·설정·시각 무접촉)」이라고 자리 규칙을 선언하는데, 같은 모듈의 `resolve_organization_id` 는
  세션을 받아 `select()` 를 도는 코루틴이다. 배치 자체는 (IB-9 가 «어댑터가 소유하는 해소» 로 쓴 자리라)
  받아들일 만하지만, **모듈이 스스로 세운 경계 문장이 사실과 어긋난 채 남아 있다** — 다음 사람이 이
  문장을 믿고 여기에 순수 함수 테스트만 붙인다. 근거: rules.md 「자리 규칙」. 권장: docstring 을
  「파싱·매핑은 순수, 조직 해소만 DB 접촉」으로 좁힌다(코드 이동 불필요).
- IB-9 사다리에 **테스트가 0건**이다. 이번 delta 에서 유일하게 DB 를 만지는 신규 로직인데,
  ① 대표 조직 선택 ② `MEDISOLVE` 폴백 어느 갈래도 단언되지 않는다(`_RaiseSpy` 는 그 뒤 단계를 대역으로
  세우지만 `resolve_organization_id` 자체는 통과만 하고 아무도 보지 않는다). 근거: rules.md backend
  「신규 라우터/서비스에 대응 테스트가 있나(존재·의미)」. 권장: 대표 1행 + 미해소 2케이스 단위 테스트.
- `slack_error_adapter.py:198` `_RE_PLAIN_INLINE` 의 라벨 길이 상한 32자 — 평문/attachment 경로에서
  32자 넘는 라벨(제품별 추가 필드 이름)은 extras 보존에서 조용히 빠진다. 원문(`text`·`blocks`)은
  언제나 `event` 에 동봉되므로 **IB-3 의 「드롭 금지」자체가 깨지지는 않는다** — 상한이 의도된 값인지만
  확인 요청(근거 불충분, 코디네이터 판단).

## 기존 부채 (이번 판정 제외)

- `raise_incident` → `runner.start` 가 **커밋 전에** 비동기 조사단을 dispatch 하는 구조는 웹
  `/incidents/raise`(`action_runtime_v2.py:318-331`)와 동형이다 — 어댑터가 새로 만든 축이 아니다.
- `from app.routers.action_runtime_v2 import _assemble`(`slack.py:403`)는 라우터→라우터 private import
  지만 **같은 파일 `:576` 에 이미 있던 패턴**이라 이번 delta 의 위반으로 세지 않는다(rules.md #5).

## 확인한 것 (PASS 근거)

1. **IB-1 수신 경계** — 순서가 채널(`slack.py:311`) → 봇(`:325`) → `event_id` 멱등(`:337`) → 승격이다.
   멱등 마킹이 경계 **뒤**라 남의 채널·사람 메시지가 dedupe 슬롯을 태우지 않는다. 봇 판정은
   `bot_id`/`app_id`/`bot_profile` 식별자 축이고 텍스트 모양을 보지 않는다
   (`slack_error_adapter.py:94-111`, 테스트 `:422 test_human_message_never_passes_even_with_the_same_text`).
   빈 allowlist 는 **전부 차단**(`:102-104`, 테스트 `:429`). 헤더 `ENV` 는 파싱·보존만 하고 2차 게이트로
   쓰지 않는다(IB-1「환경 경계를 소유하는 것은 채널」준수 — grep 결과 `environment` 소비처 0).
2. **미주입 = 비가동 + 회귀 0** — `_error_alert_enabled()`(`slack.py:279-289`)가 **둘 다** 요구하고,
   설정 기본값은 빈 문자열(`config.py:389-390`). 반쪽 설정도 서지 않는다(테스트 `:286`).
   미가동 시 `message` 는 예전 `ignored_message` 그대로(테스트 `:274`), 기존
   `tests/api/test_slack_events.py:181` 도 기본 설정에서 그대로 통과한다(monkeypatch 는 새 파일 안에서만).
   `app_mention` 경로 무수정 확인(diff 상 4b 블록 삽입 + 함수 3개 추가뿐, 테스트 `:297`).
3. **IB-3/IB-6 파서** — `blocks`/`attachments`/평문 `text` 3경로를 `_text_chunks`(`:320-342`) 한 자리에서
   모아 같은 매핑을 태운다(테스트 `TestAlternateShapes`). 계약 키가 보존분을 덮는 방향이 맞다
   (`:280-293` — `event.update(extras)` 뒤에 계약 키 update, 테스트 `:250
   test_contract_keys_win_over_preserved_labels`). 반쪽 매핑을 성공으로 표기하지 않는다(`:264-265`).
   ⚠ 「어떤 입력에도 raise 없음」만 V-1 로 깨져 있다.
4. **IB-4 슬러그** — 대소문자·주변 공백만 무시한 정확 일치, `slug` → `label` 순, 비활성 행 제외,
   미매칭 시 빈 문자열(`:119-137`). 부분 일치 거부 테스트(`:393`). 실제 카탈로그 행 모양
   (`product_repo.py:20-29` — `slug`·`label`·`is_active` 존재)과 키가 일치해 라이브에서 빈 결과로
   떨어지지 않는다. 미매칭이 승격을 막지 않음(API 테스트 `:206`).
5. **IB-5 dedupe** — `trace_id` 없으면 `None`, 합성 없음(`:311-313`, 테스트 `:357`).
   두 축 분리 확인: `event_id` 는 라우터 Redis 마킹, `dedupe_key` 는 서비스 층 열린 run 합류
   (`runs_surface.py:82-87`) — API 테스트 `TestIdempotencyAxes` 가 둘을 각각 고정한다.
6. **IB-7 처분 7종 전부 배선** — `ignored_channel`(`slack.py:311-320`) · `ignored_non_bot`(`:325-334`) ·
   `duplicate_error_alert`(`:337-346`) · `incident_raised` / `incident_raised_unparsed` / `incident_deduped`
   (`:377-383`) · `incident_raise_failed`(`:366-375`). 나머지 2행(서명 실패 401 · 구독 밖 `ignored_*`)은
   기존 경로 그대로. 승격 갈래는 전부 200(실패 포함, 테스트 `:252`) — **단 V-1 경로만 예외.**
7. **IB-8/IB-9** — HTTP 자기호출 0(`_raise_from_error_alert:396-419` 가 `incident_surface.raise_incident`
   직호출, `started_by_user_id=None`, `source=slack_error_channel`; 테스트 `TestServiceLayerWiring`).
   `/raise` HTTP 스키마·declare 게이트·기존 decision 슬랙 분기(`/interact`·`app_mention`) 무수정.
   커밋 경계는 라우터 소유로 `runs_surface.start_run` 주석 계약과 일치. tenant 사다리는 IB-9 ①②와
   문면 일치(대표 `is_lead` 조인 → `MEDISOLVE_ORGANIZATION_ID` 폴백, `slack_error_adapter.py:167-180`);
   활성 필터 차이만 위 WARN.
8. **보안** — 새 분기는 `_verify_or_audit`(`slack.py:148-157`) **뒤**의 `event_callback` 블록 안에만
   있어 서명검증 우회 경로가 없다. 신규 설정 2종은 비밀값이 아니고(채널 id·봇 id) 로그·감사에
   그 값을 싣지 않는다(`logger.exception` 은 event_id 만, 감사 params 는 event_id/채널/파싱표식/
   service/dedupe_key). `.env.example` 도 빈 값으로만 제공.
9. **allowed_paths·migration** — diff 전량 `back/` 이하, `front/`·`mcp/`·문서 레포 이탈 0.
   `models/` 변경 0 → `alembic/versions/` 필요 없음(WP-126 §Code Surface 「P7 도 migration 0」과 일치).
   신규 상수 `TRIGGER_SOURCE_SLACK_ERROR_CHANNEL`(`const.py:224`)은 이미 열려 있던 `source` 축에 값 하나.
10. **계층·재사용** — 파싱은 순수 함수로 services 층에 있고 라우터는 경계 판정·감사·커밋만 한다
    (WP-126 §Code Surface「라우터에 파싱 로직을 두지 않는다」). 라우터에 `session.execute`/`select()`
    직접 호출 없음. 기존 `mark_event_seen`·`_record_audit`·`bind_tenant`·`get_catalog`·`_assemble` 재사용,
    동명 기능 재구현 0(grep 대조).
11. **확인 안 함** — 테스트 실행(브리프상 금지) · 실제 Slack payload 대조(실물 JSON 미확보, OI-10
    과 같은 축) · 리포터 라벨 SoT(레포 밖, OI-11).
