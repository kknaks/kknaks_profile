# 계약 v3 — 공지 수정 (backend ↔ frontend) · 결정 R58 ~ R61

## 보기 모델 (기존 `notice` 바꿈)
notice { content: str|null (그 날짜 첫 공지 · 없으면 null), editable: bool (date >= 오늘 KST ∧ 권한 reservation.notice edit), date: "YYYY-MM-DD" }
- 일반 · 조각 · poll=1 응답 모두. 빈 상태는 지금 화면 그대로.

## 저장
`PUT /reservations/notice` (HTMX · form: date, content)
- 200 → 공지 칸 조각(`#reservation-notice` · 저장 뒤 다시 읽은 값) + HX-Trigger 로 성공 알림(문구 「공지를 저장했어요」)
- 400 invalid(길이 2,000 초과 · 날짜 꼴) · 403 권한 · 409 notice_past_date · 409 kos_rejected · 503 kos_unavailable(기존 KosUnavailable 재사용 · 보충 2) → 화면은 편집 상태와 글 그대로 + 칸 안 「저장하지 못했습니다」 · 「다시 시도」(다시 시도 = 같은 저장 다시)
- 응답 본문 오류 꼴은 기존 DAY 오류 규약 따름(backend 가 worker_done 에 적음)

## 보충 1 (R62 ② · 검수 10 W10-2)
- 보기 모델 `notice.id: str|null` — 화면이 보인 공지의 DAY `notice.id`(없으면 null).
- 저장 form 에 `notice_id`(위 값 · 없으면 빈 값). backend 는 이 id 의 `external_ref` KOS id 가 다시 읽은 목록에 있으면 그 공지를 대상으로, 없으면 목록 첫 번째.
- 보충 2: KOS 장애 = 503 kos_unavailable(기존 예외 재사용 · taut 규칙 · backend 질문 답 A). SPEC 문구 502 → 503 정정은 다음 planner 판에.
