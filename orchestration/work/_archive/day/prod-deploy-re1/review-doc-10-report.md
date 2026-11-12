# 리뷰 리포트 — 마감 문서 sync (2026-11-12)

대상: 스펙 워크트리(`kknaksss/prod-deploy-re1-spec-web` · HEAD `9ddbebeb`)의 미커밋 5파일
- `40-architecture/deployment.md`
- `40-architecture/mobile-deployment.md`
- `60-release/app-store-preparation.md`
- `20-spec/spec-001-login-session.md`
- `log.md`

요약은 `doc-sync-report.md` 를 봤다.

원천(사실)
- `_RESUME.md` §5 2026-11-12 줄 7개
- `mobile-prod-build-2-report.md` · `mobile-dev-build-report.md` · `mobile-asc-apply-report.md` · `mobile-presubmit-report.md` · `be-5-report.md`
- `delivery-web-report.md` 「승인」 절
- 코드 레포 `CENTURION_DAY` 확인(`git fetch` 뒤 `origin/prod` · `origin/dev` · 커밋 내용)

## 판정: WARN

FAIL 은 없다. deployment.md 「prod 첫 배포 절차」의 「지금」 칸은 원천과 하나하나 같다. 커밋 · 브랜치도 코드 레포에서 맞다. 값 · 키 · 계정 이메일 · 테넌트 id · IP · 고객 값은 추가 줄에 없다. 닫은 미결 두 개(KOS IP 제한 · M-20)는 정말 닫혔고, 「구현 전」을 「구현됨」으로 고친 것도 코드와 맞다. 다만 Unlisted 에 관한 사실 세 가지(「웹 양식」 · 「승인 뒤 되돌릴 수 없음」 · 「이후 버전 모두 Unlisted」)는 원천에서 찾을 수 없다(W1).

검증
- `lint-pipeline.py --strict`: exit 0 · 0 error · 263 warning · `products/day` 0건
- diff 추가 줄 검사: 이메일 모양 0 · IP 모양 0 · 테넌트 끝자리 · uuid 모양 0. 숫자 `28` · `92` 같은 히트는 모두 커밋 해시(`382827d5`) 안의 글자였다. 동기화 수치(방 · 직원 · 방문)와 Unlisted 인원수는 옮기지 않았다.

## ① deployment.md 「prod 첫 배포 절차」 ↔ 원천

| # | 문서 「지금」 | 원천 | 판정 |
|---|---|---|---|
| 2 | 채움 · #244 로 들어감(`dev` 머지 `382827d5`) | `382827d5` = `Merge pull request #244`. 그 트리에 `deploy/config/prod.env` 가 있다(값은 보지 않음) | 맞음 |
| 3 | 완료 — #244 dev 일반 머지 `382827d5` · dev 배포 OK(`/privacy` · `/support` 200) | _RESUME §5 「prod 첫 배포 완료」 줄 첫 부분 | 맞음 |
| 4 | 완료 — prod ff `382827d5` · deploy-prod 1차 revision-mismatch(정상) · migrate-prod OK | 같은 줄. `382827d5` 는 `origin/prod` 조상이다 | 맞음 |
| 5 | 완료 — 재실행 OK · `https://day.medisolveai.com` ready · `/privacy` · `/support` · `/login` 200 | 같은 줄 | 맞음 |
| 5-1 | 풀림 — VM 에서 운영 내부 API 200 | _RESUME 「VM 에서 … get-user-account 200 = 내부 API IP 차단 풀림」 | 맞음(테넌트 끝자리 · 계정은 옮기지 않음) |
| 6 | 완료 — prod api 컨테이너 1회 · 「운영 연결 넣음」 · 시스템 계정 dev · prod 통일(값 레포 밖) | 「운영 연결 등록(명동점 · 시스템 … · 「운영 연결 넣음」)」 · 「시스템 계정 dev · prod 모두 … 통일」 | 맞음(이메일 안 옮김). 「prod api 컨테이너에서」는 절차 칸의 지시를 되풀이한 것이다. 원천은 실행 위치를 따로 적지 않았다 — 참고 1 |
| 7 | 첫 동기화 OK — 구역 · 방 · 직원 · 일정 · 오류 0 · OQ-01-3 따로 닫지 않음 | 「동기화 OK(구역 · 방 · 직원 · 오늘 방문 · 오류 0)」 | 맞음. 수치는 일부러 뺐다 |
| 표 아래 #246 | `dev` → `prod` ff `0b2f8cff` | _RESUME 2026-11-12 줄에는 없다. 코드 레포에서는 맞다: `origin/prod` = `0b2f8cff Merge pull request #246`(그 아래 `d8d0910f` R1) · `0b2f8cff` 는 `origin/dev` 조상이다(ff 가능) | 맞음(원천 = 코드 레포) |
| 표 아래 푸시 | dev → DAY Dev · prod → 정식 앱만 · M-20 안 함 | _RESUME 「M-20 안 함(사용자)」. `382827d5` `prod.env` 허용 앱 = 정식 앱 하나 | 맞음 |
| 준비 표 네트워크 · Key Vault | 나가는 IP 확인 · 허용됨(값 안 적음) · 「prod 첫 배포 2026-11-12」 | 위와 같음 | 맞음 |
| 미결 KOS IP 제한 | 닫음 | 5-1 · 7 이 근거다 | 정말 닫힘 |

## ② mobile-deployment.md · ③ 60-release ↔ 원천

| 문장 | 원천 | 판정 |
|---|---|---|
| 정식 DAY 0.1.0 (2) 업로드 · VALID · 0.1.0 버전 연결 | prod-build-2 「VALID · 버전 0.1.0 에 빌드 2 연결」 · presubmit 「빌드 연결 0.1.0 (2) VALID」 | 맞음 |
| DAY Dev 0.1.0 (3) VALID | dev-build 「0.1.0 (3) 업로드 · VALID · 내부 IN_BETA_TESTING」 | 맞음(참고 2 — 문장이 둘을 한데 묶음) |
| 내부 그룹(사용자 추가) | _RESUME 「내부 그룹 medisolveai(사용자 추가)」 · prod-build-2 「이 워커는 만들지 않았다」 | 맞음 |
| 심사 제출 · Unlisted 신청 완료 · 결과 대기 · 블록 A + B(「알림」 뺌) · 출시 수동 | _RESUME 「앱 심사 제출 · Unlisted 신청 완료(사용자) … 메모 블록 A + B(「알림」 뺌) … 승인 뒤 수동 출시」 · asc-apply `releaseType MANUAL` | 맞음 |
| App Privacy 게시 · 무료 · 한국만 · 저작권 · 제3자 콘텐츠 권리 | _RESUME 「App Privacy 게시 7종」 · 「무료 · 한국만 · 2026 Medisolve AI Co., Ltd. · 제3자 콘텐츠 권리 보유」 · asc-apply 가격 0 · presubmit App Privacy 사용자 게시 | 맞음 |
| 연령 12+ | asc-apply `appStoreAgeRating = TWELVE_PLUS`(API 값) | 맞음 — 참고 3 |
| Unlisted 신청서 = 관리 기기 아님(Unmanaged) · 규모(#12 · M-1) | _RESUME Unlisted 양식 「32명 · … · Unmanaged」 | 맞음(인원수는 옮기지 않음). M-1 을 닫지 않은 것도 맞다(개인 폰 / 관리 기기 문항은 사용자 결정으로 남음) |
| **「웹 양식」 · 「승인 뒤 되돌릴 수 없음」 · 「이후 버전 모두 Unlisted」**(mobile-deployment §6 · 60-release §7-2 #11) | _RESUME · 이번 각 리포트 · HEAD 의 60-release · mobile-deployment 어디에도 없다(grep 0 — doc-sync-report 를 빼면) | **원천 없음 → W1** |
| prod 서버 APNs 허용 앱 = 정식 앱 하나(`prod.env`) | `382827d5:deploy/config/prod.env` 의 허용 앱 = 정식 번들 하나 | 맞음 |
| §1-1 · §6 「정식 레코드 아직 없다」 지움 | 60-release §1-3(HEAD)에 정식 앱 record · ASC 앱 id 가 이미 있다 · prod-build-2 「앱 6833456680 · bundleId 일치」 | 맞음 |
| 60-release §1-1 · §5-1 · §7-2 #1 · #6 「/privacy · /support 200」 | _RESUME 「dev · prod `/privacy` · `/support` 200」 | 맞음 |
| §7-2 #3 · #4 · #8 「제출됨」 | _RESUME 제출 줄 · ASC 답안 줄 | 맞음. #4 의 전제(D-1 · 데모 데이터 · 푸시 실물)는 presubmit 이 「워커가 확인하지 않음」으로 남겼다. 사용자가 그대로 제출했다는 사실과는 어긋나지 않는다 — 참고 4 |
| §7-2 #5 「테스트 결과 기록 없음」 · 「발행 가능 여부」 T1 · T3 · T4 · T5 「기록 없음」 | 원천에 결과 없음 | 맞음 — 모르는 것을 지어 넣지 않았다 |

## ④ 「구현 전」 고친 것 · 닫은 미결

- **앱 환경 연결 「구현 전」 → 구현됨**: SPEC-001 §3 제목 · 매트릭스 줄 · 규칙 14 · mobile-deployment §1 · §9-1. `backend/day/services/environments.py` 는 `382827d5` 트리에 있고 `382827d5` 는 `origin/prod` 에 있다. 맞다. 다만 SPEC-001 머리 개정 노트(2026-11-09 「앱 환경 연결」 :35)의 「아직 구현 전이다 — 현행 기능으로 쓰지 않는다」는 남았다 — 참고 5.
- **M-20 닫음(안 함)**: _RESUME 원문 그대로다. §9-1 「푸시」 줄과 [미결] 줄에 취소선을 긋고 [확정]으로 바꿨다. deployment.md · §1-1 · §13 이 같은 말이다. SPEC-003 기기 등록(:582 허용 목록 밖 = 400 · 「앱은 400 을 띄우지 않는다 — 푸시만 없이 앱 사용」)과도 충돌하지 않는다. 정식 앱 데모 세션은 dev 서버 등록이 400 이 되고 푸시 없이 쓰인다. 사용자 「필요 없음」과 같다.
- **KOS IP 제한 닫음**: 위 ① 5-1 · 7.
- **그대로 둔 것**(doc-sync 「그대로 둠」): OQ-01-3 · §6-1 시행일 「(예정)」 · §5-3 메모 글자 · GitHub prod Environment · 실기기 푸시 · §7-2 #9 · #10 · T1 ~ T6. 모두 원천에 결과가 없거나 공개 글자라 손대지 않은 것이 맞다.
- `log.md` 2026-11-12 `arch-change, spec-change` · `DAY-SPEC-001` 1행 · 요약 1줄 — 형식 맞음.

## WARN

### W1. Unlisted 의 성질 세 가지는 원천이 없다
- 위치: `mobile-deployment.md` §6 새 [설정 완료] 줄(:175) 「(… · 웹 양식) … Unlisted 는 승인 뒤 되돌릴 수 없고 이후 버전도 모두 Unlisted 다」 · `60-release` §7-2 #11 「Unlisted = 웹 양식(승인 뒤 되돌릴 수 없음 · 이후 버전 모두 Unlisted)」.
- 근거: _RESUME §5 의 Unlisted 줄은 신청 항목만 적었다(Business · Externally · 인원 · Corporate customers · Healthcare · Unmanaged · 한국). 이번 각 리포트와 HEAD 문서에도 이 세 사실이 없다. doc-sync-report 는 원천을 「_RESUME + 코디 지시」라고 했다. 코디 지시에 있었다면 원천은 그 지시다. 아니라면 Apple 정책을 기억으로 적은 것이다. 「되돌릴 수 없음」은 운영 판단(나중에 공개 배포로 바꿀 수 있는지)에 영향을 주는 주장이라 출처가 필요하다.
- 고칠 것(택1 · 코디): (가) 코디 지시나 Apple 화면 · 문서가 출처면 그 출처를 괄호로 단다(예: 「ASC Unlisted 신청 화면 안내 · 사용자 2026-11-12」). (나) 출처가 없으면 세 구절을 지우고 「Unlisted 신청(사용자 2026-11-12) · 결과 대기」만 남긴다.

## 참고(차단 아님)
1. deployment.md #6 「prod api 컨테이너에서 1회」: 원천은 「운영 연결 등록 … 넣음」까지만 적고 실행 위치는 적지 않았다. 절차상 prod 컨테이너가 맞고, 결과가 `day_prod`(prod 동기화 OK)에 나왔으니 사실과 어긋날 가능성은 낮다. 코디가 알면 그대로 두면 된다.
2. mobile-deployment §1-1 TestFlight 줄 「DAY Dev 0.1.0 (3) · 정식 DAY 0.1.0 (2) 업로드 · VALID · 0.1.0 버전에 연결 · 내부 그룹」은 두 앱을 한 문장에 묶었다. 「버전에 연결」은 정식 (2)에만 맞다(App Store 버전 연결). DAY Dev (3)는 TestFlight 내부 시험(`IN_BETA_TESTING`)이다. 다음에 손볼 때 두 앱을 나누면 오해가 없다.
3. 연령 「12+」는 ASC API 값(`TWELVE_PLUS`)이다. asc-apply 는 「새 등급 체계 화면 값(13+ 일 수 있음)은 ASC 웹에서 확인」을 열어 두었다. 그 확인 결과는 원천에 없다. 문장을 「12+(API 값)」로 적으면 정확하다.
4. 60-release #4 블록 B 「제출됨」은 사실이다. 다만 presubmit 이 남긴 블록 B 전제(prod 데모 연결 D-1 · 데모 데이터 · 푸시 실물)를 확인한 기록은 원천에 없다. M-20 안 함으로 정식 앱 데모 세션에는 푸시가 없으니, 「알림」 문구를 뺀 것과는 맞다. 심사 중 데모 로그인 실패 위험만 기억해 두면 된다.
5. SPEC-001 :35 머리 개정 노트(2026-11-09)의 「**아직 구현 전이다** — 현행 기능으로 쓰지 않는다」는 남았다. 개정 노트는 그날의 기록이라 고치지 않는 것도 맞다. 하지만 같은 파일 §3 제목은 「구현됨」이라 지금 시점 문장처럼 읽힌다. 「→ 구현됨(2026-11-12 · §3)」 한 구절을 붙이면 한 파일 안에서 말이 같아진다.

## 재리뷰 (2026-11-12 · doc-sync 수정 1)

범위는 수정 1 뿐이다. Unlisted 두 원천, 확인일, 그 밖에 바뀐 것이 없는지를 봤다.

### 판정: PASS

W1 이 닫혔다. 새로 생긴 어긋남은 없다.

검증
- `lint-pipeline.py --strict`: exit 0 · 0 error · 263 warning · `products/day` 0건
- diff 추가 줄 이메일 모양: 0

| 항목 | 결과 | 근거 |
|---|---|---|
| 원천 두 개 | 닫힘 | `mobile-deployment.md` §6(:175)과 `60-release` §7-2 #11 끝에 같은 괄호가 붙었다. ① Apple 「Unlisted app distribution」 문서 링크 · 인용 「…will apply to any future versions of the app.」(= 이후 버전 모두) ② 신청서 `unlisted-app` 링크 · 동의 문구(사용자 화면) 「Once switched to unlisted app distribution, the app cannot be changed back to public or set to private app distribution.」(= 되돌릴 수 없음) ③ 「웹 양식」= 같은 괄호의 신청서 링크. 링크 · 인용이 `_RESUME.md` §5 「2026-11-12 Unlisted 근거(코디 확인)」 줄과 글자까지 같다 |
| 확인일 | 맞음 | 괄호에 「확인일 2026-11-12」가 있다. _RESUME 줄 날짜와 같다 |
| 그 밖 변경 없음 | 없음 | 10 차 리뷰 때 저장한 diff 추가 줄과 지금 추가 줄을 `diff` 했다. 다른 줄은 위 두 줄뿐이다. 참고 1 ~ 5 자리도 그대로다 |

### 참고(차단 아님)
- Apple 페이지는 이 리뷰에서 직접 열어 보지 않았다. 원천은 코디가 확인한 _RESUME 줄이고, 문서 글자는 그 줄과 같다.
- 60-release #11 은 괄호가 겹쳐 「…모두 Unlisted (원천 … 」))」로 끝난다. 읽는 데 문제는 없다.
