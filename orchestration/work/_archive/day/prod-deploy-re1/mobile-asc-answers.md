# [mobile] ASC-1 — 정식 DAY 0.1.0 ASC 빈칸 답안 (App Privacy · 연령 등급 · 가격 · 판매 지역 · 저작권 · 콘텐츠 권리)

## 상태: done — 답안만. **ASC 에 쓴 것 0**(GET 만)

- 코드 기준: `CENTURION_DAY/prod-deploy-re1` HEAD `79e730b5`(= 정식 빌드 2 의 소스).
- 판정 표시: **확실** = 코드 · Apple 문서 · ASC GET 으로 확인한 사실 / **제안** = 사실을 바탕으로 한 권장 답(사용자 승인 필요) / **확인 필요** = 사용자 · 서버 쪽이 정해야 함(지어 내지 않음).
- ASC 현재 값(GET 2026-11-12): `contentRightsDeclaration = null` · 버전 `copyright = null` · 연령 등급 설문 칸 **전부 null**(override `NONE`) · 가격 일정 · 판매 지역(`appAvailabilities`) **404 = 아직 없음** · `isOrEverWasMadeForKids = false`.

---

## 0. 사용자 가설 검증 — 「앱이 새로 수집하는 건 직원 채팅뿐 · 나머지는 EMR 조회」

**결론: 대체로 맞지만 더 있다.** 채팅(글 · 사진 · 동영상) 말고도 앱이 서버로 보내고 서버가 **보관**하는 것이 있다.

| 앱이 보내는 것 | 서버 보관 | 근거(파일:줄) |
|---|---|---|
| 채팅 글 | `chat_message.body` | `backend/day/models/misc.py:245`~ (`body` Text · `account_id`) |
| 채팅 사진 · 동영상(파일 첨부는 **없음** — 종류 = photo · video 둘뿐) | `chat_attachment`(Blob `file_key` · 크기 · 해시 · 가로세로 · 길이) | `backend/day/enums/misc.py:71-73` · `models/misc.py:275`~ · `app/lib/chat/chat_api.dart`(`/api/chat/photos` · `/api/chat/videos`) |
| 로그인 이메일 · 비밀번호 | 이메일 = `account.email`(로그인 때 만들고 매번 갱신) · **비밀번호는 저장 안 함**(KOS 로 확인만) · 이름도 같은 때 `account.name` 에 저장(KOS 응답 값) | `app/lib/data/day_api.dart:110-113` · `backend/day/services/auth.py:337-347` · `models/staff.py:27-28` |
| 푸시 등록: 설치 id · APNs 토큰 · 플랫폼 · 앱 id · push_env · 기기 종류(폰/태블릿) | `device`(토큰 암호화 저장 · 계정 연결) · 발송 기록 `push_log`(토큰 끝 6자) | `app/lib/state/push_coordinator.dart:156-162` · `models/misc.py:62-90 · 119-140` |
| **업무 조작**: 시술 시작 · 종료 · 되돌리기 · 의사 호출 · 수락 · 마취 · 귀가 | EMR 로 보내고(outbox) DAY 에 **업무 이력** `event_log`(누가 `actor_staff_id` · 언제 · 무엇) | `app/lib` `/api/tasks/$taskId/$action` · `/api/calls/…` · `/api/visits/…/anesthesia|home|calls` · `backend/day/services/board.py:183-186` · `models/task.py:197-203` |
| 알림 읽음 · 알림 받기 설정 · 채팅 읽은 위치 | `notification.read_at` · `notification_setting` · `chat_member.last_read_seq` | `app/lib/notify/notification_api.dart:60-68` · `models/misc.py:106 · 109-116 · 227`~ |
| 통역 마이크 음성(PCM 실시간) | **저장 안 함** — 서버 메모리 중계 → Soniox 실시간 API → 끝나면 사라짐 | `backend/day/services/interpret/session.py:1-11`(「통역 기록기 옮기지 않음 — 메모리에서 세션과 함께 사라진다」) · `soniox.py:26-27`(실시간 WS 둘만) |
| 그 밖 | 위치 · 연락처 · 광고 id 없음(Info.plist 권한 = 카메라 · 사진 · 마이크뿐) · 분석/오류 SDK 없음 · 추적 없음 | `app/ios/Runner/Info.plist:52-59` · `app/pubspec.yaml` dependencies(http · crypto · flutter_tts · record · audio_session · flutter_pcm_sound · image_picker · flutter_image_compress · photo_manager · video_player · url_launcher) · `pubspec.lock` firebase/sentry/analytics 등 grep 0 · `AppTrackingTransparency` · `advertisingIdentifier` grep 0 |

EMR 사본(고객 · 시술 · 차트)은 **서버가 EMR 에서 받아 오는 것**이고 앱이 기기에서 보내는 것이 아니다(`backend/day/services/emr_sync.py`). 앱이 고객 사진 · 신분증 · 문진을 올리는 경로는 없다(`app/lib` 에서 `id_photo` · `identity` · `questionnaire` grep 0).

---

## ① App Privacy (데이터 수집 신고)

Apple 정의(https://developer.apple.com/app-store/app-privacy-details/):
- 「“Collect” refers to transmitting data off the device in a way that allows you and/or your third-party partners to access it for a period longer than necessary to service the transmitted request in real time.」
- 「Data that is processed only on device is not “collected”」 · 인증 토큰 · IP 를 서버 호출에 실어 보내고 **보관하지 않으면** 신고 대상 아님.
- Linked: 「Data collected from an app is often linked to the user’s identity, unless specific privacy protections are put in place」 · Tracking: 사용자 · 기기 데이터를 **다른 회사 데이터(Third-Party Data)와 연결해 광고 · 광고 측정**에 쓰는 것.
- App Functionality 목적: 「to authenticate the user, enable features, prevent fraud, implement security measures, ensure server up-time …」

### 1-1. 첫 질문

| ASC 칸 | 답 | 근거 | 판정 |
|---|---|---|---|
| Do you or your third-party partners collect data from this app? | **Yes** | 위 0절 — 이메일 · 채팅 · 사진/동영상 · 기기 등록을 서버가 보관 | 확실 |
| Tracking(추적) | **No**(어떤 항목도 추적에 쓰지 않음) | 광고 · 분석 SDK 0 · ATT 없음 · 데이터 판매/브로커 없음 | 확실(코드) |

### 1-2. 신고할 데이터 종류 — 모두 「Linked to the user = Yes」 · 「Tracking = No」 · 목적 = **App Functionality** 하나

| ASC 칸(종류) | 수집 | 무엇 | 근거 | 판정 |
|---|---|---|---|---|
| Contact Info › **Email Address** | Yes | 로그인 이메일 → `account.email` | `day_api.dart:113` · `auth.py:338-345` | 확실 |
| Contact Info › **Name** | Yes | 직원 이름(KOS 로그인 응답) → `account.name` · 채팅 상대 · 보낸 사람 표시 | `auth.py:339 · 346` · `chat_model.dart:25` | 확실(저장) · 신고 = 제안(앱 입력은 아니지만 로그인으로 생기는 계정 값이라 보수적으로 신고) |
| Identifiers › **User ID** | Yes | 계정 · 직원 id(세션 · 채팅 · 업무 이력에 연결) | `models/staff.py:83-98` · `task.py:200` | 확실 |
| Identifiers › **Device ID** | Yes | 앱이 만든 설치 id(`install_id`) · APNs 토큰 · 기기 종류 | `push_coordinator.dart:156-162` · `misc.py:82-89` | 제안 — Apple 정의 「other device-level ID」 에 설치 id 가 해당한다고 보수적으로 판단 |
| User Content › **Emails or Text Messages** | Yes | 직원 채팅 글(보낸 사람 · 받는 방 · 내용) | `misc.py:245`~ | 확실(보관) · 칸 선택 = 제안(Apple 정의 「contents of the … message」 — 앱 내 메시지를 여기에 둠. **Other User Content** 로 둘 수도 있으나 메시지 정의에 더 가깝다) |
| User Content › **Photos or Videos** | Yes | 채팅 사진 · 동영상(기기에서 줄여 Blob 저장) | `chat_storage.py:1-12` · `enums/misc.py:71-73` | 확실 |
| Usage Data › **Product Interaction** | 확인 필요 — **신고 제안** | 업무 조작 이력(누가 · 언제 시술 시작/종료 · 호출 · 수락 · 마취 · 귀가) `event_log` · 알림 읽음 · 채팅 읽은 위치 | `board.py:183-186` · `task.py:197-203` · `notification_api.dart:60` | 확인 필요 — Apple 예시(「app launches, taps, clicks …」)와 딱 같지는 않지만 앱 안 행동 기록이 계정에 연결돼 보관되므로 **보수적으로 신고 권장**. 안 쓰기로 하면 사용자 결정으로 기록 |

### 1-3. 신고하지 않는 것 (답 = 수집 안 함)

| ASC 칸 | 답 | 근거 | 판정 |
|---|---|---|---|
| User Content › **Audio Data**(통역 마이크) | **수집 안 함** | 실시간 중계 · 기기 파일 저장 없음 · DAY 서버 기록 없음(`session.py:9-11`) · Soniox 실시간 API 만(`soniox.py:26-27`) · Soniox 공개 정책 「Real-time API requests are processed transiently and are not stored by Soniox.」(https://soniox.com/policies/privacy-policy §5). Apple 「collect」 정의의 「longer than necessary to service the transmitted request in real time」 에 해당하지 않음 | **제안** — Soniox 별도 계약 · DPA · Console 보관 설정은 확인 안 함(app-store-preparation §7-1 T2). 거기서 보관이 있으면 **Audio Data 신고(Linked 여부 다시 판단)** 로 바꾼다 |
| Health & Fitness › **Health** | **수집 안 함**(제안) | 고객의 시술 · 차트 정보는 **서버가 병원 EMR 에서 받아 온 것**이고 앱 사용자(직원)에게서 모으는 데이터가 아니다 · 앱은 차트 읽기만(DAY-SPEC-003 `:780`) · 앱이 건강 데이터를 입력 · 업로드하는 경로 없음. 다만 업무 조작(시술 시작 · 마취 등)이 고객 시술 상태를 바꾸어 EMR · `event_log` 에 남는다 | **확인 필요** — Apple 문서는 「다른 출처에서 받은 데이터」를 명시적으로 다루지 않는다(「data collected from your app」 만). 앱 조작이 **환자 시술 상태**를 만들어 보관한다는 점을 Health 로 볼지 사용자 판단. 보수적으로 가면 Health 신고(Linked = Yes · App Functionality) |
| Diagnostics › Crash · Performance · Other Diagnostic | 수집 안 함 | 오류 · 분석 SDK 0 · 앱이 진단 데이터를 서버로 보내는 코드 없음 | 확실(코드) |
| Location · Contacts · Financial · Browsing · Search History · Purchases · Sensitive Info · Customer Support · Other Data | 수집 안 함 | 해당 권한 · API 없음 · 채팅 상대 목록은 검색어 없이 GET(`chat_api.dart:83`) · 접근 로그는 쿼리 문자열을 지움(`backend/common/logs.py` `DropQueryString`) · 지원은 앱 밖 메일 | 확실(코드) |
| 서버 접근 로그(IP · 경로) | 신고 안 함(제안) | uvicorn 접근 줄(JSON · 쿼리 제거). 로그에 남는 client 주소가 Caddy 뒤 프록시 주소인지 실제 IP 인지 · 보관 기간 확인 안 함 | 확인 필요(§7-1 T3) — 실제 IP 를 오래 보관하면 Apple 「IP … not retained」 예외 밖 → 그때 다시 판단 |
| 비밀번호 | 신고 안 함 | 저장 안 함(KOS 확인만 · `auth.py:263-267`) · 세션 토큰은 해시만 저장(`staff.py:90`) — 인증 요청 처리용 | 확실 |

### 1-4. ASC 화면 순서대로 체크할 것(요약)

1. Collect data? **Yes**
2. 체크: Contact Info(Email Address · Name) · Identifiers(User ID · Device ID) · User Content(Emails or Text Messages · Photos or Videos) · Usage Data(Product Interaction — 확인 필요 · 권장) · [Health — 확인 필요]
3. 각 종류: 목적 **App Functionality** 만 · Linked **Yes** · Tracking **No**

---

## ② 연령 등급 설문

ASC API 칸 이름(GET · 지금 전부 null): `parentalControls` · `ageAssurance` · `unrestrictedWebAccess` · `userGeneratedContent` · `socialMedia` · `messagingAndChat` · `advertising` · `profanityOrCrudeHumor` · `horrorOrFearThemes` · `alcoholTobaccoOrDrugUseOrReferences` · `medicalOrTreatmentInformation` · `healthOrWellnessTopics` · `matureOrSuggestiveThemes` · `sexualContentOrNudity` · `sexualContentGraphicAndNudity` · `violenceCartoonOrFantasy` · `violenceRealistic` · `violenceRealisticProlongedGraphicOrSadistic` · `gunsOrOtherWeapons` · `gambling` · `gamblingSimulated` · `contests` · `lootBox` · (한국) `koreaAgeRatingOverride` · `gracRatingClassificationNumber`. 기준 문서: https://developer.apple.com/help/app-store-connect/reference/age-ratings-values-and-definitions/ (등급 4+ · 9+ · 13+ · 16+ · 18+ — 답을 넣으면 ASC 가 계산).

| ASC 칸 | 답 | 근거 | 판정 |
|---|---|---|---|
| Parental Controls | No | 해당 기능 없음 | 확실 |
| Age Assurance | No | 나이 확인 기능 없음(병원 발급 직원 계정) | 확실 |
| Unrestricted Web Access | **No** | 앱 안 브라우저 없음 · 링크는 기기 Safari 로 엶(`chat_link.dart:10` · 설정 「정보」 링크) | 확실(코드) |
| **Messaging and Chat** | **Yes** | 직원 채팅(1:1 · 방) | 확실 |
| User-Generated Content | **확인 필요 — 제안 Yes** | 채팅 글 · 사진 · 동영상은 사용자가 만든 콘텐츠지만 **같은 병원 직원 사이 비공개**(공개 피드 · 공개 공유 없음) | 확인 필요 — Yes 면 심사관이 가이드라인 1.2(신고 · 차단 · 필터) 를 볼 수 있다. 앱에 신고 · 차단 기능은 없다 → 사용자 판단. 비공개 업무 메시지만이면 Messaging and Chat = Yes 로 충분하다고 보고 No 를 고르는 선택지도 있음 |
| Social Media | No | 공개 프로필 · 팔로우 없음 | 확실 |
| Advertising | No | 광고 SDK 0 | 확실 |
| Medical or Treatment Information | **확인 필요 — 제안 Infrequent** | 직원에게 고객 시술명 · 차트 메모를 **읽기로** 보여 줌(진료 · 치료 조언을 사용자에게 주는 앱은 아님) | 확인 필요 — 업무용 시술 정보 표시를 「의학/치료 정보」로 볼지 사용자 판단. 보수적으로 Infrequent |
| Health or Wellness Topics | 제안 No | 건강 · 웰니스 콘텐츠 제공 앱 아님 | 제안 |
| Profanity · Horror · Alcohol/Tobacco/Drug · Mature/Suggestive · Sexual(두 칸) · Violence(세 칸) · Guns | None / No | 앱이 만드는 콘텐츠 없음(채팅은 직원 업무 대화) | 확실(앱 콘텐츠 기준) |
| Gambling · Simulated Gambling · Contests · Loot Boxes | No / None | 해당 없음 | 확실 |
| Made for Kids | 아님(Not Applicable) | `isOrEverWasMadeForKids = false` | 확실(GET) |
| 한국 연령 등급(`koreaAgeRatingOverride` · GRAC 번호) | NONE · 비움 | 게임 아님 | 제안 |
| 결과 등급 | ASC 계산 값 | Messaging and Chat · (UGC) 답에 따라 올라갈 수 있음 — 입력 뒤 화면 값을 리포트에 옮김 | 확인 필요(계산 규칙을 문서에서 확인하지 못함) |

---

## ③ 가격 · 판매 지역

| ASC 칸 | 답 | 근거 | 판정 |
|---|---|---|---|
| 가격 | **무료(Free · 0)** · 앱 내 구입 없음 | 앱에 결제 · IAP 코드 없음 · Unlisted 직원용 | 제안(사용자 결정 「무료」가 문서에 없으면 확인) |
| 배포 방식 | **Unlisted** 신청(심사 통과 뒤 별도 신청) | app-store-preparation §5-4 · handoff §2 「최종 배포 방식은 Unlisted」 | 확실(사용자 결정) · 신청 시점은 사용자 |
| 판매 지역 | **대한민국만** | 연결 병원 · 직원 · 앱 언어(ko) · 사용자 결정 없음 | **제안** — 사용자 확인 |
| 새 지역 자동 포함(`availableInNewTerritories`) | **끔** | 한국만 판매 제안과 같은 이유 | 제안 |
| 현재 ASC | 가격 일정 · 판매 지역 **없음**(GET 404) | `/v1/apps/{id}/appPriceSchedule` · `/v2/appAvailabilities/{id}` 404 | 확실(GET) |

---

## ④ 저작권

| ASC 칸 | 답 | 근거 | 판정 |
|---|---|---|---|
| Copyright | **`2026 Medisolve AI Co., Ltd.`** | 형식 = 「권리를 얻은 해 + 권리자」(예 `2014 Example, Inc.` · © 는 Apple 이 붙임 — https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information) · 운영사 표기 = 사용자 결정 Medisolve AI Co., Ltd.(app-store-preparation §6-1 · 배포 서명 조직 표기와 같음) | 제안 — 연도(2026)는 첫 공개 해로 제안 · 사용자 확인 |

---

## ⑤ 콘텐츠 권리 (Content Rights)

| ASC 칸 | 답 | 근거 | 판정 |
|---|---|---|---|
| Does your app contain, show, or access third-party content? | **확인 필요 — 제안 「Yes, … and I have the necessary rights」**(`USES_THIRD_PARTY_CONTENT`) | 앱이 **병원 EMR(KOS)** 의 고객 · 시술 정보를 서버를 거쳐 **보여 준다**(접근 = 병원 직원 계정 · 업체 API) · 통역 자막 · 음성은 Soniox 가 만든 결과. Apple 규칙: 「Apps that contain, show, or access third-party content must have all the necessary rights to that content」(App Information 도움말) | 확인 필요 — 「권리가 있다」는 **병원 · EMR 업체(KOS)와의 연동 계약 · Soniox 이용 약관**이 있어야 쓸 수 있는 답. 계약 여부는 사용자만 안다. 반대로 「EMR 데이터는 고객(병원) 자신의 데이터라 서드파티 콘텐츠가 아니다」로 보고 No 를 고를 수도 있음 — 보수적인 쪽은 Yes(권리 확인 후) |
| 현재 ASC | `contentRightsDeclaration = null` | GET | 확실 |

---

## 사용자 확인 목록 (오늘 심사 전)

1. **Product Interaction 신고 여부**(업무 조작 이력 · 읽음) — 권장: 신고.
2. **Health 신고 여부**(앱 조작이 환자 시술 상태를 만들어 보관) — 권장: 판단 필요 · 보수적이면 신고.
3. **Audio Data 미신고의 전제** — Soniox 별도 계약 · Console 보관 설정이 공개 정책(실시간 미저장)과 같은지.
4. 연령 등급 **User-Generated Content** Yes/No(1.2 신고 · 차단 기능 없음 위험) · **Medical or Treatment Information** None/Infrequent.
5. 판매 지역 「한국만」 · 가격 무료 확정.
6. 저작권 연도 2026.
7. 콘텐츠 권리 — KOS 등 EMR 업체 · 병원과 연동 계약 · Soniox 약관 유무.
8. 서버 접근 로그의 실제 IP 보관 여부 · 기간(§7-1 T3).

## 하지 않은 것
ASC 쓰기(PATCH/POST) 0 · 소스 수정 0 · 커밋 0 · 키 출력 0. 연령 등급 계산 결과 · App Privacy 화면 미리보기는 입력 전이라 없음.
