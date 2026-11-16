# [planner] 3회차 — 범위 확장: 개발 앱 Play 내부 테스트 업로드

1·2회차 planner 와 같은 역할이다. 맥락이 없으면 이 폴더(`/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/`)의 `android-app-spec-brief.md` · `spec-report.md` · `spec-2-report.md` · `review-doc-2-report.md` 를 읽어라.

워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/android-app-spec` — **2회차 변경은 커밋 `cb14f570` 으로 올라가 PR mediness#940(미머지)에 있다.** 그 위에 이어서 고친다(미커밋으로 남겨라 — 코디가 같은 PR 에 커밋한다). allowed_paths `products/day/` · 커밋 · push · PR · Delivery · receipt 금지는 그대로.

## 사용자 결정 (2026-11-13 · 새로 정해짐)

| 항목 | 결정 |
|---|---|
| 범위 확장 | **올릴 수 있으면 Play 에 올린다** — 회사(조직) 명의 Play Console 권한 받음(사용자) |
| 올릴 앱 | **개발 앱 먼저** — `day.medisolveai.dev` · `DAY Dev` → Play **내부 테스트 트랙**. iOS 개발판 TestFlight 와 같은 자리. **정식 앱 Android id · 정식 배포 방식은 [미결] 그대로**(다음 작업) |
| 서명 | **Play 앱 서명(Play App Signing)** — 앱 서명 키는 Google 이 보관 · **업로드 키는 로컬 `~/.config/day/android/`**(저장소 밖 · 600). 업로드 키 백업 위치는 사용자가 아직 안 정함 → [미결] |
| 업로드 수단 | Google Play Developer API(서비스 계정 JSON · `~/.config/day/android/`). 새 앱의 첫 빌드는 Play Console 화면에서 손으로(사용자) — API 는 그 뒤부터 |
| 그대로 | FCM(푸시)는 다음 작업 · 개발 앱 로컬 실행 · 통역 범위 안 · `day/video` 스텁 · iOS 무변경 |

## 고칠 것

1. **mobile-deployment** — 결정을 반영하되 **닫히는 만큼만**:
   - M-3(Android 배포 방식): 개발 앱 = Play 내부 테스트만 닫음 · 정식 앱 배포 방식(내부 테스트 / 비공개 앱 / 기타 — M-1 관련)은 [미결]. 회사 Google 계정은 「있음(Play Console 권한 · 사용자 2026-11-13)」.
   - M-11(keystore): Play 앱 서명 · 업로드 키 로컬 보관 닫음 · 백업 위치 · 담당은 [미결]. dev/prod 키 분리는 정식 앱 때.
   - M-12(CI 서명 · 비밀 저장): 업로드 = 로컬 + API 서비스 계정 키가 로컬에 있다는 사실만 · CI 는 [미결].
   - M-17: 「착수 = 로컬 실행만」 → 「개발 앱 로컬 실행 + Play 내부 테스트」. 정식 출시 여부 · 시점은 [미결].
   - §7(7-0 · 7-1 · 7-2 · 7-3) · §9 표 · §12 · §1 · §1-1 에 반영. 값(계정 이메일 · 키 · 서비스 계정 이름 · 개발자 계정 id)은 쓰지 마라 — 경로 · 칸 이름만.
2. **Play 내부 테스트에 필요한 조건을 공식 문서로 확인해 적어라**(확인일 · 링크를 §14 표에): 내부 테스트 첫 출시 심사 여부 · targetSdk 최소 요구(지금 시점 값) · 앱 콘텐츠 선언(데이터 보안 · 개인정보처리방침 URL 등)이 내부 테스트에도 필요한지 · AAB 필수 · 첫 업로드 수동 · 테스터 초대 방식(이메일 목록 · 최대 100). 확인 못 한 것은 「확인 안 됨」. 사용자가 Play Console 에서 손으로 할 일 목록을 따로 적는다(앱 만들기 · 첫 AAB · 앱 서명 등록 · 테스터 · 서비스 계정 초대).
3. **SPEC-003 개정 ⑭(머지 전이라 같은 개정 안 「2026-11-13 보강」)** — §1 범위 표 · Android 절 · 범위 밖 줄을 「Play 내부 테스트까지」로. 인수 조건: A-48(로컬 에뮬레이터)은 그대로 두고, **새 A(Play 내부 테스트)** — 내부 테스트 트랙에 개발 앱 빌드가 올라가 처리 완료 · 테스터 기기(실기기 또는 Play 가 있는 에뮬레이터)에서 Play 로 설치 → dev 로그인 → 시술 현황이 뜸. 실기기 유무는 모른다 — 「테스터 기기」로만 적고 정할 것에.
4. 20-spec.md · spec-004 · spec-005 의 Android 줄을 다시 전수조사(`grep -rn -i "android\|play\|fcm\|keystore" products/day/`)해 사실이 바뀐 곳만 고친다. 표로 리포트에.
5. lint `--strict` products/day ERROR 0.

## 하지 말 것

- 정식 앱 id · 정식 배포 방식 · FCM · 업로드 키 백업 위치를 [확정]으로 쓰지 마라.
- 계정 이메일 · 키 · 서비스 계정 · 개발자 id 값 금지. 화면 문구 발명 금지.
- Delivery v2 는 아직 하지 마라 — 스펙 PR 머지 뒤 코디가 따로 발주한다. 대신 **v2 에 넣을 변경 목록을 2회차 §4 + 리뷰 2 R-1~R-4 + 이번 Play 범위까지 합쳐** 리포트에 적어 둔다(code_surface · phase · verification · dependencies(사용자 수동 단계 · 서비스 계정 키 · dev 서버 통역 D-3) 포함). risk 를 다시 판단해라(외부 쓰기 = Play 업로드가 생김).

## 산출물

- 리포트 `spec-3-report.md`(같은 폴더) — 변경 파일:줄 · 전수조사 표 · 공식 문서 확인 표 · 사용자 수동 단계 · 닫은/남은 미결 · v2 목록 · lint · 정할 것
- 완료 보고는 1회차 브리프 §9 두 명령(새 dispatch preamble 의 taskId · dispatchId).
