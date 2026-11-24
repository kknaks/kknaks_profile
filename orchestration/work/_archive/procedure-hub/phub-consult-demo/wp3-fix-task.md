# [app] WP-3 검수 FAIL 고침 (11-20 · WP-4 다음에)

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 검수 `$W/review-wp3.md`(P1 1 · P2 5) · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo`. 커밋 0 · 서브에이전트 0 · 18222 손대지 마라 · 시험은 관련만.

## 코디 판단
- **P1-1:** 허브 오류(호출 실패 · 시간 넘김)는 「0 결과」 가 아니다 — 그 턴은 목록 · 조건 칸을 **바꾸지 않고**(D1 거름 · 새 주제 판단 안 함) 장부 `items.hub_error` 표지 · 봇은 0.4 오류 처리 그대로. 시험 한 줄(허브 오류 → 조건 · 목록 · 주제 그대로).
- **P2-1:** 주제 수 한도는 **화면 · LLM 블록 · 되돌림 대상 모두** 한도 안 주제만(장부에만 전부 남음).
- P2-2 ~ P2-5: 검수 「고칠 방향」 대로. `test_consult_page::test_t17` 실패도 원인 찾아 고침(0.4 회귀).

리포트 `$W/wp3-fix-report.md`.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: WP-3 고침" --body "P1 · P2 · 시험"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app WP-3 고침 완료 — <한 줄>. 상세는 인박스." --enter
```

## 덧붙임 — WP-4 G1(그림 시드 경로) 코디 판단
그림 자리 = **허브 레포 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/assets/procedure-images/images/`**(원리 55 · 방법 66 · 새 18 포함 · 허브와 함께 배포됨). `CHAT_IMAGE_DIR` 기본 · 시험 · README · 리포트를 이 자리로. 옛 시드 경로(`프로시저허브-데이터-메달리온/...`)는 쓰지 않는다.
