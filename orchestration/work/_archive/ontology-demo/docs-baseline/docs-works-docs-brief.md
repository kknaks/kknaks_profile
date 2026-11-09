
# [docs] 30-work — WORK-001~010 작성 (WP 분할)

너는 **ontology-demo `docs` 워커**다. 같은 워크트리, 같은 규칙.
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline`
직전 산출물(spec 5건)은 커밋됨(2523b40) — 그 위에 쌓는다.

## 1. SSOT

- `20-spec/` SPEC-001~005 — **work 는 spec 의 조합·순서화다. spec 본문을 복사하지 않는다.**
- `para/projects/project.md` §3.2 work 규칙 + `templates/projects/30-work/work.md`
  (WORK-010 은 `work-release.md`) + `30-work/README.md` 양식(Status Board·Spec Coverage)
- 모범: `para/projects/summer-star/kknaks-dev/30-work/work-023-recruiter-chat-backend.md`
- 구현 환경 사실: 백 `app/ontology-agent/`(FastAPI 스캐폴드 존재) · 프론트 `app/front/`
  (Next.js 15) · LLM 인프라 = `app/back` compose 의 redis + open-kknaks codex 워커
  (queue=ontology 분리) · 원천 데이터·산출 DB 는 워커 로컬(ONTOLOGY_DATA_DIR env)

## 2. 계약 — WP 분할 (코디 확정 · 2026-09-02 개정: 10건 → **5건**, 작업 단위는 WP 안 phase 로 쪼갠다)

| ID | 파일 slug | 담당 | 내용 (specs) | 의존 |
|---|---|---|---|---|
| WORK-001 | `data-foundation` | be | 데이터 기반 전체 — DB 스키마·마스킹 뷰 · 브론즈 적재 · 실버·골드 빌드 DB 이식(+월 View) · 온톨로지 적재(고아 0). SPEC-001. **게이트 1(행수 대사)·2(빌드 재현)** | — |
| WORK-002 | `tools-and-api` | be | 조회 도구 4종 FastMCP 서버 + 계층·KPI·그래프·예보 API + 접속 게이트 인증. SPEC-002 · SPEC-003(채팅 제외) | 001 |
| WORK-003 | `agent-loop-and-chat` | be | 에이전트 루프(open-kknaks·codex) + 채팅 API. SPEC-005 + SPEC-003 채팅 절. **게이트 4(회귀 3본)·5(근거 무결성)** | 002 |
| WORK-004 | `frontend-three-screens` | fe | 프론트 전체 — phase 로 분해: P1 셸·토큰 레이어 `--ont-*`·Pretendard·접속 게이트 화면·라우팅(U-1~3) → P2 모니터링(U-4~7) → P3 데이터(U-13~15) → P4 채팅(U-8~12). SPEC-004 | P1~P3 은 002 이후, P4 는 003 이후. BE 와 병렬 진행 |
| WORK-005 | `integration-and-deploy` | be+fe | 통합 검증(게이트 1~5 전건 재실행·PII 0건 스캔·회귀 자동화) + 배포(홈서버 compose·NPM 서브도메인·Vercel env·비번 주입 절차). DEC-005. `work_type: release` | 003·004 |

- frontmatter `roles`: be = `@ontology-be`, fe = `@ontology-fe` (fe 워커는 발주 준비 때 코디가 신설 — 이름만 이렇게 쓴다).
- **phase 가 태스크 단위다** — WP 당 3~5개, 각 phase 에 Status(TODO)·실행 내용·**완료 증거**(게이트 수치·테스트·화면 확인 방법)를 적는다. 발주·재개·검증이 phase 단위로 돈다.
- 게이트 5종(SPEC-005 §게이트) 배치: 1·2 → WORK-001, 4·5 → WORK-003, 전건 재실행+3(PII) → WORK-005.
- 이미 쓴 `work-001-db-foundation-and-bronze.md` 는 **새 WORK-001(data-foundation)로 갈아엎는다** — 파일명도 위 slug 로.
- rollback 절: DB 산출물은 재빌드로 복원(파괴적 마이그레이션 없음), 프론트는 라우트 그룹 삭제로 원복 — 이 수준이면 된다.

## 3. 동기 갱신

`30-work/README.md`(Status Board 10행 · Spec Coverage — spec 별 커버 WP derived view) ·
각 spec frontmatter 는 **손대지 않는다**(SPEC→WORK 단방향, work 의 `links.specs` 만) ·
제품 README 현재 상태 · log.md.

## 4. 하지 말 것

- 분할·의존 변경 금지(발견한 문제는 질문으로). spec 본문 복사 금지. 코드 착수 금지.
- PII·커밋·push 금지. allowed_paths(`para/projects/summer-star/ontology-demo/`) 밖 금지.

## 5. 완료 보고 — 동일 2채널 (preamble 값, 코디 `term_45e793be-0adb-44c7-9d9a-eb35c4f48320`)

body 에: 변경 파일 / WP 별 phase 수·게이트 배치 / Spec Coverage 요약 / 질문·미결.
