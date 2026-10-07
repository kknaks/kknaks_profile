# 4차 검수 반영 fix-map — SPEC-008·009 v0.5.1 · WORK-011 (2026-10-06)

리포트 `review-spec-work-r4.md`(조건부 PASS)의 ★1~★4 와 WARN 을 어디에 반영했는지. S8=spec-008 · S9=spec-009 ·
S6=spec-006 · WP=work-011. **SPEC-006 은 r4 에 내용 변경이 없어 v0.6.0 유지.**

## ★ (발주 문서에 바로)

| # | 어떻게 고쳤나 | 어디 |
|---|---|---|
| **★1** handshake 에 chatId | handshake `selected_rooms` 에 **`external_id`(=chatId)** 추가 — 앱이 서버 `room_id` ↔ 로컬 chatId 를 잇고, 서버는 그 chatId 로 `(연동,chatId,logId)`·`aid` 를 만든다(앱도 같은 값) | S8 §4.6 handshake·★1 불릿 · S9 §3.1·§4 handshake · WP BE-3 |
| **★2** reset-account 인증 모순 | `reset-account` 를 **웹 세션 라우트(§4.3)** 로 옮김 — 기기 토큰 절에 있어 웹 「다시 연결」이 401 나던 모순 해소. 앱은 handshake `reset_at` 으로 안다 | S8 §4.3·§4.6(행 삭제) · S9 §2.2·§4 · WP BE-3 |
| **★3** 슬랙 로컬 측정 불가 | BE-2 에 **개발 전용 토큰 주입 make 타겟**(`~/.slack_test_token` → 연결된 슬랙 연동 레코드 · 운영 프로파일 거절) · 「슬랙 연결」 OAuth 버튼은 **운영 반영 뒤 확인** | WP BE-2 완료 조건·시험 |
| **★4** 반영 순서 선행 둘 없음 | 「반영」 Phase 를 **순서 목록**으로: ①노드 mkdir(hostPath Directory) ②manual SQL ③Secret(SA 파일 볼륨) ④차트 ⑤이미지→sync ⑥dmg · 롤백 역순 | WP 반영 Phase |

## SPEC WARN

| # | 어떻게 | 어디 |
|---|---|---|
| W4-1 | 기기 토큰 범위 = **§4.6 라우트만**(고른 방 조회는 handshake 겸함) — 「+ 고른 방 조회」 모호성 제거 | S8 §4 머리·§4.2·§4.6·AC-14c · S9 §4 |
| W4-2 | 옛 문장 셋 — §1 표(두 갈래 인증 명시) · Case Matrix 502(답장은 실시간 사건) · S9 메시지 키 `(연동,chatId,logId)` | S8 §1 표·Case Matrix · S9 §4 |

## WORK-011 WARN

| # | 어떻게 | 어디 |
|---|---|---|
| W4-3 | BE-1 계약에 **동기화 상태 칸**(Gmail historyId·watch 만료·슬랙 방별 ts·team·백필 건수·마지막 반영 지점) · **모듈 골격**(BE-2 `sync_*` · BE-3 `inbox_*`) · **NOTIFY 채널·페이로드** 추가 → BE-2∥BE-3 나란히 조건 성립 | WP BE-1·파일 겹침 |
| W4-4 | FE-b 카톡 방 추가·「이 Mac 연결」은 **SHELL 의 `lib/shell.ts` 바인딩 뒤**(시그니처 먼저 커밋) | WP FE-b 시작 조건 |
| W4-5 | **SHELL-0 카톡 DB 탐침 Phase** 신설 — BE-1 과 동시(가장 먼저) · 완료=방 목록 1회 · 막히면 코디가 범위 결정(카톡만 뒤로) | WP SHELL-0 · Work Summary · 파일 겹침 |
| W4-6 | SHELL 시험에 **판 가르기 검증**: `SHELL_FLAVOR=medi-ax`→`--features kakao-collector` · `shell-final-preflight` 가 개인판에 수집기 심볼 없음 확인 | WP SHELL 시험 |
| W4-7 | 비번 변경 때 **기기 토큰 철회**(BE-3) · **「이 Mac 연결」+토큰 목록·철회 화면**(FE-b) · **`selected_rooms_version` 만들기**(BE-3) · **첫 handshake 연동 생성**(BE-3) · **AX_WEB_ORIGIN**(BE-1 Makefile) · **운영 인벤토리 json**(BE-1·3 시험) · **iframe 높이·링크·아바타 GET**(FE-a) | WP 각 Phase |
| W4-8 | WP 옛 문장 — Meta SPEC 판 v0.4.0→v0.5.1 · BE-1 시작 조건 · 답장 502·aid·SHELL 커맨드 「…류·넷 넘음」→정확히 셋 | WP Meta·BE-1·BE-3·SHELL |
| W4-9 | 롤백에 **외부 쪽 잔여** 한 줄(watch 7일·Socket Mode 끊김 · 재반영 시 pull 잔여는 history 메우기가 흡수) | WP Rollback |

## 상태

- WORK-011 frontmatter·README: `todo`→**`in_progress`**(BE-1·SHELL-0 발주됨)
- SPEC-008·009 v0.5.0→**v0.5.1**(머리에 변경 이력). SPEC-006 변경 없음 → v0.6.0 유지
- 열린 OQ 0 · 발주 전 남은 것은 ★ 넷(★1 SHELL 전·★2 BE-3 전·★3 BE-2 전·★4 반영 전) — 모두 WP 에 반영돼 발주문이 참조

## 범위 밖 / 구현 몫

- 인프라 레포(차트·Secret·ingress·worker.kinds) — infra 워커·운영 (WP INFRA·반영)
- 카톡 DB 여는 절차 — 구현 몫, mykakao SPEC-001 · SHELL-0 에서 1회 실증(막히면 코디)
- DEC-008 은 이번 판에서 손대지 않음(r4 판정 밖 · W3-4 는 r3 에서 반영됨)
