# [researcher] 제조사 · 제품/장비 원장 초안 — 식약처 조회 (승인 게이트 원료)

너는 **procedure-hub `researcher` 워커**다. 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` (아래 산출물 외 수정 금지)

## 1. 기준 (`orchestration/work/phub-recommend/`)

- `DEC-003.md` ← 원장 셋 필드(D-01) · 승인 게이트 · `_RESUME.md` §2 10-27 행(특히 OQ 처리 · 외국어 오타 → 게이트 · **OQ-I08 기본값 C: 정규화 완전 일치는 auto 지만 게이트에 「자동」으로 노출**)
- `SPEC-003-mfds-ingest.md` ← 질의 목록 규칙 · 매칭 규칙(정규화 완전 일치 = auto, 나머지 후보) · products_key — **이 규칙을 그대로 쓴다**(Hub 구현 전 수작업 초안이라 저장 위치만 다르다)
- 대상: `taxonomy-classify-v2.json` 의 kind product · device 항목(status 무관 — waiting_mfds 포함). 1차 검수 반려 사유에 사용자가 붙인 허가 정보(evidence)는 매칭 근거로 쓴다
- 원천: stg 저장본 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/` (taxonomy 제품 필드 · products.json · market-pricing 규격 표현)

## 2. 식약처 조회 도구

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp` 의 MCP 패키지를 **파이썬에서 직접** 쓴다(`cd /Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp && uv run python <스크립트>` 로 `mfds_mcp.tools` 함수 호출). 스크립트는 레포 밖 `/tmp/phub-master/` 에 둔다
- 키는 그 폴더 `.env` — 값을 출력 · 기록하지 마라. **캐시를 켠 채로**, 전체 호출 800회 이내(일일 상한 1000). 넓은 질의(결과 300 초과)는 SPEC-003 대로 빼고 표시
- 의약품(톡신 · 수액 성분 · 약) = drug_search/detail · 의료기기(필러 · 스킨부스터 · 실 · 장비) = device_search/detail · 업체 = device_company

## 3. 산출물

1. `orchestration/work/phub-recommend/product-master-draft.json`
   - `manufacturers[]`: id · 국문명 · **원어명**(의약품 ENTP_ENG_NAME / 의료기기 MANUF_NM, 표기 갈림은 정규화 + 원문 둘 다) · 국가 · 역할(제조 / 수입) · 동의어 · 출처
   - `products[]`: 원장 항목 id(taxonomy) · 원장 이름 · 계열 · 허가 구분(의약품 / 의료기기) · **match**: {status: auto | candidate | none | too_broad, candidates[]: {공식 품목명 · 영문명 · 업체 · 제조원 · 허가번호 · 허가일 · 상태(정상/취소) · 모델명 · 사용목적/효능 요약 · 규격(PACK_UNIT · MATERIAL_NAME) · 질의}, reason}
   - `specs[]`: 제품별 규격(허가 정보 · 시장가 표현에서) · 숫자 + 단위(ml→cc)
   - `summary`: status 별 건수 · 호출 수 · 캐시 적중 · 넓은 질의 수
2. `product-master-draft.md` — 사람이 읽는 요약(status 별 · 원어명 채운 수 · 대표 예 · 못 찾은 것 목록)

## 4. 제약

- 매칭은 결정론 규칙만(SPEC-003). 추측 · 편집거리 자동 확정 금지 — 애매하면 candidate
- 키 · 캐시 내용 원문을 산출물에 넣지 않는다(필요한 필드만). 업체 주소 등 쓰지 않는 필드 제외
- public — 키 · 실명(사람) 금지. 코드 · 다른 문서 수정 금지

## 5. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 제품 원장 초안" \
  --body "status 별 건수 / 원어명 채운 수 / 호출 수 / 미결"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 제품 원장 초안. 상세는 인박스." --enter
```
