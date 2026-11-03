# [researcher] 실버 5단계 추가 조사 — 계열 없는 시술 계열 판정 · 정체/성분 미상 11 웹 조사 (read-only)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 원장 · 결정 · 원천 수정 금지. 산출 2파일만.

## 읽을 것
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 2026-10-29 행 셋(5단계 시작 · **원칙: 클리닉에서 하는 시술은 전부 단위 시술 — 계열이 없으면 계열을 늘린다** · 웹 조사) · 2단계 계열 기준 행(10-28 「계열 = 문헌 · 늘리는 건 경계가 완전히 다를 때만(17 정의 밖 + 문헌 독립 분야)」)
- 앞 조사 `step5-research.json` · `.md`(F1 · F2 · F4 · F7 · ledger · unit_procedures) · 계열 `step2-families.json` · 기법 `step4-techniques.json` · 부위 `step3-sites.json` · 제품 `step1-products.json`
- 2단계 계열 조사 방식 참고 `step2-research.md`(문헌 근거 · PMID ESummary 확인)
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/` · MFDS MCP `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp/` · KPIC MCP `reference/2026-10-28-kpic-mcp/`

## A. 계열 없는 시술 — 계열 판정 (2단계 기준)
대상: 카복시테라피 1 · 반영구 화장 4(문제 트리 P1-7) · 소수술 4(서브시전 · 펀치 · 면포압출 · 스테로이드 병변 내 주사) · 태반주사 2(라엔넥 · 멜스몬) · 성장호르몬주사 1 · 헤어셀 1(자기장 탈모 치료기).
각각: 기존 18계열 정의에 드는가(어디) / 새 계열(17 정의 밖 + 문헌 독립 분야 — 인용 PMID 를 NCBI ESummary 로 실재 확인) / 새 계열이면 이름 · 정의 · 근거 · 하위 · 계열 기본 기법(4단계 노드) · 부위 + 그 시술이 만드는 단위 시술 키(계열 × 부위 × 기법)

## B. 정체 · 성분 미상 11 — 웹 조사 (논문 · 전문 자료 · 제조사 · 식약처 · 피부과 홈페이지)
- F4 정체 7: 사파이어레이저(「사파이어냉각팁 … 레이저 제모 및 모공관리」 — 어떤 장비 · 매질) · 에이팩(「진동형 마이크로니들링」 — 제조사 · 허가) · 파셀라 메디컬 경락(「경락 자극 · 림프순환 · 리프팅 준비」 — 의료 시술인가 관리인가 · 장비) · MPE(「줄기세포 다기능추출물」 — 제품 · 성분) · 프로락틴주사(「프로작 성분 … 탈모부위 주입」 — 실제 쓰는 성분 · 이름의 원래 제품) · 이모드(시장가 복부 · 힙 EMS — 장비 · 제조사 · 허가) · 수소토닝(듀오 하이드로젠 — 원리 · 장비)
- 성분 미상 수액 4: 셀디톡스수액 · 에너지부스트수액 · 이뮨코어수액 · 다이어트 수액 — 병원들이 이 이름으로 쓰는 실제 성분 구성(여러 병원이 다르면 다르다고 · 공통 성분)
- 항목마다: 정체 · 근거 URL/PMID · 근거 수준(강 = 제조사/허가/논문 · 중 = 여러 병원 일치 · 약 = 한 곳) · **5단계 행선지**(단위 시술 키 · 기존 키 동의어 · 1단계 새 제품 행 후보 · 성분이 여럿이면 키 처리 안) · 추정 금지 — 못 찾으면 「못 찾음 + 찾은 범위」

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step5-research2.json` · `.md`. md 맨 위: ① 계열 판정 표(시술 · 판정 · 새 계열이면 이름 · 근거 · 만드는 키 수) ② 정체/성분 11 표(정체 · 근거 수준 · 행선지) ③ **사용자 최종 판단만 한 표**(빈 추천 금지) ④ 2단계 계열 원장에 더해질 줄 · 1단계 제품 원장에 더해질 행 후보

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_cab3032d-a597-480f-91af-eeb8ccaf6855 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 5단계 추가 조사" \
  --body "새 계열 N / 기존 계열 N / 정체 밝힘 N/11 / 사용자 판단 N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 5단계 추가 조사. 상세는 인박스." --enter
```
