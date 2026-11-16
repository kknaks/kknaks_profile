
# [docs] SPEC-001·002·003·005 작성 — 발주 가능한 계약으로

너는 **ontology-demo `docs` 워커**다. 직전 태스크들과 같은 워크트리, 같은 규칙
(역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/roles/ontology-demo/docs/`).

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline`
시작 전 `git fetch origin` 만 — base 이동 금지(rebase 는 코디 몫). 직전 산출물(BASE-001·DEC-001~005)은 커밋됨(0400ddb).

## 1. SSOT — 먼저 읽을 것 (전부 레포 루트 기준, read-only)

- `para/projects/summer-star/ontology-demo/10-decision/` — DEC-001~005 + README 미결 표. **spec 은 이 결정들의 계약화다.**
- 기록(사실의 SoT): `para/resources/note/ontology/` — 02(브론즈 실사·행수) · 03(글로서리·PII 반입 규칙) · 04(실버 변환) · 05(골드 KPI·게이트) · 07(nodes/edges·판정) · 08(에이전트 루프·시나리오·게이트) · 09(전체 계획)
- `para/projects/project.md` + `templates/projects/20-spec/spec.md` 양식 + 모범: `para/projects/summer-star/kknaks-dev/20-spec/spec-017-recruiter-chat.md`
- 코드 현황(참조만): `app/ontology-agent/`(FastAPI 스캐폴드·config.py) · `app/back/service/chat/`(open-kknaks 스트림 패턴) · `app/mcp/`(FastMCP 패턴)

**기대는 개념** — [[medallion-architecture]] · [[pii-masking]] (DEC-001·002 가 이미 잇고 있다. spec frontmatter 에는 `up:` 없음 — spec 은 decision 계보를 links 로만 탄다.)

## 2. 배경

decision 5건이 accepted 로 닫혔고(PR #32), 미결 중 2건이 사용자 문답으로 추가 확정됐다(§3 확정값).
이제 구현 워커(backend·frontend)가 **이 문서만 읽고 코드를 시작할 수 있는 계약**을 만든다.
SPEC-004(화면 3페이지)는 디자인 세션 귀환 대기라 이번 범위 밖이다 — 채번만 비워 둔다.

## 3. 계약 — 고정값

파일명·ID (전건 `status: draft`, 날짜 2026-09-02, `links.decisions` 는 각 건이 계약화하는 DEC):

| ID | 파일 | 무엇의 계약 | 주 근거 |
|---|---|---|---|
| SPEC-001 | `spec-001-data-layer-contract.md` | 데이터 계층 — 테이블 목록(bronze/silver/gold/ontology)·계층 경계·행수 대조값·마스킹 뷰·적재 게이트 | DEC-001·002, 기록 02~05 |
| SPEC-002 | `spec-002-mcp-tools-contract.md` | 조회 도구 4종 MCP — 파라미터·응답 스키마·에러·뷰 경유 강제 | DEC-002·003, 기록 07·08 |
| SPEC-003 | `spec-003-api-and-chat-contract.md` | FE↔BE API — 계층 조회·KPI·그래프·예보 엔드포인트, 채팅 스트림, 접속 게이트 | DEC-003·004·005 |
| SPEC-005 | `spec-005-agent-loop-and-gates.md` | 에이전트 루프·응답 스키마(`used_edges` 필수)·게이트 5종 수치 기준·회귀 3본 | DEC-003, 기록 08·09 §4 |

(SPEC-004 는 결번으로 남긴다 — 20-spec/README 에 「디자인 귀환 대기」로 표기.)

**사용자 확정값 (2026-09-02 문답 — 이대로 박는다):**

- **마스킹 표기 형식** (SPEC-001): 이름 `김○○`(성만 노출) · 전화 `010-****-1234`(가운데 마스킹) ·
  생년월일 `1990-**-**`(연도만). 리뷰 본문 내 직원 실명은 기록 03/04 의 기존 마스킹 규칙 그대로.
- **접속 게이트** (SPEC-003): env 난수 비밀번호 **하나** (예: `ONTOLOGY_DEMO_PASSWORD` — 값은
  배포 시 사용자가 직접 주입, 문서·레포에 값 미기재). 프론트에서 1회 입력 → 세션 성립.
  백 API 는 같은 env 값을 공유하는 단순 토큰 검증. 내부망 전제 — rate limit·계정·권한 등급 없음.
- **행수 대조값** (SPEC-001): vegas 78,216 · 리뷰 1,962(**csv 파서 기준** — `wc -l` 은 셀 내
  개행으로 2,118 이 나온다, 코디 검증값) · nexus 테이블별 원본 행수 일치. 오차 0.

## 4. 설계 재량과 그 경계

- 도구 파라미터·응답 스키마(SPEC-002), 엔드포인트 경로·응답 shape(SPEC-003), 회귀 3본의
  입력·기대 출력(SPEC-005)은 **기록 07·08 의 실제 사용례·시나리오에서 도출해 네가 제안한다.**
  기록에 근거가 없는 설계 선택은 만들되 **Open Questions 표에 「제안 — 리뷰 필요」로 표시**해라.
- 스키마 전문·ORM·파일 경로 같은 내부 구현은 넣지 않는다(project.md — 스키마 SoT 는 코드).
  spec 에는 외부에 드러나는 것만: 테이블/도구/엔드포인트 이름, 파라미터, enum, 상태, 게이트 수치.
- `trace_ontology` 는 판정(채택/자동 확정/선언/보류/기각) 구분과 기각 사유를 반환에 포함(기록 07 판정 체계).
- 채팅 응답 스키마: `used_edges` 필수 + 수치 인용의 역추적 필드(기록 08 스펙 기반) — SPEC-002·003·005 간 같은 정의를 **한 곳(SPEC-005)에 두고 나머지는 링크**해라.

## 5. allowed_paths — `para/projects/summer-star/ontology-demo/`

## 6. 구현 단계

1. §1 정독(특히 기록 07·08 은 스키마 도출 원천이라 꼼꼼히).
2. SPEC-001 → 002 → 005 → 003 순으로 작성(의존 방향).
3. 동기 갱신 — `20-spec/README.md`(4행 + SPEC-004 결번 표기), `10-decision/README.md` 미결 표
   (마스킹 표기·가드 위치 → 해당 SPEC 으로 해소 표기), 각 DEC 의 Resulting Spec 표(미정 → 실 SPEC ID),
   제품 `README.md` 현재 상태, `log.md`.
4. 자체 점검 후 §7 보고 — 「제안 — 리뷰 필요」 목록을 반드시 명시.

## 7. 하지 말 것 / 검증 / 완료 보고

- work 선작성 금지 · spec 본문에 work ID 금지 · PII 원값 금지 · 기록에 없는 수치 발명 금지(제안은 §4 규칙으로) · 커밋·push 금지.
- 검증: 기계 검증 없음 — frontmatter·links·index·log 동기 자체 점검. 판정은 코디 검증 + 사용자 리뷰.
- 완료 보고: 직전 태스크와 동일 2채널, preamble 의 taskId·dispatchId·코디handle(`term_45e793be-0adb-44c7-9d9a-eb35c4f48320`) 사용.

```bash
orca orchestration send --to term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --from <네 워커handle> \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "docs 완료: SPEC 4건" --body "변경 파일 / 요약 / 제안-리뷰필요 목록 / 미결"
orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 \
  --text "[worker_done] docs 완료 — SPEC-001·002·003·005. 상세는 인박스." --enter
```
