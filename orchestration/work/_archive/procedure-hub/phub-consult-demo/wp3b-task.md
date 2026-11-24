# [app] SPEC-010 WP-3 고침(D1) + WP-3b 다음 질문 축 (11-20)

너는 WP-3 을 한 앱 워커다. `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · 정본 `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `$W/SPEC-010-consult-myeongdong.md` 0.2.7 · 네 리포트 `$W/wp3-report.md`.

커밋 0 · push 0 · 서브에이전트 0 · 18222 손대지 마라 · 시험은 관련 파일만(전체 금지) · ruff 손댄 파일.

## 1. WP-3 고침 — D1 코디 판단 **(가)**
LS 로 막은 칸 값은 **주제 조건 칸에서 뺀다**(장부 `blocked` 에만 남김). 그래야 다음 턴 좁히기(「쥬비덤으로」)가 막은 값에 걸려 새 주제로 튀지 않는다. 실물 `wp3real000000001` 꼴(「볼 꺼짐 때문에 필러」 → 「쥬비덤으로」 → 같은 주제 좁히기)로 시험 한 줄 + 실물 한 번 확인. 스펙 LS3 문구와 다른 점은 리포트에 적는다(코디가 스펙에 옮김).

## 2. WP-3b — 다음 질문 축
§5-4 AX1 ~ AX7 · §13 WP-3b 행 그대로(축 = 부위 / 고민 / 효과 / 제품 · 회차 · 대상 — 목록을 가장 잘 가르는 축 · 0.2 `ask` 에 축 · 선택지 연결 · 지금 주제 기준). 완료: `tests/test_v05_ask_axis.py` 통과 · 실물 허브로 표본(팔자주름 → 제품 5 · 보톡스 → 부위 21 · LDM → 축 0) 고른 축 · 점수 리포트.

리포트 `$W/wp3b-report.md`: D1 고침 · WP-3b 파일 · 시험 · 실물 표.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: D1 · WP-3b" --body "파일 / 시험 / 실물"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app D1 · WP-3b 완료 — <한 줄>. 상세는 인박스." --enter
```
