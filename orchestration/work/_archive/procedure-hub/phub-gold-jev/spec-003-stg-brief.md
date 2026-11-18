# [writer] SPEC-003 stg 판(gold 를 app.main 에 붙임 · 일회성 적재) + WORK-018

너는 **procedure-hub `writer` 워커**다. 앞 판 맥락이 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/writer/role.md`(+ 같은 폴더 문서). 회사 레포 — 비밀값 · 접속 값 · 내부 주소 값 쓰지 마라.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(HEAD fdc155b · 읽기만).

## 정본

- 결정: `$W/_RESUME.md` §2 맨 위 11-18 행(「stg gold = app.main 에 붙임」 · 「stg 시드 = 일회성 적재」 · 「배포로 닫는다」 · 「승인 없이 이어서」).
- 조사: `$W/research-stg-seed.md`(7 항목 · 반입 절차 초안 · 근거 줄).
- 계약: `$W/SPEC-003-hub-gold-db.md`(D-7 열림 자리) · `$W/SPEC-001-hub-gold-mcp.md` 0.8.1 · `$W/SPEC-007-image-data.md`(적재기 V13).
- 코드: `$H/backend/app/main.py` · `app/gold_main.py` · `app/modules/gold/db_inputs.py`(F2) · `config.py` · `Dockerfile` · `.dockerignore` · `scripts/load_medallion.py` · `docs/guides/deployment.md` · `docs/adr/0004-*`.

## 쓸 것

### `$W/SPEC-003-hub-gold-db.md` → 다음 판(변경 기록에)
1. **D-7 닫음**: gold REST · MCP 를 `app.main` 에 마운트(경로는 gold 설정 기본값 그대로) · `app.gold_main` 은 로컬 단독 실행용으로 남김(동작 같음). 기동 규칙: `GOLD_REPOSITORY=db` 이고 `medallion_build` 에 행이 있으면 시작 때 메모리 색인 · **행 0 · 해시 불일치 · 적재 오류면 gold 만 꺼짐(`app.main` 은 정상 기동 · 기존 API · health 불변)** — 꺼진 gold 의 REST/MCP 응답 꼴(상태 코드 · 오류 꼴 — SPEC-001 오류 표 꼴로) · 꺼짐 이유를 로그 · gold health 에. `GOLD_REPOSITORY` 가 없거나 `csv` 면? (stg 는 db 만 — CSV 판은 로컬) 정리. 켜기 = 적재 뒤 컨테이너 재시작.
2. **레포 데이터 폴더**: 루트 `data/medallion/`(silver CSV 59 · gold CSV 15 · `notes/ledger-check-list.csv` · 원장 JSON 21 — 자리 · 이름 · README) · 생성 스크립트는 안 넣음(까닭) · build context · CD 트리거 밖.
3. **적재기 이미지 포함**: Dockerfile 에 `scripts/load_medallion.py` 한 줄(데이터는 안 실음) · 일회성 컨테이너 실행 꼴(env 이름 · 마운트 · `--dry-run` → 적재 · exit code) · 되돌리기(적재 실패 = 롤백 · 이전 판 그대로 · alembic downgrade 쓰지 않음).
4. **stg 반입 절차서(사용자가 VM 에서 직접)**: 순서 · 명령 꼴(값은 자리표시) · 확인 지점(alembic current · dry-run 요약 · 적재 요약 · 재시작 · gold health 해시) · 실패 때 멈출 곳.
5. 시험 몫: 빈 표 기동(gold 꺼짐 · app.main health 200) · 적재 뒤 기동(gold 켜짐) · 해시 불일치 · CI(SQLite · 데이터 env 없음)에서 기존 시험 그대로 통과.

### `$W/WORK-018-hub-stg.md`
WP: ① 데이터 폴더 반입(복사 원천 경로 · 개수 · sha 대조 · `.gitignore` 확인) ② app.main 마운트 + 꺼짐 기동 ③ Dockerfile 적재기 한 줄 · 적재기 기본 경로(`data/medallion/`) ④ 시험(그 WP 시험만 · 전체 pytest 금지 — 단 CD verify 가 도는 꼴(SQLite · `alembic check` · ruff)을 로컬에서 한 번 흉내) ⑤ 로컬 실물(18107: 빈 DB 로 기동 → gold 꺼짐 확인 · 로컬 PG 18432 로 기동 → gold 켜짐 · 18105 와 응답 같음) · 18105 · 18108 · 18432 데이터 건드리지 마라(빈 DB 시험은 임시 DB 이름으로). 커밋 금지(코디).

## allowed_paths

쓰기: `$W/SPEC-003-hub-gold-db.md` · `$W/WORK-018-hub-stg.md` 둘만. 코드 · 데이터 · 서버 금지.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer(SPEC-003 stg · WORK-018) 완료: <한 줄>" \
  --body "변경 파일 / D-7 계약 요약 / WP 수 / 정할 것" \
  --outcome succeeded

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] writer(SPEC-003 stg) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
