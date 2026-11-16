# 리뷰 리포트 — fix 1판 / code (2026-11-11)

검수 대상: `CENTURION_DAY/fix`(`kknaksss/fix`) 미커밋 변경 전부 — `git diff origin/dev`(5 파일) + untracked(`app/assets/brand/app-icon.svg` · 아이콘 PNG 15).
read-only. Key ID · Team ID 값은 이 리포트에 옮기지 않는다.

## 판정: WARN

FAIL 0 · WARN 2. 머지 자체를 막을 결함은 없다. dev 서버 기동 · 앱 로그인 · 중간 상태(APNs 키 없음 · 저장소 빔)의 동작을 코드로 따라가 봤고 500 · 기동 실패가 날 자리는 없다.
다만 로그인 응답 계약을 보는 유일한 시험이 이번 검수에서도, 배포 경로에서도 실제로 돌지 않았다(W1).

## FAIL

없음.

## WARN

### W1. 「dev + 공개 주소 → 앱 로그인 응답 `api_base_url` · `environment=dev`」 시험이 이번 판에서 한 번도 안 돌았다
- `backend/tests/day/auth/test_environments_api.py:26` `pytestmark = pytest.mark.infra` → 지시된 명령에서 **6 skipped**(사유: `DAY_TEST_DATABASE_URL · DAY_TEST_REDIS_URL 없음`). 작성자도 `tests/deploy` 만 돌렸다(be-dev-env-report 「검증」).
- `.github/workflows/deploy-dev.yaml:7-9` — `dev` push 가 곧 배포이고, 워크플로 어디에도 `scripts/test.sh` 가 없다(`grep test.sh .github/workflows/*` 0건). 이번 수정의 목적(TestFlight 앱 `environment_unavailable` 해소 · DAY-SPEC-001 §3)을 증명하는 시험 `:58` `test_앱_로그인_응답에_자기_환경과_공개_주소_웹은_없음` 이 머지 전에 돌았다는 기록이 없다.
- 코드 경로는 맞다(아래 「따라간 경로」). 그래도 AGENTS.md 「테스트」 — 커밋 전 `scripts/test.sh`(전부). 커밋 전 코디가 `scripts/test.sh -q` 를 한 번 돌려 위 6건이 passed 인지 확인할 것. (리뷰어는 사용자 로컬 compose DB 를 쓰지 않아 돌리지 않았다.)

### W2. 저장소에 Team ID 가 들어갔는데 「저장소 어디에도 넣지 않는다」 문서 · 열린 결정이 그대로다
- `deploy/config/dev.env:29-30` — Key ID · Team ID 값(형식 10자 대문자영숫자 · 비밀 아님 · 사용자 확인 · 브리프 A 허용). 값 자체는 지적하지 않는다.
- 그런데 같은 저장소의 `app/README.md:164` 「Apple Team ID · 서명 값 · provisioning 을 저장소에 넣지 않는다(mobile-deployment M-16)」, `app/ios/Flutter/Identity.xcconfig:4` 「Apple Team ID · 서명 값은 여기에도, **저장소 어디에도** 넣지 않는다」, spec `mobile-deployment.md:38 · :128 · :294`(M-16 [미결]: 저장소에 어디까지 기록할지)가 바뀌지 않았다.
- 서버 APNs 설정(`common/config.py` 의 `day_apns_team_id` 는 원래 env 이름 칸)과 앱 서명(`DEVELOPMENT_TEAM`)은 다른 자리라 규칙 위반으로 보진 않는다. 다만 문구가 「저장소 어디에도」라 다음 리뷰 · 워커가 FAIL 로 읽거나 지우려 할 수 있다. `_RESUME.md` §2 에 「서버 `dev.env` 의 APNs Key/Team ID 는 저장소 허용(2026-11-11 사용자)」 한 줄 + M-16 범위(앱 서명만) 정리 필요 — 코드 수정이 아니라 결정 기록.

## 따라간 경로 — dev.env 가 머지 · 배포될 때

| 단계 | 코드 | 결과 |
|---|---|---|
| 일반 설정 검사 | `scripts/deploy/day_vm.py:115-126` `validate_config` · `:54-57` 금지 키(`SECRETS` · `OPTIONAL_SECRETS` · `REDIS_PASSWORD` · `DAY_LOCAL_`/`SEED_`/`TEST_` 접두어) | 바뀐 칸(`DAY_PUBLIC_API_BASE` · `DAY_APNS_*`)은 금지 목록 밖 → 통과. 값에 `'` · 줄바꿈 없음(`render_env` `:104-112`) |
| 기동 설정 | `backend/common/config.py:186-193` `_public_base_is_origin` | `https://day-dev.medisolveai.com` 은 `normalize_origin` 통과 → 기동 실패 없음. `DAY_APNS_KEY_ID` · `TEAM_ID` 는 검증자 없음(빈 키와 섞여도 기동 됨) |
| 앱 로그인 응답 | `config.py:245` `public_api_origin` → `day/services/environments.py:117` `own_target` → `day/routers/api/auth.py:58 · 70 · 82` → `schemas/auth.py:52 · 62` | 앱 로그인 · 병원 고르기 응답에 `environment=dev` · `api_base_url=https://day-dev.medisolveai.com` |
| 앱 수락 | `app/lib/state/session_controller.dart:269-289` `_targetFrom` | release(`requireEnvironment`) 는 두 칸 다 있어야 통과 → 이제 둘 다 실림. 허용 origin 은 업로드 빌드 `DAY_ALLOWED_ORIGINS` 와 같은 주소 |
| 도메인 정합 | `deploy/config/edge.env` `DAY_DEV_DOMAIN` · `docs/development/deployment.md:14` | 같은 호스트 |
| 기기 등록 | `day/services/devices.py:49-56` `check_app_id` ← `config.py:265` | 앱 `app_id` = 네이티브 번들 id(`app/lib/data/push_bridge.dart:27`) = `day.medisolveai.dev` → 200. 정식 번들은 dev 에서 400(의도) |
| 채팅 푸시(키 없음) | `config.py:269-275` `apns_enabled`(키 본문 · Key ID · Team ID 셋 다) → `day/services/push.py:280-287` | Key Vault 에 `day-dev-apns-auth-key` 가 없는 지금은 `push_log.status = skipped_no_key` 로 쌓고 INFO 로그 · 예외 없음. 메시지 보내기는 그대로 성공 |
| 선택 비밀 없음 | `day_vm.py:222-238` `read_optional_key_vault` | 404 는 건너뜀 → 배포 계속. 그 밖 오류(403 등)는 배포가 멈춘다 |
| 키 형식(나중) | `day_vm.py:184-195` `optional_app_env`(줄바꿈 → `\n`) ↔ `apns.py:52`(되돌림) | 여러 줄 PEM 그대로 Vault 에 넣으면 맞음(작성자 확인과 같음) |
| 첨부(저장소 빔) | `day/services/chat_storage.py:190-198` `storage_from` → None | 409 `photo_disabled`(fail-closed) · 기동 영향 없음 |

## 시험 계약 변경 — 느슨해졌나

`backend/tests/deploy/test_chat_env_contract.py`

- 이전: dev · prod 모두 `SERVER_NAMES` 다섯 칸 `== ""`, `DAY_CHAT_STORAGE != "disk"`.
- 지금:
  - 공통(`:62-72`): 칸 존재 · 비밀 키 없음 · 저장소 `("", "blob")`(이전 `!= "disk"` 보다 **좁음**) · 저장소/컨테이너 같이 참/같이 빔(**새로 생김**) · Key/Team ID 는 빈 값 또는 `[A-Z0-9]{10}`(값은 실패 메시지에 안 실음 — 키 이름만).
  - prod(`:75-78`): 다섯 칸 전부 `== ""` **그대로 묶임**.
  - dev(`:81-90`): 허용 앱 = 개발 번들 하나(정확 일치) · Key/Team ID 함께 · 공개 주소 정규화 = dev 도메인 · 데모 두 칸 빈 값.
- 판단: 느슨해지지 않았다. 공통 단언이 `== ""` → `in config` 로 약해진 몫은 prod 전용 시험과 dev 전용 시험이 각각 다시 묶는다.
- 참고: `:88` 이 dev 도메인을 문자열로 고정한다. 하드코딩된 주소라기보다 설정 파일을 고정하는 계약 시험이다. 도메인이 바뀌면 `edge.env` · `dev.env` · 이 시험 세 곳을 같이 고쳐야 한다.

## 조용히 통과하는 자리

1. **infra 시험 skip**(W1): `uv run pytest tests/day/auth/test_environments_api.py` 는 DB env 가 없으면 실패가 아니라 skip 이다(`DAY_REQUIRE_INFRA=1` 은 `scripts/test.sh` 만). 명령은 초록이지만 로그인 응답 계약은 확인하지 않은 상태다.
2. **APNs 반쪽 설정**: Key ID · Team ID 가 있고 키 본문(Vault)이 없는 지금은 `apns_enabled=False` → `skipped_no_key`. 오류도 경고도 없이 INFO 로그 한 줄이다. 의도된 fail-closed 지만, Vault 에 키를 넣어도 **재배포 전에는** 계속 skip 이다(키는 배포 때 app.env 로 실림).
3. `test_dev_…:86` `bool(KEY_ID) == bool(TEAM_ID)` 는 둘 다 비어도 통과한다. dev 에서 두 칸이 지워져도 시험은 초록이다. 결과는 위 2와 같은 skip 이라 위험은 낮다(의도로 봄).
4. 공통 시험의 Key/Team ID 형식 검사는 빈 값을 허용한다. prod 는 `:78` 이 따로 막는다.

## 비밀값

- diff + untracked 전부를 IPv4 · `BEGIN`/`PRIVATE` · `AccountKey`/`DefaultEndpoints` · `/subscriptions/` · JWT(`eyJ`) · `password`/`secret`/`token=` 로 훑었다 → 0건.
- `dev.env` 의 비밀 칸(`DAY_CHAT_BLOB_CONNECTION_STRING` · `DAY_APNS_AUTH_KEY`)은 없다 → `day_vm.py` 금지 키 검사에 안 걸린다(작성자 dry-run exit 0 과 같은 결론).
- `DAY_ADMIN_EMAILS` 줄은 이번 diff 가 아니다(기존).
- `app/README.md` 에는 번들 id · 표시 이름 · 색 · 명령만 있다. 비밀값은 없다.

## 앱

| 항목 | 확인 | 결과 |
|---|---|---|
| `Info.plist` 키 | diff = `ITSAppUsesNonExemptEncryption` `<false/>` 한 키(+2줄) · `plutil -lint` OK | PASS |
| `false` 근거 | `pubspec.yaml:13-24` 직접 의존 중 암호 계열은 `crypto` 하나 · `lib/interpret/interpret_client.dart:14,82` `sha1`(WS `Sec-WebSocket-Accept` 검증) · `ios/Runner/AppDelegate.swift:222-227` Keychain `SecItem*` · `lib` · `ios/Runner` · `pubspec*` 에 `pointycastle`/`encrypt`/`cipher`/`CryptoKit`/`CCCrypt` 0건 | 리포트 근거와 같음. 면제(TLS · OS Keychain · 해시) |
| 아이콘 세트 | `Contents.json` 19칸 전부 `filename` 있음 · 15 PNG(같은 픽셀은 공유) · `sips` 로 칸마다 픽셀 = size×scale(20@1 … 83.5@2=167 · 1024) · `hasAlpha=no` 19/19 | PASS |
| 아이콘 원본 | `app/assets/brand/app-icon.svg` 512 · 흰 `rect` 불투명 · `#1D8BFF` 도형 1개 · `pubspec` 에 asset 으로 선언 안 됨(번들에 안 들어감) | PASS(흰 배경은 `_RESUME` §2 「사용자 확인 전」 그대로) |
| Bundle ID 소스 기본값 | `ios/Flutter/Identity.xcconfig:5` `com.example.day.placeholder` 그대로 · `pbxproj` `$(DAY_BUNDLE_ID)` · `Info.plist:10,18` `$(DAY_DISPLAY_NAME)` · `lib`/`ios` 에 `medisolveai` 0건 · `Identity.local.xcconfig` 는 `ios/.gitignore:37` | PASS — dev 값이 소스에 박히지 않음 |
| README 사실 | 번들 · 이름 표 = `_RESUME` §2 결정 · xcconfig `#include?` 경로 · `.gitignore` 일치 · `--dart-define` 이 아님 맞음 | PASS. 단 SDWebImage `CC_MD5` 언급은 `Podfile.lock` 이 저장소에 없어 이 레포만으로는 확인 불가(참고) |

## 범위

- 변경 경로 = `app/README.md` · `app/ios/Runner/Info.plist` · `AppIcon.appiconset/` · `app/assets/brand/` · `deploy/config/dev.env` · `backend/tests/deploy/test_chat_env_contract.py` — 브리프 3개(fix-app §5 · export-compliance 2 · be-dev-env §4)의 allowed_paths 안. `prod.env` · `backend/` 앱 코드 · `scripts/` · `.github/` · `app/lib` 무변경.
- 화면 문구를 새로 지어 넣은 곳은 없다. 이름은 `DAY Dev` · `DAY` 뿐이다(README 표).
- `dev.env` 주석 변경은 상태가 바뀐 줄만 고쳤다(「사용자가 직접 넣는다」 → 승인 날짜, 「배포 연결은 후속」 → Vault 이름). 사실과 맞는다(`day_vm.py:47-52`).

## 직원이 실물에서 만날 자리

- 머지 · 배포 뒤 TestFlight DAY Dev 로그인 → 통과해야 한다(지금 `environment_unavailable`).
- 알림 허용 → 기기 등록은 된다. 하지만 **채팅 푸시는 안 온다**(Vault 키 없음 → `skipped_no_key`). 키를 넣은 뒤 **dev 재배포**가 있어야 온다.
- 채팅 사진 첨부는 409 `photo_disabled` 다(Blob 미정). 텍스트 메시지는 된다.
- 알림이 안 오는 이유가 화면에 드러나지 않는다. 실기기 확인 때 `push_log.status` 로 봐야 한다.

## 참고(기존 부채 · 범위 밖)

- `deploy/config/prod.env` 주석 「서버 app.env(Key Vault) 몫(사용자 설정 · **배포 연결은 후속**)」은 이제 사실과 다르다. 배포 연결은 `day_vm.py` `OPTIONAL_SECRETS` 에 이미 있다. prod.env 는 이번 범위 밖이라 다음 판에.
- PR 게이트에서 테스트를 돌리는 워크플로가 없다(W1 의 뿌리). AGENTS.md 「CI 는 `scripts/test.sh` 만 쓴다」와 `.github/workflows/` 가 어긋난다.

## 돌린 명령 · 수치(각 1회)

| 명령 | 결과 |
|---|---|
| `cd backend && uv run pytest -q tests/deploy tests/day/auth/test_environments_api.py` | **96 passed, 6 skipped**(skip 6 = `test_environments_api.py` 전부 · infra env 없음) |
| `cd backend && uv run ruff check tests/deploy/test_chat_env_contract.py` | All checks passed! |
| `cd app && fvm flutter analyze` | No issues found! |
| `plutil -lint app/ios/Runner/Info.plist` | OK |
| `sips` 아이콘 19칸(픽셀 · 알파) | 19/19 OK · 알파 0 |
| diff 비밀값 패턴 grep | 0건 |
