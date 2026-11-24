# [app] 테스트 고침 D — 넓히기 · 되돌리기 다음에 이어서 (사용자 11-23 「다른 거는 안 고칠 거야?」)

너는 앱 워커다. **지금 하는 `topic-widen-task.md` 를 끝내고 보고한 뒤** 이어서 한다. `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo`. 커밋 0 · 서브에이전트 0 · **18222 · 18105 손대지 마라** · 빈 포트 · **새 브라우저 프로필(캐시 없이)로 스크린숏** · 시험은 관련만.

1. **얼굴 점은 항상 다 떠 있다(사용자 여러 번 지시).** 점 = 대화 전체(모든 주제)의 부위 · 지금 주제 점만 강조 · 점 클릭 · 주제 바뀜에도 사라지지 않음. **점 = 필터:** 점을 누르면 그 부위 진료항목만 목록에(앞 주제 점이면 그 주제 조건으로) · 누른 점 웨이브 · 다른 점 그대로 · 같은 점 다시 누르면 전체. (`items_view.py` 「점 · 몸 목록은 지금 주제의 대화 부위」 를 고침.) 실물: 「팔자주름 고민이야」 → 「미간 주름도 고민이야」 → 점 둘 다 · 팔자주름 점 클릭 → 팔자주름 목록.
2. **모달 효과 · 부작용 = LLM 최종 문장 하나만**(`$W/e2e-fixC-task.md` 내용 그대로 — 원문 칩 · 값 줄 없앰 · 한 줄, 길어도 짧은 두 문장 · 위급은 「바로 병원」 뜻 · 137 케이스 다시 만듦 · 길이 셈 · 표본 15 대조).
3. **CSS · JS 캐시:** 정적 파일 주소에 판 표지(예 `?v=<파일 해시>`)를 붙여 브라우저가 새 파일을 받게. (사용자 화면에서 스피너가 두 줄 · 위급 빨간 상자가 안 보였던 원인 후보.)
4. 리포트 `$W/e2e-fixD-report.md` · 스크린숏 `$W/e2e-shots/fixD-*.png`(점 둘 · 앞 주제 점 클릭 · 모달 효과 · 부작용 · 스피너 한 줄).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: 테스트 고침 D" --body "점 / 모달 문장 / 캐시"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app 테스트 고침 D 완료 — <한 줄>. 상세는 인박스." --enter
```
