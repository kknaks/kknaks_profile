# [researcher] 1단계 마지막 반영 — domestic7 + 「허가 대상 아님」 45행

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 원장 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` · `.md`(네가 만든 `step1-apply.py` 로 결정론 유지).

## 결정 (`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 10-28 마지막 행)
1. **domestic7**(`step1-domestic7.json`): 고우리 제허 25-634 · 더블로 골드 제허 11-946 · 잼버실 제허 13-1507 연결(정상) · N코그 = 허가번호 미확인 · 인트라셀 = 허가 취소(이력, 09-682 만료) · 에코2 에볼루션 · 스텔라듀오 = 확인 불가(현장 사진만으로 국내 사용 근거 안 봄)
2. **「허가 대상 아님」 중 출처 없는 45행**(검수 v3 「사용자 판단으로 넘어간 것」 목록): 행마다 **국내 유통 출처**(피부과 홈페이지 · `/Users/kknaks/Downloads/data-anyang` read-only · 제조/판매사 공식 · 보도 · URL 필수)를 찾는다
   - 있으면: 상태 「허가 대상 아님」 유지 + `license_basis: "국내 유통 확인 · 허가 대상 여부 출처 없음"` 표시 · recommendable true · 판매사 채움
   - 없으면: 상태 「확인 불가」 · recommendable false · 원천 질문 목록에 추가
   - 허가 대상 아님을 뒷받침하는 출처(화장품 · 미용기기 명시)가 나오면 그 근거로 확정
3. summary · apply-log · open · origin-questions 갱신
- 결정에 없는 변경 금지 · 추정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 1단계 마지막 반영" \
  --body "domestic7 처리 / 45행: 유통 확인 N · 출처로 확정 N · 확인 불가 N / 갱신 수치"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 1단계 마지막 반영. 상세는 인박스." --enter
```
