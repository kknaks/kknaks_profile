# [backend] procedure back — 시술 · 상품 메뉴 저장 + 외부 연동 API(`/api/ext`) + Swagger

너는 **cc-prototype `backend` 워커**다. 앞 맥락은 믿지 말고 이 브리프와 아래 파일만 믿어라. 역할 문서(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/roles/cc-prototype/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs` (브랜치 `kknaksss/api-swagger-docs` · `origin/main` `c9f30ac` 위로 맞춰 둠)
PR 대상 `main` (PR 은 코디네이터가 올린다)

## 1. SSOT — 계약은 여기서만

- **SPEC-008(0.2.0)** `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md` ← 계약의 정본. 경로 · 칸 · 오류 code · 시험 T 번호 전부 여기
- **WORK-012** `.../30-work/work-012-product-ext-api.md` ← WP 순서 · 완료 조건 · 부분 검증 명령. **BE1 → BE6 를 차례로 전부** 한다(한 번의 발주로 끝까지)
- 결정 원천: `.../10-decision/decision-010-product-ext-api.md`(D-01 ~ D-36). SPEC 에 없으면 DEC 를 보고, DEC 에도 없으면 **짓지 말고 물어라**(§9 질문 채널)
- KOS 사실: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/research-*.md` 4개
- 지금 Swagger 규약: `procedure/back/app/openapi_docs.py` · `app/api/docs.py` · `tests/test_openapi_docs.py`(이번에 더하는 외부 API 도 summary · description · 모든 필드 description · 오류 표 · security 표시를 같은 수준으로 — 「설명 빠진 곳 0」 시험이 그대로 통과해야 한다)

SPEC 문서 검수 2차가 너와 **병렬로** 돌고 있다. 거기서 SPEC 이 고쳐지면 코디가 고친 점만 따로 보낸다. 그 전까지는 SPEC 0.2.0 대로 간다.

## 2. 범위

- `procedure/back/**` 만. front · app · infra · compose · `.env.example` 은 건드리지 않는다. 단 **`procedure/.env.example` 에 새 env 3개 이름(값 빈칸)** 을 더하는 것은 허용한다
- 직원 API 동작 무변경(직원 `search()` `countInPage:20` · 직원 예약 생성 · `event_log` 값 · 401 모양). 예약 생성에 actor 문자열을 넘기려고 손댈 때도 직원 경로 결과가 같아야 한다(기존 시험이 그대로 통과)

## 3. 실물 확인(데모 KOS) — 허용 범위

- 데모 KOS 접속값은 `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/.env` 에 있다(데모 테넌트). **읽어서 env 로만 쓰고, 복사 · 커밋 · 리포트에 값을 남기지 마라.** 운영 지점 키(`KOS_API_tenent`)는 절대 쓰지 않는다
- BE1(메뉴 동기화 한 바퀴) · BE4(데모 고객 조회 200 / 404)는 **조회만**, 스크립트 또는 TestClient + 실 KosClient 로 1회씩. 임시 DB 파일은 scratch 경로(`/tmp` 아래 너의 폴더)에 두고 끝나면 지운다
- **KOS 쓰기(예약 · 고객 생성)는 하지 않는다** — 코디가 E2E 에서 한다
- 사용자 포트(8700 · 3000 등) · 떠 있는 compose · 프로세스를 건드리지 않는다. uvicorn 을 띄워야 하면 쓰이지 않는 포트에 띄우고 끝나면 내린다

## 4. 검증

- WP 마다 WORK-012 의 부분 명령만. **전체 `uv run pytest -q` · `uv run ruff check .` 는 BE6 끝에 한 번**
- 기준선(시작 전 `uv run pytest -q` 수치)을 리포트에 적는다
- public 레포: 시험 · 예시 · 리포트에 실명 · 이메일(`a@example.com` 꼴 말고) · 연락처 · KOS id · 키 값 0 — 끝에 grep

## 5. 하지 말 것

- 커밋 · push · PR 금지(워크트리에 변경만)
- SPEC 에 없는 칸 · 경로 · 오류 code 추가 금지. 막히면 묻는다
- 없는 KOS 값을 다른 칸으로 추정해 채우지 않는다(예: `lastVisitedDateTimeUtc` 가 없으면 null 그대로 + 리포트)

## 6. 리포트

`/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/ext-be-report.md` (이 파일만 쓴다)
1. 변경 파일 · WP 별 무엇
2. 기준선 → 이후 수치(pytest · ruff)
3. SPEC §9 T1 ~ T30(+ 0.2.0 에서 더해진 시험) 대조표 — 시험 이름
4. 데모 실물 확인 결과(BE1 표별 행 수 · SINGLE 진료항목 채움 수 · 공개 경로 8 · N 값 근거 · BE4 200/404 · `lastVisitedDateTimeUtc` 있음/없음) — 값 0, 수만
5. Swagger: 외부 tag · securityScheme · 세 엔드포인트 설명 확인
6. SPEC ↔ 코드 차이 · 확인 못 한 것

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> \
  --dispatch-id <이 태스크의 dispatchId> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 / 수치 / T 대조 / 데모 확인 / 주의점"

# (2) 직접 주입
orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 ext-be-report.md." --enter
```

- 막히면: `orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --text "[질문] backend: <질문>" --enter`
