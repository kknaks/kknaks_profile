# [backend] 허브 구현 — WORK-010(SPEC-003 0.1.0 로컬 DB 화)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-be-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · SSOT · allowed_paths(`backend/`) · 제약 · §8 검증 · §9 완료 보고 그대로(핸들은 preamble 값). 워크트리 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(HEAD 85c28af 위에 이어서 · 커밋하지 마라). 11-17 사용자 결정: Procedure Hub 데이터는 공개 정보 — 「회사 데이터 본문 0」 은 이 데이터에 걸지 않는다. **비밀값 · 접속 문자열은 어디에도 찍지 마라(그대로).**

**이번 일 = `WORK-010-hub-db.md`(같은 폴더) WP-0 ~ WP-4 전부.** 계약 = `SPEC-003-hub-gold-db.md` 0.1.0. `_RESUME.md` §2 11-17 행(U-1 · U-2 · 검수 뒤 코디 W-1~W-4 · WORK B-1~B-3) · 검수 `review-spec-003.md` · `review-work-010.md` 반영.

## 코디 답 · 받을 것

- **접속 값(B-1)**: `~/.config/phub/medallion-pg.env`(KEY=VALUE · `DATABASE_URL` asyncpg 꼴 · DB 이름 `phub_medallion` · 127.0.0.1:18432). 올리는 법은 `set -a; . ~/.config/phub/medallion-pg.env; set +a` **만** — `cat` · `echo` · 로그 · 보고에 찍지 마라. 컨테이너 `phub-medallion-pg` 는 내리거나 다시 만들지 마라(지금 빈 DB · public 테이블 0).
- **답 키(B-2 · N-1)**: 앱 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev/data/eval-set/calls/`(37 파일 · 원소 `tool` · `request` · `kinds`)와 형제 `answer-key/` — 읽기만.
- **18107(B-3 · N-2)**: WP-4 끝에 네 프로세스를 스스로 내리고 `lsof -nP -iTCP:18107 -sTCP:LISTEN` 0 줄을 보고에. 18105 · 18106 · 18220 · 18210 · 18005 는 건드리지 마라.
- **W-1**: 합성 시험 설정이 프로세스 env 를 물려받지 않게 — `settings_for` 에 `GOLD_REPOSITORY=csv` · `DATABASE_URL` 빈 값을 박는다(`tests/gold_fixture.py` 고쳐도 된다). §8-1 ⑤ 의 PostgreSQL URL pytest 에서는 `test_medallion_*` 를 뺀다(합성 적재가 로컬 PG 를 덮지 않게).
- **W-2**: WP-0 에 O-6 둘째 물음 더함 — 「모델에 없는 테이블을 `alembic check` 가 잡나」 실물로.
- **W-3**: DT10 두 판 대조는 같은 `medallion_fixture` 폴더로(aux_hash 같게).
- **N-4**: 「모르는 `GOLD_REPOSITORY` 값 = 시작 실패」 판정은 lifespan 에서(설정 검증기 X · DT12 꼴).
- NOTE 나머지(N-3 수 · N-5 · N-6 · N-7 · N-8)는 WORK 그대로 + 보고에 한 줄.

## 단계 보고

- WP-0 끝나면 결과(지연 FK · alembic check · pytest 시간 앞뒤 · 242 · 순환 0)를 `[진행] backend: WP-0 …` 한 줄로 코디에게(§9 의 (2) 방식) 보내고 **이어서 진행**(막히면 `[질문]`).
- 완료 조건: WORK §9 1 · 2 · 4(워커 몫) — DE7(18105 교체 · 앱 37 키)은 코디 몫이니 하지 마라.
- 기준선: 기존 pytest(CSV 판) 한 줄도 안 바뀌고 통과 — 바뀐 fixture 줄 · 이름 · 까닭 목록 보고.
