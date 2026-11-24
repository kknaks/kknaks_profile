# [app] SPEC-010 WP-5 — 장바구니 옵션 줄 · 최저가 (11-20)

너는 WP-0 ~ WP-4 를 한 앱 워커다. `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · 정본 `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `$W/SPEC-010-consult-myeongdong.md` 0.2.7(§4-6 장바구니 · OP1 ~ OP8 · §6 최저가 RC1 ~ RC10 · CO 조건부 옵션 · D-15 ~ D-17 · §13 WP-5 행) · 결정 표 `$W/_RESUME.md` §2(이벤트가 기준 · 0 원 · 회원권 후보 제외 · **첫방문은 후보** · 남성/여성 낱말 같을 때만 · group 은 모든 구성이 장바구니 옵션 줄에 있을 때만 · 장바구니 밖 구성 group 제외 · 드롭다운 = single 만 · group = 패키지 · 카드 2). 데이터 `$A/data/kos/myeongdong-mapping-20261120-v3.json`(1af2216c).

커밋 0 · push 0 · 서브에이전트 0 · 18222 손대지 마라 · 시험은 `test_v05_price.py` · `test_v05_cart.py` + 관련 0.4 만 · ruff 손댄 파일.

## 할 일
§13 WP-5 행 그대로. 완료: 시험 통과 · 실물 v3 로 표본 장바구니 셋(single 만 · group 이 덮는 쌍 · 「[11월 이벤트] 온다50kj+티타늄30kj」 구성 둘) 카드 2 값을 원본과 대조 · CO 에 걸린 옵션 수 · 장부 가격 숫자 0(grep) · 장바구니 드로어 스크린숏 `$W/wp5-shots/`(옵션 줄 추가 · 최저가 카드 2 · 옵션 안 고른 진료항목).
리포트 `$W/wp5-report.md`.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: WP-5" --body "파일 / 시험 / 대조 / 스크린숏"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app WP-5 완료 — <한 줄>. 상세는 인박스." --enter
```
