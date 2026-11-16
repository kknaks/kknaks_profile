# chat-spec-fix 결과 보고 — 채팅 SPEC 리뷰 W1 ~ W3 + 코디 기기/멱등 경계 정정 · SPEC-004 stable

## 상태: done (코드 · WP · GitHub · 커밋 · 하위 위임 없음 · HEAD 06239a1c 위 미커밋)

## 변경 (편집 경계 안 — 5경로 그대로)

| 파일 | before → after | 근거 |
|---|---|---|
| `spec-004-internal-chat.md` | `status: draft` → **stable** | 사용자 채팅 전체 구현 · 같은 병원 활성 직원 · 서버 이 세션 확정 + 이번 정정은 같은 계약(브리프) |
| 〃 W1 | 「실시간 이벤트 5종」 3곳(범위 표 · API #21 · C-A11) → **6종**(C-A11 은 이름 나열) | 리뷰 W1 · 프로토 B/`service/chat.py` emit 6종 · A/`chat_state.dart:406-432` |
| 〃 W3 | 케이스 「노란 줄 없이(… 끊김 줄 규칙 그대로)」 → 채팅 화면 머리 아래 **DAY-SPEC-003 U-12 와 같은 노란 줄 · 같은 글자**(「연결 끊김 · 다시 연결 중」 · 처음 「서버에 연결 중…」) · 기준 = 채팅 스트림 · 재연결 뒤 메우기 | 프로토 = 판 스트림 공용 줄 하나(A/`app_state.dart:104`) → DAY 채팅 독립 스트림에 같은 줄을 잇는 정합 · 새 글자 없음 |
| 〃 멱등 | 「동시성」 → 「동시성 · 멱등」: 같은 `clientId` 는 **지운 메시지 포함** 처음 것 하나 · 재전송 = 처음 행(지운 모양) · 새 메시지/이벤트/푸시 0 · DAY `live_unique(account_id, client_id)` 는 살아 있는 행만이라 조회 · 동시 판정은 지운 행 포함(방법은 WP) · C-A5 보강 | 프로토 `repository/repo.py:734-737`(deleted 조건 없이 조회) · `service/chat.py:440-441` · 리뷰 참고 1 |
| 〃 격리 | 「멱등 응답도 검증 뒤」 줄 추가 — 재전송 · 이미 지운 것 삭제 · 같은 글 수정 · 읽음 0 · 전달 재전송도 세션 병원 · 지금 멤버 · 경계 검증 먼저 · 아니면 404 · 모든 방/메시지/첨부 경로 공통 | 프로토 `_member` 가 client 조회보다 먼저(`service/chat.py:438-441`) |
| 〃 기기 | 「기기 ↔ 세션」 행 · C-A18 에 늦은 이전 세션 `PUT` 무시 · 토큰 유일 namespace(`platform`+`app_id`+`push_env`) · 동시 `PUT` 결과 하나 · 다른 topic/환경 행 그대로 | 코디 후속 1 · 2 |
| 〃 참고 4 | Frontend 권한에 `PHPhotoLibraryPreventAutomaticLimitedAccessAlert = true` 를 **화면 동일 이식에 포함**(최근 사진 · 「더 고르기」 권한 흐름 · 보이는 글자 없음) | 프로토 `Info.plist:72-73` |
| `spec-000-data-model.md`(device 절만) | `push_token_hash` 설명 「색인(유일 제약 아님)」 → 「이 칸만으로 유일성 보장한다고 보지 않음 · 방법은 WP」 · 등록 규칙에 ① **늦은 이전 세션 등록 막기 불변식** ② **같은 토큰 = 연결 하나 (platform, app_id, push_env, hash) 안 · 원자적 · 다른 topic/환경 그대로** | 코디 후속 1 · 2 · 리뷰 참고 2 |
| `spec-003-mobile-app.md` | W2: §4 권한 줄 · A-17 에 「직원 채팅 카메라 · 사진 보관함 = DAY-SPEC-004 §4(구현 때부터 · 여권 · 띄우기 · QR 은 여전히 없음)」 · §3 `PUT` 줄에 namespace · 늦은 세션 무시 한 구절 · U-2 / §1 뺌의 SPEC-004 표기 draft → stable | 리뷰 W2 · 코디 후속 |
| `20-spec.md` | SPEC List DAY-SPEC-004 draft → **stable** · In Scope 「(draft)」 삭제 | index 동기 |
| `30-work.md` | 무변경(앞 정정의 Coverage 1행 그대로) | — |

SPEC-000 은 기존 draft 그대로(전체 stable 아님) · SPEC-003 stable 유지 · canonical main baseline pending · 머지 없음.

## 코디 후속 결정 · 결과 (새 제품 정책 아님 — 기존 등록 계약의 경계)

1. **늦은 이전 세션 `PUT`** — 서버 불변식: 그 설치의 지금 결속 세션보다 먼저 만들어진 로그인 세션의 요청이면 결속 · 토큰 무변경 + `{ok}`(무시 응답 · 기존 응답 모양 · 앱은 화면에 띄우지 않음). 같은 세션 토큰 갱신 = 정상. 동시 등록도 서버가 믿는 세션 생성 순서(동률 = 서버 고정 판정)로 가장 나중 세션만 남음. 근거 = 서버 `login_session` 행만 · 앱이 보낸 세션 id/시각 신뢰 0(앱은 보내지 않음). 끝난 세션은 인증에서 401(DAY-SPEC-001). 구현(순서 · 동률 · 잠금) = WP. **결정: 무시 시 응답 `{ok}` 200**(409 등 새 오류 코드를 만들지 않음).
2. **토큰 유일성** — (platform, app_id, push_env, push_token_hash) 안에서 이어진 살아 있는 행은 늘 하나 · 동시 `PUT` 결과도 하나 · 다른 topic/환경의 같은 토큰 행은 해제하지 않음. 「hash 비유일 색인으로 보장」 표현 삭제 · 구체 방법(잠금 · 부분 유일 색인) = WP.
3. **clientId 멱등** — 지운 행 포함 · 원천 동작 그대로 · DAY live_unique 주의 보완.
4. **병원 검증** — 멱등 응답 경로도 검증 먼저(한 구절).
- 서버에 없는 권한 · API 를 덧붙이지 않았다(새 권한 키 · 새 경로 0).

## doc_no 확인 (read-only)

- `DAY-DOC-8`: 이 트리 외 어디에도 없음 — 옆 spec 워크트리(`day-procedure-board-2-spec` HEAD `bd029f3c`) 최대 DAY-DOC-6 · `origin/kknaksss/day-procedure-board-2-spec`(PR #920) 최대 DAY-DOC-6 · 모든 remote ref `git grep DAY-DOC-8` 0건. 번호 그대로 둠(사실만 보고 · 머지 때 재확인 권장).

## 검증 (최종 변경 뒤 1회)

- `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error, 263 warning** · `products/day/` **0건**(전체 출력은 scratchpad 로그 · 경고는 타 제품 기존분)
- `git diff --check` 통과
- 편집 경계: M `20-spec.md` · `spec-000-data-model.md`(device 절만) · `spec-003-mobile-app.md`(채팅 · 푸시 · 권한 연결만) · `30-work.md`(이번 무변경) + ?? `spec-004-internal-chat.md`
- 「5종」 잔존 0

## 정직 미결

- mobile-deployment §5-3 권한 목록(알림 · 마이크)도 채팅 카메라 · 사진을 반영해야 함 — 이번 편집 경계 밖(리뷰 W2 후속 · 코디 판단).
- OQ-C3 · C4 · C5 · C8(구현 확인 · 기본값) · OQ-C9 프로토 SPEC-007 원문 미확인 · OQ-C10 DAY-ESC-001 참조만 — 그대로.
- 원장 호출 푸시에도 「세션 병원 = 일의 병원」 기기 필터가 걸림(격리 강화 · 받는 사람 정책 무변경) — WP 회귀 대상(리뷰 참고 3).
- 기기 불변식 · 토큰 유일성 · clientId 지운 행 멱등의 구체 구현은 WP · 코드 단계(미실행).
