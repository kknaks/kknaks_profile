# 리뷰 리포트 — ext-api-staff-fields / doc r2 (2026-11-17)

대상: r1(`review-doc-r1.md`)의 W1 ~ W5 · §0 근거 칸이 SPEC-008 0.4.7 · WORK-015 · DEC-012 D-48 에 반영됐는지와, 고치면서 새로 어긋난 곳.
범위는 r1 그대로다(새 범위로 넓히지 않음 · 코드 main `969f44f` 읽기만 · 시험 실행 안 함).

`SPEC` = `para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md`,
`WORK` = `para/projects/summer-star/cc-prototype/30-work/work-015-ext-api-staff-fields.md`,
`DEC` = `para/projects/summer-star/cc-prototype/10-decision/decision-012-ext-api-charty1.md`.
줄 번호는 지금 작업 트리 기준이다(r1 때보다 SPEC 이 한 줄씩 밀렸다).

## 판정: PASS

FAIL 0 · WARN 0 · 참고 2. r1 의 다섯 WARN 과 §0 근거 칸이 전부 반영됐고, 고치면서 새로 어긋난 줄은 없다. BE1 발주를 막는 것이 없다.

## FAIL

없음.

## WARN

없음.

## r1 항목별 확인

| r1 | 고친 자리 | 확인 |
|---|---|---|
| **W1** §4.4 「KOS id 는 … 에만」 | `SPEC:380` — 「KOS id 는 메뉴 · 시술권 id 와 직원 목록 `kosAccountId`(§6.17 · 0.4.7)에만 낸다 — 코디 Q2 · 부록 B · DEC-012 D-48」 | 반영. §6.1 「id」(`SPEC:418`)와 맞다. 부록 B Q2(`SPEC:1155`) · 부록 G Q1(`SPEC:1261`)은 기록이라 그대로 — 지시대로다 |
| **W2** 옛 Swagger 문장 시험 · `test_ext_docs.py` | `SPEC:1073` T70 — 「직원 목록 설명에 `kosAccountId` **있음** · 옛 문장 『이메일 · 실명 · KOS id 는 내지 않는다』 **없음**(`tests/test_ext_docs.py`)」 · `SPEC:896` 이 「시험 = §9 T70」 을 가리킴 · `WORK:68` 대상 파일에 `procedure/back/tests/{test_ext_clinic.py,test_ext_docs.py}` · 완료 조건 「T70 직원 목록 단언 통과」 · 검증 명령에 `tests/test_ext_docs.py` · `WORK:69` REVIEW 계약에 T70 | 반영. 옛 문장이 남으면 이제 시험이 빨갛다. 단언이 들어갈 실물 자리(`tests/test_ext_docs.py:138-140`)와도 맞다 |
| **W3** `null` 값 규칙 | `SPEC:889` · `:890`(「`null` · 빈 문자열 · 칸 없음 → null」) · `SPEC:1070` T67(「`null` → null · 빈 문자열 → null · 칸 없음 → null(가짜 원소 세 갈래)」) · `WORK:58` · `:68` · `:82` · `DEC:147` D-48(「KOS 가 `null` · 빈 문자열을 주거나 칸을 빼면 `null`(2026-11-17 · 문서 검수 r1 W3 코디 기본값)」) | 반영. DEC · SPEC 표 · T67 · WORK 네 곳의 문장이 같은 뜻이다 |
| **W4** 2단계 조건 · `id` 없는 원소 시험 | `SPEC:873` — 「원소가 객체가 아님 · 원소에 `id` 없음(빈 값) → `502 kos_unavailable`(지금 코드 그대로 … 동작 변화 0 · 코드 규약: `app/service/ext.py:884`)」 · `SPEC:1070` T67 끝 「`id` 없는 원소가 하나라도 있음 → 502」 · `WORK:68`(「코드는 지금 그대로 · 시험만 더함」) · `WORK:81` | 반영. 코드 `app/service/ext.py:884` 의 검사(전 원소 `isinstance(x, dict) and x.get("id")`)와 같다 — 「하나라도」 도 맞다. 4단계(`SPEC:875`)의 「2단계의 `502`」 가 이제 가리킬 곳이 있다 |
| **W5** 실행 위치 · 경로 기준 | `WORK:49`(「명령은 **`procedure/back` 에서** 돌린다(시험 경로 `tests/…` 는 그 폴더 기준)」) · `WORK:68` 명령 앞 「(`procedure/back` 에서)」 · 대상 파일은 전부 `procedure/back/…` 로 통일 | 반영 |
| **§0 근거 칸** | `SPEC:120` — 「DEC-012 D-01 ~ D-48」 | 반영(D-46 · D-47 빠짐 메움) |
| 변경 이력 | `SPEC:105` 0.4.7 행 끝 「문서 검수 r1(`review-doc-r1.md` · WARN W1 ~ W5) 반영(같은 판 고침 · 미배포)」 + 항목별 한 줄 · sources `SPEC:70` | 지시대로. 버전 0.4.7 그대로 |
| `app/openapi_docs.py` 앱 설명 | SPEC · WORK 어디에도 넣지 않음 | 지시대로(범위 밖) |

## 새로 어긋난 곳 — 확인

- **diff 범위**: SPEC 의 바뀐 덩어리는 r1 때의 것에 `:70`(sources) · `:105`(이력 덧붙임) · `:120` · `:380` · `:873` · `:889-890` · `:896` · `:1070` · `:1073` 만 더해졌다. 직원 목록과 무관한 절은 바뀌지 않았다
- **필드 추가만**: W4 의 2단계 문장은 지금 코드를 그대로 적은 것이라 동작 변화가 없다 — D-48 의 「필드 추가만」 과 어긋나지 않는다. §6.9 KOS 호출 수(`SPEC:675` 내부 1) 그대로
- **T67 ↔ T70 겹침 없음**: 응답 계약은 T67(`tests/test_ext_clinic.py`), 설명 문장은 T70(`tests/test_ext_docs.py`)으로 갈렸고 WORK 의 명령이 두 파일을 다 돈다
- **DEC ↔ SPEC**: D-48 문장을 고친 뒤에도 칸 이름 셋 · 원천 · `name` 과 다른 칸 · 사본 저장 안 함 · 응답 밖 규칙은 r1 대조표 그대로다
- **public**: 새로 바뀐 줄에 이메일 꼴 · uuid 꼴 문자열 0

## 고객이 실물에서 만날 자리

r1 과 같다. 달라진 것 하나 — Swagger 직원 목록 설명에 옛 문장이 남는 경우는 이제 T70 이 막는다(`SPEC:1073`). WP-DEPLOY 의 `/api/docs` 눈 확인은 그대로 둔다.

## 참고(막지 않음)

- `SPEC:1253` 부록 F D-48 줄 — 요약이 「빈 값 · 칸 없음 = null」 로 남아 `null` 이 글자로는 없고, 자리 칸에 r1 반영으로 생긴 §4.4 · §6.17 2 · §9 T70 이 없다. 뜻이 어긋나지는 않는다(대응표 요약). 다음에 그 줄을 만질 때 맞추면 된다
- `SPEC:82` 머리말 0.4.7 줄 — D-48 을 근거로 하는 자리 나열에 §4.4 · §9 T70 이 없다. 같은 종류의 요약 누락이다
