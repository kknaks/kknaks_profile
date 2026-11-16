# [writer] 실버 3단계(부위) 과정 기록 — 전후 비교 · 교육 자료 · 갱신 근거

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.
**1 · 2단계 기록과 같은 형식 · 같은 자리**: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-28-silver-step1-product-normalization.md` · `2026-10-28-silver-step2-family.md` 를 먼저 읽고 그 틀(0 요약 · 1 왜 · 2 전후 · 3 규칙 · 4 과정 · 5 틀린 것 · 6 남은 것)을 따른다. 새 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-28-silver-step3-site.md` · README 지도에 한 줄.

## 원천 (전부 읽어라)
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 10-27 부위 행 · 10-28 3단계 행 전부(시작 · 조사 반영 · 끝 조건 = 지금 원천 · 부위 = 「어디에 맞냐」 = 몸 겉 · 해부학 용어 = 시술 방법 · 작용기전 · 안전 쪽 · 이름 2벌 · 끝)
- 전: `DEC-002.md` 부위 트리 · `procedure-master-v3.json` site_tree · site_out_of_tree / 후: `step3-sites.json` · `.md` · `step3-decisions.json` · `step3-lexicon.json` · `step3-source-fix.md` · `step3-fixtures/`
- 과정: `step3-research.*` · 브리프 `phub-recommend-step3-*-brief.md` · 검수 `review-step3-report.md` · `-v2` ~ `-v5`

## 담을 것
1. 왜 — 부위가 원천에 어떻게 흩어져 있었나(이름 칸 · 설명 문장 · 위험 부위 zone · 트리 밖 이름)
2. 전후 — 수치(노드 43 → 53 · 이름 칸 17 · 문자열 · 질문) + 같은 이름 전/후 6~8개(브라라인 → 등 · 엉덩이 → 힙 · 옆구리 새 노드 · 팔자주름 → 팔자 + 주름 · 사각턱 전문의 용어 교체 · 코조각주사 · 치골궁(왜 부위가 아닌가))
3. 정한 규칙 — 부위 = 「어디에 맞냐」 = 몸 겉 · 원천은 이름 칸만 · 해부학 용어 행선지 · 이름 2벌(일반인 · 전문의 = 겉자리 이름) · 쪼개는 규칙 D-05 · 부위+다른 축 분리 D-07 · ‹부위›라인/살 · 근거 약은 값 + 질문
4. 과정 — 조사 → 결정 → 반영 → 검수 고리 · 검수 6판(v1 ~ v5 + 마지막 한 줄)
5. **틀린 것 · 배운 것 — 정직하게**: 코디가 조사 범위를 설명 문장 22,749칸으로 넓혀 해부 낱말이 부위 후보로 들어옴 · 검수 브리프에 「미래 원천 · 가상 문장 시험」을 넣어 v2~v4 FAIL 루프(사용자 지적 「원천에 없는 가상 문장을 왜 테스트」 · 「치골궁에 필러 맞으러 왔어요?」) · 해부학 표준 목록 확장을 했다가 되돌림 · 조사의 「잔여 0」이 사실이 아니었던 것(v1) · 지방흡입술 → 입술 오매칭
6. 남은 것 — 의료진 질문 35 · 원천 수정 후보 · 4 · 5 · 7 · 8단계로 넘긴 것 · 알려진 한계
- 실명(개인) · 키 금지. 수치는 파일에서 다시 세어 쓴다. 추정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_a9dffe97-d50e-4f9c-ab79-2974a582e945 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: 3단계 부위 기록" \
  --body "파일 경로 / 섹션 / 전후 수치 요약"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] writer 완료 — 3단계 부위 기록. 상세는 인박스." --enter
```
