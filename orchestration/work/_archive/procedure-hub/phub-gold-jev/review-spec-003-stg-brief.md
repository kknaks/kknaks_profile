# [reviewer] SPEC-003 0.2.0 §11 · WORK-018 검수(stg 판)

너는 **procedure-hub 문서 검수 워커**다(read-only). 앞 판 맥락이 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/` 아래 reviewer(없으면 researcher) `role.md`. 회사 레포 — 비밀값 · 내부 주소 값 쓰지 마라.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 허브(읽기만) `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(fdc155b).

대상: `$W/SPEC-003-hub-gold-db.md` 0.2.0 §11 · 변경 기록 · `$W/WORK-018-hub-stg.md`. 정본 `$W/_RESUME.md` §2 맨 위 11-18 행(「stg gold = app.main 에 붙임」 · 「SPEC-003 0.2.0 정할 것 코디 답」 · 「stg 시드 = 일회성 적재」). 근거 `$W/research-stg-seed.md` · 작성 브리프 `$W/spec-003-stg-brief.md`.

## 볼 것(짧게 · 구현 막을 것만)

1. **기존 stg 허브를 죽일 길이 남았나**: app.main 기동이 gold 의 어떤 실패에도 살아남나(접속 · 행 0 · 해시 · import · 메모리 · 예외 종류 전부) · lifespan 순서 · CD verify(SQLite · `alembic check` · pytest · ruff)를 깨는 길 · `test_public_api_contract` · OpenAPI 영향.
2. **절차서 ①~⑨**: 순서가 맞나(GOLD_REPOSITORY=db env 를 CD 전에 · `docker restart` 가 env 를 다시 안 읽는 점) · 실패 때 멈출 곳 · 되돌리기(downgrade 금지) · 사용자가 그대로 따라 할 수 있나 · 값 자리표시만.
3. 데이터 폴더(`data/medallion/` · silver 59 · gold 16 · notes · bronze 24) · Dockerfile 한 줄 · `.dockerignore` · 적재기 기본 경로 — 이미지 · 레포 · CI 트리거 영향.
4. WORK-018 WP ↔ SPEC §11 줄 대응 · 시험 범위(그 WP 시험만) · 로컬 실물이 18105 · 18108 · 18432 데이터를 안 건드리나.

## 산출

`$W/review-spec-003-stg.md` 1개: PASS / WARN / FAIL + 한 줄 · 결함 표 · 「구현 전 꼭 고칠 것」.

## 하지 마라

쓰기 1개만. 수정 · 서버 · stg 접속 금지.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer(SPEC-003 stg) 완료: <PASS|WARN|FAIL> <한 줄>" \
  --body "결함 수 / 구현 전 꼭 고칠 것" \
  --outcome succeeded

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] reviewer(SPEC-003 stg) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
