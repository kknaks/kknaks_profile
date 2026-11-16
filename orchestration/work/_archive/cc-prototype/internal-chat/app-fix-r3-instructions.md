# [mobile] 시뮬레이터 2차 피드백 — 입력줄 알약 · 키보드 (F5 · F6)

역할 · allowed_paths(`procedure/app/`) · 하지 말 것 · 완료 보고는 앞 브리프 그대로. subject 「mobile 수정 r3 완료: …」. 작업 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` — 2판이 커밋 `edabe00` 로 있다(커밋 금지).

근거: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/sim-feedback.md` 2차 F5 · F6 · DEC-009 **D-60 · D-61**(`/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md`)

## 고칠 것
1. **F5 · D-60 입력줄 = 카톡 모바일 꼴 한 줄 알약** — 지금의 「큰 네모 입력칸 + 아래 줄 [+] … 회색 [전송]」을 바꾼다:
   - 둥근(알약) 바 하나: 왼쪽 **둥근 [+]**(지금 [+] 시트 그대로 엶) · 가운데 입력칸(테두리 없음 · placeholder 「메시지 입력」 · 처음 한 줄 → 쓰면 최대 5줄까지 늘고 그 뒤 스크롤) · 오른쪽 **둥근 [↑] 보내기**(테마 primary 바탕 · 흰 화살표 · 글자 없으면 흐림 · 누르면 지금 [전송] 과 같은 동작)
   - 이모지 버튼 없음 · 색 · 모양은 기존 테마 토큰(`Ms` 등)으로 · 새 색 금지
   - 수정 모드(5메뉴 [수정])도 같은 알약 안에서 — 지금 수정 UI 가 입력줄을 쓰면 그 꼴에 맞춘다
   - 비활성 1:1(입력 막음 · D-42) 안내 줄은 그대로
   - 폰 · 아이패드 같게
2. **F6 · D-61 키보드**
   - 화면 키보드가 열리면 **탭바를 숨기고**, 입력줄이 키보드 바로 위에 붙는다. 닫히면 탭바가 돌아온다(D-36 은 키보드가 닫혀 있을 때만)
   - 키보드가 열릴 때 대화 맨 아래(마지막 메시지)가 가려지지 않게 — 맨 아래를 보고 있었으면 따라 올라간다
   - 대화 목록을 끌거나 바깥을 누르면 키보드가 닫힌다(onDrag dismiss)
   - 아이패드(레일 · 두 칸)에서도 입력줄이 키보드 위로
3. 1판 · 2판 시험의 입력줄 키를 바꾸면 같이 고친다 · 새 시험: 키보드 열림(viewInsets) = 탭바 없음 · 입력줄 보임 / 닫힘 = 탭바 있음 · 여러 줄 늘어남 상한

## 검증
`/Users/kknaks/fvm/versions/3.44.8/bin/flutter analyze` · `flutter test` 1회 · `flutter build ios --simulator --debug` 1회. 시뮬레이터 · 기기는 건드리지 않는다(코디가 올린다).
