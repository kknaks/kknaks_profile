# 코드 검수 — WORK-011 BE-1 (커밋 `78f014f`) (2026-10-06)

## 판정: WARN

규율 위반(FAIL)은 없다. 계약 핵심은 코드와 시험 양쪽에 다 서 있다.
- 소프트 딜리트
- 연동 범위 중복 키
- 남의 것 404
- Fernet 암호화
- 일회용 `state`(해시·10분·회원·종류)
- 기기 토큰(Bearer 전용·해시·범위·철회)
- NOTIFY 계약
- manual SQL ↔ 모델 일치(시험이 강제)
- 운영 인벤토리 갱신

다만 **운영 반영 전에 반드시 닫을 것 하나(W-1)** 와 보안상 고칠 것 둘(W-2·W-3)이 있다. BE-2·BE-3 이 나란히 가려면 갈라야 할 파일 하나(W-6)도 남았다.

> 검수 방법: 같은 워크트리에서 BE-2·BE-3 이 작업 중이라 **`git show 78f014f:…` · `git diff 78f014f~1 78f014f` 로만** 읽었다(작업 트리 안 봄). 시험·빌드는 돌리지 않았다(역할 규칙). 27 파일 +3084/−6.
> 기준: SPEC-008 v0.5.x §4.1·§4.2·§4.3·§4.6(handshake·reset-account)·§5 · WORK-011 Phase BE-1 · 4차 검수(`review-spec-work-r4.md`) ★1·★2·W4-3·W4-7.
> 경로 약칭: `B/` = `backend/src/ax_workspace/` · `T/` = `backend/tests/` · CHART = `/Users/kknaks/git/harness_works/k8s_infra_mac/charts/strong-hajin`

## 항목별 판정

| # | 항목 | 판정 | 근거 파일:줄(커밋 78f014f) | 비고 |
|---|---|---|---|---|
| 1 | 스키마 — 소프트 딜리트 | PASS | `B/platform/persistence.py` `ExternalIntegrationRecord.removed_at`·`ExternalRoomRecord.removed_at` · `B/modules/external_channels/application.py` `disconnect`·`remove_room`·`kakao_reset_account`(전부 `removed_at` 만 찍음 · 행 삭제 없음) · 되살림 `_store_grant`·`add_rooms` | 시험 `T/contract/test_external_channels.py:207`·`:244` |
| 2 | 스키마 — 사람마다 복제 · 카톡 키 연동 범위 | PASS | `uq_external_integrations_member_account(member_id, kind, account_key)` · `uq_external_rooms_integration_external(integration_id, external_id)` · `uq_external_messages_dedup(integration_id, container_key, external_key)` — 키가 전부 연동 범위 · `domain.py` `kakao_attachment_aid` = `SHA-256("{integration_id}:{chatId}:{logId}:{seq}")` | 시험 `T/unit/test_external_channel_rules.py:31` |
| 3 | 소유 검사 — 남의 것 404 | PASS | `B/platform/external_channels.py` 조회가 전부 `member_id` 조건 · `application.py` `_owned` → `IntegrationMissing(ResourceNotFound)` → 404 | 시험 `:231`·`:244`·`:334`·`:386` |
| 4 | 토큰 암호화(Fernet · 키 없으면) | PASS(경미 W-4) | `B/platform/external_tokens.py` · `B/bootstrap/application.py` `_make_external_cipher` — 키 있으면 Fernet · **운영에서 키 없으면 `None` → `IntegrationNotConfigured` → 503 `integration_not_configured`** · 개발은 `.scax/external-token.key`(0600 · 원자적 생성 · `.gitignore:14`) | 시험 `:128` · unit `:82`·`:93` |
| 5 | OAuth `state` — 일회용·만료·회원·CSRF | **WARN(W-2)** | `application.py` `_issue_state`(32바이트 · 해시만 · 10분) · `complete_callback`(잠금 조회 · 종류 일치 · 미사용 · 미만료 · **결과와 무관하게 소비**) · `bootstrap/application.py` `complete_integration_callback`(예외여도 commit — 실패한 state 재사용 불가) | 일회용·만료·회원 묶기는 됐다. **브라우저에 묶이지 않는다** → W-2 |
| 6 | 기기 토큰 — Bearer 전용·해시·범위·웹 거절·철회 | PASS | `B/entrypoints/http_auth.py` `device_principal`(Bearer 만 · 쿠키·페르소나 안 봄) · `current_principal` 은 Bearer 를 안 봄 · `application.py` `issue_device_token`(옛 토큰 철회 · `axdt_` 머리 · 해시만) · `device_token_principal`(**회원이 지금 활동 중일 때만**) · `revoke_member_device_tokens`(BE-3 비번 API 용) · 라우트 `http.py` handshake = `device_principal` · reset-account = 세션(★2 반영) | 시험 `:297`·`:320`(웹 라우트·reset-account 에 Bearer=401 · handshake 에 세션=401)·`:334` |
| 7 | 비밀값이 로그·repr·시험에 새나 | **WARN(W-3)** | `Settings` 비밀 칸 `repr=False`(시험 unit `:101`) · `external_oauth.py` 로그는 상류 host·오류 코드만 · 응답 `Cache-Control: no-store`·`Referrer-Policy: no-referrer` | `OAuthGrant` 데이터클래스 repr 에 토큰이 찍힌다 → W-3 |
| 8 | NOTIFY 계약 | PASS(경미 W-9) | `B/modules/external_channels/events.py`(채널 둘 · 판 번호 · `member_id` = 받는 사람 · 본문 안 실음 · `from_payload` 가 모르는 판 버림) · `B/platform/user_events.py`(같은 트랜잭션 `pg_notify` · PG 아니면 무동작) | 4차 W4-3 ③ 반영. PG 경로 시험 없음 → W-9 |
| 9 | 모듈 분할 → BE-2 ∥ BE-3 | **WARN(W-6)** | `__init__.py` 소유 표 · `sync.py`(BE-2)·`inbox.py`·`kakao_ingest.py`(BE-3) 빈 자리 · 동기화 상태 칸을 BE-1 이 다 놓음 · 시험 `T/architecture/test_external_channel_schema.py:42` | 모듈은 갈랐다. **저장소(`platform/`) 파일은 하나뿐**이다 → W-6 |
| 10 | manual SQL ↔ schema_sync 일치 | PASS | `backend/migrations/manual/2026-10-06-external-channels.sql`(표 아홉 · `IF NOT EXISTS` · 머리에 「이미지보다 먼저」 ★4) · 시험 `test_external_channel_schema.py:27` 이 **모델 컴파일 결과가 SQL 안에 있음**을 표·인덱스마다 확인 + 새 `external_*` 표 누락 검사 · `local-stack` 표지에 `external_integrations` 추가(`T/architecture/test_local_stack_targets.py`) | — |
| 11 | 시험이 계약을 덮나 | PASS(빈칸 W-9) | contract 17개(state 위조·재사용·만료·교차 · 가짜 code 가 state 를 태움 · 동의 거부 · 암호화 저장 · 메일 여럿·되살림 · 슬랙 하나 · 남의 것 404 · 방 저장·되살림·빼기 · 기기 토큰 범위·철회·대체 · 첫 handshake·chatId·reset-account) · unit 8개 · 인벤토리 json(+275) | 빠진 것은 W-9 |
| 12 | 4차 검수 BE-1 항목 | PASS | ★1 handshake `external_id` · ★2 reset-account 세션 · W4-3 동기화 칸·NOTIFY·모듈 분할 · W4-7 `AX_WEB_ORIGIN`(local-stack)·인벤토리·첫 handshake 생성·`selected_rooms_version`·기기 토큰 일괄 철회 함수 | 전부 반영 |

## 경미 (WARN) — 고칠 것

| # | 근거 파일:줄 | 무엇 | 고칠 것 (한 줄) |
|---|---|---|---|
| **W-1** ★운영 전 필수 | `B/bootstrap/settings.py` `web_origin` 기본 `http://localhost:5173`(`from_environment` `AX_WEB_ORIGIN`) · `api_origin = api_origin or web_origin`(`__post_init__`) · `application.py` `redirect_uri()`·`settings_return_url` / CHART `templates/configmap.yaml`(**`AX_WEB_ORIGIN` 이 없고 `PUBLIC_ORIGIN` 만** 있음 · 백엔드는 `PUBLIC_ORIGIN` 을 읽지 않음 — `git grep PUBLIC_ORIGIN 78f014f -- backend` 결과 0) | 운영 pod 에서 `redirect_uri` 가 **`http://localhost:5173/api/integrations/mail/callback`** 이 되고, 콜백 뒤 302 도 localhost 로 간다. 운영 Gmail·슬랙 연결이 `redirect_uri_mismatch` 로 전부 실패한다 | INFRA Phase 에 configmap `AX_WEB_ORIGIN: https://ax.medisolveai.xyz` 를 넣는다. 코드에도 「`PRODUCTION` 인데 OAuth 가 설정됐고 origin 이 https 가 아니면 부팅 거절」 한 줄을 둔다 |
| **W-2** 보안 | `application.py` `complete_callback`(회원 = `state` 의 회원 · 브라우저 확인 없음) | `state` 가 **브라우저에 묶이지 않아** 링크를 넘기는 공격이 가능하다. 공격자가 자기 계정으로 `connect` → 받은 `authorize_url` 을 동료에게 보냄 → 동료가 10분 안에 동의하면 **동료의 Gmail 이 공격자의 연동으로 들어온다**. 데스크톱(OS 브라우저 · 쿠키 없음)을 살리려고 SPEC-008 §4.2(F-2)가 고른 구조의 대가다. r1 F-2 의 권고 문장이 이것을 따지지 않았다(리뷰어 몫) | 콜백 요청에 **유효한 세션 쿠키가 있고 그 회원이 `state` 의 회원과 다르면 거절**한다(웹 흐름은 막히고 데스크톱 흐름은 그대로). 동의 화면 문구·설정에 연결된 주소를 크게 보인다. SPEC-008 §4.2 에 한 줄로 받는다 |
| **W-3** 보안 | `application.py` `@dataclass(frozen=True, slots=True) class OAuthGrant` — `access_token`·`refresh_token` 이 기본 repr 에 들어간다 | 예외 추적·디버그 로그가 grant 를 찍으면 평문 토큰이 남는다(모듈 머리 주석 「로그·응답에 싣지 않는다」와 어긋남) | 두 칸을 `field(repr=False)` 로. `Settings` 처럼 repr 시험 한 줄 |
| W-4 | `bootstrap/application.py` `_external_cipher`(처음 쓸 때 만듦) · `external_tokens.py` `FernetTokenCipher.__init__`(잘못된 키 = `ValueError`) · `settings.py` `api_origin`(형식 검사 없음 — `web_origin` 은 검사함) | 운영에서 키 값이 잘못되면 부팅은 멀쩡하고 **연결·수집 요청마다 500** 이 난다. `AX_API_ORIGIN` 은 경로·쿼리가 붙어도 통과한다 | `PRODUCTION` 이면 부팅 때 암호기를 한 번 만들어 잘못된 키로 실패하게 한다. `api_origin` 도 `web_origin` 과 같은 검사를 거친다 |
| W-5 | `application.py` `disconnect`(카톡도 허용) ↔ `kakao_handshake`(`elif row.removed_at is not None:` → **되살림**) | 웹에서 카톡 연동을 「연결 해제」해도 앱의 다음 handshake(30초 안)가 되살린다. 해제가 사실상 효과가 없다(D-27) | 카톡 `disconnect` 는 그 회원의 기기 토큰도 철회한다. 또는 카톡은 422 로 거절하고 「기기 토큰 철회」로 안내한다. 둘 중 하나를 SPEC-008 §2.5 에 맞춘다 |
| **W-6** 배치 | `B/platform/external_channels.py`(저장소 하나 · BE-1 이 씀) · `__init__.py` 소유 표에 `platform/` 은 없음 · `sync.py` 머리 「BE-2 는 이 파일(persistence)을 다시 열지 않는다」 | BE-2(슬랙·Gmail 메시지 저장)와 BE-3(카톡 메시지·첨부 저장 · 메시지함 조회)이 **같은 메시지 upsert·첨부 메타 쓰기**가 필요하다. 그런데 저장소 파일은 `platform/external_channels.py` 하나다 — 둘 다 그 파일을 열게 된다. BE-3 은 `bootstrap/application.py`·`http.py` 도 연다(BE-2 는 안 연다 — 이건 괜찮다) | 코디가 BE-2·BE-3 에 **저장소 파일을 따로** 준다(`platform/external_sync_store.py` · `platform/external_inbox_store.py`). 공유 upsert(중복 키로 버리기)는 한쪽 소유로 정하고, 다른 쪽은 그 함수만 부른다 |
| W-7 | `application.py` `kakao_handshake`(없으면 `add_integration`) · `issue_device_token`(철회 후 추가) | 동시 첫 handshake 둘이면 유니크 위반이 500 으로 난다. 발급을 동시에 두 번 하면 활성 토큰이 둘 남을 수 있다(D-45) | 유니크 위반은 잡아 다시 읽고, 발급은 회원 행을 잠근 뒤 철회·추가 |
| W-8 | `ExternalOAuthStateRecord` — 소비·만료된 행을 지우는 곳 없음 | 해시뿐이라 위험은 없다. 행만 무한히 는다 | 연동 워커(BE-2)의 주기 일에 「만료 1일 지난 state 삭제」 한 줄(물리 삭제 금지 원칙은 회사 데이터 대상이라 해당 없음 — 코디 확인) |
| W-9 | 시험 빈칸 | ① `user_events.publish` 의 PostgreSQL 경로(sqlite 에선 무동작이라 미검증) ② **비활성 회원의 기기 토큰 → 401**(`device_token_principal` 의 `authenticated_principal` 분기) ③ W-5 카톡 해제 의미 | ①은 `@pytest.mark.postgres`(make test-postgres) 하나, ②③은 contract 하나씩 |

## 확인한 것 — 참고

- **local-stack**: `Makefile` 의 스키마 표지에 `external_integrations` 가 더해졌다 → 이 커밋 뒤 **기존 로컬 DB 는 `make sync-demo-schema` 를 돌려야 `local-stack` 이 뜬다**(의도된 동작 · 안내 문구 그대로). 코디 로컬 스택을 쓰는 사람에게 알릴 것
- `api-e2e` 가 `AX_WEB_ORIGIN=127.0.0.1:5176`·`AX_API_ORIGIN=127.0.0.1:8001` 을 넘긴다. `api` 타겟(개발 `--reload`)은 넘기지 않아 기본 `localhost:5173` 이다 — 그 타겟으로 OAuth 를 시험하면 콜백이 어긋난다(경미)
- 카톡 업로드 `POST …/kakao/attachments/{aid}` 는 **BE-3 이 구현할 때** `aid` 만으로 찾으면 안 된다(`ix_external_attachments_aid` 는 유니크가 아님). 기기 토큰 회원의 연동 범위로 찾게 BE-3 발주문에 넣을 것
- 인벤토리 json(+275)·`docs/domain-model.md` 갱신 확인. 경계 시험(`domain`·`application` 에 sqlalchemy 없음) 위반 없음 — `application.py` 는 pydantic·typing 만 씀

## 총평

**WARN.** BE-1 은 계약대로 섰고 시험도 실제로 계약을 덮는다. 다음 Phase 를 막지 않는다. 고칠 것의 순서는 이렇다.
1. **W-6 — BE-2·BE-3 이 저장소 파일에서 부딪치기 전에** 코디가 파일을 가른다.
2. **W-2·W-3** — 짧은 보안 수정. BE-3 과 함께 가도 된다.
3. **W-1** — INFRA Phase 와 운영 반영 전에. 반드시 닫는다.
4. 나머지 — 그 Phase 안에서.
