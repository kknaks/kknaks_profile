# 3차 검수 반영 fix-map — SPEC-008·009 v0.5.0 · SPEC-006 v0.6.0 (2026-10-06)

리포트 `review-spec-008-009-r3.md` 의 R3-F1·R3-F2 + WARN 9 를 어디에 반영했는지. S8=spec-008 · S9=spec-009 ·
S6=spec-006 · DEC=decision-008 · WP=work-011.

## FAIL

| # | 어떻게 고쳤나 | 어디 |
|---|---|---|
| **R3-F1** 기기 토큰 계약 | `Authorization: Bearer` · **서버 해시만 보관** · **범위 = §4.6 수집기 라우트 + 고른 방 조회만**(웹 라우트·`current_principal` 거절) · 발급은 세션 웹 → **`kakao_store_device_token`** 으로 Rust 키체인(화면에 안 남김) · **새 발급이 옛 토큰 철회**(D-45) · 비밀번호 변경·회원 비활성 때 함께 무효 · 만료 없음→마지막 사용 시각. 인증 두 갈래를 §4 머리에 못박음 | S8 §4 머리·§4.2 기기 토큰 표·§4.6 머리·§4.7 비밀번호·AC-14c·20 · S9 §2.1·§4 인증 · S6 커맨드 표·수집기 인증 절 |
| **R3-F2** 닫기 vs 녹음 | 「닫기=숨기기·숨김에서 L-06 해제」를 **걷고** **「닫기=웹뷰 실제 파괴·앱 프로세스만 메뉴 막대 상주」**(트레이 「열기」가 창 새로 만듦)로. 창이 파괴되므로 `Destroyed` 가 와서 **L-06·S-6·`E-12`·AC-T32 무변경** · OQ-T10 닫힘 · 수집기는 기기 토큰이라 창과 무관 | S6 불변식 표 닫기 행·그대로인 것·OQ-T10·헤더 v0.6.0 · S9 §2.1 상주·창·AC-06b |

## WARN

| # | 어떻게 고쳤나 | 어디 |
|---|---|---|
| W3-1 | S6 커맨드 수 자기모순 해소 — **medi-ax 웹 커맨드 정확히 일곱**(넷 + `kakao_list_rooms`·`kakao_collector_status`·`kakao_store_device_token`) · strong-hajin 넷. I-2·AC-T23/T47·그대로인 것·커맨드 표 한 문장으로 | S6 불변식·AC 표·커맨드 표 |
| W3-2 | 카톡 중복 키·aid 에 **연동(사용자) 범위** — 키 `(연동, chatId, logId)` · **`aid`=SHA-256("{integration_id}:{chatId}:{logId}:{seq}") hex**(바이트 식) | S8 §4.1·§4.6 messages·키 불릿 · DEC D-15 · WP |
| W3-3 | 웹에서 고른 방 바뀜을 앱이 알게 — **status 응답 `200 {selected_rooms_version}`** · handshake 에 버전 · 바뀌면 재호출 | S8 §4.6 status·handshake · S9 §2.1 인증·§4 |
| W3-6 | 스크립트 없는 iframe — 높이=**부모가 `contentDocument.scrollHeight`** · 링크=**부모가 iframe 클릭 가로채** 웹 새 탭/데스크톱 `open_external`(postMessage·iframe 내 커맨드 안 됨) | S8 §2.1 메일 본문 |
| W3-7 | 옛 문장 정리 — §4 머리(세션→두 갈래) · Case Matrix(매니페스트→서버 고른 방·「Mac 앱 켜져」→「카카오톡 켜야」) · AC-12(502→실시간 사건) · S9 머리 v0.4.0(선택=서버 정본) · `rooms_seen`→`selected_rooms` | S8 §4 머리·Case Matrix·AC-12 · S9 머리·§4·인증 |
| W3-8 | cargo feature 빌드 배선 — `shell-build`/`tauri-local` 이 medi-ax 에 `--features kakao-collector` · preflight 가 개인판에 수집기 심볼·FDA 없음 확인 | S6 판 가르기 절 |
| W3-9 | `room_id` = **서버 내부 id** · 외부 id 는 `external_id`(회원끼리 겹침) | S8 §4.1·§4.6 |
| W3-4 | DEC-008 「뒤집힌 결정 2」에 **D-15 행**(방 목록만 로컬·고른 방 서버 · RES:75 근거) — D-15 본문은 안 고침 | DEC §뒤집힌 결정 2 |
| W3-5 | 「사람당 Mac 한 대」 = 새 토큰 발급이 옛 것 철회(R3-F1 ⑤ 와 함께) | S8 §4.2·AC-14c |

## 앞 판 FAIL 재확인

- R-F1(선택 서버 정본·목록만 로컬) · R-F2(쿠키→기기 토큰) 유지. R3 는 R-F2 의 「숨기기」 부작용만 교정

## WORK-011 반영

- SHELL Phase·Meta·Code Surface 를 이 판에 맞춤(닫기=웹뷰 파괴·커맨드 일곱·기기 토큰 Bearer·store 커맨드·키 연동 범위·aid 식)

## 열린 것

- **없음.** OQ-T10 닫힘(S6). OQ-811·906 은 앞 판에서 닫힘. SPEC-008·009 OQ 전부 닫힘

## 범위 밖 / 구현 몫

- 인프라 레포 차트·Secret·ingress — infra 워커·운영(WP INFRA Phase · S8 §5)
- 카톡 DB 여는 절차(키·userId·복호) — 구현 몫(mykakao SPEC-001) · WP Open Issue I-1
- 나머지 WARN(이미 전부 본문 반영) — 구현 중 세부는 WORK-011
