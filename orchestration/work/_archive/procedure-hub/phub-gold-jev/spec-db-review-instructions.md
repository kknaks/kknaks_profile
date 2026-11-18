# SPEC-003 0.1.0 검수 지시서(로컬 DB 화)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-review-doc-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 그대로(핸들은 preamble 값). 단 **11-17 사용자 결정: Procedure Hub 데이터(원장 · silver · gold)는 공개 정보 — 브리프 §8 의 「회사 데이터 본문 0」 은 이 데이터에 걸지 않는다.** 비밀값 · 내부 호스트/URL · 실명 0 은 그대로 본다.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(읽기만 · HEAD 85c28af) · `SM=…/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`

읽을 것: `$W/spec-db-instructions.md`(지시 · 「정해진 것」) · `$W/_RESUME.md` §2 11-17 행 · `$W/research-db.md` · `$W/SPEC-003-hub-gold-db.md` · 대조용 `$W/SPEC-001-hub-gold-mcp.md` §2 · §3-1 · `$H/backend/app/modules/gold/*` · `$H/backend/alembic/` · `$H/backend/app/model/base.py` · `$H/backend/tests/`(create_all 쓰는 곳).

할 것:
1. 지시 「할 것」 1~8 이 문서:줄로 닫혔나 표 · 「정해진 것」(D-0~D-8) 위반 0.
2. **재셈**: 표 72+2 대응 빠짐 0 · 행 · 칸 수 · silver FK 80칸 중 빈칸 든 35칸 · 빈칸 12,968 · gold_hash 8accbb21 · aux_hash 6435fe41 재현 · 기존 167 · 옛 브랜치 이름과 겹침 0. 다르면 세는 식까지.
3. **DB 판 = CSV 판 같은 결과**가 계약으로 닫혔나(값 왕복 · NULL↔'' · 행 순서 load_seq · 해시 · 도구 응답 동일 시험) — 메모리 색인을 그대로 세우는 길에서 빠지는 입력 없나(inputs.py 가 읽는 것 전부 grep 전수).
4. alembic · 모델 · SQLite create_all(28 파일) · CI `alembic check` 에서 깨질 곳 · 지연 FK(O-6) 위험이 WORK 첫 WP 로 막혔나 · revision id 겹침.
5. 적재 CLI 한 트랜잭션 교체 · 실패 때 그대로 · exit code · dry-run 계약 구멍.
6. 로컬 실행(§6): 포트 18210 · 18005 · 18105 · 18220 과 안 겹침 · 기존 허브 테이블 167 을 건드리는 명령 없음.
7. U-1 · U-2 추천이 결정 · 원칙과 맞나 · 그 밖 숨은 사용자 결정 0.
8. **최종**: PASS 면 「U-1 · U-2 정해지면 WORK 진행 가능」 명시.

산출: `$W/review-spec-003.md` 1개만.
