# [backend · 원인 찾기] F6 — 예약 상세 [문진 QR] 누르면 QR 이 잠깐 떴다 사라짐 · 태블릿에 안 감

너는 **day `backend` 워커**다. 맥락이 없다고 생각하고 이 파일만 따른다. 먼저 역할 문서를 읽어라(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservations-fix` (base `origin/dev` `65506f35`) — 레포 루트 `AGENTS.md` 먼저
- 앞 조사: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/research-1-report.md`(코드 읽기 결과 · 파일:줄)

**이번 일은 구현이 아니다. 레포 파일을 고치거나 커밋하지 마라.** 스크립트는 레포 밖 `/private/tmp/<이 작업 폴더>/` 에만. 결과는 리포트 하나.

## 1. 증상 (사용자 · dev `https://day-dev.medisolveai.com/reservations`)

- 예약 상세에서 [문진 QR] 을 누르면 **QR 이 잠깐 떴다가 바로 사라진다.** [태블릿에 보내기] 도 순간 사라져 누를 수 없다. 태블릿엔 아무것도 안 간다.
- 상세 스크린샷(`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/f3-day-detail-modal.png`) 머리에 「만료 · 시간이 지났어요」 — 요청이 만들어지자마자 만료로 읽히는 꼴.
- 코드 경로(research-1 §3.3 · §3.5): `routers/reservation_displays.py` → `services/displays.py` `create`(10분 시한 · 같은 방문 열린 요청 취소) → `signal` → 모달 다시 그림 → `reservations_display.html` 진행 칸(pending ∧ qrUrl 일 때만 QR · [태블릿에 보내기]).

## 2. 찾을 것

1. **왜 바로 사라지나** — 후보를 코드 + 실물 근거로 하나로 좁혀라. 예: 시한 계산(시간대 · naive / aware · DB `now()` 와 앱 시각) · `signal` 로 다시 그릴 때 새 요청이 또 만들어지거나 앞 요청을 취소 · 다시 그리는 조각이 상태를 다르게 읽음 · `qr_url_of` 가 origin 없음으로 null 등. 지어내지 말고 근거로.
2. dev 실물 근거(읽기만):
   - dev 서버 로그 — `ssh day-vm`(dev 컨테이너 로그 · 배포 문서 `products/day/40-architecture/deployment.md` 또는 레포 deploy 문서에서 dev 가 어디 떠 있는지 먼저 확인). 오늘 `display-requests` 요청 · 응답 · 오류.
   - dev DB 읽기 SELECT — 접속법은 레포 · 배포 문서에서(`ssh -N day-db` 터널 + `psql service=day` 는 **prod** 일 수 있다 — dev DB 가 어디인지 먼저 확인하고, prod 면 접속하지 마라). 오늘 `display_request` 행: 만든 시각 · 만료 시각 · 상태 · 취소 시각 · kind · device — 값 대신 시각 차이(초)와 상태만.
   - dev 환경 값 중 시한 · origin 관련 **키 이름과 있음 / 없음**만(값 출력 금지).
3. 로컬 재현이 필요하면 레포 시험(pytest)으로만 — 로컬 스택 · docker · 포트 띄우지 마라.
4. 같은 원인이 [여권 스캔] · 앱 「태블릿 보내기」에도 닿는지.
5. 고칠 자리(file:line) 후보 — **고치지는 마라.** 다음 단계가 이 흐름을 「기기 팝오버에서 고르면 그때 요청 생성 · 바로 보냄」으로 바꾼다(문진 · 여권 같음). 원인이 그 새 흐름에도 남는지 적어라.

## 3. 하지 말 것

- 레포 수정 · 커밋 · push 금지. dev · prod 에 쓰기(INSERT / UPDATE / DELETE · 재시작 · 배포) 금지. **prod DB · prod 로그는 보지 마라.**
- `~/.config/day/` 아래 `prod-*` 열지 마라. 비밀값 · 토큰 · 고객 개인정보 원문 출력 · 기록 금지(id 앞 8자만).
- 확인 못 한 것은 「확인 못 함」. 지어내지 마라.

## 4. 리포트

`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/be-f6-debug-1-report.md` — 맨 위: 원인 한 줄(확정 / 후보) + 근거 · 그 아래 실물 근거 표 · 고칠 자리 · 새 흐름에도 남는지 · 여권 · 앱 영향.

## 5. 검증

- 원인은 실물 근거(로그 줄 · DB 시각 차) 하나 이상과 코드 file:line 이 같은 말을 해야 「확정」. 아니면 「후보」.

## 6. 완료 보고 — **문구 변경 금지**

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
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
