# 리뷰 리포트 — 고객 문진 웹(WORK-010 · back WP-BE · front WP-FE · app WP-APP) / code (2026-10-28)

- 대상: `cc-prototype/overall-board` branch `kknaksss/overall-board-6` 커밋 안 된 변경 전체(35 파일 수정 · 지움 4 · 새 파일 10). `7e39bd3` 은 대상 밖
- 기준: SPEC-006 0.1.0 · DEC-008 · WORK-010 WP-REVIEW 줄 · `_RESUME` §2 10-28 「OQ 사용자 몫 = 추천대로」
- 직접 돌린 수치

| 어디 | 명령 | 결과 |
|---|---|---|
| back | `uv run pytest -q` | **467 passed**(경고 1 — starlette httpx 폐기 예고) · `tests/test_app_qweb.py` 만 다시(진행 중 수정 반영 뒤) **20 passed** |
| front | `npx tsc --noEmit` · `npm run lint` | **0 · 0** |
| app | `flutter analyze` · `flutter test` | **No issues** · **123 passed** |

## 판정: WARN (FAIL 0 · WARN 3) — 운영 배포 · 고객 폰 E2E 막는 것 없음

## FAIL

없음.

## WARN

1. **IP 헤더를 조건 없이 믿음** — `procedure/back/app/api/public_questionnaire.py:26-31`. `CF-Connecting-IP` → `X-Forwarded-For` 첫 값 → 소켓 순. Cloudflare 경로에선 맞다(SPEC-006 §7.3 「WP-BE 가 한 곳에 적는다」 충족). 그런데 LAN(MetalLB → ingress 바로)으로 들어오면 두 헤더 다 꾸밀 수 있어서 속도 제한(토큰 맞히기 막기 포함)을 피할 수 있다. 워커 보고에도 「PoC 수용」이라고 적혀 있다. 고칠 사람: back. 나중에 ingress 에서 Cloudflare 경로가 아닐 때 이 헤더를 지우거나, 파드가 믿을 프록시 주소를 정해 두면 된다. 배포는 막지 않는다
2. **메모리 카운터가 줄지 않음** — `procedure/back/app/service/questionnaire.py` `RateLimiter._hits`(`_recent` 가 빈 목록이 돼도 키는 남는다) · `_locks`(요청 id 마다 `asyncio.Lock`) · `_denied`. 지울 때가 없다. 아무 토큰이나 POST 하면 `post_token` 키가 1개씩 쌓인다(IP 당 1분 5회로 묶이지만 IP 를 바꾸면 계속). 한 파드 · 재시작하면 비는 PoC 라 OQ-804 범위 안. 고칠 사람: back(창 밖 키 지우기)
3. **데스크 상자의 새로고침 뒤 남은 시간이 10분 고정** — `procedure/front/components/reservations/Display.tsx`(`Q_TTL_MS = 10 * 60 * 1000` · `createdAt + Q_TTL_MS`). 상세 `displays[]` 에 `expiresAt` 이 없어서 이렇게 했다(front 보고 §2 에 적힘). 운영 `PROC_DISPLAY_TTL_MIN` 을 바꾸면 표시가 어긋난다. QR 은 back 의 상태로 사라지니 기능은 맞다. 고칠 사람: back(`DisplayItem.expiresAt` 더하기) + front 한 줄

## 항목별 대조

### 1. 보안

| 항목 | 결과 | 근거 |
|---|---|---|
| 토큰 — DB 원문 0 | 같음 | `service/display.py` create: `qr_nonce` · `token_hash(token)` 만 저장 · `qweb_token` = HMAC-SHA256 base64url 43자(§3.1) · 시험 `test_questionnaire_token_shape_and_hash_only` |
| 토큰 — 로그 0 | 같음 | `questionnaire.py` 로그는 `describe(err)` · `request=%d` 만 · `test_questionnaire_logs_have_no_token`(caplog DEBUG) · event_log `qweb_open` · `qweb_denied` · `questionnaire_submit` 에 토큰 · IP 없음(§7.4) |
| 토큰 — 푸시 0 | 같음 | `reach()` 에서 qrUrl 은 SSE `data` 에만 · `self.push(request_id)` 그대로 · `push.py` 변경 없음 |
| 토큰 — URL 쿼리 0 | 같음 | front `/q#<token>`(fragment) · API 헤더 `X-Questionnaire-Token`(`publicApi.ts:53`) · `?lang=` 만 쿼리 · uvicorn 접근 로그 `DropQueryString` 원래 있음 |
| 공개 응답 허용 키 | 같음 | `schemas/actions.py` `_Strict(extra="forbid")` · `PublicQuestionnaireForm` = customerName · language · form.pages · agreements · prefill · fillUntil — reservationId · customerId · KOS id 없음 · 오류 본문에서 `requestId` 뺌(`_target_or_deny`) |
| 직원 세션 분리 | 같음 | back: `deps.Actor` 안 씀 · `Authorization` 무시. front: `lib/publicApi.ts` 가 `credentials:'omit'` · `referrerPolicy:'no-referrer'` · session/api.ts import 0 · `app/q` 는 `(main)` 밖 · 루트 layout 은 CSS 만 |
| 한 번 제출 | 같음 | `done` = 409 `q_submitted` · 겹친 제출 = 요청 id 별 Lock → 409 `q_submitting` · 잠금 안에서 `public_target` 다시 확인 · 시험 overlap |
| 시한 10분 · 60분 | 같음 | `repo.expire_displays(now, fill_min)` — pending `expires_at` · 문진 opened `opened_at + PROC_QWEB_FILL_MIN` · 모든 `_expire` 자리에 fill_min 넘김 · `.env.example` 이름 한 줄 |
| 속도 제한 | 같음 | GET IP 30 · POST IP 5 · 404/410 IP 10 · POST 토큰 3 · 1분 · 직원 API 안 걸림 · 시험 3개 |
| CF-Connecting-IP | 같음(+WARN 1) | 먼저 봄 · 시험이 그 헤더로 IP 를 가름 |
| no-store · no-referrer | 같음 | `main.py` 미들웨어(오류 응답 포함) · `app/q/page.tsx` metadata robots noindex · referrer no-referrer · 제목 「Céramique」 |
| 가짜 판 | 같음 | POST 403 `fake_board`(토큰보다 먼저) |

### 2. back ↔ front ↔ app 계약

| 계약 | back | front | app |
|---|---|---|---|
| `qrUrl` = `{PROC_FRONT_ORIGIN}/q#<token>` · 문진만 · `qrToken:null` | `display.qr_url` · create · SSE · pending(pending 만) · 상세 `displays[]`(pending 만) + `openedAt` | `types.ts` `DisplayCreated.qrToken: string\|null` · `qrUrl` · Display.tsx 가 `qrUrl` 로 QR | `DisplayReq.qrUrl` · launchers `showQuestionnaireQrHere` 가 응답 qrUrl · SSE 는 pending 응답으로 열고 실패할 때만 프레임 |
| pending 이 문진을 opened 로 안 바꿈 | `pending()` 이 스캔만 바꿈 | — | 문진은 `status == 'pending'` 만 연다(`app_state.dart`) |
| claim 에 문진 토큰 = 404 | `claim()` | — | [QR 읽기] https = 「고객 폰으로 찍는 QR 이에요」 토스트(`isCustomerQr`) |
| 공개 GET/POST 모양 | §6.1 그대로 · POST 에 deviceId · displayRequestId = 400(extra forbid) | `PublicQuestionnaire` · `PublicSubmit` 같음 | — |
| 오류 코드 | 400 `q_token_missing` · 404 `q_not_found` · 410 `q_expired`/`q_canceled` · 409 `q_submitted`/`q_submitting` · 429 · 400 `questionnaire_field` · 409 `questionnaire_rejected` · 502 · 403 `fake_board` | `failOf` 가 §5 표 그대로 고르고 `data-code` 로만 코드를 둔다 · 제출 실패 중 화면 바꾸는 것만 따로(`SUBMIT_SCREEN`) · 그 밖은 입력 유지 + [다시 제출] | — |
| 데스크 상자 단계 | `displays[]` status · openedAt · closedAt | pending = QR + 남은 시간 → opened 「고객이 입력 중 · HH:MM」(QR 숨김) → done 「제출됨」 → expired [다시 만들기] · canceled 닫힘 · 「오늘 이미 제출함」 | — |
| 앱 QR 화면 | 상세 `displays[]` | — | `qr_show_screen.dart` — 5초 폴링 · pending 아니면 한 줄 → 1.5초 뒤 닫힘 · [닫기] = 화면만 · `keepAwake` · QR 은 기기 안 CoreImage(`TextScanner.swift qrPng`) · 고객 이름 없음 |
| 새 요청이 opened 도 닫음 | `closing = ("pending","opened")` 문진만 | — | — |

### 3. 지운 것 회귀

- 앱 `questionnaire_screen.dart` · `l10n/questionnaire_text.dart` · `model/questionnaire.dart` · `test/questionnaire_test.dart` 지움 · `api.dart` 의 문진 · unlock 호출 지움 · 앱 코드(lib · test · integration_test)에 남은 참조 **0**(grep)
- back `api/questionnaire.py` · `POST /api/auth/unlock` · `UnlockRequest` · `AuthService.unlock` 지움 · 남은 참조는 「없어졌는지」 보는 시험뿐(`test_app_qweb.py:308-310` · `test_order.py:259`)
- 경로 `test_route_count_49`(`test_order.py:246`) 통과 = HTTP 48 + WS 1(§6.7)
- front `lib/q/text.ts` · `form.ts` 가 앱 문구 · 양식 읽기를 옮겨 받음(주석으로 출처 적음)

### 4. 법적 검토 주석 · grep

- §7.6 세 곳: `back/app/api/public_questionnaire.py:3` · `front/app/q/page.tsx:2` · `back/app/repository/db.py:142`(`questionnaire_history` 정의 바로 위 · `web_submit` · 보관 기간 미정 줄과 함께) — **3/3**. 더해서 `service/questionnaire.py` `read_prefill`(OQ-807)
- 바뀐 파일 · 새 파일에서 43자 base64url · 긴 hex id · 휴대폰 번호 꼴 · 운영 주소 하드코딩 · 고객 이름 리터럴 grep → **0**. 운영 주소는 env(`PROC_FRONT_ORIGIN` · `NEXT_PUBLIC_API_BASE_URL`)로만 받는다
- 레포에 스크린샷 png 새로 들어온 것 없음(untracked 목록) — §7.5 「QR · 주소창 가림」은 리포트 쪽에서 볼 것

### 5. 판정 밖 — 진행 중 back 수정(메모만)

- `service/questionnaire.py` `submit_for` 가 리뷰하는 동안 바뀌었다. KOS 제출 확인(`getQuestionnaireSubmit`)이 이번 제출보다 오래된 것(`started - FRESH_SEC`)이면 받은 답을 KOS 제출본 꼴(`submitted_answers` · `kos_utc`)로 바꿔 `web_submit` 행에 넣는다. event 에 `kosReadStale` 를 더했고 시험 `test_questionnaire_health_after_resubmit_when_kos_keeps_first` 도 생겼다
- 바뀐 뒤 `test_app_qweb.py` 20 passed. 전체 467 은 바뀌기 전에 돈 수치일 수 있다 — 끝나면 전체를 다시 돌릴 것
- 이 수정으로 이력 `answers` 의 원천이 「KOS 제출본 그대로」(§6.4 · §9 ②)에서 「없으면 ccc 가 만든 사본」으로 넓어진다. SPEC-006 §6.4 · §5.11(데스크 「건강 정보」 원천)에 한 줄 더할지는 planner 몫

## 고객이 실물에서 만날 자리

- 아이폰 카메라 → Safari 로 열 때 `#` 뒤 토큰이 남아 있어야 한다(카메라 앱은 보통 남긴다). E2E Q1 에서 첫 화면이 뜨는지로 본다
- 휴대폰 미리 채움이 KOS 값이라 맨 앞 0 이 빠져 보인다(§6.3 · 그대로 둠) — 고객이 「틀렸다」고 느낄 수 있다
- 고객이 열고 그냥 닫으면 데스크 상자는 60분 동안 「고객이 입력 중」으로 남는다. 다시 띄우면 옛 링크는 「새 QR …」 화면이 된다(§3.3)
- 성별은 여성 · 남성 둘 중 하나가 필수다. KOS 값이 그 밖이면 고른 칸 없이 시작한다(front 기본값 · 보고 §2)
- 오류 화면 언어는 `navigator.languages`(§4.1) — 고객 폰 언어가 KOS 고객 언어와 다를 수 있다
- 링크를 가진 사람은 미리 채운 개인정보를 본다(OQ-807 · 법적 검토 주석) — 사용자가 「추천대로」로 받아들임

## 참고(기존 부채)

- SSE `/api/board/stream?token=` 은 쿼리에 직원 토큰이 실린다(원래 있던 것). 문진 `qrUrl` 은 이 연결의 본문으로만 가고, 접근 로그는 `DropQueryString` 이 쿼리를 지운다
- 같은 링크로 첫 GET 이 거의 동시에 둘 오면 `qweb_open first:true` 가 두 줄 남을 수 있다(상태는 opened 하나 · 기능 영향 없음)
- reviewer `tools.md` 는 「테스트 실행 금지」인데, 이번 브리프가 직접 돌리라고 해서 돌렸다(파일 · 포트는 건드리지 않음)
