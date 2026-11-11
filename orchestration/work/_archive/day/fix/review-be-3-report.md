# 리뷰 리포트 — fix 서버 검수 3: WP-BE-4 파일 저장소(관리 ID · 컨테이너로 환경 분리) / code (2026-11-11)

대상: `CENTURION_DAY/fix`(브랜치 `kknaksss/fix-app-re1`) `app/` 밖 — 앞 서버 검수(2) 뒤 바뀐 것. 중심은 `chat_storage.py` · `chat.py`(저장 · 열기 · 전달) · `errors.py` · `config.py` · `public.py` · `runtime/main.py` · `day_vm.py` · `deploy/*` · `pyproject.toml` · `uv.lock` · 시험이다.
SoT: `deployment.md` 「파일 저장소(Blob)」 · SPEC-004 개정 ⑤ + 정정 3(`:32` · `:406` · `:425` · `:479-480` · C-A26 `:613` · C-A27 `:614`) · `correction-storage-2/3.md`. read-only · 저장소 · Azure · IMDS 호출 0. **값(주소 · 계정 · 컨테이너 이름) 없음.**

## 판정: PASS

FAIL 0 · WARN 0 · 참고 4. 연결 문자열 · 환경 접두는 완전히 걷혔다. 인증은 관리 ID 하나에 30초 상한이다. 실패 갈래(409 · 503 · 404 · 413 · 끊김), 클라이언트 수명, 배포 설정, 의존성이 스펙 · 정정 3 과 같다.

## 항목별

| # | 결과 | 자리 · 근거 |
|---|---|---|
| 1 연결 문자열 | 걷힘 | 내 grep(`from_connection_string` · `chat_blob` · `CHAT_BLOB` · `chat-blob`, `app/` · `uv.lock` 제외) 결과 = `day_vm.py:48`(「읽지 않음」 주석) · `:57` `RETIRED_SECRETS` · `deployment.md:109`(설명) · 시험의 금지 단언(`test_chat_env_contract.py:27 · 125` · `test_day_vm.py:410-570`)뿐 — 코드 · 설정 0. `FORBIDDEN_CONFIG_KEYS = {*SECRETS, *OPTIONAL_SECRETS, *RETIRED_SECRETS, …}`(`day_vm.py:58-60`) → 없앤 키가 Git 일반 설정에 들어오면 계속 거절된다. `OPTIONAL_SECRETS` = APNs · Soniox 둘 → Vault 에 옛 비밀이 있든 없든 읽지 않으니 배포는 같다(시험 `test_materialize_옛_연결_문자열이_Vault_에_남아_있어도_배포는_그대로`) |
| 2 관리 ID 만 | 맞음 | `chat_storage.py:219-223` `ManagedIdentityCredential()` 하나 · `DefaultAzureCredential` · `EnvironmentCredential` · CLI 0(`grep` · 계약 시험이 `DefaultAzureCredential` 문자열도 막음). `TimedCredential`(`:191-216`)이 `get_token` · `get_token_info` 둘 다 `asyncio.timeout(30)` 으로 감싼다 → 넘기면 안쪽 작업이 취소되어(aiohttp 요청 정리) 밖으로 `TimeoutError` → `_unavailable` → 503. 토큰 캐시는 라이브러리(자격 증명 · Blob 정책) 그대로다. 첫 사용 때 동시 요청이 토큰을 여러 번 받을 수 있지만 무해하다 |
| 3 수명 | 맞음 | `LazyContainer.client()`(`:262-268`)가 처음 쓸 때 자격 · 클라이언트를 만든다(기동 · import 때 IMDS · 저장소 0 — 시험 `…기동때는_닿지_않고_재사용`). `_blob_cache`(`:290`) = (주소, 컨테이너)마다 한 벌. lifespan `finally` 에서 `close_file_storage()`(`runtime/main.py:35` · `public.py:91`) → `close_storage` 가 캐시를 비우고 클라이언트 · 자격을 닫는다(닫기 실패 = 로그). 닫은 뒤 다시 쓰면 새로 만든다(캐시를 비웠으므로). 자식 `BlobClient` 의 `async with` 는 SDK 가 transport 를 래퍼로 넘겨 부모 세션을 닫지 않는다. 시험은 `_blob_cache` 를 `monkeypatch` 로 시험마다 비워 누수가 없다. worker · scheduler: `day/tasks` 에서 저장소를 쓰지 않는다(`grep`) → 클라이언트가 생기지 않는다 |
| 4 키 | 맞음 | `KEY_PATTERN = ^chat/{uuid}/{32 hex}\.(jpg\|mp4)$`(`:43`) · `new_key` 같은 모양. 저장소 코드 · 시험에 `APP_ENV` · `app_env` 0(`grep`) — 환경 접두 · 환경 `check_key` 잔재 없음. 모양 밖 키: 열기 = `is_key` → `missing()` 404(`chat.py:1410`) · 전달 = 원본 없음(`:1065`) · 지우기 = `check_key` 의 `InvalidKey` 를 `delete_quietly` 가 로그로 삼킴 — 500 길 없음. 다른 병원: 열기는 `ChatAttachment` 행 → 방 경계(`_room_for` · 세션 병원 · `from_seq`)로 막고 키 모양에 기대지 않는다(`:1378-1404`) |
| 5 실패 | 맞음 | 설정 빔 → `storage_from` None → 409(기존). `_unavailable`(`AzureError \| TimeoutError` — 토큰 · 403 `HttpResponseError` · 연결/읽기 시간 초과 `ServiceRequestError/ResponseError`)와 `ResourceNotFoundError(ContainerNotFound)` → `StorageUnavailable` → `chat.py:1202` 503 `photo_disabled`(같은 글자 · `errors.py:185`). `BlobNotFound` → `size()` None → 404. 크기 초과는 `ChatError`(Azure 아님)라 바뀌지 않아 413 그대로다. `save` 실패 · 취소 → `shield` 로 지우기 시도 후 다시 올림. 본문 도중 → `stream_file`(`:1349-1360`) 이 로그(키 앞 13자 · 원인 종류) 뒤 다시 올려 응답이 끊긴다 — 머리를 보낸 뒤라 상태는 바뀌지 않는다(503 으로 둔갑 없음). 로그 `_cause` = 예외 이름 · status · 오류 코드만(메시지 · 주소 · 토큰 없음). **앱**: 409 · 503 모두 code `photo_disabled` 지만 앱은 상태로 가른다 — 올리기 4xx = 토스트 + 지움 / 5xx = 「보내지 못했어요」 + [다시 보내기](`chat_state.dart` `_deliver`) · 사진 열기 실패 = 그리지 않음(`_load`) · 전달 5xx = 시트 남김(`chat_forward_sheet.dart`). 스펙 `:425 · :479` 와 같다 |
| 6 컨테이너 이름 | 설정에서만 | `daydev` · `dayprod` · `"files"` 리터럴 = 코드 0. 시험에는 `test_chat_units.py:237`(그 리터럴이 **없음**을 단언)과 `conftest.py:268`(디스크 저장소 임시 폴더 이름 — 컨테이너 아님)뿐 |
| 7 배포 설정 | 맞음 | `dev.env` = 스위치 `blob` · 주소 · 컨테이너 세 칸(값 있음 — 옮기지 않음) · `prod.env:31-33` = 세 칸 빈 값 + 주석 · `compose.local.yaml:32-38` · `local.env.example:57-64` 새 이름 · 빈 기본. 설정 계약 시험은 모양만 보고 값을 메시지에 싣지 않는다(작성자 표 · 앞 판 규칙 유지). `materialize --dry-run` 통과는 작성자 주장 그대로(내가 돌리지 않음 — 코드상 새 칸은 금지 목록 밖) |
| 8 의존성 | 맞음 | `pyproject.toml` `azure-identity>=1.19,<2`(+ 앞 판 opencc · websockets). `uv.lock` diff 의 `+name` = `azure-identity 1.27.0` · `msal 1.39.0` · `msal-extensions 1.3.1` 셋(+ 앞 판 opencc) · **`-version` 줄 0** = 기존 패키지 변경 없음. `msal` 의존 `requests` · `pyjwt` 는 이미 잠금에 있다 |
| 10 범위 · 앞 판 | 깨진 것 없음 | `.github/` · `backend/migrations` 무변경 · `common/logs.py` · `services/interpret/` · `queries/chat.py` diff 줄 수가 앞 검수 때와 같다(읽음 표시 · 통역 · 접근 로그 필터 무변경). `app/` 변경은 같은 워크트리 mobile 워커 몫(대상 아님) |

## C-A27 실물 확인 명령(작성자 · 코디가 dev 컨테이너에서 돌림) — 읽고 판정

- ⓐ 올리기 → 속성 읽기 → 범위 읽기 → 지우기: `save` → `size` → `read(0, len−1)` → `delete` → **맞음.** 다만 범위가 파일 전체(0 ~ 끝)라 「부분 범위」가 실제로 잘리는지는 보지 않는다 — 참고 R1.
- ⓑ 경로 = `chat/{병원 id}/…`: 설정 컨테이너 안에서 `list_blobs(name_starts_with="chat/{가짜 병원}/")` 에 그 키가 있음 → **맞음**(컨테이너 이름은 설정에서 오고 출력하지 않음).
- ⓒ 없는 키 열기 = 404(503 아님): 지운 뒤 `size(key) is None`(= `BlobNotFound` → 404 길) → **맞음.** 서비스(`open_attachment`)를 거치지는 않지만 404 판정은 `size()` 한 곳이다.
- 출력은 키 앞 13자뿐이다(주소 · 값 없음) · 가짜 병원 id 아래라 실제 폴더와 섞이지 않는다.

## 조용히 통과하는 자리

1. **관리 ID 경로는 실물에서만 확인된다** — 시험은 가짜 자격 · 가짜 클라이언트 경계(`credential_factory` · `client_factory` · `client_for`)를 쓴다. 작성자 보고에 「실물(C-A27)은 dev 배포 뒤 코디」 · 「503 길은 C-A26 단위로만」이 분명하다(스펙 `:614` 「받아들임」과 같음).
2. 가짜 예외는 SDK 모양 그대로다 — `process_storage_error` 로 만든 `ResourceNotFoundError` + `StorageErrorCode`(BlobNotFound / ContainerNotFound) · `HttpResponseError(403)` · `ServiceRequestError` · `ClientAuthenticationError` · `TimeoutError`(작성자 시험 표 · 정정 W7). 실제 SDK 가 **올리기 본문 생성기의 예외**(크기 초과 `ChatError`)를 감싸지 않고 그대로 올리는지는 가짜로만 확인됐다. 블록 올리기는 SDK 파이썬 코드가 생성기를 읽으므로 그대로 올라올 것으로 보이지만, 실물(큰 동영상 413)은 dev 에서 한 번 보면 확실하다 — 참고 R2.
3. infra 시험(`test_chat_attachments.py` API 갈래 · 303 deselected)은 내 실행에서 빠졌다. 865 + 303 = **1168** 이 작성자 격리 전체 수와 같다 — 못 믿을 근거 없음.
4. 토큰 30초 상한 시험은 가짜 자격(멈추는 `get_token`)으로 짧은 상한을 걸어 본다. 실제 IMDS 재시도 합(약 24초)과 30초 사이 여유는 실물에서만 보인다.

## 참고

- R1. C-A27 명령의 범위 읽기를 부분 범위(예: `read(key, 1, len(body) − 2)` = `body[1:-1]`)로 바꾸면 「206 범위」를 실제로 확인한다.
- R2. dev 배포 뒤 실기기에서 상한을 넘는 동영상 한 번 → 413(503 아님) 확인.
- R3. 첫 사용 순간 동시 요청이 몰리면 토큰을 여러 번 받을 수 있다(무해 · 캐시로 곧 하나).
- R4. `TimedCredential.get_token_info` 는 안쪽에 그 메서드가 없으면 `AttributeError` 다. 지금 `azure-identity>=1.19` 에는 있으므로 문제 없음(하한을 1.19 로 둔 이유와 맞음).

## 돌린 명령 · 수치(각 1회)

| 명령 | 결과 |
|---|---|
| `cd backend && uv run pytest -q -m "not infra"` | **865 passed, 303 deselected**, 1 warning(기존) · exit 0 |
| `cd backend && uv run ruff check . ../scripts` | All checks passed! |
| infra · 저장소 · Azure · IMDS | 돌리지 않음(지시) |
