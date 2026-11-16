# [researcher] 1단계 D18 — 비슷한 이름 허가 후보 11개 「같은 제품인가」

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 형식은 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d09-web.md` 와 같게. 행 상세 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` · `step1-decisions.json` D18 · 원천 설명 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/taxonomy.json`(detail · extracted).

## 질문 (행마다 하나)
「식약처의 비슷한 이름 허가(후보)가 원장 제품과 **같은 제품인가**?」 → 같음 / 다름(실제 무엇인지) / 확인 불가(질의 기록)

## 대상 11
쿨소닉(후보 아스테라시스 제허 25-78 「Liftera Cool 외 1건」 · IR 2025-02-10 「쿨소닉 식약처 승인」 — 허가 상세 모델 목록에 CoolSoniq 있는지) · 바넥스 · 바넥스프로(후보 BTL Vanquish Me 13-3408 — 원천은 RF+석션 · RF+EMS+석션, 실제 제조사 · 국내 허가) · 피코코어(후보 블루코어 Picore 20-59 · 원장 업체 루트로닉) · 아큐어(후보 ACURE e · Acure 레이저 — 원장 계열 RF 리프팅) · 헤어셀(후보 트리비스 H-Cell ST 제인 12-1201) · 힐퓨전프로(후보 힐룩스 HFUSION 제인 26-4871) · 트리필 프로(후보 엠큐어 TF2004NIWS 제인 21-4246) · 오메가라이트(이름 든 허가 전부 취하 · 취소 — 현장 LED 의 실제 제품 · 현행 허가) · 아톰레이저(후보 대주메디테크 ATOM Laser 21-712 · 사진 업체 LCI) · 스킨스탬프(대종의료기 · 비즈엔몰드 여러 개 — 일반 명칭인지)

## 출처 (대한민국 기준) — **피부과 홈페이지 우선(사용자 지시)**
- **데이뷰의원 · 세라믹의원(사용자 지정) 공식 홈페이지**의 장비 · 시술 소개 페이지에서 각 장비의 정식 이름 · 제조사 · 사진 · 설명을 먼저 본다(공식 URL 은 직접 찾아라)
- 그다음 다른 피부과 장비 소개 · 제조 · 수입사 공식 · 보도 · 식약처 허가 상세(모델 목록 · 사용목적) · 현장 사진 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-reference-image/`
- 병원 페이지 문구는 그대로 인용 + URL. 판매사 여러 개 가능. 추정 금지

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d18.json` · `.md` 만. 원장 · 결정 파일 수정 금지. md 맨 위에 **행마다 한 줄 결론**(사용자가 읽을 수 있게 쉬운 말)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: D18 11개" \
  --body "같음 N / 다름 N / 확인 불가 N — 행별 한 줄"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — D18 11개. 상세는 인박스." --enter
```
