# backend 수정 r1 — 코드 검수 r1 W1

너는 cc-prototype backend 다. 앞 판 맥락 없음 — 먼저 읽을 것:
- 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-3/orchestration/work/ext-api-staff-fields/ext-api-staff-fields-be-brief.md`(금지 · 검증 · 보고 그대로)
- 검수 리포트 `…/ext-api-staff-fields/review-code-r1.md` W1
- SPEC-008 §8 새 행 「앱 설명 id 줄(0.4.7)」(코디가 더함)

할 일(한 곳):
- `procedure/back/app/openapi_docs.py:108-109` 외부 절 **id** 줄 괄호를 SPEC 문장대로 — 「(고객의 KOS id 는 내지 않는다 · 예외 — 직원 목록 `kosAccountId` 는 직원의 KOS 계정 id 문자열)」
- `tests/test_ext_docs.py` 에 앱 설명에 `kosAccountId` 가 있다는 단언 한 줄
- allowed_paths 에 이번만 `procedure/back/app/openapi_docs.py` 추가. 그 밖은 브리프 그대로
- W2(비문자열 → 500)는 고치지 않는다(코디 결정 · 기존 roleName 과 같은 동작 · 별 판)

검증: (`procedure/back` 에서) `uv run pytest -q tests/test_ext_docs.py tests/test_openapi_docs.py tests/test_ext_clinic.py` · `uv run ruff check .` 1회씩.
끝나면 브리프 §9 두 채널로 보고(subject 「backend 수정 r1 완료」).
