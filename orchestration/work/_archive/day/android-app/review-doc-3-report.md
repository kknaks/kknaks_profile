# 리뷰 리포트 — android-app / doc 3회차 · Play 내부 테스트 범위 확장 (2026-11-13)

검수 대상: 워크트리 `android-app-spec` 미커밋 변경(커밋 `cb14f570` 뒤 · `products/day/` 5파일) + `spec-3-report.md`.
기준: `spec-3-instructions.md` 「사용자 결정」 표(2026-11-13). 리포 파일 수정 0.

## 판정: WARN (FAIL 0 · WARN 3 · 권고 5)

결정 표와 어긋나 [미결]이 [확정]으로 오른 곳은 0이다(정식 앱 id · 정식 배포 방식 · FCM · 업로드 키 백업 위치 · CI · minSdk 모두 그대로). M-3 · M-11 · M-12 · M-17 은 정한 만큼만 닫혔고 §13 표와 본문이 같은 말이다. 공식 문서 표본 6개는 모두 문서와 맞았다. 값(이메일 · 키 · 서비스 계정 · 개발자 id) 0, lint products/day ERROR 0. WARN 은 낡은 줄 하나(§3 표 「Google 쪽 등록 없음」), 사용자 손 단계에서 빠진 「코드 작업이 AAB 를 만든다」 고리, 그리고 같은 기기에 로컬 빌드와 Play 빌드를 함께 깔 수 없다는 점이 스펙에 없는 것이다.

## 축별 결과

| # | 축 | 결과 |
|---|---|---|
| 1 | 결정 표 일치 | **PASS(WARN 1)** — 아래 표. 낡은 줄 W-1 |
| 2 | M-3 · M-11 · M-12 · M-17 닫힘 | **PASS** — 아래 표 |
| 3 | §7-3-1 공식 문서 | **PASS** — 표본 6개 직접 확인 · 「확인 안 됨」 표기 정직. 보충 권고 R-1 |
| 4 | §7-3-2 사용자 손 단계 | **WARN** — W-2(AAB 만드는 고리 빠짐) |
| 5 | A-49 | **PASS(WARN 1)** — 확인 가능 · 문구 발명 0. W-3(서명이 달라 같은 기기에 함께 못 깜) |
| 6 | 값 0 · 전수조사 | **PASS** — 값 0. 전수조사 누락 = W-1 하나 |
| 7 | v2 목록 · L3 | **동의** — 고칠 점 R-3 · R-4 |
| 8 | lint | **PASS** — `--strict` exit 0 · `0 error, 263 warning` · products/day 0줄 |

### 1. 결정 표 ↔ 스펙

| 결정 | 스펙 | 판정 |
|---|---|---|
| Play 에 올린다 · 조직 Play Console 권한 | mobile-deployment :40 · :64 · :209 | 같음(값 안 적음) |
| 개발 앱만 내부 테스트 · 정식 id · 정식 배포 [미결] | :192 · :229 · :230 · M-3 :367 · M-4 :368 · spec-003 :95 · :108 | 같음 |
| Play 앱 서명 · 업로드 키 로컬 600 · 백업 [미결] | :215-217 · M-11 :375 · §9 :308 | 같음 |
| API 업로드(서비스 계정 JSON 로컬) · 첫 빌드 손 | :216 · :243 · :255-259 · M-12 :376 · spec-003 :575 | 같음 |
| 그대로: FCM 다음 · 로컬 실행 · 통역 · video 스텁 · iOS 무변경 | :275 · M-9 :373 · :191 · :193 · :194 | 같음 |

[미결]→[확정] 0: 정식 앱 id(:108 · M-4) · 정식 배포(:230 · M-3) · FCM(:274-275 · M-9) · 업로드 키 백업(:217 · M-11) · CI(M-12 · :205) · minSdk(M-7 :371) 모두 열린 그대로. targetSdk 36 은 「Play 요구 · 결정 아님」으로 적혔다(spec-3-report §5 · 스펙 :240) — 맞다.

### 2. 닫힘 범위 — §13 ↔ 본문

| M | §13 | 본문 | 같은 말 |
|---|---|---|---|
| M-3 | 개발 앱 = 내부 테스트 · 계정 있음 닫음 · 정식 배포 남음(:367) | §1 :40 · §7-1 :209 · §7-3 :229-230 · §9 :307 · §12 :359 | 예 |
| M-11 | 보관 = Play 앱 서명 + 로컬 업로드 키 닫음 · 백업 · 담당 · dev/prod 분리 남음(:375) | §7-2 :215-217 · §9 :308 · §7-0 :205 | 예 |
| M-12 | 닫지 않음 · 지금 로컬이라는 사실만 · CI 남음(:376) | §7-0 :205 · §12 :359 | 예 |
| M-17 | 착수 = 로컬 + 내부 테스트 · 정식 출시 남음(:381) | §1 :39 · §1-1 :64 · §7 :187 · §7-0 :189-192 | 예 |

### 3. §7-3-1 공식 문서 — 직접 열어 대조 (2026-11-13 · 영어판)

| 스펙 줄 | 문서 원문(발췌) | 판정 |
|---|---|---|
| :238 첫 출시 · 「might not」 · :244 100명 · 이메일 · 참여 링크 (answer/9845334) | 「First-time app uploads are available immediately to internal testers」 · 「Internal tests might not be subject to standard Play policy or security reviews」 · 「up to 100 testers per app」 · 「create a list of internal testers by email address」 · 「The opt-in link displays only when an app status is 'Published'」. Google 그룹은 **비공개 테스트** 절에만 나옴 | 맞음 · 「그룹 = 확인 안 됨」 정직 |
| :240 targetSdk (answer/11926878) | 「New apps and app updates must target Android 16 (API level 36) or higher」 · 「Starting August 31, 2026」 · 연장 「November 1, 2026」. 트랙 언급 없음 | 맞음 · 「트랙 적용 확인 안 됨」 정직 |
| :241 데이터 보안 (answer/10787469) | 「Apps that are exclusively active on this track do not need to complete the Data safety form」(내부 테스트 절) | 맞음 |
| :243 첫 업로드 손 (android-publisher/edits) | 「only use this API to make changes to an existing app (that has at least one APK uploaded)」 · 「upload at least one APK through the Play Console」 | 맞음 — 문서는 「APK」라고 씀(AAB 를 따로 말하지 않음) · 스펙 「빌드」 표현은 무리 없음 |
| :245 Play 앱 서명 (answer/9842756) | 업로드 키 분실 시 「Request upload key reset」. 기본 등록 문장은 이제 「automatically enrolled in quantum-ready, hybrid signing with Google-generated keys」 | 맞음 · 기본 등록 방식의 이름이 바뀜(R-1) |
| :246 서비스 계정 (android-publisher/getting_started) | Cloud 프로젝트 → API 켜기 → 서비스 계정 → Users & Permissions 「Invite new users」 · 「You no longer need to link your developer account to a Google Cloud Project」 · 출시 권한 이름 없음 | 맞음 · 「권한 이름 확인 안 됨」 정직 |

「확인 안 됨」을 확인된 것처럼 쓴 곳 **0**. 앱 콘텐츠(:242) · 12명 14일 조직 예외(:247)는 열지 않았다(planner 가 「확인 안 됨」으로 둔 줄이라 더 강하게 쓴 곳이 아님).

## FAIL

없음.

## WARN

### W-1. mobile-deployment :107 §3 표 — 「Google 쪽 등록 없음」이 이번 결정과 반대다
- 위치: `products/day/40-architecture/mobile-deployment.md:107` dev 행 「Android **[확정]** `day.medisolveai.dev`(사용자 2026-11-12 · 로컬 실행용 · **Google 쪽 등록 없음**)」.
- 근거: 결정 「올릴 앱 = 개발 앱 → Play 내부 테스트」 · 같은 문서 :191 은 「Google 쪽 등록은 하지 않는다」를 취소선으로 지웠다. :107 만 그대로라 두 줄이 다르다. spec-3-report §1 변경 표 · §2 전수조사 표에도 이 줄이 없다(grep 어휘 「android」에는 걸렸지만 mobile-deployment 는 「§1 에서 전부 다뤘다」로 넘김).
- 고칠 방향: 「로컬 실행 · Play 내부 테스트(2026-11-13) — Play 에 이 패키지로 올리면 바꿀 수 없음」. 이 줄은 :103 「한 번 등록 · 배포하면 사실상 바꿀 수 없다」와도 이어진다.

### W-2. §7-3-2 손 단계 — 2와 3 사이에 「코드 작업이 첫 AAB 를 만든다」가 없다
- 위치: mobile-deployment :255-256.
- 순서 자체는 맞다: 업로드 키(2) → 첫 AAB 손 업로드(3) → 앱 콘텐츠(4) → 테스터 · 게시(5) → 서비스 계정 · 둘째 빌드부터 API(6). 업로드 키가 첫 AAB 보다 먼저이고, 앱 서명은 첫 업로드 때 기본으로 등록된다(문서: 「automatically enrolled」) — 시점 맞음.
- 빠진 것: 3의 「첫 AAB(업로드 키로 서명)」를 **누가 · 무엇으로** 만드는지. 코드 작업이 release AAB(targetSdk 36 · versionCode · 업로드 키 서명)를 만들어 사용자에게 넘겨야 3이 된다. 머리말 :252 「코드 작업이 대신할 수 없는 단계」라 코드 단계를 일부러 뺐겠지만, 그 고리가 없으면 사용자는 3에서 AAB 를 어디서 받는지 모른다.
- 함께 적을 만한 것(문서 근거): 참여 링크는 출시가 「Published」일 때만 보이고 첫 게시 뒤 **몇 시간** 걸릴 수 있다(answer/9845334 「the test link can take several hours to become available」). A-49 를 확인하는 사람이 「안 된다」로 오판하지 않게.
- 고칠 방향: 2와 3 사이에 「(코드 작업) 업로드 키로 서명한 release AAB 를 만들어 넘긴다 — §7-0 · Delivery」 한 줄 · 5 끝에 「링크는 게시 뒤 몇 시간 걸릴 수 있다」.

### W-3. A-49 · A-48 — 같은 기기에 로컬 빌드와 Play 빌드를 함께 깔 수 없다
- 근거: Play 앱 서명이면 Play 로 받는 앱은 **Google 의 앱 서명 키**로 서명된다(:215 · 문서 answer/9842756). 로컬 에뮬레이터 빌드(A-48 — debug 키)와 Application ID 가 같고(`day.medisolveai.dev` · spec-003 :565 「같은 앱」) 서명이 다르므로, A-48 을 본 에뮬레이터에 A-49 를 Play 로 깔려면 로컬 빌드를 **지워야** 한다(세션 묶음도 같이 지워짐). spec-003 :565 · :575 「같은 앱 · 같은 채널 동작」은 맞지만 이 점이 없다.
- A-49 확인 가능성: 사용자 몫 「테스터 기기」로 적힌 것은 맞다. 에뮬레이터로 본다면 **Google Play 시스템 이미지**여야 하고, 테스터 목록에 넣은 Google 계정으로 그 기기의 Play 에 로그인해야 한다. 인수인계에 적힌 AVD(`Medium_Phone_API_36.1` · `mediness_api36`)가 Play 이미지인지 확인 안 됨.
- 겹침: A-49 는 설치 경로(Play)만 보고 로그인 → 시술 현황으로 끝난다. 통역 · 자동 로그인은 A-48 이 맡는다 — 겹침 없음 · 빠짐 없음(같은 빌드라). 화면 문구 발명 0(시술 현황 · 참여 링크는 기존 이름 · Play 용어).
- 고칠 방향: spec-003 :575 에 「로컬 빌드와 Play 빌드는 서명이 달라 한 기기에 함께 깔 수 없다 — 바꿀 때 지우고 깐다」 한 줄. A-49 확인 칸 · 정할 것에 「Play 이미지 에뮬레이터면 테스터 계정 로그인」.

## 권고 (스펙 필수 아님 · v2 · 코드 브리프)

- **R-1** :245 · :409 「새 AAB 앱은 기본으로 Play 앱 서명에 등록」 — 지금 문서는 「quantum-ready, hybrid signing with Google-generated keys」로 부른다. 뜻(앱 서명 키 = Google · 업로드 키 = 개발자)은 같다. 다음 확인 때 이름만 맞추면 된다.
- **R-2** 데이터 보안(:241) — 문서 본문에 그 문장이 있다. 다만 Play Console 이 게시 전에 무엇을 막는지는 실물에서만 안다(:242 「확인 안 됨」과 같은 이유). 손 단계 4에서 막히면 그대로 사용자 판단으로.
- **R-3 v2 phase 순서** — spec-3-report §6 phases 는 AND-5(release AAB · 업로드 키 서명) → AND-6(사용자 손 단계 1~6)인데, AND-5 는 손 단계 **2(업로드 키)** 가 먼저 있어야 한다(dependencies ② 도 그렇게 적음). AND-6 을 「손 단계 1–2(앱 만들기 · 업로드 키)」 → AND-5 → 「손 단계 3–6」으로 나누면 순서와 의존이 같아진다. 또 A6 「둘째 빌드」는 versionCode 가 첫 빌드보다 커야 올라간다 — verification 에 한 줄.
- **R-4 「올릴 수 있으면」** — 결정 원문은 조건부(「올릴 수 있으면 Play 에 올린다」)인데 v2 A6 은 완료 조건이다. Play 쪽이 사용자 손 단계 · 앱 콘텐츠 요구로 막혀도 코드 PR(A1~A5)을 먼저 머지할지, A6 까지 묶을지 v2 에 적는다(사용자 판단 U-1).
- **R-5 L3 상향** — 동의. `rules/delivery-workflow.md:60` 「`L3` = destructive · production · **external write** · merge/deploy …」 — Play 업로드는 외부 쓰기다. 패키지명이 그 Play 에 한 번 올라가면 다시 쓸 수 없다는 근거는 planner 도 「일반 지식 · 확인 안 됨」으로 적었고 나도 이번에 문서로 확인하지 않았다 — L3 근거는 「외부 쓰기」 하나로 충분하다. 같은 key 사용 권장도 동의(v1 대체).

## v2 목록(spec-3-report §6)에 대한 의견

- target_specs · Target Delta 3묶음 · A1~A6 · 저장소 비밀 0 · Non-Goals(R-3 ① · ② 반영) · code_surface(`.gitignore` · `key.properties` · `app/.metadata`) · dependencies ①~⑤ · rollback — 리뷰 1 · 2 지적이 모두 들어갔다. 동의.
- 더할 것: R-3(phase 순서 · versionCode) · R-4(조건부 범위) · W-3(서명 다른 빌드 공존 불가 — verification 에 「A6 전에 로컬 빌드 지움」).

## 조용히 통과하는 자리

- **업로드 스크립트 증명** — 스펙 A-49 는 첫 빌드(손)만 본다. 결정 「업로드 = API」는 v2 A6 「둘째 빌드 API → 테스터 기기 업데이트」에만 있다. v2 에서 A6 의 둘째 빌드를 빼면 API 업로드가 한 번도 증명되지 않은 채 통과한다.
- **저장소 비밀 0** — `~/.config/day/android/` 경로를 빌드 설정이 읽게 하면 경로 문자열은 저장소에 들어간다(값 아님 · 괜찮음). 반대로 `key.properties` 를 저장소 안에 만들고 gitignore 만 믿으면 실수 한 번에 들어간다 — v2 「`git grep` · gitignore 확인」이 그 자리.

## 직원 · 사용자가 실물에서 만날 자리

- 에뮬레이터에서 A-48(로컬) → A-49(Play)로 넘어가면 앱을 지우고 다시 깔아야 하고 다시 로그인한다(W-3).
- 참여 링크가 게시 직후엔 안 열릴 수 있다(몇 시간 — W-2).
- 테스터는 테스터 목록에 넣은 Google 계정으로 Play 에 로그인돼 있어야 받는다.

## 사용자 판단이 필요한 것

- **U-1** Play 단계(A6)가 막혀도 코드 PR(A1~A5)을 먼저 머지할지(R-4).
- **U-2** A-49 를 실기기로 볼지, Google Play 시스템 이미지 에뮬레이터로 볼지(+ 테스터 계정 로그인) — planner 「정할 것」과 같음.
- **U-3** 업로드 키 백업 위치 · 담당(M-11) — 그대로 사용자 몫.

## 참고

- 값 검사: `git diff products/day` 추가 줄에서 이메일 · `.json` 키 파일 이름 · `.jks` · `.keystore` 파일 · 15자리 이상 숫자 · PEM 머리 0건. 경로 `~/.config/day/android/` 만 있음 — iOS 쪽 `~/.config/day/apple/`(60-release :63)와 같은 방식이라는 :216 말도 맞음.
- 전수조사(`grep -rn -i "android\|play\|fcm\|keystore" products/day/` · display · player 류 제외): mobile-deployment · spec-003 밖은 20-spec.md :41 · spec-004 :38 · :78 · :452 · spec-005 :68 · 40-architecture/README.md :22 — planner 표와 같음. 누락은 mobile-deployment :107(W-1)뿐.
- mobile-deployment §7-4(개발자 인증 · :265-267) · M-15 — Play 로 배포하는 앱은 Play Console 로 인증한다는 기존 줄과 어긋나지 않는다. 그대로.
- log.md :17 새 행 PR 칸 모양 — 1 · 2회차와 같음.
