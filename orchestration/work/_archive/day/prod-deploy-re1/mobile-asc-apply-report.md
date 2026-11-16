# [mobile] ASC-2 — 정식 DAY 0.1.0 ASC 빈칸 API 입력 결과 보고

## 상태: done — 연령 등급 · 콘텐츠 권리 · 저작권 · 가격 · 판매 지역 **API 입력 + GET 대조 완료**. App Privacy 는 **공개 API 없음** → 아래 「ASC 웹에서 사용자가 할 것」

- 앱: DAY `day.medisolveai` (6833456680 · bundleId GET 확인 뒤에만 씀). DAY Dev 손대지 않음.
- 하지 않음: 심사 제출 · Unlisted 신청 · 빌드 · 설명/키워드/URL 변경 · 키 출력.
- 원천: `mobile-asc-answers.md` + 사용자 결정(2026-11-12 「추천대로 · 소니옥스는 스트림만 · 접속 IP 수집 안 함」).

## API 로 넣은 것 · GET 대조

| 항목 | API 호출 | 결과 | GET 대조(입력 뒤) |
|---|---|---|---|
| 연령 등급 설문 | `PATCH /v1/ageRatingDeclarations/bab0fc09-…` | 200 | `messagingAndChat = true` · `userGeneratedContent = false` · `medicalOrTreatmentInformation = INFREQUENT_OR_MILD` · `parentalControls` · `ageAssurance` · `unrestrictedWebAccess` · `socialMedia` · `advertising` · `healthOrWellnessTopics` · `gambling` · `lootBox` = **false** · 그 밖 12칸(욕설 · 공포 · 술/담배/약물 · 성적 2칸 · 선정 · 폭력 3칸 · 무기 · 모의 도박 · 콘테스트) = **NONE** · override 3칸 `NONE` · `kidsAgeBand` null — **입력값과 같음** |
| **연령 등급 결과(ASC 계산)** | — | — | appInfo `appStoreAgeRating = TWELVE_PLUS`(12+) · `brazilAgeRating = TWELVE` · `brazilAgeRatingV2 = SELF_RATED_TWELVE` · `koreaAgeRating = null` · 호주/프랑스 null. ※ 새 등급 체계(13+ 등)의 화면 표시는 ASC 웹에서 한 번 보길 권함 — API 의 `appStoreAgeRating` 칸은 예전 체계 값(12+) |
| 콘텐츠 권리 | `PATCH /v1/apps/6833456680` `contentRightsDeclaration` | 200 | **`USES_THIRD_PARTY_CONTENT`** |
| 저작권 | `PATCH /v1/appStoreVersions/e0ae563c-…` `copyright` | 200 | **`2026 Medisolve AI Co., Ltd.`** |
| 가격 | `POST /v1/appPriceSchedules`(기준 지역 KOR · 수동 가격 1개 = KOR 가격 포인트 customerPrice 0 · 시작일 없음 = 지금부터) | 201 | baseTerritory **KOR**(KRW) · manualPrices 1개 = **customerPrice 0 · proceeds 0** · start/end 없음 → **무료** |
| 판매 지역 | `POST /v2/appAvailabilities`(175개 지역 전부 명시 · KOR 만 available · 새 지역 자동 포함 끔) — 첫 시도는 KOR 하나만 보내 409(「모든 지역을 포함하라」) → 전부 명시로 다시 보내 201 | 201 | `availableInNewTerritories = false` · 지역 175개 중 available = **['KOR'] 하나** · KOR `contentStatuses = CANNOT_SELL · AVAILABLE_FOR_SALE_UNRELEASED_APP`(아직 출시 전 앱이라 판매 불가 상태로 보임 — 출시 · Unlisted 뒤 바뀌는지 확인 필요) |
| (참고) 그대로인 것 | — | — | 버전 0.1.0 `PREPARE_FOR_SUBMISSION` · `releaseType MANUAL` · 연결 빌드 `21071da9-…`(빌드 2) · `isOrEverWasMadeForKids false` |

로그 · 스크립트: 세션 scratchpad(`asclib.py` · `age.py` · `rest.py` · `avail.py` · `verify.py`) — 키 값은 파일 · 출력에 없음(credentials 에서 읽기만).

## App Privacy — API 불가 → ASC 웹에서 사용자가 할 것

`GET /v1/apps/{id}/dataUsages` → 404 「The relationship 'dataUsages' does not exist」 — App Store Connect **공개 API 에 App Privacy 가 없다**. 억지로(비공개 API) 하지 않았다.

### 클릭 순서 (App Store Connect 웹 · 영어 화면 기준 · 한국어 화면이면 같은 자리)

| # | 어디서 | 누를 것 · 고를 것 |
|---|---|---|
| 1 | appstoreconnect.apple.com → **Apps** → **DAY** | (DAY Dev 아님 확인) |
| 2 | 왼쪽 메뉴 **App Privacy**(앱 개인정보 보호) | Privacy Policy URL 이 `https://day.medisolveai.com/privacy` 인지만 보고 바꾸지 않음 |
| 3 | Data Collection 의 **Get Started** | 질문 「Do you or your third-party partners collect data from this app?」 → **Yes, we collect data from this app** → **Next** |
| 4 | 데이터 종류 체크 화면 | 아래 「체크할 칸」 표의 **7개만** 체크 → **Save** |
| 5 | 목록에 생긴 각 종류마다 **Set Up**(7번 반복) | (a) 목적: **App Functionality** 만 체크 → Next · (b) 「Is … linked to the user’s identity?」 → **Yes** → Next · (c) 「Do you or your third-party partners use … for tracking purposes?」 → **No** → **Save** |
| 6 | 7개 모두 Set Up 끝 | 화면 오른쪽 위 미리보기(Product Page Preview)에 「Data Linked to You」 아래 7개 · 「Data Used to Track You」 없음 확인 |
| 7 | 오른쪽 위 **Publish** | 게시(심사 제출과 별개) |

### 체크할 칸 (7개) — 모두 목적 App Functionality · Linked Yes · Tracking No

| 분류(화면 묶음) | 체크할 칸 | 근거 |
|---|---|---|
| Contact Info | **Email Address** | 로그인 이메일 → `account.email`(`backend/day/services/auth.py:337-347`) |
| Contact Info | **Name** | 직원 이름 → `account.name`(같은 줄) |
| Identifiers | **User ID** | 계정 · 직원 id(`backend/day/models/staff.py:83-98`) |
| Identifiers | **Device ID** | 설치 id · 푸시 토큰 · 기기 종류(`app/lib/state/push_coordinator.dart:156-162`) |
| User Content | **Emails or Text Messages** | 직원 채팅 글(`backend/day/models/misc.py:245`~) |
| User Content | **Photos or Videos** | 채팅 사진 · 동영상(`backend/day/services/chat_storage.py`) |
| Usage Data | **Product Interaction** | 업무 조작 이력 · 읽음(`backend/day/services/board.py:183-186`) — 사용자 결정 「신고」 |

### 체크하지 않을 칸 (사용자 결정 · 근거)

| 칸 | 이유 |
|---|---|
| Health & Fitness › Health | 사용자 결정 「신고 안 함」 — 고객 시술 정보는 서버가 EMR 에서 받는 것 · 앱이 건강 데이터를 입력/업로드하지 않음 |
| User Content › Audio Data | 사용자 결정 「신고 안 함」 — 통역 음성은 Soniox 실시간 스트림만 · DAY · Soniox 저장 없음(Apple 「collect」 정의 밖) |
| (접속 IP · 서버 로그) | 사용자 결정 「수집 안 함」 — 해당 칸(Coarse Location 등) 체크 안 함 |
| Diagnostics 3칸 · Location · Contacts · Financial · Browsing · Search History · Purchases · Sensitive Info · Customer Support · Other User Content · Other Data | 수집 안 함(코드 근거 — `mobile-asc-answers.md` §1-3) |

## 남은 것 · 주의

1. **App Privacy 웹 입력 · Publish**(사용자) — 위 표대로. 끝나면 심사 제출 전 상태 「Published」 확인.
2. 연령 등급 결과: API 값 12+(TWELVE_PLUS). 새 체계 화면 값(13+ 일 수 있음)은 ASC 웹에서 확인.
3. 판매 지역 KOR 상태가 지금 `CANNOT_SELL` 를 함께 가짐 — 출시 전이라 그런 것으로 보이나 제출 화면에서 경고가 나오면 알려 주기.
4. 심사 제출 · Unlisted 신청 · 데모 계정 · 심사 메모 블록 B 는 손대지 않음(사용자 · 코디 몫).
