# [planner] SPEC-008 · WORK-012 수정 r2 — review-doc r1 반영

너는 같은 `planner` 워커다. 원 브리프(`api-swagger-docs-spec-brief.md`)의 제약은 **그대로** 유효하다: allowed_paths(SPEC-008 · WORK-012 · README 행 · DEC-010 links 만) · 코드 읽기만 · KOS 호출 0 · 커밋 0 · public(키 · 실명 · 이메일 · KOS id 값 0) · 새 정책 발명 금지 · 열린 것 만들지 않기.

- 검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/review-doc-r1.md` — **전부 읽어라**
- DEC-010 이 고쳐졌다(코디 · 사용자 승인). **D-16 · D-19 · D-31 고침, D-35 · D-36 추가.** 다시 읽고 SPEC 을 맞춰라:
  `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/para/projects/summer-star/cc-prototype/10-decision/decision-010-product-ext-api.md`

## 1. DEC 질문 답 (사용자 결정 — 그대로 반영)

| Q | 결정 | 반영할 D |
|---|---|---|
| Q-A | 이름 검색은 **한 페이지(`countInPage` 1000)만**. `count` > 1000 이면 거르지 않고 404 「없음」(D-21 과 같은 바이트). 받은 결과는 KOS id 로 중복 제거. 그다음 **이름 정확 일치**: 양쪽 공백 전부 제거 + 대소문자 무시 후 KOS `name` 또는 `phoneticName` 과 같아야 후보. 그다음 이메일 대조(D-18) | D-16 · D-19 |
| Q-B | 예약 0명 갈래가 중복 검사로 이메일 존재를 드러내는 것은 **받아들인다**. Swagger 예약 설명에 이 사실을 적는다 | D-35 |
| Q-C | 시술권 가격 칸 = **KOS 묶음 가격**(KOS `price` 그대로). 칸 이름에 `purchase` · `VatIncluded` 를 넣지 마라(예: `bundlePrice`). 설명: 「고객이 낸 돈이 아님 · 산 시점 값에서 출발하지만 세트를 쓰면 줄 수 있음 · 부가세 포함 여부 표기 안 함」. 근거 = R2 §0 · §3.3 | D-31 |
| W11 | 메뉴 응답 `syncedAt` 은 **둔다**(메타 칸) | D-36 |

## 2. WARN · 참고 처리

| # | 처리 |
|---|---|
| W1 · W2 | Q-A 로 풀린다(한 페이지 · 상한 · 중복 제거). 「끝까지 넘긴다」 문장 · 페이지 루프를 지운다. 시험: 같은 id 두 번 → 1명 · `count` 1001 → 404(KOS 호출 1번) · 부분 일치만 맞는 이름 → 404 · 발음명 일치 → 200 · 공백 · 대소문자 차이 → 200 |
| W3 | 키 없는 401 · 없는 경로 404 에 **IP 당 제한**(문진 웹 `public_questionnaire.py:45-55` 선례: `client_ip` · `RateLimiter`)과 「같은 IP · 같은 결과는 1분에 1줄」 기록 줄이기. IP 는 카운터에만 쓰고 저장하지 않는다. 값(횟수 · 차단 시간)은 문진 웹 선례 값을 그대로 쓰고 근거 줄을 단다 |
| W4 · W6 | `ext_call` 은 **미들웨어**가 쓴다. `client` = 의존성이 `request.state` 에 남긴 값, 없으면 null(키를 다시 견주지 않음). `endpoint` = 매칭된 라우트 `path_format`, 없으면 고정값. 검사 순서 문장을 「키 → 제한 → 칸 검증. 단 JSON 이 아닌 본문은 키보다 먼저 400 · 없는 경로는 키 없이 404」로 고친다. T25 · T27 보강 |
| W5 | 없는 경로 `endpoint` = `"<METHOD> (unknown)"` 고정값. T27 에 「경로에 이메일 꼴 → 표에 없음」 |
| W7 | §6.5 1단계(503 검사)에 「외부 그룹에 켜진 구역 0 → 503 `ext_not_configured`」(KOS 호출 전 · 사본 기준). T20 보강 |
| W8 | Q-C 로 처리 |
| W9 | 하나로 정한다: `create()` 가 `Account` 대신 **행위자 문자열(`login_id`)**을 받는 얇은 겹 — 직원 경로는 `actor.login_id` 를 넘겨 `event_log` 값이 같다 · 외부는 `ext:<연동처>`. 다른 방식이 코드상 더 작으면 근거와 함께 그것을 골라도 되지만 하나만 적는다. T17 · T30 이 고정 |
| W10 | `test_openapi_docs.py:119-141` 로 고침 · `openapi_docs.py:33` 근거 삭제(「지금 배포 가정 = 파드 1개」로 적기) |
| W12 | §8 에 `api/docs.py` `STATUS_TEXT` 에 503 추가 · 외부 401 설명 줄에 「직원 로그인이 아니라 `X-Api-Key`」 |
| W13 | KOS id 설정이 지금 infra 에 들어가는 방식(`KOS_ZONE_ID` 등)을 따라 「infra 레포(private)엔 값 · profile · 코드 레포엔 0」으로 문구 통일 |
| 참고 2 | 구성 · 타겟 국가 「없음」 표시 = 별도 함수(복합 키 · raw 키) · 되살림은 `reservation_sync.py:200-201` 선례 |
| 참고 3 | BE2 임시 시험 경로는 BE3 에서 지운다 |
| 참고 4 | `IN_USE` 는 남은 장수에 넣지 않는다는 설명 한 줄 |
| 고객 자리 | §8 앱 설명 첫 줄에 「email 없는 기존 고객은 404 · 처음 예약하면 KOS 에 고객이 하나 더 생길 수 있음(데스크 정리)」 |

## 3. 마무리

- SPEC-008 `version 0.2.0` · 변경 이력 한 줄 · 부록 A(D→SPEC)에 D-35 · D-36 추가 · 부록 B 의 Q 들은 「답함」으로 · 열린 것 0
- WORK-012 를 SPEC 0.2.0 에 맞춘다(BE4 · BE5 · BE2 완료 조건) · README 행 버전 갱신
- public grep 0 확인
- 완료 보고는 원 브리프 §9 두 채널(이번 dispatch 의 taskId · dispatchId)
