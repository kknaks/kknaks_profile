# 작업 요약 — ext-api-staff-fields (cc-prototype)

기간: `2026-11-17` ~ `2026-11-17`
결과: 머지 · 배포 완료 — 코드 #25 `0553173` · infra #62 `0ad0e6d` · 운영 실호출 확인(로컬 데모 실물은 KOS 기기 한도로 건너뜀)

## 1. 무엇을 했나

11-16 에 배포한 외부 연동 API 직원 목록(`GET /api/ext/clinics/{clinicId}/staff`)은 이메일 · 실명 · KOS 계정 id 를 일부러 빼고 있었다(DEC-012 D-15). 연동처가 계정을 이으려면 셋 다 필요하다고 해서 사용자가 D-15 를 뒤집었다(D-48).
DEC-012 D-48 → SPEC-008 0.4.7 → WORK-015 를 세우고(문서 검수 r1 FAIL → r2 PASS), 한 워커가 스키마 · 서비스 · Swagger 문구 · 시험을 고쳤다(767 passed). 코드 검수 r1 PASS(WARN 2) 뒤 W1(Swagger 공통 id 줄)만 반영했다.
로컬 데모 실물은 KOS 시스템 계정 동시 로그인 기기 한도에 막혀 건너뛰고, back 만 운영에 올려 운영 실호출로 확인했다(직원 78 · 원소 키 여덟).

## 2. 적용한 기술·개념

- **비노출로 정했던 칸을 내보내기 — 「없음」 단언을 「있음」 으로 뒤집되 남은 비노출 · 응답 밖 0 은 그대로**
  - 왜 이걸 골랐나: D-15 는 「필요 없는 것은 내지 않는다」 였고 T67 이 「키 0」 으로 고정하고 있었다. 연동처가 계정을 이을 값이 필요해지자 결정을 지우지 않고 취소선 + D-48 로 뒤집었다. 표면은 세 칸만 넓히고 `userId` · `licenseNumber` · `mfaMethods` · `roleId` 「없음」 단언은 지우지 않았다. 세 값은 응답에만 싣고 직원 사본 · `ext_call` · 앱 로그에는 남기지 않는다(시험으로 확인)
  - 무엇이 어려웠나: `kosAccountId` 는 다른 ext 응답의 `staffId`(ccc 정수)와 체계가 다르다. SPEC §6.1 「id」 규약(「고객의 KOS id 는 내지 않는다」)과 Swagger 공통 설명 줄에 예외를 적지 않으면 연동처가 둘을 같은 번호로 읽는다 — 문서 검수 r1 과 코드 검수 W1 이 같은 자리를 짚었다. 실명은 운영 78명 중 14명이 비어 있어(null) 연결 열쇠로는 `email` · `kosAccountId` 가 안전하다
  - 근거: DEC-012 D-15(고침 줄) · D-48 · SPEC-008 0.4.7 §6.1 · §6.17 · §8 · T67 · T70 · `review-doc-r1.md` · `review-code-r1.md` W1 · 코드 #25(`app/service/ext.py` staff · `app/openapi_docs.py:109` · `tests/test_ext_clinic.py`)
  - 개념: [[minimal-api-surface]]
- **외부 시스템 계정의 로그인 슬롯은 환경 사이 공유 자원이다** — 로컬 e2e 가 운영과 같은 KOS 시스템 계정으로 sign-in 해야 했다
  - 왜 이걸 골랐나: 로컬 서버를 띄우자 내부 API 가 401 이었고, sign-in 을 직접 불러 본문 `SignInLimitExceeded`(동시 로그인 기기 5대)로 원인을 갈랐다. 운영은 PVC DB 에 저장한 토큰을 다시 쓰므로 pod 를 갈아도 슬롯을 새로 쓰지 않는다. 로컬에서 슬롯을 비우려 KOS 「계속하기」(다른 기기 로그아웃)를 누르면 운영 세션이 끊길 수 있어, 재시도를 멈추고 사용자에게 물어 운영 확인으로 갈음했다
  - 무엇이 어려웠나: 첫 401 은 env 를 못 읽은 것처럼 보여 `.env` 를 두 번 다르게 넣어 봤다. 상태 코드만 보고 자격 문제로 읽은 것이다 — 본문을 본 뒤에야 기기 한도로 판정했다
  - 근거: `_RESUME.md` §1 · §5 · DEC-012 D-21 · 운영 배포 뒤 back 로그(저장 토큰 사용 · 재로그인 없음)
  - 개념: [[external-api-error-classification]]

## 3. 막혔던 것 / 사고

- **로컬 데모 e2e 가 KOS 시스템 계정 기기 한도에 막혔다** → 첫 401 을 env 문제로 보고 `.env` 를 셸 source · 워크트리 복사 두 번 넣어 봤다 → sign-in 을 직접 불러 본문 `SignInLimitExceeded` 로 판정 → 재시도 멈춤 · 서버 내림 · 워크트리 `.env` 사본 지움 → 사용자 결정으로 운영 확인. 같은 시스템 계정을 다른 서버(DAY 등)도 쓰는지는 확인하지 못했다 → 다음에는 로컬 e2e 전에 그 계정이 지금 몇 기기에 붙어 있는지부터 본다. 401 은 본문부터 읽는다
- **「로컬」 이 무엇인지 사용자에게 바로 전하지 못했다** → 사용자가 KOS 기기 화면 스크린샷을 보이며 「서버 등록은 잘 돼 있다」 고 했다. 로컬 = 사용자 맥북에서 띄운 서버라는 점을 처음 물을 때 적었어야 했다
- **SPEC 이 Swagger 고칠 자리를 `STAFF_DOC` 하나로만 적었다** → 공통 설명 id 줄(`openapi_docs.py:109`)이 빠져 코드 검수 W1 로 나왔다 → SPEC §8 에 한 줄 더하고 수정 r1 로 반영. 규약 문장을 뒤집을 때는 그 문장이 나오는 곳 전부를 grep 해서 범위에 넣는다

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-17 | ~~직원 목록에 이메일 · 실명 · KOS id 를 내지 않는다(D-15)~~(11-17 D-48 로 뒤집음 — 연동처가 계정 연결에 필요) → `email` · `realName` · `kosAccountId` 추가 · 필드 추가만 | 사용자 「이메일 실명 코스 id 다 받아야」 · 칸 이름 승인 |
| 2026-11-17 | `email` · `realName` 은 `null` · 빈 문자열 · 칸 없음 → null · 다듬지 않음 · `name` 그대로 · 사본에 저장 안 함 · 응답 밖에 기록 안 함 | 코디 기본값(D-48) |
| 2026-11-17 | Swagger 공통 id 줄에 `kosAccountId` 예외 한 구절 · SPEC §8 한 줄 | 코디 기본값(코드 검수 W1) |
| 2026-11-17 | 문자열 아닌 `email` · `realName` → 500 은 이번에 안 고침(기존 `roleName` 과 같음 · SPEC 에 갈래 없음) | 코디 기본값(코드 검수 W2) |
| 2026-11-17 | 로컬 데모 e2e 건너뛰고 운영 배포 뒤 운영 실호출로 확인 | 사용자(기기 한도) |

## 5. 날짜별 로그

- `2026-11-17` D-48 → SPEC-008 0.4.7 · WORK-015 → 문서 검수 r1 · r2 → BE1 → 코드 검수 r1 → 수정 r1 → 로컬 e2e 막힘(기기 한도) → 코드 #25 · infra #62 · 운영 실호출 확인

## 6. 산출물

프로젝트와 당시 작업 문서는 `sync-work-links.py`가 만드는 작업 목차로 연결한다.
아래에는 판단의 근거가 된 리포트·PR·커밋을 구체적으로 남긴다.

- spec PR: profile(이 마감 PR)
- code PR: https://github.com/kknaksss/cc-prototype/pull/25 (`0553173`) · infra https://github.com/MediSolveAIDev/k8s_infra_mac/pull/62 (`0ad0e6d`)

- `kknaksss/ext-api-staff-fields` → `main`
  - `8fbd307` feat(procedure): ext 직원 목록에 email · realName · kosAccountId (SPEC-008 0.4.7 · DEC-012 D-48)
- `kknaksss/cc-ext-staff-fields` → `main`
  - `2a9759a` deploy(cc-prototype): procedure back 0553173 — ext 직원 목록 칸 셋
- 리포트: `review-doc-r1.md` · `review-doc-r2.md` · `review-code-r1.md`

## 7. 잔여

- 연동처 안내(사용자 몫) — `kosAccountId` ≠ `staffId` · 실명 14명 null → 연결은 `email` · `kosAccountId` · 비활성 직원 23명의 이메일 · 실명도 응답에 들어간다
- W2 — `email` · `realName` · `roleName` 이 문자열이 아니면 500. 바꾸려면 SPEC §6.17 2단계에 갈래를 먼저 더하고 셋을 같이 맞춘다(별 판)
- 로컬 데모 실물 확인은 하지 못했다 — KOS 시스템 계정 기기 한도. 그 계정이 어느 서버들에 붙어 있는지 정리가 필요하다

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/cc-prototype/ext-api-staff-fields/README|ext-api-staff-fields]]
<!-- work-links:end -->
