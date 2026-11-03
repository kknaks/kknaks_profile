# [researcher] 1단계 — 「허가 취소(이력)」 22개 현재 허가 재조사

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 왜
젠틀맥스프로는 옛 허가(신한씨스텍)만 취소됐고 현재 정품 허가(수허 18-338 시너론켄델라코리아)는 따로 있었다(`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d09-web.md` ③). 「취소뿐」 22개가 같은 경우일 수 있다 — 지금은 전부 추천에서 빠져 있다.

## 대상
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` 에서 `4_license.status == "허가 취소(이력)"` 인 22행 전부(아쿠아미드 · 해피리프트 · 오메가리프트 · BBL · BBL스킨타이트 · 브이빔 · 브이빔퍼펙타 · 젠틀맥스프로 · 젠틀레이즈 · 벡터스 · E-MAX · 펠레베 … — 파일에서 직접 세라). 젠틀맥스프로 · 젠틀레이즈는 `step1-d09-web` 결과(18-338 · 18-315 후보)를 확인만.

## 할 일 (행마다)
1. 현재 허가 찾기 — 식약처 API(제조 · 수입 **업체명** 전부: 원 제조사 · 현 국내 법인 · 수입사 후보 / 제품명 · 영문 · 모델명 · 품목) + emedi(query2 = 제품명 · 영문 · 제조사). 수입사가 바뀐 경우를 특히 본다
2. 국내 현재 유통 여부(웹 · 대한민국 기준) — 제조 · 수입사 공식 · 보도 · 병원 장비 소개, URL 필수
3. 결과 = 「현재 허가 있음(허가번호 · 업체 · 모델 · 상태)」 / 「현재 허가 없음(질의 기록 전부)」. 재제조 허가는 「재제조」로 구분(정품 아님)
4. 판매사 여러 개 가능 · 출처 URL
- 추정 금지 · URL/질의 없는 칸 금지

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-cancel-recheck.json` · `.md` 만. 원장 · 결정 파일 수정 금지(코디가 반영 판단)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 취소(이력) 22 재조사" \
  --body "현재 허가 찾음 N(제품 · 허가번호) / 없음 N / 재제조만 N"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 취소(이력) 22 재조사. 상세는 인박스." --enter
```
