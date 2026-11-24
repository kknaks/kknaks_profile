# [reviewer · 읽기만] SPEC-010 0.2.1 재검수 r4 (11-20)

너는 SPEC-010 을 r1 ~ r3 검수한 워커다. `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo`. 0.1.2(PASS) 뒤 사용자 결정으로 크게 바뀌었다 — 고침 지시 `$W/spec-010-fix3-task.md`(조건 누적 · 질문 고르기 · 장바구니 · 이벤트가 · 최저 조합 · 그림 앱 서빙 · JSON v3) · `$W/spec-010-fix4-task.md`(장바구니에서 [옵션 추가 +] 드롭다운 → [추가] · single 만 고름 · group = 패키지 · 최저가 후보로만 · O-9 country) · 결정 표 `$W/_RESUME.md` §2 11-20 행. 데이터 `myeongdong-mapping-20261120-v3.json`(94b88022 · `/Users/kknaks/git/clinic_chat/data/kos/` · `$W/mapping-json-v3-report.md`).

`$W/SPEC-010-consult-myeongdong.md` 0.2.1 을 **사용자 결정과 같은지 · 데이터(v3 · 허브 18105)로 성립하는지 · WP 가 순서대로 되는지 · 시험 가능한지** 본다(실측 필요하면 JSON 셈 · 허브 GET). 특히: 조건 누적 상태 · 0 일 때 · 다음 질문 고르기 규칙의 시험 꼴 · 최저가 집합 덮기(옵션 줄 · 회차 · 이벤트가 옵션 단위 · group 후보 · 장바구니 밖 구성 제외 · 옵션 없는 진료항목 · 탐색 크기 한도) · 그림 앱 서빙 경로 · WP-H 범위(method_codes · method_texts · country).
리포트 1 개만 · 다른 파일 수정 0.

산출 `$W/review-spec-010-r4.md`: 판정 · 지적(P0 / P1 / P2 · 근거 · 고칠 방향).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_dbc58c9f-06a3-4337-9ad3-b1f7102f121a --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "review 완료: SPEC-010 r4" --body "판정 / 지적 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] review r4 완료 — <한 줄>. 상세는 인박스." --enter
```
