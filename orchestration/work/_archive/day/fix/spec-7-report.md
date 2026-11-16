# fix-spec-7 결과 보고 — 파일 저장소(Blob) 구조 · 채팅 첨부 관리 ID 연결 · WP-BE-4 · Delivery #241 v3

## 상태: done

- 사용자 정정(용도 폴더 **셋** — `correction-storage-1.md`) 반영함: `chat`(씀) · `identity` · `before-after`(이름만 예약 · 이름 = 코디 기본값).
- 안내문의 값(계정 이름 · 주소 · 컨테이너 이름 · 리소스 그룹 · 구독 · VM 이름 · 로그인 계정)은 스펙 · 계획 · 리포트 · Delivery 어디에도 옮기지 않았다(grep 확인). env **이름**과 구조만.
- 스펙 커밋 · push · PR 0 · 코드 수정 0.

## 구조를 어느 문서에 · 왜

**`40-architecture/deployment.md` 새 절 「파일 저장소(Blob) — 구조 · 인증 · 규칙」(`:177`) 한 곳.** 채팅만의 것이 아니라 DAY 파일 저장 전체(채팅 · 신분증 · 전후 사진 · dev/prod)의 규칙이고, 이미 deployment.md 가 Blob 준비 행 · env 표 · Key Vault 를 갖고 있어서다. SPEC-004 는 그 절을 가리키고 채팅이 쓰는 것(용도 `chat` · 키 모양 · 실패 동작)만 적는다. system.md 「Azure Blob」 줄은 그 절로 링크만. 같은 규칙을 두 곳에 적지 않았다.

## 바꾼 문서 · 절 (고친 뒤 줄)

| 문서 | 자리 |
|---|---|
| `40-architecture/deployment.md` | 머리 2026-11-11 줄 `:19` · env 표 `:170`(`DAY_BLOB_ACCOUNT_URL` · `DAY_BLOB_CONTAINER` 새) · `:171`(`DAY_CHAT_STORAGE`) · `:172`(옛 두 칸 없앰 취소선) · **새 절 `:177`** · 용도 폴더 표 `:197` · Key Vault `:214`(필수 6 + **선택 2**) · Blob 준비 행 `:222`(준비됨 · 확인된 것 / 아직) · 미결 3줄 `:238-240` |
| `20-spec/spec-004-internal-chat.md` | 머리 개정 ⑤ `:32` · 오류 표 `photo_disabled` 409 · 503 `:406` · §3 첨부 「저장소」 `:416` · 「키」 `:417` · 「저장소 꺼짐」 `:424` · 새 「저장소 접근 실패」 `:425` · 케이스 매트릭스 `:479` · 프로토와 다른 곳 `:564` · 서버 의존 C-3 `:578` · 새 C-A26 `:612` · C-A27 `:613` |
| `20-spec/spec-000-data-model.md` | 머리 개정 ③ `:31` · `id_photo.file_key` `:1089`(`identity` 예약) · `chat_attachment.file_key` `:1161` |
| `40-architecture/system.md` | `:66` Azure Blob 줄(용도 셋 · 링크) · `last_updated` |
| `log.md` | 7판 1줄 |

## 설정 계약

| | 칸 | 비고 |
|---|---|---|
| **더함** | `DAY_BLOB_ACCOUNT_URL` · `DAY_BLOB_CONTAINER` | 일반 설정(비밀 아님) · DAY 파일 저장소 공통(용도 무관) · dev · prod 같은 값 |
| **그대로** | `DAY_CHAT_STORAGE`(`disk` · `blob`) · `DAY_CHAT_STORAGE_DIR` | 채팅 첨부 스위치 · 로컬 = `disk` |
| **없앰** | `DAY_CHAT_BLOB_CONTAINER` · `DAY_CHAT_BLOB_CONNECTION_STRING` · Key Vault 선택 비밀 `day-<env>-chat-blob-connection-string` | 저장소가 연결 문자열 · 키를 받지 않음 → 선택 비밀 = APNs · Soniox 둘 |
| 인증 | VM 시스템 할당 관리 ID 만(다른 자격 증명으로 넘어가지 않게 — 기술 기본값) | 새 의존성 `azure-identity` |
| 로컬 | 디스크 그대로 · 로컬 Blob 길 **두지 않음**(planner 기본값) | |
| 꺼짐 | fail-closed 그대로(칸 빔 = 409 `photo_disabled`) | |

env 이름 `DAY_BLOB_*` 는 저장소가 용도 셋 공통이라 `CHAT` 을 뺀 이름으로 정했다(planner 기본값 · 기존 `DAY_…` 규칙).

## 실패 동작

| 상황 | 서버 | 앱(지금 코드 그대로 · 새 글자 0) |
|---|---|---|
| 설정 없음(꺼짐) | 409 `photo_disabled`(지금 그대로) | 올리기 = 토스트 「사진 저장이 꺼져 있어요」 |
| 관리 ID 토큰 못 받음 · 권한 없음 403 · 컨테이너 없음 · 시간 초과(연결 20초 / 읽기 60초) · 그 밖 저장소 오류 | **503 `photo_disabled`**(같은 글자) · 쓰던 파일 지우기 시도 · 로그 = 원인 종류 · 키 앞자리 | 올리기 = 「보내지 못했어요」 + [다시 보내기](5xx 갈래 — `chat_state.dart` `SendState.failed`) · 열기 = 그 사진 그리지 않음(`_load` null) · 전달 = 시트 남김 + 「보내지 못했어요」 |
| 기동 | **막지 않음**(자격 증명 · 클라이언트는 처음 쓸 때) — 지금 fail-closed(기능만 꺼짐)와 같은 방향 · 저장소 장애가 로그인 · 시술현황 · 채팅 글을 막지 않게 | — |

시간 상한 = `azure-storage-blob` 12.31 기본값(`CONNECTION_TIMEOUT = 20` · `READ_TIMEOUT = 60` — 코드에서 확인)을 명시적으로 넘김(기술 기본값) · 토큰 받기 시간은 구현 때 확인 · 저장소 전용 동시 상한 없음(요청당 하나 · api worker 1).

## 경로 바뀜의 파급

- 키 = `{APP_ENV}/chat/{병원 id}/{32 hex}.{jpg|mp4}` · `check_key` = 모양 + 키 환경 = 자기 `APP_ENV`(아니면 404 처럼 — 실수 방지 · 권한 경계 아님).
- 이미 저장된 키: dev 는 저장소가 꺼져 있어 첨부 행 없음 · prod 없음 · **로컬 디스크 옛 `chat/…` 키만** — 읽지 않음 · 옮기지 않음(planner 기본값 · 로컬 시험 데이터).
- DB 칸(SPEC-000 `file_key` · `thumb_file_key` varchar) 변경 · migration 없음.

## 정할 것 (사용자 몫 · 후보 · 추천)

1. **용도 폴더 이름** `identity` · `before-after`(코디 기본값) — 다른 이름? 이름만 예약이라 지금 바꿔도 비용 없음. 추천 = 그대로.
2. **dev ↔ prod 차단** — (가) 지금대로(같은 컨테이너 · 폴더만 · dev 가 prod 를 읽을 수 있음) (나) 환경별 컨테이너 · 권한 분리를 인프라에 요청. 추천 = **prod 에 고객 신분증 · 전후 사진이 들어가기 전에 (나)**.
3. **보관 · 복구** — (가) 지금대로(자동 삭제 · soft delete · 버전 꺼짐) (나) soft delete 기간 켜기. 추천 = 채팅은 지금대로 · 고객 사진 기능 때 보관 기간과 함께(DAY-ESC-001).

(deployment.md 미결 `:238-240` 에 같은 셋.)

## `wp-plan.md` — WP-BE-4

- 나눔 표에 한 줄 · 새 절 「WP-BE-4 파일 저장소 — 관리 ID · 환경 경로 (7판)」 · 순서 줄 · 실기기 확인 11번.
- 고칠 파일(grep — `from_connection_string` · `day_chat_blob` · `DAY_CHAT_BLOB` · `chat-blob` · `new_key` · `check_key` · `KEY_PATTERN` 쓰는 곳 전부): `chat_storage.py` · `chat.py`(올리기 · 열기 · 전달 503) · `errors.py` · `common/config.py` · `scripts/deploy/day_vm.py` · `deploy/config/dev.env` · `prod.env`(값은 사람) · `deploy/compose.local.yaml` · `deploy/local.env.example` · `pyproject.toml` · `uv.lock` · `docs/development/deployment.md` · 시험 `test_chat_units.py` · `test_chat_attachments.py` · `conftest.py` · `test_chat_env_contract.py` · `test_day_vm.py` · `test_config.py`. 확인만: `deploy/compose.yaml` · `Dockerfile`.
- 하지 말 것: 값 쓰기 · 연결 문자열 · `DefaultAzureCredential` · 로컬 Blob · `identity` · `before-after` 쓰는 코드 · 옛 키 옮기기 · 새 code · 글자 · 앱 수정 · 기동 막기 · 저장소 · Key Vault 설정 변경.
- 실물: 코디(dev 설정 값 · 배포) · 워커/코디(dev api 컨테이너에서 관리 ID 올리기 → 읽기 → 지우기 · 경로 확인) · 사용자(TestFlight 사진 · 동영상).

**앱 변경: 없음** — 올리기 · 열기 경로 · 응답 모양 그대로 · 409 = 토스트 · 5xx = 실패 말풍선 + 다시 보내기 · 열기 실패 = 안 그림이 이미 코드에 있다(`app/lib/chat/chat_state.dart` 보내기 `on ApiError` · `_load`).

## Delivery #241

| 항목 | 값 |
|---|---|
| contract_version | **3**(scope delta 기록) |
| risk | L3 그대로 |
| contract_digest | `sha256:f9ba9ef920d53fdcdaf7db95d4ad318be4ed47ed75ddb76c03e215759947bef9` |
| plan_digest | `sha256:dd76aa1d2a1798cefd27d214c7eb48f1a30d98994601c31d2316e1584c6b87df`(v2 승인 stale) |
| 라벨 | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:pending` |
| 승인 | **적용함**(`human` · `kknaksss` · 사용자 「이번에 같이 가야」) — 더한 것 = 파일 저장소 연결뿐(Target Delta 1 · Acceptance A12 ~ A14 · Non-Goals 1 · Review Surface 1 · Execution) · 등급 · 조건 변화 없음 |
| next_action | `prepare-spec-baseline` |

- 주의: 첫 `--apply` 를 셸 변수로 부를 때 zsh 단어 나눔 문제로 명령이 실행되지 않았다(exit 127 · 아무것도 안 바뀜 — #241 이 v2 그대로인 것 확인) → 같은 명령을 다시 실행해 적용.
- request: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-fix-spec/61d7eb92-2114-46d5-8714-6da5e5f849de/scratchpad/delivery/fix.v3.request.json`(+ `fix.v3.*.json`)

## 검증

`python3 scripts/lint-pipeline.py --strict` → exit 0 · 0 error, 263 warning · `products/day/` 줄 0.
