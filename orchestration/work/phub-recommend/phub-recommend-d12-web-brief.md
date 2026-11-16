# [researcher] 1단계 D12 — 업체 관계 7개 국내 웹 확인 (판매사 여러 개)

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 방법 · 형식은 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d09-web.md` 와 같게.

## 대상 (`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-decisions.json` D12 · 행 상세 `step1-products.json`)
- ② 원장 업체 ≠ 허가 업체 — 사용자 판단 「원장 업체 = 판매사 · 허가 업체 = 식약처 허가사」. **이 관계의 출처를 찾는다**(판매 · 유통 · 공동판매 계약 보도, 공식 사이트 등)
  - 셀레스텔라(판매 더에쓰씨 · 허가 알에프바이오) · 힐로웨이브(하이어코퍼레이션 · 에스씨엘) · 테스리프트(리젠바이오텍 · 테스) · 블루로즈클레어(휴젤 · 제이월드)
- ③ 제조사 충돌 — 어느 회사가 제조 · 허가 · 판매인지 출처로
  - 큐라스토닝(허가 클래시스 · 제조원 칸 LaserPair · 유리드알앤디 ↔ C 기록 이루다 FDA K173038) · 아포지플러스(사진 Cynosure ↔ 허가 제조원 Cogmedix · 수입 루트로닉) · 아쿠아필(허가 엠아이테크 1건 — 판매사 · 현재 유통 확인)

## 할 일 (행마다, 대한민국 기준)
1. 관계 확인: 일치(출처) / 다름(실제 관계) / 확인 불가(질의 기록)
2. 판매사 전부(여러 개 가능 · 역할 표현 그대로 · URL · 시기)
3. 제조 · 수입 충돌은 덮어쓰지 않고 출처별로 기록
- 추정 금지 · URL 없는 칸 금지

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d12-web.json` · `.md` 만. 원장 · 결정 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: D12 업체 관계 웹 확인" \
  --body "② 관계 확인 결과 4 / ③ 충돌 정리 3 / 판매사"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — D12 업체 관계 웹 확인. 상세는 인박스." --enter
```
