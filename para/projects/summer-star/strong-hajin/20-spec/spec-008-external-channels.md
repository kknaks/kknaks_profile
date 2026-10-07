---
type: spec
id: SPEC-008
title: "외부 채널 연동 · 메시지함 · 프로필 설정 — 메일·슬랙은 실시간으로 쌓고 답장까지, 카톡은 Mac 앱이 올린다"
status: draft
product: strong-hajin
version: 0.5.1
created_at: 2026-10-06
updated_at: 2026-10-06
tags:
  - product/strong-hajin
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-006-external-channels|BASE-006]]"
  decisions:
    - "[[decision-008-external-channels|DEC-008]]"
    - "[[decision-007-production-deploy|DEC-007]]"
  specs:
    - "[[spec-009-mac-kakao-collector|SPEC-009]]"
    - "[[spec-001-work-management|SPEC-001]]"
    - "[[spec-006-tauri-wrapper|SPEC-006]]"
  works: []
  releases: []
  related: []
---

# 외부 채널 연동 · 메시지함 · 프로필 설정 — 메일·슬랙은 실시간으로 쌓고 답장까지, 카톡은 Mac 앱이 올린다

> **⚠ v0.2.0 (2026-10-06 · 사용자 — OQ 처리)** — 미결 여덟을 사용자 결정으로 닫았다(§7). 본문에 반영한
> 것: 토큰 암호화 = env 대칭키 하나(§5 env · §4 Data) · 슬랙 Socket Mode = **연동 전용 워커 새로**(§5 동기화) ·
> **보존·파기 없음 — 회사 데이터라 계속 보관**(D-49 를 대체 · §2.3·§5 저장) · 첨부 한도 = **메일 보내기 25MB ·
> 그 밖 50MB**(§2.2·§4 Validation) · 슬랙 메시지 사본은 **사람마다 복제**(§5 권한) · **비밀값 위치·이름 규칙**
> 한 절을 더하고 내부 env 를 `AX_` 접두어로 바꿨다(§5 비밀값). 계약 문서라 바뀐 문장은 **이 판으로 덮고**
> (취소선을 남기지 않는다), 무엇이 왜 바뀌었는지는 §7 Open Questions 의 처분과 이 머리 주석이 센다.
>
> **⚠ v0.3.0 (2026-10-06 · 검수 FAIL 4·WARN 17 반영 — `review-spec-008-009.md`)** — 고친 자리:
> **F-1** 카톡 방 목록·선택은 **Mac 이 정본**, 서버는 웹 고르기 창용 **중계만**(§4.3·§4.6) · **F-2** 연결 시작을
> **서버가 회원에 묶은 일회용 `state` 동의 URL 을 JSON 으로** 돌려주고 데스크톱은 `open_external`, 콜백은 쿠키가
> 아니라 `state` 로 회원을 찾는다(§4.2) · **F-3** HTML 메일 **소독·샌드박스 iframe·CSP·원격 이미지 차단** 계약(§2.1)
> · **F-4** §4.3·4.4·4.6 에 **요청/응답/오류** 세 칸 · WARN 열일곱(슬랙 팬아웃·카톡 방상태·heartbeat·계정 바뀜·
> 인증 수명·한도 단위·pod 배치·local-stack·캐릭터 둘째 진입점·프로필 API 재사용 등)은 §5·§7·각 절에 반영.
> **SPEC-006 개정은 그 문서 v0.4.0 이 받는다.** 앞 판 표기는 이 판으로 덮고(취소선 없음) 바뀐 자리는 각 절의
> `(F-n·W-n)` 꼬리표와 `review-spec-008-009-fix.md` 가 센다.
>
> **⚠ v0.4.0 (2026-10-06 · 재검수 R-F1·R-F2·새 WARN 12 + 사용자 결정·정정 — `review-spec-008-009-r2.md`)** —
> **카톡 방 «목록 탐색»은 데스크톱 앱(Rust)이 로컬에서**(앱 웹뷰 Tauri 커맨드), **고른 방(선택)은 서버가
> 저장·정본**이다(사용자 정정 2026-10-06 · `POST …/rooms` · handshake 가 내려줌). 그래서 **고른 방 목록·빼기는
> 브라우저에서도** 보이고 되고, 업로드 403 은 **서버 고른 방 기준**이다(매니페스트·`rooms/report`·카톡
> `available-rooms` 걷음). **D-15 는 「방 «목록»이 로컬」로 좁혀 읽는다.** **수집기 인증 = 장수명 기기 토큰**
> (OQ-906 닫힘 — 창 쿠키 아님 · 창 닫아도 수집). 「Mac 앱 받기」 = Strong_hajin GitHub Releases(OQ-811 닫힘).
> 그 밖 새 WARN 12(메일 409 없음·콜백 쿼리 목적지·샌드박스 토큰·이미지 프록시 SSRF·실시간 WS 신설·방 목록 API·
> aid 결정식·딥링크·문구)는 §2·§4·§5·§7 에 반영. **SPEC-006 은 v0.5.0**(닫기=숨기기·점유 해제·카톡 커맨드 노출)이 받는다.
>
> **⚠ v0.5.1 (2026-10-06 · 4차 검수 ★1·★2·W4-1·W4-2 — `review-spec-work-r4.md`)** — handshake `selected_rooms`
> 에 **`external_id`(=chatId)** 추가(서버 room_id ↔ 로컬 chatId 잇기 · ★1) · **`reset-account` 를 웹 세션 라우트**로
> 옮김(§4.3 · ★2 — 기기 토큰 절에 있어 웹 「다시 연결」이 401 나던 모순) · 기기 토큰 범위 = **§4.6 라우트만**(고른 방
> 조회는 handshake 겸함 · W4-1) · §1 표·Case Matrix 옛 문장 정정(W4-2).

> **⚠ v0.5.0 (2026-10-06 · 3차 검수 R3-F1·R3-F2 + WARN 9 — `review-spec-008-009-r3.md`)** —
> **R3-F1** 기기 토큰 계약 완성: **`Authorization: Bearer` · 서버는 해시만 보관 · 범위 = §4.6 수집기 라우트 + 고른 방
> 조회 «만»**(웹 라우트·`current_principal` 은 기기 토큰을 받지 않음) · 발급은 세션 있는 웹 · **새 발급은 옛 토큰 철회**
> (D-45) · 비밀번호 변경·회원 비활성 때 함께 무효(§4.2·§4.7·§5) · **R3-F2** 닫기 의미를 「숨기기」에서 **「웹뷰 실제
> 파괴 · 프로세스만 메뉴 막대 상주」**로 바꿔 L-06·S-6·AC-T32 무변경(SPEC-006 v0.6.0) · W3-2 카톡 키·aid 에 **연동
> 범위**(`(연동,chatId,logId)` · `aid`=SHA-256) · W3-3 status 응답에 **고른 방 버전** · W3-6 iframe 높이=부모가
> `contentDocument` 로·링크=부모 가로채기 · W3-7 옛 문장 정리 · W3-9 `room_id`=서버 내부 id. **SPEC-006 은 v0.6.0.**

흩어진 메일·슬랙·카카오톡 대화를 **내 메시지함**으로 가져오는 계약이다. DEC-008(accepted · D-01~D-50)이
정한 **1단계** — 연동 · 수집 · 조회 · 읽음 · 답장 — 의 서버와 웹을 센다. 카톡을 읽어 올리는 **Mac 앱**은
SPEC-009 이고, 두 SPEC 사이의 업로드·상태 계약은 **이 문서 §4 가 정본**이다.

> **초안이다.** 검수 전이며 `status: draft`.
>
> **정책은 DEC-008 이 정본이다.** 이 SPEC 은 그 결정을 **지금 코드 구조 위**에 계약으로 옮긴다 —
> 새 정책을 만들지 않는다. DEC-008 에 답이 없는데 계약에 필요한 것은 **§7 미결(OQ-8xx)** 로 남긴다.
> **시안은 UX 정본**이고 화면·상태는 `design-change-1~6.md` 로 근거를 단다.
>
> **스키마 전문·테이블/컬럼·ORM·마이그레이션 전문은 쓰지 않는다**(`20-spec/README.md` Data/Domain Boundary).
> 드러나는 것 — 리소스·상태값·enum·API 계약·acceptance — 만 둔다. 저장 구조 초안은 `30-work/` 몫이다.

---

## 1. Context

### Meta

| 항목 | 값 |
|---|---|
| Decision | DEC-008 (accepted) |
| Baseline | BASE-006 |
| 코드(읽기만) | `/Users/kknaks/git/toy_pr2/Strong_hajin` origin/main `202078b` |
| 운영 origin | `https://ax.medisolveai.xyz` (DEC-007 D-03 · 같은 origin 하나 — front·`/api`·WebSocket) |
| 짝 SPEC | SPEC-009(Mac 카톡 수집기) · SPEC-006(데스크톱 래퍼) |

**경로 규약.** 코드 경로는 저장소 루트 기준(`backend/src/ax_workspace/…` · `frontend/src/…`). 문서 경로는
`para/projects/summer-star/strong-hajin/` 을 생략. 시안 로컬 사본은 `reference/2026-09-10-sc-meeting/package 2/`
이하 `P2/`. 변경 기록은 `orchestration/work/strong-hajin-inbox/design-change-n.md` 이하 `DC-n`.

### Business Requirement

메일·슬랙은 **사용자 1회 연결**로 받은편지함·고른 방이 **실시간**으로 메시지함에 쌓이고, 메시지함에서
**읽고 답장**한다(D-04·D-09·D-22·D-32). 카톡은 **Mac 앱이 로컬에서 읽어 서버로 올린** 것을 **조회만** 한다
(D-14·D-17 · SPEC-009). 연동·방·메시지는 **연결한 사람 소유**이고 **본인만** 본다(D-24·D-25). 설정의 계정
메뉴는 **프로필 설정**으로 바뀐다 — 이미지·AX 캐릭터·비밀번호 변경(D-36).

### Scope

**In Scope**

- 연동 데이터의 소유·상태·소프트 딜리트, 고른 방, 원문 메시지, 첨부 메타, 읽음, 보낸 답장 기록, 프로필 이미지
- 연결 흐름 — Gmail OAuth(readonly+send) · 슬랙 OAuth(사용자 토큰) · 리디렉션 경로
- 동기화 — 슬랙 Socket Mode · Gmail watch+Pub/Sub · 최초 백필 · 재시작 메우기
- 메시지함 API — 목록(출처·미읽음) · 본문 · 읽음/모두 읽음 · 첨부 받기(중계/저장본)
- 답장 — 슬랙(채널·스레드·첨부) · 메일(답장/전체 답장·첨부 25MB)
- 설정 API — 연동 목록·연결·해제·재연결 · 방 고르기 목록 · 상태 · 실패 배너
- 카톡 수신 쪽 — Mac 앱 → 서버 업로드·상태 계약(§4) · 첨부 저장(hostPath)
- 프로필 설정 — 이미지 즉시 저장 · AX 캐릭터 이동 · 비밀번호 변경 API 신설
- 메시지함을 여는 **내비 항목 하나**(메시지함) — 기존 「업무 > 수신함」과 **별개**(D-06)

**Out of Scope** — DEC-008 「하지 않는 것」·「다음 단계로 미룬 것」 전부. 특히:

- **2단계 AX 판단**(도착 이벤트 → 생성/업데이트/패스 → 업무 > 수신함) — D-03·D-39. 이벤트 단위 미정
- **카톡 발송** — D-17. 조회만
- **설정 알림 메뉴** — D-37. 수집 실패는 §2 배너로만 보이고 알림 설정 화면은 손대지 않는다
- 「업무 > 수신함」의 계약 변경 — SPEC-001 U-12 · DEC-001 그대로
- 메시지함 카드의 업무 행동(`업무`/`참고`·`+`·`내 업무로`·`확인완료`) — D-07
- 저장 구조·테이블·마이그레이션·수집 구현 방식(사이드카/포팅) — `30-work/` 몫

### 이 SPEC 과 기존 코드의 관계 (근거 파일:줄)

| 무엇 | 지금 코드 | 이 SPEC 이 더하는 것 |
|---|---|---|
| 인증 경계 | 세션 쿠키 `scax_session`(opaque) → 로그인 세션 스토어가 member 로 해석. 「Google OIDC 가 같은 로그인 라우트·세션 스토어에 붙어도 인가를 건드리지 않는다」 | **연동 토큰은 인증과 별개** — OAuth 는 외부 채널 읽기·쓰기 권한일 뿐 로그인이 아니다. 세션은 그대로 쓴다 (`backend/src/ax_workspace/entrypoints/http_auth.py:1-19`·`:38-77`) |
| 로그인 세션 | `SqlAlchemyAuthSessionStore` · `AuthSessionRecord`(id·member_id·provider·created_at·expires_at·revoked_at) | 건드리지 않는다 (`backend/src/ax_workspace/platform/auth_sessions.py` · `platform/persistence.py:1993`) |
| 비밀번호 | PBKDF2-SHA256 `hash_password`/`verify_password` · `MINIMUM_PASSWORD_LENGTH=8` · `MemberCredentialRecord`(member_id·email·password_hash) | **비밀번호 변경 API 신설**(§2.7·§4). 저장·검증 코드를 재사용 (`backend/src/ax_workspace/modules/organization_access/credentials.py` · `platform/persistence.py:92`) |
| 명부 | `MemberRecord`(display_name·employment_* 등) · organization_access | 이름·직무는 **읽기 전용**으로 비춘다. 여기서 안 고친다 (`backend/src/ax_workspace/platform/persistence.py:59`) |
| AX 캐릭터 | `PUT /api/profile/preferences/assistant-character`(`expected_version`) · `AssistantCharacterPreferenceRecord` · 409 conflict · 422 unsupported | API 를 **재사용**하고 **진입점만** 프로필 설정으로 옮긴다(D-48 · §2.6). 프론트의 기존 모달 진입점 **둘** 제거(설정 `:417`·신원 줄 `:402-405`, W-14) (`backend/src/ax_workspace/entrypoints/http.py:679` · `frontend/src/App.tsx:402-405`·`:417`·`:606`) |
| 첨부 저장 | `LocalDirectoryMaterialStorage(Path(settings.materials_dir))` · `put(key,data,content_type)` · env `AX_MATERIALS_DIR`(기본 `.scax/materials`) | **같은 방식**으로 카톡 첨부·프로필 이미지를 hostPath 에 둔다(§5 저장). 회의 자료가 쓰는 그 저장소 계열 (`backend/src/ax_workspace/platform/materials.py:26`·`:31` · `bootstrap/application.py:948`) |
| 자료 업로드 본보기 | `POST /api/meetings/{id}/materials` — `UploadFile` 여럿 · 되는 것만 붙고 안 되는 것은 사유와 함께 · `/content` 는 Content-Disposition | 메시지함 첨부 받기·답장 첨부·카톡 업로드가 이 틀을 따른다 (`backend/src/ax_workspace/entrypoints/http.py:1066`·`:1105`) |
| 라우트 | `create_app` 하나에 `@app.<verb>("/api/…")` · `Depends(developer_principal)`(=`current_principal`) | 새 라우트를 같은 자리에 더한다. **인증은 두 갈래**(§4 머리 · W4-2) — 웹 라우트는 `current_principal`(세션), **§4.6 수집기 라우트는 기기 토큰 `Authorization: Bearer`**(세션 거절). 모듈은 `modules/external_channels`(신규) 제안 (`backend/src/ax_workspace/entrypoints/http.py:609`) |
| 워커 | `entrypoints/{conversation,material,meeting,report}_worker.py` · 각 `Worker(Settings.from_environment())` · 신호 처리 · k8s `worker-*` 디플로이(back 과 같은 이미지) | **동기화 워커가 는다** — 슬랙 Socket Mode · Gmail Pub/Sub pull · 백필(§5 프로세스 배치) (`backend/src/ax_workspace/entrypoints/material_worker.py` · runbook-002:42·157) |
| 설정 로딩 | `Settings.from_environment()` · `os.getenv` | 새 env 를 같은 방식으로 읽는다(§5 env) (`backend/src/ax_workspace/bootstrap/settings.py:141`) |
| 스키마 변경 | 로컬은 `schema_sync`(additive), 운영은 **별도 gate** · `backend/migrations/manual/*.sql`(+인덱스 `.concurrent.sql`) | 새 표·인덱스는 **그 방식**을 따른다. 전문은 `30-work/` (`backend/src/ax_workspace/bootstrap/schema_sync.py:1-6` · `backend/migrations/manual/`) |
| 프론트 라우팅 | 라우터 없음 — `App.tsx` 의 `surface` 상태. `navigation` 배열에 id. 설정은 `utilityItems` 가 여는 모달 | **메시지함은 새 surface** · **설정은 새 surface**(모달 아님 — 시안이 전체 화면). `min-width:1542px`(`shell.css:70`)를 따른다 (`frontend/src/App.tsx:37-48`·`:395`·`:401`·`:417`) |
| 데스크톱 | SPEC-006 래퍼(커맨드 넷 · 파일 권한 없음) · 쿠키로 같은 origin 붙음 | 카톡 수집은 **SPEC-009**(Mac 앱)이 **회사판 medi-ax** 에서 맡는다. 래퍼 불변식 개정은 **SPEC-006 v0.6.0**(§5 데스크톱 경계) (`frontend/src-tauri/src/lib.rs:7-13`) |

---

## 2. UX Contract

시안이 UX 정본이다. 화면·상태는 아래 근거(DC-n)로 옮긴다. 셋 이상 상태(기본·빈·로딩·오류)는 시안이
그린 대로 그린다.

### Placement

- **메시지함** = 내비의 **독립 항목**. 시안 `P2/Inbox.html` · 라벨 「메시지함」(DC-1). 기존 「업무 > 수신함」
  (`frontend/src/shell/InboxRail.tsx`)과 **다른 화면**이다(D-06). 둘 다 「수신함/메시지함」이라는 이름을 갖되
  **합치지 않는다**
- **설정** = 메일 연동 · 슬랙 연동 · 카카오톡 연동 · **프로필 설정** · 알림 설정 메뉴. 이번에 손대는 것은
  앞 넷(알림은 그대로). 시안 `P2/Settings.html`(DC-2·4·6)
- 좁은 화면 대응은 하지 않는다 — 앱 공통 최소 폭 `.scax-app-shell{min-width:1542px}`(`frontend/src/styles/shell.css:70`)을
  따른다(D-44)

### 2.1 메시지함 — 레일 · 본문 (DC-1·5·6)

- **출처 전환** `전체 · 메일 · 슬랙 · 카톡`(SegmentedControl). 레일 숫자 = **미읽음 카드 수**
- **카드** — 모양은 시안 그대로, **행동은 읽음뿐**(D-07):
  - 메일 = **단건**. 출처 배지 `메일` · 안 읽음 점 · 제목 · 본문 두 줄 · 보낸 사람 · 시각 · 첨부 수
  - 슬랙·카톡 = **대화방 하나 = 카드 하나**(D-08). 배지(`슬랙`/`카카오톡`) · 미읽음 수 · 방 이름 · 마지막 3줄 · 「참여 N명 · 마지막 …」
  - 카드를 누르면 본문이 서고 **그 카드가 읽음**. 머리 `모두 읽음으로`
  - **없는 것**: `업무`/`참고` 배지 · `+` · `내 업무로` · `확인완료` · `대화 보기`(D-07)
- **본문은 폭 전체를 쓴다**(읽기 폭 제한 없음, D-34 · DC-5)
  - **메일 본문**: 머리 표(보낸 사람·받는 사람·참조·날짜·받은 계정) · HTML 메일 틀 · 인용 접기 · 첨부 카드.
    **HTML 메일 보안(F-3)**: 외부 누구나 보낸 HTML 을 **세션이 사는 같은 origin** 에 그리므로 — ① 서버가 저장
    원문을 **소독(sanitize)** 해 `<script>`·이벤트 속성(`on*`)·`<form>`·`<iframe>`·`<object>` 를 지운 뒤 보관본과
    별개로 **렌더용 안전본**을 만든다(원문은 그대로, D-28 — 가공은 렌더에서) · ② 본문은 **샌드박스 iframe**에
    담되 토큰은 **`sandbox="allow-same-origin allow-popups allow-popups-to-escape-sandbox"` · `allow-scripts` 금지**
    (N-4 — 스크립트가 없으니 `allow-same-origin` 은 안전하다) · CSP `default-src 'none'; img-src`(아래) 로 묶는다 ·
    ③ **원격 이미지는 기본 차단**(추적 픽셀), 「이미지 보기」를 누르면 **서버 프록시**(§4.4 `remote-image`)로만 ·
    ④ 인라인 `cid:` 이미지는 첨부 중계 경로(§4.4)로 · ⑤ **인용 접기는 소독 때 인용을 `<details>` 로 감싼다**(스크립트
    없이 동작 · N-4) · ⑥ **높이는 부모가** iframe 의 `contentDocument.scrollHeight` 로 직접 잰다(스크립트 없는 iframe 은
    postMessage 를 못 보냄 · `allow-same-origin` 이라 부모가 읽는다 · W3-6) · ⑦ **링크는 부모가 iframe 문서의 클릭을
    가로채** 웹이면 새 탭(`rel="noopener"`), 데스크톱이면 `open_external` 로 OS 브라우저에 넘긴다(iframe 안에서는
    `_blank`·커맨드가 안 통하고 macOS 셸이 `_blank` 를 막는다 · W3-6 · SPEC-006)
  - **슬랙 본문**: 진짜 슬랙 대화방처럼(D-33 · DC-1) — 날짜 구분선 · 아바타·이름·시각 · **같은 날·같은 사람·5분 안 묶음** · 서식(굵게·목록·멘션·링크·코드·이모지) · URL 미리보기 · 첨부(이미지·PDF·파일 카드) · 리액션(읽기 전용) · 봇 `앱` 표시 · 「새 메시지 N개」
  - **슬랙 스레드 = 오른쪽 패널**(3열 레일|대화|스레드, 패널 420px · DC-5). 한 번에 하나
  - **머리 「슬랙에서 열기」**(DC-1 §2.4) — 메시지의 **퍼머링크**로 OS 브라우저/슬랙 앱을 연다. 서버는 원문 JSON
    에서 퍼머링크를 함께 보관하거나(저장 시) 사용자 토큰으로 얻는다(UX-4 보강)
  - **카톡 본문**: 슬랙 대화방과 같은 모양 · **입력창·스레드·외부 열기 없음**(조회 전용, D-17) · 머리 「카카오톡 · 1:1/단체방 · 참여 N명 · 조회 전용 · Mac 앱에서 수집」
- **네 상태**(DC-1): 레일/본문 각각 기본 · 빈(「설정에서 메일·슬랙을 연결하면 …」) · 로딩(Skeleton) · 오류(「불러오지 못했습니다」+다시 시도) · 출처 필터로 빈 경우

### 2.2 메시지함 첨부 — 받기 (D-29·D-30·D-31)

- **메일·슬랙**: 파일 카드(이름·유형·크기·받기). 누르면 **그때 받아 넘긴다**(서버가 그 사용자 토큰으로 중계 ·
  저장하지 않음). 이미지는 썸네일 + 카드. 슬랙 URL 미리보기 정보는 저장돼 바로 그린다
- **카톡**: 사진·앨범·파일 = **저장본**(수집 순간 받아 둔 것)을 서버가 낸다. 동영상·음성 = **표시만**(받기 없음 ·
  「카카오톡에서 보기」) · 이모티콘 = 「(이모티콘)」 · 만료 = 점선 흐린 카드 · 이름 취소선 · 「만료됨」(받기 없음)
- **첨부 한도(v0.2.0)**: 카톡 수집 저장·슬랙 보내기 = **50MB** · 메일 보내기 = **25MB**(Gmail 자체 한도). 한도를 넘는
  카톡 첨부는 저장하지 않고 「**너무 큼 — 카톡에서 확인**」으로 보인다(D-31 의 동영상·음성 미저장과 같은 결) ·
  메일 25MB 초과는 §4 Validation 대로 보내기를 막는다(OQ-806·807 → 사용자 결정 2026-10-06)

### 2.3 설정 — 메일 연동 (DC-2)

- 연결 전: 「Google 계정 연결」 + 「한 번 연결하면 받은편지함이 실시간으로 쌓인다. 연결할 때 받은편지함 전체를
  가져온다.」 + **「Google로 연결」**
- 연결 후: 「연결된 메일 계정 N개」 · 적재 상태 3칸(`마지막 수집`·`DB 적재 건수`·**`수집: 실시간`**) · 계정 줄 ·
  **「다른 계정 연결」**(계정 여럿, D-10)
  - 계정 줄 상태: `실시간` / `과거 메일 채우는 중 · N건`(점 깜빡임) / **`연결 끊김 다시 연결`**(붉은 바탕 + 「토큰이
    만료됐거나 Google 에서 권한을 거둔 경우 — 「다시 연결」로 한 번 더 동의하면 이어 받는다」)
  - **「연결 해제」** + 확인 창(「{주소} 에서 더 이상 메일을 받지 않는다 · 이 계정으로 쌓인 메일은 메시지함에서
    사라진다」) — 소프트 딜리트(D-27), 다시 연결하면 되살림(D-46)
- IMAP 폼 · 「가져올 범위」 선택 · 비밀번호 · 「받아오기」 수동 단추는 **없다**(D-09·D-23)
- **보존·파기(v0.2.0)**: 수집한 원문·첨부는 **계속 보관한다 — 보존·파기 기간을 두지 않는다**(회사 데이터, 사용자
  결정 2026-10-06 이 D-49 의 「이번에 정하지 않는다」를 대체). **연결 해제·방 빼기는 소프트 딜리트뿐이고 물리 삭제가
  없다** — 화면에서만 사라지고 DB 에는 남아 재연결 때 되살아난다(D-46 · OQ-805 닫힘)

### 2.4 설정 — 슬랙 연동 (DC-2)

- 워크스페이스 카드 — 연결 전 「내 슬랙 계정으로 연결한다 … 고른 방만 가져온다」 + **「슬랙 연결」** / 연결 후
  「워크스페이스 · 도메인」·`연결됨`·`실시간`·**「연결 해제」** / 연결 끊김 `연결 끊김 다시 연결`
- 「수집 방 N개」 카드 — 적재 상태 3칸 · 방 줄(종류 표식 # 공개 · # 비공개 · @ DM · 그룹 DM · 이름 · 메타 ·
  적재 N건 · 상태 · **「빼기」**) · 머리 **「방 추가」**
- **방 고르기 창**(모달) — 검색 · 묶음 탭 `전체·채널·비공개·DM·그룹 DM` · 줄(체크·표식·이름·봇이면 `앱`·인원) ·
  이미 넣은 방은 「추가됨」 · **「선택한 N개 추가」** · 네 상태(기본·로딩·결과 없음·오류)
  - **그룹 DM 은 참여자 실명으로**(슬랙 내부 이름 `mpdm-…` 안 보임, D-12). 봇 DM 도 DM 묶음에 섞여 나옴(D-13)
- 봇 권한 문구 · 채널 이름 입력은 **없다**(D-11)

### 2.5 설정 — 카카오톡 연동 (DC-6)

- 소개 「이 Mac 의 카카오톡에서 고른 1:1·단체방의 대화를 우리 DB 로 적재한다. 조회만 한다 — 메시지함에서
  보내지는 않는다. Mac 에서만 된다.」
- **어디서 여느냐로 갈린다(R-F1 정정)**: **방 «추가」 창은 앱 웹뷰에서만** 뜬다(방 목록이 Mac 로컬이라 — Tauri
  커맨드). **브라우저**에서는 「방 추가는 Mac 앱에서」 안내만. 다만 **고른 방 목록·빼기는 서버 정본이라 웹에서도
  보이고 뺄 수 있다**(DELETE). 앱 웹뷰 판정은 **Tauri 커맨드가 있는지**(SPEC-006 노출)로 한다
- **수집 상태 카드** — 칸 넷(`데스크톱 앱`: 연결됨(기기 이름·버전)/꺼짐 · `카카오톡`: 실행 중/꺼짐/알 수 없음 ·
  `로그인 계정`: 이름 · `마지막 수집`) — 실을 정보는 **D-43**(기기 이름·앱 버전·마지막 연결·카톡 로그인 계정 이름).
  앱·카톡 꺼짐이면 적재 상태 「멈춤 — …」(붉은 점). 문구의 앱 이름은 **판 이름(medi-ax)**/중립 「데스크톱 앱」(N-12)
  - **카톡을 못 읽을 때(W-2)**: 사유에 따라 문구가 둘이다 — `permission`(전체 디스크 접근 없음) = **「전체 디스크
    접근을 켜 주세요」** · `version`/`unknown`(DB 못 엶) = **「카카오톡을 읽을 수 없습니다 — 카카오톡 버전이
    바뀌었을 수 있습니다」**(§4.6 status 의 `reason` 으로 고른다, D-42·OQ-905)
  - **계정이 바뀌었을 때(W-4)**: 상태 카드에 **「계정이 바뀌었습니다 — 다시 연결」** 줄 — 누르면 `reset-account`
    (§4.6). 옛 계정의 방·대화는 소프트 딜리트로 남는다(D-45·D-46)
- **앱 없음**: 상태 카드 대신 「Mac 앱을 설치하고 켜 두면 카톡이 쌓입니다」 + **「Mac 앱 받기」 = Strong_hajin 레포
  GitHub Releases**(OQ-811 닫힘 · DEC-007 D-10 dmg)
- **방 추가 창(앱 웹뷰에서만)**: 탭 `전체·1:1·단체방` · 오픈채팅 제외 · 「선택한 N개 추가」. **방 «목록»은 프론트가
  Tauri 커맨드로 Rust 로컬에서 받고**(서버 아님), **고른 결과의 저장은 `POST …/rooms`(서버 정본)**(R-F1 정정 ·
  SPEC-006 카톡 커맨드 · SPEC-009 §3.2). 카톡이 꺼져 있으면 「카카오톡을 켜야 방 목록을 볼 수 있습니다」
- **「수집 방」 목록**: 앱 웹뷰·브라우저 **둘 다 `GET /api/integrations/{id}/rooms`(서버 정본, N-7)** — 고른 방·상태·
  적재 건수. 빼기(DELETE)도 둘 다 된다
- 참여자 안내·동의 문구 · 수집 주기 · 대화방 이름 입력은 **없다**(D-20·D-18)

### 2.6 설정 — 프로필 설정 (DC-4)

- 메뉴 `계정 설정` → **`프로필 설정`**(D-36)
- 머리: 아바타 · **이름 · 소속 · 직책 · 직무**(명부 값, **읽기 전용**) · 「조직 명부에서 관리됩니다 …」
- **프로필 이미지**: DropZone · 「이미지 변경」 · 「정사각형 1MB 이하 PNG·JPG」 · 「이미지 삭제」 · **고르면 바로
  저장**(「프로필 저장」 단추 없음) · 올리는 중 · 용량 초과 붉은 줄
- **AX 캐릭터**: 앱의 캐릭터 고르기를 **이 자리로 옮긴다**(D-48) — 4열 카드 · 고르면 바로 저장(기존
  `set_assistant_character`) · 저장 중 · 실패 시 이전으로 되돌림. **앱의 기존 진입점(런처·머리 단추)은 없앤다**
- **비밀번호 변경**: 현재·새·새 확인 · 규칙 문구 · 불일치/현재 틀림 오류 · 「변경하면 다른 기기의 로그인이 모두
  해제된다」

### 2.7 설정 — 상태·실패 배너 (D-50)

- 수집 실패(토큰 만료·권한 회수·앱 꺼짐)는 **연동 화면 상태 + 메시지함 머리 배너**(「슬랙 연결이 끊겼습니다 —
  다시 연결」)로 알린다. **알림 메뉴는 범위 밖 그대로**(D-37 · Out of Scope)

### 2.8 답장 (D-32 · DC-3)

- **슬랙**: 대화 아래 입력창(서식 막대 모양만 · 「+」 첨부 창 · 끌어다 놓기 · Enter 보내기) · 스레드 패널 입력창 ·
  보내면 **내 이름**으로 바로 섬 · 보내는 중/실패/다시 보내기
- **메일**: 원문 머리 `답장`·`전체 답장` → 원문 아래 작성 칸(받는 사람·참조 칩 · 제목 `Re:` 고정 · 본문 · 이전 내용
  접기 · DropZone 「한 번에 25MB까지」) · 보내는 중/실패 · 보내면 원문 아래 「보낸 답장」 덩어리(= **우리가 보낸
  기록**, D-47). **전달·새 메일 쓰기 없음**

---

## 3. User Scenario

- **S-1. 메일 연결** — 프로필의 이름으로 로그인한 사람이 설정 → 메일 → 「Google로 연결」 → Google 동의(readonly+send)
  → 돌아오면 계정이 「과거 메일 채우는 중」으로 붙고, 백필이 끝나면 「실시간」. 받은편지함이 메시지함 메일 탭에 쌓인다
- **S-2. 슬랙 연결·방 고르기** — 「슬랙 연결」 → 슬랙 동의(사용자 토큰) → 「방 추가」 창에서 채널·DM·그룹 DM 을 골라
  추가 → 고른 방이 「과거 메시지 채우는 중」 → 「실시간」. 안 고른 방은 쌓이지 않는다
- **S-3. 메시지함 조회·읽음** — 메일 탭에서 한 통을 열면 HTML 본문·첨부가 서고 그 카드가 읽음. 슬랙 방을 열면
  대화가 서고, 「답글 N개」를 누르면 오른쪽 스레드 패널이 열린다
- **S-4. 첨부 받기** — 메일/슬랙 첨부를 누르면 서버가 그때 내 토큰으로 받아 넘긴다(저장 안 함). 카톡 사진은
  저장본이 바로 뜨고, 오래된 카톡 사진은 「만료됨」으로 받을 수 없다
- **S-5. 답장** — 슬랙 방 입력창에 쓰고 파일을 끌어다 보내면 내 이름으로 선다. 메일은 「전체 답장」 → 작성 칸에
  쓰고 25MB 이하 첨부를 붙여 보내면 원문 아래 「보낸 답장」이 붙는다
- **S-6. 카톡 — Mac 앱으로** — Mac 앱(SPEC-009)을 켜 두면 카톡 상태 카드가 「연결됨·실행 중」. 방 고르기에서 1:1·단체방을
  골라 두면 앱이 올린 대화가 카톡 탭에 쌓인다. 카톡을 끄면 「멈춤 — 카카오톡 꺼짐」
- **S-7. 연결 해제·재연결** — 메일 계정을 「연결 해제」하면 그 계정 메일이 메시지함에서 사라진다(소프트 딜리트).
  같은 계정을 다시 연결하면 예전 것이 되살아나고 빈 구간만 새로 받는다(D-46)
- **S-8. 끊김** — Google 이 권한을 거두면 그 계정이 「연결 끊김」이 되고, 메시지함 머리에 배너가 선다. 「다시 연결」로
  한 번 더 동의하면 멈춘 뒤의 메일부터 이어 받는다
- **S-9. 프로필** — 설정 → 프로필 설정에서 이미지를 고르면 바로 올라가 저장되고, AX 캐릭터를 고르면 바로 저장된다.
  이름·직무는 읽기 전용이다. 비밀번호를 바꾸면 다른 기기의 로그인이 풀린다
- **S-10. 카톡 로그인 계정이 바뀜** — Mac 카톡이 다른 계정으로 로그인되면 앱이 그 사실을 올리고 수집이 멈춘다 —
  「계정이 바뀌었습니다 — 다시 연결」(D-45)

---

## 4. Interface Contract

**리소스·상태·enum·엔드포인트만** 둔다. 스키마·컬럼·인덱스는 `30-work/`. **인증은 두 갈래다(R3-F1)** — ① **웹
라우트**는 `current_principal`(로그인 세션 · `entrypoints/http_auth.py:68`) ② **§4.6 수집기 라우트**(handshake·messages·attachments·status — 고른 방 조회는 handshake 겸함)는 **기기 토큰**(`Authorization: Bearer`). **기기 토큰은 웹 라우트에서 받지 않고, 세션은 수집기 라우트에서
받지 않는다** — 토큰 하나가 만료 없는 전체 계정 권한이 되지 않게 범위를 가른다. 둘 다 **연동·방·메시지는 호출자
소유**, 남의 것은 **404 로 가린다**(D-24·D-25).

### 4.1 리소스와 상태값 (드러나는 것만)

| 리소스 | 드러나는 상태/종류 |
|---|---|
| 연동(integration) | `kind`: `mail` · `slack` · `kakao` / `status`: `connected`(실시간) · `backfilling`(과거 채우는 중) · `disconnected`(끊김) · `removed`(소프트 딜리트) |
| 고른 방(source) | **`room_id` = 서버 내부 id**(회원끼리 겹치지 않음) · **`external_id`** = 슬랙 channel / 카톡 chatId(회원끼리 겹칠 수 있음 · W3-9) / 슬랙: `channel`·`private`·`dm`·`group_dm` / 카톡: `direct`·`group` / `status`: `backfilling`·`live`·`paused` |
| 메시지(message) | `source_kind`: `mail`·`slack`·`kakao` / 메일 = 단건 · 슬랙·카톡 = 방에 속함 / 원문 JSON 은 서버 보관, 렌더는 프론트 |
| 첨부(attachment) | 메일·슬랙 = 참조만(받기는 중계) / 카톡 = 저장본 또는 `expired` / 종류: `image`·`album`·`file`·`video`·`audio`·`sticker` |
| 읽음(read) | **사용자별** · 카드 단위(방은 미읽음 수) |
| 보낸 답장(sent_reply) | 우리가 보낸 기록(D-47). 메일 보낸편지함을 재수집하지 않는다 |
| 프로필 이미지 | 저장 경로만 DB(저장본은 hostPath) |

### 4.2 연결 흐름 — OAuth (F-2 · W-9)

**연결 시작은 302 리다이렉트가 아니라 JSON 이다.** 회사판 데스크톱 셸은 같은 origin `/api/` 이동을 가로채
직접 GET 하고(SPEC-006 U-5 · `lib.rs:483-498`) redirect 0 이라 302 가 실패 토스트로 끝나기 때문이다(F-2).
그래서 **서버가 회원에 묶인 일회용 `state` 를 박은 동의 URL 을 JSON 으로 돌려주고**, 웹이면 그 URL 로
`location` 이동, **데스크톱이면 `open_external` 로 OS 브라우저**에서 연다. **콜백은 쿠키가 아니라 `state` 로
회원을 찾는다** — OS 브라우저엔 `scax_session` 이 없다.

| 경로 | 요청 | 응답 | 오류 |
|---|---|---|---|
| `POST /api/integrations/{mail\|slack}/connect` | (본문 없음) | `200 {authorize_url, state}` — `state` = **회원 id·종류·만료(짧음)·nonce** 를 묶은 서명값, 서버가 발급·보관. `authorize_url` = Google/슬랙 동의 URL(scope 는 아래 주) | **슬랙만** 이미 연결됨=`409`(워크스페이스 하나) · **메일은 409 없음**(계정 여럿 · N-1) |
| `GET /api/integrations/{mail\|slack}/callback?code&state` | — | code→토큰 교환 · `state` 로 **회원 확인**(쿠키 안 씀) · 토큰 **암호화 저장**(§5) · **메일은 같은 주소면 D-46 되살림**(N-1) · (메일) watch 등록 · 백필 시작 · **`302 → {AX_WEB_ORIGIN}/?surface=settings&tab={mail\|slack}&connect={ok\|denied}`**(라우터 없는 SPA 라 **쿼리**로 · `App.tsx:385-389` 가 쿼리를 읽는다 · N-2) | `state` 만료·위조=`400`, 동의 거부=`302 …&connect=denied` |
| `POST /api/integrations/{id}/reconnect` | (본문 없음) | **connect 와 같은 모양** `200 {authorize_url, state}` — 예전 것 되살리고 빈 구간만 새로(D-46) | 남의 것=`404` |
| `POST /api/integrations/{id}/disconnect` | (본문 없음) | `204` — 소프트 딜리트(D-27), 되살릴 수 있게 남김 | 남의 것=`404` |
| `POST /api/device-tokens` | `{device_name}` · **세션 인증(웹)** | `201 {token}` — **장수명 기기 토큰**(OQ-906). 로그인한 회원으로 발급 · 회원에 묶임 · **서버는 토큰의 해시만 보관**(원문은 이 응답에서만, 뒤엔 못 읽음) · 전달은 **`Authorization: Bearer`** · **허용 범위 = §4.6 수집기 라우트만**(= handshake·messages·attachments·status · 「카톡 고른 방 조회」도 handshake 가 겸한다 · W4-1) · 웹 라우트엔 안 통함 · **새 발급은 같은 회원의 옛 토큰을 철회**(D-45 — 사람당 Mac 한 대) · 만료 없음 → 「마지막 사용 시각」 표시 | — |
| `GET /api/device-tokens` · `DELETE /api/device-tokens/{id}` | 세션 | 내 기기 토큰 목록(이름·마지막 사용) · 철회(설정 · 철회 즉시 그 토큰 무효) | 남의 것=`404` |

- **발급 → Rust 전달(R3-F1 ④ · P-5)**: 발급은 **세션 있는 앱 웹뷰**가 하고, 받은 토큰을 곧바로 **Tauri 커맨드
  `kakao_store_device_token`**(SPEC-006)으로 Rust 키체인에 넣는다 — **화면·브라우저 저장소에 남기지 않는다**.
  설정의 「이 Mac 연결」 단추 하나가 이 흐름이다
- **무효화(R3-F1 ⑤)**: 비밀번호 변경·회원 비활성 때 그 회원의 **기기 토큰도 함께 무효**(세션만 revoke 하던 §4.7 을 확장)

- scope: 메일 = `gmail.readonly`+`gmail.send` **한 번에**(D-09 · web OAuth client) / 슬랙 = 사용자 토큰 읽기
  권한 + `files:write`(§5 슬랙 권한)
- **redirect_uri(§4.5 대체)**: **운영** = `https://ax.medisolveai.xyz/api/integrations/{mail|slack}/callback`
  (같은 origin 하나 · DEC-007 D-03). **로컬** = **Google(메일)만** `http://127.0.0.1:8001/...`(`make local-stack`
  API 포트 8001 · `Makefile:16-17`·`:285-288` — W-9) · local-stack 이 **`AX_WEB_ORIGIN=http://127.0.0.1:5176`** 을
  넘겨 콜백이 프론트로 돌아오게 한다(N-2). **슬랙 OAuth 는 https 가 필요해 로컬에서 안 되고 운영에서만 시험**
  한다(원장 RES:93). 그래서 슬랙 redirect_uri 는 운영 하나만 등록
- **데스크톱 — 동의 뒤 갱신(N-3)**: OS 브라우저에서 동의가 끝나 앱은 그 사실을 모른다. 앱 창이 **`focus`/
  `visibilitychange`** 때 `GET /api/integrations` 를 다시 읽어 갱신한다(또는 §4.4 실시간 채널 사건)

### 4.3 설정·방 고르기 API (R-F1 정정 · F-4 · N-7)

**고른 방(설정)은 슬랙·카톡 모두 서버가 저장·정본이다**(사용자 정정 2026-10-06). **카톡만 다른 점은 방 «목록
탐색»** — 그 목록은 서버가 모르고 **데스크톱 앱(Rust)이 로컬 카톡 DB 에서** 읽어 고르기 창에 준다(Tauri 커맨드).
고른 결과의 **저장은 서버 API** 이고, 수집기는 시작·생존 신호 때 서버에서 고른 방을 받아 로컬 캐시한다.

| 경로 | 요청 | 응답 | 오류 |
|---|---|---|---|
| `GET /api/integrations` | — | `[{id, kind, status, synced_count, last_synced_at}]` — 내 연동만 | — |
| `GET /api/integrations/{id}/rooms` | — | `[{room_id, type, name, synced_count, status}]` — **고른 방(= 수집 방) 목록**(N-7 · **서버 정본**). 슬랙·카톡 모두. 웹에서도 보인다 | 남의 것=`404` |
| `GET /api/integrations/slack/available-rooms?q&cursor` | 검색어·커서 | 슬랙 방 목록 — **사용자 토큰으로 실시간 조회**(그룹 DM 은 참여자 실명, D-12) · `{rooms:[{room_id, type, name, is_bot, member_count, already_added}], next_cursor}` | 끊김=`409` |
| (카톡 방 **목록 탐색**) | — | **서버 API 아님** — 앱 웹뷰에서 **Tauri 커맨드**로 Rust 로컬 조회(§2.5 · SPEC-009 §3.2). 서버는 목록을 저장·중계하지 않는다 | — |
| `POST /api/integrations/{id}/rooms` | `{room_ids:[...]}` | `202` — 고른 방이 `backfilling`→`live`. **슬랙·카톡 모두 서버 저장**(연동에 매달림, D-26). 카톡은 **앱 웹뷰에서 고른 결과를 이 API 로** 올린다 | 남의 연동=`404` |
| `DELETE /api/integrations/{id}/rooms/{room_id}` | — | `204` — 방 빼기(소프트 딜리트) · **슬랙·카톡 모두** · **웹에서도** 뺀다(서버 정본이므로) | — |
| `POST /api/integrations/kakao/reset-account` | — | `204` — **웹 설정 「다시 연결」 단추(세션 인증 · ★2)**. `account_changed` 로 멈춘 뒤 부른다 → **옛 계정의 방·대화는 소프트 딜리트로 남기고**(D-46) `reset_at` 을 찍는다. **앱은 다음 handshake 의 `reset_at` 으로 알고** 새 계정 기준으로 다시 수집(W-4·N-9) | 남의 것=`404` |

**R-F1(정정) — 고른 방은 서버 저장·정본, 방 목록 탐색만 로컬.** 카톡 방 «목록»은 서버가 모르므로 **앱 웹뷰에서
Tauri 커맨드로 Rust 가 로컬 카톡 DB 에서 읽어** 고르기 창에 준다(SPEC-006 v0.6.0 노출 · SPEC-009 §3.2). 하지만
**고른 방 자체는 `POST …/rooms` 로 서버에 저장**되고(D-26), 그래서 **브라우저에서도 고른 방 목록·빼기가 보이고
된다.** 수집기는 handshake·생존 신호 때 서버의 고른 방을 받아 로컬 캐시한다(SPEC-009 §3.2). 업로드 **검사(403)는
서버가 가진 고른 방 기준**이다 — 앞 판의 「고른 방 매니페스트」는 **걷었다**(서버가 정본이라 불필요). **D-15 는
「방 «목록»이 로컬」로 좁혀 읽는다**(선택·정본은 서버). 「방 추가」 창은 앱 웹뷰에서만 열리고(목록이 로컬), 앱이
꺼져 있으면 「카카오톡을 켜야 방 목록을 볼 수 있습니다」.

### 4.4 메시지함 · 답장 API (F-3 · F-4 · W-11)

| 경로 | 요청 | 응답 | 오류 |
|---|---|---|---|
| `GET /api/inbox/messages?source&unread&cursor` | `source`(all/mail/slack/kakao) · `unread`(bool) · `cursor` | `{items:[메일 단건 \| 방 카드], next_cursor}` — 방 카드 = `{room_id, kind, title, unread_count, last_at, preview[3]}` / 메일 = `{message_id, subject, from, at, unread, attach_count}` | — |
| `GET /api/inbox/mail/{message_id}` | — | 메일 원문 — 머리 표 + **소독한 안전본 HTML**(§2.1 F-3) + 첨부 메타 `[{aid, name, size, mime}]` | 남의 것=`404` |
| `GET /api/inbox/rooms/{room_id}/messages?cursor&thread_ts` | `cursor`(과거로) · `thread_ts`(스레드면) | `{messages:[원문 JSON], next_cursor}` — **방 메시지는 페이지네이션**(슬랙 백필이 「허용 전부」라 한 번에 못 냄 · 기본 최신 N, 위로 `cursor`). `thread_ts` 주면 그 스레드 답글 | 남의 것=`404` |
| `POST /api/inbox/rooms/{room_id}/read` | `{up_to_ts}` | `204` — 그 방을 **`up_to_ts` 까지 읽음**(방 카드 미읽음 수 재계산, W-4 의 사용자별) | — |
| `POST /api/inbox/mail/{message_id}/read` · `POST /api/inbox/read-all?source` | — | `204` — 메일 단건 읽음 · 모두 읽음(출처 한정 가능) | — |
| `GET /api/inbox/mail/{message_id}/attachments/{aid}` · `GET /api/inbox/rooms/{room_id}/attachments/{aid}` | — | 바이트 + Content-Disposition — 메일·슬랙 = **그 사용자 토큰으로 중계(저장 안 함)** · 카톡 = 저장본. 경로를 **메일/방으로 가른다**(N-9 · 다른 경로와 결 맞춤). **응답은 `inline_media_type` 허용 목록만 inline, 나머지 `attachment`**(F-3 · `entrypoints/http.py:1105`) | 카톡 만료=`410 expired` · 상류 실패=`502` |
| `GET /api/inbox/mail/{message_id}/remote-image?u=` | 본문 속 이미지 URL | 서버 프록시로 받아 중계(N-5 · F-3 「이미지 보기」). **그 메일 본문에 실제로 있는 URL 만 · http(s) 만 · 사설·루프백·메타데이터 IP 거절(SSRF) · 이미지 MIME 만 · 크기 상한** | 규칙 위반=`400` · 상류 실패=`502` |
| `POST /api/inbox/rooms/{room_id}/reply` | `{text, thread_ts?, files[]}` · `Idempotency-Key` 헤더 | `202 {local_id}` → 보내는 중 → **결과는 실시간 채널(아래) 사건**으로(N-9). 슬랙 채널·스레드 · **내 이름(사용자 토큰)** · 첨부 `files:write`. **재시도 중복 방지 = `Idempotency-Key`**(기존 `create_task` 본보기 `entrypoints/http.py:1364-1367`) | 끊김=`409` · 상류 429/5xx 은 **실시간 사건으로 실패 통지**+「다시 보내기」 |
| `POST /api/inbox/mail/{message_id}/reply` | `{reply_all, body, to[], cc[], files[]}` | `202` → 보낸 답장 기록(D-47) · `Re:` · 스레드 이어짐 · 결과는 실시간 사건 | **첨부 합계(인코딩 전) 25MB 초과=`413`**(Gmail 은 메일 «전체» 한도라 파일당이 아니라 합계 · W-11) · 상류 실패=실시간 사건 |

- **실시간 갱신(F-4 ③ · N-6)**: 지금 WS 는 **회의 하나에 묶인 것 하나뿐**(`/api/meetings/{id}/stream` ·
  `entrypoints/http.py:1023`)이라 못 쓴다. **사용자 단위 WS `/api/inbox/stream`(= 사용자 사건 채널)을 새로** 둔다 —
  새 메시지 도착·답장 결과(202 뒤 성공/실패)를 민다. 새 메시지를 받는 곳은 **연동 워커(다른 프로세스)**이고 WS 는
  back 에 사니, **워커 → back 알림은 Postgres `LISTEN/NOTIFY`**(또는 짧은 폴링)로 잇는다. 이 채널은 2단계(AX
  판단·알림)도 쓰므로 「메시지함 전용」이 아니라 **사용자 사건 채널**로 짓는다(제안 P-4)
- **첨부 한도(W-10·W-11)**: 메일 = **첨부 합계 25MB**(Gmail 전체 한도) · 슬랙 보내기·카톡 저장 = **파일 하나당
  50MB**. 운영 ingress `proxyBodySize` 를 그보다 크게(§5 배치 · W-10)

### 4.5 redirect_uri — §4.2 로 옮김

연결 흐름과 한 몸이라 **§4.2 끝**에 적었다(운영 하나 · 로컬은 Google 만 · 슬랙은 운영에서만). 개인판 redirect 는
이번 범위 밖(**OQ-804 닫힘** · 회사판만, W-7).

### 4.6 카톡 수신 — Mac 앱 → 서버 (F-1 · F-4 · W-1·2·3·4 · SPEC-009 가 소비 · **이 절이 정본**)

Mac 앱(SPEC-009)은 **장수명 기기 토큰으로** 서버에 붙는다 — `Authorization: Bearer`(§4.2). 이 **아래 §4.6 라우트에만** 통한다(고른 방 조회도 handshake 가 겸함 · W4-1) · 웹 라우트엔 안 통한다(R3-F1 범위). 올린 것은 **그 회원 소유**로만 들어간다.
토큰은 설정에서 철회·비밀번호 변경 때 무효(§4.2·§4.7). **고른 방은 서버 정본**이라(R-F1 정정) handshake 가
내려준다 — 앱은 방 «목록 탐색»만 로컬로 한다.

| 경로 | 요청 | 응답 | 오류 |
|---|---|---|---|
| `GET /api/integrations/kakao/handshake` | — | `{integration_id, selected_rooms:[{room_id(서버 내부), external_id(=chatId), last_logId}], reset_at}` — **서버가 고른 방(정본)과 각 방 마지막 반영 지점을 내려준다**(앱이 로컬 캐시 · 그 뒤만 올린다 · R-F1 정정) · `reset_at` = 계정 reset 시각(N-9) · `selected_rooms_version`(status 가 이 값으로 변경을 알린다 · W3-3). 연동이 없으면 **첫 handshake 가 카톡 연동 레코드를 만든다**(F-4 ④) | — |
| `POST /api/integrations/kakao/messages` | `{room_id(서버 내부 id), messages:[{logId, seq_in_log?, author, at, type, text, attachments:[{kind, seq, name, size, mime, expired?}]}], backfill_done:bool}` | `202 {accepted, attachment_upload:[{logId, seq, aid}]}` — **중복 키 = `(연동, chatId, logId)`**(회원 범위 · 동료 둘이 같은 단체방이어도 각자 저장 · D-25 · W3-2) · **`aid` = `SHA-256("{integration_id}:{chatId}:{logId}:{seq}")` hex**(앱·서버가 같은 바이트 식 · W3-2·N-8) · `backfill_done` 이면 그 방 `live`(W-1) | **`room_id` 가 서버의 고른 방이 아니면 `403`**(서버 정본 기준 · 매니페스트 없음) · 묶음 **최대 500건**(초과=`413`) |
| `POST /api/integrations/kakao/attachments/{aid}` | 바이트 + `{name, size, mime}` | `201` — hostPath 저장 · DB 는 경로만. **50MB 초과는 받지 않고 `413`**(앱이 메타만, §2.2) | 알 수 없는 `aid`=`404` |
| `POST /api/integrations/kakao/status` | `{app:{device_name, version}, kakao:{state: running\|off\|unreadable, reason?: permission\|version\|unknown}, account:{name}, account_changed:bool}` — **주기 보고(기본 30초)** | `200 {selected_rooms_version}` — 상태 카드·배너 반영(§2.5). **서버는 「마지막 보고 후 90초 무보고 = `app:off`」로 판정**(W-3). **버전이 바뀌었으면**(웹에서 방 추가·빼기) 앱이 handshake 를 다시 불러 고른 방을 받는다(W-3) | — |

- **★1 — 서버 `room_id` ↔ 로컬 chatId 잇기**: handshake 의 `external_id`(=chatId)로 앱이 「서버 고른 방 = 로컬 어느 방」을 안다. 업로드는 서버 내부 `room_id` 로 보내고, **서버는 그 방의 `external_id`(chatId)로 중복 키 `(연동,chatId,logId)`·`aid` 를 만든다**(앱도 같은 chatId 라 값이 일치)
- 방 **목록**을 올리는 `rooms/report` 는 **없다** — 카톡 방 «목록 탐색»이 앱 로컬이라 서버가 전체 목록을 받을 일이
  없다. 하지만 **고른 방(선택)은 `POST /api/integrations/{id}/rooms`(§4.3)로 서버에 저장**되고 handshake 가 내려준다
- **업로드 검사(403)는 서버가 가진 고른 방 기준**이다(R-F1 정정). 앞 판의 `selected_room_ids` 매니페스트는 **걷었다**
- **`unreadable` 사유(W-2)**: `reason` = `permission`(전체 디스크 접근 없음) · `version`(DB 못 엶) · `unknown`.
  문구는 §2.5 한 곳
- **방별 상태(W-1)**: `backfill_done` 표지로 `backfilling`→`live`. `paused` 는 status 의 `app:off`/`kakao:off` 에서 파생
- **중복 방지 키**(전부 **연동 범위** · D-25): 슬랙 `(연동, channel, ts)`(팬아웃 W-8) · Gmail `(연동, message id)` · 카톡 `(연동, chatId, logId)`(W-3·W3-2 · `kakao-db-fields.md` §6)
- 첨부 종류·만료 규칙은 §2.2 · SPEC-009 §(첨부)

### 4.7 프로필 API

**프로필 머리 값은 새 API 를 만들지 않고 기존 `GET /api/organization/me`(`entrypoints/http.py:1360-1362` ·
`MyOrganizationProfileView` = 소속·직책·직무 + `assistant_character`, `organization_access/results.py:67-68`)에
`profile_image_url` 한 칸을 더해 재사용한다**(W-15 — 새 `GET /api/profile` 는 같은 값이라 겹친다).

| 경로 | 요청 | 응답 | 오류 |
|---|---|---|---|
| `GET /api/organization/me` (확장) | — | 기존 값 + **`profile_image_url`**(없으면 null → 이니셜 아바타) | — |
| `GET /api/profile/image` (신설) | — | 이미지 바이트 + Content-Type — **아바타를 그리는 곳**(SideNav·대화)이 쓴다(W-15, 지금은 내려받는 길이 없었다) | 없음=`404` |
| `PUT /api/profile/image` | 파일(멀티파트) | `200 {profile_image_url}` — **고르면 바로 저장**(즉시) · 정사각형 1MB 이하 PNG·JPG · hostPath 저장(§5) | 1MB 초과·형식 아님=`413`/`415` |
| `DELETE /api/profile/image` | — | `204` | — |
| `PUT /api/profile/preferences/assistant-character` | 기존 그대로 | **기존 API 재사용**(`entrypoints/http.py:679`) — `expected_version` · 409/422 | — |
| `POST /api/profile/password` (신설) | `{current, new}` | `204` — `verify_password` 로 현재 확인 · `hash_password` 로 새 저장(≥8자) · **다른 기기 로그인 모두 해제 + 기기 토큰 모두 무효**(내 세션 외 `AuthSessionRecord` 일괄 revoke + 그 회원의 기기 토큰 revoke — 회원 단위 일괄 revoke 를 **새로 필요**, `platform/auth_sessions.py` · R3-F1 ⑤) | 현재 틀림=`401`(전용 오류) · 규칙 위반=`422 PasswordRejected` (`modules/organization_access/credentials.py`) |

### Validation

- 메일 답장 첨부 **합계(인코딩 전) 25MB** 초과면 **거절**(Gmail 은 메일 «전체» 한도라 파일당이 아니라 합계 ·
  W-11 · OQ-806 닫힘). 응답 `413`
- 슬랙 보내기·카톡 수집 저장 한도 = **파일 하나당 50MB**(OQ-807 닫힘). 50MB 초과 카톡 첨부는 저장하지 않고
  「너무 큼 — 카톡에서 확인」(§2.2). 운영 ingress `proxyBodySize` 를 그보다 크게(W-10 · §5 배치)
- 비밀번호: 현재 틀림 = 전용 오류 · 새 비밀번호 규칙(≥8자) 위반 = `PasswordRejected` · 불일치는 프론트
- 방 추가: 이미 고른 방은 다시 안 붙음 · 오픈채팅은 애초 목록에 없음(카톡)
- 토큰 만료/권한 회수 = 해당 연동 `disconnected`, 수집 멈춤, 배너

### Case Matrix (에러·경계)

| 경우 | 응답/상태 |
|---|---|
| 남의 연동/방/메시지 접근 | 404(존재를 가린다) |
| 카톡 고르지 않은 방 업로드(서버 고른 방 아님) | 403(R-F1 정정 · 매니페스트 없음) |
| OAuth `state` 만료·위조 | 400 |
| 메일 답장 첨부 합계 25MB 초과 | 413(W-11) · 카톡 첨부 50MB 초과 업로드 413 |
| 슬랙/Gmail 상류 429·5xx | 답장은 `202` 뒤 **실시간 사건으로 실패 통지**(§4.4) + 「다시 보내기」 · 조회 중계는 `502` |
| 끊긴 연동으로 첨부 받기·답장 | 409 또는 배너로 「다시 연결」 유도 |
| 카톡 첨부 만료 | 410 `expired` |
| 카톡 방 고르기(앱 웹뷰) · 카톡 꺼짐 | 방 목록 비움 + 「카카오톡을 켜야 방 목록을 볼 수 있습니다」(§2.5) |
| 카톡 읽기 불가(권한/버전) | 상태 `unreadable` → 상태 카드 문구(D-42) |
| Google/슬랙 동의 거부·취소 | 설정 화면으로 302 · 「연결되지 않았습니다」 |
| 비밀번호 변경 성공 | 내 세션만 남고 나머지 revoke |

### Data Contract (드러나는 것만)

- 토큰은 **암호화 저장** — **env 의 대칭키 하나(Fernet 류)**로 암호화(§5 env). 키 회전은 범위 밖(OQ-801 닫힘 — 사용자 결정 2026-10-06). 평문·로그 금지(비밀번호 코드와 같은 결, `credentials.py` 머리 주석)
- 원문 메시지는 **그대로 저장**(가공은 렌더에서, D-28)
- 카톡 첨부·프로필 이미지 = hostPath 저장본, DB 는 경로만(D-29·D-30)
- 스키마 전문은 `30-work/` 의 Domain/Schema

---

## 5. Implementation Rules

### 권한·소유

- 웹 라우트 `current_principal`(로그인 세션 · 개발 `X-Demo-Persona` 그대로 — `http_auth.py:68`) · **수집기 라우트
  (§4.6)는 기기 토큰**으로 회원을 찾는다(쿠키 아님 · OQ-906). 둘 다 **그 회원 소유**만, 남의 것 404
- 연동·방·메시지·첨부·읽음·보낸 답장은 **연결한 사람 것**. 조회·중계·답장 모두 그 사람 토큰으로. 남의 것 404
- 같은 방을 여럿이 골라도 **사람마다 따로**(각자 토큰·각자 읽음, D-25). **원문 메시지 사본도 사람마다 복제한다** —
  공유 한 벌이 아니다(OQ-808 닫힘 — 사용자 결정 2026-10-06). 소유 경계가 저장 비용보다 앞선다

### 동기화 — 프로세스 배치

- **슬랙 Socket Mode**: **앱 토큰 1개**로 연결은 **서버 한 곳에서만** 뜬다 — **연동 전용 워커를 새로 둔다**
  (`worker-external` 계열 제안 · `replicas: 1`, 이름은 구현). 기존 워커 넷(conversation·material·meeting·report)에
  얹지 않고 별도 디플로이로 세운다(OQ-802 닫힘 — 사용자 결정 2026-10-06). 틀은 회의/자료 워커의
  `Worker(Settings.from_environment())` 단일 루프와 같다(`entrypoints/material_worker.py` · runbook-002:42). 여러
  레플리카가 같은 앱 토큰으로 붙으면 이벤트가 갈리므로 **단일 소유·단일 레플리카**가 계약이다. Gmail Pub/Sub
  pull·백필도 이 연동 워커가 함께 돈다
- **슬랙 이벤트 팬아웃(W-8)**: 사용자 토큰 이벤트는 앱 토큰 하나로 들어오지만 이벤트의 `authorizations` 는 한
  사람만 담아 온다(슬랙이 잘라 보냄). D-25(사람마다 따로 저장)를 지키려면 워커가 **이벤트 1건 → 그 `(team,
  channel)` 을 고른 «모든» 연동에 복제 저장**해야 한다. 중복 방지 키는 **`(연동, channel, ts)`** — 연동마다 한 벌
- **Gmail**: `users.watch`(7일 만료) → Pub/Sub **pull** 구독을 워커가 돈다 · watch 는 **매일 갱신**(D-22)
- **최초 백필**: 메일 = 받은편지함 전체 · 슬랙 = API 허용 끝까지(D-23). 뒤에서 채우며 진행률(「채우는 중 · N건」).
  진행은 **그 연동의 워커 작업**으로, 사용자 조작과 독립
- **재시작 메우기**: 각 방/계정의 **마지막 반영 지점** 이후를 훑어 빠진 것을 메운다(D-22)
- **카톡**: 서버는 **Mac 앱이 올린 것을 받기만** 한다(§4.6). 폴링·복호는 **Mac 안**(SPEC-009)

### 저장 (hostPath)

- 카톡 첨부·프로필 이미지 = `LocalDirectoryMaterialStorage` 계열로 **같은 방식** 저장(`platform/materials.py:26`).
  **운영 hostPath 전용 마운트** — runbook-002 의 `/mnt/mac/strong-hajin/{recordings,materials}` 옆에 외부 채널용
  디렉터리 하나를 더한다(이름은 구현, env 로 연다). type `Directory`(마운트 빠지면 안 뜸, runbook-002:164)
- DB 는 **경로만**. 크기 한도: 프로필 이미지 **1MB**(DC-4) · 카톡 수집 저장 **50MB**(초과는 저장 안 함 · §2.2, OQ-807 닫힘)
- 메일·슬랙 첨부는 **저장하지 않는다** — 받을 때 중계(D-29)
- **보존·파기 기간을 두지 않는다 — 계속 보관**(회사 데이터, 사용자 결정 2026-10-06 · §2.3). 소프트 딜리트만 있고
  물리 삭제가 없으므로 저장본도 지우지 않는다(OQ-805 닫힘)

### 운영 배치 — pod × (env · Secret 파일 · hostPath) (W-10 · W-12)

차트는 `MediSolveAIDev/k8s_infra_mac` 소유이고 **이 작업의 쓰기 범위 밖**이다 — 아래는 `30-work/`·운영 할 일의
계약이다. 근거 `CHART/templates/{back,worker,ingress}.yaml` · `values.yaml`.

| 무엇 | back(API) | 연동 워커 | 왜 |
|---|---|---|---|
| OAuth client 비밀값·`AX_EXTERNAL_TOKEN_ENCRYPTION_KEY` | ✅ | ✅ | back 은 연결/콜백·중계·답장, 워커는 수집에서 토큰 복호 |
| `SLACK_APP_TOKEN`·`GMAIL_PUBSUB_*` | — | ✅ | Socket Mode·pull 은 워커만 |
| `GOOGLE_PUBSUB_SA_KEY_FILE` | — | ✅ **(Secret 볼륨 마운트)** | **파일**이라 `envFrom secretRef` 로 안 들어간다 — Secret 을 파일로 마운트해 그 경로를 env 로(W-12 ②) |
| `AX_EXTERNAL_CHANNEL_STORAGE_DIR` hostPath | ✅ **(마운트)** | ✅ **(마운트)** | **카톡 첨부·프로필 이미지 업로드는 API(back)가 받는다** — 새 hostPath 는 back 에도 마운트돼야 한다(W-12 ① · 지금 hostPath 둘은 워커만, `CHART/worker.yaml:54-62`) |

- **replicas(W-12 ③)**: 연동 워커는 **kind 별 레플리카 고정 1**이 계약(Socket Mode 단일 소유). 지금 차트는 kind
  별 레플리카가 없어(`CHART/worker.yaml:18-19` 공용 `worker.replicas`) 남이 올리면 이벤트가 갈린다 → 차트 할 일
- **ingress 바디 크기(W-10)**: 앱 한도 50MB 와 `proxyBodySize: "50m"`(`CHART/values.yaml:23`)가 같아 multipart
  머리만큼 넘쳐 nginx 가 413 을 먼저 낸다. **`proxyBodySize` 를 앱 한도보다 크게**(예 60m) 올리는 것을 운영 할 일로
- **운영 워커 목록(기존 부채)**: `CHART/values-prod.yaml` 의 `worker.kinds` 에 연동 워커를 넣어야 뜬다

### 로컬 스택 (W-13)

- 새 **연동 워커 Make 타겟**을 만들고 `make local-stack`·`acceptance-e2e` 감독 목록에 넣는다
  (`Makefile:296-323` 가 띄우는 프로세스들 옆). 지금 Soniox 가 `meeting-worker` 타겟에만 실리듯
  (`Makefile:263`), **`~/.config/google/env`·`~/.config/slack/env` 를 api·연동 워커 타겟에 싣는다**
- 로컬 API 포트는 **8001**(`make local-stack` · `Makefile:16-17`) — §4.2 redirect_uri 가 그 포트다(W-9)

### 토큰·env

값은 쓰지 않는다. 이름만. **이름 규칙(v0.2.0)**: 외부 서비스 값은 **그 서비스 접두어**(기존 `TDL_*` 처럼 ·
`bootstrap/settings.py:179-183`), 내부 설정은 **`AX_*`**(기존 `AX_MATERIALS_DIR` 등 · `settings.py:158`).

| env | 종류 | 뜻 |
|---|---|---|
| `GOOGLE_OAUTH_CLIENT_ID` · `GOOGLE_OAUTH_CLIENT_SECRET` | 외부(Google) | Gmail web OAuth client(D-09 — 회사 GCP 프로젝트, 이전 시 교체) |
| `GMAIL_PUBSUB_TOPIC` · `GMAIL_PUBSUB_SUBSCRIPTION` | 외부(Google) | watch 알림을 받는 Pub/Sub |
| `GOOGLE_PUBSUB_SA_KEY_FILE` | 외부(Google) | Pub/Sub pull 용 서비스 계정 키 파일 경로 |
| `SLACK_CLIENT_ID` · `SLACK_CLIENT_SECRET` | 외부(Slack) | 슬랙 OAuth |
| `SLACK_APP_TOKEN` | 외부(Slack) | Socket Mode 앱 토큰(1개 · 단일 워커) |
| `AX_EXTERNAL_TOKEN_ENCRYPTION_KEY` | **내부** | 저장 토큰 암호화 **대칭키 하나(Fernet 류)**. 키 회전은 범위 밖(OQ-801). 내부 설정이라 `AX_` 접두어 |
| `AX_EXTERNAL_CHANNEL_STORAGE_DIR` | **내부** | 카톡 첨부·프로필 이미지 hostPath. 내부 설정이라 `AX_` 접두어 |

`Settings.from_environment()` 에 같은 방식으로 더한다(`bootstrap/settings.py:141`).

### 비밀값 위치 (v0.2.0)

레포 규칙을 따른다 — Soniox·THE CONNECT 키가 쓰는 그 틀(`Makefile:2`·`:5`·`:6`·`:9`).

- **로컬**: 서비스별 env 파일 `~/.config/<서비스>/env` —
  - `~/.config/google/env` : `GOOGLE_OAUTH_*` · `GMAIL_PUBSUB_*` · `GOOGLE_PUBSUB_SA_KEY_FILE`
  - `~/.config/slack/env` : `SLACK_*`
  - Makefile 이 `SONIOX_ENV_FILE`·`THECONNECT_ENV_FILE` 과 **같은 방식**(`set -a; [ -f 파일 ] && . 파일; set +a`)으로
    읽어 값은 어디에도 찍지 않는다. 파일이 없으면 그 연동이 **스스로 없다고 말한다**(Soniox·THE CONNECT 의 결, D-50 배너)
  - 내부 값(`AX_EXTERNAL_TOKEN_ENCRYPTION_KEY`·`AX_EXTERNAL_CHANNEL_STORAGE_DIR`)은 다른 `AX_*` 처럼 프로세스 환경으로
- **운영**: **k8s Secret → 차트 `secretRef`** — 회의·STT 키가 들어오는 그 길
  (`k8s_infra_mac/charts/strong-hajin/templates/back.yaml:48-50` · `worker.yaml:39-41`). 토큰 암호화 키도 Secret.
  인프라 레포(`MediSolveAIDev/k8s_infra_mac`)는 **이 작업의 쓰기 범위 밖** — 차트·Secret 추가는 `30-work/`·운영 몫

### 슬랙 권한

- 사용자 토큰 **실측 10개**(§BASE-006 입력 4-2) + **`files:write`**(답장 첨부, D-32) = 11. 앱 설정에 더한다

### 스키마 변경

- 새 표·인덱스는 로컬 `schema_sync`(additive, `bootstrap/schema_sync.py`) · 운영은 `backend/migrations/manual/*.sql`
  (인덱스는 `.concurrent.sql`, `backend/migrations/manual/2026-09-28-w7-successor-index.concurrent.sql` 본보기). 전문은 `30-work/`

### 프론트

- **메시지함 = 새 surface** · **설정 = 새 surface**(모달 아님 — 시안이 전체 화면). `navigation` 배열(`App.tsx:37`)과
  `surface` 라우팅(`App.tsx:395`)에 더한다.
- **AX 캐릭터 진입점은 둘이다(W-14)** — ① `utilityItems` 설정(`App.tsx:417`·`:606`) ② **신원 줄 `onUserClick`**
  (`App.tsx:402-405`). D-48 「런처·머리 단추를 없앤다」를 지키려면 **둘 다** 프로필 설정으로 보낸다 — 설정 진입점은
  설정 화면을 열고, 신원 줄의 모달 열기도 없애거나 프로필 설정로 보낸다
- 슬랙 렌더(blocks·mrkdwn·멘션 이름)는 프론트 책임. DS 부품 재사용(DropZone·FileList, DC-3)

### 데스크톱 경계

- 카톡 수집은 **SPEC-009(Mac 앱)**. **수집은 회사판(medi-ax) 데스크톱 앱에 더한다**(W-7 · 개인판은 주소가
  정해질 때). 이 때문에 SPEC-006 의 「커맨드 넷·파일 권한 없음」 불변식(I-2)과 「창 하나·트레이 없음·백그라운드
  없음」이 **개정 대상**이 된다 — **SPEC-006 v0.6.0 이 받는다**(닫기=웹뷰 파괴·프로세스 상주(L-06 무변경)·카톡 커맨드 노출 포함). 이 SPEC 은 그 사실만 적는다

---

## 6. Verification

### Acceptance Criteria

**연동·흐름**

- AC-01 메일 「Google로 연결」 → **connect 가 `{authorize_url, state}` JSON** → 웹은 이동/데스크톱은 `open_external`
  → 동의(readonly+send 한 번) → **콜백이 `state` 로 회원 찾음**(쿠키 아님) → 계정 `backfilling` → 백필 끝 `connected`
- AC-01b 데스크톱 셸 안에서 연결이 **기본 브라우저로 열리고**, 앱 창이 **`focus`/`visibilitychange`** 때 연동 목록을
  다시 읽어 갱신한다(F-2·N-3) · `state` 만료=400 · 콜백 302 목적지는 **쿼리**(`?surface=settings&tab=…&connect=ok`, N-2)
- AC-01c **메일은 둘째 계정 연결이 409 로 막히지 않는다**(N-1) · 같은 주소 재연결은 콜백에서 D-46 되살림
- AC-02 슬랙 「슬랙 연결」 → 사용자 토큰 동의 → 방 고르기 창에서 채널·DM·그룹 DM·비공개를 골라 추가 → `backfilling`→`live`
- AC-03 그룹 DM 이 **참여자 실명**으로 보인다(`mpdm-…` 아님)
- AC-04 안 고른 슬랙 방·오픈채팅은 쌓이지 않는다
- AC-05 연결 해제 → 메시지함에서 사라짐 · 재연결 → 예전 것 되살고 빈 구간만 새로(D-46)
- AC-06 Google 권한 회수 → 그 계정 `disconnected` · 메시지함 머리 배너 · 「다시 연결」로 이어 받음

**메시지함·첨부**

- AC-07 출처 필터(전체/메일/슬랙/카톡) · 미읽음 수 · 카드 누르면 읽음 · 모두 읽음
- AC-08 메일 본문 = 머리 표·HTML·첨부 / 슬랙 = 대화방 모양·묶음·서식·스레드 패널 / 카톡 = 입력창 없는 대화방
- AC-08b **HTML 메일 소독**(F-3) — `<script>`·`on*`·`<form>`·`<iframe>` 가 지워진 안전본이 **샌드박스 iframe**
  (`allow-same-origin allow-popups allow-popups-to-escape-sandbox` · **`allow-scripts` 금지**, N-4)에 선다 ·
  부모가 높이를 재고 링크 새 탭이 열린다 · 인용 접기는 `<details>` · 원격 이미지 기본 차단 · 「이미지 보기」는
  서버 프록시(**사설·루프백 IP 거절 SSRF**, N-5)
- AC-09 메일·슬랙 첨부 = 누를 때 중계(저장 안 함, 경로 `mail/…`·`rooms/…` 로 가름 N-9) · 카톡 사진 = 저장본 ·
  만료 카톡 = 410 「만료됨」 · 중계 응답은 허용 목록만 inline, 나머지 `attachment`
- AC-10 본문이 폭 전체를 쓴다 · 슬랙 스레드가 오른쪽 3열 패널 · **방 메시지가 페이지네이션으로 온다**(위로 cursor)
- AC-10b 새 메시지·답장 결과가 **새 사용자 WS `/api/inbox/stream`**(회의 WS 아님)로 밀려 갱신된다 ·
  워커→back 은 Postgres `LISTEN/NOTIFY`(F-4 ③·N-6)
- AC-11 읽음은 사용자별 — 같은 방을 둘이 골라도 각자 읽음 · 방 읽음은 `up_to_ts` 까지

**답장**

- AC-12 슬랙 채널·스레드 답장이 내 이름으로 섬 · 첨부(`files:write`) · 보내는 중/실패/다시 보내기 ·
  **재시도는 `Idempotency-Key` 로 중복 없음** · `202` 뒤 상류 429/5xx 은 **실시간 사건으로 실패 통지**(§4.4)
- AC-13 메일 답장/전체 답장 · `Re:` · 스레드 이어짐 · **첨부 합계 25MB 초과=413**(파일당 아님, W-11) · 「보낸 답장」 = 우리 기록

**카톡 수신(§4.6 · SPEC-009 소비)**

- AC-14 카톡 방 **목록 탐색은 앱 웹뷰 Tauri 커맨드(Rust 로컬)** · **고른 방 저장은 `POST …/rooms`(서버 정본)**(R-F1 정정) ·
  고른 방 목록·빼기는 **웹에서도** 보이고 된다(`GET/DELETE …/rooms`) · 카톡 `rooms/report`·`available-rooms` 없음
- AC-14b **서버의 고른 방이 아닌 방 메시지 업로드는 403**(서버 정본 기준 · 매니페스트 걷음) · 카톡 연동 레코드는 **첫 handshake 가 만든다**
- AC-14c 수집기는 **기기 토큰 `Authorization: Bearer`** 로 붙고(키체인·창 쿠키 아님) · **서버는 해시만 보관** ·
  토큰은 **§4.6 수집기 라우트에만** 통하고(고른 방 조회는 handshake 겸함 · W4-1) **웹 라우트엔 거절**(R3-F1) · **새 발급이 옛 토큰 철회**(D-45) ·
  비밀번호 변경·회원 비활성 때 함께 무효 · 발급 토큰은 **`kakao_store_device_token` 으로 바로 Rust 키체인**(화면에 안 남김)
- AC-15 메시지 묶음 업로드가 `(chatId, logId)` 로 **중복을 버린다** · **`aid`=`(chatId,logId,seq)` 결정식**(앱·서버 같은 규칙, N-8) · 묶음 500건 초과=413
- AC-16 첨부(사진·앨범·파일) 저장본 · 동영상·음성 표시만 · 이모티콘 표식 · 만료 「만료됨」 · 50MB 초과 업로드=413
- AC-17 상태 보고(주기 30초)로 상태 카드가 바뀐다 — 앱 off(**90초 무보고 판정**) · 카톡 off · **읽기 불가 사유별
  문구**(permission/version) · 계정 바뀜→수집 멈춤→`reset-account`
- AC-17b `backfill_done` 표지로 방이 `backfilling`→`live`(W-1)

**프로필**

- AC-18 이미지 고르면 바로 저장 · 1MB 초과 거절 · 삭제
- AC-18b 머리 값은 `GET /api/organization/me`(+`profile_image_url`) 재사용 · 아바타는 `GET /api/profile/image` 로 그린다(W-15)
- AC-19 AX 캐릭터가 프로필 설정에서 저장(기존 API) · **진입점 둘(설정 · 신원 줄 `onUserClick`)이 다 사라진다**(W-14)
- AC-20 비밀번호 변경 — 현재 틀림 오류 · 성공 시 **다른 기기 로그인 모두 해제 + 기기 토큰 모두 무효**(R3-F1 ⑤) · 이름·직무 읽기 전용

**경계**

- AC-21 라우트는 **로그인 세션**(웹)이나 **기기 토큰**(수집기)을 요구(남의 것 404) · 저장 토큰은 암호화, 로그·평문 없음 ·
  기기 토큰은 설정에서 철회
- AC-22 슬랙 Socket Mode 가 **한 워커에서만** 붙는다(레플리카 하나) — 이벤트가 갈리지 않는다

### 실물에서만 답이 나는 것

- Gmail watch 갱신 주기·Pub/Sub pull 지연(운영 GCP) · 슬랙 Socket Mode 재연결 · 백필이 슬랙 플랜 한도에서 어디서 멈추나
- 카톡 첨부 CDN 만료가 수집 간격 안에 들어오나(`kakao-db-fields.md` §3 — 사진 ~3일)
- hostPath 마운트가 외부 채널 디렉터리에도 필요(runbook-002:164) — 없으면 안 뜸

### DEC-008 결정 → SPEC-008 절 (이 SPEC 이 받는 것)

D-01~D-50 전수. **범위 밖은 「해당 없음(사유)」**. 카톡 수집 내부(DB 열기)는 SPEC-009.

| D | 절 | D | 절 |
|---|---|---|---|
| D-01 순서 | 해당 없음(과정) | D-26 별도 연동 테이블·FK | §4.1 · Data Contract |
| D-02 착수 순서 | 해당 없음(과정) | D-27 소프트 딜리트 | §2.3 · §4.2 |
| D-03 단계 분리 | §1 Out(2단계) | D-28 원문 그대로 저장 | §4 Data Contract · §4.6 |
| D-04 1단계=연동+조회+답장 | §1 BR · §2·§2.8 | D-29 메일·슬랙 첨부 중계 | §2.2 · §4.4 · §5 저장 |
| D-05 한 slug | 해당 없음(과정) | D-30 카톡 첨부 저장본 | §2.2 · §4.6 · §5 저장 |
| D-06 메시지함 vs 업무>수신함 | Placement · §1 관계 | D-31 카톡 첨부 종류 | §2.2 · AC-16 |
| D-07 읽음만 | §2.1 | D-32 답장 | §2.8 · §4.4 · AC-12·13 |
| D-08 채널 단위 | §2.1 · §4.1 | D-33 메일·슬랙 본문 | §2.1 |
| D-09 Gmail API readonly+send | §4.2 · §5 env | D-34 폭 전체·스레드 3열 | §2.1 · AC-10 |
| D-10 받은편지함만·여러 계정 | §2.3 · §4.2 | D-35 설정 시안 | §2.3·2.4 |
| D-11 슬랙 사용자 토큰·목록 | §2.4 · §4.2·4.3 | D-36 프로필 설정 | §2.6 · §4.7 |
| D-12 그룹 DM 참여자 이름 | §2.4 · §4.3 · AC-03 | D-37 알림 메뉴 밖 | §1 Out · §2.7 |
| D-13 봇 처리 없음 | §2.4 | D-38 시안 로컬 사본 | 해당 없음(과정) |
| D-14 Mac 앱(Rust) | §4.6 · §5 경계 · SPEC-009 | D-39 도착→AX 판단 | §1 Out(2단계) |
| D-15 방 정보 로컬 Rust | §4.3·§4.6 — **「방 «목록»이 로컬」로 좁혀 읽는다**. 고른 방(선택)은 **서버 정본**(R-F1 정정 2026-10-06) | D-40 카톡 DB 1회 확인 | 해당 없음(조사 근거) |
| D-16 키 Mac 안 | SPEC-009 · §4.6(서버는 키 안 받음) | D-41 Gmail 내부 앱 유지 | §5 env(이전 시 교체) · OQ 없음 |
| D-17 카톡 조회만 | §2.1·2.5 · §4.6 | D-42 카톡 못 읽음 표시 | §2.5 · §4.6 status `unreadable` |
| D-18 고른 1:1·단체·오픈채팅 제외 | §2.5 · §4.3·4.6 | D-43 상태 카드 정보 | §2.5 · §4.6 status |
| D-19 카톡 실행 확인 | §2.5 · §4.6 status | D-44 좁은 화면 안 함 | Placement |
| D-20 동의 문구 없음·로컬만큼 | §2.5 | D-45 계정 바뀌면 멈춤·사람당 1대 | §2.5 · §4.6 `account_changed` · AC-17 |
| D-21 카톡 질문 셋 닫힘 | §2.5 | D-46 재연결 되살림 | §2.3 · §4.2 · AC-05 |
| D-22 실시간·메우기 | §5 동기화 · AC-01·22 | D-47 보낸 답장 = 우리 기록 | §2.8 · §4.1·4.4 |
| D-23 최초 백필 | §5 동기화 | D-48 캐릭터 진입점 하나 | §2.6 · §5 프론트 · AC-19 |
| D-24 개인별 소유 | §4 머리 · §5 권한 | D-49 보존 기간 | §2.3·§5 저장 — **계속 보관**으로 대체(2026-10-06) · 물리삭제 없음 |
| D-25 사람마다 따로 | §5 권한 · AC-11 | D-50 실패 배너 | §2.7 · §4.1 · AC-06 |

---

## 7. Open Questions

OQ-801~808·811 은 **2026-10-06 사용자 결정으로 닫혔다.** v0.3.0 검수가 OQ-811 을 열었고 v0.4.0 이 닫았다. 행은
지우지 않는다.

| ID | 무엇 | 처분 |
|---|---|---|
| **OQ-801** | 토큰 암호화 방식·키 회전 | **닫힘** — env 대칭키 하나(Fernet 류) · 키 회전은 범위 밖. → §4 Data · §5 env |
| **OQ-802** | 슬랙 Socket Mode 를 어느 프로세스가 지나 | **닫힘** — 연동 전용 워커를 새로(기존 넷에 안 얹음 · `replicas:1`). → §5 동기화·배치 |
| **OQ-803** | Gmail Pub/Sub 푸시냐 pull 이냐 | **닫힘** — pull. → §5 동기화 |
| **OQ-804** | 개인판 OAuth redirect_uri | **닫힘** — 이번엔 회사판(`ax.medisolveai.xyz`)만 · 개인판 redirect 는 범위 밖. → §4.2 |
| **OQ-805** | 원문·첨부·카톡 저장본 보존·파기 | **닫힘** — 보존·파기 없음, 계속 보관(D-49 대체) · 물리 삭제 없음. → §2.3 · §5 저장 |
| **OQ-806** | 메일 25MB 초과 첨부 | **닫힘** — 첨부 **합계** 25MB 초과면 전부 거절(Gmail 전체 한도, W-11). → §4.4 |
| **OQ-807** | 카톡 첨부 저장본 한도·동영상/음성 | **닫힘** — 파일당 50MB · 동영상·음성은 메타만 · 초과는 「너무 큼」. → §2.2 · §5 저장 |
| **OQ-808** | 슬랙 메시지 사본 공유냐 복제냐 | **닫힘** — 사람마다 복제(D-25). → §5 권한 |
| **OQ-811** | 「Mac 앱 받기」 링크의 **목적지** | **닫힘** — **Strong_hajin 레포 GitHub Releases**(사용자 결정 2026-10-06 · DEC-007 D-10 dmg). → §2.5 |

### 미결이 아닌 것 — 다음 문서의 몫

- 저장 구조·테이블·컬럼·인덱스 전문 · 수집 워커 구현 · 슬랙 blocks 렌더 상세 → `30-work/`
- 카톡 DB 를 **여는 방식**(키·userId·복호) → SPEC-009(그것도 구현 몫으로 참조만)
