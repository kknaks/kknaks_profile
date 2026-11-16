# fix WP-BE-4 파일 저장소(관리 ID · 컨테이너로 환경 분리) 결과 보고

## 상태: done · 정정 2(`correction-storage-2.md`) · 정정 3(`correction-storage-3.md`) 반영 · 실물(C-A27)은 dev 배포 뒤 코디

> 정정 3 이 정정 2 의 「맨 위 환경 폴더」를 뒤집었다 → **최종 = 환경은 컨테이너로 나눔 · 키 = `chat/{병원 id}/{32 hex}.{jpg|mp4}`(환경 폴더 없음 · 지금까지의 `new_key` 그대로)**. 중간에 넣었던 `{APP_ENV}/` 접두 · 환경 `check_key` 는 모두 걷어 냈다.

## 변경 파일

| 파일 | 무엇 |
|---|---|
| `backend/day/services/chat_storage.py` | 키 규칙 `:43 · 67 · 72 · 78`(`is_key` = 모양 검사 · 아니면 서비스가 404) · 시간 상한 `:45-49`(연결 20 · 읽기 60 · 토큰 30) · `StorageUnavailable :56`(원인 종류만) · `TimedCredential :191`(토큰 받기 전체 상한 · `get_token` · `get_token_info` 둘 다) · `managed_identity_credential :219`(`ManagedIdentityCredential` 하나 — 체인 없음) · `container_client :226`(주소 · 컨테이너 · 자격 · 20/60 을 클라이언트에 명시) · `LazyContainer :239`(처음 쓸 때 자격 · 클라이언트 생성 · 재사용 · `close`) · `BlobStorage :290`((주소, 컨테이너)마다 한 벌 캐시 · Azure 오류/시간 초과 → `StorageUnavailable` · BlobNotFound = None · ContainerNotFound = 접근 실패 · `_delete_quiet :373` 은 blob 없음만 삼킴) · `close_storage :382` · `storage_from :391`(`blob` + 주소 + 컨테이너 둘 다일 때만) |
| `backend/day/services/chat.py` | `_unavailable :1202` · `_size :1208` · `_store :1215`(접근 실패 → 503 `photo_disabled` · 로그 = op · 키 앞 13자 · 원인 종류) · 전달 `:1065` · 열기 `:1410`(모양 밖 키 = 없는 것처럼) · `stream_file :1349`(본문 도중 실패 = 로그 + 끊김) |
| `backend/day/errors.py:185` | `chat_storage_unavailable()` = 503 · code `photo_disabled` · 글자 그대로(새 code · 새 글자 없음) |
| `backend/day/routers/api/chat.py:464` | 본문 스트림 = `chat.stream_file` |
| `backend/common/config.py:154-155` | **더함** `day_blob_account_url` · `day_blob_container`(비밀 아님) · **없앰** `day_chat_blob_container` · `day_chat_blob_connection_string` |
| `backend/day/public.py:91` · `backend/runtime/main.py:36` | `close_file_storage()` — lifespan 종료 때 클라이언트 · 자격 증명 닫기(정정 W6) |
| `scripts/deploy/day_vm.py:49 · 57-59` | 선택 비밀 = APNs · Soniox 둘 · **`RETIRED_SECRETS`** = 없앤 `DAY_CHAT_BLOB_CONNECTION_STRING` 을 일반 설정 금지 목록에 유지(정정 W5) |
| `deploy/config/dev.env` | `DAY_CHAT_STORAGE=blob` · `DAY_BLOB_ACCOUNT_URL` = 설정됨(사용자 안내문에서 스크립트로 읽어 넣음 · 모양 검사) · `DAY_BLOB_CONTAINER` = 설정됨(정정 3 의 dev 컨테이너 이름) · 주석 |
| `deploy/config/prod.env` | 칸 · 주석만(값 없음) |
| `deploy/compose.local.yaml` · `deploy/local.env.example` | 옛 두 이름 → `DAY_BLOB_ACCOUNT_URL` · `DAY_BLOB_CONTAINER`(로컬은 비움 · `disk`) |
| `docs/development/deployment.md` | 선택 비밀 줄에서 연결 문자열 뺌 · 파일 저장소 단락(컨테이너 = 환경 · 관리 ID · 503 · 종료 때 닫기 · 옛 비밀 무시/거절) |
| `pyproject.toml` · `uv.lock` | `azure-identity>=1.19,<2`(1.27.0) — 잠금 차이 = `azure-identity` · `msal` 1.39.0 · `msal-extensions` 1.3.1 **셋만 추가 · 기존 패키지 버전 변경 0**(잠금 비교로 확인) |
| 시험 | `tests/day/chat/test_chat_units.py` · `test_chat_attachments.py` · `tests/deploy/test_chat_env_contract.py` · `test_day_vm.py` |

확인만: `deploy/compose.yaml`(api 는 `env_file` 로 받음 — 새 칸 따로 줄 필요 없음 · 시험이 지킴) · `deploy/Dockerfile` 무변경 · `app/` 무변경 · migration 0.

## 걷어 낸 낱말 grep 전수(작업 전 · 기준 = 레포의 py · env · yaml · example · md · toml)

| 낱말 | 자리(작업 전) | 처리 |
|---|---|---|
| `from_connection_string` | `chat_storage.py:138` | 삭제 → 관리 ID `ContainerClient`(시험이 다시 들어오지 못하게 지킴) |
| `day_chat_blob_container` · `day_chat_blob_connection_string` | `common/config.py:151 · 153` · `chat_storage.py:195-196` · `test_chat_units.py:144` | 칸 삭제 · `day_blob_account_url` · `day_blob_container` 로 |
| `DAY_CHAT_BLOB_CONTAINER` · `DAY_CHAT_BLOB_CONNECTION_STRING` | `compose.local.yaml:36-37` · `local.env.example:61 · 63` · `dev.env:22 · 28` · `prod.env:23 · 26` · `test_chat_env_contract.py:18-28 · 68` · `test_day_vm.py:392-523` | 설정 · 예시 · compose 에서 삭제 · 시험은 새 이름 + 「없앤 이름이 다시 나타나지 않음」 시험 · `day_vm.py` 금지 목록엔 **남김**(W5) |
| `chat-blob` | `day_vm.py:49` · `deployment.md:100` · `test_day_vm.py:431 · 451 · 523` | 선택 비밀에서 삭제 · 문서 · 스크립트엔 「더 읽지 않음」 설명만 |
| `new_key` | `chat_storage.py:40` · `chat.py:1252 · 1298 · 1299` · 시험 | **모양 그대로**(정정 3) |
| `check_key` · `KEY_PATTERN` | `chat_storage.py:33 · 45 · 70 · 148-177` · 시험 | 모양 그대로 + `is_key` 로 열기 · 전달이 모양 밖 키를 404 길로(500 아님) |

작업 뒤 grep: `from_connection_string` · `CHAT_BLOB` · `chat_blob` 은 코드 · 설정에 0(남은 것 = `day_vm.py` 금지 목록 · 문서 · 스크립트의 「안 읽음」 설명 · 시험의 금지 단언).

## 수용 항목 ↔ 시험

| 항목(C-A26 · 정정 2 · 3) | 시험 |
|---|---|
| 키 = `chat/{병원 id}/{32 hex}.{jpg\|mp4}` · 모양 밖(환경 폴더 붙은 것 · 다른 용도 · 경로 탈출 · 확장자 · 대문자) 거절 | `test_chat_units.py::test_저장소_키는_chat_병원_무작위_모양만` · `test_chat_attachments.py::test_올린_파일은_chat_병원_경로` · `::test_사진_올리기_붙기_전엔…`(경로) |
| 모양 밖 키 = 열기 404 · 전달 = 원본 없음 | `test_chat_attachments.py::test_키_모양이_아니면_없는_것처럼_404` |
| 컨테이너 이름은 설정에서만(코드에 특정 이름 0 · 환경마다 다른 값) | `::test_컨테이너_이름은_설정에서만_온다` · `::test_종료_때_클라이언트와_자격_증명을_닫는다`(두 컨테이너 = 두 벌) |
| 설정: `blob` + 주소 + 컨테이너 = 켜짐 / 하나라도 빔 = 꺼짐(409) | `::test_첨부_저장소는_값이_빠지면_꺼짐` · `test_chat_attachments.py::test_저장소가_꺼지면_409_photo_disabled` |
| 관리 ID 하나 · 체인 아님 · 토큰 상한 30초 | `::test_자격_증명은_관리_ID_하나_토큰_받기에_상한` |
| 클라이언트에 주소 · 컨테이너 · 자격 · 20 · 60 초 명시 | `::test_컨테이너_클라이언트는_관리_ID_자격과_시간_상한_20_60` |
| 기동 때 저장소 · 토큰에 닿지 않음 · 처음 쓸 때 한 번 만들고 재사용 | `::test_blob_설정이면_관리_ID_저장소_기동때는_닿지_않고_재사용` |
| 접근 실패(토큰 · 403 · 컨테이너 없음 · 연결 실패 · 시간 초과) → `StorageUnavailable` · 원인 종류만 · 쓰다 실패 = 지우기 시도 | `::test_저장소_접근_실패는_StorageUnavailable_원인_종류만`(5갈래 × save · size · read · delete) |
| **SDK 예외 모양 그대로**(정정 W7) — `process_storage_error` 로 만든 `ResourceNotFoundError` + `StorageErrorCode`: BlobNotFound = None(404 길) · ContainerNotFound = 접근 실패 | `::test_그_blob_만_없으면_None_컨테이너_없음은_접근_실패` · 위 5갈래의 403 · 컨테이너 없음도 SDK 모양 |
| 크기 초과(413)는 접근 실패로 바꾸지 않음 | `::test_쓰기_크기_초과는_접근_실패로_바꾸지_않는다` |
| API: 올리기(사진 · 동영상) · 열기 · 전달 = 503 `photo_disabled` 같은 글자 · 글은 됨 · 동영상 실패 = 두 키 지우기 시도 | `test_chat_attachments.py::test_저장소_접근_실패는_503_photo_disabled_같은_글자` |
| 보내는 중 실패 = 끊김 + 로그(키 앞자리 · 원인)(정정 W3) | `test_chat_units.py::test_보내는_중_실패는_끊김과_로그만` |
| 종료 때 닫기(정정 W6) | `::test_종료_때_클라이언트와_자격_증명을_닫는다` · `::test_lifespan_종료가_파일_저장소를_닫는다` |
| 연결 문자열 칸 없음 · 없앤 이름 재등장 0 · 선택 비밀 둘 · 옛 비밀이 Vault 에 남아도 배포 그대로 · 없앤 키 이름은 일반 설정에서 계속 거절(W5) | `tests/deploy/test_chat_env_contract.py`(전체 · `::test_없앤_저장소_이름은_…`) · `test_day_vm.py::test_파일_저장소는_선택_비밀이_없고_옛_연결_문자열은_무시` · `::test_materialize_옛_연결_문자열이_Vault_에_남아_있어도_배포는_그대로` · `::test_선택_비밀을_Git_일반_설정에_넣으면_거부한다[DAY_CHAT_BLOB_CONNECTION_STRING]` |
| dev 설정 = blob · 주소 모양 · 컨테이너 모양(값은 메시지에 없음) · prod = 빈 칸 | `test_chat_env_contract.py::test_dev_서버는_…` · `::test_prod_서버_채팅_설정은_아직_비움` |
| C-A9 · C-A10 회귀 | `test_chat_attachments.py` 기존 전부 통과 |

## 설정 계약 표 ↔ 구현

| 계약(deployment.md · 정정 3) | 구현 |
|---|---|
| `DAY_BLOB_ACCOUNT_URL`(비밀 아님 · config) | 칸 있음 · dev = 설정됨 · prod = 빈 칸 |
| `DAY_BLOB_CONTAINER`(환경별 값 · dev / prod 컨테이너) | 칸 있음 · dev = 설정됨(dev 컨테이너) · prod = 빈 칸 · 코드는 이름 가정 0 |
| `DAY_CHAT_STORAGE` = `blob`(두 칸과 함께) | dev = `blob` · prod = 빈 칸 |
| 없앰 `DAY_CHAT_BLOB_CONTAINER` · `DAY_CHAT_BLOB_CONNECTION_STRING` | 설정 · compose · 예시 · 코드 0 · 금지 목록엔 유지 |
| 선택 비밀 = APNs · Soniox | 같음 |
| 인증 = VM 시스템 할당 관리 ID 만 | `ManagedIdentityCredential` 하나(시험) |
| 경로 = 컨테이너 안 `{용도}/{병원 id}/…` · 채팅 = `chat` | 같음 |
| 로컬 = disk · 로컬 Blob 길 없음 | 같음(로컬 예시는 Blob 칸 비움) |

## 실패 동작 표 ↔ 구현

| 경우 | 스펙 | 구현 |
|---|---|---|
| 설정 빔 | 409 `photo_disabled` | 같음(`storage_from` → None) |
| 토큰 못 받음(30초 · 인증 오류) | 503 `photo_disabled` | `TimeoutError` · `ClientAuthenticationError` → `StorageUnavailable` → 503 |
| 403 | 503 | `HttpResponseError(403)` → 503 |
| 컨테이너 없음(아직 안 만든 dev 컨테이너 포함) | 503 | `ResourceNotFoundError(ContainerNotFound)` → 503 |
| 그 blob 없음 | 404(열기) · 전달 불가 | `BlobNotFound` → None → 기존 404 · `chat_not_forwardable` |
| 연결 20 · 읽기 60 초 초과 | 503 | `ServiceRequestError` · `ServiceResponseError`(AzureError) → 503 |
| 본문 보내는 중 실패 | 끊김 + 로그 | `stream_file` 이 로그 뒤 예외로 끊음 |
| 쓰다 실패 | 지우기 시도 · 실패는 로그 | 같음(save 안 · 동영상 두 키) |
| 기동 | 막지 않음 | 처음 쓸 때 생성(시험) |
| 로그 | 원인 종류 · 키 앞자리 | `cause` = 예외 이름 · status · 오류 코드만 · 키 앞 13자 |
| 종료 | 클라이언트 · 자격 닫기 | lifespan `close_file_storage` |

## 수치

- 격리 스택(`docker compose -p daybetest` · 127.0.0.1:11142/11143 · 일회용 자격 · 끝나고 `down -v` · 볼륨 0) · 사용자 `day-local-*` · 11040/11042/11043 무변경
- 고친 시험: `test_chat_units.py tests/deploy tests/common tests/architecture` → **226 passed**(3 skipped = 기존) · 격리 `test_chat_attachments.py` → **12 passed**(정정 3 반영 전 마지막 실행 기준 · 정정 3 뒤 전체에 포함)
- `uv run ruff check backend scripts` → All checks passed · `ruff format --check` → 227 files already formatted
- `uv run pytest -q -m "not infra"` → **865 passed**, 303 deselected
- 격리 스택 `scripts/test.sh -q` 전체 → **1168 passed**(경고 1 = 기존 `fastapi.testclient` deprecation)
- `day_vm.py materialize --environment dev --dry-run`(새 dev.env) → exit 0 · 선택 비밀 이름 2개(APNs · Soniox)만 · 옛 Blob 비밀 없음
- 실제 저장소 · Azure · Key Vault 호출 0 · 로컬에서 저장소에 붙지 않음

## dev 배포 뒤 코디가 dev api 컨테이너에서 돌릴 실물 확인(C-A27 ① — 값 없이)

전제: dev 설정 컨테이너가 저장소에 **만들어져 있고** VM 관리 ID 에 그 컨테이너 권한이 있다(정정 3 ④ — 아직 없으면 아래는 `StorageUnavailable … ContainerNotFound` 로 끝나는 것이 정상).

```sh
docker exec -i <dev api 컨테이너> python - <<'PY'
import asyncio, secrets, uuid
from common.config import get_settings
from day.services import chat_storage

async def main():
    s = get_settings()
    store = chat_storage.storage_from(s)
    assert store is not None, "storage off — DAY_CHAT_STORAGE / DAY_BLOB_* 확인"
    hospital = uuid.UUID("00000000-0000-4000-8000-00000000c0de")   # 시험 전용 가짜 병원 id
    key = chat_storage.new_key(hospital, "jpg")                    # chat/{가짜 병원 id}/{32 hex}.jpg
    body = b"\xff\xd8\xff" + secrets.token_bytes(32)
    async def chunks():
        yield body
    await store.save(key, chunks())                                 # ① 올리기
    assert await store.size(key) == len(body)                       # ② 크기
    got = b"".join([c async for c in store.read(key, 0, len(body) - 1)])
    assert got == body                                              # ③ 읽기 = 같은 바이트
    lazy = store.lazy
    names = [b.name async for b in lazy.client().list_blobs(name_starts_with=f"chat/{hospital}/")]
    assert key in names                                             # ④ 실제 경로 = chat/{병원 id}/…
    await store.delete(key)                                         # ⑤ 지우기
    assert await store.size(key) is None                            # ⑥ 지운 것 확인
    names = [b.name async for b in lazy.client().list_blobs(name_starts_with=f"chat/{hospital}/")]
    assert key not in names
    await chat_storage.close_storage()
    print("C-A27 ok — key prefix", key[:13], "…")                   # 값 · 주소 출력 없음

asyncio.run(main())
PY
```

- 시험 파일 이름 규칙: 가짜 병원 id `00000000-0000-4000-8000-00000000c0de` 아래 무작위 이름 — 실제 병원 폴더와 섞이지 않고, 남아도 이 접두로 찾아 지울 수 있다.
- 실패 갈래 확인(선택): 같은 스크립트를 컨테이너 이름만 없는 이름으로 바꾼 env 로 돌리면 `StorageUnavailable … ContainerNotFound`(앱 = 503).
- ② 사용자 실기기(TestFlight 사진 · 동영상 보내기 · 받기)는 그 뒤.

## 스펙과 다른 곳 · 물을 것

1. **토큰 상한 30초**: 스펙 7판은 「azure-identity 기본(구현 때 확인)」이었다 — 확인 결과 IMDS 기본 = 연결 2초 · 재시도 5번(대기 합 약 24초) · 읽기 상한은 aiohttp 기본 300초라 사실상 상한이 없어 `TimedCredential` 로 전체 30초를 걸었다. 정정 2 W1 이 30초로 확정 — 같음.
2. 정정 3 으로 「옛 키 읽지 않음」이 사라졌다 — 이전 로컬 `disk` 의 `chat/…` 키는 다시 열린다(정정 3 ⑥ 그대로).
3. 본문 도중 실패의 「끊김」은 서버가 예외로 응답을 끊는 것이라 uvicorn 이 오류 줄(예외 이름)을 하나 더 남긴다 — 값 · 주소 없음.
4. 짐작으로 메운 것 없음. 작업 중 정정 2 · 3 을 받아 반영했고, 정정 2 의 「맨 위 환경 폴더 유지」는 정정 3 대로 걷어 냈다.

## pending

- **dev · prod 컨테이너 생성 + VM 관리 ID 권한**(사용자 → 인프라 담당) — 없으면 dev 첨부는 503(채팅 글은 정상).
- dev 배포 뒤 위 실물 확인(코디) · 사용자 실기기(C-A27 ②).
- prod.env 값(주소 · prod 컨테이너)은 prod 배포 때 사용자.
- 커밋 · push 없음.
