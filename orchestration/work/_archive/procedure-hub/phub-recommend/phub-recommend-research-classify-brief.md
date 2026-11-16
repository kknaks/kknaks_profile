# [researcher] taxonomy 시술 항목 521 → 축별 분류표 (DEC-002 기준 제안)

너는 **procedure-hub `researcher` 워커**다(read-only). 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` (아래 2개 파일 외 수정 금지)

## 1. 기준 (먼저 읽을 것 — `orchestration/work/phub-recommend/`)

- `DEC-002.md` ← **정본.** 단위 시술 = 무엇을(약제·장비 계열) × 어디에(부위) × 어떻게(기법). 제품·용량 = 속성, 목적 = 고민 엣지, 패키지 = 묶음. 이름 원칙(상담 용어). 부위 트리 37 노드. M1 31개 분류 예시 표(D-03)가 **분류 방식의 본보기**다
- `_RESUME.md` §2 마지막 행(10-27): 부위 추가 — 콧등(코 하위) · 손 · 발 · 다리 · 비키니 · 힙(바디 하위). 자갈턱 = 턱끝의 증상 → 고민
- 원천: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/taxonomy.json`(modality 17 → subcategories 74 → items 521. 항목의 이름 · 설명 · extra 필드 · 적응증 문장 전부) · 필요하면 같은 폴더 `market-pricing.json` · `products.json` · `problem-packages.json`

## 2. 할 일

taxonomy 시술 항목 521개 각각을 DEC-002 축으로 나누는 **제안**을 만든다. 사용자가 항목마다 답(맞음 / 고침 / 보류 + 메모)을 다는 화면(아티팩트)의 원료라 **JSON 이 정본**이다.

항목마다:
- `kind` — 이 항목이 원장에서 실제로 무엇인가: `product`(제품·브랜드) · `site_or_purpose`(용도별 — 부위나 목적) · `technique`(기법 변형) · `package`(묶음) · `unit_procedure`(이미 단위 시술에 가까움) · `device`(장비 모델) · `other`(약물 등 시술이 아닌 것 — 예: 이소트레티노인). 판정 못 하면 `unclear`
- `what` — 약제·장비 계열(시술군 M 코드 + 이름)
- `where` — 부위 노드 이름 배열(DEC-002 트리 + 위 추가분만. 트리에 없는 부위 표현이 나오면 `where_unmapped` 에 원문)
- `how_source` — **원천에 적힌 기법 표현 그대로**(예: 「교근축소」 「진피 주입」). 없으면 빈 배열. 지어내지 않는다
- `product` — 제품이면 제품 이름 · 제조사(원천 그대로)
- `purpose` — 목적 · 고민 표현(원천 그대로. 예: 「주름」 「다한증」 「미니리프팅」)
- `synonyms` — 구어 · 별칭 후보(원천 괄호 안 표현 등)
- `unit_procedures` — 이 항목이 풀리는 단위 시술 후보 목록 `[{what, where, how}]`(제품 항목이면 「이 제품을 쓰는 단위 시술」은 비우고 `product` 만)
- `confidence` — high / medium / low, `basis` — 판정 근거(원천 필드 인용 한 줄)
- `needs_medical_review` — 의학 판단이 필요한가
- `notes`

## 3. 산출물

1. `orchestration/work/phub-recommend/taxonomy-classify.json` — 정본:
```json
{ "generated_at": "...", "source_snapshot": "phub-stg-2026-10-26", "basis": "DEC-002",
  "summary": { "by_kind": {...}, "by_modality": {...}, "techniques_found": [{"term": "교근축소", "count": 3, "items": ["M1-3-2", ...]}], "unmapped_sites": [{"term": "...", "count": 0}] },
  "modalities": [{ "id": "M1", "name": "보톡스", "subcategories": [{"id": "M1-3", "label": "용도별", "kind_hint": "site_or_purpose"}] }],
  "items": [{ "id": "M1-3-2", "modality": "M1", "subcategory": "M1-3", "name": "사각턱", "source_text": "원천 이름 · 설명 요약", "kind": "...", "what": "...", "where": [], "where_unmapped": [], "how_source": [], "product": null, "purpose": null, "synonyms": [], "unit_procedures": [], "confidence": "high", "basis": "...", "needs_medical_review": false, "notes": "" }] }
```
   - M1 31개는 DEC-002 D-03 표와 **같은 판정**이어야 한다(다르면 notes 에 이유)
   - `techniques_found` 는 DEC-002 OQ-201(기법 목록)을 닫는 원료 — 원천 표현 · 횟수 · 항목 id
2. `orchestration/work/phub-recommend/taxonomy-classify.md` — 사람이 읽는 요약: kind 분포 · 시술군별 특징(어느 시술군은 제품 위주, 어느 쪽은 부위 위주) · 기법 표현 목록 · 트리 밖 부위 · low confidence · 의료 검토 목록. JSON 과 수치 일치

## 4. 제약

- 원천 저장본만 읽는다. stg · DB 접속 금지 · 코드 · 다른 문서 수정 금지
- **추측 금지** — 원천에 없는 기법 · 부위 · 제조사를 채우지 않는다. 모르면 빈 값 + `unclear` / low
- public — 키 · 실명 금지

## 5. 검증

JSON 이 json.tool 통과 · items 521 · id 중복 0 · M1 31 이 DEC-002 D-03 과 일치 · md 수치 일치

## 6. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_92a9e861-40e9-4ab0-bec1-e792cb83801e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 축별 분류표" \
  --body "kind 분포 / 기법 표현 수 / 트리 밖 부위 / low · 의료 검토 수 / M1 대조 결과 / 미결"

orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e \
  --text "[worker_done] researcher 완료 — 축별 분류표. 상세는 인박스." --enter
```
