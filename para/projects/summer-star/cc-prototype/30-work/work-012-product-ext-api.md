---
type: work
id: WORK-012
title: "시술 · 상품 메뉴 저장 + 외부 연동 API — BE1 메뉴 표 · 동기화 → BE2 외부 인증 · 기록 · 제한 → BE3 메뉴 API → BE4 고객 조회 → BE5 예약 → BE6 Swagger · 시험 → REVIEW → INFRA(Secret · env) → 로컬 데모 실물 확인 → 배포 → 운영 실물 확인"
status: draft
product: cc-prototype
feature: procedure
work_type: enhancement
owner: kknaks
progress: 0
created_at: 2026-11-11
updated_at: 2026-11-11
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/work
  - status/draft
links:
  baselines: []
  decisions:
    - "[[decision-010-product-ext-api|DEC-010]]"
  specs:
    - "[[spec-008-product-ext-api|SPEC-008]]"
    - "[[spec-005-reservation-board|SPEC-005]]"
  works:
    - "[[work-007-reservation-board|WORK-007]]"
  releases: []
  related: []
sources:
  - "para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md (0.2.1)"
  - "para/projects/summer-star/cc-prototype/10-decision/decision-010-product-ext-api.md (D-01 ~ D-36)"
  - "orchestration/work/api-swagger-docs/_RESUME.md §2"
  - "cc-prototype procedure/back origin/main c9f30ac (읽기만 — 대상 파일 · 줄)"
---

# 시술 · 상품 메뉴 저장 + 외부 연동 API — 빌드 계획

계약은 **SPEC-008 0.2.1** 에 있다. 이 문서는 빌드 순서만 적고, 계약을 다시 쓰지 않는다. 결정은 DEC-010(D-01 ~ D-36)이다. 화면은 없다(D-01).

## Meta

- **진행**: 문서만 있다. 코드는 아직 손대지 않았다. progress 0
- Covers spec: SPEC-008 0.2.1. SPEC-005 의 예약 생성(§5.5)은 고치지 않고 다시 쓴다(D-11)
- 코드 레포: `kknaksss/cc-prototype` — 범위는 **`procedure/back/**`** 하나다. `procedure/front/**` · `procedure/app/**` 는 건드리지 않는다(D-01)
- **infra**: 새 env 3개(SPEC-008 §2.2 — 키 2 · 기본 그룹 1)가 생긴다. 세 env 모두 지금 `KOS_ZONE_ID` 와 같은 길이다 — infra 레포(private) `provisioning/secrets/cc-prototype-prod.env.example` 에 이름만 빈 값으로 더하고, 값은 **클러스터 Secret** `cc-prototype-secret` 에만 둔다(D-23 · SPEC-008 §2.2). 값은 사용자가 넣고, infra · profile · 코드 레포와 문서에는 이름만 적는다. 새 표는 back 이 부팅할 때 `CREATE TABLE IF NOT EXISTS` 로 만든다(같은 SQLite 파일 · PVC 그대로). 새 경로는 `/api/ext/…` 이고 지금 ingress `/api` → back 안에 들어간다(`_RESUME` §2 — ingress 무변경)
- base: 지금 main(`c9f30ac` 이후 운영본). 워크트리 · 브랜치는 코디가 정한다
- 워커: backend(BE1 ~ BE6 · 한 브랜치에서 차례로) · reviewer · 코디(INFRA · 실물 확인 · 배포)
- **검증 규칙**: WP 마다 **그 WP 의 시험만** 돌린다(`uv run pytest -q tests/test_ext_<…>.py` 꼴). 전체 `uv run pytest -q` 는 **BE6 끝에 한 번** 돌린다
- **실물 e2e 없이 done 금지**: 데모 KOS 로 이름 + 이메일 조회와 예약이 실제로 되는지(WP-E2E-LOCAL) · 운영 호스트에서 연동처 키로 1번(WP-E2E-PROD)
- public 레포다 — 리포트 · 커밋 · 시험 데이터에 키 · 실명 · 이메일 · 연락처 · KOS id 값을 쓰지 않는다. 시험 값은 `<이름>` · `a@example.com` 꼴로만 쓴다

## 계약 고정점 (WP 사이에서 바뀌면 멈추고 코디에게)

| 고정점 | SPEC-008 | 쓰는 WP |
|---|---|---|
| 메뉴 표 9 · 칸 · 맞추는 키 · `raw` | §3.2 | BE1 · BE3 |
| `ext_call` 칸 | §3.4 | BE2 |
| env 이름 3 | §2.2 | BE2 · BE5 · INFRA |
| 헤더 `X-Api-Key` · 연동처 `linky` · `charty` · actor `ext:<연동처>` | §7.1 · §3.5 | BE2 · BE5 |
| 경로 셋 · 요청 · 응답 칸 | §6.3 ~ §6.5 | BE3 ~ BE5 · BE6 |
| 오류 code(`ext_unauthorized` · `too_many_requests` · `customer_not_found` · `customer_ambiguous` · `ext_not_configured` + 지금 code) | §6.2 ~ §6.5 | BE2 ~ BE6 |
| 조회 함수 하나(조회 · 예약 같이 씀) | §5 | BE4 · BE5 |
| 시술권 가격 칸 `bundlePrice` · 메뉴 `syncedAt` | §4.3 · §6.3 · §6.4 | BE3 · BE4 |
| 행위자 겹(`actor: Account \| str`) | §3.5 | BE5 |
| 키 없는 거절 IP 제한 · `ext_call` 미들웨어 | §3.4 · §7.3 · §7.4 | BE2 |

## Work Packages

| WP | 내용 | 계약 | 워커 | 대상 파일(범위) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| **WP-BE1** | **메뉴 표 · 동기화** — `MENU_SCHEMA`(표 9 · 인덱스 2) · `Database.__init__` 에 `executescript` 한 줄 · repo upsert(`kos_id` · 구성 = (`option_kos_id`, `seq`) · 타겟 국가 = `raw`) · 「없음」 표시(작업 성공 때만 · 구성 · 타겟 국가는 자기 키로 하는 함수를 따로 · 되살림 = upsert 에 `present: True`) · 새 `kos/menu_sync.py`(작업 ① ~ ⑧ · ③ `getProductOptions` 를 N개씩 나눠 부름 · ③ 에서 빠진 옵션은 이전 값 · 작업마다 독립 · 실패 = 그 표 그대로 · `sync_state("menu")` · 잠금) · `runtime.master_once()` 에서 `resv.master()` 다음에 호출(조회 시간과 상관없이) | SPEC-008 §3.1 ~ §3.3 · §4.1 | backend | `procedure/back/app/{repository/db.py,repository/repo.py,kos/menu_sync.py,kos/runtime.py,container.py}` · `tests/test_ext_menu_sync.py` · `tests/fake_kos.py`(메뉴 응답 더함) | SPEC-008 §9 T1 ~ T5 통과 · **데모 KOS 로 한 바퀴 1회**(코디가 허락한 로컬 실행 — 표 행 수가 조사 1 §4 와 같은 규모(상품 101 · 옵션 323 · 구성 32 · 시술 804 · 진료항목 226 · 기기 302 · 약물 349 · 카테고리 15 · 국가 4)인지 · SINGLE 옵션의 `medical_service_kos_id` 가 채워졌는지(수만 적음)) · 리포트에 **실제 공개 경로 8개**(스펙 operationId 에서 옮긴 것)와 **N 값 · 근거**(KOS 문서 상한 또는 실측) | `uv run pytest -q tests/test_ext_menu_sync.py tests/test_kos_sync.py` | 대기 |
| **WP-BE2** | **외부 인증 · 기록 · 제한** — `config.py` env 3 · `domain/errors.py` `ServiceUnavailable`(503) · `api/deps.py`(또는 `api/ext.py`) `require_ext_key`(`X-Api-Key` · `hmac.compare_digest` · 빈 env 연동처 제외 · `Authorization` 안 봄 → 연동처 이름) · `RateLimiter` 재사용(키당 최근 60초 60 · 막힌 요청 안 셈 · 401 은 키당 카운터에 안 셈) · **키 없는 거절 IP 제한**(키 없는 거절 = `client` null 인 오류 응답 전부 — 401 · 없는 경로 404 · 깨진 본문 400 · 405 를 IP 당 셈 · IP 차단 429 는 안 셈 · 최근 60초 10번이면 그 IP 를 키 검사 전 429 · `client_ip()` 재사용 · IP 저장 안 함 — 문진 웹 값 그대로) · `EXT_SCHEMA` `ext_call` 을 **`/api/ext` 미들웨어**가 모든 응답 뒤 1줄(`client` = 의존성이 `request.state` 에 남긴 값 · 없으면 null · `endpoint` = 매칭 라우트 `path_format` · 없으면 `"<METHOD> (unknown)"` · 키 없는 거절(위 정의 · IP 차단 429 포함)은 같은 IP · 같은 `outcome` 1분에 1줄 · 쓰기 실패는 응답 안 바꿈) · `/api/ext` 응답 `Cache-Control: no-store` · 빈 라우터 `api/ext.py`(`prefix="/api/ext"`) 등록 | SPEC-008 §2.2 · §3.4 · §6.1 · §6.2 · §7.1 ~ §7.4 | backend | `procedure/back/app/{config.py,domain/errors.py,api/deps.py,api/ext.py,repository/db.py,repository/repo.py,main.py,container.py}` · `tests/test_ext_auth.py` | §9 T23 ~ T28 · T31 통과(시험용 임시 경로 하나로 단언하거나 BE3 와 같이 확인 — **임시 경로는 BE3 에서 진짜 경로를 만든 뒤 지운다**. 남으면 Swagger 개수 단언 `n_ops - 5 - 3` 이 깨진다) · 검사 순서 T25 다섯 경우 · 로그 · `ext_call` 에 키 · 이름 · 이메일 · IP 문자열 0(caplog · 표 전수 · 경로에 이메일 꼴 → 표에 없음) | `uv run pytest -q tests/test_ext_auth.py tests/test_auth_roles.py` | 대기 |
| **WP-BE3** | **메뉴 API** — `GET /api/ext/menu`(`async def`) · `service/ext.py` 메뉴 트리 조립(DB 만 · 「지금 있는 것」 걸러내기 · 카테고리 `order` → 상품 · 옵션 · 구성 `seq` · SINGLE 단위 = 진료항목 단위 · 내지 않는 칸 0) · `schemas/ext.py` `ExtMenu`(모든 칸 `description` · `syncedAt` 메타 칸 D-36 — 메뉴 동기화가 실패한 바퀴도 이전 `last_ok_at` 을 남김: BE1 의 `set_sync("menu", None, …)` 가 `ok_at or prev_ok` 로 지키는지 T6 으로 확인) · BE2 시험용 임시 경로 지움 | SPEC-008 §6.3 | backend | `procedure/back/app/{api/ext.py,service/ext.py,schemas/ext.py,repository/repo.py}` · `tests/test_ext_menu.py` | §9 T6 ~ T8 통과 | `uv run pytest -q tests/test_ext_menu.py tests/test_ext_auth.py` | 대기 |
| **WP-BE4** | **고객 조회** — 조회 함수 하나(§5 — 이름 `strip` · `get-visitors` **한 페이지만**(`countInPage` 1000 · 조회 1건당 1번) · `count` > 1000 = 「없음」(시술권 조회 안 함) · KOS id 중복 제거 · **이름 정확 일치**(공백 전부 지움 · 대소문자 무시 · `name` 또는 `phoneticName`) · 이메일 `strip().lower()` 정확 일치 · 빈 email 후보 제외 · 0 / 1 / 2+) · 1명 = `customer` 사본 덮어쓰기(email 저장 안 함) · `getTicketBundlesQuery` 1번 · 묶음 → 한 줄(`bundlePrice` = KOS `price` 그대로 · `remainingCount` = `AVAILABLE` 만) · `{}` = `[]` · 실패 = 502 · `POST /api/ext/customers/lookup` · `ExtLookupRequest` · `ExtLookupResponse` · 직원 `search()` 는 건드리지 않음(O11) | SPEC-008 §4.2 · §4.3 · §5 · §6.4 | backend | `procedure/back/app/{service/ext.py,api/ext.py,schemas/ext.py}` · `tests/test_ext_lookup.py` · `tests/fake_kos.py` | §9 T9 ~ T16 통과(T9 = 한 페이지 · 같은 id 두 번 → 1명 · `count` 1001 → 404 KOS 호출 1번 / T12 = 부분 일치만 → 404 · 발음명 일치 → 200 · 대소문자 차이 → 200 · 공백 차이 → 가짜 KOS 응답을 직접 지정한 경우만 200 · 가운데 공백이 다른 입력 → KOS 0건 → 404. `tests/fake_kos.py` 의 `get-visitors` 검색 규칙(공백 그대로 · 부분 일치)은 고치지 않는다 / T13 「없음」 여섯 경우 바이트 같음) · **데모 KOS 로 1회**(email 이 채워진 데모 고객 1명 — 맞는 이름 + 이메일 → 200 · 이메일 한 글자 틀림 → 404 · 응답 키 집합 확인 · **`get-visitors` 원소에 `lastVisitedDateTimeUtc` 키가 오는지** 확인해 리포트에 적음(값 없이 「있음/없음」)) | `uv run pytest -q tests/test_ext_lookup.py tests/test_resv_detail.py` | 대기 |
| **WP-BE5** | **예약** — `POST /api/ext/reservations` · `ExtReservationRequest`(그룹 · 구역 · 담당자 칸 없음 · 모르는 키 400) · 기본 그룹(`KOS_EXT_RESERVATION_GROUP_ID` → `present` 그룹 ccc id · env 빔 · 그룹 없음 · **그 그룹에 켜진 구역 0** 이면 503 `ext_not_configured` · 사본 기준 · KOS 호출 전) · BE4 조회 함수로 1 / 0 / 2+ · 서버 안에서 `CreateReservationRequest` 를 만들어 `ReservationService.create()` 를 다시 씀(**행위자 문자열 겹** — `create()` · `_new_visitor()` · `kos_write()` · `_event()` 의 `actor` 를 `Account | str` 로 넓히고 `_event` 한 곳에서 문자열은 그대로 · `Account` 는 `login_id`. 외부는 `"ext:<연동처>"` 를 넘김 · 가짜 `Account` 없음 · 부르는 곳 무변경 — SPEC-008 §3.5) · `duplicated_visitor` → `409 customer_ambiguous`(`candidate` 없음) · 응답 = `{reservationId, customerId}` | SPEC-008 §3.5 · §6.5 | backend | `procedure/back/app/{service/ext.py,api/ext.py,schemas/ext.py}` · `service/reservations.py`(행위자 겹 네 함수 서명 · `_event` 한 줄만 — 직원 동작 그대로) · `tests/test_ext_reserve.py` | §9 T17 ~ T22 통과(T17 = actor `ext:linky` · T20 = 켜진 구역 0 → 503) · 직원 예약 · 접수 시험 회귀 0(T30 — 직원 `event_log.actor` = `login_id` 그대로) · **외부 응답 어디에도 `duplicated_visitor` · `candidate` 없음**(grep + 시험) | `uv run pytest -q tests/test_ext_reserve.py tests/test_resv_write.py` + 접수 시험 파일 1개(`reception` 을 부르는 기존 시험) | 대기 |
| **WP-BE6** | **Swagger · 시험 정리** — `api/docs.py` `T_EXT`(`외부 연동`) · `openapi_docs.py` tag 설명 · `ExtApiKey` securityScheme · `require_ext_key` 에 `security` 달기 · `DESCRIPTION` `## 외부 연동 API` 절(첫 줄 = email 없는 기존 고객 404 · 처음 예약하면 KOS 고객이 하나 더 생길 수 있음 · 이어서 「이름은 KOS 에 저장된 띄어쓰기 그대로」 · 공통 오류 표에 `405 http_error`) · `STATUS_TEXT` 503 · 외부 401 줄 「직원 로그인이 아니라 `X-Api-Key`」 · 세 엔드포인트 `summary` · `description`(조회 「없음」 · 이름 띄어쓰기 그대로(「공백 무시」 약속 금지) · `bundlePrice` 성질 · `IN_USE` · 예약 D-35 문장 · 메뉴 `syncedAt`) · 응답 표(`- \`code\` — 언제`) · `tests/test_openapi_docs.py` 개수 단언 `n_ops - 5 - 3` + 외부 단언 · **전체 시험 한 번** | SPEC-008 §8 · §9 T29 · T30 | backend | `procedure/back/app/{api/docs.py,openapi_docs.py,api/ext.py,schemas/ext.py}` · `tests/test_openapi_docs.py` · `tests/test_ext_docs.py` | T29 통과 · `/api/docs` 에 외부 셋이 `외부 연동` tag 로 보임 · **전체 `uv run pytest -q` 통과(수치 리포트)** · `ruff`(레포 설정이 있으면) | `uv run pytest -q`(이 WP 끝에 한 번) | 대기 |
| **WP-REVIEW** | reviewer: SPEC-008 §2 ~ §9 ↔ 코드 · 부록 A(D-01 ~ D-36) · 부록 B(Q1 ~ Q5 · Q-A ~ Q-C · W11) · 경로 셋 · 외부 라우터에 `require_login` · `Actor` 0 · 직원 라우터에 `X-Api-Key` 0 · 외부 응답의 내지 않는 칸 0 · `duplicated_visitor` · `candidate` 누출 0 · `ext_call` · 로그에 이름 · 이메일 · 키 0 · 「없음」 여섯 경우 바이트 같음 · 이름 검색 1번 · 키 없는 거절 IP 제한 · `ext_call` `endpoint` 고정값 · 직원 `event_log.actor` 그대로 · 메뉴 실패 = 이전 값 · `countInPage:20` 직원 검색 그대로 · 실명 · 키 grep. FAIL 은 모아서 한 번에 수정 발주 | 전체 | reviewer | 코드 변경 전체 | PASS | — | 대기 |
| **WP-INFRA** | 코디: env 3개(`PROC_EXT_KEY_LINKY` · `PROC_EXT_KEY_CHARTY` · `KOS_EXT_RESERVATION_GROUP_ID`)를 지금 `KOS_ZONE_ID` 와 같은 길로 더한다 — infra 레포(private) `provisioning/secrets/cc-prototype-prod.env.example` 에 **이름만 빈 값으로**, 값은 클러스터 Secret `cc-prototype-secret` 에만(SPEC-008 §2.2). 그룹 id 는 사용자가 고른다. **키 · id 값은 사용자가 넣는다**(infra · profile · 코드 레포 · 문서 · 리포트에 값 0). 로컬 `.env` 도 같은 이름으로 넣는다(값은 레포 밖) | SPEC-008 §2.2 · D-23 · D-33 | 코디 · 사용자 | infra 레포 `provisioning/secrets/cc-prototype-prod.env.example` · 클러스터 Secret | infra PR 머지 · Secret 생성 확인(값 안 봄) | — | 대기 |
| **WP-E2E-LOCAL** | 코디: 백엔드 커밋 뒤 로컬 compose 를 재기동한다(옛 코드로 확인 금지) → **데모 KOS 실물**로 ① 서버 시작 메뉴 동기화 · `GET /api/ext/menu` 200 · 행 수 ② 데모 email 보유 고객 1명 `lookup` 200(맞음) · 404(틀림) ③ **기존 고객 예약 1번**(그 고객 · 그룹 = env 그룹 · KOS 웹에서 예약이 보임) ④ **새 고객 예약 1번**(시험용 이름 + 사용자가 정한 시험 이메일 → KOS 고객 생성 + email 저장 → 같은 이름 + 이메일로 `lookup` 이 200) ⑤ 키 없음 401 · 61번째 429 · 없는 경로 404 의 `ext_call.endpoint` = `"<METHOD> (unknown)"`. 끝나면 ③ · ④ 예약을 직원 화면으로 취소한다. ④ 로 생긴 KOS 고객은 데모에 남는다(D-22 — 데스크가 정리하는 몫) · 값은 기록하지 않는다 | SPEC-008 §9 「실물 확인」 | 코디 · 사용자 | — | ① ~ ⑤ 확인 | — | 대기 |
| **WP-DEPLOY** | 코디: 코드 PR 머지 → back 이미지 → infra `back.imageTag` PR(+ WP-INFRA env) → sync · `/api/health` · `/api/docs` 에 `외부 연동` tag 확인 | — | 코디 | — | 운영 back = 이 판 | — | 대기 |
| **WP-E2E-PROD** | 코디: **운영 호스트 `https://ccc.medisolveai.xyz`**(운영 조건 · Cloudflare 경유)에서 연동처 키로 `GET /api/ext/menu` 200 · `lookup` 1번(데모 고객) · 키 없음 401 · `ext_call` 행 확인. 예약은 WP-E2E-LOCAL 에서 했으므로 운영에서는 하지 않는다(사용자가 원하면 1번 하고 취소) · 협업자에게 키를 건넬지와 admin 계정 회수 시점은 사용자 몫(D-26) | SPEC-008 §7.6 · D-26 | 코디 · 사용자 | — | 운영 확인 끝 · 사용자에게 보고 | — | 대기 |

## 병렬

- BE1 ~ BE6 은 **한 워커가 한 브랜치에서 차례로** 한다. `api/ext.py` · `service/ext.py` · `schemas/ext.py` · `repository/*` 를 같이 고치므로 나누면 충돌한다
- BE1(메뉴)과 BE2(인증)는 서로 기대지 않지만, 둘 다 `db.py` · `repo.py` · `container.py` 를 고친다. 그래서 차례로 한다
- WP-INFRA 는 BE2 의 env 이름이 고정되면(이미 SPEC-008 §2.2) 코드와 **병렬로** 할 수 있다
- WP-REVIEW 는 BE6 끝 · 전체 시험 통과 뒤에 한다

## 주의

- **KOS 쓰기는 WP-E2E-LOCAL 에서만** 한다. 데모 테넌트에서 하고, 운영 지점 키는 쓰지 않는다(`config.py` 주석 · D-06). BE1 · BE4 의 데모 확인은 **조회만** 한다
- 내부 API 는 브라우저 UA 가 필요하다(`kos/client.py` — 11-03 부터). 이름 검색은 지금 `KosClient.internal` 로만 부른다. 새 HTTP 클라이언트를 만들지 않는다
- 백엔드 커밋 뒤에는 compose 를 재기동한다. 옛 코드가 떠 있으면 「안 된다」로 보인다. 워커는 사용자 포트 · 프로세스를 건드리지 않는다(실물 확인은 코디가 허락한 1회만)
- 직원 고객 검색(`search()` · `countInPage:20`)과 직원 예약 생성 동작은 바꾸지 않는다. 예약 생성에 actor 를 넘기는 행위자 겹(SPEC-008 §3.5)은 타입만 넓힌다 — 부르는 곳을 고치지 않고 직원 경로의 `event_log` 값은 그대로 둔다
- `getProductOptions` 한 번에 넣을 수 N 과 공개 경로 8개는 **실측 · 스펙에서 옮긴 값**이다. 추정한 값으로 채우지 말고 BE1 리포트에 근거를 적는다
- `lastVisitedDateTimeUtc` 가 `get-visitors` 원소에 없으면 `lastVisitDate` 는 늘 null 이다. 다른 칸으로 추정해 채우지 않는다. BE4 리포트에 「없음」으로 올리면 코디가 판단한다
- 시술권 `totalCount` · `bundlePrice` 는 KOS 가 준 묶음 기준이다(GROUP 한 세트를 다 쓰면 줄어든다 — SPEC-008 §4.3). 산 때 값으로 되돌려 계산하지 않고, 칸 이름에 `purchase` · `VatIncluded` 를 넣지 않는다(D-08 · D-31)
- 외부 응답 · `ext_call` · 로그 · 리포트 어디에도 이름 · 이메일 · 키 값을 남기지 않는다(D-24 · public)
