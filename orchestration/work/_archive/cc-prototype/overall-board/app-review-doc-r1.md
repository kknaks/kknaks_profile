# 리뷰 리포트 — overall-board ① 앱 계약 / doc (2026-10-27)

- 대상: DEC-007(새) · SPEC-004 0.4.0 · WORK-009(새) · README 3 · log · SPEC-003 · SPEC-005 frontmatter · workflow-app r2 (planner 보고 `app-spec-report.md`)
- 기준: `_RESUME` §2 10-26 · 10-27 앱 줄 · AP-1 ~ AP-45 · `workflow-app.md` r2 · `app-kos-report.md` · **`app-wp-kos-report.md`(K1 ~ K4 결과 · 재발주 추가분)** · SPEC-005 0.4.0 · SPEC-003 0.6.0 · 코드(읽기만) `cc-prototype/overall-board` `kknaksss/overall-board-2` `95c64bc`
- read-only · 수정 · 커밋 0. 줄 번호 = 이 리뷰 시점 파일
- 약어: S4 = `para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` · S5 = `…/spec-005-reservation-board.md` · D7 = `…/10-decision/decision-007-app-v2.md` · W9 = `…/30-work/work-009-app-v2.md` · WA = `reference/2026-10-27-cc-app/workflow-app.md` · WK = `orchestration/work/overall-board/app-wp-kos-report.md` · `back/` · `app/` · `front/` = 코드 `procedure/` 아래

## 판정: FAIL

FAIL 6 · WARN 14 · 사용자 결정 필요 6. 결정 줄 · AP 반영은 거의 다 맞다(AP 하나 빠짐). FAIL 은 대부분 **BE 와 앱이 SPEC 만 보고 따로 짜면 어긋나는 계약 빈칸**(기기 식별 · 웹 썸네일 인증 · `push_log` 마이그레이션)과 **WP-KOS 결과가 아직 SPEC 에 반영되지 않은 것**이다.

---

## FAIL

### F1. `push_log.call_id` 를 null 로 바꾸는 법이 계약에 없고, 쓰라고 한 방식으로는 바꿀 수 없다
- 자리: S4:531(§5-2 `push_log` 「`call_id` · `visit_id` 를 null 가능으로」) · S4:857(§7.4 「`call_id` · `visit_id` null 가능」) · S4:848(§7.4 머리 「`CREATE TABLE IF NOT EXISTS` + `MIGRATIONS` · SPEC-005 §3.2 방식」)
- 근거: 코드 `back/app/repository/db.py:54` `push_log(… call_id INTEGER NOT NULL …)`. `MIGRATIONS`(`db.py:158-173`)는 `ALTER TABLE … ADD COLUMN` 만 한다. SQLite 는 `ALTER` 로 NOT NULL 을 풀지 못한다(표를 다시 만들어야 함). 배포 DB(ccc 운영 · compose 볼륨)에는 이미 NOT NULL 표가 있다
- 결과: 상담사 호출 · 띄우기 푸시의 `push_log` 행(`call_id` 없음)이 기존 DB 에서 INSERT 실패 → 발송 기록이 안 쌓이거나 발송 경로가 예외로 끊긴다. 새 DB(시험)에서는 통과하므로 **pytest 는 초록 · 배포에서만 깨지는 자리**
- 필요: 표 재생성 마이그레이션(새 표 → 복사 → 이름 바꿈)을 계약에 적거나, `call_id` 를 그대로 두는 다른 모양(예: 별도 표)을 정한다. §8.6 에 「옛 모양 DB 파일에서 시작」 시험 한 줄

### F2. 웹 썸네일 인증이 「로그인 쿠키」인데 이 시스템에 쿠키 인증이 없다
- 자리: S4:800(§6.17 「썸네일(`GET /api/id-photos/{id}` · **로그인 쿠키** · 공개 URL 아님)」) · S4:323(§3.4)
- 근거: 웹은 `localStorage` 토큰 + `Authorization: Bearer`(`front/lib/api.ts:51` · S4 §3.6 「세션(localStorage)」). back 인증은 헤더만(`back/app/api/deps.py:18-21`) · 쿠키 코드 0(grep). `<img src>` 는 헤더를 못 싣는다
- 결과: BE 는 헤더 인증으로 짜고 FE 는 `<img src>` 로 짜면 썸네일이 401 로 깨진다. 어느 쪽이 맞는지 SPEC 으로 정할 수 없다
- 필요: ① `fetch`(Bearer) → blob URL 로 그림 ② SSE 처럼 `?token=`(접근 로그 쿼리 지움 필터 `DropQueryString` 있음) 중 하나를 계약으로. 앱(§6.16 사진 작게 · 스캔 확인)도 같은 줄

### F3. 「그 기기」를 back 이 어떻게 아는지 — pending · claim · 문진 이력 기기가 계약에 없다
- 자리: S4:542 ③(`GET /api/display-requests/pending` 「그 기기 `pending`」) · S4:543(`POST /api/display-requests/claim {qrToken}` 「그 기기 요청으로 묶고」) · S4:321(§3.4 「부른 기기 · 계정 것만」) · S4:457(`last_seen_at` = `pending` 때 갱신) · S4:766(문진 제출 → `questionnaire_history.device_id`)
- 근거: 기기 id 를 싣는 자리는 SSE 쿼리 `deviceId`(S4:813)와 `passport-scan` 의 `deviceId` 필드(S4:784)뿐. pending 의 쿼리 · claim 본문 · 헤더 어디에도 기기 표시가 없다. 한 계정이 기기 여럿에 로그인한다(D7-10 · D7-26 — 데스크 태블릿 · 코디 폰이 같은 코디 계정)
- 결과: 계정만으로는 태블릿 것인지 폰 것인지 못 가른다 → 태블릿에 보낸 문진이 코디 폰에서 열리거나, BE · 앱이 서로 다른 전달 방식(쿼리 / 헤더 / 본문)을 지어낸다. [이 기기에서 열기](S4:724 — 띄우기 요청 없음)로 연 문진은 `device_id` 원천이 없다
- 필요: `deviceId` 를 pending(쿼리) · claim(본문) · 문진 GET/POST(본문 또는 쿼리)에 싣는 꼴과 남의 계정 기기 id 처리(404 · 무시)를 §5-3 · §6.15 표에 한 줄씩

### F4. WP-KOS K4 결과와 다름 — 고객 이미지 조회 경로가 틀렸다
- 자리: S4:893(§8.0 #23 `get-visitor-files`) · W9:71(WP-KOS K4 「내부 `get-visitor-files` 로 K3 사진이 보이는지」) · S4:1021(OQ-619 「내부 고객 파일 조회」)
- 근거: WK:24 · WK:136-142 — `get-visitor-files` = 고객 **첨부 파일**(0건) · 공개 `registerVisitorImages` 로 올린 사진은 내부 **`image/visitor-image/v1/queries/get-visitor-images`** 에 보인다(확인). `_RESUME` 상황판(researcher 줄)에 코디 기본값 「K4 경로 = get-visitor-images」(Q-154)
- 필요: §8.0 #23 · W9 WP-KOS · §8.8 E7 확인 방법의 경로 이름을 `get-visitor-images` 로. 게이트 상태 표기도 아래 F5 와 같이 「받음」으로

### F5. WP-KOS K2 · K3 결과와 다름 — §6.16 ④-a · ④-c 와 §8.0 #8 · #21 · #22 가 결과 전 문구 그대로
- 자리: S4:785(④-a 「`passportExpiryDate` 는 K2 가 확인될 때까지 보내지 않는다 · `skipped`」) · S4:973(§8.6 「만료일 K2 전 = 안 보냄」) · S4:787(④-c `registerVisitorImages{source, category, equipment}` · 「분류 · 장비 코드는 K3 가 정한 값을 env 없이 코드 상수로」) · S4:878 · 891 · 892(§8.0 #8 · #21 · #22 「게이트」) · S4:1021 · 1024(OQ-619 · OQ-622 열림) · W9:74(WP-BE2 「K1 뒤」)
- 근거(WK):
  - K1 a · b 받음(WK:20-21) · K2 받음 — `yyyy-MM-dd` 문자열 그대로 저장 · **공개 `getVisitor` 엔 안 보임 · 내부 `get-visitor` 만**(WK:75-80)
  - K3 받음 — 필수 = `fileName · visitorId · source · shootingDateTimeUtc`(WK:97) · `source = HOSPITAL`(WK:109) · `equipment` = `get-codes` 객체 6키 그대로 「태블릿」(WK:96 · 106) · **`category` 안 보냄**(지점 분류 = 시술 전/후뿐 · WK:97) · `scheduleId` · `path` 안 보냄(WK:106 · 127) · 코드 id 는 지점마다 다름 → **이름 상수 → 실행 때 `get-codes` 로 찾기**(WK:178)
  - `_RESUME` researcher 줄: Q-154 ~ 157 = 코디 기본값(분류 안 보냄 · scheduleId · path 안 보냄 · 흔적 둠)
- SPEC 과 어긋나는 점: ④-c 는 `category` 를 보내라고 적었고 `fileName` · `visitorId` · `source` 값 · `shootingDateTimeUtc` · `memo` 가 없다. 「코드 상수」만 적고 실행 때 id 찾기가 없어 워커가 데모 id 를 박아 넣을 수 있다(운영 지점에서 틀림 · public 레포에 KOS id). ④-a 의 K2 조건은 이미 의미 없다 — **코드도 웹 [고객 기본 정보 저장]에서 이미 만료일을 보낸다**(`back/app/service/reservations.py:1093-1095` `PERSONAL_KEYS` 에 `passportExpiryDate` · `:1113-1114`)
- 필요: ④-c 본문 모양을 WK §3.2 ③ 그대로 적고(`category` · `scheduleId` · `path` 없음 · `source HOSPITAL` · 장비 = 이름 「태블릿」 → `get-codes` 실행 때 찾기 · 못 찾으면 처리) · ④-a K2 조건 지움 · §8.0 #8 · #21 ~ #23 「확인(WP-KOS 2026-10-27)」 · OQ-619 · OQ-622 닫음 · W9 WP-KOS 「완료」 · WP-BE2 의존 갱신

### F6. AP-41 「암호화」가 DEC · SPEC · WORK 에서 빠졌다
- 자리: WA:533(AP-41 정해진 값 「클러스터 PVC(back 파드에 붙인 볼륨 · **암호화** · 백업 없음)」) ↔ D7:151(D-54 「클러스터 볼륨(… · 백업 없음)」 — 암호화 없음) · S4:211 · 786 · W9:72(WP-INFRA 「PVC(작게 · 백업 없음)」)
- 근거: 브리프 「빠짐 = FAIL」. AP-1 ~ AP-45 전부 승인(`_RESUME` 10-27)이라 승인 값이다. grep `암호화` = D7 · S4 · W9 0건
- 필요: D-54 · §2.3 / §6.16 · WP-INFRA 완료 조건에 넣거나, 클러스터가 볼륨 암호화를 못 하면 사용자 결정(아래 U2)

---

## WARN

| # | 자리 | 무엇 | 근거 |
|---|---|---|---|
| W1 | S4:812-813(§7.1) · W9:73(WP-BE1 대상 파일) | `display` 는 「같은 계정 스트림」 · `notification` 은 「그 계정 스트림에만」 · `online` = 기기 SSE 열림인데, 지금 SSE 는 **계정을 모르는 전체 방송 허브**다 — `api/board.py:20-28`(토큰 검증 값을 버림) · `service/stream.py:17-60`(큐 집합 하나). 허브를 계정 · 기기 단위로 바꾸는 일이 WP-BE1 대상 파일에 없다(`service/stream.py` · `api/board.py` 빠짐). 새 이벤트가 `id:`(version)를 싣는지 · 허브 version 을 올리는지도 없다(웹 `front/lib/hooks.ts:77-85` · 앱 `app/lib/sse/board_stream.dart:123-132` 가 version 으로 board 를 버린다) | 「계약이 닿는 표면 전수」 |
| W2 | S4:766(§6.15 ⑥) · S4:858(§7.4) | `questionnaire_history` 에 `UNIQUE(customer_id, kos_submitted_at)`(`db.py:150-153`). 웹 상세 5초 폴링(§6.17 · S5 §5.11 「읽기 때 쌓기」)이 KOS 새 제출본을 먼저 읽어 `source = read` 행을 넣으면 앱 제출 뒤 `app_submit` 행이 충돌한다 — 충돌 때 규칙(덮어써 `source` · `language` · `device_id` 채움 / 버림)이 없다. 본 언어(D7-46 · Q-149)가 빠질 수 있다 | 코드 · 계약 빈칸 |
| W3 | S4:785 · S4:973 · W9:77 · D7:78(D-16) | 「13키 전부 + 바뀐 칸」 — 코드 재사용 함수는 `PERSONAL_KEYS` 17개 중 **다시 읽은 응답에 있는 키 전부**(`reservations.py:1036` · `:1093-1095`). K2 시험도 14 + 1 키를 보냈다(WK:65). 「13」을 시험값으로 쓰면 틀린 단언이 된다 → 「SPEC-005 §5.13 함수 그대로(있는 키 전부)」로 | 코드 · WK |
| W4 | S5:272 · S5:460 | SPEC-005 본문이 낡았다 — 「상담사(실장) 계정 이번 판 없음」 · 「앱 알림은 이번 판 없음(D-38)」. 또 웹 상세 응답 변경(`displays[]` · `identity.method/device/photoId` — S4:545 · S4:836)이 S5 §7.3 에는 없다. planner 는 S5 frontmatter 만 고쳤다. 웹 front 워커가 S5 만 보면 빠진다(WP-FE 는 S4 §6.17 을 가리키므로 막히지는 않음) | doc-first · 「schema 변경 시 spec 동기」 |
| W5 | S4:803 | §6.17 표 끝에 다른 표의 줄 「`| 15 | 「수납 필요」 · 「KOS 반영 중 · 실패」 자리 없음 | 룸 상세 머리 아래 작게 |`」 — 열 수도 다르다(§6.7 쪽 잔재로 보임) | 문서 |
| W6 | W9:71 | WP-KOS 산출 이름 `app-kos-probe-report.md` ↔ 실제 `app-wp-kos-report.md`(WK:12) · 상태 「대기」 그대로 | WK |
| W7 | W9:97 | 병렬 그림이 WP-FE 를 WP-APP6 뒤에 줄 세운다. 표(W9:84)의 의존은 BE3 · BE5 뿐 — 그림대로면 웹이 앱 끝까지 기다린다. 그림 · 표 중 하나로 맞춘다 | 문서 |
| W8 | S4:766 · S4:889(§8.0 #19) | 문진 제출은 KOS 고객 정보를 바꾼다 — 성별 · 생년월일 · 주소 · 동의 · **휴대폰(11자리 → 10자리 · 맨 앞 0 빠짐)**(`app-kos-report.md` §5.3 · 223줄). SPEC 은 「반영」만 적고 휴대폰 0 빠짐 · 미리 채운 값을 고객이 고치면 KOS 고객 값이 바뀐다는 것을 화면 · 시험에 두지 않았다 | AK §5.3 |
| W9 | S4:771(잠금) · S4:767(⑦ 대기) | ① 「잠긴 대기 화면」이 잠금 범위(탭 · 배너 · 뒤로)에 드는지 · 대기 화면에서 나가는 길이 [직원] 길게인지 문장에 없다 ② 나가기 = 그 계정 `POST /api/auth/login` — 고객이 5번 틀리면 §3.3 규칙대로 **그 코디 아이디가 1분 잠김**(웹 · 다른 기기 로그인 포함). 받아들일지 적어 두기(아래 U5) | D7-45 · S4 §3.3 |
| W10 | S4:782(② 읽기) | MRZ 날짜는 `YYMMDD` — 생년월일 · 만료일의 세기(19xx / 20xx) 정하는 규칙이 없다. KOS 는 `yyyy-MM-dd`(WK:75). 워커가 추측으로 메운다(흔한 규칙: 생년월일 = 오늘보다 뒤면 19xx · 만료일 = 20xx) | 계약 빈칸 |
| W11 | S4:542 ② · S4:234 · S4:1022(OQ-620) | AP-21 정해진 값은 「아니면 푸시(**조용한 알림** · 누르면 문진)」(WA:517). SPEC 은 「보이는 알림 · 소리 없음」으로 읽었다. iOS 조용한 푸시(content-available)는 누를 것이 없어 planner 해석이 맞을 가능성이 크지만 승인 문구와 글자가 다르다 + D7-08 「알림 둘만」과의 경계 → U1 | WA · D7 |
| W12 | S4:554 · S4:555 · D7:128 | AP-19 원천 = 「서버 `push_log` 중 그 계정이 받은 것」 ↔ SPEC = 새 `notification` 표 · **기기가 없어도 행을 쓴다**. 기기 없는 계정의 목록에 「받지 않은」 알림이 보인다 — 승인 값과 뜻이 다르다 → U3 | WA:510 |
| W13 | S4:749(§6.14 「이 기기」 칸) | AP-30 「설정 = 알림 · 앱 정보 · [로그아웃]만」 ↔ AP-6 「기기 이름 앱에서 고칠 수 있음」 — 승인 값끼리 부딪힌다. SPEC 은 설정에 칸을 하나 더했다 → U4 | WA:486 · 545 |
| W14 | S4:723 · D7:115(D-33) | AP-12 정해진 값 「웹과 같은 줄(… · **[스캔할 기기]**)」 ↔ D-33 「웹과 같음 + [여권 스캔]」 · SPEC §6.11 = [여권 스캔](이 기기)만 — 앱에서 다른 기기로 스캔 보내기가 빠졌다. AP-35 는 「앱 = 그 기기 카메라」라 승인 값끼리 어긋남 → U6 | WA:497 · 527 |

그 밖(고칠 때 같이): S4:462 `POST /api/devices` 「세 역할 모두」 → 다섯 · §5-1.2 받는 사람 표(S4:503-507)에 coordinator · counselor 줄 없음(§5-4 S4:559 에만 있음).

---

## 볼 것별 결과

| # | 항목 | 판정 | 요지 |
|---|---|---|---|
| 1 | 결정 줄 · AP 45 → DEC · SPEC | FAIL(F6) · WARN(W11 ~ W14) | `_RESUME` 10-26 · 10-27 앱 줄 → D-01 ~ D-21 빠짐 없음(앱 범위 · 앱도 쓴다 · 상담사 · 문진 언어(바뀐 순서) · 스캐너 여권만 · 마스킹 · 사진 둘 다 · 법적 검토 주석 · iOS 만 · 시안에서 뺌 · 수납 · 처방전 웹만 · 알림 둘 · 새 틀 · 2계층). AP 45 → D-22 ~ D-66 한 줄씩 · 부록 C 로 SPEC 절 있음. 다름 = AP-41 암호화 빠짐 · AP-21 / 19 / 6 ↔ 30 / 12 해석 |
| 2 | 웹 규칙과 같은가 | PASS(+W4) | 앱 쓰기 = S5 §7.5 경로 그대로(S4:715-723 ↔ `back/app/api/reservations.py:85-132` 존재) · 새 쓰기 로직 없음 · 409 · 403 토스트 + 다시 부름 · 상세 5초 · 표 10초. 상태 = §6.9 원천 `front/components/reservations/view.tsx` `MAIN_TONE`(74) · `phaseStyle`(90) · `stateText`(107) 실재 · S5 §5.1 표와 같은 이름 · 색. 뺀 것 — 수납 · 처방전 버튼(S4:725) · 알림 다섯 + 「수락됨」 · 아이콘 배지(S4:142) · 리포트 QR(S4:141) · 공지 · 등록 · 드래그 · 이동 · 예약 요청(S4:140 · 704) · 앱 시술 드래그(S4:596) 모두 Out |
| 3 | KOS 표 25 ↔ 리포트 · 게이트 | FAIL(F4 · F5) | 25행 = WA §7 25행 그대로(#24 만 「이번 판 없음」으로 — D-52 근거 있음). 미확인 4 = K1 ~ K4 게이트로 다 덮였고 못 넘을 때 처리(S4:897)도 있다. 지어낸 KOS 동작은 못 찾음. 다만 **결과가 나온 지금 SPEC 이 결과와 다르다**(경로 · 본문 · 게이트 문구) |
| 4 | 계약 완결성 | FAIL(F1 · F2 · F3) · WARN(W1 · W2 · W10) | 새 HTTP 14 = §5-3 5 + §6.15 2 + §6.16 3 + §5-4 4 · 지금 35(`back/tests/test_order.py:237` `test_route_count_35` ↔ S5:827) + 14 = 49 계산 맞음(② 판이 경로를 더하면 다시 셀 것). 표 5종(`device` 열 · `notification` · `notification_setting` · `display_request` · `questionnaire_history` 열 · `id_photo` · `identity_check` 열 — 지금 `identity_check.device` 는 이미 있음 `db.py:146-149`) 필드 있음. 푸시 payload 두 종 + `display` 있음 · 원장 호출 payload `kind` 더함(옛 빌드 호환 적음). **기존 원장 호출 푸시**: 받는 사람 계산(`service/push.py:72-101` — admin + doctor) 그대로 · coordinator · counselor 0 · 회귀 시험 S4:969 있음 — PASS. **시술 현황 회귀**: §8.6 · §8.8 E8 · E9 있음 — PASS. 앱 `model/account.dart:6-9` 는 모르는 역할을 admin 으로 읽는다(지금 coordinator 도 그렇다) — §3.4 가 grep 을 시켰으니 PASS. 웹 `front/lib/session.ts:12 · 34` 는 모르는 역할이면 세션을 버린다 → WP-FE 에 `counselor` 있음(W9:84) — PASS |
| 5 | 개인정보 · 보안 | FAIL(F2) · WARN(W8 · W9) | 사진 = 비공개 볼륨 · 무작위 이름 · DB 엔 이름만 · 로그인 열람 · `id_photo_view` 이벤트 · 원본 메모리만 · 사진첩 권한 문구 넣지 않음(S4:229) — PASS. 주민번호: 문진 칸 없음 · `registrationNumber` 400 · 스캔 칸 없음 — PASS. 법적 검토 주석 자리 5곳(S4:793) + §7.4 표 머리(S4:860) + W9 grep 조건(BE ≥ 3 · 앱 ≥ 2) — PASS. 잠금 화면 글자: 상담사 호출 「<방> · 상담 대기」 · 띄우기 「데스크에서 보냈어요」 · 고객 이름 · 국적 · 시술 없음 — PASS |
| 6 | WORK-009 | WARN(W1 · W6 · W7) | WP 순서(KOS ∥ INFRA ∥ BE1 → BE2 ∥ BE3 → BE4 → BE5 / APP1 → APP6) · 같은 파일 충돌 피함 이유 · 부분 검증 명령 · 전체 검증은 WP-E2E 한 번 — 맞다. 완료 = 사용자 TestFlight 실기기 E1 ~ E9(시뮬레이터 · 웹 대신 금지 · 카메라 · 푸시는 실기기만) — **사용자 표면 맞음**. ③ → ② → ① 순서 · 백엔드 커밋 뒤 재기동 · archive 전 ignored 확인 적힘 |
| 7 | public | PASS | 새 · 바뀐 8파일 grep: 24자 hex · uuid · `eyJ` · `Bearer <값>` · 메일 · `+82` · 휴대폰 꼴 · `AKIA` = 0. 사람 이름 + 직함 꼴 = 일반 명사(「다른 원장」 등)뿐. env 는 이름만 · 시험 데이터 `[ccc 시험]` · 여권 견본만 |

---

## 사용자 결정 필요

| # | 무엇 | 왜 | 지금 문서 |
|---|---|---|---|
| U1 | 띄우기를 앱이 뒤에 있을 때 무엇으로 깨우나 (OQ-620 · AP-21) | 승인 문구 「조용한 알림」 ↔ SPEC 「보이는 알림 · 소리 없음」 · D-08 「알림 둘만」과 경계 | 보이는 알림 · 목록 · 배지 · 설정 밖 |
| U2 | 사진 볼륨 암호화 (AP-41) | 승인 값인데 DEC · SPEC · WORK 에서 빠짐(F6). 홈 · 맥 클러스터가 볼륨 암호화를 할 수 있는지 infra 확인 필요 | 없음 |
| U3 | 알림 목록 원천 (AP-19) | 「받은 것(`push_log`)」 ↔ 「기기 없어도 계정 행」 — 기기 없는 계정도 목록에 쌓을지 | 계정 행(기기 무관) |
| U4 | 설정에 「이 기기」 이름 칸 (AP-6 ↔ AP-30) | 승인 값끼리 부딪힘 | 칸 넣음 |
| U5 | 문진 잠금 해제 비밀번호를 고객이 틀릴 때 그 코디 아이디가 1분 잠기는 것을 받아들일지 (W9) | 데스크 태블릿 = 코디 계정 고정(D-25) — 웹 · 폰 로그인까지 막힌다 | §3.3 규칙 그대로 |
| U6 | 앱 예약 상세에서 다른 기기로 스캔 보내기 [스캔할 기기] (AP-12 ↔ AP-35) | 승인 값끼리 다름 | 이 기기 [여권 스캔]만 |

(Q-154 ~ Q-157 은 `_RESUME` 상황판에 코디 기본값으로 닫혀 있다 — 결정이 아니라 SPEC 반영 몫 → F4 · F5)

---

## 고객이 실물에서 만날 자리

- 운영 DB 에서 상담사 호출 푸시 · 띄우기 푸시가 `push_log` INSERT 에서 깨진다 — 시험(새 DB)은 초록(F1)
- 웹 예약 상세 신분 확인 썸네일이 안 뜬다(401)(F2)
- 데스크 태블릿에 보낸 문진이 같은 코디 계정의 폰에서 열리거나 반대(F3)
- KOS 웹 고객 이미지를 확인하러 갔는데 「파일」 쪽을 보면 0건(F4) · 운영 지점에서 장비 코드 id 가 데모 값이면 KOS 이미지 등록 실패(F5)
- 고객이 문진에서 휴대폰을 고치면 KOS 고객 휴대폰 맨 앞 0 이 빠진 값으로 바뀐다(W8)
- 여권 MRZ 생년월일 세기가 틀려 KOS 생년월일이 100년 어긋날 수 있다(W10)
- 고객이 문진 화면에서 [직원] 비밀번호를 장난으로 5번 틀리면 데스크 코디 아이디가 1분 잠긴다(W9)
- 문진 본 언어가 이력에서 빠질 수 있다(웹 상세 폴링과 겹칠 때)(W2)

## 참고(기존 부채)

- S4 §8.1 · §8.3 · §8.4 의 「세 역할」 표기(0.3.0 판) — 0.4.0 은 §3.4 끝 문단 · §8.6 으로 다섯 역할을 덮는다. 옛 표 본문은 그대로
- 데모 흔적(WK §5 · Q-157)은 코디 기본값 「둠」 — 리뷰 범위 밖
- SPEC-003 §10.1 본문은 「SPEC-004 0.4.0 이 닫음」으로 본다(S4:1145) — SPEC-003 본문 갱신은 하지 않음(planner 보고대로)
