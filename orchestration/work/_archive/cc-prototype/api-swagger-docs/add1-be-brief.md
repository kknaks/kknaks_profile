# [backend] add1 — 외부 API 3개: 예약 가능 시간대 · 과거 시술 · 예약 내역

너는 **cc-prototype `backend` 워커**다(1차 외부 API 를 만든 그 워커). 앞 맥락은 믿지 말고 이 브리프와 아래 파일만 믿어라. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/roles/cc-prototype/backend/` (role · rules · skills · tools · workflow)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs` — 브랜치 **`kknaksss/ext-api-add1`** · main `e0e4a16`(1차 #22 머지본) 위로 맞춰 둠. PR 은 코디가 올린다.

## 1. SSOT

- **SPEC-008 0.3.0** `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md` — 새 절 §6.6 ~ §6.9 · 시험 T32 ~ T44. 계약의 정본
- **WORK-013** `.../30-work/work-013-ext-api-add1.md` — WP 순서 · 완료 조건 · 부분 검증 명령. 처음부터 끝까지 한 번에
- 결정: `.../10-decision/decision-011-ext-api-add1.md`(D-01 ~ D-14) · DEC-010. 둘 다에 없으면 **짓지 말고 물어라**
- SPEC 문서 검수가 **병렬로** 돈다. 고칠 점이 나오면 코디가 따로 보낸다. 그 전까지 0.3.0 대로

## 2. 범위

- `procedure/back/**` 만. 기존 직원 API · 기존 외부 API 3개 동작 무변경(기존 시험 그대로 통과)
- 예약 생성의 정원 검사와 가능 시간대 계산은 **같은 함수 · 같은 사본**을 쓰게 한다(규칙이 두 벌이 되지 않게). 공유 코드를 빼낼 때 직원 경로 결과가 같아야 한다
- 내보내는 칸에 메모 · 의사 이름 · 담당자 · 그룹 이름 0 (SPEC 칸만)

## 3. 실물 확인(데모 KOS) — 조회만

- 데모 접속값: `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/.env` (워크트리 `procedure/.env` 에도 같은 값 + 외부 env 있음). 읽어서 env 로만. 값을 복사 · 커밋 · 리포트에 남기지 마라. 운영 지점 키(`KOS_API_tenent`) 절대 금지
- 가능 시간대(오늘 · 내일 1번씩) · 과거 시술 · 예약 내역(데모 고객 1명 200 · 틀린 이메일 404)을 스크립트 또는 TestClient + 실 KosClient 로 1회씩. 임시 DB 는 `/tmp` 아래 네 폴더, 끝나면 지움
- **KOS 쓰기 0** (예약 · 고객 생성은 코디가 E2E 에서)
- 사용자 포트(8700 · 3000) · 떠 있는 compose · 프로세스 금지

## 4. 검증

- WP 마다 WORK-013 의 부분 명령만. 전체 `uv run pytest -q` · `uv run ruff check .` 는 끝에 한 번. 기준선(시작 전 수치) 리포트에
- Swagger: 새 세 operation 도 summary · description · 모든 필드 description · 오류 표 · security — 「설명 빠진 곳 0」 시험 통과
- public 레포: 실명 · 실제 이메일 · 연락처 · KOS id · 키 값 0 — 끝에 grep

## 5. 하지 말 것

- 커밋 · push · PR 금지
- SPEC 에 없는 칸 · 경로 · 오류 code 금지. 없는 KOS 값을 다른 칸으로 추정해 채우지 않는다(null 그대로 + 리포트)

## 6. 리포트

`/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/add1-be-report.md` (이 파일만)
1. 변경 파일 · WP 별 무엇 2. 기준선 → 이후(pytest · ruff) 3. T32 ~ T44 대조표(시험 이름) 4. 데모 실물 결과(수만 · 값 0) 5. Swagger 확인 6. SPEC ↔ 코드 차이 · 확인 못 한 것

## 7. 완료 보고 — 문구 변경 금지

> 핸들은 dispatch preamble 의 값을 믿어라.

```bash
orca orchestration send \
  --to term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --from <네 워커handle> \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: <한 줄>" --body "변경 파일 / 수치 / T 대조 / 데모 확인 / 주의점"

orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 \
  --text "[worker_done] backend add1 완료 — <한 줄 요약>. 상세는 add1-be-report.md." --enter
```

막히면: `orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --text "[질문] backend: <질문>" --enter`
