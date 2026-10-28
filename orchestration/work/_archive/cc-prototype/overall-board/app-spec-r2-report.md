# app-spec r2 결과 보고 — 앱 계약 리뷰 r1 처분(SPEC-004 0.4.1 · DEC-007 · WORK-009)

## 상태: done (문서만 · 코드 미착수 · 커밋 0 · 리뷰 대기)

원천: `app-review-doc-r1.md`(FAIL 6 · WARN 14 · U1 ~ U6) · `app-wp-kos-report.md`(K1 ~ K4 · Q-154 ~ Q-157) · `_RESUME` §2 10-27 「앱 계약 리뷰 r1 사용자 결정 U1~U6 기본값」 · 지시 `app-spec-r2-instructions.md`. 바뀐 줄 끝 표기 `(r2)`.

## 수행 내용

| 문서 | 무엇 |
|---|---|
| `para/.../20-spec/spec-004-procedure-app.md` | 0.4.0 → **0.4.1** · 머리말 0.4.1 줄 · sources 한 줄 · `(r2)` 53곳 |
| `para/.../10-decision/decision-007-app-v2.md` | **D-67 ~ D-72 새 절**(U1 ~ U6 · 코디 기본값) · D-16 · D-33 · D-41 · D-43 · D-45 · D-54 · D-61 에 「→ D-xx」 · 열린 것 · 부록 A 한 줄 |
| `para/.../30-work/work-009-app-v2.md` | WP-KOS **완료** · 산출 이름 · WP-INFRA 암호화 확인 · WP-BE1 대상 파일(stream · board · db) · BE2 ~ BE5 · APP1 · APP3 ~ APP6 · FE 줄 · 고정점(경로 50 · 기기 · 사진) · 병렬 그림 |
| `para/.../20-spec/spec-005-reservation-board.md` | W4 — 낡은 두 줄 취소선 + 「SPEC-004 0.4.0 로」 · §7.3 머리에 가리킴 한 줄(아래 주의) · 버전 그대로 |
| `reference/2026-10-27-cc-app/workflow-app.md` | §10 머리에 메모 한 줄(U1 ~ U6 이 AP-6 · 12 · 19 · 21 · 23 · 30 · 35 · 41 을 어떻게 읽는지 → DEC-007 이 이김) |
| README 3 · `log.md` | SPEC-004 0.4.1 · DEC-007 D-67 ~ 72 · WORK-009 WP-KOS 완료 · log 한 줄 |

## 처분 → 고친 곳 대조표 (빠짐 0)

S4 = SPEC-004 · D7 = DEC-007 · W9 = WORK-009 · S5 = SPEC-005

### FAIL 6

| # | 처분 | 고친 곳 |
|---|---|---|
| F1 `push_log.call_id` NOT NULL | **표 다시 만들기**로 정함 — `Database.__init__` `MIGRATIONS` 뒤 한 번: `call_id.notnull = 1` 이면 한 트랜잭션에서 `push_log_new` → 옛 행 복사(`kind = doctor_call`) → DROP → RENAME · 멱등 | S4 §7.4 머리 「`push_log` 다시 만들기」 · §7.4 `push_log` 줄 · §5-2 `push_log` 줄 · **§8.6 「마이그레이션」(옛 모양 DB 파일에서 시작 · 새 DB 시험으로 대신 금지)** · W9 WP-BE1(`repository/db.py` · 시험 키 `migrat`) |
| F2 사진 열람 쿠키 | **fetch + Bearer → blob URL**(지금 인증 = 헤더만 · 새 토큰 체계 없음 → 서명 URL 대신 이쪽) · 앱 = `Image.network` 에 헤더 | S4 §6.17 썸네일 칸 · §6.17 아래 r2 두 줄 · §8.6 스캔(헤더 없음 · `?token=` = 401) · §8.8 E7 · W9 WP-BE5 · WP-FE · 고정점 |
| F3 기기 식별 | `deviceId` 를 SSE 쿼리 · `pending?deviceId=`(필수 · 없으면 400) · claim `{qrToken, deviceId?}` · 문진 GET 쿼리 · POST 본문 · 스캔 본문 · unlock 본문에. back = `device.account_id` 가 로그인 계정인지 · 아니면 **404 `device_not_found`**(SSE 만 무시). 알림 거부 기기(행 없음) 처리 | S4 §5-1.1 아래 `deviceId` 문단 · §5-3 기닿기 ③ · QR 줄 · **「기기 확인」 줄** · §3.4 · §6.11 [이 기기에서 열기] · §6.15 ① ⑥ · §7.3 오류 코드 · §8.6 띄우기(태블릿 · 폰 가르기) · §8.8 E6 · W9 고정점 · BE1 · BE3 · BE4 · APP1 · APP4 · APP5 |
| F4 K4 경로 | `get-visitor-files`(= 첨부 파일) → **`image/visitor-image/v1/queries/get-visitor-images`**(Q-154) | S4 §8.0 #23 · §8.8 E7 · W9 WP-KOS · OQ-619 닫음 |
| F5 K2 · K3 결과 | ④-a K2 조건 지움 · 만료일 보냄(내부 `get-visitor` 에만 보임) · ④-c 본문 = `fileName · visitorId · source:"HOSPITAL" · shootingDateTimeUtc · equipment · memo` · `category` · `scheduleId` · `path` 안 보냄(Q-155 · Q-156) · 장비 = **업로드 때마다 `get-codes` 에서 이름 「태블릿」 객체 그대로** · 못 찾으면 `failed` · `equipment_code_missing` · §8.0 #8 · #21 · #22 · #23 = 확인 · 「못 넘으면」 분기 = 기록만 · 흔적 둠(Q-157) | S4 §6.16 ④-a · ④-c · §7.4 `kos_error` · §8.0 머리 · #8 · #21 · #22 · #23 · 끝 줄 · §8.6 스캔 · §9 OQ-619 · OQ-622 닫힘 · W9 WP-KOS 완료 · WP-BE2 · BE5 의존 갱신 |
| F6 AP-41 암호화 | U2 대로 — 지원하면 켬 · 안 되면 없음 + 주석 · infra 확인 · 보고 | D7 D-54 · **D-68** · S4 §1.1 infra · §2.3 `PROC_PHOTO_DIR` · §7.4 `id_photo` · **OQ-626(새)** · W9 WP-INFRA 완료 조건 · 고정점 |

### WARN 14

| # | 처분 | 고친 곳 |
|---|---|---|
| W1 SSE 허브 | 연결마다 `(account_id, device_id?)` · `publish()` = 전부(board) · `send_to_account`(notification) · `send_to_device`(display) · `online` = 기기 연결 · **새 이벤트 `id:` 없음 · version 안 올림** · 앱 파서 `board` 만 version | S4 §7.1 파싱 줄 · **「허브」 줄** · §5-3 ① · §8.6 「SSE 허브」 · §8.7 · W9 WP-BE1 대상 파일 `service/stream.py` · `api/board.py` · APP4 |
| W2 이력 UNIQUE 충돌 | 같은 제출본 `read` 행이 있으면 **그 행을 `app_submit` 으로 고침**(언어 · 기기 · 요청 채움) · 읽기 쪽 `INSERT OR IGNORE` 그대로(덮지 않음) | S4 §6.15 ⑥ · §7.4 `questionnaire_history` · §8.6 문진 · W9 WP-BE4(`repository/repo.py`) |
| W3 「13키」 | SPEC-005 §5.13 함수 그대로 — 다시 읽은 응답에 있는 `PERSONAL_KEYS` 전부 · 고정 수 단언 금지 | S4 §6.16 ④-a · §8.6 스캔 · D7 D-16 · W9 WP-BE5 |
| W4 SPEC-005 낡은 줄 | 「상담사 계정 이번 판 없음」 · 「앱 알림 이번 판 없음」 취소선 + SPEC-004 0.4.0 로 · §7.3 머리에 「앱 판이 `displays[]` · `identity` 열 더함 → SPEC-004」 한 줄 | S5 §3(로그인 표 아래 줄) · §4 [실장 호출] 줄 · §7.3 머리 |
| W5 §6.17 잔재 줄 | 지움(그 자리 = r2 두 줄) | S4 §6.17 |
| W6 WP-KOS 산출 이름 · 상태 | `app-wp-kos-report.md` · **완료** | W9 WP-KOS |
| W7 병렬 그림 | WP-FE = BE3 · BE5 뒤 바로(앱과 따로) · REVIEW = APP6 · FE 뒤 | W9 병렬 그림 + 한 줄 |
| W8 문진 → KOS 고객 값 · 휴대폰 0 | 제출이 성별 · 생년월일 · 주소 · 휴대폰 · 동의를 바꾼다는 것 · **휴대폰 = KOS 가 앞 0 뺀 꼴로 저장 · ccc 는 고치지 않고 그대로** · 시험은 그 값을 맞는 값으로(11자리 단언 금지) | S4 §6.15 ⑥ · §8.6 문진 · §8.8 E6 |
| W9 잠금 범위 · 아이디 잠김 | 대기 화면도 잠금 · 나가는 길 = [직원] 길게뿐 · 나가기 = **새 `POST /api/auth/unlock`**(U5) | S4 §6.15 ⑦ · 잠금 문단 · §3.3 · §3.4 · §7.3 · §8.6 · §8.7 · §8.8 E6 · W9 WP-BE4 · APP5 |
| W10 MRZ 세기 | 생년월일 = `20YY` 가 오늘 뒤면 `19YY` · 만료일 = 늘 `20YY` → `yyyy-MM-dd` · 데스크가 고칠 수 있음 | S4 §6.16 ② · §8.7 · W9 WP-APP6 |
| W11 AP-21 「조용한 알림」 | U1 — 보이는 알림 · 소리 없음 · 목록 · 배지 · 설정 밖 | S4 §2.4 · §5-3 ② · §8.6 띄우기 · OQ-620 닫음 · D7 D-43 · **D-67** · WA 메모 |
| W12 알림 원천 | U3 — 계정 행(기기 없어도) | S4 §5-4 원천 · D7 D-41 · **D-69** · WA 메모 |
| W13 설정 기기 이름 | U4 — 칸 넣음 · 기기 행 없으면 안내 | S4 §6.14 · D7 D-61 · **D-70** · W9 WP-APP1 · WA 메모 |
| W14 [스캔할 기기] | U6 — 앱은 이 기기 [여권 스캔]만 · 다른 기기로 = 웹 | S4 §6.11 · §6.17 · D7 D-33 · **D-72** · W9 WP-APP3 · WA 메모 |
| 그 밖 | `POST /api/devices` 「세 역할」 → 다섯 · §5-1.2 받는 사람 표에 coordinator · counselor 「안 받음」 줄 | S4 §5-1.1 · §5-1.2 |

### 사용자 결정 U1 ~ U6 (코디 기본값)

| U | DEC-007 | SPEC-004 |
|---|---|---|
| U1 띄우기 = 보이는 알림 · 소리 없음 · 목록 · 배지 · 설정 밖 | D-67 | §2.4 · §5-3 ② · OQ-620 닫힘 · 부록 C |
| U2 볼륨 암호화 = 지원하면 켬 · 안 되면 없음 + 주석 · infra 확인 | D-68 · D-54 | §1.1 · §2.3 · §7.4 · OQ-626 · W9 WP-INFRA |
| U3 알림 목록 = 계정 행 | D-69 · D-41 | §5-4 |
| U4 설정 「이 기기 이름」 | D-70 · D-61 | §6.14 |
| U5 잠금 해제 실패 = 기기별 5회 · 1분 · 아이디 안 잠금 | D-71 · D-45 | §3.3 · §3.4 · §6.15 · §7.3(경로 50) · §8.6 · W9 WP-BE4 · APP5 |
| U6 앱 상세 = 이 기기 [여권 스캔]만 | D-72 · D-33 | §6.11 · §6.17 |

### WP-KOS Q-154 ~ Q-157 (코디 기본값)

| Q | SPEC-004 |
|---|---|
| Q-154 K4 경로 = `get-visitor-images` | §8.0 #23 · §8.8 E7 · W9 WP-KOS |
| Q-155 `category` 안 보냄 · KOS 코드 만들지 않음 | §6.16 ④-c · §8.0 #22 · OQ-622 닫힘 |
| Q-156 `scheduleId` · `path` 안 보냄 | §6.16 ④-c · §8.0 #22 · OQ-622 닫힘 |
| Q-157 데모 흔적 둠 | §8.0 끝 줄 · W9 WP-KOS |

## 검증

| 항목 | 결과 |
|---|---|
| 처분 대조 | FAIL 6 · WARN 14(+ 그 밖 2) · U 6 · Q 4 · 경로 50 = **32 항목 × 고친 곳 문구 스크립트 대조 — 빠짐 0**(W5 는 「잔재 줄 없음」 확인) |
| 낡은 문구 grep | SPEC-004 에서 취소선 밖 `13키` · `get-visitor-files` · `route_count_49` · `경로 49` · `로그인 쿠키` · `K2 전` · `게이트 K` · `{source, category, equipment}` = **0**(0.4.0 머리말 이력 줄 · 부록 C 대응 줄 · 「게이트 K1 ~ K4 = 통과」 문구만 남음) |
| public grep | 바뀐 9 파일: 24자 hex · uuid · `eyJ` · `Bearer <값>` · 메일 · `+82` · 휴대폰 꼴 · `AKIA` = **0**. KOS 코드는 이름(「태블릿」)만 · id 없음 |
| frontmatter | SPEC-004 `version 0.4.1` · sources 줄 · DEC-007 · WORK-009 sources 줄 · `updated_at` 2026-10-27 그대로 |
| allowed_paths | 앞 판 목록 + SPEC-005(W4 줄 · §7.3 가리킴 한 줄) 안 · 코드 · 다른 문서 수정 0 · 커밋 0 |
| 린트 | `scripts/lint-pipeline.py` 이 레포에 없음(앞 판과 같음) — 돌리지 못함 |
| 코드 근거(읽기만) | `repository/db.py:54`(`call_id NOT NULL`) · `:158-173`(ADD COLUMN 만) · `:150-153`(UNIQUE) · `repository/repo.py:486`(`INSERT OR IGNORE`) · `service/stream.py`(큐 집합 하나) · `api/board.py`(토큰 값 버림) · `service/reservations.py:162 · :1036 · :1093`(만료일 이미 읽고 · 보냄) — `kknaksss/overall-board-2` `95c64bc` |

## 계약에서 새로 정한 구현값(결정 밖 · 리뷰가 볼 곳)

- **`POST /api/auth/unlock {password, deviceId?}`** — U5 를 지키려면 로그인 경로를 쓸 수 없어 새 API 하나(경로 49 → **50**). 실패 수는 기기마다 · `deviceId` 없으면 계정의 「기기 없음」 한 칸 · 토큰 안 바꿈
- 알림 거부 기기 = `device` 행 · `deviceId` 없음 → targets 밖 · pending 안 부름 · claim · 문진 · unlock 은 `deviceId` 없이(이력 `device_id` null)
- claim 에 `deviceId` 가 오면 이미 다른 기기로 보낸 요청도 그 기기로 바꿈
- 장비 코드 = 업로드 때마다 `get-codes`(캐시 없음) · 못 찾으면 `failed` · `equipment_code_missing`(다시 올리기로 회복)
- KOS 이미지 `memo` = 「ccc 여권 스캔」 고정 글자 · `fileName` = ccc 무작위 파일 이름 재사용
- 웹 썸네일 = fetch → blob(서명 URL 은 만들지 않음 — 지금 인증 구조 그대로)

## 미결 · 주의점

- **OQ-626(새)**: 볼륨 암호화 가능 여부 — WP-INFRA 확인 · 보고 뒤 닫는다
- SPEC-005 §7.3 머리에 한 줄을 더했다 — 지시 「그 줄만」보다 한 줄 많다(W4 근거가 §7.3 응답 변경도 짚어서 가리킴만 둠 · 응답 블록은 안 고침). 빼라면 그 한 줄만 지우면 된다
- SPEC-005 §4 [실장 호출] 줄의 「접수 뒤 단계에서는 미시험 → E2E #25」는 K1 로 확인됐지만 W4 범위 밖이라 두었다(SPEC-005 판에서 닫을 것)
- 경로 수 50 은 ② 시술 현황 판(WORK-008)이 경로를 더하지 않는다는 전제 — 더하면 그 수 + 15 로 다시 센다(S4 §7.3 에 적음)
- 남은 OQ: 621 · 623 · 624 · 625 · 626 (+ 0.3.0 이전 열린 것 그대로)
