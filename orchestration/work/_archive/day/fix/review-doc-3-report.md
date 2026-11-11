# fix 스펙 7판 검수 — 파일 저장소(Blob) 구조 · 채팅 첨부 관리 ID 연결 (reviewer_doc)

- 대상: `mediness-mediness/fix-spec` 미커밋 7판분 — `40-architecture/deployment.md` 머리 줄 · env 표 · 새 절 「파일 저장소(Blob)」 · Key Vault 줄 · Blob 준비 행 · 미결 / SPEC-004 개정 ⑤ / SPEC-000 개정 ③ / `system.md:66` / `log.md` + `wp-plan.md` WP-BE-4.
- 원천: `_RESUME.md` §2(`:65-66`) · `correction-storage-1.md` · 인프라 담당 안내문(사용자 로컬). **안내문의 값은 이 리포트에 옮기지 않았다.**
- 코드 대조: `CENTURION_DAY/fix`. 서버 워커가 이미 `chat_storage.py` 를 고치는 중이라 고치기 전 줄과 지금 줄을 둘 다 봤다. 앱은 `app/lib/chat/` 를 직접 읽었다.
- read-only. 이 리포트 말고 고친 파일 0 · 커밋 · push · 서버 호출 0. Delivery #241 은 읽기만 했다.

## 판정: **WARN**

FAIL 0 · WARN 7. 계약을 바꿔야 하는 지적은 없다. 서버 워커가 이미 지은 코드도 스펙과 같은 방향이다(컨테이너 없음 구별 · 토큰 시간 상한). 그래서 `[긴급]` 은 보내지 않았다.

**맞는 것**
- 사용자 확정과 기본값이 구별돼 있다.
  - 사용자 확정: 맨 위 = 환경 · 용도 셋의 수와 뜻.
  - 코디 기본값: 폴더 이름 `identity` · `before-after` · dev/prod 차단 안 됨 받아들임 · 보관 그대로.
  - planner 기본값: 로컬 Blob 길 없음 · env 이름 `DAY_BLOB_*` · 옛 키 안 옮김.
  - 기술 기본값: 관리 ID 만 · 시간 상한.
  - 근거: `deployment.md:181-196` · 용도 표 · 미결 3줄.
- 안내문과 사실이 맞는다: 관리 ID 만 · 키 · 연결 문자열 · SAS · 익명 꺼짐 · 컨테이너 하나 · 권한 = 컨테이너 전체 · 자동 삭제 규칙 · soft delete · 버전 관리 없음 · 서버 경유 · 브라우저 업로드 · 공유 링크 · CORS 없음 · Docker 안 관리 ID 는 인프라 담당이 확인 안 함(코디가 따로 확인했다고 출처를 밝힘).
- 값이 새지 않았다.
  - `git diff` 의 `+` 줄에서 안내문 값으로 걸린 것은 하나뿐이다. `deployment.md` Key Vault 행(`:421` diff 줄)인데, 원래 있던 Vault 이름 · 리소스 그룹 줄에 「선택 2」 문구만 고친 것이다(이번 새 값 아님).
  - `wp-plan.md` · `spec-7-report.md` · Delivery #241 v3 본문(디코드해서 확인)에도 값 0.
- 새 화면 글자 0 · 새 오류 code 0 · migration 0.

---

## WARN

| # | 자리 | 무엇이 문제인가 · 근거 | 고칠 방향 |
|---|---|---|---|
| W1 | `deployment.md` 「시간 상한」 줄(새 절 표) · SPEC-004 `:425` · C-A26 `:612` | **토큰 받기의 시간 상한을 「구현 때 확인」으로 비워 뒀다.** DAY `AGENTS.md:129` 는 timeout 을 명시하라고 한다. `azure-identity` 1.27.0 의 관리 ID 토큰 요청 기본값은 연결 2초 · 재시도 5번 · backoff 0.8(최대 60)이다(`.venv/.../azure/identity/_credentials/imds.py:26-32`). 그대로 두면 토큰 하나에 수십 초가 걸릴 수 있다. 서버 워커는 이미 `TOKEN_TIMEOUT = 30`(`chat_storage.py:47` · `asyncio.timeout` 으로 감쌈)을 정했다. | 문서 표 · C-A26 에 「토큰 받기 30초(감쌈) → 넘으면 503」을 적어 코드와 맞춘다. 이 칸은 비워 두지 않는다. |
| W2 | SPEC-004 `:425`(「열기 실패 = 그 사진을 그리지 않음」) · 케이스 매트릭스 `:479` · `wp-plan` WP-BE-4 「앱 변경 없음」 근거 | **동영상 재생 갈래가 빠졌다.** 재생기는 HTTP 상태를 모른다. 실패하면 앱은 목록을 한 번 읽고, 채팅 거절이 아니면 토스트 「동영상을 찾을 수 없어요」 + 화면 닫힘으로 간다(`app/lib/chat/screens/chat_video_screen.dart:120-130`). 그래서 저장소 접근 실패(503)인데 「찾을 수 없어요」가 보인다. 앱을 고칠 필요는 없다. 다만 「앱이 이미 상태로 갈래를 나눈다」는 문장은 재생에는 맞지 않는다. | 매트릭스 `:479` 에 「재생 = 「동영상을 찾을 수 없어요」 토스트 + 닫힘(재생기는 상태를 모름 · 기존 글자 · 앱 변경 없음)」을 더한다. 썸네일은 사진과 같은 `_load` 라 「그리지 않음」이 맞다. |
| W3 | SPEC-004 `:425`(열기 = 503) · `wp-plan` WP-BE-4 고칠 파일 | **본문을 보내기 시작한 뒤의 실패는 503 이 될 수 없다.** 열기는 `size()`(속성 읽기)를 먼저 한다. 그 뒤 본문은 `StreamingResponse(opened.storage.read(...))` 로 보낸다(`routers/api/chat.py:463-468`). 이미 200/206 머리를 보낸 뒤 내려받기가 시간 초과 등으로 실패하면 응답이 끊길 뿐이다. 앱은 끊긴 응답을 네트워크 오류(`ApiError(0)`)로 받아 그리지 않는다(사진) · 재생 실패(동영상)로 간다 — 결과는 W2 와 같은 화면. `routers/api/chat.py` 가 WP 고칠 파일 · 확인 목록에 없다. | §3 「저장소 접근 실패」에 「503 = 본문을 보내기 전 실패만 · 보내는 중 실패 = 응답이 끊김(로그만)」 한 줄. WP-BE-4 확인 목록에 `routers/api/chat.py` 의 스트림 자리를 더한다(끊김 로그에 키 앞자리만). |
| W4 | `deployment.md` 새 절 「저장소」 줄(「컨테이너 하나(dev · prod 같이)」 → 근거 「인프라 담당 안내문」) | **출처가 섞였다.** 안내문은 컨테이너 하나와 VM 하나만 말한다. dev · prod 가 같은 컨테이너를 쓰는 것은 사용자 · 코디 결정이다(`_RESUME.md:65` 「dev/prod 차단 안 됨 받아들임」). 「dev ↔ prod」 줄은 근거를 「안내문 · 코디 기본값」으로 잘 적었다. | 「저장소」 줄 근거에 「dev · prod 같이 = 사용자 2026-11-11 · 코디 기본값」을 더한다. |
| W5 | `wp-plan.md` WP-BE-4 `scripts/deploy/day_vm.py` 줄(「일반 설정 금지 목록이 자동으로 따라오는지 확인」) | 금지 목록은 `FORBIDDEN_CONFIG_KEYS = {*SECRETS, *OPTIONAL_SECRETS, …}` 다(`day_vm.py:56-58`). `OPTIONAL_SECRETS` 에서 연결 문자열 줄을 빼면 **`DAY_CHAT_BLOB_CONNECTION_STRING` 을 Git 일반 설정에 넣어도 더는 막히지 않는다.** 앱은 `extra="ignore"`(`config.py:75`)라 읽지 않지만, 비밀이 Git 에 들어가는 길이 열린다. | 옛 비밀 키 이름을 금지 목록에 따로 남긴다(또는 `DAY_*CONNECTION_STRING` 접두 금지). `test_day_vm.py:492` 같은 시험을 「없앤 키도 config 에 있으면 거절」로 유지한다. |
| W6 | `deployment.md` 새 절 「기동」 줄 · 「의존성」 줄 | 자격 증명 · 클라이언트를 처음 쓸 때 만들어 재사용한다고 했다. 하지만 **닫는 때**(앱 종료 때 `credential.close()` · aiohttp 세션)가 없다. 지금 코드는 요청마다 `BlobClient` 를 `async with` 로 열고 닫는다 — 요청마다 HTTP 세션을 새로 만든다. 계약이 아니라 품질 문제다. | 「앱 종료 때 자격 증명 · 클라이언트를 닫는다(lifespan)」 한 줄 + 클라이언트 재사용 범위(컨테이너 클라이언트 하나)를 WP 에 적는다. |
| W7 | SPEC-004 C-A26 `:612` · C-A27 `:613` · Delivery A12 ~ A14 | **조용히 통과하는 자리.** 아래 표. | 아래 표의 방향대로 더한다. |

W7 — 조용히 통과하는 자리:

| 무엇 | 왜 통과해 버리나 | 고칠 방향 |
|---|---|---|
| 「컨테이너 없음 = 503」 | 가짜 저장소에서는 어떤 예외를 던지느냐로 정해진다. 실제 Azure 는 속성 읽기(HEAD)에서 `ResourceNotFoundError` 를 던지고 `error_code` 로 `BlobNotFound` 와 `ContainerNotFound` 를 가른다. 고치기 전 코드(`size()` — 모든 `ResourceNotFoundError` = 없음 → 404)가 바로 이 함정이었다. 서버 워커의 지금 코드는 `ContainerNotFound` 를 따로 본다(`chat_storage.py:178-181`). | C-A26 에 「`ContainerNotFound` 코드 = 503 · `BlobNotFound` = 404(열기) — 가짜 저장소가 SDK 예외 모양 그대로 던짐」을 적는다. |
| 관리 ID · 시간 상한 · 경로 | C-A26 은 가짜 팩토리라 실제 SDK 인자 · IMDS 를 타지 않는다. 실물은 C-A27 ① 하나뿐이다. | 확인 항목에 아래 셋을 적는다. ⓐ dev api 컨테이너에서 올리기 → 속성 → 범위 읽기(206) → 지우기 ⓑ 저장소 목록에서 경로 `dev/chat/…` 확인 ⓒ 없는 키 열기 = 404(503 아님). |
| 사용자 실기기(C-A27 ②) | 정상 길만 본다. 503 길은 실물로 재현할 수 없다. | 단위 시험으로만 판정한다고 적는다(받아들임). |

---

## 볼 것별 결과

### 1 · 2 · 3 — 사용자 확정 · 안내문 사실 · 값

| 항목 | 결과 |
|---|---|
| 맨 위 환경 `dev` · `prod` | `APP_ENV` 의 허용 값이 이 둘뿐이다(`common/config.py:31` `Literal["dev","prod"]`). 로컬 · 시험도 `dev` 라 로컬 디스크 키는 `dev/chat/…` 가 된다. `local` 같은 값은 없어 경로가 깨질 일이 없다 ✅ |
| 용도 셋 · 이름 | 확정 / 기본값이 구별돼 있다 · 「새 용도는 표에 먼저」 규칙 있음 ✅ |
| 병원 id 층 | 사용자 말에는 없고 `_RESUME:65` 「경로에 병원 id = 코디 기본값」이다. 그런데 문서 「경로」 줄 근거는 「사용자 2026-11-11(맨 위 = 환경 · 그 아래 용도)」로만 돼 있다 — 병원 id 층은 기본값이라는 표시가 없다. W4 와 같은 결의 작은 출처 문제라 W4 에 같이 고치면 된다 |
| 안내문에 없는 것을 사실처럼 | 「dev · prod 같이」(W4) 외에는 없음. 안내문의 「로컬 = 사용자 자격 증명」은 planner 기본값으로 쓰지 않는다고 적었다 ✅ |
| 값 | 새로 들어간 값 0 ✅ |

### 4 — 설정 계약

| 항목 | 결과 |
|---|---|
| 옛 칸을 쓰는 곳 | `config.py:151-153` · `chat_storage.py`(고치기 전) · `day_vm.py:49` · `dev.env` · `prod.env` 주석과 칸 · `compose.local.yaml:36-37` · `local.env.example:61-63` · `test_chat_env_contract.py:18-28 · 68` · `test_day_vm.py:392-523` · `test_chat_units.py:144` · `docs/development/deployment.md:100`. 모두 WP-BE-4 고칠 파일에 있다 ✅ (`test_config.py` 는 옛 이름을 안 쓰지만 새 칸 시험 자리로 맞음) |
| Key Vault 에 옛 선택 비밀이 남은 경우 | 배포는 목록에 있는 이름만 읽는다(`OPTIONAL_SECRETS`). 남아 있어도 무시되고 배포는 그대로 성공한다. 혹시 app.env 에 남아도 설정이 `extra="ignore"` 라 기동이 깨지지 않는다 ✅ (금지 목록이 풀리는 건 W5) |
| `blob` 인데 주소 · 컨테이너가 빔 | 스펙 `:424` = 꺼짐 409. 고치기 전 코드 `storage_from` 과 같은 방식 ✅ |
| compose | api 는 `env_file` 두 개로 설정을 받으므로 새 칸에 compose 변경이 필요 없다. 저장소를 쓰는 건 api 뿐이고(`chat_storage` 를 쓰는 곳 = `services/chat.py` · 라우터), api 는 `internal`(외부 차단 아님) + `edge` 망이라 IMDS · Blob 에 닿는다 ✅ |

### 5 — 경로 규칙

- `{APP_ENV}/chat/{병원 id}/{32 hex}.{ext}` 는 `new_key` · `check_key`(키 환경 = 설정 환경)와 맞고, DB `file_key` 칸(varchar)에는 키 문자열이 그대로 들어간다. 열기는 `check_key`, 전달은 같은 키 재사용 + `size()`, 지우기는 `check_key` 를 거친다. 서버 워커 코드 `KEY_PATTERN = ^(dev|prod)/chat/…` · `match.group(1) != app_env` 로 맞다 ✅
- 정당한 데이터를 깨뜨리지 않는다.
  - dev 는 배포된 `dev.env` 가 `DAY_CHAT_STORAGE=`(빔 — HEAD 기준 · 미커밋 작업본은 서버 워커가 `blob` 으로 바꾸는 중)라 지금까지 첨부 행이 생길 수 없었다.
  - prod 는 배포 전이다.
  - 로컬 디스크 옛 키만 못 읽는데, 이것은 기본값으로 표시돼 있다 ✅
  - 시험은 새 키로 다시 만든다(WP 에 있음).

### 6 — 실패 동작(앱 실제 코드)

| 경로 | 409 `photo_disabled` | 503 `photo_disabled` | 스펙과 |
|---|---|---|---|
| 올리기 · 보내기(`chat_state.dart:892-902`) | 4xx → 말풍선 지움 + 토스트 「사진 저장이 꺼져 있어요」(`chat_copy.dart:39`) | 5xx → `SendState.failed` · 「보내지 못했어요」 + [다시 보내기] | 같음 ✅ |
| 사진 · 썸네일 열기(`_load` `:1021-1036`) | null → 안 그림 | null → 안 그림(실패를 캐시하지 않음 — 다음에 다시 요청) | 같음 ✅ |
| 전달(`chat_forward_sheet.dart:6-7`) | 4xx → 닫힘 + 글자 | 5xx → 시트 남김 + 「보내지 못했어요」 | 같음 ✅ |
| 동영상 재생(`chat_video_screen.dart:120-130`) | 「동영상을 찾을 수 없어요」 + 닫힘 | 같음 | **스펙에 없음 — W2** |

- 409 와 503 에 같은 code 를 써도 앱이 헷갈리지 않는다. 앱은 `photo_disabled` code 로는 글자만 고르고, 갈래는 상태(4xx · 5xx)로 나눈다 ✅
- 「기동을 막지 않는다」는 AGENTS 와 맞는다. 다만 토큰 시간 상한이 문서에 없다(W1).

### 7 — 관리 ID 만

- 로컬 = 디스크 · 시험 = 가짜 팩토리 · CI = Azure 없음. 그래서 `DefaultAzureCredential` 을 안 써도 막히는 곳이 없다 ✅
- 토큰 캐시 · 갱신은 `ManagedIdentityCredential` 이 안에서 한다. 단, 인스턴스 하나를 재사용해야 한다 — 문서에 「처음 쓸 때 만들고 재사용」으로 적혀 있다 ✅
- 동시 첫 요청은 토큰 요청이 겹칠 수 있지만 해는 없다. 닫는 때는 W6.

### 8 — 예약 폴더

`identity` · `before-after` 는 「이름만 예약」이다. 세부 경로 · 암호화 · 보관 · 열람 기록은 그 기능 때 정한다(`spec-000:1089` · 용도 표). SPEC-000 의 「법적 검토 필요」(`:1085`)를 그대로 뒀다. 민감정보 암호화 규칙(`:108` — 주민 · 외국인 · 여권 **번호**)과도 부딪히지 않는다(파일 암호화는 그 기능 때 정하는 일). 구현을 미리 정한 곳은 없다 ✅

### 9 — 수용 항목

| 항목 | 판정 |
|---|---|
| C-A26 | 통과 · 실패를 가른다. 「컨테이너 없음」 · 토큰 상한 문구는 W1 · W7 |
| C-A27 | 실물 몫이 나뉘어 있다(① 워커 · 코디 / ② 사용자) ✅ — 확인 항목 보강은 W7 |
| Delivery A12 ~ A14 | C-A26 · C-A27 ① · ② 와 1:1 · 값 없음 · Non-Goals(신분증 · 전후 사진 기능 · 옛 키 · 로컬 Blob · 설정 변경 · 컨테이너 분리 · soft delete)가 미결과 맞다 ✅ |

### 10 — WP-BE-4 고칠 파일 · 앱 변경 없음

- 직접 grep 한 낱말: `chat_blob` · `chat-blob` · `CHAT_BLOB` · `from_connection_string` · `KEY_PATTERN` · `new_key` · `check_key` · `DAY_BLOB` · `azure-identity`. 이 낱말이 나오는 파일 전부가 고칠 파일에 있다 ✅
- 빠진 확인 자리는 `routers/api/chat.py` 의 스트림(W3)과 금지 목록(W5)이다.
- 「앱 변경 없음」은 참이다. 재생 화면 글자는 W2 에서 스펙에 적기만 하면 된다.

### 11 — 옛 문장

- `products/day` 에서 연결 문자열 · `chat-blob` · `DAY_CHAT_BLOB_*` · 「선택 비밀 3」 · `chat/{hospital_id}` 는 모두 취소선이거나, 「없음 · 대체」를 설명하는 문장에만 남았다 ✅
- 다른 SPEC · `mobile-deployment.md` 의 「선택 비밀」은 APNs · Soniox 만 말해 맞다 ✅
- 코드 쪽 `dev.env:22-26` · `prod.env` 주석의 「연결 문자열 · Blob 아직 없다」는 WP-BE-4 가 고칠 대상에 들어 있다.

## lint

```
python3 scripts/lint-pipeline.py --strict   → exit 0 · 0 error, 263 warning
products/day/ 범위: ERROR 0 · WARN 0
```
