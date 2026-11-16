# fix — dev 서버 설정(앱 로그인 공개 주소 · APNs · 채팅 첨부) 결과 보고

## 상태: done (A · D) / blocked (B · C — Key Vault 방화벽 · Storage 읽기 권한)

## 수행 — 변경 파일

- `deploy/config/dev.env` — A 표 네 칸 · 주석 세 곳
- `backend/tests/deploy/test_chat_env_contract.py` — 「서버 채팅 칸은 비어야 한다」를 새 계약으로 고침(아래 D)
- `app/` 은 건드리지 않음(mobile 워커의 미커밋 변경 그대로 · `git status` 로 분리 확인)

### A. `deploy/config/dev.env`

| 키 | 결과 |
|---|---|
| `DAY_PUBLIC_API_BASE` | 설정됨(dev 공개 주소 · `normalize_origin` 통과) |
| `DAY_APNS_KEY_ID` | 설정됨(로컬 자격 파일에서 스크립트로 넣음 · 화면 출력 없음) |
| `DAY_APNS_TEAM_ID` | 설정됨(같음) |
| `DAY_APNS_ALLOWED_APP_IDS` | 설정됨(dev 개발 앱 번들 하나 · 정식 번들 없음) |
| `DAY_CHAT_STORAGE` | 비움 — C 미완 |
| `DAY_CHAT_BLOB_CONTAINER` | 비움 — C 미완 |
| `DAY_DEMO_LOGIN_EMAILS` · `DAY_DEMO_API_BASE` | 비움 유지(prod 만 읽음) |

주석: 「사용자가 직접 넣는다」→ 사용자 승인 날짜로, 「배포 연결은 후속」→ Key Vault 선택 비밀 두 이름이 배포에서 app.env 로 실린다는 사실로(배포 연결은 `day_vm.py` `OPTIONAL_SECRETS` 에 이미 있음), 첨부 저장소 미정 · dev 는 개발 앱만이라는 줄 추가. `prod.env` 무변경.

### B. Key Vault `day-dev-apns-auth-key` — **blocked**

- `az` 로그인은 돼 있음. 그러나 Vault 데이터 평면 호출(비밀 목록)이 **`ForbiddenByFirewall`** — Vault 방화벽이 VM 서브넷만 허용하고 로컬 출구 IP 는 막힌다(배포 문서 「로컬에서 비밀을 넣을 땐 잠깐 IP 허용 또는 VM 에서」와 일치).
- IP 허용은 네트워크 변경이라 브리프상 금지 → 존재 확인 · 쓰기 모두 하지 않음.
- 형식 확인(코드): Key Vault 에 .p8 PEM 을 **여러 줄 그대로** 넣으면 된다. `day_vm.py optional_app_env` 가 `MULTILINE_SECRETS` 의 줄바꿈을 `\n` 두 글자로 바꿔 한 줄 app.env 에 싣고, `apns.py:52` 가 `\\n` → 줄바꿈으로 되돌린다. `az keyvault secret set --vault-name <vault> --name day-dev-apns-auth-key --file <p8 경로>` 로 파일에서 곧바로 넣으면 형식이 맞는다.
- 배포 경로: `dev` push → 워크플로가 run-command 로 VM 에서 `day_vm.py materialize` → VM managed identity(IMDS)로 Vault 를 읽는다. 선택 비밀은 없으면 빠지고(fail-closed) 배포는 계속된다.

### C. 채팅 첨부 Blob — **blocked(조사 불가) · 만들지 않음**

- 리소스 그룹 Storage 계정 목록: 사용자 계정에 `Microsoft.Storage/storageAccounts/read` 권한이 없어 `AuthorizationFailed`.
- `day-dev-chat-blob-connection-string` 존재 여부: B 와 같은 방화벽으로 확인 불가.
- 배포 문서(`deployment.md`) 「사용자가 Azure 에서 준비할 것」의 Blob 행 = 「신분증 사진 · 채팅 첨부 · **구현 뒤**」 · 환경 표 「Blob 접속값 · APNs 키 — 구현 뒤 이름 확정」. 준비됐다는 기록 없음 → 없을 가능성이 높다.
- `dev.env` 채팅 두 칸은 비워 둠 → dev 에서 첨부는 계속 409 `photo_disabled`(메시지 · 푸시는 무관).

## 검증 — 명령과 수치

- `cd backend && uv run pytest -q tests/deploy` → **96 passed**(처음 1 failed: 기존 시험이 서버 채팅 칸 = 빈 값을 단정 → 계약에 맞게 고친 뒤 통과)
- `uv run ruff check tests/deploy/test_chat_env_contract.py` → All checks passed · `ruff format --check` → already formatted
- `day_vm.py materialize --environment dev --dry-run`(서버 · Vault 접속 없음, 자리 sha · ACR digest 모양 이미지) → **exit 0** · 일반 설정 검사 통과 · app.env 에 선택 비밀 두 이름이 `<key-vault-optional:…>` 로 실릴 자리 확인
- `git status --short` → 내 변경 2 파일 · `app/` 은 mobile 변경 그대로

### D. 시험 계약 변경 내용

- 기존: dev · prod 모두 채팅/APNs 이름 칸 = `""` 단정.
- 지금: (dev · prod 공통) 칸은 있고 · 비밀 키는 없고 · 저장소는 `""`/`blob` 만 · 저장소와 컨테이너는 같이 차거나 같이 빔 · Key/Team ID 는 빈 값 또는 10자 대문자영숫자(값은 실패 메시지에 싣지 않음).
  (prod) 모든 칸 `""` 유지. (dev) 허용 앱 = 개발 앱 하나 · Key/Team ID 함께 · `DAY_PUBLIC_API_BASE` 정규화 = dev 공개 주소 · 데모 두 칸 빈 값.
- 「dev 서버 + 공개 주소 → 앱 로그인 응답 `api_base_url` · `environment=dev`」 시험은 **이미 있다**: `backend/tests/day/auth/test_environments_api.py::test_앱_로그인_응답에_자기_환경과_공개_주소_웹은_없음`(+ 비면 칸 없음 · 병원 고르기 응답도 확인).

## 배포 뒤 확인할 것(dev 머지 → 워크플로 배포 후, 사용자와)

1. TestFlight DAY Dev 앱 로그인 → `environment_unavailable` 사라짐(응답에 `api_base_url` · `environment=dev`).
2. 기기 등록 200(허용 목록 통과). APNs 키를 Vault 에 넣기 전까지 채팅 푸시는 `push_log.status = skipped_no_key`.
3. B 완료 뒤 재배포(키는 배포 때 읽힘) → 실기기 채팅 푸시 수신. push_env(sandbox/production)는 기기 등록 값 기준 — TestFlight 는 production.
4. 첨부는 C 완료 전까지 409 `photo_disabled` 가 정상.

## 정할 것(사용자)

- **B**: APNs 키 넣을 경로 — (a) Vault 방화벽에 사용자 IP 를 잠깐 허용하고 로컬에서 `--file` 로 넣은 뒤 허용 제거, 또는 (b) VM 에서 넣기(VM identity 는 Secrets User 라 쓰기 불가 → 사용자 계정 로그인 필요). 넣은 뒤 dev 재배포가 있어야 반영.
- **C**: Blob 저장소를 새로 만들지 — 정할 값: Storage 계정 이름(전역 고유 · 소문자 3–24) · 지역(나머지와 같은 koreacentral 권장) · 이중화(LRS 로 충분) · **공개 접근 끔**(앱은 서버 경유로만 읽음 · 익명 blob 읽기 금지) · 네트워크(VM 서브넷만 허용 여부) · 컨테이너 이름(dev/prod 분리: 예 `day-dev-chat` · `day-prod-chat` 또는 계정 분리) · 수명 규칙(첨부 보존 기간 · 삭제 정책 — SPEC-004 확인) · 비용(LRS Hot 저용량이면 월 수천 원 수준 · 트랜잭션 소량). 그 뒤 연결 문자열을 `day-dev-chat-blob-connection-string` 에 넣고 `dev.env` 두 칸(`blob` · 컨테이너)을 채운다. 연결 문자열 대신 managed identity 는 현 코드(`BlobClient.from_connection_string`)가 받지 않는다.
- 사용자 계정에 Storage 읽기 권한이 없다 — C 조사를 다시 하려면 리소스 그룹 Reader 이상 필요.

## pending

- B · C (위 「정할 것」 결정 뒤). 커밋 · push · PR 은 하지 않음(코디 몫).
