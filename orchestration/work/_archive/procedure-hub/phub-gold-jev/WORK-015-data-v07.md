---
type: work
id: WORK-015
title: "데이터 판 구현 계획 — concern_site 보강(7고민 8행) + 그림 데이터(silver 표 2 → DB 테이블 2 · 에셋 103) 재빌드 한 번 · 재적재 · 37 키 대조"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.1.0
created_at: 2026-11-17
updated_at: 2026-11-17
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/work
  - status/draft
links:
  specs:
    - "orchestration/work/phub-gold-jev/SPEC-007-image-data.md (0.1.0 · 검수 PASS — FAIL 0 · WARN 1 · NOTE 6 · review-spec-007.md) ← 계약(그림 · 재빌드 11단계)"
    - "orchestration/work/phub-gold-jev/SPEC-003-hub-gold-db.md (0.1.0 — 테이블 규칙 R1 ~ R10 · 적재 V · L · 빌드 기록)"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.7.2 — §5-11 SP1 · 「보강 뒤 어림 ①」 · T22 · T28)"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 — 「SPEC-007 U7-1~3 = 추천」 · 「정정 — 그림은 DB 까지 이번 판 · 출력은 다음 스펙」 · 「규칙 변경 = 넣음 … concern_site 보강 판정 = 추천 → 7고민 8행(95→103)」 · 「concern_site 보강은 한 번에 · 코드 구현 끝난 뒤」 · 「순차 진행 · 시험은 구현한 것만 돌림(전체 테스트 안 돌림)」 · 「서버 시드 방식 · 원천 CSV 자리 · stg gold 진입점은 대기」 · 「Procedure Hub 데이터는 공개 정보」)"
  sources:
    - "orchestration/work/phub-gold-jev/research-concern-site.md (§4 행 초안 · 근거 경로 표 · §5-3 37 키 · §6 추천 7고민 8행)"
    - "orchestration/work/phub-gold-jev/review-spec-007.md (W-1 gold-check A3 · N-1 ~ N-6 — 이 문서 §11)"
  related:
    - "orchestration/work/phub-gold-jev/WORK-010-hub-db.md (앞 허브 DB WORK — 꼴 · 접속 값 · 포트 규칙)"
    - "orchestration/work/phub-gold-jev/WORK-013-hub-v07.md (허브 0.7.2 — 지금 다른 워커가 구현 중 · 이 문서의 허브 쪽은 그 뒤)"
    - "orchestration/work/phub-gold-jev/WORK-009-v06.md (앱 답 키 다시 뽑기 · 대조 걸음)"
---

# WORK-015 — 데이터 판 구현 계획(concern_site 보강 + 그림 데이터 재빌드)

> 경로 접두어: `P` = 프로필 워크트리 · `W` = `$P/orchestration/work/phub-gold-jev` · `SM` = `$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬 데이터 · 스크립트까지 통째로 무시됨) · `I` = `$P/reference/2026-11-17-procedure-images`(그림 시드 · 미추적 · 읽기만) · `H` = `~/orca/workspaces/PROCEDURE-HUB/phub-gold-jev` · `B` = `$H/backend` · `A` = `~/orca/workspaces/clinic_chat/phub-gold-jev`(앱 · 읽기만).
> **계약은 SPEC-007 0.1.0(그림 · 재빌드 순서)과 보강 조사 §4 · §6(7고민 8행)이다.** 이 문서는 「어느 파일을 · 어떤 순서로 · 누가 · 무엇으로 확인하나 · 어떻게 되돌리나」 만 정한다. SPEC · 조사에 없는 것을 만들지 않는다 — 어긋나면 고쳐 맞추지 말고 보고한다(§12).
> **사용자 결정은 닫혔다**(_RESUME §2 11-17): SPEC-007 U7-1 ~ U7-3 = 추천(gold 에 그림 안 넣음 · 이번 판 `kind = silver` · 에셋 폴더 = 허브 레포 루트 `assets/procedure-images/`) · 보강 = 추천 7고민 8행 · 재빌드는 한 번에 · 허브 구현(0.7.2)이 끝난 뒤.
> 데이터(원장 · silver · gold) · 그림은 공개 정보다(11-17). **비밀값 · 접속 문자열 · 내부 주소 금지는 그대로다.** 이 문서에는 표 · 칸 · 코드 · 경로 · 셈만 있다 — 그림 라벨 글자 · 접속 값은 없다.

## 0. 요약

- WP 다섯 · 순서대로: **WP-1 silver**(보강 8행 + 근거 19행 · 그림 표 2 · 스키마 · silver-check) → **WP-2 gold**(재빌드 · gold-check A1 · **A3** · 해시) → **WP-3 허브**(계약 상수 · alembic 74 → 76 · 적재기 V13 · 에셋 103) → **WP-4 DB 재적재**(로컬 18432) → **WP-5 37 키 대조 · 0.7.2 SP 재셈**.
- 누가: WP-1 · WP-2 = **데이터 워커**(`$SM` 만 고친다) / WP-3 · WP-4 = **backend 워커**(`$H` 만 고친다 · 0.7.2 구현이 끝난 HEAD 위) / WP-5 · 18105 재시작 · 로컬 PG 띄우기 = **코디**.
- **검수 WARN 1 을 닫는 법**(§11 W-1): 보강의 8행 · 근거 19행을 손으로 덧붙이지 않고 **`silver-supplement.py` 에 5번째 단계로 넣는다** — 그 스크립트는 인자 없이 돌면 기준 사본에서 silver 를 통째로 다시 쓰므로, 스크립트 밖에서 고친 `concern_site.csv` 는 다음 실행 때 지워진다(§1). gold-check 는 **A1(허용 목록) · A3(재현 대상)** 둘 다 고친다.
- 해시: **`gold_hash` 는 안 바뀐다(기대 · WP-2 에서 확인 — 다르면 멈춘다)** · **`aux_hash` 는 바뀐다**(보강의 두 파일 `concern_site.csv` · `source_ref.csv` 때문 — 그림 때문이 아니다) · silver 폴더 전체 해시는 바뀐다.
- 37 답 키: **행이 바뀌는 문항 0(기대)** · `build.aux_hash` 만 다르다. 기준 키는 **적재 앞에**(0.7.2 코드 · 보강 전 데이터로) 백업해 둔다 — 코드 변화와 데이터 변화가 섞이지 않게(§7).
- 시험은 **그 WP 것만** 돌린다. 전체 pytest · 전체 batch 는 어느 WP 에서도 돌리지 않는다(_RESUME §2 11-17). 돌린 파일 · 명령을 보고에 적는다.
- **데이터는 커밋 대상이 아니다**(`$SM` 은 gitignore — 서버 시드 방식이 정해지기 전). 허브 레포에 들어가는 것은 **코드 + 에셋(SVG 103 + README)** 뿐이다.

## 1. 지금(11-17 확인 — 읽기만 · 돌려 보지 않은 것은 그렇게 적었다)

| 무엇 | 지금 | 이번에 뜻하는 것 |
|---|---|---|
| silver | CSV **57** · **66,936**행 · `concern_site.csv` 95행(끝 `CSI-0098` · 빈 번호 `CSI-0038` · `0073` · `0074`) · `source_ref.csv` 48,094행(그 가운데 `target_table = concern_site` **574** · `field` 전부 빈칸) | 보강 뒤 `concern_site` **103** · `source_ref` **48,113**(`concern_site` 593) · 그림 뒤 CSV **59** · **67,853**행 |
| gold | 15표 + `questions.csv` · `gold_hash` = `8accbb21…f6228c`(이 워커 재셈 — `gold-check.py:46-50` 식 · SPEC-003 §2-5 값과 같다) | 불변(기대) |
| `gold/silver-supplement.py`(250줄) | 기준 = `archive/silver-before-gold-final/silver`. **기준 사본의 파일을 전부 `silver/` 로 복사한 뒤**(`:203-204`) `procedure_relation` · `product_procedure` · `source_ref` 를 다시 쓴다. `source_ref.csv` = 기준 바이트 + 덧붙임 목록(`:237-239`) · 인자로 폴더를 주면 그 폴더에만 쓴다(`:21-24`) | **보강을 스크립트 밖에서 하면 다음 실행 때 `concern_site.csv` 가 95행으로 되돌아간다** → 보강은 이 스크립트 안에(§3-2). 새 그림 두 CSV 는 기준 사본에 없어 이 스크립트가 건드리지 않는다 |
| `gold/gold-check.py` A1(`:66-102`) | 기준 사본의 파일마다 — `procedure_relation` · `source_ref` 밖은 **바이트가 같아야** 한다(`:89-90`) · `source_ref` 덧붙임은 `product_procedure` 또는 (`procedure_relation`, `same_day_text`) 뿐(`:86-88`) · 표 목록 = 기준 + `product_procedure` + `external_code`(`:91-94`) | 셋 다 걸린다 — `concern_site.csv` 바뀜 · 덧붙임 목록 밖 · 표 목록 2 추가 → A1 을 고친다(§4) |
| `gold/gold-check.py` A3(`:105-116`) | `silver-supplement.py` 를 임시 폴더에 돌려 `procedure_relation` · `product_procedure` · `source_ref` 3 파일 + 판정 표를 바이트로 견준다 | 재현 대상에 `concern_site.csv` 를 더한다(§4 — 검수 W-1) |
| **git 환경 검사** | silver-check **G3**(`silver-check.py:907-911`) · gold-check **G1**(`:418-422`)은 `git status` 줄에 옛 경로 글자 `orchestration/work/phub-ledger-redesign/` 가 없으면 FAIL 이다. 이 워크트리는 그 폴더가 `_archive/…` 로 옮겨졌고 다른 미추적 파일이 있어 **데이터와 무관하게 걸린다** — `check-stats.json`(11-16)의 FAIL 1 이 그 G3 이다. gold-check **A2** 는 silver-check 끝 줄이 `PASS (WARN 0)` 인지 보므로 함께 걸린다 | SPEC-007 의 「silver-check PASS」 · 「gold-check PASS」 를 이 워크트리에서 글자 그대로는 못 얻는다 — **판정 기준을 §2 에 문장으로 정한다**(· §12 B-1). 돌려 보지는 않았다(두 검사 모두 파일을 쓴다) |
| `drafts/glossary/schema-edit.py` | `silver-schema.json` 을 **기준 사본에서 통째로 다시 쓴다**(`external_code` 표를 이 스크립트가 넣었다) | 스키마를 손으로만 고치면 이 스크립트를 다시 돌릴 때 사라진다 → 두 표 · 층 ⑤ 는 이 스크립트에 넣는다(§3-4 · §12 A-2) |
| `notes/vocabulary.csv` | 값마다 `n_rows` 칸이 있다 — `source_ref.target_table` 의 값별 행 수가 들어 있다 | 근거 19행 · 그림 두 표가 들어가면 수가 달라진다 → `glossary-build.py` 로 다시 뽑는다(gold-check V1 이 「지금 파일 = 다시 뽑은 것」 을 본다) |
| 근거 경로 | 조사 §4 의 8행에 딸린 경로 **19** 를 `silver-check.py` 의 `resolve()` 로 풀었다 — 19 / 19 가 원장 글자로 풀린다(이 워커 · 읽기만). 8 짝은 지금 `concern_site` 에 없고(중복 0) 고민 · 부위 코드는 전부 사전에 있다 | S1(포인터 해석) · R1 · C11(같은 연결 중복)에 안 걸린다(기대) |
| 그림 시드 `$I` | `image-assets.csv` · `image-labels.csv` · `images/mechanism/MEC-NNN.svg` **54** · `images/method/MET-NNN.svg` **49**(대표 이름으로 센 수) · 그 밖 `previews/` · `legacy-source/` · 제작 지시 · `image-map.csv` · 미추적 · gitignore 아님 | 읽기만 · 대표 103 만 허브로 |
| 허브 `$H` | HEAD `daa54e3` · **작업 트리에 0.7.x 변경이 있다**(수정 13 · 새 파일 3 — 다른 워커가 구현 중) · `assets/` 없음 · `backend/alembic/versions` 끝 `b202611170001` · `LOADER_VERSION = "load_medallion 0.1.0"`(`medallion_load.py:36`) · `SILVER_UNIQUES`(`model/medallion.py:49`) · `GOLD_IMAGE_DIR` 없음(`config.py`) | **WP-3 은 0.7.2 구현 · 검수가 끝나 커밋된 HEAD 위에서 한다** — 줄 번호는 그때 grep 으로 다시 본다(검수 N-3) |
| 허브 시험에 박힌 **보강 관련** 수 | `tests/test_gold_holes.py:410`(`concern_site` 행 **95**) · `:426`(`health.aux.concern_site` = 행 95 · 고민 85 · 부위 51) — 실물(데이터 env) 시험이다 | 보강 뒤 **103 · 92 · 52**(이 워커 재셈). SPEC-007 부록 B ⑧ 목록(그림 쪽 수)에는 없는 자리다 — WP-3 이 함께 고친다(§5-3) |
| 포트 | 듣는 중: 18105 · 18106 · 18210 · 18220 · 18222. **18432(로컬 PostgreSQL)는 지금 닫혀 있다**(`nc` 로 본 값 · `docker ps` 출력 없음) · 18107 은 비어 있다 | WP-4 앞에 코디가 로컬 PG 를 다시 띄운다(§12 B-2). 데이터가 남아 있는지는 띄운 뒤 본다 |
| 앱 `$A` | `data/` 는 gitignore · `data/eval-set/answer-key/` 37 · `calls/` 37 · 앞 판 폴더 `_v041` · `_v051` · `_v052a` ~ `c` · `_v06a` · `_v06db_csv` · 키의 `build` = `gold_hash` · `aux_hash` 두 칸 · `answer_key --diff` 가 두 해시의 앞 · 뒤를 찍는다(`evalset/answer_key.py:511-512,544-546`) · 확인 잇기는 키 전체가 같을 때만(WORK-009 §15 B-2) · 작업 트리에 0.3 변경이 있다(다른 워커) | `aux_hash` 가 달라져 확인이 저절로 이어지지 않는다 → 대조 뒤 코디가 `--confirm`(§7) |

## 2. 공통

| 항목 | 이번 판 |
|---|---|
| 고치는 자리 — 데이터 워커(WP-1 · WP-2) | `$SM` 안만: `gold/silver-supplement.py` · 새 `gold/silver-image.py` · `gold/gold-check.py` · `drafts/silver-check/{silver-schema.json, silver-check.py, check-stats.json}` · `drafts/glossary/{schema-edit.py, glossary-build.py}` · `notes/{silver-erd.md, silver-tables.md, vocabulary.csv, glossary.md}` · `silver/{concern_site, source_ref, concept_image, concept_image_label}.csv` · 새 사본 폴더 `archive/silver-before-data-v07/`. **`gold/gold-build.py` · gold 15표 · `questions.csv` · 사전(`mechanism` · `method` · `concern` · `site`) · `$I` 는 고치지 않는다**(gold CSV 는 재빌드가 같은 바이트로 다시 쓴다) |
| 고치는 자리 — backend 워커(WP-3 · WP-4) | `$H` 안만 — 목록은 §5-1. `$SM` · `$I` · `$A` 는 읽기만 |
| 데이터 · 커밋 | `$SM` 은 전부 gitignore — **커밋 대상이 아니다**(서버 시드 결정 전 · SPEC-007 G-12). 허브 레포에는 코드 + 에셋만 — silver CSV · 시드 CSV · dump · 접속 값을 넣지 않는다. 커밋 · push · PR 은 코디 몫 |
| 시험 | **그 WP 의 시험 · 명령만.** 전체 pytest(`--ignore=tests/integration`) · 전체 batch 는 돌리지 않는다. 돌린 것 목록 · 통과 / skip 수를 보고에 적는다 |
| **「PASS」 의 판정**(§1 git 환경) | silver-check = **G3 밖 FAIL 0 · WARN 0**(출력의 「걸린 것」 줄이 G3 뿐) / gold-check = **A2 · G1 밖 FAIL 0 · 구조 문제 0**(A2 는 silver-check 끝 줄이 G3 때문에 `PASS` 가 아니라서 걸린다 — 그래서 silver-check 를 **따로 한 번** 돌려 위 기준으로 본다). 걸린 줄을 보고에 그대로 붙인다. 두 검사의 git 필터를 고치는 것은 이 WORK 의 기본이 아니다(§12 B-1) |
| 접속 값 | 로컬 PostgreSQL 접속 값은 레포 밖 파일 — 코디가 발주서에 적은 방법으로 **프로세스 env 에 올리기만** 한다(WORK-010 §2 그대로 · 찍지 않는다) |
| 포트 · 프로세스 | 워커는 **18107 에만** 허브를 띄웠다 내린다(띄우기 전 `lsof -nP -iTCP:18107 -sTCP:LISTEN`). 18105 · 18106 · 18210 · 18220 · 18222 를 내리거나 띄우지 않는다 · PostgreSQL 컨테이너를 내리거나 다시 만들지 않는다. **WP-1 ~ WP-3 사이에는 떠 있는 허브를 다시 띄우지 않고 · 적재기를 돌리지 않는다**(CSV 판은 다시 뜰 때 보강된 보조 입력을 읽고 · 옛 적재기는 계약 밖 CSV 로 exit 2 다 — SPEC-007 §8-1) |
| 시작 문(gate) | **`$SM/silver` 에 쓰는 걸음(§3-5 ④)은 코디의 시작 신호 뒤에만** — 허브 0.7.2 구현 워커가 같은 폴더를 데이터 env 로 읽어 실물 시험(행 95 · `filter` 191 짝)을 돌린다. 그 앞에는 스크립트 · 스키마 편집과 **임시 폴더 출력**까지만 한다(두 스크립트 모두 폴더 인자를 받는다) |

## 3. WP-1 — silver(데이터 워커)

**목표**: `concern_site` 8행과 그 근거, 그림 표 2 를 silver 에 올리고 silver-check 가 새 층까지 본다.
**대응**: SPEC-007 §2 · §3 · §4 · §8-1 1 ~ 5 · §10-1 IS1 ~ IS3 · 보강 조사 §4 · §6 · §7 끝 줄.

### 3-1. 사본(맨 먼저)

`$SM/archive/silver-before-data-v07/` 에 — `silver/`(57 CSV) · `gold/`(CSV 16) · `notes/`(`vocabulary.csv` · `glossary.md` · `silver-erd.md` · `silver-tables.md`) · `scripts/`(`silver-supplement.py` · `gold-check.py` · `silver-check.py` · `silver-schema.json` · `check-stats.json` · `schema-edit.py` · `glossary-build.py`). 전례 = `archive/silver-before-*` 21 폴더. 사본의 파일 수 · `silver_sha256`(지금 `check-stats.json` 값 `2471b2f1…fc6918`)을 보고에 적는다.

### 3-2. concern_site 8행 · 근거 19행

**행**(id 는 조사 §4-1 → §4-2 순 · 결정이 뺀 행 제외 · `CSI-0099` 부터 — 빈 번호는 채우지 않는다):

| id | concern_code | site_code | 등급 | 근거 경로(= `source_ref.ref` · `field` 빈칸) | 경로 수 |
|---|---|---|---|---|---:|
| `CSI-0099` | `CON-200` | `SITE-083` | 가 | `extracted.json:/M5/indications/extended/1` · `extracted.json:/M4/indications/extended/2` · `extracted.json:/M12/indications/extended/1` · `taxonomy.json:/modality/4/extracted/indications/extended/1` · `taxonomy.json:/modality/3/extracted/indications/extended/2` · `taxonomy.json:/modality/11/extracted/indications/extended/1` · `market-pricing.json:/categories/11/items/5/name` · `market-pricing.json:/categories/16/items/3/name` | 8 |
| `CSI-0100` | `CON-193` | `SITE-103` | 가 | `taxonomy.json:/modality/15/subcategories/6/items/10/extracted/indications/primary/0` | 1 |
| `CSI-0101` | `CON-193` | `SITE-109` | 가 | 위와 같음 | 1 |
| `CSI-0102` | `CON-162` | `SITE-076` | 나 | `taxonomy.json:/modality/0/subcategories/2/items/1/name` · `…/items/1/extracted/indications/primary/1` | 2 |
| `CSI-0103` | `CON-166` | `SITE-117` | 나 | `taxonomy.json:/modality/0/subcategories/2/items/2/detail` · `…/items/2/extracted/indications/primary/2` | 2 |
| `CSI-0104` | `CON-190` | `SITE-112` | 나 | `taxonomy.json:/modality/15/subcategories/6/items/9/name` · `…/items/9/detail` | 2 |
| `CSI-0105` | `CON-209` | `SITE-083` | 나 | `taxonomy.json:/modality/14/subcategories/9/items/5/name` · `…/items/5/extracted/indications/primary/1` | 2 |
| `CSI-0106` | `CON-176` | `SITE-035` | 가(이름) | `extracted.json:/M1/indications/extended/5` | 1 |

- 합 **8행 · 근거 19행**. 경로는 조사 §4-1 · §4-2 표 **그대로**다(더하지도 빼지도 않는다 — 예: `CON-176` 은 같은 글자의 `taxonomy.json` 쪽 경로가 조사 §3-2 에 있지만 §4-2 표에는 한 경로다 → 한 행).
- 넣지 않는 것(결정): 조사 §4-1 의 `CON-156` 2행 · `CON-133` · `CON-269`(윗고민 뒤집힘 — 「정할 것 2」 (b)) · §4-2 의 `CON-122`(모공 막힘) · 불독살 · 부위 코드 없는 3. **`site` 사전은 고치지 않는다.**

**어떻게 쓰나 — `silver-supplement.py` 의 5번째 단계**(검수 W-1 의 ⓐ):

| 만들 것 | 내용 |
|---|---|
| 상수 | 위 표를 그대로 옮긴 목록 하나(id · 고민 · 부위 · 경로들) — 스크립트 머리말 docstring 에 「5. concern_site 보강(사용자 11-17 · 조사 §4 · §6)」 한 줄 |
| `concern_site.csv` | **기준 사본 바이트 + 끝에 8줄**(기존 95행 바이트 그대로 · BOM · `\n`). 다시 돌려도 같은 바이트 |
| `source_ref.csv` | 덧붙임 목록의 **맨 끝**(지금 끝인 사용자 11-16 의 3행 뒤)에 19행 — `concern_site,<id>,,<경로>` · 표의 순서대로. 앞 48,094행 바이트 그대로 |
| 쓰기 전 확인 | 8 짝이 기준 `concern_site` 에 없다 · 고민 · 부위 코드가 사전에 있다 · 19 경로가 `resolve()` 로 글자로 풀린다 — 하나라도 어긋나면 `SystemExit`(스크립트의 기존 꼴) |
| 끝 줄 출력 | `concern_site +8 · source_ref +19` 를 지금 요약 줄 옆에 |

- 폴더 인자를 준 실행(`<폴더>/silver`)에서도 같은 두 파일이 나와야 한다 — A3 가 그것을 견준다(§4).
- **`concern.csv` 의 설명 문장은 고치지 않는다**(조사 §7 끝 줄 — `CON-190` · `CON-162` 의 설명이 「자리를 따로 적지 않는다」 꼴이다). 고치면 `concern.csv` 가 보조 입력이라 `aux_hash` 가 한 파일 더 바뀌고, gold 가 고민 사전을 읽으므로 `gold_hash` 까지 닿을 수 있다 — 결정에 없는 변경이다(§12 B-3).

### 3-3. 그림 → silver: 새 `gold/silver-image.py`

SPEC-007 §3 그대로 — 입력 `$I`(인자 또는 env · 기본 `$I`)의 `image-assets.csv` · `image-labels.csv` · `images/` + `silver/mechanism.csv` · `method.csv`(대조만) → 출력 `silver/concept_image.csv`(103행 · 7칸 · `CIM-0001` ~ `0103`) · `concept_image_label.csv`(787행 · 6칸 · `CIL-0001` ~ `0787`). 칸 · 번호 · 값 바꿈은 SPEC §2-2 ~ §2-4. 쓰기 전 검사 **K1 ~ K6**(§3 표) — 하나라도 어긋나면 쓰지 않고 끝. 폴더 인자를 주면 그 폴더에만 쓴다 · 다시 돌려 같은 바이트 · 그림 파일은 읽기만(sha256 대조).

### 3-4. 스키마 · silver-check · 문서 · 값 목록(SPEC §4 의 여섯 가운데 다섯 — gold-check 는 §4)

| 무엇 | 어디 | 내용 |
|---|---|---|
| 스키마 | `drafts/glossary/schema-edit.py` → `silver-schema.json` | `layers` 에 「⑤」(매체) · `tables` 에 두 표(SPEC §4 첫 줄의 꼴 — `key` · `id_pattern` · `columns` · `fk: concept_image` · `poly` · `vocab` 셋). **`schema-edit.py` 에 넣어 다시 돌린다**(§1 — 전례 `external_code`). 손으로만 고쳤다면 그 사실을 보고한다(§12 A-2) |
| silver-check | `drafts/silver-check/silver-check.py` | ① 층 ⑤ 의 표는 「행 근거 ≥ 1」(D4 · D5 · C7 · E1 · O1)의 대상이 아니다(지금 식은 ① ~ ④ 밖을 D5 로 보낸다) ② **I1 ~ I5**(SPEC §4 표 · I5 는 시드 폴더가 없으면 건너뛰고 그렇게 찍는다) ③ `--negative` 에 I 마다 하나 ④ 머리말의 「57표」 문장 |
| 문서 | `notes/silver-erd.md` · `silver-tables.md` | `silver-check.py --write-docs` 로만 다시 쓴다 |
| 값 목록 | `drafts/glossary/glossary-build.py` → `notes/vocabulary.csv` | 묶음 「표 이름」 에 `concept_image.target_table` · 「번역 언어」 에 `concept_image_label.lang` · 새 묶음 「그림 검수 상태」(`concept_image.medical_review` · 값 `검수 전` · 뜻은 SPEC-007 §2-2 의 문장만 — 지어 쓰지 않는다). 다시 뽑으면 보강의 `source_ref` 행 수도 함께 반영된다 |
| 용어집 | `notes/glossary.md` | 표 둘 · 접두어 `CIM-` · `CIL-` 줄 · `concern_site` 줄은 그대로(행 수를 적은 문장이 있으면 103 으로) |

### 3-5. 순서 · 완료 조건 · 명령

걸음: ① 사본(§3-1) → ② 스크립트 · 스키마 편집(§3-2 ~ §3-4 · §4 의 gold-check 까지 같이 고쳐 둔다) → ③ **임시 폴더로 먼저**: `silver-supplement.py <임시>` · `silver-image.py <임시>` → 행 수 · 바이트 확인 → ④ **(코디 시작 신호 뒤)** 실제 `silver/` 에: `silver-supplement.py` → `silver-image.py` → `glossary-build.py` → `silver-check.py --write-docs` → ⑤ `silver-check.py` · `silver-check.py --negative`.

완료 조건:
1. **IS1** — 두 그림 파일 103 · 787행 · 다시 돌려 같은 바이트 · **그 밖 silver 파일 가운데 바뀐 것은 `concern_site.csv` · `source_ref.csv` 둘뿐**(나머지 55 는 사본과 sha256 이 같다).
2. `concern_site.csv` = 사본 바이트 + 8줄 · `source_ref.csv` = 사본 바이트 + 19줄(앞쪽 바이트 불변을 `cmp` 또는 sha 로 보인다).
3. **IS2** — 깨뜨린 시드(K1 ~ K6 하나씩 · **레포 밖 임시 폴더**) → 쓰지 않고 끝.
4. **IS3** — silver-check 가 §2 의 판정으로 통과(G3 밖 FAIL 0 · WARN 0) · I1 ~ I5 통과 · `--negative` 가 I 마다 「잡음」 · G1(문서 = 스키마) 통과 · `glossary-build.py --check` 끝 줄 `PASS`.
5. 셈: silver CSV **59** · 행 **67,853** · `concern_site` 103(고민 92 · 부위 52) · `source_ref` 48,113 · 새 `silver_sha256` 을 보고에 적는다.

```bash
# $SM 에서 — 이 WP 의 명령은 이것뿐
python3 gold/silver-supplement.py <임시 폴더>          # ③ — silver/ 를 건드리지 않는다
python3 gold/silver-image.py <임시 폴더>               # ③ (인자 꼴은 구현이 정한다 — §12 A-1)
python3 gold/silver-supplement.py                      # ④ — 코디 신호 뒤
python3 gold/silver-image.py
python3 drafts/glossary/glossary-build.py
python3 drafts/silver-check/silver-check.py --write-docs
python3 drafts/silver-check/silver-check.py            # ⑤
python3 drafts/silver-check/silver-check.py --negative
python3 drafts/glossary/glossary-build.py --check
```

**되돌리기**: `archive/silver-before-data-v07/` 의 `silver/` · `notes/` · `scripts/` 를 제자리에 덮고 새 두 CSV · `silver-image.py` 를 지운다 → `silver-check.py` 로 옛 `silver_sha256`(`2471b2f1…`)이 다시 나오는지 본다.

## 4. WP-2 — gold 재빌드 · gold-check · 해시(데이터 워커)

**대응**: SPEC-007 §4 끝 줄(A1) · §5 · §8-1 6 · §8-2 · §10-1 IS4 · 검수 **W-1(A3)** · N-4.

| 고칠 것(`gold/gold-check.py`) | 내용 |
|---|---|
| **A1 — 고정 기대값 보탬** | ① `concern_site.csv` 가지: 「기준 사본 바이트로 시작하고 덧붙은 줄이 8 · id 가 `CSI-0099` ~ `CSI-0106`」 일 때만 통과(그 밖의 변경은 FAIL 그대로) ② `source_ref` 덧붙임 허용 목록에 (`concern_site`, `field` 빈칸) — 그 `target_id` 가 위 8 id 안 ③ 표 목록 기대값에 `concept_image.csv` · `concept_image_label.csv` ④ docstring 의 A1 설명에 한 줄 |
| **A3 — 재현(검수 W-1)** | 견주는 파일을 3 → **4**(`concern_site.csv` 추가). 그림 두 CSV 의 재현은 silver-check **I5** 가 본다(A3 에 넣지 않는다 — 스크립트가 다르다) |
| 그 밖 | K · M · Q · H 검사는 고치지 않는다. `gold-build.py` 는 고치지 않는다 |

걸음: `python3 gold/gold-build.py` → `python3 gold/gold-check.py`(H1 이 재빌드를 한 번 더 돈다).

완료 조건:
1. **`gold_hash` = `8accbb213ac5327d8675f8156bc57d87c12a3245c383c8239074444da7f6228c`**(지금 값). **다르면 멈추고 보고한다** — gold 16 파일 가운데 어느 파일의 sha 가 달라졌는지를 사본(`archive/silver-before-data-v07/gold/`)과 견줘 적는다. 고쳐 맞추지 않는다.
   - 기대의 근거: `gold-build.py` 본문에 `concern_site` 가 없다(SPEC-007 부록 B ⑤) · 새 두 표는 **읽어 들이지만 쓰는 자리가 없다**(`gold-build.py:35` 가 silver 폴더의 CSV 를 전부 읽는다 — 검수 N-4) · 근거 19행은 gold 행이 가리키는 silver 행의 것이 아니다. 「기대」 일 뿐이라 확인이 완료 조건이다.
2. **IS4** — gold-check 가 §2 의 판정으로 통과(A2 · G1 밖 FAIL 0 · 구조 문제 0) · **A1 통과 · A3 통과** · V1 통과.
3. 역검증 둘(레포 밖 임시 사본 또는 되돌릴 수 있는 한 줄로): `concern_site.csv` 끝에 9번째 줄을 더하면 A1 이 FAIL · `silver-supplement.py` 의 보강 상수에서 한 행을 빼고 A3 를 돌리면 FAIL. 원래대로 돌린 뒤 다시 통과를 본다.
4. **해시 표를 보고에 적는다**(앞 · 뒤):

| 값 | 바뀌나 | 까닭 |
|---|---|---|
| `gold_hash` | 안 바뀐다(위 1) | gold 16 파일 바이트 불변 |
| `aux_hash` | **바뀐다** | 보조 입력 6 파일 가운데 `concern_site.csv` · `source_ref.csv` 의 sha256 이 바뀐다(나머지 4 — `concern` · `adverse` · `condition` · 원장 확인 목록 — 불변). 그림 때문에는 안 바뀐다 |
| 파일별 sha256 | 4 파일 | `concern_site.csv` · `source_ref.csv`(바뀜) · `concept_image.csv` · `concept_image_label.csv`(새로) |
| silver 폴더 전체 해시 | 바뀐다 | 위 4 파일 |
| `GOLD_EXPECTED_HASH` | 그대로 | `gold_hash` 만 견준다 |

- 새 `aux_hash` 값은 여기서는 **셈으로** 구해 적는다(허브 식 = 「파일 이름 + 공백 + sha256」 줄을 이어 다시 sha256 — `$B/app/modules/gold/inputs.py` 의 `combined_hash` · 줄 순서는 그 코드가 정본). WP-4 의 dry-run 이 내는 값이 정본이고, 둘이 다르면 보고한다.

**되돌리기**: gold CSV 는 바뀌지 않았어야 한다. 바뀌었다면 사본의 `gold/` 를 덮는다. `gold-check.py` 는 사본의 `scripts/` 에서.

## 5. WP-3 — 허브(backend 워커 · **0.7.2 구현 뒤**)

**전제**: 허브 0.7.2(WORK-013)가 구현 · 코드 검수 · 커밋까지 끝난 HEAD 다(지금은 다른 워커가 구현 중 — §1). 시작할 때 `git status --porcelain` 이 비어 있지 않으면 **멈추고 보고**한다. 0.7.x 는 새 입력 · 새 테이블이 없어 revision 줄은 겹치지 않는다(SPEC-007 §6-2 끝 줄).
**대응**: SPEC-007 §6-1 ~ §6-4 · §7 · §8-1 7 · 8 · §10-2 IT1 ~ IT7.

### 5-1. 고치는 자리

| 만들 · 고칠 것 | 어디 | 내용 |
|---|---|---|
| 계약 상수 | `backend/app/modules/gold/silver_contract.py` | `SILVER_HEADERS` · `SILVER_KEY` 에 두 표 · `SILVER_FK` 에 `concept_image_label.image_id → concept_image` · `SILVER_POLY` 에 `concept_image.target_table`(SPEC §6-2). 칸 이름 · 순서는 WP-1 이 만든 CSV 헤더 = SPEC §2-2 · §2-3 |
| 모델 | `backend/app/model/medallion.py` | `SILVER_UNIQUES` 에 두 표의 유일 묶음 · 머리말의 수(74 · 72 · 82 · 57)만 — 그 밖은 상수에서 기계로 지어진다 |
| 마이그레이션 | 새 `backend/alembic/versions/b202611170002_<이름>.py` | `down_revision = 'b202611170001'` · 테이블 2 · FK 1(지연) · 유일 제약 2 · `load_seq` · 풀어 쓴 고정본(앱 상수 import 0) · `downgrade` = 라벨 → 그림 순. 구현 날이 바뀌면 그날 id(SPEC O7-6). **`b202611170001` 파일은 고치지 않는다** |
| 설정 | `backend/app/modules/gold/config.py` | `GOLD_IMAGE_DIR: str = ""`(적재기만 읽는다 — `gold_main` 은 읽지 않는다) |
| 적재기 | `backend/app/modules/gold/medallion_load.py` · `backend/scripts/load_medallion.py`(주석의 수) | **V13**(SPEC §6-3 — env 가 있으면 표의 경로 103 ↔ 폴더의 `images/**/*.svg` 가 정확히 같고 sha256 이 같다 · 어긋나면 exit 2 · env 가 없으면 건너뛰고 `image_files unchecked(GOLD_IMAGE_DIR 없음)`) · 요약 한 줄 · `LOADER_VERSION = "load_medallion 0.2.0"` · V13 은 dry-run 에서도 돈다(파일 읽기만 · DB 접속 0) |
| 주석의 수 | `backend/app/modules/gold/db_inputs.py`(「나머지 silver 52표」 → 54) | 읽는 범위(P5)는 그대로 — 새 두 표를 읽지 않는다 |
| **박힌 수** | 위 파일들 + `backend/tests/test_medallion_{model,load,repo}.py` · `tests/medallion_fixture.py` | 74 → 76 · 57 → 59 · 52 → 54 · 72 → 74 · 15 → 16 · 82 → 83 · 3 → 5 · 749 → 764 를 **grep 으로 전부** 찾아 고친다(SPEC 부록 B ⑧ 은 그때의 목록일 뿐 — 0.7.x 뒤 줄 번호가 밀렸다). `health.files` 22 를 박은 자리는 **그대로**다(U7-2 (a)) |
| 합성 fixture | `backend/tests/medallion_fixture.py` | 두 표(가짜 코드 · 가짜 글자 — 실제 라벨 · 실제 그림을 넣지 않는다) · FK · 유일 묶음이 한 번씩 걸리게 |
| 시험 | `backend/tests/test_medallion_{model,load,repo}.py` + 새 `backend/tests/test_medallion_image.py`(이름 제안 — V13 · 에셋 폴더) | IT1 ~ IT7(§5-2) |
| 에셋 | 새 `assets/procedure-images/images/mechanism/MEC-NNN.svg` **54** · `…/method/MET-NNN.svg` **49** · `assets/procedure-images/README.md` | `$I/images/{mechanism,method}/` 에서 **이름이 `(MEC\|MET)-\d{3}\.svg` 인 파일만** 복사(별칭 83 · `.gitkeep` · `.DS_Store` · `previews/` · `legacy-source/` · 제작 지시 · 시드 CSV · `image-map.csv` 는 안 옮긴다). README = 판 값 · 규격(SPEC §7-3) · 「의료 검수 전 원리 개념도」 · 파일 수 103 · 대조 방법(V13). **`.dockerignore` · `.gitignore` 는 고치지 않는다**(루트 `assets/` 는 이미 이미지에 안 실린다) |
| 문서 | `backend/README.md` gold 절 · `backend/envs/.env.example` | 테이블 74 → 76 · `GOLD_IMAGE_DIR` 설명 한 줄 · 적재 명령에 그 env. `DATABASE_URL` 줄은 건드리지 않는다 |

손대지 않는 것: `backend/app/main.py` · `backend/app/core/**` · gold 도구 코드(`service` · `concern` · `resolve` · `memory` · `repository` · `mcp_server` · `router/gold.py`) · `health` 응답 · `pyproject.toml` · `uv.lock` · `.github/**` · `Dockerfile`.

### 5-2. 완료 조건(합성 · CI 에서 도는 것)

1. **IT1** 모델 = 계약 — 테이블 76 · silver 59 · 칸 764 · FK 83 · 유일 5 · 인덱스 30 · 이름 ≤ 63 · 중복 0.
2. **IT2** SQLite `create_all` · 새 revision 의 `down_revision` · 헤드 하나 · 옛 세 id 와 다름 · `create_table` 2 · 지연 FK 1.
3. **IT3** 합성 적재 — 행 수 · `load_seq` · 되읽기 · 빌드 기록 76행(`silver` 54).
4. **IT4** 두 표에서 V2 · V5 · V6 · V7 → exit 2 · 쓴 것 0.
5. **IT5** V13 — 일치 = 통과 · 바이트 바꿈 · 파일 빠짐 · 표에 없는 SVG 하나 더 → 각각 exit 2 · env 없음 = `unchecked`.
6. **IT6** 읽는 범위 불변 — DB 판이 새 두 표를 읽지 않는다 · `health.files[]` 22줄 · 기존 합성 도구 시험 통과.
7. **IT7** 에셋 폴더 — SVG 103 · `mechanism/` 54 · `method/` 49 · 그 밖 파일 0(README 제외) · 금지 요소 0 · `viewBox="0 0 1200 800"` 103(SPEC §7-2 A1 · A3).

```bash
# $B 에서 — 이 WP 의 시험은 이 파일들뿐(전체 pytest 금지)
uv run ruff check app tests scripts
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest \
  tests/test_medallion_model.py tests/test_medallion_load.py tests/test_medallion_repo.py tests/test_medallion_image.py -q
uv run alembic heads          # 헤드 하나 — 새 revision
```

### 5-3. 보강 때문에 바뀌는 실물 기대값(데이터 env 시험 — WP-2 가 끝난 `$SM` 을 읽는다)

| 자리 | 지금 | 보강 뒤(이 워커 재셈 — silver CSV) |
|---|---|---|
| `tests/test_gold_holes.py` 의 `concern_site` 행 수 · `health.aux.concern_site`(지금 `:410` · `:426` — 줄 번호는 grep 으로) | 95 · 고민 85 · 부위 51 | **103 · 92 · 52** |
| 0.7.2 가 더한 실물 시험의 짝 수(T28 — 파일은 0.7.2 구현이 정한다 · `191` · `22949` · `8709` 류를 grep) | `sites[]` 있는 고민 100 · `filter` 191 짝 · `prefer` 22,949 짝 | **106 · 200 · 22,940**(SPEC-001 0.7.2 「보강 뒤 어림 ①」 과 같다) · 0 행 짝 5 그대로 |
| 그 밖 실물 수(`CON-001` × `SITE-014` 이름 73행 · `CON-005` × `SITE-051` 이름 54행 등) | — | 그대로(기대 — 여덟 행의 고민 · 윗고민이 아니다). 달라지면 고치지 말고 보고 |

- 이 표의 시험은 **WP-4 의 ⑤**(DB 판 실물)에서 함께 돈다. 고치는 것은 기대값 숫자뿐 — 시험의 식은 그대로다.
- 대상 파일만 돌린다: `GOLD_*` env 넷 + `uv run pytest tests/test_gold_holes.py <0.7.2 의 SP 실물 시험 파일> -q -rs`.

**되돌리기**: 허브 변경은 미커밋으로 남는다 — `git stash push -u -m "<유일한 꼬리표>"`(맨 `git stash` 금지) 또는 파일별 `git checkout -- <경로>` + 새 파일 · `assets/` 삭제. DB 에 새 revision 을 올린 뒤면 §6 의 되돌리기부터.

## 6. WP-4 — DB 재적재(backend 워커 · 로컬 18432)

**전제**: WP-1 ~ WP-3 완료 · 코디가 로컬 PostgreSQL 을 띄워 두었다(§1 — 지금 닫혀 있다) · 접속 값은 프로세스 env.
**대응**: SPEC-007 §8-1 7 · 9 · 10 · §10-3 IE1 ~ IE5.

```bash
# $B 에서 — 접속 값은 코디가 준 방법으로 프로세스 env 에(내용을 찍지 않는다)
# ⓪ 접속 대상 찍기(WORK-010 §8-1 ⓪ 그대로) → 127.0.0.1 18432 <DB> 가 아니면 멈춘다
# ⓪' 지금 판 적기 — 테이블 수 · medallion_build 행 수 · alembic 현재 revision(읽기만)
DATABASE_URL="$DATABASE_URL" uv run alembic current
# ① 스키마 — 프로세스 env 를 붙인 꼴만
DATABASE_URL="$DATABASE_URL" uv run alembic upgrade head      # +2 테이블
DATABASE_URL="$DATABASE_URL" uv run alembic check
DATABASE_URL="$DATABASE_URL" uv run alembic downgrade -1      # 새 두 테이블만 지운다 · 적재 앞에만
DATABASE_URL="$DATABASE_URL" uv run alembic upgrade head
# ② 적재
export GOLD_CSV_DIR=<gold 폴더> GOLD_SILVER_DIR=<silver 폴더> GOLD_LEDGER_CHECK_PATH=<ledger-check-list.csv>
export GOLD_EXPECTED_HASH=<§4 의 gold_hash> GOLD_IMAGE_DIR=<허브 워크트리>/assets/procedure-images
uv run python scripts/load_medallion.py --dry-run             # IE2 — DB 접속 0
uv run python scripts/load_medallion.py                       # IE3
# ③ DB 판 허브 — 18107 만(띄우기 전 lsof) → health · 요청 몇 개 → 내린다
# ④ 실물 pytest — §5-3 의 파일만(GOLD_REPOSITORY=db · PostgreSQL URL 로는 gold · medallion 시험만)
```

| # | 확인 | 기대 |
|---|---|---|
| IE1 | 스키마 | `alembic check` 통과 · `public` **243**(`alembic_version` 넣어 244) · `downgrade -1` → 241(242) → `upgrade head` 다시 243. **SPEC 의 「새 빈 DB」 와 다른 점**: 이 DB 는 이미 `b202611170001` 까지 올라가 옛 판이 실려 있다 — 여기서는 「+2」 왕복만 보고, 빈 DB 에서 처음부터 올리는 것은 CI(`backend-test.yml` 의 `upgrade head` → `check`)가 본다(§12 A-4). 로컬 PG 가 새로 만들어져 비어 있었다면 SPEC 그대로다 |
| IE2 | dry-run | `g_*` · `s_*` 74표 통과 · `s_concept_image` 103 · `s_concept_image_label` 787 · `s_concern_site` **103** · `s_source_ref` **48,113** · `poly_unresolved s_concept_image.target_table 0` · `image_files 103 checked` · `gold_hash` = §4 값 · `aux_hash` = §4 에서 센 값 · 실을 행 **130,446**(gold 62,244 + silver 67,853 + 원장 확인 273 + 빌드 기록 76) |
| IE3 | 적재 | exit 0 · 76 테이블 · 되읽기 차이 0 · FK 위반 0 · 빌드 기록 76행(`loader_version` 0.2.0) · 걸린 시간 |
| IE4 | SQL 한 줄씩 | `s_concept_image.target_code` 집합 = `s_mechanism.code` ∪ `s_method.code`(103) · 라벨 없는 그림 0 · 그림 없는 라벨 0 · `s_concern_site` 의 새 8 id 가 있다 |
| IE5 | 18107 `health`(DB 판) | `build.gold_hash` 불변 · `build.aux_hash` = 새 값 · `files[]` **22줄** · `aux.concern_site` = 행 103 · 고민 92 · 부위 52 · 열쇠 집합이 18105 의 `health` 와 같다(18105 에는 GET 만) |
| ④ | §5-3 의 실물 시험 | 통과 · skip 수 |

- 18107 은 확인 뒤 **내린다**(자기가 띄운 프로세스만 · `lsof` 로 내려간 것을 본다). 18105 는 건드리지 않는다 — 이 시점의 18105 는 **옛 코드 · 옛 메모리**로 떠 있다(DB 판은 시작 때 한 번 읽고 끝이라 적재가 요청에 닿지 않는다). 다만 **18105 를 누가 다시 띄우면 옛 코드는 76행 빌드 기록 · 새 판을 만난다** — 그래서 WP-4 가 끝나면 곧바로 코디에게 알린다(§7).

**되돌리기(DB 판)**:

| 무엇이 필요한가 | 방법 |
|---|---|
| 가장 빠른 길 — 허브만 옛 판으로 | 18105 를 **CSV 판**(`GOLD_REPOSITORY=csv`)으로, 경로 env 를 사본 `archive/silver-before-data-v07/{gold, silver}` 와 원장 확인 목록에 걸어 띄운다 — DB 없이 옛 `gold_hash` · 옛 `aux_hash` 가 뜬다(코디) |
| DB 를 옛 판으로 | `alembic downgrade -1`(새 두 테이블) → 허브를 앞 커밋(0.7.2 끝난 HEAD — WP-3 변경을 치운 상태)으로 → `GOLD_SILVER_DIR` 를 사본의 `silver/` 로 걸어 적재(옛 적재기는 57표 계약이다 · 한 트랜잭션 전체 교체라 멱등) → `health` 의 `aux_hash` 가 옛 값 |
| 적재 도중 실패 | exit 2 = DB 그대로 · exit 3 = 롤백(옛 판 그대로) — 되돌릴 것 없음 |
| dump 로 되돌리기 | 이번 판의 기본이 아니다 — 컨테이너를 다루는 일이라 코디 몫이다(§12 B-2) |

## 7. WP-5 — 37 답 키 대조 · 0.7.2 SP 재셈(코디)

**대응**: SPEC-007 §8-1 10 · 11 · §8-2 · §10-3 IE5 · IE6 · 보강 조사 §5-3 · SPEC-001 0.7.2 §5-11 「보강 뒤 어림 ①」.

| 순서 | 무엇 | 기대 · 주의 |
|---|---|---|
| (가) **적재 앞** | 앱 `data/eval-set/{calls, answer-key, key-summary.md, key-table.md}` 를 **백업 폴더로 먼저** 복사 — 이름 제안 `data/eval-set/_v07a/`(지금 없는 이름 · gitignore 로컬). 그 키가 **0.7.2 코드 · 보강 전 데이터**로 뽑힌 판인지 본다(키의 `script_sha256` · `build.aux_hash` = 옛 값) — 0.7.2 재시작 뒤 아직 안 뽑았다면 **여기서 한 번 뽑아 기준으로** 삼는다 | 코드 변화(0.7.2)와 데이터 변화(보강)를 한 대조에 섞지 않는다. 지금 확인된 키를 덮지 않는다(WORK-010 §8-2 와 같은 규칙) |
| (나) | WP-4 완료 알림 뒤 **18105 를 새 코드 · DB 판으로 다시 띄운다**(앱 18220 · 18222 도 필요하면) → `health`: `gold_hash` 불변 · `aux_hash` = WP-4 값 · `files[]` 22줄 | 18105 는 앱 · 사용자 e2e 가 보는 포트다 |
| (다) | 앱에서 `uv run python -m clinic_chat.evalset.answer_key --all` → `… answer_key --diff _v07a --diff-out key-diff-v07-data.md` → `… key_table --prev _v07a` | **37 / 37 행 같음 · 다른 것은 `build.aux_hash` 하나**(대조 파일 끝 줄 `aux_hash 앞·뒤` 에 두 값 · `gold_hash 앞·뒤` 는 한 값). **바뀌는 문항이 있으면 문항 id · 다른 칸을 그대로 보고**하고 확인을 잇지 않는다 |
| (라) | 확인 잇기 — 37 전부 같음이 보였으면 `answer_key --confirm <37 id> --by <사용자>`(근거 = `key-diff-v07-data.md`) | `aux_hash` 가 달라 키 파일이 같지 않으므로 자동 잇기가 안 된다(WORK-009 §15 B-2 와 같은 꼴) |
| (마) **SP 재셈** | 보강 뒤 0.7.2 의 짝 수를 다시 본다 — 허브 실물 시험(WP-4 ④)의 결과 + 18105 에 조회 세 번 | `sites[]` 있는 고민 **106** · `filter` **200** 짝 · `prefer` **22,940** 짝 · 0 행 짝 5 그대로 / **「흉터 + 볼」**(`CON-140` × `SITE-051` 이름) = **113행 · 묶음 40 · `prefer`**(그 고민 · 하위에 새 행이 없어 `sites[]` = `[]` 그대로) / 새로 묶인 고민 `CON-193` × `SITE-103` 이름 = `filter` 6 / 6행 · 묶음 4 / 같은 고민 × `SITE-110` 이름(밖 부위) = `prefer` 6행. 수가 다르면 SPEC-001 되적기 후보로 보고 |
| (바) | 앱 화면에서 새 얼굴 점 2 고민(저작근 비대증 → 사각턱 · 콧구멍 벌렁거림 → 코)이 찍히는지는 **보기만**(조사 §5-2) | 이 WORK 의 완료 조건이 아니다 — 사용자 e2e 때 |

- 답 키의 **37 명세(`calls/`)는 다시 뽑지 않는다**(입구 · 호출이 안 바뀐다 — `site` 를 건 호출 0 · 조사 §5-3). `set.jsonl` 의 추가 문항 키는 이 대조의 범위 밖이다.
- 전체 batch(3열 채점)는 돌리지 않는다.

**되돌리기**: `_v07a/` 의 네 가지를 제자리에 덮는다(키는 로컬 파일이다).

## 8. 순서 · 의존 · 누가

| SPEC-007 §8-1 | 무엇 | WP | 누가 | 앞선 조건 |
|---|---|---|---|---|
| 1 사본 | `archive/silver-before-data-v07/` | WP-1 ① | 데이터 워커 | — |
| 2 보강 | `concern_site` 8 · `source_ref` 19(스크립트로) | WP-1 | 데이터 워커 | 코디 시작 신호(실제 `silver/` 에 쓸 때) |
| 3 그림 | `silver-image.py` → 103 · 787 | WP-1 | 데이터 워커 | 같음 |
| 4 스키마 · 값 목록 · 문서 · gold-check A1 **· A3** | §3-4 · §4 | WP-1 · WP-2 | 데이터 워커 | — |
| 5 silver-check | G3 밖 FAIL 0 · I1 ~ I5 | WP-1 | 데이터 워커 | — |
| 6 gold | 재빌드 · gold-check · `gold_hash` 같음 | WP-2 | 데이터 워커 | WP-1 |
| 7 허브 스키마 | 계약 상수 · 모델 · revision → `upgrade head` · `check` | WP-3(코드) · WP-4(DB) | backend 워커 | **허브 0.7.2 구현 · 검수 · 커밋 끝** |
| 8 그림 파일 | 에셋 103 · A1 · A3 | WP-3 | backend 워커 | 같음 |
| 9 적재 | dry-run → 적재 | WP-4 | backend 워커 | WP-2 · WP-3 · **로컬 PG 떠 있음(코디)** |
| 10 허브 | 18107 확인(워커) → 18105 재시작 | WP-4 · WP-5 | backend 워커 → **코디** | — |
| 11 대조 | 37 키 (나) · SP 재셈 | WP-5 | **코디** | 백업 폴더는 적재 **앞** |

- WP-1 · WP-2 의 편집과 임시 폴더 출력은 허브 0.7.2 구현과 **나란히** 갈 수 있다(파일이 안 겹친다). 실제 `silver/` 에 쓰는 걸음과 WP-3 부터는 0.7.2 뒤다.
- WP-3 의 합성 시험(§5-2)은 `$SM` 없이 돈다 — WP-1 · WP-2 를 기다리지 않아도 된다. §5-3 의 실물 기대값만 WP-2 뒤다.
- 7 이 9 보다 먼저다(계약에 없는 CSV 는 적재기 V3 이 막는다 — SPEC §8-1).

## 9. 되돌리기(모음)

| 층 | 사본 · 기준 | 되돌린 뒤 확인 |
|---|---|---|
| silver · 스크립트 · 문서 | `$SM/archive/silver-before-data-v07/` | `silver_sha256` = `2471b2f1…fc6918` · CSV 57 · 66,936행 |
| gold | 같은 사본의 `gold/`(바뀌지 않았어야 한다) | `gold_hash` = `8accbb21…f6228c` |
| 허브 코드 · 에셋 | git(미커밋 변경을 치운다 — 꼬리표 붙인 stash 또는 파일별) | `git status --porcelain` 비어 있음 · `alembic heads` = `b202611170001` |
| DB 판 | §6 표 | `health.build.aux_hash` = 옛 값(`6435fe41…1803a3` — SPEC-003 §2-5) · 테이블 241 |
| 답 키 | 앱 `data/eval-set/_v07a/` | `answer_key --diff` 가 37 같음 |

## 10. 완료 조건 · 검증(모음)

| # | 완료 조건 | 누가 | 무엇으로 |
|---|---|---|---|
| 1 | IS1 ~ IS3 — silver 59 · 67,853행 · 바뀐 기존 파일 2 뿐 · silver-check(G3 밖 FAIL 0 · WARN 0) · I1 ~ I5 · `--negative` | 데이터 워커 | §3-5 |
| 2 | IS4 — `gold_hash` 같음 · gold-check(A2 · G1 밖 FAIL 0) · **A1 · A3 통과** · 역검증 둘 · 해시 표 | 데이터 워커 | §4 |
| 3 | IT1 ~ IT7 · `ruff` · 에셋 폴더에 SVG 103 + README 만 | backend 워커 | §5-2 |
| 4 | IE1 ~ IE5 · §5-3 실물 기대값(103 · 92 · 52 · 106 · 200 · 22,940) | backend 워커 | §6 |
| 5 | **IE6 — 37 / 37 행 같음(`build.aux_hash` 만 다름)** · SP 재셈(흉터 + 볼 113행) | **코디** | §7 |
| 6 | 허브 레포에 silver CSV · 시드 CSV · dump · 접속 값 0 · `$SM` · `$I` 가 커밋 후보에 없다 | 워커 → 코디 | 아래 |

```bash
# 허브 워크트리 루트에서 — 커밋 후보 전체
git status --porcelain                                    # §5-1 의 자리 + assets/procedure-images/ 뿐 · *.csv · *.dump · *.db · *.sqlite 0
ls assets/procedure-images/images/mechanism | wc -l       # 54
ls assets/procedure-images/images/method | wc -l          # 49
find assets/procedure-images -type f ! -name '*.svg' ! -name 'README.md'   # 0
git diff HEAD -U0 | grep -n -i -E "postgresql(\+asyncpg)?://[^<]|passw|secret|token|api[_-]?key"   # 자리 표시 밖 0
git diff HEAD -U0 | grep -n -E "/(Users|home)/[a-z]"      # 0
git diff HEAD --stat -- backend/app/main.py backend/app/core .dockerignore .gitignore   # 비어 있다
# 프로필 워크트리에서
git status --porcelain -- orchestration/work/_archive     # 비어 있다($SM 은 무시된다)
```

허브 브랜치의 push · PR · 머지 · stg · 서버 시드는 이 WORK 의 완료 조건이 아니다(SPEC-007 §10-4 끝 줄 · G-12).

## 11. 검수 지적 반영(`review-spec-007.md`)

| # | 지적 | 이 문서에서 | 어디 |
|---|---|---|---|
| **W-1** | 재빌드에 gold-check **A3**(`silver-supplement` 로 `source_ref` 재현) 이 빠졌다 — 손으로 덧붙이면 A3 가 FAIL 하고, 스크립트를 다시 돌리면 덧붙인 행이 지워진다 | **ⓐ 로 닫는다** — 보강 8행 · 근거 19행을 `silver-supplement.py` 의 5번째 단계로 · A1 허용 목록 + A3 재현 대상(4 파일) + 역검증 둘. `concern_site.csv` 도 같은 까닭으로 스크립트가 쓴다(그 파일은 A1 이 「바이트 그대로」 를 보던 54표 가운데 하나다) | §1 · §3-2 · §4 |
| N-1 | `_RESUME.md` 줄 번호 +1 밀림 | 이 문서는 줄 번호 대신 결정 행의 머리 글자로 가리킨다 | 머리말 · links |
| N-2 | U7-1 ~ U7-3 · O7-7 은 닫혔다 | 닫힌 값으로 적었다(O7-7 = 마감 때 gitignore — 코디 몫 · 이 WORK 밖) | 머리말 |
| N-3 | 허브 작업 트리가 깨끗하지 않다 · ⑧ 줄 번호 밀림 | WP-3 전제 = 0.7.2 끝난 HEAD · 수는 grep | §1 · §5 |
| N-4 | gold 는 그림 표를 「읽어 들이지만 쓰지 않는다」 | 그렇게 적고 `gold_hash` 확인을 완료 조건으로 | §4 완료 조건 1 |
| N-5 | 키 접두어 54 / 55종 | `CIM` · `CIL` 겹침 0 은 같다 — WP-1 이 스키마 `id_pattern` 으로 한 번 세어 보고한다 | §3-4 |
| N-6 | 「74표 통과」 가 옛 테이블 수와 같은 숫자 | 「`g_*` · `s_*` 74표」 로 적었다 | §6 IE2 |

## 12. 열린 것 · 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다)

**A — 구현 때 정한다(제안값 · 정한 값을 보고에 적는다)**

| # | 무엇 | 제안 |
|---|---|---|
| A-1 | `silver-image.py` 의 인자 꼴(시드 폴더 · 출력 폴더) · 보강 상수의 이름 · 사본 폴더 이름 `silver-before-data-v07` · 새 시험 파일 `test_medallion_image.py` · 앱 백업 폴더 `_v07a` · 대조 파일 `key-diff-v07-data.md` | 본문 그대로 |
| A-2 | 스키마의 두 표 · 층 ⑤ 를 `schema-edit.py` 에 넣나 | **넣는다** — 그 스크립트가 스키마를 기준 사본에서 통째로 다시 쓴다(§1). 손으로만 고치면 다음 실행 때 사라진다 |
| A-3 | 근거 19행을 `source_ref.csv` 어디에 | **맨 끝**(A1 의 「앞쪽 바이트 불변」 · 기존 덧붙임 순서 보존). `concern_site` 의 옛 574행은 파일 중간에 모여 있지만 순서를 보는 검사는 없다 |
| A-4 | IE1 의 「새 빈 DB」 | 지금 DB 에서 「+2」 왕복 · 빈 DB 는 CI — SPEC-007 §10-3 IE1 되적기 후보 |
| A-5 | SPEC-007 이 넘긴 O7-1(층 ⑤) · O7-2(키) · O7-5(I2 = FAIL) · O7-6(이름) · O7-8(V13 건너뜀) | 전부 SPEC 본문 그대로 |

**B — 코디에게 받을 것 · 알릴 것**

| # | 무엇 | 왜 |
|---|---|---|
| **B-1** | silver-check **G3** · gold-check **G1**(· 따라 걸리는 **A2**)이 이 워크트리에서 데이터와 무관하게 FAIL 이다 — 본문은 「그 셋 밖 FAIL 0」 을 판정으로 삼았다. 두 검사의 git 필터를 지금 경로(`_archive/…`)에 맞게 고쳐 글자 그대로 `PASS` 를 얻을지는 **코디가 정한다** | SPEC-007 §8-1 5 · 6 · IS3 · IS4 가 「PASS」 라고 적었다. 고치면 검사 스크립트의 뜻이 바뀌고(무시되는 폴더라 `git status` 가 산출물을 못 본다) 안 고치면 A2 가 silver-check 의 데이터 FAIL 을 가릴 수 있다 — 그래서 silver-check 를 따로 돌리는 줄을 넣었다 |
| **B-2** | **로컬 PostgreSQL(18432)이 지금 내려가 있다** — WP-4 앞에 띄우기 · 띄운 뒤 옛 판이 남아 있는지(테이블 241 · 빌드 기록 74행) · 접속 값을 워커에 주는 방법 · dump 로 되돌릴 길을 둘지 | 워커는 컨테이너를 다루지 않는다. 18105 가 DB 판으로 떠 있다면 메모리에 올린 판으로 도는 중이라 다시 띄울 때 DB 가 필요하다 |
| B-3 | `concern.csv` 의 설명 문장(`CON-190` · `CON-162` 등이 「자리를 따로 적지 않는다」 꼴)을 새 행에 맞춰 고칠지 | 본문 = **안 고친다**. 고치면 `aux_hash` 가 한 파일 더 바뀌고 `gold_hash` 까지 닿을 수 있어 결정이 필요하다(조사 §7 끝 줄) |
| B-4 | `$SM/silver` 에 실제로 쓰는 시작 신호 · WP-3 시작 신호(0.7.2 커밋 해시) · 18107 을 쓰는 다른 워커와 겹치지 않게 | §2 「시작 문」 · §5 전제 |
| B-5 | (가) 의 기준 키 — 0.7.2 재시작 뒤 37 키를 이미 다시 뽑았는지 | 안 뽑았으면 적재 **앞**에 한 번 뽑아야 대조가 데이터 변화만 본다 |

**이번 판에 하지 않는 것**: 허브 도구 · 정적 서빙 · 바인드 마운트 실행 · 앱 화면(SPEC-007 §9 N7-1 ~ N7-4) · 서버 시드 · 원천 CSV 자리(N7-5) · 영어 라벨(N7-6) · 검수 절차(N7-7) · `site` 사전 보강(조사 「정할 것 5」) · 뒤집힘 4행 · 모공 막힘 · 불독살 · 프로필 `$I` 의 gitignore(O7-7 — 마감 때 코디).

## 13. 대응(미대응 0)

**SPEC-007 절 ↔ WP**

| SPEC-007 | 무엇 | WP | 확인 |
|---|---|---|---|
| §1-2 G-1 ~ G-12 | 정해진 것 | 전부(범위 · 금지) | §2 · §10 · §12 끝 줄 |
| §2-1 S1 ~ S4 | silver 표 공통 · 층 ⑤ · 사전 불변 | WP-1 | IS1 · IS3 |
| §2-2 · §2-3 | `concept_image` · `concept_image_label` | WP-1 §3-3 | IS1 · I1 ~ I4 |
| §2-4 | 시드 칸 → 싣는 것 / 안 싣는 것 | WP-1 §3-3(K4) | IS2 |
| §3 K1 ~ K6 | 시드 → silver 스크립트 | WP-1 §3-3 | IS1 · IS2 |
| §4 | 스키마 · silver-check I1 ~ I5 · 문서 · 값 목록 · 용어집 | WP-1 §3-4 | IS3 |
| §4 끝 줄 | gold-check A1 | WP-2 | IS4 |
| §5 | gold 에 안 넣음 | WP-2(불변 확인) | `gold_hash` |
| §6-1 | 테이블 2 · 셈 | WP-3 | IT1 · IE1 |
| §6-2 | 계약 상수 · 모델 · revision | WP-3 | IT1 · IT2 · IE1 |
| §6-3 | 적재기 · V13 · 박힌 수 · `LOADER_VERSION` | WP-3 | IT3 ~ IT6 · IE2 · IE3 |
| §6-4 | 해시 | WP-2 · WP-4 | §4 해시 표 · IE2 · IE5 |
| §7-1 ~ §7-3 | 에셋 폴더 · 대조 A1 ~ A3 · 규격 | WP-3(A1 · A3 · README) · WP-4(A2 = V13) | IT7 · IE2 |
| §8-1 1 ~ 11 | 재빌드 순서 | §8 표 | — |
| §8-2 | 해시 · 37 키 | WP-2 · WP-5 | §4 · §7 |
| §9 N7-1 ~ N7-7 | 다음 스펙 | **범위 밖** | §12 끝 줄 |
| §10-1 IS1 ~ IS4 | silver 쪽 시험 | WP-1 · WP-2 | §10 #1 · #2 |
| §10-2 IT1 ~ IT7 | 허브 단위 | WP-3 | §10 #3 |
| §10-3 IE1 ~ IE6 | 로컬 실물 | WP-4(1 ~ 5) · WP-5(5 · 6) | §10 #4 · #5 |
| §10-4 | 완료 조건 | §10 | — |
| §11-1 U7-1 ~ U7-3 | 사용자 결정 | 닫힘 — 전부 (a) | 머리말 |
| §11-2 O7-1 ~ O7-8 | 열린 것 | A-5(본문 그대로) · O7-3 · O7-4 는 뒤 · O7-7 은 코디 | §12 |

**보강 조사 ↔ WP**

| research-concern-site | 무엇 | WP | 확인 |
|---|---|---|---|
| §4-1 가운데 `CON-200` · `CON-193` 3행 | 넣음 | WP-1 §3-2(`CSI-0099` ~ `0101`) | IS1 · IE4 |
| §4-1 가운데 `CON-156` 2 · `CON-133` · `CON-269` | 결정이 뺌(정할 것 2 (b)) | **안 넣음** | §3-2 |
| §4-2 가운데 4건 + `CON-176` | 넣음(정할 것 1 · 4) | WP-1 §3-2(`CSI-0102` ~ `0106`) | 같음 |
| §4-2 `CON-122` · §6 정할 것 3 · 5 | 뺌 · 안 넣음 · 보류 | **안 넣음** | §3-2 · §12 끝 줄 |
| §4 머리 「근거 경로 = `source_ref` 에 넣을 값」 | 19행 | WP-1 §3-2 | 완료 조건 2 · A1 · A3 |
| §5-1 거름으로 바뀌는 고민 | 0.7.2 기준으로 다시 — 106 · 200 · 뒤집힘 0 | WP-4 ④ · WP-5 (마) | §5-3 · §7 |
| §5-2 얼굴 점 | 새 점 2 고민 | WP-5 (바) — 보기만 | — |
| §5-3 37 답 키 | 행 불변 · `aux_hash` 만 | WP-5 (가) ~ (라) | IE6 |
| §6 추천 → 7고민 8행 · 95 → 103 | 이번 판 전체 | WP-1 ~ WP-5 | — |
| §7 끝 줄 `concern` 설명 문장 | 본문 = 안 고침 | §12 B-3 | 코디 결정 |

## 변경 기록

### 0.1.0 (2026-11-17)

- 새로 씀 — SPEC-007 0.1.0 의 재빌드 11단계와 보강 조사의 7고민 8행을 WP 다섯(silver · gold · 허브 · DB 재적재 · 키 대조)으로. 누가(데이터 워커 · backend 워커 · 코디) · 시험(그 WP 것만) · 되돌리기(silver · gold 사본 · DB 판 · 답 키)를 WP 마다 적었다.
- 검수 WARN 1(A3) 을 ⓐ 로 닫았다 — 보강을 `silver-supplement.py` 안에 · gold-check A1 + A3 + 역검증.
- 이 워커가 읽어서 본 것(SPEC · 조사에 없던 것 — §12): ① 그 스크립트가 silver 를 기준 사본에서 통째로 다시 써서 `concern_site.csv` 도 스크립트로 써야 한다 ② `schema-edit.py` 가 스키마를 통째로 다시 쓴다 ③ `vocabulary.csv` 의 `n_rows` 가 근거 행 수를 따라 바뀐다 ④ silver-check G3 · gold-check G1 · A2 가 이 워크트리에서 환경 때문에 FAIL 이다 ⑤ 허브 실물 시험에 `concern_site` 95 · 85 · 51 이 박혀 있다 ⑥ 로컬 PostgreSQL 18432 가 지금 닫혀 있다 ⑦ 기준 키는 적재 앞에 0.7.2 코드로 뽑혀 있어야 한다.
- 이 워커 재셈(읽기만 · 표준 라이브러리): 근거 경로 19 / 19 해석됨 · 8 짝 중복 0 · 보강 뒤 `concern_site` 103행 · 고민 92 · 부위 52 · `sites[]` 있는 고민 100 → 106 · `filter` 191 → 200 짝 · silver 67,853행 · 실을 행 130,446 · `gold_hash` 지금 값.
- 돌려 보지 않은 것: silver-check · gold-check · gold-build · silver-supplement(전부 파일을 쓴다) · alembic · 적재기 · pytest · 서버. `$SM` · `$I` · 허브 · 앱은 한 글자도 고치지 않았다. 접속 값 파일 · `.env` 는 열지 않았다.
