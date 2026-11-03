# [researcher] 실버 2단계(계열) 조사 — 문헌 기준 계열 정의 + 제품 352행 배치

너는 앞 판의 맥락이 없다. 아래 「읽을 것」부터 읽어라.

## 읽을 것
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`
- 결정표 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 — 정해진 것은 다시 논의하지 않는다
- 1단계 정본(고정 · 수정 금지) `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` — `items[]` 중 `active: true` 352행이 대상. 계열은 `family` · 이름 `2_names` · 허가 품목명 `4_license.licenses[].official_name` · `item`
- **분류 기준(문헌)** `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/literature-evidence.json` — `categories.M1~M17` 의 `name`(영문 임상 명칭)과 moa/effects 진술 · 인용(PMID)
- 문헌 검수 경위 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/docs/reviews/clinical-review.md` · 외부 코드 체계 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/docs/references/medical-codes.md`
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/taxonomy.json`(modality 17 · 항목 detail/extracted) · 기존 계열 초안 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/procedure-master-v3.json` `families`(M1~M17 + X1~X6 — X 는 워커 판단으로 세운 것이라 확정 아님)

## 사용자 확정(10-28) — 지켜라
- **계열 = 교과서 · 임상 · 학회 문헌 근거.** 기준은 literature-evidence 의 M1~M17 카테고리. 체계를 새로 짜지 않는다
- **계열을 늘리는 것은 경계가 완전히 다를 때만.** 새 계열은 「17개 정의 어디에도 안 들어간다」 + 「문헌에서 독립 분야로 다룬다」 근거(인용)가 둘 다 있을 때만 추천
- 리프팅(M9) · 스킨케어(M15) 같은 원천 계열도 문헌 카테고리다 — 목적·경로라고 빼지 마라
- 2단계 범위 = 계열 정의 + 제품→계열 연결. 「용도별」 하위 항목(턱선보톡스 등)의 단위 시술 재판정은 5단계 — 표시만. 부위 · 기법은 손대지 않는다
- 추정 금지. 근거(파일:줄 · PMID/DOI · URL) 없는 칸은 「확인 안 됨」

## 할 일

### A. 계열 정의 (계열 단위)
M1~M17 각각:
1. 정의 한 줄(무엇을 쓰는 시술인지) + 문헌 근거. literature-evidence 에 있으면 그 인용, 진술 0건 계열(M6 · M10 · M11 · M13 · M14)은 **정의를 확인할 인용**을 새로 찾는다(PubMed — PMID 를 NCBI ESummary 로 실재 확인. 임상 주장 검수는 범위 밖)
2. 공식 한글 이름 추천 + 근거(M1 은 「보툴리눔 톡신」 확정). 상담 용어 · 원천 이름은 동의어
3. 하위 계열 기준 추천 — 원천 하위(수입/국산 · 브랜드 · 재질별 · 형태별 · 용도별 …) 중 문헌 정의상 하위 계열인 것 / 제품 속성으로 뺄 것 / 5단계로 넘길 것

### B. 경계 판정 — 「17 안(어디) / 분리(새 계열) / 계열 밖」 중 하나 + 근거
코디 1차 훑기(이름만 본 것 — 확정 아님)에서 걸린 묶음. 아래 행 이름은 `2_names.display_name`:
- 지방분해주사 10행(벨카이라 · 올리핏 · 펜카이라 · 바이블 · 리포린 · 브이올렛 · 벨라콜린 · 밀리핏 · 원더브이 · 뉴비쥬) — M16 문헌은 정맥 영양 수액(IV micronutrient)
- 비침습 지방감소 장비 2행(트루스컬프트 RF · 바넥스 RF+석션 — 바넥스는 원천 M14 냉각에 있으나 설명이 RF) + 바넥스프로(M10)
- 진단 장비 4행(미라쥬 · 3D 메타뷰 · 마크뷰 · 스케나)
- 태반제제 2행(멜스몬 · 라이넥) · 먹는 약 아큐탄 · 콘투락투벡스
- **M15 메디컬스킨케어 65행** — 문헌 정의는 「Topical cosmeceuticals」. 필링(케미컬 · 허벌 · 해초) · LED 광 · 딥클렌징(수압 박피) · 주입 장비(큐어젯 · 미라젯 · 비타인젝터 등) · 초음파(LDM) · 자기장(헤어셀) · 제네오X · 올타이트 각각이 M15 정의에 드는지, 다른 M 에 드는지, 분리가 필요한지
- 엑소좀 — 문헌 M5 에 포함, 원천은 M4 · M17 에도. 어디에 둘지
- X1~X6(procedure-master-v3) 각각 — 위 판정과 같은 기준으로

이 목록 밖에서도 정의에 안 맞는 행을 찾으면 같은 형식으로 추가하라(아래 C 전수에서 나온다).

### C. 제품 352행 배치 (행 단위 · 전수)
행마다 근거(원천 detail/extracted · 허가 품목명 · 성분/원리)를 계열 정의(A)와 대조:
- **맞음** / **옮김**(어디로 + 근거) / **여러 계열**(복합 장비 — 주 계열 + 이유) / **판단 필요**(이유 한 줄)
- 자동 추가(`ledger_id` 가 `auto-`) 219행은 설명 ↔ 계열 대조를 특히 꼼꼼히(원천 자동 병합 오배치 사례: 바넥스 · 바넥스프로)
- 다른 계열끼리 합친 4건(하모니카 M3→M2 · 볼뉴머 M4→M9 · LDM M16→M15 · 아포지 플러스 현장 기기→M8) — 합쳐진 대표 행의 계열
- 계열 없는 현장 기기 29행(`family.name` 이 「원천 시술군 없음(현장 기기 …)」)에 계열 부여

## 산출 — 이 두 파일만
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step2-research.json` · `step2-research.md`. 원장 · 결정 · 원천 파일 수정 금지.

json: `families[]`(id · 정의 · 근거 · 추천 이름 · 동의어 · 하위 계열 처리) · `boundaries[]`(묶음 · 판정 · 근거 · 대상 ledger_id[]) · `rows[]`(ledger_id · 현재 계열 · 판정 · 추천 계열 · 근거)

md 맨 위(사용자가 이것만 읽고 판단할 수 있게):
1. **결정 묶음 목록** — 묶음마다 추천 한 줄 + 근거 한 줄 + 영향 행 수(「N행」 / 「N계열」 단위를 밝혀라)
2. **사용자가 최종 판단해야 하는 것만** 따로(이유 한 줄)
3. 셈: 맞음 / 옮김 / 여러 계열 / 판단 필요 행 수(합 352)
그 아래 계열별 · 행별 상세.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_99ecdef9-59f9-4620-8a6b-cfdd39f0bc09 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 2단계 계열 조사" \
  --body "결정 묶음 N개 / 사용자 판단 필요 N건 / 행 셈 맞음·옮김·여러·판단필요"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 2단계 계열 조사. 상세는 인박스." --enter
```
