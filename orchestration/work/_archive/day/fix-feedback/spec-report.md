# fix-feedback-spec 결과 보고 — 현장 피드백 F-1 · F-2 · F-3 · F-4 · F-6 · F-7 스펙 개정 · Delivery 발행

## 상태: done (승인 대기 — plan 승인은 사용자 몫 · receipt 적용 안 함)

| 항목 | 값 |
|---|---|
| Delivery Issue | **CENTURION_DAY#254** — https://github.com/MediSolveAIDev/CENTURION_DAY/issues/254 |
| 라벨 | `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:ready` |
| risk | **L2**(새 엔드포인트 2 · KOS 쓰기 조합 추가 · 기존 결정 뒤집음) |
| contract_digest | `sha256:eab82ce2ced0df14a1e49120f5402f555b0920b4df9424598c6134bb391941b3` |
| plan_digest (승인 대상) | `sha256:06bfccd8ae4218d3ad982c47c92f2d4ceb45ee30f2117c9be4aaabe0ee1578b0` |
| baseline | `ready` · mediness `origin/main` `c3639503159bf1861cff5ada5277270be6ac406d` — **개정 ㉑(SPEC-002) · SPEC-005 2026-11-17 개정 · SPEC-003 개정 ⑰ 은 이 워크트리에만 있음(미커밋)**. Review Surface[0] 에 적음: 스펙 PR 머지 → 같은 key(`day/fix-feedback-2026-11-17`)로 contract_version 2 재결속 → 그 뒤 사용자 승인 권장(fix-web #249 때와 같은 순서) |
| next_action | `review-delivery-plan` · human_gate true |
| task_projection | blocked(`delivery-plan-review-required`) · `partial: true` — 승인 전이라 정상 |
| request / plan / apply | scratchpad `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-fix-feedback-spec/0363c69c-4505-419e-a765-28d545e68aed/scratchpad/delivery/fb.v1.{request,plan,apply}.json` |

## 수행 내용 — 변경 파일

워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec` (미커밋 · `products/day/` 만):

- `products/day/20-spec/spec-002-procedure-board.md` — 개정 ㉑ · `last_updated` 2026-11-17
- `products/day/20-spec/spec-005-notifications.md` — 2026-11-17 개정(F-4)
- `products/day/20-spec/spec-003-mobile-app.md` — 개정 ⑰(연결만 · 앱 무수정)
- `products/day/20-spec.md` — In Scope 시술 현황 · 알림 줄 · Out Of Scope 한 줄 · 최종 수정
- `products/day/log.md` — 2026-11-17 spec-change 행

`version` 은 `0.0.1` 그대로 — `rules/document-pipeline.md` 「문서를 고쳤다고 올리지 않는다」(제품 버전 = 상위기획 사이클). 브리프 「버전 올림」은 개정 번호(㉑ · ⑰) · `last_updated` · log 로 대신했다.

## 결정 표 항목별 반영 위치 (spec-002 줄 번호 = 수정 뒤)

| # | 반영 위치 |
|---|---|
| 공통 | 개정 ㉑ 머리 노트 :42 · 1차 범위 표(빈 방 · F-5 다음) · 기획안 차이 표 :958 「개정 ㉑ — 기획안 · 앞 판과 달라진 곳」 · DB `event_log` 값 · OQ-58 ~ 66 :986-994 |
| **F-1** 귀가 대기 취소 | 기획안 표 :134(「귀가 대기 취소만 넣음」) · 4-1 정책 7 행 · 화면 구성 E28 · U-9 :290 · U-12 ⋮ 줄 · S-6 3 :432 · 방문 단계 Lifecycle 보충 · API 표 `POST /board/visits/{visit_id}/undo-home`(제안) :573 · 「귀가 대기 취소 응답」 · 케이스 매트릭스(`visit_not_home` 제안 · 404 · 방 없음) · 토스트 표 :765 · KOS 쓰기 표 :838(`change-flow-step` 직전 단계 · 확인 안 됨) · 규칙 20 :908(취소선 · 날짜 · 사유) · 새 규칙 35 :928 · OQ-27 보충 |
| **F-2** 정렬 탭 | 화면 구성 E07 :165 · U-2 :203 · API 보충(「정렬 탭」 — 새 행 없음 · OQ-59) · 새 규칙 36 :929 · OQ-59 |
| **F-3** 바로 시작 | 기획안 표 4-1 흐름 1 행 :116 · 3-1 흐름 5 행 보충 · 화면 구성 E46 :169 · U-3 :216(N · 일부 거절 토스트 · 웹만) · U-3 시간 칸(취소선 · OQ-62) · U-7 「바로 시작」 + :272(**「원장 없이 시작하는 길 없음(2026-11-09)」 취소선 · 2026-11-17 뒤집음 · 사유**) · U-14 시스템 계정 집도의 줄(OQ-65) · S-4 2 :420 · API 표 `POST /board/visits/{visit_id}/quick-start`(제안) :571 · 「바로 시작 응답」(`{startedTaskIds, rejected:[{taskId, code}]}` · 하나라도 시작 = 200 · 전부 거절 = 409 기본값) · Validation `taskIds` · 케이스 매트릭스 `no_doctor` 행 보충 + 바로 시작 6행 :719 근처 · 바로 시작 검사 순서 :742 · KOS 쓰기 표 :823-824(`change-tasks-doctors` · `doctorIds=[시스템 계정]` → 기존 [시작] 쓰기 순서 · 사용자 HAR 근거) · 규칙 10 :889(취소선 · 사유) · 규칙 25 보충 · 새 규칙 34 :922 · 실시간 갱신 범위 보충 |
| **F-6** 차트 아이콘 | 화면 구성 E30 · E46 행 · 차트 행 :173(「여는 곳 = … 차트 아이콘」 취소선 → 줄 전체) · U-12 :343(예시 4가지) · U-13 걸러진 카드 줄 · U-14 여는 곳 · 규칙 23 :911 · 새 규칙 37 :930(`ui.chart_icons` · 완료 줄 · 시술 완료 탭 · 키트 견본 · 미완료 줄 그대로) |
| **F-7** 원장 계정 수락 | U-6 :251(원장 = 팝오버 없이 본인 · 다른 원장 지정 호출도 · 그 밖 대리 · 「수락」 그대로 · 옛 문장 취소선) · 수락하는 곳 · 규칙 8 · API 보충(변경 없음) · OQ-19 :1037 · OQ-64 |
| **F-4** 웹 알림 | spec-005: 개정 노트 :32 · 범위 표 :64 + 뺌(웹 푸시 등 다음 스펙) · U-5 :152 · S-6 :190 · §3 「웹 — 브라우저 OS 알림」 :271(원천 · 붙는 곳 = 공통 틀 · 스트림 코드 사실 · 이벤트 후보 ㉠㉡㉢ · 여러 탭 · 재연결 · 설정) · 케이스 매트릭스 5행 · OQ-N8 ~ N13 :420 근처. spec-002 1차 범위 표 「알림」 칸에 연결 한 줄 |
| SPEC-003 | 개정 ⑰ :70(F-7 웹 = 앱 U-6 · F-3 앱 버튼 없음 · 앱 `canStart` 그대로 · 시스템 계정 줄 앱 「담당의 미정」 코드 사실 · F-1 앱 재표시 · F-6 · F-2 앱 없음 · F-4 앱 무영향) · U-6 :336 한 문장 |

## 계약 요약 (코드 사실 근거 — CENTURION_DAY `origin/dev` `4f8316a7`)

- **F-3**: 새 엔드포인트 필요(지금 시작은 단건 `POST /board/tasks/{id}/start` 뿐 · `routers/board.py:646-666`). 판정은 `board_rules.py:280-292` 를 쓰되 `no_doctor` 대신 시스템 계정 집도의. 시스템 계정 KOS id = 기존 `_system_account`(`services/board.py:225`). 시스템 계정은 원장 목록 밖이라 `task_doctor`/`kos_doctor` → `null` · 원장 상태 · 고객 검색에 안 잡힘. 단건 `no_doctor` 는 OQ-60(기본값 그대로).
- **F-1**: 귀가 대기 되돌리기 라우트 없음(`routers/board.py`). `home`(`services/board.py:948-985`)은 `PROCEDURE_DONE` + 마취 닫기 + 「방 배정」 `CANCEL` — 되돌리기는 단계만(기본값) · KOS 되돌림 확인 안 됨.
- **F-2**: 새 칸 없음(`cards[].room.title`) · 화면/서버 OQ-59.
- **F-4**: `GET /api/notifications/stream` 이 웹 쿠키 세션도 받음(`routers/api/notifications.py` 머리 · `current_session` cookie) · 이벤트 `notification {unread}` 만(`services/notification_events.py`) · 웹 SSE 는 `board.html:8` 뿐 · `base.html` 에 없음 · 앱은 `notification` 이벤트만 구독(`app/lib/notify/notification_controller.dart:55`) → 새 이벤트를 더해도 앱 무영향.
- **F-6 · F-7**: API · 스냅샷 변경 없음(템플릿 `ui.html:258-260` · `board_regions.html:55-60` · `board_parts.html:226-228`).
- migration 없음.

## 검증

- `python3 scripts/lint-pipeline.py --strict` → **exit 0 · 0 error · 263 warning** · `products/day/` **ERROR 0 · WARN 0**. WARN 263건은 전부 타 제품(selly 등 doc_no 누락 · map frontmatter) — **무관**(기존).
- 화면 문구 발명 없음 — 새로 적은 화면 글자는 사용자 말(「귀가 대기 취소」 · 「시술순」 · 「방별순」(임시) · 「바로 시작 · N건」 · 「의사 호출 · N건」 · 「수락」)과 기존 스펙 글자(알림 제목 · 본문 · 기존 토스트)뿐. 토스트 · 확인 창 · 원장 없는 줄 글자 · 권한 안내는 「정할 것」.

## 정할 것 (사용자 결정 필요 — 기본값은 결정 아님)

**SPEC-002**
- **OQ-58 귀가 대기 취소** — ⓐ 직전 단계 값(기본 `visit_flow_log` 직전 · 보통 `procedure`) ⓑ KOS `change-flow-step(PROCEDURE_DONE → PROCEDURE)` 데모 실물 1회 ⓒ 취소한 「방 배정」 되살림(기본 안 함) ⓓ 닫은 마취(기본 안 엶) ⓔ 확인 창 · 토스트 · `visit_not_home` 글자 ⓕ 방 없는 방문 ⓖ 카드 자리(기본 규칙 18) ⓗ 데스크가 이미 귀가 처리한 직후 경합.
- **OQ-59 정렬 탭** — 이름(임시) · 처음 탭 · 기억 · 같은 방 이름 순서 · 자연 정렬 vs 문자열 vs `room.order` · 화면/서버 · 다시 그릴 때 유지.
- **OQ-60** 단건 [시작] `no_doctor` 도 시스템 계정으로 풀지(기본 안 풂).
- **OQ-61** N = 0 일 때 버튼 · 수락 줄이 오면 · 전체 선택과 N.
- **OQ-62** 원장 없이 시작한 줄의 「{원장} · 진행 / n분」 자리 글자 · 「원장 변경」 툴팁 — 앱은 지금 코드대로 「담당의 미정」.
- **OQ-63** 일부 거절 토스트 모양 · 전부 거절 HTTP(기본 409 + 첫 코드) · `event_log` 줄마다 vs 1행.
- **OQ-64** 원장 태그 공용 계정 PC 의 본인 즉시 수락.
- **OQ-65** 시스템 계정 집도의 줄의 시술 전 의사차트(X 를 집도의로 쓸지 등) · 의사차트 집도의 처음 값.
- **OQ-66** `change-tasks-doctors` 여러 `sequences` 일부 거절 · 확인 조건 `status` · 시스템 계정 id 없음(기본 409 `conflict`).

**SPEC-005**
- **OQ-N8** 브라우저 알림 권한 묻는 때 · 거절 시 화면 · **OQ-N9** 탭이 앞일 때도 띄울지 · **OQ-N10** 눌렀을 때(탭 앞으로 · 카드 · 읽음) · **OQ-N11** 이벤트 이름/방식(㉠ 기존 `notification`+목록 GET ㉡ 새 이벤트 `doctor_call` ㉢ 웹 전용 경로) · **OQ-N12** 여러 탭 중복 · **OQ-N13** 끊긴 동안 생긴 호출(기본 안 띄움).

## 미결 · 주의점

- 스펙이 미커밋이라 Delivery #254 v1 의 baseline(`c3639503`)은 옛 계약이다 — 스펙 PR 머지 뒤 v2 재결속(Review Surface[0]) 후 승인 권장. v1 plan_digest 는 승인하지 않는 쪽 권장.
- F-4 웹 알림은 받는 계정 규칙상 **원장 계정 웹에서만** 뜬다(간호 PC 에는 안 뜸) — 결정 「받는 계정 · 설정 규칙 그대로」의 결과라 그대로 적었으나 현장 기대와 맞는지 확인 거리.
- `uv run` 이 `tools/harness/.venv` 를 만들었다 — git status 에 안 잡힘(ignore 됨).
- 작업 중 디스크 가득(ENOSPC)으로 한 번 멈췄다 — 사용자가 비운 뒤 이어서 끝냄. 중단 전 편집분은 diff 로 확인했고 손상 없음.
