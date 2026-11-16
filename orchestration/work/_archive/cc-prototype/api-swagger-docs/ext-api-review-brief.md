# [reviewer] 외부 연동 API(`/api/ext`) · 메뉴 저장 코드 검수 — SPEC-008 0.2.1 ↔ 코드

너는 **cc-prototype `reviewer` 워커**다. 앞 작업(Swagger 설명 검수)과 **별개의 새 작업**이다. 역할 문서(절대경로):
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs` (base `origin/main` `c9f30ac` · 변경은 미커밋 — `git diff` + untracked). **read-only — 고치지 마라.**

## 1. 기준

- 계약: SPEC-008 **0.2.1** `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md` (부록 A = DEC-010 D-01 ~ D-36 대조)
- 빌드 계획: `.../30-work/work-012-product-ext-api.md` — 특히 WP-REVIEW 행의 점검 목록
- backend 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/ext-be-report.md` — 주장을 **실물로 다시 확인**(§6 「SPEC 과 다르거나 정한 것」 7개는 하나씩 SPEC · DEC 와 견줘 판정)
- 문서 검수 r2: `review-doc-r2.md` N1 ~ N3 (같은 폴더) · 보정 `be-amend-1.md`

## 2. 검수 축 (전수)

1. **보안 · 개인정보**: 외부 라우터에 `require_login` · `Actor` 0 · 직원 라우터가 `X-Api-Key` 를 보지 않음 · 키 비교 `hmac.compare_digest` · 빈 env 연동처 무효 · `ext_call` · 앱 로그 · 예외 메시지에 이름 · 이메일 · 키 · IP 원문 0(코드 경로 전부 grep) · 외부 응답에 `duplicated_visitor` · `candidate` · 전화 · 생년월일 · 여권 · KOS 고객 id 0 · 「없음」 404 네 경우 바이트 같음
2. **조회 규칙 §5**: 한 페이지 1000 · `count` > 1000 → 404 · KOS id 중복 제거 · 이름 정확 일치(공백 · 대소문자 · `name`/`phoneticName`) · 이메일 trim+lower 정확 · 빈 email 제외 · 0/1/2+ 갈래. `fake_kos` 검색 규칙이 실물 성질(공백 그대로 · 부분 일치)에서 바뀌지 않았는지(diff)
3. **예약 §6.5**: 503 조건 4개(env 빔 · 그룹 없음 · present 0 · 켜진 구역 0)가 KOS 호출 **전** · 행위자 문자열 겹이 직원 `event_log.actor` 를 바꾸지 않음 · 409 매핑 · 0명 갈래 새 고객
4. **제한 · 기록 §7**: 키당 60/60s · 막힌 요청 안 셈 · IP 제한 범위 = client null 인 오류 전부(N1) · 1분 1줄 · 미들웨어 기록 실패가 응답을 바꾸지 않음 · `Cache-Control: no-store` · 다중 요청 동시성(락)
5. **메뉴 동기화 §4.1**: 8 작업 · 작업별 독립 · 실패 = 그 표 그대로 · 「없음」 표시 성공 때만 · 복합 키 표 별도 함수 · 되살림 · `syncedAt` 실패 때 이전 값 유지(N3 — `set_sync` 가 실제로 그런지 `repo.py` 를 열어 확인. `INSERT OR REPLACE` 면 덮인다) · 마스터 루프 순서 · 기존 예약 동기화 회귀
6. **직원 동작 불변**: 직원 `search()` `countInPage:20` · 직원 예약 생성 · 기존 시험 고침 3건(리포트 §6)이 단언 약화가 아닌지
7. **Swagger**: 외부 tag · `ExtApiKey` securityScheme · 세 operation 설명 · 오류 표가 실제 raise 와 일치(빠진 · 안 나는 code) · 「설명 빠진 곳 0」 시험 · 직원 문서 차이 0
8. **시험**: T1 ~ T31 이 계약을 실제로 고정하는지(약한 단언 · 가짜가 실물과 다른 곳 = 「조용히 통과」)
9. **public**: diff 전체에 실명 · 이메일(`example.com` 외) · 연락처 · KOS id · 키 꼴 0

검증: `procedure/back` 에서 `uv run pytest -q` · `uv run ruff check .` 1회씩 직접 돌려 수치를 리포트에 적는다. KOS 호출 · 서버 기동 · 사용자 포트 금지.

## 3. 리포트

`/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/ext-review-r1.md` 1개. 판정 PASS / WARN / FAIL · 항목마다 `파일:줄` · 근거 · 고칠 방향. 「조용히 통과하는 자리」 절 포함.

## 4. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --from <네 워커handle> \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer 완료: <판정 한 줄>" --body "판정 / FAIL · WARN 수 / 수치 / 주요 항목"
orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 \
  --text "[worker_done] reviewer 완료 — <판정 한 줄>. 상세는 ext-review-r1.md." --enter
```
