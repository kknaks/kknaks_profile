# [writer] DEC-003 — 제조사 · 제품/장비 · 규격 원장 + 식약처 원천

너는 **procedure-hub `writer` 워커**다. 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` (코디 워크트리 공유)

## 1. SSOT (`orchestration/work/phub-recommend/`)

- `_RESUME.md` §2 — **2026-10-27 행 전부가 이번 결정의 정본**(특히 「실버에 제조사 · 제품/장비 · 규격 원장 추가」 · 「식약처 공개 허가 정보로 확인」 · 「부위 없는 시술」 · 「반려 ③」 · 「식약처 조회 MCP 작업용 reference」). 여기 없는 결정을 만들지 마라
- `DEC-002.md` — 단위 시술 정의 · 축(D-03) · 이름 원칙(D-04). DEC-003 은 그 위에 얹는다(번호 · 양식 동일)
- `taxonomy-classify.json` · `.md` — 제품 183 · 장비 157 판정과 §10 미결
- 1차 검수 답: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-----------/7f782343-8998-41d7-8392-00bd3c8596ee/scratchpad/classify-answers/answers/*.json` (항목 id → {decision, reason}). 반려 사유를 유형별로 읽는다 — 근거로 인용만, 사유 원문의 긴 설명은 옮기지 않는다
- 원천: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/` 의 `taxonomy.json`(제품 필드: 제조사 · 국가 · 식약처) · `products.json`(제품 · 제조사 사전) · `market-pricing.json`(규격 표현: cc · 바이알 · 샷 · 회)
- 식약처 API(공공데이터포털): 의약품 제품 허가정보 https://www.data.go.kr/data/15095677/openapi.do · 의료기기 품목허가 정보 https://www.data.go.kr/data/15057456/openapi.do · 의료기기 수입 및 제조허가 상세 https://www.data.go.kr/data/15073895/openapi.do · DUR 품목정보 https://www.data.go.kr/data/15059486/openapi.do
- 양식: `templates/projects/10-decision/decision.md`

## 2. DEC-003 에 담을 결정 (사용자 확정)

- **D-01 원장 셋** — 실버에 추가:
  - 제조사: 국문명 · **원어명** · 국가 · 동의어(예: 엘러간 / 애브비 / Allergan) · 출처
  - 제품·장비: 공식 품목명 · 제조사 · 계열(DEC-002 「무엇을」) · 성분/원리 · 허가 구분(의약품 / 의료기기) · 허가번호 · 허가일 · 효능효과 · **원장 이름 동의어**(리즈톡신 → 리즈톡스) · 출처
  - 규격: 제품별 단위(1cc · 2cc · 1바이알 · 900샷 · 100유닛 …) — 시장가 항목명에서 나온 표현
  - 필드 표는 「필드 · 뜻 · 원천(어느 파일/어느 API) · 필수 여부」로. **스키마 · 테이블 설계는 하지 않는다**(SPEC 몫)
- **D-02 시술 1회** = 단위 시술 + 제품 + 규격·양. 가격은 이 조합에 붙는다(시장가 원장 모양 근거)
- **D-03 공식 정보 원천 = 식약처 허가 정보.** 의약품(톡신 · 수액 성분 · 약)은 의약품 제품 허가정보, 의료기기(필러 · 스킨부스터 · 실 · PLLA · 장비)는 의료기기 품목허가 정보. 매칭 결과는 출처와 함께 승인 게이트로 확인
- **D-04 식약처 데이터 두 갈래** — ① Hub: 적재 스크립트가 API 를 직접 불러 응답을 **브론즈로 저장**(LLM 없음 — DEC-001 D-12) ② 작업용 MCP: 프로필 `reference/2026-10-27-mfds-mcp/` 에 직접 만든다(키는 env, 캐시 gitignore). 상담 에이전트 단계에서 DUR(병용 · 임부 · 연령 금기)도 이 MCP 로
- **D-05 부위 없는 시술** — 수액 · 정맥 = 부위 「전신」 + 기법 「정맥 주사」 / 원천에 부위가 없는 필링 등 = 기본 「얼굴 전체」. DEC-002 부위 트리에 「전신」이 이미 바디 하위에 있으면 그대로, 의미가 다르면 OQ 로
- **D-06 1차 검수 처리 원칙** — 반려를 유형으로 나눠 처리 경로를 정한다: ① 정체 확인 불가 → 식약처 원장이 생긴 뒤 재판정 ② 부위 없음 → D-05 로 재판정 ③ 판정 틀림(사유에 고칠 값 명시) → 적힌 대로 고쳐 재승인 ④ 분류 경계 → OQ 로 모아 사용자 결정 ⑤ 참고 자료(링크 · 허가 정보 붙임) → 해당 원장 행의 근거로 사용. 유형별 건수는 검수 답에서 센다
- **다음 단계(한 줄씩)**: 키로 API 실호출 → 응답 필드 확인 → MCP SPEC · 적재 SPEC → 원장 초안(승인 게이트) → 분류표 재판정

**OQ** — 결정하지 말고 질문 · 왜 · 영향 D: 원어명이 API 에 없을 때의 원천 · 해외 제조원과 국내 수입사를 둘 다 둘지 · 허가 안 된 제품(직구 · 화장품 계열 엑소좀 등) 처리 · 규격 표기 정규화 규칙 · 단종/취소 품목 · 반려 ④ 유형의 개별 질문(실 재질 · 도구명 vs 기법 · 마케팅명 · 패키지 구성)

## 3. allowed_paths

- 생성: `orchestration/work/phub-recommend/DEC-003.md` 1개만

## 4. 제약

- §2 에 없는 결정 추가 금지 — OQ 로. 스키마 · API 필드 설계 금지(API 응답을 아직 안 봤다 — 필드 표는 「원천에서 기대하는 것」으로 쓰고 확인은 다음 단계라고 적는다)
- API 를 호출하지 않는다(키 없음). stg 호출 금지. public — 키 · 실명 금지. 검수 사유에 실린 사람 이름 · 연락처가 있으면 옮기지 않는다

## 5. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_92a9e861-40e9-4ab0-bec1-e792cb83801e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: DEC-003" \
  --body "D 목록 / 원장별 필드 수 / 반려 유형별 건수 / OQ"

orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e \
  --text "[worker_done] writer 완료 — DEC-003. 상세는 인박스." --enter
```
