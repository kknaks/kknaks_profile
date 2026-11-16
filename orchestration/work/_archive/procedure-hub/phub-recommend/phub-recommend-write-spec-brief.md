
# [writer] SPEC-001 · WORK-001 — Hub 데이터 그래프 + 조회 tool (로컬 E2E 1차)

너는 **procedure-hub `writer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디네이터 워크트리에 함께 탄다. 만들 파일은 `SPEC-001.md` · `WORK-001.md` 2개뿐 — DEC · _RESUME · 리포트 · 브리프를 포함해 다른 파일을 고치지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/DEC-001.md` ← **계약의 정본.** 특히 D-02~D-07 · D-10 · D-12 · D-13a~g. 여기 없는 정책을 발명하지 마라 — 필요하면 SPEC 의 「열린 것」으로
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/research-report.md` ← 원천 데이터 형태 · 수치 · 끊긴 참조 예시(검증 게이트 항목의 원료)
- 코드: `/Users/kknaks/git/PROCEDURE-HUB` (`release/v1.2.0`, read-only) — 새 모듈이 따를 관례는 **실물에서** 가져온다: `backend/app/modules/*`(모듈 구조) · `backend/app/core/container.py`(DI) · `backend/app/router/*` · `backend/app/core/app_builder.py` · `backend/alembic/` · `backend/README.md` · `docs/guides/api.md` · `.agents/skills/be-reviewer/`
- 양식: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/templates/projects/20-spec/` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/templates/projects/30-work/` (각 폴더 README 포함)

**기대는 개념** — `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/areas/concept/db/medallion-architecture.md` (레이어마다 입력·출력 계약 · 허용 변환 · 품질 검사를 SPEC 에 명시) · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/areas/concept/db/data-lineage.md` (엣지 → 원천 브론즈 행까지 거슬러 갈 수 있게)

## 2. 배경

사용자 지시(2026-10-26): **Hub 를 먼저 로컬 E2E 가능한 상태까지 세운다.** 상담 에이전트(LLM)는 이번 범위가 아니다. Hub 에는 LLM 이 없다(D-12).
이 SPEC · WORK 를 문서 리뷰 → 백엔드 워커가 그대로 구현한다. 사용자는 다음 날 로컬에서 E2E 한다.

## 3. 계약 — SPEC-001 이 반드시 정할 것

1. **브론즈** — stg 공개 GET 목록 엔드포인트 21개(리포트 부록 · Q3 수집 목록)를 받아 원본 그대로 저장하는 적재 명령(CLI). 행마다 엔드포인트 · 수집 시각 · 내용 해시 · 원본 JSON. 재실행 시 같은 해시는 새 행을 만들지 않는다. stg 주소는 env
2. **실버(노드)** — 노드 타입과 각 타입이 어느 브론즈 필드에서 오는지 표. 최소: 고민(taxonomy 트리 3단 — D-13d) · 시술군 17 · 시술 항목 521(D-13a) · 제품 · 부작용(합병증) · 부위(위험 부위 11 — D-13f) · 다른 고민 어휘(optimization 고민 · synergy target — D-13d). 노드마다 안정 id · 이름 · 동의어 · 원천 참조
3. **시맨틱(엣지)** — 엣지 타입 표: 고민→시술(taxonomy modality_ref · problem-combos · problem-packages · treatment-optimization — 원천 표시, 합치지 않음 D-13e) · 시술군⊃시술 항목 · **시술↔시술 단일 엣지**(synergy · contraindications · treatment-sequence 를 속성으로 — D-03, 원천 충돌은 값 모두 보존 + 상태 「충돌」 D-13b) · 시술→부작용 · 시술→제품 · 동의어(정규화 완전 일치만 — D-13d). 엣지 메타: 원천 · 근거 텍스트 · 강도(원천에 있을 때만) · 조건 · 검수 상태 · 원천 브론즈 행 참조(D-04). **이름 문자열 → 노드 해석은 결정론 정규화(리포트 Q3 머리의 normalize 와 같은 규칙)만.** 못 푼 것은 엣지를 만들지 않고 검증 리포트로
4. **검증 게이트 · 발행** — 빌드마다 검사: 끊긴 이름 참조 · 원천 충돌 · 연결 빈칸(시술 없는 고민 등) · 고아 노드. 결과를 저장하고 조회 가능하게. 발행본(버전 · 시각 · 브론즈 해시 집합 · 검사 요약)을 남기고 tool 은 **최신 발행본만** 읽는다. 검사 실패를 발행 차단으로 할지 경고로 할지는 SPEC 이 근거와 함께 정한다(로컬 1차라 데이터 결함이 많다는 점 고려)
5. **조회 tool** — 읽기 전용 · 범용(D-05): 노드 검색(이름 · 동의어 · 부분일치로 **후보** 목록, 점수 기준 명시) · 노드 상세 · 이웃(엣지 타입 필터) · 부분 그래프(시작 노드 · 홉 · 엣지 타입) · 노드 목록/스키마 설명(노드·엣지 타입의 뜻 — 외부 LLM 이 읽는다). **REST 와 MCP 가 같은 서비스 계층을 호출.** 모든 응답에 발행본 버전 · 시술 노드에는 금기 · 간격 · 부작용 엣지 동반(D-06). 요청 · 응답 shape 을 필드 단위로 적는다
6. **MCP** — 공식 MCP Python SDK 기준으로 전송 방식(streamable HTTP 권장)과 붙는 위치(기존 FastAPI 앱 마운트 vs 별도 프로세스)를 **공식 문서 URL 근거와 함께** 하나 고른다. tool 이름 · 입력 스키마 · 설명 문구
7. **모듈 위치** — 새 모듈(예: `backend/app/modules/graph/`) · 라우터 · 마이그레이션. **레거시 · canonical 테이블과 코드는 읽지도 고치지도 않는다(D-13c).** 기존 테스트가 깨지지 않을 것
8. **로컬 실행** — 사용자 포트와 겹치지 않게: 이미 쓰는 포트 3700 · 3800 · 8700 · 8800 · 54329 · 5000번대 다수. 기본값 **PostgreSQL 55434 · API 18005**(MCP 가 별도 프로세스면 18006). 컨테이너 이름 · 볼륨은 `phub-graph-` 접두. 「빈 DB → 마이그레이션 → 브론즈 적재 → 빌드/발행 → API 기동」 명령 순서
9. **E2E 시나리오(수용 기준)** — 사용자가 Swagger 와 MCP 클라이언트로 그대로 따라 할 수 있게, 기대 결과까지:
   - 「모공」 노드 검색 → 고민 노드 → 부분 그래프에 시술군 · 원천별 엣지
   - 「기미」 → 하위 고민 노드 → 세 원천이 서로 다른 엣지로 보임
   - 「처짐」 → 정규화 완전 일치로는 「쳐짐」과 안 이어짐(D-13d). 노드 검색이 무엇을 돌려주는지 **있는 그대로** 기대값으로 적는다(되는 척 금지)
   - 보톡스 ↔ 필러 시술↔시술 엣지 → 원천별 순서 값과 상태 「충돌」
   - 시술 노드 상세 → 금기 · 간격 · 부작용 동반 · 발행본 버전
   - 검증 리포트 조회 → 리포트 Q3 수치와 대조 가능한 숫자
10. **열린 것** — DEC OQ 중 이 SPEC 이 임시값으로 넘어간 것과, SPEC 작성 중 새로 나온 것

## 4. WORK-001 이 정할 것

- 백엔드 워커 1명이 순서대로 할 Phase(예: 모델 · 마이그레이션 → 브론즈 적재 → 빌드 · 검증 · 발행 → REST → MCP → 로컬 실행 문서 · E2E 스크립트). Phase 마다 완료 기준 · 테스트(stg 를 부르지 않는 fixture 기반) · 검증 명령
- 마지막 Phase 산출: 로컬 실행 안내(브랜치 안 `backend/` 하위 문서 1개 — 위치는 SPEC 이 정함)와 E2E 시나리오 확인 스크립트 또는 체크리스트
- 테스트는 `backend/README.md` 「검증」 관례(sqlite 메모리 + 마이그레이션은 빈 Postgres)와 맞춘다

## 5. allowed_paths — 이 밖은 건드리지 마라

- 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-001.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/WORK-001.md` **2개만**

## 6. 구현 단계

1. DEC · 리포트 · 코드 관례를 읽는다(코드는 read-only)
2. SPEC-001 → WORK-001 순서로 쓴다. 모든 절이 DEC D 번호 · 리포트 절 · 코드 파일:줄 중 하나를 가리킨다
3. MCP 결정은 공식 문서 URL 을 단다(웹 확인)

## 7. 범위 제약 — 하지 말 것

- 상담 에이전트 · LLM · Jev · 프론트 화면은 범위 밖
- 코드 · 회사 문서 레포를 고치지 않는다. stg 는 필드 확인이 꼭 필요할 때만 GET(각 엔드포인트 1회 이내)
- DEC 에 없는 정책은 「열린 것」으로
- public — 키 · 토큰 · 실명 금지

## 8. 검증

```
모든 결정·요구가 _RESUME §2 결정 · 조사 리포트 · 코드(파일:줄) 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 열린 것으로. public — 키 · 토큰 · 실명 0(grep)
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_92a9e861-40e9-4ab0-bec1-e792cb83801e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
