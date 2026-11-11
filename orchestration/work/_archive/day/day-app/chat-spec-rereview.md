# 리뷰 리포트 — day-app 채팅 SPEC W1 ~ W3 + 코디 기기 · 멱등 경계 정정 재검수 / doc (2026-11-10)

- 대상:
  - 스펙 트리 `06239a1c` 위 미커밋 — `spec-004-internal-chat.md`(신규 · draft → stable) · `spec-000-data-model.md`(device 절) · `spec-003-mobile-app.md` · `20-spec.md` · `30-work.md`
- 근거:
  - 앞 리뷰 `chat-spec-review.md` W1 ~ W3 · 참고 1 · 2 · 4 · 5
  - `chat-spec-fix-brief.md`(코디 후속 1 · 2 · status 정리 지시)
  - `chat-spec-fix-report.md`
  - 프로토 `77173cf8` `git show`(read-only)
- 방법:
  - 수정 문장 직접 대조 · 프로토 근거 줄 확인
  - lint 1회 · `git diff --check`
  - 수정 · 하위 위임 없음

## 판정: PASS (FAIL 0 · WARN 0)

| 지적 · 지시 | 수정 실물 | 결과 |
|---|---|---|
| W1 이벤트 수 | `spec-004:60` 「6종」 · `:306` API #21 「이벤트 6종(아래 표)」 · `:540` C-A11 6종 이름 나열(`chat_read` 포함). 「5종」 잔존 0 | PASS — 프로토 emit 6종 · 앱 `case` 6종과 일치 |
| W2 SPEC-003 권한 충돌 | `spec-003` §4 권한 줄에 「직원 채팅의 카메라 · 사진 보관함 권한(문구 · `PHPhotoLibraryPreventAutomaticLimitedAccessAlert`)은 DAY-SPEC-004 §4 · 그 SPEC 구현 때부터 · 여권 · 띄우기 · QR은 여전히 없음」 · A-17 「채팅 구현 뒤 SPEC-004 §4의 카메라 · 사진 보관함 권한만 더함」 | PASS — 빌드 검사 AC가 채팅 구현과 충돌하지 않음 · 다른 권한 확대 없음 |
| W3 끊김 표시 | `spec-004:433` 채팅 화면 머리 아래 DAY-SPEC-003 U-12와 같은 노란 줄 · 같은 글자(「연결 끊김 · 다시 연결 중」 · 「서버에 연결 중…」) · 기준 = 채팅 스트림 · 재연결 뒤 메우기 | PASS — 단일 규칙 · 새 글자 없음(SPEC-003 기존 원문) |
| clientId 멱등(지운 행 포함) | `:338` 「동시성 · 멱등」 — 지운 메시지 포함 처음 것 하나 · 재전송 = 처음 행(지운 모양) · 새 메시지 · 이벤트 · 푸시 0 · `live_unique`는 살아 있는 행만이라 조회 · 동시 판정은 지운 행 포함(방법 WP) · C-A5 보강 | PASS — 프로토 `repository/repo.py:734-737` `chat_message_by_client`가 `deleted_at` 조건 없이 조회 · `service/chat.py:440-441` 재사용과 일치(원천 동작 그대로) |
| 멱등 응답도 병원 검증 먼저 | `:278` 「멱등 응답도 검증 뒤」 — 재전송 · 이미 지운 것 삭제 · 같은 글 수정 · 읽음 0 · 전달 재전송 모두 세션 병원 = 방 병원 · 지금 멤버 · 경계 검증 뒤, 아니면 404 · 모든 경로 공통 · C-A5 「다른 병원 · 나간 방이면 404」 | PASS — 프로토 `service/chat.py:438-441` `_member`가 client 조회보다 먼저와 일치 |
| 늦은 이전 세션 `PUT` | SPEC-000 device 규칙 「늦은 이전 세션 등록 막기(서버 불변식)」 — 지금 결속 세션보다 먼저 만들어진 세션 요청 = 결속 · 토큰 무변경 + `{ok}` · 같은 세션 토큰 갱신 정상 · 동시 등록도 서버 `login_session` 생성 순서(동률 고정 판정)로 가장 나중 세션만 · 앱이 보낸 id · 시각 신뢰 0 · 구현 WP · SPEC-003 `PUT` 줄 · SPEC-004 「기기 ↔ 세션」 · C-A18 | PASS — 무시 응답 = 기존 `{ok}` 200(새 오류 코드 없음) · 새 권한 · 경로 없음 |
| 토큰 유일성 namespace | SPEC-000 「같은 토큰 = 연결 하나」 — (`platform`, `app_id`, `push_env`, `push_token_hash`) 안에서 이어진 살아 있는 행 늘 하나 · 동시 `PUT`도 결과 하나(원자적 · 방법 WP) · 다른 topic/환경 행 그대로 · `push_token_hash` 설명에서 「색인으로 보장」 표현 제거 · SPEC-003 `PUT` · C-A18 같은 뜻 | PASS — 관찰 결과로 보장을 적고 구현 수단은 WP로 |
| 참고 4 Info.plist 키 | `:478` `PHPhotoLibraryPreventAutomaticLimitedAccessAlert = true`(프로토 `Info.plist:72-73`)를 화면 동일 이식에 포함(보이는 글자 없음) | PASS |
| 참고 5 doc_no | planner read-only 확인: 옆 spec 트리 · PR #920 브랜치 · remote ref에 `DAY-DOC-8` 0건 → 번호 유지 · 머지 때 재확인 | PASS(사실 보고) |
| status | SPEC-004 `status: stable` · `20-spec.md` List stable · In Scope 「(draft)」 삭제 · SPEC-003 U-2 · §1 뺌의 SPEC-004 표기 stable(「구현 전」 · 「승인 · 구현되기 전까지 자리만」 유지). SPEC-000은 draft 그대로 · SPEC-003 stable 유지 · baseline pending · 머지 없음 | PASS — 코디 브리프 지시 범위 · lint 정합(`30-work.md` Coverage proposed · stable SPEC과 충돌 없음) |

## 경계 · 회귀

- SPEC-000 diff hunk = frontmatter `last_updated` + device 절(:944 ~ :973)뿐이다. 다른 테이블 · 주제는 무변경이다.
- SPEC-003 변경 = U-2 · §1 뺌 SPEC-004 표기 · §3 `PUT` / `DELETE` 줄 · D-2 문장 · §4 권한 줄 · A-17뿐이다. 원장 호출 받는 사람(U-14) · 시술현황 · 세션 · 환경 계약은 무변경이다.
- 앞 리뷰에서 PASS였던 원천 매핑 · 오류 code · 글자 · API · DAY 모델 정합 · 사용자 확정 · DAY-ESC-001 참조만은 그대로다. 새 제품 정책 · Android · 알림센터 · 원장 호출 정책 확장은 없다.

## 검증 (실결과)

- `python3 scripts/lint-pipeline.py --strict` 1회 → exit 0 · **0 error, 263 warning** · `products/day/` **0건**(경고는 타 제품 기존분)
- `git diff --check` → 출력 없음 · exit 0
- `git status` = M `20-spec.md` · `spec-000-data-model.md` · `spec-003-mobile-app.md` · `30-work.md` + ?? `spec-004-internal-chat.md` — 허용 5경로 안

## 남은 것 (결함 아님)

- mobile-deployment §5-3 권한 목록(알림 · 마이크)에 채팅 카메라 · 사진 반영 — 이번 편집 경계 밖 · 코디 판단(planner 보고와 같음).
- 원장 호출 푸시에도 「세션 병원 = 일의 병원」 기기 필터 — WP 회귀 대상으로 적기(격리 강화 · 받는 사람 정책 무변경).
- 기기 불변식(세션 순서 · 동률) · namespace 원자성 · clientId 지운 행 멱등의 구체 구현 = WP · 코드 단계.
- 다음: 개정 커밋(exact head) → 기존 #235 WP 갱신 → 독립 리뷰 → 서버 · 앱 구현.
