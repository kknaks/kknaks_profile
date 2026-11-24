# [app] SPEC-010 WP-2 — 화면 틀 (사용자 승인 11-20)

너는 WP-0 · WP-1 을 한 clinic_chat 앱 워커다(WP-1 끝 · 매핑 JSON v3 sha 는 이제 1af2216c — WP-H 반영). `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · 정본 `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · **`$W/SPEC-010-consult-myeongdong.md` 0.2.3**(§4 화면 · §12 slot · §13 WP-2 행) · 시안 `$W/design-consult-20261120.html`(정본 · 마크업 · CSS · 클래스 그대로 이식 · 시안에 없는 문구 0 — slot 빈 자리) · 얼굴 그림 `$W/design-face-0.svg` · `$W/gui-feedback.md`.

커밋 0 · push 0 · 서브에이전트 0 · 사용자 포트 18222 손대지 마라(빈 포트로 띄워 확인 · 끝나면 끔) · 시험은 `tests/test_v05_page.py` + 손댄 파일 관련 0.4 시험만 · ruff 손댄 파일.

## 할 일
§13 WP-2 행 그대로: 시안 마크업 · CSS 이식 · 얼굴 점(`$J` sites 좌표 · 얼굴 32 전부 점) · 몸 목록(「• 전신 · • 팔뚝」 꼴) · 진료항목 KOS 시술별 접기 · 장바구니 드로어(진료항목 줄 · [옵션 추가 +] · 드롭다운 · [추가] 자리 — 동작은 WP-5) · 모달 빈 틀(탭 · 칸 · 원리 그림 + 방법 그림 자리) · 가짜 턴(`CHAT_FAKE_TURN`)에 `items` 이벤트 · RT1 코드 전달.
완료 조건: 시험 통과 · **가짜 턴 화면 스크린숏**(`$W/wp2-shots/` — 첫 화면 · 진료항목 펼침 · 장바구니 드로어 · 모달)이 시안과 같은 자리 · 글자 · 클래스(예시 값 차이는 FAIL 아님).

리포트 `$W/wp2-report.md`: 바뀐 파일 · 시험(명령 · 통과 수) · 스크린숏 목록 · 시안과 다른 점(있으면 이유) · slot 목록 대조.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: WP-2" --body "파일 / 시험 / 스크린숏"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] app WP-2 완료 — <한 줄>. 상세는 인박스." --enter
```
