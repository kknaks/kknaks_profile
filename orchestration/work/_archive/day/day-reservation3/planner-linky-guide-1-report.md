# planner-linky-guide-1 결과 보고 — 링키 개발자용 ext 예약 요청 설명서

## 상태: done (새 파일 하나 · 커밋 없음 · 코드 · mediness 수정 없음)

- 새 파일: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/reference/2026-11-26-reservation-request/linky-ext-reservation-request-guide.md`
- 목차는 지시 순서 1 ~ 11 그대로이고, 끝에 12 「아직 정하지 않은 것 · 바뀌는 중」을 더했습니다.

## 근거

- 코드는 워킹트리 기준입니다(BE 미커밋 변경 · HEAD `3543d8b2`).
  - `ext_reservation_request_docs.py`: FLOW · 상태 × 행동 · NOTES · E1 ~ E8 설명 · COMMON · 경로별 오류
  - `schemas/ext_reservation_request.py`: 칸 · 길이 · Literal · 값 뜻 표
  - `ext_reservation_requests.py`: 경로 · 성공 코드 · `Idempotency-Key` 범위
  - `ext.py`: `partner`(401 → 429 → 400 · 분당 60 · `X-Day-Client` 형식) · `_middleware`(IP 분당 10) · 앱 description · `/customers/lookup`
  - `policies/reservation_request.py`: `merged_memo` 형식 · 1000자
  - `ext_refresh.py`: lookup 404 · 409 코드
- be-swagger-1 ② 표는 문서 §6 에 글자 그대로 옮겼습니다. ③ 은 §7 에, ④ 는 「코드가 맞다」는 기준으로 반영했습니다. 판정 규칙(식별값 하나 이상), `birthDate` 선택, 예약이 취소된 스레드의 `cancel` = 202 `canceled`, 동기화 때 `canceled` 가 여기에 해당합니다.
- be-swagger-2 는 아직 반영 전입니다. `_replay` 가 여전히 `status="requested"` 를 돌려줍니다.
  - §2 에는 기준을 「처음 응답 그대로」로 적었습니다. 지금 코드가 다르다는 점과 그동안 E5 로 확인하라는 안내를 함께 적었습니다.
  - §12 에도 「고치는 중」으로 남겼습니다.
  - be-swagger-2 가 끝나면 §2 · §12 의 해당 줄을 지워야 합니다.

## 자체 대조

- 문서 안의 백틱 토큰(enum · 오류 코드 · 칸 · 헤더 이름)을 모두 뽑았습니다. 그다음 위 코드 파일과 `common/error_codes.py` 를 합친 글에서 글자 그대로 grep 했습니다.
  - 결과: 없음 1건, `Content-Type`(HTTP 표준 헤더 · 코드에 둘 필요 없음).
  - 나머지는 모두 일치합니다.

| 묶음 | 문서 값 | 코드 |
|---|---|---|
| `status` | requested · confirmed · canceled · closed | `STATUS` Literal |
| `closedReason` | withdrawn · expired · folded | `ExtRequestDetail.closedReason` |
| `kind` | new · change · cancel | `KIND` |
| 댓글 `type` | message · change_request · reservation_applied | `ExtRequestCommentView.type` |
| `state` | waiting · superseded · withdrawn | 같은 클래스 `state` |
| `action` | create · update · cancel | 같은 클래스 `action` |
| `author.side` | hospital · partner · system | `ExtRequestAuthor.side` |
| SNS | etc · kakaotalk · line · instagram · whatsapp · wechat | `SNS` |
| 통역 | en · ja · zh · zh-Hant · th · vi · yue | `LANGUAGE` |
| 공통 오류 | invalid_request · ext_unauthorized · http_error · too_many_requests · internal_error · ext_unavailable | `COMMON` · `METHOD` · `ext.py` |
| 경로 오류 | request_past_start · memo_too_long · customer_not_found · idempotency_conflict · customer_changed · request_not_found · request_not_applied · request_finished · request_already_applied · request_closed | `docs` E1 ~ E6 `_ERRORS` |
| lookup | customer_not_found · customer_ambiguous · kos_unavailable | `ext_refresh` · `ext.py:520` |
| 길이 | name 100 · phoneticName 100 · sns.id 1~100 · email 254 · desiredProcedures 500 · memo 1000 · reason 500 · body 1~1000 · authorName 50 · Idempotency-Key 1~128 · X-Day-Client 1~16 · dial 1~4 · number 4~15 · E4 100개 | 스키마 `Field` · 패턴 |

- 비밀값 grep(키 형태 32자 이상 · URL · 도메인 · 이메일 · 전화 · 실제 UUID) 결과는 0건입니다. 예시 UUID 는 모두 `00000000-…` 이고, 주소는 `<DAY ext 주소>`, 키는 `<병원 키>` 입니다.
- 실명 · 병원 id · 고객 정보는 없습니다. 예시 고객은 스키마 `examples` 의 가짜 값(`HONG GILDONG` · `886`/`900000000` · `example.id`)입니다.

## 지시에 없던 것 · 주의점

- §9 에 lookup 409 `customer_ambiguous`(같은 이름 · 이메일 고객 여럿)를 적었습니다. 링키가 `customerId` 를 얻는 길에서 실제로 나는 코드라서 넣었습니다.
- §2 에 「스웨거 화면은 별도 Basic 로그인」을 적었습니다(`_docs_allowed`). 계정 값은 적지 않았습니다.
- §10 에 「댓글만 바뀌면 `latestVersion` 이 그대로이니 `updatedAt` 도 함께 비교」를 적었습니다. 코드의 「`requestId` · `latestVersion` 으로 거른다」에서 따라 나오는 주의라 덧붙였습니다. 빼고 싶으면 한 줄만 지우면 됩니다.
- 메모 필드 이름 · 언어 이름 · 화면 문구는 OQ-Q04 의 임시값이라 §12 에 「임시」로 두었습니다. 「고객 확인 필요」 `body` 를 글자로 분기하지 말라는 안내도 넣었습니다.
- 옛 키 전환은 「예전 링키용 키는 안 씀 · 병원 키를 새로 받기 · 값은 별도 경로」까지만 적었습니다. 전환 날짜 · 방법은 근거가 없어 적지 않았습니다.
