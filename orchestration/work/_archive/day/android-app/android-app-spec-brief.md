# [planner] Android 로컬 실행 — mobile-deployment · spec-003 반영 + Delivery 발행

너는 **day `planner` 워커**다. 맥락이 하나도 없다고 가정하고 아래를 읽어라. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/android-app-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ 같은 워크트리를 reviewer_doc 워커가 나중에 읽는다 — 리포트 외 파일은 스펙만.

## 1. SSOT — 먼저 읽을 것

### 사용자 결정 (2026-11-12 · 이 표가 정본)

원천: `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/_archive/day/fix-web/android-app-handoff.md` §2 (사용자와 범위를 닫은 인수인계) + 이번 세션 사용자 「스펙에도 반영함」.

| 항목 | 결정 |
|---|---|
| 이번 Android 범위 | **로컬 Android 에뮬레이터에서 개발 앱을 띄워 dev 서버 로그인 → 화면 확인까지.** 스토어 출시 · 푸시 · 배포는 범위 밖 |
| Android 개발 앱 식별자 · 이름 | Application ID `day.medisolveai.dev` · 이름 `DAY Dev` — iOS 개발 앱과 같게 |
| Android 정식 앱 식별자 | 정하지 않음 — **[미결]** 그대로 |
| 세션 보관 `day/session` | Android(Kotlin)에서 **구현** — iOS 와 같은 동작(load · save · clear · clearIf) |
| 푸시 `day/push` | Android 에선 **스텁** — 권한 false · 토큰 없음 · installId/appId/appName 정도만 값. FCM 은 **다음 작업**(회사 Google 계정 생긴 뒤) |
| 동영상 · 오디오 `day/video` | Android 에선 **스텁** — 채팅 동영상 첨부 · 통역 오디오 전환이 Android 에서 빠진다 |
| 알림 [수락] | Android 판 안 함(푸시 뒤) |
| iOS | 안 건드린다(정식 0.1.0 (2) 심사 중) |
| Play Console · 서명 keystore · Android 배포 방식 · FCM | 나중 — 별도 작업. **[미결]** 그대로 |

### 스펙 — 고칠 곳

- `products/day/40-architecture/mobile-deployment.md` — §1 · §3 표 · §7 · §8-1 · §9 표 · §12 끝 · §13(M-4 · M-9 · M-17 · 필요하면 M-6 · M-8)
- `products/day/20-spec/spec-003-mobile-app.md` — Android 행(:105 근처 · 범위 밖 표) · 네이티브 채널 · 푸시 · 채팅 동영상 · 통역 오디오를 다루는 절
- `products/day/20-spec.md:41` — Android 를 범위 밖으로 적은 줄
- spec-004(:76) · spec-005(:68) 의 Android 줄은 「FCM 미결 그대로」라 사실이 바뀌지 않으면 두되, 고칠지 판단해 리포트에 적는다
- **계약이 닿는 곳 전수조사**: `grep -rn -i "android\|fcm\|application id" products/day/` 로 전부 세고 시작해, 고친 곳 · 그대로 둔 곳(이유)을 리포트 표로 남긴다

- Delivery 절차: `start-delivery` 스킬 · `rules/delivery-workflow.md` · `tools/harness/references/requests.md`
- 직전 발행 기록(형식 참고): `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/_archive/day/fix-web/spec-report.md` · `_archive/day/prod-deploy-re1/delivery-report.md`

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

지금 스펙은 Android 착수 시점(M-17) · Android Application ID(M-4)를 **[미결]**로 두고, 여러 스펙이 「Android 는 범위 밖」이라고 적는다. 사용자가 2026-11-12 「Android = 개발 앱 로컬 실행만 · 푸시 없음」으로 착수 범위를 정했다. 이 결정을 스펙에 먼저 적고(코드보다 먼저), 코드 작업용 Delivery Issue 를 발행한다.

**닫히는 것과 남는 것을 섞지 마라.** M-17 은 「착수 = 로컬 실행만(2026-11-12)」으로 일부 닫히고 「출시 여부 · 시점」은 남는다. M-4 는 「dev = `day.medisolveai.dev`」만 닫히고 정식 앱 id 는 남는다. M-9(FCM)는 「이번엔 안 함 · 다음 작업」 사실만 더하고 미결 그대로.

## 3. 계약

코드 레포(CENTURION_DAY `app/`)의 네이티브 채널 3개(지금 iOS `ios/Runner/AppDelegate.swift` 에만 있음). Dart 쪽 동작은 바꾸지 않는다 — Android 에서 못 하는 것은 Kotlin 스텁으로 막는다.

| 채널 | Dart | Android |
|---|---|---|
| `day/session` | `app/lib/data/session_store.dart:79` | 구현(load · save · clear · clearIf — clearIf 는 token · api_base_url 비교 뒤 삭제, 직렬로 원자적) |
| `day/push` | `app/lib/data/push_bridge.dart:35` | 스텁 |
| `day/video` | `app/lib/chat/video_pick.dart:22` | 스텁 |

세션 토큰을 Android 에서 어디에 보관할지는 mobile-deployment §7-2 의 **[제안]**(Android Keystore 로 보호되는 암호화 저장소)이 있다. 사용자가 정하지 않았으니 **[확정]으로 올리지 마라** — 「이번 구현은 이 제안을 따른다」는 Delivery Target Delta 에 적는 정도로 둔다.

Application ID 를 빌드에 넣는 방식(productFlavors · 명령줄 빌드 값 등 — §4)은 정하지 않는다. 코드 작업에서 정해지면 나중에 반영한다 — 리포트 「정할 것」으로.

## 4. 먼저 읽을 핵심 파일

- 인수인계 §2~§6 (위 경로) — 지금 상태 · 빌드 값 · 완료 조건
- 코드(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/android-app` (base dev `0106654e`) — `app/ios/Runner/AppDelegate.swift` · 위 Dart 파일 3개 · `app/README.md` 「빌드 설정」 · `app/pubspec.yaml`(권한이 필요한 플러그인)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`

## 6. 구현 단계

1. 전수조사(위 grep) → 고칠 곳 표.
2. 스펙 개정 — 위 결정 표대로. 개정 머리글(문서 상단 개정 기록 형식 그대로 · 원천 = 이 브리프 경로 · 사용자 2026-11-12). 기획안(`00-baseline/planning/`)은 고치지 않는다. 사용자 말에 없는 화면 문구를 지어 넣지 마라.
3. 리포트에 변경 요약(파일:줄)을 남긴 뒤 **Delivery Issue 를 발행**한다: `mediness start-delivery --mediness-repo <이 워크트리> --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/android-app --github-repo MediSolveAIDev/CENTURION_DAY` — `--plan` → `--apply`. baseline 은 스펙 PR 머지 전이라 pending 이어도 된다.
   - Target Delta = `app/android/` 생성(개발 앱 `day.medisolveai.dev` · `DAY Dev`) · `day/session` Kotlin 구현 · `day/push` · `day/video` Kotlin 스텁 · 플러그인 권한(인터넷 · 마이크 · 사진/동영상 등 `pubspec.yaml` 플러그인이 요구하는 것) · `app/README.md` Android 실행법 한 절
   - 완료 조건 = 에뮬레이터에서 실제 dev 로그인 → 시술 현황 · 채팅 목록이 뜬다 · iOS `flutter build ios --no-codesign` 통과
   - Non-Goals = iOS 변경 · Dart 동작 변경 · FCM · Play Console · 서명 keystore · Android 배포 · 정식 앱 Android id · 서버 변경
4. **승인 receipt 는 적용하지 마라** — 승인은 사용자 몫. plan_digest 와 승인 대기 상태를 보고한다.

## 7. 범위 제약 — 하지 말 것

- 코드 워크트리 수정 금지 · 커밋 · push · PR 금지.
- 키 · 토큰 · 계정 이메일 · Team ID · 서버 IP 금지. 화면 문구 발명 금지.
- 사용자가 정하지 않은 것(정식 앱 id · 배포 방식 · keystore 보관 · FCM 도입 · 세션 보관 방식 확정)을 [확정]으로 쓰지 마라.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/spec-report.md` (전수조사 표 · 변경 파일:줄 · 닫은 미결 / 남은 미결 · Issue 번호 · URL · 라벨 · risk · digest · baseline · 정할 것)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_8e0ca63c-29ac-420f-ac99-dbde1f5f2c96 --from term_e9f03e6f-b6e0-4532-ad16-d6e966b1ff58 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_8e0ca63c-29ac-420f-ac99-dbde1f5f2c96 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_8e0ca63c-29ac-420f-ac99-dbde1f5f2c96 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
