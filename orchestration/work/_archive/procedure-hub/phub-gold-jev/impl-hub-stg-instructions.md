# [backend] 허브 stg 판 구현 — WORK-018(SPEC-003 0.2.0 §11)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-be-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 꼴만 써라(핸들은 preamble 값 · 그 브리프의 WORK-001 · 18105 문구는 옛 판). 워크트리 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(HEAD fdc155b · **커밋 금지** · 회사 레포 — 비밀값 · 접속 문자열 · 내부 주소 값 금지).

**이번 일 = `WORK-018-hub-stg.md` WP-1 ~ WP-5.** 계약 = `SPEC-003-hub-gold-db.md` 0.2.0 §11 · `SPEC-001-hub-gold-mcp.md` 0.8.1. 결정 = `_RESUME.md` §2 맨 위 11-18 행. 검수 `review-spec-003-stg.md` 반영 — 아래가 코디 답(이대로 · SPEC 문장 되적기는 코디가 마감 때).

## 검수 반영

- **R-1**: 꺼짐 503 본문에는 **F 코드 + 짧은 사유만**(DB 호스트 · 포트 · DB 이름 등 대상 값 금지) — 대상은 서버 로그에만.
- **R-2**: `app.main` 안 gold 적재에 **시간 한도**(설정값 · 기본 제안 60초 — 근거 보고) — 넘으면 gold 만 꺼짐 · 허브 기동은 막지 않는다(백그라운드로 돌릴지 · lifespan 안 한도로 할지 네가 고르고 까닭 보고 · 어느 쪽이든 「gold 때문에 app.main 이 안 뜨는 길 0」).
- **R-3**: SPEC §11 절차서는 코디가 고치니 코드 몫은 없음 — 다만 로컬 실물에서 gold 켜진 상태의 **메모리(RSS)를 재서 보고**(절차서 ① · ⑦ 재료).
- **R-4**: WORK §6-2 ③ 시험 목록에 `app.main` 을 import 하는 시험 3 파일(glossary_router · glossary_template · corpus_import_publication)을 더해 그 WP 에서 돈다.
- 나머지 Low(③ 마이그레이션 실패 · 설정 생성 실패 범위 · CD 90초 창 · 끄기 명령 · ⑨ 호스트 가림 · IMG 고르기 · 부록 B · 시험이 앱 전역을 재사용하지 않게)는 코드에 닿는 것만 반영(시험 격리 · 설정 생성 실패도 gold 만 꺼짐).

## 데이터 반입(WP-1)

원천 — 복사만 · 원천 수정 금지: silver-model `…/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/{silver,gold,notes/ledger-check-list.csv}` · 원장 `…/orchestration/work/phub-recommend/bronze/phub-ledger/`. 경로 앞머리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온`. sha256 대조 · 개수 · `.gitignore` 확인. Procedure Hub 데이터는 공개 정보다.

## ⚠ 시험 — 사용자 지시

**WP 마다 그 WP 시험 파일만 · 전체 pytest 금지.** 단 WORK 가 정한 「CD verify 꼴 한 번」(SQLite · `alembic check` · ruff · 그 시험 묶음)은 한 번 돈다. 돌린 파일 · 수 보고.

## 포트 · 실물

18107 만 · 빈 DB 시험은 **로컬 PG 18432 에 임시 DB 이름**을 새로 만들어 쓰고 끝나면 지움(`phub_medallion` 은 읽기만 · 적재 금지). 18105 · 18108 · 18220 · 18222 · 18106 프로세스 건드리지 마라. 접속 값은 `~/.config/phub/medallion-pg.env` 를 `set -a; . 파일; set +a` 로만. Docker 빌드(SE3)는 로컬에서 해도 됨 · push 금지.

## 보고

WP 끝마다 `[진행] backend: …` 한 줄 · 완료에 RSS · 적재 시간 · 「코디: 커밋 · push · PR」.
