# [researcher] 업체 관계 조사 — 「이름은 맞는데 업체가 다른」 제품 23개

역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md` (read-only). 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 배경
제품 매칭 게이트의 「직접 확인」 23개는 **원장(Procedure Hub)에 적힌 업체**와 **식약처 허가 업체(+제조원)**가 글자가 다르다. 예: 더채움 — 원장 「휴젤」 / 식약처 허가 「(주)아크로스」(허가번호 제허 20-527 = 국내 제조 허가).
사용자 지시(10-27): **「휴젤이 판매사다」 같은 관계는 조사해서 근거를 달고 넣는다. 근거 없이 단정하지 않는다.**

## 대상
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/gate-answers/product-match.json` 의 `status: pending` 23개(ledger_id)
- 각 항목의 원장 업체 · 식약처 후보(공식명 · 허가 업체 · 제조원 · 허가번호 · 상태)는 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/product-master-draft.json` 의 같은 id 행(match.candidates)

## 할 일 — 항목마다
1. 원장 업체와 식약처 허가 업체의 **관계**를 웹으로 확인(회사 공식 사이트 · 공시 · 보도 · 식약처 · 제품 공식 페이지 우선). 분류:
   - 제조사 = 판매사가 다른 경우(위탁 생산 · 판매 계약) / 같은 그룹 계열사(지분 관계 출처 필요) / 수입사 변경(이전 · 현재) / 원장 업체 표기 오류 / **다른 제품**(이름만 같음) / 확인 불가
2. 그 근거로 **같은 제품인가**: 예 · 아니오 · 확인 불가
3. 원장에 넣을 역할: 제조사 · 수입사 · 판매사(브랜드사) 각각 누구인지 — 확인된 것만
4. 출처 URL 필수. 출처끼리 다르면 둘 다 적고 「충돌」

## 산출물
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/company-relation-check.json` · `.md` — md 맨 위 표: 원장 이름 | 원장 업체 | 식약처 허가 업체(제조원) | 관계 | 같은 제품? | 근거(URL)
- 결정하지 않는다 — 판단 근거만. 사용자가 이 표로 결정한다

## 제약
- 식약처 · stg 호출 금지(이미 받은 데이터 사용). 다른 파일 수정 금지. 근거 없는 추정은 「확인 불가」

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 업체 관계 조사" \
  --body "같은 제품 예/아니오/확인 불가 수 · 관계 분류별 수 · 미결"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 업체 관계 조사. 상세는 인박스." --enter
```
