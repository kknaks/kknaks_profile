# [researcher] 조사 4 — 「이름으로 KOS 검색 → 이메일로 거르기」가 되는지

너는 cc-prototype `researcher` 워커다. 원 브리프의 제약은 **그대로** 유효하다. 데모 키(`KOS_API_tenent_dev`)만 쓰고 운영 지점 키는 쓰지 않는다 · 조회만 한다(`/commands/` 0) · public 이라 이름 · 이메일 · 연락처 · id 값 · 토큰 · 키는 적지 않고 모양 · 건수 · 비율만 적는다 · 리포트 1개만 쓴다.

- 원 브리프: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/api-swagger-docs-research-brief.md`
- KOS 참고: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/reference/2026-10-12-cc-prototype/kos-demo-api.md` (내부 API 는 브라우저 UA 필수)
- 우리 코드(읽기만): `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/back/app/service/reservations.py` — `PATH_VISITORS="visitor/v2/queries/get-visitors"`(약 78줄) · `search()` 본문 · 약 167줄 `v.get("email")`(어느 응답에서 읽는지 확인)

## 배경 (사용자 결정)

외부 연동(링키 · 차티)에서 AI 또는 상담자가 **고객 이름 + 이메일(둘 다 필수)** 으로 고객을 찾고, 그 고객의 남은 시술권을 본다. 방식은 **KOS 를 이름으로 검색한 뒤 우리 쪽에서 이메일로 거른다**(사용자 결정 · 이메일 검색 조건 여부는 더 묻지 않는다). 이 방식이 실제로 되는지, 비용이 얼마인지만 확인한다.

## 알아낼 것

1. **검색 응답에 email 이 오는가** — 내부 `get-visitors`(우리가 쓰는 것) 목록 응답의 각 고객에 `email` 칸이 있는지. 없으면 고객 1명씩 상세(내부 `get-visitor` 또는 공개 `getVisitor`)를 불러야 하는지, 어느 쪽에 email 이 있는지. 공개 API `searchVisitors` 에도 같은 질문
2. **이름 검색의 성질** — `visitorName` 이 정확 일치인지 부분 일치인지 · 대소문자 · 공백 · 한글/영문 이름(외국인 고객이 많다) 표기 차이. 한 페이지 최대 건수 · 페이지 넘김. 데모에서 흔한 이름으로 검색했을 때 몇 명이 나오는지(건수만)
3. **email 채워진 비율** — 데모 고객 중 email 이 있는 비율(표본 크기와 함께). 같은 email 을 가진 고객이 둘 이상인 경우가 있는지(건수만)
4. **이메일 대조 규칙 후보** — KOS 에 저장된 email 모양(대소문자 섞임 · 앞뒤 공백 등이 있는지). 「정확 일치」로 할 때 놓치는 경우가 보이면 건수와 유형만
5. **호출 비용** — 이름 검색 1회 + (필요하면) 상세 N회 + 그 고객 시술권(`getTicketBundlesQuery` · 조사 2 기준 1~3호출)까지 1건 조회의 총 호출 수 · 걸린 시간(ms)
6. **동명이인 + 같은 email** 이면 무엇으로 갈라야 하는지 — 데모에서 실제로 생기는지만 확인(정하지 않는다)

## 산출물

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/research-name-email-lookup.md`
- 맨 위: 질문 1~6 한 줄 답 + **판정**(그대로 가능 / 상세 호출 추가하면 가능 / 막힘 · 이유)
- 1건 조회 호출 순서 그림(이름 검색 → (상세) → 이메일 대조 → 시술권)
- 정할 것(결정하지 않고 모음)

완료 보고는 원 브리프 §9 와 같은 두 채널로 한다(이번 dispatch 의 taskId · dispatchId 를 쓴다).
