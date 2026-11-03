# [researcher] 제품 원장 초안 2차 — 못 찾은 153개 다시 찾기

너는 직전에 `product-master-draft.json` 을 만든 researcher 다. 같은 스크립트 · 캐시(`/tmp/phub-master/`) · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp` 패키지를 그대로 쓴다.

## 사용자 지시(2026-10-27)

1. **업체명으로 찾는다** — 비교 · 검색에 업체명은 법인 표기(「(주)」「㈜」「주식회사」「유한회사」「Inc.」「Co., Ltd.」 등)를 떼고 쓴다. 이미 받은 응답(캐시)으로 1차 142 후보도 다시 매칭한다(추가 호출 없음)
2. **못 찾은 153개를 다시 찾는다** — 방법:
   - 원장에 업체(maker_texts)가 있으면 **그 업체 이름으로 의료기기 상세(ENTRPS) · 의약품 목록(entp_name) 을 조회**해 그 업체의 허가 목록을 받고, 계열(필러 → 조직수복용생체재료 등 품목명 · 사용목적)로 후보를 좁힌다
   - 원장에 업체가 없거나 업체로 못 찾으면, **영문 브랜드명 · 모델명 검색어를 만들어 TYPE_NAME 으로 조회해도 된다**(예: 이브아르 → YVOIRE, 테오시알 → Teosyal). 이 검색어는 추측이므로 질의에 `guessed: true` 로 표시
   - **추측 검색어 · 업체 목록으로 찾은 것은 절대 auto 로 확정하지 않는다** — 전부 candidate(사람이 게이트에서 판정)
   - 호출 상한: 이번 2차 400회 이내(오늘 누적 ~900). 결과가 300 넘는 업체는 계열 품목명(prduct)을 함께 걸어 좁힌다
3. 45개(no_service)는 그대로 두되, 항목마다 「무엇인지 한 줄」(원천 detail 요약)을 붙인다

## 산출물

- `product-master-draft.json` 을 **v2 로 갱신**(파일명 그대로, summary 에 1차 → 2차 변화 · 이번 호출 수). 각 product 의 match 에 `round: 1|2` · 질의마다 `guessed`
- `product-master-draft.md` 를 갱신: **맨 위에 사람이 읽는 표** — 시술군별로 「원장 이름 → 찾은 식약처 품목(공식명 · 업체 · 상태) 또는 못 찾음」. 기술 용어(status 코드 · OQ 번호)는 표 아래로

## 제약

- 키 · 캐시 원문 · 업체 주소 · 사업자번호를 산출물에 넣지 않는다. 다른 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 제품 원장 초안 2차" \
  --body "153 중 찾은 수 / auto · candidate · none 변화 / 이번 호출 수"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 제품 원장 초안 2차. 상세는 인박스." --enter
```
