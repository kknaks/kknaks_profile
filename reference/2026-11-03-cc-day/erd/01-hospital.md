# 01 브랜드 · 병원 · 외부 CRM 연결

2026-11-03 사용자와 정함. 공통 규칙은 [README.md](README.md) 「모든 테이블에 공통」.

## 왜 필요한가

- 한 DAY 서버가 **여러 병원**을 받는다(사용자 2026-11-03). 그래서 병원 테이블이 있고 업무 테이블마다 `hospital_id` 가 붙는다.
  cc-prototype 은 지점 하나(명동)를 가정해 병원 테이블이 없었다.
- 병원마다 붙는 외부 CRM 이 다를 수 있다(KOS · 나중에 Vegas). 어느 업체에 어떤 값으로 붙는지를 병원별로 둔다.
- 같은 브랜드에 지점이 여러 개일 수 있고, **브랜드 입장에서는 소속 지점 전체 데이터를 조회해야 한다**(사용자 2026-11-03). 그래서 병원 위에 브랜드를 둔다.
- **각 병원은 독립 운영 주체다. 본사(브랜드)가 하는 일은 데이터 조회뿐이다**(사용자 2026-11-03). 데이터의 주인은 병원이고, 브랜드는 묶어서 읽기만 한다.
- 모양은 centurion 을 따른다 — 병원 = `sso` `organizations`, 연결 = `crm` `connections`(키가 들어가 따로 암호화).

## `brand` — 브랜드

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `id` | uuid PK | ✓ | |
| `code` | varchar(50) UNIQUE | ✓ | 영문 식별자 — 예: `ceramique` · `vellicell` · `daybeau`(v0.1 의 브랜드 코드) |
| `name` | varchar(100) | ✓ | 예: 세라미크 |
| `is_active` | bool | ✓ | |
| `deleted_at` | timestamptz | | 소프트 딜리트 |
| `created_at` · `updated_at` | timestamptz | ✓ | |

## `hospital` — 병원(지점)

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `id` | uuid PK | ✓ | 모든 업무 테이블이 가리킨다 |
| `brand_id` | uuid FK → `brand.id` | ✓ | 소속 브랜드. 지점이 하나뿐인 브랜드도 브랜드 행을 둔다 |
| `name` | varchar(100) | ✓ | 예: 세라미크의원 명동점 |
| `is_active` | bool | ✓ | 운영 여부. 끊긴 병원은 지우지 않고 끈다 |
| `deleted_at` | timestamptz | | 소프트 딜리트 |
| `created_at` · `updated_at` | timestamptz | ✓ | |

## `crm_connection` — 병원별 외부 CRM 연결

병원 하나에 연결 하나(0..1). 연결이 없으면 그 병원은 동기화하지 않는다.

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `hospital_id` | uuid PK · FK → `hospital.id` | ✓ | |
| `vendor` | enum `kos` · `vegas` | ✓ | 어느 업체인지 |
| `is_demo` | bool | ✓ | 데모 테넌트 연결인지 |
| `config` | 암호화 JSONB | ✓ | 업체별 접속값 — 아래 |
| `connected_at` · `updated_at` | timestamptz | ✓ | |
| `deleted_at` | timestamptz | | 소프트 딜리트 — 연결을 끊어도 행은 남긴다 |

### `config` — 업체별 접속값 (암호화)

나중에 화면의 「CRM 설정」에서 넣는 값이다(사용자 2026-11-03). 업체마다 필요한 값이 달라 JSON 하나로 둔다.
centurion `crm.connections.config` 처럼 민감 키는 **최상위**에 둔다(한 겹 감싸면 암호화되지 않는다).

| 업체 | 키 | 무엇 | cc-prototype 이름 |
|---|---|---|---|
| KOS | `open_api_key` | 공개 API 키 — 토큰 받기 | `KOS_OPEN_API_KEY` |
| KOS | `tenant_id` | KOS 테넌트(병원) id — 내부 API 경로 · 웹 링크 | `KOS_TENANT_ID` |
| KOS | `system_email` | 내부 API 로그인 계정 | `KOS_SYSTEM_EMAIL` |
| KOS | `system_password` | 내부 API 로그인 비밀번호 | `KOS_SYSTEM_PASSWORD` |
| Vegas | — | 정할 것 | — |

## 테이블에 두지 않는 것

| cc-prototype 설정 | 어디로 | 이유 |
|---|---|---|
| `KOS_OPEN_API_BASE` · `KOS_INTERNAL_API_BASE` · `KOS_WEB_BASE` | 서버 env (업체 설정) | 업체가 정한 주소라 병원마다 다르지 않다 |
| `KOS_POLL_SCHEDULE_SEC` · `KOS_POLL_MASTER_SEC` · `KOS_RESV_CACHE_SEC` | 서버 env | 모든 병원에 같은 동작값 |
| `KOS_ZONE_ID` (기본 구역) | 뺀다 | PoC 에서 「이 화면은 4층만」 고정값이었다. 구역은 KOS 데이터 — 6번 주제 |
| `KOS_EXCLUDE_ACCOUNT_IDS` | 4번 직원 주제 | 원장 목록에서 뺄 계정 = 직원 데이터의 표시 |
| `KOS_ROOM_TASK_ID` | 5 · 6번 주제 | 「방 배정」 기타 작업 = KOS 기타 작업 종류 데이터 |
| `CCC_*_KOS_ACCOUNT_ID` | 4번 직원 주제 | 계정 ↔ KOS 직원 연결 |

## 환경 — 데모 테넌트와 DAY 서버

2026-11-03 조회로 확인(토큰 받기 · `getZones` 만):

| 키 | `open-api.kos-solution.com` | `open-api.kos-solution.dev` | 구역 |
|---|---|---|---|
| 데모 지점 키 | 200 · 토큰 받음 | 400 | `4층` · `미사용` |
| 명동점 키 | 200 · 토큰 받음 | 400 | `4층` |

- **데모 계정도 KOS 운영 호스트에 있고, 테넌트만 데모다.** KOS dev 호스트는 두 키 모두 받지 않는다.
  그래서 연결에 KOS 환경(dev · prod) 칸을 두지 않는다 — KOS 호스트는 운영 고정(서버 env). 가를 것은 `is_demo` 다.
- **DAY 서버 dev · prod 구분은 서버 env 로 한다**(사용자 2026-11-03) — `APP_ENV`(`dev` · `prod`), centurion `deploy/config/<env>.env` 의
  `APP_ENV` 와 같은 이름. `APP_ENV=dev` 인 서버는 `is_demo = true` 연결만 동기화한다 — 개발 중에 실제 병원 데이터를
  건드리지 않게 하는 장치. 테이블에는 서버 환경 칸을 두지 않는다.

## 정할 것

1. **Vegas** 접속값 — Vegas 를 붙일 때 확인한다(사용자 2026-11-03).

`hospital` 의 `phone` · `address` 는 두지 않는다(사용자 2026-11-03 — 필요 없음).

## 다음 주제로 넘긴 것

- **브랜드 전체 조회의 권한** — 브랜드 단위로 보는 사람(계정)을 어떻게 표시할지는 4번 직원 / 계정에서 정한다.
- ~~브랜드 안 같은 고객~~ → 2번에서 정함: 병원별 고객 1명, 묶지 않는다.
