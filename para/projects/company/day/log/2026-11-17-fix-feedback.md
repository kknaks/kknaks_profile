# 작업 요약 — fix-feedback (day)

기간: `2026-11-17` ~ `2026-11-17`
결과: 코드 CENTURION_DAY#255(dev `0c401726`) · 스펙 mediness#945(main `4443a99a`) 스쿼시 머지 · **dev 배포 성공**(GitHub Actions `DAY dev` · day-dev 새 JS 서빙 확인). migration 0 · 앱 무수정(스냅샷 `systemDoctor` 칸만 추가). prod 배포 · Delivery #254 승인은 이 작업 밖.

## 1. 무엇을 했나

명동점 현장 피드백 7건(F-1 ~ F-7)을 받아 웹 시술 현황(`/board`)을 고쳤다 — 귀가 대기 취소 · 정렬 탭(시술순/방별순) · **원장 호출 없이 「바로 시작」** · 웹 OS 알림 · 작성된 차트만 아이콘 · 원장 계정 본인 수락.
핵심은 F-3 이었다 — 마스크팩처럼 원장이 필요 없는 시술이 있는데 11-09 결정(「원장 없이 시작하는 길 없음」)과 코드(`no_doctor`)가 막고 있었다. 사용자가 「시스템 계정을 집도의로 넣으면 안 되냐」를 냈고 HAR 로 KOS 가 받는 걸 확인해 그 길로 열었다.
로컬 E2E 1회차에서 6건(E1 ~ E6)이 더 나와 2루프로 고쳤고, 보류했던 F-5(줄마다 ⋮ 되돌리기 · 호출 취소)도 같은 묶음에 넣었다. 호출 취소 「알림」은 심사 중 앱 때문에 뒤로 미뤘다. E2E 2회차 확인 뒤 머지 · dev 배포.

## 2. 적용한 기술·개념

- **집도의 「없음」을 비우지 않고 자리 채움 값(병원 시스템 계정)으로** — 원장 없이 시작하는 시술 → [[tolerant-reader]]
  - 왜 이걸 골랐나: 후보는 B(준비중이면 집도의 없이 누구나 시작) · C(「호출 불필요 시술」 목록을 새로 둠)였다. 둘 다 KOS 가 「집도의 빈 작업」의 진행 · 완료를 받는지 모르는 채였고, C 는 데이터에 근거 칸이 없었다(research-1 Q3). 시스템 계정은 이미 호출 때 KOS 담당자로 쓰던 값이라 KOS id 가 병원마다 있고, 사용자 HAR(`change-tasks-doctors`[시스템 계정] 200 → `change-tasks-complete` 200)로 KOS 쪽 길이 확인됐다. DAY 화면에서는 원장 목록 밖이라 원장 칸이 비므로 「간호관리」로 표시(E3).
  - 무엇이 어려웠나: 표시 칸 `systemDoctor` 를 「집도의 = 시스템 계정」만으로 켜서, 시작 취소 → 다시 호출한 줄도 「간호관리 호출」이 돼 호출 대상이 가려졌다(검수 N1 — 어느 테스트도 안 잡음). 진행중 · 완료 줄에서만 참으로 좁혔다. 앱은 모르는 칸을 무시해 심사 중에도 안전했다.
  - 근거: `research-1-report.md` Q1 · Q2 · Q3 · `review-code-2-report.md` N1 · `be-3-report.md` · CENTURION_DAY#255
- **새 알림 종류 = PG enum 값 추가 = migration · 앱 배지 어긋남 → 기능은 넣고 알림만 미룸** — 호출 취소 알림 → [[database-migration]] · [[tolerant-reader]]
  - 왜 이걸 골랐나: 앱은 모르는 알림 종류를 목록에서 버리지만(관대한 읽기), 서버 `unread` 는 종류를 안 가리고 세서 **종 배지 숫자와 목록이 어긋난다** — 개별 원소에 관대한 것과 집계가 맞는 것은 다르다. 게다가 enum 값은 더하면 못 뺀다. 호출 취소 자체는 기존 칸(`doctor_call_task.deleted_at` · `closed_at`)으로 되어 migration 0 으로 갔다.
  - 근거: `spec-3-report.md` 「앱 코드 사실」 · `spec-4-instructions.md` · `_RESUME.md` §2 2026-11-17 호출 취소 행
- **페이지 가시성(`document.hidden`) ≠ 사용자가 그 화면을 보고 있음** — 웹 OS 알림 → [[desktop-native-notification]]
  - 무엇이 어려웠나: 「탭이 뒤일 때만 띄움」을 코디 기본값으로 박았는데, 웨일 창이 오른쪽 모니터에 **보이는 채로** 있으면 `hidden=false` 라 알림이 아예 안 만들어졌다(알림 센터에도 없음). 서버 로그로 「행 생성 → 스트림 신호 → 목록 GET」까지 정상임을 먼저 확인하고 나서야 화면 조건으로 좁혀졌다. 사용자 결정 = 늘 띄움.
  - 근거: `e2e-feedback.md` E1 · E5 · `fe-2-report.md`
- **같은 401 이 서로 다른 사유** — KOS sign-in 401 = 비밀번호 틀림 / `SignInLimitExceeded`(기기 5대 제한) → [[external-api-error-classification]]
  - 무엇이 어려웠나: DAY 는 sign-in 400/401 을 전부 「비밀번호 틀림」으로 처리해서(`emr/kos/staff_client.py:88-90`) E2E 중 로그인이 안 되는 원인이 안 보였다. 사용자 HAR 의 본문(`"message":"SignInLimitExceeded"` · `maxSignInCount: 5`)으로 갈렸다. 다른 기기 로그인에 밀린 토큰 401 → 세션 종료까지 같은 뿌리. 고치는 건 범위 밖 후속.
  - 근거: `_RESUME.md` §1 「새 항목」 · HAR `~/Downloads/기기로그인.har`(비밀번호 평문 — 레포 밖)
- **숨은 입력 요소의 기준 상자(containing block)가 스크롤을 끌어간다** — 의사 호출 팝오버 위쪽 잘림(E2)
  - 무엇이 어려웠나: 숨은 라디오(`.day-opt__radio` · `position:absolute`)의 기준이 목록이 아니라 고정 팝오버(`.day-pop`)라, 아래쪽 원장이 기본 선택일 때 포커스가 `overflow:hidden` 인 팝오버 자체를 스크롤했다. `.day-opt{position:relative}` + `.day-pick{overflow:clip}`. dev 에 원래 있던 버그였다.
  - 근거: `fe-2-report.md` E2 · `review-code-2-report.md`

## 3. 막혔던 것 / 사고

- **디스크 가득(ENOSPC)이 두 군데를 동시에 죽였다** — 11:35 planner 가 파일 쓰기 · 셸 · 코디 보고까지 못 해 조용히 멈췄고(사용자가 디스크를 비운 뒤 재개), 같은 시각 **Docker 엔진이 crash** 했다. 그 뒤 Docker Desktop 을 다시 열고 업데이트해도 엔진이 안 떴다 — 로그(`com.docker.backend.log` 「recovering from engine crash」 뒤 무음)와 프로세스 시작 시각(11-09 의 backend 가 살아 있음)으로 **죽은 backend 프로세스가 남아 새 실행이 그것에 붙기만 했다**는 걸 찾았다 → 강제 종료 후 재실행. 그 전에 내 대기 루프가 `timeout` 명령이 없는 셸에서 바로 끝나 「안 뜬다」를 잘못 보고했다. 시간을 가장 많이 쓴 구간.
- **KOS 로그인 기기 제한** — E2E 중 로그인이 갑자기 안 됨 → 로그(동기화 401 · 세션 종료)로 KOS 거절까지 좁히고, 사용자 HAR 로 `SignInLimitExceeded` 확인. 해제 API(`get-active-sign-ins` · `revoke-active-sign-in`)로 DAY 서버(52.x) 외 로그인을 정리했다. kknaks@ 계정은 로컬 개인정보 플러그인이 「이메일 + User-Agent 한 호출」을 막아 스크립트를 만들어 사용자가 직접 실행.
- **워커 완료 알림이 코디를 못 깨웠다**(be-2 · fe-2 · review-code-2 세 번) — 인박스에는 들어와 있었다. 사용자가 「돌아가고 있냐」를 두 번 물었다. → 발주 뒤 리포트 파일 · 인박스를 직접 확인하는 루프로 바꿈.
- **코디 기본값이 E2E 에서 틀렸다** — 「탭이 뒤일 때만 알림」(E5)은 사용자 기대와 반대였다. 착수를 막는 OQ 에 기본값을 박는 건 맞았지만, 사람 눈이 닿는 동작은 E2E 첫 항목으로 짚었어야 했다.
- **F-1 을 「DAY 안에서만 되돌린다」로 잘못 말했다** — 그러면 다음 동기화에 카드가 다시 빠진다. 바로 정정하고 KOS `change-flow-step` 을 보내는 쪽으로.
- **용어를 넓혀 썼다** — 사용자 「선택한 거 바로 시작」을 「일괄 시작」으로 불러 정정받음.

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-17 | F-1 귀가 대기 취소 = 직전 단계(완료)로 · ⋮ · KOS `change-flow-step` 보냄 | 사용자 · 안 보내면 다음 동기화에 카드가 빠짐 |
| 2026-11-17 | F-2 시술순(오더지 순 · 끌기) / 방별순(방 이름 오름차순 · 끌기 없음 · 빈 방 제외) · 서버 정렬 `?sort=room` | 사용자 · SSE 로 다시 그려도 탭 유지 |
| 2026-11-17 | F-3 바로 시작 · 집도의 없으면 시스템 계정 · ~~원장 없이 시작 없음(11-09)~~ 이 경로에 한해 뒤집음 · 단건 [시작] 그대로 | 사용자 · HAR |
| 2026-11-17 | F-4 웹 OS 알림 = 원장 호출만 · ~~탭이 뒤일 때만~~ → 늘 띄움 | 사용자(E5) |
| 2026-11-17 | F-5 = 준비중 ⋮ 없음 · 호출 → 호출 취소 · 진행중 → 시작 취소 · 완료 → 완료 취소 | 사용자(E4) |
| 2026-11-17 | 호출 취소 = DAY 만(KOS 에 명령 없음) · 알림 · 앱 푸시는 앱 업데이트 뒤 | 사용자 · 심사 중 앱 배지 · migration |
| 2026-11-17 | F-6 작성된 차트만 파란 아이콘 · F-7 원장 계정 본인 수락(앱과 같게) · E6 차트 = 시술 이름 글자만 + 호버 「차트 작성」 · E3 「간호관리」 | 사용자 |

## 5. 날짜별 로그

- `2026-11-17` 현장 피드백 7건 수집 · researcher 조사 → F-3 시스템 계정 결정(HAR) · planner SPEC-002 ㉑ · SPEC-005(디스크 가득으로 한 번 멈춤) · 문서 검수 2회 · be · fe 1루프 · 코드 검수 · Docker 복구 · 전체 1281 passed · 로컬 E2E 1회차(E1 ~ E6 · KOS 기기 제한 정리) · 2루프(spec-3 · 4 · 검수 · be-2 · fe-2 · 검수 · N1) · 전체 1298 passed · E2E 2회차 · 머지 #255 · #945 · dev 배포

## 6. 산출물

프로젝트와 당시 작업 문서는 `sync-work-links.py`가 만드는 작업 목차로 연결한다.

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/945 (스쿼시 `4443a99a`)
- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/255 (스쿼시 `0c401726` · dev 배포 run 44028948837)
- `kknaksss/fix-feedback-spec` → `main`
  - `ec0546e9` docs(day): DAY 현장 피드백 F-1~F-7 · E2E — SPEC-002 개정 ㉑ · ㉒ · SPEC-005 2026-11-17 개정
- `kknaksss/fix-feedback` → `dev`
  - `bef7bd0a` feat(board): 현장 피드백 F-1~F-7 · E2E — 바로 시작 · 귀가 대기 취소 · 호출 취소 · 정렬 탭 · 웹 OS 알림
- 리포트: `research-1-report.md` · `spec-report.md` ~ `spec-5-report.md` · `review-doc-1` ~ `3-report.md` · `be-1` ~ `3-report.md` · `fe-1` · `2-report.md` · `review-code-1` · `2-report.md` · `e2e-feedback.md`

## 7. 잔여

- **prod 배포** — dev 까지. prod 는 사용자 판단(병원 마감 뒤 · migration 없음).
- **Delivery CENTURION_DAY#254** — 스펙 머지됐으니 v2 재결속 → 승인 또는 닫음(사용자).
- **호출 취소 알림 · 앱 푸시** — 앱 업데이트 뒤(새 알림 종류 = enum migration · `unread` 를 앱이 아는 종류만 셀지 SPEC-005 OQ-N14).
- **KOS 로그인 기기 제한** — `SignInLimitExceeded` 를 「비밀번호 틀림」과 구분해 보여 주기 · 시스템 계정(동기화) 자리 관리.
- 토스트 글자 미정: `conflict`(시스템 계정 KOS id 없음) · `task_not_called` · `visit_not_home` — 지금 일반 거절 글자.
- 빈 방 표시(방별순) · 웹 푸시(탭 닫아도) — 다음 스펙.
- `day-local` 은 이 작업 코드 이미지로 떠 있다(워크트리 제거 뒤에도 이미지 유지 · dev 와 같은 코드).

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/day/fix-feedback/README|fix-feedback]]
<!-- work-links:end -->
