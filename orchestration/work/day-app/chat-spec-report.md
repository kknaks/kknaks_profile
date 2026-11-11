# chat-spec 결과 보고 — DAY-SPEC-004 직원 내부 채팅 초안

## 상태: done (SPEC 단계만 · WP · 코드 · 서버 · GitHub · 커밋 · 하위 위임 없음)

- 스펙 트리 `day-app-spec` HEAD `06239a1c7d45e95a02e5aab61b9d29bea6b7aca3` 위 미커밋 · origin/main `9692e1fb461bf8c4e52bf489e37ab8ff875f9918`
- 원천: cc-prototype `77173cf8b62f0b27ec54ec4ee22e9d308b7f701e` 를 `git show` 로만 읽음(checkout · pull · 편집 0) · CENTURION_DAY day-app `b6c034bfa239bd4f12f1a29c6e58c74d82c87de6` read-only · 코디 후속 4건(사용자 두 결정 확정 · 채팅 푸시 누락 없이 · 저장소는 기존 architecture 확정 · SPEC-000 device 최소 개정 허용) 반영 · ack 완료

## 변경 파일 (편집 경계 안)

| 파일 | 변경 |
|---|---|
| `products/day/20-spec/spec-004-internal-chat.md` | **신규** · `id: DAY-SPEC-004` · `doc_no: DAY-DOC-8` · `status: draft` · `owner: TBD` · `version: 0.0.1` |
| `products/day/20-spec/spec-003-mobile-app.md` | U-2 「채팅」 bullet 끝 · §1 뺌 행 끝에 DAY-SPEC-004 연결 문장만(「자리만」 계약 무변경) |
| `products/day/20-spec.md` | In Scope 1줄 · Out Of Scope 에서 「채팅 기능」 뺌 · SPEC Bundle · SPEC List · 영역별 읽는 순서 각 1행 |
| `products/day/30-work.md` | Spec Coverage 1행(DAY-SPEC-004 · 미발주 · 기존 #235 갱신 예정 · proposed) |
| `products/day/20-spec/spec-000-data-model.md` | **코디 허용 확대로 `device` 절만** — `last_updated` 2026-11-10 · 07 「정한 것」 개정 1줄 · `device` 표 5칸 추가 + 「device 규칙」(아래) · 다른 테이블 · 주제 무변경 |
| `products/day/20-spec/spec-003-mobile-app.md`(추가) | §3 「푸시」 `DELETE` 줄에 「요청 세션에 이어진 경우만」 · D-2 칸 변경 문장을 SPEC-000 개정 참조로 |

- SPEC-004 번호: 현재 브랜치 · origin/main · `origin/kknaksss/day-app-spec` · `origin/kknaksss/day-procedure-board-2-spec` · 옆 spec 워크트리 모두 spec-000 ~ 003 뿐 → 사용 가능.
- doc_no: products/day 현행 max = DAY-DOC-7(SPEC-003) · origin/main · 옆 브랜치 max = DAY-DOC-6 → **DAY-DOC-8**. 옆 브랜치가 머지 전에 DOC-8 을 쓰면 충돌 — 머지 때 doc_no 전수 확인 필요.
- SPEC-001 · 002 · log.md · 10-decision · architecture · 코드 무수정(SPEC-000 은 device 절만).

## SPEC-004 구성

개요(원천 · 사용자 확정 · 정직 표기 「서버엔 테이블만」) · 범위 넣음/뺌 · Placement · Wireframe(폰 목록/대화/길게 누르기 · 아이패드 두 칸 · 첨부 시트 · 공유 시트 · 방 정보 · 모아보기) · 문구 원칙 · U-1 ~ U-8 · S-1 ~ S-5 · 용어 · 권한·격리 · API 21(프로토 20 + 채팅 스트림) · 응답 모양 · 규칙 표 · 오류 code·글자 표 · 첨부 저장·열기 · 실시간 · 채팅 푸시(최소 기기 등록·발송) · 케이스 매트릭스 · Flow · Lifecycle · Frontend/Backend 구현 규칙 · Functional Rule · 프로토와 다른 곳 · 서버 의존 C-1 ~ C-4 · 인수 조건 C-A1 ~ C-A17 · OQ.

## 원천 기능 대비 매핑 (누락 0 확인)

| 원천 기능(77173cf8) | SPEC-004 |
|---|---|
| 셸 탭 「채팅」 · 안 읽은 방 수 배지 99+ (A/screens/shell.dart:2 · 244-261) | Placement · U-1 탭 배지(4메뉴 자리로 — 5번째 탭 아님) |
| 방 목록 행 · 시각 · 미리보기 · 빈 목록 · 아이패드 360 + 오른쪽 칸 (chat_list_screen · chat_ui:23 · chat_view:17-56) | U-1 |
| 새 대화 1:1/그룹 · 그룹 이름 · 최대 20 · 초성 검색 (chat_new_screen · chat_search) | U-3 · API #1 #3 #4 |
| 초대(그룹 · 1:1 → 새 그룹) · 「이미 참여 중」 · 시스템 줄 (chat_new_screen:3-5 · service:186-190 · 279-308) | U-3 · 규칙 「초대」 |
| 대화 말풍선 · 날짜 구분선 · 그룹 이름 묶기 · 위로 더 · 따라 내려가기 · 키보드 (chat_room_screen:1-3 · 110-116 · 228-251 · chat_view:58-88) | U-2 |
| 링크 → 기기 브라우저 (chat_view:127-128 · chat_link) | U-2 · 격리 |
| 보내기 · 보내는 중 · 실패 · 다시 보내기 · clientId (chat_room_screen:421-435 · chat_state:627-666 · chat_view:103) | U-2 · 규칙 「보내기」 · C-A5 |
| 여러 개 보내기 · 진행 글자 (chat_state:554-618 · chat_room_screen:404 · 560) | U-2 · U-6 · C-A9 |
| 비활성 상대 1:1 (chat_room_screen:676 · service:386-392) | U-2 · 권한 · C-A3 |
| 길게 누르기 메뉴 5종 · 선택 복사 · 복사 토스트 (chat_room_screen:441-500 · 789-854) | U-4 |
| 수정 모드 · 「수정됨」 · 실패 (chat_room_screen:513-631 · service:579-609) | U-4 · 규칙 「수정」 · C-A7 |
| 삭제 확인 · 소프트 · 파일 마지막 참조 (chat_room_screen:508 · service:547-577) | U-4 · 규칙 「삭제」 · C-A7 |
| 전달(공유 시트 · 칩 · 10곳 · 결과 처리 · 같은 파일) (chat_forward_sheet · service:459-545) | U-5 · API #14 · C-A8 |
| [+] 시트 · 최근 줄 · 카메라 칸 · 「사진」 메뉴 · 권한 안내 (chat_attach_sheet · chat_room_screen:147-174) | U-6 |
| 사진 2048/85 JPEG · 동영상 네이티브 변환 · 3분 · 90MB · 썸네일 (photo_pick · video_pick) | U-6 · 첨부 저장 · C-A9 |
| 크게 보기 · 재생(Range · 디스크 없음 · 무음 스위치) (chat_photo_screen · chat_video_screen) | U-6 · C-A10 |
| 방 정보(알림 · 사진·동영상 · 참여자 · 초대 · 나가기 · 숨기기) · 아이패드 오른쪽 시트 420 (chat_info_screen · chat_ui:150) | U-7 · API #5 ~ #8 · C-A4 |
| 모아보기 3열 · 60 · 빈/실패/다시 시도 (chat_media_screen · service:373-384) | U-7 · API #10 |
| 읽음 · 보고 있는 방 · 1초 묶음 (chat_state:329-396 · service:611-631) | U-2 · API #15 · C-A6 · C-A12 |
| 앱 안 배너 4초 · messageId 한 번 · [보기] (chat_state:509-531 · shell:268-290 · chat_model:325-331) | U-8 · C-A13 |
| SSE 5종 · 끊긴 동안 메우기 · 경계 바뀐 방 처음부터 (service:166-172 · chat_state:290-327 · 403-507) | 실시간 · S-5 · C-A11 |
| 채팅 푸시(받는 사람 · 본문 · thread-id · 1일 만료 · notification 행 없음 · 앞에서 = 배너 · 누르면 방) (push.py:32-45 · 165-196 · A/push/push.dart · app_state:214-233) | 채팅 푸시 · U-8 · C-A14 |
| 로그아웃 · 계정 바뀜 비우기 · 푸시 열기 요청 보존 (chat_state:761-763 · app_state:291 · 432) | U-8 · 케이스 매트릭스 · C-A15 |
| 서버 API 20 · 오류 코드 · 제한값(2000 · 40 · 20 · 50 · 60 · 100 · 10 · 5MB · 90MB · 3분) (api/chat.py · service/chat.py:33-48) | API · 규칙 · 오류 표 |
| 법적 검토 표시(보존 기간 · 열람 로그 · 잠금 화면) (service:3 · api:156 · push.py:38) | 첨부 · 푸시 · OQ-C10(DAY-ESC-001 참조만) |

뺀 것은 원천에도 없는 기능(그룹 이름 바꾸기 · 강퇴 · 이모지 · 공유 시트 · 저장)과 사용자 범위 밖(알림센터 · Android · 호출 정책)뿐 — §1 「뺌」에 근거와 함께.

## 사용자 확정 반영 (OQ 두 건 닫음)

- OQ-C1 「채팅 상대는 같은 병원 활성 직원」 → §3 「권한 · 격리」: 세션 병원 · `staff.is_active` · 시스템 계정 제외 · `account_id` · `account.is_active` · 비밀번호 무관 · 직무 무관 · `board` 무관 · 다른 병원/비활성/나간 멤버 서버 차단(없는 것처럼 404 · 내 staff 비활성 403) · C-A1 · C-A2.
- OQ-C2 「백엔드 우리가 가면 돼」 → §4 Backend · 서버 의존 C-1 · C-2: 이 Delivery 가 채팅 서버 · 채팅에 필요한 기기 등록 · APNs 발송까지 구현(SPEC 은 계약만 · 구현/완료 주장 없음).

## 서버 · 앱 구현 의존

- 서버(이 Delivery · 아직 미구현): 채팅 HTTP 20 · `/api/chat/stream` · 첨부 저장(Azure Blob / 로컬 디스크) · 기기 등록 `PUT/DELETE /api/devices/{install_id}`(SPEC-003 계약) · 채팅 푸시 발송(APNs 직접).
- 앱: 프로토 화면 이식 · DAY 셸 · 세션 · 오류 표 · 스트림 · 기존 푸시 코드에 `kind = chat` 처리.
- 사용자: APNs 키 · Apple App ID/Push · 서명 · 실기기 · 저장소(Blob) 설정 · 운영 앞단 본문 한도.

## SPEC-000 `device` 최소 개정 (OQ-C6 닫음 · 코디 지시로 같은 문서 리뷰 묶음)

- 근거: 옛 `device` = `account_id` · `install_id` · `push_token` · `name · kind` · `last_seen_at` 뿐(세션 · 병원 · 앱 id · 푸시 환경 · platform 없음) · SPEC-003 §3 「푸시」 D-2 와 mobile-deployment M-10 이 「SPEC-000 개정 필요」로 남겨 둔 자리.
- 추가 칸: `login_session_id`(FK · **서버가 등록 요청 Bearer 세션으로 채움** · 병원 · 직원은 그 세션) · `push_token_hash`(SHA-256 · 색인 · 암호화 칸 검색 불가라 「토큰 하나 = 연결 하나」용) · `platform`(enum ios) · `app_id` · `push_env`(production · sandbox) — 모두 DB null 허용 · 등록 API 는 필수.
- 규칙: 등록 = 요청 세션으로 덮어씀 · 같은 토큰의 다른 설치 연결 끊음(한 tx) / **해제 = 요청 세션에 이어진 경우만 비움 → 늦은 이전 로그아웃 DELETE 가 새 등록을 지우지 않음** / 보내기 대상 = 살아 있는 세션 · 칸 다 있음 · **세션 병원 = 그 일의 병원**(계정 다중 병원 격리) · 받는 사람 규칙은 각 SPEC 그대로 / 환경 칸 없음(dev · prod DB 분리) / migration = null 허용 추가만 · 옛 행은 세션 null 이라 보내기 대상 아님 · 다음 PUT 때 채워짐.
- SPEC-003 정합: `DELETE` 줄 · D-2 문장만 고침(원장 호출 받는 사람 정책 무변경).
- 주의: 옆 브랜치(day-procedure-board-2-spec · PR #920)도 SPEC-000 을 고쳤다(`crm_connection.is_demo` 등 — device 절 아님). 머지 때 SPEC-000 충돌 · `last_updated` 확인 필요.
- 첨부 저장소 종류는 새 OQ 로 만들지 않았다 — system.md 「Azure Blob(로컬 디스크) 기본값」 그대로 · 리소스 · 키만 사용자(서버 의존 C-3).

## 남은 OQ (구현 확인 · 기본값 진행)

- (OQ-C6 은 위 개정으로 닫음)
- OQ-C3 역할 Badge 색 ↔ DAY 직무 태그 · OQ-C4 첨부 한도 vs DAY 앞단 본문 한도 · OQ-C5 크기 초과 413 · OQ-C8 채팅 전용 스트림.
- OQ-C7 닫음(코디 지시): 사진 보관함 문구 = 프로토 Info.plist:74 원문 · 카메라 문구 = Info.plist:70 원문에서 「여권 사진면을 찍거나 」만 삭제 → 「채팅으로 보낼 사진을 찍기 위해 카메라를 사용합니다. 찍은 사진은 사진첩에 저장하지 않습니다.」 · 채널 이름 DAY 규칙 — SPEC-004 §4 Frontend.

## 확인 불가 원천

- 프로토 채팅 SPEC(SPEC-007 internal-chat) 원문 — 보관 기록이 가리키는 경로에 없음(OQ-C9). 코드 주석의 `§` · `D9-` · `OQ-9xx` 는 위치 표시로만 쓰고 원문 인용 0.
- 실행 · 빌드 · 서버 · 기기 확인 0(정적 읽기만). 프로토 시험 수(앱 7파일 110 · 서버 5파일 58 케이스)는 세기만 했고 돌리지 않음.

## 검증

- `python3 scripts/lint-pipeline.py --strict` 1회 → exit 0 · **0 error, 263 warning** · `products/day/` 해당 **0건**(경고는 전부 다른 제품의 기존 것)
- `git diff --check` 통과
- 편집 경계: `git status` = `20-spec.md` · `spec-000-data-model.md`(device 절 · 코디 확대 허용) · `spec-003-mobile-app.md` · `30-work.md` 수정 + `spec-004-internal-chat.md` 신규 — 모두 허용 목록 안
- lint 는 SPEC-000 개정 뒤 한 번 더 확인 → 같은 결과(0 error · products/day 0)

## 다음

- 독립 문서 리뷰(SPEC-004 + SPEC-000 device 개정 + SPEC-003 연결) → 기존 #235 WP 갱신 → 서버 · 앱 구현 → 각 리뷰. 이번 발주는 여기까지.
