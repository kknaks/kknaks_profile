# [researcher] 실버 2단계 최종 검수 v4 지적 수정

`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-step2-v4-report.md` F1 · F2 · W1~W3 를 고친다. 고칠 곳은 `step2-open-resolve.json`(해결안) → `step2-apply.py` 재실행(결정론). step1-products.json 수정 금지 · 결정에 없는 변경 · 추정 금지.

1. **F1 소프라노 티타늄**(`M9-2-4`): `also_sub_families: []` — 주 반도체 레이저 단독. conflict = 「원천 설명이 파장(755 · 1064)을 매질 이름처럼 씀 — FDA 510k K222064 는 세 파장 모두 diode 모듈」
2. **F2 울트라V**(`auto-M7-1775364775158`): `also_sub_families: []` — 주 PDO 단독(1단계 「연결 안 함」 수출 허가 20-682 를 재질 근거로 쓰지 않는다)
3. **같은 성격 전수**: 해결안 강 28 · 약 9 중 보조 값의 근거가 (a) 파장 숫자만 (b) 이 제품에 연결 안 된 허가(수출용 · 다른 품목) 인 행이 더 있는지 다시 보고 같은 기준으로 처리 — 처리한 행 목록을 md 에
4. **W1 브이빔 퍼펙타**: 인용문을 실제 페이지 문구로 바꾸거나 Perfecta 제품 문서(IFU · 허가 상세)로 출처 교체
5. **W2**: also_sub_families 를 `{family, sub_family}` 객체 배열로 통일(같은 계열 보조도 family 적기)
6. **W3**: 아이콘 · 디스커버리 피코 해결안 `ask` 채우기(지금 질문 문장 그대로) · W4 소프웨이브 근거 문구를 taxonomy 실제 위치(M9-4 복합 에너지 아래)로
7. open 0 유지 · md 셈 갱신

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_99ecdef9-59f9-4620-8a6b-cfdd39f0bc09 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 2단계 v4 지적 수정" \
  --body "F1 · F2 처리 / 같은 성격 추가 N행 / open N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 2단계 v4 지적 수정. 상세는 인박스." --enter
```
