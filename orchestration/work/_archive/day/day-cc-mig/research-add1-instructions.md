# researcher 추가 지시 1 — Swagger (사용자 2026-11-20)

같은 리포트(`research-cc-ext-report.md`)에 **D 절**로 더한다. 범위 제약(read-only · 외부 호출 금지 · 비밀값 금지 · 결정 금지)은 브리프 그대로.

배경: cc 에 ext Swagger 를 이미 썼는데, 다른 개발자들이 **각 필드가 무엇을 뜻하는지 명확히 알려 달라**고 요청했다. 이관 때 Swagger 도 함께 옮기고, 이번에는 **Swagger 에 로그인**을 넣는다.

- **D1. cc Swagger 현황** — 문서 URL · 노출 방식(공개 여부 · 어떤 라우터만 포함) · 설정 코드(파일:줄) · `test_ext_docs.py` 가 지키는 것 · 회고 `log/2026-11-12-api-swagger-docs.md` 에 남은 결정.
- **D2. 필드 설명 상태** — A2 의 필드 표에 칸을 하나 더 둔다: Swagger 상 설명(그대로 인용) · 판정 `충분`(뜻 · 출처 시점 · 단위 · null 일 때를 다 말함) / `부족`(무엇이 빠졌나) / `없음`. 엔드포인트별 집계를 요약에 넣는다. A2-1 「뜻 불일치 후보」와 겹치면 표시.
- **D3. 로그인 관련 사실** — cc Swagger 에 지금 인증이 있나(문서 페이지 보호 · Try it out 의 연동처 키 Authorize 버튼, 각각). DAY `origin/dev` 의 docs 설정(FastAPI `docs_url` · `openapi_url` 등)과 DAY 의 로그인 수단(세션 로그인 · 시스템 계정 등, 파일:줄). 두 방식을 붙일 수 있는 자리만 사실로 적고, 어느 것을 쓸지는 C 「정할 것」에 올린다.
