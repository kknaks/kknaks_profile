# [planner] 링키 개발자용 설명서 md — ext 예약 요청 (planner-linky-guide-1)

너는 day `planner` 워커다. 맥락이 없으면 먼저 읽어라: `day-reservation3-spec-brief.md`(규칙 · 완료 보고 §9) · `_RESUME.md` §2.

## 무엇

링키 개발자(외부)가 이번에 DAY ext 에 생긴 **예약 요청 스레드 API** 를 붙일 수 있게 설명서 한 장. 스웨거(`/api/ext/docs`)를 대신하지 않고 **같이 읽는 안내서**다.

- 쓸 곳(새 파일 하나): `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/reference/2026-11-26-reservation-request/linky-ext-reservation-request-guide.md`
- 이 파일 밖은 고치지 않는다(mediness 스펙 · 코드 수정 금지). 커밋 금지.

## 근거 — 이것만 (지어 넣지 않는다)

- **스웨거 원문 = 코드**: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation3/backend/day/routers/api/ext_reservation_request_docs.py` · `day/schemas/ext_reservation_request.py` · `day/routers/api/ext_reservation_requests.py` · `day/routers/api/ext.py`(공통 오류 · 키). 읽기만.
- `be-swagger-1-report.md` ②(상태 × 행동) · ③(오류 코드) · ④(SPEC 과 다른 곳 — **코드가 맞다**) · `be-swagger-2-instructions.md`(재시도 = 처음 응답 그대로 — 고치는 중)
- `ext-request-body-draft.md` 는 옛 초안 — 칸 이름은 코드 스키마로 확인
- SPEC-008 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation3-spec/products/day/20-spec/spec-008-reservation-request.md` — 배경 설명만(스레드 · 버전 · 댓글 개념). 동작 숫자는 코드 기준.

## 목차(이 순서)

1. 무엇이 생겼나 — 「예약 요청」= 링키가 요청을 보내면 병원 코디가 현황판 스레드에서 확인하고 [예약 생성]. 바로 예약하는 기존 `POST /reservations` 와 차이 한 줄.
2. 키 · 헤더 — **키 바뀜**: 병원당 키 하나(링키 · 차티 공용) · 옛 키 안 됨 · 선택 `X-Day-Client`(형식) · `X-Api-Key` · `Idempotency-Key`(쓰기 필수 · 재시도 규칙) · 한도 병원 분당 60.
3. 경로 8개 표(E1 ~ E8 · 메서드 · 경로 · 하는 일 · 성공 코드).
4. 요청 본문 칸 표(필수 · 형식 · 길이 · 값 목록 SNS · 통역 언어) + 예시 JSON 하나(가짜 값).
5. 값 사전 — `status` · `closedReason` · `kind` · 댓글 `type` · `state` · `action` · `author.side` 값마다 뜻.
6. 상태 × 행동 표(be-swagger-1 ② 그대로) + 상태 그림(text 다이어그램).
7. 오류 코드 표(공통 + 경로별).
8. 흐름 예시 셋 — 요청/응답 순서로: ① 신규 → 병원 변경 요청(`change_request` · `proposals`) → 링키 `change` → 병원 생성(`reservation_applied` `create`) ② 확정 뒤 취소 ③ 같은 고객이 여럿 → 병원 「고객 확인 필요」 댓글 → `customerId` 넣은 `change`.
9. 초진 · 재진 판정 규칙 · `customerId` 얻는 길(`/customers/lookup`).
10. 병원 처리 알기 — E4 `updated_since` 폴링(5분 겹쳐 읽기 · 거르는 법) → E5.
11. 알아 둘 것 — 생성 전 `change` = `new` 로 기록 · 버전 번호는 서버 · 예약 있는 스레드에 다른 고객 `change` = 400 · 자동 처리(`expired` · `canceled`).

## 금지 (이 레포는 PUBLIC)

- 키 값 · 서버 주소 · 실제 병원 id · 직원 이름 · 고객 정보 **넣지 않는다**. 주소는 `<DAY ext 주소>` · 키는 `<병원 키>` 자리로.
- 화면 문구 · 미정 사항을 확정된 것처럼 쓰지 않는다. 열린 것은 마지막 「아직 정하지 않은 것」 절에(예: 에이전시 페이지는 이 문서 범위 밖).

## 검증 · 보고

자체 대조: 문서의 enum 값 · 오류 코드 · 칸 이름이 코드와 글자 그대로 같은지 표로 확인(리포트에). 비밀값 grep 0. 리포트 `planner-linky-guide-1-report.md`(이 폴더). 완료 보고는 브리프 §9 두 명령 · subject `planner 완료: 링키 설명서 md`.
