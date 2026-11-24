# [reviewer · 읽기만] SPEC-010 WP-1 코드 검수 (11-20)

너는 SPEC-010 을 검수한 워커다. `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 앱 워크트리 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`(미커밋 변경 — `git -C $A status` · `git -C $A diff`). 정본 `$W/SPEC-010-consult-myeongdong.md` 0.2.3 §3 · §2-3 · §13 WP-1 행 · 리포트 `$W/wp1-report.md`. 데이터 `$A/data/kos/myeongdong-mapping-20261120-v3.json`(sha 1af2216c).

볼 것: 스펙 계약(JS1 ~ · 설정 칸 · 장부 `kos_map` 칸)과 코드가 같은가 · 시험이 계약을 실제로 막는가(깨기 시험이 맞는 이유로 실패하는가) · 0.4 회귀 · 장부 · 오류 글에 가격 숫자 0 · 코드 규약(0.4 꼴). 시험은 `tests/test_v05_kos_map.py` + 리포트의 0.4 관련 파일만 다시 돌려 확인(전체 pytest 금지). **수정 0 · 리포트 1 개만** · 사용자 포트 18222 손대지 마라.

산출 `$W/review-wp1.md`: 판정(PASS / FAIL) · 지적(P0 / P1 / P2 · 파일:줄 · 고칠 방향).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_e9e9922f-2211-43e5-bd97-3403b59f0b99 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: WP-1" --body "판정 / 지적"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review WP-1 완료 — <한 줄>. 상세는 인박스." --enter
```
