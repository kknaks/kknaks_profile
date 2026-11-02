# 리뷰 리포트 — strong-hajin-inbox / SPEC-008 · SPEC-009 (v0.2.0) 검수 (2026-10-06)

## 판정: FAIL

FAIL 4건 · WARN 17건. 결정 대부분(D-01~D-50 · 원장 후속 결정)은 본문 계약에 들어가 있고, 코드 근거 줄도 거의 다 맞는다.
FAIL 이 난 자리는 셋이다. **결정과 정면으로 다른 곳 한 곳**(D-15), **지금 코드 구조에 붙지 않는 곳 한 곳**(데스크톱 셸 안 OAuth),
그리고 **구현 워커가 이 문서만으로는 짤 수 없는 곳 두 곳**(API 요청/응답 모양 · HTML 메일 보안)이다.

> 사용 범례 — `S8` = `para/projects/summer-star/strong-hajin/20-spec/spec-008-external-channels.md` ·
> `S9` = `…/spec-009-mac-kakao-collector.md` · `DEC` = `…/10-decision/decision-008-external-channels.md` ·
> `RES` = `orchestration/work/strong-hajin-inbox/_RESUME.md` · `CODE` = `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-inbox`(origin/main `202078b`) ·
> `CHART` = `/Users/kknaks/git/harness_works/k8s_infra_mac/charts/strong-hajin`

## 검수 범위

- 대상: S8(558줄) · S9(273줄) 본문 전부. 문서 리포 diff 검수(린트)는 이번 브리프 범위 밖이라 **돌리지 않았다** — 계약 리뷰다
- 기준: DEC D-01~D-50 · RES §2 의 DEC-008 뒤 행 4개(Socket Mode/pull · 보존 없음·50MB · mykakao·OQ 추천안 · 비밀값 위치) · DC-1~6 · SPEC-006 · runbook-002 · CHART
- 실행한 검사: S8·S9 가 든 코드 근거 **35곳**을 `sed -n`/`grep -n` 으로 하나씩 열어 봤다(아래 §확인한 것 표). 데스크톱 셸 `lib.rs`·`download.rs`·`flavors/*` · 차트 `worker.yaml`·`ingress.yaml`·`values*.yaml` · `Makefile` local-stack 를 대조했다. 테스트·빌드는 돌리지 않았다

---

## 위반 (FAIL 사유)

| # | 항목 | 근거 파일:줄 | 무엇이 어긋났나 | 고칠 것 (한 줄) |
|---|---|---|---|---|
| **F-1** | 결정 정합 — **D-15 와 반대 방향** | S8:286 · S8:287 · S8:318-319 · S8:525 / DEC:164 · DEC:379 | DEC D-15 는 「~~서버에 … 사용자가 저장한 채팅방 ID 를 보관~~」을 **명시적으로 뒤집고** 고른 방 정보를 로컬 Rust 에 둔다고 했다. 그런데 S8 은 ① 카톡 고른 방을 `POST /api/integrations/{id}/rooms` 로 **서버에 저장**하고 ② handshake 가 「고른 방 id 목록」을 **서버에서 내려주며**(즉 서버가 정본) ③ `rooms/report` 로 **고르지 않은 방까지 전부**(이름·참여자)를 서버에 올린다. ③은 D-18 「사용자가 고른 대화방만 수집」과도 부딪힌다. S8 대응표(S8:525)는 이 충돌을 「SPEC-009(§4.6 handshake 는 고른 방 id)」로만 적고 넘어갔다 | 둘 중 하나로 정하고 본문에 적는다: (a) 방 목록·선택은 **Mac 이 정본**이고 서버는 웹 고르기 창을 위해 **중계만**(목록은 저장 안 함 · 앱 꺼지면 비움 — DC-6 「앱 꺼짐이면 목록 대신 …」과 맞는다) · 서버에 남는 방은 메시지가 올라온 방뿐, 또는 (b) 서버 저장이 맞다면 **D-15 재해석을 사용자 결정으로 받아** 원장·DEC 에 행을 더한다. 어느 쪽이든 `rooms/report` 의 고르지 않은 방 이름 저장 여부를 명시 |
| **F-2** | 코드 정합 — **데스크톱 셸 안에서 「Google로 연결」·「슬랙 연결」이 돌지 않는다** · OAuth `state` 계약 없음 | S8:271-276 · S8:304-307 / `CODE/frontend/src-tauri/src/lib.rs:494-498`(같은 origin `/api/` 이동은 셸이 가로챈다) · `download.rs:54-61` · `download.rs:398`(`max_redirects(0)`) · `lib.rs:483-492`(허용 목록 밖은 기본 브라우저로) · `flavors/medi-ax/shell.config.json`(`navigationAllowlist: []`) | S8 은 연결을 「`GET /api/integrations/mail/connect` → 302 → Google」로 정했다. 회사판 앱(medi-ax) 안에서 이 주소로 가면 SPEC-006 U-5 가 **이동을 취소하고 셸이 직접 GET** 한다 — redirect 0 이라 302 는 **실패 토스트**로 끝난다. Google 주소로 바로 보내도 허용 목록 밖이라 **기본 브라우저**로 열리고, 그 브라우저엔 `scax_session` 쿠키가 없어 콜백이 누구의 연결인지 모른다. 또 S8 전체에 OAuth `state`(CSRF·회원 묶기) 계약이 없다. `POST …/reconnect` 가 「302 → 동의」인 것도 fetch POST 로는 화면이 넘어가지 않는다(S8:276) | 연결 시작을 「서버가 **회원에 묶인 일회용 `state`** 를 발급한 동의 URL 을 JSON 으로 돌려준다 → 웹이 브라우저면 `location` 이동, 데스크톱이면 `open_external`」로 바꾸고, **콜백은 쿠키가 아니라 `state` 로 회원을 찾는다**고 적는다. reconnect 도 같은 모양. 콜백 뒤 302 목적지는 `AX_WEB_ORIGIN`(`bootstrap/settings.py:178`) 기준이라고 적는다. SPEC-006 개정 범위(W-10)에 이 흐름을 넣는다 |
| **F-3** | 위험 — **HTML 메일·중계 첨부의 보안 계약 없음** | S8:143 · S8:261 · S8:295 · S8:362 | 메일은 「원문 그대로 저장 · 렌더는 프론트 · HTML 메일 틀」만 있다. 외부 누구나 보낼 수 있는 HTML 을 **세션이 사는 같은 origin** 에 그리므로 소독(sanitize)·격리(샌드박스 iframe·CSP)·원격 이미지(추적 픽셀) 처리·`cid:` 인라인 이미지 출처가 계약에 있어야 한다. 쿠키가 HttpOnly 여도 스크립트가 돌면 `/api` 를 그 사람으로 부를 수 있다(답장 보내기 포함) | §2.1·§4.4 에 한 단락: 「HTML 본문은 **스크립트·이벤트 속성·폼 제거 + 샌드박스 iframe(allow-scripts 없음)** 으로 그린다 · 원격 이미지는 기본 차단(또는 서버 프록시) · `cid:` 는 첨부 중계 경로로 · 중계 응답은 기존 `inline_media_type` 허용 목록만 inline, 나머지 `attachment`」 |
| **F-4** | 계약 완결성 — **API 요청/응답·오류 모양이 없다**(특히 §4.4 · §4.6) | S8:280-300 · S8:316-322 | 경로와 「뜻」만 있고 요청 필드·응답 필드·오류 코드가 거의 없다. BE·FE·Rust 워커가 각자 짜면 어긋난다. 빠진 것 중 구현이 막히는 것: ① 방 본문 `GET /api/inbox/messages/{id}` — 메일/방 id 구분, **방 메시지 페이지네이션**(슬랙 백필 = 「API 허용 전부」라 한 번에 못 낸다), **스레드 답글 받는 경로** ② 방 카드의 「읽음」이 무엇까지를 읽음으로 치나(마지막 메시지 ts 까지) ③ 웹이 **새 메시지를 어떻게 아나**(「새 메시지 N개」·실시간 — WS/폴링 미정) ④ 카톡: **`aid` 를 누가 만드나**(메시지 업로드 응답이 돌려주나, `(chatId,logId,순번)` 인가) · 카톡 **연동 레코드를 누가 언제 만드나**(첫 handshake?) · **방별 상태**(`backfilling/live/paused`) 보고 필드 · 메시지 묶음 최대 크기 ⑤ 슬랙 보내기 재시도의 중복 방지(기존 `Idempotency-Key` 헤더 — `entrypoints/http.py:1364-1367` `create_task` 본보기) ⑥ 오류 표(S8:349-357)에 슬랙/Gmail 상류 실패(429·5xx) 응답 | §4.3·§4.4·§4.6 경로마다 「요청 → 응답 → 오류」 세 칸을 더한다. 스키마 전문이 아니라 **드러나는 필드 이름·enum** 수준이면 된다(README Data Boundary 안) |

---

## 경미 (WARN)

| # | 항목 | 근거 파일:줄 | 내용 | 고칠 것 (한 줄) |
|---|---|---|---|---|
| W-1 | SPEC 둘 사이 — 방별 상태 | S9:122 ↔ S8:322-325 | S9 은 앱이 방별 `backfilling/live/paused` 를 보고한다고 하는데 S8 §4.6 status 입력에는 방별 칸이 없다. 서버가 카톡 방의 「과거 대화 채우는 중 → 실시간」(DC-6 §2)을 언제 바꾸는지 정해지지 않았다 | §4.6 status(또는 messages 업로드)에 `rooms:[{room_id, state}]` 를 넣거나, 「첫 묶음의 `backfill_done` 표지」로 정한다 |
| W-2 | SPEC 둘 사이 — 「읽기 불가」 문구 둘 | S8:192 ↔ S9:263-266 / DEC:229 | 같은 `unreadable` 상태에 문구가 둘이다 — D-42 「…권한·버전 확인」 vs OQ-905 「…버전이 바뀌었을 수 있습니다」. 상태에 **사유**가 없어 어느 것을 띄울지 못 고른다(권한=전체 디스크 접근 없음 · 버전=DB 못 엶) | status 에 `kakao_reason: permission|version|unknown` 을 더하고 사유별 문구를 S8 §2.5 한 곳에 둔다 |
| W-3 | 카톡 「앱 꺼짐」을 서버가 알 길 | S8:322-325 · S9:119 | `app: off` 는 꺼진 앱이 스스로 올릴 수 없다(강제 종료·잠자기). heartbeat 주기와 「마지막 보고 후 N초면 꺼짐」 판정이 없다. D-43 「마지막 연결」도 여기서 나온다 | status 를 주기 보고(예: 30초)로 정하고 서버가 「N초 무보고 = 꺼짐」으로 판정한다고 적는다 |
| W-4 | 카톡 계정 바뀜 → 「다시 연결」 흐름 | S8:244-245 · S8:325 / DEC:232 | `account_changed` 로 멈춘 뒤 사람이 누르는 「다시 연결」이 어떤 호출인지, 예전 계정의 방·대화는 남나(D-46 과의 관계) 정해지지 않았다. S8 §2.5 화면 계약에도 이 상태가 없다(S-10 시나리오에만 있음) | §2.5 에 상태 줄 하나 + §4.6 에 `POST …/kakao/reset-account`(또는 handshake 의 확인 플래그) 와 옛 방 처리(소프트 딜리트 유지) |
| W-5 | 앱의 인증 수명 — 백그라운드 수집기가 12시간마다 끊긴다 | S9:167-171 · S8:312-314 / `CODE/backend/src/ax_workspace/entrypoints/http_auth.py:22`(`SESSION_MAX_AGE` 12h) · `platform/auth_sessions.py:12` · `src-tauri/src/lib.rs:298-303`(쿠키는 메인 창 웹뷰에서 꺼낸다) | 수집기는 웹뷰 쿠키를 빌려 쓰므로 ① 세션 12시간이 지나면 업로드가 401 로 멈추고 ② 메인 창이 없으면 쿠키를 못 꺼낸다. 사진 CDN TTL ~3일이라 주말 동안 끊기면 「만료됨」이 쌓인다 | S9 에 「세션 만료 시 상태 `login_required` · 트레이 표식 · 재로그인 뒤 handshake 의 마지막 지점부터 메운다」를 적고, 장수명 기기 토큰이 필요하면 OQ 로 연다 |
| W-6 | SPEC-006 **개정 범위가 I-2 하나로 좁게 적혔다** | S9:95-98 · S9:202-205 / `spec-006-tauri-wrapper.md:110` · `:150` · `:272` · AC-T23(`:885`) · AC-T33(`:907`) · AC-T47(`:950`) / `src-tauri/src/lib.rs:853-855`(`trayIcon` 금지 시험) · `flavors/medi-ax/capabilities/*.json`(권한 넷) | 같은 앱에 수집을 더하면 깨지는 것은 I-2 만이 아니다 — 「창 하나 · 트레이·메뉴 막대 상주 없음 · 백그라운드 실행 안 함」(§2·§110·§272) · AC-T23·AC-T33·AC-T47 · 셸 시험 `trayIcon` 금지 · 전체 디스크 접근(Info.plist/Entitlements). S9 §2.1 의 트레이 아이콘은 지금 시험과 정면 충돌한다 | 「SPEC-006 개정 필요」 목록을 위 항목 전부로 늘리고, F-2 의 OAuth 외부 열기 흐름도 함께 넣는다 |
| W-7 | 어느 앱 판(flavor)에 수집을 넣나 | S9:95 · S9:202 · S8:549 / `src-tauri/flavors/medi-ax/shell.config.json`(origin `https://ax.medisolveai.xyz`) · `flavors/strong-hajin/shell.config.json`(`operationalOrigin: null`) · 커밋 `015bed2` | S9 은 「같은 **Strong Hajin** 데스크톱 앱」이라 하는데 지금 앱은 두 판이다. 운영 서버에 붙는 것은 **회사판 medi-ax** 이고 개인판 Strong Hajin 은 주소가 없다. S8 OQ-804 「이번엔 회사판만」과도 맞춰야 한다 | 「수집은 **회사판(medi-ax)** 에 넣는다(개인판은 주소가 정해질 때)」처럼 판을 적는다 |
| W-8 | 슬랙 Socket Mode 이벤트를 **사람마다 나눠 담기** | S8:374-375 · S8:379-384 / DEC:184 | 사용자 토큰 이벤트는 앱 토큰 하나로 들어오지만 같은 채널을 고른 사람이 여럿이면 이벤트 `authorizations` 가 한 사람만 담는다(슬랙이 잘라서 보냄). D-25(사람마다 따로 저장)를 지키려면 워커가 「그 팀에서 이 방을 고른 **모든** 연동」으로 펼쳐야 한다 | §5 동기화에 「이벤트 1건 → (team, channel) 을 고른 모든 연동에 복제 저장 · 중복 키 `(연동, channel, ts)`」를 적는다 |
| W-9 | 로컬 개발 주소가 local-stack 과 다르다 · 슬랙은 http 리디렉션 불가 | S8:306-307 / `CODE/Makefile:16-17`(`E2E_API_PORT=8001` · `E2E_FRONTEND_PORT=5176`) · `Makefile:285-288` / RES:93(「슬랙 OAuth 버튼 흐름은 https 필요 → 운영에서 확인」) · RES:93(「리디렉션 localhost+운영」) | S8 은 로컬 redirect_uri 를 `http://127.0.0.1:8000` 으로 적었지만 `make local-stack` 은 API 를 **8001** 에 띄운다. 또 원장은 슬랙 OAuth 가 https 필요라 **운영에서 확인**한다고 했는데 S8 은 「Google·슬랙 앱에 두 redirect_uri 를 등록」이라 적었다 | 로컬은 Google 만(`…:8001` 또는 프론트 origin 경유), 슬랙 연결은 운영에서만 시험한다고 원장대로 고친다 |
| W-10 | 운영 배치 — 업로드 크기가 ingress 에서 먼저 막힌다 | S8:155-157 · S8:342 / `CHART/values.yaml:23`(`proxyBodySize: "50m"`) · `CHART/templates/ingress.yaml:30-32`(「앱 한도보다 커야 한다」 주석) | 앱 한도 50MB 와 ingress 50m 이 같다 — multipart 머리만큼 넘쳐 nginx 가 맨 413 을 낸다. 슬랙 보내기가 파일 여럿을 한 요청에 실으면 더 넘는다. 한도가 **파일 하나당인지 요청 합계인지**도 없다 | 한도를 「파일 하나당 50MB · 요청 합계 N」으로 적고, 차트 `proxyBodySize` 를 그보다 크게 올리는 것을 `30-work/` 운영 할 일로 적는다 |
| W-11 | 메일 25MB — 파일당인가 합계인가 | S8:300 · S8:341 / DC-3 §2.3 | S8 은 「25MB 초과 파일이 하나라도 있으면 거절」(파일당)이다. Gmail 한도는 **메일 전체**(본문 + base64 로 부푼 첨부)라 20MB 파일 둘이면 파일당 검사는 통과하고 Gmail 이 거절한다 | 「첨부 합계(인코딩 전) 기준 한도 + 파일당 표시」로 고치거나, 서버가 합계 초과를 같은 오류로 낸다고 적는다 |
| W-12 | 운영 배치 — 어느 pod 가 무엇을 마운트·주입받나 | S8:379-384 · S8:393-396 · S8:410 · S8:428-430 / `CHART/templates/worker.yaml:18-19`(모든 kind 가 `worker.replicas` 하나를 같이 씀) · `worker.yaml:54-62`(hostPath 둘만) · `back.yaml:48-50` | ① 카톡 첨부·프로필 이미지 업로드는 **API(back)** 가 받으므로 새 hostPath 는 back 에 마운트돼야 한다 — 워커만이 아니다 ② `GOOGLE_PUBSUB_SA_KEY_FILE` 은 **파일**이라 `envFrom secretRef` 로는 안 들어간다(Secret 볼륨 마운트 필요) ③ 「replicas:1 이 계약」인데 차트는 kind 별 레플리카가 없다 — 남이 `worker.replicas` 를 올리면 Socket Mode 가 갈린다 ④ OAuth 클라이언트 비밀값·암호화 키는 **back 과 연동 워커 둘 다** 필요 | §5 에 pod×(env·Secret 파일·hostPath) 표 한 장. 「연동 워커는 kind 별 replicas 고정 1」을 차트 할 일로 적는다 |
| W-13 | 로컬 스택에 새 워커가 없다 | S8:379-384 · S8:422-427 / `CODE/Makefile:296-323`(local-stack 이 띄우는 프로세스 다섯) · `Makefile:256-266` | 새 연동 워커를 `make local-stack`·`acceptance-e2e` 가 띄우고 `~/.config/google/env`·`~/.config/slack/env` 를 그 타겟에 싣는다는 말이 없다(지금 Soniox 는 `meeting-worker` 타겟에만 실린다, `Makefile:263`) | 「연동 워커 Make 타겟 + local-stack 감독 목록에 추가 + 두 env 파일은 api·연동 워커 타겟에 싣는다」 한 줄 |
| W-14 | AX 캐릭터 진입점이 **둘인데 하나만** 지운다 | S8:443-445 · S8:107 / `CODE/frontend/src/App.tsx:402-405`(`onUserClick` — 신원 줄) · `App.tsx:416-428`(`utilityItems` 설정) · `frontend/src/shell/SideNav.tsx:18` | D-48 「런처·머리 단추를 없앤다」. S8 §5 은 `utilityItems → AssistantCharacterPicker` 만 옮긴다고 적었다. 신원 줄을 눌러도 같은 모달이 열린다(`onUserClick`) | §5 프론트에 `App.tsx:402` `onUserClick` 도 없애거나 프로필 설정으로 보낸다고 적는다 |
| W-15 | 프로필 API — 있는 것 재사용 · 이미지 받는 길 없음 | S8:333-335 / `CODE/backend/src/ax_workspace/entrypoints/http.py:1360-1362`(`GET /api/organization/me`) · `modules/organization_access/results.py:67-68`(`MyOrganizationProfileView` = 소속·직책·직무 + `assistant_character`) | `GET /api/profile` 을 새로 만들면 이미 있는 `/api/organization/me`(같은 값)와 겹친다. 반대로 **프로필 이미지를 내려받는 GET 이 없다** — 아바타를 어디서 그리나(SideNav·대화) 정해지지 않았다 | `GET /api/profile` 대신 `/api/organization/me` 에 `profile_image_url` 을 더하고, `GET /api/profile/image`(또는 `/api/members/{id}/image`) 를 둔다 |
| W-16 | 결정 문서와의 표 정합 — 「D-49 대체」가 DEC 에 반영되지 않음 | S8:33 · S8:170-172 · S8:534 / DEC:236 · RES:94 | S8 은 「보존·파기 없음 — D-49 를 대체」라고 하는데 DEC-008(accepted)은 여전히 「이번에 정하지 않는다」다. 계약 문서가 결정을 뒤집는 구조라 둘을 읽는 사람이 어긋난다 | DEC-008 에 개정 행(D-49 갱신 · 원장 2026-10-06 「보존 없음」)을 다는 일을 코디 할 일로 남긴다 — SPEC 쪽은 그대로 둬도 된다 |
| W-17 | 문서 규율 | S8:34-36(「바뀐 문장은 취소선 + `→ v0.2.0`」) — 본문 `~~` 0건 · S8:308(「→ **OQ-803** 아님, **OQ-804** 참조」 남은 초안 문장) · S8:23(`DEC-007` 을 `links.specs` 에 둠) · S8:113·S8:438-439(`migrations/manual/` — 실제는 `CODE/backend/migrations/manual/`) · S9:201·S9:206(폴링 2초 두 번) | 머리 주석이 약속한 변경 표시가 본문에 없고, 정리 안 된 문장·틀린 경로·frontmatter 자리가 섞였다 | 취소선 약속을 지우거나 지키고 · S8:308 을 「개인판 redirect 는 범위 밖(OQ-804 닫힘)」으로 · `DEC-007` 을 `links.decisions` 로 · 경로를 `backend/migrations/manual/` 로 · S9:206 삭제 |

---

## 항목별 판정 표 (브리프 §2 의 1~7)

| # | 항목 | 판정 | 요지 |
|---|---|---|---|
| 1 | 결정 정합 (D-01~D-50 + 원장 후속) | **FAIL** | D-15 반대 방향(F-1). 나머지 49건은 본문 계약에서 확인 — 아래 「확인한 것」. 원장 후속 4행(Socket Mode·pull · 보존 없음·25/50MB · mykakao·OQ 추천안 · 비밀값 위치)은 모두 반영(S8:31-36 · :155-157 · :361 · :379-385 · :401-430 · S9:29-47 · :255-263). D-49 대체의 DEC 미반영은 W-16 |
| 2 | 코드 정합 (근거 줄 · 붙을 수 있나) | **FAIL** | 근거 35곳 중 **33곳 맞음 · 1곳 경로 틀림(W-17) · 1곳 범위 부족(W-14)**. 붙기 어려운 곳: 데스크톱 셸 OAuth(F-2) · 수집기 인증 수명(W-5) · 앱 판(W-7) · local-stack 포트·워커(W-9·W-13) · 차트 배치(W-10·W-12) |
| 3 | 계약 완결성 | **FAIL** | 요청/응답/오류 모양 없음(F-4). 데이터(소유·소프트 딜리트·중복 키) · 동기화(단일 소유·watch 매일·pull·백필·메우기) · 첨부(중계·hostPath·한도) · 답장 · 비밀번호는 **있다**. 슬랙 팬아웃(W-8) · 카톡 방 상태·heartbeat·계정 바뀜(W-1·W-3·W-4) · 한도 단위(W-10·W-11) 빠짐 |
| 4 | UX 정합 | **WARN** | 메시지함 2/3열·420px·폭 전체·네 상태 · 답장 상태(작성·보내는 중·보냄·실패·다시 보내기) · 설정 세 연동(연결 전·연결됨·채우는 중·끊김 / 앱 없음·앱 꺼짐·카톡 꺼짐) · 방 고르기 네 상태 · 프로필(즉시 저장·용량 초과·저장 실패 되돌림·불일치·현재 틀림) 모두 S8 §2 에 있음. 빠짐: 카톡 「계정이 바뀌었습니다」 상태 줄(W-4) · 슬랙 본문 머리 「슬랙에서 열기」(DC-1 §2.4 — S8:144 에 없음, 퍼머링크 출처 필요) · 「Mac 앱 받기」 링크 목적지(DC-6 §5 「자리만」 — 계약에 없음) |
| 5 | SPEC 둘 사이 계약 (S8 §4.6 ↔ S9) | **WARN** | 다섯 경로·중복 키·인증 방식·첨부 종류·50MB 는 일치(S9:159-165 ↔ S8:316-322 · S9:177 ↔ S8:155). 어긋남: 방별 상태(W-1) · 「읽기 불가」 문구·사유(W-2) · `aid` 출처(F-4 ④) |
| 6 | 위험 | **FAIL** | 비밀값 — 값 없음·이름만·로컬 `~/.config/<서비스>/env`·운영 Secret(S8:401-430) 은 원장대로 **문제없음**. 남의 메시지 — 「남의 것 404」(S8:253 · :351) 원칙은 있으나 카톡 업로드가 **고른 방만 받는지** 서버 검사 규칙이 없음(F-1 과 묶어 고칠 것). HTML 메일 XSS(F-3) · 운영 배치(W-10·W-12) · SPEC-006 개정 범위(W-6) |
| 7 | SPEC-009 DB 여는 절차 비움 | **PASS** | 브리프 지시대로 FAIL 로 치지 않음. 경계 입출력(입력 = 로그인 계정 / 출력 = 방·메시지 행·첨부 메타 / 실패 = `unreadable`)은 S9 §3.1(S9:133-144)에 **충분**하다. 참조처가 mykakao DEC-001·SPEC-001 로 원장(RES:95)대로 바뀌었다 |

**총평: FAIL** — F-1~F-4 를 고치면 WARN 수준으로 내려간다. 구조(소유 경계·워커 단일 소유·비밀값 규칙·카톡 경계)는 탄탄하다.

---

## 기존 부채 (이번 판정 제외)

- `CHART/values-prod.yaml:20` `worker.kinds: []` — 운영 워커 목록이 배포 때 정해지는 구조. 새 연동 워커도 그 목록에 넣어야 뜬다(W-12 와 함께 운영 할 일로)
- 회사판 셸 `navigationAllowlist: []` — 인증 흐름용 자리는 이미 비어 있다(F-2 의 해법 중 하나가 될 수 있다)
- DC-1 §5 · DC-4 §3 — `assets/avatar-person.png` 로컬 사본 없음(RES:24 `[!]`)

## 확인한 것 (PASS 근거)

### 코드 근거 대조 — 35곳

| SPEC 이 든 자리 | 실제 | 결과 |
|---|---|---|
| `entrypoints/http_auth.py:1-19` · `:38-77` · `:68` | 머리 주석(OIDC 가 같은 세션 스토어에 붙음) · `session_id_from`~`current_principal`(정의는 `:69`) | 맞음 |
| `platform/auth_sessions.py` | `create`·`member_for`·`revoke(session_id)` — 회원 단위 일괄 revoke 는 없다(비밀번호 변경 때 새로 필요 · S8:337 이 그 일을 적음) | 맞음 |
| `platform/persistence.py:1993` · `:92` · `:59` | `AuthSessionRecord` · `MemberCredentialRecord` · `MemberRecord` | 맞음 |
| `modules/organization_access/credentials.py` | PBKDF2 · `MINIMUM_PASSWORD_LENGTH=8` · `PasswordRejected` | 맞음 |
| `entrypoints/http.py:679` | `PUT /api/profile/preferences/assistant-character` · 422/409 | 맞음 |
| `http.py:1066` · `:1105` · `:609` | 자료 업로드(되는 것만 붙음) · `/content` Content-Disposition · `create_app` | 맞음 |
| `platform/materials.py:26` · `:31` | `_path` 안 · `put` | 맞음 |
| `bootstrap/application.py:948` | `LocalDirectoryMaterialStorage(Path(settings.materials_dir))` | 맞음 |
| `bootstrap/settings.py:141` · `:158` · `:179-183` | `from_environment` · `AX_MATERIALS_DIR` · `TDL_*` | 맞음 |
| `bootstrap/schema_sync.py:1-6` | additive 전용·운영은 별도 gate | 맞음 |
| `migrations/manual/…w7-successor-index.concurrent.sql` | 실제 `backend/migrations/manual/` | **경로 틀림(W-17)** |
| `entrypoints/material_worker.py` | `Worker(Settings.from_environment())` + 신호 | 맞음 |
| `frontend/src/App.tsx:37-48` · `:395` · `:401` · `:417` · `:409-423` · `:606` | `navigation` · `AppShell` · `onSelect` · `utilityItems` · 피커 | 맞음 — 단 `:402` `onUserClick` 누락(W-14) |
| `frontend/src/styles/shell.css:70` | `.scax-app-shell{min-width:1542px}` | 맞음 |
| `frontend/vite.config.ts:14` | `/api` → `127.0.0.1:8000` | 맞음(단 local-stack 은 8001 — W-9) |
| `frontend/src/shell/InboxRail.tsx` | 있음 | 맞음 |
| `frontend/src-tauri/src/lib.rs:7-13` | 커맨드 넷 · 파일 권한 없음 | 맞음 |
| `src-tauri/src/download.rs:387` · `:465` | `fetch(url, cookie_header, dir)` · `cookie_header` | 맞음 |
| `Makefile:2` · `:5` · `:6` · `:9` | `SONIOX_ENV_FILE` · `set -a` · `THECONNECT_ENV_FILE` · 같은 결 | 맞음 |
| runbook-002 `:42` · `:157` · `:164` | 워커 넷 · Secret patch · hostPath `Directory` | 맞음 |
| `CHART/templates/back.yaml:48-50` · `worker.yaml:39-41` | `secretRef` `optional: true` | 맞음 |

### 결정 → 본문 계약 (대응표가 아니라 본문에서 확인)

- D-06·D-07(읽음만·카드 행동 없음) S8:126-141 · D-08 S8:138-139 · D-09(readonly+send 한 번·env 로만) S8:271 · :408 · D-10(받은편지함만·여러 계정) S8:161-164 · D-11·D-12·D-13 S8:180-183 · :285 · D-14·D-16·D-17·D-18·D-19·D-20 S9:35-50 · :75-87 · :133-144 · D-22(Socket Mode·watch 매일·메우기) S8:379-388 · D-23 S8:386 · D-24·D-25 S8:252-253 · :373-375 · D-26 S8:259-261 · D-27·D-46 S8:167-172 · :275-276 · D-28 S8:261 · :362 · D-29 S8:151-152 · :297 · D-30·D-31 S8:153-157 · S9:175-180 · D-32 S8:214-220 · :298-300 · :434 · D-33·D-34 S8:142-146 · D-35 S8:159-196 · D-36·D-48 S8:198-207 · :329-337 · D-37·D-50 S8:94 · :209-212 · D-41 S8:408 · D-42·D-43·D-45 S8:189-192 · :322-325 · D-44 S8:131-132 · D-47 S8:219-220 · :264
- **D-15 만 반대 방향(F-1)**. 과정 결정 D-01·D-02·D-05·D-38·D-40 은 「해당 없음」 처리가 맞다

### 원장 DEC-008 뒤 행

- 수신 방식 = Socket Mode · Pub/Sub pull · 공개 수신 주소 없음 → S8:379-385 · OQ-803 ✓ / web OAuth 클라이언트 새로 → S8:271 ✓ / 슬랙 OAuth https → **어긋남(W-9)**
- 보존 없음 · 25/50MB → S8:155-157 · :170-172 · :396-399 ✓ (DEC 미반영 W-16)
- mykakao 방식 · kakaocli 참고만 → S9:41-47 · :63 · :193-197 ✓ / OQ 추천안 801·802·803·804·808·901~905 → S8 §7 · S9 §7 ✓
- 비밀값 위치 `~/.config/google/env`·`~/.config/slack/env` · 운영 Secret → S8:418-430 ✓ (원장의 `oauth-web-client.json`·`pubsub-sa.json` 파일 중 SA 파일만 env 경로로 받음 — 운영 Secret 파일 마운트는 W-12)

## 제안 (판정과 별개 — 새 정책)

- **P-1** 카톡 수집기의 서버 인증을 웹 세션 쿠키 대신 「기기 등록 토큰」(설정에서 1회 발급 · 회원에 묶임 · 철회 가능)으로 두면 W-5(12시간 만료)·창 없는 백그라운드·D-45(사람당 Mac 한 대) 판정이 한 번에 풀린다. 정책이라 사용자 결정 몫
- **P-2** 연결 시작을 「서버가 state 를 박은 동의 URL 을 돌려준다」로 바꾸면(F-2) 웹·데스크톱 두 셸이 같은 흐름을 쓴다. 데스크톱은 기본 브라우저에서 동의하고, 웹 화면은 연동 목록을 다시 읽으면 된다
