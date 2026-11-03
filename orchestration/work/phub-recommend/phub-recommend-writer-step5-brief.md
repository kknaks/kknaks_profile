# [writer] 실버 5단계(단위 시술) 과정 기록

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 1~4단계 기록(`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-28-silver-step1-product-normalization.md` · `-step2-family.md` · `-step3-site.md` · `-step4-technique.md`)과 같은 형식 · 같은 자리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-29-silver-step5-unit.md` · README 지도 한 줄.

## 원천
- 결정 `orchestration/work/phub-recommend/_RESUME.md` §2 2026-10-29 행 전부(5단계 시작 · 원칙 「클리닉에서 하는 시술은 전부 단위 시술」 · 재추천 · 웹 조사 · 추가 조사 U1~U9 · 반영 확인 3 · 검수 처리 · 데이터 끝)
- 조사 `step5-research.*` · `step5-research2.*` · 결정 `step5-decisions.json` · `step5-apply.py` · 정본 `step5-units.*` · `step5-origin-questions.md` · 검수 `review-step5-report.md` · `-v2` · `-v3` · 브리프 `phub-recommend-step5-*-brief.md` · 앞 단계 보강(step1 · step2 · step4 의 10-29 변경)

## 담을 것
1. 왜 — 원장 521 에 시술 · 제품 · 패키지 · 성분이 섞임 · 초안 236 · 계열 없는 시술
2. 전후 — 수치(원장 521 행선지 · 키 143 · 계열 18 → 24 · 기법 24 → 25 · 상속 쌍 1934 → 1227 · 제모 장비 1 → 11) + 같은 것 전/후 6~8개(카복시 · 반영구 화장 · 성분 미상 수액 · 파셀라 · 브이빔 · 젠틀맥스 제모 · 하이드로퀴논(버림 → 성분) · 줄기세포 관절치료)
3. 정한 규칙 — 단위 시술 = 계열 × [안 C 하위] × 부위 × 기법 · 원천에 있는 조합만 · **클리닉에서 하는 시술은 전부 단위 시술(계열이 없으면 계열을 늘림)** · 얼굴 전체 기본값 · 병변 단위 · 성분 미상은 「미상」 · 제품 상속 = 기법 근거(장비 속성 · 1단계 출처) · 계열 기법 하나면 계열 기본 · 출처가 목적을 채우면 잇기
4. 과정 — 조사 2판 · 사용자 판단 표 하나로 · 검수 3판
5. **틀린 것 — 정직하게**: 「계열 없으면 시술 0」 추천(사용자 「카복시 · 반영구는 시술 아니야?」 「클리닉 모든 시술 포함해야」) · 「버림 17」 · 지도 5단계 칸 45 로 잘못 셈(실물 63) · F1 기법 조건 누락 → 계열 일부에만 적용 → 하위 키 → 반대 방향(제모 장비 미연결) 순으로 한 번에 안 닫힌 것 · 코디가 같은 성격 전수를 매번 늦게 찾음
6. 남은 것 — 원천 질문(병원 · 의료진) · 6단계로 넘긴 것 · 6단계 경계 질문(패키지 ↔ 추천 조합)
- 실명 · 키 금지 · 수치는 파일에서 다시 셈 · 추정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_ba4223c5-bb9d-4ea6-bf7a-392bd71b4d32 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: 5단계 단위 시술 기록" \
  --body "경로 / 섹션 / 전후 수치"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] writer 완료 — 5단계 단위 시술 기록. 상세는 인박스." --enter
```
