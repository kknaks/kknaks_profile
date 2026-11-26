# renumber-refs 결과 보고 — 코드 주석 · 시험 설명의 옛 스펙 번호를 새 번호로

## 상태: done (커밋 · push 안 함)

- 워크트리 `CENTURION_DAY/day-app-re1` · 브랜치 `kknaksss/spec-refs-re1`(← `origin/dev` `a76496c4`). 시작할 때 워크트리는 깨끗했다.
- diff: **129 파일 · +270 / −270**(줄 수 그대로 · 한 줄 안의 번호만 바뀜). 내역: 주석 · 시험 글 128 파일 + `backend/day/static/day.css` 생성 헤더 1줄.
- 로컬 스택(11040) · 시뮬레이터 · 실행 중 프로세스는 건드리지 않았다(`check.sh` 는 격리 인프라).

## 1. 대상 줄을 고른 방법

- #295 는 dev 에 squash(`8fe0095a`)로 들어갔다. 그 트리는 우리 합치기 끝 `1142b480` 과 같다(`git diff 1142b480 8fe0095a` 비어 있음). 부모 `4ba07ffe` 에는 dev 쪽 줄이 모두 이미 있다. 그래서 **HEAD 에서 `git blame` 이 `8fe0095a`(#295) 또는 `a76496c4`(#296)인 줄 = 우리 줄**이다. 165 파일 · 19,250 줄이다. #296 두 줄(Info.plist 문구)에는 스펙 인용이 없다.
- 그 줄들 가운데 옛 번호 패턴(㉚ · ㉑ · ㉒ · OQ-99/100 · U-23~30 · OQ-A63~91 · D-7/8 · OQ-N21/22 · 고침 5)이 든 줄 = **270줄 · 129 파일**.
- 줄마다 그 번호가 어느 SPEC 인지 봤다.
  - `SPEC-00x` 를 붙인 인용은 모두 SPEC-003(U · OQ-A · ㉑ · ㉒), SPEC-002(㉚ · OQ-100), SPEC-005(OQ-N21), SPEC-007(고침 5)이다.
  - 붙이지 않은 인용(`U-29` · `OQ-A87` · `개정 ㉒` 등)은 모두 앱 · 차트 · 예약 · 띄우기 · 여권 문맥이다. 같은 이름공간의 우리 번호다.
  - `DAY-SPEC-002 U-14 · U-16` · `SPEC-006 U-1 ~ U-5` · `SPEC-007 U-3` · `U-2` · `U-12` · `U-21` · `A-xx`(인수 조건) · `개정 ⑭`(SPEC-006) · `cc D-50` · `D7-49` 같은 cc 번호 · `C33` · `D55` 는 대상이 아니다. 그대로 뒀다.
- 스펙 워크트리(`day-app-re1-spec` `538befe4`)에서 대응을 확인했다.
  - 옛 OQ-A66(아이패드 차트 창 크기)은 지금 OQ-A70 행이다.
  - A-64 는 지금 「U-27 [문진 QR]」로 다시 매겨져 있다. A- 번호는 그대로다.
  - A-51 ~ A-60 = 「개정 ㉒」, A-61 ~ A-76 = 「개정 ㉓」이다.

## 2. 번호별 바꾼 수

| 이름공간 | 옛 → 새 | 바꾼 수 |
|---|---|---|
| SPEC-002 개정 | ㉚ → ㉜ | 22 |
| SPEC-002 OQ | OQ-100 → OQ-120 | 1 (OQ-99 인용 0) |
| SPEC-003 개정 | ㉑ → ㉒ | 5 |
| SPEC-003 개정 | ㉒ → ㉓ | 30 |
| SPEC-003 U | U-23→24 18 · U-24→25 18 · U-25→26 8 · U-26→27 7 · U-27→28 19 · U-28→29 5 · U-29→30 27 · U-30→31 24 | 126 |
| SPEC-003 OQ | A66→70 1 · A67→71 1 · A68→72 2 · A69→73 4 · A70→74 3 · A72→76 1 · A73→77 3 · A74→78 1 · A75→79 4 · A78→82 2 · A80→84 1 · A81→85 3 · A82→86 3 · A83→87 2 · A84→88 3 · A85→89 1 · A86→90 2 · A87→91 6 · A91→95 1 | 44 |
| SPEC-003 서버 의존 | D-7 · D-8 | 0 (우리 줄에 인용 없음) |
| SPEC-005 OQ | OQ-N21 → OQ-N25 | 2 (OQ-N22 인용 0) |
| SPEC-007 고침 | 고침 5 / 고침5 → 고침 6 / 고침6 | 86 |

파일 분포: app/android 8 · app/ios 4 · app/lib 31 · app/test 16 · backend/common 2 · backend/day 53(+ day.css 1) · backend/tests 14 · deploy/caddy 1.

㉒ → ㉓ 을 먼저 바꾸고 ㉑ → ㉒ 를 나중에 바꿨다. 그래서 한 번 바뀐 번호가 두 번 밀리지 않는다.

## 3. 안 바꾼 것과 이유

1. **`backend/migrations/versions/20261125_0030_display_questionnaire_kos.py:1`** docstring 의 「DAY-SPEC-007 고침 5(WORK-002)」를 그대로 뒀다. 브리프의 「migration 변경 0」을 지켰다. 주석이라 동작에는 영향이 없다. 바꿀지 코디가 정해 달라.
2. **dev 사람들이 쓴 줄** 0줄을 건드렸다. 예: `theme.dart` 「DAY-SPEC-003 U-23 ② · OQ-A65」 = main 뜻.
3. 커밋 메시지(#296 「OQ-A79」 → 새 번호로는 A83)는 히스토리라 손대지 않았다.

## 4. 코드 줄이 섞였는지 — 확인한 것

주석 기호로 시작하지 않는 바뀐 줄을 모두 손으로 봤다. 다음 다섯 가지뿐이다.
- 코드 끝에 붙은 `//` · `#` 주석
- 시험 이름 · 설명(`test('…')` · `testWidgets('…')` · `group('…')` · `def test_고침5_…` → `test_고침6_…` 6개. 다른 곳에서 이 이름을 부르지 않는다)
- docstring 안의 줄
- `test_screen_copy.py` VISIBLE 값(인용 글 · 키 = 화면 글자는 그대로)
- `day.css` 헤더의 `source-sha256`. `app.css` 주석이 바뀌어 `scripts/build-css.sh` 로 다시 생성했다. 규칙 줄 변경은 0이고, CSS 재현 검사도 통과했다.

**확인할 것 1개**: pydantic 필드 `description="이 기기 이름(… — DAY-SPEC-003 U-31)"`(옛 U-30). OpenAPI 설명 글 안의 스펙 인용이다. 값 · 경로 · 모양은 같고 `check.sh` 계약 시험도 통과했다. OpenAPI 문서 글자를 바꾸는 것도 안 된다면 이 1줄만 되돌리면 된다.

## 5. 남은 옛 번호 grep(우리 줄 · 바꾼 뒤)

새 번호와 겹치지 않는 옛 번호만 셌다.

| 패턴 | 남은 수 |
|---|---|
| ㉚ | 0 |
| ㉑ | 0 |
| OQ-99 · OQ-100 | 0 |
| OQ-N21 · N22 | 0 |
| U-23 | 0 |
| OQ-A63 ~ A66 | 0 |
| D-7 · D-8 | 0 |
| 고침 5 | 1 (위 migration — 일부러) |

나머지 번호(U-24~30 · OQ-A67~91 · ㉒)는 새 번호와 범위가 겹쳐 grep 으로 가를 수 없다. 대신 스크립트가 줄마다 옛 값을 정해진 대응으로 한 번에 바꿨다. 같은 줄을 두 번 밀지 않는다. 바뀐 줄 수는 270 → 270 이다.

## 6. 시험 수치

| 검사 | 결과 |
|---|---|
| `scripts/check.sh` 1회차 | 실패 — frontend 「Generated CSS differs」(`app.css` 주석이 바뀌어 `day.css` 헤더 hash 가 달라짐). `build-css.sh` 로 다시 생성(규칙 변경 0) |
| `scripts/check.sh` 2회차 | **exit 0** — 구조 · Jinja(714 소스) · ruff · format · mypy · taut-audit · taut-check · frontend **135/135** · tests **3211 passed**(386s). 증거 `.local/checks/20261126-214302-77294` |
| `fvm flutter analyze` | No issues found |
| `fvm flutter test` | **544 passed** · 81 skipped · 0 failed |
