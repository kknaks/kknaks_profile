# [researcher] 1단계 — 허가 규칙 적용(정상 연결 · 취소는 이력) + 결정 목록 정리 + 페이지 재생성

사용자 결정(10-27, `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 「허가 규칙」 행): **정상 허가에 연결 · 취소 허가는 이력으로만 보관(추천에 쓰지 않음).** 정상 없이 취소뿐인 제품 = 「허가 취소(이력)」 상태, 원장에 남기되 추천 제외. 디클래씨 = 제허 11-1324(정상) 연결, 23-60 은 이력.

## 할 일
1. `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` · `.md`: 모든 행의 `4_license` 를 규칙대로 — 연결(linked) = 정상 허가만, 취소 허가는 `history[]` 로 이동. 취소뿐인 22개 상태 = 「허가 취소(이력)」 + `recommendable: false`. 규격(`5_spec`)도 연결 허가 기준으로. summary 갱신
2. `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-decisions.json` · `.md`: 이 규칙으로 답이 정해지는 묶음 · 행(정상이냐 취소냐 · 취소 허가 연결 여부 · 디클래씨 등)을 **목록에서 빼고** 「규칙으로 정리됨」 기록. 남은 묶음 수 갱신
3. 결정 페이지 재생성: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-decisions.html` 의 내장 데이터(`<script id="data" type="application/json">`)만 새 `step1-decisions` · `step1-products` 로 교체(페이지 코드 · 스타일 · db 컬렉션 decisions 그대로). U+FFFD 는 JSON 이스케이프. node 구문 검사 1회. 게시는 코디
- 다른 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 허가 규칙 적용" \
  --body "바뀐 행 수 / 취소(이력) 수 / 빠진 결정 묶음 · 남은 묶음 수"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 허가 규칙 적용. 상세는 인박스." --enter
```
