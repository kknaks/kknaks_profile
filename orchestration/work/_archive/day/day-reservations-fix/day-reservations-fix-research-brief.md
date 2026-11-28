# [researcher · 읽기 전용] 예약 현황판 피드백 F1 ~ F6 — 원인 · 지금 동작 · 고칠 자리 전수

너는 **day `researcher` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix` (코디와 같은 워크트리 — **리포트 파일 1개 말고는 아무것도 만들거나 고치지 마라**)

**코드 · 문서 · DB 를 고치지 않는다. 결과는 리포트 하나.** 결정하지 말고 「정할 것」으로 모은다.

## 1. SSOT — 먼저 읽을 것

- 피드백 원문 · 스크린샷: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/_RESUME.md` §1 (F1 ~ F6) · 같은 폴더 `f1-kos-add-slot.png` · `f3-day-detail-modal.png` · `f3-kos-survey-menu.png` · `f5-day-device-card.png` (이미지는 Read 로 본다)
- 코드: CENTURION_DAY 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservations-fix` (`origin/dev` `65506f35` — **읽기만**. 레포 루트 `AGENTS.md` 먼저)
- 스펙(mediness `origin/main`, `git -C /Users/kknaks/git/harness_works/mediness-mediness show origin/main:<path>`): `products/day/20-spec/` 중 예약 현황(spec-006) · 예약 상세(SPEC-007) · 앱 · 문진 · 태블릿 관련 스펙 전부(파일 목록을 `git ls-tree` 로 먼저 세라) · `products/day/10-decision.md`
- 앞 작업 기록(왜 지금 모양인지): `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/_archive/day/day-reservation/` · `day-reservation2/` · `day-app-re1/` 의 `_RESUME.md` §2 결정 표
- KOS 문서: `/Users/kknaks/git/ax-clinic-project` · 참고 구현 cc-prototype `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:<path>`

기대는 개념: 해당 없음.

## 2. 배경

DAY 예약 현황판(웹 `/reservations` · dev `day-dev.medisolveai.com`)을 사용자가 써 보고 피드백 6개를 줬다. 고치기 전에 **각각 지금 코드가 어떻게 동작하는지 · 왜 그런지 · 고칠 자리가 어디인지**를 근거와 함께 알고 싶다.
이 조사 다음에 사용자가 예약 · 접수 · 상담 · 시술 모달 디자인을 고칠 예정이다 — 이번 조사 범위는 아니지만, F3 · F5 처럼 모달에 닿는 자리는 「어느 템플릿 · 조각이 그리는지」를 적어 두면 다음 단계에 쓴다.

## 3. 물음 (각각 답 + 근거 file:line · git ref)

1. **F1 예약 추가 자리** — 시간 칸에 카드가 있을 때 예약 등록을 여는 클릭 자리가 어떻게 정해지나(빈 칸 클릭 핸들러 · 칸 너비 · 카드 배치 CSS · JS). 카드가 칸을 꽉 채우는 원인. KOS 모양(카드 오른쪽 여백 + 호버 점선 [+] + 툴팁 「그룹 | 시작 ~ 끝」 · `f1-kos-add-slot.png`)을 넣으려면 닿는 파일 전부. 툴팁에 쓸 그룹 이름 · 칸 시작 ~ 끝 값이 지금 화면 데이터에 있나.
2. **F2 카드 높이** — 카드가 몇 칸을 차지할지 무엇으로 정하나(예약 시작 ~ 끝 · 그룹 간격 · 고정 1칸). 사용자 질문 「설정에 그룹 시간 설정이 돼 있는 거 아니야?」의 답: 그룹 간격 설정이 DAY 에 있나(어디 · 어떤 값) · 화면이 그걸 쓰나. 60분 예약(`_RESUME` F2 카드)의 DB 시작 · 끝 값이 실제로 60분인지(로컬 데모 DB 읽기 SELECT 로 · 못 하면 「확인 못 함」) · KOS 동기화가 끝 시간을 제대로 담는지(매퍼 file:line).
3. **F3 [문진 QR] 버튼** — 예약 상세 모달의 [문진 QR] · [여권 스캔] 버튼이 지금 비활성인가(템플릿 조건 · 클래스). day-reservation2 결정 「버튼 자리만 · 비활성」 이후 day-app-re1 등에서 웹 쪽 동작이 열렸나. 문진 링크 · QR 을 만드는 서버 경로(라우터 · 서비스)가 있나 · 링크 복사 / 링크 열기에 쓸 URL 을 웹이 얻을 수 있나. 앱에는 문진 QR 이 어떻게 붙어 있나(웹과 비교).
4. **F5 기기 상태 카드** — 「데스크 · 접속 중」 카드를 그리는 곳(템플릿 · JS file:line) · 언제 왜 생겼나(git log · 커밋 · 스펙 근거). 기기 목록 · 연결 상태(연결 / 미연결)를 웹이 어디서 얻나(SSE · API · 테이블) · 기기가 여러 대일 때 고를 수 있는 데이터가 있나.
5. **F6 태블릿 전송이 안 됨** — 웹 → 서버 → 기기(태블릿 앱) 전송 경로를 끝까지 따라가라(버튼 핸들러 · 엔드포인트 · 서비스 · 기기 연결 채널 · 앱 수신부). 앱의 「태블릿 보내기」(day-app-re1)와 같은 경로인가. **어디서 끊기는지** 코드 근거로 후보를 좁혀라(웹 버튼이 비활성이라 안 가는 것인지 · 엔드포인트 없음 · 기기 매칭 · 채널 등). 실행 확인은 하지 말고 코드로만 — 확정 못 하면 후보 + 「실물로 확인할 것」.
6. **F4 문진 재작성 6개월 정책** — 문진 기록이 DAY 에 어떻게 남나(테이블 · 칼럼 · 작성일 / 제출일 칸이 있나) · 고객 단위인가 방문 단위인가. 예약 상세 「초진 문진」 줄은 지금 무엇으로 「작성 필요」를 정하나. 재진 고객에 문진 줄이 보이나. KOS · cc-prototype 에 문진 유효 기간 개념이 있나. 6개월 정책을 넣으려면 닿는 자리.
7. **빠진 것** — 위를 고치려면 새로 필요한 것(엔드포인트 · 칼럼 · 동기화 · 앱 수정) 목록.

## 4. allowed_paths

- 리포트 1개만 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/research-1-report.md`
- 임시 파일이 필요하면 `/private/tmp/` 아래 너만의 폴더(워크트리 밖).

## 5. 하지 말 것

- 고치기 · 커밋 · push · PR 금지. git checkout · pull · worktree 만들기 금지. CENTURION_DAY 워크트리는 **읽기만**.
- 로컬 스택 · docker · 포트를 띄우거나 내리지 마라(이미 떠 있는 로컬 DB 에 읽기 SELECT 는 됨 · 접속법은 레포 문서에서 · 못 찾으면 「확인 못 함」). INSERT / UPDATE / DELETE 금지. dev · prod 서버 · DB 접속 금지.
- KOS 를 직접 호출하지 마라. 고객 이름 · 전화 · 메모 원문을 리포트에 쓰지 마라(방문 id 앞 8자만). `*.env` 읽지도 출력하지도 마라.
- 없는 값을 다른 필드로 추정해 채우지 마라. 모르면 「없음 / 확인 못 함」. 결정하지 말고 「정할 것」으로. 화면 문구를 지어 쓰지 마라.

## 6. 리포트 모양

맨 위: 물음 1 ~ 7 답 한 줄씩 표(F 번호 붙여서) → 「정할 것」(사용자에게 물을 것 · 각각 선택지와 근거 · 추천이 있으면 추천과 이유) → 아래 물음별 근거(file:line).

## 7. 검증

```
질문마다 답 + 근거(파일:줄 · git ref · 문서 URL). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다
```

- 「닿는 파일」은 목록을 내가 주지 않는다 — **관련 클래스 · 엔드포인트 · 함수 이름으로 grep 해서 쓰는 곳을 전부** 세고, 센 수를 적어라.

## 8. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_99b025fc-f3ef-403e-8162-509c41545e2e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
