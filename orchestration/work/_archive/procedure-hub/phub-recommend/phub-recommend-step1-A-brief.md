# [researcher] 1단계 제품 원장 — 구간 A (시술군 M1 · M2 · M3 · M4 · M7 (원장 126))

역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 목적
실버 1단계 = **제품 원장 확정.** 끝 조건은 **미확인 0** — 원천에 근거가 없으면 「근거 없음」을 근거와 함께 확정하는 것까지가 끝이다. 근거 없는 추정 · 추론 금지.

## 대상 — 구간 A
시술군 M1 · M2 · M3 · M4 · M7 (원장 126)
- 원장 제품 행: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/product-master-draft.json` 의 `products[]`(modality 로 거름) · 현장 기기: 같은 파일 `new_ledger_candidates[]`
- 이미 있는 재료(다시 조사하지 말고 먼저 쓴다): 각 행의 `match`(식약처 후보 · 1~4차) · `web`/`web4`(웹 조사 · 출처) · `photo_evidence` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/company-relation-check.json` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/gate-answers/company-relation-decisions.json`(23건 결정)
- 원천: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`(taxonomy · products · market-pricing)
- 도구: 식약처 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp` 패키지(`uv run python`, 키는 `.env` · 값 출력 금지) · 웹 검색. 재료로 안 풀리는 것만 새로 조사

## 항목마다 채울 것 (전부 · 빈칸이면 이유)
1. **정체**: 무엇인가(제품 / 장비 / 진단 장비 / 화장품 / 병원 메뉴명 / 시술 아님) · 계열(원천 시술군 코드)
2. **이름**: 원장 이름 · 제품 이름(정규화 — 식약처 공식명에서 제형·성분 괄호·용량을 뗀 브랜드명, 공식명 없으면 원장 이름) · 동의어(원장 이름 · 영문 · 오기는 「오기」 표시)
3. **라인 · 품목**: 라인 제품이면 라인 아래 품목 목록(허가별). 원장 항목 둘이 같은 허가를 가리키면 라인 + 품목으로 묶는다(예: 울쎄라 ⊃ 울쎄라 프라임)
4. **허가**: 허가번호 · 상태(정상/취소) · 구분(의약품/의료기기) — 없으면 상태를 **「허가 대상 아님(근거)」 · 「미허가(근거)」 · 「단종(근거)」 · 「확인 불가(조사 범위 · 근거)」** 중 하나로. 「확인 불가」는 실제로 다 찾아본 기록(질의 · URL)이 있을 때만
5. **규격**: 허가 포장단위 · 함량(1바이알당 100단위 등) · 시장가 표현 — 숫자 + 단위
6. **업체 역할**: 제조사 · 수입사 · 판매사 — 각각 이름(국문 · 원어) + 근거(식약처 필드 또는 URL). 국산이면 수입사 「해당 없음」. 근거 없으면 「근거 없음(조사 기록)」
7. **현장 사용**: 더데이랩스 사진 id(있으면)

## 산출물
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products-A.json` — items[] (위 1~7 필드 + 근거 목록) · summary(항목 수 · 허가 상태별 · 업체 역할 채움 수 · 확인 불가 수와 이유)
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products-A.md` — 사람이 읽는 표: 원장 이름 | 제품 이름 | 계열 | 허가(번호·상태) | 제조사 | 수입사 | 판매사 | 근거
- 다른 파일 수정 금지 · 키 · 실명(사람) 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 1단계 제품 구간 A" \
  --body "항목 수 / 허가 상태별 / 업체 역할 채움 / 확인 불가와 이유"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 1단계 제품 구간 A. 상세는 인박스." --enter
```
