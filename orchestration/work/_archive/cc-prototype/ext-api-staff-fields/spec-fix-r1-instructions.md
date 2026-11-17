# planner 수정 r1 — 문서 검수 r1 WARN 5 반영

너는 cc-prototype planner 다. 앞 판 맥락 없음 — 먼저 읽을 것:
- 브리프 `orchestration/work/ext-api-staff-fields/ext-api-staff-fields-spec-brief.md` (allowed_paths · 금지 · 검증 그대로)
- 검수 리포트 `orchestration/work/ext-api-staff-fields/review-doc-r1.md`

리포트의 「고칠 방향」 그대로 다섯 개 전부 반영한다(코디 결정 — 묻지 말 것):
- W1 SPEC §4.4 괄호 → 「KOS id 는 메뉴 · 시술권 id 와 직원 목록 `kosAccountId`(§6.17 · 0.4.7)에만 낸다」. 부록 B · G 기록 줄은 그대로
- W2 T70(또는 T67)에 「직원 목록 설명에 `kosAccountId` 있음 · 옛 문장 『이메일 · 실명 · KOS id 는 내지 않는다』 없음」 단언 · WORK-015 BE1 대상 파일 · 검증 명령에 `tests/test_ext_docs.py` 추가
- W3 `email` · `realName` null 규칙 = 「`null` · 빈 문자열 · 칸 없음 → null」 (SPEC 표 · T67 · WORK 같이). 코디 기본값 — DEC-012 D-48 은 코디가 같은 뜻으로 고친다
- W4 §6.17 2단계에 「원소가 객체가 아님 · `id` 없음(빈 값) → 502」(지금 코드 그대로 · 동작 변화 0) · T67 에 `id` 없는 원소 → 502 갈래
- W5 WORK-015 검증 명령 앞에 「(`procedure/back` 에서)」 · 시험 파일 경로 기준 맞춤
- 참고 중 `SPEC:119` §0 근거 칸 D-46 · D-47 누락은 같이 고친다. `app/openapi_docs.py` 앱 설명은 범위 밖(손대지 않음)

버전은 0.4.7 그대로(아직 미배포 · 같은 판 고침) — 변경 이력 0.4.7 행에 「검수 r1 W1 ~ W5 반영」 덧붙임.
끝나면 브리프 §9 두 채널로 보고(subject 「planner 수정 r1 완료」).
