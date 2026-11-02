# WORK-011 FE-a(메시지함) + FE-b(설정·프로필) 결과 보고

## 상태: done (커밋 안 함 · frontend/src 만)

## 수행 내용
신규: features/inbox/{InboxPage,MessageRail,MailView,MailFrame,RoomView,RoomComposer,InboxAttachments}.tsx · inboxModel.ts · inboxStream.ts
      features/settings/{SettingsPage,IntegrationSections,KakaoSection,ProfileSection,RoomPicker,settingsParts}.tsx · consent.ts
      styles/inbox.css · styles/settings.css (시안 CSS 이식)
      테스트: inbox/inboxModel.test.ts(14) · inbox/InboxPage.test.tsx(11) · settings/SettingsPage.test.tsx(12) · lib/shellKakao.test.ts(4) · SettingsLanding.test.tsx(1)
수정: App.tsx(내비 「메시지함」·surface inbox/settings·콜백 쿼리 landing·머리 제목 seam·아바타·캐릭터 진입점 둘 제거) · lib/api.ts · lib/shell.ts(카톡 커맨드 3 자리) · lib/viewModels.ts · lib/labels.ts · styles/index.css · styles/ax.css(고아 picker 규칙 정리)
      shell/AppShell.test.tsx · AssistantPreferenceApp.test.tsx (진입점 이동 반영)
삭제: features/assistant/AssistantCharacterPicker.tsx(+test) — 프로필 설정 CharacterCard 로 이동(W-14)

## 테스트
- tsc --noEmit 0 에러
- vitest --no-file-parallelism 전체 1회: 1352 passed / 5 failed — 실패 5건은 무관(CreateWork·CreateWorkLayout: 2026-09-20 등 고정 날짜를 오늘(10월) 달력에서 찾음 — 날짜 의존 기존 부채, work 파일 미변경)
- 새/고친 테스트 41 + 기존 3 통과. InboxPage 5회 반복 안정
- 미실행(pending): make frontend-build / make verify(코디 몫), 실서버 연동(코디가 BE-3 뒤)

## 계약 준수
- BE-3 리포트(be3-report.md) 모양 그대로: 카드 `sender`, multipart 답장 필드, Idempotency-Key, `inbox.reply_result`, `data-ax-remote-src`, profile_image_url
- HTML 메일 = sandbox iframe(allow-same-origin allow-popups allow-popups-to-escape-sandbox, allow-scripts 없음) · 부모가 높이 측정 · 링크 가로채 open_external/새 탭 · 원격 이미지 차단+「이미지 보기」=remote-image 프록시 · 인용은 서버 <details>(답장 칸 인용도 iframe)
- 연결 시작 = 서버 authorize_url → 브라우저 location / 데스크톱 open_external · focus/visibilitychange 재조회
- 기기 토큰: 발급 즉시 kakao_store_device_token 으로만, 화면·저장소 미보관(시험으로 확인)
- api.ts 밖 fetch 없음 · 셸 invoke 는 shell.ts 만

## 다른 팀 영향 / BE 요청(gap)
1. 방 메시지 응답에 사용자 이름표(`users: {id:{name,is_bot}}`) 없음 → 지금은 raw.user_profile/bot_profile 로 풀고 없으면 id 표시. 멘션 이름도 같은 이유로 id 가 보일 수 있음. 목록 preview.author 도 슬랙은 user id
2. 「슬랙에서 열기」 퍼머링크(room.permalink) 미제공 → 서버가 주면 표시, 없으면 단추 숨김
3. /api/organization/me 에 직책·직무(position/job) 없음 → 「—」 표시
4. 슬랙 워크스페이스 domain 미제공 → 워크스페이스 줄에 이름만
5. GET /api/integrations/slack/available-rooms 는 SPEC 모양으로 호출(BE 구현 여부 확인 필요 — BE-1/3 리포트에 없음)
6. 첨부 크기 외 카톡 동영상 길이·앨범 묶음 정보 없음 → 칩에 길이 없음, album 첨부 여러 개를 격자로

## SPEC·시안 어긋남 / DS-gaps
- 앱 이름: 시안 「Strong Hajin 앱」 → SPEC N-12 대로 중립 「데스크톱 앱」
- 시안에 없음(최소 추가): 원격 이미지 차단 안내줄, 수집 실패 배너(D-50), 「이 Mac 연결」 기기 토큰 카드, 카톡 계정 바뀜 줄, 위로 더 읽기/더 보기 단추, 실제 이미지 썸네일, iframe 틀 → inbox.css 「앱이 더한 자리」 블록
- PDF 첫 페이지 미리보기: 서버 미리보기 이미지 없어 머리 카드만
- 알림 설정 메뉴: 범위 밖(D-37) → 비활성 자리만
- 슬랙 서식 막대: 선택 글을 mrkdwn 기호로 감싸는 정도
- CSS: 인박스 `.scax-msg*` 가 AX 대화 ax.css 와 충돌해 `.scax-imsg*` 로 이름만 바꿔 실음

## 주의
- 슬랙 보낸 줄은 결과 사건 뒤 다음 재조회 때 서버 사본으로 교체(BE: Socket Mode 가 같은 ts 로 수집)
- 메일 답장 결과는 WS 사건 + 3초 간격 10회 sent_replies 재조회(폴백)
- WS 첫 프레임 {"type":"ready"} 무시됨(무해)
- 작업 중 frontend/node_modules 를 npm ci 로 설치함(gitignore)
