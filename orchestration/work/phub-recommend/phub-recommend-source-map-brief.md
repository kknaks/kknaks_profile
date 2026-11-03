# [researcher] 원천 21개 JSON 전수 행선지 지도 — 메달리온에 전부 녹이기 (read-only)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

이전 작업(3단계)과 별개다. 원장 · 결정 · 원천 수정 금지. 산출 2파일만.

## 왜
사용자(10-28): 「지금 모든 json 이 메달리온에 녹아야 하는데」. 실버 8단계(1 제품 → 2 계열 → 3 부위 → 4 기법 → 5 단위 시술 → 6 목적 · 패키지 → 7 고민 → 8 관계 → 빌드)를 taxonomy 중심으로 짜고 단계마다 필요한 파일만 봐서, **어느 단계에도 없는 원천**(pih-risk · pre-procedure-checklist · consent-checklist · patient-education · post-procedure-timeline · procedure-comparison 등)이 물어볼 때마다 드러났다. 사용자는 고민(7) 자리와 combo-recipes 자리도 이상하다고 본다.

## 읽을 것
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 전부(특히 10-26 메달리온 · 경계 · 안전 엣지 · 10-27 단위 시술 정의 · 실버 순서 · 10-28 「단계로 넘길 결정」 줄) · `DEC-001.md` · `DEC-002.md` · `DEC-003.md` · `SPEC-004.md`(그래프 노드 16 · 엣지 16 · 원천 대응)
- 정본: `step1-products.json` · `step2-families.json` · `step3-sites.json` · `procedure-master-v3.json`(단위 시술 초안)
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/` 21파일 전부 · 메달리온 개요 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/resources/note/db/2026-09-10-data-medallion-overview.md`

## 할 것
1. **21파일 × 칸 전수**(키 경로 단위 — 배열 원소 키까지). 칸마다: 무엇인가(한 줄) · 단위(계열 / 원장 항목 / 단위 시술 / 고민 / 전역) · 행선지(실버 몇 단계 · 노드 / 속성 / 엣지 / 원문 보관 / 버림 — 이유) · 상태(끝 = 정본에 들어감 / 표시 = 넘김 표시만 / 결정됨 = 결정표에 자리 있음 / **미정**) · 근거(결정표 행 · DEC · SPEC 절)
2. **겹침 · 충돌**: 같은 사실이 여러 파일에 있는 곳(예: 금기 = contraindications · consent-checklist · taxonomy extracted.safety / 조합 = combo-recipes · problem-combos · synergy · treatment-sequence · treatment-optimization / 고민 = taxonomy.problem · problem-packages · problem-combos) — 어느 것이 정본이 될지 추천
3. **단계 순서 점검**: 지도로 볼 때 6 · 7 · 8 의 경계와 순서가 맞는지(고민 · 패키지 · 콤보 레시피 · 조합 엣지). 바꿔야 하면 추천 + 이유. **정해진 결정은 뒤집지 말고 충돌로만 적어라**
4. 미정 칸은 행선지 추천을 꼭 낸다(빈칸 금지)

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/source-map.json` · `source-map.md`. md 맨 위: ① 파일 21개 한 줄 표(파일 · 무엇 · 주 행선지 단계 · 칸 수 · 끝/표시/결정됨/미정 칸 수) ② 결정 묶음(묶음마다 추천 · 근거 · 영향 — 「N칸/N파일」 단위) ③ 사용자 최종 판단만 ④ 단계 순서 점검 결론

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_91895551-bfba-4dc0-bbba-c421fa65b2c5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 원천 21개 행선지 지도" \
  --body "칸 N · 미정 N · 결정 묶음 N · 사용자 판단 N · 순서 점검 결론 한 줄"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 원천 21개 행선지 지도. 상세는 인박스." --enter
```
