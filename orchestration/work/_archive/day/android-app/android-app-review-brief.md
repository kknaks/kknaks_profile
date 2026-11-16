# [reviewer] Android 개발 앱 1판(AND-1~4) 코드 검수

너는 **day `reviewer` 워커**다. 맥락이 없다고 가정하라. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`) · 코드 레포 `AGENTS.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/android-app` (read-only — mobile 워커의 **미커밋** 변경을 본다)
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

- Delivery `gh issue view 251 -R MediSolveAIDev/CENTURION_DAY`(v2 approved · L3) — 이번 판은 AND-1~4 · A1~A5 · A7.
- 스펙(mediness main — `git -C /Users/kknaks/orca/workspaces/mediness-mediness/android-app-spec show origin/main:<path>`): `products/day/40-architecture/mobile-deployment.md` §7-0 · §7-2 · §3 / `products/day/20-spec/spec-003-mobile-app.md` §3 「Android 개발 앱 — 네이티브 채널」 · A-48.
- 워커 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/app-1-report.md` · 스크린샷 `app-1-shots/` · 브리프 `android-app-app-brief.md`.
- 사용자 결정: A5 음성 입력(말하기 → 자막 → 번역 음성)은 에뮬레이터가 아니라 Play 내부 테스트 실기기(A6)에서 확인(2026-11-13) — 이것을 FAIL 로 잡지 마라.

기대는 개념: 해당 없음.

## 2. 배경

`app/android/` 를 새로 만들고 네이티브 채널 3개(`day/session` 구현 · `day/push` · `day/video` 스텁)를 Kotlin 으로, 통역 권한 · 플러그인 설정, README Android 절을 더했다. Dart(`app/lib`) · iOS 변경 0 이 기본.

## 3. 볼 것 — 판정 축

1. **채널 계약** — `app/ios/Runner/AppDelegate.swift` 와 Kotlin 을 줄 단위로 대조(메서드 이름 · 인자 · 반환 · 오류 코드). 특히 **`clearIf` 원자성**(읽기 · 비교 · 삭제가 하나의 직렬 실행 · save 와 섞이지 않음 · 비교 칸이 iOS 와 같음)과 `load` 실패 처리.
2. **세션 저장 보안** — Keystore AES-GCM(IV 재사용 0 · 키 alias · 예외 처리) · 백업 · 기기 이전 제외 · 평문 저장 0 · 로그에 토큰 출력 0.
3. **id 주입** — `-P` > `identity.local.properties` > `identity.properties` 우선순위가 실제 gradle 코드에서 그렇게 동작하나 · 소스에 실제 id 없음 · `.gitignore` 에 local 파일.
4. **권한 · 매니페스트** — 플러그인 필요 권한 누락 · 불필요 권한(Play 정책 리스크: READ_MEDIA_* — 워커 이슈 2) · cleartext 0 · queries.
5. **Dart · iOS 무변경** — `git status` · `git diff` 로 `app/lib` · `app/ios` · `app/test` 변경 0. `app/.metadata` · `app/README.md` 변경은 추가만인지(README 기존 줄 수정 0 — 다른 브랜치에서 사용자가 README 를 고치고 있다).
6. **빌드 설정** — targetSdk 36 · minSdk 24 근거 · `flutter_pcm_sound` compileSdk 덮어쓰기 범위가 그 모듈만인지 · release 서명이 debug 키라는 점이 다음 판 전까지 위험 없는지.
7. **A7 비밀 0** — 새 파일 전체 grep(키 · 토큰 · 비밀번호 · 이메일).
8. **조용히 통과하는 자리** · **사용자가 실물에서 만날 자리**(Android 개발 앱).
9. 관문 명령 1회씩: `cd app && fvm flutter analyze` · `fvm flutter test` · `fvm flutter build apk --debug`(워커 리포트의 `-P` · `--dart-define` 인자). iOS 빌드는 워커 결과 인용 가능(시간이 되면 1회).

## 4. allowed_paths

- (read-only — 리포 파일 수정 금지. 산출물은 리포트 1개뿐 · 빌드 산출물은 gitignore 된 build/ 만)
- 에뮬레이터를 띄우지 마라. 사용자 프로세스를 끄지 마라.

## 5. 산출물

- `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/review-code-1-report.md` — 판정 FAIL/WARN/PASS · 지적마다 파일:줄 + 근거(SPEC 절 · Delivery A · iOS 줄) · 고칠 방향 · 「조용히 통과하는 자리」 · 「사용자가 실물에서 만날 자리」 · 스펙에 반영할 것(id 주입 · 세션 저장 · minSdk).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_8e0ca63c-29ac-420f-ac99-dbde1f5f2c96 --from term_dd8d4e4a-ede4-45b0-bb51-a7ac356c3143 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_8e0ca63c-29ac-420f-ac99-dbde1f5f2c96 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_8e0ca63c-29ac-420f-ac99-dbde1f5f2c96 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
