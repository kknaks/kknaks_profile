# [app] 속도 탭 화면 수정 (좁게)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-app-brief.md`(같은 폴더)의 역할 · allowed_paths · 공개 레포 제약 · §9 완료 보고 그대로. 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(미커밋 위에 이어서). 계획 = `WORK-004-speed-tab.md`.

사용자 화면(라이트 모드)에서 속도 탭이 꾸밈 없이 보인다. 원인: `style.css` 가 정확도 탭을 id(`#ask` · `#q` · `#set-id`)로만 꾸미고, 속도 탭 요소(`#s-ask` · `#s-q` · `#s-set-id` · 세트 여러 문항 고르기 · 그 보내기)는 스타일이 없다.

할 것:
- 입력 줄 · 고르기 · 버튼 스타일을 **공통 클래스**로 옮겨 두 탭이 같은 꼴(질문칸 넓게 · 세트 고르기 · 보내기 한 줄)이 되게. 「세트 몇 문항 한꺼번에」 고르기 · 버튼도 같은 꼴로 정돈.
- 속도 탭 체크박스 「B」 → **「B 전체」**(WORK-004 의 말) · B 선별 · C 는 늘 돈다는 것은 카드 머리 이름(「B 선별」 · 「C gold MCP」)으로 이미 보이니 새 문장은 넣지 마라.
- **라이트 · 다크 둘 다** 확인(prefers-color-scheme). 18221 에서 띄워 headless 로 두 탭 스크린샷 · 라이트 · 다크 4 장을 scratchpad 에 남기고 경로를 보고(18220 · 18105 는 코디 것).
- 실물 LLM 호출 없음. ruff · pytest · 커밋 후보 grep.
