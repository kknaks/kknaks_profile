---
type: work
id: WORK-015
title: "외부 연동 API — 직원 목록에 `email` · `realName` · `kosAccountId` 더함 — BE1 스키마 · 서비스 · Swagger · T67 → REVIEW → 로컬 데모 실물 → 배포 · 운영 실물"
status: done
product: cc-prototype
feature: procedure
work_type: enhancement
owner: kknaks
progress: 100
created_at: 2026-11-17
updated_at: 2026-11-17
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/work
  - status/done
links:
  baselines: []
  decisions:
    - "[[decision-012-ext-api-charty1|DEC-012]]"
    - "[[decision-010-product-ext-api|DEC-010]]"
  specs:
    - "[[spec-008-product-ext-api|SPEC-008]]"
  works:
    - "[[work-014-ext-api-charty1|WORK-014]]"
  releases: []
  related: []
sources:
  - "para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md (0.4.7 · §4.4 · §6.1 「id」 · §6.17 · §8 엔드포인트(0.4.0) · §9 T67 · T70 · 부록 F D-48)"
  - "para/projects/summer-star/cc-prototype/10-decision/decision-012-ext-api-charty1.md (D-48 · D-15 고침 줄 · D-21 · D-29)"
  - "orchestration/work/ext-api-staff-fields/ext-api-staff-fields-spec-brief.md (WP 구성 · 검증 명령)"
  - "cc-prototype procedure/back main 969f44f (읽기만 — 대상 파일 · 줄 · tests/ 파일 이름)"
---

# 외부 연동 API — 직원 목록 칸 셋 더함 — 빌드 계획

계약은 **SPEC-008 0.4.7** 에 있다(§6.17 · §6.1 「id」 · §8 · §9 T67 · T70). 이 문서는 빌드 순서만 적고 계약을 다시 쓰지 않는다. 결정은 DEC-012 **D-48** 하나다(D-15 의 「이메일은 내지 않는다」 를 뒤집음). 경로 `GET /api/ext/clinics/{clinicId}/staff` 는 WORK-014 로 이미 운영 중이다(main `969f44f`). 화면은 없다.

## Meta

- **진행**: 끝(2026-11-17) — 코드 #25 `0553173` · infra #62 `0ad0e6d` · 운영 실호출 확인(직원 78 · 원소 키 여덟 · `kosAccountId` 78/78 · `email` 78/78 · `realName` 64/78 — 값은 기록 안 함). WP-E2E-LOCAL 은 데모 KOS 시스템 계정이 동시 로그인 기기 한도(`401 SignInLimitExceeded`)에 걸려 건너뛰고 운영 실호출로 갈음했다(사용자 결정). 코드 검수 r1 W2(`email` · `realName` 이 문자열이 아닌 값이면 500 — 기존 `roleName` 과 같은 동작)는 고치지 않음. progress 100
- **착수 전 게이트**: 없음. 남은 질문 없음
- Covers spec: SPEC-008 0.4.7. **필드 추가만** 한다 — `staff[]` 원소의 기존 다섯 칸 · 행 고르기(시스템 계정 · 제외 목록) · 차례 · 오류 · KOS 호출 수(1)는 바꾸지 않는다. 다른 ext 경로 · 직원 API · 직원 사본 표 · 동기화는 손대지 않는다
- 코드 레포: `kknaksss/cc-prototype` — 범위는 **`procedure/back/**`** 하나다. front · app 은 건드리지 않는다
- **infra**: 새 env · 표 · ingress 변경이 없다. 배포는 `back.imageTag` 올리기뿐이다
- base: 지금 main(`969f44f`). 워크트리 · 브랜치는 코디가 정한다
- 워커: backend(BE1) · reviewer · 코디(실물 확인 · 배포)
- **검증 규칙**: BE1 은 아래 부분 시험만 돌린다. 명령은 **`procedure/back` 에서** 돌린다(시험 경로 `tests/…` 는 그 폴더 기준)
- **실물 e2e 없이 done 금지**: 데모 KOS 실호출 1번(WP-E2E-LOCAL) · 운영 실호출 1번(WP-DEPLOY)
- public 레포다 — 리포트 · 커밋 · 시험 데이터에 키 · 실명 · 이메일 · KOS id 값을 쓰지 않는다. 시험 값은 지어낸 값(`…@example.com` · `<실명…>` 꼴)만 쓴다

## 계약 고정점 (WP 사이에서 바뀌면 멈추고 코디에게)

| 고정점 | SPEC-008 | 쓰는 WP |
|---|---|---|
| 새 칸 이름 셋 = `email` · `realName` · `kosAccountId`(원소 키 집합 = 여덟) | §6.17 응답 표 | BE1 |
| `email` · `realName` = 내부 원소 값 그대로 · `null` · 빈 문자열 · 칸 없음 → null · `name` 은 그대로(`realName` 과 다른 칸) | §6.17 응답 표 | BE1 |
| `kosAccountId` = 내부 원소 `id` 문자열 · null 없음 · `staffId`(ccc 정수)와 다른 체계 · 사본에 없는 계정도 값이 있다 | §6.17 4 · 응답 표 · §6.1 「id」 | BE1 |
| 여전히 내지 않는 칸 = `userId` · `licenseNumber` · `mfaMethods` · `roleId` | §6.17 「넣지 않는 칸」 | BE1 |
| 직원 사본(`staff`)에 이메일 · 실명을 저장하지 않는다 · 세 값을 `ext_call` · 앱 로그에 쓰지 않는다 | §6.17 「응답 밖」 | BE1 |
| 기존 다섯 칸 · 행 고르기 · 차례 · 오류 code · KOS 호출 수 1 무변경 | §6.17 · §6.9 | BE1 |

## Work Packages

| WP | 내용 | 계약 | 워커 | 대상 파일(범위) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| **WP-BE1** | **스키마 · 서비스 · Swagger 문구 · T67 시험** — `ExtStaff` 에 `email: str \| None` · `realName: str \| None` · `kosAccountId: str` 를 더하고 세 칸에 `description` 을 단다 · `staff()` 가 내부 원소의 `email` · `realName`(`null` · 빈 문자열 · 칸 없음 → null)과 `id`(문자열)를 옮긴다 · `STAFF_DOC` 의 「이메일 · 실명 · KOS id 는 내지 않는다」 를 SPEC §6.17 문장으로 고치고 첫 줄 칸 나열에 셋을 더한다 · T67 시험을 SPEC §9 T67(0.4.7)대로 고친다(지금의 「새지 않음」 단언 중 이메일 · 실명 · KOS id 몫을 「있음」 단언으로 · `userId` · `licenseNumber` · `mfaMethods` · `roleId` 몫은 그대로) · 가짜 KOS 원소에 세 칸(`null` · 빈 문자열 · 칸 없음 갈래 포함 · 지어낸 값만) · `id` 없는 원소 → 502 갈래(코드는 지금 그대로 · 시험만 더함) · 직원 목록 Swagger 설명 단언(SPEC §9 T70 — `kosAccountId` 있음 · 옛 문장 없음)을 `tests/test_ext_docs.py` 에 더함 | SPEC-008 §6.17 · §8 · §9 T67 · T70 | backend | `procedure/back/app/{schemas/ext.py,service/ext.py,api/ext.py}` · `procedure/back/tests/{test_ext_clinic.py,test_ext_docs.py}` · (가짜 원소를 거기 두면) `procedure/back/tests/fake_kos.py` | T67 통과 · T70 직원 목록 단언 통과 · Swagger 시험 통과 · ruff 0 | (`procedure/back` 에서) `uv run pytest -q tests/test_ext_clinic.py tests/test_ext_docs.py tests/test_openapi_docs.py` · `uv run ruff check .` | 끝(767 passed · 수정 r1) |
| **WP-REVIEW** | reviewer: SPEC-008 0.4.7 §6.17 · T67 ↔ 코드 · **필드 추가만**인지(기존 다섯 칸 · 행 고르기 · 차례 · 오류 · KOS 호출 수 · 다른 ext 경로 · 직원 API · 사본 표 무변경) · 세 값이 `ext_call` · 로그 · 사본에 안 남는지 · Swagger 옛 문장이 지워졌는지 · 실명 · 이메일 · KOS id 실제 값 grep 0. FAIL 은 모아서 한 번에 수정 발주 | SPEC-008 §6.17 · §8 · §9 T67 · T70 | reviewer | 코드 변경 전체 | PASS | — | 끝(r1 PASS · WARN 2 — W1 반영 · W2 보류) |
| **WP-E2E-LOCAL** | 코디: 백엔드 커밋 뒤 로컬 스택을 **재기동**한다(옛 코드로 확인 금지) → **데모 KOS 실호출 1번** — `GET /api/ext/clinics/1/staff` 응답 원소에 세 칸이 있고 채워지는지(`kosAccountId` 는 전부 값 있음 · `email` · `realName` 은 값 또는 null) · 기존 다섯 칸이 앞 판과 같은지 · KOS 호출 수 1(로그). **값은 기록하지 않는다**(건수 · 키 · null 수만) | SPEC-008 §6.17 | 코디 | — | 세 칸 확인 · 기존 칸 회귀 없음 | — | 건너뜀(기기 한도 · 사용자 결정 → 운영 확인으로) |
| **WP-DEPLOY** | 코디: 코드 PR main 머지 → back 이미지 → infra `back.imageTag` PR → ArgoCD sync · `/api/health` · `/api/docs` 의 직원 목록 설명이 새 문장인지 → **운영 호스트 실호출 1번**(연동처 키 · 세 칸 있음 · 값은 기록하지 않음). 협업자에게 새 칸을 알리는 것은 사용자 몫 | SPEC-008 §6.17 · §8 | 코디 | — | 운영 back = 이 판 · 운영 확인 끝 | — | 끝(#25 · infra #62 · 운영 확인) |

## 병렬

- 없다. BE1 → REVIEW → E2E-LOCAL → DEPLOY 차례로 한다
- infra 작업은 배포 때 태그 올리기뿐이라 코드와 병렬로 할 일이 없다

## 주의

- **필드 추가만**이다. `name` 의 원천을 `realName` 으로 바꾸거나 둘을 합치지 않는다(DEC-012 D-48 — 둘은 다른 칸)
- `kosAccountId` 는 지금 코드가 사본을 잇는 데 쓰는 값(`str(a["id"])`)을 그대로 낸다. 원소가 객체가 아니거나 `id` 가 없을(빈 값) 때의 `502` 는 지금 동작 그대로 둔다(SPEC §6.17 2 — 시험 갈래만 더한다)
- `email` · `realName` 은 KOS 값을 그대로 옮긴다. 다듬거나(소문자 · 공백) 검증하지 않는다 — `null` · 빈 문자열 · 칸 없음만 null 로 바꾼다
- 직원 사본(`staff` 표) · 1시간 동기화 · 다른 ext 응답의 `staffId` 는 손대지 않는다. 사본에 이메일 칸을 만들지 않는다
- 세 값을 `ext_call` · 앱 로그 · 리포트 · 커밋 메시지 · 시험 데이터(실제 값)에 남기지 않는다(DEC-010 D-24 · public). e2e 리포트에는 건수 · 키 · null 수만 적는다
- `userId` · `licenseNumber` · `mfaMethods` · `roleId` 는 이번에도 내지 않는다 — 시험의 그 단언을 지우지 않는다
