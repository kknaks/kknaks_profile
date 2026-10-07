# 재검수 반영 fix-map 2 — SPEC-008·009 v0.4.0 · SPEC-006 v0.5.0 (2026-10-06, 2차)

리포트 `review-spec-008-009-r2.md` 의 R-F1·R-F2 + 새 WARN 12, 그리고 **사용자 정정**(고른 방 = 서버 저장·정본,
목록 탐색만 로컬)을 어디에 반영했는지. S8=spec-008 · S9=spec-009 · S6=spec-006.

## FAIL (이번 판)

| # | 어떻게 고쳤나 | 어디 |
|---|---|---|
| **R-F1** (+ 사용자 정정) | 고른 방 = **서버 저장·정본**, **방 «목록 탐색»만 Rust 로컬**. `POST/DELETE /api/integrations/{id}/rooms`(슬랙·카톡 공통, 웹에서도 가능) · handshake 가 **서버의 고른 방(`selected_rooms`)을 내려줌** · 업로드 403 = **서버 고른 방 기준**(매니페스트 걷음) · `rooms/report`·`available-rooms`(카톡) 제거 · D-15 는 「방 목록이 로컬」로 좁혀 읽음 | S8 §2.5·§4.3·§4.6·대응표 D-15 · S9 §3.1·3.2·§4·AC-05 |
| **R-F2** | medi-ax **닫기 = 숨기기**(메뉴 막대 상주)·**숨김에서 L-06 점유 해제**(L-06 을 「창 숨김」까지 확장) · **OQ-T10 닫힘** · 수집기 인증 = **장수명 기기 토큰**(창 쿠키 아님)이라 창 닫아도 수집 이어짐 | S6 「외부 채널 수집기 수용」 불변식 표·수집기 인증 절·OQ-T10 · S9 §2.1·§4 인증 |

## 새 WARN (N-1~N-12)

| # | 어떻게 고쳤나 | 어디 |
|---|---|---|
| N-1 | 메일 connect **409 없음**(계정 여럿) · 슬랙만 409 · 같은 주소 재연결은 콜백 D-46 | S8 §4.2 · AC-01c |
| N-2 | 콜백 302 = **쿼리**(`?surface=settings&tab=…&connect=ok`, 라우터 없는 SPA) · local-stack 이 `AX_WEB_ORIGIN=127.0.0.1:5176` 넘김 | S8 §4.2 · AC-01b |
| N-3 | 동의 뒤 앱 창이 **`focus`/`visibilitychange`** 때 `GET /api/integrations` 재조회(또는 WS 사건) | S8 §4.2 · AC-01b |
| N-4 | 샌드박스 토큰 = **`allow-same-origin allow-popups allow-popups-to-escape-sandbox` · `allow-scripts` 금지** · 높이 postMessage · 인용 접기 = `<details>` | S8 §2.1 · AC-08b |
| N-5 | 이미지 프록시 경로 `GET …/mail/{id}/remote-image?u=` + **SSRF 규칙**(본문 URL만·http(s)·사설/루프백/메타데이터 거절·이미지 MIME·크기 상한) | S8 §4.4 · AC-08b |
| N-6 | 실시간 = **새 사용자 WS `/api/inbox/stream`**(회의 WS 아님) + **워커→back Postgres `LISTEN/NOTIFY`** · 사용자 사건 채널로 | S8 §4.4 · AC-10b |
| N-7 | **`GET /api/integrations/{id}/rooms`** = 고른 방(서버 정본) 목록 | S8 §4.3 · §2.5 |
| N-8 | `aid` = **`(chatId, logId, seq)` 결정식**(앱·서버 같은 규칙) · 응답 `[{logId, seq, aid}]` · 요청 `seq` | S8 §4.6 · S9 §4 · AC-15 |
| N-9 | 첨부 경로 **메일/방으로 가름**(`mail/{id}/attachments`·`rooms/{id}/attachments`) · 202 결과는 WS 사건 · handshake `reset_at` | S8 §4.4·§4.6 |
| N-10 | **판 가르기 = cargo feature `kakao-collector`**(런타임 identifier 아님) · capabilities 판별 · 오버레이 키 시험(`lib.rs:841-846`) 개정 명시 | S6 「판 가르기 수단」·AC 표 |
| N-11 | 시스템 설정 **딥링크는 수집기 네이티브가 직접**(`open_external` http(s) 전용 그대로) · **FDA = 사용자 TCC 허용**(plist 키 아님) · 읽기 실패로 `reason=permission` | S9 §2.1 · S6 불변식 표 |
| N-12 | 화면 문구 = **medi-ax/중립 「데스크톱 앱」** · `login_required` = **앱 로컬 표식**(서버가 아니라 앱이 띄움) · S8 §1 표·경계 문장 정리 | S8 §2.5·§1·§5 · S9 §2.1·§4 |

## 앞 판 부분 해소

- **W-6**(SPEC-006 개정 범위) → S6 v0.5.0 이 I-2·창·트레이·백그라운드·FDA·AC-T23/T33/T47·`trayIcon`·오버레이 키 시험·
  닫기=숨기기·카톡 커맨드·판 가르기까지 전수. S9 §1 관계 표가 가리킴
- **W-5**(인증 수명) → 기기 토큰 채택으로 **닫힘**(OQ-906)

## 사용자 결정 (정정 포함)

- 고른 방 = **서버 저장·정본**, 목록 탐색만 Rust 로컬(정정) · 기기 토큰(OQ-906) · 닫기=숨기기(R-F2) ·
  「Mac 앱 받기」 = Strong_hajin GitHub Releases(OQ-811) · 딥링크 네이티브(N-11)

## 열린 것

- **없음.** OQ-811·OQ-906 닫힘. SPEC-008 OQ-801~808·811 닫힘 · SPEC-009 OQ-901~906 닫힘

## 범위 밖(다른 문서 몫)

- 인프라 레포 `k8s_infra_mac` 차트·Secret·ingress·worker.kinds — `30-work/`·운영 (S8 §5)
- SPEC-009 DB 여는 절차(키·userId·복호) — 구현 몫, mykakao SPEC-001 참조
- DEC-008 은 이번 판에서 손대지 않음(지시대로)
