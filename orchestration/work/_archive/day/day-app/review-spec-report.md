# 리뷰 리포트 — day-app / doc (2026-11-09)

- 대상: 워크트리 `mediness-mediness/day-app-spec` · branch `kknaksss/day-app-spec` · base `origin/main` b4cd1a00 · 커밋 전 변경(아래 5파일)
- 대조 원천: `day-app-spec-brief.md`(planner 최종 브리프 §2 · §3) · `_RESUME.md` 「결정」 · `research-prototype-board.md` · `procedure-board-decisions.md` · DAY-SPEC-001/002 · CENTURION_DAY `dev` 91728737(`routers/api/auth.py` · `routers/api/board.py` · `schemas/auth.py` · `services/auth.py` · `services/board_rules.py` · `templates/partials/board_parts.html` · `routers/board.py` · `AGENTS.md` 「앱」) · interpret-pwa SPEC §4 · §5 · `origin/main:back/seed/glossary.json`
- 검수자: reviewer_doc · read-only(이 리포트 한 파일만 씀)

## 판정: FAIL

FAIL 1건(F-1)은 범위가 좁고 고치기 쉽다. 나머지는 WARN 9건이다. 브리프의 핵심 계약(iOS 우선, DAY 로그인·색·권한, 간호사 대리 수락, 통역 사전, 사용자 기준 푸시, 데모 계정의 dev 연결)은 **빠짐없이 들어가 있다**. 서버 미구현분(D-1~D-3)도 현행 기능과 섞이지 않고 구분돼 있다. F-1을 고치면 WARN만 남는다. 다만 W-1·W-2·W-3은 앱 구현 전에 SPEC에서 닫는 편이 낫다.

### 범위 · 절차 확인 (통과)

| 항목 | 결과 | 근거 |
|---|---|---|
| 변경 파일 = allowed_paths | 통과 | `git status`: `20-spec/spec-003-mobile-app.md`(새로) · `spec-001-login-session.md` · `20-spec.md` · `30-work.md`(Spec Coverage 1줄) · `40-architecture/mobile-deployment.md`. `10-decision.md` · `log.md` · `30-work/` · SPEC-000/002는 손대지 않음 |
| WP를 SPEC보다 먼저 썼나 | 아님 | `30-work/` 변경 0. `30-work.md` 변경은 `DAY-SPEC-003 \| — (WP · Delivery Issue 미발주) \| proposed` 한 줄뿐(브리프 §5 허용) |
| lint `--strict` | exit 0 · **products/day ERROR 0 · WARN 0** | 전체 `0 error, 263 warning`은 모두 다른 제품(selly `doc_no` 누락 등) — 무관 |
| `doc_no` | `DAY-DOC-7` 유일 | 이 워크트리에는 DOC-1~7이 있다. 옆 워크트리(`day-procedure-board-2-spec` · 커밋 336b44e4)는 DOC-1~6만 써서 충돌 없음 |
| SPEC-002 JSON/SSE 존재 정정 | 맞음 | SPEC-003 L335가 조사 리포트의 「계약 없음」을 정정한다. `routers/api/board.py` · `board_rules.py` `snapshot()`과 칸을 하나씩 대조했고 표(L324-333)가 사실과 맞는다 |
| UUID · 서버 판정 | 맞음 | L312 · L453. `can*` · `pickable` · `inbox.section` · `need`를 서버가 싣는 것도 확인(`board_rules.py:440-445` · `:512-517`) |
| 간호사 대리 수락 · 원장 본인 수락 | 맞음 | L180-183 = SPEC-002 권한 표(L346-353) · U-6 · OQ-19. 서버는 `board.accept` edit로 막는다(`routers/api/board.py:37` · `:166`). 프로토의 반대 규칙은 L180 · L464에서 배제 |
| 귀가 대기 제거 · 시작 취소 유지 | 맞음 | L141 · L199(`BOARD_STEPS`에 `PROCEDURE_DONE` 없음 — `board_rules.py:23`) · L188(시작 취소 버튼 유지, KOS 쓰기는 옆 세션 몫) |
| 방 이동 · 차트 작성 · 시드 | 발명 없음 | L61 · D-4. 읽기 전용 차트(L165)는 SPEC-002 L123 · 규칙 23과 같다 |
| 통역 사전 | 맞음 | 시드 실측: `schema 1` · `version 2026-10-27.6` · terms **170** · entries `en/ja/zh/zh-Hant/th/vi/yue`. SPEC-003 L240 · L375-377 = interpret-pwa §5.5 · §5.6(`s2tw` + 「激光→雷射」 · yue `s2tw` · context `t2s`) · §4.5. 사전 화면·API 없음(D-37), 앱 안 번역 없음(L244 · 규칙 6) |
| 푸시 = 로그인 유저 자동 연결 · 별도 화면 없음 | 맞음 | L235 · L351 · L359-361. 토큰 교체 · 여러 설치 · 권한 거부 · 네이티브 수락 · 환경 격리 모두 계약에 있음 |
| 미구현과 제외·완료 혼동 | 없음 | API 표 L305-309 「없음 — 서버 의존 D-n」 · L483-490 「앱 구현(더블) / 통합 검증(실물)」 분리 · 사용자 설정은 「착수 조건 아님」(L490 · L521) |
| 데모 환경 연결 필수 성질 | 대부분 충족 | 인증 우회 없음(dev가 실제 KOS 인증 — SPEC-001 L287) · 서버가 판별(L284) · 요청 칸·헤더로 못 고름(L258) · 서버 env 분리 유지(L238 · mobile-deployment L238) · dev 장애에 prod 우회 금지(L288 · SPEC-003 L388 · 규칙 3) · pending부터 같은 대상(L289 · SPEC-003 L124) · token+주소 함께 저장·복원·삭제(SPEC-003 L342-346) · HTTP/SSE/WS/푸시/네이티브 수락이 같은 환경(규칙 3 L455). 예외는 W-1 · W-2 · W-3 |

## FAIL

### F-1. [재호출] 노출 조건이 DAY 웹보다 넓다 — 업무 동작 변경인데 조건이 정의되지 않았다

- **자리**: `products/day/20-spec/spec-003-mobile-app.md:159`(U-4 호출 상자). `[재호출](U-5 재호출 모드 · board edit 있을 때 · 웹 E22 는 확인 필요 칸에만 있지만 앱은 룸 상세 호출 상자에 둔다 — 프로토 「다른 의사 호출」 자리)`
- **근거**: DAY-SPEC-002 U-5(L140)는 [재호출]을 「확인 필요 칸의 **응답 없는** 호출 카드」에만 둔다. dev 웹 구현 조건도 같다: `need.why == "call"` **이고** `state == called` 줄이 있고 `board` edit일 때(`templates/partials/board_parts.html:174-185`). SPEC-003은 버튼 **자리**만 옮긴 게 아니다. 조건을 `board` edit 하나로 줄여서, 방금 한 호출이나 이미 수락된 호출에도 [재호출]이 보이게 된다. 서버(`services/board.py` `recall`)는 `accept_block`만 보기 때문에 이 요청을 막지 않는다. 그래서 「업무 동작은 DAY 기준」(브리프 §2 · `_RESUME` 결정)에서 벗어난 정책이 생긴다. 근거는 프로토 자리 하나뿐이다. 거기에 「규칙은 서버 값만」(L453)도 깨진다. 노출 조건을 정할 서버 값(`canRecall` 같은 것)이 없으니 앱이 조건을 직접 짓게 된다.
- **고칠 안**(둘 중 하나):
  1. 노출 조건을 웹과 같게 적는다 — `card.need.why == "call"` · 그 호출에 `state = called` 줄이 있음 · `board` edit. 이 값들은 모두 스냅샷에 있으니 표시 조건일 뿐 재계산이 아니다. 자리(룸 상세 호출 상자)는 플랫폼 적응으로 남겨도 된다.
  2. 넓은 조건을 원하면 §5 「정책」에 OQ로 올린다. 사용자 결정 전에는 1을 기본으로 둔다.
- **직원이 만날 자리**: 간호사가 호출하고 몇 초 뒤 룸 상세에서 [재호출]을 누를 수 있다. 그러면 기존 호출이 닫히고 새 호출이 생긴다(SPEC-002 규칙 6). 원장이 받은 푸시는 무효가 되고 「응답 없음」 줄이 바로 생긴다.

## WARN

### W-1. prod→dev 넘김의 15초 제한이 dev의 KOS 호출 시간(최대 15초 × 3)보다 짧다

- **자리**: `spec-001-login-session.md:270`(`(15초)`) · `:288` · `:321`
- **근거**: dev 로그인은 KOS를 sign-in → get-user-tenants → get-user-account 순서로 차례로 부르고, 호출마다 제한이 15초다(SPEC-001 규칙 10 L384 · L427 · `services/auth.py` 머리 ①~④). 그래서 KOS가 느리기만 해도 dev 응답이 15초를 넘을 수 있다. 이때 prod는 dev가 줄 `kos_unavailable` 대신 `environment_unavailable`을 돌려준다. dev가 늦게라도 성공하면 dev 스키마에 **앱이 모르는 `login_session` 행이 남는다**.
- **고칠 안**: 넘김 제한을 「dev 로그인 최장 시간보다 길게」로 정의한다. 예: KOS 제한 × 3 + 여유. 아니면 숫자를 구현 때 확정하는 칸으로 열어 둔다. 그리고 「넘김 시간 초과로 끝났는데 dev는 성공한 경우」를 케이스 매트릭스에 한 줄 넣는다(남은 세션은 만료로 정리 — 받아들일지).
- **직원(심사관)이 만날 자리**: 심사 중 KOS가 느릴 때 「환경 연결 안 됨」 오류가 뜬다. 심사관에게는 앱 결함으로 보인다.

### W-2. 받은 `api_base_url`을 https만 보고 믿으면 「토큰을 임의 주소로 보내지 않음」이 서버 env 값 하나에만 걸린다

- **자리**: `spec-001-login-session.md:447`(열린 것) · `spec-003-mobile-app.md:489`(https만 확인)
- **근거**: 브리프 §3과 검수 지시 2단계가 「토큰을 임의 주소로 보내지 않음」을 요구한다. 그런데 지금 계약에서는 prod env `DAY_DEMO_API_BASE`를 잘못 넣으면 dev 세션 토큰·비밀번호 다음 요청이 그 주소로 간다. 두 호스트는 이미 **[확정]**이다(mobile-deployment L41 · L226 · deployment.md L27 · `deploy/config/edge.env`의 `DAY_DEV_DOMAIN` · `DAY_PROD_DOMAIN`). 정식 빌드에 허용 호스트 두 개를 `--dart-define`으로 넣고 맞춰 보는 데는 새 제품 결정이 필요 없다.
- **고칠 안**: 정식 빌드는 `api_base_url` 호스트가 빌드 허용 목록(prod · dev 두 개)에 없으면 A-18과 같은 로그인 실패로 다룬다. 개발 빌드는 지금처럼 둔다. SPEC-001 L447의 OQ를 닫고 A-18에 한 줄 더한다. 그대로 열어 두려면 「열린 동안 정식 빌드의 신뢰 근거 = prod env 값」이라는 위험을 메모로 남긴다.

### W-3. 세션 묶음을 저장하는 시점이 SPEC 안에서 두 가지로 적혀 있다

- **자리**: `spec-003-mobile-app.md:126`(「세션 묶음을 Keychain 에 한 번에 저장 → `/me`」) ↔ `:343`(`staff_id`는 `/me` 뒤 확정 · `/me` 실패면 지움) · `:418-419`(Flow: `/me` → 저장)
- **근거**: 묶음에는 `staff_id`가 있어야 한다(L296 · L342). 그런데 U-1은 `/me`보다 **먼저** 저장한다고 적었다. 이렇게 구현하면 `staff_id` 없는 묶음이 생긴다. 「일부만 남는 상태를 두지 않는다」(L342 · A-7)와 충돌한다. 그러면 네이티브 알림 수락(L233)이 `doctorStaffId` 없이 나갈 수 있다.
- **고칠 안**: U-1 L126을 「`/me` 성공 뒤 묶음을 한 번에 저장」으로 고쳐 §3 · Flow와 맞춘다.

### W-4. 병원 고르기 응답의 `api_base_url`이 로그인 때 받은 값과 다를 때 어느 쪽을 쓸지 없다

- **자리**: `spec-001-login-session.md:252-254` · `:289` · `spec-003-mobile-app.md:124` · `:416`
- **근거**: 데모 로그인의 `api_base_url`은 prod env `DAY_DEMO_API_BASE`가 정한다(L254). 병원 고르기 응답은 dev 서버가 직접 내므로 dev env `DAY_PUBLIC_API_BASE`(L253)가 된다. 같은 값을 두 서버의 env 두 곳이 갖고 있다. 둘이 다르면(끝 `/` 하나만 달라도) 앱이 어느 값을 저장할지 SPEC에 없다.
- **고칠 안**: 앱은 「로그인 단계에서 받은 `api_base_url`을 유지하고, hospital 응답 값이 다르면 로그인 실패(`environment_unavailable` 자리)」로 정한다. 아니면 prod가 dev 응답의 `api_base_url`을 그대로 넘기게 해서 원천을 하나로 줄인다(`DAY_DEMO_API_BASE`는 넘김 대상 주소로만 쓴다).

### W-5. 「현황」 탭 칩으로 거른 목록의 순서가 정해지지 않았다

- **자리**: `spec-003-mobile-app.md:135`(「전체」 = `cards[]` 서버 순서). 칩별 순서는 적혀 있지 않다.
- **근거**: DAY 인박스 칸에는 칸마다 정렬이 있다. 확인 필요 = 넘긴 시간 긴 순, 시작 가능 = `urgency` 큰 순, 시술 대기 = 입실 오래된 순(SPEC-002 U-10 L168-170 · `board_rules.py:592-605` `inbox()`). 그런데 이 정렬 결과는 앱 JSON에 없다(`snapshot()`에 `inbox` 키 없음). 칩을 「DAY 인박스 칸」의 적응이라고 정했으면(OQ-A2) 순서도 따라와야 한다. 정하지 않으면 구현자가 `cards[]` 순서나 재정렬 중 하나를 추측해서 고르게 된다.
- **고칠 안**: 칩 안 순서를 정한다. ① `cards[]` 순서(판 순서) 그대로 — 웹 인박스와 달라짐을 명시한다. ② 인박스 순서 — 스냅샷에 칸별 순서(`inbox.rank` 등)를 더하도록 SPEC-002 주인에게 요청(OQ-A12에 더함)하고, 그 전엔 ①. 어느 쪽이든 OQ-A2 줄에 같이 적는다.

### W-6. 호출 · 재호출 요청 본문에 `doctorStaffId`가 빠졌다

- **자리**: `spec-003-mobile-app.md:173`(`{taskIds, target}`) · `:174`(`{target}`)
- **근거**: dev는 `target = "one"`이면 `doctorStaffId`가 필수다. 없으면 400 `invalid_request`가 난다(`routers/api/board.py:46-55` · 웹 주석 `board_parts.html:43`). 정본(SPEC-002 §3)을 가리키고 있기는 하지만, 앱 SPEC에 적은 본문 모양이 틀려 있어서 그대로 옮기면 지정 호출이 실패한다.
- **고칠 안**: `{taskIds, target: "all" | "one", doctorStaffId?}` · `{target, doctorStaffId?}`(one일 때 필수)로 고친다.

### W-7. 기기 등록 API(제안)에 오류·검증이 없고 `app_id`를 앱이 보낸 값 그대로 믿는다

- **자리**: `spec-003-mobile-app.md:355-358`
- **근거**: 검수 지시 2단계는 「API 응답 필드·분기·오류가 구현 가능한지」를 본다. `PUT /api/devices/{install_id}`에는 성공 `{ok}`만 있다. 형식 오류(400 · `push_env` 값 밖) · 세션 없음(401) · `install_id` 형식이 없다. 서버는 앱이 보낸 `app_id`로 APNs topic을 고르는데(L358), 허용 번들 id 목록과 맞춰 보는 규칙도 없다. 지금은 제안 계약(D-2)이라 앱 더블은 만들 수 있다. 하지만 D-2를 맡을 사람이 이 칸들을 추측하게 된다.
- **고칠 안**: 케이스 3~4줄을 더한다. 400 `invalid_request`(칸 · enum 밖 · `app_id`가 서버 허용 목록 밖) · 401 `unauthorized` · `install_id` = uuid 문자열. 허용 목록은 서버 env로 두고 이름만 제안한다. 값은 사용자 몫이다.

### W-8. OQ-A8 「전체 호출 vs 모든 의사」의 전제 일부가 사실과 다르다 — DAY 웹에도 「전체 호출」 · 「전체 의사」 글자가 있다

- **자리**: `spec-003-mobile-app.md:231` · `:542`
- **근거**: DAY 웹 원장 줄 글자는 `kind = all`일 때 「전체 의사」(`board_parts.html:164` · `:201`), 응답 없음 줄은 「전체 호출 응답 없음」(`:167`)이다. 「모든 의사」는 호출 창의 고르기 줄 이름이다(`ui.html`). 그래서 「DAY 웹은 모든 의사라 부른다」는 일부만 맞다. 문구 OQ를 사용자에게 올릴 때 근거로 쓰기 전에 고쳐야 한다.
- **고칠 안**: OQ-A8 설명을 「DAY 웹: 창 = 모든 의사 · 줄 = 전체 의사 / 전체 호출 응답 없음 — 푸시 글자 「전체 호출」은 DAY 웹 줄 글자와 겹친다」로 바로잡는다. 결정은 그대로 열어 둔다.

### W-9. OQ-A2를 「정책 — 기본값 구현 금지」 표에 두고, U-2에서는 확정 계약으로 썼다

- **자리**: `spec-003-mobile-app.md:532`(정책 표 · 「기본값을 결정으로 구현 금지」 · L521) ↔ `:135`(U-2 본문이 인박스 칸 칩을 계약으로 서술)
- **근거**: 코디 지시(2026-11-09 · 「정책 미결을 임의로 닫은 것은 구분해서 검수」)에 따라 구분했다. U-2는 그 칩을 확정 동작으로 적었는데, §5는 같은 항목을 「사용자 결정 전 구현 금지」로 묶었다. 둘 중 하나만 맞을 수 있다. 칩 구성은 업무 규칙을 바꾸지 않는 표시 적응(서버 `inbox.section`만 씀)이다. 그러니 「UI · 구현 선택 — 기본값으로 진행」 표(L545-552)로 옮기는 편이 내용과 맞는다.
- **고칠 안**: OQ-A2를 「UI · 구현 선택」 표로 옮긴다(기본값 = 인박스 칸 칩). 이것을 정책으로 본다면 U-2에 「OQ-A2 결정 전 임시」를 적는다. W-5(칩 안 순서)도 같은 줄에서 정한다.

### 정책 미결을 닫았나 — 구분 결과 (코디 지시 반영)

| 항목 | 판정 |
|---|---|
| 데모 계정 → dev 환경 계약(SPEC-001 §3 · SPEC-003 §3) | **사용자 승인 사항** — 미승인으로 지적하지 않는다 |
| OQ-A15 통역 권한 · OQ-A17 푸시 받는 사람 · 알림 수락 조건 · OQ-A9 · OQ-A11 · OQ-A1 | 열어 두고 「기본값 구현 금지」로 막았다 — 적절 |
| [재호출] 노출 조건 확대(U-4) | **임의로 닫음** → F-1 |
| OQ-A2 칩 구성 | 정책 표와 본문이 엇갈림 → W-9 |
| OQ-A3 · A4 · A13 · A14(셸 · 글꼴 · 이메일 기억 · `push_env`) | 표시 · 구현 선택 — 기본값으로 진행 가능 |
| env 이름 셋 · 넘김 15초 | 「이름 제안 · 구현 때 확정」으로 열려 있다(15초의 길이 문제는 W-1) |

### 코드 단계 정합 기록 (지적 아님 — 코디 지시)

- CENTURION_DAY `AGENTS.md` 「앱 (Flutter)」 L106 「서버 주소 · 환경값은 빌드 설정(`--dart-define`)으로」는 사용자 최신 결정과 맞춰 고쳐야 한다. 최신 결정 = 빌드에는 **고정 로그인 진입점**(+ W-2를 받아들이면 허용 호스트 목록)만 넣고, 세션의 연결 대상은 로그인 응답 `api_base_url`로 정한다. 코드 PR에서 AGENTS 문구를 함께 고친다. SPEC-003 L444 「서버 주소 · 환경값 = `--dart-define`(고정 진입점 · APNs 환경)」도 같은 뜻으로 맞춘다.

### 참고 수준(판정에 넣지 않음)

- `spec-003-mobile-app.md:224` `kos_failed` 토스트 = 「<방> · <고객> — KOS 반영 실패 — …」. 이것은 dev 웹 구현(`partials/board_toast_kos_failed.html` — `action`을 넘기지만 그리지 않음)과 같다. SPEC-002 규칙 22(L585)는 「실패한 동작」도 조각에 넣는다고 적었다 → SPEC-002 · 구현 차이이므로 OQ-A12 목록에 같이 올리면 좋다.
- A-4 「prod 에 그 계정 행이 생기지 않음」(L501)의 실물 확인은 prod DB 조회가 필요하다. 누가 · 무엇으로 볼지(사용자 · 읽기 쿼리)를 적어 두면 확인하기 쉽다.
- U-4 호출 상자 [수락](L159)은 `board.accept`에 「수락 대기일 때만」을 명시하면 구현 추측이 줄어든다(호출 탭 · 시술 줄 [수락]은 `state = called`로 정해져 있다).

## 직원이 실물에서 만날 자리

| 자리 | 누가 | 무엇을 겪나 | 관련 |
|---|---|---|---|
| 룸 상세 호출 상자 [재호출] | 간호사 | 호출 직후에도 재호출이 보인다 → 원장 푸시가 무효가 되고 「응답 없음」 줄이 생긴다 | F-1 |
| 정식 앱 로그인(KOS 느릴 때) | 심사관 | 「환경 연결 안 됨」 계열 오류 — 문구는 OQ-A16이라 아직 코드만 보인다 | W-1 · OQ-A16 |
| 잠금 화면 알림 [수락] | 원장 | 묶음을 `/me` 전에 저장하면 `staff_id`가 비어 「수락 못 함」이 뜬다 | W-3 |
| 「현황」 탭 「확인 필요」 칩 | 간호사 · 원장 | 웹 인박스와 카드 순서가 다르다(웹은 오래 넘긴 순) | W-5 |
| 지정 호출 | 간호사 | SPEC 본문 그대로 구현하면 원장 한 명 호출이 400으로 실패한다 | W-6 |
| 데모 → 일반 계정 전환(같은 기기) | 테스터 · 심사관 | dev에 남은 기기 연결로 푸시가 오면 `environment` 비교로 무시된다(계약상 맞음 — 실기기에서 확인할 것) | A-15 |
| 빈 판 · 오더 메모 없음 · 네트워크 실패 토스트 | 전 직무 | 글자 없이 비거나 코드만 보인다(문구 OQ) | OQ-A5 · A6 · A7 |
| 통역 `vi` · `yue` | 시술실 | 빠른 말하기 칩이 없다(번역 원천 없음 — 의도) | OQ-A11 |

## 참고(기존 부채 · 무관 분리)

- **lint**: `python3 scripts/lint-pipeline.py --strict` → exit 0 · `0 error, 263 warning`. products/day 해당 0. 263건은 모두 다른 제품(예: `products/selly/30-work/*` `doc_no` 누락 · `products/selly/30-work.md` frontmatter 없음) — **무관**.
- **SPEC-002 · 구현 차이(옆 세션 소유)**: 오류 본문 `{detail, code, field}` · SSE `session_expired` · 연결 수명 1시간 · 구현에만 있는 칸(`firstKind` · `lateAt` · `need.overSec` · `anesthesia.lateAt`). SPEC-003 OQ-A12가 정확히 기록했다(코드 대조 확인 — `routers/api/board.py:1-15` · `board_rules.py:426-430` · `:352` · `:506`). 이번 판정과 무관하다.
- **옆 세션 PR #920(origin `kknaksss/day-procedure-board-2-spec` · 745e8ef3 · main 미머지)과 겹침**: SPEC-001(머리 개정 ⑥ · 후보 규칙 · 매트릭스 · 규칙 5 · OQ-10)과 mobile-deployment(§1 · 그림 · §9 KOS 행 · M-18)를 같이 고친다. 이 워크트리의 mobile-deployment L34 · L61 · L230 · L295에 `is_demo` 문장이 아직 남아 있는데, 이는 기존 문장이고 #920이 바꾸는 자리다. 이쪽 SPEC-001 개정 줄(L33)과 M-19(L296)는 바로 옆 줄이라 머지 충돌이 나니 둘 다 남겨야 한다(planner 보고 「머지 충돌 주의」와 같음). #920 뒤에는 dev가 스키마로 데모 병원만 보므로 이 SPEC의 dev 넘김과 정합한다. `doc_no` 충돌은 없다(#920은 DOC-1~6).
- `_RESUME` 「첫 업로드 = iOS 개발 버전」과 최종 「정식 앱 하나 · 데모 → dev」의 관계는 mobile-deployment M-19로 열려 있다. 열린 것을 열린 채로 둔 것이라 지적하지 않는다.
- `10-decision.md` 변경 없음은 적절하다 — escalation 거리가 없다(사용자가 정한 방향 · 남은 것은 팀 몫 OQ).
