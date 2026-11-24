# [app] SPEC-010 WP-4 — 모달 값 · 그림 라우트 (11-20)

너는 WP-0 ~ WP-3b 를 한 앱 워커다. `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · 정본 `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `$W/SPEC-010-consult-myeongdong.md` 0.2.7(§4-5 모달 · §8 그림 · §13 WP-4 행 · MD · IM · 결정 D-11 · D-12 · D-19) · WP-H 끝(허브 18105 gold caa03560 — 케이스 profile `method_codes` · `method_texts` · 제품 `country` · `$W/wph-report.md`). 그림 시드 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/reference/2026-11-17-procedure-images/images/`(원리 55 · 방법 66 · 명동점 빠짐 0).

커밋 0 · push 0 · 서브에이전트 0 · 18222 손대지 마라 · 시험은 `test_v05_modal.py` · `test_v05_images.py` + 관련 0.4 만 · ruff 손댄 파일.

## 할 일
§13 WP-4 행 그대로: 모달 값(시술 개요 · 원리 글 · **원리 그림 + 방법 그림**(케이스 method_codes 순서) · 방법 글 · 효과(자기 + 물려받음 · 경과 줄 뺌) · 부작용 · 제품) · 케이스 0 진료항목(MD2) · 케이스 여럿(MD1) · 그림 라우트(앱이 `CHAT_IMAGE_DIR` 시드에서 서빙 · 경로 · 캐시 · 없을 때 처리).
완료: 시험 통과 · 실물 허브로 진료항목 3 개(케이스 1 · 여럿 · 0) 모달 값 대조 · 방법 그림 순서 · 명동점 그림 빠짐 0 · **모달 스크린숏** `$W/wp4-shots/`(입꼬리보톡스 제오민 · BBL HERO 1가지 모드(케이스 둘) · 셀코어(케이스 0)).

리포트 `$W/wp4-report.md`.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: WP-4" --body "파일 / 시험 / 대조 / 스크린숏"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app WP-4 완료 — <한 줄>. 상세는 인박스." --enter
```
