# 4차 검수 리포트 — SPEC-008·009 v0.5.0 · SPEC-006 v0.6.0 + WORK-011 초안 (2026-10-06)

## 총평: 조건부 PASS — 구현 발주해도 된다

FAIL 은 없다. r3 의 **R3-F1 · R3-F2 는 본문에서 닫혔다**. 원장 `_RESUME.md:78` 과도 맞는다.
- 닫기 = 웹뷰를 실제로 파괴하고 프로세스만 상주한다
- 기기 토큰 범위 = 수집 라우트 + 고른 방 조회만
- 해시로만 보관한다
- 비밀번호 변경·새 발급 때 철회한다
- 카톡 중복 키에 연동 범위가 들어갔다

WARN 9 도 8건 해소, 1건 부분 해소다.

남은 것은 **발주하며 고칠 WARN** 이다. 그중 **발주 문서에 바로 반영해야 할 것 넷**(★)이 있다.
- 둘은 SPEC 계약의 작은 빈칸이다(★1 handshake 에 chatId 없음 · ★2 reset-account 인증 모순)
- 둘은 WORK-011 의 실행 구멍이다(★3 슬랙 Phase 완료 조건을 로컬에서 잴 수 없음 · ★4 운영 반영 순서에 스키마·hostPath 선행 단계 없음)

★3·★4 는 해당 Phase 시작 전까지만 고치면 된다. ★1 은 SHELL 착수 전, ★2 는 BE-3 착수 전까지다. 그래서 **BE-1 은 지금 발주해도 된다.**

> 약칭 S8·S9·S6 = `para/projects/summer-star/strong-hajin/20-spec/spec-00{8,9,6}-…md` · WP = `…/30-work/work-011-external-channels.md` · FIX3 = `orchestration/work/strong-hajin-inbox/review-spec-008-009-fix3.md` · RES = `…/_RESUME.md` · CODE = `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-inbox`(origin/main `202078b`)

## 검수 범위

- S8(719줄)·S9(321줄) 중 이번에 바뀐 절 전부(§4 머리 · §4.1 · §4.2 기기 토큰 · §4.6 · §4.7 비밀번호 · Case Matrix · AC-12·14c·20·21 / S9 머리 · §2.1 · §3.2 · §4 인증) · S6 「외부 채널 수집기 수용」 절 v0.6.0 전부 · WP 전부(255줄)
- FIX3 의 행마다 본문 반영을 확인했다. 원장 `RES:76-78` 과 대조했다
- 코드 대조: `backend/tests/architecture/test_operation_inventory.py:131`(HTTP 인벤토리 시험) · `Makefile` local-stack · runbook-002 스키마 절차 유무(grep 결과 없음)
- 테스트·빌드는 돌리지 않았다

---

## 1. r3 FAIL·WARN — 해소 여부

| # | 판정 | 근거 |
|---|---|---|
| **R3-F1** 기기 토큰 계약 | **해소** | S8:300-304(인증 두 갈래 · 토큰은 웹 라우트 거절 · 세션은 수집기 라우트 거절) · S8:333-339(Bearer · 해시만 · 범위 · 새 발급이 옛 것 철회 · `kakao_store_device_token` · 비번 변경·비활성 무효) · S8:438 · AC-14c·20 · S6 커맨드 표 · S9:145-147·:209-217 |
| **R3-F2** 닫기 vs 녹음 | **해소** | S6 수용 절 닫기 행(「웹뷰 실제 파괴 · 프로세스만 상주 · L-06·S-6·`E-12`·AC-T32 무변경」) · 「그대로인 것」 · OQ-T10 · S9:139-141 · AC-06b · RES:78 과 일치 |
| W3-1 커맨드 수 | 해소 | S6 I-2 행 · AC-T23/T47 행 · 카톡 커맨드 표(정확히 셋) — WP:182 에 옛 문장 남음(아래 W4-8) |
| W3-2 키·aid 범위 | **부분** | S8:405·:411(`(연동, chatId, logId)` · `aid = SHA-256("{integration_id}:{chatId}:{logId}:{seq}")`) · WP:249. 남은 것: S9:202 가 아직 `(chatId,logId)` · WP:149 가 옛 식 · 요청에 chatId 가 없다 → ★1 |
| W3-3 선택 변경 감지 | 해소 | S8:413(`200 {selected_rooms_version}`) · :410 |
| W3-4 DEC D-15 | 해소(FIX3) | 판정 밖이라 본문 확인은 생략 |
| W3-5 사람당 Mac 한 대 | 해소 | S8:333 |
| W3-6 iframe | 해소 | S8:177 근처(부모가 `contentDocument.scrollHeight` · 부모가 클릭 가로채기) |
| W3-7 옛 문장 | **대부분** | S9 머리 정정 · Case Matrix 매니페스트 정정. 남음: S8:458 Case Matrix 「슬랙/Gmail 상류 429·5xx → 502 + 다시 보내기」(답장은 실시간 사건 · S8:368) · S9:202 |
| W3-8 빌드 배선 | 해소(S6) | S6 「판 가르기 수단 · 빌드 배선」 — WP 에는 안 옮겨짐(W4-6) |
| W3-9 room_id | 해소 | S8:312 |

---

## 2. SPEC — 새 WARN

| # | 항목 | 근거 파일:줄 | 내용 | 고칠 것 (한 줄) |
|---|---|---|---|---|
| ★1 | **handshake 가 chatId 를 주지 않는다** | S8:410(`selected_rooms:[{room_id, last_logId}]`) · S8:411(업로드 요청은 서버 내부 `room_id`) · S8:312(`room_id` = 서버 내부 id) · S9:187·:201 | 앱은 로컬 카톡 DB 의 **chatId** 로 방을 찾는다. 그런데 서버가 주는 것은 내부 `room_id` 뿐이다. 그래서 **「서버의 고른 방 X = 로컬의 어느 방인가」를 앱이 알 수 없다.** 반대로 `aid` 식에도 chatId 가 들어간다 | `selected_rooms:[{room_id, external_id(=chatId), last_logId}]` 한 칸. SHELL 착수 전에 |
| ★2 | **`reset-account` 를 누가 부르나 — 인증 모순** | S8:302-303(「**세션은 수집기 라우트에서 받지 않는다**」) · S8:403-404(§4.6 「아래 라우트」 = 기기 토큰 전용) ↔ S8:414(`reset-account` 는 사람이 「다시 연결」을 눌러 부른다 — §2.5 설정 화면 · 세션) · WP:149(BE-3 이 기기 토큰 라우트로 묶음) | 웹 설정 단추가 부르는 라우트를 기기 토큰 전용 절에 넣었다. 문자대로 짜면 **웹에서 「다시 연결」이 401** 이 된다 | `reset-account` 를 **웹 라우트(세션)** 로 옮겨 §4.3 쪽에 둔다. 앱은 지금처럼 handshake 의 `reset_at` 으로 안다. BE-3 착수 전에 |
| W4-1 | 「카톡 고른 방 조회」가 어느 경로인가 | S8:302 · S8:333(기기 토큰 범위 = 「§4.6 + **카톡 고른 방 조회**」) | §4.6 의 handshake 가 이미 고른 방을 준다. `GET /api/integrations/{id}/rooms`(웹)까지 기기 토큰을 받는다는 뜻으로도 읽힌다 — 범위가 한 경로만큼 모호하다 | 「= handshake(§4.6)」로 못박는다 |
| W4-2 | 옛 문장 셋 | S8:458(Case Matrix 502 + 다시 보내기) · S9:202(`(chatId,logId)`) · S8:136 §1 표(`Depends(current_principal)` 만 — 두 갈래 인증 없음) | 구현자가 표를 보고 짠다 | 본문대로 고친다 |

## 3. WORK-011 — Phase·배치·겹침·완료 조건·누락·운영

### 3.1 Phase 순서·워커 배치·파일 겹침

| # | 판정 | 근거 | 내용 | 고칠 것 |
|---|---|---|---|---|
| W4-3 | **BE-2 ∥ BE-3 「파일이 안 겹친다」 주장이 약하다** | WP:99-100 · WP:115(BE-1 스키마 목록) · WP:129 · WP:142 | ① BE-1 스키마 목록에 **동기화 상태가 없다** — Gmail `historyId`·watch 만료, 슬랙 방별 마지막 `ts`·team id, 백필 진행 건수, 「마지막 반영 지점」. BE-2 가 이것을 만들려면 `persistence.py` 를 다시 연다. BE-3 도 같은 파일을 연다 → **겹친다** ② 두 Phase 모두 「서비스 모듈」(`modules/external_channels/`)을 쓴다 ③ **`LISTEN/NOTIFY` 채널 이름·페이로드**는 BE-2(보냄)·BE-3(받음) 사이 계약인데 정하는 자리가 없다 | BE-1 계약에 「동기화 상태 칸 · NOTIFY 채널·페이로드 · 모듈 골격(도메인/애플리케이션 파일 분할 — BE-2 는 `sync_*.py`, BE-3 은 `inbox_*.py` 처럼)」을 더한다. 그러면 나란히 가는 주장이 성립한다 |
| W4-4 | FE-b 의 카톡 방 추가는 SHELL 에 기대는데 순서가 없다 | WP:169(FE-b 가 `kakao_list_rooms` 로 목록) · WP:180-182(커맨드는 SHELL 이 만든다) · WP:103-104 | FE-b 는 SHELL 의 커맨드 바인딩(`lib/shell.ts`) 없이 그 부분을 끝낼 수 없다. 「FE-a ∥ FE-b ∥ SHELL」 셋이 `App.tsx`·`lib/shell.ts` 를 겹쳐 쓴다(I-4)는 적었지만, **의존**은 적지 않았다 | 「FE-b 카톡 방 추가·『이 Mac 연결』은 SHELL 의 `lib/shell.ts` 바인딩 뒤」 한 줄 · 또는 SHELL 이 바인딩 타입 시그니처를 먼저 커밋 |
| W4-5 | **카톡 DB 모듈 위험을 맨 뒤에 둔다** | WP:175-190(SHELL 은 FE 와 나란히 가지만 시작 조건이 「SPEC-006 검수 뒤」뿐) · WP:240(I-1) · RES:21(writer 가 같은 지점에서 안전 분류기에 막힘) | 기능 하나가 통째로 걸린 가장 불확실한 모듈인데, 막혔을 때의 **대안·범위 축소 경로**가 「코디에게」뿐이다. 늦게 터지면 BE·FE 가 다 끝난 뒤 카톡만 빈다 | **SHELL-0 탐침**을 BE-1 과 동시에 둔다: mykakao 방식 그대로 Rust 로 키 유도·userId·읽기 전용 열기·방 목록 1회. 완료 조건 = 방 목록이 나온다. 실패하면 그때 범위 결정(카톡만 뒤로)을 코디가 한다 |

### 3.2 완료 조건 — 실물로 잴 수 있나

| # | 판정 | 근거 | 내용 | 고칠 것 |
|---|---|---|---|---|
| ★3 | **BE-2·BE-3 의 슬랙 완료 조건을 로컬에서 잴 수 없다** | WP:135(「슬랙 실제 워크스페이스에서 메시지 1건 수신→저장→팬아웃」) · WP:150(「슬랙 답장+파일 실제 전송 1회」) ↔ S8:329-330 · RES:69(**슬랙 OAuth 는 https 필요 → 운영에서만**) | 슬랙 연동 레코드는 OAuth 콜백으로만 생긴다. 그 콜백은 운영에서만 된다. 그러면 BE-2·BE-3 은 **배포 전에는 슬랙 사용자 토큰을 가질 수 없어** 완료 조건을 못 잰다. Socket Mode 자체는 로컬에서 붙는다 | 둘 중 하나를 WP 에 적는다. (a) **개발 전용 이음새** — 사용자가 실측 때 받은 사용자 토큰(`~/.config/slack/env`)을 로컬 연동 레코드로 넣는 `make` 타겟(운영 프로파일에서는 거절, `X-Demo-Persona` 와 같은 결) (b) 슬랙 완료 조건을 「반영」 Phase(운영)로 옮기고 로컬은 녹화한 이벤트 픽스처로 잰다 |
| W4-6 | SHELL 완료 조건에 판 가르기 검증이 없다 | WP:181 · WP:190 ↔ S6 「빌드 배선」(`shell-build`/`tauri-local` 이 medi-ax 에 `--features kakao-collector` · `shell-final-preflight` 가 개인판에 수집기 심볼 없음 확인) | WP 시험은 `cargo check/test/clippy` 뿐이다. 개인판에 수집기가 안 들어갔는지를 잴 자리가 없다 | SHELL 계약에 「Makefile `SHELL_FLAVOR=medi-ax` → `--features kakao-collector` · `make shell-final-preflight` 가 개인판 통과」를 넣는다 |
| — | 나머지 완료 조건 | WP:122 · :162 · :172 · :189 · :200 | BE-1(Gmail 로컬 왕복 — 사용자 콘솔 설정 완료 RES:74 · 로컬 redirect 등록됨) · FE·SHELL(코디 macOS) · INFRA(50MB 통과) 는 **잴 수 있다** | — |

### 3.3 SPEC 계약 → Phase — 빠진 것

| # | 빠진 계약 | SPEC 근거 | 어느 Phase 에 |
|---|---|---|---|
| W4-7 | 비밀번호 변경 때 **기기 토큰도 철회** · 회원 비활성 때 무효 | S8:339 · :438 · AC-20 ↔ WP:148(세션만) | BE-3 |
| W4-7 | 「이 Mac 연결」 단추 · **기기 토큰 목록·철회 화면** | S8:334 · :338 · AC-21(「설정에서 철회」) ↔ WP:169(FE-b 에 없음) · WP:186(SHELL 은 store 만) | FE-b(+SHELL 바인딩) |
| W4-7 | `selected_rooms_version` **만들기**(웹에서 방 바뀔 때 올림) | S8:413 ↔ WP:149(status 에 버전 없음 · 소비는 SHELL WP:186) | BE-3 |
| W4-7 | 카톡 **첫 handshake 가 연동 생성** | S8:410 | BE-3(WP:149 에 없음) |
| W4-7 | local-stack 이 `AX_WEB_ORIGIN=http://127.0.0.1:5176` 을 넘김 | S8:328 | BE-1 Makefile(WP:120 에 없음) |
| W4-7 | **HTTP 운영 인벤토리 갱신** — 새 라우트 수십 개가 `docs/unified-operations-inventory.json` 에 없으면 `make verify` 가 깨진다 | CODE `backend/tests/architecture/test_operation_inventory.py:131`(`test_inventory_includes_each_declared_http_operation`) · AGENTS.md(「MCP 도구·HTTP 시그니처를 바꿨다면 … drift 를 잡아낸다」) | BE-1·BE-3 시험 줄 |
| W4-7 | iframe 높이·링크 가로채기 · 아바타를 `GET /api/profile/image` 로 그리기(SideNav) | S8:177 · AC-18b | FE-a · FE-b |
| W4-8 | WP 안 옛 문장 | WP:58-59(SPEC 판 v0.4.0 · 「숨김 공존」) · WP:112(「v0.4.0 검수 통과(3차)」) · WP:147(「상류 429/5xx=502」) · WP:149(`aid=(chatId,logId,seq)` — 연동 빠짐) · WP:182(「…류 · 넷을 넘음」) | Meta·BE-3·SHELL 줄을 S8 v0.5.0·S6 v0.6.0 대로 |

### 3.4 운영 반영·롤백

| # | 판정 | 근거 | 내용 | 고칠 것 |
|---|---|---|---|---|
| ★4 | **반영 순서에 선행 단계 둘이 없다** | WP:203-208 · WP:196-200 / runbook-002:160-164(hostPath 가 `Directory` 라 **없으면 back·워커가 안 뜬다**) · S8 §1 표(운영 스키마 = `backend/migrations/manual/*.sql` 별도 gate — runbook-002 에 스키마 절차가 없다, grep 0) | ① 새 hostPath 디렉터리를 노드에 **먼저** `mkdir` 하지 않고 차트를 sync 하면 **back 전체가 `ContainerCreating` 에 멈춘다** — 메시지함만이 아니라 서비스 전체가 멈춘다 ② 새 표를 만드는 manual SQL 을 **이미지보다 먼저** 운영 DB 에 넣는 단계가 없다 | 「반영」 Phase 를 순서 목록으로: ① 노드 `mkdir` ② manual SQL(+`.concurrent.sql`) 적용 ③ Secret patch(SA 키 파일 포함) ④ 차트 PR(hostPath·워커·ingress) ⑤ 이미지 태그 → Argo sync ⑥ dmg. 롤백도 그 역순(이미지만 · SQL 은 additive 라 남김) |
| W4-9 | 롤백 때 외부 쪽 잔여 | WP:222-228 | 이미지를 되돌려도 Gmail `users.watch` 가 최대 7일 Pub/Sub 에 계속 쌓이고, 슬랙 앱은 Socket Mode 가 끊긴 채 남는다. 해롭지는 않지만 다시 올릴 때 pull 구독에 쌓인 메시지를 어떻게 다루나(버림/재처리)가 없다 | 롤백 절에 한 줄: 「재반영 시 pull 구독 잔여는 history 메우기가 흡수(중복 키로 버림)」 |
| — | 롤백 기본 | WP:224-228 | 이미지 레벨·additive 스키마·워커 replicas 0·기기 토큰 철회·직전 dmg — **적절하다** | — |

---

## 4. 항목별 판정 (브리프 축)

| 축 | 판정 | 요지 |
|---|---|---|
| SPEC — r3 해소 | **PASS** | R3-F1·R3-F2 해소 · WARN 9 중 8 해소 |
| SPEC — 새 어긋남 | **WARN** | ★1(chatId) · ★2(reset-account 인증) · W4-1·W4-2 |
| WP — Phase 순서·배치 | **WARN** | W4-3(BE-2∥BE-3 겹침 조건) · W4-4(FE-b→SHELL 의존) · W4-5(카톡 DB 위험을 앞으로) |
| WP — 겹침 주장 | **WARN** | FE·SHELL 은 「코디가 조각 순서」로 처리돼 있음. BE 쪽은 W4-3 조건부로 성립 |
| WP — 완료 조건 측정 | **WARN** | ★3(슬랙 로컬 측정 불가) · W4-6 |
| WP — 계약 누락 | **WARN** | W4-7 일곱 항목(특히 운영 인벤토리 시험 · 기기 토큰 철회·UI) |
| WP — 운영 반영·롤백 | **WARN** | ★4(hostPath·SQL 선행) · W4-9 |
| WP — 카톡 DB 모듈 위험 | **WARN** | I-1 로 이름은 붙었다. 앞으로 당기는 탐침이 없다(W4-5) |

## 5. 발주하며 고칠 WARN 목록 (조건부 PASS 의 조건)

| 우선 | 무엇 | 언제까지 |
|---|---|---|
| ★1 | S8 handshake `selected_rooms` 에 `external_id`(chatId) | SHELL 착수 전 |
| ★2 | `reset-account` 를 웹 라우트(세션)로 | BE-3 착수 전 |
| ★3 | 슬랙 로컬 측정 경로(개발 전용 토큰 주입 타겟 또는 운영으로 이관) | BE-2 착수 전 |
| ★4 | 반영 순서 ①mkdir ②manual SQL ③Secret ④차트 ⑤이미지 ⑥dmg | 반영 Phase 전 |
| 1 | W4-3 BE-1 에 동기화 상태 칸·NOTIFY 계약·모듈 파일 분할 | BE-1 발주문에 |
| 2 | W4-7 운영 인벤토리 json 갱신을 BE-1·BE-3 시험에 | BE-1 발주문에 |
| 3 | W4-5 SHELL-0 카톡 DB 탐침을 BE-1 과 동시 | 지금 |
| 4 | W4-7 나머지(토큰 철회·UI·버전·첫 handshake·`AX_WEB_ORIGIN`·iframe·아바타) | 해당 Phase 발주문에 |
| 5 | W4-4 · W4-6 · W4-8 · W4-9 · W4-1 · W4-2 | 해당 Phase 발주문에 |

## 기존 부채 (판정 제외)

- 인프라 레포 쓰기 범위 밖(I-3) · 운영 `worker.kinds: []` — r1 부터 그대로

## 제안 (판정과 별개)

- **P-6** ★3 의 (a) 개발 전용 토큰 주입은 「실측 시험 스크립트로 이미 받은 사용자 토큰」(RES:45 행 근거)을 재사용하므로 새 동의가 필요 없다. 운영 프로파일에서 거절하는 시험을 하나 붙이면 `X-Demo-Persona` 와 같은 수준의 이음새가 된다
