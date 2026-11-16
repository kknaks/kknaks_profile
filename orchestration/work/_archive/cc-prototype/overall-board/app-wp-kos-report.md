# 앱 WP-KOS 게이트 — 데모 실호출 K1 ~ K4

- 조사일: 2026-10-27 (KST) · 조사자: cc-prototype researcher (task_0cef45eebef6)
- 계약: WORK-009 WP-KOS 줄 · SPEC-004 0.4.0 §8.0 #8 · #21 ~ #23 · §6.16 ④-a · ④-c · OQ-619 · OQ-622
- 원천
  - 데모 실호출(2026-10-27, 데모 테넌트) — 아래 §5
  - 공개 스펙 `openapi.yaml` 1.0.1(2026-10-26 받은 사본 · `Image` 태그 · `protos.image.RegisterVisitorImageConfiguration` · `protos.tenant.Code`)
  - KOS 웹앱 JS `visitor-information-client_v0.0.157`(2026-10-26 받은 사본 · 다시 받지 않음) — 내부 경로 이름 · 본문 키
  - 앞 판: `app-kos-report.md`(AK§) · `reservation-kos-probe-report.md`(KP§) · `reservation-consultation-report.md`(CS§) · `reservation-create-report.md`
- 표기: **확인** = 데모에서 호출해 본 것 · **스펙** = openapi.yaml · **JS** = 웹앱 코드 · **추정** = 해석
- 리포트에 테넌트 · 고객 · 일정 · 계정 · 코드 id, 토큰, presigned URL, 이름, 만료일 값은 적지 않았다. 모양 · 필드 이름 · 상태 · 코드 **이름**(KOS 지점이 붙인 표시 이름)만 적는다
- 산출 경로: 브리프대로 `app-wp-kos-report.md`. WORK-009 WP-KOS 줄의 산출 칸은 `app-kos-probe-report.md` 라고 적혀 있다 — 이름이 다르다(코디 확인)

---

## 0. 게이트 판정

| 게이트 | 호출 | 판정 | 한 줄 |
|---|---|---|---|
| **K1-a** | 내부 `update-reservation{scheduleId, counselor}` · `CONSULTATION_WAITING` 일정 | **받음** | 200 `{}` · `reservation.counselor` 만 바뀜 · 단계 그대로 |
| **K1-b** | 같은 호출 · `CONSULTATION` 일정 | **받음** | 200 `{}` · 같음 |
| **K2** | 내부 `update-visitor-personal-information` + `passportExpiryDate`(`yyyy-MM-dd`) | **받음** | 200 `{}` · 내부 `get-visitor` 에 **보낸 문자열 그대로** 생김 · 다른 칸 그대로 |
| **K3** | 공개 `generateUploadingImageUrl` → PUT → `registerVisitorImages` | **받음** | 200 · 200 · 200 `{}` · 내부 이미지 목록에 1장 · 받아 보니 올린 바이트와 같다 |
| **K4** | 내부 `get-visitor-files` | **모양 다름** | 200 · **0건**(올린 사진이 안 보인다). 사진은 다른 내부 조회 `image/visitor-image/v1/queries/get-visitor-images` 에 보인다(확인) |

- **SPEC-004 §8.0 끝 줄의 「못 넘으면」 분기는 하나도 타지 않는다.** K1 · K2 · K3 모두 받음. K4 는 「기록만(기능 영향 없음)」 자리이고, 조회 경로 이름만 다르다 → §6 Q-154
- K1 은 앞 판으로 닫을 수 없었다: 웹 SPEC-005 §9 #25(접수 뒤 실장 호출) 결과는 어느 리포트에도 없다(`reservation-e2e-batch1 ~ 3-backend-report` · `reservation-e2e-feedback` grep). KP§ K5 는 `RESERVED` 에서만 보냈다(KP§ 98줄). CS§ HAR 에는 **KOS 웹 사용자가** `CONSULTATION_WAITING` 에서 같은 호출을 보내 `{}` 를 받은 기록이 있다(CS§ W3) — ccc 호출이 아니고 `CONSULTATION` 은 없어서 호출했다

---

## 1. K1 — 접수 뒤 상담사 지정

### 1.1 대상 · 보낸 것

| | K1-a | K1-b |
|---|---|---|
| 일정 | `[ccc 시험]` 고객 일정 · `IN_PROGRESS` · **`CONSULTATION_WAITING`**(앞 판 batch 1 이 남긴 것) | `[ccc 시험]` 고객 일정 · `IN_PROGRESS` · **`CONSULTATION`** |
| 전 `reservation.counselor` | 비어 있음(`{id:"", name:""}` 꼴) | 비어 있음 |
| 본문 | `{scheduleId, counselor:{id, name}}` — ccc `reception.py` [실장 호출] 과 같은 2키 | 같음 |
| 상담사 | 공개 `get-accounts` 에서 `roleTags ∋ COUNSELOR` · `activate:true` · 시스템 계정 · `KOS_EXCLUDE_ACCOUNT_IDS` 뺀 목록(10명)의 첫째 | 같은 목록의 둘째 |
| 응답 | **200 `{}`** | **200 `{}`** |

### 1.2 전 ↔ 후 (2초 뒤 다시 읽기 · 응답 전체를 펼쳐 키마다 비교)

| 조회 | 바뀐 키 | K1-a | K1-b |
|---|---|---|---|
| 내부 `schedule/v1/queries/get-schedule-detail` | `reservation.counselor.id` · `reservation.counselor.name` · `updatedDateTimeUtc` **3개뿐** | 같음 | 같음 |
| 공개 `getScheduleDetail` | `data.reservation.counselor.id` · `.name` · `data.updatedDateTimeUtc` **3개뿐** | 같음 | 같음 |

- 바뀐 상담사 = **보낸 계정과 같다**(id 비교, 확인)
- **단계(`flowStep`)는 그대로**다 — 상담 대기는 상담 대기, 상담 진행은 상담 진행(확인)
- **일정 요약 `consultation{counselor, doctor, consultationMemo}` 는 바뀌지 않는다**(diff 에 없음, 확인). 이 요약과 `consultations[]`(상담 기록)는 KOS 웹 [상담 시작] 의 `create-consultation` 이 채운다(CS§2). 즉 ccc [실장 호출] 은 「희망 상담사」 칸만 바꾸고 KOS 상담 기록은 만들지 않는다 — DEC-006 「상담 기록 · 상담 진행은 KOS 가 만든다」와 같다
- `CONSULTATION` 일정인데 `reservation.counselor` 가 비어 있었다. 공개 스펙의 「상담 진행으로 바꿀 때 상담 담당자가 없으면 `counselor NotFound`」 조건은 이 칸이 아니라 상담 기록 쪽을 보는 것으로 보인다(추정 · CS§ Q-94 재료)
- 화면 근거: ccc 예약 현황 · 상세가 읽는 내부 `get-schedule-detail` · 공개 `getScheduleDetail` 두 곳 모두에 새 상담사가 보였다. KOS 웹 화면은 열어 보지 않았다

---

## 2. K2 — 여권 만료일

### 2.1 보낸 것

| 항목 | 내용 |
|---|---|
| 대상 | AK§6 의 시험 고객(같은 사람 · 국적 · 언어 · 여권번호가 이미 들어 있음). 쓰기 직전 내부 `get-visitor` 로 다시 읽고 이름이 `[ccc 시험]` 으로 시작하는지 assert |
| 본문 | ccc `reservations.py` `personal()` 과 같은 규칙 — `id` + `PERSONAL_KEYS` 17개 중 **다시 읽은 응답에 있는 키 전부**(이 고객은 14개: `name · phoneticName · phoneNumber · dateOfBirth · gender · registrationNumber · foreignRegistrationNumber · passportNumber · passportSurname · passportGivenNames · address · nationality · language · snsInfo`) + **`passportExpiryDate`(`yyyy-MM-dd` 문자열 · 가상 날짜)** = 16키 |
| 전 상태 | `passportExpiryDate` **키 없음**(데모 시험 고객 10명 모두 키 없음, 확인) |
| 응답 | **200 `{}`** |

- 앞 판 HAR(13키)과 달리 이번에는 `phoneNumber` · `snsInfo` 를 넣었다 — 이 고객은 AK§5 문진 제출로 휴대폰이 생겼고, ccc 함수는 「있는 키는 보낸다」이기 때문이다. 둘 다 그대로 남았다

### 2.2 전 ↔ 후

| 조회 | 결과 |
|---|---|
| 내부 v2 `get-visitor` | 바뀐 키 = **`passportExpiryDate`(키 생김)** · `updatedDateTimeUtc` **2개뿐**. 저장 값 = 보낸 문자열 그대로(`yyyy-MM-dd` · 문자열). `dateOfBirth` 처럼 `00:00:00.000Z` 가 붙지 않는다 |
| 내부 v1 `get-visitor`(옛 경로) | 같은 키 · 같은 값 |
| 공개 `getVisitor` | 바뀐 키 없음 · **만료일 키 없음** — 공개 고객 조회에는 안 보인다 |
| 공개 `getSchedulesByVisitor` | `data[0].updatedDateTimeUtc` 만 바뀜(고객 수정이 일정 수정 시각을 움직인다 — 추정: 일정에 실린 고객 사본 갱신) |

- **결론**: SPEC-004 §6.16 ④-a 의 「`passportExpiryDate` 는 K2 확인 전 보내지 않는다 · `skipped`」 조건이 풀린다. 꼴은 `yyyy-MM-dd`, 읽기는 내부 `get-visitor` 에서만 된다
- 형식이 틀린 값(예: `yyyy-MM-dd 00:00:00.000Z`)을 보냈을 때 거절하는지는 시험하지 않았다(1회 허가)

---

## 3. K3 — 공개 이미지 올리기

### 3.1 분류 · 장비 코드 고르기 (내부 `meta/codes/v1/queries/get-codes`)

| `category` | 건수 | 코드(표시 이름 · `closed` · `default` · `order`) |
|---|---|---|
| `IMAGE_CATEGORY`(이미지 분류) | 2 | 「시술 전」 false · false · 0 / 「시술 후」 false · false · -1 |
| `IMAGE_EQUIPMENT`(이미지 장비) | 5 | 「태블릿」 false · false · 0 / 「피부진단기」 false · false · 1 / 「DSLR」 false · **true** · 2 / 「APE」 false · **true** · 3 / 「ETC」 false · **true** · 4 |

- 코드 객체 키 = `id · category · name · order · closed · default`(확인). 스펙 `protos.tenant.Code` 의 필수 5개 + `default`. `color` 는 이 지점 코드에 없다
- **고른 것**
  - `equipment` = **「태블릿」** — 앱이 아이폰 · 아이패드 카메라로 찍는다(SPEC-004 §6.16 ①). 5개 중 기기와 맞는 것은 이것뿐이다. `default:true` 가 3개(DSLR · APE · ETC)라 「기본값」으로 고를 수는 없다
  - `category` = **보내지 않음** — 지점 분류가 「시술 전 / 시술 후」 둘뿐이고 여권 사진은 어느 쪽도 아니다. 「시술 전」으로 넣으면 KOS 시술 사진 모음에 신분증이 섞인다(추정). 스펙에서 `category` 는 선택 칸이다(`required` = `fileName · visitorId · source · shootingDateTimeUtc`) → Q-155
- 코드를 **만드는** 것(예: 「신분증」 분류 `create-code` — JS)은 허가 밖이라 하지 않았다

### 3.2 호출 순서 · 결과

| # | 호출 | 보낸 것 | 응답 | 판정 |
|---|---|---|---|---|
| ① | 공개 `POST /image/open/v1/commands/generate-uploading-url` | `{fileName}` — `ccc-test-<무작위 32자>.png`(고객 정보 없는 이름 · 스펙 「병원별 유니크」) | **200 `{data: "<presigned URL>"}`** · S3 presigned PUT(`X-Amz-Algorithm · Credential · Date · Expires · Security-Token · Signature · SignedHeaders`) | 스펙과 같다 |
| ② | `PUT <presigned URL>` | 지어낸 그림 PNG(1250 × 880 · 단색 + 흰 「TEST」 글자 · 12.7KB) · `Content-Type: image/png` · 인증 헤더 없음 | **200**(본문 없음) | 스펙과 같다 |
| ③ | 공개 `POST /image/open/v1/commands/register-visitor-images` | `{images:[{fileName(①과 같음), visitorId, source:"HOSPITAL", shootingDateTimeUtc(ISO · Z), equipment:{get-codes 객체 그대로 6키}, memo:"[ccc 시험] TEST 그림"}]}` — `category` · `path` · `scheduleId` 없음 | **200 `{}`** | 받음 |

- 오류 className: 없음(세 호출 모두 2xx)
- `source` 는 스펙 enum 중 `HOSPITAL`(원내 촬영)을 골랐다. `VISITOR`(내원객 촬영)는 고객이 자기 폰으로 찍은 것이라 맞지 않는다(스펙 표)

### 3.3 등록 결과 (K4 와 함께 읽음)

내부 `image/visitor-image/v1/queries/get-visitor-images{visitorId}` — 전 0건 → **후 1건**. 항목 모양:

```text
{ id, visitorId, scheduleId, source, equipment{id, category, name, order, closed, default},
  fileName, shootingDateTimeUtc, deleted, memo }
```

| 키 | 보낸 값과 |
|---|---|
| `fileName` | 같다 |
| `source` | `HOSPITAL` 같다 |
| `equipment` | 「태블릿」 코드 같다 |
| `memo` | 같다 |
| `deleted` | `false`(스펙 「삭제되지 않은 상태로 생성」) |
| `scheduleId` | `""` — 안 보냈으니 일정에 안 묶였다 |
| `category` · `path` | **키 없음**(안 보낸 선택 칸은 응답에서 빠진다) |

- **바이트 확인**: 내부 `image/v1/commands/generate-signed-url{fileName}` → 200 `{data{url}}` → `GET` 200 `image/png` · **올린 파일과 sha256 같다**(확인). 이 호출은 열람 URL 을 만드는 것이고 데이터를 바꾸지 않는다(JS 이름 · 응답으로 판단 — 추정)

---

## 4. K4 — 내부 고객 파일 조회

| 조회 | 전 | 후 | 메모 |
|---|---|---|---|
| 내부 `visitor/files/v1/queries/get-visitor-files{visitorId}` | 200 · 0건 | **200 · 0건** | WORK-009 · SPEC-004 §8.0 #23 이 적은 경로. **올린 사진이 안 보인다** |
| 내부 `image/visitor-image/v1/queries/get-visitor-images{visitorId}` | 200 · 0건 | **200 · 1건** | §3.3 |

- KOS 웹앱 JS 에서 둘은 다른 기능이다: `visitor/files/v1/*` = **고객 첨부 파일**(`create-visitor-file{fileName, persistenceFileName, mimeType, visitorId}` · `generate-signed-file-urls`), `image/visitor-image/v1/*` = **고객 이미지**(`register` · `update` · `delete-visitor-images` · `get-visitor-images`). 공개 `registerVisitorImages` 는 뒤쪽에 들어간다(확인)
- **판정 = 모양 다름**: 게이트가 묻는 「올린 사진이 KOS 고객 이미지로 보이나」의 답은 **보인다**(이미지 쪽). 다만 SPEC 에 적힌 조회 경로가 틀렸다 → Q-154. SPEC-004 §8.0 대로 ccc 기능에는 영향 없다(ccc 는 자기 저장소로 연다)
- KOS 웹 화면(고객 상세 · 이미지 탭)은 열어 보지 않았다 — 사용자 눈 확인 자리(SPEC-004 §8.8)

---

## 5. 호출 기록 · 데모 확인 · 흔적

**데모 테넌트 확인**(값은 출력하지 않고 같은지만 비교 · 스크립트 assert)
- `.env` 공개 키 = ax-clinic-project `KOS_API_tenent_dev` → **같다** · 운영 `KOS_API_tenent` → **다르다**
- 시스템 계정 sign-in 응답 `tenantIds` 에 `.env` 테넌트 id 가 있다
- 쓰기 대상마다 이름이 `[ccc 시험]` 으로 시작하는지 확인(10명 모두 시험 고객)

**호출**(2026-10-27 · 데모 테넌트 · 합계 71 · 모두 2xx · 운영 키 0)
- 공개: `exchange-token` 5 · `getSchedulesByVisitor` 14 · `getScheduleDetail` 4 · `get-accounts` 2 · `getVisitor` 2 · **`generate-uploading-url` 1** · **`register-visitor-images` 1(쓰기)**
- presigned `PUT` 1(쓰기 · S3) · 열람 URL `GET` 1
- 내부: sign-in 7 · `get-user-account` 1 · `get-visitors` 1 · v2 `get-visitor` 13 · v1 `get-visitor` 1 · `get-schedule-detail` 6 · `get-codes` 3 · `get-visitor-files` 3 · `get-visitor-images` 4 · `generate-signed-url` 1 · **`update-reservation` 2(쓰기)** · **`update-visitor-personal-information` 1(쓰기)**
- **쓰기 = 브리프 허가 그대로**: K1 2 · K2 1 · K3 1 묶음(URL 발급 · PUT · 등록). 그 밖 쓰기 0

**남긴 데모 흔적 — 되돌리지 않았다**(브리프에 되돌리기 지시 없음)
1. K1-a: `[ccc 시험]` 고객 일정 1건(`CONSULTATION_WAITING`)의 `reservation.counselor` 빈칸 → 데모 상담사 1명
2. K1-b: `[ccc 시험]` 고객 일정 1건(`CONSULTATION`)의 `reservation.counselor` 빈칸 → 데모 상담사 1명(1 과 다른 사람)
3. K2: AK§6 시험 고객 1명에 `passportExpiryDate`(가상 날짜) 키가 생김
4. K3: 같은 고객에 **고객 이미지 1장**(지어낸 「TEST」 그림 · `source HOSPITAL` · 장비 「태블릿」 · 메모 `[ccc 시험] TEST 그림` · 일정 연결 없음) + KOS 저장소(S3)에 그 PNG 파일 1개
- 되돌리는 길(부르지 않음): 1 · 2 = 같은 `update-reservation` 에 빈 상담사(빈 값을 받는지는 모름) · 3 = 같은 `update-visitor-personal-information` 에 `""`(지워지는지는 모름) · 4 = 내부 `image/visitor-image/v1/commands/delete-visitor-images`(JS 에만 있음 · 본문 모양 미확인 · S3 파일이 지워지는지 모름)
- 앞 판 흔적(AK§7 — 국적 · 언어 · 여권 · 문진 제출 등)은 같은 고객에 그대로 있다

**빠진 행**
- 브리프 쓰기 목록 K1(2) · K2(1) · K3(1) · K4(조회) → §1 · §2 · §3 · §4. 각 결과에 상태 · 오류 className · 바뀐 필드 · 화면 근거 · 판정을 적었다(오류 className 은 거절이 없어 모두 「없음」)

---

## 6. 정할 것 (결정하지 않음) — 4개

| # | 자리 | 왜 정해야 하나 |
|---|---|---|
| Q-154 | SPEC-004 §8.0 #23 · WORK-009 K4 의 조회 경로 | 적힌 `get-visitor-files` 에는 올린 사진이 안 보이고 `get-visitor-images` 에 보인다. SPEC · 시험(§8.8 E2E 확인 방법)의 경로 이름을 고칠지. 기능 영향은 없다 |
| Q-155 | `registerVisitorImages.category`(OQ-622) | 데모 지점 분류는 「시술 전 / 시술 후」 둘뿐이다. ① 보내지 않음(이번 시험 · 받음) ② 지점에 「신분증」 분류를 만들어 그 코드를 보냄(지점 설정 · 운영 지점도 따로) ③ 기존 코드 하나. 장비는 「태블릿」 하나로 맞다. 값은 지점마다 id 가 달라 **코드 상수(이름) → 실행 때 `get-codes` 로 id 찾기**가 필요하다(코드 객체 6키 전체를 보내야 하는지, `id` 만으로 되는지는 시험 안 함) |
| Q-156 | `registerVisitorImages.scheduleId` · `path` | 스펙에 「연결된 스케줄 ID」 · 「폴더 경로」 칸이 있다. 안 보내면 일정에 안 묶이고(`scheduleId:""`) 폴더 없음. 스캔은 예약 상세에서 열리니 그 일정 id 를 넣을지, 폴더(예: 신분증)를 쓸지. SPEC-004 §6.16 ④-c 는 `{source, category, equipment}` 만 적었다 |
| Q-157 | 데모 흔적 되돌리기 | §5 의 4가지. 그대로 둘지, 되돌릴지(상담사 · 만료일을 빈 값으로 받는지, 이미지 삭제 본문 · S3 삭제 여부는 미확인) |

- 참고(정할 것 아님): K1 은 「희망 상담사」 칸만 바꾸고 KOS 상담 요약 · 상담 기록은 건드리지 않는다(§1.2). 만료일은 공개 조회에 안 보인다(§2.2) — 앱 스캔 확인 화면의 「KOS 지금 값」은 내부 `get-visitor` 기반 응답(`personal`)이어야 만료일이 나온다
