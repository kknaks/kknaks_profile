# frontend WP-FE4 수정 1 — 상품 키 = KOS 상품 id (back 계약 바뀜)

back 이 상품 키를 id 로 바꿨다(사용자 결정). 바뀐 계약(back `schemas/sales.py` · `schemas/settings.py` 가 정본 — 읽어서 맞춰라):
- 응답 `lines[].productKey` 에 `key` · `by` · `productId` · `optionId`
- 설정 `rows[]` 에 `key` · `by` · `optionIds` · PUT 본문 = `rates[{key, rateBp}]` · `changes[].key`
- `counts.nameKeyedItems`(이름 키로 대체한 줄 수) — 결산/설정에 작게 표시
- 같은 이름 다른 id 상품은 **따로 줄** → 「같은 이름 n개」 배지 없앰 · 대신 이름 옆 작은 id 끝 4자리(구분용)
- `by = option` 줄 = 「KOS 목록에 없음」 · `by = name` 줄 = 「이름으로 연결」 회색 배지
`npx tsc --noEmit && npm run lint` · 가짜 응답 스크린샷 갱신(settings · monthly) · WP-FE4 §9 두 채널 · subject 「frontend FE4 수정 1 완료」
