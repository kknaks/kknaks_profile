# 코드 리뷰 r3 WARN 수정 (코디 · 2026-10-27) — 작게

리뷰 `reservation-review-code-r3.md`(FAIL 0 · WARN 3). 커밋 금지 · 끝나면 같은 두 명령으로 보고(보고서에 「리뷰 r3 수정」 절).

- **backend · W1**: `event_log(notice_save)` 키를 SPEC 대로 **`action` → `op`**. `requestedNoticeId` · `length` 는 남긴다(코디가 SPEC 에 더한다). 시험이 키를 보면 같이 고친다. `ruff` · `pytest`
- **frontend · W2**: [오늘]이 **날짜가 바뀔 때만** 편집을 버린다(이미 오늘이면 그대로) · **W3**: [수정하기] 다시 읽기 응답이 왔을 때 지금 보는 날짜와 다르면 버린다(`setDraft` 안 함). `tsc` · `lint`

- **planner · W1 문서**: SPEC-005 §3.2 `notice_save` 줄을 `{date, noticeId, op, requestedNoticeId, length}` 로 — `requestedNoticeId` = 요청 값(기록용) · `length` = 저장한 글자 수(내용 아님). 0.4.0 변경 표 한 줄 · log. 보고서 「리뷰 r3 수정」 절
