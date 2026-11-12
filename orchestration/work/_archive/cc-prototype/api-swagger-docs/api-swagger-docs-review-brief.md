# [reviewer] procedure back Swagger 설명 검수 — 설명이 코드와 맞나 · 동작 불변인가

너는 **cc-prototype `reviewer` 워커**다. **앞 맥락이 하나도 없다** — 이 브리프와 아래 파일만 믿어라. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs` (base `origin/main` = `77173cf` · 변경은 미커밋 상태 — `git diff` + untracked 3개)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

backend 워커는 작업을 끝냈다. 워크트리 파일을 **고치지 마라**(read-only).

## 1. SSOT — 먼저 읽을 것

- backend 브리프(계약): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/api-swagger-docs-be-brief.md` §3 · §7
- backend 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/be-report.md` — 주장(구조 변화 0 · 커버리지 · security 문서만)을 **실물로 다시 확인**한다
- `openapi-before.json` · `openapi-after.json` (같은 폴더)
- **설명의 SoT 는 코드**(`procedure/back/app/` service · domain · repository). SPEC(`/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/para/projects/summer-star/cc-prototype/20-spec/` 003~007)은 참고만

**따를 개념** — 없는 정보를 짓지 않는다(추정 설명 = 결함) · 동작 불변.

## 2. 배경 / 무엇을 보나

협업자가 운영 `https://ccc.medisolveai.xyz` API 를 부르려 하고 「API 설명 · 반환값 정의」를 요청했다. back 에 Swagger(`/api/docs`)를 열고 70 operation · 683 필드에 한국어 설명을 달았다. 이 문서를 **외부 사람이 믿고 호출**한다 — 틀린 설명은 빈 설명보다 나쁘다.

## 3. 검수 축

1. **설명 ↔ 코드 사실 대조(제일 중요)**: 표본이 아니라 **전 operation** 을 본다. 각 operation 의 description(허용 역할 · 부수효과 KOS 쓰기/SSE/푸시 · 멱등성) 과 `responses` 오류 코드 목록이 실제 코드 경로(service 까지)와 맞는지. **빠진 오류 코드 · 나지 않는 오류 코드 · 틀린 역할 · 틀린 부수효과**를 짚는다. 필드 설명은 enum 값 · null 뜻 · 단위 · 시간대 · 정렬을 중심으로 코드와 대조(전 필드가 어렵다면 응답 모델 전부 + 요청 모델 전부의 enum/nullable 칸은 전수, 나머지는 표본 — 본 범위를 리포트에 밝힌다)
2. **지어낸 설명**: 코드 근거 없는 의미 · 값 · 단위를 단정한 곳 → FAIL 후보
3. **동작 불변**: `git diff` 로 라우트 함수 본문 · 의존성 · 예외 처리기 · 미들웨어 · `response_model` · alias · CORS 가 그대로인지. `openapi_docs.decorate` 가 요청 처리 경로에 끼지 않는지. FastAPI 비공개 함수(`_get_api_route_for_openapi`) 사용의 위험 — 실패 시 앱 부팅을 막는지(막으면 FAIL) · 조용히 틀리는지
4. **공통 설명(app description)**: 인증 · 토큰 만료 · 역할 · 오류 형식 · 시간대 · SSE `?token=` · 공개 문진 토큰 · 통역 WS 프로토콜이 코드와 맞는지
5. **public 레포**: 예시 · 설명에 실명 · 실 연락처 · KOS id · 키 · 토큰 · 내부 호스트가 없는지(grep)
6. **조용히 통과하는 자리**: 커버리지 시험(`tests/test_openapi_docs.py`)이 「비어 있지 않음」만 보고 의미 없는 채움(필드 이름 반복 등)을 통과시키는지 · 422 제거가 맞는지(서버가 실제로 422 를 낼 길이 없는지)

## 4. 먼저 읽을 핵심 파일

- `procedure/back/app/openapi_docs.py` · `app/api/docs.py`(신규) · `app/main.py`
- `procedure/back/app/api/*.py` · `app/schemas/*.py` diff
- `procedure/back/tests/test_openapi_docs.py`

## 5. allowed_paths — 이 밖은 건드리지 마라

- (read-only — 리포 파일 수정 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-2/orchestration/work/api-swagger-docs/review-report.md`

## 6. 단계

1. 역할 문서 · be 브리프 · be 리포트 읽기
2. `uv run pytest -q tests/test_openapi_docs.py` 1회 · `app.openapi()` 를 직접 덤프해 after 와 같은지 1회
3. §3 축 순서로 검수 → 리포트

## 7. 범위 제약 — 하지 말 것

- 파일 수정 · 커밋 금지. 서버를 띄우지 마라(TestClient · `app.openapi()` 만). 사용자 포트 · 프로세스 금지
- be 리포트 §7 의 「발견한 버그」(display-requests 소유 검사 등)는 **이번 범위 밖** — 동작 변경 금지 작업이다. 다시 지적하지 말고, 그 버그가 **문서에 사실대로 적혔는지만** 본다
- 시술 · 상품 API 부재는 범위 밖

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 기능 독립 위반은 FAIL. 「조용히 통과하는 자리」를 따로 본다
```

리포트 형식: 맨 위 종합 판정 → 지적 표(번호 · 판정 · 파일:줄 · 설명이 말하는 것 · 코드가 하는 것 · 근거) → 본 범위(전수/표본) → 확인한 것(PASS 근거).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_2be25447-14e8-4dcf-9ed4-6b05f0fb0e46 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
