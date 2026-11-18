# [researcher] silver · gold DB 화 — stg 에 테이블을 올리기 위한 설계 조사

너는 **procedure-hub `researcher` 워커**다(read-only). 앞 판의 맥락이 없다 — 아래 「읽을 것」만으로 일한다.
먼저 역할 문서를 읽어라(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리(코디 워크트리 · 공유): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온`
**코디가 같은 트리에서 일한다 — 리포트 파일 1개 외에는 아무것도 만들거나 고치지 마라.**

경로 접두어:
- `P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온`
- `W=$P/orchestration/work/phub-gold-jev` (이번 작업 폴더)
- `SM=$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model` (gitignore · 로컬 데이터)
- `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev` (허브 · 회사 레포 · 브랜치 `kknaksss/phub-gold-jev` · base `origin/release/v1.2.0` · **미커밋 gold 모듈이 있다 — 읽기만**)

## 1. 배경

허브는 지금 gold CSV 15표 + silver 보조 입력을 **시작 때 메모리로** 읽는다(router → service → repository · repository 만 DB 로 바꾸게 지어 둠 — `$W/_RESUME.md` §2 11-16 「D2 저장」 결정).
이번에 **silver · gold 를 DB 테이블로 만들어 허브 stg 에 올린다.** 같은 허브 워크트리 `$H` 에 alembic 으로 추가하는 전제다.
그 위에서 채팅(상담)을 Anthropic SDK 로 짓는다(`$W/_RESUME.md` 11-16 D8 결정) — 이번 조사 범위는 **DB 만**.

**정해진 것(다시 논의하지 마라)**
- 실패한 옛 브랜치 `kknaksss/phub-recommend`(PR #31)의 graph · gold 스키마 · 시드는 **버린다.** 왜 실패했는지(되풀이 막기)만 본다.
- `release/v1.2.0` 의 기존 테이블(`canonical_*` · `legacy_prod` 등)은 stg/prod 에서 응답 중 — **건드리지 않는 전제**로 새 테이블을 옆에 둔다. 기존 테이블과 겹치거나 부딪히는 곳이 있으면 사실만 적는다.
- 새 데이터 기준 = silver 57 · gold 15(11-16 확정). 옛 25타입 247필드 · 옛 gold 노드 체계는 기준으로 끌어오지 마라.

## 2. 읽을 것

**새 데이터**
- `$SM/gold/README.md` · `semantic-map.md` · `gold-final-notes.md` · `gold-build.py` · `gold-check.py` · `silver-supplement.py` · `g_*.csv`(15)
- `$SM/notes/silver-erd.md` · `silver-tables.md` · `glossary.md` · `$SM/silver/`(57표)
- `$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/_RESUME.md` §2 (11-16 gold 결정: 「관계형 먼저 + 그래프 내보내기」 · 근거 표 참조)

**지금 허브(메모리 판)** — `$H/backend/app/modules/gold/*`(특히 `repository.py` · `memory.py` · `inputs.py` · `headers.py` · `closure.py` · `concern.py` · `ledger.py` · `config.py`) · `$H/backend/app/router/gold.py` · `$H/backend/app/gold_main.py` · `$H/backend/envs/.env.example`(값 없음 꼴만) · 계약 `$W/SPEC-001-hub-gold-mcp.md`(0.6.0)

**허브 기존 DB · 배포** — `$H/AGENTS.md`(첫 줄의 `/Users/marin/...` 는 무시) · `$H/backend/README.md` · `$H/backend/alembic/` · `alembic.ini` · `$H/backend/app/model/` · `$H/backend/app/repository/` · `$H/backend/import-data/` · `$H/backend/app/importing/` · `$H/docs/guides/{design,deployment,prod-migration,prod-db-rename}.md` · `$H/.github/workflows/csp-azure-deploy.yml` · `$H/docs/README.md`(ADR 지도)
- `origin/stg` · `origin/prod` 과 `release/v1.2.0` 의 차이: `git -C $H log --oneline origin/release/v1.2.0..origin/stg` 등 **읽기 명령만**(fetch 금지)

**실패한 옛 판(되풀이 막기만)** — `git -C $H show origin/kknaksss/phub-recommend:<경로>` 로 `backend/alembic/versions/b2026103*` · `backend/app/model/{gold,graph}.py` · `backend/app/modules/gold/build.py` · `$P/orchestration/work/phub-recommend/_RESUME.md` §2(11-08 중단 · ERD 바탕 틀림)

**기준 개념** — `$P/para/areas/concept/cs/artifact-traceability.md`(gold 행 → silver 근거 되짚기)

## 3. 계약

해당 없음(조사).

## 4. 질문 — 답마다 근거(파일:줄 · 표.칸 · 셈 명령과 결과)

**Q1. 허브 기존 DB 와 stg 반영 길**
- DB 엔진 · 접속 설정 꼴 · alembic 체인(헤드) · 테이블 소유(모듈별) · 스키마(네임스페이스) 쓰는 법 · 시드/적재 방식(`import-data` · `importing`).
- stg 에 새 테이블이 올라가는 길: 마이그레이션이 언제 · 누가 도나(배포 워크플로 · 수동 절차) · freeze guard · 이름 전환 등 **새 테이블 추가 때 지켜야 할 것**. 데이터 반입(시드)은 어떻게 하나.
- 새 테이블을 별도 스키마(예: `gold`)로 둘 수 있나 · 기존 테이블과 이름 · FK 충돌.

**Q2. silver · gold → 테이블**
- 15 gold 표 · 57 silver 표 각각: 키 · 행 수 · 칸 수 · 다른 표와 잇는 칸 · 값 종류(문자 · 수 · 목록 · 빈칸 비율).
- 허브가 실제로 읽는 범위(메모리 판 `inputs.py` 기준): gold 15 전부 · silver 는 어디까지(`source_ref` · concern/adverse/condition 계층 · concern_site · 원장 확인 목록 등). **DB 에 올릴 범위 선택지**(a) gold 15 + 허브가 읽는 silver 만 (b) silver 57 전부 + gold 15 (c) 그 밖 — 각각 행 수 · 위험 · 되짚기(근거 경로 끊기나).
- 표 → 테이블 대응 초안(표 1:1 · 칸 타입 · PK/FK · 인덱스 후보). **기준: 「담을 칸 없는 값 0」** — 칸 값을 실제로 쪼개 보고(목록 · 묶음 · 여러 값 든 칸) 1:1 로 안 맞는 칸을 전부 센다.

**Q3. 적재 · 빌드 추적**
- 지금 `gold_hash` · `aux_hash` 를 어떻게 셈하나(파일:줄) · 응답 머리에 어떻게 싣나.
- DB 판에서 옮기는 법 선택지: 빌드(판) 테이블 + 표마다 판 칸 / 판 하나만 살아 있게 전체 교체 / 그 밖. 재적재 · 되돌리기 · stg 와 로컬 같은 판 확인.
- 원천 CSV 를 어디서 가져와 적재하나(지금 로컬 gitignore). 회사 데이터라 **공개 레포(kknaks_profile · clinic_chat) 금지** — 허브 레포 안 · 바깥 저장소 등 선택지만.

**Q4. repository 교체 자리**
- 메모리 repository 인터페이스(메서드 · 쓰는 곳 전부 — grep 으로 전수) · 메모리에서 미리 지어 두는 색인(closure · 계층 펼침 · resolve 사전 등).
- DB 로 바꿀 때 각각: 쿼리로 / 시작 때 DB 에서 읽어 메모리 색인 그대로 / 빌드 때 테이블로 미리 — 선택지와 응답 속도 영향(지금 gold+Jev 0.7s).
- 기존 시험(`$H/backend/tests/test_gold_*`)이 DB 판에서 어떻게 돌 수 있나.

**Q5. 옛 판(PR #31) 실패와 대조**
- 옛 스키마가 어디서 틀렸나(11-08 기록 기준) · 새 안이 같은 실수를 하지 않으려면 무엇을 확인해야 하나 — 한 줄씩.

**Q6. 정할 것**
- 리포트 머리에 요약(질문당 2~3줄) + **「정할 것」 표**(사용자가 고를 것만 · 각각 추천 · 근거 · 위험). 결정하지 마라.

## 5. allowed_paths — 이 밖은 건드리지 마라

- **쓰기: `$W/research-db.md` 1개만.** 임시 파일은 네 세션 scratchpad 에만.

## 6. 진행

1. 「읽을 것」 → Q1 → Q6. 셈은 python/csv 로 직접 하고 명령을 리포트에 남긴다.
2. 리포트 머리에 요약 + 정할 것 표, 본문에 근거.

## 7. 하지 말 것

- 결정하지 마라 — 추천만, 「정할 것」 으로.
- DB · 서버 · docker 를 띄우거나 접속하지 마라(로컬 · stg · prod 전부). `.env` 를 열지 마라 · 키 · 접속 문자열 출력 금지. 외부 API 호출 금지.
- `$H` 작업 트리를 바꾸지 마라(stash · checkout · reset · fetch · 파일 수정 금지). 다른 브랜치는 `git show <ref>:<경로>` 로만.
- 사용자 포트 18210 · 18005 · 실행 중인 18105 · 18220 건드리지 마라.
- **공개 레포 리포트다 — 회사 데이터 본문 0.** 표 이름 · 칸 이름 · id · 셈까지만. 시술 설명 · 원장 문장 · 가격 값 · 내부 URL · 비밀값 금지.
- silver/gold 를 고치지 마라(`gold-check.py` 는 돌려도 된다).
- 디스크 여유가 적다 — 큰 파일 만들지 마라.

## 8. 검증

질문마다 답 + 근거. 확인 못 한 것은 「확인 안 됨」. 끝내기 전 `git -C $P status --porcelain` 에서 네 변경이 리포트 1개뿐인지 · 리포트에 회사 데이터 본문이 없는지 확인.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다. 다르면 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 / 요약 / 셈 수치 / 정할 것 개수 / 미결·주의점"

# (2) 직접 주입 — 코디를 깨운다
orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] researcher(DB) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고:
  `orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 --text "[질문] researcher(DB): <질문>" --enter`
