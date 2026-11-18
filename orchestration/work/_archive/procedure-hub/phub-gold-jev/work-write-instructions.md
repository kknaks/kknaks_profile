# WORK-001 · WORK-002 작성 지시서 (구현 계획)

**너는 앞 판의 맥락이 없다.** 먼저 `phub-gold-jev-write-brief.md`(같은 폴더) 의 역할 · 제약(공개 레포 · 외부 API · .env · 코드 레포 변경 금지) · §8 검증 · §9 완료 보고를 그대로 적용한다. **allowed_paths 는 이번엔 아래 두 파일만**(SPEC 은 고치지 마라 — 구멍을 찾으면 보고에 적어라).

`P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` · `W=$P/orchestration/work/phub-gold-jev`

## 읽을 것

1. `$W/_RESUME.md` §2 결정 표 전체 ← 정본
2. `$W/SPEC-001-hub-gold-mcp.md` · `$W/SPEC-002-chat-eval.md`(0.4.1 · 검수 PASS r5) ← **계약. 여기 없는 건 발명하지 마라**
3. `$W/review-spec-001-002-r5.md` §Z-1 ~ Z-3(구현 때 한 줄씩 정할 것)
4. 코드 레포(읽기만):
   - 허브: `~/git/PROCEDURE-HUB` 를 `git show origin/release/v1.2.0:<경로>` 로 — `AGENTS.md` · `backend/README.md`(「검증」 절) · `backend/app/` 구조 · `backend/Dockerfile` · `docs/guides/`. 옛 틀: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`(`git show HEAD:` — `backend/app/graph_main.py` · `modules/gold/{mcp_server,container,service,memory,resolve}.py`)
   - 앱: `~/git/clinic_chat` 를 `git show origin/main:<경로>`(README · pyproject · 구조) · 옛 틀: `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`(`git show HEAD:` — `clients/{jev_client,hub_mcp,hub_rest}.py` · `llm/cli.py` · `runs.py` · `timing.py` · `tests/fake_jev.py`)
5. Jev: `$P/para/resources/note/ai/llms.txt`

## 쓸 것

### `$W/WORK-001-hub.md` — 허브 구현 계획(PROCEDURE-HUB · 새 브랜치 `kknaksss/phub-gold-jev` base `origin/release/v1.2.0`)

frontmatter(type: work · id · links → SPEC-001 · 0.1.0). WP 단위로 나눈다(예: WP-1 적재 · repository · 색인 / WP-2 service + 도구 8 · REST / WP-3 MCP 마운트 · 진입점 · health / WP-4 시험). WP 마다:
- 목표 · SPEC-001 절 대응 · **만들 파일 경로(실제 레포 구조에 맞춰)** · 옛 틀에서 가져올 것(파일:줄)
- 완료 조건(검사 가능한 문장) · 검증 명령(레포 README 「검증」 절 기준 · `DATABASE_URL=sqlite+aiosqlite:///:memory:` · 데이터 env 없으면 skip · 데이터 env 있으면 37 문항 `gold_pointers` 되짚기)
- 사용자 포트 · 프로세스 · 개발/운영 DB 금지 · 로컬 실행 방법(포트는 **18005 와 겹치지 않는 새 포트** 제안 — 사용자 e2e 용)
- 데이터 env 이름 · 경로(SPEC-001 §2 · 로컬 `SM/gold` · silver · notes 경로)

### `$W/WORK-002-app.md` — 앱 구현 계획(clinic_chat · 새 브랜치 `kknaksss/phub-gold-jev` base `origin/main`)

WP 예: WP-1 클라이언트(Jev · 허브 REST/MCP · CLI LLM — 옛 틀 가져오기) / WP-2 A 열 원장 로컬 stdio MCP 3 / WP-3 B 열 걷기(①~⑤ · RG1~RG8 · 입구 고르기 · FT 묶음 표 · 깊이 · 종료 상태 · gate) / WP-4 C 열(LLM + 허브 MCP 직접) / WP-5 기록(runs.jsonl · trace) / WP-6 **전체 답 키 스크립트**(SPEC-002 §9-5 — 결과는 gitignore 로컬 · 사용자 확인 절차) / WP-7 채점 두 층 + 보고서 / WP-8 batch 실행기 + **사용자 e2e 실행 안내**(한 질문 · 한 열 · 전체 세트 명령 · 어디서 결과를 보나).
WP 마다 WORK-001 과 같은 항목. 추가로:
- **실물 확인 단계**(외부 서비스 경로는 실물 호출 1회가 완료 조건): Jev 1회 · `claude -p` Sonnet 1회(추론 끔 가능 여부 첫 확인 · 안 되면 가장 낮은 effort) · Haiku 1회 · 허브 로컬 서버 1회. 키는 앱 `.env`(gitignore)에서 읽음 — 문서엔 env 이름만.
- 시험 세트 파일 69 문항 · 모범 답 원문은 **gitignore 로컬 파일**(자리 · 이름 제안). 질문 문장은 이 문서에 쓰지 마라.
- r5 Z-1 ~ Z-3 를 해당 WP 에 한 줄씩.

### 두 문서 공통

- 순서 · 의존(WORK-001 WP-2 계약이 서면 WORK-002 는 모의 허브로 병행 가능한지 — 근거와 함께 제안)
- 코드 레포 allowed_paths(허브 `backend/` · 앱 레포 전체에서 무엇) · 커밋 · push 는 코디 몫
- 열린 것(구현 때 정함으로 SPEC 이 넘긴 것 — 번호 그대로 · 이번에 정할 제안값)

## 검증

- 두 문서의 모든 WP 가 SPEC 절을 가리키는지 · SPEC 의 구현 대상 절 중 WP 에 안 걸린 것 0(표로)
- 파일 경로가 실제 레포 구조와 맞는지(`git show … --name-only` · `git ls-tree` 로 확인한 결과)
- 공개 grep 0
