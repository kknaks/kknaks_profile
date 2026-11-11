# fix-spec-1 결과 보고 — 실기기 피드백 6건 + 배포 문서

## 상태: done

- 워크트리 `mediness-mediness/fix-spec`(`kknaksss/fix-spec`) · 범위 `products/day/` 만 · 커밋 · push · PR 0.
- 통역(피드백 5)은 손대지 않았다.
- frontmatter `version` 은 규칙대로 그대로 `0.0.1`(문서 개정으로 올리지 않음 — 개정 이력은 머리말 · `log.md`). `status` 그대로(SPEC-000 draft · 003 · 004 · 005 stable). `last_updated` 는 2026-11-11 로 바꿨다. `20-spec.md` · `30-work.md` 에는 스펙 버전 칸이 없다 → `20-spec.md` 최종 수정 · 채팅 범위 한 줄만 고쳤고 `30-work.md` 는 손대지 않았다.

## 바꾼 문서 · 절 (문서:줄 — 고친 뒤 기준)

| 문서 | 자리 |
|---|---|
| `20-spec/spec-003-mobile-app.md` | 머리 개정 ⑧ `:49` · §2 모두 완료 카드 · 확인 필요 와이어 `:156` · U-1 채팅 403 줄 `:211` · U-3 상자 5상태 `:238` · 「시술 모두 완료」 `:239` · 범위 · 겹침(서버 규칙) `:247-248` · 모두 완료 카드 [귀가 대기] `:250` · 확인 필요 표시 `:255` · 겹침 표 `:256` · U-4 5번 [귀가 대기] 조건 · U-9 `:357-358` · 케이스 매트릭스 403 줄 `:618` · 새 두 줄 `:625` · 프로토와 다른 곳 `:710` · A-33 `:785` · A-37 `:789` · 새 A-41 ~ A-43 `:793` · OQ-A21 `:853` · OQ-A29 `:859` · OQ-A35 닫음 `:871` · 새 절 OQ-A37 · OQ-A38 `:878` |
| `20-spec/spec-004-internal-chat.md` | 머리 2026-11-11 개정 `:28` · §1 넣음 2줄 `:60` · 뺌 2줄 · 와이어 `:122` · U-1 채팅 거절 `:155` · U-7 그룹 이름 `:215` · 바꾸기 절 `:218` · U-8 전체 알림 `:233` · API #22 `:325` · 규칙 알림 끄기 · 그룹 이름 바꾸기 `:349` · 실시간 `chat_room` `:416` · 푸시 받는 사람 `:431` · 제목 · 케이스 매트릭스 `:449` + 3줄 · 프로토와 다른 곳 `:537` · C-1 · C-A14 · 새 C-A19 ~ 21 `:574` · 새 OQ-C11 ~ 13 `:605` |
| `20-spec/spec-005-notifications.md` | 머리 2026-11-11 개정 `:30` · 「고치지 않는 것」 · 범위 2줄 · 와이어 「채팅」 `:101` · U-3 · 「채팅」 스위치 · 새 S-5 `:166` · 받는 종류 · `chat` 효과 `:221` · 케이스 매트릭스 `:257` · 프로토와 다른 곳 · N-A5 `:342` · 새 N-A13 `:343` · N-A10 · 새 OQ-N6 `:374` · 모델 대조 `:385` |
| `20-spec/spec-000-data-model.md` | 머리 2026-11-11 개정 `:31` · `notification_setting.kind` 값 `:1025` · `chat_room.title` `:1115` |
| `40-architecture/mobile-deployment.md` | 머리 개정 `:16` · §1 확정 4줄 `:30-45` · 새 §1-1 지금 상태 `:47` · §3 표 · 문단 · §5-1 표(+ 수출 규정 · 아이콘) · §5-2 · §5-4 · §6 Unlisted `:168` · §9 표 `:242` · §9-1 `:259` · §12 · §13 M-1 · M-2 · M-4 · M-16 `:313` · M-19 · 새 M-20 `:317` |
| `40-architecture/deployment.md` | env 표 5줄(`DAY_PUBLIC_API_BASE` `:163` · 데모 · APNs 셋 · APNs 키 파일 · 채팅 저장소) · Blob 행 `:187` |
| `20-spec.md` | 최종 수정 · 채팅 범위 한 줄 |
| `log.md` | 변경 이력 3줄(spec-change SPEC-003 · spec-change SPEC-004/005/000 · decision-add, arch-change 배포) |

## 피드백 ↔ 반영 자리

| # | 피드백 | 반영 | 찾아 고친 자리 수 |
|---|---|---|---|
| 1 · 4 | 목록 카드 「모두 완료」 상태 · [귀가 대기] | SPEC-003 U-3 다섯째 상태(글자 · 계산 = U-4 5번) · 모두 완료 카드 [귀가 대기] 줄(수락 자리 · `canHome` + `board` edit · 동작 = U-9) · 겹침 판정: 호출 ↔ 모두 완료 **안 생김**(완료 줄은 `called` 아님 — SPEC-002 규칙 5 · 7) · 마취 ↔ 모두 완료 **생김**(규칙 15) → 기본값 「모두 완료」(OQ-A21 · A37) | 13(머리 · 와이어 · U-3 ×4 · U-4 · U-9 ×2 · 케이스 · 프로토 표 · A-33 · A-41 · A-42 · OQ-A21 · OQ-A38) |
| 2 | 확인 필요 표시 B안 | SPEC-003 카드 테두리 없앰 → 상자 옅은 빨강 + 왼쪽 띠 · 조건(`needs[]`) 그대로 · 겹침 7자리 표(시술 대기 · 마취 끝난 대기 · 마취 중 · 마취 20분 초과 · 시술 중 · 호출 상태 · 모두 완료) · 겹침 색 = OQ-A37 기본값(확정 아님) | 9(머리 · 와이어 · U-3 ×3 · 케이스 · A-37 · A-43 · OQ-A29 · OQ-A35 닫음 · OQ-A37) |
| 3 | 채팅 403 | SPEC-004 U-1 채팅 거절(DAY-SPEC-001 `forbidden` 글자 + [로그아웃] — 시술현황과 같음 · 다시 시도 없음 · 스트림 재연결 안 함 · 메모리 비움 · 셸 · 세션 유지) · 케이스 매트릭스 · C-A19 · OQ-C12 · SPEC-003 U-1 · 케이스 매트릭스 채팅 줄 | 7 |
| 6 | 그룹 이름 바꾸기 | SPEC-004 「뺌」에서 뺌 · U-7(지금 참여자 누구나 · 그룹만 · 방 공통 · 새 대화 「그룹 이름」 · 「비우면 참여자 이름으로 보여요」만 · 시스템 줄 없음) · API #22 `PUT /api/chat/rooms/{roomId}/title` `{title}` → `Room`(제안) · 규칙(만들기와 같은 40자 · 빈 값 null · 같은 이름 200 이벤트 없음 · 1:1 400 `chat_group_only` · 404 범위 · 순서 · 안 읽음 · 푸시 없음 · 동시 = 방 행 잠금 나중 것) · 실시간 = **기존 `chat_room` 이벤트**(새 이벤트 없음) · 푸시 제목 = 보낼 때 이름 · SPEC-000 `chat_room.title` | 12 |
| 7 | 채팅 전체 알림 | SPEC-005 U-3 「채팅」 스위치 · 종류 `chat`(받는 종류 = SPEC-004 활성 직원 · 저장 없으면 켜짐 · 계정 단위 · 차례 원장 호출 → 채팅) · S-5 · N-A13 · SPEC-004 U-8 · 규칙 · 푸시 받는 사람 · C-A14 · C-A21 · SPEC-000 kind 값 · **migration 없음**(`notification_setting.kind` 는 구현이 문자열 칸 · `notification.kind` DB enum 은 안 건드림) | 15 |
| 앱 후속 2 | `version` 같은 값 · `calls[].canRecall` | **이미 있음** — SPEC-003 U-12 `:350대` · A-9 · U-4 · A-22 · 개정 ⑥ · ⑦. 고치지 않음(머리 ⑧ ④ 에 「이미 있음」 기록). 코드는 아직 다름(아래) | 0(확인만) |
| 배포 | Unlisted · 두 앱 · 지금 상태 · M-16 · dev 서버 | mobile-deployment §1 · §1-1 · §3 · §5 · §6 · §9 · §9-1 · §12 · §13 · deployment.md env · Blob | 20+ |

## 정할 것 (사용자에게 · 후보 · 추천)

1. **OQ-A37 확인 필요 겹침 색** — (가) 확인 필요가 바탕을 가져감(옅은 빨강 + 띠 · 상태 글자 색만 유지 · 20분 초과는 띠만 더함) (나) 상태 바탕 유지 + 띠만. **추천 (가)**.
2. **OQ-A37 「시술 모두 완료」 상자 오른쪽 칸 · 마취 겹침** — 오른쪽 비움 · 마취가 열려 있어도 「시술 모두 완료」. **추천 그대로**.
3. **OQ-A38 목록 [귀가 대기] 줄 왼쪽 글자** — 비움(버튼만) / 사용자 글자. **추천 비움**.
4. **OQ-C11 그룹 이름 저장 · 취소** — (가) 메시지 수정 모드와 같은 ✓ · ✕ 아이콘(새 글자 없음 · 접근성 이름만 정함) (나) 「저장」 · 「취소」 글자 (다) 버튼 없이 완료 키 · 칸 나가면 저장. **추천 (가)**.
5. **OQ-C12 채팅 403 안내 다시 시도 때** — 다시 로그인 · 앱 다시 열 때만 / 앱이 앞으로 올 때도 한 번. **추천 앞으로 올 때도 한 번**(시스템 계정 교체 같은 dev 상황에서 앱을 껐다 켜지 않아도 풀림) — 지금 문서 기본값은 앞쪽(보수적)으로 적어 둠.
6. **M-20 dev 서버 APNs 허용 앱에 정식 앱(`day.medisolveai`) 추가** — 정식 앱 데모 세션 푸시가 dev 서버에서 나가려면 필요. **추천 정식 앱 record · 심사 준비 때 추가**.
7. **M-1 설치 기기** — 개인 폰 / 병원 관리 기기(사용자가 말하지 않음 · Android 방식에 영향).
8. **M-16 남은 것 — 앱 정식 서명 방법** — (가) 우회 절차 README (나) 기기 1대 등록 (다) 수동 서명(`_RESUME` §1 의 기존 열린 질문 그대로).

리뷰 확인용(사용자 질문 아님): OQ-C13(앱이 `chat` 설정을 읽는 때 — 로그인 · 복원 · 앞으로 · 바꾼 뒤) · OQ-N6(종류 이름 `chat`).

## 충돌 점검

- 「정식 앱 하나로 심사 · 데모 → dev」([확정]) ↔ 개발 앱 둘째: **충돌 없음** — 개발 앱은 TestFlight 확인용 · dev 주소 하나만 · 심사 · Unlisted 배포 바이너리 아님. 정식 앱 진입점 · 허용 목록 · 데모 규칙은 그대로(mobile-deployment §9-1). 개발 앱 연결은 SPEC-003 §4 「D-1 전 동작 — 개발 빌드」에 이미 들어맞는다.
- 실제 공백 하나: dev 서버 APNs 허용 = 개발 앱 하나 → 정식 앱 데모 세션 푸시 불가 → M-20 으로 올림(지우지 않음).
- 앞 판 Bundle ID 후보 `com.medisolveai.day*` 는 등록 값 `day.medisolveai*` 로 바꾸고 옛 줄은 취소선.

## 코드 영향 (다음 WP 용)

**서버(CENTURION_DAY `backend/`)**
- 새 `PUT /api/chat/rooms/{roomId}/title` — `routers/api/chat.py` + `services/chat.py`(그룹만 · 지금 멤버 · `strip` · `MAX_TITLE` 40 재사용 · 같은 값 = 이벤트 없음 · 방 행 잠금 · 커밋 뒤 지금 멤버 전부 `chat_room` · 시스템 줄 · `last_message_at` 안 바꿈).
- 채팅 푸시 받는 사람 — `services/chat_push.py:93` 조건에 `notification_setting(kind='chat', is_enabled=false)` 계정 빼기.
- 알림 설정 — `services/notifications.py:216-225` `_receivable` 에 채팅 활성 직원이면 `chat` 추가(활성 직원 판정은 `services/chat.py:115-146` 과 같게) · 차례 `doctor_call` → `chat`.
- **migration 없음** — `notification_setting.kind` 는 `String`(`models/misc.py:114`) · `NotificationKind` DB enum 은 안 건드림 · `chat_room.title` 칸 그대로.

**앱(CENTURION_DAY `app/`)**
- `ui/board_screen.dart:285-296` 카드 테두리 빨강(`need ? Ms.red … width 2`) 없앰 → `_box`(`:331`) · `_callBox`(`:389`)에 확인 필요 바탕 + 왼쪽 띠.
- `_nowBox`(`:369`)에 `card.allDone`(`model/board.dart:201`) 먼저 — 「시술 모두 완료」 / 「마지막 종료 HH:MM」(`room_screen.dart:580-585` 계산 재사용).
- 모두 완료 카드 [귀가 대기] 줄 — `card.canHome && me.canEditBoard` · `b.home(visitId, ok: OkToast.home…)` · 잠금 키 `home:{visitId}` 공유(`room_screen.dart:596-604` 와 같음).
- `data/board_stream.dart:213` `snap.version > current` → `>=`(SPEC 이미 「같은 값 받음」).
- `ui/room_screen.dart:23` `canRecallCall` 이 `tasks[].canRecall` → `calls[].canRecall`(모델에 `calls[].canRecall` 추가 · OQ-A33).
- 채팅 403 — `chat/chat_state.dart:213-231` `_forbidden` 을 본문 안내(`ui/shell.dart:347` `BoardForbiddenBody` 와 같은 글자 · [로그아웃])로 · `chat/chat_stream.dart:99-102` 403 재연결 멈춤 · 연결 줄(`chat_kit.dart:475`) 숨김.
- 그룹 이름 — `chat/screens/chat_info_screen.dart:105` 「그룹 이름」 편집(저장 · 취소 모양은 OQ-C11 결정 뒤) · `chat_api.dart` #22 · `chat_room` 이벤트 처리는 이미 있음.
- 「채팅」 스위치 — `notify/notification_settings.dart` 에 `chat` → 「채팅」 · 앱 안 배너 억제(`chat_state.dart` 배너 조건)에 `chat` 설정 값.

## 검증

```
python3 scripts/lint-pipeline.py --strict   → exit 0 · 0 error, 263 warning
products/day/ 범위: ERROR 0 · WARN 0
나머지 263 WARN 은 모두 타 제품(procedure-hub · selly 등 doc_no · version 누락) — 무관
```

## 미결 · 주의점

- 새 화면 글자는 하나만 들어갔다: 설정 스위치 「채팅」(사용자가 정한 이름 · 메뉴 이름과 같은 글자). 그 밖은 기존 글자만(「시술 모두 완료」 · 「마지막 종료」 · 「귀가 대기」 · 「그룹 이름」 · 「비우면 참여자 이름으로 보여요」 · `forbidden` 문구 · 「로그아웃」).
- 확인 필요 겹침 색 · 저장 · 취소 · 403 재시도 · 귀가 줄 왼쪽 글자는 **기본값으로 적었고 확정이 아니다**(OQ 표시).
- 배포 문서에 값(Key ID · Team ID · IP · Vault 이름 · 리소스 ID)은 적지 않았다. Bundle ID 와 env **이름**만 적었다.
- 「채팅 첨부 Blob 없음」은 브리프 · `_RESUME` 대로 적었다 — 조사는 계정 권한이 없어 확인되지 않은 상태라 deployment.md 에 그 사정도 함께 적었다.
