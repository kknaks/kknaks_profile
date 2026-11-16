# 지시서 — silver 통합 검사 + ERD · 표 문서

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

Procedure Hub 실버를 ① 사전 → ② 시술 · 케이스 → ③ 관계 순으로 단계마다 만들어 `silver/` 47표에 올렸다. 단계마다 검증 스크립트가 있지만 **그 단계 시점 silver 에 고정**이라 지금은 앞 단계 검사가 FAIL 한다(정상). 다음 단계(상품 → gold) 전에 **지금 silver 47표 전체를 한 번에 검사하는 스크립트**와 **표 구조 문서(ERD · 표 사전)** 를 만든다. silver 는 고치지 않는다 — 걸리는 것은 목록과 추천으로.

## 2. 읽을 것

- `silver/` 47표 전부
- 단계별 검사(기준을 모아 올 곳): `drafts/*/` 의 `*-check.py` 전부 — 특히 최신 `drafts/dict-fill-2/dict-fill-2-check.py` · `drafts/relation-gapfill/gapfill-check.py` · `drafts/relation-merge/merge-check.py` · `drafts/combo-merge/` · `drafts/dict-fill/` · `drafts/site-finalize*/` · `notes/site-finalize-check.py`
- 표 구조 정본: `drafts/relation-pilot/relation-notes.md` §9-2(③ 20표) · `notes/combo-notes.md`(②) · `notes/atoms-notes.md` · `notes/*-notes.md` · `drafts/concern/` · `drafts/effect/` · `drafts/adverse/` · `drafts/condition/` notes(①) · `../combo-pilot-brief.md` §2(② 규칙) · `../_RESUME.md`(결정 표)
- 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 3. 사용자 결정 (11-15 「응」)

**A. 통합 검사 `drafts/silver-check/silver-check.py`** — 47표 전부, 지금 silver 기준. 단계별 검사에서 **지금도 성립해야 하는 기준을 전부** 모은다(어느 단계 검사의 어느 기준인지 notes 표에 — 시점 고정 기준(전/후 셈 · 특정 행 수)은 빼고 이유).
- 형식: UTF-8 BOM · 헤더 · 칸 수 · `;` 0(원장 문장 통째 예외는 단계 검사와 같은 규칙) · id 형식 · id 중복 0.
- 참조: **모든 FK 칸**(표 사이 · `target_table` + `target_code`/`target_id` 다형 참조 — modality · procedure · procedure_case · product · package 등) 존재 · 공통 `alias` · `source_ref` 의 대상 존재 · 고아 행 0(부모 없는 연결 행).
- 사전: 3단(대 · 중 · 소 · 깊이 ≤ 3 · 대분류 아래) · 이름 괄호 0 · name_ko 중복 0 · 사전 행 근거(source_ref) ≥ 1.
- ②: 시술 정체(계열 + 재료 집합 + 주된 원리) 중복 0 · procedure_material ≥ 1 · 케이스 조합 중복 0 · 케이스 site 하나.
- ③: 모든 관계 행 근거 ≥ 1 · `*_text` · text · statement 원장 글자 그대로 · `*_min` · `*_max` 숫자는 같은 행 원문에 있음 · polarity 값 범위 · rating 값이 scale 범위 안.
- source_ref: ref 포인터가 원장에 있음(JSON 포인터 해석 — 단계 검사와 같은 방식).
- 셈 출력(검사 아님, 기록): 표별 행 수 · 입구 현황(relation-notes §4 셈법 — 고민 192/50/18 등).
- 음성 시험: 일부러 깨뜨린 사본으로 FAIL 하는지 확인(silver 원본은 건드리지 않음 — 임시 복사본에서).

**B. ERD · 표 문서**(`notes/silver-erd.md` · `notes/silver-tables.md`):
- `silver-erd.md`: 3층(① 사전 · ② 조합 · ③ 관계)별 mermaid `erDiagram` — 표 · PK · FK · 다형 참조(`target_table`)는 설명 줄로. 층마다 「무엇을 담나」 두세 줄 · 조회 규칙(관계는 아래로 복사 안 함 · 계열 → 시술 → 케이스 물려받기 · 제품은 케이스를 가르지 않음 등 — `_RESUME.md` 결정에 있는 것만).
- `silver-tables.md`: 47표 각각 — 무엇 · 행 수 · 칸(이름 · 뜻 · 값 범위 · FK) · 근거 결정(notes 링크). 칸 뜻은 notes · 결정에 적힌 것만 쓰고, 적힌 데 없으면 「(정의 없음)」으로 두고 목록에.
- 다이어그램과 표 사전의 FK 는 통합 검사가 쓰는 FK 정의 한 벌(`drafts/silver-check/silver-schema.json` 등)에서 뽑는다 — 문서와 검사가 따로 놀지 않게.

**C. 걸린 것**: silver 를 고치지 않는다. FAIL · 경고는 `drafts/silver-check/silver-check-notes.md` 「걸린 것」 표(표 · 행 · 기준 · 원인 · 추천 · 선택지). 단계 결정으로 남겨 둔 것(보류 · 원리 빈 시술 2 · 대상 빈 케이스 등)은 FAIL 이 아니라 「알려진 빈칸」 셈으로. 미룬 작은 것(골수 · method 별칭 띄어쓰기 8 · modality_alias 용도 · 멀티비타민/미네랄 성분 펼치기)이 검사에 걸리면 같은 표에 표시만.

## 4. 쓰기 규칙

- 쓰는 곳: `drafts/silver-check/`(`silver-check.py` · 스키마 정의 · `silver-check-notes.md`) · `notes/silver-erd.md` · `notes/silver-tables.md`. 그 밖 변경 금지 — **silver · notes 의 다른 파일 · 원장 · 커밋 · push 금지.**

## 5. 검증 (코디가 `python3 drafts/silver-check/silver-check.py` 를 다시 돌린다)

- 걸린 것이 없으면 PASS, 있으면 FAIL 과 그 목록이 notes 「걸린 것」 표와 같음.
- 스키마 정의의 표 · 칸 = silver 실제 헤더(47표 · 빠진 칸 0) · ERD/표 사전의 FK = 스키마 정의.
- 단계 검사 기준 모음 표의 모든 기준이 「넣음」 또는 「뺌 — 이유」.
- silver · 원장 바이트 불변(해시) · `git status` 로 산출물 외 변경 없음.

## 6. notes (`drafts/silver-check/silver-check-notes.md`, 짧게)

1. 단계 검사 기준 모음 표 2. 검사 출력 3. 걸린 것(추천 · 선택지) 4. 알려진 빈칸 셈 5. 「(정의 없음)」 칸 목록 6. 음성 시험

## 7. 완료 보고

범위를 넓히지 않는다(silver 수정 · 새 판정 · 외부 조사 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/silver-check/silver-check-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "silver 통합 검사 완료: drafts/silver-check/silver-check-notes.md" --enter`
