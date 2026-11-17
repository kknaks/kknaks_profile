
# [backend] WP-BE1 — ext 직원 목록에 email · realName · kosAccountId

너는 **cc-prototype `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-3/orchestration/roles/cc-prototype/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/ext-api-staff-fields`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 앞 판 맥락이 없다 — 아래 파일만 믿어라. 같은 워크트리에 다른 워커 없음. 코드 레포 `AGENTS.md` 가 있으면 먼저 읽어라.

## 1. SSOT — 먼저 읽을 것 (문서는 코디 워크트리 절대경로 · read-only)

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-3/para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md` — **0.4.7 §6.17**(계약) · §6.1 「id」 · §8(직원 설명) · **§9 T67 · T70**(시험 기준). 여기 없는 건 발명하지 마라
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-3/para/projects/summer-star/cc-prototype/30-work/work-015-ext-api-staff-fields.md` — **WP-BE1** 행 · 계약 고정점 표
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-3/para/projects/summer-star/cc-prototype/10-decision/decision-012-ext-api-charty1.md` — D-48(결정 근거)
- 개념: 해당 없음

## 2. 배경

배포된 `GET /api/ext/clinics/{clinicId}/staff`(main `969f44f`)는 이메일 · 실명 · KOS id 를 일부러 뺀다. 연동처 요청으로 사용자가 뒤집었다(D-48). **필드 추가만** — 기존 다섯 칸 · 행 고르기 · 차례 · 오류 · KOS 호출 수(1) 무변경.

## 3. 계약

`ExtStaff` 원소 키 = 여덟: 기존 `staffId` · `name` · `roleName` · `roleTags` · `active` + 새 `email: str | None` · `realName: str | None` · `kosAccountId: str`.
- `email` · `realName` = 내부 `get-accounts` 원소 값 · `null` · 빈 문자열 · 칸 없음 → null. `name` 은 그대로
- `kosAccountId` = 내부 원소 `id` 문자열 · null 없음 · 사본에 없는 계정도 값 있음
- 여전히 안 냄: `userId` · `licenseNumber` · `mfaMethods` · `roleId`
- 사본 테이블 · 동기화 무변경(이메일 저장 안 함) · 세 값을 `ext_call` · 로그에 쓰지 않음
- Swagger: `STAFF_DOC` 의 「이메일 · 실명 · KOS id 는 내지 않는다」 를 SPEC §6.17 Swagger 문장으로 · 첫 줄 칸 나열에 셋 · 세 칸 `description`

## 4. 먼저 읽을 핵심 파일

- `procedure/back/app/schemas/ext.py:491` `ExtStaff`
- `procedure/back/app/service/ext.py` `staff()`(880 ~ 900줄 근처 · `:884` 모양 검사 · `:894` `kid = str(a["id"])` · `:899` `roleName` 선례 `or None`)
- `procedure/back/app/api/ext.py:520-545` `STAFF_DOC` · 라우트
- `procedure/back/tests/test_ext_clinic.py:95-140`(가짜 원소 · 단언) · `tests/test_ext_docs.py:138-140`(직원 설명 단언)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `procedure/back/app/schemas/ext.py` · `procedure/back/app/service/ext.py` · `procedure/back/app/api/ext.py`
- `procedure/back/tests/test_ext_clinic.py` · `procedure/back/tests/test_ext_docs.py` · (필요할 때만) `procedure/back/tests/fake_kos.py`
- 문서(`para/` · `orchestration/`)는 코디 소유 — 손대지 않는다

## 6. 구현 단계

1. 착수 전 기준선: (`procedure/back` 에서) `uv run pytest -q tests/test_ext_clinic.py tests/test_ext_docs.py tests/test_openapi_docs.py` 1회 — 수치 기록
2. 스키마 · 서비스 · `STAFF_DOC` 고침
3. 시험: T67(0.4.7) 그대로 — 키 여덟 · 세 칸 값 대조 · `null` / 빈 문자열 / 칸 없음 → null 세 갈래 · 사본에 없는 계정도 `kosAccountId` · `id` 없는 원소 → 502 · 남은 넷 키 0 · KOS 호출 1 · `ext_call` · 로그에 세 값 0. T70 직원 설명 단언(`kosAccountId` 있음 · 옛 문장 없음). 가짜 값은 지어낸 것만(`…@example.com` · `<실명…>` 꼴)
4. 검증 후 전체 `uv run pytest -q` 1회(회귀) · `uv run ruff check .`

## 7. 범위 제약 — 하지 말 것

- 다른 ext 경로 · 직원 API · 사본 표 · KOS 동기화 · `app/openapi_docs.py` 손대지 않음
- 실명 · 이메일 · KOS id **실제 값** 0(public 레포). 데모 KOS 실호출 하지 않는다(코디 몫)
- 사용자 포트 · 프로세스 · docker 건드리지 않음 · 커밋 · push 금지

## 8. 검증

```
(procedure/back 에서) uv run pytest -q tests/test_ext_clinic.py tests/test_ext_docs.py tests/test_openapi_docs.py · uv run ruff check . — 각 1회, 통과하면 반복하지 마라. 끝에 전체 uv run pytest -q 1회. 기능 폴더 밖 import 없음. 실행 못 한 검증은 사유와 함께 pending
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다(기준선 수치와 비교).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_94d17da5-ee50-4f74-ade5-221f35a1ea02 --from term_2b24ee55-2fac-4c06-804a-14401d958071 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94d17da5-ee50-4f74-ade5-221f35a1ea02 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94d17da5-ee50-4f74-ade5-221f35a1ea02 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
