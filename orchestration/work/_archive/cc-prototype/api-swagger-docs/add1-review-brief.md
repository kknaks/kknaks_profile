# [reviewer] add1 코드 검수 — 외부 API 3개(가능 시간대 · 과거 시술 · 예약 내역) — SPEC-008 0.3.1 ↔ 코드

너는 **cc-prototype `reviewer` 워커**다(1차 외부 API 를 검수한 그 워커). 이번은 **별개의 새 작업**이다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/roles/cc-prototype/reviewer/` (role · rules · skills · tools · workflow)

워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs` — 브랜치 `kknaksss/ext-api-add1` · base main `e0e4a16` · 변경은 미커밋(`git diff` + untracked). **read-only — 고치지 마라.**

## 1. 기준

- 계약: SPEC-008 **0.3.1** `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md` §6.6 ~ §6.9 · §7 · §8 · T32 ~ T44(+ 0.3.1 에서 더해진 줄)
- 결정: `.../10-decision/decision-011-ext-api-add1.md` D-01 ~ D-15 · DEC-010
- 빌드 계획: `.../30-work/work-013-ext-api-add1.md` (WP-REVIEW 점검 목록)
- 문서 검수: `orchestration/work/api-swagger-docs/review-doc-add1.md` W1 ~ W6 · I2 — 코드에서 닫혔는지 하나씩
- backend 리포트: `add1-be-report.md` — 주장을 실물로 다시 확인. §6 차이 1 ~ 7 은 SPEC · DEC 와 견줘 하나씩 판정

## 2. 검수 축 (전수)

1. **정원 규칙 하나**: 가능 시간대의 남은 자리 계산과 예약 생성의 정원 검사가 같은 함수 · 같은 사본을 쓰는가. 「목록에 있는 시각이면 정원으로 거절되지 않음」이 코드로 성립하는가. 공유로 빼낸 코드가 직원 예약 생성 · 예약표 결과를 바꾸지 않았는가(기존 시험 단언 약화 여부 포함)
2. **가능 시간대**: 기본 그룹만 · 운영 구간 × 간격 · 남은 0 제외 · 행 없는 구역 제외 · 오늘 지난 시각 제외(KST) · 날짜 검사(str · 빈 문자열 · 꼴 · 오늘~90일) · 503 조건이 KOS 호출 전 · 요청마다 slots 1번 → replace_slots(I2 잠금) · KOS 실패 갈래 502
3. **과거 시술 · 예약 내역**: 고객 찾기가 1차 조회와 같은 함수(404 바이트 같음) · 일정 응답 `{}`/`[]` = 빈 목록 · 배열 아님 = 502 · deleted 제외 · 최신 순 / 오늘 0시 이후 오름차순 · state 7값 매핑 · reservationId 사본 조회만(사본에 쓰지 않음) · 50건 상한
4. **개인정보 · 보안**: 응답에 메모 · 의사 이름 · 담당자 · 그룹 이름 · KOS 고객 id · 전화 0 · `ext_call` · 로그 · 예외 메시지에 이름 · 이메일 · 키 원문 0 · 이름 · 이메일이 query/path 에 0 · 키 · 호출 제한 · no-store 가 새 셋에도
5. **Swagger**: 새 세 operation 설명 · 필드 description · 오류 표가 실제 raise 와 일치 · 429 문구 「외부 경로 전부」 · parameters 단언(`date` 만 허용) 약화 아님 · 직원 문서 차이 0
6. **시험**: T32 ~ T44 가 계약을 실제로 고정하는가 · 가짜 KOS 가 실물과 다른 곳(「조용히 통과」)
7. **public**: diff 전체 실명 · 실제 이메일 · 연락처 · KOS id · 키 꼴 0

검증: `procedure/back` 에서 `uv run pytest -q` · `uv run ruff check .` 1회씩 직접. KOS 호출 · 서버 기동 · 사용자 포트 금지.

## 3. 리포트

`/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/add1-review-r1.md` 1개. 판정 PASS / WARN / FAIL · 항목마다 `파일:줄` · 근거 · 고칠 방향. 「조용히 통과하는 자리」 절 포함.

## 4. 완료 보고 — 문구 변경 금지

> 핸들은 dispatch preamble 의 값을 믿어라.

```bash
orca orchestration send \
  --to term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --from <네 워커handle> \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer 완료: <판정 한 줄>" --body "판정 / FAIL · WARN 수 / 수치 / 주요 항목"
orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 \
  --text "[worker_done] reviewer add1 완료 — <판정 한 줄>. 상세는 add1-review-r1.md." --enter
```
