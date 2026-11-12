# prod-deploy-re1 — 마감 문서 sync (2026-11-12 · planner)

## 상태: done (미커밋 · 코디가 커밋)

- 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec` · 브랜치 `kknaksss/prod-deploy-re1-spec-web`(PR #934) · 시작 HEAD 9ddbebeb · 깨끗한 상태에서 시작.
- 원천 = `_RESUME.md` §5 2026-11-12 줄 + 코디 지시. #246 · `0b2f8cff` 는 코드 레포에서 확인(`0b2f8cff Merge pull request #246` · 그 아래 `d8d0910f` 「시술 현황 보기 = 모든 직군」).
- 값 · 키 · 계정 이메일 · 테넌트 id · IP 는 적지 않았다(diff 에서 `@` · IP · 테넌트 끝자리 grep 0).
- 바뀐 파일 5: `40-architecture/deployment.md` · `40-architecture/mobile-deployment.md` · `60-release/app-store-preparation.md` · `20-spec/spec-001-login-session.md` · `log.md`. 수정 전 사본: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-prod-deploy-re1-spec/8d8c24d2-03ef-495b-b925-3c9c99a3c800/scratchpad/sync-before/`.

## ① deployment.md

- 머리 노트 「2026-11-12 — prod 첫 배포 완료」 한 줄 · `last_updated` 2026-11-12.
- 「prod 첫 배포 절차」 표 「지금」 칸:

| # | 지금 |
|---|---|
| 1 | 넣음(그대로) |
| 2 | 채움 · 코드 PR #244 로 들어감(`dev` 머지 `382827d5`) |
| 3 | 완료 — #244 dev 일반 머지 `382827d5` · dev 배포 OK(`/privacy` · `/support` 200) |
| 4 | 완료 — prod ff `382827d5` · deploy-prod 1차 revision-mismatch(정상) · migrate-prod OK |
| 5 | 완료 — deploy-prod 재실행 OK · `https://day.medisolveai.com` ready · `/privacy` · `/support` · `/login` 200 |
| 5-1 | 풀림 — VM 에서 운영 내부 API 200 |
| 6 | 완료 — prod api 컨테이너에서 1회 · 「운영 연결 넣음」 · 시스템 계정 = dev · prod 같은 계정(사용자 · 값은 레포 밖) |
| 7 | 첫 동기화 OK — 구역 · 방 · 직원 · 일정 · 오류 0(OQ-01-3 은 스펙에서 따로 닫지 않음) |

- 표 아래 두 줄: #246 → prod ff `0b2f8cff` · 푸시 = dev 서버 → DAY Dev · prod 서버 → 정식 앱만(M-20 안 함 · dev APNs 허용 앱 = 개발 앱 하나 그대로).
- 준비 표: 네트워크 「나가는 IP 미확인」 → 확인 · 허용됨(값 안 적음) · Key Vault 「첫 배포는 dev 만」 끝에 「prod 첫 배포 2026-11-12」.
- 「미결」: **KOS IP 제한 닫음**.

## ② mobile-deployment.md

- 머리 노트 2026-11-12 한 줄 · §1-1 제목 (2026-11-12) · `last_updated`.
- §1 「앱 환경 연결 · 구현 전」 → 구현됨(`backend/day/services/environments.py` — 코드 레포에서 확인 · prod 배포).
- §1-1:
  - ASC record = DAY Dev · 정식 DAY(옛 「정식 record 없음」 지움 — 60-release §1-3 에 이미 정식 record 가 있었음).
  - TestFlight 줄에 DAY Dev 0.1.0 (3) · 정식 DAY 0.1.0 (2) VALID · 버전 연결 · 내부 그룹(사용자 추가).
  - 「prod 서버의 앱 · APNs 설정은 아직」 → prod 첫 배포 · 허용 앱 = 정식 앱 하나(`prod.env`).
  - 새 줄: 심사 제출 · Unlisted 신청(결과 대기) · 푸시 경로 [확정].
- §6: 「정식 레코드 아직 없다」 지움 · [설정 완료] 줄 — 0.1.0 (2) 심사 제출 · Unlisted 신청(웹 양식) · App Privacy 게시 · 연령 12+ · 무료 · 한국만 · 출시 수동 · Unlisted 는 승인 뒤 되돌릴 수 없음 · 이후 버전 모두 Unlisted · 결과 대기.
- §9 표: iOS 배포 prod = 제출 · 신청 · 결과 대기 · APNs prod = 허용 앱 정식 앱 하나.
- §9-1: 「구현 전」 → 구현됨 · 「푸시」 줄(dev 서버가 정식 topic 으로) 지우고 → [확정] 하지 않음 · M-20 [미결] 줄 닫음.
- §13: **M-20 닫음(안 함)** · M-1 에 「Unlisted 신청서에는 Unmanaged 로 냄」(M-1 은 닫지 않음).

## ③ 60-release

- §1-1 공개 페이지 두 줄 → 로그인 없이 200(2026-11-12).
- §1-2 업로드 빌드 → 심사 제출 빌드 `0.1.0 (2)`.
- §1-3 (2026-11-12 기준): URL 200 · 메모 블록 A + B(「알림」 뺌) 제출 · 바이너리 (2) VALID · 제출 · TestFlight = 내부 그룹 추가(결과 기록 없음) · 마지막 줄 = **제출 · 신청 완료 · 결과 대기**.
- §5-1: URL 칸 200 · 연령 등 = 12+ · 무료 · 한국만 · 저작권 · App Privacy 게시 · 메모 A + B · 데모 로그인(값 없음) — 입력 · 제출.
- §7-2: #1 완료(담당 칸 그대로) · #3 사용자 입력 · 제출됨 · #4 제출됨 · #5 내부 그룹 추가 · 결과 기록 없음 · #6 `/privacy` 200 · #8 입력 · 제출 · #11 **제출 · 신청 완료 · 결과 대기**(막는 것 = 심사 · Unlisted 결과) · #12 Unlisted 신청서 값으로.
- 「발행 가능 여부」: 2026-11-12 공개됨 · T1 · T3 · T4 · T5 대조 결과는 기록 없음.

## ④ 그 밖 낡은 문장

- **고침**: DAY-SPEC-001 「앱 환경 연결」 「구현 전」 세 곳(§3 제목 · 매트릭스 줄 · 규칙 14) → 구현됨(`environments.py`).
- **그대로 둠(사실 미확인 · 또는 공개 문구)**:
  - 60-release §6-1 공개 본문 「시행일: 2026년 11월 12일(예정)」 · 내부 주석 :246 · §7-2 #10 — 페이지가 공개됐으니 「(예정)」을 뗄지는 공개 글자 변경이라 코디 · 사용자 몫(새 문구 금지).
  - 60-release §5-3 메모 블록 「Unlisted 배포를 신청할 예정입니다」 — 제출된 메모 글자.
  - deployment.md 준비 표 GitHub Environments 「prod 없음 · 첫 prod 실행 때 자동 생성 예상(그때 확인)」 — 실제로 생겼는지 원천에 없음.
  - mobile-deployment 「실기기 푸시 수신 확인은 아직」 · §1-1 「수출 규정 키 · 앱 아이콘 — 코드 미머지」 — 원천에 없음.
  - DAY-SPEC-000 OQ-01-3(운영 테넌트 응답 모양) — 첫 동기화 OK 만으로 닫지 않음(코디 판단).
  - 60-release §7-2 #9(5.1.2(i)) · #10 · §7-1 T1 ~ T6 — 원천에 결과 없음.

## log.md

- 2026-11-12 `arch-change, spec-change` · DAY-SPEC-001 한 행(맨 위).

## 검증

- `python3 scripts/lint-pipeline.py --strict` → exit 0 · 0 error · 263 warning · `products/day` 0.

## 수정 1 — review-doc-10 W1 · Unlisted 원천 붙임 (2026-11-12)

- 원천 = `_RESUME.md` §5 「Unlisted 근거」 줄(코디 확인).
- 「승인 뒤 되돌릴 수 없음 · 이후 버전 모두 Unlisted」가 있는 두 곳 끝에 같은 괄호를 붙였다:
  - `mobile-deployment.md` §6 [설정 완료] 줄(:175).
  - `60-release` §7-2 #11.
- 괄호 = 「원천 · 확인일 2026-11-12: Apple [Unlisted app distribution](https://developer.apple.com/support/unlisted-app-distribution/) 「…will apply to any future versions of the app.」 · 신청서 [unlisted-app](https://developer.apple.com/contact/request/unlisted-app/) 동의 문구(사용자 화면) 「Once switched to unlisted app distribution, the app cannot be changed back to public or set to private app distribution.」」.
- 「웹 양식」은 위 신청서 링크가 같은 괄호 안에서 출처가 된다.
- 그 밖 변경 없음 — review-doc-10 「참고」 1 ~ 5 는 손대지 않음.
- lint `--strict` exit 0 · 0 error · `products/day` 0 · 미커밋 5파일 그대로.
