
# [researcher] DAY 직원 앱 다음 버전 — 현황 조사(read-only)

너는 **day `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 워크트리는 코디네이터 워크트리다. **리포트 파일 1개 말고는 아무것도 만들거나 고치지 마라.**

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/_RESUME.md` §1 · §2 — 범위와 결정
- 스펙(mediness, 읽기만): `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/` — `20-spec/spec-001-login-session.md` · `spec-002-procedure-board.md` · `spec-003-mobile-app.md` · `spec-005-notifications.md` · `40-architecture/mobile-deployment.md` · `10-decision.md`
- 회고(이전 작업의 결정 · 잔여):
  - `para/projects/company/day/log/2026-11-17-kos-signin-limit.md` (앱 기기 선택 = 다음 앱 버전)
  - `para/projects/company/day/log/2026-11-17-fix-feedback.md` (바로 시작 · 호출 취소 · 귀가 취소 · 호출 취소 알림 = 앱 업데이트 뒤)
  - `para/projects/company/day/log/2026-11-11-fix.md` (통키 통역 이식)
  - `para/projects/company/day/log/2026-11-16-android-app.md` (빌드 · 업로드)
- 통키 문서: `para/projects/summer-star/interpret-pwa/` (DEC D-43 ~ D-71 · SPEC-001) · 회고 `para/projects/summer-star/interpret-pwa/log/2026-11-16-*.md`

기대는 개념: `para/areas/concept/` 에서 `tolerant-reader` 를 찾아 읽어라 — 깔린 옛 앱이 새 서버 응답을 받을 때의 기준.

## 2. 배경 / 무엇을 바꾸나

DAY 직원 앱(Flutter · `app/`) 다음 버전을 낸다. Play 정식 DAY 는 프로덕션 공개됨, iOS 0.1.0 (2) 는 심사 대기. 방법(사용자 결정): DAY Dev 앱(dev 서버)으로 먼저 내고 실기기 통과하면 같은 코드를 prod 설정으로 빌드한다.

범위 4건:
1. KOS 기기 로그인 제한 → 앱에서 이전 기기 로그아웃(웹은 #257 에 기기 선택이 있다)
2. 시술 현황 탭 — 웹에서 바뀐 것(바로 시작 · 호출 취소 · 귀가 취소 등)을 앱에
3. 호출 취소 알림 · 앱 푸시(새 notification_kind)
4. 통역 — 통키(interpret-pwa) 최신을 따라간다

이 조사는 **지금 어떻게 되어 있나와 차이**만 낸다. 무엇을 할지는 정하지 않는다.

## 3. 계약

해당 없음(조사).

## 4. 먼저 읽을 곳 (코드는 전부 읽기만)

- DAY 코드: `/Users/kknaks/git/CENTURION_DAY` — **사용자 체크아웃. checkout · pull 금지.** `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:<path>` · `git ls-tree -r origin/dev` 로 읽는다(origin/dev = `844eace4`). 레포 루트 `AGENTS.md` 먼저.
  - 앱 `app/` (pubspec 버전 · lib/ · ios/ · android/) · 서버 `backend/`(로그인 · 기기 선택 POST /login/device · 시술 현황 API · 알림 · 통역)
- 통키 코드: `/Users/kknaks/git/toy_pr2/interpret-pwa` — 읽기만. `git -C … log origin/main` 기준(최신 code #15 `56e43a0` 근처). `back/` · `front/`
- 웹 시술 현황 바뀐 것: CENTURION_DAY PR #255 · #257 (`gh pr view <n> -R MediSolveAIDev/CENTURION_DAY --json files,body` · `gh pr diff`)

## 5. allowed_paths — 이 밖은 건드리지 마라

- 생성 1개만: `orchestration/work/day-mobile-v2/research-current-state.md`

## 6. 조사 단계 — 질문마다 답 + 근거(파일:줄 · ref)

**A. 앱 공통**
- A1. 앱 버전 · 빌드 번호 지금 값(pubspec · iOS · Android versionCode) · dev/prod 설정이 어떻게 갈리나(flavor · dart-define 등) · 빌드/업로드 절차 문서 위치
- A2. 앱이 서버 응답의 모르는 코드 · 모르는 값을 어떻게 다루나(로그인 오류 · 알림 종류 · 시술 상태). 「깔린 옛 앱 + 새 서버」에서 깨질 곳 전수

**B. 기기 로그인 제한**
- B1. 앱 로그인 흐름(화면 · API · 병원 고르기 단계) 지금 모양
- B2. 서버에서 KOS `SignInLimitExceeded` 가 앱 경로로 올 때 지금 응답 · 웹 기기 선택(POST /login/device)이 쓰는 API · 응답 모양 · 앱이 그대로 쓸 수 있나 / 앱용으로 무엇이 더 필요해 보이나
- B3. DAY 로그아웃 때 KOS 세션 해제가 앱 경로에도 되나

**C. 시술 현황 탭**
- C1. 웹 시술 현황에서 가능한 동작 전수(바로 시작 · 호출 · 호출 취소 · 귀가 · 귀가 취소 · 시작 취소 · 방 옮기기 …) × 앱에서 가능한지 표 — **grep 으로 전부 센다**. 목록을 받아 맞추지 말고 웹·서버의 동작을 다 세서 표로
- C2. 각 동작의 서버 API · 오류 코드 · 토스트 글자(정해진 것 / 미정)
- C3. 앱 화면 구조(탭 · 카드 · 버튼 위치)와 웹의 차이 — 시안 · 스펙(spec-002 · spec-003 · 21-screen)이 있는지

**D. 호출 취소 알림**
- D1. 지금 notification_kind 목록(DB enum · 서버 · 앱) · 호출 취소 때 서버가 하는 일 · 푸시 경로(APNs · FCM 상태)
- D2. 새 종류 추가에 필요한 것(migration · 앱 배지/unread 셈 · SPEC-005 OQ-N14) · 옛 앱이 새 종류를 받으면 어떻게 되나

**E. 통역**
- E1. DAY 통역 지금 구현(서버 · 앱 화면 · Soniox 설정 · 사전/시드 버전)과 이식 시점의 통키 sha
- E2. 통키 그 뒤 바뀐 것 전수(코드 · 시드 · DEC D-번호) — 이식 대상 후보 / DAY 에 안 맞을 수 있는 것(PWA 전용 · 데모 로그인 등) 구분
- E3. Soniox 한도(음성 합성 3 vs 통역 상한 6 미결)가 지금 어떤가

**F. 정할 것** — 위에서 나온, 사용자나 스펙이 정해야 할 것만 목록으로(추천 있으면 한 줄).

## 7. 범위 제약 — 하지 말 것

- 코드 · 문서 수정 · 커밋 · PR 금지. 리포트 1개만.
- 서버(dev · prod) · DB · KOS 실호출 금지. 사용자 포트 · 프로세스 · docker 건드리지 마라.
- 비밀값(키 · 토큰 · IP · Azure 리소스 이름)을 리포트에 쓰지 마라 — profile 은 공개 레포.
- 화면 문구를 지어 넣지 마라. 원천에 없는 글자는 「미정」.
- 결정하지 마라. 「정할 것」으로 모은다.

## 8. 검증

```
질문마다 답 + 근거(파일:줄 · git ref · 문서 URL). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
