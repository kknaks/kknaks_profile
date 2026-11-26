# planner-2 결과 보고 — WORK-002 앱 예약현황(읽기 전용) · 문진 QR · 여권 스캐너 · 태블릿으로 보내기

## 상태: done

- 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec`(브랜치 `kknaksss/day-app-re1-spec` · `319dd82e` 위 · **커밋 · push 안 함**)
- 9 파일 · +469 −60 · 30-work 안 건드림
- 결정 원천 = `_RESUME.md` §2 2026-11-25 WORK-002 행 + **보충 1**(앱 예약현황 = 웹 SPEC-006 · 007 과 닮게 — 브리프 §2 결정 1 구조 줄 대신 읽음)

## 수행 내용 — 바꾼 절

| 파일 | 개정 | 바꾼 절 |
|---|---|---|
| `spec-003-mobile-app.md` | **개정 ㉒** | 머리 첫 문단(4메뉴) · 새 개정 머리 ㉒ ①~⑦ · §1 범위(넣음 줄 · 뺌 3줄 취소선 · 새 뺌 줄) · Placement · Wireframe · U-2(4메뉴 · 취소선 2) · U-16(기기 이름 취소선) · **새 U-24 예약현황 목록 · U-25 예약 상세(읽기 전용) · U-26 문진 QR · U-27 여권 스캔 · U-28 태블릿에 보내기 · U-29 띄우기 받기 · U-30 「이 기기 이름」** · §3 API 표 3줄 · 새 「여권 스캔 · QR 네이티브 채널」(`day/scan`) · §4 Frontend 화면 · 권한(취소선 + 여권 카메라 · Android `CAMERA`) · Functional Rule 10 · 프로토 대조 셸 줄 · 개정 ㉑ 범위 행 취소선 · **새 「개정 ㉒ — 결정 ↔ 바꾼 곳」 · 「고칠 절 처분」 · 「웹 예약 상세 17 · 목록 6 처분」 · 「cc 이식 처분」** · 서버 의존 D-8 · A-25 취소선 · 새 A-61 ~ A-76 · OQ-A3 · 새 OQ-A79 ~ A90 |
| `spec-007-reservation-detail.md` | **고침 5** | 머리(결정 · 「어디에 두나」 판단) · §1 범위 2칸 취소선 · RD-02 · RD-03 · 시안 요소 #8 · #9/#10 · B3 ~ B8 · U-3([문진 QR] · [여권 스캔] 켬 · 판정 · 외국인 신분확인 · 새 「초진 문진 · 건강정보」) · 경계 표 · 화면이 읽는 칸 3줄 · API 머리 취소선 · API 표 4줄 · 권한 · **새 「앱 JSON 짝 — 예약 상세 읽기」 · 「태블릿 띄우기 · 문진 QR · 여권 스캔」(규칙 1 ~ 8) · 「여권 스캔 저장」 · 「고객 문진 웹 — 공개 페이지 · 공개 API」** · 케이스 9줄 · 실시간 `display` · 시안과 다른 곳 · DB(migration) · 새 OQ-D27 ~ D40 · D13 · D20 · D23 행 · 새 「고침 5 — 결정 ↔ 바꾼 곳」 |
| `spec-006-reservation-board.md` | **개정 ⑭** | 머리 · §1 R5 취소선(여권 · 문진 넣음 · 전후 사진 그대로 뺌) · 직원 앱 숨김 줄 취소선 · API 「앱 JSON 은 두지 않는다」 취소선 · 새 「앱 JSON 짝」(`GET /api/reservations` · `/api/reservations/stream`) · 실시간 ⑭ 문단 · OQ-R40 |
| `spec-005-notifications.md` | 2026-11-25 개정 | 머리 · 범위 넣음 줄 · 뺌 줄 취소선 · 새 §3 「띄우기 — 기기 하나」 · OQ-N21 · N22 |
| `spec-004-internal-chat.md` | 2026-11-25 맞춤 | 머리 한 줄 · OQ-C7(「범위 밖」 이유 취소선 · 문구 = SPEC-003 OQ-A79) |
| `spec-000-data-model.md` | 2026-11-25 개정 | 머리 ①~⑤ · 07 「정한 것」 outbox 문장 취소선(:1076) · device 규칙 띄우기 줄 · `device.name` · `display_request.kind` · `device_id` · `qr_token_hash · qr_nonce` null 허용 · `identity_check.method` · `id_photo` KOS 상태 = `external_ref` · `questionnaire_history` `source` · 새 `kos_status` · `kos_error` · `kos_sent_at` · `created_at` 취소선 |
| `20-spec.md` | — | In Scope 직원 앱 · 예약 상세 줄 · Out Of Scope 4곳 취소선 · 읽는 순서 직원 앱 · 열린 것 2줄 |
| `10-decision.md` | — | 현재 결론 1줄(새 ESC 없음 · DAY-ESC-001 참조 늘어남) · 로그 1줄 |
| `log.md` | — | 2026-11-25 `spec-change, decision-change` 1행 |

### 문진 공개 페이지 · 공개 API 를 어디에 — planner 판단

**DAY-SPEC-007 §3 에 둠(새 SPEC 없음).** 근거: 문진 QR · 여권 스캔은 SPEC-007 RD-02 버튼(D13 · D55)과 RD-03 「초진 문진 · 건강정보 · 신분확인」(D20)의 다른 끝이라 책임 · lifecycle 이 같다 / 웹(007)과 앱(003)이 같은 service 를 불러 한 곳에 둬야 복제가 없다(SPEC-002 ㉚ 이 앱 JSON 짝을 웹 정본 SPEC 에 둔 선례) / 새 SPEC 이면 30-work Spec Coverage 행(lint ERROR 대상)이 필요한데 이번엔 30-work 를 안 쓴다. 고객 독자 · 법적 검토로 따로 승인해야 하면 나눈다 → **OQ-D35**. 띄우기 · 여권 스캔 저장도 같은 이유로 007 §3. 앱 목록 JSON 은 006, 상세 JSON 은 007(웹 정본 옆).

## research-3 §5 고칠 절 표 처분(빠진 행 0 — SPEC-003 「고칠 절 처분」 표가 정본)

| # | 행 | 처분 |
|---|---|---|
| 1 | SPEC-003 :29 · :108 · :144 3메뉴 | 고침(4메뉴) |
| 2 | SPEC-003 :71 개정 ⑮ | 그대로(기록) + ㉒ ① 에 다시 넣는 이유 |
| 3 | SPEC-003 :123 범위 밖 | 고침(취소선 3 · 새 뺌 줄) |
| 4 | SPEC-003 :134 · :1099 「다음 작업」 | 고침(취소선) |
| 5 | SPEC-003 :1044 권한 | 고침(취소선 · iOS 문구 OQ-A79 · Android CAMERA) |
| 6 | SPEC-005 :77 | 고침 |
| 7 | SPEC-006 :111 R5 | 고침(여권 · 문진 넣음 · 전후 사진 그대로 뺌) |
| 8 | SPEC-007 :67 · :109 · :152 · :202 · :345 · :626 | 고침 |
| 9 | SPEC-007 D13 · D20 · D55 | D13 · D20 고침 · D55 그대로 |
| 10 | SPEC-004 :538 · :636 OQ-C7 | 고침(이유만 · 문구는 사용자) |
| 11 | SPEC-000 display_request · device | 고침 |
| + | SPEC-000 `id_photo` KOS 상태 · `questionnaire_history` 상태 · :1076 outbox 문장 | 고침(차이 = SPEC-000 2026-11-25 개정 ③) |

웹 상세 17 · 목록 6(보충 1 요구) 행마다 「앱에 넣음(읽기) / 쓰기라 뺌」 = SPEC-003 「웹 예약 상세 17 · 목록 6 처분」 표. 요약: 넣음(읽기) = #1 #2 #3 #5 #7 #9 #14 #15 · L1 L2 L3 L6 / 일부 = #6(값만) #10(이름만) #11(값만) #12(목록만) #13(값만) · L4(카드 누름만) · L5(보기만) / 누르는 것 = #4 / 쓰기라 뺌 = #8 #16 #17.

## research-2 처분

- **S1 ~ S10 · Q1 ~ Q8** = SPEC-003 「cc 이식 처분」 표. 전부 넣음. 예외: S9 열람 · 삭제는 이번 판 없음(결정에 없음 · OQ-D34) · S10 iOS 문구 = 사용자 몫(OQ-A79).
- **§5 Q1 ~ Q12**(§2 결정이 이김): Q1 예약 탭 신설 ✓ · Q2 「목록 + 스캔 · QR 만」 → 뒤집힘(웹 모달 내용 읽기 전용 + 버튼 셋) · Q3 「Android 손 입력만」 → 뒤집힘(CameraX + ML Kit) · Q4 직원 토큰 직접 ✓ · Q5 시술전후 경로 ✓ · Q6 KOS + DAY 둘 다 · ESC 참조만 ✓ · Q7 KOS 제출 · 부작용 받음 ✓ · Q8 DAY 공개 Jinja ✓ · Q9 「태블릿 뺌」 → 뒤집힘 · Q10 「스캐너 먼저」 → 뒤집힘(둘 다) · Q11 「웹은 비활성」 → 뒤집힘(웹 켬) · Q12 cc 수명 그대로 ✓.
- **research-3 T1 ~ T9**: T1 a ✓ · T2 공용 코디 계정 하나 ✓ · T3 설정 「이 기기 이름」 ✓ · T4 기기 하나 ✓ · T5 cc 그대로 ✓ · T6 실시간 신호 ✓ · T7 읽기 전용 ✓ · T8 폰 목록 / 태블릿 표 ✓ · T9 A ✓.

## migration 판단 — **있음 1**

근거(CENTURION_DAY `96036397` `models/reception.py` · `models/customer.py` 확인):
- `display_request.qr_token_hash` · `qr_nonce` = **NOT NULL** → 여권 스캔 요청(토큰 없음)을 위해 null 허용 = migration
- `questionnaire_history` 에 KOS 보냄 상태 칸 없음 → `kos_status`(sending · sent · failed) · `kos_error` · `kos_sent_at` = migration
- migration 없음: `display_request.kind` · `identity_check.method` · `id_photo.doc_type` · `external_ref.entity_type` = 열린 문자열(값만 정함) · `id_photo` KOS 상태 = `external_ref` 로(칸 없음 · visit_photo 원칙) · 권한 = `reservation.detail` edit 재사용(권한 행 없음) · `device.name` 칸 있음
- 번호 = WORK(dev 끝 `0028_visit_discharge_reason` 뒤)

## 검증

```
python3 scripts/lint-pipeline.py --strict → 0 error, 263 warning · products/day 범위 0 error · 0 warning
```
263 WARN 은 전부 다른 제품(selly · procedure-hub 등 doc_no / frontmatter 누락) — 무관.
OQ · AC · U 번호 중복 확인: 새 것 중복 0(OQ-A3 두 번은 HEAD 부터 있던 것).

## 미결 · 주의점

1. **OQ-A79 iOS 카메라 문구 여권 용도 = 사용자 문구 필요**(D15 엔 여권 없음 · cc 원문과 합쳐 짓지 않음) — **정식 심사 제출을 막음**(구현은 안 막음).
2. **OQ-D36 외국인 [상담 대기]** — 스캔으로 신분 확인돼도 웹 [상담 대기] 「신분확인 빠짐」은 지금 그대로 둠(웹 예약 동작 바꾸지 말라는 범위 제약). 사용자 확인 필요할 수 있음.
3. **알림 권한을 켠 태블릿만 목록에 나옴**(기기 행이 푸시 등록 때만 생김 · cc 설정 글자 「알림을 켜면 웹 기기 목록에 보여요」로 계약화) — 현장 셋업 때 주의.
4. **문진 KOS 400 처리** — 결정 5(실패여도 답 남음)에 따라 고객은 늘 끝 화면 · KOS 가 400 으로 거절한 답은 [다시 보내기]도 같은 결과일 수 있음(OQ-D32). cc 의 고객 409 `questionnaire_rejected` 길은 없앰.
5. 웹 [문진 QR] = cc 웹 꼴(PC 화면에 QR + [태블릿에 띄우기]) · [여권 스캔] = 기기 고르기 → 태블릿(웹 카메라 없음) — 결정이 「켬」까지라 동작 모양은 cc 웹을 따름.
6. 글자 없는 자리(비움 + OQ): 기기 고르기 머리(cc 「태블릿에 띄우기」 ↔ 결정 「태블릿에 보내기」 — OQ-A83) · 스캔 결과 DAY 사진 줄(cc 「ccc 사진」 — OQ-A85) · Android 띄우기 알림 채널(OQ-N22) · 웹 기기 없음 · 보내는 중 · 다시 보내기 알림(OQ-D33) · KOS 사진 메모(OQ-D29).
7. 「확인 안 됨」 그대로 OQ: 파드 수(online · 속도 제한 — OQ-D31 · D40) · ML Kit 판독률 · 지표 고지(OQ-A89 · A-69 실물) · KOS 5개 한도 범위(OQ-A90) · 문진 언어표(OQ-D38) · KOS 자격(OQ-D39).
8. SPEC status 는 stable 그대로(개정 관례) · 30-work Spec Coverage 는 안 건드림(새 SPEC 없음이라 lint 정합 유지).
