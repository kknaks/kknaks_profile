# [reviewer_code] 허브 코드 검수 — WORK-018 stg 판(gold 를 app.main 에 붙임)

**앞 판 맥락 없음.** `phub-gold-jev-review-code-hub-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 꼴만(그 브리프의 옛 「볼 것」 은 무시 · 핸들은 preamble 값). 워크트리 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(HEAD fdc155b 위 미커밋). **고치지 마라 · stash · checkout 금지.** 회사 레포 — 비밀값 · 내부 주소 값 쓰지 마라.

읽을 것: `SPEC-003-hub-gold-db.md` 0.2.0 §11 · `WORK-018-hub-stg.md` · `impl-hub-stg-instructions.md`(검수 R-1~R-4 코디 답) · `review-spec-003-stg.md` · `_RESUME.md` §2 맨 위 11-18 행(MCP 421 고침 포함) · `research-stg-seed.md`(stg 구조).

## 볼 것 — 이번 배포가 **기존 stg 허브를 죽이거나 깨뜨릴 길**이 우선

1. `app.main` 기동: gold 의 어떤 실패(접속 · F1~F7 · 시간 초과 · import · 설정 생성 · 예외)에도 app.main 이 뜨고 기존 health · API 가 그대로인가 — 코드 경로를 따라가 확인. 데몬 스레드 · 늦게 끝난 적재 버림의 경합 · 자원 누수.
2. 기존 동작 불변: `test_public_api_contract` · health · OpenAPI · lifespan.py 본문 · glossary 등 기존 라우터 wiring(시험 끝 재wire 가 운영 코드에 영향 없나) · `app.main` import 시간.
3. CD verify 를 깨는 길: SQLite 판 pytest 전체에서 새 시험이 데이터 env 없이 skip/통과 · `alembic check` · ruff · Docker 빌드(`.dockerignore` · COPY 한 줄).
4. 503 본문에 대상 값 0(R-1) · MCP 허용 호스트 기본값 = 보호 켬 · 값 있을 때만 더함.
5. `data/medallion/` — 원천과 sha 같음 · 크기 · 비밀 0 · CD 트리거 밖.
6. **직접 돌려라**: WORK-018 의 시험 묶음(전체 pytest 아님 — 단 CD 와 같은 SQLite 판으로 `tests/` 전체를 한 번 돌려 기존 시험이 안 깨지는지는 확인해도 된다 — 이번 배포가 stg CD 를 통과해야 하므로 예외로 허용). 서버는 띄우지 마라.

## 산출

`review-code-hub-stg.md` 1개(같은 폴더). PASS/WARN/FAIL + 지적 표(파일:줄 · 심각도 · 근거 · 고칠 방향) + 「stg 배포를 막을 것」 목록.
