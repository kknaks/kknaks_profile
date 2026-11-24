# [app] SPEC-010 WP-2 추가분 + WP-2 검수 P2 (11-20)

너는 WP-0 ~ WP-2 를 한 앱 워커다. `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · 정본 `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `$W/SPEC-010-consult-myeongdong.md`(0.2.6 · §13 WP-2 행 「추가분」 = IL11 주제 묶음 머리 · `/topic` 라우트 · slot 둘 — 주제 **화면 틀**만, 주제 로직은 WP-3) · WP-2 검수 `$W/review-wp2.md` P2 ① ~ ⑦(⑤ 는 스펙 쪽에서 고침 — 화면은 스펙 문구대로).

커밋 0 · push 0 · 서브에이전트 0 · 18222 손대지 마라 · 시험은 `tests/test_v05_page.py`(+ 주제 틀 시험) + 손댄 파일 관련 0.4 만 · ruff 손댄 파일. 스크린숏 `$W/wp2-shots/07-topics.png`(가짜 턴에 주제 둘 — 지금 펼침 + 앞 접힘).

리포트 `$W/wp2b-report.md`: 바뀐 파일 · 시험 · P2 ① ~ ⑦ 처리 · 스크린숏.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: WP-2 추가분" --body "파일 / 시험 / P2"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app WP-2 추가분 완료 — <한 줄>. 상세는 인박스." --enter
```
