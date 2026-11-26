# research-2 — WORK-002 여권 스캐너 · 문진 QR 현황 조사(read-only)

- 기준: cc-prototype `origin/main` = `0553173`(이하 **cc**) · CENTURION_DAY `96036397`(이하 **DAY**) · mediness 스펙 워크트리 `day-app-re1-spec` HEAD `319dd82e`(이하 **SPEC** · `products/day/` 기준 경로)
- 코드는 `git show <ref>:<path>` 로만 읽었다. 빌드 · 실행 · KOS · 서버 · DB 접속 없음. 설계 · WP 없음.
- 경로 줄임: cc 앱 = `procedure/app/` · cc 백 = `procedure/back/app/` · cc 웹 = `procedure/front/` · DAY 백 = `backend/day/` · DAY 앱 = `app/`

## 0. 한 화면 요약

| 묶음 | cc 에 있음 | DAY 에 있음(일부 포함) | 새로 필요 |
|---|---|---|---|
| 여권 스캐너(10행 · §4 S1 ~ S10) | 10 | 5 — 고객 여권 칸 4개 · `id_photo` · `identity_check` 표 · KOS 사진 등록 코드(시술전후용) · KOS 고객 수정 키 목록. **쓰는 코드는 0** | 10 전부(앱 화면 · 네이티브 iOS 채널 · Android 쪽 · 백 API · KOS 연결) |
| 문진 QR(8행 · §4 Q1 ~ Q8) | 8 | 3 — `display_request` · `questionnaire_history` 표 · 기기(`device`) 표. **쓰는 코드는 0** | 8 전부(토큰 · 공개 API · 고객 웹 · KOS 문진 경로 · 앱 QR 화면 · 결과 보기) |
| **정할 것** | | | **12개**(§5) |

핵심 사실 다섯:

1. **앱에는 예약 · 접수 단계 고객이 보이는 화면이 없다.** 앱 탭 = 시술현황 · 채팅 · 설정 3개, 예약현황은 숨겨 둠(DAY `app/lib/ui/shell.dart:2` · `:26` · SPEC `spec-003-mobile-app.md:123`). 시술현황 판 = 시술 대기 · 시술 단계만(DAY `backend/day/policies/board_rule_values.py:28`). 그런데 [여권 스캔] · [문진 QR] 이 켜지는 때 = **예약 · 접수 단계**(SPEC `spec-007-reservation-detail.md:202` D55). → 시술현황에 넣으면 대상 고객이 판에 없다.
2. **DAY 는 표만 있고 쓰는 코드가 없다.** `display_request` · `identity_check` · `id_photo` · `questionnaire_history`(DAY `backend/day/models/reception.py:33-99`) — 행을 만드는 곳은 내국인 「신분증 확인」 체크 하나뿐(`services/reservation_care_writes.py:187`, 외국인은 400 `:181-182`).
3. **cc 스캐너는 iOS 전용이다.** cc 앱에 `android/` 폴더 자체가 없다(`git ls-tree origin/main procedure/app/` = assets · integration_test · ios · lib · test · test_driver · tool). 결정 D-02 「앱 = iOS 만」(cc 문서 `10-decision/decision-007-app-v2.md:60`). DAY 는 Android 도 배포한다(Kotlin 채널 `day/session` · `day/push` · `day/video` — `app/android/app/src/main/kotlin/day/medisolveai/MainActivity.kt:23-29`).
4. **cc 고객 문진 웹은 Next.js 별도 front(`/q`)다. DAY 엔 별도 front 가 없다** — 웹 = FastAPI Jinja2 + HTMX, 로그인 없는 경로 = `/privacy` · `/support` 둘뿐(DAY `backend/day/routers/public_pages.py:1-8`).
5. **DAY 웹 예약 상세에 [문진 QR] · [여권 스캔] 버튼 자리가 비활성으로 이미 있다**(DAY `templates/partials/reservations_detail.html:100-101` · SPEC `spec-007-reservation-detail.md:152` D13 · `:202` D55). 웹 예약 현황 스펙은 이것을 「앱으로 보내기 — 여권 스캔 · 전후 사진 · 문진(R5)」로 적었다(SPEC `spec-006-reservation-board.md:111`).

---

## 1. cc 여권 스캐너 — 단계별 흐름

### 1.1 진입

| 길 | 위치 |
|---|---|
| 앱 **예약 상세 「신분 확인」 상자 [여권 스캔]** — 이 기기 카메라 | cc `procedure/app/lib/screens/reservation_detail_screen.dart:218-268`(버튼 `:262` · `_scan` `:302-307`) |
| 웹에서 띄우기(kind = scan) → 그 기기 앱이 예약 상세를 읽어 스캔 화면 | cc `procedure/app/lib/screens/launchers.dart:106-124` · 결정 D-48(`decision-007-app-v2.md:146`) |
| 앱엔 「다른 기기로 스캔 보내기」 없음(웹만) | cc `launchers.dart:3` · D-72(`decision-007-app-v2.md:180`) |
| cc 앱 탭 = 예약 현황 · 내원 현황 · 시술 현황 · 채팅 · 설정 — 예약 상세는 예약 현황 · 내원 현황에서 연다 | cc `procedure/app/lib/screens/shell.dart:20-24` · `reservation_detail_screen.dart:28-30` |

화면은 `rootNavigator: true` 전체 화면 dialog(cc `scan_screen.dart:27-31`).

### 1.2 흐름(찍기 → MRZ → 확인 → 저장 → KOS)

| 단계 | 하는 일 | 근거 |
|---|---|---|
| ① 카메라 | 네이티브 `PassportScanController` — `AVCaptureSession` 연속 프레임 · 가이드 틀(125 × 88) · 자동 매크로(triple → dual wide → wide 순 카메라) · [촬영] 버튼 항상 · [닫기] · [손으로 입력] | cc `procedure/app/ios/Runner/TextScanner.swift:5-13` · `:50-67` · `:106-160` |
| ② MRZ 읽기 | 틀 영역만 잘라 Vision `VNRecognizeTextRequest(.accurate)` → 줄마다 Dart `checkMrz` 로 물음 → `mrz.dart` 가 보정(OCR-B 오인식 표 · `<` 변형 · K 보정) · TD3 두 줄 44자 · 검사 숫자(여권번호 · 생년월일 · 만료일 — **종합 검사 숫자는 안 봄**) · **같은 판독 연속 2번 = 자동 촬영** · `windowSec` 8초 × 3번 못 읽으면 failed | Swift `:410-445` · `:459-468` · cc `lib/scan/scan_channel.dart:43-62` · `lib/scan/mrz.dart:43-219` |
| ②' 실패 | [다시 찍기] · 3번 실패 또는 [촬영] 사진에서도 못 읽음 → 손 입력(빈 확인 화면 · 사진 없이 저장 `app_manual`) · 카메라 없음 / 권한 꺼짐 = `no_camera` → 손 입력 | cc `scan_screen.dart:105-153` · Swift `:32-46` |
| ③ 확인 화면 | 칸 7개(영문 성 · 영문 이름 · 여권번호 · 국적 · 생년월일 · 성별 · 만료일 — `name` 없음 D-53) · 「읽은 값」(고칠 수 있음) ↔ 「KOS 지금 값」 나란히 · 다른 칸 노란 강조 · 썸네일 88 × 62 | cc `scan_screen.dart:33-60` · `:271-360` |
| ④ 저장 | multipart `POST /api/customers/{id}/passport-scan` — `fields`(바뀐 칸만 JSON) · `photo`(JPEG ≤ 5MB · 손 입력이면 없음) · `reservationId` · `displayRequestId?` · `deviceId` · `manual` | cc `lib/api/api.dart:163-165` · `scan_screen.dart:157-187` · 백 `api/photos.py:69-126` |
| ④-a 고객 수정 | KOS 내부 `get-visitor` 다시 읽기 → 개인정보 키 전부 + 바뀐 칸 → 내부 `update-visitor-personal-information`(같으면 안 부름) · 실패(409 · 502) = 아무것도 저장 안 함 | cc 백 `service/passport_scan.py:65-67` · `service/reservations.py:1061-1089` |
| ④-b ccc 사진 | `PROC_PHOTO_DIR/<무작위>.jpg` 바로 쓰기(임시 파일 없음) + `id_photo` 행(sha256 · bytes · `kos_status`) | cc 백 `service/id_photo.py:49-63` |
| ④-c KOS 사진 | 내부 `get-codes{IMAGE_EQUIPMENT}` 에서 이름 「태블릿」 · `get-codes{IMAGE_CATEGORY}` 에서 이름 「여권」(없으면 안 보냄) → **공개** `generate-uploading-url` → presigned PUT → **공개** `register-visitor-images`(`scheduleId` = 그 예약 KOS 일정 · memo 「ccc 여권 스캔」) · 실패해도 앞 단계는 남김(`failed` → [사진 다시 올리기]) | cc 백 `service/id_photo.py:22-35` · `:65-108` |
| ④-d 기록 | `event_log passport_scan` · `identity_check`(confirmed · `app_scan` / `app_manual` · 기기 이름 · photo_id) · 띄우기 요청 done | cc 백 `service/passport_scan.py:72-80` |
| ⑤ 결과 | 「저장했어요」 + ccc 사진 · KOS 사진 결과 줄 따로 · KOS 실패면 [사진 다시 올리기](`POST …/kos-retry`) | cc `scan_screen.dart:362-389` · 백 `service/id_photo.py:127-140` |
| 그 뒤 | 사진 열람 `GET /api/id-photos/{id}`(Bearer 헤더만 · `no-store` · 열 때마다 event_log) · [사진 삭제](ccc 파일 · 행 + KOS 이미지 · 신분 확인 → 미확인) | cc 백 `api/photos.py:128-140` · `service/id_photo.py:110-125` · `:142-150` · 앱 `reservation_detail_screen.dart:270-295` |

### 1.3 패키지 · 권한 · 채널

- **스캐너용 Flutter 패키지 0** — 카메라 · 글자 인식 · QR 그리기 전부 자체 Swift 채널 `procedure/scan`(cc `TextScanner.swift:18-22` · 등록 `ios/Runner/AppDelegate.swift:20` · `:42`). cc pubspec 의존(`http_parser` = multipart Content-Type)만 관련(cc `procedure/app/pubspec.yaml` dependencies).
- 카메라 문구: 「여권 사진면을 찍거나 채팅으로 보낼 사진을 찍기 위해 카메라를 사용합니다. 찍은 사진은 사진첩에 저장하지 않습니다.」(cc `ios/Runner/Info.plist:69-70`)
- 법적 검토 주석: 원본은 메모리만 · 사진첩 · 파일 · 캐시 쓰지 않음 · 저장 성공 / [다시 찍기] / [닫기] 때 버림(D-50 · cc `scan_screen.dart:8-9` · `scan_channel.dart:2` · Swift `:11-13`). 가림 없음 · 여권만(D-17 · D-51).
- 시험: cc `test/mrz_test.dart` · `test/scan_test.dart` · 백 `tests/test_app_be5.py`.

### 1.4 막혔던 것(cc 기록)

| 무엇 | 근거 |
|---|---|
| 한 장 촬영(UIImagePickerController)은 근접 초점 · 매크로 전환이 안 됐고, 검사 숫자 전부 일치 조건은 실기기에서 한 번도 통과 못 함(`<` → `K` 등) → 연속 프레임 · 틀 영역만 · 오인식 보정 · 연속 2 프레임 확정 · 종합 검사 숫자 안 봄 | cc 문서 `log/2026-10-28-overall-board.md:35-36` · cc `mrz.dart:43-73` · `:132-133` |
| KOS 사진이 `kos_status=ok` 인데 KOS 일정 사진 탭에 안 보임 → 사용자 HAR 로 KOS 자체 여권 스캔이 `scheduleId` · 분류 「여권」을 싣는 것 확인 · 분류는 지점 코드에 「여권」이 있을 때만 | `log/2026-10-28-overall-board.md:22-23` · `:71` · cc `id_photo.py:26` · `:69-73` |
| 장비 코드 id 는 지점마다 다름 → 이름 「태블릿」으로 매번 찾음 · 없으면 `equipment_code_missing` | cc `id_photo.py:27` · `:84-89` · WORK-009 `30-work/work-009-app-v2.md:79` |
| KOS 고객 수정은 공개 API 가 없어 내부 `update-visitor-personal-information` · 만료일 키는 데모에서 받음(K2) | D-18(`decision-007-app-v2.md:86`) · WORK-009 `:73` |
| KOS 고객이 없는 사람(워크인) 스캔 = 그 판 없음 | D-52(`decision-007-app-v2.md:150`) |
| 사진 볼륨 암호화 = 없음(local-path) · 보관 기간 미정 → 법적 검토 남음 | D-54 · D-55 · D-68 · `log/2026-10-28-overall-board.md:106` |

---

## 2. cc 문진 QR — 흐름

### 2.1 QR 에 실리는 것 · 토큰

| 항목 | 내용 | 근거 |
|---|---|---|
| 만들기 | 직원이 `POST /api/display-requests {reservationId, kind: "questionnaire", deviceId?}` — 같은 예약 · 같은 종류 pending · opened 는 canceled 로 닫고 새로 | cc 백 `api/display.py:51-60` · `service/display.py:1-11` · `:102-132` |
| QR 내용 | 고객 웹 링크 `{PROC_FRONT_ORIGIN}/q#<token>` — 토큰은 `#` 뒤(서버 접근 로그에 안 감) | cc 백 `service/display.py:7` · `:72-77` · 웹 `components/q/QuestionnairePage.tsx:52-57` |
| 토큰 | HMAC(`PROC_SESSION_SECRET`, `q|{id}|{nonce}`) · DB = `qr_nonce` · sha256(token)만 · 로그인한 직원 응답에만 `qrUrl` | cc 백 `service/display.py:34-40` · WORK-010 `30-work/work-010-customer-questionnaire-web.md:56` |
| 대상 | 띄우기 요청 행 = 예약(방문) 하나 → 고객. 공개 API 는 예약 · 고객 id 를 입력으로 받지 않고 응답에도 싣지 않음 | cc 백 `service/questionnaire.py:5` · `api/public_questionnaire.py:40-42` |
| 수명 | 여는 시한 = 만든 뒤 `PROC_DISPLAY_TTL_MIN`(기본 10분) · 쓰는 시한 = 처음 연 뒤 `PROC_QWEB_FILL_MIN`(기본 60분) · 지나면 410 `q_expired` | cc 백 `api/public_questionnaire.py:49-50` · `service/questionnaire.py:191` |
| 재사용 | 제출 1회 — 끝난 뒤 다시 = 409 `q_submitted` · 겹친 제출 = 409 `q_submitting` · 새 링크가 앞 링크 canceled = 410 `q_canceled` | `api/public_questionnaire.py:50-53` · `:111` |
| 공개 경로 보안 | `Authorization` 무시(직원 토큰 실려도 직원 권한 아님) · 토큰 = 헤더 `X-Questionnaire-Token` 만(경로 · 쿼리 금지) · 응답 허용 키 모델 · `Cache-Control: no-store` · `Referrer-Policy: no-referrer` · 속도 제한(메모리 · IP 당 GET 30 / POST 5 · 토큰당 POST 3 · 틀린 토큰 60초 10번이면 IP 막음) · 거절 `qweb_denied` 기록(IP · 토큰 안 남김) | `api/public_questionnaire.py:1-8` · `:39-56` · `service/questionnaire.py:11` · `:72-97` |

### 2.2 앱 QR 화면

- 예약 상세 「고객 기본 정보」 상자 [태블릿에 띄우기](기기 고르기 시트 → 그 기기에 QR) · [이 기기에 QR 보이기](cc `reservation_detail_screen.dart:412-413` · `launchers.dart:19-100`).
- QR 화면: 흰 전체 화면 · 가운데 큰 QR(네이티브 CoreImage `CIQRCodeGenerator` · 오류 정정 M) · 남은 시간 mm:ss · 화면 꺼짐 막기(`isIdleTimerDisabled`) · 5초마다 예약 상세 `displays[]` 폴링 → pending 아니면 한 줄 알림 뒤 닫힘 · 고객 이름 · 예약 정보 없음 · `qrUrl` 은 로그 · 토스트 금지(cc `screens/qr_show_screen.dart:1-31` · `:62-78` · Swift `TextScanner.swift:68-79` · `:84-97`).
- **QR 그리기 · 꺼짐 막기도 iOS 네이티브** — Android 길 없음(cc 에 android 없음).

### 2.3 고객이 쓴 답이 가는 곳

| 단계 | 내용 | 근거 |
|---|---|---|
| 불러오기 `GET /api/public/questionnaire` | KOS **공개** `getVisitorQuestionnaire`(양식) · `get-questionnaire-agreements`(약관) — 실패 = 502 · 내부 `get-visitor` = 언어 근거 · 미리 채움(이름 · 휴대폰 · 주소 · 생년월일 · 성별) · 첫 성공 = 요청 opened | cc 백 `api/public_questionnaire.py:68-93` · `service/questionnaire.py:137-191` |
| 언어 | KOS 고객 `language` → 국적표 → `en` · 양식 번역 6개(ko · ja · zh-Hans · zh-Hant · en · id) | `api/public_questionnaire.py:76-77` · D-15(`decision-007-app-v2.md:78`) |
| 고객 웹 | 단계 ① 불러오기 → ② 언어 칩 6 · 「{이름} 님」 → ③ 기본 정보(미리 채움 · 고칠 수 있음) → ④ KOS 양식 쪽마다 → ⑤ 동의 → ⑥ 제출 → ⑦ 끝 · 쓰던 답은 브라우저에 저장 안 함 · DS = `@medisolve-ai/medikit` | cc 웹 `components/q/QuestionnairePage.tsx:1-7`(509줄) · `app/q/page.tsx` |
| 제출 `POST /api/public/questionnaire` | `registrationNumber` · `phoneticName` 보내면 400 · KOS **공개** `submit-visitor-questionnaire`(+ visitorId) — **KOS 고객 성별 · 생년월일 · 주소 · 휴대폰 · 동의를 바꾼다** · KOS 400 = 409 `questionnaire_rejected` · 그 밖 502 | `api/public_questionnaire.py:96-130` · `service/questionnaire.py:7-9` · `:197-232` |
| 저장 | 제출본 다시 읽어 ccc `questionnaire_history`(source `web_submit`) · 다시 읽은 게 이번 제출이 아니면(KOS 는 첫 제출본을 줌 · Q-27) 보낸 답을 그 꼴로 · 요청 done · `event_log questionnaire_submit` | `service/questionnaire.py:206-231` · `service/reservations.py:628-645` |
| 직원이 보는 곳 | 예약 상세 「건강 정보」 상자(질문 × 제출본 · 제출 시각) · 띄우기 단계 줄(pending = QR 보이는 중 · opened = 고객이 입력 중 · done) | cc `reservation_detail_screen.dart:457-470` · `:415-419` · `:771-772` · 백 `service/reservations.py:514` · `:574` · `:628-645` |

### 2.4 막혔던 것 · 결정(cc 기록)

| 무엇 | 근거 |
|---|---|
| 처음엔 **앱 안 문진 화면 + 잠금 + unlock** 까지 계약 · 구현 → 사용자 뜻 오독(「고객이 그 기기에서 채운다」) → 고객 폰 웹 `/q` 로 다시(QR 만 · 미리 채움 · 안드로이드 포함) · 앱 문진 화면 · unlock · 문진 API 지움 | `log/2026-10-28-overall-board.md:53` · `:70` · WORK-010 `:59` · `:71` |
| KOS 설문 링크(30일)는 안 씀 · 질문지 = KOS 문진 양식 그대로 · 매 방문 · 방문별 이력 = ccc | D-13 · D-14(`decision-007-app-v2.md:76-77`) |
| KOS 문진은 고객당 1건 · 다시 제출하면 덮어씀 · 제출이 성별 · 휴대폰 · 주소를 고객 정보에 반영 | cc 문서 `00-baseline/baseline-009-reservation-board.md:76` |
| 주민번호 안 넣음 · 스캐너 먼저 → 문진에 스캔 값 | D-16(Q-151 · Q-152 · `decision-007-app-v2.md:79`) |
| 리뷰 WARN 3 남음 — IP 헤더 무조건 신뢰 · 속도 제한 dict 안 줄어듦 · 데스크 상자 새로고침 남은 시간 · 속도 제한 / 잠금 = 한 파드 메모리 | `log/2026-10-28-overall-board.md:104` · `service/questionnaire.py:11` |
| 법적 검토: 고객 건강 문진 답의 ccc 저장 · 링크 가진 사람이 미리 채운 개인정보를 봄(OQ-807 · PoC = 보임) | `log/2026-10-28-overall-board.md:106` · `service/questionnaire.py:45` |

---

## 3. DAY 에 있는 것 / 없는 것

| 항목 | 상태 | 근거 |
|---|---|---|
| 고객 여권 칸 | **있음** — `passport_surname` · `passport_given_names` · `passport_number`(암호화) · `passport_expiry_date` · KOS 매퍼가 채움 | DAY `backend/day/models/customer.py:56-67` · `emr/kos/mapper_kos_keys.py:451-456` · migration `backend/migrations/versions/20261105_0002_data_model_first_data_model.py:900-911` |
| 웹 여권 표시 | 고객 정보 「여권 · 유입」 — 이름 · 만료일 · 「여권 이미지를 볼 수 없어요 / 없음」(사진 보기 없음) · 예약 상세 「성명(여권)」 = `customer.name`(여권 칸 안 씀) | DAY `templates/partials/customer_info.html:30-50` · `queries/customers.py:456-465` · SPEC `spec-007-reservation-detail.md:133` |
| `id_photo` · `identity_check` · `display_request` · `questionnaire_history` 표 | **있음 · 쓰는 코드 0**(내국인 체크 1곳 뿐) · `id_photo` 에 `kos_status` 칸 없음(→ `external_outbox` 라고 적음) | DAY `models/reception.py:33-99` · SPEC `spec-000-data-model.md:1153-1194` · `:1076` · grep `IdPhoto(` · `DisplayRequest(` · `QuestionnaireHistory(` = 모델 · 시험만 |
| 신분 확인 쓰기 | 내국인 「신분증 확인」 체크만(`method = manual` · KOS 쓰기 없음) · **외국인이면 400** | DAY `services/reservation_care_writes.py:170-199` · SPEC `spec-007-reservation-detail.md:204` D20 · D24 |
| 웹 [문진 QR] · [여권 스캔] | 자리만 · `disabled` · 보이는 조건 = 시안(문진 QR = 오늘 ∧ 예약 · 접수 ∧ 문진 안 함 / 여권 스캔 = 외국인 ∧ 1년 안 재진 아님 ∧ 오늘 ∧ 예약 · 접수 ∧ 신분 미확인) | DAY `templates/partials/reservations_detail.html:4` · `:100-101` · SPEC `spec-007-reservation-detail.md:109` · `:152` · `:202` · `:345` |
| 예약 / 접수 API | **웹 HTML 경로만**(`/reservations/...` · 세션 쿠키 · HTMX partial) — 접수 `PUT …/reception` · 신분 `…/identity` 등. **앱 JSON(`/api/...`)엔 예약 · 고객 경로 0** | DAY `routers/reservation_detail.py:170-507` · `routers/customers.py:31-199` · 앱 호출 전수 `app/lib/**` grep `/api/` = auth · devices · board · visits · tasks · calls · chat · notifications · interpret 만 |
| 앱 탭 | 시술현황 · 채팅 · 설정 — 예약현황 숨김(2026-11-13 · 「예약 기능이 생기면 다시 넣음」) | DAY `app/lib/ui/shell.dart:2` · `:26-37` · SPEC `spec-003-mobile-app.md:123` |
| 앱 판 대상 | 시술 대기 · 시술(방 있음)만 | DAY `policies/board_rule_values.py:28` · `policies/board_rules.py:68` |
| 앱이 아는 고객 값 | 판 고객 = 이름 · 발음 · 성별 · 생년월일 · 국적(customerId · 여권 칸 없음) | DAY `app/lib/model/board.dart:29-36` · `schemas/board_responses.py:196` |
| 네이티브 채널 | iOS · Android 둘 다 `day/session` · `day/push` · `day/video` 만 — **카메라 연속 스캔 · 글자 인식 · QR 그리기 · 꺼짐 막기 채널 0** | DAY `app/ios/Runner/AppDelegate.swift:50` · `:54` · `:376` · `MainActivity.kt:23-29` |
| 앱 패키지 | `image_picker` · `flutter_image_compress` · `photo_manager`(채팅 · 차트 사진) — 연속 프레임 · OCR 패키지 없음 | DAY `app/pubspec.yaml` dependencies |
| 앱 사진 올리기(WORK-001) | `POST /api/visits/{v}/photos` multipart(시술전후 · `board` 권한) — 방문 · 분류 「시술 전 / 후」 전용 | DAY `routers/api/board_photos.py:1-13` · `:83-84` |
| iOS 카메라 문구 | 「채팅으로 보낼 사진과 차트에 올릴 시술 전후 사진을 찍기 위해 … 사진첩에 저장하지 않습니다.」 — **여권 없음**(SPEC-004 가 cc 문구에서 「여권 사진면을 찍거나 」를 일부러 지움) | DAY `app/ios/Runner/Info.plist:52-53` · SPEC `spec-004-internal-chat.md:538` · `:636` OQ-C7 |
| Android 카메라 권한 | `android.permission.CAMERA` 선언 없음(INTERNET · RECORD_AUDIO · READ_MEDIA_* · POST_NOTIFICATIONS) | DAY `app/android/app/src/main/AndroidManifest.xml:5-13` |
| KOS 고객 수정 | 키 목록 `PERSONAL_KEYS`(여권 4키 포함) · 다시 읽기 → 전체 + 바꿀 칸 → `update-visitor-personal-information` — **partner worker 가 시스템 계정으로 `language` 만** 부름 | DAY `emr/kos/ext_reads.py:214-231` · `:235-257` |
| KOS 사진 등록 | 내부 경로 · **직원 토큰 직접**(쓰기 큐 없음 · [다시 시도]) · `get-codes` 이름 매칭(분류 = 「시술 전」 · 「시술 후」만 · 장비 「태블릿」) · presigned → PUT → `register-visitor-images` · 삭제 | DAY `emr/kos/photos.py:1-29` · `policies/photos.py:10-17` · `services/visit_photo_kos.py:1-8` · `:275-276` · cc 공개 경로를 안 쓴 이유 = SPEC `spec-002-procedure-board.md:1165` |
| KOS 문진 경로 | **0** — `getVisitorQuestionnaire` · `get-questionnaire-agreements` · `submit-visitor-questionnaire` grep 결과 없음 · KOS 공개 호출 메서드 `open()` 은 있음 | grep `96036397 -- backend/day` · DAY `emr/kos/client.py:571` |
| 문진 언어표 | 문진용 표 없음 — 통역 `APP_LANGS` 만 | DAY `policies/interpret/languages.py`(import `bootstrap/interpret.py:27`) · 문진 6언어와 같은지 = 확인 안 됨 |
| 공개(로그인 없는) 웹 | `/privacy` · `/support` 만(세션 · CSRF 의존성 없음) | DAY `routers/public_pages.py:1-8` |
| 저장소 | 채팅 · 시술전후 사진과 같은 파일 저장소 · 용도 「고객 신분증(여권)」이 SPEC-004 개정 ⑤ 용도 셋에 이미 적힘 · 키 = `{용도}/{병원 id}/…` | SPEC `spec-004-internal-chat.md:32` · `spec-000-data-model.md:63` |
| 법적 검토 | DAY-ESC-001 대기(경영지원) — 신분증 · 여권 사진 · 문진 · 채팅 속 고객 정보의 보관 기간 · 열람 기록. SPEC 은 참조만 · 비차단 | SPEC `10-decision.md:28` · `:45` · `:60` · `spec-000-data-model.md:81` · `:1081` |
| 스펙 범위 | 「여권 스캐너 · 문진 QR · 예약 탭 = 다음 작업(WORK-002)」 · 띄우기(`display`) · 여권 스캔은 SPEC-003 · SPEC-005 범위 밖으로 적혀 있음 | SPEC `spec-003-mobile-app.md:123` · `:134` · `:1099` · `spec-005-notifications.md:77` |

---

## 4. 이식 표

「옮기기」 열 = 그대로 못 옮기는 이유. 설계 아님 — 무엇이 다른지만.

### 여권 스캐너

| # | 기능 | cc 위치 | DAY 위치 | 새로 필요 | 그대로 못 옮기는 이유 |
|---|---|---|---|---|---|
| S1 | 진입 [여권 스캔] | 앱 예약 상세 신분 확인 상자 `reservation_detail_screen.dart:262` · 띄우기 `launchers.dart:106-124` | 웹 예약 상세 비활성 `reservations_detail.html:101` · 앱 없음 | 앱 진입 화면 · 앱이 읽을 예약 · 고객 JSON | 앱에 예약 상세 · 예약 API 없음 · 판엔 예약 · 접수 단계 고객이 안 보임(§0 1) |
| S2 | 카메라 연속 스캔 | iOS `TextScanner.swift`(478줄) · 채널 `procedure/scan` · `AppDelegate.swift:20,42` | 없음 | 네이티브 **iOS** 채널 · **Android** 쪽(cc 에 없음) | 채널 이름 규칙 `day/*` · cc 는 iOS 만 · DAY 는 Android 배포 |
| S3 | MRZ 파서 · 확정 규칙 | `lib/scan/mrz.dart`(순수 Dart · 231줄) · `test/mrz_test.dart` | 없음 | 앱(옮길 후보) | 플랫폼 무관 Dart — 막는 구조 차이 확인 안 됨 |
| S4 | 실패 · 손 입력 · 확인 화면 | `screens/scan_screen.dart`(394줄) | 없음 | 앱 화면 | cc DS(`theme/tokens.dart` · `widgets/ui.dart` · `MsButton`) ↔ DAY 앱 DS(`app/lib/ui/theme.dart`) · cc `ResvDetail` 모델 · `AppState` |
| S5 | KOS 고객 수정 | `service/reservations.py:1061-1089`(직원 actor · 내부) | 키 목록 `ext_reads.py:214-231` · 부르는 곳은 partner worker `language` 만 `:235-257` | 백 쓰기(직원 경로) | DAY 의 이 호출은 시스템 계정 · 쓰기 큐 쪽 — 직원 토큰 / 큐 중 어느 길인지 정해지지 않음(§5 Q4) |
| S6 | 사진 저장 | `service/id_photo.py:49-63`(로컬 폴더 `PROC_PHOTO_DIR`) | `id_photo` 표 `models/reception.py:68-82`(`file_key` = 저장소) · 저장소 용도 「고객 신분증(여권)」 SPEC-004:32 | 백 서비스 · API(multipart) | 저장소 구조 다름(로컬 볼륨 ↔ 공용 파일 저장소) · `kos_status` 칸 없음(SPEC-000 = outbox) |
| S7 | KOS 사진 등록 | **공개** `generate-uploading-url` · `register-visitor-images` · 분류 「여권」 · 장비 「태블릿」 · `scheduleId` `id_photo.py:65-108` | **내부** 경로 · 직원 토큰 `emr/kos/photos.py` · 분류는 「시술 전 / 후」만 `policies/photos.py:11-14` | 분류 「여권」 매칭 · `id_photo` 용 연결 · 다시 시도 | DAY 는 내부 + 직원 토큰을 택함(SPEC-002:1165) · SPEC-000:1076 은 신분증 업로드를 `external_outbox` 로 적음 — 두 기록이 다름(§5 Q5) |
| S8 | 신분 확인 기록 | `identity_check` `app_scan` / `app_manual` + 기기 · 사진 `passport_scan.py:72-80` | 표 있음 · 쓰기 = 내국인 체크만 · 외국인 400 `reservation_care_writes.py:181-182` | 백(외국인 · 스캔 방법) | 방법 값 이름 = WORK 에서 정함(SPEC-000:1175) |
| S9 | 사진 열람 · 삭제 · KOS 다시 올리기 | `api/photos.py:128-140` · `id_photo.py:110-150` · 앱 `reservation_detail_screen.dart:270-295` | 웹 「여권 이미지를 볼 수 없어요」 문구만 `customer_info.html:34` | 백 · 앱 · (웹) | 열람 기록 · 보관 = DAY-ESC-001 대기 |
| S10 | 권한 문구 | cc `Info.plist:69-70`(여권 포함) | DAY `Info.plist:52-53`(여권 없음) · Android CAMERA 없음 | iOS 문구 · Android 권한(방식에 따라) | SPEC-004 OQ-C7 이 여권 구절을 범위 밖이라 지움 — 다시 넣으려면 SPEC-004 §4 · SPEC-003 권한 줄(`:1044`) 고침 |

### 문진 QR

| # | 기능 | cc 위치 | DAY 위치 | 새로 필요 | 그대로 못 옮기는 이유 |
|---|---|---|---|---|---|
| Q1 | 띄우기 요청 · 토큰 | `service/display.py:1-132` · `api/display.py:51-60` | `display_request` 표(`qr_token_hash` · `qr_nonce`) `models/reception.py:33-49` · 쓰기 0 | 백 서비스 · API | cc 는 `reservation_id`(정수) ↔ DAY `visit_id`(uuid) · 비밀값 이름(`PROC_SESSION_SECRET`) 다름 |
| Q2 | 앱 QR 화면 | `screens/qr_show_screen.dart` · 네이티브 `qrImage` · `keepAwake` `TextScanner.swift:68-97` | 없음 | 앱 화면 · QR 그리기 · 꺼짐 막기(iOS · Android) | QR 그리기가 cc 는 iOS CoreImage — Android 길 없음 |
| Q3 | [태블릿에 띄우기](기기 고르기 · SSE · 푸시) | `launchers.dart:19-79` · `service/display.py:134-140` | `device` 표 · 푸시는 있음 · 띄우기는 범위 밖으로 적힘 SPEC-003:123 · SPEC-005:77 | (넣는다면) 백 · 앱 · 푸시 | 스펙이 뺀 기능 — 넣을지 정할 것(§5 Q9) |
| Q4 | 공개 API · 보안 | `api/public_questionnaire.py`(130줄) · 속도 제한 `service/questionnaire.py:72-97` | 공개 경로 = `/privacy` · `/support` 만 `routers/public_pages.py` | 백 공개 라우터 | DAY `/api` 공통 인증(Bearer · 쿠키 CSRF)을 비켜야 함 · 속도 제한 저장 위치(cc = 한 파드 메모리) 확인 안 됨 |
| Q5 | 고객 웹 페이지 | Next.js `front/app/q/page.tsx` · `components/q/QuestionnairePage.tsx`(509줄 · medikit · 6언어 문구 `lib/q/text.ts`) | 없음 · 웹 = Jinja2 + HTMX | 웹(고객 폰 모바일) | React → Jinja2/HTMX 로 다시 짜야 함 · cc DS 패키지 = React 컴포넌트 |
| Q6 | KOS 문진 양식 · 약관 · 제출 · 미리 채움 | `service/questionnaire.py:137-175`(공개 3 + 내부 `get-visitor`) | KOS 문진 경로 0 · `open()` 은 있음 `emr/kos/client.py:571` | KOS 어댑터 · 백 | SPEC-000:1076 은 문진 제출도 `external_outbox` 로 적음 — cc 는 즉시 호출 · 응답에 성공 / 실패 |
| Q7 | 이력 저장 · 직원 보기(건강 정보) | `questionnaire.py:206-231` · `reservations.py:628-645` · 앱 `reservation_detail_screen.dart:457-470` | `questionnaire_history` 표 · 읽기 `queries/customers.py:448-453`(survey) · 웹 예약 상세 「초진 문진 · 건강정보」 = 줄만 · 값 비움 SPEC-007:110 · :136 D20 | 백 쓰기 · 웹 / 앱 보기 | 「KOS 가 첫 제출본을 준다」(Q-27) 처리 · 보는 화면 자리 정할 것 |
| Q8 | 언어 결정 | `domain/languages.py`(KOS language → 국적표 → en) | 문진 언어표 없음 | 백 | 확인 안 됨 — DAY 통역 `APP_LANGS` 와 겹치는지 |

---

## 5. 정할 것 — 12개

| # | 질문 | 추천 | 근거 |
|---|---|---|---|
| Q1 | **진입 자리** — 앱 예약 탭 신설 / 시술현황 · 고객 화면에 넣기 | **예약 탭 신설**(오늘 예약 · 접수 단계 목록 → 상세에 두 버튼) | 버튼이 켜지는 때 = 예약 · 접수 단계(SPEC-007 D55) · 시술현황 판엔 그 단계 고객이 없음(`board_rule_values.py:28`) · 예약현황 메뉴는 「예약 기능이 생기면 다시 넣음」으로 숨겨 둠(SPEC-003:123) · cc 도 예약 상세에서 엶 |
| Q2 | 예약 탭의 깊이 — 목록 + 스캔 · QR 만 / 웹 예약 상세 전체(접수 · 상담사 · 방 등) | **목록 + 스캔 · QR 만** | 사용자 「주요 기능 = 여권 스캐너 · 문진 QR」 · 앞서 「사이즈가 크잖아 · 차트만」(`_RESUME.md:43`) |
| Q3 | **Android 스캐너 범위** — iOS 만 / Android 도 카메라 스캔 / Android 는 손 입력만 | **iOS 카메라 + Android 는 손 입력 길** | cc 원천은 iOS Vision 기준으로 실기기 튜닝(§1.4) · Android 원천 0 · 손 입력 길은 cc 에 이미 있음(`no_camera` → 손 입력 · `scan_screen.dart:242-249`) |
| Q4 | KOS 고객 수정을 누구 이름으로 — 로그인 직원 토큰 직접 / 시스템 계정 쓰기 큐 | **직원 토큰 직접** | DAY 사진(같은 화면 · 같은 저장 흐름)이 직원 토큰 직접 · [다시 시도](`photos.py:1-6`) · cc 도 저장 응답 안에서 성공 / 실패(④-a 실패 = 아무것도 저장 안 함) |
| Q5 | 여권 사진 KOS 등록 방식 — 시술전후사진과 같은 내부 경로 · 직원 토큰 / SPEC-000 대로 `external_outbox` | **시술전후사진 방식 재사용** | 코드가 이미 있음(`emr/kos/photos.py` · `visit_photo_kos.py`) · cc 공개 경로 대신 내부를 택한 이유가 SPEC-002:1165 에 있음 · 바꾸면 SPEC-000:1076 · :1194 고침 |
| Q6 | 여권 사진을 DAY 저장소에 둘지(DAY-ESC-001 대기 중) | **둔다 · ESC 는 참조만(비차단)** | cc D-18 「사진 = ccc · KOS 둘 다」 · SPEC 은 ESC 를 비차단으로 둠(`10-decision.md:28` · SPEC-000:81) · 저장소 용도에 이미 「고객 신분증(여권)」(SPEC-004:32) — **결정권자 몫인지 사용자 확인 필요** |
| Q7 | **문진 결과를 KOS 에 쓰나** | **쓴다(KOS 양식 · 공개 제출 그대로)** | cc D-14 · 양식 · 약관이 KOS 것 · 단 제출이 KOS 고객 성별 · 생년월일 · 주소 · 휴대폰을 바꾼다(`questionnaire.py:9` · baseline-009:76) — 이 부작용을 받는지가 판단 지점 |
| Q8 | **고객 웹을 어디서** — DAY 백엔드 공개 Jinja 페이지 / 별도 front | **DAY 백엔드 공개 페이지** | DAY 엔 별도 front 없음 · 로그인 없는 페이지 선례 `public_pages.py` · 토큰은 `#` 뒤 · 헤더로(cc 규칙 그대로 가능) |
| Q9 | [태블릿에 띄우기](다른 기기로 보내기) 넣나 | **이번 판 뺌 — [이 기기에 QR 보이기]만** | 띄우기는 SPEC-003:123 · SPEC-005:77 이 범위 밖으로 둠 · 고객이 자기 폰으로 찍는 QR 이면 이 기기 화면으로 충분 |
| Q10 | **이번 판 범위** — 스캐너 먼저 / 문진 QR 먼저 / 둘 다 | **스캐너 먼저**(진입 예약 탭과 같이) · 문진 QR 은 다음 판 | 스캐너 = 앱 · 백 · KOS(코드 있는 사진 경로 재사용) · 문진 = 공개 API · 고객 웹 · KOS 문진 경로 · 보안까지 새로라 덩어리가 큼(§4 Q4 ~ Q6) · 사용자 앞선 「사이즈」 판단(`_RESUME.md:43`) |
| Q11 | 웹 예약 상세의 비활성 [문진 QR] · [여권 스캔] 도 켜나 | **앱만 · 웹은 비활성 그대로** | 웹 예약 현황 스펙 R5 「앱으로 보내기 — 여권 스캔 · 전후 사진 · 문진」(SPEC-006:111) · 웹 스캔은 카메라가 없음 |
| Q12 | 문진 링크 수명 · 재사용 — cc 값(열기 10분 · 쓰기 60분 · 제출 1회 · 새 링크가 앞 링크 닫음) 그대로 | **그대로** | cc 운영 E2E 를 거친 값(`public_questionnaire.py:49-53`) · 바꿀 근거 없음 |

---

## 6. 확인 안 됨

- DAY 문진 6언어(ko · ja · zh-Hans · zh-Hant · en · id)와 통역 `APP_LANGS` 가 같은지
- 공개 API 속도 제한을 DAY 에서 어디에 둘지(파드 수 · 앞단 Caddy) — DAY 배포가 한 파드인지 확인 안 함
- cc `mrz.dart` 를 DAY 앱에 옮길 때 막는 의존 — 파일 자체는 `import` 0줄(grep 확인 · 순수 Dart) · 시험 파일 `test/mrz_test.dart` 의존은 열지 않음
- KOS 데모 · 운영 지점에 이미지 분류 「여권」 코드가 있는지(cc = 「운영 지점엔 있음 · 데모엔 없음」 주석 `id_photo.py:26`) — DAY 쪽 지점 값은 KOS 접속 금지로 확인 안 함
- DAY Android 에 `image_picker` 카메라를 쓸 때 CAMERA 권한이 필요한지(지금 선언 없음 · 차트 사진 카메라가 Android 에서 동작하는지) — 실행 금지로 확인 안 함
