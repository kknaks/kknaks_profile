
# [mobile] TestFlight 준비 — 개발용 Bundle ID 등록 + 앱 아이콘

너는 **day `mobile` 워커**다. **너는 앞 판의 맥락이 없다** — 아래 「읽을 것」만으로 시작한다.

먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/roles/day/mobile/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

지금 이 워크트리에서 일하는 다른 워커는 없다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix/AGENTS.md` — 레포 구조 · 규칙
- `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix/app/README.md` — 빌드 설정(`--dart-define`) · iOS 구조
- `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/40-architecture/mobile-deployment.md` — 앱 배포 계약(읽기만)
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/config/projects/day.json` 의 `apple` 섹션 — Apple 설정이 어디 있는지
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/_archive/day/day-app/_RESUME.md` 머리 「Apple」 줄 — 앞 판이 한 것

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

DAY 직원 앱을 TestFlight 에 **개발 버전 먼저** 올린다(사용자 2026-11-11). 개발 / 정식 두 앱으로 나눈다.

| | Bundle ID | 이름 | 붙는 서버 |
|---|---|---|---|
| 개발 | `day.medisolveai.dev` | `DAY Dev` | day-dev |
| 정식 | `day.medisolveai` | `DAY` | prod (나중) |

지금 상태(코디가 2026-11-11 App Store Connect API 로 직접 조회):

- Bundle ID 는 `day.medisolveai` 하나만 등록돼 있다(푸시 활성). `day.medisolveai.dev` 는 **없다**.
- App Store Connect 앱 record 는 DAY 로 하나도 없다 — 이건 사용자가 웹에서 만든다(네 몫 아님).
- `app/ios/Runner/Assets.xcassets/AppIcon.appiconset/` 에 `Contents.json` 만 있고 **이미지가 없다.** 아이콘이 없으면 업로드 검증에서 거절된다.
- Xcode 프로젝트는 `PRODUCT_BUNDLE_IDENTIFIER = $(DAY_BUNDLE_ID)` · `CODE_SIGN_STYLE = Automatic` · `DEVELOPMENT_TEAM` 없음.

이번 발주는 **올리기 직전까지의 준비 둘**이다. 서명 · 아카이브 · 업로드는 이번에 하지 않는다.

## 3. 계약

해당 없음(서버 · 화면 계약 변경 없음).

## 4. 먼저 읽을 핵심 파일

- `app/ios/Runner.xcodeproj/project.pbxproj` — `DAY_BUNDLE_ID` · `DAY_DISPLAY_NAME` 이 어디서 오는지(xcconfig · 빌드 인자)
- `app/ios/Flutter/*.xcconfig` · `app/ios/Runner/Info.plist` — 번들 ID · 표시 이름 · 아이콘 이름
- `app/ios/Runner/Assets.xcassets/AppIcon.appiconset/Contents.json` — 지금 선언된 아이콘 칸
- `app/lib/ui/theme.dart:7` — 앱 메인 색 `Ms.primary = 0xFF1D8BFF` (웹 `backend/day/styles/app.css:31` `--ms-primary: #1d8bff` 와 같다)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/ios/Runner/Assets.xcassets/AppIcon.appiconset/` (이미지 추가 · `Contents.json`)
- `app/assets/brand/` (아이콘 원본 SVG 1개 — 새 폴더)
- `app/README.md` (아이콘 원본 · 다시 만드는 법 · 개발/정식 빌드 인자 몇 줄)
- 번들 ID · 표시 이름을 빌드 인자로 바꾸는 데 **꼭 필요할 때만** `app/ios/Flutter/*.xcconfig` · `app/ios/Runner/Info.plist` · `project.pbxproj` — 이미 되면 손대지 않는다
- 레포 밖: `~/.config/day/apple/credentials.local.json`(아래 6-A 의 `dev_app` 칸 추가만) · 리포트 1개(아래 §9)

## 6. 구현 단계

### A. 개발용 Bundle ID 등록 (App Store Connect API)

1. 자격은 `~/.config/day/apple/credentials.local.json` 의 `app_store_connect.key_id` · `issuer_id` · `private_key_path` 로 읽는다. JWT(ES256 · aud `appstoreconnect-v1` · 10분)는 스크립트 프로세스 안에서만 만들고 **Key ID · Issuer ID · Team ID · 키 내용 · 토큰을 화면 · 리포트 · 로그에 출력하지 않는다.** 스크립트는 네 scratchpad 에 두고 레포에 넣지 않는다. (`uv run --with pyjwt --with cryptography python <스크립트>` 로 된다 — 코디가 조회에 쓴 방식.)
2. 먼저 `GET /v1/bundleIds` 로 `day.medisolveai.dev` 가 없는지 다시 확인한다. 이미 있으면 만들지 말고 그 상태를 쓴다.
3. `POST /v1/bundleIds` — identifier `day.medisolveai.dev` · name `DAY Dev` · platform 은 기존 `day.medisolveai` 와 같은 값.
4. `POST /v1/bundleIdCapabilities` — `PUSH_NOTIFICATIONS`. 기존 `day.medisolveai` 에 켜진 capability 목록을 조회해 **같은 것만** 켠다(더 켜지 않는다).
5. 다시 조회해 등록 · capability 를 확인한다.
6. `credentials.local.json` 에 `dev_app` 칸을 **추가**한다 — `{ "bundle_id", "app_name", "bundle_resource_id", "push_notifications_enabled" }`. 기존 칸은 한 글자도 바꾸지 않는다. 파일 권한 600 유지.

기존 `day.medisolveai` 는 조회만 한다 — 수정 · 삭제 금지. 앱 record · 인증서 · 프로비저닝 프로파일 · 기기 등록은 만들지 않는다.

### B. 앱 아이콘

1. 원본: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/assets/icon-source.svg` (512×512 · 도형 하나 · `fill="#6F21FF"` · 배경 투명).
2. **색만 바꾼다**(사용자) — 도형 fill 을 앱 메인 색 `#1D8BFF` 로. 도형 모양 · 비율 · 위치는 그대로.
3. iOS 아이콘은 투명을 못 쓴다 → 배경은 **흰색 `#FFFFFF` 불투명**. 도형 크기 · 여백은 원본 그대로(원본이 512 안에서 차지하는 비율 유지). 그림자 · 그라데이션 · 글자를 넣지 않는다.
4. 색 바꾼 SVG 를 `app/assets/brand/app-icon.svg` 로 둔다(원본 1개).
5. `AppIcon.appiconset` 을 채운다 — `Contents.json` 이 선언한 칸 전부(아이폰 · 아이패드 · 1024 마케팅). 1024 는 **알파 채널 없는** PNG. 파일 이름을 `Contents.json` 의 `filename` 에 적는다. 선언된 칸이 요즘 Xcode 기준으로 부족하거나 넘치면 고치되, 왜 그랬는지 리포트에 적는다.
6. 개발 / 정식 아이콘은 **같은 것**을 쓴다 — 개발용 띠 · 배지를 지어 넣지 않는다.
7. `app/README.md` 에 원본 위치와 다시 만드는 명령을 몇 줄 적는다.

### C. 개발 빌드 인자 확인

1. `DAY_BUNDLE_ID=day.medisolveai.dev` · `DAY_DISPLAY_NAME=DAY Dev` 를 **빌드 인자로만** 넣어 서명 없는 빌드가 되는지 확인한다(소스 기본값을 dev 로 바꾸지 않는다).
2. 산출물 `Runner.app/Info.plist` 의 `CFBundleIdentifier` · `CFBundleDisplayName` 과 아이콘이 들어갔는지(`Assets.car` · `CFBundleIcons`) 확인한다.
3. 서명 아카이브 → IPA → 업로드에 **쓸 명령을 리포트에 적기만 한다**(실행하지 않는다). Team ID 는 `credentials.local.json` 의 `team_id` 에서 읽게 쓰고 값을 적지 않는다. 서버 주소는 `<dev 공개 주소>` 자리표시로 둔다.

## 7. 범위 제약 — 하지 말 것

- 서명 빌드 · 아카이브 · `altool` 업로드 · 앱 record 생성 · 인증서 · 프로파일 생성 **금지**.
- 서버(`backend/` · `deploy/` · `scripts/`) · Dart 코드(`app/lib/` · `app/test/`) 수정 금지.
- 화면 문구 · 앱 이름을 지어 넣지 않는다 — 이름은 위 표의 `DAY Dev` · `DAY` 뿐.
- 사용자 포트(로컬 11040) · 프로세스 · 시뮬레이터 · 실기기를 건드리지 않는다.
- Key ID · Issuer ID · Team ID · 키 내용 · 토큰 · 고객 값을 출력 · 기록하지 않는다. profile 레포는 PUBLIC 이다.
- 커밋 · push · PR 금지.

## 8. 검증

```
cd app && fvm flutter analyze                      # 1회
cd app && fvm flutter build ios --no-codesign --dart-define=… (6-C 의 dev 인자)   # 1회
```

- `flutter test` 전체는 이번엔 돌리지 않는다(Dart 변경 없음). Dart 를 건드렸다면 범위를 넘은 것이다 — 멈추고 물어라.
- A 는 등록 뒤 재조회 결과(identifier · name · capability 이름)로 증명한다.
- B 는 `Contents.json` 의 모든 칸에 파일이 있는지 · 각 PNG 의 픽셀 크기가 칸과 맞는지 · 1024 에 알파가 없는지(`sips -g hasAlpha`)를 표로 낸다.
- 실행 못 한 검증은 사유와 함께 pending.

## 9. 완료 보고 — **문구 변경 금지**

리포트를 먼저 파일로 쓴다: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/app-testflight-prep-report.md`
(변경 파일 · A 재조회 결과 · B 아이콘 표 · C 산출물 확인 · 업로드에 쓸 명령 · 정할 것 · pending)

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_8fae9ebc-816d-4674-970b-4107e45084ff \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
