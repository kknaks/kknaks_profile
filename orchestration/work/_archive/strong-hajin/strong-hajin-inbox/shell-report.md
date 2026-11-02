# WORK-011 Phase SHELL 결과 보고 — 데스크톱 앱(medi-ax) 카톡 수집기

## 상태: done (커밋 안 함 · 워크트리 변경만 · 실물 E2E 1회 통과)

SPEC-009 v0.5.1 · SPEC-006 v0.6.0 「외부 채널 수집기 수용」을 구현했다. mykakao Mac 방식(DEC-001·SPEC-001)의
키 유도·user_id 복구·SQLCipher 복호를 **Rust 로 그대로 옮겼고**, 이 Mac 에서 방 목록 추출 → 로컬 API 업로드를
실제로 한 번 통과시켰다.

## 변경 파일 (전부 frontend/src-tauri + 빌드 배선 — 백엔드는 건드리지 않았다)

신규 — `frontend/src-tauri/src/kakao/`
- `mod.rs` — 모듈 묶음 + `#[ignore]` 실기 테스트 둘(방 목록 · collect_once E2E)
- `crypto.rs` — IOPlatformUUID·`_hashed_uuid`·`secure_key`·`db_name`·SHA512 preimage user_id 복구(스레드 brute force·캐시) — extract.py 그대로
- `db.rs` — SQLCipher read-only 열기(compat 3→4 폴백)·방 목록(1:1·단체 · 오픈채팅 `linkId>0` 제외)·메시지·첨부 JSON 파싱(사진 2·앨범 27·파일 18·동영상 3·음성 4/5·스티커 6/12/20 · 만료 `expires`/`expire` 짧은 쪽)
- `client.rs` — §4.6 Bearer 클라이언트(handshake·messages·attachments multipart·status) · ureq native-tls
- `collector.rs` — 2초 폴링 수집 루프 · `collect_once`(handshake→방별 묶음 ≤500→pending 첨부 CDN 받아 업로드→status 30초) · Shared 상태
- `keychain.rs` — 기기 토큰을 macOS 키체인에(apple-native) · axdt_ 접두 검사
- `commands.rs` — 웹뷰 커맨드 **정확히 셋**: `kakao_list_rooms`·`kakao_collector_status`·`kakao_store_device_token`(FE `lib/shell.ts` 계약과 맞춤)
- `tray.rs` — 메뉴 막대 트레이(열기=창 새로 만듦·종료·FDA 설정 열기) · `x-apple.systempreferences:` 딥링크 네이티브 직접(N-11)

수정
- `src/lib.rs` — 창 빌더를 `spawn_main_window` 로 추출(부팅·트레이 「열기」가 같은 창을 만든다) · feature `kakao-collector` 일 때 트레이+수집기+커맨드 셋 배선 · `RunEvent::ExitRequested` 에서 `prevent_exit`(닫기=웹뷰 파괴·프로세스만 상주 · R3-F2) · 커맨드 수 시험을 판별로(strong-hajin 4 · medi-ax 7)
- `build.rs` — **판 가르기 · feature↔판 대조**(medi-ax ⟺ `kakao-collector`, 어긋나면 빌드 중단 · W3-8) · medi-ax 에 카톡 커맨드 셋 ACL 추가
- `Cargo.toml` — `[features] kakao-collector`(tray-icon·image-png·rusqlite(bundled-sqlcipher-vendored-openssl)·keyring·sha1·sha2·pbkdf2·base64·plist, 전부 optional)
- `flavors/medi-ax/capabilities/product-shell.json` — 권한 일곱(넷 + 카톡 셋) · 파일·프로세스 권한은 여전히 0
- `Makefile` shell-build · `scripts/run-tauri-local.mjs` — medi-ax 일 때 `--features kakao-collector`
- `scripts/verify-shell-build.mjs` · `verify-final-build.mjs` — 커맨드 수를 판별로(medi-ax 7·그밖 4) · 개인판에 카톡 커맨드 샘 검사

## 검증 수치

- `cargo check` — strong-hajin ✓ / medi-ax(+feature) ✓
- `cargo clippy --all-targets -- -D warnings` — strong-hajin ✓ / medi-ax ✓ (경고 0)
- `cargo test` — strong-hajin **66 passed** / medi-ax **83 passed**(카톡 단위 17 추가 · 실기 2 ignored)
- `make shell-verify-strict` — strong-hajin ✓ / medi-ax ✓ (구성 미비 0건)
- **실기 SHELL-0** — 이 Mac 카톡 DB 복호 성공: user_id=39411126, SQLCipher key 256-hex, **방 426개** 추출(이름·종류)
- **실기 E2E (로컬 API `http://127.0.0.1:8001` · 데모 jiho)** — 기기 토큰 발급(axdt_) → 방 「메디솔브에이아이」(chatId 474083620228748) 서버 고르기 202 → handshake → **메시지 28건 업로드** → status 보고. 서버 확인:
  - `GET /api/inbox/messages?source=kakao` → 그 방 카드 `unread_count=28`, 미리보기 실내용(작성자 "이건학" · "끝!"·"재빌드 테스트")
  - `GET /api/integrations` → kakao **connected · synced=28**, collector 상태 `app_state=on · kakao_state=running · account_name=이건학 · account_changed=false · device_name="admin의 MacBook Pro"`
  - 첨부 업로드는 이 방이 텍스트라 0건 — 첨부 파싱/다운로드/업로드 경로는 단위 테스트로 덮음(사진·앨범·파일·만료·종류 분류)

## 미결 / 유의

1. **첨부 CDN 실물 업로드 1회는 미확인** — 선택한 방이 텍스트였다. 최근(3일 내) 사진 있는 방을 고르면 확인된다. 경로는 단위 테스트 + 서버 `attachment_upload` pending 응답 소비로 검증.
2. **그룹방 이름** — chatName 이 비면 "(이름 없음)"으로 둔다(1:1 은 상대 이름 잘 나온다). 참여자 BLOB(`displayMemberIds`) 조합은 형식 미문서화라 보류 — mykakao 도 안 했다. AC-04 「참여자 이름으로」는 부분 충족.
3. **폴링 틱마다 handshake+status** — `collect_once` 가 매 2초 tick 에서 handshake·status 를 함께 보낸다(상태 30초보다 잦음 · 기능상 무해, 서버 90초 무보고=off 판정에 영향 없음). 단일 사용자 데스크톱이라 부하 미미. 더 조이려면 version 변화 때만 re-handshake 하도록 분리 가능.
4. **GUI 전체 E2E(창 닫아도 수집 이어짐·FDA 안내 화면)** 는 headless 로 못 재 수치 보고는 `collect_once` 헤드리스 경로로 했다. 닫기=웹뷰 파괴+프로세스 상주는 `prevent_exit` 로 구현, 코드/시험으로 고정(수동 GUI 확인은 코디 몫).
5. **데모 토큰** — jiho 기기 토큰 하나를 데모 스택에 남겼다(새 발급이 옛 것 철회 · D-45 라 자기 정리됨).
6. 워크트리에 **내가 안 만든 backend/* 미커밋 변경**이 있다(세션 시작 스냅샷은 clean 이었음 · BE 진행분으로 추정). 건드리지 않았다.

## 실기 재현 명령(코디용)
```
# 방 목록(FDA·로그인 필요)
cd frontend/src-tauri && SHELL_FLAVOR=medi-ax cargo test --features kakao-collector -- --ignored --nocapture kakao_live_room_list
# E2E 업로드
KAKAO_API_ORIGIN=http://127.0.0.1:8001 KAKAO_DEVICE_TOKEN=<axdt_…> \
KAKAO_E2E_CHATID=<chatId> KAKAO_E2E_NAME=<이름> KAKAO_PERSONA=jiho \
SHELL_FLAVOR=medi-ax cargo test --features kakao-collector -- --ignored --nocapture kakao_live_collect_once
# 토큰 발급: curl -XPOST :8001/api/device-tokens -H 'X-Demo-Persona: jiho' -H 'Content-Type: application/json' -d '{"device_name":"mac"}'
```

---

## §9 운영 E2E 결함 — 원인·수정 (ureq native-tls provider)

**증상(코디 운영 E2E)**: 새 medi-ax dmg 에서 설정>카카오톡 연동에 「Mac 앱 받기」 카드가 뜨고, 수집기가 서버에
한 번도 안 붙음(handshake 없음·기기 토큰 「마지막 사용 아직 없음」). FE 로직상 그 카드는 `integration === null`
(= 수집기 첫 handshake 가 서버 연동 레코드를 못 만든 상태)이고, 「이 Mac 연결」 버튼이 보이므로 `hasKakaoCollector`
(=`inApp`)는 **true** — 커맨드·ACL·키체인 저장은 정상이었다.

**원인(확정)**: 수집기 스레드가 **첫 https 요청에서 패닉**해 죽었다. 설치된 서명 바이너리를 터미널에서 띄워 stderr 에서 잡음:
```
thread 'kakao-collector' panicked at ureq-3.4.2/.../transport/mod.rs:485:
uri scheme is https, provider is NativeTls but feature is not enabled: native-tls
```
`frontend/src-tauri/Cargo.toml` 의 ureq 가 `features = ["native-tls-no-default"]` 였다. ureq 3.x 는 **NativeTls
provider 등록을 `feature = "native-tls"` 로 가른다** — `native-tls-no-default` 는 `dep:native-tls` 만 들이고 그
cfg 를 안 켜서 `TlsProvider::NativeTls` 가 https 에서 런타임 패닉한다. 스레드가 handshake 전에 사망 → 서버에
아무 요청도 안 감 → integration 미생성 → 「Mac 앱 받기」 카드 + 토큰 미사용. **로컬 E2E 는 `http://127.0.0.1:8001`
(TLS 안 탐)이라 안 드러났고, 운영 `https://ax.medisolveai.xyz` 에서만 터진다.** 같은 결함이 `download.rs`(U-5 https
첨부 내려받기)에도 잠복해 있었다 — 함께 고쳐진다.

**수정**: ureq feature 를 `native-tls-no-default` → **`native-tls`**(provider 를 등록하는 상위 feature · rustls 는
여전히 안 싣음). 회귀 가드 테스트 신설(`https_네이티브tls_가_패닉하지_않는다`): 같은 NativeTls+PlatformVerifier
에이전트로 `https://ax.medisolveai.xyz/` GET → **status 200, 패닉 0**. collect_once 업로드 로직은 이미 로컬 28건으로 검증됨.

**추가 보강**: 수집기 스레드·collect_once·토큰 유무에 `log_event` 로그를 넣었다(이전엔 로그 0건이라 이런 런타임
결함을 못 봤다). 이제 운영에서 `[shell][kakao]` 로그로 resolve/handshake/status 결과가 바로 보인다.

**검증 수치(수정 후)**: base `cargo test` 66 · medi-ax 83(+ignored 6) · clippy(-D warnings) 양 판 0경고 · https NativeTls 200.

**남은 것(코디·운영)**: 수정 소스로 **dmg 재빌드·서명·공증**(RUNBOOK-002) → 사용자 재설치 → 「이 Mac 연결」 다시
누름(기존 토큰은 못 쓰니 재발급) → handshake→방 고르기→수집 확인. 운영 https 대상 실물 handshake 1회는 그때 완성.
(기기 토큰 keychain 서비스 = `app.ax.desktop.kakao-collector` · account `device-token`.)

**운영 실물 검증(수정본 재빌드 스모크)**: 고친 소스로 `make shell-build SHELL_FLAVOR=medi-ax` 후 그 바이너리를
실행하니 `https://ax.medisolveai.xyz` 로 **패닉 0 · handshake OK**:
```
[shell][kakao] 수집기 스레드 시작 base=https://ax.medisolveai.xyz
[shell][kakao] collect_once 시작
[shell][kakao] DB 열림 user_id=39411126 account=Some("이건학")          ← FDA·복호 정상
[shell][kakao] handshake OK integration=b73bbbf8-… rooms=0 version=0    ← 운영 서버에 붙음(integration 생성)
[shell][kakao] status OK selected_rooms_version=0
```
수집기가 운영 https 에 붙어 연동 레코드를 만들고 상태를 올렸다 → 「Mac 앱 받기」 상태가 풀린다. 이제 사용자는
(서명 dmg 재배포 후) 방을 고르면 수집이 돈다. **남은 것은 코디의 서명·공증 dmg 재빌드뿐.**

---

## §10 E2E 3 — 단체방 「(이름 없음)」 → 참여자 이름 조합

**증상**: 「방 추가」 창의 단체방이 전부 「(이름 없음)」(참여 1·8·5·10·101명 …). 내 이전 미결(그룹방 참여자 이름 보류)이 이것.

**조사**: mykakao 는 그룹 이름을 **안 풀었다**(chatName 없으면 "(이름 없음)" 그대로 · `COALESCE(NULLIF(chatName,''),…)`)
— 참고 대상 아님. 실 DB 를 뜯어 보니 멤버 테이블은 없고 `NTChatRoom.displayMemberIds` 가 **바이너리 plist**
(`bplist00` 헤더 · 정수 배열 = 표시 멤버 userId 들 · **나 자신은 이미 빠져 있다**). 내 userId 는 `NTChatContext.userId`.

**수정(`frontend/src-tauri/src/kakao/db.rs`)**: 방 이름 = **사용자가 정한 방 이름(chatName)** 우선 → 없으면
① 1:1 = 상대 이름 ② 단체방 = `displayMemberIds`(plist 크레이트로 파싱)의 멤버 이름을 **「, 」로 이은 것**(카톡 방
제목 방식) → 그래도 비면 "(이름 없음)". 이름 우선순위를 **friendNickName(내가 준 이름) → displayName → nickName**
으로 바꿔 카톡에 보이는 이름과 맞췄다(1:1·그룹 공통). 이름풀이는 `NTUser` 를 한 번만 읽어 map 으로(N+1 회피).

**실 DB 검증**: 단체방 78개 중 **70개가 이제 참여자 이름으로** 뜬다(예: "엄마, 하지니♥️, 형, 정재연" · "이용준, 이상혁,
이학준, 엄재훈, 양희승"). 남은 8개는 `displayMemberIds` 가 **빈/멤버 0·1·시스템방(chatId=-2)** 이라 풀 멤버가 없어
"(이름 없음)" — 더 못한다. 1:1 이름도 정상(회사/공식계정은 displayName, 지인은 커스텀/프로필 이름). 카톡처럼 표시
멤버가 참여수보다 적으면(예 101명 중 5명) 그 5명만 — 카톡 제목과 같다.

**검증 수치**: medi-ax `cargo test` 85(+2 단위테스트: bplist 파싱·그룹이름 조합)·clippy(-D warnings) 0경고 · base 66.

**dmg 재빌드 필요?** → **예.** 방 목록은 Rust 커맨드 `kakao_list_rooms`(=`db::list_rooms`)가 주므로 **웹만 고쳐선
안 되고 수집기(앱) 재빌드·서명·공증이 필요**하다(fix2). 참고: 선택 시 FE 가 이 이름을 서버에 저장하므로
**새로 고르는 방**은 바른 이름이 들어가고, **이미 추가해 둔 방**은 재선택(또는 서버 백필) 전까지 옛 이름이 남는다.
