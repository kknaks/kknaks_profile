# 리뷰 리포트 — day-app 직원 내부 채팅 SPEC(DAY-SPEC-004 신규 · SPEC-000 device 개정 · SPEC-003 연결 · 인덱스/coverage) / doc (2026-11-10)

- 대상:
  - 스펙 트리 `day-app-spec` HEAD `06239a1c` 위 미커밋 — `spec-004-internal-chat.md`(신규 581줄) · `spec-000-data-model.md`(+16/−2 · device 절) · `spec-003-mobile-app.md`(±4) · `20-spec.md`(+5/−1) · `30-work.md`(+1)
- 원천:
  - `chat-spec-brief.md` · `chat-decisions-20261110.md`(사용자 확정 2건 · 코디 `msg_c7bb47e0e0e2` device 허용 · 저장소 = system.md 기본값) · `chat-spec-report.md`
  - 프로토 cc-prototype `77173cf8b62f0b27ec54ec4ee22e9d308b7f701e`(`git show`만)
  - DAY 코드 day-app `b6c034bf` `backend/day/models/misc.py` · `_columns.py`(읽기만)
- 방법:
  - diff 전수 대조 · 프로토 원문 줄 표본 대조 — 오류 code · 글자 28개, 상수, push 받는 사람, 이벤트, UI 글자 11개, Info.plist
  - DAY 모델 대조 · lint 1회 · `git diff --check`
  - 수정 · 하위 위임 없음

## 판정: WARN (FAIL 0 · WARN 3)

원천 기능 매핑은 충실하다: 1:1 · 그룹 · 초대 · 나가기 · 숨기기 · 음소거 · 읽음 · 수정 · 삭제 · 전달 · 검색 · 사진 · 동영상 · 모아보기 · 푸시 · 배너 · 배지 모두.

- **문구**: 표본 전부가 프로토 원문 줄과 일치하고 새 글자는 없다.
- **사용자 확정 반영**: 같은 병원 활성 직원 전체, 비밀번호 · 직무 · `board` 무관, 이 세션 서버 구현.
- **API 계약**: 21개의 요청 · 응답 · uuid/`seq`/`clientId`/`beforeSeq`/`since` · 오류 · 재접속 메우기 · 병원 격리 · 세션 교체 비움 · 동시성이 DAY 모델(`chat_*` 테이블 · 유일 색인)과 맞다.
- **정직 표기**: 「서버 테이블만 · 제안 계약」이다.
- **채팅 푸시**: D2를 핑계로 빼지 않고 이 Delivery 범위로 계약했다. 키 · Apple 등록은 사용자 설정으로 분리했다.
- **DAY-ESC-001**: 참조 · 비차단만이다.
- **SPEC-000 device 개정**: 코디 허용 범위(device 절만)이고 숨은 다른 모델 변경은 없다.

WARN 3건은 문서 안 수치 불일치 1건, SPEC-003과의 권한 충돌 1건, 표시 규칙 모호 1건이다.

## FAIL

없음.

## WARN

### W1. 실시간 이벤트 수가 표와 다르다 — 「5종」 3곳 vs 표 6종
- 위치: `spec-004-internal-chat.md:60` 「실시간 이벤트 5종」 · `:305` API #21 「이벤트 5종 + session_expired」 · `:538` C-A11 「스트림 이벤트 5종」 ↔ `:390-397` 표 = `chat_message` · `chat_message_edited` · `chat_message_deleted` · `chat_room` · `chat_room_removed` · `chat_read` **6종**
- 원천: 프로토 서버 B/`service/chat.py:168 · 272 · 325 · 339 · 577 · 608 · 630`(6종 emit) · 앱 A/`chat/chat_state.dart:406-432` `case` 6종
- 영향: 인수 조건 C-A11이 「5종」이라 다기기 읽음 맞춤 `chat_read`가 검증 · 구현에서 빠질 수 있다(누락 판정 근거가 흐려짐).
- 최소 정정: 세 자리를 「6종」(또는 이름 나열)으로 고친다.

### W2. SPEC-003의 「알림 · 마이크 외 권한 없음」과 SPEC-004의 카메라 · 사진 권한 추가가 충돌한다
- 위치:
  - `spec-004-internal-chat.md:474-476` 「DAY-SPEC-003 §4의 「알림 · 마이크만」을 채팅 범위만큼 넓힘」 + NSCamera/NSPhotoLibrary 문구
  - ↔ `spec-003-mobile-app.md:637` 「알림 · 마이크만 … 카메라 · 사진 … 넣지 않는다」 · `:715` A-17 「알림 · 마이크 외 권한 없음」
- 원천: 사용자 「채팅 기능 스펙부터 앱 구현까지」(사진 · 동영상 포함) · 프로토 Info.plist:70 · 74
- 영향: 같은 앱 바이너리라 채팅 구현이 들어가면 SPEC-003 A-17(빌드 검사)이 실패로 판정된다. SPEC-003 쪽 연결이 U-2 · §1 뺌만 고쳐 권한 줄은 옛 계약 그대로다.
- 최소 정정(브리프 허용 「SPEC-003 채팅 연결만」 범위): `spec-003:637`과 A-17에 「채팅의 카메라 · 사진 보관함 = DAY-SPEC-004 §4(그 SPEC 승인 · 구현 뒤)」 한 구절을 단다. mobile-deployment §5-3 권한 목록도 같은 후속 대상으로 보고서에 적는다(이번 편집 경계 밖).

### W3. 채팅 화면의 스트림 끊김 표시가 자기 모순이다
- 위치: `spec-004-internal-chat.md:432` 케이스 매트릭스 「스트림 끊김 | 노란 줄 없이(채팅 화면엔 DAY-SPEC-003 끊김 줄 규칙 그대로)」
- 원천: DAY-SPEC-003 U-12 끊김 규칙 = 머리 아래 노란 줄 「연결 끊김 · 다시 연결 중」(시술 현황 스트림)
- 영향: 「노란 줄 없음」과 「끊김 줄 규칙 그대로」가 한 칸에 함께 있다. 채팅 전용 스트림이 끊길 때 채팅 탭에 노란 줄을 보일지 앱 워커가 추측해야 한다.
- 최소 정정: 프로토 동작(판 스트림 공용 줄)과 DAY 별도 스트림 구조를 보고 하나로 적는다. 예: 「채팅 스트림 끊김 = DAY-SPEC-003 U-12와 같은 노란 줄(같은 글자)」 또는 「줄 없음 · 재연결 뒤 메우기만」. 원문이 없으면 UI 선택 OQ로 둔다.

## 원천 대조 실측 (표본)

| 항목 | 결과 |
|---|---|
| 오류 code · 글자 28개(`chat_room_not_found` ~ `photo_disabled`) | B/`service/chat.py` 해당 줄 원문과 전부 일치(HTTP · 글자 · 줄 번호) |
| 상수 | MAX_TEXT 2000 · MAX_TITLE 40 · GROUP 2 ~ 19(나 포함 3 ~ 20) · ROOM_MAX 20 · PAGE 50 · GRID 60 · PREVIEW 100 · VIDEO 90MB · 180000ms · FORWARD 10 — SPEC 값과 일치 |
| API 수 | 프로토 `api/chat.py` 라우트 20개 = SPEC #1 ~ #20 · #21 채팅 스트림은 DAY 추가로 명시 |
| 푸시 | 받는 사람(멤버 − 보낸 사람 − 알림 끔 − 비활성 − 경계 안 · 숨긴 1:1 포함) · 시스템/지운 것 제외 · `thread-id` · 1일 만료 · 본문 규칙 · `notification` 미사용 — B/`service/push.py:32-45 · 167-196`과 일치. DAY는 `environment` · `hospitalId` · 세션 병원 기기 필터만 더함 |
| UI 글자 표본 11개 | 「비활성 계정이에요」 · 「복사했어요」 · 「메시지를 삭제할까요?」 · 빈 목록 · 「10곳까지」 · 숨기기 안내 · 모아보기 빈 · 「90MB」 · 「찾는 직원이 없어요」 · 사진 접근 안내 · 「왼쪽에서 대화를 골라 주세요」 — 인용 줄과 일치 |
| Info.plist | :74 사진 원문 그대로 · :70 카메라는 「여권 사진면을 찍거나 」만 뺌(코디 정합 · 새 글자 없음) |

## DAY 모델 · 계약 정합

| 확인 | 결과 |
|---|---|
| 채팅 테이블 | `ChatRoom.last_seq` · `live_unique(hospital_id, direct_key)` · `ChatMember`(from_seq · last_read_seq · is_muted · hidden_at · left_at · last_viewed_at) · `ChatMessage` `live_unique(room_id, seq)` · `(account_id, client_id)` · `ChatAttachment`(room_id · account_id · message_id nullable · file_key · thumb_file_key · sha256) — SPEC 규칙(붙기 전 첨부 · seq · 1:1 병원 유일 · clientId 멱등)과 맞다. 채팅 테이블 칸 추가 요구 없음 |
| SPEC-000 device 개정 | `login_session_id`(서버가 채움) · `push_token_hash` · `platform` · `app_id` · `push_env` 모두 null 허용 추가 · 등록/해제(요청 세션일 때만)/보내기 대상(살아 있는 세션 · 세션 병원 = 일의 병원)/옛 행 규칙. `login_session`에 `hospital_id` · `staff_id` · `revoked_at` · `expires_at` 실재(SPEC-000 :634-646). 환경 칸 없음(DB 분리) 근거 있음. 다른 테이블 · 주제 무변경 — 허용 범위 안 |
| SPEC-003 연결 | U-2 「채팅 = SPEC-004 · 승인 · 구현 전 자리만 그대로」 · §1 뺌 꼬리 · §3 `DELETE` 「요청 세션일 때만」 · D-2 문장 → SPEC-000 개정 참조. 원장 호출 받는 사람(U-14) 무변경 |
| 인덱스 · coverage | `20-spec.md` In Scope · Out(「채팅 기능」 제거) · Bundle · List(draft) · 읽는 순서 각 1행 · `30-work.md` Coverage 1행(미발주 · proposed) — lint 통과 |
| 정책 범위 | Android · FCM · 알림센터 · 원장/상담사 호출 정책 · 새 권한 키 없음 · DAY-ESC-001 참조만(OQ-C10) |
| 미결 구분 | 닫음 OQ-C1 · C2 · C7 · C6(사용자/코디 근거) · 구현 확인 OQ-C3 · C4 · C5 · C8(기본값) · 원천 확인 불가 OQ-C9 · 법적 OQ-C10 — 실제 미결과 구현 선택이 구분돼 있다 |
| 인수 조건 | C-A1 ~ C-A18 — 서버 단위/API · 앱 더블 · 로컬/실기기로 각각 검증 가능(W1 수치만 정정) |

## 참고 (결함 아님 · 구현 때 유의)

1. **clientId 멱등과 소프트 삭제**: DAY 유일 색인은 `live_unique`(= `deleted_at IS NULL`)라 `(account_id, client_id)`가 지운 행에는 걸리지 않는다(`_columns.py:74-84`). 다른 기기에서 지운 뒤 같은 `clientId`로 다시 보내면 새 메시지가 생길 수 있다. 구현은 멱등 조회를 지운 행 포함으로 하거나, SPEC 「동시성」 줄의 「유일 제약으로 하나만」을 「살아 있는 행 기준」으로 한 구절 보강하면 된다.
2. **`push_token_hash`는 유일 제약이 아니다**: 같은 토큰으로 두 설치가 동시에 `PUT`하면 둘 다 이어질 수 있다. 「한 트랜잭션」만으로는 경합이 남으므로 구현 때 행 잠금 또는 유일 부분 색인을 선택한다(구현 상세).
3. **원장 호출 푸시에도 「세션 병원 = 일의 병원」 기기 필터가 적용된다**(SPEC-000 device 규칙). 받는 사람(계정) 정책은 그대로이고 기기만 좁힌다 — 정책 확장이 아니라 격리 강화다. WP에서 원장 호출 푸시 회귀 대상으로 적어 두면 좋다.
4. 프로토 Info.plist에는 `PHPhotoLibraryPreventAutomaticLimitedAccessAlert = true`도 있다(:72-73). 「제한 접근이면 「더 고르기」」 동작과 묶이는 키라 구현 때 같이 옮길지 확인한다.
5. `doc_no DAY-DOC-8` — 옆 브랜치(PR #920) 머지 전후 doc_no 충돌 전수 확인 필요(planner 보고와 같은 주의).

## 검증 (실결과)

- `python3 scripts/lint-pipeline.py --strict` 1회 → exit 0 · **0 error, 263 warning** · `products/day/` **0건**(경고는 타 제품 기존분 · 무관)
- `git diff --check` → 출력 없음 · exit 0
- 편집 경계: `git status` = M `20-spec.md` · `spec-000-data-model.md`(device 절만) · `spec-003-mobile-app.md`(채팅 연결 · 푸시 DELETE · D-2 문장) · `30-work.md`(Coverage 1행) + ?? `spec-004-internal-chat.md` — 모두 허용 목록(코디 확대 포함) 안 · 코드 · 서버 · 다른 SPEC 무변경

## 남은 것

- planner: W1(「6종」) · W2(SPEC-003 :637 · A-17 연결 구절) · W3(끊김 표시 한 가지로) 최소 정정 → 재검수.
- 그 뒤: 기존 #235 WP 갱신 → 서버 · 앱 구현 → 각 리뷰. 사용자 설정(APNs 키 · App ID · 서명 · Blob 리소스) · 배포 본문 한도 확인(OQ-C4)은 별도.
