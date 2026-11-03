# [researcher] 1단계 D17 — 플랫폼 · 부속 6개 허가 포함 여부 + 놓친 허가

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. MFDS MCP `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp/`(NOTES.md 의 실호출 기록 참고) · emedi. 형식은 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d09-web.md` 와 같게. 행 상세 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` · `step1-decisions.json` D17 · BBL 은 `step1-cancel-recheck.json` 도.

## 대상
1. **BBL** — 본체 Joule(수허 18-144) · mJoule(수허 21-192) 허가에 BBL(IPL) 모듈 포함 여부. 이름 든 18-141 · 09-1220 은 취소
2. **BBL히어로** — mJoule(수허 21-192 · 반도체 레이저 수술기) 허가에 BBL HERO 포함 여부
3. **쿨미니** — 쿨스컬프팅 시스템 허가(수허 18-96 · 수인 21-4556)에 CoolMini 어플리케이터 포함 여부
4. **AUTO MTS** — 제인 10-343(모델 MICRO NEEDLE)에 본체 기계 포함 여부 · 본체 별도 허가
5. **모르페우스8** (InMode) — 놓친 허가 재탐색: 국내 수입사 후보 전부(인모드코리아 · 신한네트웍스 등) · 모델명 · 품목(고주파 · 마이크로니들 RF) · emedi(query2=Morpheus, 모피어스, 인모드). 기존 수허 19-352 등 인모드 허가 3건의 구성 확인
6. **제네오X** (Pollogen/Lumenis) — 놓친 본체 허가 재탐색: 루메니스비코리아 · Pollogen · 모델명(Geneo X · Geneo+ · TriPollar) · 품목

## 할 일
- 식약처 허가 상세(구성 · 모델 · 사용목적 · 첨부 모델 목록)로 포함 확인이 1순위. 없으면 수입 · 제조사 공식 자료(국내 사이트 · 카탈로그 · 보도) + URL
- 결과: 포함(허가번호 · 근거 문구) / 별도 허가(허가번호) / 확인 불가(질의 기록). 판매사 여러 개 · URL · 추정 금지

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d17.json` · `.md` 만. 원장 · 결정 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: D17 플랫폼 · 부속 6" \
  --body "제품별 결과(포함/별도 허가/확인 불가 · 허가번호) / 판매사"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — D17 플랫폼 · 부속 6. 상세는 인박스." --enter
```
