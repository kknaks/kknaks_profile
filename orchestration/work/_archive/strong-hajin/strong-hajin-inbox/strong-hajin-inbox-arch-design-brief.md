# [architect] 메시지함 시안 고치기 — Claude Design `Inbox.html` (쓰기 작업)

너는 strong-hajin `architect` 워커다. 맥락이 없으면 먼저 읽어라:
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 rules·skills·tools·workflow)
- 앞 판 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/design-survey.md` (§3 수신함 화면)
- 결정 원장 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/_RESUME.md` §2 — 특히 2026-10-05~06 행

## 1. 무엇을

Claude Design 프로젝트 `7e839512-977c-4142-b4b5-d992df566ffc` 의 **수신함 시안을 「메시지함」으로 고친다.** DesignSync 로 쓴다(사용자 승인 받음 — 이번 발주는 시안 **쓰기**다).
대상 파일만: `Inbox.html` · `handoff/inbox/js/inbox.v1.jsx` · `handoff/inbox/js/data.js` · `handoff/inbox/css/inbox.css` · `handoff/shell/js/nav.js`(라벨만). 다른 화면·DS 부품(`components/ds/*`, `_ds_bundle.*`)은 건드리지 마라. 새 부품이 필요하면 `inbox.css` 안에서 만든다(settings.css 와 같은 규칙 — 「DS 에 없는 것만 여기서 만든다」).

## 2. 정해진 것 (사용자 결정 — 다시 논의하지 마라)

- 화면 이름 **「메시지함」** — 내비 라벨·`<title>`·레일 제목 전부. 역할 = 수집한 메일·슬랙을 **조회만**, 읽음 표시만
- **1단계 범위는 메일·슬랙** — 카톡 카드·탭은 빼라(출처 전환 = 전체·메일·슬랙)
- **행동 단추 전부 뺀다**: `+`(업무로 추가) · `내 업무로` · `답장` · `확인완료` · `원문 확인하기` · `대화방 열기` · 메일 카드의 `업무`/`참고` 배지. 남기는 것: 카드 누르면 원문+읽음 · 머리 `모두 읽음으로`
- 레일 카드 모양(메일 단건 카드 · 슬랙 대화방 카드 = 방 하나, 마지막 3줄 미리보기)은 시안 그대로

## 3. 본문(원문) 영역 — 다시 그린다

**공통**: 지금은 문단이 1359px 폭 전체로 퍼지고 머리가 회색 한 줄이라 이상하다(사용자 지적). 읽기 폭을 둔다(메일 본문 ~720px).

**메일**
- 머리: 제목 → 표처럼 줄마다 `보낸 사람` · `받는 사람` · `참조` · `날짜` · `받은 계정`
- 본문: HTML 메일을 전제로 — 원래 모양(표·서명·인용)을 담는 틀(목업은 HTML 조각을 흉내낸 영역이면 된다). 인용 접기 정도는 있어도 됨
- 첨부: 파일 칩(유형 아이콘 · 이름 · 크기 · 받기), 이미지면 썸네일

**슬랙 — 진짜 슬랙 대화방처럼** (사용자 첨부 캡처 기준)
- 머리: `#채널명` 또는 DM·그룹DM은 참여자 이름 · 참여 N명 · 「슬랙에서 열기」 링크 하나(이건 남긴다 — 외부 링크일 뿐 행동 아님)
- 날짜 구분선(가운데 알약 「10월 2일 금요일」 · 「어제」 · 「오늘」)
- 메시지: 아바타 · **이름** · 시각 → 본문. **같은 사람이 연달아 쓴 메시지는 묶어** 아바타·이름 없이 왼쪽에 시각만
- 서식: 굵게 · 번호/글머리 목록 · 들여쓴 하위 목록 · `@멘션` 칩 · 링크 칩 · 인라인 코드 · 이모지
- 첨부: 이미지 인라인 미리보기(파일명 + 큰 썸네일) · 파일 칩
- 리액션 칩(이모지 + 수) — **읽기 전용**
- 스레드: 부모 메시지 아래 「답글 N개 · 마지막 답글 시각」 줄, 누르면 답글이 펼쳐진다(들여쓰기)
- 봇 메시지도 같은 모양(앱 표시만)
- **없음**: 메시지 입력창 · hover 행동 막대 · 리액션 추가 — 조회 전용이다
- 새 메시지가 실시간으로 들어온다는 전제 — 맨 아래 「새 메시지 N개」 정도의 표시는 자유

## 4. 목데이터
`data.js` 를 위 모양이 다 드러나게 바꾼다: 메일 2~3통(HTML 본문·첨부·참조 있는 것 포함), 슬랙 채널 1 · DM 1 · 그룹DM 1, 날짜 두세 날 · 연속 메시지 묶음 · 목록 서식 · 멘션 · 링크 · 이미지 · 리액션 · 스레드 · 봇 메시지. 실명·실제 회사 대화 넣지 마라(가상 인물).

## 5. 네 상태
시안 README 규약 「화면은 네 상태를 같이 그린다」 — 레일·본문에 로딩·빈·오류를 시안 안에서 확인할 수 있게(토글이든 별도 상태든).

## 6. 끝나면
1. 고친 파일을 로컬 사본 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/reference/2026-09-10-sc-meeting/package 2/` 같은 경로로 다시 받는다(원문 그대로 · 256KiB 넘는 파일 없음 확인)
2. `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/design-change-1.md` 에 바꾼 것 · 파일별 바이트 · 시안에서 일부러 안 그린 것을 적는다
3. 코드 레포·문서 레포 다른 파일 건드리지 마라. 커밋·push 금지

## 9. 완료 보고 — 문구 변경 금지

> 핸들은 dispatch preamble 의 값을 믿어라. 아래 코디handle 과 다르면 preamble 이 맞다.

```bash
orca orchestration send \
  --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_208c9243-9983-47ba-9983-e3aa67ecf049 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: 메시지함 시안" \
  --body "바꾼 파일 / 요약 / 로컬 사본 / 미결"

orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b \
  --text "[worker_done] architect 완료 — 메시지함 시안. 상세는 design-change-1.md" --enter
```
- 막히면: `orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[질문] architect: <질문>" --enter`
