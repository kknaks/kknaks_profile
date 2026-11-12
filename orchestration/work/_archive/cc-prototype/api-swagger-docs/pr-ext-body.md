## 배경

협업자의 외부 시스템(링키 · 차티)이 상담 중에 시술 · 상품 가격과 기존 고객의 남은 시술권을 보고, 고객 **이름 + 이메일**로 조회 · 예약해야 한다. 지금까지 back 에는 메뉴 API 가 없었고, 고객 검색 · 예약은 직원 로그인 전용이었다. 그래서 협업자에게 admin 계정을 공유해 쓰고 있었다.

결정: DEC-010 · 계약: SPEC-008 0.2.x · 빌드: WORK-012 (profile 레포 `para/projects/summer-star/cc-prototype/`).

## 변경 내용

### 1. KOS 메뉴 전부를 DB 에 저장 (D-03 ~ D-07)

- 표 9개: 카테고리 · 상품 · 옵션 · 구성 · 시술 · 진료항목 · 기기 · 약물 · 타겟 국가(`menu_*`). 칸마다 KOS 원본 JSON(`raw`)도 같이 둔다.
- 마스터 루프(1시간)와 서버 시작 때 KOS 공개 API 8개 작업으로 동기화한다(`app/kos/menu_sync.py`).
  - 작업마다 독립이다. 실패하면 그 표는 이전 값을 유지한다.
  - KOS 에서 사라진 행은 지우지 않고 `present = 0` 으로 둔다.
- SINGLE 옵션의 진료항목 id 는 `getProductOptions` 를 100개씩 나눠 불러 채운다.

### 2. 외부 연동 API `/api/ext/*` — 직원 API 와 분리 (D-10 ~ D-36)

| 경로 | 무엇 |
|---|---|
| `GET /api/ext/menu` | 카테고리 → 상품 → 옵션(정가 · 부가세 별도) → 구성 → 시술(id · 이름). `translsMap` · `syncedAt` |
| `POST /api/ext/customers/lookup` | 이름 + 이메일 → 고객(id · 이름 · 신규 여부 · 최근 방문일) + 남은 시술권(KOS 실시간 · `bundlePrice` = KOS 묶음 가격) |
| `POST /api/ext/reservations` | 이름 + 이메일 + 시작 시각 → 1명이면 그 고객, 0명이면 새 고객을 만들어 예약 · 2명 이상이면 409 |

- **조회 규칙**:
  1. KOS 내부 이름 검색 1페이지(1000)를 받는다. 넘으면 「없음」이다.
  2. KOS id 로 중복을 지운다.
  3. 이름(또는 발음명)이 정확히 같아야 한다(공백 · 대소문자 무시).
  4. 이메일을 trim + 소문자로 바꿔 정확히 맞춘다.
  - 틀린 입력과 없는 고객은 바이트까지 같은 404 다.
- **예약**:
  - 그룹은 env 기본 그룹 하나다. 구역 · 정원은 지금 규칙을 따른다.
  - 기존 `ReservationService.create()` 를 다시 쓴다. 행위자는 `ext:<연동처>` 다. 직원 `event_log.actor` 는 그대로다.
  - 설정 문제(env 빔 · 그룹 없음 · 켜진 구역 0)는 KOS 를 부르기 전에 `503 ext_not_configured` 로 막는다.
- **인증 · 보안**:
  - 연동처별 키를 `X-Api-Key` 헤더로 받는다(`hmac.compare_digest`).
  - 직원 경로는 이 헤더를 보지 않고, 외부 경로는 Bearer 를 보지 않는다.
  - 호출 제한은 키당 60회/60초다. 넘으면 `429` 다.
  - 키 없는 오류 응답에는 IP 제한을 둔다.
  - 모든 `/api/ext` 응답에 `Cache-Control: no-store` 를 단다.
- **기록**: `ext_call` 에 연동처 · 경로 틀 · 상태 · 결과만 남긴다. 이름 · 이메일 · 키 · IP 원문은 0 이다. 키 없는 거절은 같은 IP · 같은 결과면 1분에 1줄만 남긴다.

### 3. Swagger

- tag 「외부 연동」 · securityScheme `ExtApiKey`(Authorize 에 키 입력).
- 세 operation 의 summary · 설명 · 오류 표를 전부 달았다.
- 앱 설명에 「외부 연동 API」 절을 더했다. 첫 줄은 「email 없는 기존 고객은 404」다.
- 직원 API 문서는 차이 0 이다.

## 검증

- `uv run pytest -q`: 544 → **599 passed** · `ruff` 통과(reviewer 가 독립으로 다시 돌림).
- reviewer 1판 WARN 7 → 수정 → 재검수 **PASS**.
  - 이름 검색 응답 모양이 깨지면 502 로 막는다(새 고객 생성 0).
  - 동시 요청에도 카운터가 정확하다.
  - 처리하지 못한 예외는 `500 internal_error` + 기록 1줄로 남긴다.
- **데모 KOS 실물(로컬 compose)**:
  - 메뉴 200(카테고리 15 · 상품 101 · 옵션 323) · 키 없음 / 직원 토큰 401.
  - 데모 고객 3명 조회 200 · 틀린 이메일 404 · 한 글자 이름 404.
  - 기존 고객 예약 200 · 새 고객 예약 200 → 같은 이름 + 이메일로 조회 200(신규).
  - 두 예약 모두 취소했다.
  - 61번째 호출부터 429 · `ext_call` · `event_log` 행위자 `ext:linky` 확인.

## ⚠ 배포 주의

- **새 env 3개는 클러스터 Secret `cc-prototype-secret` 에 넣는다**: `PROC_EXT_KEY_LINKY` · `PROC_EXT_KEY_CHARTY` · `KOS_EXT_RESERVATION_GROUP_ID`. 비어 있으면 그 연동처는 401, 예약은 503 이다. 메뉴 · 조회는 그대로다.
- 새 표는 부팅 때 `CREATE TABLE IF NOT EXISTS` 로 만든다(같은 SQLite · PVC). 마이그레이션 없음.
- back 만 바뀐다 → `back.imageTag` 만 올린다.

## 리뷰 포커스

1. **예약이 이메일 존재를 드러냄**(D-35 수용): 0명 갈래에서 KOS 중복 검사에 걸리면 409, 아니면 200 이다. 키를 가진 연동처만 부를 수 있고, 호출 제한 · 기록이 있다. Swagger 에 적어 두었다.
2. **KOS 내부 API 의존**(D-15): 이름 검색이 내부 `get-visitors` 를 쓴다. 조건이 바뀌면 조회 · 예약이 502 로 멈춘다(지금 직원 검색과 같은 위험).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
