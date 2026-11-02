# frontend WP-FIX3 추가 지시 1 (코디 · 2026-10-27)

review-doc r3 처분(`reservation-review-doc-r3-dispositions.md`) 중 frontend 몫:
- 공지는 board `notices` **첫 번째 하나만** 그리고, 저장 때 그 공지의 `id` 를 `noticeId` 로 보낸다(없으면 null)
- 글자 수 「n / 2000」 · 2000 넘으면 [저장] 끔 = **trim 길이**로 센다(back 과 같음)
- **편집 중 날짜 이동**(‹ › · [오늘] · 달력): 막지 않고 편집을 버린다 + 토스트 「저장하지 않은 공지 편집을 취소했어요」
- 드래그 원인이 `procedure/front/app/**` · 공용 컴포넌트에 있으면 **고쳐도 된다**(범위 넓힘) · 원인은 보고에
