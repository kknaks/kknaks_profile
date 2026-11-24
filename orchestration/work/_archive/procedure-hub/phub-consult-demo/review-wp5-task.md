# [reviewer · 읽기만] WP-5 코드 검수 (11-20)

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(미커밋). 정본 `$W/SPEC-010-consult-myeongdong.md` 0.2.7(§4-6 · OP1 ~ OP8 · §6 RC1 ~ RC10 · CO · §13 WP-5 행) · 결정 표 `$W/_RESUME.md` §2 11-20(이벤트가 기준 · 0 원 · 회원권 제외 · 첫방문 둠 · 남성/여성 · group 조건) · `$W/wp5-report.md` · `$W/wp5-shots/`. 데이터 v3 `$A/data/kos/myeongdong-mapping-20261120-v3.json`.
볼 것: 최저가 집합 덮기가 결정과 같은가 · 실물 v3 로 표본 장바구니 몇 개를 **직접 다시 계산**해 카드 값 대조(손으로 · 스크립트로) · 옵션 줄 계약 · 시험이 결정을 막는가 · 탐색 한도 · 장부 가격 0 · 0.4 회귀. 시험은 WP-5 관련만. **수정 0 · 리포트 1 개** · 18222 손대지 마라.
산출 `$W/review-wp5.md`.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_e9e9922f-2211-43e5-bd97-3403b59f0b99 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: WP-5" --body "판정 / 지적"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review WP-5 완료 — <한 줄>. 상세는 인박스." --enter
```
