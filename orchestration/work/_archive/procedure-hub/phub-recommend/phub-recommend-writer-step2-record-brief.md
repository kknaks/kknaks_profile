# [writer] 실버 2단계(계열) 과정 기록 — 전후 비교 · 교육 자료 · 갱신 근거

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.
**1단계 기록과 같은 형식 · 같은 자리**: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-28-silver-step1-product-normalization.md` 를 먼저 읽고 그 틀(0 요약 · 1 왜 · 2 전후 · 3 규칙 · 4 과정 · 5 틀린 것 · 6 남은 것)을 따른다. 새 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-28-silver-step2-family.md` · README 지도(`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/README.md`)에 한 줄.

## 사용자 요구(10-28)
새 제품 · 기존 제품 수정 때 업데이트하는 구조(스킬)를 만들기 위한 **근거 자료**. 1단계 기록처럼 — 전후 비교 · 정한 규칙(왜 · 예) · 과정 · 틀린 것.

## 원천 (전부 읽어라)
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 10-28 행 전부(2단계 계열 기준 · 조사 반영 · 재검수 v2 WARN 처리 · 하위 계열도 주 · 보조로 · open 해결안 반영 · ~~마감 철회~~)
- 전: `step1-products.json` 의 `family`(67가지 표기) · `procedure-master-v3.json` families(M1~M17 + X1~X6) · stg `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/taxonomy.json` modality
- 기준: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/literature-evidence.json` · `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/docs/reviews/clinical-review.md` · `docs/references/medical-codes.md`
- 과정 · 후: `step2-research.*`(D01~D18) · `step2-apply.py` · `step2-families.json` · `.md`(최종) · `step2-open-resolve.*` · `step2-origin-questions.md` · 검수 `review-step2-report.md` · `-v2` · `-v3` · `-v4` · `-v5`(최종 PASS) · `step2-families.v3.json`(v3 시점 사본)
- 브리프 `phub-recommend-step2-*-brief.md` · `phub-recommend-review-step2*-brief.md`

## 담을 것
1. **왜** — 원천 계열이 왜 그대로 못 쓰였나(표기 67가지 · 원천 하위에 수입/국산 · 브랜드 · 용도 섞임 · auto- 오배치(바넥스) · 계열 없는 현장 기기 · X 계열을 워커가 세움) — 실제 예로
2. **전후** — 수치 표(계열 수 · 행 판정 셈 · 하위 계열 채움 · open) + 같은 제품 전/후 5~8개(바넥스 · 지방분해주사(벨카이라) · LED(옴니룩스) · hADM(리투오) · 젠틀맥스 프로(주 · 보조 매질) · 소노퀸(조사 정정) · 트리필 프로 · 소프라노 티타늄)
3. **정한 규칙** — 한 줄 + 왜 + 예: 계열 = 문헌 카테고리 · 늘리는 건 경계가 완전히 다를 때만(N1 은 되고 카복시 · LED · 비침습 지방감소는 안 된 이유) · 하위 계열 처리(속성 · 다른 단계로) · M8 하위 = 매질 한 축, 방식은 4단계 기법 · 주 + 보조(계열 · 하위 둘 다) · 허가 품목 > 원천 설명(충돌 기록) · 근거 약은 값 + 표시 · 정체 미확인은 계열도 보류 · 이름 = 국내 공식 출처 있으면 그것
4. **과정** — 조사 → 결정 묶음 → 반영 → 검수 고리 · 검수 4판(FAIL → PASS → PASS → 최종) · open 처리
5. **틀린 것 · 배운 것** — 정직하게: 코디가 「물질 · 에너지원 재분류」를 제안했다가 사용자 정정(리프팅 · 스킨케어도 문헌 카테고리 — 기준은 레포 문헌부터) · 기본값(하위 한 칸 · 칸 안 만듦)이 open 22 를 만듦 · 검수 PASS 를 단계 끝으로 착각(끝 = open 0) · 조사 파일 recommended_family 기재 오류 4행 · 셈 실수
6. **남은 것** — 원장님 문의 3 · 근거 약 9 확인 질문 · 4단계로 넘긴 메모(technique_hint 재확인 · 매질 충돌 6) · 원천 수정 후보
- 실명(개인) · 키 금지. 수치는 파일에서 다시 세어 쓴다(이 브리프 수치 베끼지 말 것). 추정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_afa7e146-d56c-45ce-b965-abdcc356d9ce \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: 2단계 계열 기록" \
  --body "파일 경로 / 섹션 / 전후 수치 요약"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] writer 완료 — 2단계 계열 기록. 상세는 인박스." --enter
```
