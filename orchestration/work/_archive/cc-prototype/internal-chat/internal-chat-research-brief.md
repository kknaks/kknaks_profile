
# [researcher] 내부 채팅 — Mattermost 참고 조사 + 지금 procedure 코드에 붙일 자리

너는 **cc-prototype `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 워크트리는 코디네이터 워크트리다. **리포트 파일 1개 말고는 아무것도 만들거나 고치지 마라.**

## 1. SSOT — 먼저 읽을 것

아직 SPEC 이 없다. 이 조사 결과로 BASE-010 · DEC-009 를 닫고 그 뒤에 SPEC 을 쓴다.
사용자 입력과 이미 정한 기본값은 §2 에 있는 것이 전부다.

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md`: 지금 앱 계약. §3 계정 · §5-1 ~ §5-4 푸시 · 알림 · §6.8 공통 틀(탭) · §7.1 SSE · §7.4 표 · §2.3 `PROC_PHOTO_DIR`
- 코드 (read-only · canonical · pull/checkout 금지): `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/` (`back/app/` · `app/lib/`)
- Mattermost: `https://github.com/mattermost/mattermost`. **레포 밖** 임시 폴더에 `git clone --depth 1` 해서 읽어라 (예: `$TMPDIR/mattermost-ref`). 이 워크트리나 코드 레포 안에 받지 마라

**기대는 개념**: 해당 없음

## 2. 배경

사용자 입력 (2026-10-29): 「mattermost 참고하고, cc-prototype 앱에 내부 채팅을 넣을 건데 텔레그램처럼 그냥 메신저, 사진, 이런 것만 보내면 돼」

사용자가 정한 것:
- 방 = **1:1 + 그룹방**(사람을 골라 만든다 · 참여자 추가 · 나가기)
- **새 메시지 푸시(APNs) 넣는다**
- **앱(iOS Flutter)만**. 웹 화면은 없지만 back API 는 웹이 나중에 붙을 수 있는 모양으로

코디 기본값 (확정 전 — 조사 결과에 따라 고칠 수 있음):
- 자리 = `procedure/back` + `procedure/app` · 앱에 「채팅」 탭 하나 더
- 사람 = 기존 ccc `account`(어드민 · 의사 · 간호사 · 코디 · 상담사). 새 계정 체계 없음
- 보내는 것 = 텍스트 + 사진(카메라 · 앨범). 파일 · 음성 · 영상 · 반응 · 스레드 · 수정 없음. 삭제 = 내 메시지만
- 실시간 = 기존 계정 단위 SSE 허브에 이벤트 추가 · 보내기 = REST
- 안 읽음 = 방마다 `last_viewed_at` → 방 목록 배지. 메시지별 「1」 숫자 없음
- 사진 = ccc 볼륨 별도 폴더 · 열람 Bearer
- Mattermost 는 **개념만** 참고한다 (코드 복사 금지 · 라이선스 확인)

## 3. 계약

해당 없음 (조사)

## 4. 먼저 볼 곳

Mattermost (`server/` 아래에서 찾는다. 경로가 다르면 실제 경로를 적어라):
- 모델: `Channel`(타입 D/G/O/P) · `ChannelMember`(`LastViewedAt` · `MsgCount` · `MentionCount` · `NotifyProps`) · `Post`(`RootId` · `FileIds` · `DeleteAt`) · `FileInfo`(썸네일 · 미리보기)
- DM 채널 이름 규칙(두 user id 정렬) · 그룹 DM(G) 이 참여자 변경을 어떻게 다루나
- 안 읽음 계산 · 「읽음 처리」 API(view channel)
- 파일 업로드 → 글 작성 두 단계 흐름 · 썸네일 생성
- WebSocket 이벤트 종류(posted · post_deleted · channel_viewed …) 와 페이로드
- 푸시 알림 내용 · 언제 안 보내나(보고 있는 방 · 음소거)
- 메시지 페이지네이션(before/after · since)

procedure 코드:
- SSE 허브 · 계정/기기 단위 전송 (`back/app/` 에서 grep `sse` · `stream`)
- APNs 발송 · `push_log` · 기기 토큰 (`back/app/push/`)
- 사진 저장 · Bearer 열람 (`PROC_PHOTO_DIR` grep)
- 표 만드는 방식(`CREATE TABLE IF NOT EXISTS` + `MIGRATIONS`)
- 인증 · 역할 검사
- 앱 탭 틀(`app/lib/screens/shell.dart`) · SSE 클라이언트(`app/lib/sse/`) · 푸시 받기(`app/lib/push/`)

## 5. allowed_paths: 이 밖은 건드리지 마라

- 생성 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/research-mattermost-report.md`
- 그 밖은 전부 read-only. Mattermost 클론은 레포 밖 임시 폴더

## 6. 할 일 — 리포트 절

1. **Mattermost 라이선스**: 서버 · 모바일 각각. 개념 참고 · 스키마 모양을 따라 쓰는 것이 문제 되는지 「사실」만 (판단은 「정할 것」으로)
2. **데이터 모델 요약**: 위 4개 모델의 필드 중 **우리 범위(1:1 · 그룹 · 텍스트 · 사진 · 안 읽음 · 삭제)에 필요한 것만** 표로. 뺀 필드는 한 줄로 「뺌 · 이유」
3. **동작 흐름**: DM 만들기(이미 있으면 재사용) · 그룹 만들기 · 참여자 추가/나가기 · 보내기 · 사진 업로드 · 읽음 처리 · 삭제 · 페이지네이션 · 푸시 판단. 각 흐름마다 Mattermost 파일:줄
4. **우리 코드에 붙일 자리**: §4 procedure 항목마다 파일:줄 + 지금 모양 + 채팅이 얹힐 때 바뀔 곳. 특히 SSE 허브가 「특정 계정 여럿에게만」 보낼 수 있는지, APNs 가 계정별 발송을 이미 하는지
5. **매핑 표**: Mattermost 개념 → 우리 표 · API · SSE 이벤트 · 푸시 초안. **초안이라고 표시**하고 결정하지 마라
6. **정할 것**: 조사하다 나온 갈림길 전부 (예: 그룹방 이름 · 방장 있나 · 나간 방 기록 · 사진 원본 크기 제한 · 썸네일을 서버/앱 어디서 · 보존 기간 · 지운 메시지 표시). 항목마다 Mattermost 의 선택 + 코디 기본값 후보 1개

## 7. 하지 말 것

- 코드 · 문서 수정 · 커밋 · 브랜치 · PR 금지
- Mattermost 코드 블록을 리포트에 길게 옮기지 마라 (파일:줄 + 요약)
- 결정하지 마라. 갈림길은 §6-6 「정할 것」으로
- 사용자 포트 · 프로세스 · docker 를 건드리지 마라. procedure 서버 · 앱을 띄우지 마라
- public 레포다. 키 · 토큰 · 실명 · 연락처를 리포트에 쓰지 마라

## 8. 검증

```
질문마다 답 + 공식 문서 URL. 문서에 없는 것은 「문서에 없음」. 결정하지 않고 「정할 것」으로 모은다
```

- 모든 사실 줄에 근거(Mattermost 파일:줄 또는 공식 문서 URL · procedure 파일:줄)를 단다
- 리포트 끝에 `git -C /Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅 status --short` 결과를 붙여 리포트 1개만 생겼음을 보인다

## 9. 완료 보고: **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_cc59b27c-b9ef-412c-b7e7-c37af3bb4424 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_cc59b27c-b9ef-412c-b7e7-c37af3bb4424 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_cc59b27c-b9ef-412c-b7e7-c37af3bb4424 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
