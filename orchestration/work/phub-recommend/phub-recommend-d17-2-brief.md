# [researcher] 1단계 D17 재조사 — 남은 4개

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 1차 결과 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d17.md` 를 이어서. MFDS MCP `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp/` · emedi.

## 대상 · 질문
1. **BBL** — Joule(수허 18-144)은 IPL 미포함. ① 원장 「BBL」(현장 · 원천 설명 확인)이 mJoule 의 BBL HERO 와 같은 것인지 ② Joule/BBL 계열 현행 국내 허가가 아이맥 · 사이톤 다른 허가(모델 목록 전체)에 있는지
2. **AUTO MTS** — 니들 허가(제인 10-343)만 있음. 원장 · 현장 사진(`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-reference-image/` 확인) · 원천 설명으로 **어느 회사 오토 MTS 인지** 특정 → 그 회사 본체 허가(전동식 MTS · 의료용 침 · 피부 미세침) 탐색
3. **모르페우스8** (InMode) — 신한네트웍스 허가 3건(19-352 · 21-205 · 26-107)의 **허가 상세 모델 목록 · 구성 · 사용목적 전체**에서 Morpheus8 핸드피스/모듈 포함 여부. 다른 수입사 · 병행수입 허가 탐색
4. **제네오X** (Pollogen/Lumenis, 2024-07 국내 출시 보도) — 루메니스비코리아 허가 전체 모델 목록(TriPollar · Geneo · OxyGeneo · 피부관리기 · 고주파 품목) · 품목 「미용기기」로 빠진 경우인지 · 다른 수입사

## 할 일
- 식약처 허가 상세(모델 · 구성 · 사용목적) 1순위 · 공식 자료 · 보도 URL. 결과 = 포함/별도 허가/확인 불가(질의 기록 전부). 판매사 여러 개 · 추정 금지

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d17-2.json` · `.md` 만. 원장 · 결정 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: D17 재조사 4" \
  --body "제품별 결과 · 허가번호 · 판매사"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — D17 재조사 4. 상세는 인박스." --enter
```
