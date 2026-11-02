# backend — 여권 사진 KOS 등록 = KOS 웹과 같은 꼴 · 분류 「여권」 (코디 · 2026-10-28) — **먼저 이것, 그다음 WORK-010 WP-BE**

사용자: KOS 에 여권 사진이 여전히 안 보인다 · KOS 웹 여권 스캔 HAR `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/여권스캔.har`(데모 테넌트) · **데모 지점 분류엔 「여권」이 없고 운영(prod) 지점엔 있다**.
(코디 확인: 운영 `id_photo` 는 fad8b56 배포 전 1장뿐 — 수정 뒤 다시 찍은 적 없음)

1. HAR 해부(모양만): `image/v1/commands/generate-presigned-url` → S3 PUT → `image/visitor-image/v1/commands/register-visitor-images` 본문 전부(scheduleId · category · equipment · shootingDateTime · fileName · source 등) · `meta/codes/v1/queries/get-codes` 어떤 코드 그룹을 읽나 → **ccc 본문과 필드마다 대조**(지금 ccc 는 공개 `generateUploadingImageUrl` 경로 — 다르면 HAR 경로로 바꿀지 판단 · 근거 보고)
2. **분류**: `get-codes` 에서 **이름이 「여권」인 코드를 찾아 category 에 넣는다** · 없으면(데모) category 를 안 보낸다(지금처럼) · 이름 판정은 이 한 곳 · 시험(있음 · 없음)
3. 데모 실호출 1회(허가 · TEST 그림 · 데모 assert · 운영 키 금지) — HAR 꼴로 올려 일정 탭(`get-visitor-images{visitorId, scheduleId}`)에 보이는지
4. 브랜치 `kknaksss/overall-board-6`(코디가 만듦 · 체크아웃됨) · **이 수정 파일만 따로 보고**(코디가 이것만 먼저 커밋 · 배포한다) · 커밋 금지 · 보고서 `app-backend-report.md` 「여권 사진 분류」 절 + (2) 알림
5. 그다음 **WORK-010 WP-BE**: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/30-work/work-010-customer-questionnaire-web.md` WP-BE 줄 · 계약 `20-spec/spec-006-customer-questionnaire-web.md` 0.1.0 · 결정 DEC-008 + `_RESUME` 10-28 「OQ 사용자 몫 = 추천대로」 · 끝나면 보고서 「WORK-010 WP-BE」 절 + 두 명령
