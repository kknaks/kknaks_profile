# backend BE4 수정 1 — 목록 밖 옵션을 상품 id 로 (코디 실물)

코디가 9 · 10 · 11월을 [전체 다시 받기] + 상품 받기 한 뒤 셈(숫자 · 실결제는 옮기기 전과 같음):
- 9월 키: product 1,367 · **option 1,002** · name 110 / 10월: product 1,393 · option 52 · name 59 / 11월: product 98 · name 3
- option 키의 꼴: 「[오픈] 피코토닝」 · 「[첫방문] 포텐자」 처럼 **지금도 있는 상품**인데, 그때 팔린 옵션이 지금 목록(⑦ — 삭제 안 된 것만)에 없다(옵션 교체 · 이벤트 종료)
- 공개 스펙: ⑦ `deleted` 요청값은 무시(삭제 안 된 것만) · `getProductOptions` 응답(`ProductOptionDetail`)엔 **상품 id 칸이 없다** → 옵션 id 로 상품을 찾을 공개 길 없음

규칙(추가):
1. option 키가 되는 줄은 ⑤ `optionConfiguration.productTitle`(그때의 상품 이름)을 ⑦ 목록의 상품 `title` 과 맞춰 **하나로 정해지면 그 상품 id**(`by = product_title` 같은 새 by 값) · 둘 이상/없음이면 지금처럼 option 키
2. 저장된 품목에 다시 적용(상품 받기 · 품목 저장 때) — KOS 다시 안 불러도 되게(⑤ productTitle 저장 칸이 없으면 더함)
3. 셈: counts 에 by 별 수 · 시험(옵션 교체된 상품 → 상품 id · 이름 둘 → option 유지)
- 8800 · back/data · back/.env · 운영 PG(5434) 건드리지 마라(dev PG 5433 · testcontainers 만) · ruff · pytest · WP-BE4 §9 두 채널 · subject 「backend BE4 수정 1 완료」
