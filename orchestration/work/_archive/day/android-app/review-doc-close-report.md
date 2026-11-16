# 리뷰 리포트 — android-app / doc 마감 · spec-sync · Delivery #251 마감 sync (2026-11-16)

대상: 워크트리 `android-app-spec` 브랜치 `kknaksss/android-app-close` 미커밋 7파일(+79 / −57) · `spec-close-report.md`. 코드 대조 = CENTURION_DAY `4f8316a7`(#253 squash · MERGED 확인). 리포 수정 0.

## 판정: WARN (FAIL 0 · WARN 3 · 참고 5)

사실은 거의 다 맞다. 코드 · 리포트 · 결정 표와 대조해 틀린 값은 없다. WARN 3건은 모두 **말을 정직하게 고르는 문제**다. 결정의 범위를 바꿔 읽은 곳 하나, 누가 했는지가 틀린 곳 하나, 추정을 사실처럼 적은 곳 하나다. 셋 다 한 줄 고치면 된다.

---

## 1. 사실 대조 (브리프 §1)

| 항목 | 스펙 줄 | 근거 | 판정 |
|---|---|---|---|
| 정식 앱 id · 이름 · 서버 | `mobile-deployment.md:24` ① · `:51` · `:113`~`:114` · `:116`~`:117` · spec-003 `:100` · `:580` | `_RESUME.md` §2 2026-11-13 「정식 Android 앱 = day.medisolveai · DAY · prod」 · app-4 `--dart-define` 진입점 prod · 허용 prod+dev | 맞음 |
| 프로덕션 출시 진행 | `:24` ① · `:41` · `:68` · `:211`~`:212` · `:240` · `:395` M-17 | §2 2026-11-15 · §5 2026-11-15 「프로덕션 vc3 심사 제출 · 대한민국 · 관리형 게시 꺼짐」 | 맞음 · 단 W-1 |
| 트랙 이력(vc1 · vc3 · 날짜) | `:68` | §5: 개발 internal vc1 11-13 손 → vc3 11-14 API · 정식 alpha vc1 11-14 21:52 출시 → vc3 11-15 API → 프로덕션 11-15 | 맞음 |
| 업로드 키 공유 · 위치 · 백업 [미결] | `:67` · `:223`~`:225` · `:321` · `:389` M-11 | §2 11-13 「업로드 키 dev 와 공유」 · app-4 `keytool -printcert` 지문 = dev 와 같은 키 | 맞음 |
| 서비스 계정(이름 · 값 없음 · 정책 재정의) | `:69` · `:224` | §5 11-14. 정책 이름 · 키 파일 이름 · 계정 이름은 diff 에 없다(아래 §3) | 맞음 |
| 3단 주입 | `:117` · spec-003 `:580` | 코드 `app/android/app/build.gradle.kts:10-29` 「-P > identity.local.properties > identity.properties」 · `identity.properties` = placeholder `com.example.day.placeholder` · `DAY` | 맞음 |
| release 는 업로드 키 없으면 멈춤 | `:226` | 코드 `build.gradle.kts:83` · `:92` `GradleException` | 맞음 |
| 세션 저장 | `:228` · spec-003 `:561` | 코드 `SessionChannel.kt:61` AES-256-GCM · `:65` `getSharedPreferences(MODE_PRIVATE)` · `:137` `newSingleThreadExecutor` · 매니페스트 `allowBackup=false` · `fullBackupContent=false` · `data_extraction_rules.xml` | 맞음 |
| minSdk 24 · targetSdk · compileSdk 36 | `:218` · spec-003 `:580` | 코드 `build.gradle.kts:62` · `:64` · compileSdk = `flutter.compileSdkVersion`(Flutter 3.44.8) → aapt 결과 compileSdk 36(review-code-1 `:17`) | 맞음 |
| F1 | spec-003 `:124` · `:571` · `mobile-deployment.md:201` | 코드 `theme.dart` `paneReservesBottomInset`(= Android) · `listEndInset` · `chat_room_screen` · `board_screen` · `chart_sheet` · `shell` — 「태블릿 채팅 칸 입력줄 · 판 · 설정 · 폰 차트 시트 목록 끝 · iOS 0」과 같다 | 맞음 |
| `play_upload.py` 짝 | `:271` · spec-003 `:581` · `:390` M-12 | 코드 `play_upload.py:38` `UPLOAD_TRACKS = {dev: internal, 정식: alpha}` · `:156-161` 그 밖은 멈춤 · `--dry-run` = validate | 맞음 |
| 콘텐츠 선언 「했다」 | `:251`~`:252` · `:272` 7 | §5 11-14 「앱 콘텐츠 11/11 · 18+ · 광고 없음 · 데이터 보안 · 사진 · 동영상 권한 신고」 · 정식 vc1 이 게시됐으므로 「통과」도 맞음 | 맞음 |
| A-48 · A-49 | spec-003 `:928` · `:929` | app-1 `:92` 「에뮬레이터: 권한 · 드로어 · 듣는 중 · 칩 TTS PASS · 음성 입력 = 실기기로」 · §2 11-13 · §5 | 맞음 · 단 W-3 |

### W-1 — 「최종 배포는 비공개」 결정을 「이 줄은 iOS 다」로 범위를 좁혀 읽었다

- `mobile-deployment.md:43` 의 [확정]은 사용자가 2026-11-11 에 정한 것이다. 「최종 배포는 **비공개**(누구나 검색해 받는 공개 스토어 앱이 아님) · 병원 직원에게만 공유」.
- 이번에 덧붙인 문장은 「이 줄은 iOS 다 — Android 정식은 Play 프로덕션(공개) 트랙」이다.
- 그런데 원래 줄은 iOS 한정이 아니었다. 문서 머리말(`:12`)도 「비공개로 나눠 주려면」이다. 그러니 이건 11-11 결정을 Android 에서는 **뒤집은 것**이다. 처음부터 iOS 만 말한 줄이 아니다.
- 근거가 된 2026-11-15 사용자 말은 「이제 출시 준비도 하면 되나?」다. 「공개」라는 말은 코디가 결정 표(`_RESUME.md` §2)에 기록한 해석이다. 관리형 게시를 꺼 두었기 때문에, 심사를 통과하면 Play 에서 대한민국 누구나 검색해 받을 수 있게 된다.
- **고칠 방향**: 이 줄을 「11-11 결정(비공개)은 iOS 에 남고, Android 정식은 2026-11-15 사용자 결정으로 Play 프로덕션(공개)으로 바뀌었다 — 앱 로그인으로 막는 것은 같다」로 적는다. 뒤집힌 결정은 지우지 말고 바뀐 날짜와 사유를 남기는 규칙(`_RESUME.md` §2 끝)에 맞춘다.
- 심사가 끝나기 전에 사용자에게 「Play 에서 누구나 검색해 받을 수 있게 되는 것」을 한 번 확인받을지는 코디가 판단할 일이다. 고객 약속에 닿는 변경이라 `10-decision.md` 감인지도 함께 본다(참고 R-5).

### W-2 — §7-3-2 「1 ~ 6 은 사용자가 했다」에 업로드 키 만들기가 들어 있다

- `mobile-deployment.md:262` 머리말은 「코드 작업이 대신할 수 없는 단계 … **1 ~ 6 은 개발 앱에서 했다**(사용자 2026-11-13 ~ 14)」다.
- 그런데 2(`:265` 「업로드 키 만들기 · 보관」)는 코드 워커가 keytool 로 만들었다. 근거는 `app-3-report.md` 「업로드 키」 절(`~/.config/day/android/upload-keystore.jks` 생성 · JDK 17 keytool)과 `_RESUME.md` §2 2026-11-13 「업로드 키 = 코드 워커가 keytool 로」다.
- review-doc-4 참고 1 과 같은 자리다. 이번에 「했다(사용자)」가 붙으면서 이제는 사실과 어긋난다.
- **고칠 방향**: 2 에 「(코드 워커가 keytool 로 만들었다 · 2026-11-13 · 백업은 사용자 [미결])」 한 줄을 넣는다. 또는 머리말을 「1 · 3 ~ 6 은 사용자 · 2 는 코드 워커」로 고친다.

### W-3 — 통역 음성 입력 「실기기 확인」은 사용자 말을 코디가 해석한 것이다

- `_RESUME.md` §2 2026-11-13 의 기록은 「실기기(Z Fold3) 확인 끝 — 「확인했어」(**통역 음성 입력 포함으로 봄**)」이다.
- 사용자가 음성 입력을 따로 짚어 확인했다는 기록은 없다. 「포함으로 봄」은 코디의 해석이다.
- 그런데 아래 세 곳은 이걸 확인된 사실로 적었다.
  - spec-003 `:928` A-48 「말하기 → 자막 · 번역 음성 = **실기기** … 사용자 Galaxy Z Fold3 확인 2026-11-13」
  - spec-003 `:68` ⑤
  - spec-close-report B Acceptance A5 「실기기에서 확인(사용자 「확인했어」 11-13)」 · 댓글 초안 A5 행 · log.md `:17`
- A5 는 Acceptance 에서 실물 확인이 가장 약한 칸이다. 에뮬레이터에서는 음성 입력이 안 됐고, 실기기 근거는 이 한 마디뿐이다.
- **고칠 방향**: 둘 중 하나를 고른다.
  - (a) 사용자에게 「통역에서 말하기 → 자막 → 번역 음성까지 실기기에서 봤나」를 한 번 묻고, 답을 그대로 적는다.
  - (b) 「사용자 「확인했어」(11-13 · 통역 음성 입력 포함으로 봄)」처럼 해석이라는 것이 드러나게 적는다.
- 브리프 §8 「통역 음성 입력은 실기기에서 확인됨」이 코디 판단이라면 (b) 로 충분하다.

---

## 2. 누락 — grep 직접 전수 (브리프 §2)

`grep -rn -i "android\|play\|aab\|keystore\|업로드 키\|day.medisolveai\|\[미결\]" products/day/`(archive · log · `display*` 제외) → mobile-deployment 133 · spec-003 23 · deployment.md 9 · 60-release 8 · spec-004 4 · 20-spec · 30-work · README · spec-005 각 1.

- **spec-003 23줄**: 모두 개정 ⑯ 사실과 맞다. `:598` 「Android 개발 앱(개정 ⑭): 푸시 없음」은 개발 앱만 말하지만, 정식 앱도 푸시가 없다는 것은 `:100` · `:113` 에 있어 모순은 없다.
- **spec-004 · spec-005 · 20-spec · 40-architecture/README**: 낡은 줄 0. spec-005 `:68` 「FCM 미결 그대로」는 사실이다.
- **deployment.md · 60-release**: 걸린 줄은 전부 `day.medisolveai.com` 도메인 · iOS 다. Android 줄은 0.
- **mobile-deployment 남은 「아직 · 안 함 · 범위 밖」 줄**(`grep 아직\|하지 않는다\|안 함\|범위 밖`): 남은 것은 모두 취소선 · iOS · 이력(`:18` · `:20` 개정 노트) · FCM · 푸시다. 정식 앱 · 프로덕션을 「안 한다」고 남긴 줄은 0.
- **낡은 줄 = W-2 한 곳**(§7-3-2 · 2). 그 밖에 planner 전수 표에서 빠진 낡은 줄은 찾지 못했다.

## 3. 과잉 (브리프 §3)

- **[미결] → [확정] 0** — diff 에서 새로 생긴 [확정]은 다섯 곳이다. `:41` 정식 앱 Play 출시 · `:225` · `:321` 같은 업로드 키 · `:240` 정식 배포 방식 · `:321` prod 칸 「같음」. 모두 `_RESUME.md` §2 의 사용자 결정(11-13 · 11-15)이다.
- 구현으로 생긴 사실(세션 · 주입 · minSdk · 스크립트)은 「코드 작업이 정함」 · [설정 완료]로 적었다. [확정]으로 올린 곳은 없다.
- **범위 밖 · [미결] 그대로** — FCM(M-9) · 동영상 보내기 · 알림 [수락] Android 판 · 업로드 키 백업(M-11) · CI(M-12) · 빌드 번호(M-13). KOS 세션 14시간은 diff 에 언급 0 이라 손대지 않았다.
- **값 0** — diff 추가 줄에서 grep 했다. `@` · `iam.` · `gserviceaccount` · `.json` · `.jks` · 12자리 이상 숫자 · `BEGIN ` · password · 정책 이름 · 개발자 id 모두 0건이다. 서비스 계정 키 파일 이름(`play-service-account.json`)과 조직 정책 이름도 스펙에는 안 들어갔다.
- **화면 문구 발명 0** — 추가 줄의 「」 인용은 기존 문구 · 사용자 말 · 기존 기능 이름(「채팅 최근 사진 줄」)뿐이다. F1 줄은 레이아웃 사실만 적었다.

## 4. Delivery 마감 sync (브리프 §4)

- **#936 꼴과 같음** — `gh pr view 936`(merge `fe639680`)을 대조했다.
  - `30-work.md` Spec Coverage 칸에 이슈 링크를 덧붙이는 방식이 같다(`:46` · `:47`).
  - Delivery 대시보드 행의 열 순서가 같다(`… | spec-baseline:ready | closed | implementation:conformant | spec-sync:pending`).
  - 행 제목은 Issue #251 실제 title 과 글자까지 같다(`gh issue view 251`).
  - `log.md` `wp-status` 행 꼴도 같다.
  - #936 은 log 행이 하나였다. 이번에 spec-sync 행이 하나 더 있는 것은 문서 변경이 같이 있어서 맞다.
- **conformant 근거** — Delivery v2 `android.v2.request.json` `acceptance` 는 **A1 ~ A7** 이다. 브리프 §B 의 「A1~A6」은 잘못 적은 것이고, planner 가 A1 ~ A7 로 대조한 것이 맞다.
  - Target Delta 10행 · Acceptance 7행 모두 근거(리포트 · 코드 · 사용자)가 붙어 있다.
  - A5 는 조건 문구가 「에뮬레이터 호스트 마이크를 켜고 … 말하기」였다. 사용자 결정으로 실기기로 넘긴 것을 정직하게 적었다. 다만 실기기 근거의 세기는 W-3 이다.
  - A4 는 참고 R-2 다.
- **범위 밖 3건** — F1 · 정식 앱 · 프로덕션을 v2 Non-Goal 과 나란히 「Delivery 뒤 사용자 결정으로 늘어남」 표(spec-close-report B)로 적었다.
  - v2 `non_goals[3]` 「정식 앱(M-4 · Play 정식 앱 등록 · 프로덕션 트랙 · M-3)」과 대조했다. 정식 앱 · 프로덕션은 Non-Goal 을 넘은 것이고, 그렇게 적었다.
  - Issue 마감 댓글 초안에도 「승인 뒤 사용자 결정으로 늘어난 것」 절이 있다. 정직하다.
  - conformant 판정은 「v2 계약은 다 지켰고, 그 밖에 더 들어갔다」는 뜻이다. Scope Delta v3 를 남길지는 planner 가 코디에게 넘겼다. 맞는 처리다.

## 5. lint (브리프 §5)

`python3 scripts/lint-pipeline.py --strict` → exit 0 · `0 error, 263 warning` · `products/day` 걸린 줄 0.

---

## 참고 (지적 아님 · 코디 판단)

- **R-1** `log.md:18` spec-change 행의 PR 칸이 「근거 코디 … (PR 전 · 코디가 PR)」다. `document-pipeline.md` §log 는 PR 칸에 `#NNN` 또는 닿는 링크를 적게 한다. 코디가 PR 을 열 때 mediness PR 번호로 바꾼다. 같은 PR 커밋 안에서 고치면 된다.
- **R-2** A4 조건은 「바꿨다면 코디 확인 기록을 **PR 에** 남김」이다. #253 본문에는 F1 Dart 변경 설명과 iOS 픽셀 동일 기록은 있다(§5 · 리뷰 포커스 1). 하지만 「사용자 · 코디가 Dart 변경을 OK 했다」는 문장은 없다. 확인 기록은 `e2e-feedback.md` · `_RESUME.md` 에만 있다. Issue 마감 댓글 초안 A4 행 「하단 시스템 영역 수정(사용자 OK)」이 그 기록을 대신한다. 그래서 댓글을 게시하면 메워진다.
- **R-3** `30-work.md:73` 대시보드 행은 `closed` 다. 실제 Issue #251 은 아직 OPEN 이다(라벨 `execution-plan:ready` · `delivery-plan:approved` · `spec-baseline:ready`). #936 처럼 머지 뒤 닫는다는 전제로 적은 것이다. 코디가 이 PR 머지 → 댓글 → 닫기 순서를 지키면 맞는다.
- **R-4** spec-003 `:68` ⑤ · `:928` 의 「에뮬레이터는 맥 호스트 마이크를 받지 못함」은 일반 사실처럼 읽힌다. 근거(app-1 `:92`)는 「이번 맥에서 macOS 가 에뮬레이터 프로세스에 마이크를 주지 않음(호스트 권한)」이다. 「이번 환경에서」 정도로 좁히면 정확하다.
- **R-5** W-1 과 이어진다. 병원 직원용 앱이 Play 대한민국 공개 스토어에 오르는 것은 11-11 「비공개」 약속을 바꾼다. `document-pipeline.md` §의사결정 레벨의 「고객 약속이 바뀜 → 10-decision」에 닿을 수 있다. 사용자가 decision owner 로 직접 정했다면 ESC 없이 log 의 결정 근거로 충분하다. 이번 log 행은 `arch-change, spec-change` 라 결정 근거 칸이 짧다. 이 판단은 코디 몫이다.
