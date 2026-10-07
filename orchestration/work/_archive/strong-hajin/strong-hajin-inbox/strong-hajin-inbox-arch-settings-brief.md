# [architect] 설정 시안 고치기 — Claude Design `Settings.html` 메일·슬랙 연동 (쓰기 작업)

너는 strong-hajin `architect` 워커다. 맥락이 없으면 먼저 읽어라:
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/roles/strong-hajin/planner/role.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/design-survey.md` §2(설정 화면) · `design-change-1.md`(앞 판 — 같은 방식으로)
- 결정 원장 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/_RESUME.md` §2 (2026-10-05~06 행 전부)

## 1. 무엇을
Claude Design `7e839512-977c-4142-b4b5-d992df566ffc` 의 설정 시안에서 **메일 연동 · 슬랙 연동 두 메뉴만** 고친다. DesignSync 쓰기(사용자 승인 받음).
대상: `Settings.html` · `handoff/settings/js/settings.v1.jsx` · `handoff/settings/js/data.js` · `handoff/settings/css/settings.css`. DS 부품·다른 화면 건드리지 마라. 새 부품은 settings.css 안에서.
**손대지 않는 것**: 카카오톡 연동 메뉴 · 계정 설정 · 알림 설정 — 지금 모양 그대로 둔다.

## 2. 메일 연동 (Gmail API · 1회 연결)
- IMAP 폼(서버 이름 · IMAP 서버 · 계정 · 비밀번호 · 「연결 확인」 · 「추가하고 받아오기」)을 **걷고**, 「Google로 연결」 단추 하나(설명 한 줄: 한 번 연결하면 받은편지함이 실시간으로 쌓인다 · 연결 때 받은편지함 전체를 가져온다)
- **계정 여러 개 가능** — 연결된 계정 목록에 한 줄씩(주소 · 「Gmail」 · 적재 N건 · 상태), 아래에 「다른 계정 연결」
- 「가져올 범위」 Select **없앰**(최초 연동 = 받은편지함 전체)
- 적재 상태 3셀: `마지막 수집` · `DB 적재 건수` · 셋째 칸 = 수집 주기 Select 대신 **「실시간」** 표시
- 계정 줄 상태: `실시간` / `과거 메일 채우는 중 · N건` / `연결 끊김 — 다시 연결`(토큰 만료·권한 취소)
- 휴지통 → **「연결 해제」**(확인 문구: 더 받지 않는다 · 쌓인 메일은 메시지함에서 사라진다)

## 3. 슬랙 연동 (사용자 토큰 · 1회 연결 · 방 고르기)
- 워크스페이스 카드: 연결 전 = 설명 + 「슬랙 연결」 / 연결 후 = 「MediSolve AI 같은 가상 이름 · workspace.slack.com · 연결됨」 + 「연결 해제」. 봇 권한 문구(channels:history…) 빼라
- 「채널 이름」 입력 + 「봇이 초대된 채널만」 힌트 **걷고**, 「방 추가」 단추 → **방 고르기 창(모달)**:
  - 검색 · 묶음 탭/구획 `채널` · `비공개` · `DM` · `그룹 DM` · 각 줄 체크박스 · 이미 추가된 방은 「추가됨」
  - 그룹 DM 은 **참여자 실명을 「, 」로**(내부 이름 mpdm-… 안 보임) · DM 은 상대 이름 · 봇 DM 도 그대로 섞여 나온다(따로 묶지 않음, 이름 옆 `앱` 표시 정도)
  - 하단 「선택한 N개 추가」
- 수집 방 목록 한 줄: 방 이름 · 메타 `채널 · 공개` / `채널 · 비공개` / `DM` / `그룹 DM · N명` · 적재 N건 · 상태(`실시간` / `과거 메시지 채우는 중`) · 「빼기」
- 적재 상태 3칸의 셋째 = **「실시간」**
- 처음 추가하면 「과거 메시지 채우는 중」 — 슬랙이 허락하는 끝까지 가져온다는 설명 한 줄

## 4. 네 상태 · 목데이터
- 두 메뉴에 연결 전 / 연결됨 / 과거 채우는 중 / 연결 끊김 을 시안에서 볼 수 있게(앞 판 StateSwitch 방식 참고)
- 방 고르기 창: 로딩 · 검색 결과 없음 · 불러오기 오류
- 가상 인물·가상 워크스페이스만

## 5. 끝나면
1. 고친 파일을 로컬 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/reference/2026-09-10-sc-meeting/package 2/` 같은 경로로(원격과 같은 바이트)
2. `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/design-change-2.md` — 바꾼 것 · 파일별 바이트 · 일부러 안 그린 것 · 미결
3. 다른 파일·레포 금지 · 커밋 금지

## 9. 완료 보고 — 문구 변경 금지
> 핸들은 dispatch preamble 의 값을 믿어라.
```bash
orca orchestration send --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_208c9243-9983-47ba-9983-e3aa67ecf049 --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: 설정 시안" --body "바꾼 파일 / 요약 / 로컬 사본 / 미결"
orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[worker_done] architect 완료 — 설정 시안. 상세는 design-change-2.md" --enter
```
- 막히면: `orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[질문] architect: <질문>" --enter`
