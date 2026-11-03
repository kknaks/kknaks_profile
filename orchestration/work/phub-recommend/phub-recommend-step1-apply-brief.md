# [researcher] 1단계 원장 반영 — 사용자 결정 전부를 step1-products 에

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 이 원장(`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` · `.md`)을 만든 사람이 너다.

## 입력 (전부 읽어라)
- **최종 결정 요약** `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/gate-answers/step1-decisions-db-2026-10-28.md` — 묶음별 최종
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 결정표 10-27 · 10-28 행 전부 — 규칙 · 결정의 정본(요약과 다르면 이쪽)
- 조사 결과: `step1-d09-web` · `step1-d12-web` · `step1-d15-web` · `step1-d16-web` · `step1-d17` · `step1-d17-2` · `step1-d18` · `step1-d19` · `step1-d20-31` · `step1-cancel-recheck` (.json)
- KPIC MCP `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-28-kpic-mcp/`(NOTES.md 등록 · 실행법) — 의약품 행 보강용

## 규칙 (원장 전체 390행 + 새 행에 적용)
1. **허가**: 정상 허가만 연결 · 취소/취하 → `history[]` · 수출용(「수출용에 한함」) → 연결 안 함 · 참고 · 재제조 → 정품 아님 · 이력
2. **상태**: 정상 / 허가 취소(이력) / 미허가 / 확인 불가 / 허가 대상 아님(출처 있을 때만 — **비침습 ≠ 허가 대상 아님**) / **허가번호 미확인**(실제 제품 · 국내 유통 출처 있음 · 허가번호 특정 못 함) — `recommendable`: 정상 · 허가 대상 아님 · 허가번호 미확인 = true, 나머지 false
3. **이름**: 대표 이름 = 국내에서 부르는 한글 1개 · 허가 이름 = 허가 쪽에만 · 검색 이름[] = 한/영 표시만. 음역 · 오기 · 약칭 등 **이유는 근거 칸에만**
4. **라인 · 품목**: 라인으로 정한 것(온다 · 더채움 · 더블로 · 밸피엔 · 오메가브이 · 브이빔 · 바이리즌 · 라라 · DB FNS · 엘라비에 프리미어 · BBL 등) — 품목 미정은 「미정」
5. **업체**: 제조 · 수입 · 판매 각각 여러 개 · 역할 표현 · 출처. 국내 제조(「제」)는 수입사 「해당 없음」. 충돌은 덮지 않고 기록
6. **합치기 · 빼기**: D16 14쌍 · 에이비오톡신→디스포트 · 리프세라→리프테라 · 레티보→보툴렉스 = 대표 행 하나 + 검색 이름 · 합쳐진 행은 `merged_into` 로 남김(지우지 않음). 시술 이름으로 빠지는 행(PHA필 · 물톡스 · 해피리프트 · 크라이오셀 · 메소건 · D21 · D24 등) = `moved_to: "5단계 시술 이름"` 로 남김(지우지 않음)
7. **의약품 행**: KPIC 로 성분 · 업체 · ATC/분류 · 보험 코드 보강(출처 = KPIC drugcode)
8. **원천 수정 목록**: 이번에 생긴 원천 수정(원텍 · 프리미어 · 리즈톡신 등 · 리프세라 중복 · 리젠바이오텍 · 라엔넥 · 컨트라투벡스 · 헤어셀 LED 설명 · 바넥스 계열 등)을 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-source-fix.json` · `.md` 로 따로 (기존 source-fix-list 는 건드리지 않음)
9. **원천 질문 목록**: 확인 불가 중 원천(병원)에 물을 것 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-origin-questions.md`(질문 한 줄씩 · 쉬운 말)
- 추정 금지 · 결정에 없는 변경 금지 — 애매하면 바꾸지 말고 `open[]` 에 기록

## 산출
- `step1-products.json` · `.md` 갱신(summary: 상태별 · recommendable · 라인 수 · 합침 · 시술 이름으로 빠짐 · 판매사 채움 수)
- `step1-source-fix.json/.md` · `step1-origin-questions.md`
- 반영 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-apply-log.md` — 결정마다 「어느 행에 무엇을 바꿨나」 한 줄
- 결정 파일(step1-decisions)은 건드리지 않음

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 1단계 원장 반영" \
  --body "상태별 수 / recommendable 수 / 합침 · 시술로 빠짐 / 원천 수정 · 질문 수 / open 수"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 1단계 원장 반영. 상세는 인박스." --enter
```
