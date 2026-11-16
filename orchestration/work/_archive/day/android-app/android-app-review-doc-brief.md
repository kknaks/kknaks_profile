# [reviewer_doc] Android 개발 앱 로컬 실행 — 스펙 개정 · Delivery #251 v1 검수

너는 **day `reviewer_doc` 워커**다. 맥락이 하나도 없다고 가정하라. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/android-app-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ **read-only.** planner 가 이 워크트리에 미커밋 변경을 남겼다 — 리포 파일을 고치지 마라. 산출물은 리포트 1개뿐.

## 1. SSOT — 먼저 읽을 것

- 사용자 결정 표: `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/android-app-spec-brief.md` §1 「사용자 결정」 · §2 · §3 — **이 표가 기준**
- 범위 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/_archive/day/fix-web/android-app-handoff.md` §2~§6
- planner 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/spec-report.md` (전수조사 표 · 변경 파일:줄 · 미결 · 주의점)
- Delivery v1 산출물: `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/delivery/android.v1.request.json` · `.plan.json` · `.apply.json` · Issue https://github.com/MediSolveAIDev/CENTURION_DAY/issues/251 (`gh issue view 251 -R MediSolveAIDev/CENTURION_DAY`)
- 코드(읽기만 · 사실 확인용): `/Users/kknaks/orca/workspaces/CENTURION_DAY/android-app` (dev `0106654e`) — `app/ios/Runner/AppDelegate.swift` · `app/lib/data/session_store.dart` · `push_bridge.dart` · `app/lib/chat/video_pick.dart` · `chat/screens/chat_video_screen.dart` · `app/lib/interpret/audio_io.dart`

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

사용자 2026-11-12: Android 는 **개발 앱(`day.medisolveai.dev` · `DAY Dev`)을 로컬 에뮬레이터에서 띄워 dev 로그인 → 화면 확인까지**만. session 은 구현, push · video 는 스텁, iOS 무변경, FCM · Play · keystore · 정식 앱 id 는 [미결]. planner 가 이것을 mobile-deployment · SPEC-003(개정 ⑭) · SPEC-004(개정 ⑥) · 20-spec · log 에 반영하고 Delivery #251(L2) v1 을 발행했다. 승인 전 검수다.

## 3. 계약

해당 없음(문서 검수). 채널 3개 사실은 위 코드로 확인한다.

## 4. 볼 것 — 판정 축

1. **결정 표 일치** — 스펙 · Delivery 가 결정 표와 다른 곳(넓힘 · 좁힘 · 빠짐). 특히 [미결]이어야 할 것(정식 id · 배포 방식 · keystore · FCM · 세션 저장 위치 · 빌드 주입 방식)이 [확정]으로 올라간 곳.
2. **닫힘/남음 분리** — M-4 · M-17 · M-9 가 정한 만큼만 닫혔나. §13 표와 본문(§1 · §3 · §7 · §9 · §12)이 서로 같은 말을 하나.
3. **전수조사 누락** — `git -C /Users/kknaks/orca/workspaces/mediness-mediness/android-app-spec diff` + `grep -rn -i "android\|fcm\|application id\|app/android" products/day/` 로 다시 세서 planner 표 밖에 낡은 줄이 남았나.
4. **코드 사실** — planner 의 정정(「`day/video` 오디오 = 채팅 동영상 재생 화면 · 통역은 `audio_session` 으로 별개」)이 코드와 맞나. 채널 메서드 목록이 AppDelegate 와 맞나.
5. **A-48 인수 조건** — planner 가 브리프보다 넓힌 항목(재실행 자동 로그인 · 로그아웃 뒤 세션 없음 · 푸시 없이 오류 화면 없음)이 결정 범위 안인지, 에뮬레이터에서 확인 가능한지 의견.
6. **Delivery** — Target Delta · Non-Goals · risk L2 · baseline pending/v2 재결속 메모가 스펙과 맞나. 화면 문구 발명 · 키 · 계정 · 서버 값 0.
7. lint: `python3 scripts/lint-pipeline.py --strict` → products/day ERROR 0 (직접 1회).

## 5. allowed_paths — 이 밖은 건드리지 마라

- (read-only — 리포 파일 수정·생성 금지. 산출물은 아래 리포트 파일 1개뿐)

## 6. 단계

1. 위 문서 읽기 → 2. 판정 축 1~7 → 3. 리포트 작성 → 4. 완료 보고.

## 7. 범위 제약 — 하지 말 것

- 파일 수정 · 커밋 · push · PR · Issue 코멘트 · 라벨 변경 · receipt 적용 금지.

## 8. 검증 / 산출물

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/review-doc-1-report.md` — 판정(PASS/WARN/FAIL) · 지적마다 파일:줄 + 근거(결정 표 행 · 코드 파일:줄) · 고칠 방향 · 「조용히 통과하는 자리」 따로 · 사용자 판단이 필요한 것 따로

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_8e0ca63c-29ac-420f-ac99-dbde1f5f2c96 --from term_ff662177-d76e-437b-af67-574540a68ea3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_8e0ca63c-29ac-420f-ac99-dbde1f5f2c96 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_8e0ca63c-29ac-420f-ac99-dbde1f5f2c96 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
