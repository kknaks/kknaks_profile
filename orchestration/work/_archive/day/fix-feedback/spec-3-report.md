# spec-3 결과 보고 — 2루프: E2E 피드백 · F-5 · 검수 잔여

## 상태: done (미커밋 · `products/day/` 만 · Delivery 손대지 않음 · 커밋/push/PR 없음)

워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec` — 앞 판 미커밋 위에 이어서.

| 파일 | 무엇 |
|---|---|
| `products/day/20-spec/spec-002-procedure-board.md` | **개정 ㉒**(머리 노트 :42) — F-5/E4 호출 취소 · E3 「간호관리」 · E6 차트 여는 곳 · D1 · D2 · D4 · W3 · W5 · W6 · W8 |
| `products/day/20-spec/spec-005-notifications.md` | **2026-11-17 2차 개정**(머리 노트 :32) — E5 웹 OS 알림 늘 띄움 · 호출 취소 알림 |
| `products/day/20-spec/spec-003-mobile-app.md` | 개정 ⑰ 끝에 「같은 날 보충」 ⑥ ⑦(:70) — 앱 무수정 연결(호출 취소 · 새 알림 종류 · 「간호관리」 · `systemDoctor`) |
| `products/day/20-spec.md` | 지도 줄 :32 · :35 · 범위 밖 :42(F-5 보류 취소선) |
| `products/day/log.md` | 새 행 :17 · **D3** :18 PR 칸 넣음(5칸) |

## 1. 결정 반영 위치 (spec-002 = `spec-002-procedure-board.md`, spec-005 = `spec-005-notifications.md` · 줄 = 고친 뒤)

| # | 결정 | 반영 위치 |
|---|---|---|
| **F-5 = E4** | 준비중 ⋮ 없음 · 호출 → 「호출 취소」 · 진행중 → 시작 취소 · 완료 → 완료 취소 · 수락 ⋮ 없음(기본값) | spec-002 화면 구성 E50 :171 · U-3 줄 버튼 :224 · ⋮ :226-227 · U-7 「호출 취소」 :275 · S-6 4 :437 · 호출 상태 도표 :541 · :547 · API 표 행 :578 · 「호출 취소 응답」 :595 · 매트릭스 :701 · :740-743 · 검사 순서 :756 · 토스트 :782 · KOS 쓰기 행 :847 · 갱신 범위 :887 · 규칙 20 :927 · **새 규칙 38** :953 · §4 개정 ㉒ 표 :993 · DB :1008 · OQ-67 :1031 · OQ-68 :1032 · spec-005 §3 「알림 행 만들기 — 호출 취소」 :260 · OQ-N14 :446 |
| **E3** | 시스템 계정 집도의 줄 = 「간호관리 · 진행 mm:ss」 · 「간호관리 · n분」 · 원장 바꾸기 원장 줄과 똑같이 | spec-002 U-3 시간 칸 :225 · 완료 · 원장 바꾸기 :228 · 스냅샷 `systemDoctor` :660 · 규칙 27 :933 · 규칙 34 :941 · **OQ-62 닫음**(:1026 행 취소선 · 「닫은 것」 :1038) |
| **E5** | 웹 OS 알림 늘 띄움 — OQ-N9 뒤집음 | spec-005 U-5 :156 · S-6 3 :196 · 매트릭스 :318 · **OQ-N9 닫음** :441 |
| **E6** | 차트 여는 곳 = 시술 이름 글자만 · 호버 「차트 작성」 | spec-002 화면 구성 E30 :170 · 차트 행 :175 · U-3 :229 · U-12 :346-347 · U-13 :367 · U-14 :371 · 규칙 23 :930 · 규칙 37 :951 · §4 ㉑ 표 · ㉒ 표 |
| **E2** | 팝오버 위쪽 잘림 | **스펙 변경 없음 — 버그.** U-4 「의사 호출 창」(머리 → 검색 → 추천 「모든 의사」 → 원장 줄 · 오른쪽 「선택됨」)이 늘 보이는 구성이 지금 계약이고, 열림 규칙은 「버튼 아래 · 공간 없으면 위 · 넘치면 당김」뿐 — 선택 줄로 스크롤하며 팝오버가 밀리는 것은 구현 문제. 개정 ㉒ 노트 ④ 에 한 줄 |
| E1 | 고칠 것 없음 | spec-005 2차 노트 · spec-002 ㉒ 노트 ④ |
| D1 | 귀가 대기 취소 웹 응답 = 판 전체 다시 받기(본문 없음 · `HX-Trigger day:board-refresh` · `X-Day-Version` 없음) | spec-002 :594 · 갱신 범위 :887 |
| D1 · D2 · W8 | `sort` 는 GET 쿼리로만 · 「조작 응답도 같은 sort」 → 「판 전체를 다시 그리는 응답만」 · 판 렌더가 `hx-get` 에 `sort` 박음 · 탭 = 링크 이동 | spec-002 「정렬 탭」 :592 |
| D3 | log PR 칸 | `log.md:18` |
| D4 | `room.order` → `room.sort_order` 3곳 | spec-002 :351 · :388 · :670(옛 이름 취소선 · 개정 ⑱ 머리 노트 :52 의 역사 기록은 그대로) |
| W5 | 직전 단계가 판 단계가 아니면 `procedure` | OQ-58 ⓐ :1022 — **ⓐ 닫음** |
| W6 | 연결 없는 병원 = KOS 쓰기 없이 DAY 만 | 규칙 34 :946 |
| W3 | `conflict` 토스트 글자 | 토스트 표 `conflict` 행(정해지지 않음) · OQ-66 ⓓ :1030 |

## 2. 새 계약

### 호출 취소 엔드포인트 (spec-002 :578 · 규칙 38 · 매트릭스)

- 웹 `POST /board/tasks/{task_id}/cancel-call`(경로 이름 제안) · 본문 없음 · `board` edit · **JSON 짝 없음(이번엔 웹만 — 기본값 planner)**.
- 대상 = 판 카드의 **호출(수락 전) 줄 하나**. 결과 = 그 줄에 유효 호출이 없게 → 준비중. 앞 열린 호출로 되살아나면 안 됨. 남은 줄 없는 호출은 `closed_at`.
- 저장 제안(OQ-67 ⓒ · migration 없음): 그 줄이 든 **열린 호출 전부**의 `doctor_call_task.deleted_at` + 받을 시술 없는 호출 `closed_at`. 근거 = `queries/board.py:229-230` 판 조회가 이미 `DoctorCallTask.deleted_at IS NULL` 만 읽음 · `board_rules.py:62-69` 유효 호출 = 가장 최근 · 닫힌 호출이면 없음.
- 검사 순서 = 401 → 403 → 404(`not_found`) → 409 `visit_home` → 수락됨 `call_already_accepted`(기존 코드 · 기존 글자) → 호출 아님 `task_not_called`(**새 코드 제안 · 글자 비움**) → 취소.
- 응답 = 다른 조작과 같음(그 카드 조각 + 인박스 · 탭 숫자 · 원장 상태 OOB + `version`).
- `event_log` `call.cancel`(제안) 1행. 확인 창 · 성공 토스트 없음(기본값 planner — 글자를 짓지 않음).
- **KOS 쓰기** = 「KOS 명령 미확인 — HAR 대기」 · 「기본값(코디 2026-11-17 · HAR 받으면 바꿈)」 DAY 만. 코드 사실:
  - ① 쓸 수 있는 기존 명령이 없다. `change-tasks-doctors` 는 수락 쓰기라(확인 `status=READY` · `writes.py:144-151`) KOS 를 「진행」으로 보내고 집도의를 남긴다. `change-tasks-complete(false)` 는 완료→READY 쓰기라 WAITING 작업에 어떻게 되는지 모른다. `cancel-flow-tasks` 는 작업을 취소해 DAY 줄이 사라진다.
  - ② DAY 만 하면 다음 동기화 뒤에도 DAY 는 준비중이다. 줄 상태는 KOS `WAITING` 을 보지 않는다(`board_rules.py:117-125`). 동기화는 `doctor_call` 을 만들지 않는다 — 호출 의사는 `visit_task_staff.called_doctor` · `doctor_called_at` 으로만 옮기고, 판 코드는 둘 다 읽지 않는다. 대신 **KOS 쪽에는 「호출」이 남아 데스크 화면과 어긋난다**(OQ-68).

### 호출 취소 알림 (spec-005 §3 :260 · OQ-N14)

| 항목 | 내용 |
|---|---|
| 받는 계정 | 원래 호출의 원장 호출 알림 행(`doctor_call_id` = 그 호출)을 받은 계정 — 「기본값(코디 2026-11-17 · 사용자 E2E 에서 확인)」 |
| 종류 이름 | 제안 `doctor_call_cancel`. **DB enum `notification_kind` 값을 더해야 하므로 migration 1개**(`models/misc.py:49`). 앱 푸시까지 보내면 `push_kind` 도(:50) |
| 제목 · 본문 | **비움 — 정할 것.** 기존 「원장 호출」 · 「{방} · 시술 {N}건 · …」 규칙에서 따라 나오는 글자가 없다. `title` · `body` 가 NOT NULL 이라(`models/misc.py:104-105`) **알림 행을 쓰려면 사용자 글자가 먼저 필요하다**(호출 취소 동작 자체는 글자 없이 지을 수 있음) |
| 웹 OS 알림 | 넣음(기본값 planner) — 같은 조건 · 늘. 1루프 `day.js` 는 `kind=="doctor_call"` 만 띄우므로 고쳐야 함 |
| 앱 푸시 | **정할 것**(기본값 planner = 보내지 않음). 앱 코드 사실은 아래와 같다 |
| 원래 호출 알림 행 | 그대로 둔다 |

앱 코드 사실(앱 푸시 · 목록 관련):

- iOS 는 `aps.alert` 로 OS 배너를 띄운다. 하지만 눌러도 이동하지 않는다(`push_coordinator.dart:205` 에서 return).
- 앱이 앞에 있을 때 받으면 아무 처리도 하지 않는다(`:232-236`).
- 알림 목록은 모르는 종류를 버린다(`notification_model.dart:13 · 74`).
- 서버 `unread` 는 종류를 가리지 않고 센다(`services/notifications.py:96-110`). 그래서 **앱 종 배지 수와 목록이 어긋날 수 있다**(OQ-N14 ⓓ).

## 3. 정할 것 (지어내지 않음)

| OQ | 무엇 | 기본값 · 지금 |
|---|---|---|
| spec-005 OQ-N14 ⓑ | **호출 취소 알림 제목 · 본문 글자** | 비움 — **알림 행 쓰기를 막음**(NOT NULL) · 사용자 글자 필요 |
| OQ-N14 ⓒ | 앱 푸시까지 보낼지 | 보내지 않음(planner) |
| OQ-N14 ⓐ | 종류 이름 · 받는 계정 | `doctor_call_cancel`(planner) · 원래 알림 받은 계정(코디) |
| OQ-N14 ⓓ | 앱 배지 어긋남(서버 `unread` 를 원장 호출만 세게 할지) | 정해지지 않음 |
| OQ-N14 ⓔ ⓕ | 웹 OS 알림에 넣을지 · 원래 호출 알림을 닫을지(기획 상담 호출 「호출 취소」 = 알림 닫힘 선례 · 참고만) | 넣음 · 그대로 둠 |
| spec-002 OQ-67 ⓐ | 수락된 호출도 취소할지 | 수락 전 「호출」 줄만 · 수락 줄 ⋮ 없음(코디 꼬리표) |
| OQ-67 ⓑ ⓒ ⓓ ⓔ ⓕ | 단위(줄 vs 호출 통째) · 저장 방법 · 확인 창/토스트 · 앱 JSON · 거절 코드 | 줄 하나 · `deleted_at` + `closed_at` · 없음 · 웹만 · `call_already_accepted` / `task_not_called`(새 · 글자 비움) — 모두 planner 제안 꼬리표 |
| OQ-68 | 호출 취소 KOS 명령 | **HAR 대기** · 기본값 DAY 만(KOS 는 「호출」로 남음 — 감수 여부) |
| OQ-66 ⓓ | `conflict` 토스트 글자(W3) | 정해지지 않음 — 지금 「요청이 올바르지 않습니다」 |
| (그대로 열림) | OQ-58 ⓗ · OQ-59 ⓐ · OQ-61 ⓒ · OQ-64 · OQ-65 ⓑ ⓒ · OQ-66 ⓐ · OQ-N8(원장만 물을지) · OQ-N13 | 앞 판 그대로 |

## 4. 검증

- `python3 scripts/lint-pipeline.py --strict` 결과는 **exit 0 · 0 error · 263 warning** 이다. `products/day/` 는 ERROR 0 · WARN 0 이다. WARN 263건은 모두 다른 제품(selly 등)에 원래 있던 경고라 이번 변경과 관계없다.
- 새 화면 글자는 사용자 말만 썼다: 「호출 취소」 · 「간호관리」 · 「차트 작성」. 그 밖의 확인 창 · 토스트 · 알림 제목/본문 · `task_not_called` 글자는 비워 두었다.
- 기획안(`00-baseline/planning/`)은 고치지 않았다. 코드 워크트리는 읽기만 했다.

## 5. be · fe 에 넘길 주의

- **알림 행은 사용자 글자가 정해지기 전에는 쓸 수 없다**(OQ-N14 ⓑ). 그 전까지는 호출 취소(DAY 동작 · 화면 · 응답)만 지을 수 있다. 알림 부분은 글자를 기다리거나 사용자에게 먼저 받아야 한다.
- 새 알림 종류를 넣으면 migration 1개(enum 값 추가)가 생긴다. 지금까지 이 묶음은 「migration 없음」이었다.
- 스냅샷 새 칸 `tasks[].systemDoctor`(이름 제안)는 앱이 모르는 칸이라 무시한다(앱 무수정).
- E6: 1루프는 줄 전체를 `data-day-row-get` 으로 열었다. 이제 시술 이름 글자만 열고, 호버 툴팁 「차트 작성」을 단다.
- E3: 1루프는 `board_parts.html` `doctor_pop` 이 `t.doctor` 없으면 원장 바꾸기를 열지 않는다. 서버 `doctor_change_block` 은 진행중 줄을 이미 받는다.
