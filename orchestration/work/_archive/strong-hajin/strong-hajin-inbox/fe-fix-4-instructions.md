# [frontend] FE 수정 판 4 — 방 추가 성공인데 「Unexpected end of JSON input」 토스트 (사용자 2026-10-06)

재현: 설정 > 슬랙 연동 > 방 추가 > DM 하나 선택 > 「선택한 1개 추가」 → 방은 **실제로 추가됨**(목록에 「추가됨」·「과거 메시지 채우는 중」) 그런데 오류 토스트 「Unexpected end of JSON input」.
원인 추정: `POST /api/integrations/{id}/rooms` 는 **202 + 빈 본문**(be3/be-fix 보고) — `lib/api.ts` 가 빈 본문에 `res.json()` 을 부른다.
고칠 것: api.ts 공통 처리에서 **204·202 빈 본문·Content-Length 0** 이면 JSON 파싱하지 않기(다른 빈 본문 응답 — DELETE 방 · disconnect · read-all · 읽음 등 — 도 전수 grep) · 시험. `frontend/src/` 만 · 커밋 금지 · 끝나면 §9(subject "frontend 완료: FE 수정 판 4") · 코디 핸들 term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b
